import os
import uuid

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from data_manager.json_data_manager import JSONDataManager
from data_manager.user import User
from helpers.authentication_helpers import is_valid_password
from helpers.omdb_api_extractor import data_extractor, get_imdb_link

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("app.secret_key")
bcrypt = Bcrypt(app)
data_manager = JSONDataManager('data/data.json')
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    """Loads a user from the user ID."""

    user_data = data_manager.get_user_data()
    user = next((user for user in user_data if user['id'] == user_id), None)
    if user:
        return User(user)
    return None


def id_generator():
    """Generates a unique ID using UUID."""
    return str(uuid.uuid4())


@app.route('/')
def home():
    """Renders the homepage template."""
    show_my_movies_button = False
    if current_user.is_authenticated:
        show_my_movies_button = True
    return render_template('homepage.html', show_my_movies_button=show_my_movies_button)


@app.route('/users')
def list_users():
    """Retrieves all users and renders the users template."""
    try:
        users = data_manager.get_all_users()
        return render_template('users.html', users=users)
    except Exception as e:
        error_message = "An error occurred while retrieving user data."
        print(f"Error: {str(e)}")
        return render_template('general_error.html', error_message=error_message)


@app.route('/users/<user_id>')
@login_required
def user_movies(user_id):
    """Retrieves a specific user's movies and renders the user_movies template."""

    try:
        user_name = data_manager.get_user_name(user_id)
        movies = data_manager.get_user_movies(user_id)
        return render_template('user_movies.html', movies=movies, user_name=user_name, user_id=user_id)
    except Exception as e:
        error_message = "An error occurred while retrieving  the user data."
        print(f"Error: {str(e)}")
        return render_template('general_error.html', error_message=error_message)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Adds a new user to the system."""
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_password = request.form.get('password')
        try:
            if is_valid_password(user_password):
                encrypted_password = bcrypt.generate_password_hash(user_password).decode('utf-8')
                user_id = id_generator()
                user_movie_list = []

                data_manager.add_user(user_name, encrypted_password, user_id, user_movie_list)
                return redirect(url_for('login', username=user_name))
            else:
                error_message = "Invalid password. Password needs to have at least 8 characters, " \
                                "one uppercase letter, one number and one special character."
                return render_template('add_user.html', error_message=error_message)

        except Exception as e:
            error_message = "An error occurred while adding a new user."
            print(f"Error: {str(e)}")
            return render_template('general_error.html', error_message=error_message)

    return render_template('add_user.html')


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie(user_id):
    """Adds a movie to a specific user's movie list."""

    if request.method == 'POST':
        movie = request.form.get('movie')

        movie_info = data_extractor(movie)
        movie_link = get_imdb_link(movie)

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

            return redirect(url_for('user_movies', user_id=user_id))

        else:
            error_message = "Failed to retrieve movie information. Please make sure the movie exists."
            return render_template('general_error.html', error_message=error_message)

    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
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
        updated_title = request.form['title']
        updated_director = request.form['director']
        updated_year = request.form['year']
        updated_rating = request.form['rating']
        updated_poster_link = request.form['poster']
        updated_imdb_link = request.form['imdb_link']

        try:
            data_manager.update_movie(user_id, movie_id, updated_title, updated_rating,
                                      updated_year, updated_poster_link, updated_director, updated_imdb_link)

            return redirect(url_for('user_movies', user_id=user_id))

        except Exception as e:
            error_message = "An error occurred while updating the movie."
            print(f"Error: {str(e)}")
            return render_template('error.html', error_message=error_message)

    return render_template('update_movie.html', movie_id=movie_id, user_id=user_id, movie=movie_to_update)


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['GET', 'POST'])
@login_required
def delete_movie(user_id, movie_id):
    """Deletes a movie from a specific user's movie list."""
    if request.method == 'POST':
        try:
            data_manager.delete_movie(user_id, movie_id)
            return redirect(url_for('user_movies', user_id=user_id, movie_id=movie_id))
        except (ValueError, TypeError):
            # Handle possible errors with the movie id
            error_message = "Sorry, we could not find that movie!"
            return render_template('general_error.html', error_message=error_message)

    error_message = "Sorry, this page does not support GET requests"
    return render_template('general_error.html', error_message=error_message)


@app.route('/users/<user_id>/manage_account', methods=['GET'])
@login_required
def manage_account(user_id):
    """Renders the manage account page for a specific user."""
    return render_template('manage_account.html', user_id=user_id)


@app.route('/users/<user_id>/manage_account/update_password', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    """Updates the password for a specific user."""
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        try:
            user_data = data_manager.get_user_data()
            user = next(user for user in user_data if user['id'] == user_id)
            if user and bcrypt.check_password_hash(user['password'], current_password):
                if is_valid_password(new_password):
                    encrypted_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                    data_manager.update_password(user_id, encrypted_password)
                    message = "Password successfully updated"
                    return render_template('successfully_changed_password.html', message=message, user_id=user_id)

                else:
                    error_message = "Invalid password. Password needs to have at least 8 characters, " \
                                    "one uppercase letter, one number and one special character."
                    return render_template('change_password.html', error_message=error_message)
            else:
                error_message = "Password Incorrect, please try again"
                return render_template('change_password.html', error_message=error_message)

        except Exception as e:
            error_message = "An error occurred while adding updating the password."
            print(f"Error: {str(e)}")
            return render_template('general_error.html', error_message=error_message)

    return render_template('change_password.html', user_id=user_id)


@app.route('/users/<user_id>/manage_account/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    """Deletes a user """
    if request.method == 'POST':
        try:
            data_manager.delete_user(user_id)
            return redirect(url_for('home'))

        except ValueError as e:
            error_message = str(e)
            return render_template('general_error.html', error_message=error_message)
        except RuntimeError as e:
            error_message = str(e)
            return render_template('general_error.html', error_message=error_message)

    error_message = "Sorry, this page does not support GET requests"
    return render_template('general_error.html', error_message=error_message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Authenticates the user and logs them in"""
    if request.method == 'POST':
        username = request.form.get('username')
        user_password = request.form.get('password')

        try:
            user_data = data_manager.get_user_data()
            for user in user_data:
                if user['name'] == username and bcrypt.check_password_hash(user['password'], user_password):
                    user_obj = User(user)  # Create an instance of the User class
                    login_user(user_obj)
                    user_id = user['id']
                    return redirect(url_for('user_movies', user_id=user_id))
            else:
                error_message = "Username or password Incorrect, please try again"
                return render_template('login.html', error_message=error_message)

        except Exception as e:
            error_message = "An error occurred while login in."
            print(f"Error: {str(e)}")
            return render_template('general_error.html', error_message=error_message)

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Logs out the currently logged-in user."""
    logout_user()
    return redirect(url_for('home'))


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
    app.run(debug=True)
