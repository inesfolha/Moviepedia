from sqlalchemy import create_engine, text, exc

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
    QUERY_GET_MOVIE_BY_TITLE
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

    def _execute_query(self, query, params=None):                         # CHECKED
        """
        Execute an SQL query with the params provided in a dictionary,
        and return a list of records.
        If an exception was raised, print the error, and return an empty list.
        """
        try:
            # Create a connection and execute the query with the provided params
            with self._engine.connect() as connection:
                if params is not None:
                    result = connection.execute(text(query), params)
                else:
                    result = connection.execute(text(query))

                # Check if the result contains rows
                if result.returns_rows:
                    rows = result.fetchall()

                    # Get column names from the result set
                    columns = result.keys()
                    # Convert each row to a dictionary with column names as keys
                    records = [dict(zip(columns, row)) for row in rows]
                    # Commit the changes to the database
                    connection.commit()
                    return records
                else:
                    # Commit the changes to the database
                    connection.commit()
                    return []

        except exc.SQLAlchemyError as error:
            # Catch any other unexpected exceptions
            print("Error executing query:", error)
            return []

    def get_all_users(self):                                                     # CHECKED
        """
        Retrieves a list of all users in the data in the same format as JSONDataManager.
        """
        users = self._execute_query(QUERY_GET_ALL_USERS)
        users_data = [{'name': user['username'], 'id': user['ID']} for user in users]
        if users_data:
            return users_data
        else:
            raise RuntimeError("An error occurred while retrieving user data.")

    def get_user_name(self, user_id):                                      # CHECKED
        """Retrieves the name of a user based on the provided user ID."""
        try:
            params = {"id": user_id}
            user = self._execute_query(QUERY_GET_USER_NAME_BY_ID, params)
            if user:
                return user[0]['username']
            else:
                raise TypeError(f"Error finding the user with id {user_id}")
        except Exception as e:
            raise RuntimeError("An error occurred while retrieving user data.") from e

    def get_user_movies(self, user_id):                                                    # CHECKED
        """
        Retrieves the list of movies associated with the provided user ID in the same format as JSONDataManager.
        """
        params = {"user_id": user_id}
        movies = self._execute_query(QUERY_GET_USER_MOVIES, params)
        return movies

    def _get_movie_by_title(self, title):                                                     # CHECKED
        """
        Retrieves a movie by title from the 'movies' table.
        Returns None if the movie does not exist.
        """
        params = {"title": title}
        result = self._execute_query(QUERY_GET_MOVIE_BY_TITLE, params)
        return result[0] if result else None

    def add_movie(self, user_id, movie_id, title, rating, year, poster, director, movie_link):       # CHECKED
        """Adds a new movie to the movie list of the user with the provided user ID."""
        existing_movie = self._get_movie_by_title(title)

        if existing_movie:
            movie_id = existing_movie["movie_id"]
            print('movie already exists')
        else:
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

        # Associate the movie with the user in the 'user_movies' table
        params = {"user_id": user_id, "movie_id": movie_id}
        self._execute_query(QUERY_INSERT_USER_MOVIE, params)
        return True

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


file_name = r'C:\Users\inesf\PycharmProjects\movie_web_app(phase5)\movie_web_app\data\movie_web_app.sqlite3'
data_manager = SQLiteDataManager(file_name)
print(data_manager.get_all_users())  # Works
print('should be Bob: ', data_manager.get_user_name('deadee'))  # Works
print('bob movies:',data_manager.get_user_movies('deadee'))  # Works
print(data_manager.add_movie('1', "26983540-d74a-4aba-aa17-259f9b2e2208", "Spider-Man: Across the Spider-Verse", 9.1,
2023, "https://m.media-amazon.com/images/M/MV5BNzQ1ODUzYjktMzRiMS00ODNiLWI4NzQtOTRiN2VlNTNmODFjXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_SX300.jpg"
, "Joaquim Dos Santos, Kemp Powers, Justin K. Thompson", "https://www.imdb.com/title/tt9362722/")) # WORKS
