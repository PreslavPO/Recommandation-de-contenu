from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Activer CORS
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

@app.route("/api/hello")
def hello_world():
    return {"message": "Bonjour voici la recommandation de contenus !"}

if __name__ == "__main__":
	app.run(debug=True)