from grocery_shopper.setup_dirs import setup_dirs, setup_dirs_helper
import pytest
import configparser
from grocery_shopper.vars import directories
import os


def isdir_helper(path):
    for _, v in directories.items():
        assert os.path.isdir(path / v)


@pytest.fixture
def config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.add_section('General')
    return config


def test_setup_dirs_helper(tmp_path):
    # Testing equality on return values basically implies testing `os.path.join()`. I trust the python developers more than me.
    setup_dirs_helper(tmp_path)
    isdir_helper(tmp_path)


@pytest.mark.parametrize("dir_name", directories.values())
def test_setup_dirs_helper_one_exists(tmp_path, dir_name):
    """Test setup_dirs() in case on directory already exists.

    :tmp_path: Path where directories were created
    :dir_name: One of the values of vars.directories
    """
    os.mkdir(tmp_path / dir_name)
    with pytest.raises(SystemExit) as e:
        setup_dirs_helper(tmp_path)
    assert e.type == SystemExit
    assert e.value.code == 1


def test_setup_dirs_first_run(monkeypatch, tmp_path, config):
    """First run implies, config has no dir entry.
    """
    monkeypatch.setattr('os.getcwd', lambda: str(tmp_path))

    setup_dirs(config)

    assert config['General']['dir'] == str(tmp_path)
    isdir_helper(tmp_path)


def test_setup_dirs_second_run(tmp_path, config):
    """Simulates a second (or third, fourth, ...) run, ie. dir in config is set and necessary directories exists.
    """
    # Set config
    config['General']['dir'] = str(tmp_path)

    assert directories == setup_dirs(config)
