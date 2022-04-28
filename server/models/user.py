from flask import Flask, jsonify, redirect, request, session, make_response, redirect
from config import db
from bson import json_util
import bcrypt
import uuid
import json

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
	
	def signout(self):
		session.clear()
		return { "message": "Session cleared" }, 200
	
	def login(self):
		req = request.get_json(force=True)

		# Search user with email provided
		user = db.users.find_one({ "email": req["email"] })

		# Generate salt
		if user and bcrypt.checkpw(req["password"].encode("utf-8"), user["password"]):
			return self.start_session(user)

		return { "message": "Invalid email or password" }, 401

	def check_session(self):
		if (session.get("logged_in")):
			return { "login": True, "user": session["user"] }, 200
		return { "login": False }, 200

	def get_rating(self, userId, movieId):
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

	def set_rating(self, userId):
		req = request.get_json(force=True)
		print(req)
		if (not (req.get("movieId") and req.get("score"))):
			return { "message": "movieId or score is missing"}, 400
		if(not db.users.find_one({"_id": userId})):
			return { "message": "User not Found"}, 401
		
		if (db.users.find_one({"_id": userId, "ratings.movieId": req["movieId"]})):
			db.users.update_one(
				{ "_id": userId, "ratings.movieId": req["movieId"] },
				{ "$set": {"ratings.$.rating": req["score"]} }
			)
		else:
			db.users.update_one(
				{ "_id": userId },
				{ "$addToSet": {"ratings": {"movieId": req["movieId"], "rating": req["score"]}}
			})

		return { "message": "Movie score updated" }, 200