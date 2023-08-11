api_menu = {
"WELCOME TO MOVEPEDIA API -We have the following routes": [
    {"GET": "api/users - Returns a list of all users"},
    {"GET": "api/users/<user_id>/movies - Returns a list of a user movies"},
    {"POST": "api/users/<user_id>/movies - Adds a movie to a user's list"},
    {"PATCH": "api/users/<user_id>/update_movie/<movie_id> - Updates a user movie details"},
    {"DELETE": "api/users/<user_id>/delete_movie/<movie_id> - Deletes a movie from a user's list"},
    {"POST": "api/add_user - Creates a new user account"},
    {"PUT": "api/users/<user_id>/update_password - Updates a user password"}
]}
