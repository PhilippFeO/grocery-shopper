# from collections import namedtuple


class Ingredient:
    def __init__(self, name, quantity, optional=False,
                 category='N/A-CATEGORY',
                 url='N/A-URL',
                 meal='N/A-MEAL'):
        self.name = name
        self.quantity = str(quantity)  # may have one of the following form: 2 (pieces), 250g, 1 Block => string necessary
        self.optional = optional
        self.category = category
        self.url = url
        self.meal = meal

    def __eq__(self, other) -> bool:
        return (self.name == other.name and
                self.quantity == other.quantity and
                self.optional == other.optional and
                self.category == other.category and
                self.meal == other.meal)

    def __hash__(self):
        """Necessary for tests, especially for the use of collections.Counter()"""
        return hash((self.name, self.quantity, self.optional, self.category, self.meal))

    def __repr__(self) -> str:
        return f'Ingredient(name={self.name},\nquantity={self.quantity},\noptional={self.optional},\ncategory={self.category},\nurl={self.url},\nmeal={self.meal})'


# # `Card = collections.namedtuple('Card', ['rank', 'suit'])`
# Ingredient = namedtuple(
#     'Ingredient',
#     ['name', 'quantity', 'optional', 'category', 'url', 'meal'],
#     defaults=(False, 'N/A-CATEGORY', 'N/A-URL', 'N/A-MEAL'))
