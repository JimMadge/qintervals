#  This file is part of qintervals.
#
#  Copyright 2018 Jim Madge <jmmadge@gmail.com>
#
#  qintervals is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
from enum import Enum, auto

# Interval class
class Interval(object):
    def __init__(self, interval_type, text, length):
        if interval_type in IntervalType:
            self.interval_type = interval_type
        else:
            raise IntervalTypeError('Invalid interval type provided {}'.format(interval_type))

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
            raise TimeUnitError('Length of interval must be given in minutes(m) or seconds(s). Given unit was {}'.format(time_unit))

# Interval type enum
class IntervalType(Enum):
    WORK = auto()
    REST = auto()
    WARMUP = auto()
    WARMDOWN = auto()

# Incorrect time unit exception
class TimeUnitError(Exception):
    pass

# Invalid interval type exception
class IntervalTypeError(Exception):
    pass
