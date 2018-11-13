from controllers.database import Database 
import re

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
            mail = re.match('[^@]+@[^@]+\\.[^@]+', self.email)
            if not mail:
                return "Email should be in the format john@smith.com", 400
            else:            
                does_email_exist = Users.query_record('users', 'email', self.email)
                if type(does_email_exist) is tuple:
                    return "User with this email already exists in the database", 400
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
    
    @staticmethod
    def query_record(table_name, column_name, record):
        record = db.query(table_name, column_name, record)
        if not record:
            return {"Record Not Found"}
        else:
            return record