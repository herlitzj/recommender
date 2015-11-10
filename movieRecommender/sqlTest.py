import MySQLdb as mdb
import scipy as sp
import numpy as np
import scipy.spatial.distance as ssd

connection = mdb.connect('localhost', 'root', 'root', 'movieRatings');
	
def getItemVector(itemNumber):
	itemVector = []
	cursor = connection.cursor()
	cursor.execute('SELECT * from (select id from users)U left join (select movie, user, rating from ratings where movie={0})R on U.id=R.user'.format(itemNumber))
	rows = cursor.fetchall()
	for row in rows:
		if row[3] != None:
			itemVector.append(int(row[3]))
		else:
			itemVector.append(0)
	return itemVector



def getMovieCount():
	cursor = connection.cursor()
	cursor.execute('SELECT count(id) FROM movies')
	count = cursor.fetchone()
	return count[0]

def movieMatrix():
	movieMatrix = np.zeros((getMovieCount(), len(getItemVector(0))))
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM (SELECT id FROM users)U left join (SELECT movie, user, rating FROM ratings)R ON U.id=R.user')
	ratings = cursor.fetchall()
	for rating in ratings:
		movieMatrix[int(rating[1])-1][int(rating[0])-1] = rating[3]
	return movieMatrix


def cosineDistanceMatrix():

	"""Returns a matrix of the cosine distance between all Item-Item vectors. To get cosine similarity, subtract returned values from 1"""

	matrix = movieMatrix()
	similarity = np.dot(matrix, matrix.T)
	squareMag = np.diag(similarity)
	invSquareMag = 1/squareMag
	invSquareMag[np.isinf(invSquareMag)]=0
	invMag = np.sqrt(invSquareMag)
	cosine = similarity * invMag
	cosine = cosine.T * invMag
	return cosine

distanceMatrix = cosineDistanceMatrix()
