import context
import pytest
from qintervals import interval
import yaml

def test_invalid_yaml():
    with pytest.raises(yaml.YAMLError):
        workout = interval.Workout(yaml_file=context.test_data_dir+'invalid_yaml.yml')
