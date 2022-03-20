# Recommandation de contenus 🎬
🎬 Application pour recommander des musiques en fonction des préférences de l'utilisateur à partir de celles des autres utilisateurs.

Lien de la base de données utilisées : https://www.kaggle.com/rounakbanik/the-movies-dataset

## Technologies
* Python :
	* [Flask](https://flask.palletsprojects.com/en/2.0.x/) : Micro Framework web pour gérer les interactions entre le client et le serveur
	* [Pandas](https://pandas.pydata.org) : Bibliothèque pour manipuler et analyser des données
	* [venv](https://docs.python.org/fr/3/library/venv.html) : Module python pour créer un environnement virtuel
* Javascript :
	* [Electron](https://www.electronjs.org) : Environnement pour développer des applications de bureau en Javascript (basé sur Chromium). Installer avec Vue CLI
	* [Vue](https://vuejs.org) : Framework pour gérer l'interface en Javascript
* [Sass](https://sass-lang.com) : Préprocesseur pour css


## Installation

### Partie serveur
Situez vous dans le dossier `server`

Exécutez les lignes de commande suivantes (Effectif sur Windows, cela diffère sur Linux) :
```
      > python -m venv venv
      > .\venv\Scripts\activate
(env) > pip install -r .\requirements.txt
```
Commande pour démarrer le serveur :
```
      > .\venv\Scripts\activate
(env) > python server.py
```
*(env) indique que l'on se situe dans l'environnement virtuel*


L'adresse du serveur est `localhost:5000`

### Partie client
Situez vous dans le dossier `client`

Exécutez la commande suivante : 
```
npm install
```

Pour lancer l'application sur navigateur :
```
npm run serve
```
L'adresse du client est `localhost:8080`

Pour lancer l'application avec electron :
```
npm run electron:serve
```

### Import data in mongoDB

Go to `./server/dataToDb` directory and install dependencies :
```bash
npm install
```

Create a database `<NameDB>` and a collection `movies` beforehand, the collection name is `movies`. Replace `<NameDB>`, `<Username>`, `<Password>` in the commands below

Import csv to mongoDB :
```properties
mongoimport --db <NameDB> --collection movies --type csv --file ./server/data/movies_metadata.csv --headerline --uri mongodb+srv://<Username>:<Password>@cluster0.xyttr.mongodb.net/
```

Convert mongoDB data :
```properties
mongosh mongodb+srv://<Username>:<Password>@cluster0.xyttr.mongodb.net/<NameDB> mongodb-import.js
```