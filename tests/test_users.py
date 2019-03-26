from app import app
import json
from controllers.database import Database
from tests.base_test import BaseTest


class TestUser(BaseTest):

    def setUp(self):
        self.client = app.test_client(self)
        self.db = Database()

    def test_user_login(self):
        response = self.client.post(
            "/auth/login",
            content_type='application/json',
            data=json.dumps(dict(email='ezramahlon@andela.com',
                            password='1234'))
        )
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_if_new_user_is_saved_in_database(self):

        res = self.login_user_to_get_token()
        token = res['access_token']
        user = {
            "first_name": "Kibalama",
            "last_name": "Bogere",
            "email": "ezrai@gmail.com",
            "password": "1234",
            "role": "Admin"
        }
        reply = self.client.post('/auth/signup',
                                 content_type='application/json',
                                 headers={'access-token': token},
                                 data=json.dumps(user),
                                 )

        response_data = json.loads(reply.data)
        print(response_data)
        self.assertEqual(response_data['msg'], "Kibalama successfully saved")
        self.assertEqual(reply.status_code, 201)

        def tearDown(self):
            pass
