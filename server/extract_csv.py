import pandas as pd

# TODO : clear broken lines
def csv_to_dataframe(filepath):
	# Création du dataframe
	df = pd.read_csv(filepath)
	# TODO : Définir les dtypes (pour éviter d'avoir des id comme string par exemple)
	"""df = pd.read_csv(filepath,
		on_bad_lines="warn",
		dtype={
			"adult": bool,
			"belongs_to_collection": object,
			"budget": int,
			"genres": object,
			"homepage": "string",
			"id": int,
			"imdb_id": int,
			"original_language": object,
			"original_title": "string",
			"overview": "string",
			"popularity": float,
			"poster_path": "string",
			"production_companies": object,
			"production_countries": object,
			"release_date": "string",
			"revenue": int,
			"runtime": float,
			"spoken_languages": object,
			"status": "string",
			"tagline": "string",
			"title": "string",
			"video": bool,
			"vote_average": float,
			"vote_count": int
		}
	)"""
	return df

def dataframe_to_dict(dataframe):
	jsonArray = dataframe.to_dict(orient="records")
	return jsonArray

def get_dataframe_files():
	return csv_to_dataframe("./data/movies_metadata.csv")
	#, csv_to_json("./data/credits.csv"), csv_to_json("./data/keywords.csv"), csv_to_json("./data/links.csv"), csv_to_json("./data/links_small.csv"), csv_to_json("./data/ratings.csv"), csv_to_json("./data/ratings_small.csv")