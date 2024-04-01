import yaml
import logging
from grocery_shopper.read_csv import read_csv
from typing import Callable
from grocery_shopper.ingredient import Ingredient


def read_icu_file(icu_file: str) -> Callable[str, tuple[list[Ingredient], list[Ingredient]]]:
    """
    Uses a closure. Reads the ingredient_category_url.csv file and returns a function. This function has access
    to the constructed dictionary.
    """
    icu_dict: dict[str, tuple[str, str]] = {}
    try:
        icu_dict = read_csv(icu_file)
    except FileNotFoundError:
        # File will be created in the following (programming flow, not here, s. handle_ing_miss_url.py)
        pass

    def build_ingredients_inner(recipe_file: str) -> tuple[list[Ingredient], list[Ingredient]]:
        """
        Builds the ingredient list of a recipe by parsing the yaml file and adding
        the information from the corresponding CSV files, namely `category` and `url`.

        The function will return two lists, the first holding `Ingredient`s with valid `category` and `url` attributes, the latter with predefined ones.
        This necessary to ask the user for completing the data.

        I know, there are other methods to store objects but Text (in comparison to binary) gives the user the opportunity to edit the data.
        Additionally, this surely becomes necessary because nobody can guarantee that an URL will stay valid. The vendor might change it.
        """
        recipe_data = None
        with open(recipe_file, 'r') as file:
            recipe_data = yaml.safe_load(file)
        recipe_name = recipe_data.get('recipe', [])[0]['name']

        ings_with_cu: list[Ingredient] = []
        # User will be asked to provide `[c]ategory` and `[u]rl`
        ings_missing_cu: list[Ingredient] = []
        # Build ingredients
        # get() returns list of dicts resembling an ingredient as defined in the corresponding yaml file
        for name_quantity_optional in recipe_data.get("ingredients", []):
            # Retrive information from CSV files ('category', 'url')
            # Check for 'KeyError' in all CSV files
            try:
                # If URL is missing, it will be added later by the user
                category = icu_dict[
                    (ingredient_name := name_quantity_optional['name'])
                ][0]
                urls = icu_dict[ingredient_name][1]
            except KeyError:
                logging.info(f'Ingredient "{ingredient_name}" missing in "{icu_file}". Default value for <category> will be used.')
                ings_missing_cu.append(
                    Ingredient(**name_quantity_optional,
                               meal=recipe_name))
                continue
            ings_with_cu.append(
                Ingredient(**name_quantity_optional,
                           category=category,
                           urls=urls,
                           meal=recipe_name))
        return ings_with_cu, ings_missing_cu
    return build_ingredients_inner
