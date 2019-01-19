import context
import pytest
from qintervals.workout import Workout
import yaml

def test_invalid_yaml():
    with pytest.raises(yaml.YAMLError):
        workout = Workout(yaml_file=context.test_data_dir+'invalid_yaml.yml')
