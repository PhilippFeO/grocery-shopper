import random
from typing import Generator
from grocery_shopper.ingredient import Ingredient


def query_for_url(ings_miss_cu: list[Ingredient],
                  icu_file: str):
    """
    Ask user for URL of every `Ingredient` in `ing_miss_url`, append collected URLs to `icu_file` ([i]ngredient, [c]ategory, [u]rl).
    """
    icu_entries = ''
    for ing in ings_miss_cu:
        c = input(f'\nCategory of "{ing.name}": ')
        # Only change `category` if there was a "real" input ("real" == "not empty")
        # Otherwise, `category` keeps the default value set in the constructor
        if c != '':
            ing.category = c
        # Same with url
        u = input(f'URL(s) of "{ing.name}": ')
        if u != '':
            urls = u.split(' ')
            ing.url = random.sample(urls, 1)[0]
        icu_entries = icu_entries + f'{ing.name},{ing.category},{",".join(urls)}'
    # Now, all missing `category` and `url` were completed => append to CSV file
    with open(icu_file, 'a') as f:
        # Remove last '\n' char to have a continuous CSV file
        f.write(icu_entries.rstrip())


def handle_ing_miss_cu(ings_miss_cu: list[Ingredient],
                       final_ingredients: list[Ingredient],
                       icu_file: str) -> list[str]:
    """
    Initial query to give the opportunity to add `category` and `url` to the `Ingredient`s in `ings_miss_cu`.
    The `Ingredient`s are listed before user input is parsed. After all Categories and URLs were collected, they will be appended to the `icu_file` ([i]ngredient, [c]ategory, [u]rl).

    The list of **all** URLs is returned.
    """
    intersection = set(ings_miss_cu) & set(final_ingredients)
    if intersection:
        while True:
            print("Do you want to add the missing Category and URL for the following ingredients? You can add multiple URLs separated by space.\n")
            ing_names_miss_url: Generator[str, None, None] = (f'{ing.name}\n' for ing in intersection)
            join_str = '\t - '
            bullet_list_ing_miss_url: str = join_str + join_str.join(ing_names_miss_url)
            print(f'{bullet_list_ing_miss_url}')
            user_input: str = input("yes/no: ").lower()
            if user_input in {'yes', 'y'}:
                query_for_url(intersection,
                              icu_file)
                break
            elif user_input in {'no', 'n'}:
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
    # `final_ingredients` shares `Ingerdient`s from `valid_ingredients` and `ings_miss_cu` (s. `main.py`), since we are dealing with objects, **references** were passed around.
    urls = tuple(ing.url for ing in final_ingredients)
    return urls
