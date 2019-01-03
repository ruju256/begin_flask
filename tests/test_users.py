from app import app
from unittest import TestCase
import json
from controllers.config import DevelopmentConfig, TestingConfig
from controllers.database import Database
from models.users import Users
from tests.base_test import BaseTest

class TestUser(BaseTest):

    def setUp(self): 
        self.client = app.test_client(self)        
        self.db = Database()        
        


    def test_if_new_user_is_saved_in_database(self):

        res = self.login_user_to_get_token()      
        token = res['access_token']
        
        user = {
            "first_name":"Kibalama",
            "last_name":"Bogere",
            "email":"ezra@gmail.com",
            "password":"1234",
            "role":"Admin"
        }   
        response =  self.client.post('/auth/signup',
                                    content_type='application/json',
                                    data=json.dumps(user),
                                    headers={'Authorization':'Bearer {}'.format(token)})
        
        response_data = json.loads(response.data.decode())
        self.assertEqual(response_data['msg'],"Kibalama successfully saved")        
        self.assertEqual(response.status_code, 201)

