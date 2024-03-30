from grocery_shopper.handle_ing_miss_url import query_for_url
from grocery_shopper.ingredient import Ingredient


def test_query_for_url(monkeypatch, tmp_path):
    ings_miss_cu = [Ingredient((ing1_name := 'Ingredient 1'), '5 Pieces'),
                    Ingredient((ing2_name := 'Ingredient 2'), '400g')]
    icu_file = tmp_path / 'ingredient_category_url.csv'
    # print(icu_file)

    inputs = [(cat1 := 'Category 1'), (url1 := 'URL-1'),
              (cat2 := 'Category 2'), (url2 := 'URL-2.1 URL-2.2')]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
    query_for_url(ings_miss_cu, icu_file)

    expected_contents = f'{ing1_name},{cat1},{url1}\n{ing2_name},{cat2},{url2.replace(" ", ",")}'
    assert icu_file.read_text() == expected_contents
