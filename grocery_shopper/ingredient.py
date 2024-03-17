class Ingredient:
    def __init__(self, name, quantity, optional=False,
                 category='N/A-CATEGORY',
                 category_weight=0,
                 url='N/A-URL',
                 meal='N/A-MEAL'):
        self.name = name
        self.quantity = str(quantity)  # may have one of the following form: 2 (pieces), 250g, 1 Block => string necessary
        self.optional = optional
        self.category = category
        # Category weight is assigned accoirding to order in supermarket (=> walk from
        # category to category to be efficient).
        # This key is also used for sorting the ingredients when generating the shopping list.
        # 0 is used, when category is missing in the according csv file (2024-01-05: res/category_weight.csv)
        self.category_weight = category_weight
        self.url = url
        self.meal = meal
