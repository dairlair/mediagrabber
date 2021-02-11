from mediagrabber.meter.meter import MeterInterface, Metric
from influxdb import InfluxDBClient
from typing import List


class InfluxDBMeter(MeterInterface):
    client: InfluxDBClient
    metrics: List = []
    batch_size: int = 5000

    def __init__(self, dsn: str) -> None:
        self.client = InfluxDBClient.from_dsn(dsn)
        version = self.client.ping()
        print(f"InfluxDB server version: {version}")

    def write_metric(self, metric: Metric) -> None:
        print(metric.__dict__)
        self.metrics.append(metric.__dict__)
        if (len(self.metrics) >= self.batch_size):
            self.flush()

    def flush(self) -> None:
        count: int = len(self.metrics)
        print(f'Metrics count: {count}')
        self.client.write_points(self.metrics)
        self.metrics = []

    def __del__(self):
        print("Destructor called, metrics flushed")
        self.flush()
