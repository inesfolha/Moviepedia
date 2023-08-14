import os
from flask import render_template, Blueprint, request, flash, get_flashed_messages, redirect, url_for
from dotenv import load_dotenv

import requests
from movie_web_app.data_manager.sqlite_data_manager import SQLiteDataManager
from movie_web_app.helpers.helper_functions import generate_secure_password
from movie_web_app.helpers.helper_functions import bcrypt
from movie_web_app.helpers.chat_gpt_interface import ai_interface, ai_prompt, ai_welcome

load_dotenv()

email_bp = Blueprint('email_bp', __name__)

DATABASE_FILE = os.getenv('DATABASE_FILE')
data_manager = SQLiteDataManager(DATABASE_FILE)

ELASTIC_EMAIL_API_KEY = os.getenv('ELASTICMAILAPIKEY')


def send_notification(subject, recipient, message_body):
    url = 'https://api.elasticemail.com/v2/email/send'
    payload = {
        'apikey': ELASTIC_EMAIL_API_KEY,
        'to': recipient,
        'subject': subject,
        'bodyHtml': message_body,
        'from': 'moviepedia.app@gmail.com'
    }
    response = requests.post(url, data=payload)
    return response.json()


def welcome_email(user_id):
    user = data_manager.get_user_emails(user_id)[0]
    print(user)
    user_name = user['username']
    user_email = user['email']

    welcome_message = ai_interface(ai_welcome(user_name))
    subject = "Welcome to Moviepedia"
    recipient = user_email
    message_body = welcome_message

    response = send_notification(subject, recipient, message_body)
    print(f"Notification sent! Response: {response}")



@email_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """ Updates the user password with a random generated code and sends
    "an email notification to the user with the code to reset his password"""
    try:
        if request.method == 'POST':
            # Get email input
            input_email = request.form.get('email')
            try:
                # check if email address is in database (create a data_manager method)
                user_data = data_manager.check_email_address(input_email)
            except ValueError as e:
                flash(str(e), 'error')
                return redirect(url_for('email_bp.forgot_password'))

            # generate a new password for the user
            new_password = generate_secure_password()
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

            # update the password to the new one (do not forget bcrypt)
            user_id = user_data[0]['ID']
            data_manager.update_password(user_id, hashed_password)

            # send email to the user with the new temporary password and instructions to change it
            # Render the HTML template with the new password
            html_content = render_template('email_reset_password.html', new_password=new_password)

            user_email = user_data[0]['email']
            subject = "Moviepedia Password Reset"
            recipient = user_email
            message_body = html_content

            response = send_notification(subject, recipient, message_body)
            print(f"Notification sent! Response: {response}")
            flash('Email sent!', 'success')
            return redirect(url_for('email_bp.forgot_password'))

        # render template to insert user email address
        success_messages = get_flashed_messages(category_filter=['success'])
        error_messages = get_flashed_messages(category_filter=['error'])
        return render_template('forgot_password.html', error_messages=error_messages, success_messages=success_messages)

    except ValueError as e:
        error_message = str(e)
        return render_template('general_error.html', error_message=error_message)

    except RuntimeError as e:
        error_message = "Error retrieving data from database"
        print(f"Error: {str(e)}")
        return render_template('general_error.html', error_message=error_message)


@email_bp.route('/ai_recommends/<user_id>', methods=['GET', 'POST'])
def ai_recommendations(user_id):
    if request.method == 'POST':
        user = data_manager.get_user_emails(user_id)[0]
        user_id = user['ID']
        user_name = user['username']
        user_email = user['email']
        movies = data_manager.get_user_movies(user_id)
        user_fav_movies = []
        for movie in movies:
            user_fav_movies.append(movie['title'])

        user_recommendations = ai_interface(ai_prompt(user_name, user_fav_movies))
        html_content = user_recommendations

        subject = "Your Moviepedia Recommendations"
        recipient = user_email
        message_body = html_content

        response = send_notification(subject, recipient, message_body)
        print(f"Notification sent! Response: {response}")

        flash('Email sent! Check the spam!!', 'success')
        return redirect(url_for('movie_bp.user_movies', user_id=user_id))
