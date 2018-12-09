from flask import Flask, jsonify, request
from models.users import Users
from controllers.config import app_configuration
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Welcome Home"


@app.route('/auth/signup', methods=['POST'])
def signup():
    post_data = request.json
    first_name = post_data['first_name']
    last_name = post_data['last_name']
    email = post_data['email']
    hashed_password = generate_password_hash(post_data['password'], method='sha256')
    role = post_data['role']
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
                    "password": hashed_password,
                    "role": role
                    },
            }), 201
