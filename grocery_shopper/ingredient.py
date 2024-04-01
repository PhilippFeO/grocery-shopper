# from collections import namedtuple


class Ingredient:
    def __init__(self, name, quantity, optional=False,
                 category='N/A-CATEGORY',
                 urls: list[str] = 'N/A-URL',
                 selected_url='',
                 meal='N/A-MEAL'):
        self.name = name
        self.quantity = str(quantity)  # may have one of the following form: 2 (pieces), 250g, 1 Block => string necessary
        self.optional = optional
        self.category = category
        self.urls: list[str] = urls
        self.selected_url = selected_url
        self.meal = meal

    def __eq__(self, other) -> bool:
        return (self.name == other.name and
                self.quantity == other.quantity and
                self.optional == other.optional and
                self.category == other.category and
                # self.url == other.url and
                self.meal == other.meal)

    def __hash__(self):
        """Necessary for tests, especially for the use of collections.Counter()"""
        return hash((self.name, self.quantity, self.optional, self.category, self.meal))

    def __repr__(self) -> str:
        return f'Ingredient(name={self.name}, quantity={self.quantity}, optional={self.optional}, category={self.category}, url={self.url}, meal={self.meal})'

    # def __repr__(self) -> str:
    #     return self.name


# # `Card = collections.namedtuple('Card', ['rank', 'suit'])`
# Ingredient = namedtuple(
#     'Ingredient',
#     ['name', 'quantity', 'optional', 'category', 'url', 'meal'],
#     defaults=(False, 'N/A-CATEGORY', 'N/A-URL', 'N/A-MEAL'))
