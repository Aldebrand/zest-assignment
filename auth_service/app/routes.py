from flask import Blueprint, request, jsonify

from users import login_user, signup_user

auth_routes = Blueprint('auth_routes', __name__)


@auth_routes.route('/login', methods=['POST'])
def login():
    """
    Logs in a user with the provided email and password.

    Returns:
        A JSON response containing a success message and a JWT token if the login is successful.
        Otherwise, returns a JSON response containing an error message and an appropriate HTTP status code.
    """
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    jwt_token = login_user(email, password)

    if not jwt_token:
        return jsonify({'error': 'Invalid email or password'}), 401

    return jsonify({'message': f"You've successfuly logged in", 'jwt_token': jwt_token}), 200


@auth_routes.route('/signup', methods=['POST'])
def signup():
    """
    Signs up a new user with the provided email and password.

    Returns:
        A JSON response containing a success message and a JWT token.
        If the email or password is missing, returns a 400 error.
        If the user already exists, returns a 409 error.
    """

    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing email, or password'}), 400

    jwt_token = signup_user(email, password)

    if jwt_token is None:
        return jsonify({'error': 'User is already exists'}), 409

    return jsonify({'message': 'User created successfully', 'jwt_token': jwt_token}), 201
