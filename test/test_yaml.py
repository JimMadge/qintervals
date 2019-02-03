import context
import pytest
from qintervals.workout import Workout, WorkoutFileError, MissingKeyError
import yaml

def test_invalid_yaml():
    with pytest.raises(WorkoutFileError):
        workout = Workout(yaml_file=context.test_data_dir+'invalid_yaml.yml')

def test_yaml_basic():
    n_intervals = 4
    names = ['One', 'Two', 'Three', 'Four']
    workout = Workout(yaml_file=context.test_data_dir+'basic.yml')
    interval_names = [interval.text for interval in workout.intervals]

    assert len(workout.intervals) == n_intervals
    assert interval_names == names

def test_yaml_block():
    n_intervals = 6
    names = ['One', 'Two'] + ['Block One', 'Block Two']*2
    workout = Workout(yaml_file=context.test_data_dir+'block.yml')
    interval_names = [interval.text for interval in workout.intervals]

    assert len(workout.intervals) == n_intervals
    assert interval_names == names

def test_yaml_nested_blocks():
    n_intervals = 12
    names = ['One', 'Two'] + (['Block One'] + ['Nested Block One', 'Nested Block Two']*2 )*2
    workout = Workout(yaml_file=context.test_data_dir+'nested_blocks.yml')
    interval_names = [interval.text for interval in workout.intervals]

    assert len(workout.intervals) == n_intervals
    assert interval_names == names

class TestMissingKeyError(object):
    def test_missing_title_key(self):
        with pytest.raises(MissingKeyError):
            workout = Workout(yaml_file=context.test_data_dir+'missing_title.yml')

    def test_missing_intervals(self):
        with pytest.raises(MissingKeyError):
            workout = Workout(yaml_file=context.test_data_dir+'missing_intervals.yml')

    def test_missing_interval_key(self):
        with pytest.raises(MissingKeyError):
            workout = Workout(yaml_file=context.test_data_dir+'missing_interval_key.yml')

    def test_block_missing_repeats(self):
        with pytest.raises(MissingKeyError):
            workout = Workout(yaml_file=context.test_data_dir+'block_missing_repeats.yml')

    def test_block_missing_intervals(self):
        with pytest.raises(MissingKeyError):
            workout = Workout(yaml_file=context.test_data_dir+'block_missing_intervals.yml')
