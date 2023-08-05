import os

from dotenv import load_dotenv
from flask import render_template, request, redirect, url_for, Blueprint
from flask_login import LoginManager, login_required, current_user
from movie_web_app.helpers.helper_functions import bcrypt

from movie_web_app.data_manager.sqlite_data_manager import SQLiteDataManager
from movie_web_app.data_manager.user import User

load_dotenv()

# Create the user_bp Blueprint
review_bp = Blueprint('review_bp', __name__)

DATABASE_FILE = os.getenv('DATABASE_FILE')
data_manager = SQLiteDataManager(DATABASE_FILE)
login_manager = LoginManager()


@review_bp.route('/movie_details')
def movie_details(movie_id):
    """Displays the details of a movie along with their reviews and their authors
    and the buttons to add a review, delete and edit"""
    return render_template('movie_details.html', movie_id=movie_id)


@review_bp.route('/add_review', methods=['GET', 'POST'])
@login_required
def add_review(user_id, movie_id):
    """Loads the add review template and allows the user to publish a review"""
    if request.method == 'POST':
        pass
    return render_template('add_review.html', movie_id=movie_id, user_id=user_id)


@review_bp.route('/edit_review', methods=['GET', 'POST'])
@login_required
def edit_review(user_id, movie_id):
    """Loads the edit review template and allows the user to edit
    an already submitted review if published by the user"""
    if request.method == 'POST':
        pass
    return render_template('edit_review.html', movie_id=movie_id, user_id=user_id)


@review_bp.route('/delete_review', methods=['POST'])
@login_required
def delete_review(user_id, movie_id):
    """Allows the user to delete a review if published by him"""
    pass
