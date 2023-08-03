# API_Tripadvisor

Cette API extrait et renvoie des informations utiles telles que : les avis (en français) et le score global d'un restaurant à partir de TripAdvisor.

Elle extrait les données en utilisant les instructions suivantes :

Si vous voulez uniquement extraire tous les restaurants et les informations de base d'une zone environnante, utilisez
http://127.0.0.1:8000/restaurant/{cityid}

Vous pouvez trouver le cityid sur TripAdvisor.
Par défaut, cela extrait uniquement les 30 meilleurs restaurants de votre zone environnante.

Selon vos instructions, vous pouvez ajouter une requête telle que :
http://127.0.0.1:8000/restaurant/{cityid}?review=True

ou

http://127.0.0.1:8000/restaurant/{cityid}?full=True

qui renvoie soit tous les avis de la zone environnante, soit tous les restaurants de la zone.
Vous pouvez combiner ces requêtes en quelque chose comme ceci :

http://127.0.0.1:8000/restaurant/{cityid}?review=True&full=True

Cela renvoie tous les avis de tous les restaurants de la zone.
Cela prend quelques heures en fonction du nombre de restaurants dont vous souhaitez extraire les informations.

Vous pouvez également extraire des informations utiles d'un restaurant unique en utilisant :

http://127.0.0.1:8000/restaurant/{cityid}/{restaurantid}

Cela renvoie les informations de la première page web affichée sur TripAdvisor pour le restaurant.
Cela prend également les requêtes pour extraire tous les avis.

Cette API peut également afficher un tableau de bord utile en utilisant l'instruction :

http://127.0.0.1:8000/restaurant/{cityid}/{restaurantid}/dashboard

Cela renvoie alors :
- Informations sur le restaurant
- Liste des mots les plus utilisés dans les avis
- Un top 10 des commentaires
- Un pire 10 des commentaires

## Structure du projet

Le projet contient les fichiers suivants :

- `FranceCitiesGeoTag.xlsx` : Un fichier Excel contenant des informations géographiques sur les villes de France.
- `IntegratedSA.py` : Un script Python pour l'analyse de sentiment intégrée.
- `IntegratedScraper.py` : Un script Python pour le scraper intégré qui extrait les données de TripAdvisor.
- `README.md` : Le fichier README du projet.
- `chromedriver` : Le pilote Chrome utilisé par Selenium pour automatiser la navigation sur les pages web.
- `lstm_model.h5` : Un modèle LSTM pré-entraîné pour l'analyse de sentiment.
- `mainapi.py` : Le fichier principal de l'API.
- `requierments.txt` : Un fichier contenant les dépendances Python nécessaires pour exécuter le projet.
- `resto_semtiment.ipynb` : Un notebook Jupyter pour l'analyse de sentiment des avis de restaurants.

Pour utiliser ce projet, vous devez d'abord cloner le dépôt sur votre machine locale. Ensuite, naviguez jusqu'au répertoire du projet et installez les dépendances nécessaires en utilisant pip :

```bash
pip install -r requierments.txt
```

Ensuite, vous pouvez démarrer l'API en utilisant la commande suivante :

```bash
python mainapi.py
```

Cela démarrera l'API sur votre machine locale. Vous pouvez alors accéder à l'API en ouvrant votre navigateur web et en naviguant jusqu'à `http://localhost:8000`.
