from app import app
import json
from controllers.database import Database
from tests.base_test import BaseTest
from models.products import Product


class TestProducts(BaseTest):

    def setUp(self):
        self.client = app.test_client(self)
        self.db = Database

    def test_fetch_all_products(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']
        response = self.client.get('/api/v1/products',
                                   headers={'access-token': token})

        resp_data = json.loads(response.data.decode())
        if not resp_data:
            self.assertEqual(resp_data['msg'], "You have no products in store")
        else:
            self.assertEqual(resp_data['products'], Product.products)
            self.assertEqual(response.status_code, 200)
