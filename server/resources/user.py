from flask import Flask
from flask_restful import Resource

class User(Resource):
	def get(self):
		return { "message": "WORK !" }, 200