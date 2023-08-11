import os

from dotenv import load_dotenv
from flask import Blueprint, jsonify, request

from movie_web_app.data_manager.sqlite_data_manager import SQLiteDataManager
from movie_web_app.helpers.authentication_helpers import is_valid_password
from movie_web_app.helpers.helper_functions import bcrypt
from movie_web_app.helpers.helper_functions import id_generator
from movie_web_app.static.api_menu import api_menu

load_dotenv()

# Create the user_bp Blueprint
api_user = Blueprint('api_user', __name__)

DATABASE_FILE = os.getenv('DATABASE_FILE')
data_manager = SQLiteDataManager(DATABASE_FILE)


@api_user.route('/', methods=['GET'])
def home():
    return jsonify(str(api_menu))


@api_user.route('/add_user', methods=['POST'])
def add_user():
    """Adds a new user to the database."""
    if request.method == 'POST':
        json_data = request.json  # Access JSON data from the request body
        user_name = json_data.get('name')
        user_password = json_data.get('password')
        email = json_data.get('email')

        if not user_name or not user_password or not email:
            raise ValueError('Sign up unsuccessful -  Missing fields')

        try:
            if is_valid_password(user_password):
                encrypted_password = bcrypt.generate_password_hash(user_password).decode('utf-8')
                user_id = id_generator()

                # Call the add_user method and check if the user was added successfully
                if data_manager.add_user(user_name, encrypted_password, user_id, email):
                    return jsonify('user added successfully')
                else:
                    error_message = "Username already exists. Please choose a different username."
                    return jsonify(error_message)
            else:
                error_message = "Invalid password. Password needs to have at least 8 characters, " \
                                "one uppercase letter, one number and one special character."
                return jsonify(error_message)
        except ValueError as ve:
            return jsonify(str(ve))
        except IOError as e:
            error_message = "An error occurred while adding a new user."
            print(f"IOError: {str(e)}")
            return jsonify(error_message)
        except RuntimeError as e:
            error_message = "An unexpected error occurred."
            print(f"Error: {str(e)}")
            return jsonify(error_message)


@api_user.route('/users/<user_id>/update_password', methods=['PUT'])
def change_password(user_id):
    """Updates the password for a specific user."""
    json_data = request.json  # Access JSON data from the request body
    current_password = json_data.get('current_password')
    new_password = json_data.get('new_password')
    if not current_password or not new_password:
        raise ValueError('Error -  Missing fields')
    try:
        user_data = data_manager.get_user_data()
        user = next(user for user in user_data if user['id'] == user_id)
        if user and bcrypt.check_password_hash(user['password'], current_password):
            if is_valid_password(new_password):
                encrypted_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                data_manager.update_password(user_id, encrypted_password)
                message = "Password successfully updated"
                return jsonify(message)

            else:
                error_message = "Invalid password. Password needs to have at least 8 characters, " \
                                "one uppercase letter, one number and one special character."
                return jsonify(error_message)
        else:
            error_message = "Password Incorrect, please try again"
            return jsonify(error_message)

    except TypeError as te:
        print(f"Error: {str(te)}")
        return jsonify(str(te))
    except IOError as e:
        error_message = "An error occurred while updating the password."
        print(f"IOError: {str(e)}")
        return jsonify(error_message)
    except RuntimeError as e:
        error_message = "An unexpected error occurred."
        print(f"Error: {str(e)}")
        return jsonify(error_message)


@api_user.route('/users/<user_id>/delete_user', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user and all its associated movies """
    json_data = request.json  # Access JSON data from the request body
    user_password = json_data.get('password')
    user_password_2 = json_data.get('confirm_password')

    if not user_password or not user_password_2:
        raise ValueError('Error -  Missing fields')

    if user_password == user_password_2:
        try:
            user_data = data_manager.get_user_data()
            for user in user_data:
                if bcrypt.check_password_hash(user['password'], user_password):
                    data_manager.delete_user(user_id)
                    return jsonify("User successfully deleted")

        except ValueError as e:
            error_message = str(e)
            return jsonify(error_message)
        except RuntimeError as e:
            error_message = str(e)
            return jsonify(error_message)
    else:
        error_message = 'Passwords need to match'
        return jsonify(error_message)
