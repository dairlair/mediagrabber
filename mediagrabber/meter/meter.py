from abc import ABC, abstractmethod
from time import time_ns
from typing import Callable


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

    def measure(self, measurement: str, fn: Callable, tags: dict = {}, fields: dict = {}):
        """ Measures duration of specified function execution
        and pushes the collected duration to the TSDB

        Args:
            measurement (str): Measurement which should be pushed to the TSDB.
            fn (Callable): The function which should be measured.
            tags (dict, optional): [The tags, which should be published]. Defaults to {}.
            fields (dict, optional): [The additional fields, which should be published]. Defaults to {}.

        Returns:
            any: Returns the same value which is returned by `fn`.
        """
        start = time_ns()
        result = fn()
        finish = time_ns()
        fields['duration'] = finish - start

        metric = Metric(measurement, tags, fields, finish)
        self.write_metric(metric)

        return result
