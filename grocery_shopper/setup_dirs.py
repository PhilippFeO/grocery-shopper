import configparser
import logging
import sys
from pathlib import Path

from grocery_shopper.vars import defaults_file, directories


def setup_dirs_helper(path: Path) -> None:
    for v in directories.values():
        tmp_dir = Path(path, v)
        try:
            tmp_dir.mkdir(parents=True)
        except OSError:
            msg = f"(Re)move (possible old) directoy '{tmp_dir}' or change location completely."
            logging.warning(msg)
            sys.exit(2)


def setup_dirs(
    config: configparser.ConfigParser,
    defaults_file_path: Path = Path(Path(__file__).parent, defaults_file),
) -> Path:
    """Check if necessary directories (s. `vars.py`) exists and if not, creates them.

    :config: Config with default values set by user.
    :defaults_file_path: Path to the `defaults.ini` file
    :returns: Path of the three directories, ie. path + name (mentioned above).
    """
    # Check if directory was already set, ie program was ran at least once
    try:
        general_dir = Path(config['general']['dir'])
    # If not (probably on first run), then set it to CWD
    # Except block entered on first run => directories don't exists
    except (configparser.NoSectionError, configparser.NoOptionError, KeyError):
        general_dir = Path.cwd()
        # Call to setup_dirs_helper() has to come before setting config
        # The function might exit, then no values should be written to config
        setup_dirs_helper(general_dir)
        config['general']['dir'] = str(Path.expanduser(general_dir))
        # Write default values
        with defaults_file_path.open('w') as f:
            config.write(f)

    return general_dir
