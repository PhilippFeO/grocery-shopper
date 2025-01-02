import contextlib
import glob
import itertools
import os
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

from grocery_shopper.archive_contents import archive_contents
from grocery_shopper.handle_ing_miss_url import handle_ing_miss_cu
from grocery_shopper.make_table import make_table
from grocery_shopper.read_csv import CategoryURL, read_csv
from grocery_shopper.recipe import Recipe
from grocery_shopper.retrieve_required_ingredients import retrieve_required_ingredients
from grocery_shopper.vars import MISC_DIR, RESOURCE_DIR

if TYPE_CHECKING:
    from configparser import ConfigParser

    from grocery_shopper.recipe import Ingredient


def main(
    recipes: list['Recipe'],
    config: 'ConfigParser',
) -> None:
    """Conducts shopping process. Either callable with number of recipes to randomly select some or with list of recipes."""
    firefox_profile = config['general']['firefox_profile']
    general_dir = config['general']['dir']

    # i=ingredient, c=category, u=url
    # TODO: csv files may contain error/bad formatted entries (ie. no int were int is ecpected); Check for consistency <05-01-2024>
    # TODO: Move path to config file <17-03-2024>
    icu_file: Path = Path(general_dir) / RESOURCE_DIR / 'ingredient_category_url.csv'

    # Superlist to store ingredients from all files
    all_ingredients: list[Ingredient] = []
    all_ings_missing_cu: list[Ingredient] = []
    shopping_list_str: list[str] = []

    # File will be created in the following (programming flow, not here, s. handle_ing_miss_url.py)
    icu_dict: dict[str, CategoryURL] = {}
    with contextlib.suppress(FileNotFoundError):
        icu_dict = read_csv(icu_file)

    misc_dir = Path(general_dir) / MISC_DIR
    misc_recipes: list[Recipe] = [
        Recipe(Path(file)) for file in glob.glob(os.path.join(misc_dir, '*.yaml'))
    ]

    # Assign `category` and `url`
    # Collect ingredients without entry in the CSV
    for recipe in itertools.chain(recipes, misc_recipes):
        for ingredient in recipe.ingredients:
            if ingredient.name in icu_dict:
                ingredient.category = icu_dict[ingredient.name].category
                ingredient.url = icu_dict[ingredient.name].url
            else:
                all_ings_missing_cu.append(ingredient)

    # Collect ingredients of selected recipes to assemble shopping list string
    for recipe in recipes:
        all_ingredients += recipe.ingredients
    shopping_list_str.append(make_table(all_ingredients) + '\n' * 2)

    # I want to add a destinct heading for each file in misc_dir misc.
    # Iterating over `sys.argv[1:] + misc_files` would only be possibe with various if-statements
    # because the CLI provided files don't get a "filename" heading like `misc_files` do.
    # To many if-statements affect readability, hence two for loops and helpfer function.
    shopping_list_str.extend(
        f'{misc_recipe.name}:\n' + make_table(misc_recipe.ingredients) + '\n' * 2
        for misc_recipe in misc_recipes
    )

    # Write the shopping list
    shopping_list_file = Path('shopping_list.txt')
    shopping_list_file.write_text('\n'.join(shopping_list_str))

    # Open shopping list in $EDITOR to modify it
    # (some ingredients may already be in stock, like salt, so we can delete/don't have to buy it)
    # Set cursor on Position (3,1) for my Vi, Vim and Neovim friends :)
    # 'vi', 'vim' and 'nvim' all in 'nvim'
    if (editor := os.environ['EDITOR']) in 'nvim':
        subprocess.run([editor, '+call cursor(3, 1)', shopping_list_file])
    else:
        subprocess.run([editor, shopping_list_file])

    # Retrieve required ingredients from shopping list
    final_ingredients: list[Ingredient] = retrieve_required_ingredients(
        shopping_list_file,
        all_ingredients,
    )

    # Side effect: `Ingredient` instances in `final_ingredients` are now equipped with `url` attributes
    # => Makes printing with URL in the following possible
    urls = handle_ing_miss_cu(
        all_ings_missing_cu,
        final_ingredients,
        icu_file,
        firefox_profile,
    )

    # TODO: When printing give user the chance to reedit list <18-01-2024>
    # Print and save sorted final shopping list
    final_ingredients.sort(
        key=lambda ingredient: ingredient.name,
    )
    print('\nFinal shopping list:')
    print(
        make_table(final_ingredients),
        end='\n',
    )
    shopping_list_file.write_text(make_table(final_ingredients, with_url=True))

    # Archive shopping list and recipes
    # Return values is mainly for unit testing
    # archive_contents(shopping_list_file, general_dir, recipes)

    # Open firefox with specific profile
    # subpress warnings
    firefox = f'firefox --profile {firefox_profile}'
    # Add checkout link (to save time and avoid accidental closing of the browser window)
    urls.append('https://shop.rewe.de/checkout/basket')
    subprocess.run([*firefox.split(), *urls], stderr=subprocess.DEVNULL, check=False)

    print('\n\nEnjoy your meals and saved time! :)')
