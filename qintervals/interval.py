from enum import Enum, auto
from time import time
import yaml

# Work out class
class Workout(object):
    def __init__(self):
        self.intervals = []
        self.cum_times = [0]
        self.total_time = 0

    def from_yaml(self, yaml_file):
        # Parse yaml file as a dictionary
        with open(yaml_file, 'r') as stream:
            try:
                yaml_dict = yaml.load(stream)
            except yaml.YAMLError as exc:
                raise Exception('Error in yaml file')

        # Read workout definition from dictionary
        self.set_name(yaml_dict['title'])
        for interval in yaml_dict['intervals']:
            self.add_interval(Interval(interval['type'], interval['name'], interval['length']))

    def set_name(self,name):
        self.name = name

    def add_interval(self, interval):
        self.intervals.append(interval)
        self.cum_times.append(self.cum_times[-1] + interval.length)
        self.total_time += interval.length

    def start(self):
        self.start_time = time()

    def progress(self):
        elapsed = time() - self.start_time
        remaining = self.total_time - elapsed

        # Determine current interval
        for i in range(len(self.intervals)):
            if elapsed > self.cum_times[i]:
                current = i
        interval = self.intervals[current]

        interval_elapsed = elapsed - self.cum_times[current]
        interval_remaining = interval.length - interval_elapsed

        return elapsed, remaining, interval_elapsed, interval_remaining, interval

    def upcoming(self):
        elapsed = time() - self.start_time
        for i in range(len(self.intervals)):
            if elapsed > self.cum_times[i]:
                current = i
        return  self.intervals[current+1:]

# Interval class
class Interval(object):
    def __init__(self, interval_type, text, length):
        self.interval_type = interval_type
        self.text = text

        # Ensure time unit is minutes or seconds
        time_unit = length[-1]
        try:
            assert time_unit in ['s','m']
        except AssertionError:
            raise AssertionError('Length of interval must be given in minutes(m) or seconds(s). Given unit was {}'.format(time_unit))

        # Convert time to seconds
        if time_unit == 's':
            self.length = float(length[:-1])
        elif time_unit == 'm':
            self.length = float(length[:-1]) * 60.0

# Interval type enum
class IntervalType(Enum):
    WORK = auto()
    REST = auto()
    WARMUP = auto()
    WARMDOWN = auto()
