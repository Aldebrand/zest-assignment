import requests
import json

from app.config import GITHUB_API_SEARCH_REPOS_URL, CACHE_EX
from app.app_logging import logger
from redis_manager import create_redis_client

redis_client = create_redis_client()

def create_session(token=None):
    session = requests.Session()
    session.headers.update({'Accept': 'application/vnd.github.v3+json'})

    if token:
        session.headers.update({'Authorization': f'token {token}'})

    return session

def get_top_100_repos_by_stars(session, sort_by='stars', order='desc', per_page=100):
    if  redis_client:
        cache_key = f'top_repositories:{sort_by}:{order}:{per_page}'
        cached_response = redis_client.get(cache_key)

        if cached_response:
            logger.info(f"Retrieved top 100 repos by stars from cache")

            return json.loads(cached_response)
    
    params = {'q': f'stars:>0', 'sort': sort_by, 'order': order, 'per_page': per_page, 'page': 1}
    response = session.get(GITHUB_API_SEARCH_REPOS_URL, params=params)

    if response.status_code == 200:
        logger.info(f"Retrieved top 100 repos by stars from GitHub API")
        repositories = response.json().get('items', [])

        if redis_client:
            redis_client.set(cache_key, json.dumps(repositories), ex=CACHE_EX)
            logger.info(f"Saved top 100 repos by stars to cache")

        return repositories
    else:
        logger.error(f"Failed to retrieve top 100 repos by stars. Status code: {response.status_code}")
        return []

if __name__ == '__main__':
    session = create_session()
    top_100_repos = get_top_100_repos_by_stars(session)

    print(top_100_repos)