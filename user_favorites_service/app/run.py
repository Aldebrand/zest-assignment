import os
from flask import Flask

from routes import favorite_repos_routes

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(favorite_repos_routes)


if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = os.environ.get('PORT', 8082)
    app.run(host=host, port=port, debug=True)
