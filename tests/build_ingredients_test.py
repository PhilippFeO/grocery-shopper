import os
from grocery_shopper.build_ingredients import read_icu_file
from grocery_shopper.ingredient import Ingredient


def test_build_ingredients():
    icu_file = os.path.join('tests', 'icu_build_ingredients.csv')
    build_ingredients = read_icu_file(icu_file)
    recipe_file = os.path.join('tests', 'recipe_build_ingredients.yaml')
    ings_with_cu, ings_missing_cu = build_ingredients(recipe_file)

    kirsche = Ingredient('Kirsche',
                         16,
                         optional=False,
                         category='Obst',
                         url='https://de.wikipedia.org/wiki/Vogelkirsche_(Baum)',
                         meal='Testgericht für build_ingredients_test.py')
    paprika = Ingredient('Paprika',
                         1,
                         optional=True,
                         category='Gemüse',
                         url=['https://de.wikipedia.org/wiki/Paprika', 'https://de.wikipedia.org/wiki/Nachtschattengew%C3%A4chse'],
                         meal='Testgericht für build_ingredients_test.py')
    orange = Ingredient('Orange', 2, meal='Testgericht für build_ingredients_test.py')
    erdbeere = Ingredient('Erdbeere', 5, meal='Testgericht für build_ingredients_test.py')

    assert len(ings_missing_cu) == 2
    assert orange in ings_missing_cu
    assert erdbeere in ings_missing_cu

    assert len(ings_with_cu) == 2
    assert kirsche in ings_with_cu
    assert paprika in ings_with_cu
