import os

from dotenv import load_dotenv
from flask import Blueprint, jsonify, request

from movie_web_app.data_manager.sqlite_data_manager import SQLiteDataManager
from movie_web_app.helpers.helper_functions import id_generator, save_date


api_reviews = Blueprint('api_reviews', __name__)

load_dotenv()
DATABASE_FILE = os.getenv('DATABASE_FILE')
data_manager = SQLiteDataManager(DATABASE_FILE)


@api_reviews.route('/movie_details/<movie_id>', methods=['get'])
def movie_details(movie_id):
    """Displays the details of a movie along with their reviews and their authors"""

    movie = data_manager.get_movie_details(movie_id)
    reviews = data_manager.get_all_movie_reviews(movie_id)
    movie_review_likes = data_manager.movie_review_likes(movie_id)
    return jsonify(movie, reviews, movie_review_likes)


@api_reviews.route('/add_review/<user_id>/<movie_id>', methods=['POST'])
def add_review(user_id, movie_id):
    """Loads the add review template and allows the user to publish a review"""
    json_data = request.json
    review_id = id_generator()
    publication_date = save_date()
    review_rating = json_data.get('rating')
    review_title = json_data.get('review_title')
    review_text = json_data.get('review_text')
    try:
        data_manager.add_reviews(review_id, user_id, movie_id, review_rating, review_text, review_title, 0,
                                 publication_date)
        return jsonify('Review added successfully')
    except ValueError as e:
        return jsonify(str(e))


@api_reviews.route('/like_review/<user_id>/<review_id>/<movie_id>', methods=['POST'])
def like_review(user_id, review_id, movie_id):
    """Loads the add review template and allows the user to publish a review"""
    if request.method == 'POST':
        try:
            data_manager.like_review(user_id, review_id)
            return jsonify("review liked")
        except ValueError:
            data_manager.unlike_review(user_id, review_id)
            return jsonify("review unliked")


@api_reviews.route('/edit_review/<user_id>/<movie_id>/<review_id>', methods=['PATCH'])
def edit_review(user_id, movie_id, review_id):
    """Loads the edit review template and allows the user to edit
    an already submitted review if published by the user"""

    json_data = request.json

    review = data_manager.get_review_info(review_id)
    print(review)
    edit_date = save_date()

    review_title = json_data.get("title", review['review_title'])
    review_text = json_data.get("text", review['review_text'])
    rating = json_data.get("rating", review['rating'])
    data_manager.edit_reviews(review_id, user_id, movie_id, rating, review_text, review_title, edit_date)
    return jsonify("Review successfully updated")


@api_reviews.route('/delete_review/<user_id>/<movie_id>/<review_id>', methods=['DELETE'])
def delete_review(user_id, movie_id, review_id):
    """Allows the user to delete a review if published by him"""
    data_manager.delete_reviews(user_id, movie_id, review_id)
    return jsonify("Review successfully deleted")

# NEXT ->  VERIFY ALL ERROR HANDLING CONNECTIONS BETWEEN DATAMANAGER AND ROUTES (APP AND API)
#      ->  CHECK ALL FUNCTIONS WITH FLASHED MESSAGES AND SEE IF THEY ARE ALL RETURNING IN THE TEMPLATES
