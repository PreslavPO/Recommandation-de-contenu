# Recommandation de contenus 🎶
🎶 Application pour recommander des musiques en fonction des préférences de l'utilisateur à partir de ces des autres utilisateurs.

## Technologies
* Python :
  * [Flask](https://flask.palletsprojects.com/en/2.0.x/) : Micro Framework web pour gérer les intéractions entre le client et le serveur
  * [Pandas](https://pandas.pydata.org) : Bibliothèque pour manipuler et analyser des données
  * [venv](https://docs.python.org/fr/3/library/venv.html) : Module python pour créer un environnement virtuel
* Javascript :
  * [Electron](https://www.electronjs.org) : Environnement pour développer des applications de bureau en javascript (basé sur Chromium). Installer avec Vue CLI
  * [Vue](https://vuejs.org) : Framework pour gérer l'interface en javascript

## Installation

### Partie serveur
**Sur Windows**

Exécutez `install.bat`

Commande pour démarrer le serveur :
```
python server.py
```
**Sur Linux**

Exécutez les lignes suivantes :
```
python3 -m venv venv
source env/bin/activate
pip install -r requirements.txt
```
Commande pour démarrer le serveur :
```
python3 server.py
```

### Partie client