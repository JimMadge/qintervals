import argparse
import os
from PyQt5 import QtWidgets
from qintervals.workout import Workout
from qintervals.gui import Ui
import sys


def main():
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = QtWidgets.QApplication(sys.argv)

    # Get command line arguments
    clargs = parse_args()
    # Create workout object
    workout = Workout(clargs.workout)

    ui = Ui(workout)  # noqa: F841
    sys.exit(app.exec_())


def parse_args():
    parser = argparse.ArgumentParser(prog='qintervals',
                                     description='Interval training timer')
    parser.add_argument('workout', type=str, action='store',
                        help='YAML workout file to read')

    clargs = parser.parse_args()
    return clargs


if __name__ == "__main__":
    main()
