from app import app
import json
from controllers.database import Database
from tests.base_test import BaseTest
from models.products import Product


class TestProducts(BaseTest):

    def setUp(self):
        self.client = app.test_client(self)
        self.db = Database

    # def test_fetch_all_products_with_empty_database(self):
    #     res = self.login_admin_to_get_token()
    #     token = res['access_token']
    #     response = self.client.get('/api/v1/products',
    #                                headers={'access-token': token})

    #     resp_data = json.loads(response.data.decode())
    #     print(resp_data)
    #     self.assertEqual(resp_data['msg'], "You have no products in store")
    #     self.assertEqual(response.status_code, 200)

    def test_adding_product_if_one_of_the_fields_is_empty(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']
        product = {
            "category_id": 1,
            "product_name": "balls",
            "unit_price": "",
            "quantity": "20"
        }
        response = self.client.post('/api/v1/products',
                                    content_type="application/json",
                                    headers={"access-token": token},
                                    data=json.dumps(product)
                                    )
        resp_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(resp_data['message'],
                         "All fields should be completed")

    def test_adding_product_with_invalid_product_name(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']
        product = {
            "category_id": 1,
            "product_name": "$$balls",
            "unit_price": "3000",
            "quantity": "20"
        }
        response = self.client.post('/api/v1/products',
                                    content_type="application/json",
                                    headers={"access-token": token},
                                    data=json.dumps(product)
                                    )
        resp_data = (response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(resp_data, "Invalid Product Name")

    def test_adding_product_successfully(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']
        product = {
            "category_id": 1,
            "product_name": "Geometry sets",
            "unit_price": "5000",
            "quantity": "100"
        }
        response = self.client.post('/api/v1/products',
                                    content_type="application/json",
                                    headers={"access-token": token},
                                    data=json.dumps(product)
                                    )
        resp_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(resp_data['message'],
                         "Geometry sets saved successfully")
        self.assertEqual(resp_data['product'], {"category": 1,
                                                "name": "Geometry sets",
                                                "price": "5000",
                                                "quantity": "100"})

    def test_adding_product_that_already_exists(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']
        product = {
            "category_id": 5,
            "product_name": "Jumaji Bracellet",
            "unit_price": "30000",
            "quantity": "75"
        }
        response = self.client.post('/api/v1/products',
                                    content_type="application/json",
                                    headers={"access-token": token},
                                    data=json.dumps(product)
                                    )
        resp_data = response.data.decode()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(resp_data, "Jumaji Bracellet is already registered")

    def test_fetch_all_products(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']
        response = self.client.get('/api/v1/products',
                                   headers={'access-token': token})

        resp_data = json.loads(response.data)
        self.assertEqual(resp_data['products'], Product.products)
        self.assertEqual(response.status_code, 200)

    def test_editing_product_when_one_field_is_mising_in_post_request(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']
        product = {
            "category_id": 1,
            "product_name": "Jumaji Necklace",
            "unit_price": "88000",
            "quantity": ""
        }
        response = self.client.put('/api/v1/products/16',
                                   content_type="application/json",
                                   headers={"access-token": token},
                                   data=json.dumps(product)
                                   )
        resp_data = json.loads(response.data.decode())
        print(resp_data)
        self.assertEqual(resp_data['msg'],
                         "Ensure that all fields are not empty")
        self.assertEqual(response.status_code, 400)

    def test_editing_product_that_does_not_exist_in_the_database(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']
        product = {
            "category_id": 1,
            "product_name": "Firefox tyres",
            "unit_price": "2000000",
            "quantity": "100"
        }
        response = self.client.put('/api/v1/products/100',
                                   content_type="application/json",
                                   headers={"access-token": token},
                                   data=json.dumps(product)
                                   )
        resp_data = json.loads(response.data.decode())
        print(resp_data)
        self.assertEqual(resp_data['msg'], "Product Not Found")
        self.assertEqual(response.status_code, 400)

    def test_editing_product_successfully(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']
        product = {
            "category_id": 5,
            "product_name": "Diamonds",
            "quantity": "12",
            "unit_price": "18000",
        }
        response = self.client.put('/api/v1/products/16',
                                   content_type="application/json",
                                   headers={"access-token": token},
                                   data=json.dumps(product)
                                   )
        resp_data = json.loads(response.data.decode())
        print(resp_data)
        self.assertEqual(response.status_code, 200)

    def test_deleting_product_that_does_not_exist(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']
        respose = self.client.delete('/api/v1/products/100',
                                     content_type="application/json",
                                     headers={"access-token": token}
                                     )
        resp_data = respose.data.decode()
        print(resp_data)
        self.assertEqual(respose.status_code, 400)
        self.assertEqual(resp_data, "Product does not exist")

    def test_deleting_product_successfully(self):
        res = self.login_admin_to_get_token()
        token = res['access_token']
        respose = self.client.delete('/api/v1/products/16',
                                     content_type="application/json",
                                     headers={"access-token": token}
                                     )
        resp_data = json.loads(respose.data.decode())
        print(resp_data)
        self.assertEqual(respose.status_code, 200)
        self.assertEqual(resp_data['msg'],
                         "Product with ID 16 successfully deleted")
