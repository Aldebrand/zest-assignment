from flask import jsonify, make_response, abort, Blueprint
from utils.github_api import get_top_100_repos_by_stars, create_session
from utils.app_logging import logger

github_routes = Blueprint('github_routes', __name__)


@github_routes.route('/top-starred-repositories')
def top_starred_repositories():
    """
    Retrieves the top 100 repositories by stars from the database and returns them as a JSON response.

    Returns:
        A Flask response object containing a JSON representation of the top 100 repositories by stars.

    Raises:
        HTTPException: If there is an internal server error while retrieving the repositories.
    """

    try:
        with create_session() as session:
            repositories = get_top_100_repos_by_stars(session)

        response = make_response(jsonify(repositories))
        response.status_code = 200

        return response
    except Exception as e:
        logger.error(
            f"Failed to retrieve top 100 starred repos by stars. Error: {e}")

        abort(500, description="Internal server error")
