import os

from dotenv import load_dotenv
from flask import render_template, request, redirect, url_for, Blueprint

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from movie_web_app.helpers.helper_functions import bcrypt

from movie_web_app.data_manager.sqlite_data_manager import SQLiteDataManager
from movie_web_app.data_manager.user import User
from movie_web_app.helpers.authentication_helpers import is_valid_password
from movie_web_app.helpers.helper_functions import id_generator

load_dotenv()

# Create the user_bp Blueprint
user_bp = Blueprint('user_bp', __name__)

DATABASE_FILE = os.getenv('DATABASE_FILE')
data_manager = SQLiteDataManager(DATABASE_FILE)
login_manager = LoginManager()


@user_bp.route('/')
def home():
    """Renders the homepage template."""
    show_my_movies_button = False
    if current_user.is_authenticated:
        show_my_movies_button = True
    return render_template('homepage.html', show_my_movies_button=show_my_movies_button)


@user_bp.route('/users')
def list_users():
    """Retrieves all users and renders the users template."""
    try:
        users = data_manager.get_all_users()
        return render_template('users.html', users=users)
    except TypeError as te:
        print(f"Error: {str(te)}")
        return render_template('general_error.html', error_message="Error retrieving users data")
    except IOError as e:
        error_message = "An error occurred while retrieving user data."
        print(f"IOError: {str(e)}")
        return render_template('general_error.html', error_message=error_message)
    except RuntimeError as e:
        error_message = "An unexpected error occurred."
        print(f"Error: {str(e)}")
        return render_template('general_error.html', error_message=error_message)


@user_bp.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Adds a new user to the system."""
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_password = request.form.get('password')
        email = request.form.get('email')

        try:
            if is_valid_password(user_password):
                encrypted_password = bcrypt.generate_password_hash(user_password).decode('utf-8')
                user_id = id_generator()

                # Call the add_user method and check if the user was added successfully
                if data_manager.add_user(user_name, encrypted_password, user_id, email):
                    return redirect(url_for('user_bp.login', username=user_name))
                else:
                    error_message = "Username already exists. Please choose a different username."
                    return render_template('add_user.html', error_message=error_message)
            else:
                error_message = "Invalid password. Password needs to have at least 8 characters, " \
                                "one uppercase letter, one number and one special character."
                return render_template('add_user.html', error_message=error_message)

        except IOError as e:
            error_message = "An error occurred while adding a new user."
            print(f"IOError: {str(e)}")
            return render_template('general_error.html', error_message=error_message)
        except RuntimeError as e:
            error_message = "An unexpected error occurred."
            print(f"Error: {str(e)}")
            return render_template('general_error.html', error_message=error_message)

    return render_template('add_user.html')


@user_bp.route('/users/<user_id>/manage_account', methods=['GET'])
@login_required
def manage_account(user_id):
    """Renders the manage account page for a specific user."""
    return render_template('manage_account.html', user_id=user_id)


@user_bp.route('/users/<user_id>/manage_account/update_password', methods=['GET', 'POST'])
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

        except TypeError as te:
            print(f"Error: {str(te)}")
            return render_template('general_error.html', error_message="Error retrieving user data")
        except IOError as e:
            error_message = "An error occurred while updating the password."
            print(f"IOError: {str(e)}")
            return render_template('general_error.html', error_message=error_message)
        except RuntimeError as e:
            error_message = "An unexpected error occurred."
            print(f"Error: {str(e)}")
            return render_template('general_error.html', error_message=error_message)

    return render_template('change_password.html', user_id=user_id)


@user_bp.route('/users/<user_id>/manage_account/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    """Deletes a user and all its associated movies """
    if request.method == 'POST':
        user_password = request.form.get('password')
        user_password_2 = request.form.get('confirm_password')

        if user_password == user_password_2:
            try:
                user_data = data_manager.get_user_data()
                for user in user_data:
                    if bcrypt.check_password_hash(user['password'], user_password):
                        data_manager.delete_user(user_id)
                        return redirect(url_for('user_bp.home'))

            except ValueError as e:
                error_message = str(e)
                return render_template('general_error.html', error_message=error_message)
            except RuntimeError as e:
                error_message = str(e)
                return render_template('general_error.html', error_message=error_message)

        else:
            error_message = 'Passwords need to match'
            return render_template('delete_user.html', error_message=error_message)

    return render_template('delete_user.html')


@user_bp.route('/login', methods=['GET', 'POST'])
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
                    return redirect(url_for('movie_bp.user_movies', user_id=user_id))
            else:
                error_message = "Username or password Incorrect, please try again"
                return render_template('login.html', error_message=error_message)

        except IOError as e:
            error_message = "An error occurred while logging in."
            print(f"IOError: {str(e)}")
            return render_template('general_error.html', error_message=error_message)
        except RuntimeError as e:
            error_message = "An unexpected error occurred."
            print(f"Error: {str(e)}")
            return render_template('general_error.html', error_message=error_message)

    return render_template('login.html')


@user_bp.route('/logout')
@login_required
def logout():
    """Logs out the currently logged-in user."""
    logout_user()
    return redirect(url_for('user_bp.home'))
