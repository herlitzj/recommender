import csv

movieData = []
ratingDictionary = {}
userList = []
ratingData = []


with open('../movieData.csv', 'r') as movies:
	filereader = csv.reader(movies, delimiter='|')
	for row in filereader:
		movieData.append(row)

with open('../u.user', 'r') as users:
	filereader = csv.reader(users, delimiter='|')
	for row in filereader:
		userList.append(row)

with open('../u.data', 'r') as ratings:
	filereader = csv.reader(ratings, delimiter='	')
	for row in filereader:
		ratingData.append(row)

for i in range(1, len(movieData) +1):
	ratingDictionary[i] = []
	for user in userList:
		ratingDictionary[i].append(0)

for rating in ratingData:
	ratingDictionary[int(rating[1])][int(rating[0])-1] = int(rating[2])

def returnMovieData():
	return movieData

def returnRatingDictionary():
	return ratingDictionary

def returnUserList():
	return userList

def returnRatingData():
	return ratingData

def averageRating(itemVector):
	counter = 0
	total = 0.0
	for rating in itemVector:
		if rating != '':
			total = total + rating
			counter = counter + 1
	return total/counter





