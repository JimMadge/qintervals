from enum import Enum, auto

# Work out class
class Workout(object):
    def __init__(self, name):
        self.name = name
        self.intervals = []
        self.cum_times = [0]
        self.total_time = 0

    def add_interval(self, interval):
        self.intervals.append(interval)
        self.cum_times.append(self.cum_times[-1] + interval.length)
        self.total_time += interval.length

    def start(self, time):
        self.start_time = time

    def progress(self, time):
        elapsed = time - self.start_time
        remaining = self.total_time - elapsed

        # Determine current interval
        for i in range(len(self.intervals)):
            if elapsed > self.cum_times[i]:
                current = i
        interval = self.intervals[current]

        interval_elapsed = elapsed - self.cum_times[current]
        interval_remaining = interval.length - interval_elapsed

        return elapsed, remaining, interval_elapsed, interval_remaining, interval

    def upcoming(self, time):
        elapsed = time - self.start_time
        for i in range(len(self.intervals)):
            if elapsed > self.cum_times[i]:
                current = i
        return  self.intervals[current+1:]

# Interval class
class Interval(object):
    def __init__(self, interval_type, text, length):
        self.interval_type = interval_type
        self.text = text
        self.length = length

# Interval type enum
class IntervalType(Enum):
    WORK = auto()
    REST = auto()
    WARMUP = auto()
    WARMDOWN = auto()
