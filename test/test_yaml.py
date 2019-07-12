import pytest
from qintervals.workout import Workout, WorkoutFileError, MissingKeyError


def test_invalid_yaml(test_data):
    with pytest.raises(WorkoutFileError):
        Workout(yaml_file=test_data+'/invalid_yaml.yml')


def test_yaml_basic(test_data):
    n_intervals = 4
    names = ['One', 'Two', 'Three', 'Four']
    workout = Workout(yaml_file=test_data+'/basic.yml')
    interval_names = [interval.text for interval in workout.intervals]

    assert len(workout.intervals) == n_intervals
    assert interval_names == names


def test_yaml_block(test_data):
    n_intervals = 6
    names = ['One', 'Two'] + ['Block One', 'Block Two']*2
    workout = Workout(yaml_file=test_data+'/block.yml')
    interval_names = [interval.text for interval in workout.intervals]

    assert len(workout.intervals) == n_intervals
    assert interval_names == names


def test_yaml_nested_blocks(test_data):
    n_intervals = 12
    names = (
        ['One', 'Two']
        + (
            ['Block One']
            + ['Nested Block One', 'Nested Block Two']*2
        )*2
    )
    workout = Workout(yaml_file=test_data+'/nested_blocks.yml')
    interval_names = [interval.text for interval in workout.intervals]

    assert len(workout.intervals) == n_intervals
    assert interval_names == names


class TestMissingKeyError(object):
    def test_missing_title_key(self, test_data):
        with pytest.raises(MissingKeyError):
            Workout(yaml_file=test_data+'/missing_title.yml')

    def test_missing_intervals(self, test_data):
        with pytest.raises(MissingKeyError):
            Workout(yaml_file=test_data+'/missing_intervals.yml')

    def test_missing_interval_key(self, test_data):
        with pytest.raises(MissingKeyError):
            Workout(yaml_file=test_data+'/missing_interval_key.yml')

    def test_block_missing_repeats(self, test_data):
        with pytest.raises(MissingKeyError):
            Workout(yaml_file=test_data+'/block_missing_repeats.yml')

    def test_block_missing_intervals(self, test_data):
        with pytest.raises(MissingKeyError):
            Workout(yaml_file=test_data+'/block_missing_intervals.yml')
