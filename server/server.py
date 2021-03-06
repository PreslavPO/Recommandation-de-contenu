from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv
import os

from resources.user import SignUp, Logout, Login, CheckSession, UserRating, UserRatingMovies, UserRecommendation, UserInformation
from resources.api import Movie, MovieCredits, ListMovies, Genres, Languages, MovieRecommendation

# Environment variables
load_dotenv()

# Init flask
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET")
api = Api(app)

# Enable CORS
CORS(app, supports_credentials=True)

# Movie api routes
api.add_resource(Movie, "/api/movie/<int:movieId>")
api.add_resource(MovieCredits, "/api/movie/<int:movieId>/credits")
api.add_resource(ListMovies, "/api/movie/list")
api.add_resource(Genres, "/api/movie/genres")
api.add_resource(Languages, "/api/movie/languages")
api.add_resource(MovieRecommendation, "/api/movie/<int:movieId>/recommendation")

# User routes
api.add_resource(SignUp, "/user/signup")
api.add_resource(Logout, "/user/logout")
api.add_resource(Login, "/user/login")
api.add_resource(UserRating, "/user/rating/<int:movieId>")
api.add_resource(UserRatingMovies, "/user/rating")
api.add_resource(CheckSession, "/user/session")
api.add_resource(UserRecommendation, "/user/recommendation")
api.add_resource(UserInformation, "/user/information")

# Routes for swagger docs and specs (Don't use restful -> template not working with it)
@app.route("/docs")
def swagger_ui():
    return render_template('swagger_ui.html')

@app.route('/spec')
def get_spec():
    return send_from_directory(app.root_path, 'openapi.yaml')

if __name__ == "__main__":
	app.run(debug=True)