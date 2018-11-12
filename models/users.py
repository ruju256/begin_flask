from controllers.database import Database

db = Database()
class Users(object):

    def __init__(self, first_name, last_name, email, password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role
    

    #Adding a new user to the system
    def save_user(self):
        db.saving_a_new_user(self.first_name, self.last_name, self.email, self.password, self.role)
        return 