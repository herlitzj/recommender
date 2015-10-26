import csv
import statistics
import math

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

#sort rating data so it can iterate easily
#ratingData.sort(key=lambda x: (int(x[0]), int(x[1])))

#create an empty dictionary do dump ratings into. Key is user, value is list of ratings
for i in range(1, len(userList) + 1):
	ratingDictionary[i] = []
	for j in range(0, 1682):
		ratingDictionary[i].append('')

#iterate through rating data and insert rating into list in correct position
for rating in ratingData:
	ratingDictionary[int(rating[0])][int(rating[1])-1] = int(rating[2])

print(ratingDictionary)

