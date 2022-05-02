# Recommandation de contenus 🎬
🎬 Application pour recommander des films avec différents algorithmes.

![Miniature recommandation de contenus](https://imgur.com/a/MiVACDt)

Lien de la base de données utilisées : https://www.kaggle.com/rounakbanik/the-movies-dataset

## Technologies
* Python :
	* [Flask](https://flask.palletsprojects.com/en/2.0.x/) : Micro Framework web pour gérer les interactions entre le client et le serveur
	* [Pandas](https://pandas.pydata.org) : Bibliothèque pour manipuler et analyser des données
	* [venv](https://docs.python.org/fr/3/library/venv.html) : Module python pour créer un environnement virtuel
* Javascript :
	* [Electron](https://www.electronjs.org) : Environnement pour développer des applications de bureau en Javascript (basé sur Chromium). Installé avec Vue CLI
	* [Vue](https://vuejs.org) : Framework pour gérer l'interface en Javascript
* [Sass](https://sass-lang.com) : Préprocesseur pour css


## Installation

### Prérequis

Assurer vous d'avoir tous les prérequis.
 - Windows
 - Etre connecté à internet (Avec une connexion qui ne bloque pas les requêtes : l'université les bloque)
 - Python avec version <= 3.7, Voir détails en [bas de page](#python) si ce n'est pas le cas
   - Vérifiez avec la commande ```python --version```
 - Microsoft Visual C++ 14.0, voir en [bas de page](#c) pour plus d'informations
 - NodeJS (npm) : Disponible [ici](https://nodejs.org)

### Partie serveur
Situez vous dans le dossier `server`

Téléchargez les fichiers non présent sur github à [cette adresse](https://1fichier.com/?8stcfjpgvbsurfe58swj) (Variables d'environnement et fichiers csv).

Mettez le fichier `.env` et le dossier `data` à la base du dossier `server`.

Une fois cela fait, exécutez les lignes de commande suivantes (En étant bien situé dans le dossier server) :
```
      > python -m venv venv
      > .\venv\Scripts\activate
(env) > pip install -r .\requirements.txt
```
Commande pour démarrer le serveur :
```
(env) > python server.py
```
*(env) indique que l'on se situe dans l'environnement virtuel*


L'adresse du serveur est `localhost:5000`.
Vous pouvez par exemple taper `localhost:5000/docs` pour voir la documentation de l'API.

### Partie client
Situez vous dans le dossier `client`

Exécutez la commande suivante : 
```
npm install
```

Pour lancer l'application avec electron :
```
npm run electron:serve
```
Pour lancer l'application sur navigateur :
```
npm run serve
```
L'adresse du client est `localhost:8080`

## Détails d'installation

Toutes les informations supplémentaires pour les dépendances non installées.
### Python
Pour installer python 3.7.9 pour windows 64 bit, télécharger [ici](https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64-webinstall.exe)
Si vous avez un système différent, téléchargez le [ici](https://www.python.org/downloads/windows/)

Ensuite, suivez les instructions de l'installer, vous pouvez mettre python dans le PATH, mais si vous avez déjà une configuration, vous pouvez lancer une commande python en prenant le chemin du fichier où il est installé : 
```properties
> C:\Users\<Nom>\AppData\Local\Programs\Python\Python37\python.exe <Commande>
```

### C++
Il faut avoir C++ d'installer sur sa machine pour permettre à `scikit-surprise` de s'intaller. Vous pouvez l'installer avec [Build Tools](https://visualstudio.microsoft.com/fr/visual-cpp-build-tools/). Selectionnez bien `Développement Desktop en C++` lors de l'installation.