import subprocess
from typing import TYPE_CHECKING, NamedTuple

from grocery_shopper.make_table import name_col_num, spacing

if TYPE_CHECKING:
    from pathlib import Path

    from grocery_shopper.recipe import Ingredient


class IngNQ(NamedTuple):
    name: str
    quantity: str


def retrieve_required_ingredients(
    shopping_list_file: 'Path',
    all_ingredients: list['Ingredient'],
) -> list['Ingredient']:
    # Filter final ingredients for `name` and `quantity`
    # Dont hardcode column number, otherwise changes have to be adapted here again => annoying
    # Keep `name` column and `quantity` column (the following one)
    # Insert `•` as separator
    awk_output = subprocess.run(
        [
            '/usr/bin/awk',
            '-F',
            f' {{{spacing},}}',
            f'{{print ${name_col_num}, "•", ${name_col_num + 1}}}',
            shopping_list_file,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    # Firt two entries are "Name" and "" (empty line) due to header
    # awk adds '\n', hence there is an empty string entry on the last index
    # I dont know why awk does it and I dont care
    # list[str]!!! The edited table was splitted above and 'final_ingerdients' contains the names of the ingredients, not the objects!
    # TODO: Consistency checks for the remaining lines <17-01-2024>
    final_ingredient_names: list[str] = awk_output.stdout.split('\n')[:-1]
    final_ingredient_names = [
        e for e in final_ingredient_names if e not in {' • ', 'Name • Menge'}
    ]
    # Transform list of "name • quantity"-strings into list of tuples with (name, quantity) entries
    ing_nqs = (
        IngNQ(name.strip(), quantity.strip())
        for name, quantity in (fin.split('•') for fin in final_ingredient_names)
    )
    # Filter `all_ingredients` to keep described ones by `final_ingredient_names`
    #   "described" because `final_ingredient_names` holds only strings (and not `Ingredient`s)
    final_ingredients: list[Ingredient] = []
    for ing_nq in ing_nqs:
        for ingredient in all_ingredients:
            if (
                ingredient.name == ing_nq.name
                and ingredient.quantity == ing_nq.quantity
            ):
                final_ingredients.append(ingredient)
                break

    return final_ingredients
