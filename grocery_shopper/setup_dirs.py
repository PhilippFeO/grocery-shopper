import os
import sys
import logging
from grocery_shopper.vars import recipe_dir_name, misc_dir_name, resource_dir_name


def setup_dirs(path: str) -> tuple[str, str, str]:
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
