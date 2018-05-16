class Category():
    """Class representing the 'Categories' table of the database"""

    def __init__(self, tag, name, url):
        self.tag = tag
        self.name = name
        self.url = url

		

class Product():
    """Class representing the 'Product' table of the database"""

    def __init__(self, name, store, nutrition_grade, url, category):
        self.name = name
        self.store = store
        self.nutrition_grade = nutrition_grade
        self.url = url
        self.category = category





