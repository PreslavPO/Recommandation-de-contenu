from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import json_util
import json
import os

app = Flask(__name__)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Environment variables
load_dotenv()
dbUsername = os.environ.get("DB_USERNAME")
dbPassword = os.environ.get("DB_PASSWORD")
dbName = os.environ.get("DB_NAME")

# Database
load_dotenv()

cluster = MongoClient(
    "mongodb+srv://%s:%s@cluster0.xyttr.mongodb.net/%s" % (dbUsername, dbPassword, dbName),
	tls=True,
    tlsAllowInvalidCertificates=True
)
db = cluster[dbName]

# Routes
@app.route("/api/movie/<int:movieId>", methods=["GET"])
def movie(movieId):
	data = db.movies.find_one({ "id": movieId })
	if (data != None):
		return json.loads(json_util.dumps(data)), 200
	return { "msg": "Movie id not found" }, 404

@app.route("/api/movie/<int:movieId>/credits", methods=["GET"])
def movieCredits(movieId):
	data = db.credits.find_one({ "id": movieId })
	if (data != None):
		return json.loads(json_util.dumps(data)), 200
	return { "msg": "Movie id not found" }, 404

if __name__ == "__main__":
	app.run(debug=True)