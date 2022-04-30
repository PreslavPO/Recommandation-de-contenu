import pandas as pd
import pickle
from surprise import Reader, Dataset, SVD

# Renvoie les id des nb_films films les mieux notés pour l'user user_id selon notre algo
def films_mieux_notes_par_l_user(algo, trainset, user_id):
    pred = []
    # Predit les films
    for i in trainset.all_items():
        pred.append((i, algo.predict(user_id, i).est))

    # trie les predictions par ordre décroissant
    pred = sorted(pred, key=lambda x: x[1], reverse=True)

    return pred

def get_trainset(userId, ratings):
	# Transform ratings list into the correct dataframe format
	user_ratings = pd.DataFrame(ratings)
	user_ratings = user_ratings[["movieId", "rating"]]
	user_ratings.insert(0, "userId", userId)
	# Divide ratings by 2 because entry ratings is /10 but ratings wanted is /5
	user_ratings["rating"] = user_ratings["rating"].div(2).round(1)

	print("-------------- user_ratings --------------")
	print(user_ratings)
	print("------------------------------------------")

	# Add ratings to the global ratings
	global_ratings = pd.read_csv("./data/ratings_small.csv", usecols=['userId', 'movieId', 'rating'], low_memory=False)
	# Convert int to string (because userId is a string)
	# global_ratings["userId"] = global_ratings["userId"].astype(str)
	global_ratings = global_ratings.append(user_ratings, ignore_index=True)

	print("-------------- global_ratings --------------")
	print(global_ratings)
	print("--------------------------------------------")

	# Trainset
	reader = Reader()
	data = Dataset.load_from_df(global_ratings[['userId', 'movieId', 'rating']], reader)
	trainset = data.build_full_trainset()

	# Ça marche avec le truc de base
	# ratings = pd.read_csv("./data/ratings_small.csv", usecols=['userId', 'movieId', 'rating'], low_memory=False)
	# data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
	# trainset = data.build_full_trainset()

	# TODO : Save into csv each time a new rating is present (Current : at each get redo the training => not good)
	# with open('./data/trainset.pkl', 'wb') as f:
	# 	pickle.dump(trainset, f)
	return trainset

def get_collaborative_recommendation(trainset, userId):
	algo = SVD()
	algo.fit(trainset)
	# algo = None
	# with open('./data/model.pkl', 'rb') as f:
	# 	algo = pickle.load(f)

	return films_mieux_notes_par_l_user(algo, trainset, userId)