import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import numpy as np

movies_metadata = pd.read_csv("./data/movies_metadata.csv", low_memory=False)

# Calcule le nombre de vote minimum pour que le film soit comptabilisé, m
m = movies_metadata['vote_count'].quantile(0.90)

# Définit le TF-IDF Vectorizer. (Term frequency-inverse document frequency)
# C'est une méthode de calcul qui prend en compte la fréquence d'un terme dans un texte divisée par
# le nombre d'occurences de ce terme dans tous les textes
# ça permet de mettre en valeur les mots plus rares qui sont souvent plus déterminants
# Le stop_words supprime tous les mots anglais inutiles comme 'the', 'a' ...
tfidf = TfidfVectorizer(stop_words='english')

#Supprime les films avec peu de votes
movies_metadata = movies_metadata.copy().loc[movies_metadata['vote_count'] >= m]

#Remet les index à jour comme on a supprimé des films
movies_metadata = movies_metadata.reset_index()

#overview = synopsis
#Remplace les synopsis inexistants par '' car sinon ça fait des erreurs
movies_metadata['overview'] = movies_metadata['overview'].fillna('')

#Crée la matrice qui contient les films et les mots qui apparaissent
tfidf_matrix = tfidf.fit_transform(movies_metadata['overview'])

# Algorithme pour calculer la similarité entre les films en fonction dees mots (cosine)
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

#Crée une map qui associe l'index a l'id d'un film, on en a besoin pour la fonction get_recommandations
indices = pd.Series(movies_metadata.index, index=movies_metadata['id']).drop_duplicates()

# Fonction qui prend un titre de film en entrée et resort les id des films avec le plus de similarités
def get_movies_recommendations(movieId, cosine_sim=cosine_sim):
	#Récupère l'index du film et prend uniquement le premier film avec cet id
	movieId = str(movieId)
	temp = indices[movieId]
	if(temp.size > 1):
		idx = temp[0]
	else:
		idx = temp

	# Récupère les scores de similarité de tous les autres films avec celui-là
	sim_scores = list(enumerate(cosine_sim[idx]))

	# Trie les films en fonction du score de similarité
	sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

	# Enlève le premier film car cela correspond à lui même
	sim_scores = sim_scores[1:]

	# Récupère les index des films
	movie_indices = [i[0] for i in sim_scores]

	return movies_metadata['id'].iloc[movie_indices]