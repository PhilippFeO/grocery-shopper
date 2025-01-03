import argparse
import configparser
import logging
import os
import sys
from pathlib import Path
from random import choice

from grocery_shopper import main, yaml2pdf
from grocery_shopper.recipe import Recipe
from grocery_shopper.select_recipes import select_recipes
from grocery_shopper.setup_dirs import setup_dirs
from grocery_shopper.vars import FIXED_MEALS, RECIPE_DIR, defaults_file

logging.basicConfig(
    level=logging.WARNING,
    format='[%(levelname)s: %(asctime)s] %(message)s',
    datefmt=' %H:%M:%S',
)


def start():
    grocery_shopper_dir = Path(__file__).parent
    defaults_file_path: Path = Path(f'{grocery_shopper_dir}/{defaults_file}')
    config = configparser.ConfigParser()
    try:
        # According to Doc: Use read_file() when file is expected to exists
        with defaults_file_path.open('r') as config_file:
            config.read_file(config_file)
    except FileNotFoundError:
        config['general'] = {}

    p = argparse.ArgumentParser(__file__)
    p.add_argument('-n', '--num-recipes', help='Number of recipes', type=int)
    p.add_argument(
        '--dir',
        help='Top level directory. Here will all files and directories be saved.',
        type=str,
    )
    p.add_argument('--firefox-profile', help='Path to the firefox profile.', type=str)
    p.add_argument(
        '--pdf',
        metavar='recipe.yaml',
        help='Generate pdfs from yaml files using LaTeX.',
        nargs='+',
        type=str,
    )
    p.add_argument(
        '--take',
        metavar='recipe.yaml',
        help='Take the following ingredients and do no random selection.',
        nargs='+',
        type=str,
    )
    args = p.parse_args()

    # Check config for firefox profile
    key_firefox_profile = 'firefox_profile'
    if args.firefox_profile is None:
        try:
            config['general'][key_firefox_profile]
        except (configparser.NoSectionError, configparser.NoOptionError, KeyError):
            logging.exception(
                "No default firefox profile path set. Please use\n\t--firefox_profile PATH\nif it's your first run.",
            )
            sys.exit(1)
    else:
        config['general'][key_firefox_profile] = str(
            Path.expanduser(args.firefox_profile),
        )
        # Write default values
        with defaults_file_path.open('w') as f:
            config.write(f)

    _ = setup_dirs(config, defaults_file_path)
    recipes: list[Recipe] = []
    # TODO: Remove unnecessary tuple(select_recipes(…)) casts of <12-04-2024>
    #   ...without type checker complains...
    # TODO: Allow user to define fixed meals <24-08-2024>
    if any(fixed_meal.is_file() for fixed_meal in FIXED_MEALS):
        pre_selected_recipe_yamls: list[Path] = [
            choice(FIXED_MEALS),  # noqa: S311
        ]
    else:
        pre_selected_recipe_yamls = []
    if args.pdf is not None:
        yaml2pdf.yaml2pdf(args.pdf)
        sys.exit(0)
    if args.num_recipes is not None:
        if args.take is not None and args.num_recipes > 0:
            pre_selected_recipe_yamls += [
                RECIPE_DIR / Path(recipe_file) for recipe_file in args.take
            ]
            recipes = select_recipes(
                args.num_recipes,
                RECIPE_DIR,
                pre_selected_recipe_yamls,
            )
        elif args.num_recipes > 0:
            recipes = select_recipes(
                args.num_recipes,
                RECIPE_DIR,
                pre_selected_recipe_yamls,
            )
    elif args.take is not None:
        pre_selected_recipe_yamls += [
            RECIPE_DIR / recipe_file for recipe_file in args.take
        ]
        recipes = [Recipe(yaml_file) for yaml_file in pre_selected_recipe_yamls]

    # recipes always contains the FIXED_MEALS (if they are any)
    main.main(recipes, config)


if __name__ == '__main__':
    start()
