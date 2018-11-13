from app import app
from unittest import TestCase
import json
from controllers.config import app_configuration
from controllers.database import Database
from models.users import Users

class TestingUserFunctionality(TestCase):

    def setUp(self):
        app.config = ["testing"]
        DB = Database()
        DB.drop_table('users')
        self.create_table_users = DB.creating_users_table()
        self.app = app
        self.client = app.test_client()       


    def test_if_new_user_is_saved_in_database(self):
        self.user = {
            "first_name":"Kibalama",
            "last_name":"Bogere",
            "email":"ezra@andela.com",
            "password":"1234",
            "role":"Admin"
        }   
        response =  self.client.post('/auth/signup',data=json.dumps(self.user)
        ,content_type='application/json')
        response_data = json.loads(response.data.decode())
        self.assertEqual(response_data['msg'],"Ezra successfully saved")        
        self.assertEqual(response.status_code, 201)

