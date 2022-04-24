from flask import Flask
from flask_restful import Resource
from models.user import User

class SignUp(Resource):
	def post(self):
		return User().signup()