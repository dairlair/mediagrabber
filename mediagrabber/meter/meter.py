from abc import ABC, abstractmethod
from time import time_ns
from typing import Callable, Tuple, Union


class Metric:
    measurement: str
    tags: dict = {}
    fields: dict = {}
    # Metric timestamp in nanoseconds
    time: int = None

    def __init__(self, measurement: str, tags: dict = {}, fields: dict = {}, time: int = None) -> None:
        self.measurement = measurement
        self.tags = tags
        self.fields = fields
        self.time = time if time else time_ns()


class MeterInterface(ABC):
    @abstractmethod
    def write_metric(self, metric: Metric) -> None:
        raise NotImplementedError

    def calculate_metric(self, measurement: str, fn: Callable) -> Tuple[Metric, any]:
        """Runs specified function and creates metric, which
        contains functiot execution duration (nanonoseconds).

        Args:
            measurement (str): Measurement which should be specified in the Metric.
            fn (Callable): The function which should be measured.

        Returns:
            Tuple[Metric, any]: Tuple, with created metric and returned value from `fn` function.
        """
        start = time_ns()
        result = fn()
        finish = time_ns()
        fields = {"duration": finish - start}

        return Metric(measurement, {}, fields, finish), result

    def measure(
        self,
        measurement: str,
        fn: Callable,
        tags: Union[dict, callable] = {},
        fields: Union[dict, callable] = {},
    ) -> any:
        """Measures duration of specified function execution
        and pushes the collected duration to the TSDB

        Args:
            measurement (str): Measurement which should be pushed to the TSDB.
            fn (Callable): The function which should be measured.
            tags (Union[dict, callable], optional): [The tags, which should be published]. Defaults to {}.
              If the `tags` argument is callable - this function will be called with result of called `fn` function
              and returned dict will be used.
            fields (Union[dict, callable], optional): [The additional fields, which should be published]. Defaults to {}.
              If the `fields` argument is callable - this function will be called with result of called `fn` function
              and returned dict will be used.

        Returns:
            any: Returns the same value which is returned by `fn`.
        """

        (metric, result) = self.calculate_metric(measurement, fn)
        if callable(tags):
            tags = tags(result)

        if callable(fields):
            fields = fields(result)

        metric.tags = {**metric.tags, **tags}
        metric.fields = {**metric.fields, **fields}

        self.write_metric(metric)

        return result
