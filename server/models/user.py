from flask import Flask, jsonify, redirect, request, session, make_response, redirect
from config import db
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

	def get_rating(self):
		return {"work": True}, 200 # TODO : Renvoyer la note par rapport à un id

	def set_rating(self):
		return { "todo": True }, 200