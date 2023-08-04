import uuid
from flask_bcrypt import Bcrypt

# Initialize the bcrypt instance
bcrypt = Bcrypt()


def id_generator():
    """Generates a unique ID using UUID."""
    return str(uuid.uuid4())
