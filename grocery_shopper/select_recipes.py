import glob
import logging
import os
import random
import sys
from pathlib import Path

from grocery_shopper.recipe import Recipe
from grocery_shopper.vars import FIXED_MEALS


def select_recipes(
    num_recipes: int,
    recipe_dir: Path,
    pre_selected_recipe_yamls: list[Path],
) -> list[Recipe]:
    """Randomly selects submitted number of recipes.

    :param int num_recipes: Number of recipes
    :param str recipe_dir: Directory containing all recipes
    """
    # Check if the directory exists
    if not Path(recipe_dir).is_dir():
        msg = f"Directory '{recipe_dir}' not found."
        logging.error(msg)
        sys.exit(1)

    # Collect all yaml files
    yaml_files_glob: list[str] = glob.glob(os.path.join(recipe_dir, '*.yaml'))  # noqa: PTH118
    # Remove 'FIXED_MEALS' to avoid one fixed meal twice
    yaml_files: list[Path] = [
        yf
        for yaml_file in yaml_files_glob
        if (yf := Path(yaml_file)).name not in [fm.name for fm in FIXED_MEALS]
    ]
    # Check if yaml files were found
    num_files = len(yaml_files)
    assert (
        num_files != 0
    ), f"No yaml-files found in directory '{recipe_dir}'. Just add some."
    assert (
        1 <= num_recipes <= num_files
    ), f'<num_recipes> must be within 1 and {num_files}, but was {num_recipes}.'

    recipes: list[Recipe] = [Recipe(recipe) for recipe in pre_selected_recipe_yamls]

    while True:
        # Generate an array of random indices within the range of the number of files
        recipe_indices = random.sample(range(num_files), num_recipes)
        # Turn every selected yaml file into a Recipe instance
        selection: list[Recipe] = [Recipe(yaml_files[i]) for i in recipe_indices]
        selection += recipes

        print('The following recipes were chosen:')
        for idx, recipe in enumerate(selection):
            print(f'\t{idx + 1}. {recipe.name}')
        print(
            'Proceed: yes/y\n',
            f'Reselect: {"/".join(str(i) for i in range(1, num_recipes+1))} (0 = all)',
            sep='',
        )

        # Check for admissible inputs
        admissible = {'yes', 'y', 'all'} | {str(i) for i in range(num_recipes + 1)}
        while (user_input := input('Input: ').lower()) not in admissible:
            print(f'Invalid input. Please enter one of the following:\n\t{admissible}')

        # Asses user input
        if user_input in {'yes', 'y'}:
            break
        if user_input in {'0', 'all'}:
            continue
        # User inserted a valid number
        else:
            # Select new recipe until a different one was chosen
            # TODO: Remove potential of running indefinetly <17-03-2024>
            user_input = int(user_input) - 1
            while recipe_indices[user_input] == (
                new_recipe_index := random.sample(range(num_files), 1)[0]
            ):
                continue
            selection[user_input] = Recipe(yaml_files[new_recipe_index])
        print()

    return selection
