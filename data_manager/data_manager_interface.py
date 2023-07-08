from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """This class will be responsible for reading the JSON file,
        parsing the JSON into Python data structures (lists and dictionaries),
        and providing methods to manipulate the data (like adding, updating, or removing movies)."""

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_name(self, user_id):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def add_movie(self, user_id, movie_id, title, rating, year, poster, director, movie_link):
        pass

    @abstractmethod
    def add_user(self, user_name, encrypted_password, user_id, user_movie_list):
        pass

    @abstractmethod
    def update_movie(self, user_id, movie_id, title, rating, year, poster, director, movie_link):
        pass

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        pass

    @abstractmethod
    def delete_user(self, user_id):
        pass

    @abstractmethod
    def get_user_data(self):
        pass

    @abstractmethod
    def update_password(self, user_id, new_password):
        pass
