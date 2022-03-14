from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from extract_csv import get_dataframe_files, dataframe_to_dict

app = Flask(__name__)

# Esquisse de l'implémentation de la bdd
# app.config ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
# db = SQLAlchemy(app)

# class movie(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	name = db.Column(db.String(255), nullable=False)

# db.create_all()

# Activer CORS
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

@app.route("/api/movie/<int:id>", methods=['GET'])
def movie(id):
	movies = get_dataframe_files()
	movieFinded = movies.loc[movies["id"] == str(id)] # L'id est stocké comme un string
	return jsonify(dataframe_to_dict(movieFinded)[0])

if __name__ == "__main__":
	app.run(debug=True)