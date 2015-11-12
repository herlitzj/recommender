import MySQLdb as mdb
import scipy as sp
import numpy as np
import scipy.spatial.distance as ssd

connection = mdb.connect('localhost', 'root', 'root', 'movieRatings');


def databaseQuery(query):
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

def searchDatabase():
	user_answer = raw_input("Do you want to search by title or ID?")
	if user_answer == "ID" or user_answer == "id":
		search_id = raw_input("Please enter the movie id. ")
		is_movie_in_database = int(databaseQuery("SELECT COUNT(*) FROM movies WHERE id={0}".format(search_id))[0][0])
		if is_movie_in_database != 0:
			return databaseQuery("SELECT * FROM movies where id={0}".format(search_id))
		else: print("Movie was not found. Please try again.")
	elif user_answer == "title":
		search_title = raw_input("Please enter the title to search. ")
		is_movie_in_database = int(databaseQuery("SELECT count(*) FROM movies WHERE title like '%{0}%'".format(search_title))[0][0])
		if is_movie_in_database != 0:
			queryReturn = databaseQuery("SELECT * FROM movies WHERE title like '%{0}%'".format(search_title))
			for item in queryReturn:
				print item[0], item[1]
		else: print("Movie was not found. Please try again.")
	else: searchDatabase()

def getItemVector(itemNumber):
	itemVector = []
	rows = databaseQuery('SELECT * from (select id from users)U left join (select movie, user, rating from ratings where movie={0})R on U.id=R.user'.format(itemNumber))
	for row in rows:
		if row[3] != None:
			itemVector.append(int(row[3]))
		else:
			itemVector.append(0)
	return itemVector

def getMovieCount():
	count = databaseQuery('SELECT count(id) FROM movies')
	return count[0][0]


def movieMatrix():
	movieMatrix = np.zeros((getMovieCount(), len(getItemVector(0))))
	ratings = databaseQuery('SELECT * FROM (SELECT id FROM users)U left join (SELECT movie, user, rating FROM ratings)R ON U.id=R.user')
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

print("Building cosine distance matrix for all movie items...")
distanceMatrix = cosineDistanceMatrix()

def chooseNeighbors(target):
	neighborhood = []
	for i in range(len(getItemVector(0))):
		if i != target:
			neighborhood.append([distanceMatrix[i][target], [i]])
	return neighborhood #sorted(neighborhood, key=lambda x: x[0], reverse=True)[0:20]


class User(object):

	def __init__(self):
		userInput = raw_input("Are you a returning user?")
		if userInput == "yes" or userInput == "y":
			self.ID = int(raw_input("Please enter your user ID"))
			self.age = int(databaseQuery("SELECT age FROM users where id={0}".format(self.ID))[0][0])
			self.name = "No name"
			self.vector = movieMatrix().T[self.ID - 1]
		else:
			print("Welcome new user.")
			self.name = raw_input("Please enter your name.")
			self.age = raw_input("Please enter your age.")
			self.ID = int(databaseQuery("SELECT count(*) FROM users")[0][0]) + 1

	def returnName(self):
		return self.name

	def returnAge(self):
		return self.age

	def returnID(self):
		return self.ID

	def returnVector(self):
		return self.vector

	def addRating(self, movieID, rating):
		return rating

	def predictRating(self, movieID):
		"""Method for generating a rating for a given movie ID based on
		calculating relation between existing ratings and the ratings
		of similar movies in the database."""
		
		return movieID

	def topTen(self):
		self.topTen = []
		return self.topTen


class Movie(object):
	"""
	Movie class object
	cosineDistance() returns the cosine distance between two movies
	"""		

	def __init__(self, ID):
		self.name = databaseQuery('SELECT title FROM movies WHERE id={0}'.format(ID))[0][0]
		self.ID = ID
		self.vector = getItemVector(ID)


	def returnName(self):
		return self.name

	def returnVector(self):
		return self.vector

	def cosineDistance(self, comparisonID):
		return ssd.cosine(self.vector, getItemVector(comparisonID))

	def cosineDistance2(self, comparisonID):
		return distanceMatrix[self.ID - 1][comparisonID - 1]
