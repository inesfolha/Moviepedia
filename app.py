from flask import Flask, render_template
from data_manager.json_data_manager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('data/data.json')


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)

    # NEXT


@app.route('/users/<user_id>')  # BUILDING THE OTHER ROUTES + OMDB API INTERFACE
def user_movies():
    # user = data_manager.get_user_movies()
    return "This route will exhibit a specific user’s list of favorite movies. " \
           "We will use the <user_id> in the route to fetch the appropriate user’s movies."


@app.route('/add_user')
def add_user():
    return "This route will present a form that enables the addition of a new user to our MovieWeb App."


@app.route('/users/<user_id>/add_movie')
def add_movie():
    return "This route will display a form to add a new movie to a user’s list of favorite movies."


@app.route('/users/<user_id>/update_movie/<movie_id>)')
def update_movie():
    return "This route will display a form allowing for the updating of details of a specific movie in a user’s list."


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie():
    return "Upon visiting this route, a specific movie will be removed from a user’s favorite movie list."


if __name__ == '__main__':
    app.run(debug=True)
