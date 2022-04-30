from flask import Flask, jsonify, redirect, request, session, make_response, redirect
from config import db
from bson import json_util
from src.utils import get_page_of_movies, get_nb_movies, get_nb_pages
from src.collaborative_filtering.recommendation import get_collaborative_recommendation, get_trainset
import pandas as pd
import bcrypt
import uuid
import json
import time
import datetime

class User:
	def start_session(self, user):
		del user["password"]
		session["logged_in"] = True
		session["user"] = user
		return user, 200

	def signup(self):
		req = request.get_json(force=True)

		# Create user object
		user = {
			"_id": uuid.uuid4().hex,
			"username": req["username"],
			"email": req["email"],
			"password": req["password"],
		}

		# Check values
		if (user["username"] == ""):
			return { "message": "Username cannot be empty" }, 400
		if (user["email"] == ""):
			return { "message": "Email cannot be empty" }, 400
		if (user["password"] == ""):
			return { "message": "Password cannot be empty" }, 400
			
		if (db.users.find_one({ "email": user["email"] })):
			return { "message": "Email already used" }, 400

		# Password to byte
		bytePwd = user["password"].encode("utf8")
		# Generate salt
		saltPwd = bcrypt.gensalt()
		# Hash password
		user["password"] = bcrypt.hashpw(bytePwd, saltPwd)

		# Insert into db
		if (db.users.insert_one(user)):
			return self.start_session(user)

		return { "message": "Signup failed" }, 400
	
	def logout(self):
		session.clear()
		return { "message": "Session cleared" }, 200
	
	def login(self):
		req = request.get_json(force=True)

		# Search user with email provided
		user = db.users.find_one({ "email": req["email"] }, {"_id": 1, "email": 1, "username": 1, "password": 1})

		# Generate salt
		if user and bcrypt.checkpw(req["password"].encode("utf-8"), user["password"]):
			return self.start_session(user)

		return { "message": "Invalid email or password" }, 401

	def check_session(self):
		if (session.get("logged_in")):
			return { "login": True, "user": session["user"] }, 200
		return { "login": False }, 200

	def get_rating(self, movieId):
		userId = request.args.get("userId")

		data = db.users.find_one(
			{"_id": userId, "ratings.movieId": movieId},
			{"_id": 0, "ratings.$": 1}
		)
		jsonData = json.loads(json_util.dumps(data))
		if (jsonData != None):
			res = jsonData["ratings"][0]
			return { "movieId": res["movieId"], "rating": res["rating"] }, 200
		else:
			return { "message": "Didn't find rating for this movie with this user"}, 204

	def set_rating(self, movieId):
		req = request.get_json(force=True)
		userId = request.args.get("userId")

		if (not req.get("score")):
			return { "message": "movieId or score is missing" }, 400
		if(not db.users.find_one({"_id": userId})):
			return { "message": "User not Found" }, 401
		
		if (db.users.find_one({"_id": userId, "ratings.movieId": movieId})):
			db.users.update_one(
				{ "_id": userId, "ratings.movieId": movieId },
				{ "$set": {"ratings.$.rating": req["score"], "ratings.$.timestamp": datetime.datetime.now()} }
			)
		else:
			db.users.update_one(
				{ "_id": userId },
				{ "$addToSet": {"ratings": {"movieId": movieId, "rating": req["score"], "timestamp": datetime.datetime.now()}}
			})

		return { "message": "Movie score updated" }, 200

	def get_movies(self):
		userId = request.args.get("userId")
		page = int(request.args.get("page", 1))
		# Values : rating.asc, rating.desc, last_rated
		sort_by = request.args.get("sort_by", "last_rated")

		# Get movie list
		data = db.users.find_one({ "_id": userId })
		if (data.get("ratings")):
			result_movies = pd.DataFrame(list(data["ratings"]))

			# Value to sort
			sort_value = ""
			if (sort_by.startswith("rating")):
				sort_value = "rating"
			elif (sort_by == "last_rated"):
				sort_value = "timestamp"
			
			# Sort by descending, ascending or last rated
			if (sort_by == "rating.asc"):
				result_movies = result_movies.sort_values(sort_value, ascending=True)
			else:
				result_movies = result_movies.sort_values(sort_value, ascending=False)

			# List of movie ids
			idTopList = get_page_of_movies(result_movies, page)["movieId"].astype(int).tolist()

			# Get all movies corresponding to the list of ids
			data = db.movies.find({ "id": { "$in": idTopList } })
			json_data = json.loads(json_util.dumps(data))

			# Sort to correspond original id sort (mongodb shuffle the list)
			json_data_sorted = []
			for movieId in idTopList:
				for doc in json_data:
					if movieId == doc["id"]:
						json_data_sorted.append(doc)
						break;

			if (data != None):
				return {
					"page": page,
					"result": json_data_sorted,
					"total_results": get_nb_movies(result_movies),
					"total_pages": get_nb_pages(result_movies)
				}, 200

		return {
			"page": 0,
			"result": [],
			"total_results": 0,
			"total_pages": 0
		}, 204
		
	def getRecommendation(self):
		userId = request.args.get("userId")
		page = int(request.args.get("page", 1))

		# Find user document
		user = db.users.find_one({ "_id": userId })

		# Get the trainset
		trainset = get_trainset(userId, list(user["ratings"]))

		# Get collaborative
		result_movies = get_collaborative_recommendation(trainset, userId)
		result_movies = pd.DataFrame(result_movies)
		print("-------------- Resultat --------------")
		print(result_movies)
		print("--------------------------------------")

		# List of movie ids
		idTopList = get_page_of_movies(result_movies[0], page).astype(int).tolist()

		# Get all movies corresponding to the list of ids
		data = db.movies.find({ "id": { "$in": idTopList } })
		json_data = json.loads(json_util.dumps(data))

		# Sort to correspond original id sort (mongodb shuffle the list)
		json_data_sorted = []
		for movieId in idTopList:
			for doc in json_data:
				if movieId == doc["id"]:
					json_data_sorted.append(doc)
					break;

		if (data != None):
			return {
				"page": page,
				"result": json_data_sorted,
				"total_results": get_nb_movies(result_movies),
				"total_pages": get_nb_pages(result_movies)
			}, 200

		return { "message": "Movie list not found" }, 404