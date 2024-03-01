import csv
import random


def read_csv(file_path: str) -> dict[str, tuple[str, str]]:
    """
    Reads a CSV file and returns a dictionary. First entry (name of ingredient) is key, value is tuple consisting of `category` and `url`.
    """
    csv_dict = {}

    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            ingredient, category, *urls = row
            # Randomly select URL to have some variation
            url = random.sample(urls, 1)[0]
            csv_dict[ingredient] = (category, url)

    return csv_dict


if __name__ == "__main__":
    file_path = 'res/ingredient_category_url.csv'
    result = read_csv(file_path)
    print(result)
