import context
import pytest
from qintervals.interval import Interval, IntervalType, TimeUnitError, IntervalTypeError

def test_time_unit_error():
    with pytest.raises(TimeUnitError):
        interval = Interval(IntervalType.WORK, 'test', '100f')

def test_invalid_interval_type_error():
    with pytest.raises(IntervalTypeError):
        interval = Interval(70.5, 'test', '100s')

def test_invalid_text():
    with pytest.raises(TypeError):
        interval = Interval(IntervalType.WORK, 54, '100s')

def test_time_unit_conversion():
    interval = Interval(IntervalType.WORK, 'test', '1m')
    interval2 = Interval(IntervalType.WORK, 'test', '60s')
    assert interval.length == interval2.length == 60
