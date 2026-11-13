# Projet 2 INF1007 : « Êtes-vous spécial ? »

Un petit quiz interactif en 8 questions autour de nos habitudes et réflexes du quotidien (façon de s'organiser, gestion des tensions, réveil, imprévus, etc.). L'application compare les réponses à un échantillon statistique et utilise un modèle de Machine Learning pour déterminer le profil de l'utilisateur.

## Jeu de données
- Source : Sondage anonyme de 3 000 participants sur les comportements du quotidien.
- Licence : Usage éducatif ouvert (Polytechnique Montréal).
- Fichier : `donnees/etes_vous_special.csv` (environ 560 Ko).

## Organisation du travail avec Git
- `main` contient toujours une version qui passe les tests (CI verte).
- Chaque tâche se fait sur une **branche courte** créée à partir de `main` à jour (`donnees`, `modele`, `interface`, `docs`…).
- On fusionne dans `main`, une fois la CI verte, et on supprime la branche.
- Messages de commit courts et clairs, sous la forme « Ajout de… », « Correction de… », « Modification de… ».

## Installation et lancement
```
pip install -r requirements.txt
python src/main.py
```

## Tests et couverture
```
python -m pytest -v
coverage run -m pytest
coverage report
```
Couverture mesurée : 19 tests unitaires validés (100 % de réussite).

## Résultat du modèle
Métrique : Exactitude (Accuracy) de **88.5 %** · Référence (DummyClassifier) : **40.0 %**

## Structure du code
- `src/donnees.py` : lecture, nettoyage, classes de variables
- `src/modele.py` : entraînement, évaluation, prédiction
- `src/exceptions.py` : exceptions personnalisées
- `src/interface.py` : interface graphique
- `src/main.py` : point d'entrée
- `tests/` : tests pytest

## Outil du chapitre 7 utilisé
Générateur avec le mot-clé `yield` (`lire_lignes_blocs` dans `src/donnees.py`) pour lire le fichier CSV par morceaux et économiser la mémoire.

## Documentation consultée
1. pandas : documentation sur `read_csv` et la manipulation de DataFrame.
2. scikit-learn : guides sur `RandomForestClassifier`, `Pipeline` et `ColumnTransformer`.
3. Matplotlib : intégration dans Tkinter avec `FigureCanvasTkAgg`.

## Équipe
| Nom | Matricule | Courriel personnel |
|---|---|---|
|Kate Eliora Yoboue |2537234| keyorawork@gmail.com |
|Mohamed Kassi-Lahlou|2431989| kassilahloumohamed@gmail.com |
