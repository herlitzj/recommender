import MySQLdb as mdb
import itemItemDataHandler as IIDH
import os
import random
import time


def new_user():
	user_id = int(IIDH.database_query("SELECT max(id) FROM users")[0][0]) + 1
	print("Your user ID is {0}. Please write it down.".format(user_id))
	print("Please answer the following demographic questions. ")
	user_age = raw_input("What is your age? ")
	user_sex = raw_input("What is your gender M/F? ")
	user_prof = raw_input("What is your profession? ")
	user_zip = raw_input("What is your zipcode? ")
	IIDH.database_write("INSERT INTO users (id, age, sex, profession, zipcode) VALUES ({0}, {1}, '{2}', '{3}', {4})".format(user_id, int(user_age), user_sex, user_prof, int(user_zip)))
	answer = raw_input("Before making recommendations, we'll need you to rate some movies. \nPlease rate at least 20 of the following movies to increase accuracy.")
	rate_random_movies(user_id)


def returning_user():
        user_id = int(raw_input("What is your user ID? "))
        user_exists = int(IIDH.database_query("SELECT count(id) FROM users where id={0}".format(int(user_id)))[0][0])
        if user_exists != 0:
                main_menu(user_id)
        else:
                print("That ID was not found. Please try again.")
                returning_user()


def main_menu(user_id):
	print("MAIN MENU")
	print("Please choose a selection from the list")
	user_choice = int(raw_input("1) List existing rated movies.\n2) Rate a specific movie. \n3) Edit an existing rating. \n4) Rate movies at random. \n5) Get prediction for movie. \n6) Get top 10 movie recommendation. \n7) Search database. \n8) Exit"))
	
	if user_choice == 1:
		list_rated_movies(user_id)
	elif user_choice == 2:
		rate_specific_movie(user_id)
	elif user_choice == 3:
		edit_existing_movie(user_id)
	elif user_choice == 4:
		rate_random_movies(user_id)
	elif user_choice == 5:
		get_prediction(user_id)
	elif user_choice == 6:
		get_top_ten(user_id)
	elif user_choice == 7:
		search_database(user_id)
	elif user_choice == 8:
		return 0
	else:
		print("I did not understand your choice. Please try again.")
		main_menu(user_id)


def list_rated_movies(user_id):
	print
	existing_ratings = IIDH.database_query("SELECT movie, rating FROM ratings WHERE user = {0}".format(user_id))
	print("Your existing ratings are: ")
	for rating in existing_ratings:
		title = IIDH.database_query("SELECT title FROM movies where id = {0}".format(rating[0]))[0][0]
		print int(rating[0]), title, rating[1], "/5"
	user_choice = raw_input("Would you like to edit an existing rating? ")
	if user_choice == "yes":
		edit_existing_movie(user_id)
	else:
		main_menu(user_id)


def rate_specific_movie(user_id):
	print
	movie_id_to_rate = int(raw_input("Please enter the movie ID# for the movie you wish to rate. "))
	already_rated = int(IIDH.database_query("SELECT count(rating) FROM ratings WHERE user = {0} AND movie = {1}".format(user_id, movie_id_to_rate))[0][0])

	if already_rated > 0:
		user_answer = raw_input("You have already rated this movie. Do you wish to edit your rating?")
		if user_answer == "yes":
			edit_existing_movie(user_id)
		else:
			main_menu(user_id)

	movie_title_to_rate = IIDH.database_query("SELECT title FROM movies WHERE id = {0}".format(int(movie_id_to_rate)))[0][0]

	print("The movie you chose is {0}".format(movie_title_to_rate))
	user_answer = raw_input("Is this the movie you want to rate?")
	if user_answer == "no":
		rate_specific_movie(user_id)
	elif user_answer == "yes":
		user_rating = raw_input("Please rate {0} on a scale from 1 to 5.".format(movie_title_to_rate))
		IIDH.database_write("INSERT INTO ratings (user, movie, rating, timestamp) VALUES ({0}, {1}, {2}, {3})".format(user_id, movie_id_to_rate, int(user_rating), int(time.time())))
	print "Thank you for your rating."
	user_answer = raw_input("Would you like to rate another movie?")
	if user_answer == "yes":
		rate_specific_movie(user_id)
	else:
		main_menu(user_id)


def edit_existing_movie(user_id):
	print
	movie_id_to_edit = int(raw_input("What is the ID# of the movie you wish to edit?"))
	movie_title_to_edit = IIDH.database_query("SELECT title FROM movies WHERE id = {0}".format(movie_id_to_edit))[0][0]
	current_rating = int(IIDH.database_query("SELECT rating FROM ratings WHERE user = {0} AND movie = {1}".format(user_id, movie_id_to_edit))[0][0])
	print("Your current rating for {0} is {1}/5".format(movie_title_to_edit, current_rating))
	answer = raw_input("Do you want to change this?")
	if answer == "yes":
		new_rating = raw_input("What would you like to rate {0} from 1 to 5.".format(movie_title_to_edit))
		IIDH.database_write("UPDATE ratings SET rating = {0} where user = {1} AND movie = {2}".format(new_rating, user_id, movie_id_to_edit))
		main_menu(user_id)
	else:
		main_menu(user_id)


def rate_random_movies(user_id):
	print("Please rate the following movies. \nType 'done' to end this rating session. ")
	movie_count = IIDH.get_movie_count()
	already_rated = set(sum(IIDH.database_query("SELECT movie FROM ratings WHERE user = {0}".format(user_id)), ()))
	all_movies = set(sum(IIDH.database_query("SELECT id FROM movies"), ()))
	random_movie_list = all_movies - already_rated
	shuffled_movie_list = list(random_movie_list)
	random.shuffle(shuffled_movie_list)
	print(random_movie_list)
	print(shuffled_movie_list)
	for movie_id in shuffled_movie_list:
		movie_title = IIDH.database_query("SELECT title FROM movies WHERE id={0}".format(movie_id))[0][0]
		user_answer = raw_input("Have you seen {0} {1}? ".format(movie_id, movie_title))
		if user_answer == "no":
			pass
		elif user_answer == "done":
			main_menu(user_id)
		else:
			user_rating = raw_input("Please rate {0} from 1 to 5. ".format(movie_title))
			IIDH.database_write("INSERT INTO ratings (user, movie, rating, timestamp) VALUES ({0}, {1}, {2}, {3})".format(user_id, movie_id, int(user_rating), int(time.time())))
	main_menu(user_id)


def search_database(user_id):
	print
        user_answer = raw_input("Do you want to search by keyword or ID?")
        if user_answer == "ID" or user_answer == "id":
                search_id = raw_input("Please enter the movie id. ")
                is_movie_in_database = int(IIDH.database_query("SELECT COUNT(*) FROM movies WHERE id={0}".format(search_id))[0][0])
                if is_movie_in_database != 0:
                        query_return = IIDH.database_query("SELECT * FROM movies where id={0}".format(search_id))[0]
			print query_return[0], query_return[1]
		else: print "Movie was not found. Please try again."
        elif user_answer == "keyword":
                search_keyword = raw_input("Please enter a keyword or phrase to search. ")
                is_movie_in_database = int(IIDH.database_query("SELECT count(*) FROM movies WHERE title like '%{0}%'".format(search_keyword))[0][0])
		if is_movie_in_database != 0:
			print "The following was found: "
                        query_return = IIDH.database_query("SELECT * FROM movies WHERE title like '%{0}%'".format(search_keyword))
                        for item in query_return:
                                print item[0], item[1]
                else:
			print "Movie was not found. Please try again."
			search_database(user_id)

	user_answer = raw_input("Do you want to search again? ")
	if user_answer == "yes":
		search_database(user_id)
	else: main_menu(user_id)


def get_prediction(user_id):
	movie_to_predict = raw_input("What is the ID# of the movie for which you want a prediction? ")
	prediction = IIDH.predict_rating(int(movie_to_predict), user_id)
	print(prediction)
	user_answer = raw_input("Do you want to see another prediction? ")
	if user_answer == "yes":
		get_prediction(user_id)
	else:
		main_menu(user_id)


def get_top_ten(user_id):
	print "Calculating Top Ten...\n"
	already_rated = set(sum(IIDH.database_query("SELECT movie FROM ratings WHERE user = {0}".format(user_id)), ()))
	all_movies = set(sum(IIDH.database_query("SELECT id FROM movies"), ()))
	difference = all_movies - already_rated
	difference_list = list(difference)
	ratings = []
	for item in difference_list:
		prediction = IIDH.predict_rating(item, user_id)
		ratings.append([item, prediction])
	ratings.sort(key=lambda x: x[1], reverse=True)
	print "Your Top Ten unseen movies are:"
	for i in range(10):
		movie_title = IIDH.database_query("SELECT title FROM movies WHERE id = {0}".format(ratings[i][0]))
		print "{0}. {1} - {2}".format(i+1, movie_title[0][0], ratings[i][1])
	raw_input("\nPress ENTER to return to Main Menu")
	main_menu(user_id)


os.system('clear')
print("Welcome to the Movie Recommender")
user_status = raw_input("Are you a new user? (yes or no)?")
if user_status == "yes":
        new_user()
else:
        returning_user()
	
