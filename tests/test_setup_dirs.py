import configparser
from pathlib import Path

import pytest

from grocery_shopper.setup_dirs import setup_dirs, setup_dirs_helper
from grocery_shopper.vars import directories


def isdir_helper(path: Path):
    for v in directories.values():
        assert Path.is_dir(path / v)


@pytest.fixture
def config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.add_section('general')
    return config


def test_setup_dirs_helper(tmp_path):
    # Testing equality on return values basically implies testing `os.path.join()`. I trust the python developers more than me.
    setup_dirs_helper(tmp_path)
    isdir_helper(tmp_path)


@pytest.mark.parametrize('dir_name', directories.values())
def test_setup_dirs_helper_one_exists(tmp_path, dir_name):
    """Test setup_dirs() in case on directory already exists.

    :tmp_path: Path where directories were created
    :dir_name: One of the values of vars.directories
    """
    (tmp_path / dir_name).mkdir()
    with pytest.raises(SystemExit) as e:
        setup_dirs_helper(tmp_path)
    assert e.type is SystemExit
    assert e.value.code == 2


def test_setup_dirs_first_run(monkeypatch, tmp_path, config):
    """First run implies, config has no dir entry."""

    def mock_cwd() -> Path:
        return tmp_path

    monkeypatch.setattr(Path, 'cwd', mock_cwd)
    # monkeypatch.setattr('Path.cwd', lambda: str(tmp_path))

    config_file = tmp_path / 'defaults.ini'
    general_dir = Path(tmp_path)

    setup_dirs(config, config_file)

    # Check value in config object
    assert config['general']['dir'] == str(general_dir)

    # Check value in written config file
    config = configparser.ConfigParser()
    with config_file.open('r') as config_file:
        config.read_file(config_file)
    assert config['general']['dir'] == str(general_dir)

    # Check created directories
    isdir_helper(tmp_path)


def test_setup_dirs_second_run(monkeypatch, tmp_path, config):
    """Simulates a second (or third, fourth, ...) run, ie. dir in config is set and necessary directories exists."""

    def mock_cwd() -> Path:
        return tmp_path

    monkeypatch.setattr(Path, 'cwd', mock_cwd)

    config_file = tmp_path / 'defaults.ini'
    general_dir = tmp_path

    # First run => set everythin up
    setup_dirs(config, config_file)

    # Second run, check if existing value of general.dir is used
    # If not, paths would mismatch due toe non mocked os.getcwd() call
    assert general_dir == setup_dirs(config, config_file)
