from pathlib import Path

import pytest

from grocery_shopper.recipe import Ingredient, Recipe


@pytest.fixture
def ings_missing_cu():
    orange = Ingredient(
        'Orange',
        '2',
        meal='Testgericht',
    )
    erdbeere = Ingredient(
        'Erdbeere',
        '5',
        meal='Testgericht',
    )
    rotkohl = Ingredient(
        'Rotkohl',
        '500g',
        meal='misc-test',
    )
    return orange, erdbeere, rotkohl


@pytest.fixture
def ings_with_cu():
    kirsche = Ingredient(
        'Kirsche',
        '16',
        optional=False,
        category='Obst',
        url='https://de.wikipedia.org/wiki/Vogelkirsche_(Baum)',
        meal='Testgericht',
    )
    paprika = Ingredient(
        'Paprika',
        '1',
        optional=True,
        category='Gemüse',
        url='https://de.wikipedia.org/wiki/Paprika',
        meal='Testgericht',
    )
    gurke = Ingredient(
        'Gurke',
        '2',
        optional=True,
        category='Gemüse',
        url='https://de.wikipedia.org/wiki/Gurke',
        meal='misc-test',
    )
    brombeere = Ingredient(
        'Brombeere',
        '150g',
        optional=True,
        category='Gemüse',
        url='https://de.wikipedia.org/wiki/Brombeere',
        meal='misc-test',
    )
    return kirsche, paprika, gurke, brombeere


@pytest.fixture
def all_ingredients(ings_missing_cu, ings_with_cu):
    return *ings_missing_cu, *ings_with_cu


@pytest.fixture
def recipes():
    recipes: list[Recipe] = [
        Recipe(Path('tests', recipe_yaml))
        for recipe_yaml in ('Testgericht_0.yaml', 'Testgericht_1.yaml')
    ]
    return recipes
