import csv
import statistics

movieData = []
ratingData = []
userList = []
genreDictionary = {}

with open('movieData.csv', 'r') as movies:
	filereader = csv.reader(movies, delimiter='|')
	for row in filereader:
		 movieData.append(row)

headers = ["id", "title", "release date", "videos release date", "IMDB URL", "unknown", "action", "adventure", "animation", "childrens", "comedy", "crime", "documentary", "drama", "fantasy", "film-noir", "horror", "musical", "mystery", "romance", "scifi", "thriller", "war", "western"]


with open('u.data', encoding="ascii") as ratings:
	ratingsreader = csv.reader(ratings, delimiter='	')
	for row in ratingsreader:
		ratingData.append(row)

with open('u.user', 'r') as users:
	userReader = csv.reader(users, delimiter='|')
	for row in userReader:
		userList.append(row)

for movie in movieData:
	genreDictionary[int(movie[0])] = movie[5:-1]

def averageRating(user):
	averageRating = 0.0
	cummulativeRatings = 0.0
	counter = 0.0
	for rating in ratingData:
		if int(rating[0]) == user:
			counter = counter + 1
			cummulativeRatings = cummulativeRatings + float(rating[2])
	return cummulativeRatings / counter

def buildRatingDictionary(user1, user2):
	ratingDictionary = {}
	for rating in ratingData:
		if int(rating[0]) == user1:
			ratingDictionary[int(rating[1])] = [int(rating[2]), -1]
	for rating in ratingData:
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

def findNeighbors(user):
	print("Searching for neighbors...")
	neighbors = []
	targetVector = createUserVector(user)
	for i in userList:
		similarity = 0
		compareVector = createUserVector(i[0])
		for t in range(0, len(targetVector)):
			similarity = similarity + abs(targetVector[t] - compareVector[t])
		neighbors.append([i[0], similarity])
	return sorted(neighbors, key=lambda x: int(x[1]), reverse=1)[0:50]

def createUserVector(user):
	ratedMovies = []
	userVector = []
	for rating in ratingData:
		if int(rating[0]) == int(user):
			ratedMovies.append([int(rating[1]), int(rating[2])])
	for i in range(0, 18):
		vectorItem = 0
		for ratedMovie in ratedMovies:
			vectorItem = vectorItem + int(ratedMovie[1]) *int(genreDictionary[ratedMovie[0]][i])
		userVector.append(vectorItem)
	return userVector

def ratingPrediction(user, item):
	neighbors = findNeighbors(user)
	userAverage = averageRating(int(user))
	numerator = 0.0
	denominator = 0.0
	for neighbor in neighbors:
		ratingDictionary = buildRatingDictionary(int(user), int(neighbor[0]))
		neighborAverage = averageRating(int(neighbor[0]))
		weight = ratingWeight(int(user), int(neighbor[0]))
		numerator = numerator + (ratingDictionary[int(item)][1] - neighborAverage) * weight
		denominator = denominator + weight

	return userAverage + numerator / denominator
print(userList[0])


"""
print(buildRatingDictionary(312, 225))
print(ratingPrediction(312, 512))
print(ratingPrediction(312, 265))
print(buildRatingDictionary(300, 125))
print("100: ")
print(ratingPrediction(300, 100))
print("687: ")
print(ratingPrediction(300, 687))
print("948: ")
print(ratingPrediction(300, 948))
"""
