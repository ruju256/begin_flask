from app import app
from unittest import TestCase
import json
from controllers.config import app_configuration
from controllers.database import Database
from models.users import Users

class TestingUserFunctionality(TestCase):

    def setUp(self):
        app.config = ["testing"]
        db = Database()
        self.create_table_users = db.creating_users_table()
        self.app = app
        self.client = app.test_client()     


    def test_home_page(self):
        response = self.client.get('/')
        self.assertTrue(response, "Welcome Home")


    # def test_if_new_user_is_saved_in_database(self):
    #     user = {
    #         "first_name":"Kibalama",
    #         "last_name":"Bogere",
    #         "email":"ezra@andela.com",
    #         "password":"1234",
    #         "role":"Admin"
    #     }   
    #     response =  self.client.post('/auth/signup',content_type='application/json', data=json.dumps(user))
        
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response_data['msg'],"Kibalama successfully saved")        
    #     self.assertEqual(response.status_code, 201)

