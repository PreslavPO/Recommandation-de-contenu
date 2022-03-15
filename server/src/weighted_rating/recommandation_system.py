import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import numpy as np

movies_metadata = pd.read_csv("../../Data/movies_metadata.csv", low_memory=False)
ratings = pd.read_csv("../../Data/ratings_small.csv", low_memory=False)
links = pd.read_csv("../../Data/links.csv", low_memory=False)
# print(movies_metadata.head(3))
# movies_metadata.info()

# Calculer la moyenne de la colonne vote_average
#C = movies_metadata['vote_average'].mean()
#print(C)

# calcule le nombre de vote minimum pour que le film soit comptabilisé, m
m = movies_metadata['vote_count'].quantile(0.90)
#print(m)

# Creer un nouveau DataSet avec uniquement les films qui ont assez de vote
#q_movies = movies_metadata.copy().loc[movies_metadata['vote_count'] >= m]
#print(q_movies.shape)

#print(movies_metadata.shape)

#def weighted_rating(x, m=m, C=C):
#    v = x['vote_count']
#    R = x['vote_average']
#    # Calcule avec la formule IMDB
#    return (v/(v+m) * R) + (m/(m+v) * C)

# Creer une nouvelle colonne score calculer a l'aide de la fonction weighted_rating
#q_movies['score'] = q_movies.apply(weighted_rating, axis=1)

#print(q_movies.shape)

#Trie les films en fonction du score par ordre decroissant
#q_movies = q_movies.sort_values('score', ascending=False)

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

#Supprime les films avec peu de votes
movies_metadata = movies_metadata.copy().loc[movies_metadata['vote_count'] >= m]

#Relet les index à jour comme on a supprimé des films
movies_metadata = movies_metadata.reset_index()

#overview = synopsis
#Remplace les synopsis inexistants par '' car sinon ça fait des erreurs
movies_metadata['overview'] = movies_metadata['overview'].fillna('')

#Crée la matrice qui contient les films et les mots qui apparaissent
tfidf_matrix = tfidf.fit_transform(movies_metadata['overview'])

# Algorithme pour calculer la similarité entre les films en fonction dees mots (cosine)
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

#Crée une map qui associe l'index au titre d'un film, on en a besoin pour la fonction get_recommandations
indices = pd.Series(movies_metadata.index, index=movies_metadata['title']).drop_duplicates()

# Fonction qui prend un titre de film en entrée et resort les id des 10 fillms avec le plus de similarités dans le synopsis
def get_recommendations(title, cosine_sim=cosine_sim):
    #Récupère l'index du film et prend uniquement le premier film avec ce titre
    temp = indices[title]
    if(temp.size > 1):
        idx = temp[0]
    else :
        idx = temp

    # Récupère les scores de similarité de tous les autres films avec celui-là
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Trie les films en fonction du score de similarité
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Ne garde que les 10 premiers films (sans compter le film lui-même)
    sim_scores = sim_scores[1:11]

    # Récupère les index des films
    movie_indices = [i[0] for i in sim_scores]

    # Retourne les id des 10 films
    return movies_metadata['id'].iloc[movie_indices]

#print(get_recommendations('The Dark Knight Rises'))

# ___________________________________EVALUATION_____________________________________

#Supprime les films avec des notes inférieures à 2.5/5 car on ne veut que les films que les utilisateurs ont aimé
ratings = ratings.copy().loc[ratings['rating'] > 2.5]

#Remet les index à jour comme on a supprimé des films
ratings = ratings.reset_index()

#Fonction qui évalue la qualité des recommandations :
# On va regarder dans tous les utilisateurs qui ont vu le film qu'on a choisi s'ils ont aussi vu les films qu'on a recommandé
def eval(titre_film):
    # Récupère les id des 10 films recommandés avec ce nom de film
    recommanded = get_recommendations(titre_film)

    # On doit récupèrer le movieId du film de base car on en a besoin pour faire le lien avec les notes des utilisateurs
    # (il n'y a que le movieId dans la base utilisateurs et dans la base films il n'y a que le tmdbId
    # Pour cela on va faire la passerelle avec la base links qui contient les deux id :

    # Récupère les films avec ce nom de film dans la base de données de films
    name = movies_metadata.loc[movies_metadata['title'] == titre_film, :]
    # ne garde que le tmdbId du premier film de la liste
    baseId = int(name.iloc[0, 6])
    # Récupère la ligne avec ce tmdbId dans la base links
    link2 = links.loc[links['tmdbId'] == baseId, :]
    # récupère le movieId correspondant
    baseMovieId = link2.iloc[0, 0]


    # Variable qui va augmenter à chaque fois qu'on teste si un film qu'on a recommandé a été vu
    nb = 0
    # Variable qui va augmenter à chaque fois qu'un film recommandé a été vu par un utilisateur qui avait vu le film de base
    nbReco = 0
    # Variable qui va augmenter à chaque fois qu'on passe à un nouvel idUser (permet de savoir quand est-ce qu'on a bouclé
    # dans tous les films qu'un utilisateur a vu
    varId = 1
    # Tableau qui va contenir tous les id de films d'un utilisateur et qui va être reset à chaque nouvel utilisateur
    tab = []

    #On boucle dans la table des utilisateurs
    for i,j in enumerate(ratings.T):
        movie_id = ratings.iloc[i,2]
        user_id = ratings.iloc[i,1]
        #Tant qu'on a pas passé tous les films que l'utilisateur a vu, on se contente d'ajouter les id dans le tableau
        if user_id == varId:
            tab.append(movie_id)
        #Une fois qu'on arrive à l'utilisateur suivant, on fait les tests pour voir si l'utilisateur a vu notre film et
        # si oui s'il a vu ceux qu'on recommande
        else:
            for j in tab:
                # Teste si le film de base est dans la liste des films vus
                if j == baseMovieId:
                    # Si oui, on teste tous les films qu'on a recommandé
                    for l in recommanded:
                        # Les 3 lignes suivantes récupèrent l'id de chaque film recommandé
                        id = int(l)
                        link = links.loc[links['tmdbId'] == id, :]
                        movieId = link.iloc[0, 0]
                        # A chaque test on incrémente nb
                        nb= nb + 1
                        for k in tab:
                            if k == movieId:
                                #si le film a été vu on incrémente nbReco
                                nbReco = nbReco+1
            #Une fois les tests faits on passe à l'utilisateur suivant et on reset le tableau
            varId = varId +1
            tab = []
            tab.append(movie_id)
    #On retourne le pourcentage de films recommandés vus
    return (nbReco/nb)*100

print(eval('The Dark Knight Rises'))
# Pour ce film par exemple, 15% des films qu'on a recommandés avaient déjà été vus par les utilisateurs qui avaient vu ce film.
# C'est un score correct mais on doit pouvoir faire mieux




