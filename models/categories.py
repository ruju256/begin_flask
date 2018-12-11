from controllers.database import Database
from models.users import Users

db = Database()

class Category(object):

    def __init__(self, category):
        self.category = category


    def validate_input(self):
        valid=[]
        if self.category == "":
            return "Category is required", 400

        elif not self.category.isalpha():
            return "Category should only contain Letters and no spaces", 400
        else:
            category_exists = Users.query_record("categories", "category", self.category)
            if type(category_exists) is tuple:
                    return "Category Exists in the Database", 400
            else:
                return valid.append(
                    {
                        "category": self.category
                    })

    
    def save_category(self):
        db.saving_a_new_category(self.category)
        return