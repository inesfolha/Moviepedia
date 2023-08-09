import uuid
from flask_bcrypt import Bcrypt
import datetime

# Initialize the bcrypt instance
bcrypt = Bcrypt()


def id_generator():
    """Generates a unique ID using UUID."""
    return str(uuid.uuid4())


def save_date():
    current_datetime = datetime.datetime.now()
    formatted_date = current_datetime.strftime("%d-%m-%Y")
    return formatted_date
