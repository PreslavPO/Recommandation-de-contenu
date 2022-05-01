from flask import Flask, session
from flask_restful import Resource, abort
from functools import wraps
from models.user import User

def login_required(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if "logged_in" in session:
			return func(*args, **kwargs)
		else:
			abort(401)
	return wrapper

class SignUp(Resource):
	def post(self):
		return User().signup()

class Logout(Resource):
	def post(self):
		return User().logout()

class Login(Resource):
	def post(self):
		return User().login()

class CheckSession(Resource):
	def get(self):
		return User().check_session();

class UserRating(Resource):
	method_decorators = [login_required]

	def get(self, movieId):
		return User().get_rating(movieId)

	def post(self, movieId):
		return User().set_rating(movieId)
	
	def delete(self, movieId):
		return User().delete_rating(movieId)

class UserRatingMovies(Resource):
	method_decorators = [login_required]

	def get(self):
		return User().get_movies()

class UserRecommendation(Resource):
	method_decorators = [login_required]

	def get(self):
		return User().getRecommendation()

class UserInformation(Resource):
	method_decorators = [login_required]

	def get(self):
		return User().getInformation()