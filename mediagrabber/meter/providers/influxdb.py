from mediagrabber.meter.meter import MeterInterface, Metric
from influxdb import InfluxDBClient
from typing import List


class InfluxDBMeter(MeterInterface):
    client: InfluxDBClient
    metrics: List = []
    batch_size: int = 10

    def __init__(self, dsn: str, batch_size: int = 10) -> None:
        self.client = InfluxDBClient.from_dsn(dsn)
        version = self.client.ping()
        print(f"InfluxDB server version: {version}")
        self.batch_size = batch_size

    def write_metric(self, metric: Metric) -> None:
        self.metrics.append(metric.__dict__)
        if (len(self.metrics) >= self.batch_size):
            self.flush()

    def flush(self) -> None:
        self.client.write_points(self.metrics)
        self.metrics = []

    def __del__(self):
        self.flush()
