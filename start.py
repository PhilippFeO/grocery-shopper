import argparse
import sys
import defaults
import configparser


def start():
    config = configparser.ConfigParser()
    config.read('defaults.ini')
    p = argparse.ArgumentParser(__file__)
    p.add_argument("--recipe_dir2",
                   nargs=1,
                   help="Directory containing the recipes as yaml files",
                   type=str,
                   required=False)
    args = p.parse_args()
    recipe_dir = args.recipe_dir2
    if recipe_dir is None:
        try:
            recipe_dir = config.get('General', 'recipe_dir2')
        except (configparser.NoSectionError, configparser.NoOptionError):
            print('No default recipe directory set. Please use\n\t--recipe_dir RECIPE_DIR')
    else:
        config.set('General', 'recipe_dir2', recipe_dir)

    # p.add_argument("--firefox_profile_path",
    #                nargs=1,
    #                help="Directory containing the recipes as yaml files",
    #                type=str,
    #                required=False)
    args = p.parse_args()


if __name__ == "__main__":
    start()

"""
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Accessing values
recipes_directory = config.get('General', 'recipes_directory')
default_value = config.getint('General', 'default_value')
"""
