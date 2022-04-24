from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from flask_restful import Api

from resources.user import SignUp
from resources.api import Movie, MovieCredits, ListMovies, Genres, Languages

app = Flask(__name__)
api = Api(app)

# Enable CORS
CORS(app)

# Movie api routes
api.add_resource(Movie, "/api/movie/<int:movieId>")
api.add_resource(MovieCredits, "/api/movie/<int:movieId>/credits")
api.add_resource(ListMovies, "/api/movie/list")
api.add_resource(Genres, "/api/movie/genres")
api.add_resource(Languages, "/api/movie/languages")

# User routes
api.add_resource(SignUp, "/user/signup")

# Routes for swagger docs and specs (Don't use restful -> template not working with it)
@app.route("/docs")
def swagger_ui():
    return render_template('swagger_ui.html')

@app.route('/spec')
def get_spec():
    return send_from_directory(app.root_path, 'openapi.yaml')

if __name__ == "__main__":
	app.run(debug=True)