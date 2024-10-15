import glob
import logging
import os
import random
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from grocery_shopper.vars import FIXED_MEALS

if TYPE_CHECKING:
    from collections.abc import Iterable


def select_recipes(num_recipes, recipe_dir, recipes: list[Path]) -> "Iterable[Path]":
    """Randomly selects submitted number of recipes.

    :param int num_recipes: Number of recipes
    :param str recipe_dir: Directory containing all recipes
    """
    # Check if the directory exists
    if not Path(recipe_dir).is_dir():
        logging.error(f"Directory '{recipe_dir}' not found.")
        sys.exit(1)

    # Check if there are files in the directory
    yaml_files = glob.glob(os.path.join(recipe_dir, '*.yaml'))
    # Removed 'FIXED_MEALS' to avoid one fixed meal twice
    yaml_files = [yaml_file for yaml_file in yaml_files if Path(yaml_file).name not in [fixed_meal.name for fixed_meal in FIXED_MEALS]]
    num_files = len(yaml_files)
    if num_files == 0:
        logging.error(f"No yaml-files found in directory '{recipe_dir}'. Just add one.")
        sys.exit(1)

    if num_recipes < 1 or num_files < num_recipes:
        logging.error(f"<num_recipes> must be within 1 and {num_files}, but was {num_recipes}.")
        sys.exit(1)

    # Generate an array of random indices within the range of the number of files
    recipe_indices = random.sample(range(num_files), num_recipes)
    selection = [Path(yaml_files[i]) for i in recipe_indices]

    while True:
        print('The following recipes were chosen:')
        for idx, recipe_path in enumerate(recipes + selection):
            recipe_name = Path(recipe_path).stem.replace('_', ' ')
            print(f'\t{idx + 1}. {recipe_name}')
        print('Proceed: yes/y\n',
              f'Reselect: {"/".join(str(i) for i in range(num_recipes+1))} (0 = all)',
              sep='')

        # Check for admissible inputs
        admissible = {'yes', 'y', 'all'} | {str(i) for i in range(num_recipes+1)}
        while (user_input := input("Input: ").lower()) not in admissible:
            print(f"Invalid input. Please enter one of the following:\n\t{admissible}")

        # Asses user input
        if user_input in {'yes', 'y'}:
            break
        if user_input in {'0', 'all'}:
            recipe_indices = random.sample(range(num_files), num_recipes)
            selection = [Path(yaml_files[i]) for i in recipe_indices]
        # User inserted a valid number
        else:
            # Select new recipe until a different one was chosen
            # TODO: Remove potential of running indefinetly <17-03-2024>
            user_input = int(user_input) - 1
            while recipe_indices[user_input] == (new_recipe_index := random.sample(range(num_files), 1)[0]):
                continue
            selection[user_input] = Path(yaml_files[new_recipe_index])
        print()

    return selection
