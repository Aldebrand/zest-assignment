import jwt
import os
from flask import Blueprint, request, jsonify, current_app as app

from utils.favorites_db import get_user_favorite_repositories, add_user_favorite_repository, remove_user_favorite_repository

SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_ALGORITHM = app.config["JWT_ALGORITHM"]
favorite_repos_routes = Blueprint('favorite_repos_routes', __name__)


@favorite_repos_routes.route('/favorites', methods=['POST'])
def add_favorite_repo():
    """
    Endpoint to add a repository to a user's favorites list.

    Returns:
        A JSON response with a success or error message.
    """
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'error': 'Missing authorization token'}), 401
    try:
        user_id = jwt.decode(token, SECRET_KEY, algorithms=[
                             JWT_ALGORITHM])['user_id']
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid authorization token'}), 401

    repo = request.json.get('repository')

    if not repo:
        return jsonify({'error': 'Missing repository data'}), 400

    result = add_user_favorite_repository(user_id, repo)

    if result is None:
        return jsonify({'error': 'Failed to add repository to favorites'}), 500
    elif not result:
        return jsonify({'error': 'Repository already exists in favorites'}), 400
    else:
        return jsonify({'message': 'Repository added to favorites'}), 201


@favorite_repos_routes.route('/favorites', methods=['DELETE'])
def remove_favorite_repo():
    """
    Removes a repository from a user's favorites list.

    Returns:
        A JSON response with a success or error message.
    """
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'error': 'Missing authorization token'}), 401
    try:
        user_id = jwt.decode(token, 'secret', algorithms=[
                             JWT_ALGORITHM])['user_id']
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid authorization token'}), 401

    repo_id = request.args.get('repository_id')

    if not repo_id:
        return jsonify({'error': 'Missing repository ID'}), 400

    result = remove_user_favorite_repository(user_id, repo_id)

    if result is None:
        return jsonify({'error': 'Failed to remove repository from favorites'}), 500
    elif not result:
        return jsonify({'error': 'Repository does not exist in favorites'}), 400
    else:
        return jsonify({'message': 'Repository removed from favorites'}), 200


@favorite_repos_routes.route('/favorites', methods=['GET'])
def get_favorite_repos():
    """
    Retrieves the favorite repositories of a user.

    Returns:
        A JSON response containing the user's favorite repositories and a 200 status code if successful.
        A JSON response containing an error message and a 401 status code if the authorization token is missing or invalid.
        A JSON response containing an error message and a 500 status code if the favorite repositories could not be retrieved.
    """
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'error': 'Missing authorization token'}), 401
    try:
        user_id = jwt.decode(token, 'secret', algorithms=[
                             JWT_ALGORITHM])['user_id']
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid authorization token'}), 401

    favorite_repos = get_user_favorite_repositories(user_id)

    if favorite_repos is None:
        return jsonify({'error': 'Failed to retrieve favorite repositories'}), 500

    return jsonify({'favorite_repos': favorite_repos}), 200
