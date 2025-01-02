import csv
import random
from pathlib import Path
from typing import NamedTuple


class CategoryURL(NamedTuple):
    category: str
    url: str


def read_csv(file_path: Path) -> dict[str, CategoryURL]:
    """Read a CSV file and returns a dictionary. First entry (name of ingredient) is key, value is tuple consisting of `category` and `url`."""
    csv_dict = {}
    # Remove last entry
    rows = file_path.read_text().split('\n')[:-1]
    if rows[-1] == '':
        rows = rows[:-1]
    csv_reader = csv.reader(rows)

    for row in csv_reader:
        ingredient_str, category, *urls = row
        # Randomly select URL to have some variation
        url = random.sample(urls, 1)[0]
        # csv_dict[ingredient_str] = (category, url)
        csv_dict[ingredient_str] = CategoryURL(category, url)

    return csv_dict


if __name__ == '__main__':
    file_path = Path('res/ingredient_category_url.csv')
    result = read_csv(file_path)
    print(result)
