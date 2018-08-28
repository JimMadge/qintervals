from interval import Workout, Interval, IntervalType
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

_WIDTH = 500
_HEIGHT = 500
_UPCOMING_INTERVALS_DISPLAYED = 8

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

        # Grid layout for upcoming intervals
        self.vbox_upcoming = QtWidgets.QVBoxLayout()
        self.grid_layout.addLayout(self.vbox_upcoming, 1, 2, 2, 1, QtCore.Qt.AlignCenter)

        # Upcoming intervals header
        self.label_upcoming = QtWidgets.QLabel(self.grid_widget)
        self.label_upcoming.setFont(self.font_upcoming_header)
        self.label_upcoming.setText("Upcoming")
        self.vbox_upcoming.addWidget(self.label_upcoming, QtCore.Qt.AlignCenter)

        # Upcoming interval labels
        self.label_upcoming_intervals = [QtWidgets.QLabel() for i in range(_UPCOMING_INTERVALS_DISPLAYED)]
        for label in self.label_upcoming_intervals:
            self.vbox_upcoming.addWidget(label, QtCore.Qt.AlignCenter)

        # Initialise timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.redraw)
        self.timer.start()

        # Start the workout
        self.workout.start()

        self.show()

    # Redraw dynamic elements of the ui
    def redraw(self):
        # Obtain current time elapsed and remaining, and current interval
        self.elapsed, self.remaining, self.interval_elapsed, self.interval_remaining, self.interval = self.workout.progress()
        # Write current times
        self.label_interval_remaining_time.setText(self.time_str(self.interval_remaining))
        self.label_total_remaining_time.setText(self.time_str(self.remaining))

        # Write current interval name
        self.label_interval_name.setText(self.interval.text)

        # Write upcoming interval names
        self.write_upcoming_intervals()

    # Write the names of upcoming intervals to the upcoming vbox layout
    def write_upcoming_intervals(self):
        # Write hearder
        upcoming = self.workout.upcoming()

        for i,interval in enumerate(upcoming[:_UPCOMING_INTERVALS_DISPLAYED]):
            self.label_upcoming_intervals[i].setText(interval.text)

    # Format a time in seconds for output
    def time_str(self,time):
        minutes, seconds = divmod(time, 60)
        string = "{:2d}:{:02.2f}".format(int(minutes), seconds)
        return string

def example_workout():
    workout = Workout("Threshold")
    workout.add_interval(Interval(IntervalType.WARMUP, "Warm up", 10*60))
    workout.add_interval(Interval(IntervalType.WORK, "Zone 3", 10*60))
    workout.add_interval(Interval(IntervalType.REST, "Rest", 5*60))
    workout.add_interval(Interval(IntervalType.WORK, "Zone 4, low", 5*60))
    workout.add_interval(Interval(IntervalType.REST, "Rest", 1*60))
    workout.add_interval(Interval(IntervalType.WORK, "Zone 4, low", 5*60))
    workout.add_interval(Interval(IntervalType.REST, "Rest", 1*60))
    workout.add_interval(Interval(IntervalType.REST, "Rest", 5*60))
    workout.add_interval(Interval(IntervalType.WORK, "Zone 4, high", 2*60))
    workout.add_interval(Interval(IntervalType.REST, "Rest", 0.5*60))
    workout.add_interval(Interval(IntervalType.WORK, "Zone 4, high", 2*60))
    workout.add_interval(Interval(IntervalType.REST, "Rest", 0.5*60))
    workout.add_interval(Interval(IntervalType.WORK, "Zone 4, high", 2*60))
    workout.add_interval(Interval(IntervalType.REST, "Rest", 0.5*60))
    workout.add_interval(Interval(IntervalType.REST, "Rest", 5*60))
    workout.add_interval(Interval(IntervalType.WORK, "Zone 5", 1*60))
    workout.add_interval(Interval(IntervalType.REST, "Rest", 0.5*60))
    workout.add_interval(Interval(IntervalType.WORK, "Zone 5", 1*60))
    workout.add_interval(Interval(IntervalType.REST, "Rest", 0.5*60))
    workout.add_interval(Interval(IntervalType.WORK, "Zone 5", 1*60))
    workout.add_interval(Interval(IntervalType.REST, "Rest", 0.5*60))
    workout.add_interval(Interval(IntervalType.WORK, "Zone 5", 1*60))
    workout.add_interval(Interval(IntervalType.REST, "Rest", 0.5*60))
    workout.add_interval(Interval(IntervalType.WORK, "Zone 5", 1*60))
    workout.add_interval(Interval(IntervalType.REST, "Rest", 0.5*60))
    workout.add_interval(Interval(IntervalType.WORK, "Zone 5", 1*60))
    workout.add_interval(Interval(IntervalType.REST, "Rest", 0.5*60))
    workout.add_interval(Interval(IntervalType.WARMDOWN, "Warm down", 10*60))

    return workout

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui(example_workout())
    sys.exit(app.exec_())
