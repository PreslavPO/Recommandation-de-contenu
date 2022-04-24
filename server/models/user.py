import uuid
from flask import Flask, jsonify, request
from config import db

class User:
	def signup(self):
		req = request.get_json(force=True)
		print(req)

		user = {
			"_id": uuid.uuid4().hex,
			"name": req["name"],
			"email": req["email"],
			"password": req["password"],
		}

		response = jsonify(user)
		response.status_code = 200
		return response