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

    def get_user_movies(self, user_id):
        user_name = [user.get('name') for user in self.data if user['id'] == user_id]
        user_movies = [user.get('movies') for user in self.data if user['id'] == user_id]
        return user_name, user_movies

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







movies_data = JSONDataManager('C:/Users/inesf/PycharmProjects/movies_app_proj/movie_web_app/data/data.json')
print(movies_data)
#print(movies_data.get_all_users())
#print(movies_data.get_user_movies('dfsxfs'))
#print(movies_data.get_user_movies(1))
#movies_data.add_movie('deadee','movie_id', 'title', 'rating', 'year', 'poster', 'director', 'movie_link')