from collections import defaultdict
import pandas as pd
import numpy as np
from surprise import KNNWithMeans, Reader, Dataset, accuracy
from surprise.model_selection import KFold
from surprise.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import pickle
import matplotlib.pyplot as plt

movies_metadata = pd.read_csv("../../Data/movies_metadata.csv", low_memory=False)
ratings = pd.read_csv("../../Data/ratings_small.csv", low_memory=False)
links = pd.read_csv("../../Data/links.csv", low_memory=False)

# Pour faire du collaborative filtering, il y a 3 étapes :
# 1. Trouver quels utilisateurs sont similaires entre eux (ou quels films si on fait du item-based)
# 2. Déterminer quelle note aurait mis un utilisateur à un film en se basant sur les notes qu'ont mis les utilisateurs similaires
# 3. Mesurer la précision des notes que l'on a trouvé
# A partir de ça, on peut conseiller à l'utilisateur les films qui ont les meilleures notes selon ce qu'on a trouvé


# name correspond à ce qu'on va utiliser pour calculer la similarité (il y a cosine, msd, pearson, pearson_baseline)
# min_support correspond au nombre minimum de films en commun pour que deux utilisateurs soient considérés comme similaires
# user_based = False siginifie que ce sera item-based
sim_options = {
    "name": "msd",
    "min_support": 3,
    "user_based": True,
}

# KNN = K-Nearest Neighbours
# KNNWithMeans prend en compte la note moyenne de chaque utilisateur
# car il y a des utilisateurs qui sont plus sévères sur leurs notes et on prend ça en compte pour calculer la similarité
# Il y a d'autres algos de prédiction comme le SVD par exemple
algo = KNNWithMeans(sim_options=sim_options)

# Reader lit les données
reader = Reader()
# Dataset.load_from_df permet de charger un dataset à partir d'un dataframe pandas
# On garde uniquement les 3 premières colonnes de ratings (pas besoin de timestamp)
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

# Un trainset est un dataset qui contient plus d'informations comme le nombre d'utilisateurs et le nombre de films par exemple,
# et auquel on peut appliquer des fonctions
# liste des fonctions : https://surprise.readthedocs.io/en/stable/trainset.html
trainset = data.build_full_trainset()

# Entraîne l'algorithme sur le trainset
algo.fit(trainset)
#Si on veut la note que l'user 2 aurait donné au film 123 selon notre algo :
#prediction = algo.predict(2, 123)
#print(prediction.est)

#Si on veut les 5 users les plus similaires à l'user 2 :
#similar_users = algo.get_neighbors(2, 5)
#print(similar_users)

# trainset.build_anti_testset() renvoie une liste de tuples qui contient tous les films qui n'ont pas été
# notés pour chaque user, sous la forme : (user_id, film_id, fill)
#testset = trainset.build_anti_testset()

# algo.test(testset) estime avec l'algorithme toutes les notes vides du testset
# prend beaucoup de temps
#predictions = algo.test(testset)

# Enregistre avec pickle le modèle
with open('../../Data/model.pkl', 'wb') as f:
    pickle.dump(algo, f)

# Pour récupérer le modèle depuis le fichier model.pkl :
# with open('../../Data/model.pkl', 'rb') as f:
#    algo_copie = pickle.load(f)

# Test que ça fonctionne bien
# print(algo_copie.predict(2, 123).est)


#Fonction qui prend en paramètres les prédictions et le nombre de films qu'on veut avoir
#Retourne un tableau avec les nb_films les mieux notés pour chaque user selon l'algo (on retourne le movieId du film et sa note)
def predictAll(predictions, nb_films):

    # defaultdict(list) permet de créer un dictionnaire qui va stocker les films et les notes associées
    # à un user donné
    # L'avantage de ça par rapport à un tableau est que si on essaie d'accéder à une clé qui n'existe pas,
    # il va créer la clé et lui donner une liste vide
    films = defaultdict(list)

    # On parcourt les prédictions et on ne garde dans le tableau que les prédictions
    for uid, film_id, _, note_estimee, _ in predictions:
            films[uid].append((film_id, note_estimee))

    # Trie le tableau et récupère les nb_films premiers
    for uid, note_estimee in films.items():
        note_estimee.sort(key=lambda x: x[1], reverse=True)
        films[uid] = note_estimee[:nb_films]

    return films

# Renvoie les id des nb_films films les mieux notés pour l'user user_id selon notre algo
def films_mieux_notes_par_l_user(algo, trainset, user_id, nb_films):
    pred = []
    # Predit les films
    for i in trainset.all_items():
        pred.append((i, algo.predict(user_id, i).est))

    # trie les predictions par ordre décroissant
    pred = sorted(pred, key=lambda x: x[1], reverse=True)

    # garde les 5 premiers
    pred = pred[:nb_films]
    return pred

predicted = films_mieux_notes_par_l_user(algo, trainset, 26, 5)

# Pour récupérer les noms des films :
def recup_titres(predicted):
    recommanded_films = []
    for i,j in predicted:
        # Récupère la ligne avec ce movieId dans la base links
        link = links.loc[links['movieId'] == i, :]
        # récupère le tmdbId correspondant
        tmdbId = link.iloc[0, 1]
        # On transforme un peu le tmdbId pour qu'il colle à celui dans movies_metadata ( = on rajoute tt au début puis on ajoute des
        # 0 devant le nombre jusqu'à avoir un nombre de chiffres égal à 7)
        tmdbId_new = 'tt' + str(tmdbId).zfill(7)
        # Récupère la ligne avec ce tmdbId dans la base movies_metadata
        movie = movies_metadata.loc[movies_metadata['imdb_id'] == tmdbId_new, :]
        # Récupère le titre du film
        title = movie.iloc[0, 20]
        recommanded_films.append(title)
    return recommanded_films

print(recup_titres(predicted))

###########################################################
# RMSE evaluation

# RMSE = Root Mean Square Error
# RMSE prédit les notes pour des paires user-film qui ont déjà une note et compare ces notes avec les notes réelles
# Plus on s'approche de 1 mieux c'est
#print("RMSE:", accuracy.rmse(predictions))


##########################################################
# Pour tester quels sont les meilleurs paramètres pour avoir l'algo le plus précis :

# On met toutes les possibilités qu'on veut tester
#sim_options = {
#    "name": ["msd", "cosine"],
#    "min_support": [3, 4, 5],
#    "user_based": [False, True],
#}

#param_grid = {"sim_options": sim_options}

# GridSearchCV permet de tester tous les paramètres possibles
#gs = GridSearchCV(KNNWithMeans, param_grid, measures=["rmse", "mae"], cv=3)
#gs.fit(data)

#print(gs.best_score["rmse"])
#print(gs.best_params["rmse"])

# Ici on avait le meilleur score pour name = msd, min_support = 3 et user_based = True


with open('../../Data/pred.pkl', 'rb') as f:
    predictions = pickle.load(f)


#return une liste avec les films que 'usr' à noté
def get_films_by_user(usr):

    user_to_films = []

    for ind in ratings.index:
        if ratings['userId'][ind] == usr:
            user_to_films.append(ratings['movieId'][ind])
    return user_to_films
film_listenned = get_films_by_user(1)
print(film_listenned)


#initialisation des tab
y_pred = []
y_true = []
list_film = []
list_note = []


# On parcourt les prédictions et on ne ajoute les films et note au tableau correspondant
for uid, film_id, _, note_estimee, _ in predictions:
    list_film.append(film_id)
    list_note.append(note_estimee)

#creer un dataframe
df = pd.DataFrame(
    {'note': list_note,
     'film': list_film,
    })

#trie
df = df.sort_values('note', ascending=False)

#on remplie y_pred et y_true
for index, row in df.iterrows():
   y_pred.append(row['note'])
   if int(row['note']) >= 4 and int(row['film']) in film_listenned:
       y_true.append(1)
   else:
       y_true.append(0)


#auc
def compute_roc(y_true, y_pred, plot=True):

    fpr, tpr, thresholds = metrics.roc_curve(y_true, y_pred)
    auc_score= metrics.auc(fpr, tpr)
    #fpr, tpr = roc_curve(y_true, y_pred)
    #auc_score = auc(fpr, tpr)
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


compute_roc(y_true,y_pred)