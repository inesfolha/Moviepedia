import os

from flask import Blueprint, jsonify, request

from movie_web_app.data_manager.sqlite_data_manager import SQLiteDataManager
from movie_web_app.helpers.helper_functions import id_generator, sort_movies
from movie_web_app.helpers.omdb_api_extractor import data_extractor, get_imdb_link

api_movies = Blueprint('api_movies', __name__)

DATABASE_FILE = os.getenv('DATABASE_FILE')
data_manager = SQLiteDataManager(DATABASE_FILE)


@api_movies.route('/users', methods=['GET'])
def get_users():
    """Retrieves all users in Json format"""
    try:
        users = data_manager.get_all_users()
        return jsonify(users)
    except TypeError as te:
        return jsonify(str(te))
    except IOError as e:
        error_message = "An error occurred while retrieving user data."
        return jsonify(error_message)
    except RuntimeError as e:
        error_message = "An unexpected error occurred."
        return jsonify(error_message)


@api_movies.route('users/<user_id>/movies', methods=['GET'])
def user_movies(user_id):
    """Retrieves a specific user's movies in json format"""
    try:

        user_name = data_manager.get_user_name(user_id)
        movies = data_manager.get_user_movies(user_id)

        return jsonify(user_name, movies)
    except TypeError as te:
        return jsonify(str(te))
    except IOError as e:
        error_message = "An error occurred while retrieving the user data."
        print(f"IOError: {str(e)}")
        return jsonify(error_message)
    except RuntimeError as e:
        error_message = "An unexpected error occurred."
        print(f"Error: {str(e)}")
        return jsonify(error_message)


@api_movies.route('users/<user_id>/movies', methods=['POST'])
def add_movie(user_id):
    if request.method == 'POST':
        json_request = request.get_json()
        movie = json_request['movie']
        movie_info = data_extractor(movie)
        movie_link = get_imdb_link(movie)
        try:
            if movie_info is not None and 'Title' in movie_info and 'Year' in movie_info and 'Director' in movie_info:
                title = movie_info.get("Title")
                if len(movie_info['Ratings']) > 0:
                    rating = float(movie_info['Ratings'][0]['Value'].split("/")[0])
                else:
                    rating = None

                year_str = movie_info.get('Year')
                if year_str.isdigit():
                    year = int(year_str)
                else:
                    return jsonify({"error": "Failed to retrieve movie information. Please try a different movie"})

                poster = movie_info.get('Poster')
                director = movie_info.get('Director')
                movie_id = id_generator()

                data_manager.add_movie(user_id, movie_id, title, rating, year, poster, director, movie_link)

                return jsonify({"message": "Movie added successfully"})

            else:
                return jsonify({"error": "Failed to retrieve movie information. Please make sure the movie exists."})

        except ValueError as e:
            return jsonify({"error": str(e)})
        except (IOError, RuntimeError) as e:
            return jsonify({"error": "An error occurred while adding a movie."})

    return jsonify({"error": "Method not allowed"})


@api_movies.route('/users/<user_id>/update_movie/<movie_id>', methods=['PATCH'])
def update_movie(user_id, movie_id):
    """Updates a movie in a specific user's movie list."""
    try:
        json_data = request.json  # Access JSON data from the request body
        user_movie_list = data_manager.get_user_movies(user_id)
        movie_to_update = None
        for movie in user_movie_list:
            if movie['id'] == movie_id:
                movie_to_update = movie
                break

        if movie_to_update is None:
            # Handle possible errors with the movie id
            error_message = "Sorry, we could not find that movie!"
            return jsonify(error_message)
        print(movie_to_update)
        # Retrieve existing movie details
        title = movie_to_update['title']
        updated_director = json_data.get('director', movie_to_update['director'])
        updated_year = json_data.get('year', movie_to_update['year'])
        updated_rating = json_data.get('rating', movie_to_update['rating'])
        updated_poster_link = json_data.get('poster', movie_to_update['poster'])
        updated_imdb_link = json_data.get('movie_link', movie_to_update['movie_link'])

        # CREATE A NEW MOVIE ID
        new_movie_id = id_generator()
        try:
            data_manager.update_movie(user_id, movie_id, new_movie_id, title, updated_rating,
                                      updated_year, updated_poster_link, updated_director, updated_imdb_link)

            return jsonify('Movie successfully updated')

        except ValueError as ve:
            error_message = "An error occurred while updating the movie."
            print(f"ValueError: {str(ve)}")
            return jsonify(error_message)

        except IOError as e:
            error_message = "An error occurred while updating the movie."
            print(f"IOError: {str(e)}")
            return jsonify(error_message)

        except RuntimeError as e:
            error_message = "An unexpected error occurred."
            print(f"Error: {str(e)}")
            return jsonify(error_message)

    except Exception as e:
        error_message = "An error occurred while updating the movie."
        print(f"Error: {str(e)}")
        return jsonify({"error": error_message})


@api_movies.route('/users/<user_id>/delete_movie/<movie_id>', methods=['DELETE'])
def delete_movie(user_id, movie_id):
    """Deletes a movie from a specific user's movie list."""
    try:
        data_manager.delete_movie(user_id, movie_id)
        return jsonify('Movie successfully deleted')
    except (ValueError, TypeError):
        error_message = "Sorry, we could not find that movie!"
        return jsonify(error_message)
    except RuntimeError as re:
        print(f"Error: {str(re)}")
        return jsonify(str(re))



