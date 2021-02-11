from abc import ABC, abstractmethod
import time as times


class Metric:
    measurement: str
    tags: dict = {}
    fields: dict = {}
    # Metric timestamp in nanoseconds
    time: str = None

    def __init__(self, measurement: str, tags: dict = {}, fields: dict = {}, time: str = None) -> None:
        self.measurement = measurement
        self.tags = tags
        self.fields = fields
        self.time = time if time else int(times.time() * 1000000000)


class MeterInterface(ABC):
    @abstractmethod
    def write_metric(self, metric: Metric) -> None:
        raise NotImplementedError
