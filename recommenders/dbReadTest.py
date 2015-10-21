import csv
import statistics

with open('movieData.csv', 'r') as movies:
	filereader = csv.reader(movies, delimiter='|')
	movieData = []
	for row in filereader:
		 movieData.append(row)

headers = ["id", "title", "release date", "videos release date", "IMDB URL", "unknown", "action", "adventure", "animation", "childrens", "comedy", "crime", "documentary", "drama", "fantasy", "film-noir", "horror", "musical", "mystery", "romance", "scifi", "thriller", "war", "western"]


with open('u.data', encoding="ascii") as ratings:
	ratingsreader = csv.reader(ratings, delimiter='	')
	ratings = []
	for row in ratingsreader:
		ratings.append(row)

def averageRating(user):
	averageRating = 0.0
	cummulativeRatings = 0.0
	counter = 0.0
	for rating in ratings:
		if int(rating[0]) == user:
			counter = counter + 1
			cummulativeRatings = cummulativeRatings + float(rating[2])
	return cummulativeRatings / counter


def buildRatingDictionary(user1, user2):
	ratingDictionary = {}
	for rating in ratings:
		if int(rating[0]) == user1:
			ratingDictionary[int(rating[1])] = [int(rating[2]), -1]

	for rating in ratings:
		if int(rating[1]) in ratingDictionary:
			ratingDictionary[int(rating[1])][1] = int(rating[2])

	for rating in ratingDictionary:
		if ratingDictionary[rating][1] == -1:
			del ratingDictionary[rating]

	return ratingDictionary

def userStDev(user1, user2):
	ratingDictionary = buildRatingDictionary(int(user1), int(user2))
	userOneRatings = []
	userTwoRatings = []
	for dictionary in ratingDictionary:
		userOneRatings.append(ratingDictionary[dictionary][0])
		userTwoRatings.append(ratingDictionary[dictionary][1])
	return [statistics.stdev(userOneRatings), statistics.stdev(userTwoRatings)]
		


def ratingWeight(user1, user2):
	userOneAverage = averageRating(int(user1))
	userTwoAverage = averageRating(int(user2))
	ratingDictionary = buildRatingDictionary(int(user1), int(user2))
	ratingsSum = 0.0
	userSD = userStDev(int(user1), int(user2)) 
	for dictionary in ratingDictionary:
		ratingsSum = ratingsSum + (ratingDictionary[dictionary][0] - userOneAverage)*(ratingDictionary[dictionary][1] - userTwoAverage)

	return ratingsSum / (userSD[0]*userSD[1])

def findNeighbors():
	neighbors = [10, 245, 543, 125, 312, 378, 412]
	return neighbors

def ratingPrediction(user, item):
	neighbors = findNeighbors()
	userAverage = averageRating(int(user))
	numerator = 0.0
	denominator = 0.0
	for neighbor in neighbors:
		ratingDictionary = buildRatingDictionary(int(user), int(neighbor))
		neighborAverage = averageRating(int(neighbor))
		weight = ratingWeight(int(user), int(neighbor))
		numerator = numerator + (ratingDictionary[int(item)][1] - neighborAverage) * weight
		denominator = denominator + weight

	return userAverage + numerator / denominator


print(movieData[450])

"""
print(buildRatingDictionary(300, 125))
print("100: ")
print(ratingPrediction(300, 100))
print("687: ")
print(ratingPrediction(300, 687))
print("948: ")
print(ratingPrediction(300, 948))
"""
