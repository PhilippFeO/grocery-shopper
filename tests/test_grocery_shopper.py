from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING

from grocery_shopper.retrieve_required_ingredients import retrieve_required_ingredients

if TYPE_CHECKING:
    from grocery_shopper.recipe import Ingredient

shopping_list_file: Path = Path('tests', 'shopping_list_test.txt')
icu_file: Path = Path('tests', 'ingredient_category_url_test.csv')


def filter_names(
    ingredients: list['Ingredient'],
    names: set[str],
) -> list['Ingredient']:
    return [ing for ing in ingredients if ing.name in names]


def test_parse_edited_list(all_ingredients):
    # from grocery_shopper.make_table import make_table
    # table: str = make_table(all_ingredients)
    # print(table)
    expected_final_ingredients: list[Ingredient] = filter_names(
        all_ingredients,
        {'Orange', 'Erdbeere', 'Kirsche', 'Paprika', 'Kürbis', 'Brombeere'},
    )

    final_ingredients: list[Ingredient] = retrieve_required_ingredients(
        shopping_list_file,
        all_ingredients,
    )

    assert Counter(expected_final_ingredients) == Counter(final_ingredients)
