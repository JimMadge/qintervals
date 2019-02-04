import context
from pytest import approx
from qintervals.workout import Workout, WorkoutState
from time import sleep

TOLERANCE = 1e-3
def approx_time(value):
    return approx(value, abs=TOLERANCE)

def test_start():
    workout = Workout(yaml_file=context.test_data_dir+'basic.yml')
    workout.start()
    sleep(0.01)

    assert workout.current_interval() == workout.intervals[0]
    assert workout.elapsed() == approx_time(0.01)

def test_transition():
    workout = Workout(yaml_file=context.test_data_dir+'quick.yml')
    workout.start()
    sleep(0.01)

    progress = workout.progress()

    assert workout.current_interval() == workout.intervals[1]
    assert progress.changed_interval

def test_ending():
    workout = Workout(yaml_file=context.test_data_dir+'quick.yml')
    workout.start()
    sleep(0.03)

    progress = workout.progress()

    assert workout.state == WorkoutState.stopped

def test_pause():
    workout = Workout(yaml_file=context.test_data_dir+'basic.yml')
    workout.start()
    sleep(0.01)
    workout.pause()
    sleep(0.01)

    assert workout.state == WorkoutState.paused
    assert workout.elapsed() == approx_time(0.01)

def test_resume():
    workout = Workout(yaml_file=context.test_data_dir+'basic.yml')
    workout.start()
    sleep(0.01)
    workout.pause()
    sleep(0.01)
    workout.start()

    assert workout.time_paused == approx_time(0.01)
    assert workout.state == WorkoutState.running

def test_start_pause():
    workout = Workout(yaml_file=context.test_data_dir+'basic.yml')
    workout.start()
    sleep(0.01)
    workout.start_pause()
    sleep(0.01)

    assert workout.state == WorkoutState.paused
    assert workout.elapsed() == approx_time(0.01)

    workout.start_pause()

    assert workout.time_paused == approx_time(0.01)
    assert workout.state == WorkoutState.running

def test_progress():
    workout = Workout(yaml_file=context.test_data_dir+'quick.yml')
    workout.start()
    sleep(0.01)

    progress = workout.progress()

    assert progress.elapsed == approx_time(0.01)
    assert progress.remaining == approx_time(0.02)
    assert progress.interval_elapsed == approx_time(0.)
    assert progress.interval_remaining == approx_time(0.01)
    assert progress.interval == workout.intervals[1]
    assert progress.changed_interval == True

    progress = workout.progress()

    assert progress.changed_interval == False

def test_upcoming():
    workout = Workout(yaml_file=context.test_data_dir+'quick.yml')

    assert workout.upcoming() == workout.intervals[1:]

    workout.start()
    sleep(0.01)

    assert workout.upcoming() == workout.intervals[2:]
