import itemItemDataHandler as IIDH

def predict_rating(user_id, movie_id):
	prediction = 0.0
	return prediction

def choose_neighbors(target):
        neighborhood = []
        for i in range(len(IIDH.distance_matrix)):
                if i != target:
                        neighborhood.append([IIDH.distance_matrix[i][target], [i]])
        return neighborhood


class User(object):

	def __init__(self):
		user_input = raw_input("Are you a returning user?")
		if user_input == "yes" or user_input == "y":
			self.ID = int(raw_input("Please enter your user ID"))
			self.age = int(IIDH.database_query("SELECT age FROM users where id = {0}".format(self.ID))[0][0])
		self.name = "no name"

	def return_id(self):
		return self.ID

	def return_age(self):
		return self.age

	def return_name(self):
		return self.name

	def predict_rating(self, movie_id):
		prediction = 0.0
		return prediction
