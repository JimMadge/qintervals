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
from collections import namedtuple
from copy import copy
from enum import Enum, auto
from .interval import Interval, IntervalType
from time import time
import yaml

# Container for interval starting and ending times
_Timing = namedtuple('Timing', ['starts_at', 'ends_at'])
# Container for returning workout progress information
_Progress = namedtuple('Progress', ['elapsed', 'remaining', 'interval_elapsed',
                                    'interval_remaining', 'interval',
                                    'changed_interval'])


# A collection of intervals and methods for timing a workout
class Workout(object):
    def __init__(self, yaml_file=None):
        self.intervals = []
        self.timings = {}
        self.total_time = 0
        self.time_paused = 0
        self.state = WorkoutState.stopped

        # Marker for last known interval, used for determining when the
        # current interval has changed
        self._last_interval = None

        if yaml_file:
            self.from_yaml(yaml_file)
            # Initialise last interval
            self._last_interval = self.intervals[0]

    # Parse a yaml file to read a workout
    def from_yaml(self, yaml_file):
        # Parse yaml file as a dictionary
        with open(yaml_file, 'rb') as stream:
            try:
                yaml_dict = yaml.load(stream)
            except yaml.YAMLError:
                raise WorkoutFileError(
                    'Invalid YAML in workout file: {}'.format(yaml_file))

        # Read workout title
        try:
            self.name = yaml_dict['title']
        except KeyError:
            raise MissingKeyError('Workout file missing key: "title"')

        # Read intervals and blocks
        try:
            entries = yaml_dict['intervals']
        except KeyError:
            raise MissingKeyError('Workout file missing key: "intervals"')

        # Unpack blocks or intervals and add them to the workout
        for entry in entries:
            for interval in self._unpack(entry):
                self.add_interval(interval)

    # Unpack a single interval or block into a list of interval objects
    def _unpack(self, entry):
        # Determine whether argument is a single interval or a block
        if 'block' in entry.keys():
            intervals = []
            block = entry['block']
            try:
                repeats = block['repeats']
                assert isinstance(repeats, int)
            except KeyError:
                raise MissingKeyError(
                    'Block in workout file missing key:' +
                    ' "repeats"\n\t{}'.format(entry))

            # Unpack intervals or blocks inside this entry recursively
            try:
                sub_entries = block['intervals']
            except KeyError:
                raise MissingKeyError(
                    'Block in workout file missing key:' +
                    ' "intervals"\n\t{}'.format(entry))

            for sub_entry in sub_entries:
                intervals += self._unpack(sub_entry)

            # Return the correct number of repetitions
            return [copy(interval) for interval in intervals*repeats]
        else:
            # Return single interval
            try:
                return [
                    Interval(_interval_type[entry['type']],
                             entry['name'], entry['length'])
                    ]
            except KeyError:
                raise MissingKeyError(
                    'Interval in workout file missing a key' +
                    '\n\t{}'.format(entry))

    # Add an interval to the end of the list and update timings
    def add_interval(self, interval):
        self.intervals.append(interval)
        self.timings[interval] = _Timing(
            starts_at=self.total_time,
            ends_at=self.total_time+interval.length)
        self.total_time += interval.length

    # Start the workout timer
    def start(self):
        if self.state == WorkoutState.paused:
            self.state = WorkoutState.running
            self.time_paused += time() - self.paused_at
        elif self.state == WorkoutState.stopped:
            self.state = WorkoutState.running
            self.start_time = time()
            self._last_interval = self.intervals[0]

    # Pause the workout timer
    def pause(self):
        self.state = WorkoutState.paused
        self.paused_at = time()

    # Stop the timer, return to the beginning
    def stop(self):
        self.state = WorkoutState.stopped
        self.time_paused = 0
        self._last_interval = self.intervals[0]

    # Start the workout time if paused, pause the workout timer if not paused
    def start_pause(self):
        if self.state in [WorkoutState.paused, WorkoutState.stopped]:
            self.start()
        else:
            self.pause()

    # Determine the elapsed workout time (not including time paused)
    def elapsed(self):
        if self.state == WorkoutState.paused:
            return self.paused_at - self.start_time - self.time_paused
        elif self.state == WorkoutState.stopped:
            return 0.0
        else:
            return time() - self.start_time - self.time_paused

    # Determine the current interval
    def current_interval(self):
        # If the workout is stopped return the first interval
        if self.state == WorkoutState.stopped:
            return self.intervals[0]

        # Otherwise determine the current interval
        elapsed = self.elapsed()
        for interval in self.intervals:
            starts_at = self.timings[interval].starts_at
            ends_at = self.timings[interval].ends_at
            if elapsed >= starts_at:
                if elapsed < ends_at:
                    return interval

    # Return a summary of the progress of the workout
    # Returned values are the total time elapsed and remaining,
    # current interval time elapsed and remaining, the current interval
    # and whether the interval has changed since the last call
    def progress(self):
        elapsed = self.elapsed()
        # Check for the end of the workout
        if elapsed >= self.total_time:
            self.stop()
            return _Progress(
                elapsed=0, remaining=self.total_time,
                interval_elapsed=0,
                interval_remaining=self.intervals[0].length,
                interval=self.intervals[0], changed_interval=True)

        remaining = self.total_time - elapsed

        interval = self.current_interval()

        changed_interval = interval is not self._last_interval
        if changed_interval:
            self._last_interval = interval

        interval_elapsed = elapsed - self.timings[interval].starts_at
        interval_remaining = interval.length - interval_elapsed

        return _Progress(
            elapsed=elapsed, remaining=remaining,
            interval_elapsed=interval_elapsed,
            interval_remaining=interval_remaining,
            interval=interval, changed_interval=changed_interval)

    # List upcoming intervals
    def upcoming(self):
        index = self.intervals.index(self.current_interval())
        return self.intervals[index+1:]


# Workout states
class WorkoutState(Enum):
    running = auto()
    paused = auto()
    stopped = auto()


# YAML workout file format error
class WorkoutFileError(Exception):
    pass


# Missing key in YAML file error
class MissingKeyError(Exception):
    pass


# Interval type translation dictionary
_interval_type = {
    'work': IntervalType.work,
    'rest': IntervalType.rest,
    'warmup': IntervalType.warmup,
    'warmdown': IntervalType.warmdown}
