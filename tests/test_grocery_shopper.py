from grocery_shopper.build_ingredients import read_icu_file
from grocery_shopper.ingredient import Ingredient
from grocery_shopper.handle_ing_miss_url import query_for_url
from grocery_shopper.parse_edited_list import parse_edited_list
import os
from collections import Counter

shopping_list_file: str = os.path.join('tests',
                                       'shopping_list_test.txt')
icu_file: str = os.path.join('tests',
                             'ingredient_category_url_test.csv')


def filter_names(ingredients: list[Ingredient], names: set[str]) -> list[Ingredient]:
    return [ing for ing in ingredients if ing.name in names]


def test_query_for_url(monkeypatch, tmp_path, ings_missing_cu):
    # Mock firefox call
    # None bc returned object is not used
    monkeypatch.setattr('subprocess.run', lambda _: None)
    inputs = [(cat0 := 'Category 0'), (url0 := 'URL-0'),
              (cat1 := 'Category 1'), (url1 := 'URL-1.1 URL-1.2'),
              (cat2 := 'Category 2'), (url2 := 'URL-2')]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

    tmp_icu_file = tmp_path / 'ingredient_category_url.csv'
    # Used in 'subprocess.run', which is mocked anyway => Argument serves no purpose at all
    firefox_profile = 'Lorem Ipsum'

    query_for_url(list(ings_missing_cu), tmp_icu_file, firefox_profile)

    ing0 = f'{ings_missing_cu[0].name},{cat0},{url0}'
    ing1 = f'{ings_missing_cu[1].name},{cat1},{url1.replace(" ", ",")}'
    ing2 = f'{ings_missing_cu[2].name},{cat2},{url2}'
    expected_contents = '\n'.join((ing0, ing1, ing2))

    assert tmp_icu_file.read_text() == expected_contents


def test_build_ingredients(ings_missing_cu, ings_with_cu):
    expected_ings_missing_cu = filter_names(ings_missing_cu, {"Orange", "Erdbeere"})
    expected_ings_with_cu = filter_names(ings_with_cu, {"Kirsche", "Paprika"})
    build_ingredients = read_icu_file(icu_file)
    recipe_file = os.path.join('tests', 'recipe_build_ingredients.yaml')

    bi_ings_with_cu, bi_ings_missing_cu = build_ingredients(recipe_file)

    assert Counter(expected_ings_missing_cu) == Counter(bi_ings_missing_cu)
    assert Counter(expected_ings_with_cu) == Counter(bi_ings_with_cu)


def test_parse_edited_list(all_ingredients):
    # from grocery_shopper.make_table import make_table
    # table: str = make_table(all_ingredients)
    # print(table)
    expected_final_ingredients: list[Ingredient] = filter_names(all_ingredients, {"Orange", "Erdbeere", "Kirsche", "Paprika", "Kürbis", "Brombeere"})

    final_ingredients: list[Ingredient] = parse_edited_list(shopping_list_file, all_ingredients)

    assert Counter(expected_final_ingredients) == Counter(final_ingredients)
