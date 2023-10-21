from datetime import datetime
from flask import current_app as app

from utils.db_manager import get_collection, get_database, close_client, create_mongo_client
from utils.app_logging import logger


def get_user_favorite_repositories(user_id):
    """
    Retrieve a list of favorite repositories for a given user.

    Args:
        user_id (str): The ID of the user whose favorite repositories to retrieve.

    Returns:
        list: A list of dictionaries, where each dictionary contains the repository's ID, data, and the date it was added.
              Returns None if an error occurs while retrieving the data.
    """
    
    db_uri = app.config['DB_URI']
    db_name = app.config['DB_NAME']
    favorites_collection_name = app.config['FAVORITES_COLLECTION']

    try:
        client = create_mongo_client(db_uri)
        db = get_database(client, db_name)
        collection = get_collection(db, favorites_collection_name)

        # Find all repositories that belong to the user.
        # Then, for each repository, return a dictionary containing the repository's data and the date it was added.
        cursor = collection.find({'user_id': user_id})
        favorite_repositories = [{'repository_id': repository['repository_id'], 'repository:': repository['repository_data'], 'added_at': repository['added_at']}
                                 for repository in cursor]
        logger.info(
            f"Retrieved user {user_id}'s favorite repositories. Count: {len(favorite_repositories)}")

        return favorite_repositories
    except Exception as e:
        logger.error(
            f"Failed to retrieve user's favorite repositories. Error: {e}")

        return None
    finally:
        close_client(client)


def add_user_favorite_repository(user_id, repository):
    """
    Adds a favorite repository to the user's favorites in the database.

    Args:
        user_id (str): The ID of the user.
        repository (dict): A dictionary containing the repository data.

    Returns:
        bool: True if the repository was added successfully, False if the repository already exists in the user's favorites, None if an error occurred.
    """

    db_uri = app.config['DB_URI']
    db_name = app.config['DB_NAME']
    favorites_collection_name = app.config['FAVORITES_COLLECTION']

    try:
        client = create_mongo_client(db_uri)
        db = get_database(client, db_name)
        collection = get_collection(db, favorites_collection_name)

        repository_id = str(repository.pop('id', None))

        # Check if the repository already exists in the user's favorites.
        existing_favorite = collection.find_one(
            {'user_id': user_id, 'repository_id': repository_id})

        if existing_favorite is not None:
            logger.warning(
                f"Repository {repository_id} already exists in user's favorites.")
            return False

        # Add new favorite repository to the user's favorites in the database.
        data = {
            'user_id': user_id,
            'added_at': datetime.utcnow(),
            'repository_id': repository_id,
            'repository_data': repository
        }
        result = collection.insert_one(data)
        logger.info(
            f"Added repository to user's favorites. Result: {result}")

        return True
    except Exception as e:
        logger.error(
            f"Failed to add repository to user's favorites. Error: {e}")

        return None
    finally:
        close_client(client)


def remove_user_favorite_repository(user_id, repository_id):
    """
    Remove a repository from a user's favorites in the database.

    Args:
        user_id (str): The ID of the user whose favorite repository is being removed.
        repository_id (str): The ID of the repository being removed from the user's favorites.

    Returns:
        bool: True if the repository was successfully removed, False if the repository was not found in the user's favorites, or None if an error occurred.
    """

    db_uri = app.config['DB_URI']
    db_name = app.config['DB_NAME']
    favorites_collection_name = app.config['FAVORITES_COLLECTION']

    try:
        client = create_mongo_client(db_uri)
        db = get_database(client, db_name)
        collection = get_collection(db, favorites_collection_name)

        # Remove the repository from the user's favorites in the database.
        result = collection.delete_one(
            {'user_id': user_id, 'repository_id': repository_id})

        if result.deleted_count == 1:
            logger.info(
                f"Removed repository {repository_id} from user {user_id}'s favorites.")

            return True

        logger.warning(
            f"No repository {repository_id} found in user {user_id}'s favorites to remove.")

        return False
    except Exception as e:
        logger.error(
            f"Failed to remove repository from user's favorites. Error: {e}")

        return None
    finally:
        close_client(client)
