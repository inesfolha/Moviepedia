import os

from flask import render_template, request, redirect, url_for, Blueprint
from flask_login import LoginManager, login_required

from movie_web_app.data_manager.sqlite_data_manager import SQLiteDataManager
from movie_web_app.helpers.omdb_api_extractor import data_extractor, get_imdb_link
from movie_web_app.helpers.helper_functions import id_generator, sort_movies

movie_bp = Blueprint('movie_bp', __name__)

DATABASE_FILE = os.getenv('DATABASE_FILE')
data_manager = SQLiteDataManager(DATABASE_FILE)

login_manager = LoginManager()


@movie_bp.route('/users/<user_id>')
@login_required
def user_movies(user_id):
    """Retrieves a specific user's movies and renders the user_movies template."""
    try:
        user_name = data_manager.get_user_name(user_id)
        movies = data_manager.get_user_movies(user_id)

        sort_by = request.args.get('sort')

        if sort_by:
            movies = sort_movies(movies, sort_by)

        return render_template('user_movies.html', movies=movies, user_name=user_name, user_id=user_id)
    except TypeError as te:
        print(f"Error: {str(te)}")
        return render_template('general_error.html', error_message="Error retrieving user data")
    except IOError as e:
        error_message = "An error occurred while retrieving the user data."
        print(f"IOError: {str(e)}")
        return render_template('general_error.html', error_message=error_message)
    except RuntimeError as e:
        error_message = "An unexpected error occurred."
        print(f"Error: {str(e)}")
        return render_template('general_error.html', error_message=error_message)


@movie_bp.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie(user_id):
    """Adds a movie to a specific user's movie list."""

    if request.method == 'POST':
        movie = request.form.get('movie')

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
                    error_message = "Failed to retrieve movie information. Please try a different movie"
                    return render_template('general_error.html', error_message=error_message)

                poster = movie_info.get('Poster')
                director = movie_info.get('Director')
                movie_id = id_generator()

                data_manager.add_movie(user_id, movie_id, title, rating, year, poster, director, movie_link)

                return redirect(url_for('movie_bp.user_movies', user_id=user_id))

            else:
                error_message = "Failed to retrieve movie information. Please make sure the movie exists."
                return render_template('general_error.html', error_message=error_message)

        except ValueError as e:
            error_message = str(e)
            return render_template('general_error.html', error_message=error_message)
        except IOError as e:
            error_message = "An error occurred while adding a movie."
            print(f"IOError: {str(e)}")
            return render_template('general_error.html', error_message=error_message)
        except RuntimeError as e:
            error_message = "An unexpected error occurred."
            print(f"Error: {str(e)}")
            return render_template('general_error.html', error_message=error_message)

    return render_template('add_movie.html', user_id=user_id)


@movie_bp.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
@login_required
def update_movie(user_id, movie_id):
    """Updates a movie in a specific user's movie list."""

    user_movie_list = data_manager.get_user_movies(user_id)

    movie_to_update = None
    for movie in user_movie_list:
        if movie['id'] == movie_id:
            movie_to_update = movie
            break

    if movie_to_update is None:
        # Handle possible errors with the movie id
        error_message = "Sorry, we could not find that movie!"
        return render_template('general_error.html', error_message=error_message)

    if request.method == 'POST':
        title = movie_to_update['title']
        updated_director = request.form['director']
        updated_year = request.form['year']
        updated_rating = request.form['rating']
        updated_poster_link = request.form['poster']
        updated_imdb_link = request.form['imdb_link']

        # CREATE A NEW MOVIE ID
        new_movie_id = id_generator()
        try:
            data_manager.update_movie(user_id, movie_id, new_movie_id, title, updated_rating,
                                      updated_year, updated_poster_link, updated_director, updated_imdb_link)

            return redirect(url_for('movie_bp.user_movies', user_id=user_id))

        except ValueError as ve:
            error_message = "An error occurred while updating the movie."
            print(f"ValueError: {str(ve)}")
            return render_template('general_error.html', error_message=error_message)

        except IOError as e:
            error_message = "An error occurred while updating the movie."
            print(f"IOError: {str(e)}")
            return render_template('general_error.html', error_message=error_message)

        except RuntimeError as e:
            error_message = "An unexpected error occurred."
            print(f"Error: {str(e)}")
            return render_template('general_error.html', error_message=error_message)

    return render_template('update_movie.html', movie_id=movie_id, user_id=user_id, movie=movie_to_update)


@movie_bp.route('/users/<user_id>/delete_movie/<movie_id>', methods=['GET', 'POST'])
@login_required
def delete_movie(user_id, movie_id):
    """Deletes a movie from a specific user's movie list."""
    if request.method == 'POST':
        try:
            data_manager.delete_movie(user_id, movie_id)
            return redirect(url_for('movie_bp.user_movies', user_id=user_id, movie_id=movie_id))
        except (ValueError, TypeError):
            # Handle possible errors with the movie id
            error_message = "Sorry, we could not find that movie!"
            return render_template('general_error.html', error_message=error_message)
        except RuntimeError as re:
            print(f"Error: {str(re)}")
            return render_template('general_error.html', error_message=re)

    error_message = "Sorry, this page does not support GET requests"
    return render_template('general_error.html', error_message=error_message)
