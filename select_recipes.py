import os
import sys
import random
import defaults

# TODO: logging verwenden <25-02-2024>


def select_recipes(num_recipes) -> list[str]:
    """Randomly selects submitted number of recipes.

    :param int num_recipes: Number of recipes
    """
    # Check if the directory exists
    if not os.path.isdir(defaults.recipe_dir):
        print(f"Error: Directory '{defaults.recipe_dir}' not found.")
        sys.exit(1)

    # Check if there are files in the directory
    num_files = len(os.listdir(defaults.recipe_dir))
    if num_files == 0:
        print(f"No files found in the directory '{defaults.recipe_dir}'.")
        sys.exit(1)

    if 1 > num_recipes > num_files:
        print(f"<num_recipes> must be within 1 and {num_files}.")
        sys.exit(1)

    # Get a list of files in the directory
    files = [os.path.join(defaults.recipe_dir, f) for f in os.listdir(defaults.recipe_dir)]

    # Generate an array of random indices within the range of the number of files
    indices = random.sample(range(num_files), num_recipes)

    # Loop through the randomly chosen indices and get the corresponding files
    return [files[index] for index in indices]
