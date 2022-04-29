import math

MOVIES_BY_PAGES = 15

def get_page_of_movies(movies, page=1):
	# La numérotation commence à 1 => 2 = 2ème page
	page = page-1

	# Les films du top de la page sélectionné
	return movies[page*MOVIES_BY_PAGES:page*MOVIES_BY_PAGES+MOVIES_BY_PAGES]

# Le nombre total de films retenu
def get_nb_movies(movies):
	return movies.shape[0]

# Le nombre total de pages retenu
def get_nb_pages(movies):
	return int(math.ceil(movies.shape[0] / MOVIES_BY_PAGES))