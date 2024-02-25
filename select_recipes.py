import os
import glob
import sys
import random
import logging


def select_recipes(num_recipes, recipe_dir) -> list[str]:
    """Randomly selects submitted number of recipes.

    :param int num_recipes: Number of recipes
    """
    # Check if the directory exists
    if not os.path.isdir(recipe_dir):
        logging.error(f"Directory '{recipe_dir}' not found.")
        sys.exit(1)

    # Check if there are files in the directory
    yaml_files = glob.glob(os.path.join(recipe_dir, '*.yaml'))
    num_files = len(yaml_files)
    if num_files == 0:
        logging.error(f"No yaml-files found in the directory '{recipe_dir}'.")
        sys.exit(1)

    if num_recipes < 1 or num_files < num_recipes:
        logging.error(f"<num_recipes> must be within 1 and {num_files}, but was {num_recipes}.")
        sys.exit(1)

    # Generate an array of random indices within the range of the number of files
    indices = random.sample(range(num_files), num_recipes)

    # Loop through the randomly chosen indices and get the corresponding files
    return [yaml_files[index] for index in indices]
