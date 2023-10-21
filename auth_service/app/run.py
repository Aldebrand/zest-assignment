import os
from flask import Flask

from routes import auth_routes

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(auth_routes, url_prefix='/auth')


if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = os.environ.get('PORT', 8081)
    app.run(host=host, port=port, debug=True)
