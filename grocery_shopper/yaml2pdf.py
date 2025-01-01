import logging
import shutil
import subprocess
from itertools import zip_longest
from math import ceil
from pathlib import Path

from grocery_shopper.recipe import Ingredient, Recipe
from grocery_shopper.vars import RECIPE_DIR


class RecipeYaml2Pdf(Recipe):
    def __init__(self, recipe_yaml):
        super().__init__(recipe_yaml)

    @staticmethod
    def color_ingredient(ing: Ingredient | None) -> str:
        """Dye optional ingredients gray."""
        if ing is not None and ing.optional:
            s = f'\\textcolor{{gray}}{{- {ing.quantity} {ing.name}}}'
        elif ing:
            s = f'- {ing.quantity} {ing.name}'
        else:
            s = ''
        return s

    def to_latex(self):
        # TODO: Write strings to pipe, read form pipe in latex file <06-02-2024>
        # Recipe title
        Path('/tmp', 'title.tex').write_text(self.name)  # noqa: S108
        # Preparation
        Path('/tmp', 'preparation.tex').write_text(  # noqa: S108
            ''.join(f'\\item {step.step_desc_latex}\n' for step in self.preparation),
        )

        # Ingredients
        table_body = ''

        # `sorted()` sets False before True
        ings_sorted = sorted(self.ingredients, key=lambda ing: ing.optional)
        # I prefere having optional (gray) ingredients in the right column, ie. I have to split
        # `ings_sorted` in half and align both sublists as columns or do some index mangling.
        # In case of odd number of ingredients, `fillvalue` enhances the second shorter iterable
        middle_idx = ceil(len(ings_sorted) / 2)
        for ing1, ing2 in zip_longest(
            ings_sorted[:middle_idx],
            ings_sorted[middle_idx:],
            fillvalue=None,
        ):
            ing1_as_field, ing2_as_field = (
                self.color_ingredient(ing1),
                self.color_ingredient(ing2),
            )
            table_row = f'{ing1_as_field} & {ing2_as_field}\\\\\n'
            table_body += table_row
        Path('/tmp', 'ingredients.tex').write_text(table_body)  # noqa: S108


def yaml2pdf(recipe_yamls: list[str]):
    outdir = Path('/tmp/grocery_shopper/')  # noqa: S108
    for recipe_file in recipe_yamls:
        recipe: RecipeYaml2Pdf = RecipeYaml2Pdf(Path(RECIPE_DIR, recipe_file))
        recipe.to_latex()
        # Compile recipe before moving to next
        cp: subprocess.CompletedProcess = subprocess.run(
            [
                Path('grocery_shopper', 'compile_recipe.sh'),
                Path('grocery_shopper', 'template.tex'),
                outdir,
            ],
            # stdout=subprocess.DEVNULL,
            # stderr=subprocess.DEVNULL
        )
        if cp.returncode != 0:
            msg = f'Compilation of "{recipe_file}" failed.'
            logging.error(msg)
        else:
            pdf_dir = Path(RECIPE_DIR, 'pdf')
            if not pdf_dir.is_dir():
                pdf_dir.mkdir(
                    parents=True,
                    exist_ok=True,
                )
            basename = Path(recipe_file).stem

            shutil.move(
                Path(outdir, 'template.pdf'),
                Path(pdf_dir, f'{basename}.pdf'),
            )
