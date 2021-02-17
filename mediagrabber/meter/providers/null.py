from mediagrabber.meter.meter import MeterInterface, Metric


class NullMeter(MeterInterface):
    def write_metric(self, metric: Metric) -> None:
        pass
