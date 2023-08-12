import os

from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory

from flask_login import LoginManager

from movie_web_app.data_manager.user import User
from movie_web_app.routes.movie_routes import movie_bp
from movie_web_app.routes.user_routes import user_bp
from movie_web_app.routes.review_routes import review_bp
from movie_web_app.routes.api_movie_routes import api_movies
from movie_web_app.routes.api_user_routes import api_user
from movie_web_app.routes.api_review_routes import api_reviews
from helpers.helper_functions import bcrypt
from movie_web_app.data_manager.sqlite_data_manager import SQLiteDataManager

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("APP_SECRET_KEY")
bcrypt.init_app(app)
login_manager = LoginManager(app)

DATABASE_FILE = os.getenv('DATABASE_FILE')
data_manager = SQLiteDataManager(DATABASE_FILE)

# Register the blueprints
app.register_blueprint(user_bp)
app.register_blueprint(movie_bp)
app.register_blueprint(review_bp)
app.register_blueprint(api_movies, url_prefix='/api')
app.register_blueprint(api_user, url_prefix='/api')
app.register_blueprint(api_reviews, url_prefix='/api')


@login_manager.user_loader
def load_user(user_id):
    """Loads a user from the user ID."""

    user_data = data_manager.get_user_data()
    user = next((user for user in user_data if user['id'] == user_id), None)
    if user:
        return User(user)
    return None


@app.errorhandler(404)
def page_not_found(error):
    """Renders the 404 page."""
    return render_template('404.html'), 404


@app.errorhandler(401)
def unauthorized(error):
    """Renders the 401 page."""
    return render_template('401.html'), 401


@app.route('/favicon.ico')
def favicon():
    """Serves the favicon icon file."""
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'icon.png', mimetype='image/png')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
