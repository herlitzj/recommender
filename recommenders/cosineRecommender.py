import csv
import statistics
import math

movieData = []
ratingData = []
userList = []
genreDictionary = {}
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

for movie in movieData:
	genreDictionary[int(movie[0])] = movie[5:-1]


for user in userList:
	userRatings = []
	userRatings.append(user[0])
	for movie in movieData:
		for rating in ratingData:
			thisRating = ''
			if int(movie[0]) == int(rating[0]) and int(user[0]) == int(rating[1]):
				thisRating = rating[2]
				break
		userRatings.append(thisRating)
	vectorList.append(userRatings)
	print(vectorList)

print(vectorList[0])
