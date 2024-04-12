from collections.abc import Iterable
import os
import glob
import sys
import random
import logging
from pathlib import Path


def select_recipes(num_recipes, recipe_dir) -> Iterable[str]:
    """Randomly selects submitted number of recipes.

    :param int num_recipes: Number of recipes
    :param str recipe_dir: Directory containing all recipes
    """
    # Check if the directory exists
    if not os.path.isdir(recipe_dir):
        logging.error(f"Directory '{recipe_dir}' not found.")
        sys.exit(1)

    # Check if there are files in the directory
    num_files = len((yaml_files := glob.glob(os.path.join(recipe_dir, '*.yaml'))))
    if num_files == 0:
        logging.error(f"No yaml-files found in the directory '{recipe_dir}'.")
        sys.exit(1)

    if num_recipes < 1 or num_files < num_recipes:
        logging.error(f"<num_recipes> must be within 1 and {num_files}, but was {num_recipes}.")
        sys.exit(1)

    # Generate an array of random indices within the range of the number of files
    recipe_indices = random.sample(range(num_files), num_recipes)
    selection = [yaml_files[i] for i in recipe_indices]

    while True:
        print('The following recipes were chosen:')
        for idx, recipe_path in enumerate(selection):
            recipe_name = Path(recipe_path).stem.replace('_', ' ')
            print(f'\t{idx + 1}. {recipe_name}')
        print('Proceed: yes/y\n',
              f'Reselect: {"/".join(str(i) for i in range(num_recipes+1))} (0 = all)',
              sep='')
        # Check for admissible inputs
        admissible = ', '.join(['yes', 'y', 'all'] + [str(i) for i in range(num_recipes+1)])
        while (user_input := input("Input: ").lower()) not in admissible:
            print(f"Invalid input. Please enter one of the following:\n\t{admissible}")
        # Asses user input
        if user_input in {'yes', 'y'}:
            break
        elif user_input in {'0', 'all'}:
            recipe_indices = random.sample(range(num_files), num_recipes)
            selection = [yaml_files[i] for i in recipe_indices]
        # User inserted a valid number
        else:
            # Select new recipe until a different one was chosen
            # TODO: Remove potential of running indefinetly <17-03-2024>
            user_input = int(user_input) - 1
            while recipe_indices[user_input] == (new_recipe_index := random.sample(range(num_files), 1)[0]):
                continue
            selection[user_input] = yaml_files[new_recipe_index]
        print()

    return selection
