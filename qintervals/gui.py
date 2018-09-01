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
from .interval import Workout, WorkoutState
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from os import path
import sys
import argparse

_WIDTH = 500
_HEIGHT = 500

class Ui(QtWidgets.QWidget):
    def __init__(self, workout):
        super().__init__()
        self.init_fonts()
        self.init_ui(workout)

    # Initialise QFonts
    def init_fonts(self):
        # Default font
        self.font_default = QtGui.QFont()
        self.font_default.setPointSize(14)
        self.font_default.setWeight(QtGui.QFont.Normal)
        self.setFont(self.font_default)

        # Workout name font
        self.font_workout_name = QtGui.QFont()
        self.font_workout_name.setPointSize(20)
        self.font_workout_name.setWeight(QtGui.QFont.Bold)

        # Interval name font
        self.font_interval_name = QtGui.QFont()
        self.font_interval_name.setPointSize(16)
        self.font_interval_name.setWeight(QtGui.QFont.Bold)

        # Time digits font
        self.font_time = QtGui.QFont()
        self.font_time.setPointSize(14)
        self.font_time.setStyleHint(QtGui.QFont.Monospace)

        # Upcoming intervals header font
        self.font_upcoming_header = self.font_interval_name

    # Initialise the ui
    def init_ui(self,workout):
        self.workout = workout

        # Size the widget
        self.resize(_WIDTH, _HEIGHT)

        self.setWindowTitle("qintervals")

        # Main grid layout
        self.grid_widget = QtWidgets.QWidget(self)
        self.grid_widget.setGeometry(QtCore.QRect(50, 50, 400, 400))
        self.grid_layout = QtWidgets.QGridLayout(self.grid_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        # Workout name
        self.label_workout_name = QtWidgets.QLabel(self.grid_widget)
        self.label_workout_name.setFont(self.font_workout_name)
        self.label_workout_name.setText(self.workout.name)
        self.grid_layout.addWidget(self.label_workout_name, 0, 0, 1, -1, QtCore.Qt.AlignCenter)

        # Interval name
        self.label_interval_name = QtWidgets.QLabel(self.grid_widget)
        self.label_interval_name.setFont(self.font_interval_name)
        self.label_interval_name.setText(self.workout.intervals[0].text)
        self.grid_layout.addWidget(self.label_interval_name, 1, 0, 1, 2, QtCore.Qt.AlignCenter)

        # Interval remaining label
        self.label_interval_remaining = QtWidgets.QLabel(self.grid_widget)
        self.label_interval_remaining.setText("Interval Remaining")
        self.grid_layout.addWidget(self.label_interval_remaining, 2, 0, QtCore.Qt.AlignCenter)
        # Interval remaining time
        self.label_interval_remaining_time = QtWidgets.QLabel(self.grid_widget)
        self.label_interval_remaining_time.setFont(self.font_time)
        self.label_interval_remaining_time.setText(self.time_str(0))
        self.grid_layout.addWidget(self.label_interval_remaining_time, 2, 1, QtCore.Qt.AlignCenter)

        # Total remaining label
        self.label_total_remaining = QtWidgets.QLabel(self.grid_widget)
        self.label_total_remaining.setText("Total Remaining")
        self.grid_layout.addWidget(self.label_total_remaining, 3, 0, QtCore.Qt.AlignCenter)
        # Total remaining time
        self.label_total_remaining_time = QtWidgets.QLabel(self.grid_widget)
        self.label_total_remaining_time.setFont(self.font_time)
        self.label_total_remaining_time.setText(self.time_str(0))
        self.grid_layout.addWidget(self.label_total_remaining_time, 3, 1, QtCore.Qt.AlignCenter)

        # Upcoming intervals widget
        self.upcoming_intervals = UpcomingIntervals(self.workout,self.font_upcoming_header)
        self.grid_layout.addWidget(self.upcoming_intervals, 1, 2, 3, 1, QtCore.Qt.AlignCenter)

        # Sound for changing interval
        print(path.dirname(__file__)+'/tone.wav')
        self.bell = QtMultimedia.QSound(path.dirname(__file__)+'/tone.wav')

        # Create start/pause button
        self.button_start_pause = QtWidgets.QPushButton('Start', self.grid_widget)
        self.button_start_pause.setFont(self.font_default)
        self.button_start_pause.clicked.connect(self.start_pause)
        self.grid_layout.addWidget(self.button_start_pause, 4, 0, QtCore.Qt.AlignCenter)
        self.button_stop = QtWidgets.QPushButton('Stop', self.grid_widget)
        self.button_stop.setFont(self.font_default)
        self.button_stop.clicked.connect(self.stop)
        self.grid_layout.addWidget(self.button_stop, 4, 1, QtCore.Qt.AlignCenter)
        self.update_buttons()
        # Create start/pause shortcut
        self.shortcut_start_pause = QtWidgets.QShortcut(QtCore.Qt.Key_Space, self, self.start_pause)
        # Create stop shortcut
        self.shortcut_stop = QtWidgets.QShortcut(QtCore.Qt.Key_S, self, self.stop)

        # Initialise timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.redraw)
        self.timer.start()

        self.show()

    # Redraw dynamic elements of the ui
    def redraw(self):
        # Obtain current time elapsed and remaining, and current interval
        self.elapsed, self.remaining, self.interval_elapsed, self.interval_remaining, self.interval, changed_interval = self.workout.progress()

        # Write current times
        self.label_interval_remaining_time.setText(self.time_str(self.interval_remaining))
        self.label_total_remaining_time.setText(self.time_str(self.remaining))

        if changed_interval:
            # Play sound if interval has changed
            self.bell.play()
            # Write current interval name
            self.label_interval_name.setText(self.interval.text)
            # Write upcoming interval names
            self.upcoming_intervals.write_upcoming_intervals()

    # Start or pause the workout
    def start_pause(self):
        self.workout.start_pause()
        self.update_buttons()

    # Stop the workout
    def stop(self):
        self.workout.stop()
        self.label_interval_name.setText(self.workout.intervals[0].text)
        self.upcoming_intervals.write_upcoming_intervals()
        self.update_buttons()

    # Write the appropriate button labels and activate/deactivate as necessary
    def update_buttons(self):
        if self.workout.state == WorkoutState.RUNNING:
            self.button_start_pause.setText('Pause')
            self.button_stop.setEnabled(True)
        elif self.workout.state == WorkoutState.PAUSED:
            self.button_start_pause.setText('Resume')
        elif self.workout.state == WorkoutState.STOPPED:
            self.button_start_pause.setText('Start')
            self.button_stop.setEnabled(False)

    # Format a time in seconds for output
    def time_str(self,time):
        minutes, seconds = divmod(time, 60)
        string = "{:2d}:{:04.1f}".format(int(minutes), seconds)
        return string

class UpcomingIntervals(QtWidgets.QWidget):
    def __init__(self,workout,font_upcoming_header):
        super().__init__()

        self._UPCOMING_INTERVALS_DISPLAYED = 8
        self.workout = workout

        # VBox layout for upcoming intervals
        self.vbox_upcoming = QtWidgets.QVBoxLayout(self)

        # Upcoming intervals header
        self.label_upcoming = QtWidgets.QLabel(self)
        self.label_upcoming.setFont(font_upcoming_header)
        self.label_upcoming.setText("Upcoming")
        self.vbox_upcoming.addWidget(self.label_upcoming, QtCore.Qt.AlignCenter)

        # Upcoming interval labels
        self.label_upcoming_intervals = [QtWidgets.QLabel() for i in range(self._UPCOMING_INTERVALS_DISPLAYED)]
        for label in self.label_upcoming_intervals:
            self.vbox_upcoming.addWidget(label, QtCore.Qt.AlignCenter)
        self.write_upcoming_intervals()

    # Write the names of upcoming intervals to the upcoming vbox layout
    def write_upcoming_intervals(self):
        # Write hearder
        upcoming = self.workout.upcoming()

        for i,interval in enumerate(upcoming[:self._UPCOMING_INTERVALS_DISPLAYED]):
            self.label_upcoming_intervals[i].setText(interval.text)

def parse_args():
    parser = argparse.ArgumentParser(prog='qintervals', description='Interval training timer')
    parser.add_argument('workout', type=str, action='store',
            help='YAML workout file to read')

    clargs = parser.parse_args()
    return clargs
