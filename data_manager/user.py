from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_data):
        """Initializes a User object with user data."""
        self.id = user_data['id']
        self.name = user_data['name']
        self.password = user_data['password']

    def get_id(self):
        """Gets the ID of the user."""
        return str(self.id)

    @property
    def is_authenticated(self):
        """Checks if the user is authenticated."""
        return True

    @property
    def is_anonymous(self):
        """Checks if the user is anonymous."""
        return False

