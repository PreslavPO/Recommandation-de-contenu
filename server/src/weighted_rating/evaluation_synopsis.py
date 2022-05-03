import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt

movies_metadata = pd.read_csv("../../data/movies_metadata.csv", low_memory=False)
ratings = pd.read_csv("../../data/ratings_small.csv", low_memory=False)
links = pd.read_csv("../../data/links.csv", low_memory=False)

# Calcule le nombre de vote minimum pour que le film soit comptabilisé, m
m = movies_metadata['vote_count'].quantile(0.90)

# _______________________________________________________________________________________________

# CONTENT BASED FILTERING EN FONCTION DU SYNOPSIS

# Définit le TF-IDF Vectorizer. (Term frequency-inverse document frequency)
# C'est une méthode de calcul qui prend en compte la fréquence d'un terme dans un texte divisée par
# le nombre d'occurences de ce terme dans tous les textes
# ça permet de mettre en valeur les mots plus rares qui sont souvent plus déterminants
# Le stop_words supprime tous les mots anglais inutiles comme 'the', 'a' ...
tfidf = TfidfVectorizer(stop_words='english')

# Supprime les films avec peu de votes
movies_metadata = movies_metadata.copy().loc[movies_metadata['vote_count'] >= m]

# Relet les index à jour comme on a supprimé des films
movies_metadata = movies_metadata.reset_index()

# overview = synopsis
# Remplace les synopsis inexistants par '' car sinon ça fait des erreurs
movies_metadata['overview'] = movies_metadata['overview'].fillna('')

# Crée la matrice qui contient les films et les mots qui apparaissent
tfidf_matrix = tfidf.fit_transform(movies_metadata['overview'])

# Algorithme pour calculer la similarité entre les films en fonction dees mots (cosine)
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Crée une map qui associe l'index au titre d'un film, on en a besoin pour la fonction get_recommandations
indices = pd.Series(movies_metadata.index, index=movies_metadata['title']).drop_duplicates()


# Fonction qui prend un titre de film en entrée et resort les id des 10 fillms avec le plus de similarités dans le synopsis
def get_recommendations(title, cosine_sim=cosine_sim):
    # Récupère l'index du film et prend uniquement le premier film avec ce titre
    temp = indices[title]
    if (temp.size > 1):
        idx = temp[0]
    else:
        idx = temp

    # Récupère les scores de similarité de tous les autres films avec celui-là
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Trie les films en fonction du score de similarité
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Ne garde que les 10 premiers films (sans compter le film lui-même)
    # sim_scores = sim_scores[1:11]

    # Récupère les index des films
    movie_indices = [i[0] for i in sim_scores]

    # Retourne les id des 10 films
    # return movies_metadata['id'].iloc[movie_indices]
    return sim_scores


# get_recommendations('The Dark Knight Rises')

# ___________________________________EVALUATION_____________________________________

y_pred = []
y_true = []


# ______________________________________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________________________________

def get_films_by_user(usr):
    user_to_films = []
    for ind in ratings.index:
        if ratings['userId'][ind] == usr:
            user_to_films.append(ratings['movieId'][ind])
    return user_to_films


def get_films_by_user2(usr):
    user_to_films = []
    for ind in ratings.index:
        if ratings['userId'][ind] == usr:
            user_to_films.append(ratings['rating'][ind])
    return user_to_films


#AUC
def eval(usr):
    y_true = []
    y_pred = []
    films_viewed = get_films_by_user(usr)
    ratings_films = get_films_by_user2(usr)
    titre_film = 'Avatar'
    # Récupère les films avec ce nom de film dans la base de données de films
    name = movies_metadata.loc[movies_metadata['title'] == titre_film, :]
    # ne garde que le tmdbId du premier film de la liste
    baseId = int(name.iloc[0, 6])
    # Récupère la ligne avec ce tmdbId dans la base links
    link2 = links.loc[links['tmdbId'] == baseId, :]
    # récupère le movieId correspondant
    baseMovieId = link2.iloc[0, 0]
    top_rating = get_recommendations(titre_film)

    recommanded2 = []
    recommanded = []
    notes = []

    # top_rating= top_rating.iloc[0:int(top_rating.shape[0]/100)]
    for i in range(int(len(top_rating) / 10)):
        recommanded2.append(top_rating[i][0])
        notes.append(top_rating[i][1])

    for l in recommanded2:
        # Retourne les id des 10 films
        test = movies_metadata['id'].iloc[l]
        id = int(test)
        link = links.loc[links['tmdbId'] == id, :]
        movieId = link.iloc[0, 0]
        recommanded.append(movieId)

    df = pd.DataFrame(
        {'note': notes,
         'film': recommanded,
         })
    # trie
    df = df.sort_values('note', ascending=False)

    for index, row in df.iterrows():
        test = False
        y_pred.append(row['note'])
        for i in range(len(films_viewed)):
            if (baseMovieId in films_viewed and int(row['film']) == films_viewed[i] and ratings_films[i] >= 4 and float(
                    row['note']) >= np.quantile(notes, .7)):
                y_true.append(1)
                test = True
                break
        if (test == False):
            y_true.append(0)

    fpr, tpr, thresholds = metrics.roc_curve(y_true, y_pred)
    auc_score = metrics.auc(fpr, tpr)
    # fpr, tpr = roc_curve(y_true, y_pred)
    # auc_score = auc(fpr, tpr)
    plot = True
    if plot:
        plt.figure(figsize=(7, 6))
        plt.plot(fpr, tpr, color='blue',
                 label='ROC (AUC = %0.4f)' % auc_score)
        plt.legend(loc='lower right')
        plt.title("ROC Curve")
        plt.xlabel("FPR")
        plt.ylabel("TPR")
        plt.show()

    return fpr, tpr, auc_score


# print(get_films_by_user(11))

tab_moy = []
# eval(1)

#On fait l'auc sur 100 utilisateurs et on fait la moyenne
# Sur 100 utilisateurs car beaucoup d'utilisateurs n'ont pas vu le film de base et
# on ne peut donc pas les évaluer
for i in range(1, 100):
    tab_moy.append(eval(i))

print(np.nanmean(tab_moy))