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
from math import hypot, sin, pi
import sys
import argparse

_WIDTH = 700
_HEIGHT = 500
_BORDER_HORIZONTAL = 25
_BORDER_VERTICAL = 25

_COLOUR_RED = QtGui.QColor(228,26,28)
_COLOUR_BLUE = QtGui.QColor(55,126,184)
_COLOUR_GREEN = QtGui.QColor(77,175,74)

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
        self.grid_widget.setGeometry(QtCore.QRect(_BORDER_HORIZONTAL, _BORDER_VERTICAL,
            _WIDTH-2*_BORDER_HORIZONTAL, _HEIGHT-2*_BORDER_VERTICAL))
        self.grid_layout = QtWidgets.QGridLayout(self.grid_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        # Workout name
        self.label_workout_name = QtWidgets.QLabel(self.grid_widget)
        self.label_workout_name.setFont(self.font_workout_name)
        self.label_workout_name.setText(self.workout.name)
        self.grid_layout.addWidget(self.label_workout_name, 0, 0, 1, -1, QtCore.Qt.AlignCenter)

        # Interval name
        self.label_interval_name = QtWidgets.QLabel(self)
        self.label_interval_name.setFont(self.font_interval_name)
        self.label_interval_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_interval_name.setText(self.workout.intervals[0].text)

        # Timers
        self.timers = Timers(self)

        # Count down
        self.count_down = CountDown(self)
        self.count_down.addWidget(self.label_interval_name, QtCore.Qt.AlignCenter)
        self.count_down.addWidget(self.timers, QtCore.Qt.AlignCenter)
        self.grid_layout.addWidget(self.count_down, 1, 0, 1, 1, QtCore.Qt.AlignCenter)

        # Upcoming intervals widget
        self.upcoming_intervals = UpcomingIntervals(self)
        self.grid_layout.addWidget(self.upcoming_intervals, 1, 1, 2, 1, QtCore.Qt.AlignCenter)

        # Sound for changing interval
        self.bell = QtMultimedia.QSound(path.dirname(__file__)+'/tone.wav')

        # Create buttons
        self.buttons = Buttons(self)
        self.grid_layout.addWidget(self.buttons, 2, 0, 1, 1, QtCore.Qt.AlignCenter)
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
        elapsed, remaining, interval_elapsed, interval_remaining, interval, changed_interval = self.workout.progress()

        self.timers.update_times(remaining, interval_remaining)

        self.count_down.update_times(elapsed,remaining,interval_elapsed,interval_remaining)
        self.count_down.repaint()

        if changed_interval:
            # Play sound if interval has changed
            self.bell.play()
            # Write current interval name
            self.label_interval_name.setText(interval.text)
            # Write upcoming interval names
            self.upcoming_intervals.write_upcoming_intervals()

    # Start or pause the workout
    def start_pause(self):
        self.workout.start_pause()
        self.buttons.update_buttons()

    # Stop the workout
    def stop(self):
        self.workout.stop()
        self.label_interval_name.setText(self.workout.intervals[0].text)
        self.upcoming_intervals.write_upcoming_intervals()
        self.buttons.update_buttons()

class Timers(QtWidgets.QWidget):
    def __init__(self,parent):
        super().__init__(parent)

        font_time = self.parentWidget().font_time

        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        # Interval remaining label
        self.label_interval_remaining = QtWidgets.QLabel(self)
        self.label_interval_remaining.setText("Interval")
        self.grid_layout.addWidget(self.label_interval_remaining, 2, 0, QtCore.Qt.AlignLeft)
        # Interval remaining time
        self.label_interval_remaining_time = QtWidgets.QLabel(self)
        self.label_interval_remaining_time.setFont(font_time)
        self.label_interval_remaining_time.setText(self.time_str(0))
        self.grid_layout.addWidget(self.label_interval_remaining_time, 2, 1, QtCore.Qt.AlignRight)

        # Total remaining label
        self.label_total_remaining = QtWidgets.QLabel(self)
        self.label_total_remaining.setText("Total")
        self.grid_layout.addWidget(self.label_total_remaining, 3, 0, QtCore.Qt.AlignLeft)
        # Total remaining time
        self.label_total_remaining_time = QtWidgets.QLabel(self)
        self.label_total_remaining_time.setFont(font_time)
        self.label_total_remaining_time.setText(self.time_str(0))
        self.grid_layout.addWidget(self.label_total_remaining_time, 3, 1, QtCore.Qt.AlignRight)

    # Update times
    def update_times(self,remaining,interval_remaining):
        # Write current times
        self.label_interval_remaining_time.setText(self.time_str(interval_remaining))
        self.label_total_remaining_time.setText(self.time_str(remaining))

    # Format a time in seconds for output
    def time_str(self,time):
        minutes, seconds = divmod(time, 60)
        string = "{:2d}:{:04.1f}".format(int(minutes), seconds)
        return string

class Buttons(QtWidgets.QWidget):
    def __init__(self,parent):
        super().__init__(parent)

        self.workout = self.parentWidget().workout
        font_default = self.parentWidget().font_default

        self.hbox = QtWidgets.QHBoxLayout(self)
        self.hbox.setContentsMargins(0, 0, 0, 0)

        # Create start/pause button
        self.button_start_pause = QtWidgets.QPushButton('Start', self)
        self.button_start_pause.setFont(font_default)
        self.button_start_pause.clicked.connect(self.parentWidget().start_pause)
        self.hbox.addWidget(self.button_start_pause, QtCore.Qt.AlignCenter)

        # Create stop button
        self.button_stop = QtWidgets.QPushButton('Stop', self)
        self.button_stop.setFont(font_default)
        self.button_stop.clicked.connect(self.parentWidget().stop)
        self.hbox.addWidget(self.button_stop, QtCore.Qt.AlignCenter)
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

class CountDown(QtWidgets.QWidget):
    def __init__(self,parent):
        super().__init__(parent)

        # Dimension of the sides of this widget
        self._DIMENSION = 300

        # Angle of a full circle in Qt (360*16)
        self._TOTAL_ANGLE = 5760

        self.setMinimumSize(self._DIMENSION,self._DIMENSION)

        # Pens used to draw arcs
        self._PEN_WIDTH = 10
        self._HALF_PEN_WIDTH = self._PEN_WIDTH/2
        self.pen_total = QtGui.QPen(_COLOUR_BLUE, self._PEN_WIDTH, QtCore.Qt.SolidLine)
        self.pen_interval = QtGui.QPen(_COLOUR_GREEN, self._PEN_WIDTH, QtCore.Qt.SolidLine)

        # V box in the centre of the arcs
        self._CENTRE = self._DIMENSION/2
        self._INNER_RADIUS = self._CENTRE - 2*self._PEN_WIDTH
        self._INSET = self._CENTRE - self._INNER_RADIUS * sin(pi/4)
        self.contents = QtWidgets.QWidget(self)
        self.contents.setGeometry(QtCore.QRect(
            QtCore.QPoint(self._INSET, self._INSET),
            QtCore.QPoint(self._DIMENSION-self._INSET, self._DIMENSION-self._INSET)))
        self.vbox = QtWidgets.QVBoxLayout(self.contents)
        self.vbox.setContentsMargins(0, 0, 0, 0)

        self.update_times(0,1,0,1)

    def update_times(self, elapsed, remaining, interval_elapsed, interval_remaining):
        self.angle_remaining = remaining / (elapsed+remaining) * self._TOTAL_ANGLE
        self.angle_interval_remaining = interval_remaining / (interval_elapsed+interval_remaining) * self._TOTAL_ANGLE

    def addWidget(self, *args):
        self.vbox.addWidget(*args)

    def paintEvent(self, e):
        width, height = self.size().width(), self.size().height()

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Total time arc
        painter.setPen(self.pen_total)
        painter.drawArc(self._HALF_PEN_WIDTH,
                self._HALF_PEN_WIDTH,
                width-self._PEN_WIDTH,
                height-self._PEN_WIDTH,0,self.angle_remaining)

        # Interval time arc
        painter.setPen(self.pen_interval)
        painter.drawArc(self._PEN_WIDTH+self._HALF_PEN_WIDTH,
                self._PEN_WIDTH+self._HALF_PEN_WIDTH,
                width-3*self._PEN_WIDTH,
                height-3*self._PEN_WIDTH,0,self.angle_interval_remaining)

        painter.end()

class UpcomingIntervals(QtWidgets.QWidget):
    def __init__(self,parent):
        super().__init__(parent)

        self._UPCOMING_INTERVALS_DISPLAYED = 8
        self.workout = self.parentWidget().workout
        font_upcoming_header = self.parentWidget().font_upcoming_header

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
