from pathlib import Path

import yaml


# TODO(Philipp): Rewrite as `dataclass` <01-01-2025>
class Ingredient:
    def __init__(  # noqa: PLR0913
        self,
        name: str,
        quantity: str,
        optional: bool = False,  # noqa: FBT001, FBT002
        category: str = 'N/A-CATEGORY',
        url: str = 'N/A-URL',
        meal: str = 'N/A-MEAL',
    ):
        self.name: str = name
        # may have one of the following form: 2 (pieces), 250g, 1 Block => string necessary
        self.quantity: str = quantity
        self.optional: bool = optional
        self.category = category
        self.url = url
        self.meal = meal

    def __eq__(self, other) -> bool:
        if isinstance(other, Ingredient):
            return (
                self.name == other.name
                and self.quantity == other.quantity
                and self.optional == other.optional
                and self.category == other.category
                and self.meal == other.meal
            )
        return False

    def __hash__(self):
        """Necessary for tests, especially for the use of collections.Counter()."""
        return hash((self.name, self.quantity, self.optional, self.category, self.meal))

    def __repr__(self) -> str:
        return f'Ingredient(name={self.name!r},\nquantity={self.quantity!r},\noptional={self.optional!r},\ncategory={self.category!r},\nurl={self.url!r},\nmeal={self.meal!r})'


class PreparationStep:
    def __init__(self, step_idx: int, step_desc: str):
        self.step_idx = step_idx
        self.step_desc = step_desc

    def __repr__(self):
        return f'{self.step_idx}. {self.step_desc}'


class Recipe:
    def __init__(self, recipe_yaml: Path):
        assert (
            recipe_yaml.suffix == '.yaml'
        ), f'No yaml file was provided: {recipe_yaml}'

        # Parse the YAML data
        yaml_data = yaml.safe_load(recipe_yaml.read_text())

        self.name = yaml_data['recipe'][0]['name']

        # If no 'ingredients' key, then `self.ingredients = ()`
        self.ingredients = tuple(
            Ingredient(**ingredient)
            for ingredient in yaml_data.setdefault('ingredients', [])
        )

        # If no 'preparation' key, then `self.preparation = ()`
        self.preparation = tuple(
            PreparationStep(idx + 1, desc)
            for idx, desc in enumerate(yaml_data.setdefault('preparation', []))
        )

    def __str__(self):
        return f'{self.name}: {len(self.ingredients)} Ingredients, {len(self.preparation)} Steps'

    def __repr__(self):
        return f'<{self.name}: ({len(self.ingredients)}, {len(self.preparation)})>'


if __name__ == '__main__':
    recipe_file = Path(
        '/home/philipp/programmieren/grocery-shopper/recipes/Spätzle.yaml',
    )
    recipe = Recipe(recipe_file)
    print(recipe)  # noqa: T201
