from sqlalchemy import create_engine, text, exc
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from data_manager_interface import DataManagerInterface
from sql_queries import (
    QUERY_GET_ALL_USERS,
    QUERY_GET_USER_NAME_BY_ID,
    QUERY_GET_USER_MOVIES,
    QUERY_INSERT_MOVIE,
    QUERY_INSERT_USER,
    QUERY_INSERT_USER_MOVIE,
    QUERY_UPDATE_MOVIE,
    QUERY_DELETE_USER_MOVIE,
    QUERY_DELETE_USER,
    QUERY_UPDATE_USER_PASSWORD,
)


class SQLiteDataManager(DataManagerInterface):
    """
    SQLiteDataManager is a Data Access Layer (DAL) class that provides an
    interface to interact with the SQLite database.
    """

    def __init__(self, db_file_name):
        """
        Initialize a new engine using the given database URI
        """
        db_uri = f"sqlite:///{db_file_name}"
        self._engine = create_engine(db_uri)

    def _execute_query(self, query, params=None):
        """
            Execute an SQL query with the params provided in a dictionary,
            and returns a list of records (dictionary-like objects).
            If an exception was raised, print the error, and return an empty list.
            """
        # try:
        # Create a connection and execute the query with the provided params
        with self._engine.connect() as connection:
            result = connection.execute(text(query), **params) if params else connection.execute(text(query))

            # Get all rows and convert them into a list of dictionary-like records
            records = [dict(row) for row in result]
        return records

        # except exc.SQLAlchemyError as error:
        ## Catch any other unexpected exceptions
        # print("Error executing query:", error)
        # return []

    def get_all_users(self):
        """
        Retrieves a list of all users in the data in the same format as JSONDataManager.
        """
        users = self._execute_query(QUERY_GET_ALL_USERS)
        users_data = [{'name': user['username'], 'id': user['id']} for user in users]
        return users_data

    def get_user_name(self, user_id):
        """
        Retrieves the name of a user based on the provided user ID in the same format as JSONDataManager.
        """
        params = {"id": user_id}
        user = self._execute_query(QUERY_GET_USER_NAME_BY_ID, params)
        return user[0]['username'] if user else None

    def get_user_movies(self, user_id):
        """
        Retrieves the list of movies associated with the provided user ID in the same format as JSONDataManager.
        """
        params = {"user_id": user_id}
        movies = self._execute_query(QUERY_GET_USER_MOVIES, params)
        return movies

    def add_movie(self, user_id, movie_id, title, rating, year, poster, director, movie_link):
        """
        Add a new movie to the 'movies' table and associate it with the user in the same format as JSONDataManager.
        """
        params = {
            "movie_id": movie_id,
            "title": title,
            "director": director,
            "year": year,
            "rating": rating,
            "poster": poster,
            "movie_link": movie_link,
        }
        self._execute_query(QUERY_INSERT_MOVIE, params)

        params = {"user_id": user_id, "movie_id": movie_id}
        self._execute_query(QUERY_INSERT_USER_MOVIE, params)

    def add_user(self, user_name, encrypted_password, user_id, user_movie_list):
        """
        Add a new user with the given name, ID, and movie list to the data in the same format as JSONDataManager.
        """
        params = {
            "user_id": user_id,
            "user_name": user_name,
            "encrypted_password": encrypted_password,
        }
        self._execute_query(QUERY_INSERT_USER, params)

        for movie_id in user_movie_list:
            params = {"user_id": user_id, "movie_id": movie_id}
            self._execute_query(QUERY_INSERT_USER_MOVIE, params)

    def update_movie(self, user_id, movie_id, title, rating, year, poster, director, movie_link):
        """
        Update the details of a movie identified by the user ID and movie ID in the same format as JSONDataManager.
        """
        params = {
            "movie_id": movie_id,
            "title": title,
            "director": director,
            "year": year,
            "rating": rating,
            "poster": poster,
            "movie_link": movie_link,
        }
        self._execute_query(QUERY_UPDATE_MOVIE, params)

    def delete_movie(self, user_id, movie_id):
        """
        Delete a movie with the specified movie ID from the user's movie list in the same format as JSONDataManager.
        """
        params = {"user_id": user_id, "movie_id": movie_id}
        self._execute_query(QUERY_DELETE_USER_MOVIE, params)

    def delete_user(self, user_id):
        """
        Delete a user with the provided user ID from the data in the same format as JSONDataManager.
            """
        params = {"user_id": user_id}
        self._execute_query(QUERY_DELETE_USER, params)

    def get_user_data(self):
        """
        Retrieve user data from the data manager in the same format as JSONDataManager.
        """
        users_data = []
        users = self._execute_query(QUERY_GET_ALL_USERS)
        for user in users:
            username = user['username']
            password = user['password']
            user_id = user['id']
            movies = self.get_user_movies(user_id)
            user_data = {'name': username, 'password': password, 'id': user_id, 'movies': movies}
            users_data.append(user_data)
        return users_data

    def update_password(self, user_id, new_password):
        """
        Update the password of a user in the same format as JSONDataManager.
        """
        params = {"user_id": user_id, "password": new_password}
        self._execute_query(QUERY_UPDATE_USER_PASSWORD, params)

    def close_connection(self):
        """
        Close the connection to the database explicitly when it is no longer needed.
        """
        self._engine.dispose()


file_name = 'data/movie_web_app.sqlite3'
data_manager = SQLiteDataManager(file_name)
data_manager.get_all_users()
