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

class SignOut(Resource):
	def post(self):
		return User().signout()

class UserInfo(Resource):
	method_decorators = [login_required]

	def get(self):
		return User().get_user()