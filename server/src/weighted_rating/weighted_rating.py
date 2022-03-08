import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

movies_metadata = pd.read_csv("../../Data/movies_metadata.csv", low_memory=False)
# print(movies_metadata.head(3))
# movies_metadata.info()

# Calculer la moyenne de la colonne vote_average
C = movies_metadata['vote_average'].mean()
#print(C)

# calcule le nombre de vote minimum pour que le film soit comptabilisé, m
m = movies_metadata['vote_count'].quantile(0.90)
#print(m)

# Creer un nouveau DataSet avec uniquement les films qui ont assez de vote
q_movies = movies_metadata.copy().loc[movies_metadata['vote_count'] >= m]
#print(q_movies.shape)

#print(movies_metadata.shape)

def weighted_rating(x, m=m, C=C):
    v = x['vote_count']
    R = x['vote_average']
    # Calcule avec la formule IMDB
    return (v/(v+m) * R) + (m/(m+v) * C)

# Creer une nouvelle colonne score calculer a l'aide de la fonction weighted_rating
q_movies['score'] = q_movies.apply(weighted_rating, axis=1)

#print(q_movies.shape)

#Trie les films en fonction du score par ordre decroissant
q_movies = q_movies.sort_values('score', ascending=False)

#Affiche top 20 films
#print(q_movies[['title', 'vote_count', 'vote_average', 'score']].head(20))

#_______________________________________________________________________________________________

#CONTENT BASED FILTERING EN FONCTION DU SYNOPSIS

#Définit le TF-IDF Vectorizer. (Term frequency-inverse document frequency)
# C'est une méthode de calcul qui prend en compte la fréquence d'un terme dans un texte divisée par
# le nombre d'occurences de ce terme dans tous les textes
# ça permet de mettre en valeur les mots plus rares qui sont souvent plus déterminants
# Le stop_words supprime tous les mots anglais inutiles comme 'the', 'a' ...
tfidf = TfidfVectorizer(stop_words='english')

#overview = synopsis
#Remplace les synopsis inexistants par '' car sinon ça fait des erreurs
q_movies['overview'] = q_movies['overview'].fillna('')

#Crée la matrice qui contient les films et les mots qui apparaissent
tfidf_matrix = tfidf.fit_transform(q_movies['overview'])

# Algorithme pour calculer la similarité entre les films en fonction dees mots (cosine)
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

#Crée une map qui associe l'index au titre d'un film, on en a besoin pour la fonction get_recommandations
indices = pd.Series(q_movies.index, index=q_movies['title']).drop_duplicates()

# Fonction qui prend un titre de film en entrée et resort les 10 fillms avec le plus de similarités dans le synopsis
def get_recommendations(title, cosine_sim=cosine_sim):
    #Récupère l'index du film
    idx = indices[title]

    # Récupère les scores de similarité de tous les autres films avec celui-là
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Trie les films en fonction du score de similarité
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Ne garde que les 10 premiers films (sans compter le film lui-même)
    sim_scores = sim_scores[1:11]

    # Récupère les index des films
    movie_indices = [i[0] for i in sim_scores]

    # Retourne les 10 films
    return q_movies['title'].iloc[movie_indices]

print(get_recommendations('Batman Forever'))