import json
from movie_web_app.data_manager.data_manager_interface import DataManagerInterface
from movie_web_app.data_manager.file_handler import load_json_data, save_json_file


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename
        self.data = load_json_data(filename)

    def __str__(self):
        return f'{self.data}'

    def get_all_users(self):
        users = [(user['name'], user['id']) for user in self.data]
        return users

    def get_user_name(self, user_id):
        user_name = next((user.get('name') for user in self.data if user['id'] == user_id), None)
        return user_name

    def get_user_movies(self, user_id):
        user_movies = next((user.get('movies') for user in self.data if user['id'] == user_id), None)
        return user_movies

    def add_user(self, user_name, user_id, user_movie_list):
        new_user = {'id': user_id, 'name': user_name, 'movies': user_movie_list}
        self.data.append(new_user)

    def add_movie(self, user_id, movie_id, title, rating, year, poster, director, movie_link):
        for user in self.data:
            if user['id'] == user_id:

                new_movie = {'id': movie_id, 'title': title, 'director': director, 'year': year,
                             'rating': rating, 'poster': poster, 'movie_link': movie_link}

                if 'movies' not in user:
                    user['movies'] = [new_movie]
                else:
                    user['movies'].append(new_movie)

        save_json_file(self.filename, self.data)

    def update_movie(self, user_id, movie_id, title, rating, year, poster, director, movie_link):
        movie_to_update = None
        user_movies = self.get_user_movies(user_id)
        for movie in user_movies:
            if movie['id'] == movie_id:
                movie_to_update = movie
                break

        if movie_to_update:
            movie_to_update['title'] = title
            movie_to_update['rating'] = rating
            movie_to_update['year'] = year
            movie_to_update['poster'] = poster
            movie_to_update['director'] = director
            movie_to_update['movie_link'] = movie_link
            save_json_file(self.filename, self.data)
            return movie_to_update
        else:
            return "Movie not found"

    def delete_movie(self, user_id, movie_id):
        movie_to_delete = None
        user_movies = self.get_user_movies(user_id)

        for movie in user_movies:
            if movie['id'] == movie_id:
                movie_to_delete = movie
                break

        if movie_to_delete:
            user_movies.remove(movie_to_delete)
            save_json_file(self.filename, self.data)
        else:
            return "Movie not found"










#movies_data = JSONDataManager('C:/Users/inesf/PycharmProjects/movies_app_proj/movie_web_app/data/data.json')
#print(movies_data)
#print(movies_data.get_all_users())
#print(movies_data.get_user_movies('dfsxfs'))
#print(movies_data.get_user_movies(1))
#movies_data.add_movie('deadee','movie_id', 'title', 'rating', 'year', 'poster', 'director', 'movie_link')
#print(movies_data.update_movie("07bc496f-27e5-49a9-8f61-a460039da3ad", "ef053db5-d510-49b0-bd3b-7d2a6d217ecd",  "Inception", 8.8, 2010, "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg", "Christopher Nolan", "https://www.imdb.com/title/tt1375666/"))
#print(movies_data)