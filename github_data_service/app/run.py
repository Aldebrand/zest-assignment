from flask import Flask
from .routes import github_routes

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(github_routes, url_perfix='/github')

if __name__ == '__main__':
    app.run(debug=True)
