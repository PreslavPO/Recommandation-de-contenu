from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv
import os

from resources.user import SignUp, SignOut, UserInfo
from resources.api import Movie, MovieCredits, ListMovies, Genres, Languages

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

# User routes
api.add_resource(SignUp, "/user/signup")
api.add_resource(SignOut, "/user/signout")
api.add_resource(UserInfo, "/user")

# Routes for swagger docs and specs (Don't use restful -> template not working with it)
@app.route("/docs")
def swagger_ui():
    return render_template('swagger_ui.html')

@app.route('/spec')
def get_spec():
    return send_from_directory(app.root_path, 'openapi.yaml')

if __name__ == "__main__":
	app.run(debug=True)