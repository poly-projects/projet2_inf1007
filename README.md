# Projet 2 INF1007 : de la donnée à l'application

*(Titre et description à compléter : domaine, ce que fait l'application.)*

## Jeu de données
- Source : 
- Licence : 
- Fichier : `donnees/` *(25 Mo maximum, sinon lien de téléchargement ici)*

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
Couverture mesurée : *(à compléter)*

## Résultat du modèle
Métrique : *(à compléter)* · Référence : *(à compléter)*

## Structure du code
- `src/donnees.py` : lecture, nettoyage, classes de variables
- `src/modele.py` : entraînement, évaluation, prédiction
- `src/exceptions.py` : exceptions personnalisées
- `src/interface.py` : interface graphique
- `src/main.py` : point d'entrée
- `tests/` : tests pytest

## Outil du chapitre 7 utilisé
*(à compléter en une phrase : décorateur, générateur ou lambda)*

## Documentation consultée
1. pandas : *(page)*
2. scikit-learn : *(page)*
3. Interface : *(page)*

## Équipe
| Nom | Matricule | Courriel personnel |
|---|---|---|
|Kate Eliora Yoboue |2537234| keyorawork@gmail.com |
|Mohamed Kassi Lahou|2431989| kassilahloumohamed@gmail.com |