import os
import json
from typing import Any, Dict, List, Optional, Tuple
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

try:
    from donnees import JeuDeDonnees, VariableCategorielle, VariableNumerique
    from exceptions import ModeleNonChargeError
except ImportError:
    from src.donnees import JeuDeDonnees, VariableCategorielle, VariableNumerique
    from src.exceptions import ModeleNonChargeError


def calculer_exactitude_numpy(y_vrai: np.ndarray, y_pred: np.ndarray) -> float:
    """Calcul vectorisé de l'exactitude avec numpy."""
    if len(y_vrai) != len(y_pred):
        raise ValueError("Les tableaux doivent avoir la même taille.")
    return float(np.mean(y_vrai == y_pred))


class ModelePredictif:
    """Entraîne et gère le modèle de classification."""

    def __init__(self, jeu_donnees: Optional[JeuDeDonnees] = None):
        self._jeu_donnees = jeu_donnees
        self._pipeline: Optional[Pipeline] = None
        self._classes: List[str] = []
        self._metadonnees: Dict[str, Any] = {}
        self._score_test: float = 0.0
        self._score_reference: float = 0.0

    @property
    def classes(self) -> List[str]:
        return list(self._classes)

    @property
    def score_test(self) -> float:
        return self._score_test

    @property
    def score_reference(self) -> float:
        return self._score_reference

    @property
    def est_charge(self) -> bool:
        return self._pipeline is not None

    def entrainer(self, test_size: float = 0.20, random_state: int = 42) -> Dict[str, float]:
        """Entraîne la forêt aléatoire et calcule les scores."""
        if self._jeu_donnees is None:
            raise ModeleNonChargeError("Pas de jeu de données pour l'entraînement.")

        X, y = self._jeu_donnees.extraire_caracteristiques_et_cible()

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

        cols_num = [nom for nom, var in self._jeu_donnees.variables.items() if isinstance(var, VariableNumerique)]
        cols_cat = [nom for nom, var in self._jeu_donnees.variables.items() if isinstance(var, VariableCategorielle)]

        preprocesseur = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), cols_num),
                ("cat", OneHotEncoder(handle_unknown="ignore"), cols_cat),
            ]
        )

        self._pipeline = Pipeline(
            steps=[
                ("pre", preprocesseur),
                ("clf", RandomForestClassifier(n_estimators=100, max_depth=12, random_state=random_state)),
            ]
        )

        self._pipeline.fit(X_train, y_train)

        y_pred = self._pipeline.predict(X_test)
        self._score_test = calculer_exactitude_numpy(y_test.to_numpy(), y_pred)

        dummy = DummyClassifier(strategy="most_frequent")
        dummy.fit(X_train, y_train)
        y_dummy = dummy.predict(X_test)
        self._score_reference = calculer_exactitude_numpy(y_test.to_numpy(), y_dummy)

        clf_step = self._pipeline.named_steps["clf"]
        self._classes = list(clf_step.classes_)

        self._metadonnees = {
            "score_test": round(self._score_test, 4),
            "score_reference": round(self._score_reference, 4),
            "classes": self._classes,
            "colonnes_numeriques": cols_num,
            "colonnes_categorielles": cols_cat,
        }

        return {"score_test": self._score_test, "score_reference": self._score_reference}

    def sauvegarder(self, chemin_modele: str, chemin_metadata: str) -> None:
        if self._pipeline is None:
            raise ModeleNonChargeError("Le modèle n'est pas encore entraîné.")

        os.makedirs(os.path.dirname(os.path.abspath(chemin_modele)), exist_ok=True)
        joblib.dump(self._pipeline, chemin_modele)

        with open(chemin_metadata, "w", encoding="utf-8") as f:
            json.dump(self._metadonnees, f, indent=2, ensure_ascii=False)

    def charger(self, chemin_modele: str, chemin_metadata: str) -> None:
        if not os.path.exists(chemin_modele):
            raise ModeleNonChargeError(f"Modèle introuvable : {chemin_modele}")
        if not os.path.exists(chemin_metadata):
            raise ModeleNonChargeError(f"Métadonnées introuvables : {chemin_metadata}")

        self._pipeline = joblib.load(chemin_modele)
        with open(chemin_metadata, "r", encoding="utf-8") as f:
            self._metadonnees = json.load(f)

        self._classes = self._metadonnees.get("classes", [])
        self._score_test = float(self._metadonnees.get("score_test", 0.0))
        self._score_reference = float(self._metadonnees.get("score_reference", 0.0))

    def predire(self, caracteristiques: Dict[str, Any]) -> Tuple[str, Dict[str, float]]:
        if self._pipeline is None:
            raise ModeleNonChargeError("Le modèle n'est pas chargé.")

        df_entree = pd.DataFrame([caracteristiques])
        prediction = str(self._pipeline.predict(df_entree)[0])

        probas_liste = self._pipeline.predict_proba(df_entree)[0]
        dico_probas = {cls: float(p) for cls, p in zip(self._classes, probas_liste)}

        return prediction, dico_probas
