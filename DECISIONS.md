# Fiche de Décisions — Projet 2 (INF1007)

**Équipe :** Mohamed Kassi-Lahlou & Kate Eliora Yoboue  
**Projet :** « Êtes-vous spécial ? »  
**Cours :** INF1007 — Polytechnique Montréal  

---

| Étape | Options envisagées | Choix retenu |
| :--- | :--- | :--- |
| **Domaine d'application** | Prédiction de prix, météo, jeu de quiz | **Quiz de décision du quotidien** : plus interactif et engageant pour un utilisateur. |
| **Jeu de données** | Datasets publics Kaggle, données simulées | **Échantillon de sondage (3 000 entrées)** : variables mixtes (choix de texte et scores numériques), sans données personnelles. |
| **Cible et métrique** | Régression sur le score, classification d'archétypes | **Classification en 3 profils** (*Spontané & Intuitif*, *Équilibré & Pragmatique*, *Structuré & Collectif*). Métrique : exactitude calculée avec numpy sans boucle for. |
| **Modèle IA** | Arbre unique, régression logistique, forêt aléatoire | **Forêt aléatoire (Random Forest)** : bon compromis entre simplicité et précision (88.5 % d'exactitude contre 40.0 % pour la baseline). |
| **Interface graphique** | Ligne de commande, web Streamlit, Tkinter | **Tkinter avec Matplotlib** : fonctionne en local sans serveur web, interface sobre en thème sombre. |
| **Gestion des erreurs** | Code de retour, exceptions de base | **Exceptions personnalisées** (`DonneeInvalideError`, `ReponseInvalideError`) pour intercepter les erreurs sans planter. |
| **Architecture logicielle** | Monofichier, architecture par modules POO | **Modules séparés** (`donnees.py`, `modele.py`, `interface.py`, `exceptions.py`) avec POO simple et héritage de classes. |
