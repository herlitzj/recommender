import csv
import time

data = []

with open('data.csv', 'r') as ratings:
	reader = csv.reader(ratings, delimiter='	')
	for row in reader:
		data.append(int(row[0]))

def merge_sort(A):
	if len(A) < 2:
		return A
	else:
		middle = int(len(A) / 2)
		return merge(merge_sort(A[:middle]), merge_sort(A[middle:]))

def merge(left, right):
	B = []
	for i in range(len(left) + len(right)):
#		print("Left: ", left)
#		print("Right: ", right)
		if len(left) == 0 or len(right) == 0:
			B.append(max(left, right)[0])
			max(left,right).pop(0)
		elif left[0] < right[0]:
			B.append(left[0])
			left.pop(0)
		else:
			B.append(right[0])
			right.pop(0)
#		print("B: ", B)
	return B
start = time.clock()
sortedData = merge_sort(data)
end = time.clock() - start
start2 = time.clock()
sorted(data)
end2 = time.clock() - start2

print(sortedData[3000:3030])
print(len(sortedData))
print(end)
print(end2)
