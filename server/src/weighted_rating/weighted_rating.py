import pandas as pd

movies_metadata = pd.read_csv("../../Data/movies_metadata.csv", low_memory=False)
# print(movies_metadata.head(3))
# movies_metadata.info()

# Calculer la moyenne de la colonne vote_average
C = movies_metadata['vote_average'].mean()
print(C)

# calcule le nombre de vote minimum pour que le film soit comptabilisé, m
m = movies_metadata['vote_count'].quantile(0.90)
print(m)

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
print(q_movies[['title', 'vote_count', 'vote_average', 'score']].head(20))