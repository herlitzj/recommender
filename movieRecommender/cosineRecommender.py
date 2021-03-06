import csv
import functools
import statistics
import math
import time
import os

movieData = []
ratingData = []
userList = []
ratingDictionary = {}
vectorList = []


with open('movieData.csv', 'r') as movies:
	filereader = csv.reader(movies, delimiter='|')
	for row in filereader:
		 movieData.append(row)

with open('u.data', 'r') as ratings:
	ratingsreader = csv.reader(ratings, delimiter='	')
	for row in ratingsreader:
		ratingData.append(row)

with open('u.user', 'r') as users:
	userReader = csv.reader(users, delimiter='|')
	for row in userReader:
		userList.append(row)

#create an empty dictionary do dump ratings into. Key is user, value is list of ratings
for i in range(1, len(userList) + 1):
	ratingDictionary[i] = []
	for movie in movieData:
		ratingDictionary[i].append('')

#iterate through rating data and insert rating into list in correct position
for rating in ratingData:
	ratingDictionary[int(rating[0])][int(rating[1])-1] = int(rating[2])


@functools.lru_cache(maxsize=128)
def averageRating(vectorToAverage):
	counter = 0
	total = 0
	for rating in vectorToAverage:
		if rating != '':
			total = total + rating
			counter = counter + 1
	return total/counter

def normalizeVector(vectorToNormalize):
	normVector = vectorToNormalize
	normTuple = tuple(normVector)
	average = averageRating(normTuple)
	for i in range(0, len(normVector)):
		if normVector[i] == '':
			normVector[i] = 0
		else:
			normVector[i] = normVector[i] - average
	return normVector

def vectorEuclideanDistance(vectorForDistance):
	euclideanDistance = 0
	for rating in vectorForDistance:
		euclideanDistance = euclideanDistance + float(rating)*float(rating)
	return math.sqrt(euclideanDistance)

def cosineSimilarity(user1, user2):
	user1Vec = ratingDictionary[user1][0:]
	user2Vec = ratingDictionary[user2][0:]
	user1NormedVector = normalizeVector(user1Vec)
	user2NormedVector = normalizeVector(user2Vec)
	user1EuclideanDist = vectorEuclideanDistance(user1NormedVector)
	user2EuclideanDist = vectorEuclideanDistance(user2NormedVector)
	cosineSim = 0
	for i in range(0, len(user1NormedVector)):
		cosineSim = cosineSim + user1NormedVector[i] * user2NormedVector[i]
	return cosineSim / (user1EuclideanDist * user2EuclideanDist)

def findNeighbors(inputUser):
	targetUser = inputUser
	neighbors = []
	for user in userList:
		if int(user[0]) != targetUser:
			neighbors.append([int(user[0]), cosineSimilarity(targetUser, int(user[0])), averageRating(tuple(ratingDictionary[int(user[0])][0:]))])
	return sorted(neighbors, key=lambda x: x[1], reverse=True)[0:50]


def prediction(user, movie):
	ratingTuple = ratingDictionary[int(user)][0:]
	ratingTuple = tuple(ratingTuple)
	userAverageRating = averageRating(ratingTuple)
	neighborhood = findNeighbors(user)
	sumOfRatings = 0.0
	sumOfWeights = 0.0
	for neighbor in neighborhood:
		neighborRatings = ratingDictionary[neighbor[0]][0:]
		if neighborRatings[movie - 1] != '':
			sumOfRatings = sumOfRatings + (neighborRatings[movie - 1] - neighbor[2]) * neighbor[1]
			sumOfWeights = sumOfWeights + neighbor[1]
	if sumOfWeights == 0:
		return "No neighbors rated this movie."
	else:
		return sumOfRatings / sumOfWeights + userAverageRating


def newUserVector():
	newUserVector = []
	print("Please rate the following movies. If you have not seen the movie, just press enter to give it no rating. To end the rating input, enter -1")
	for movie in movieData:
		print("How would you rate: ")
		newRating = input(movie[1])
		if newRating == '-1':
			break
		else:
			if newRating == '':
				newUserVector.append(newRating)
			else:
				newUserVector.append(int(newRating))
	if len(newUserVector) < len(movieData):
		for i in range(0, len(movieData) - len(newUserVector)):
			newUserVector.append('')
	ratingDictionary[944] = newUserVector


def topFive(user):
	topMovies = []
	movies = movieData[170:175]
	for movie in movies:
		topMovies.append([movie[0], movie[1], prediction(user, int(movie[0]))])
	return sorted(topMovies, key=lambda x: x[2], reverse=True)[0:5]

os.system('clear')
newUserVector()
print("Determining recommendations...")
topFiveMovies = topFive(944)
print()
print("Top Five Recommended Movies:")
for movie in topFiveMovies:
	print("Title: ", movie[1])
	print("Predicted Rating: ", math.ceil(movie[2]*100) / 100)





