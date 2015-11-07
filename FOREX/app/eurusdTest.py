import csv

priceData = []

with open('EURUSD_1M_2014.csv', 'r') as rawPrices:
	filereader = csv.reader(rawPrices, delimiter=";")
	for row in filereader:
		priceData.append(row)

def movingAverage():
	for x in range(11, len(priceData) - 11):
		movingAverage = 0.0
		counter = 0
		for y in range(-10, 10):
			movingAverage = movingAverage + float(priceData[x+y][1])
			counter = counter + 1
		movingAverage = movingAverage / counter
		priceData[x].append(movingAverage) 

#movingAverage()

def 

def priceTest(startRow):
	currentPrice = float(priceData[startRow][1])
	wins = 0
	losses = 0
	trades = 0
	upOrDown = "up"


	for row in priceData:
		high = float(row[2])
		low = float(row[3])
		if upOrDown == "up":
			if high > (currentPrice + 0.03):
				wins = wins + 1
				trades = trades + 1
				currentPrice = high
			elif low < (currentPrice - 0.01):
				losses = losses + 1
				trades = trades + 1
				currentPrice = low
				upOrDown = "down"

		if upOrDown == "down":
			if high > (currentPrice + 0.01):
				losses = losses + 1
				trades = trades + 1
				currentPrice = high
				upOrDown = "up"
			if low < (currentPrice - 0.03):
				wins = wins + 1
				trades = trades + 1
				currentPrice = low
			
	
	print("Wins: ", wins)
	print("Losses: ", losses)
	print("Trades: ", trades)
	print("Ratio W/L: ", int(wins / losses * 100), "%")


def pinBar():
	buyPrice = []

	for i in range(10, len(priceData) - 10):
		if float(priceData[i][1]) > float(priceData[i-1][1]) and float(priceData[i][4]) < float(priceData[i-1][4]):
			for j in range(-10, -1):
				if float(priceData[i][2]) > (1.2 * float(priceData[i+j][2])):
					buyPrice.append([float(priceData[i][4]), priceData[i][0]])
	print(buyPrice)

priceTest(0)
print(priceData[100])
pinBar()
