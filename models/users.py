from controllers.database import Database

db = Database()
class Users(object):

    def __init__(self, first_name, last_name, email, password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role
    

    def validate_input(self):
        valid = []
        if self.first_name == "":
            return "Firstname is required", 400
        elif self.last_name == "":
            return "Lastname is required", 400
        elif self.email == "":
            return "Email is required", 400
        elif self.password == "":
            return "Password is required", 400
        elif self.role == "":
            return "User role is required", 400
        else:
            return valid.append({"first_name": self.first_name,
                    "last_name": self.last_name,
                    "email": self.email,
                    "passwprd": self.password,
                    "role": self.role
            })
                        
                    
                
                

    
    #Adding a new user to the system
    def save_user(self):
        db.saving_a_new_user(self.first_name, self.last_name, self.email, self.password, self.role)
        return 