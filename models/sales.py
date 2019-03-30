from controllers.database import Database
from models.products import Product
from models.users import Users

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

    @staticmethod
    def update_prod_qty_on_sale(id, quantity):
        db.update_qty_on_sale(id, quantity)
        return

    @staticmethod
    def fetch_all_sales(table_name):
        my_sales = Users.query_all_records('sales')
        if not my_sales:
            return
        else:
            Sales.sales.clear()
            for sale in my_sales:
                sale = {
                    "id": sale[0],
                    "amount": sale[6],
                    "product_name": sale[3],
                    "price": sale[4],
                    "quantity_sold": sale[5]
                }
                Sales.sales.append(sale)
            return Sales.sales
