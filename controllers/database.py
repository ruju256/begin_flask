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
                    id SERIAL PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                );"""
            )

            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS categories
                (
                    id SERIAL PRIMARY KEY,
                    category text NOT NULL
                );"""
            )

            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS products
                (
                    id SERIAL PRIMARY KEY,
                    category_id INT REFERENCES categories ON UPDATE CASCADE ON DELETE CASCADE,
                    product_name TEXT NOT NULL,
                    unit_price TEXT NOT NULL,
                    quantity INT NOT NULL,
                    create_date TIMESTAMPTZ DEFAULT NOW() 
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

    def saving_a_new_category(self, category):
        save_a_category = """
            INSERT INTO categories(category) Values('{}')""".format(category)
        self.cursor.execute(save_a_category)
    
    def saving_a_new_product(self, category_id, product_name, unit_price, quantity):
        save_product ="""
             INSERT INTO products(category_id, product_name, unit_price, quantity)\
             Values('{}','{}','{}','{}')""".format(category_id, product_name, unit_price, quantity)
        self.cursor.execute(save_product)

    def query(self, table_name, column_name, record):
        record = """SELECT * FROM {} WHERE {}='{}';""".format(
            table_name, column_name, record)
        self.cursor.execute(record)
        row = self.cursor.fetchone()
        return row

    def query_all(self, table_name):
        records = """SELECT * FROM {};""".format(table_name)
        self.cursor.execute(records)
        rows = self.cursor.fetchall()
        return rows

    def edit_product(self, category_id, product_name, unit_price, quantity, id):
        record = """UPDATE products SET category_id = '{}', product_name = '{}', unit_price = '{}', quantity = '{}'\
        WHERE id = '{}';""". format(category_id, product_name, unit_price, quantity, id)
        self.cursor.execute(record)

    def drop_table(self, table_name):
        query = """DROP TABLE IF EXISTS {} CASCADE""".format(table_name)
        self.cursor.execute(query)
        return "Table {} dropped successfully".format(table_name)
