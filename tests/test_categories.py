from app import app
import json
from controllers.database import Database
from tests.base_test import BaseTest


class TestCategories(BaseTest):

    def setUp(self):
        self.client = app.test_client(self)
        self.db = Database()

    def test_add_products_category_with_empty_post_request(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']
        category = {"category": ""}
        reply = self.client.post('/api/v1/categories',
                                 content_type='application/json',
                                 headers={'access-token': token},
                                 data=json.dumps(category),
                                 )

        response_data = (reply.data.decode())
        self.assertEqual(reply.status_code, 400)
        self.assertEqual(response_data, "Category can not be empty")

    def test_add_product_category_if_it_already_exists(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']
        category = {"category": "Groceries"}
        reply = self.client.post('/api/v1/categories',
                                 content_type='application/json',
                                 headers={'access-token': token},
                                 data=json.dumps(category)
                                 )
        response_data = (reply.data.decode())
        self.assertEqual(reply.status_code, 400)
        self.assertEqual(response_data, "Groceries is already registered")

    def test_add_products_category_with_invalid_category_name(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']
        category = {"category": "@Cutlery"}
        reply = self.client.post('/api/v1/categories',
                                 content_type='application/json',
                                 headers={'access-token': token},
                                 data=json.dumps(category),
                                 )

        response_data = (reply.data.decode())
        self.assertEqual(reply.status_code, 400)
        self.assertEqual(response_data,
                         "Category should only contain Letters and no spaces")

    def test_add_products_category_successfully(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']
        category = {"category": "Textiles"}
        reply = self.client.post('/api/v1/categories',
                                 content_type='application/json',
                                 headers={'access-token': token},
                                 data=json.dumps(category),
                                 )

        response_data = json.loads(reply.data)
        self.assertEqual(reply.status_code, 201)
        self.assertEqual(response_data['message'],
                         "Textiles successfully saved")
