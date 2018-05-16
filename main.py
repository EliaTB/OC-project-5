import requests
import pymysql


import openfoodfact_class as cl
from config import *


new_data = 0
products_list = []
categories_list = []



def import_sql_file(cursor, sql_file):
    """ function to import the sql file and create the db """
    statement = ""
    for line in open(sql_file):
        if not line.strip().endswith(';'): 
            statement = statement + line
        else:   # when you get a line ending in ';' then exec statement and reset for next statement
            statement = statement + line
            cursor.execute(statement)
            statement = ""

try:
    """
    Connect to the database
    """
    connexion = pymysql.connect(host='localhost',
                                user=DB_USER,
                                password=DB_PW,
                                db=DB_NAME,
                                charset='utf8mb4', )
    
except pymysql.InternalError:
    print("No database detected, creating a new one...")
    connexion = pymysql.connect(host='localhost',
                                user=DB_USER,
                                password=DB_PW,
                                charset='utf8mb4', )

    cursor = connexion.cursor()
    import_sql_file(cursor, "dc_oc_project5.sql")
    new_data = 1



def fill_product():
    cursor = connexion.cursor(pymysql.cursors.DictCursor)
    result = requests.get('https://fr.openfoodfacts.org/cgi/search.pl?page_size=1000&page=1&action=process&json=1').json()
    for element in result['products']:
        try:
            product_info = (element["product_name"], element["stores"], element["nutrition_grade_fr"], element["url"], element['categories_tags'][0])
            products_list.append(cl.Product(element["product_name"], element["stores"], element["nutrition_grade_fr"], element["url"], element['categories_tags'][0]))        
            cursor.execute("INSERT INTO product" "(name, store, nutrition_grade, url, category)"\
            "VALUES (%s, %s, %s, %s, %s)", product_info)
            connexion.commit()
            print(len(products_list), " products")
        except KeyError: #Don't take lignes without 'product_name'
            pass
        except connexion.OperationalError: #Don't take the products with encoding error
            pass
        except connexion.DataError: #Pass when product name is too long
            pass




def fill_category():
    cursor = connexion.cursor()
    result = requests.get('https://fr.openfoodfacts.org/categories.json').json()
    for element in result['tags']:
        if element['products'] > 1000:
            try:
                categories_list.append(cl.Category(element["id"], element["name"], element["url"]))
                cursor.execute("INSERT INTO category (tag, name, url)"\
                                "VALUES (%s, %s, %s)", (element["id"], element["name"], element["url"]))
                connexion.commit()
                print(len(categories_list), " categories")
            except connexion.OperationalError: #Don't take the products with encoding error
                pass
            except connexion.DataError: #Pass when product name is too long
                pass





def get_products_from_db():
    """Get a list of products from the database"""
    cursor = connexion.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM product")
    result = cursor.fetchall()
    cursor.close()

    db_products = []
    for element in result:
        db_products.append(cl.Product(element['name'], element['store'], element['nutrition_grade'], element['url'], element['category']))
    return db_products


def get_categories_from_db():
    """Get a list of categories from the database"""
    cursor = connexion.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM category")
    result = cursor.fetchall()
    cursor.close()

    db_categories = []
    for element in result:
        db_categories.append(cl.Category(element['tag'], element['name'], element['url']))
    return db_categories



def categories_browser():
    global products_list
    global categories_list

    page_min = 0
    page_max = 10
    while True:
        print("\nSélectionnez une catégorie:")
        if len(categories_list)-page_max < 10 <= page_max:
            page_max += len(categories_list)-page_max
            if page_max < 10:
                page_min = 0
            else:
                page_min = page_max-10
        if page_min < 0:
            page_min = 0
            page_max = 10

        for i in range(page_min, page_max):
            print("{} - {}".format(i+1, categories_list[i].name))

        uinput = input("\nEntrez: Numéro pour selectionner la catégorie "
                       "| > page suivante | < page précédente "
                       "| 0 - revenir au menu principal\n")

        if uinput == '0':
            break
        if uinput == '>':
            page_max += 10
            page_min += 10
        if uinput == '<' and page_min > 0:
            page_max -= 10
            page_min -= 10
        if uinput.isdigit():
            category_product_browser(int(uinput)-1, categories_list[int(uinput)-1].tag)

def category_product_browser(c_id, category_name):
    global categories_list
    global products_list

    category_products = select_products_from_category(category_name)
    page_min = 0
    page_max = 10
    while True:
        if len(category_products)-page_max < 10 <= page_max:
            page_max += len(category_products)-page_max
            if page_max < 10:
                page_min = 0
            else:
                page_min = page_max-10
        if page_min < 0:
            page_min = 0
            page_max = 10

        print("\nAffichage des produits de la catégorie {} | Page : {}".format(categories_list[c_id].name, int(page_max/10)))
        for i in range(page_min, page_max):
            print("{} - {}".format(i+1, category_products[i].name))

        uinput = input("\nEntrez: Numéro pour selectionner un produit "
                       "| > page suivante | < page précédente "
                       "| 0 - revenir aux catégories\n")

        if uinput == '0':
            break
        if uinput == '>':
            page_max += 10
            page_min += 10
        if uinput == '<' and page_min > 0:
            page_max -= 10
            page_min -= 10
        if uinput.isdigit():
            if 0 < int(uinput) <= len(category_products):
                print_product(category_products[int(uinput)-1])





def select_products_from_category(category):

    cursor = connexion.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""SELECT * FROM product WHERE category LIKE %s """, (category))
    result = cursor.fetchall()
    category_products = []
    for element in result:
        category_products.append(cl.Product(element['name'], element['store'], element['nutrition_grade'], element['url'], element['category']))
    return category_products


def print_product(product):
    while True:
        print("\n\t<__/ Fiche du Produit \__>\n")
        print("Nom du produit : " + product.name)
        print("Magasin : " + product.store)
        print("Nutri score: "+ product.nutrition_grade)
        print("URL : " + product.url)

        uinput = input("Entrez: 1 - Recherche d'un produit plus sain | 2 - Enregistrer | 3 - Supprimer le produit "
                       "des favoris| 0 - Revenir aux produits ")

        if uinput == '0':
            break

        if uinput == '1':
            substitutes_browser(product)

        if uinput == '2':
            save_user_product(product)

        if uinput == '3':
            drop_user_product(product)


def drop_user_product(product):
    cursor = connexion.cursor(pymysql.cursors.DictCursor)
    sql = "DELETE FROM favorite WHERE name = '%s' "
    cursor.execute(sql % product.name)
    cursor.close()
    connexion.commit()
    print("\nProduit supprimé de votre liste.")


def save_user_product(product):
    cursor = connexion.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM favorite")
    result = cursor.fetchall()
    exist = 0
    for element in result:
        if element['name'] == product.name:
            exist = 1
    if exist == 1:
        print("Produit déjà enregistré.")
    else:
        cursor.execute('INSERT INTO favorite (name, store, nutrition_grade, url, category)' 
                       ' VALUES (%s, %s, %s, %s, %s)', (product.name, product.store, product.nutrition_grade, product.url, product.category))
        print("\nProduit sauvegardé.")
    cursor.close()
    connexion.commit()


def get_substitutes(product):
    result = select_products_from_category(product.category)
    s_products = []
    for element in result:
        if element.nutrition_grade >= product.nutrition_grade:
            continue
        s_products.append(element)
    return s_products


def substitutes_browser(product):
    substitutes = get_substitutes(product)
    page_min = 0
    page_max = 10
    while True:
        if len(substitutes)-page_max < 10 <= page_max:
            page_max += len(substitutes)-page_max
            if page_max < 10:
                page_min = 0
            else:
                page_min = page_max-10
        if page_min < 0:
            page_min = 0
            page_max = 10

        print("\nListe des {} substitution pour le produit \"{}\" : \n".format(len(substitutes), product.name))
        if len(substitutes) == 0:
            print("\nVous utilisez déjà un produit sain selon OpenFoodFacts.\nRetour à la fiche produit.\n")
            break
        else:
            for i in range(page_min, page_max):
                print("{} - {}".format(i + 1, substitutes[i].name))

        uinput = input("\nEntrez: Numéro - selectionner un produit | > - page suivante |"
                       " < - page précedente | 0 - revenir au produit\n")

        if uinput is '0':
            break
        if uinput.isdigit():
            print_product(substitutes[int(uinput)-1])
            continue
        if uinput == '>':
            page_min += 10
            page_max += 10
        if uinput == '<' and page_min > 0:
            page_min -= 10
            page_max -= 10



def favorite_browser():
    page_min = 0
    page_max = 10
    while True:
        favorite_products = get_products_from_favorite()
        if len(favorite_products) - page_max < 10 <= page_max:
            page_max = len(favorite_products)
            if page_max < 10:
                page_min = 0
            else:
                page_min = page_max - 10
        if page_min < 0:
            page_min = 0
            page_max = 10
        if len(favorite_products) < 10:
            page_max = len(favorite_products)
            page_min = 0

        print("<__/ Liste des produits enregistrés \__>")
        for i in range(page_min, page_max):
            print("{} - {}".format(i+1, favorite_products[i].name,))
        uinput = input("\nEntrez: Numéro - selectionner un produit | > - page suivante |"
                       " < - page précedente | 0 - revenir au menu principal)\n")

        if uinput == '0':
            break

        if uinput == '>':
            page_max += 10
            page_min += 10

        if uinput == '<' and page_min > 0:
            page_max -= 10
            page_min -= 10

        if uinput.isdigit():
            if 0 < int(uinput) <= len(favorite_products):
                print_product(favorite_products[int(uinput)-1])


def get_products_from_favorite():
    cursor = connexion.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM favorite")
    result = cursor.fetchall()
    cursor.close()
    favorite_db_products = []
    for element in result:
        favorite_db_products.append(cl.Product(element['name'], element['store'], element['nutrition_grade'], element['url'], element['category']))
    return favorite_db_products



def client_menu():
    global products_list
    global categories_list

    running = True

    if new_data == 1:
        fill_product()
        fill_category()
        
    else:
        print("searching for data...")
        products_list = get_products_from_db()
        categories_list = get_categories_from_db()

    while running is True:
        print("\n\t<__/ Menu Principal \__>")
        print("1 : Quel aliment souhaitez-vous remplacer ? ")
        print("2 : Afficher la liste des favoris")
        print("3 : Quitter")
        uinput = input("Entrez: Un numéro pour choisir un menu")


        if uinput == '1':
            categories_browser()
            continue

        if uinput == '2':
            favorite_browser()
            continue

        if uinput == '3':
            running = False 

client_menu()
