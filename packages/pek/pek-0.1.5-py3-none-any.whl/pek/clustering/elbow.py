import time
import warnings
from abc import ABC
from multiprocessing import Process, Queue

import numpy as np
from kneed import KneeLocator
from sklearn.utils._param_validation import (
    Integral,
    Interval,
    InvalidParameterError,
    Real,
    StrOptions,
    validate_params,
)

from ..metrics.comparison import _toComparisonMetricDict
from ..metrics.validation import _toValidationMetricDict
from ..utils.process import (
    ProcessControlMessage,
    ProcessControlMessageType,
    ProcessStatus,
)
from ..utils.random import get_random_state
from .ensemble import ProgressiveEnsembleKMeans
from .results import (
    ElbowPartialResult,
    ElbowPartialResultInfo,
    ElbowPartialResultMetrics,
    MetricGroup,
)


class _AbstractElbow(ABC):
    @validate_params(
        {
            "X": ["array-like", "sparse matrix"],
            "n_clusters_arr": [None, "array-like"],
            "n_runs": [Interval(Integral, 1, None, closed="left")],
            "init": [StrOptions({"k-means++", "random"})],
            "max_iter": [Interval(Integral, 1, None, closed="left")],
            "tol": [Interval(Real, 0, None, closed="left")],
            "random_state": ["random_state"],
            "validationMetrics": [None, str, "array-like"],
            "freq": [None, Interval(Real, 0, None, closed="left")],
        },
        prefer_skip_nested_validation=True,
    )
    def __init__(
        self,
        X,
        n_clusters_arr=None,
        n_runs=4,
        init="k-means++",
        max_iter=300,
        tol=1e-4,
        random_state=None,
        freq=None,
        et=None,  # early terminator (a single element or None),
        labelsValidationMetrics=None,
        partitionsValidationMetrics=None,
        partitionsComparisonMetrics=None,
        taskId=None,
    ):
        self._X = X
        self._n_clusters_arr = n_clusters_arr
        self._n_runs = n_runs
        self._init = init
        self._max_iter = max_iter
        self._tol = tol
        self._random_state = get_random_state(random_state)
        self._et = et
        self._freq = freq
        self._taskId = taskId
        self._metricsCalculator = _ElbowMetricsCalculator(
            X,
            labelsValidationMetrics=labelsValidationMetrics,
            partitionsValidationMetrics=partitionsValidationMetrics,
            partitionsComparisonMetrics=partitionsComparisonMetrics,
        )
        self._etArray = [] if et is None else [et]

        if n_clusters_arr is None:
            self._n_clusters_arr = [2, 3, 4, 5, 6, 7, 8, 9, 10]

        if not all(isinstance(elem, int) for elem in self._n_clusters_arr):
            raise TypeError(f"The 'n_clusters_arr' parameter must contains only integers.")

        if len(self._n_clusters_arr) <= 2:
            raise InvalidParameterError(f"The 'n_clusters_arr' must have length >=2. Got {len(self._n_clusters_arr)}.")

    """def _generateHash(self, params):
        if self._cache:
            _d = Bunch(X=hashlib.md5(self._X).hexdigest())
            for _key, _value in locals().items():
                if _key in ["self", "__class__", "X"]:
                    continue
                if "_cacheHash" in _value:
                    _d[_key] = hashlib.md5(str(_value["_cacheHash"]).encode()).hexdigest()
                else:
                    _d[_key] = hashlib.md5(str(_value).encode()).hexdigest()

            _str = "-".join([_d[_key] for _key in sorted(_d.keys())])
            return hashlib.sha1(_str.encode()).hexdigest()
        return None"""


class ProgressiveEnsembleElbow(_AbstractElbow):
    def __init__(
        self,
        X,
        n_clusters_arr=None,
        n_runs=4,
        init="k-means++",
        max_iter=300,
        tol=1e-4,
        random_state=None,
        et=None,
        freq=None,
        labelsValidationMetrics=None,
        partitionsValidationMetrics=None,
        partitionsComparisonMetrics=None,
        taskId=None,
    ):
        super().__init__(
            X,
            n_clusters_arr=n_clusters_arr,
            n_runs=n_runs,
            init=init,
            max_iter=max_iter,
            tol=tol,
            random_state=random_state,
            et=et,
            freq=freq,
            labelsValidationMetrics=labelsValidationMetrics,
            partitionsValidationMetrics=partitionsValidationMetrics,
            partitionsComparisonMetrics=partitionsComparisonMetrics,
            taskId=taskId,
        )

        self._iteration = -1
        self._completed = False
        self._killed = False

        self._pending = [int(k) for k in self._n_clusters_arr]
        self._results = []
        self._prevResultTimestamp = 0.0

    def _executeNextIteration(self):
        if not self.hasNextIteration():
            raise RuntimeError("No next iteration to execute.")

        k = self._pending.pop(0)

        ensemble = ProgressiveEnsembleKMeans(
            self._X,
            n_clusters=k,
            n_runs=self._n_runs,
            init=self._init,
            max_iter=self._max_iter,
            tol=self._tol,
            random_state=self._random_state,
            ets=self._etArray,
        )

        ensembleLastResult = ensemble.executeAllIterations()

        self._iteration += 1
        self._completed = len(self._pending) == 0
        last = not self.hasNextIteration()

        elbowResultInfo = ElbowPartialResultInfo(
            self._iteration, self._random_state, k, ensembleLastResult.info.inertia, last, self._completed
        )

        # compute the metrics
        # create the partial result (metrics)
        elbowResultMetrics = self._metricsCalculator.getMetrics(ensembleLastResult)

        """dictMetrics = {}  # {"inertia": ensembleLastResult.metrics.validation.inertia}
        for metricName, metricFunction in self._validationMetrics.items():
            if metricName not in dictMetrics:
                dictMetrics[metricName] = metricFunction(self._X, ensembleLastResult.labels)
        elbowResultMetrics = ElbowPartialResultMetrics(**dictMetrics)"""

        # set the elbow value
        elbowResultInfo.elbowPoint = self._computeElbowPoint()

        # create elbow result
        elbowResult = ElbowPartialResult(
            info=elbowResultInfo, metrics=elbowResultMetrics, taskId=self._taskId, labels=ensembleLastResult.labels
        )
        self._results.append(elbowResult)

        # manage results frequency
        currentTimestamp = time.time()
        elapsedFromPrevPartialResult = currentTimestamp - self._prevResultTimestamp
        if (self._freq is not None) and (elapsedFromPrevPartialResult < self._freq):
            time.sleep(self._freq - elapsedFromPrevPartialResult)

        self._prevResultTimestamp = time.time()

        return elbowResult

    def _computeElbowPoint(self):
        """Computes the elbow point using the inertia curve composed of all the past partial results.
        Returns the n_cluster value of the elbow, if exists. Otherwise, returns None."""
        inertiaCurve = np.array([[r.info.n_clusters, r.info.inertia] for r in self._results])
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)

                kneedle = KneeLocator(
                    np.array(inertiaCurve)[:, 0],
                    np.array(inertiaCurve)[:, 1],
                    S=1.0,
                    curve="convex",
                    direction="decreasing",
                )
                return int(kneedle.elbow)
        except:
            return None

    def hasNextIteration(self) -> bool:
        return not self._completed and not self._killed

    def executeNextIteration(self) -> ElbowPartialResult:
        return self._executeNextIteration()

    def executeAllIterations(self) -> ElbowPartialResult:
        r = None
        while self.hasNextIteration():
            r = self.executeNextIteration()
        return r

    def kill(self):
        self._killed = True


class ProgressiveEnsembleElbowProcess(Process):
    def __init__(
        self,
        X,
        n_clusters_arr=None,
        n_runs=4,
        init="k-means++",
        max_iter=300,
        tol=1e-4,
        random_state=None,
        et=None,
        freq=None,
        labelsValidationMetrics=None,
        labelsComparisonMetrics=None,
        labelsProgressionMetrics=None,
        partitionsValidationMetrics=None,
        partitionsComparisonMetrics=None,
        partitionsProgressionMetrics=None,
        taskId=None,
        verbose=False,
        resultsQueue=None,
        **wkargs,
    ):
        super().__init__()

        self._elbow = ProgressiveEnsembleElbow(
            X,
            n_clusters_arr=n_clusters_arr,
            n_runs=n_runs,
            init=init,
            max_iter=max_iter,
            tol=tol,
            random_state=random_state,
            et=et,
            freq=freq,
            labelsValidationMetrics=labelsValidationMetrics,
            partitionsValidationMetrics=partitionsValidationMetrics,
            partitionsComparisonMetrics=partitionsComparisonMetrics,
            taskId=taskId,
        )

        self._verbose = verbose
        self._status = ProcessStatus.PENDING
        self._resultsQueue = resultsQueue
        self._controlsQueue = Queue()

    def _waitForResume(self):
        while True:
            msg = self._controlsQueue.get(block=True)
            if (
                msg.messageType == ProcessControlMessageType.RESUME
                or msg.messageType == ProcessControlMessageType.START
            ):
                self._status = ProcessStatus.RUNNING
                return

    def _readControlMessage(self):
        try:
            msg = self._controlsQueue.get(block=False)

            if msg.messageType == ProcessControlMessageType.PAUSE:
                self._status = ProcessStatus.PAUSED
                self._waitForResume()

            elif msg.messageType == ProcessControlMessageType.KILL:
                self._status = ProcessStatus.KILLED
                self._elbow.kill()
        except:
            pass

    def run(self):
        self._status = ProcessStatus.RUNNING

        while self._elbow.hasNextIteration():
            r = self._elbow.executeNextIteration()
            if self.resultQueue is not None:
                self._resultsQueue.put(r)
            if self._verbose:
                print(r.info)
            if self._elbow.hasNextIteration():
                self._readControlMessage()

        self._status = ProcessStatus.COMPLETED

    @property
    def controlsQueue(self):
        return self._controlsQueue

    @property
    def resultQueue(self):
        return self._resultsQueue

    def pause(self):
        msg = ProcessControlMessage.PAUSE()
        self._controlsQueue.put(msg)

    def resume(self):
        msg = ProcessControlMessage.RESUME()
        self._controlsQueue.put(msg)

    def kill(self):
        msg = ProcessControlMessage.KILL()
        self._controlsQueue.put(msg)


class _ElbowMetricsCalculator:
    def __init__(
        self,
        X,
        labelsValidationMetrics=None,
        partitionsValidationMetrics=None,
        partitionsComparisonMetrics=None,
    ):
        self._X = X
        self._labelsValidationMetrics = _toValidationMetricDict(labelsValidationMetrics)
        self._partitionsValidationMetrics = _toValidationMetricDict(partitionsValidationMetrics)
        self._partitionsComparisonMetrics = _toComparisonMetricDict(partitionsComparisonMetrics)

    def getMetrics(self, ensembleResult):
        return ElbowPartialResultMetrics(
            labelsValidationMetrics=self._compute_labelsValidationMetrics(ensembleResult),
            partitionsValidationMetrics=self._compute_partitionsValidationMetrics(ensembleResult),
            partitionsComparisonMetrics=self._compute_partitionsComparisonMetrics(ensembleResult),
        )

    def _compute_labelsValidationMetrics(self, ensembleResult):
        """Labels validation metrics are computed only on the current best labels."""
        res = {"inertia": ensembleResult.metrics.labelsValidationMetrics.inertia}
        for metricName, metricFunction in self._labelsValidationMetrics.items():
            if metricName not in res:
                res[metricName] = metricFunction(self._X, ensembleResult.labels)

        return MetricGroup(**res)

    def _compute_partitionsValidationMetrics(self, ensembleResult):
        """Partitions validation metrics are computed on each partition.
        The result is a dictionary where each metric has an array of values, one for each partition.
        """
        res = {"inertia": ensembleResult.metrics.partitionsValidationMetrics.inertia}
        for metricName, metricFunction in self._partitionsValidationMetrics.items():
            if metricName not in res:
                res[metricName] = np.empty(ensembleResult.partitions.shape[0], dtype=float)
                for i in range(ensembleResult.partitions.shape[0]):
                    res[metricName][i] = metricFunction(self._X, ensembleResult.partitions[i, :])

        return MetricGroup(**res)

    def _compute_partitionsComparisonMetrics(self, ensembleResult):
        """
        Partitions comparison metrics are computed on each pair of partition.
        The result is a dictionary where each metric has a symmetric matrix RxR.
        """
        n_runs = ensembleResult.partitions.shape[0]
        res = {}
        for metricName, metricFunction in self._partitionsComparisonMetrics.items():
            if metricName not in res:
                res[metricName] = np.full((n_runs, n_runs), np.nan, dtype=float)

                for i in range(n_runs):
                    for j in range(n_runs):
                        if j >= i:
                            continue
                        val = metricFunction(ensembleResult.partitions[i, :], ensembleResult.partitions[j, :])
                        res[metricName][i, j] = val
                        res[metricName][j, i] = val

        return MetricGroup(**res)
