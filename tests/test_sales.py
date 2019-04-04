from app import app
import json
from controllers.database import Database
from tests.base_test import BaseTest
from models.sales import Sales


class TestSales(BaseTest):

    def setUp(self):
        self.client = app.test_client(self)
        self.db = Database

    # def test_fetch_all_sales(self):
    #     res = self.login_admin_to_get_token()
    #     token = res['access_token']
    #     response = self.client.get('/api/v1/sales',
    #                                headers={'access-token': token})
    #     resp_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(resp_data['msg'], "You have not made any sales yet")

    def test_adding_sale_when_one_of_the_fields_is_empty(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']

        response = self.client.post('/api/v1/sales',
                                    content_type='application/json',
                                    headers={'access-token': token},
                                    data=json.dumps({
                                        "product_name": "",
                                        "quantity_bought": "50"}))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.decode(),
                         "All fields should be completed")

    def test_making_sale_when_product_does_not_exist(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']

        response = self.client.post('/api/v1/sales',
                                    content_type='application/json',
                                    headers={'access-token': token},
                                    data=json.dumps({
                                        "product_name": "Sports shoes",
                                        "quantity_bought": "5"}))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.decode(),
                         "Product does not exist")

    def test_making_sale_successfully(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']

        response = self.client.post('/api/v1/sales',
                                    content_type='application/json',
                                    headers={'access-token': token},
                                    data=json.dumps({
                                        "product_name": "Jumaji Bracellet",
                                        "quantity_bought": "1"}))
        resp_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(resp_data['message'],
                         "Jumaji Bracellet sold successfully")

    def test_fetch_all_products(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']
        response = self.client.get('/api/v1/sales',
                                   headers={'access-token': token})

        resp_data = json.loads(response.data)
        self.assertEqual(resp_data['sales'], Sales.sales)
        self.assertEqual(response.status_code, 200)
