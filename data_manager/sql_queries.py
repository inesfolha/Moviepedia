# Query to get all users
QUERY_GET_ALL_USERS = "SELECT * FROM users"

# Query to get the username by user ID
QUERY_GET_USER_NAME_BY_ID = "SELECT username FROM users WHERE id = :id"

QUERY_GET_MOVIE_BY_TITLE = """
SELECT movie_id
FROM movies
WHERE title = :title
"""

# Query to get all movies associated with a user
QUERY_GET_USER_MOVIES = """
SELECT m.movie_id AS id, m.title, m.director, m.year, m.rating, m.poster, m.movie_link
FROM movies m
JOIN user_movies um ON m.movie_id = um.movie_id
WHERE um.user_id = :user_id
"""


# Query to insert a new movie into the movies table
QUERY_INSERT_MOVIE = """
INSERT INTO movies (movie_id, title, director, year, rating, poster, movie_link)
VALUES (:movie_id, :title, :director, :year, :rating, :poster, :movie_link)
"""

# Query to insert a new entry into the user_movies table to associate a movie with a user
QUERY_INSERT_USER_MOVIE = "INSERT INTO user_movies (user_id, movie_id) VALUES (:user_id, :movie_id)"

# Query to insert a new user into the 'users' table
QUERY_INSERT_USER = """
INSERT INTO users (id, username, password, email)
VALUES (:user_id, :user_name, :password, :email)
"""

# Query to update the details of a movie in the 'movies' table
QUERY_UPDATE_MOVIE = """
UPDATE movies
SET title = :title,
    director = :director,
    year = :year,
    rating = :rating,
    poster = :poster,
    movie_link = :movie_link
WHERE movie_id = :movie_id
"""

# Query to delete a movie from a user's movie list in the 'user_movies' table
QUERY_DELETE_USER_MOVIE = """
DELETE FROM user_movies
WHERE user_id = :user_id
  AND movie_id = :movie_id
"""

# Query to delete a user from the 'users' table
QUERY_DELETE_USER = """
DELETE FROM users
WHERE id = :user_id
"""

# Query to update the password of a user in the 'users' table
QUERY_UPDATE_USER_PASSWORD = """
UPDATE users
SET password = :password
WHERE id = :user_id
"""