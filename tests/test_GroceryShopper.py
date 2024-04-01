from grocery_shopper.build_ingredients import read_icu_file
from grocery_shopper.ingredient import Ingredient
from grocery_shopper.handle_ing_miss_url import query_for_url
import os
import pytest
from collections import Counter


class TestGroceryShopper():

    """This class is for testing 'grocery-shopper'."""

    icu_file = os.path.join('tests', 'test_ingredient_category_url.csv')

    @pytest.fixture
    def ings_missing_cu(self):
        return [Ingredient('Orange', 2, meal='Testgericht für build_ingredients_test.py'),
                Ingredient('Erdbeere', 5, meal='Testgericht für build_ingredients_test.py')]

    @pytest.fixture
    def ings_with_cu(self):
        ing_kirsche = Ingredient('Kirsche',
                                 16,
                                 optional=False,
                                 category='Obst',
                                 url='https://de.wikipedia.org/wiki/Vogelkirsche_(Baum)',
                                 meal='Testgericht für build_ingredients_test.py')
        ing_paprika = Ingredient('Paprika',
                                 1,
                                 optional=True,
                                 category='Gemüse',
                                 url=['https://de.wikipedia.org/wiki/Paprika', 'https://de.wikipedia.org/wiki/Nachtschattengew%C3%A4chse'],
                                 meal='Testgericht für build_ingredients_test.py')
        return [ing_paprika, ing_kirsche]

    def test_query_for_url(self, monkeypatch, tmp_path, ings_missing_cu):
        inputs = [(cat1 := 'Category 1'), (url1 := 'URL-1'),
                  (cat2 := 'Category 2'), (url2 := 'URL-2.1 URL-2.2')]
        monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

        tmp_icu_file = tmp_path / 'ingredient_category_url.csv'
        # print(icu_file)

        query_for_url(ings_missing_cu, tmp_icu_file)

        expected_contents = f'{ings_missing_cu[0].name},{cat1},{url1}\n{ings_missing_cu[1].name},{cat2},{url2.replace(" ", ",")}'
        assert tmp_icu_file.read_text() == expected_contents

    def test_build_ingredients(self, ings_missing_cu, ings_with_cu):
        build_ingredients = read_icu_file(self.icu_file)
        recipe_file = os.path.join('tests', 'recipe_build_ingredients.yaml')
        ings_with_cu_built, ings_missing_cu_built = build_ingredients(recipe_file)

        assert Counter(ings_missing_cu) == Counter(ings_missing_cu_built)
        assert Counter(ings_with_cu) == Counter(ings_with_cu_built)
