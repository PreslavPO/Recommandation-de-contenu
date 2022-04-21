from flask import Flask, request, render_template, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import json_util
from src.weighted_rating.top_rating import get_top_rating
import json
import os

app = Flask(__name__)

# Enable CORS
CORS(app)

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


@app.route("/api/movie/top_rating", methods=["GET"])
def topRating():
	page = int(request.args.get("page", 1))

	# Result of top rating : list movies ids / number of movies / number of pages
	result_top_rating = get_top_rating(page)
	idTopList = result_top_rating[0].tolist()
	nbMovies = result_top_rating[1]
	nbPages = result_top_rating[2]

	# Get all movies corresponding to the list of ids
	data = db.movies.find({
		"id": {
			"$in": idTopList
		}
	})
	if (data != None):
		return {
			"page": page,
			"result": json.loads(json_util.dumps(data)),
			"total_results": nbMovies,
			"total_pages": nbPages
		}, 200

	return { "msg": "Movie id not found" }, 404

# Routes for swagger docs and specs
@app.route("/docs")
def swagger_ui():
    return render_template('swagger_ui.html')

@app.route('/spec')
def get_spec():
    return send_from_directory(app.root_path, 'openapi.yaml')

if __name__ == "__main__":
	app.run(debug=True)