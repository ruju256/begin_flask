from app import app
from unittest import TestCase
import json
from controllers.database import Database


class BaseTest(TestCase):

    def setUp(self):
        self.client = app.test_client(self)
        self.db = Database()

    def login_admin_to_get_token(self):
        user = dict(
            email="ezramahlon@andela.com",
            password="1234")

        response = self.client.post(
            '/auth/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        admin_response = json.loads(response.data.decode())
        return admin_response

    def login_user_to_get_token(self):
        user = dict(
            email="ezra@gmail.com",
            password="1234")

        response = self.client.post(
            '/auth/login',
            content_type='application/json',
            data=json.dumps(user)
        )
        user_response = json.loads(response.data.decode())
        return user_response
