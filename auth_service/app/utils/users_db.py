from flask import current_app as app

from utils.db_manager import get_collection, get_database, close_client, create_mongo_client
from utils.app_logging import logger


def save_user_to_db(email, password):
    """
    Saves a user to the database.

    Args:
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        str: The ID of the inserted user, or None if the user already exists or an error occurred.
    """

    db_uri = app.config['DB_URI']
    db_name = app.config['DB_NAME']
    users_collection_name = app.config['USERS_COLLECTION']

    try:
        client = create_mongo_client(db_uri)
        db = get_database(client, db_name)
        collection = get_collection(db, users_collection_name)

        user = collection.find_one({'email': email})

        if user is None:
            user = collection.insert_one(
                {'email': email, 'password': password})
            logger.info(f"User {email} saved to database.")

            return user.inserted_id

        return None
    except Exception as e:
        logger.error(f"Error saving user to database: {e}")

        return None
    finally:
        close_client(client)


def get_user_from_db(email):
    """
    Retrieve a user from the database by email.

    Args:
        email (str): The email of the user to retrieve.

    Returns:
        dict: A dictionary containing the user's information, or None if the user is not found.
    """

    db_uri = app.config['DB_URI']
    db_name = app.config['DB_NAME']
    users_collection_name = app.config['USERS_COLLECTION']

    try:
        client = create_mongo_client(db_uri)
        db = get_database(client, db_name)
        collection = get_collection(db, users_collection_name)

        if collection is None:
            return None

        user = collection.find_one({'email': email})

        return user
    except Exception as e:
        logger.error(f"Error retrieving user from database: {e}")

        return None
    finally:
        close_client(client)
