import glob
import os
import subprocess
from pathlib import Path
from grocery_shopper.archive_contents import archive_contents
from grocery_shopper.build_ingredients import read_icu_file
from grocery_shopper.handle_ing_miss_url import handle_ing_miss_cu
from grocery_shopper.ingredient import Ingredient
from grocery_shopper.make_table import make_table, spacing, name_col_num
from grocery_shopper.read_default_values import read_default_values
from grocery_shopper.select_recipes import select_recipes
from grocery_shopper.parse_edited_list import parse_edited_list


def main(num_recipes: int = 0,
         recipe_files: list[str] = None):
    """
    Conducts shopping process. Either callable with number of recipes to randomly select some or with list of recipes.
    """
    config = read_default_values()
    firefox_profile = config['General']['firefox_profile']
    dir = config['General']['dir']
    recipe_dir = os.path.join(dir, 'recipes')

    # TODO: Move recipe selecting into start.py and let main do the processing <11-03-2024>
    #   Currently I have the following if logic twice, addtionally it is unreadable here.
    if recipe_files and num_recipes > 0:
        recipes = tuple(os.path.join(dir, recipe_file) for recipe_file in recipe_files) \
            + select_recipes(num_recipes, recipe_dir)
    elif num_recipes > 0:
        recipes = select_recipes(num_recipes, recipe_dir)
    elif recipe_files:
        recipes = tuple(os.path.join(dir, recipe_file) for recipe_file in recipe_files)

    # i=ingredient, c=category, u=url
    # TODO: csv files may contain error/bad formatted entries (ie. no int were int is ecpected); Check for consistency <05-01-2024>
    # TODO: Move path to config file <17-03-2024>
    icu_file: str = os.path.join(dir, 'res', 'ingredient_category_url.csv')

    # Superlist to store ingredients from all files
    all_ingredients: list[Ingredient] = []
    all_ings_missing_cu: list[Ingredient] = []
    shopping_list_str = []

    # Instanciate closure
    build_ingredients = read_icu_file(icu_file)

    def collect_ingredients_helper(recipe_file):
        # `valid_ingredients` have `category` and `url`
        # `ings_missing_cu` miss `[c]ategory` and `[u]rl`
        valid_ingredients, ings_missing_cu = build_ingredients(recipe_file)
        all_ings_missing_cu.extend(ings_missing_cu)
        return sorted(valid_ingredients + ings_missing_cu,
                      key=lambda ingredient: ingredient.name)

    # TODO: As exercise: parallelize reading/parsing the recipe.yaml <05-01-2024>
    for recipe_file in recipes:
        all_ingredients.extend(collect_ingredients_helper(recipe_file))
    shopping_list_str.append(make_table(all_ingredients) + '\n' * 2)

    misc_dir = os.path.join(dir, 'misc')
    # I want to add a destinct heading for each file in misc_dir misc.
    # Iterating over `sys.argv[1:] + misc_files` would only be possibe with various if-statements
    # because the CLI provided files don't get a "filename" heading like `misc_files` do.
    # To many if-statements affect readability, hence two for loops and helpfer function.
    for file in glob.glob(os.path.join(misc_dir, '*.yaml')):
        misc_ingredients = collect_ingredients_helper(file)
        all_ingredients.extend(misc_ingredients)
        shopping_list_str.append(f'{Path(file).stem}:\n' +
                                 make_table(misc_ingredients) +
                                 '\n' * 2)

    # Write the shopping list
    shopping_list_file = 'shopping_list.txt'
    with open(shopping_list_file, 'w') as slf:
        # for partial_shopping_list in shopping_list_str:
        #     slf.write(partial_shopping_list)
        slf.writelines((f'{partial_shopping_list}\n' for partial_shopping_list in shopping_list_str))

    # Open shopping list in $EDITOR to modify it
    # (some ingredients may already be in stock, like salt, so we can delete/don't have to buy it)
    # Set cursor on Position (3,1) for my Vi, Vim and Neovim friends :)
    if (editor := os.environ['EDITOR']) in {'vi', 'vim', 'nvim'}:
        subprocess.run([editor, '+call cursor(3, 1)', shopping_list_file])
    else:
        subprocess.run([editor, shopping_list_file])

    final_ingredients: list[Ingredient] = parse_edited_list(shopping_list_file, all_ingredients)

    # Side effect: `Ingredient` instances in `final_ingredients` are now equipped with `url` attributes
    # => Makes printing with URL in the following possible
    urls = handle_ing_miss_cu(all_ings_missing_cu,
                              final_ingredients,
                              icu_file)

    # TODO: When printing give user the chance to reedit list <18-01-2024>
    # Print and save sorted final shopping list
    final_ingredients_sorted = sorted(final_ingredients,
                                      key=lambda ingredient: ingredient.name)
    print("\nFinal shopping list:")
    print(make_table(final_ingredients_sorted),
          sep='\n',
          end='\n')
    with open(shopping_list_file, 'w') as slf:
        slf.write(make_table(final_ingredients_sorted,
                             with_url=True))

    # Archive shopping list and recipes
    archive_contents(shopping_list_file, recipe_dir, recipes)

    # Open firefox with specific profile
    # subpress warnings
    firefox = f"firefox --profile {firefox_profile}"
    # subprocess.run([editor, shopping_list_file])
    subprocess.run([*firefox.split(' '), *urls], stderr=subprocess.DEVNULL)

    print('\n\nEnjoy your meals and saved time! :)')


if __name__ == "__main__":
    main()
