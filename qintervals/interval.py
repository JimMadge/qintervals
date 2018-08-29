from enum import Enum, auto
from time import time
import yaml

# Work out class
class Workout(object):
    def __init__(self):
        self.intervals = []
        self.cum_times = [0]
        self.total_time = 0
        self.current_interval = 0
        self.paused = False
        self.time_paused = 0

    # Parse a yaml file to read a workout
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

    # Set the workout name
    def set_name(self,name):
        self.name = name

    # Add an interval to the end of the list
    def add_interval(self, interval):
        self.intervals.append(interval)
        self.cum_times.append(self.cum_times[-1] + interval.length)
        self.total_time += interval.length

    # Start the workout timer
    def start(self):
        if self.paused:
            self.paused = False
            self.time_paused += time() - self.paused_at
        else:
            self.start_time = time()

    # Pause the workout timer
    def pause(self):
        if self.paused:
            return
        else:
            self.paused = True
            self.paused_at = time()

    # Start the workout time if paused, pause the workout timer if not paused
    def start_pause(self):
        if self.paused:
            self.start()
        else:
            self.pause()

    # Determine the elapsed workout time (not including time paused)
    def elapsed(self):
        if self.paused:
            return self.paused_at - self.start_time - self.time_paused
        else:
            return time() - self.start_time - self.time_paused

    # Determine the total time elapsed and remaining, current interval time elapsed and remaining,
    # the current interval and whether the interval has changed since the last call
    def progress(self):
        elapsed = self.elapsed()
        remaining = self.total_time - elapsed

        # Determine current interval
        changed_interval = self.update_current_interval(elapsed)
        interval = self.intervals[self.current_interval]

        interval_elapsed = elapsed - self.cum_times[self.current_interval]
        interval_remaining = interval.length - interval_elapsed

        return elapsed, remaining, interval_elapsed, interval_remaining, interval, changed_interval

    # List upcoming intervals
    def upcoming(self):
        elapsed = self.elapsed()
        self.update_current_interval(elapsed)
        return  self.intervals[self.current_interval+1:]

    # Determine current interval, returns a boolean indicating whether the interval has changed since
    # the last call
    def update_current_interval(self,elapsed):
        old_interval = self.current_interval
        for i,time in enumerate(self.cum_times):
            if elapsed < time:
                self.current_interval = i-1
                break
        if self.current_interval == old_interval:
            return False
        else:
            return True

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
