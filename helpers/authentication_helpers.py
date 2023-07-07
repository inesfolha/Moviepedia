from flask_bcrypt import Bcrypt


def is_valid_password(user_password):
    required_conditions = [
        len(user_password) >= 8,
        # check for an uppercase letter
        any(character.isupper() for character in user_password),
        # check for a number
        any(character.isdigit() for character in user_password),
        # check for a non-alphanumeric character
        any(not character.isalnum() for character in user_password)
    ]

    return all(required_conditions)
