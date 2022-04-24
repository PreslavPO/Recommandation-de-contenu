from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import json_util
from src.weighted_rating.top_rating import get_top_rating, get_page_of_movies, get_nb_movies, get_nb_pages
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
	return { "message": "Movie id not found" }, 404


@app.route("/api/movie/<int:movieId>/credits", methods=["GET"])
def movieCredits(movieId):
	data = db.credits.find_one({ "id": movieId })
	if (data != None):
		return json.loads(json_util.dumps(data)), 200
	return { "message": "Movie id not found" }, 404


@app.route("/api/movie/list", methods=["GET"])
def listMovies():
	page = int(request.args.get("page", 1))
	# Values : top_rating.asc, top_rating.desc, release_date.asc, release_date.desc
	sort_by = request.args.get("sort_by", "top_rating.desc")
	# ISO 639-1 : en, fr ...
	original_language = request.args.get("original_language")
	# Genre ids
	genres = request.args.get("genres")
	# Date : YYYY-MM-DD
	release_date_gte = request.args.get("release_date.gte")
	release_date_lte = request.args.get("release_date.lte")

	# Get movie list
	result_movies = get_top_rating()
	# Filter language
	if (original_language != None):
		result_movies = result_movies.loc[result_movies["original_language"] == original_language]
	# Filter genres
	if (genres != None):
		# Regex to find each elements in genres (AND operator)
		genresRegex = "(?=.*" + ")(?=.*".join(genres.split(",")) + ")"
		result_movies = result_movies.loc[result_movies["genres"].str.contains(genresRegex)]
	# Filter dates
	if (release_date_gte != None):
		result_movies = result_movies.loc[result_movies["release_date"] >= release_date_gte]
	if (release_date_lte != None):
		result_movies = result_movies.loc[result_movies["release_date"] <= release_date_lte]

	# Value to sort
	sort_value = ""
	if (sort_by.startswith("top_rating")):
		sort_value = "score"
	elif (sort_by.startswith("release_date")):
		sort_value = "release_date"
	
	# Sort by ascending or descending
	if (sort_by.endswith(".asc")):
		result_movies = result_movies.sort_values(sort_value, ascending=True)
	elif (sort_by.endswith(".desc")):
		result_movies = result_movies.sort_values(sort_value, ascending=False)
	
	# List of movie ids
	idTopList = get_page_of_movies(result_movies, page).tolist()

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


@app.route("/api/movie/genres", methods=["GET"])
def getGenres():
	data = db.movies.aggregate([
		# Keep only each list of genres of each movie
		{ "$group": { "_id": "$genres" } },
		# One document correspond to one genre (elements in an array separated to a document for each)
		{ "$unwind": { "path": "$_id" } },
		# Select id and name of the object kept
		{ "$project": { "_id": "$_id.id", "name": "$_id.name" } },
		# Select one document for same genres (Distinct)
		{ "$group": { "_id": "$_id", "name": { "$first": "$name" } } },
		# Select document not null
		{ "$unwind": { "path": "$_id", "preserveNullAndEmptyArrays": False } },
	])

	if (data != None):
		result = list(data);
		return jsonify(result), 200
	return { "message": "Genres were not found" }, 404


@app.route("/api/movie/languages", methods=["GET"])
def getLanguages():
	data = db.movies.aggregate([
		# Count each original language while keeping all spoken languages (will be used to have full name of each language)
		{ "$group": { "_id": "$original_language", "total": { "$sum": 1 }, "name": { "$push": "$spoken_languages" } } },
		# Unwind and group to transform array of arrays of objects to an array of objects
		{ "$unwind": "$name" },
		{ "$unwind": "$name" },
		{ "$group": { "_id": "$_id", "total": { "$first": "$total" }, "name": { "$push": "$name" } } },
		# Keep only the spoken languages corresponding to the id
		{ "$addFields": { "name": { 
			"$filter": { "input": "$name", "as": "item", "cond": { "$eq": ["$$item.iso_639_1", "$_id"] } }
		}}},
		# Transform array to string (Each array have the same occurence of one element)
		{ "$set": { "name": { "$arrayElemAt": ["$name.name", 0] } } },
		# Remove empty id
		{ "$match": { "_id": { "$not": { "$eq": "" } } } },
		# Replace empty name with id
		{ "$set": { "name": { "$cond": { 
			"if": { "$or": [{ "$eq": ["$name", ""] }, { "$not": ["$name"] }] },
			"then": "$_id",
			"else": "$name"
		}}}},
		# Sort in descending order
		{ "$sort": { "total": -1 } },
	])

	if (data != None):
		result = list(data)
		return jsonify(result), 200
	return { "message": "Languages were not found" }, 404

# Routes for swagger docs and specs
@app.route("/docs")
def swagger_ui():
    return render_template('swagger_ui.html')

@app.route('/spec')
def get_spec():
    return send_from_directory(app.root_path, 'openapi.yaml')

if __name__ == "__main__":
	app.run(debug=True)