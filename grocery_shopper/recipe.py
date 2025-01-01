from pathlib import Path

import yaml


class Ingredient:
    def __init__(self, name: str, quantity: str, optional: bool = False):  # noqa: FBT001, FBT002
        self.name = name
        self.quantity = quantity
        self.optional = optional

    def __repr__(self):
        return f'<{self.name}: {self.quantity!r}, {str(self.optional)[0]}>'


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

        self.name = yaml_data['recipe']['name']
        self.ingredients = tuple(
            Ingredient(**ingredient) for ingredient in yaml_data['ingredients']
        )
        self.preparation = tuple(
            PreparationStep(idx + 1, desc)
            for idx, desc in enumerate(yaml_data['preparation'])
        )

    def __str__(self):
        return f'{self.name}: {len(self.ingredients)} Ingredients, {len(self.preparation)} Steps'

    def __repr__(self):
        return f'<{self.name}: ({len(self.ingredients)}, {len(self.preparation)})>'


if __name__ == '__main__':
    recipe_file = Path('./recipes/Spätzle.yaml')

    # Create Recipe instances
    print(Recipe(recipe_file))
