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
from .interval import Interval, IntervalType
from time import time
import yaml

# Work out class
class Workout(object):
    def __init__(self, yaml_file=None):
        self.intervals = []
        self.cum_times = [0]
        self.total_time = 0
        self.current_interval = 0
        self.time_paused = 0
        self.state = WorkoutState.stopped

        if yaml_file:
            self.from_yaml(yaml_file)

    # Parse a yaml file to read a workout
    def from_yaml(self, yaml_file):
        # Parse yaml file as a dictionary
        with open(yaml_file, 'rb') as stream:
            try:
                yaml_dict = yaml.load(stream)
            except yaml.YAMLError:
                raise WorkoutFileError('Invalid YAML in workout file: {}'.format(yaml_file))

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
                raise MissingKeyError('Block in workout file missing key: "repeats"\n\t{}'.format(entry))

            # Unpack intervals or blocks inside this entry recursively
            try:
                sub_entries = block['intervals']
            except KeyError:
                raise MissingKeyError('Block in workout file missing key: "intervals"\n\t{}'.format(entry))

            for sub_entry in block['intervals']:
                intervals += self._unpack(sub_entry)

            # Return the correct number of repetitions
            return intervals*repeats
        else:
            # Return single interval
            try:
                return [Interval(_interval_type[entry['type']], entry['name'], entry['length'])]
            except KeyError:
                raise MissingKeyError('Interval in workout file missing a key\n\t{}'.format(entry))

    # Add an interval to the end of the list
    def add_interval(self, interval):
        self.intervals.append(interval)
        self.cum_times.append(self.cum_times[-1] + interval.length)
        self.total_time += interval.length

    # Start the workout timer
    def start(self):
        if self.state == WorkoutState.paused:
            self.state = WorkoutState.running
            self.time_paused += time() - self.paused_at
        elif self.state == WorkoutState.stopped:
            self.state = WorkoutState.running
            self.start_time = time()

    # Pause the workout timer
    def pause(self):
        self.state = WorkoutState.paused
        self.paused_at = time()

    # Stop the timer, return to the beginning
    def stop(self):
        self.state = WorkoutState.stopped
        self.current_interval = 0
        self.time_paused = 0

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

# Workout state enum
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
_interval_type = {'work': IntervalType.work, 'rest': IntervalType.rest, 'warmup': IntervalType.warmup, 'warmdown': IntervalType.warmdown}
