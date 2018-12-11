from controllers.database import Database
from models.users import Users
from models.categories import Category

db = Database()

class Product:

    def __init__(self, category_id, product_name, unit_price, quantity):
        self.category_id = category_id
        self.product_name = product_name
        self.unit_price = unit_price
        self.quantity = quantity

    def save_product(self):
        db.saving_a_new_product(
            self.category_id,
            self.product_name,
            self.unit_price,
            self.quantity
            )
        return