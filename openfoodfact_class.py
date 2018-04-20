import jason
import pymysql



CATEGORIES_URL = 'https://fr.openfoodfacts.org/categories.json'
PRODUCTS_URL = 'https://world.openfoodfacts.org/country/france/'


class Categories:
    """Class representing the 'Categories' table of the database"""

	def __init__(self, data):
        
		self.id = data['id']
		self.name = data['name']


	def find_url(self, url):
		url = requests.get("https://fr.openfoodfacts.org/categories.json")
		data_c = url.json()
		for categories in data_c
			name_category = (categories["name"])
			

class category_manager:

	def __init__(self,):

	def select_category(self):

	def diplay_category(self):


	
class Product:
    """Class representing the 'Product' table of the database"""

    def __init__(self, data_info):
        self.id = data['id']
        self.name = data['name']
        self.url = data['url']
        #self.category = ""


	def find_url(self, url):
		url = requests.get("https://world.openfoodfacts.org/country/france")
		data_p = url.json()
		for products in data_p
			name_product = str(products["product_name_fr"])
			id_product = str(products["id"])


class product_manager:

	def __init__(self,):

	def select_product(self):

	def diplay_product(self):	

	def add_favorite(self:)
	# 	 print(' Do you want to save this match as favorite ?')
	#    print('1. Yes')
	#    print('2. No')
  	#  	 if choice == 1:
  	#    elif choice == 2:
	
			


