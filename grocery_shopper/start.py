import argparse
import configparser
import logging
import os
import sys
from grocery_shopper import main
from grocery_shopper.setup_dirs import setup_dirs
from grocery_shopper import yaml2pdf
from grocery_shopper.vars import defaults_file
from grocery_shopper.select_recipes import select_recipes


logging.basicConfig(level=logging.WARNING,
                    format='[%(levelname)s: %(asctime)s] %(message)s',
                    datefmt=' %H:%M:%S')


def start():
    grocery_shopper_dir = os.path.dirname(__file__)
    defaults_file_path = f'{grocery_shopper_dir}/{defaults_file}'
    config = configparser.ConfigParser()
    try:
        # According to Doc: Use read_file() when file is expected to exists
        with open(defaults_file_path) as config_file:
            config.read_file(config_file)
    except FileNotFoundError:
        config['General'] = {}

    p = argparse.ArgumentParser(__file__)
    p.add_argument('-n', '--num_recipes',
                   help='Number of recipes',
                   type=int)
    p.add_argument('--dir',
                   help='Top level directory. Here will all files and directories be saved.',
                   type=str)
    p.add_argument('--firefox_profile',
                   help='Path to the firefox profile.',
                   type=str)
    p.add_argument(
        '--pdf',
        metavar='recipe.yaml',
        help='Generate pdfs from yaml files using LaTeX.',
        nargs='+',
        type=str
    )
    p.add_argument(
        '--take',
        metavar='recipe.yaml',
        help='Take the following ingredients and do no random selection.',
        nargs='+',
        type=str)
    args = p.parse_args()

    # Check config for firefox profile
    key_firefox_profile = 'firefox_profile'
    if args.firefox_profile is None:
        try:
            config['General'][key_firefox_profile]
        except (configparser.NoSectionError, configparser.NoOptionError, KeyError):
            logging.error('No default firefox profile path set. Please use\n\t--firefox_profile PATH\nif it\'s your first run.')
            sys.exit(1)
    else:
        config['General'][key_firefox_profile] = os.path.expanduser(args.firefox_profile)
        # Write default values
        with open(defaults_file_path, 'w') as f:
            config.write(f)

    directories = setup_dirs(config)
    # TODO: Remove unnecessary tuple(select_recipes(…)) casts of <12-04-2024>
    #   ...without type checker complains...
    recipes = ()
    if args.num_recipes:
        if args.take and args.num_recipes > 0:
            recipes = tuple(os.path.join(directories['recipe_dir'],
                                         recipe_file)
                            for recipe_file in args.take) \
                + tuple(select_recipes(args.num_recipes,
                                       directories['recipe_dir']))
        elif args.num_recipes > 0:
            recipes = tuple(select_recipes(args.num_recipes, directories['recipe_dir']))
    elif args.take:
        recipes = tuple(os.path.join(directories['recipe_dir'], recipe_file) for recipe_file in args.take)

    if len(recipes) > 0:
        main.main(recipes, directories, config)

    if args.pdf:
        yaml2pdf.yaml2pdf(args.pdf, directories['recipe_dir'])


if __name__ == "__main__":
    start()
