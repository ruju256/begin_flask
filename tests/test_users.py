from app import app
import json
from controllers.database import Database
from tests.base_test import BaseTest


class TestUser(BaseTest):

    def setUp(self):
        self.client = app.test_client(self)
        self.db = Database()

    def test_user_login_with_empty_fileds(self):
        response = self.client.post(
            "/auth/login",
            content_type='application/json',
            data=json.dumps(dict(email='',
                            password='1234'))
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.decode(),
                         "All fields should be completed")

    def test_user_login_with_unknown_email(self):
        response = self.client.post(
            "/auth/login",
            content_type='application/json',
            data=json.dumps(dict(email='admin@andela.com',
                            password='1234'))
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.decode(),
                         "Email not recognized")

    def test_user_login_with_invalid_password(self):
        response = self.client.post(
            "/auth/login",
            content_type='application/json',
            data=json.dumps(dict(email='ezramahlon@andela.com',
                            password='1234567890'))
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.decode(),
                         "Invalid Password")

    def test_successful_user_login(self):
        response = self.client.post(
            "/auth/login",
            content_type='application/json',
            data=json.dumps(dict(email='ezramahlon@andela.com',
                            password='1234'))
        )
        self.assertEqual(response.status_code, 200)

    def test_adding_user_if_logged_in_user_is_not_admin(self):
        res = self.login_user_to_get_token()
        token = res['access_token']
        user = {
            "first_name": "Kibalama",
            "last_name": "Bogere",
            "email": "ezra@gmail.com",
            "password": "1234",
            "role": "Admin"
        }
        response = self.client.post('/auth/signup',
                                    content_type='application/json',
                                    headers={'access-token': token},
                                    data=json.dumps(user),
                                    )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.decode(),
                         "Only Administrators Can Add New Members")

    def test_adding_new_user_if_firstname_is_empty(self):

        res = self.login_admin_to_get_token()
        token = res['access_token']
        user = {
            "first_name": "",
            "last_name": "Bogere",
            "email": "ezrakeko@gmail.com",
            "password": "1234",
            "role": "Admin"
        }
        reply = self.client.post('/auth/signup',
                                 content_type='application/json',
                                 headers={'access-token': token},
                                 data=json.dumps(user),
                                 )

        response_data = (reply.data.decode())
        self.assertEqual(reply.status_code, 400)
        self.assertEqual(response_data, "Firstname is required")

    def test_adding_new_user_if_firstname_contains_restricted_characters(self):

        res = self.login_admin_to_get_token()
        token = res['access_token']
        user = {
            "first_name": "Mc-Mahlon",
            "last_name": "Oconor",
            "email": "ezrakeko@gmail.com",
            "password": "1234",
            "role": "Admin"
        }
        reply = self.client.post('/auth/signup',
                                 content_type='application/json',
                                 headers={'access-token': token},
                                 data=json.dumps(user),
                                 )

        response_data = (reply.data.decode())
        self.assertEqual(reply.status_code, 400)
        self.assertEqual(response_data,
                         "Firstname should only contain Letters and no spaces")

    def test_adding_new_user_if_lastname_is_empty(self):

        res = self.login_admin_to_get_token()
        token = res['access_token']
        user = {
            "first_name": "Mahlon",
            "last_name": "",
            "email": "ezrakeko@gmail.com",
            "password": "1234",
            "role": "Admin"
        }
        reply = self.client.post('/auth/signup',
                                 content_type='application/json',
                                 headers={'access-token': token},
                                 data=json.dumps(user),
                                 )

        response_data = (reply.data.decode())
        self.assertEqual(reply.status_code, 400)
        self.assertEqual(response_data, "Lastname is required")

    def test_adding_new_user_if_lastname_contains_restricted_characters(self):

        res = self.login_admin_to_get_token()
        token = res['access_token']
        user = {
            "first_name": "Mahlon",
            "last_name": "O'conor",
            "email": "ezrakeko@gmail.com",
            "password": "1234",
            "role": "Admin"
        }
        reply = self.client.post('/auth/signup',
                                 content_type='application/json',
                                 headers={'access-token': token},
                                 data=json.dumps(user),
                                 )

        response_data = (reply.data.decode())
        self.assertEqual(reply.status_code, 400)
        self.assertEqual(response_data,
                         "Lastname should only contain Letters and no spaces")

    def test_adding_new_user_if_email_is_empty(self):

        res = self.login_admin_to_get_token()
        token = res['access_token']
        user = {
            "first_name": "Mahlon",
            "last_name": "Kingston",
            "email": "",
            "password": "1234",
            "role": "Admin"
        }
        reply = self.client.post('/auth/signup',
                                 content_type='application/json',
                                 headers={'access-token': token},
                                 data=json.dumps(user),
                                 )

        response_data = (reply.data.decode())
        self.assertEqual(reply.status_code, 400)
        self.assertEqual(response_data, "Email is required")

    def test_adding_new_user_with_invalid_email(self):

        res = self.login_admin_to_get_token()
        token = res['access_token']
        user = {
            "first_name": "Mahlon",
            "last_name": "Kingston",
            "email": "ezra.com",
            "password": "1234",
            "role": "Admin"
        }
        reply = self.client.post('/auth/signup',
                                 content_type='application/json',
                                 headers={'access-token': token},
                                 data=json.dumps(user),
                                 )

        response_data = (reply.data.decode())
        self.assertEqual(reply.status_code, 400)
        self.assertEqual(response_data,
                         "Email should be in the format john@smith.com")

    def test_adding_new_user_if_role_is_empty(self):

        res = self.login_admin_to_get_token()
        token = res['access_token']
        user = {
            "first_name": "Mahlon",
            "last_name": "Mcgregor",
            "email": "ezrakeko@gmail.com",
            "password": "1234",
            "role": ""
        }
        reply = self.client.post('/auth/signup',
                                 content_type='application/json',
                                 headers={'access-token': token},
                                 data=json.dumps(user),
                                 )

        response_data = (reply.data.decode())
        self.assertEqual(reply.status_code, 400)
        self.assertEqual(response_data, "User role is required")

    def test_if_user_email_exists_in_database(self):

        res = self.login_admin_to_get_token()
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

        response_data = reply.data.decode()
        print(response_data)
        self.assertEqual(response_data, "Email is taken")
        self.assertEqual(reply.status_code, 400)

    def test_if_new_user_is_saved_in_database(self):

        res = self.login_admin_to_get_token()
        token = res['access_token']
        user = {
            "first_name": "Kibalama",
            "last_name": "Bogere",
            "email": "ezrastreetz@gmail.com",
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
        self.assertEqual(response_data['user'],
                         {
                            "first_name": "Kibalama",
                            "last_name": "Bogere",
                            "email": "ezrastreets@gmail.com",
                            "role": "Admin"
                        })
        self.assertEqual(reply.status_code, 201)

        def tearDown(self):
            pass
