import jason
import pymysql




CATEGORIES_URL = 'https://fr.openfoodfacts.org/categories.json'
PRODUCTS_URL = 'https://world.openfoodfacts.org/country/france/'


def connection():
    """
    Connect to the database
    """
    connexion = pymysql.connect(host='localhost',
                                user='root',
                                password='test',
                                db='oc_project5',
                                charset='utf8mb4', )
    return connexion


def create_table_categories():
	# data_c = url.json()
	# for categories in data_c
	# 	name_category = (categories["name"])
	# 	print(name_category)
        
   


def create_table_products():
	# data_p = url.json()
	# for products in data_p
	# 	name_product = str(products["product_name_fr"])
	# 	id_product = str(products["_id"])
	# 	print(id_product, name_product)
 
 
#def main()
