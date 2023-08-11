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
JOIN user_movies um ON m.movie_id = um.user_updated_movie_id
WHERE um.user_id = :user_id
"""

# Query to insert a new movie into the movies table
QUERY_INSERT_MOVIE = """
INSERT INTO movies (movie_id, title, director, year, rating, poster, movie_link)
VALUES (:movie_id, :title, :director, :year, :rating, :poster, :movie_link)
"""

# Query to insert a new entry into the user_movies table to associate a movie with a user
QUERY_INSERT_USER_MOVIE = """INSERT INTO user_movies (user_id, movie_id, user_updated_movie_id) VALUES (:user_id, 
                          :movie_id, :movie_id)"""

# Query to insert a new user into the 'users' table
QUERY_INSERT_USER = """
INSERT INTO users (id, username, password, email)
VALUES (:user_id, :user_name, :password, :email)
"""

# Query to delete a movie from a user's movie list in the 'user_movies' table
QUERY_DELETE_USER_MOVIE = """
DELETE FROM user_movies
WHERE user_id = :user_id
  AND user_updated_movie_id = :movie_id
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


# Query to check if the movie ID is associated with any other user
QUERY_CHECK_MOVIE_ASSOCIATION = """
SELECT 1 FROM user_movies
WHERE movie_id = :movie_id
AND user_id != :user_id
LIMIT 1;
"""


# Query to delete the movie from the movies table if it's not associated with any other user
QUERY_DELETE_MOVIE = """
DELETE FROM movies
WHERE movie_id = :movie_id
AND NOT EXISTS (
    SELECT 1 FROM user_movies
    WHERE movie_id = :movie_id
    LIMIT 1
); """


QUERY_CHECK_EXISTING_USER = """
SELECT 1 FROM users
WHERE username = :username
LIMIT 1;
"""

QUERY_DELETE_USER_MOVIES = """
DELETE FROM user_movies
WHERE user_id = :user_id;"""

QUERY_DELETE_ALIAS_ORPHAN_MOVIES = """
DELETE FROM movies
WHERE movie_id IN (
    SELECT um.user_updated_movie_id
    FROM user_movies um
    WHERE um.user_id = :user_id AND um.user_updated_movie_id != um.movie_id
);
"""


QUERY_CHECK_EXISTING_MOVIE = """
SELECT 1 FROM movies
WHERE movie_id = :movie_id
LIMIT 1;
"""

QUERY_GET_MOVIE_REVIEWS = """
SELECT r.*, u.username, m.title
FROM reviews r
JOIN users u ON r.user_id = u.ID
JOIN movies m ON r.movie_id == m.movie_id
WHERE r.movie_id = :movie_id
"""

QUERY_CHECK_PUBLISHED_REVIEW = """
SELECT COUNT(*) AS review_count
FROM reviews
WHERE user_id = :user_id AND movie_id = :movie_id
"""

QUERY_ADD_REVIEW = """
INSERT INTO reviews (review_id, user_id, movie_id, rating, review_text, likes, publication_date)
VALUES (:review_id, :user_id, :movie_id, :rating, :review_text, :likes_count, :publication_date);

"""

QUERY_EDIT_REVIEW = """
UPDATE reviews
SET review_title = :review_title,
    review_text = :review_text,
    edit_date = :edit_date,
    rating = :rating
WHERE review_id = :review_id;
"""

QUERY_DELETE_REVIEW = """
DELETE FROM reviews
WHERE review_id = :review_id;
"""

QUERY_CHECK_REVIEW = """
SELECT COUNT(*) AS review_count
FROM reviews
WHERE review_id = :review_id;
"""

QUERY_CHECK_EXISTING_LIKE = """
SELECT 1
FROM user_likes
WHERE user_id = :user_id AND review_id = :review_id;
"""

QUERY_ADD_LIKE = """
INSERT INTO user_likes (user_id, review_id)
VALUES (:user_id, :review_id);
"""

QUERY_REMOVE_LIKE = """
DELETE FROM user_likes
WHERE user_id = :user_id AND review_id = :review_id;
"""

QUERY_INCREMENT_LIKES = """
UPDATE reviews
SET likes = likes + 1
WHERE review_id = :review_id;
"""

QUERY_DECREMENT_LIKES = """
UPDATE reviews
SET likes = likes - 1
WHERE review_id = :review_id;
"""

QUERY_GET_MOVIE_DETAILS = """
SELECT * FROM movies WHERE movie_id = :movie_id
"""

QUERY_GET_REVIEW_DETAILS = """
SELECT * FROM reviews WHERE review_id = :review_id"""

QUERY_GET_REVIEW_LIKES = """
SELECT
    r.review_id,
    ul.user_id AS liked_user_id
FROM
    reviews AS r
LEFT JOIN
    user_likes AS ul ON r.review_id = ul.review_id
WHERE
    r.movie_id = :movie_id
ORDER BY
    r.review_id;
"""

QUERY_UPDATE_USER_MOVIE = """
UPDATE user_movies
SET user_updated_movie_id = :new_movie_id
WHERE user_id = :user_id
AND movie_id = :old_movie_id;
"""

QUERY_FIND_ORIGINAL_MOVIE_ID = """
SELECT movie_id
FROM user_movies
WHERE user_updated_movie_id = :updated_movie_id;
"""

QUERY_CHECK_USER_MOVIE = """
SELECT 1
FROM user_movies
WHERE user_id = :user_id AND movie_id = :movie_id AND user_updated_movie_id = movie_id;
"""

QUERY_UPDATE_MOVIE_BY_USER_UPDATED_ID = """
UPDATE movies
SET title = :title,
    director = :director,
    year = :year,
    rating = :rating,
    poster = :poster,
    movie_link = :movie_link
WHERE movie_id = :user_updated_movie_id;
"""


