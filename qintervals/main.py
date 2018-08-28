from interval import Workout, Interval, IntervalType
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

_WIDTH = 500
_HEIGHT = 500

class Ui(QtWidgets.QWidget):
    def __init__(self, workout):
        super().__init__()
        self.init_ui(workout)

    # Initialise the ui
    def init_ui(self,workout):
        self.workout = workout

        # Size the widget
        self.resize(_WIDTH, _HEIGHT)

        self.setWindowTitle("qintervals")

        # Create grid for times
        self.grid_widget = QtWidgets.QWidget(self)
        self.grid_widget.setGeometry(QtCore.QRect(50, 50, 400, 400))
        self.grid_layout = QtWidgets.QGridLayout(self.grid_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        # Workout name
        self.label_workout_name = QtWidgets.QLabel(self.grid_widget)
        self.label_workout_name.setText(self.workout.name)
        self.grid_layout.addWidget(self.label_workout_name, 0, 0, 1, -1, QtCore.Qt.AlignCenter)

        # Interval remaining label
        self.label_interval_remaining = QtWidgets.QLabel(self.grid_widget)
        self.label_interval_remaining.setText("Interval Remaining")
        self.grid_layout.addWidget(self.label_interval_remaining, 1, 0, QtCore.Qt.AlignCenter)
        # Interval remaining time
        self.label_interval_remaining_time = QtWidgets.QLabel(self.grid_widget)
        self.label_interval_remaining_time.setText(self.time_str(0))
        self.grid_layout.addWidget(self.label_interval_remaining_time, 1, 1, QtCore.Qt.AlignCenter)

        # Total remaining label
        self.label_total_remaining = QtWidgets.QLabel(self.grid_widget)
        self.label_total_remaining.setText("Total Remaining")
        self.grid_layout.addWidget(self.label_total_remaining, 2, 0, QtCore.Qt.AlignCenter)
        # Total remaining time
        self.label_total_remaining_time = QtWidgets.QLabel(self.grid_widget)
        self.label_total_remaining_time.setText(self.time_str(0))
        self.grid_layout.addWidget(self.label_total_remaining_time, 2, 1, QtCore.Qt.AlignCenter)

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
        self.elapsed, self.remaining, self.interval_elapsed, self.interval_remaining, self.interval = self.workout.progress()
        self.label_interval_remaining_time.setText(self.time_str(self.interval_remaining))
        self.label_total_remaining_time.setText(self.time_str(self.remaining))

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
