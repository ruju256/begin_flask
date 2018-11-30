import psycopg2
import os


class Database():

    def __init__(self):
        try:
            if os.getenv('APP_SETTINGS') == "testing":
                database = 'test_store_manager'
            else:
                database = 'store_manager'
            self.connection = psycopg2.connect(
                                        database=database,
                                        user="postgres",
                                        password="postgres",
                                        host="localhost",
                                        port="5432"
                                        )
            self.cursor = self.connection.cursor()
            self.connection.autocommit = True
            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS users
                (
                    id SERIAL PRIMARY KEY ,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                );"""
            )
            
            print("Connection to {} Database Successful".format(database))
        except Exception as error:
            print("Could Not Connect To {} Database".format(database), error)

    def saving_a_new_user(self, first_name, last_name, email, password, role):
        save_a_user = """
            INSERT INTO users(first_name, last_name, email, password, role)\
            Values('{}','{}','{}','{}','{}')""".format(
                first_name, last_name, email, password, role)
        self.cursor.execute(save_a_user)

    def query(self, table_name, column_name, record):
        record = """SELECT * FROM {} WHERE {}='{}';""".format(
            table_name, column_name, record)
        self.cursor.execute(record)
        row = self.cursor.fetchone()
        return row

    def drop_table(self, table_name):
        query = """DROP TABLE IF EXISTS {} CASCADE""".format(table_name)
        self.cursor.execute(query)
        return "Table {} dropped successfully".format(table_name)
