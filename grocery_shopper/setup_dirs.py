import os
import configparser
import sys
import logging
from grocery_shopper.vars import recipe_dir_name, misc_dir_name, resource_dir_name


def setup_dirs_helper(path: str) -> tuple[str, str, str]:
    recipe_dir = os.path.join(path, recipe_dir_name)
    misc_dir = os.path.join(path,misc_dir_name)
    res_dir = os.path.join(path, resource_dir_name)
    try:
        os.makedirs(recipe_dir)
        os.makedirs(res_dir)
        os.makedirs(misc_dir)
    except OSError as ose:
        # TODO: Logging <12-04-2024> 
        logging.info(f"Not all directories created because at least one already exists. (Re)move {recipe_dir_name}, {misc_dir_name} or {resource_dir_name} or change location completely.\nOriginal Error: {str(ose)}")
        sys.exit(1)

    return recipe_dir, misc_dir, res_dir

def setup_dirs(config: configparser.ConfigParser) -> tuple[str, str, str]:
    """Checks if necessary directories (`recipe_dir_name`, `misc_dir_name`, `resource_dir_name`) exists and if not, creates them.

    :config: Config with default values set by user.
    :returns: Path of the three directories, ie. path + name (mentioned above). 
    """
    # Check if directory was already set, ie program was ran at least once
    key_dir = 'dir'
    try:
        dir = config['General'][key_dir]
        recipe_dir = os.path.join(dir, recipe_dir_name )
        misc_dir = os.path.join(dir, misc_dir_name )
        resource_dir = os.path.join(dir, resource_dir_name )
    # If not (probably on first run), then set it to CWD
    # Except block entered on first run => directories don't exists
    except (configparser.NoSectionError, configparser.NoOptionError, KeyError):
        dir = os.getcwd()
        # Call to setup_dirs_helper() has to come before setting config
        # The function might exit, then no values should be written to config
        recipe_dir, misc_dir, resource_dir = setup_dirs_helper(dir)
        config['General'][key_dir] = os.path.expanduser(dir)

    return recipe_dir, misc_dir, resource_dir

