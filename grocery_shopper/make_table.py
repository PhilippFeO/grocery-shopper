from grocery_shopper.ingredient import Ingredient


# TODO: Add emtpy line after 10 rows for better overview <16-03-2024>

spacing: int = 3
row_names = ['?', 'Name', 'Menge', 'Kategorie', 'Gericht']
# Dont hardcode column number of "Name" because this number is used to filter for the ingredients with awk (s. ./main.py)
name_col_num = row_names.index('Name') + 1


def make_table(ingredients: list[Ingredient], with_url: bool = False) -> str:
    """Transform provided list of `Ingredient`s into a table.

    :param list[Ingredient] ingredients: Ingredients to print as table
    :param int spacing: Number of spaces between columns
    :returns: The table as string
    """
    data = [row_names]
    data.extend(['1' if ing.optional else '•',
                 ing.name,
                 ing.quantity,
                 ing.category,
                 ing.meal] for ing in ingredients)
    if with_url:
        row_names.append('Verweis')
        # index 0 is `header`
        for row, ing in zip(data[1:], ingredients):
            row.append(ing.selected_url)

    # Calculate the width of each column
    column_widths = [max(len(item) for item in col) for col in zip(*data)]

    # Craft table string
    table_rows = []
    for row in data:
        table_rows.append(
            ''.join(item.ljust(width + spacing) for item, width in zip(row, column_widths)).rstrip())
    # -1 due to `rstrip()`
    hline = '-' * (sum(column_widths) + (len(column_widths) - 1) * spacing)
    table_rows.insert(1, hline)

    return '\n'.join(table_rows) + '\n'
