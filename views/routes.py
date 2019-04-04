from flask import Flask, jsonify, request, make_response
from models.users import Users
from models.categories import Category
from models.products import Product
from models.sales import Sales
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from views.config import BaseConfig
import jwt
import datetime


app = Flask(__name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'access-token' in request.headers:
            token = request.headers['access-token']
        if not token:
            return jsonify({"message": "UN-AUTHORIZED ACCESS"}), 401
        try:
            token_data = jwt.decode(token, BaseConfig.SECRET_KEY)
            current_user = Users.query_record(
                'users', 'email', token_data['email'])
        except Exception as error:
            return jsonify({"message": "Invalid Token"}, error), 401
        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/', methods=['GET'])
def home():
    return "Welcome Home"


@app.route('/auth/login', methods=['POST'])
def login():
    post_data = request.json
    email = post_data['email']
    password = post_data['password']

    if not email or not password:
        return make_response('All fields should be completed', 401,
                             {
                                "WWW-Authenticate": "\
                                    Basic realm=Login Required"
                             }
                             )

    user = Users.query_record('users', 'email', email)
    if type(user) is not tuple:
        return make_response("Email not recognized", 401,
                             {
                                "WWW-Authenticate": "\
                                    Basic realm=Login Required"
                             }
                             )

    else:
        if check_password_hash(user[4], password):
            access_token = jwt.encode(
                                        {
                                         'email': user[3],
                                         'exp': datetime.datetime.utcnow() +
                                         datetime.timedelta(minutes=90)
                                        }, BaseConfig.SECRET_KEY
                                    )
            return jsonify({"access_token": access_token.decode('UTF-8'),
                            "Role": user[5]
                            })
        return make_response('Invalid Password', 401,
                             {
                                "WWW-Authenticate": "\
                                    Basic realm=Login Required"
                             }
                             )


@app.route('/auth/signup', methods=['POST'])
@token_required
def signup(current_user):
    post_data = request.json
    first_name = post_data['first_name']
    last_name = post_data['last_name']
    email = post_data['email']
    hashed_password = generate_password_hash(
        post_data['password'], method='sha256'
        )
    role = post_data['role']
    if current_user[5] != 'Admin':
        return make_response("Only Administrators Can Add New Members", 400)
    else:
        new_user = Users(first_name, last_name, email, hashed_password, role)
        valid_user = new_user.validate_input()
        if type(valid_user) is tuple:
                return valid_user
        else:
            new_user.save_user()
            return jsonify({
                'msg': '{} successfully saved'.format(first_name),
                'user': {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "role": role
                        },
                }), 201


@app.route('/api/v1/categories', methods=['POST'])
@token_required
def add_category(current_user):
    post_data = request.json
    category = post_data['category']
    if not category:
        return make_response("Category can not be empty", 400)
    else:
        new_category = Category(category)
        valid_category = new_category.validate_input()
        if type(valid_category) is tuple:
            return valid_category
        else:
            new_category.save_category()
            return jsonify({
                    "message": "{} successfully saved".format(category)
                    }), 201


@app.route('/api/v1/products', methods=['POST'])
@token_required
def add_product(current_user):
    post_data = request.json
    category = int(post_data['category_id'])
    product_name = post_data['product_name']
    price = post_data['unit_price']
    quantity = post_data['quantity']

    if not category or not product_name or not price or not quantity:
        return jsonify({
            "message": "All fields should be completed"
        }), 400
    else:
        new_product = Product(category, product_name, price, quantity)
        valid_product = new_product.validate_product()
        if type(valid_product) is tuple:
                return valid_product
        else:
            verify_category = Users.query_record('categories', 'id', category)
            if type(verify_category) is str:
                return jsonify({
                    "message": "{} is an invalid category".format(category)
                }), 400
            else:
                new_product.save_product()
                return jsonify({
                    "message": "{} saved successfully".format(product_name),
                    "product": {
                            "category": category,
                            "name": product_name,
                            "price": price,
                            "quantity": quantity
                        }
                    }), 201


@app.route('/api/v1/products/<int:id>', methods=['GET'])
@token_required
def product_details(current_user, id):
    product = Users.query_record('products', 'id', id)
    if type(product) is str:
        return make_response("Product does not exist",  400)
    else:
        return jsonify({
            "category": product[1],
            "product_name": product[2],
            "price": product[3],
            "quantity": product[4]
        })


@app.route('/api/v1/products', methods=['GET'])
@token_required
def products(current_user):
    my_products = Product.fetch_all_records('products')
    if not my_products:
        return jsonify({"msg": "You have no products in store"}), 200
    else:
        return jsonify({"products": Product.products}), 200


@app.route('/api/v1/products/<int:id>', methods=['PUT'])
@token_required
def edit_product(current_user, id):
    post_data = request.json

    category = int(post_data['category_id'])
    product_name = post_data['product_name']
    price = post_data['unit_price']
    quantity = post_data['quantity']

    if not category or not product_name or not price or not quantity:
        return jsonify({"msg": "Ensure that all fields are not empty"}), 400
    else:
        new_details = Product(category, product_name, price, quantity)
        product = new_details.edit_product(id)
        if not product:
            return jsonify({"msg": "Product Not Found"}), 400
        else:
            return jsonify({"New Product Details": product}), 200


@app.route('/api/v1/products/<int:id>', methods=['DELETE'])
@token_required
def delete_product(current_user, id):
    product = Users.query_record('products', 'id', id)
    if not product:
        return make_response("Product does not exist", 400)
    else:
        Users.delete_record('products', id)
        Product.fetch_all_records('products')
        return jsonify(
            {
                "msg": "Product with ID {} successfully deleted".format(id),
                "prouducts": Product.products
            }
            ), 200


@app.route('/api/v1/sales', methods=['POST'])
@token_required
def make_a_sale(current_user):
    post_data = request.json
    product_name = post_data['product_name']
    qty_bought = int(post_data['quantity_bought'])

    if not product_name or not qty_bought:
        return make_response("All fields should be completed", 400)
    else:
        product = Users.query_record('products', 'product_name', product_name)
        if not product:
            return make_response("Product does not exist", 400)
        else:
            product_id = int(product[0])
            user = 1
            price = product[3]
            amount = int(price) * qty_bought

            if product[4] == 0:
                return make_response("currently Out of Stock", 400)

            elif qty_bought > int(product[4]):
                return make_response("Insufficient Stock", 400)
            else:
                sale = Sales(product_id,
                             user,
                             product_name,
                             price,
                             qty_bought,
                             amount)
                sale.new_sale()
                new_quantity = int(product[4]) - qty_bought
                Sales.update_prod_qty_on_sale(product_id, new_quantity)
                return jsonify({
                        "message": "{} sold successfully".format(product_name),
                        "sale": {
                                "product_name": product_name,
                                "price": price,
                                "quantity bought": qty_bought,
                                "Total amount": amount
                            }
                        }), 201


@app.route('/api/v1/sales', methods=['GET'])
@token_required
def sales(current_user):
    if not Sales.fetch_all_sales('sales'):
        return jsonify({"msg": "You have not made any sales yet"})
    else:
        return jsonify({"sales": Sales.sales}), 200
