from flask import Flask, render_template, request, redirect, url_for
from data_manager.json_data_manager import JSONDataManager
from helpers.omdb_api_extractor import data_extractor, get_imdb_link
import uuid

app = Flask(__name__)
data_manager = JSONDataManager('data/data.json')


def id_generator():
    """Generates a unique ID using UUID."""
    return str(uuid.uuid4())


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def user_movies(user_id):
    user_name = data_manager.get_user_movies(user_id)[0]
    movies = data_manager.get_user_movies(user_id)[1]
    return render_template('user_movies.html', movies=movies, user_name=user_name, user_id=user_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_id = id_generator()
        user_movie_list = []
        data_manager.add_user(user_name, user_id, user_movie_list)
        return redirect(url_for('list_users'))
    return render_template('add_user.html')


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        movie = request.form.get('movie')

        movie_info = data_extractor(movie)
        movie_link = get_imdb_link(movie)

        if movie_info is not None:
            title = movie_info["Title"]
            if len(movie_info['Ratings']) > 0:
                rating = float(movie_info['Ratings'][0]['Value'].split("/")[0])
            else:
                rating = None

            year = int(movie_info['Year'])
            poster = movie_info['Poster']
            director = movie_info['Director']
            movie_id = id_generator()

            data_manager.add_movie(user_id, movie_id, title, rating, year, poster, director, movie_link)

            return redirect(url_for('user_movies', user_id=user_id))

    return render_template('add_movie.html')


@app.route('/users/<user_id>/update_movie/<movie_id>)')
def update_movie():
    return "This route will display a form allowing for the updating of details of a specific movie in a user’s list."


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie():
    return "Upon visiting this route, a specific movie will be removed from a user’s favorite movie list."


if __name__ == '__main__':
    app.run(debug=True)
