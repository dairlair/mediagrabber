from abc import abstractmethod
from mediagrabber.meter.meter import MeterInterface, Metric


class StdoutMeter(MeterInterface):
    def __init__(self) -> None:
        print('init')

    def write_metric(self, metric: Metric) -> None:
        print(metric.__dict__)

    def __del__(self):
        print("Destructor called, metrics flushed")
        print(self)
