api_menu = {
"WELCOME TO MOVEPEDIA API -We have the following routes": [
    {"GET": "api/users - Returns a list of all users"},
    {"GET": "api/users/<user_id>/movies - Returns a list of a user movies"},
    {"POST": "api/users/<user_id>/movies - Adds a movie to a user's list"},
    {"PATCH": "api/users/<user_id>/update_movie/<movie_id> - Updates a user movie details"},
    {"DELETE": "api/users/<user_id>/delete_movie/<movie_id> - Deletes a movie from a user's list"},
    {"POST": "api/add_user - Creates a new user account"},
    {"PUT": "api/users/<user_id>/update_password - Updates a user password"},
    {"DELETE": "api/users/<user_id>/delete_user - Deletes a user account"},
    {"GET": "api/movie_details/<movie_id> - Loads the movie details and user reviews"},
    {"POST": "api/add_review/<user_id>/<movie_id> - Adds a review to a certain movie"},
    {"POST": "api/like_review/<user_id>/<review_id>/<movie_id> - Allows a user to like or unlike a review"},
    {"PATCH": "api/edit_review/<user_id>/<movie_id>/<review_id> - Allows a user to edit a review "},
    {"PATCH": "api/delete_review/<user_id>/<movie_id>/<review_id>  Allows a user to delete a review- "},
]}

