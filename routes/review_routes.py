import os

from dotenv import load_dotenv
from flask import render_template, request, redirect, url_for, Blueprint, flash, get_flashed_messages
from flask_login import LoginManager, login_required

from movie_web_app.data_manager.sqlite_data_manager import SQLiteDataManager

from movie_web_app.helpers.helper_functions import id_generator, save_date

load_dotenv()

# Create the user_bp Blueprint
review_bp = Blueprint('review_bp', __name__)

DATABASE_FILE = os.getenv('DATABASE_FILE')
data_manager = SQLiteDataManager(DATABASE_FILE)
login_manager = LoginManager()


@review_bp.route('/movie_details/<movie_id>')
def movie_details(movie_id):
    """Displays the details of a movie along with their reviews and their authors
    and the buttons to add a review, delete and edit"""
    success_messages = get_flashed_messages(category_filter=['success'])
    error_messages = get_flashed_messages(category_filter=['error'])

    movie = data_manager.get_movie_details(movie_id)
    reviews = data_manager.get_all_movie_reviews(movie_id)
    movie_review_likes = data_manager.movie_review_likes(movie_id)
    return render_template('movie_details.html', movie=movie, reviews=reviews, likes=movie_review_likes,
                           error_messages=error_messages, success_messages=success_messages)


@review_bp.route('/add_review/<user_id>/<movie_id>', methods=['GET', 'POST'])
@login_required
def add_review(user_id, movie_id):
    """Loads the add review template and allows the user to publish a review"""
    if request.method == 'POST':
        review_id = id_generator()
        publication_date = save_date()
        review_rating = request.form.get('rating')
        review_title = request.form.get('review_title')
        review_text = request.form.get('review_text')
        try:
            data_manager.add_reviews(review_id, user_id, movie_id, review_rating, review_text, review_title, 0,
                                     publication_date)
            return redirect(url_for('review_bp.movie_details', movie_id=movie_id))
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('review_bp.movie_details', movie_id=movie_id))

    return render_template('add_review.html', movie_id=movie_id, user_id=user_id)


@review_bp.route('/like_review/<user_id>/<review_id>/<movie_id>', methods=['POST'])
@login_required
def like_review(user_id, review_id, movie_id):
    """Loads the add review template and allows the user to publish a review"""
    if request.method == 'POST':
        try:
            data_manager.like_review(user_id, review_id)
            return redirect(url_for('review_bp.movie_details', movie_id=movie_id))
        except ValueError:
            data_manager.unlike_review(user_id, review_id)
            return redirect(url_for('review_bp.movie_details', movie_id=movie_id))


@review_bp.route('/edit_review/<user_id>/<movie_id>/<review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(user_id, movie_id, review_id):
    """Loads the edit review template and allows the user to edit
    an already submitted review if published by the user"""
    review = data_manager.get_review_info(review_id)
    if request.method == 'POST':
        edit_date = save_date()
        review_title = request.form['title']
        review_text = request.form['text']
        rating = request.form['rating']
        data_manager.edit_reviews(review_id, user_id, movie_id, rating, review_text, review_title, edit_date)
        return redirect(url_for('review_bp.movie_details', movie_id=movie_id))
    return render_template('edit_review.html', movie_id=movie_id, user_id=user_id, review=review)


@review_bp.route('/delete_review/<user_id>/<movie_id>/<review_id>', methods=['POST'])
@login_required
def delete_review(user_id, movie_id, review_id):
    """Allows the user to delete a review if published by him"""
    if request.method == 'POST':
        data_manager.delete_reviews(user_id, movie_id, review_id)
        return redirect(url_for('review_bp.movie_details', movie_id=movie_id))
