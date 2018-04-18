import jason
import pymysql



CATEGORIES_URL = 'https://fr.openfoodfacts.org/categories.json'
PRODUCTS_URL = 'https://world.openfoodfacts.org/country/france/'


class Categories:
    """Class representing the 'Categories' table of the database"""

	def __init__(self, data_info):
        
		self.id = data_info['id']
		self.name = data_info['name']


	def find_url(self, url):
		url = requests.get("https://fr.openfoodfacts.org/categories.json")
		data_c = url.json()
		for categories in data_c
			name_category = (categories["name"])
			

	# def category_manager(self):
	


class Product:
    """Class representing the 'Product' table of the database"""

    def __init__(self, data_info):
        self.id = data_info['id']
        self.name = data_info['name']
        self.url = data_info['url']
        self.category = ""


	def find_url(self, url):
		url = requests.get("https://world.openfoodfacts.org/country/france")
		data_p = url.json()
		for products in data_p
			name_product = str(products["product_name_fr"])
			id_product = str(products["id"])


	# def product_manager(self):

	def select_favorite(self):	

	def add_favorite(self:)
	
			


