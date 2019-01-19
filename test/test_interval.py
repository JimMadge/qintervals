import context
import pytest
from qintervals.interval import Interval, IntervalType, TimeUnitError, IntervalTypeError

def test_time_unit_error():
    with pytest.raises(TimeUnitError):
        interval = Interval(IntervalType.WORK, 'test', '100f')

def test_invalid_interval_type_error():
    with pytest.raises(IntervalTypeError):
        interval = Interval(70.5, 'test', '100s')

