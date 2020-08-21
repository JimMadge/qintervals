from enum import Enum, auto


# Interval class
class Interval(object):
    def __init__(self, interval_type, text, length):
        if interval_type in IntervalType:
            self.interval_type = interval_type
        else:
            raise IntervalTypeError(
                'Invalid interval type provided {}'.format(interval_type))

        if isinstance(text, str):
            self.text = text
        else:
            raise TypeError('Arugment "text" must be a str')

        # Ensure time unit is minutes or seconds
        time_unit = length[-1]

        # Convert time to seconds
        if time_unit == 's':
            self.length = float(length[:-1])
        elif time_unit == 'm':
            self.length = float(length[:-1]) * 60.0
        else:
            raise TimeUnitError(
                'Length of interval must be given in minutes(m)' +
                ' or seconds(s). Given unit was {}'.format(time_unit))


# Interval type enum
class IntervalType(Enum):
    work = auto()
    rest = auto()
    warmup = auto()
    warmdown = auto()


# Incorrect time unit exception
class TimeUnitError(Exception):
    pass


# Invalid interval type exception
class IntervalTypeError(Exception):
    pass
