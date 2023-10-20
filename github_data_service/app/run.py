import os
from flask import Flask
from routes import github_routes

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(github_routes, url_prefix='/github')


if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = os.environ.get('PORT', 8080)
    app.run(host=host, port=port, debug=True)
