import context
import pytest
from qintervals.interval import Interval, IntervalType, TimeUnitError

def test_time_unit_error():
    with pytest.raises(TimeUnitError):
        interval = Interval(IntervalType.WORK, 'test', '100f')
