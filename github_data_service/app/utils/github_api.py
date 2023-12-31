import requests
from flask import current_app as app

from utils.app_logging import logger
from utils.redis_manager import create_redis_client, get_from_cache, set_in_cache, close_redis_client


    
def _get_repositories_from_github(session, sort_by, order, per_page):
    """
    Retrieve a list of up to 100 GitHub repositories sorted by the given criteria.

    Args:
        session (requests.Session): A session object to use for making HTTP requests.
        sort_by (str): The field to sort the repositories by. Valid values are 'stars', 'forks', and 'updated'.
        order (str): The order to sort the repositories in. Valid values are 'asc' and 'desc'.
        per_page (int): The number of repositories to retrieve per page.

    Returns:
        list: A list of up to 100 repositories, represented as dictionaries with the following keys:
            - id (int): The ID of the repository.
            - name (str): The name of the repository.
            - description (str): The description of the repository.
            - owner (dict): A dictionary representing the owner of the repository, with the following keys:
                - id (int): The ID of the owner.
                - login (str): The username of the owner.
                - avatar_url (str): The URL of the owner's avatar image.
                - html_url (str): The URL of the owner's GitHub profile.
            - html_url (str): The URL of the repository on GitHub.
            - clone_url (str): The URL to use for cloning the repository.
            - language (str): The primary language of the repository.
            - topics (list): A list of topics associated with the repository.
            - stars (int): The number of stars the repository has.
            - forks_count (int): The number of forks the repository has.
            - created_at (str): The date and time the repository was created, in ISO 8601 format.
            - updated_at (str): The date and time the repository was last updated, in ISO 8601 format.
            - pushed_at (str): The date and time of the last push to the repository, in ISO 8601 format.
            - archived (bool): Whether the repository is archived.
            - visibility (str): The visibility of the repository. Valid values are 'public', 'private', and 'internal'.
            - watchers_count (int): The number of users watching the repository.
            - open_issues_count (int): The number of open issues in the repository.
    """
def _get_repositories_from_github(session, sort_by, order, per_page):
    
    repositories = []
    page = 1
    params = {'q': f'stars:>0', 'sort': sort_by,
              'order': order, 'per_page': per_page, 'page': 1}
    
    while len(repositories) < 100:
        params['page'] = page

        try:
            response = session.get(
                app.config['GITHUB_API_SEARCH_REPOS_URL'], params=params)
        except requests.exceptions.Timeout:
            logger.error(
                f"Time out while retrieving a bulk of repos from GitHub API.")
            
            break
        except requests.exceptions.RequestException as e:
            logger.error(
                f"RequestException: {e} while retrieving a bulk of repos from GitHub API.")
            
            break

        if response.status_code == 200:
            try:
                data = response.json().get('items', [])
                logger.info(f"Retrieved {len(data)} repos from GitHub API")
            except ValueError as e:
                logger.error(
                    f"Falied to parse response from GitHub API. Error: {e}")
                
                break

            for repo in data:
                try:
                    owner_data = repo['owner']
                    owner = {
                        'id': owner_data['id'],
                        'login': owner_data['login'],
                        'avatar_url': owner_data['avatar_url'],
                        'html_url': owner_data['html_url']
                    }
                    repositories.append({
                        'id': repo['id'],
                        'name': repo['name'],
                        'description': repo['description'],
                        'owner': owner,
                        'html_url': repo['html_url'],
                        'clone_url': repo['clone_url'],
                        'language': repo['language'],
                        'topics': repo['topics'],
                        'stars': repo['stargazers_count'],
                        'forks_count': repo['forks_count'],
                        'created_at': repo['created_at'],
                        'updated_at': repo['updated_at'],
                        'pushed_at': repo['pushed_at'],
                        'archived': repo['archived'],
                        'visibility': repo['visibility'],
                        'watchers_count': repo['watchers_count'],
                        'open_issues_count': repo['open_issues_count']
                    })
                except KeyError as e:
                    logger.warning(
                        f"KeyError: {e} in repo: {repo}. Skipping repo.")
        elif response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers \
                and response.headers['X-RateLimit-Remaining'] == '0':
            logger.error(
                f"GitHub API rate limit exceeded.")
            
            break
        elif  response.status_code == 403 and 'Retry-After' in response.headers:
            retry_after = response.headers['Retry-After']
            logger.error(f'GitHub API abuse detection triggered. Retry after {retry_after} seconds.')

            break
        else:
            logger.error(
                f"Failed to retrieve top 100 repos by stars. "
                f"Status code: {response.status_code}, Response: {response.text}")
            
            break

        # Check if there is next page. If not, break the loop
        if 'link' in response.headers:
            links = response.headers['link'].split(',')
            for link in links:
                if 'rel="next"' in link:

                    break
            else:
                break
        else:
            break

        page += 1
        
    return repositories[:100]


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
