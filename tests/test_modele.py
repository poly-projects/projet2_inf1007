import os
import numpy as np
import pytest
from sklearn.metrics import accuracy_score

def _trouver_csv():
    d = os.path.dirname(os.path.abspath(__file__))
    candidats = [
        os.path.join(os.path.dirname(d), "donnees", "etes_vous_special.csv"),
        os.path.join(d, "donnees", "etes_vous_special.csv")
    ]
    for c in candidats:
        if os.path.exists(c):
            return c
    return candidats[0]

try:
    from donnees import JeuDeDonnees
    from exceptions import ModeleNonChargeError
    from modele import ModelePredictif, calculer_exactitude_numpy
except ImportError:
    from src.donnees import JeuDeDonnees
    from src.exceptions import ModeleNonChargeError
    from src.modele import ModelePredictif, calculer_exactitude_numpy


# Tests du calcul d'exactitude numpy
def test_calcul_exactitude_numpy_identique_a_sklearn():
    y_vrai = np.array(["Profil Spontané & Intuitif", "Profil Structuré & Collectif", "Profil Équilibré & Pragmatique", "Profil Spontané & Intuitif"])
    y_pred = np.array(["Profil Spontané & Intuitif", "Profil Équilibré & Pragmatique", "Profil Équilibré & Pragmatique", "Profil Spontané & Intuitif"])

    score_numpy = calculer_exactitude_numpy(y_vrai, y_pred)
    score_sklearn = accuracy_score(y_vrai, y_pred)

    assert score_numpy == pytest.approx(score_sklearn)
    assert score_numpy == pytest.approx(0.75)


def test_calcul_exactitude_numpy_erreur_dimensions():
    with pytest.raises(ValueError):
        calculer_exactitude_numpy(np.array([1, 2, 3]), np.array([1, 2]))


# Tests pour ModelePredictif
@pytest.fixture(scope="module")
def modele_entraine():
    chemin_csv = _trouver_csv()
    jeu = JeuDeDonnees(chemin_csv)
    modele = ModelePredictif(jeu)
    modele.entrainer(test_size=0.20, random_state=42)
    return modele


def test_modele_surpasse_baseline_dummy(modele_entraine):
    assert modele_entraine.score_test >= 0.80
    assert modele_entraine.score_test > modele_entraine.score_reference
    assert modele_entraine.score_reference > 0.30


def test_modele_prediction_unitaire(modele_entraine):
    profil_test = {
        "q_organisation": "selon_inspiration",
        "q_conflit": "message_ecrit",
        "q_decision": "coup_de_coeur",
        "q_concentration": "musique_paroles",
        "q_weekend": "chill_solo",
        "q_reveil": "reveil_naturel",
        "q_franchise": "question_miroir",
        "q_imprevu": "petite_deception",
        "score_methode": 83.5,
        "score_relations": 82.5,
        "score_choix": 83.5,
        "score_quotidien": 87.0,
        "score_total_rarete": 84.1,
        "choix_originaux": 8
    }

    prediction, dico_probas = modele_entraine.predire(profil_test)
    assert prediction in modele_entraine.classes
    assert sum(dico_probas.values()) == pytest.approx(1.0, abs=1e-3)


def test_modele_non_charge_leve_exception():
    modele_vierge = ModelePredictif()
    with pytest.raises(ModeleNonChargeError):
        modele_vierge.predire({"score_methode": 50})
