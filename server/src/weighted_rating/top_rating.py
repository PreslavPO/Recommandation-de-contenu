import pandas as pd
import math

MOVIES_BY_PAGES = 15

movies_metadata = pd.read_csv("./data/movies_metadata.csv", low_memory=False)

def get_top_rating(page=1):
	# Calcule la moyenne de la colonne vote_average
	global_mean = movies_metadata['vote_average'].mean()

	# Calcule le nombre de vote minimum pour que le film soit comptabilisé
	min_vote = movies_metadata['vote_count'].quantile(0.90)

	# Cree un nouveau DataSet avec uniquement les films qui ont assez de vote
	q_movies = movies_metadata.copy().loc[movies_metadata['vote_count'] >= min_vote]

	def weighted_rating(data, mini=min_vote, mean=global_mean):
		v = data['vote_count']
		R = data['vote_average']
		# Calcule avec la formule IMDB
		return (v/(v+mini) * R) + (mini/(mini+v) * mean)

	# Creer une nouvelle colonne score calculer a l'aide de la fonction weighted_rating
	q_movies['score'] = q_movies.apply(weighted_rating, axis=1)

	#print(q_movies.shape)

	#Trie les films en fonction du score par ordre decroissant
	q_movies = q_movies.sort_values('score', ascending=False)

	# Selection des films en fonction de la page séléctionné
	page = page-1 # La numérotation commence à 1 => 2 = 2ème page

	# Renvoie :
	#	Les ids des films du top de la page sélectionné
	#	Le nombre total de films retenu
	#	Le nombre total de pages retenu
	return (
		q_movies[page*MOVIES_BY_PAGES:page*MOVIES_BY_PAGES+MOVIES_BY_PAGES]["id"].astype(int),
		q_movies.shape[0],
		int(math.ceil(q_movies.shape[0] / MOVIES_BY_PAGES))
	)