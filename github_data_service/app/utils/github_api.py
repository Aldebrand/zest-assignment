import requests
from flask import current_app as app

from app.utils.app_logging import logger
from app.utils.redis_manager import create_redis_client, get_from_cache, set_in_cache, close_redis_client


def _get_repositories_from_github(session, sort_by, order, per_page):
    """
    Retrieves a list of repositories from the GitHub API, sorted by the given criteria.

    Args:
        session (requests.Session): The session to use for the API request.
        sort_by (str): The field to sort the repositories by.
        order (str): The order to sort the repositories in ('asc' or 'desc').
        per_page (int): The number of repositories to retrieve per page.

    Returns:
        list: A list of dictionaries, each representing a repository. Each dictionary contains the following keys:
            - name (str): The name of the repository.
            - id (int): The ID of the repository.
            - stars (int): The number of stars the repository has.
            - clone_url (str): The URL to clone the repository.
            - url (str): The URL to the repository on GitHub.

        If the API request fails, an empty list is returned.
    """

    params = {'q': f'stars:>0', 'sort': sort_by,
              'order': order, 'per_page': per_page, 'page': 1}
    response = session.get(
        app.config['GITHUB_API_SEARCH_REPOS_URL'], params=params)

    if response.status_code == 200:
        logger.info(f"Retrieved top 100 repos by stars from GitHub API")
        data = response.json().get('items', [])
        repositories = []

        for repo in data:
            repositories.append({
                'name': repo['name'],
                'id': repo['id'],
                'stars': repo['stargazers_count'],
                'clone_url': repo['clone_url'],
                'url': repo['url']
            })

        return repositories

    logger.error(
        f"Failed to retrieve top 100 repos by stars. Status code: {response.status_code}")
    return []


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
    """
    Retrieves the top 100 repositories from GitHub API sorted by stars.

    Args:
        session: A requests.Session object used to make HTTP requests.
        sort_by: A string representing the field to sort the repositories by. Default is 'stars'.
        order: A string representing the order to sort the repositories in. Default is 'desc'.
        per_page: An integer representing the number of repositories to retrieve per page. Default is 100.

    Returns:
        A list of dictionaries representing the top 100 repositories sorted by stars.
    """

    redis_client = create_redis_client()
    cache_key = f"top_repos:{sort_by}:{order}:{per_page}"

    # Check cache for data
    if redis_client:
        data = get_from_cache(redis_client, cache_key)

        if data:
            logger.info(f"Retrieved top 100 repos by stars from cache")

            return data

    # Get data from GitHub API, after could not retrieve from cache
    repositories = _get_repositories_from_github(
        session, sort_by, order, per_page)

    # Save data to cache
    if redis_client:
        set_in_cache(redis_client, cache_key,
                     repositories, app.config['CACHE_EX'])
        logger.info(f"Saved top 100 repos by stars to cache")
        close_redis_client(redis_client)

    return repositories
