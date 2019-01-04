from controllers.database import Database
from models.products import Product

db = Database()


class Sales(Product):
    sales = []

    def __init__(self,
                 category_id,
                 user_id,
                 product_name,
                 price,
                 quantity_bought,
                 amount):

        self.category_id = category_id
        self.product_name = product_name
        self.user_id = user_id
        self.price = price
        self.quantity_bought = quantity_bought
        self.amount = amount

    def new_sale(self):
        db.saving_a_new_sale(self.category_id,
                             self.user_id,
                             self.product_name,
                             self.price,
                             self.quantity_bought,
                             self.amount)
        return
