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
    return render_template('homepage.html')


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def user_movies(user_id):
    user_name = data_manager.get_user_name(user_id)
    movies = data_manager.get_user_movies(user_id)
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


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    user_movie_list = data_manager.get_user_movies(user_id)

    movie_to_update = None
    for movie in user_movie_list:
        if movie['id'] == movie_id:
            movie_to_update = movie

    if request.method == 'POST':
        updated_title = request.form['title']
        updated_director = request.form['director']
        updated_year = request.form['year']
        updated_rating = request.form['rating']
        updated_poster_link = request.form['poster']
        updated_imdb_link = request.form['imdb_link']

        data_manager.update_movie(user_id, movie_id, updated_title, updated_rating,
                                  updated_year, updated_poster_link, updated_director, updated_imdb_link)

        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('update_movie.html', movie_id=movie_id, user_id=user_id, movie=movie_to_update)


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['GET', 'POST'])
def delete_movie(user_id, movie_id):
    if request.method == 'POST':
        data_manager.delete_movie(user_id, movie_id)
        return redirect(url_for('user_movies', user_id=user_id, movie_id=movie_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
