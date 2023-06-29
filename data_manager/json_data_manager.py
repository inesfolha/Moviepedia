import json
from movie_web_app.data_manager.data_manager_interface import DataManagerInterface
from movie_web_app.data_manager.file_handler import load_json_data, save_json_file


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename
        self.data = load_json_data(filename)

    def get_all_users(self):
        users = [user['name'] for user in self.data]
        return users

    def get_user_movies(self, user_id):
        user_movies = [user.get('movies') for user in self.data if user['id'] == user_id]
        return user_movies


#movies_data = JSONDataManager('C:/Users/inesf/PycharmProjects/movie_web_app/movie_web_app/data/data.json')
#print(movies_data.get_all_users())
#print(movies_data.get_user_movies(1))
