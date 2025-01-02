from grocery_shopper.handle_ing_miss_url import handle_ing_miss_cu, query_for_url


def test_handle_ing_miss_cu_add_category_url(
    monkeypatch,
    tmp_path,
    ings_missing_cu,
    ings_with_cu,
):
    """Test for method `handle_ing_miss_cu`. Verifys that Category and URL are added to the ingredients missing these attribute (values), ie. ingredients in `ings_missing_cu`."""
    final_ingredients = ings_missing_cu + ings_with_cu
    assert any(ing.url == 'N/A-URL' for ing in final_ingredients)
    firefox_profile = ''

    monkeypatch.setattr('subprocess.Popen', lambda _: None)
    inputs = [
        'y',
        'Category 0',
        'URL-0',
        'Category 1',
        'URL-1.1 URL-1.2',
        'Category 2',
        'URL-2',
    ]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
    urls = handle_ing_miss_cu(
        ings_missing_cu,
        final_ingredients,
        icu_file=tmp_path / 'ingredient_category_url.csv',
        firefox_profile=firefox_profile,
    )
    assert all(ing.category != 'N/A-CATEGORY' for ing in final_ingredients)
    assert all(url != 'N/A-URL' for url in urls)


def test_handle_ing_miss_cu_add_no_category_url(
    monkeypatch,
    tmp_path,
    ings_missing_cu,
    ings_with_cu,
):
    """Test for method `handle_ing_miss_cu`. Verifys that Category and URL are not added to the ingredients missing these attribute (values), ie. ingredients in `ings_missing_cu` are left blank after user entered 'n'."""
    # TODO: Change name(s) of test methods <26-04-2024>
    final_ingredients = ings_missing_cu + ings_with_cu
    assert any(ing.url == 'N/A-URL' for ing in final_ingredients)
    firefox_profile = ''

    monkeypatch.setattr('builtins.input', lambda _: 'n')
    _ = handle_ing_miss_cu(
        ings_missing_cu,
        final_ingredients,
        icu_file=tmp_path / 'ingredient_category_url.csv',
        firefox_profile=firefox_profile,
    )
    assert all(ing.url == 'N/A-URL' for ing in ings_missing_cu)
    assert all(ing.url != 'N/A-URL' for ing in ings_with_cu)


def test_query_for_url(monkeypatch, tmp_path, ings_missing_cu):
    # Mock firefox call
    # None bc returned object is not used
    monkeypatch.setattr('subprocess.Popen', lambda _: None)
    inputs = [
        (cat0 := 'Category 0'),
        (url0 := 'URL-0'),
        (cat1 := 'Category 1'),
        (url1 := 'URL-1.1 URL-1.2'),
        (cat2 := 'Category 2'),
        (url2 := 'URL-2'),
    ]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

    tmp_icu_file = tmp_path / 'ingredient_category_url.csv'
    # Used in 'subprocess.run', which is mocked anyway => Argument serves no purpose at all
    firefox_profile = 'Lorem Ipsum'

    query_for_url(list(ings_missing_cu), tmp_icu_file, firefox_profile)

    ing0 = f'{ings_missing_cu[0].name},{cat0},{url0}'
    ing1 = f'{ings_missing_cu[1].name},{cat1},{url1.replace(" ", ",")}'
    ing2 = f'{ings_missing_cu[2].name},{cat2},{url2}'
    expected_contents = f'{ing0}\n{ing1}\n{ing2}\n'

    assert tmp_icu_file.read_text() == expected_contents
