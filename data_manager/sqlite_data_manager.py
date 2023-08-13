from sqlalchemy import create_engine, text, exc

from .data_manager_interface import DataManagerInterface
from .sql_queries import (
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
    QUERY_DELETE_MOVIE,
    QUERY_CHECK_EXISTING_USER,
    QUERY_DELETE_USER_MOVIES,
    QUERY_DELETE_ALIAS_ORPHAN_MOVIES,
    QUERY_CHECK_EXISTING_MOVIE,
    QUERY_GET_MOVIE_REVIEWS,
    QUERY_CHECK_PUBLISHED_REVIEW,
    QUERY_ADD_REVIEW,
    QUERY_EDIT_REVIEW,
    QUERY_DELETE_REVIEW,
    QUERY_CHECK_REVIEW,
    QUERY_CHECK_EXISTING_LIKE,
    QUERY_ADD_LIKE,
    QUERY_REMOVE_LIKE,
    QUERY_INCREMENT_LIKES,
    QUERY_DECREMENT_LIKES,
    QUERY_GET_MOVIE_DETAILS,
    QUERY_GET_REVIEW_DETAILS,
    QUERY_GET_REVIEW_LIKES,
    QUERY_UPDATE_USER_MOVIE,
    QUERY_FIND_ORIGINAL_MOVIE_ID,
    QUERY_CHECK_USER_MOVIE,
    QUERY_UPDATE_MOVIE_BY_USER_UPDATED_ID,
    QUERY_GET_USER_BY_EMAIL,
    QUERY_GET_ALL_USER_DATA,
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
        else:
            raise TypeError(f"Error finding the movies list for user id {user_id}")

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
        params = {"user_id": user_id, "movie_id": movie_id, "user_updated_movie_id": movie_id}
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

        # Check if movie_id = user_updated_movie_id from user_movies table
        params_check = {
            "user_id": user_id,
            "movie_id": old_movie_id
        }
        user_updated_movie = self._execute_query(QUERY_CHECK_USER_MOVIE, params_check)
        if len(user_updated_movie) > 0:
            # The user is editing the movie for the first time, so it will create an alias
            params_insert = {
                "movie_id": new_movie_id,
                "title": title,
                "director": director,
                "year": year,
                "rating": rating,
                "poster": poster,
                "movie_link": movie_link,
            }
            self._execute_query(QUERY_INSERT_MOVIE, params_insert)
            print('New movie added')
        else:
            # User already has one alias of that movie, so it will update the existing one
            params_update = {
                "movie_id": new_movie_id,
                "title": title,
                "director": director,
                "year": year,
                "rating": rating,
                "poster": poster,
                "movie_link": movie_link,
                "user_updated_movie_id": old_movie_id,
            }
            self._execute_query(QUERY_UPDATE_MOVIE_BY_USER_UPDATED_ID, params_update)
            print('Movie updated')

            # Update the user_movies user_updated_movie_id with the new movie_id
        params_update_user_movie = {
            "new_movie_id": new_movie_id,
            "old_movie_id": old_movie_id,
            "user_id": user_id,
        }
        self._execute_query(QUERY_UPDATE_USER_MOVIE, params_update_user_movie)
        print('User movies updated')
        return True

    def delete_movie(self, user_id, movie_id):
        """Deletes a movie with the specified movie ID from the user's movie list.
        Deletes the movie from the database if it's an alias"""

        # Check if the movie exists
        params = {"movie_id": movie_id}
        existing_movie = self._execute_query(QUERY_CHECK_EXISTING_MOVIE, params)
        if not existing_movie:
            raise ValueError(f"Movie not found")

        # Check if the user exists
        user = self.get_user_name(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        # Check if the movie has been updated
        params = {
            "user_id": user_id,
            "movie_id": movie_id
        }
        user_updated_movie = self._execute_query(QUERY_CHECK_USER_MOVIE, params)
        if len(user_updated_movie) == 0:
            # The movie is an alias we can delete from movies and user_movies
            self._execute_query(QUERY_DELETE_MOVIE, params)
            self._execute_query(QUERY_DELETE_USER_MOVIE, params)
            print('deleted alias movie from movies')
            return True

        else:
            # Movie is original data, only remove it from user_movies
            params = {"user_id": user_id, "movie_id": movie_id}
            self._execute_query(QUERY_DELETE_USER_MOVIE, params)
            print('deleted movie association with the user')
            return False

    def delete_user(self, user_id):
        """Delete a user with the provided user ID from the data and all it's associated movies"""
        # Check if the user exists
        user = self.get_user_name(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        params = {"user_id": user_id}
        # Delete all alias movies
        self._execute_query(QUERY_DELETE_ALIAS_ORPHAN_MOVIES, params)

        # Delete the user's associated movies from the user_movies table
        self._execute_query(QUERY_DELETE_USER_MOVIES, params)

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

    def update_password(self, user_id, new_password):  # CHECKED
        """Updates the password of a user."""
        # Check if the user exists
        user = self.get_user_name(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        params = {"user_id": user_id, "password": new_password}
        self._execute_query(QUERY_UPDATE_USER_PASSWORD, params)
        return True

    def get_all_movie_reviews(self, updated_movie_id):  # CHECKED
        """retrieves all the movie info and reviews for a movie with the provided ID"""

        params = {"updated_movie_id": updated_movie_id}
        movie_id_dict = self._execute_query(QUERY_FIND_ORIGINAL_MOVIE_ID, params)
        movie_id = movie_id_dict[0]['movie_id']

        # Check if the movie exists
        params = {"movie_id": movie_id}
        existing_movie = self._execute_query(QUERY_CHECK_EXISTING_MOVIE, params)
        if not existing_movie:
            raise ValueError(f"Movie reviews not found")

        params = {"movie_id": movie_id}
        movie_reviews = self._execute_query(QUERY_GET_MOVIE_REVIEWS, params)

        return movie_reviews

    def add_reviews(self, review_id, user_id, movie_id, rating, review_text, review_title, likes_count,
                    publication_date):  # CHECKED
        """Allows the user to publish a review for a certain movie with the given ID"""
        # Check if the movie exists
        params = {"movie_id": movie_id}
        existing_movie = self._execute_query(QUERY_CHECK_EXISTING_MOVIE, params)
        if not existing_movie:
            raise ValueError(f"Movie with not found")

        # Check if the user exists
        user = self.get_user_name(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        # Check if the user has a published review on that movie
        params = {'user_id': user_id, 'movie_id': movie_id}
        reviews_count = self._execute_query(QUERY_CHECK_PUBLISHED_REVIEW, params)[0]['review_count']
        if reviews_count and reviews_count != 0:
            raise ValueError("You already reviewed this movie, please edit your existing review.")

        params = {
            "review_id": review_id,
            "user_id": user_id,
            "movie_id": movie_id,
            "rating": rating,
            "review_title": review_title,
            "review_text": review_text,
            "likes_count": likes_count,
            "publication_date": publication_date
        }

        self._execute_query(QUERY_ADD_REVIEW, params)
        return True

    def edit_reviews(self, review_id, user_id, movie_id, rating, review_text, review_title, edit_date):  # CHECKED
        # Check if the movie exists
        params = {"movie_id": movie_id}
        existing_movie = self._execute_query(QUERY_CHECK_EXISTING_MOVIE, params)
        if not existing_movie:
            raise ValueError(f"Movie with not found")

        # Check if the user exists
        user = self.get_user_name(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        params = {
            "review_id": review_id,
            "review_title": review_title,
            "review_text": review_text,
            "edit_date": edit_date,
            "rating": rating,
        }

        self._execute_query(QUERY_EDIT_REVIEW, params)
        return True

    def delete_reviews(self, user_id, movie_id, review_id):  # CHECKED
        # Check if the movie exists
        params = {"movie_id": movie_id}
        existing_movie = self._execute_query(QUERY_CHECK_EXISTING_MOVIE, params)
        if not existing_movie:
            raise ValueError(f"Movie with not found")

        # Check if the user exists
        user = self.get_user_name(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        # Check if the review exists
        params = {"review_id": review_id}
        existing_review = self._execute_query(QUERY_CHECK_REVIEW, params)
        if not existing_review:
            raise ValueError(f"Review not found with ID {review_id}")

        # Delete the review
        self._execute_query(QUERY_DELETE_REVIEW, params)
        return True

    def like_review(self, user_id, review_id):
        # Check if the user exists
        user = self.get_user_name(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        # Check if the review exists
        params = {"review_id": review_id}
        existing_review = self._execute_query(QUERY_CHECK_REVIEW, params)
        if not existing_review:
            raise ValueError(f"Review not found with ID {review_id}")

        # Check if this user_id already has a like on that review_id
        params = {"user_id": user_id, "review_id": review_id}
        existing_like = self._execute_query(QUERY_CHECK_EXISTING_LIKE, params)
        if existing_like:
            raise ValueError('Movie already liked')

        # add the like to the user_likes table (user_id, review_id)
        self._execute_query(QUERY_ADD_LIKE, params)
        # increase the likes count (likes) integer on the reviews table for that review_id
        self._execute_query(QUERY_INCREMENT_LIKES, params)
        return True

    def unlike_review(self, user_id, review_id):
        # Check if the user exists
        user = self.get_user_name(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        # Check if the review exists
        params = {"review_id": review_id}
        existing_review = self._execute_query(QUERY_CHECK_REVIEW, params)
        if not existing_review:
            raise ValueError(f"Review not found with ID {review_id}")

        # remove the row like from the user_likes table (user_id, review_id)
        params = {"user_id": user_id, "review_id": review_id}
        self._execute_query(QUERY_REMOVE_LIKE, params)
        # decrease the likes count (likes) integer on the reviews table for that review_id
        self._execute_query(QUERY_DECREMENT_LIKES, params)
        return True

    def get_movie_details(self, movie_id):
        """Retrieves a movie by its ID from the database."""
        params = {"movie_id": movie_id}
        movie = self._execute_query(QUERY_GET_MOVIE_DETAILS, params)
        if movie:
            return movie[0]
        else:
            raise ValueError(f"Movie not found")

    def get_review_info(self, review_id):
        """Retrieves a review by its ID from the database."""
        params = {"review_id": review_id}
        review = self._execute_query(QUERY_GET_REVIEW_DETAILS, params)
        if review:
            return review[0]
        else:
            raise ValueError(f"Review not found")

    def movie_review_likes(self, movie_id):
        """retrieves a list of users who have liked reviews for a given movie_id"""

        # Check if the movie exists
        params = {"movie_id": movie_id}
        existing_movie = self._execute_query(QUERY_CHECK_EXISTING_MOVIE, params)
        if not existing_movie:
            raise ValueError(f"Movie with not found")

        params = {'movie_id': movie_id}
        likes = self._execute_query(QUERY_GET_REVIEW_LIKES, params)
        review_likes = {}
        for like in likes:
            review_id = like['review_id']
            liked_user_id = like['liked_user_id']
            if review_id not in review_likes:
                review_likes[review_id] = []
            review_likes[review_id].append(liked_user_id)

        return review_likes

    def check_email_address(self, email):
        # Check if email inserted is in database, users
        params = {"email": email}
        user_data = self._execute_query(QUERY_GET_USER_BY_EMAIL, params)
        if user_data:
            return user_data
        else:
            raise ValueError("Email not found in the database.")

    def get_user_emails(self, user_id):
        params = {"user_id": user_id}
        user_data = self._execute_query(QUERY_GET_ALL_USER_DATA, params)
        if user_data:
            return user_data
        else:
            raise ValueError("User not found")

    def close_connection(self):
        """
        Close the connection to the database explicitly when it is no longer needed.
        """
        self._engine.dispose()
