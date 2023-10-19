import requests
from flask import current_app as app

from .app_logging import logger
from redis_manager import create_redis_client, get_from_cache, set_in_cache, close_redis_client


def create_session(token=None):
    """
    Creates a new requests session with the appropriate headers for interacting with the GitHub API.

    Args:
        token (str, optional): A GitHub personal access token to use for authentication. Defaults to None.

    Returns:
        requests.Session: A new requests session object.
    """
    session = requests.Session()
    session.headers.update({'Accept': 'application/vnd.github.v3+json'})

    if token:
        session.headers.update({'Authorization': f'token {token}'})

    return session


def get_top_100_repos_by_stars(session, sort_by='stars', order='desc', per_page=100):
    redis_client = create_redis_client()
    cache_key = f"top_repos:{sort_by}:{order}:{per_page}"

    if redis_client:
        print('here')
        data = get_from_cache(redis_client, cache_key)

        if data:
            logger.info(f"Retrieved top 100 repos by stars from cache")

            return data

    params = {'q': f'stars:>0', 'sort': sort_by,
              'order': order, 'per_page': per_page, 'page': 1}
    response = session.get(
        app.config['GITHUB_API_SEARCH_REPOS_URL'], params=params)

    if response.status_code == 200:
        logger.info(f"Retrieved top 100 repos by stars from GitHub API")
        repositories = response.json().get('items', [])

        if redis_client:
            print(redis_client)
            set_in_cache(redis_client, cache_key,
                         repositories, app.config['CACHE_EX'])
            logger.info(f"Saved top 100 repos by stars to cache")
            close_redis_client(redis_client)

        return repositories
    else:
        logger.error(
            f"Failed to retrieve top 100 repos by stars. Status code: {response.status_code}")
        return []
