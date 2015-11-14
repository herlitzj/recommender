import MySQLdb as mdb
import numpy as np


connection = mdb.connect('localhost', 'root', 'root', 'movieRatings');

def database_query(query):
	cursor = connection.cursor()
	cursor.execute(query)
	return cursor.fetchall()

def database_write(query):
	cursor = connection.cursor()
	cursor.execute(query)
	connection.commit()

def get_user_ratings(user_id):
	user_ratings = database_query("SELECT movie, rating FROM ratings WHERE user={0}".format(user_id))
	return user_ratings

def get_item_vector(item_number):
	item_vector = []
	rows = database_query('SELECT * FROM (SELECT id FROM users)U left join (SELECT movie, user, rating FROM ratings WHERE movie = {0})R on U.id=R.user'.format(item_number))
	for row in rows:
		if row[3] != None:
			item_vector.append(int(row[3]))
		else:
			item_vector.append(0)
	return item_vector

def get_movie_count():
	count = database_query('SELECT count(*) FROM movies')[0][0]
	return int(count)

def movie_matrix():
	movie_matrix = np.zeros((get_movie_count(), len(get_item_vector(0))))
	ratings = database_query('SELECT * FROM (SELECT id FROM users)U left join (SELECT movie, user, rating FROM ratings)R on U.id=R.user')
	for rating in ratings:
		movie_matrix[int(rating[1])-1][int(rating[0])-1] = rating[3]
	return movie_matrix

def cosine_distance_matrix():
	matrix = movie_matrix()
	similarity = np.dot(matrix, matrix.T)
	square_mag = np.diag(similarity)
	inv_square_mag = 1 / square_mag
	inv_square_mag[np.isinf(inv_square_mag)] = 0
	inv_mag = np.sqrt(inv_square_mag)
	cosine = similarity * inv_mag
	cosine = cosine.T * inv_mag
	return cosine

distance_matrix = cosine_distance_matrix()

def choose_neighbors(target_movie, user):
        all_neighbors = []
        user_rated_movies = list(sum(database_query("SELECT movie FROM ratings WHERE user={0}".format(user)), ()))
        user_rated_ratings = list(sum(database_query("SELECT rating FROM ratings WHERE user={0}".format(user)), ()))
        for i in range(len(user_rated_movies)):
                all_neighbors.append([distance_matrix[user_rated_movies[i]-1][target_movie-1], user_rated_ratings[i]])
        return all_neighbors


def predict_rating(target_movie, user):
        rating_list = choose_neighbors(target_movie, user)
        rating_list.sort(key=lambda x: x[0], reverse=True)
        similarity_sum = 0.0
        rating_sum = 0.0
        for rating in rating_list[:20]:
                similarity_sum = similarity_sum + rating[0]
                rating_sum = rating_sum + (rating[0] * rating[1])
        return rating_sum / similarity_sum
