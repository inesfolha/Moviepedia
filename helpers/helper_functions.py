import uuid
from flask_bcrypt import Bcrypt
import datetime
import secrets
import string

# Initialize the bcrypt instance
bcrypt = Bcrypt()


def generate_secure_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


def id_generator():
    """Generates a unique ID using UUID."""
    return str(uuid.uuid4())


def save_date():
    current_datetime = datetime.datetime.now()
    formatted_date = current_datetime.strftime("%d-%m-%Y")
    return formatted_date
