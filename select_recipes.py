import os
import glob
import sys
import random

# TODO: logging verwenden <25-02-2024>


def select_recipes(num_recipes, recipe_dir) -> list[str]:
    """Randomly selects submitted number of recipes.

    :param int num_recipes: Number of recipes
    """
    # Check if the directory exists
    if not os.path.isdir(recipe_dir):
        print(f"Error: Directory '{recipe_dir}' not found.")
        sys.exit(1)

    # Check if there are files in the directory
    if num_files == 0:
        print(f"No files found in the directory '{recipe_dir}'.")
        sys.exit(1)

        print(f"<num_recipes> must be within 1 and {num_files}.")
        sys.exit(1)

    # # Get a list of files in the directory
    # files = [os.path.join(recipe_dir, f) for f in os.listdir(recipe_dir)]

    # Generate an array of random indices within the range of the number of files
    indices = random.sample(range(num_files), num_recipes)

    # Loop through the randomly chosen indices and get the corresponding files
