import bcrypt
import jwt

from utils.users_db import save_user_to_db, get_user_from_db
from utils.app_logging import logger

# This is just an example secret key, in production you should use a more secure one
SECRET_KEY = "mysecretkey"


def signup_user(email, password):
    """
    Signs up a new user with the given email and password.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        str: A JWT token with the user ID if the user was successfully signed up, None otherwise.
    """
    
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Save the user to the database
    user_id = save_user_to_db(email, hashed_password)

    if user_id is None:
        # If the user is None, it means the user already exists
        return None

    # Create a JWT token with the user ID
    token = jwt.encode({"user_id": user_id}, SECRET_KEY, algorithm="HS256")
    logger.info(f'jwt token for user - {user_id} created')

    return token


def login_user(email, password):
    """
    Logs in a user with the given email and password.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        str: A JWT token if the email and password match, None otherwise.
    """
    
    # Get the user from the database
    user = get_user_from_db(email)

    # Check if the password matches the hashed password in the database
    if bcrypt.checkpw(password.encode(), user.hashed_password):
        # Create a JWT token with the user ID
        token = jwt.encode({"user_id": user.id}, SECRET_KEY, algorithm="HS256")
        logger.info(f'jwt token for user - {user.id} created')

        return token

    # If the password doesn't match, return None
    return None
