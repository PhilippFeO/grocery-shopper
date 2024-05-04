import os
import configparser
import sys
import logging
from grocery_shopper.vars import directories


def setup_dirs_helper(path: str) -> None:
    for _, v in directories.items():
        tmp_dir = os.path.join(path, v)
        try:
            os.makedirs(tmp_dir)
        except OSError as ose:
            # TODO: Logging <12-04-2024>
            logging.info(
                f"(Re)move (possible old) {tmp_dir} or change location completely.\nOriginal Error: {str(ose)}")
            sys.exit(2)


def setup_dirs(config: configparser.ConfigParser,
               defaults_file_path: str) -> dict[str, str]:
    """Checks if necessary directories (s. `vars.py`) exists and if not, creates them.

    :config: Config with default values set by user.
    :defaults_file_path: Path to the `defaults.ini` file
    :returns: Path of the three directories, ie. path + name (mentioned above).
    """
    # Check if directory was already set, ie program was ran at least once
    try:
        general_dir = config['general']['dir']
    # If not (probably on first run), then set it to CWD
    # Except block entered on first run => directories don't exists
    except (configparser.NoSectionError, configparser.NoOptionError, KeyError):
        general_dir = os.getcwd()
        # Call to setup_dirs_helper() has to come before setting config
        # The function might exit, then no values should be written to config
        setup_dirs_helper(general_dir)
        config['general']['dir'] = os.path.expanduser(general_dir)
        # Write default values
        with open(defaults_file_path, 'w') as f:
            config.write(f)

    return directories
