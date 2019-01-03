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

        elif not self.first_name.isalpha():
            return "Firstname should only contain Letters and no spaces", 400

        elif self.last_name == "":
            return "Lastname is required", 400

        elif not self.last_name.isalpha():
            return "Lastname should only contain Letters and no spaces", 400

        elif self.email == "":
            return "Email is required", 400

        elif self.password == "":
            return "Password is required", 400

        elif self.role == "":
            return "User role is required", 400
        elif not self.role.isalpha():
            return "Role should only contain Letters and no spaces", 400
        else:
            mail = re.match('[^@]+@[^@]+\\.[^@]+', self.email)
            if not mail:
                return "Email should be in the format john@smith.com", 400
            else:
                email_exist = Users.query_record('users', 'email', self.email)
                if type(email_exist) is tuple:
                    return "Email is taken", 400
                else:
                    return valid.append(
                        {
                            "first_name": self.first_name,
                            "last_name": self.last_name,
                            "email": self.email,
                            "passwprd": self.password,
                            "role": self.role
                        })

    def save_user(self):
        db.saving_a_new_user(
            self.first_name,
            self.last_name,
            self.email,
            self.password,
            self.role
            )
        return

    @staticmethod
    def query_record(table_name, column_name, record):
        record = db.query(table_name, column_name, record)
        if not record:
            return "Record Not Found"
        else:
            return record

    @staticmethod
    def query_all_records(table_name):
        data = db.query_all(table_name)
        if data == []:
            return "No Data Found"
        else:
            return data

    @staticmethod
    def delete_record(table_name, id):
        db.delete_record(table_name, id)
        return "record successfully deleted"

