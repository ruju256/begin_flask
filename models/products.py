from controllers.database import Database
from models.users import Users
from models.categories import Category
import re

db = Database()

class Product:
    products = []

    def __init__(self, category_id, product_name, unit_price, quantity):
        self.category_id = category_id
        self.product_name = product_name
        self.unit_price = unit_price
        self.quantity = quantity


    def validate_product(self):
        valid = []  

        if(re.search("[$#@!%^&*(),_ +=|;:><?/|]",self.product_name)):
            return "Invalid Product Name", 400
        else:
            return valid.append({
                    "category_id": self.category_id,
                    "product_name": self.product_name,
                    "unit_price": self.unit_price,
                    "quantity": self.quantity
                })          
                

    def save_product(self):
        db.saving_a_new_product(
            self.category_id,
            self.product_name,
            self.unit_price,
            self.quantity
            )
        return

    @staticmethod
    def fetch_all_products(table_name):
       
        my_products = Users.query_all_records('products')

        if my_products == []:
            return "No Products Found"
        else:
            Product.products.clear()
            for product in my_products:
                product = {
                    "id":product[0],
                    "category":product[1],
                    "product_name":product[2],
                    "price":product[3],
                    "quantity":product[4]
                }
                Product.products.append(product)
            return Product.products
