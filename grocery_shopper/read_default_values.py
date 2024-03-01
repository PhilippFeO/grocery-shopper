import logging
import sys
import configparser
import os
from grocery_shopper.vars import defaults_file


def read_default_values():
    # Slightly different treatment because it shall be possible to execute main() directly with a list of files. In this case default values must exist.
    grocery_shopper_dir = os.path.dirname(__file__)
    defaults_file_path = f'{grocery_shopper_dir}/{defaults_file}'
    config = configparser.ConfigParser()
    try:
        # According to Doc: Use read_file() when file is expected to assist
        config.read_file(open(defaults_file_path))
    except FileNotFoundError as fnfe:
        logging.error(f'{fnfe}\nMaybe you have to run <start.py> first to initialize default arguments.')
        sys.exit(1)
    return config
