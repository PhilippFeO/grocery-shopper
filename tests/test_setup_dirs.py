from grocery_shopper.setup_dirs import setup_dirs, setup_dirs_helper
import pytest
import configparser
from grocery_shopper.vars import recipe_dir_name, misc_dir_name, resource_dir_name
import os


    
def isdir_helper(path):
    assert os.path.isdir(path / recipe_dir_name) 
    assert os.path.isdir(path / misc_dir_name)
    assert os.path.isdir(path / resource_dir_name)

@pytest.fixture
def config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.add_section('General')
    return config


def test_setup_dirs_helper(tmp_path):
    # Testing equality on return values basically implies testing `os.path.join()`. I trust the python developers more than me.
    _, _, _ = setup_dirs_helper(tmp_path)
    isdir_helper(tmp_path)


@pytest.mark.parametrize("dir_name", [recipe_dir_name, misc_dir_name, resource_dir_name])
def test_setup_dirs_helper_one_exists(tmp_path, dir_name):
    """Test setup_dirs() in case on directory already exists.

    :tmp_path: Path where directories were created
    :dir_name: One of `recipe/`, `misc/`, `res/`
    """
    os.mkdir(tmp_path / dir_name)
    with pytest.raises(SystemExit) as e:
        _, _, _ = setup_dirs_helper(tmp_path)
    assert e.type == SystemExit
    assert e.value.code == 1

    
def test_setup_dirs_first_run(monkeypatch, tmp_path, config):
    """First run implies, config has no dir entry.
    """
    monkeypatch.setattr('os.getcwd', lambda: str(tmp_path))

    _, _, _ = setup_dirs(config)

    assert config['General']['dir'] == str(tmp_path)
    isdir_helper(tmp_path)


def test_setup_dirs_second_run(tmp_path, config):
    """Simulates a second (or third, fourth, ...) run, ie. dir in config is set and necessary directories exists.
    """
    # Set config
    config['General']['dir'] = str(tmp_path)
    # Create directories
    expected_recipe_dir = os.path.join(tmp_path, recipe_dir_name)
    expected_misc_dir = os.path.join(tmp_path,misc_dir_name)
    expected_resource_dir = os.path.join(tmp_path, resource_dir_name)
    os.makedirs(expected_recipe_dir)
    os.makedirs(expected_resource_dir)
    os.makedirs(expected_misc_dir)

    # Call function
    recipe_dir, misc_dir, resource_dir = setup_dirs(config)

    # No check with 'isdir' necessary, because directories are created in this function. Every run after the first run doesn't create directories and merely returns names.
    assert expected_recipe_dir == recipe_dir
    assert expected_misc_dir == misc_dir
    assert expected_resource_dir == resource_dir
    
    
