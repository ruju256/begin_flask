from flask import Flask, request, jsonify
from models.users import Users

app = Flask(__name__) #instance of flask application

@app.route('/auth/signup', methods=['POST'])
def signup():
    post_data = request.get_json()
    first_name = post_data['first_name']
    last_name = post_data['last_name']
    email = post_data['email']
    password = post_data['password']
    role = post_data['role']

    new_user = Users(first_name, last_name, email, password, role)
    new_user.save_user()
    return jsonify({
            'msg':'{} successfully saved'.format(first_name),
            'user': {
                    "first_name": first_name,
                    "last_name":last_name,
                    "email":email,
                    "password": password,
                    "role":role
                },
        }), 201
