import argparse
import configparser
import logging
import os
import sys
from grocery_shopper import main
from grocery_shopper.setup_dirs import setup_dirs
from grocery_shopper import yaml2pdf
from grocery_shopper.vars import defaults_file


logging.basicConfig(level=logging.WARNING,
                    format='[%(levelname)s: %(asctime)s] %(message)s',
                    datefmt=' %H:%M:%S')


def start():
    grocery_shopper_dir = os.path.dirname(__file__)
    defaults_file_path = f'{grocery_shopper_dir}/{defaults_file}'
    config = configparser.ConfigParser()
    try:
        # According to Doc: Use read_file() when file is expected to exists
        config.read_file(open(defaults_file_path))
    except FileNotFoundError:
        config['General'] = {}

    p = argparse.ArgumentParser(__file__)
    p.add_argument('-n', '--num_recipes',
                   help='Number of recipes',
                   type=int)
    p.add_argument(f'--dir',
                   help='Top level directory. Here will all files and directories be saved.',
                   type=str)
    p.add_argument(f'--firefox_profile',
                   help='Path to the firefox profile.',
                   type=str)
    p.add_argument('--make-pdf',
                   metavar='recipe.yaml',
                   help='Generate pdfs from yaml files using LaTeX.',
                   nargs='+',
                   type=str)
    p.add_argument('--take',
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

    recipe_dir, misc_dir, resource_dir = setup_dirs(config)

    # Write default values
    with open(defaults_file_path, 'w') as f:
        config.write(f)

    # Abfahrt
    if args.take and args.num_recipes:
        main.main(num_recipes=args.num_recipes, recipe_files=args.take)
    elif args.num_recipes:
        main.main(num_recipes=args.num_recipes)
    elif args.take:
        main.main(recipe_files=args.take)
    elif args.make_pdf:
        yaml2pdf.yaml2pdf(args.make_pdf, recipe_dir, resource_dir)


if __name__ == "__main__":
    start()
