# Grocery Shopper
No more "What should I eat for dinner today?" and manually buying ingredients ever again! Recipes are selected randomly and a firefox instance will open to buy the necessary ingredients online [1] – Deciding and grocery shopping in one step!


## Installation
A non technical prerequisite is a supermarket or delivery service with the possibility to buy online.

Clone the git repository (wherever you like):
```sh
git clone https://github.com/PhilippFeO/grocery_shopper
```
Then, instanciate a new virtual enviornment, change into the `grocery_shopper` directory and run `pip install .`. It will create the `grocery-shopper` command, try running `grocery-shopper -h`. A classical installation via `pip` will follow soon. 


## How it works
1. Create a firefox profile for grocery shopping only [2].

2. Clone this repository where you want:
```sh
git clone https://github.com/PhilippFeO/grocery-shopper
```

3. Run (in the cloned repository) `pip install -e .`

4. Create/Enter the directory where `grocery_shopper` shall operate, fi. `~/Documents/grocery_shopper`. The programm will generate some folders on first invocation.

5. Run `grocery_shopper --firefox_profile PATH` where `PATH` points to the in step 1 created profile.

6. Create some recipes (s. below). 

7. Run `grocery-shopper -n NUM_RECIPES` to randomly select `NUM_RECIPES` recipes you want to cook.

8. The programm will parse the randomly chosen recipes and open the default text editor (`$EDITOR`) with all ingredients. There you can delete the ingredients you already have in stock. Save and quit after you are done. 

9. The URLs for each ingredient are looked up. If it can't find one for the specific ingredient, it will ask you to manually add one or multiple separated by space via the command line. The submitted link(s) are saved separately from the recipe. Ingredient name and link(s) are written in a destinct file under `.resoures/`. This directory will be created next to `recipes/` and `misc/`. 

10. After all URLs were collected, Firefox opens the URLs in tabs using your new profile. 

8. The final shopping list (ie. the contents of the buffer you edited with `$EDITOR`) and the recipes are archived (`./archive/`) and a sym link (`Selection`) is created (to have some traceability). All next to `recipes/` and `misc/`. 


## Structure of your recipes
Recipes need to be saved as `yaml` files and have the following parts, `recipe` and `ingredients` are mandatory.
```yaml
recipe:
    - name: Spaghetti Bolognese
ingredients:
    - name: Spaghetti
      quantity: 250g
    - name: Tomato(s)
      quantity: 5
    - name: Zucchini
      quantity: 1
      optional: true # Optional ingredients are possible!
    ...
preparation:
    - 1. Cook the Spaghetti.
    - 2. Produce a Tomatosauce.
    ...
```

A recipes of the `misc/` category could look like
```yaml
recipe:
    - name: Breakfast
ingredients:
    - name: Milk
      quantity: 2l # You can use any unit you want [3]
    - name: Granola
      quantity: 500g
    - name: Honey
      quantity: 100g
      optional: true
    ...
# 'preparation' is optional
```

`misc/` is for stuff needed every time or irregulary (like hygiene products) when you go grocery shopping. To put it bluntly, for things you don't want to rely on the random generator to choose them.


## Additional CLI options
- `--make-pdf`: With `grocery-shopper --make-pdf recipe_1.yaml recipe_2.yaml ...` you can generate `pdf`s from your `yaml`-recipes. Have shell expansion in mind, ie. `grocery-shopper --make-pdf recipes/*.yaml` to process all at once. Files are stored in `recipes/pdf/`. Optional ingredients are printed in gray. Requires a LaTeX installation, s. [compile_recipe.sh](./grocery_shopper/compile_recipe.sh) for at least some information (I'm no LaTeX expert).
- `--take`: By `--take recipe_1.yaml ...` you circumvent randomly selecting by providing the recipes you want to cook directly. Can be used with `-n`/`--num-recipes` in conjunction.


## Syntax completion for Neovim
- I have written a source for Neovim, ie. [nvim-cmp](https://github.com/hrsh7th/nvim-cmp), which completes the ingredients. You can find it in my Repos or [here](https://github.com/PhilippFeO/cmp-csv). Having syntax completion provides you from typos, duplication and remembering which `Ingredient` is already with URL available.

## Syntax completion for bash
Append the contents of [syntax_completion.sh](./syntax_completion.sh) to you `~/.bashrc` to enable auto completion for the recipes in your `recipes/` directory. In case you don't use `~/Documents/grocery_shopper`, you have to exchange the value of `recipe_dir` in the script. Auto completion is not activated automatically bis `pip intall -e .`! You have to do it manually.


## Some thoughts on 6.
It is also possible to provide the URL as a field (`url`) in the `yaml` of the recipe but then we have to provide the URL each time using the `Ingredient` across each recipe. By having a separate file storing `Ingredient.name` (`.name` since only the string is used in this case) and it's URL, we have one source of truth. This is quite handy if URLs change, because then we have to edit it once and not in each recipe. The combination is saved under `res/ingredient_category_url.csv`. Having plain text/csv and no binary gives us the opportunity to easily make changes afterwards. An additional benefit is that this speeds up creating a new recipe since most `Ingredient`s are already provided with an URL and wo don't have to insert the same information again and again. It is also possible to add multiple URLs for an ingredients (then the link is randomly chosen), to buy varying instance of the same product (different noodles, apples, ...).

---

[1]: At least in Germany it is possible to buy food online at some vendors like Rewe, knuspr and Flink. Especially Rewe is handy, because an App is not necessary and can be done with the desktop browser.

[2]: If you don't know how to create a new profile, check: https://support.mozilla.org/en-US/kb/profile-manager-create-remove-switch-firefox-profiles?redirectslug=profile-manager-create-and-remove-firefox-profiles&redirectlocale=en-US Keep in mind, that this profile is automatically the default one. So, you have to select your previous profile as standard afterwards. The directory of the profile(s) are also listed on this page. Just copy and paste.

[3]: Please start using metric.

