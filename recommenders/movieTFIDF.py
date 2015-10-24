import csv
import statistics
import math

movieData = []
ratingData = []
userList = []
genreDictionary = {}
documentFrequency = []

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

for i in range(5,23):
	documentSum = 0
	for movie in movieData:
		documentSum = documentSum + int(movie[i])
	documentFrequency.append(1 / documentSum)


def createUserVector(user):
	ratedMovies = []
	userVector = []
	counter = 0.0
	for rating in ratingData:
		if int(rating[0]) == int(user):
			ratedMovies.append([int(rating[1]), int(rating[2])])
			counter = counter + 1
	for i in range(0, 18):
		vectorItem = 0
		for ratedMovie in ratedMovies:
			vectorItem = vectorItem + math.sqrt(int(ratedMovie[1])) *int(genreDictionary[ratedMovie[0]][i])
		userVector.append(vectorItem)
	return userVector

def ratingPrediction(user, item):
	termFrequency = []
	prediction = 0
	userVector = createUserVector(user)
	for i in genreDictionary[item]:
		termFrequency.append(int(i) / math.sqrt(len(genreDictionary[item])))
	for i in range(0, len(termFrequency)):
		prediction = prediction + termFrequency[i] * userVector[i] * documentFrequency[i]
	return prediction

print("User #236: ", "427 - ", ratingPrediction(236,427), "179 - ", ratingPrediction(236, 179), "520 - ", ratingPrediction(236, 520), "265 - ", ratingPrediction(236, 265))



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
