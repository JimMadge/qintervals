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
from .interval import Interval
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
        self.state = WorkoutState.STOPPED

        if yaml_file:
            self.from_yaml(yaml_file)

    # Parse a yaml file to read a workout
    def from_yaml(self, yaml_file):
        # Parse yaml file as a dictionary
        with open(yaml_file, 'r') as stream:
            try:
                yaml_dict = yaml.load(stream)
            except yaml.YAMLError as exc:
                raise yaml.YAMLError('Error in YAML file: {}'.format(yaml_file))

        # Read workout definition from dictionary
        self.set_name(yaml_dict['title'])
        for interval_or_block in yaml_dict['workout']:
            # Ensure entry is an interval or a block
            try:
                assert any([key in interval_or_block for key in ['interval','block']])
            except AssertionError:
                raise AssertionError('Key in workout list must be "interval" or "block".')

            # Add repeats of block to the interval list
            if 'block' in interval_or_block:
                block = interval_or_block
                repeat = block['repeat']
                intervals = []
                for interval in block['intervals']:
                    intervals.append(Interval(interval['type'], interval['name'], interval['length']))
                self.add_block(repeat, intervals)
            # Add single interval to the interval list
            elif 'interval' in interval_or_block:
                interval = interval_or_block
                self.add_interval(Interval(interval['type'], interval['name'], interval['length']))

    # Set the workout name
    def set_name(self,name):
        self.name = name

    # Add a block of intervals to the end of the list
    def add_block(self, repeat, intervals):
        for i in range(repeat):
            for interval in intervals:
                self.add_interval(interval)

    # Add an interval to the end of the list
    def add_interval(self, interval):
        self.intervals.append(interval)
        self.cum_times.append(self.cum_times[-1] + interval.length)
        self.total_time += interval.length

    # Start the workout timer
    def start(self):
        if self.state == WorkoutState.PAUSED:
            self.state = WorkoutState.RUNNING
            self.time_paused += time() - self.paused_at
        elif self.state == WorkoutState.STOPPED:
            self.state = WorkoutState.RUNNING
            self.start_time = time()

    # Pause the workout timer
    def pause(self):
        self.state = WorkoutState.PAUSED
        self.paused_at = time()

    # Stop the timer, return to the beginning
    def stop(self):
        self.state = WorkoutState.STOPPED
        self.current_interval = 0
        self.time_paused = 0

    # Start the workout time if paused, pause the workout timer if not paused
    def start_pause(self):
        if self.state in [WorkoutState.PAUSED, WorkoutState.STOPPED]:
            self.start()
        else:
            self.pause()

    # Determine the elapsed workout time (not including time paused)
    def elapsed(self):
        if self.state == WorkoutState.PAUSED:
            return self.paused_at - self.start_time - self.time_paused
        elif self.state == WorkoutState.STOPPED:
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
    RUNNING = auto()
    PAUSED = auto()
    STOPPED = auto()
