from typing import List
from mediagrabber.meter.meter import MeterInterface, Metric
from unittest import mock
from unittest.mock import MagicMock


class TestMeter(MeterInterface):
    metrics: List = []

    def write_metric(self, metric: Metric) -> None:
        self.metrics.append(metric.__dict__)


test_measure_parameters: List = []
def test_measure():
    meter: TestMeter = TestMeter()

    # Duration of this callback execution should be measured
    # This callback should be called from meter with correct parameter x
    def external_function(parameter: str):
        global test_measure_parameters
        test_measure_parameters.append(parameter)

    x = 'ParameterX'

    def closure():
        return external_function(x)

    meter.measure('test_measurement', closure, {}, {})

    assert test_measure_parameters == ['ParameterX']
    assert meter.metrics == []
