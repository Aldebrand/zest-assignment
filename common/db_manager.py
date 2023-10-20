from pymongo import MongoClient
from pymongo.errors import PyMongoError
from utils.app_logging import logger


def create_mongo_client(uri):
    """
    Creates a MongoClient instance using the provided URI.

    Args:
        uri (str): The URI to connect to the MongoDB instance.

    Returns:
        MongoClient: A MongoClient instance if the connection is successful, otherwise None.
    """
    try:
        client = MongoClient(uri)

        return client
    except ConnectionError as e:
        logger.error(f"Failed to connect to MongoDB. Error: {e}")

        return None
    except Exception as e:
        logger.error(f"Failed to create MongoClient. Error: {e}")

        return None


def get_database(client, db_name):
    """
    Get a database from a MongoDB client.

    Args:
        client (pymongo.MongoClient): A MongoDB client instance.
        db_name (str): The name of the database to retrieve.

    Returns:
        pymongo.database.Database: The retrieved database, or None if an error occurred.
    """
    try:
        db = client[db_name]

        return db
    except PyMongoError as e:
        logger.error(f"Failed to retrieve database. Error: {e}")

        return None
    except Exception as e:
        logger.error(f"Unexpected error occurred. Error: {e}")

        return None


def get_collection(db, collection_name):
    """
    Retrieve a collection from the database.

    Args:
        db (pymongo.database.Database): The database to retrieve the collection from.
        collection_name (str): The name of the collection to retrieve.

    Returns:
        pymongo.collection.Collection: The retrieved collection, or None if an error occurred.
    """
    try:
        collection = db[collection_name]

        return collection
    except PyMongoError as e:
        logger.error(f"Failed to retrieve collection. Error: {e}")

        return None
    except Exception as e:
        logger.error(f"Unexpected error occurred. Error: {e}")

        return None


def close_client(client):
    """
    Closes the MongoClient connection.

    Args:
        client: A MongoClient instance.
    """
    try:
        client.close()
    except Exception as e:
        logger.error(f"Failed to close MongoClient. Error: {e}")
