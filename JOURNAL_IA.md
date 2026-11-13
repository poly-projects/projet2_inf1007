# Journal d'Utilisation de l'IA — Projet 2 (INF1007)

**Équipe :** Mohamed Kassi-Lahlou & Kate Eliora Yoboue  
**Projet :** « Êtes-vous spécial ? »  
**Cours :** INF1007 — Polytechnique Montréal  

---

| Outil | Question posée | Réponse reçue | Vérification faite | Décision finale |
| :--- | :--- | :--- | :--- | :--- |
| **ChatGPT** | "Comment intégrer un graphique Matplotlib dans une fenêtre Tkinter en mode sombre ?" | L'IA a proposé `plt.show()` ou de recharger la fenêtre complète à chaque fois. | En testant, la fenêtre clignotait et les anciens tracés se superposaient. | **Modifié** : Utilisation de `FigureCanvasTkAgg` avec un `Figure` propre et mise à jour ciblée dans le frame parent. |
| **GitHub Copilot** | "Comment calculer le score de rareté de manière vectorisée avec NumPy ?" | Copilot proposait une boucle `for` avec un compteur d'éléments. | Le cours (Chapitre 12) demande d'utiliser le broadcast sans boucle for. | **Rejeté et réécrit** : Utilisation directe de `np.mean(y_vrai == y_pred)` avec validation par les tests pytest. |
| **ChatGPT** | "Proposer une structure pour les classes de variables." | L'IA avait fait un seul gros fichier sans héritage avec plein de `if/else`. | La consigne demande de la POO avec des classes spécialisées. | **Rejeté** : Création d'une classe de base `Variable` et de sous-classes `VariableNumerique` et `VariableCategorielle` avec leur propre méthode `valider()`. |
| **Claude** | "Idée de modèle simple pour classer 3 profils d'utilisateurs." | L'IA a proposé un réseau de neurones avec plusieurs couches cachées. | Le cours demande un modèle classique simple de scikit-learn. | **Rejeté** : Choix d'une Forêt Aléatoire (*RandomForestClassifier*) avec comparaison à un *DummyClassifier*. |
