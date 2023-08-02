from sqlalchemy import create_engine, text, exc

from data_manager_interface import DataManagerInterface
from sql_queries import (
    QUERY_GET_ALL_USERS,
    QUERY_GET_USER_NAME_BY_ID,
    QUERY_GET_USER_MOVIES,
    QUERY_INSERT_MOVIE,
    QUERY_INSERT_USER,
    QUERY_INSERT_USER_MOVIE,
    QUERY_DELETE_USER_MOVIE,
    QUERY_DELETE_USER,
    QUERY_UPDATE_USER_PASSWORD,
    QUERY_GET_MOVIE_BY_TITLE,
    QUERY_CHECK_MOVIE_ASSOCIATION,
    QUERY_DELETE_MOVIE,
    QUERY_CHECK_EXISTING_USER,
    QUERY_DELETE_USER_MOVIES,
    QUERY_DELETE_ORPHAN_MOVIES,
    QUERY_CHECK_EXISTING_MOVIE
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

    def _execute_query(self, query, params=None):  # CHECKED
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

    def get_all_users(self):  # CHECKED
        """Retrieves a list of all users in the database."""
        users = self._execute_query(QUERY_GET_ALL_USERS)
        users_data = [{'name': user['username'], 'id': user['ID']} for user in users]
        if users_data:
            return users_data
        else:
            raise RuntimeError("An error occurred while retrieving user data.")

    def get_user_name(self, user_id):  # CHECKED
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

    def get_user_movies(self, user_id):  # CHECKED
        """Retrieves the list of movies associated with the provided user ID."""
        params = {"id": user_id}
        user = self._execute_query(QUERY_GET_USER_NAME_BY_ID, params)
        if user:
            params = {"user_id": user_id}
            movies = self._execute_query(QUERY_GET_USER_MOVIES, params)
            return movies

    def _get_movie_by_title(self, title):  # CHECKED
        """
        Retrieves a movie by title from the 'movies' table.
        Returns None if the movie does not exist.
        """
        params = {"title": title}
        result = self._execute_query(QUERY_GET_MOVIE_BY_TITLE, params)
        return result[0] if result else None

    def add_movie(self, user_id, movie_id, title, rating, year, poster, director, movie_link):  # CHECKED
        """Adds a new movie to the movie list of the user with the provided user ID."""
        existing_movie = self._get_movie_by_title(title)

        user = self.get_user_name(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

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

    def add_user(self, user_name, encrypted_password, user_id, email):  # CHECKED
        """Adds a new user with the given name, ID, and movie list to the database."""
        # Check if the provided username is already in use
        params = {"username": user_name}
        existing_user = self._execute_query(QUERY_CHECK_EXISTING_USER, params)

        if existing_user:
            return False  # User already exists

        params = {
            "user_id": user_id,
            "user_name": user_name,
            "password": encrypted_password,
            "email": email,
        }
        self._execute_query(QUERY_INSERT_USER, params)
        return True  # User added successfully

    def update_movie(self, user_id, old_movie_id, new_movie_id, title, rating, year, poster, director,
                     movie_link):
        """ Updates the details of a movie identified by the user ID and movie ID,
        by creating an alias of the same movie with a different id associated with that user """

        # Check if the movie exists
        params = {"movie_id": old_movie_id}
        existing_movie = self._execute_query(QUERY_CHECK_EXISTING_MOVIE, params)
        if not existing_movie:
            raise ValueError(f"Movie with not found")

        # Check if the user exists
        user = self.get_user_name(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        params = {
                "movie_id": new_movie_id,
                "title": title,
                "director": director,
                "year": year,
                "rating": rating,
                "poster": poster,
                "movie_link": movie_link,
            }
        params_2 = {
                "movie_id": new_movie_id,
                "user_id": user_id,
            }

        params_3 = {
                "movie_id": old_movie_id,
                "user_id": user_id,
            }

        # Add new updated movie
        self._execute_query(QUERY_INSERT_MOVIE, params)

        # Associate it with the user
        self._execute_query(QUERY_INSERT_USER_MOVIE, params_2)

        # Delete association with the old movie details
        self._execute_query(QUERY_DELETE_USER_MOVIE, params_3)
        return True

    def delete_movie(self, user_id, movie_id):  # CHECKED
        """Deletes a movie with the specified movie ID from the user's movie list.
        Deletes the movie from the database if it is not associated with any other users"""

        # Check if the movie exists
        params = {"movie_id": movie_id}
        existing_movie = self._execute_query(QUERY_CHECK_EXISTING_MOVIE, params)
        if not existing_movie:
            raise ValueError(f"Movie with not found")

        # Check if the user exists
        user = self.get_user_name(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        # Check if the movie ID is associated with any other user
        params = {"user_id": user_id,
                  "movie_id": movie_id}
        result = self._execute_query(QUERY_CHECK_MOVIE_ASSOCIATION, params)

        # If the movie is not associated with any other user, delete it from the movies table
        if not result:
            params = {"user_id": user_id, "movie_id": movie_id}
            self._execute_query(QUERY_DELETE_USER_MOVIE, params)

            # Also delete the movie from the movies table
            self._execute_query(QUERY_DELETE_MOVIE, params)
            return True

        else:
            # Movie is associated with other users, so only remove it from the current user's list
            params = {"user_id": user_id, "movie_id": movie_id}
            self._execute_query(QUERY_DELETE_USER_MOVIE, params)
            return False

    def delete_user(self, user_id):
        """Delete a user with the provided user ID from the data and all it's associated movies"""
        # Check if the user exists
        user = self.get_user_name(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        # Delete the user's associated movies from the user_movies table
        params = {"user_id": user_id}
        self._execute_query(QUERY_DELETE_USER_MOVIES, params)

        # Delete all movies that are not associated with anyone else
        self._execute_query(QUERY_DELETE_ORPHAN_MOVIES)

        # Delete the user from the users table
        self._execute_query(QUERY_DELETE_USER, params)
        return True

    def get_user_data(self):  # CHECKED
        """Retrieves user data from the database"""
        users_data = []
        users = self._execute_query(QUERY_GET_ALL_USERS)
        for user in users:
            username = user['username']
            password = user['password']
            user_id = user['ID']
            movies = self.get_user_movies(user_id)
            user_data = {'name': username, 'password': password, 'id': user_id, 'movies': movies}
            users_data.append(user_data)
        return users_data

    def update_password(self, user_id, new_password):                  #CHECKED
        """Updates the password of a user."""
        # Check if the user exists
        user = self.get_user_name(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        params = {"user_id": user_id, "password": new_password}
        self._execute_query(QUERY_UPDATE_USER_PASSWORD, params)
        return True

    def close_connection(self):
        """
        Close the connection to the database explicitly when it is no longer needed.
        """
        self._engine.dispose()


file_name = r'C:\Users\inesf\PycharmProjects\movie_web_app(phase5)\movie_web_app\data\movie_web_app.sqlite3'
data_manager = SQLiteDataManager(file_name)
# print(data_manager.get_all_users())  # Works
# print('should be Bob: ', data_manager.get_user_name('deadee'))  # Works
# print('bob movies:',data_manager.get_user_movies('deadee'))  # Works
# print(data_manager.add_movie('deadee', "26983540-d74a-4aba-aa17-259f9b2e2208", "Spider-Man: Across the Spider-Verse", 9.1,
# 2023, "https://m.media-amazon.com/images/M/MV5BNzQ1ODUzYjktMzRiMS00ODNiLWI4NzQtOTRiN2VlNTNmODFjXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_SX300.jpg"
# , "Joaquim Dos Santos, Kemp Powers, Justin K. Thompson", "https://www.imdb.com/title/tt9362722/")) # WORKS
# print(data_manager.add_user('leaf', 'superhashedpassword', 'supermegauuid', 'email@leaf.com')) # WORKS
# print(data_manager.update_movie('deadee', "26983540-d74a-4aba-aa17-259f9b2e2208","new movie id test", "Spider-Man: Across the Spider-Verse", 9.1,  #WORKS
# 2023, "https://m.media-amazon.com/images/M/MV5BNzQ1ODUzYjktMzRiMS00ODNiLWI4NzQtOTRiN2VlNTNmODFjXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_SX300.jpg", "Joaquim Dos Santos, Kemp Powers, Justin K. Thompson", "https://www.imdb.com/title/tt9362722/"))
# print(data_manager.delete_movie('deadee', "new movie id test")) # WORKS
# print(data_manager.add_user('Ines', 'encrypted_password', 'user_id', 'email')) #WORKS
# print(data_manager.get_user_data()) # WORKS
# print(data_manager.delete_user('user_id')) #WORKS
#data_manager.add_movie('supermegauuid', 'movie_id', 'title', 'rating', 'year', 'poster', 'director', 'movie_link')
# data_manager.delete_user('supermegauuid')
#print(data_manager.add_user('usertest', 'encrypted_password', 'user_id', 'email'))
#print(data_manager.update_password('user_id', 'newand changedpassword')) #WORKS
