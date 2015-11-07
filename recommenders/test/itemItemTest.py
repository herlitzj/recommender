from app.itemItemRecommender import returnMovieData, returnRatingDictionary, returnUserList, returnRatingData, averageRating

#Setup
ratingDictionary = returnRatingDictionary()


def test_that_movieData_is_list():
	result = returnMovieData()
	assert isinstance(result, list)

def test_that_movieData_is_a_list_of_lists():
	result = returnMovieData()[0]
	assert isinstance(result, list)

def test_that_movieData_has_24_columns():
	result = len(returnMovieData()[0])
	assert result == 24

def test_that_ratingDictionary_is_a_dictionary():
	result = returnRatingDictionary()
	assert isinstance(result, dict)

def test_that_ratingDictionary_length_matches_number_of_movies():
	assert len(returnRatingDictionary()) == len(returnMovieData())

def test_that_ratingDictionary_item_length_matches_userList_length():
	assert len(returnRatingDictionary()[1]) == len(returnUserList())

def test_that_userList_is_a_list():
	assert isinstance(returnUserList(), list)

def test_that_userList_items_are_length_5():
	assert len(returnUserList()[0]) == 5

def test_that_ratingData_is_a_list():
	assert isinstance(returnRatingData(), list)

def test_that_ratingData_items_have_4_columns():
	assert len(returnRatingData()[0]) == 4

def test_that_data_in_ratingDictionary_is_correct():
	user = int(returnRatingData()[10][0])
	movie = int(returnRatingData()[10][1])
	rating = int(returnRatingData()[10][2])
	assert ratingDictionary[movie][user-1] == rating

def test_that_averageRating_returns_a_float():
	testVector = ratingDictionary[10][0:]
	assert isinstance(averageRating(testVector), float)


