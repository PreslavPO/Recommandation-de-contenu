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


def get_top_rating():
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
        return (v / (v + mini) * R) + (mini / (mini + v) * mean)

    # Creer une nouvelle colonne score calculer a l'aide de la fonction weighted_rating
    q_movies['score'] = q_movies.apply(weighted_rating, axis=1)

    # Trie les films en fonction du score par ordre decroissant
    q_movies = q_movies.sort_values('score', ascending=False)

    # Converti les date
    q_movies["release_date"] = pd.to_datetime(q_movies["release_date"])

    return q_movies

# ___________________________________EVALUATION_____________________________________

y_pred = []
y_true = []

# coupe ratings en 10 pour que ça aille plus vite
#ratings= ratings.iloc[0:int(ratings.shape[0]/100)]

#Supprime les films avec des notes inférieures à 2.5/5 car on ne veut que les films que les utilisateurs ont aimé
#ratings = ratings.copy().loc[ratings['rating'] > 3.5]

#Remet les index à jour comme on a supprimé des films
ratings = ratings.reset_index()

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

#Fonction qui évalue la qualité des recommandations :
# On va regarder dans tous les utilisateurs qui ont vu le film qu'on a choisi s'ils ont aussi vu les films qu'on a recommandé
def eval(usr):
    films_viewed = get_films_by_user(usr)
    ratings_films = get_films_by_user2(usr)
    top_rating = get_top_rating()

    recommanded2 = []
    recommanded = []
    notes = []

    #top_rating= top_rating.iloc[0:int(top_rating.shape[0]/100)]
    for i in range(int(top_rating.size/1000)):
        recommanded2.append(top_rating["id"].iloc[i])
        notes.append(top_rating["score"].iloc[i])


    for l in recommanded2:
      id = int(l)
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
         if(int(row['film']) == films_viewed[i] and ratings_films[i] >= 4 and float(row['note']) >= np.quantile(notes, .7)):
           y_true.append(1)
           test = True
           break;
       if(test == False):
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

    return auc_score

tab_moy = []
#eval(1)

#On fait l'auc sur 100 utilisateurs et on garde la moyenne
#Prend un peu de temps sur 100 utilisateurs
for i in range(1,100):
  tab_moy.append(eval(i))

print(np.nanmean(tab_moy))