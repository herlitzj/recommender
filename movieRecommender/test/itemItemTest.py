import app.itemItemRecommender as rec
import app.itemItemDataHandler as IIDH
import numpy as np

def test_that_database_query_returns_proper_values():
	return_value = IIDH.database_query("SELECT movie FROM ratings LIMIT 1")[0][0]
	assert return_value == 242

def test_that_get_item_vector_returns_the_correct_vector():
	test_vector = IIDH.get_item_vector(10)
	assert isinstance(test_vector, list)
	assert len(test_vector) == 943
	assert test_vector[0] == 3

def test_that_get_movie_count_returns_proper_movie_count():
	movie_count = IIDH.get_movie_count()
	assert isinstance(movie_count, int)
	assert movie_count == 1682

def test_that_movie_matrix_returns_proper_matrix():
	matrix = IIDH.movie_matrix()
	assert np.shape(matrix) == (1682, 943)
	assert matrix[10][0] == 2

def test_that_cosine_distance_matrix_is_correct_matrix():
	matrix = IIDH.distance_matrix
	assert np.shape(matrix) == (1682, 1682)

def test_that_neighborhood_is_a_list():
	neighborhood = rec.choose_neighbors(5)
	assert isinstance(neighborhood, list)

def test_that_get_user_ratings_returns_proper_list_of_ratings():
	user_ratings = IIDH.get_user_ratings(300)
	assert isinstance(user_ratings, list)
