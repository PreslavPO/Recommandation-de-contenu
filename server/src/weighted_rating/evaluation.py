import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import numpy as np

movies_metadata = pd.read_csv("./data/movies_metadata.csv", low_memory=False)
ratings = pd.read_csv("./data/ratings.csv", low_memory=False)
links = pd.read_csv("./data/links.csv", low_memory=False)

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




