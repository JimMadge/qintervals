from enum import Enum, auto
from pytest import raises
from qintervals.interval import (Interval, IntervalType, TimeUnitError,
                                 IntervalTypeError)


def test_time_unit_error():
    with raises(TimeUnitError):
        Interval(IntervalType.work, 'test', '100f')


def test_invalid_interval_type_error():
    class InvalidIntervalType(Enum):
        test = auto()

    with raises(IntervalTypeError):
        Interval(InvalidIntervalType.test, 'test', '100s')


def test_invalid_text():
    with raises(TypeError):
        Interval(IntervalType.work, 54, '100s')


def test_time_unit_conversion():
    interval = Interval(IntervalType.work, 'test', '1m')
    interval2 = Interval(IntervalType.work, 'test', '60s')
    assert interval.length == interval2.length == 60
