import os
import pytest

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
    from donnees import (
        VariableNumerique,
        VariableCategorielle,
        QuestionQuiz,
        JeuDeDonnees,
        lire_lignes_blocs,
        verifier_fichier_existe,
        QUESTIONS_DU_JEU
    )
    from exceptions import (
        DonneeInvalideError,
        ReponseInvalideError,
        FichierDonneesIntrouvableError
    )
except ImportError:
    from src.donnees import (
        VariableNumerique,
        VariableCategorielle,
        QuestionQuiz,
        JeuDeDonnees,
        lire_lignes_blocs,
        verifier_fichier_existe,
        QUESTIONS_DU_JEU
    )
    from src.exceptions import (
        DonneeInvalideError,
        ReponseInvalideError,
        FichierDonneesIntrouvableError
    )


# Tests de vérification du fichier
def test_fichier_existant(tmp_path):
    fichier = tmp_path / "exemple.csv"
    fichier.write_text("a,b\n1,2\n")
    assert verifier_fichier_existe(str(fichier)) == str(fichier)


def test_fichier_introuvable():
    with pytest.raises(DonneeInvalideError):
        verifier_fichier_existe("n_existe_pas.csv")


# Tests pour VariableNumerique
def test_variable_numerique_cas_usuel():
    var = VariableNumerique("score_methode", "Score Méthode", min_val=0.0, max_val=100.0)
    assert var.valider("65.5") == pytest.approx(65.5)
    assert var.valider(80) == pytest.approx(80.0)


def test_variable_numerique_cas_limites():
    var = VariableNumerique("score_total", "Score Global", min_val=0.0, max_val=100.0)
    assert var.valider(0.0) == pytest.approx(0.0)
    assert var.valider(100.0) == pytest.approx(100.0)


def test_variable_numerique_erreur_hors_bornes():
    var = VariableNumerique("score_relations", "Score Relations", min_val=0.0, max_val=100.0)
    with pytest.raises(DonneeInvalideError):
        var.valider(105.0)


def test_variable_numerique_erreur_texte():
    var = VariableNumerique("score_choix", "Score Choix", min_val=0.0, max_val=100.0)
    with pytest.raises(DonneeInvalideError):
        var.valider("pas_un_nombre")


def test_variable_numerique_erreur_vide():
    var = VariableNumerique("score_quotidien", "Score Quotidien", min_val=0.0, max_val=100.0)
    with pytest.raises(DonneeInvalideError):
        var.valider("")


# Tests pour VariableCategorielle
def test_variable_categorielle_cas_usuel():
    var = VariableCategorielle("orga", "Organisation", ["priorites_urgentes", "ordre_chronologique", "selon_inspiration"])
    assert var.valider("PRIORITES_URGENTES") == "priorites_urgentes"
    assert var.valider("selon_inspiration") == "selon_inspiration"


def test_variable_categorielle_erreur_choix_invalide():
    var = VariableCategorielle("conflit", "Gestion Conflit", ["discussion_immediate", "laisser_reposer", "message_ecrit"])
    with pytest.raises(ReponseInvalideError):
        var.valider("choix_qui_existe_pas")


# Tests pour QuestionQuiz
def test_question_quiz_calcul_points():
    q = QUESTIONS_DU_JEU[0]
    pts_majoritaire = q.calculer_points_rarete("priorites_urgentes")
    pts_rare = q.calculer_points_rarete("selon_inspiration")
    assert pts_rare > pts_majoritaire
    assert pts_rare == pytest.approx(82.0)


def test_question_quiz_erreur_option_inconnue():
    q = QUESTIONS_DU_JEU[0]
    with pytest.raises(ReponseInvalideError):
        q.calculer_points_rarete("option_inconnue")


# Tests pour JeuDeDonnees
def test_jeu_donnees_chargement_et_dimensions():
    chemin = _trouver_csv()
    jeu = JeuDeDonnees(chemin)
    df = jeu.charger()
    assert len(df) == 3000
    assert "cible_archetype" in df.columns


def test_jeu_donnees_fichier_inexistant():
    jeu = JeuDeDonnees("fichier_qui_n_existe_pas.csv")
    with pytest.raises(FichierDonneesIntrouvableError):
        jeu.charger()


def test_generateur_blocs_yield():
    chemin = _trouver_csv()
    generateur = lire_lignes_blocs(chemin, taille_bloc=50)
    premier_bloc = next(generateur)
    assert len(premier_bloc) == 50
    assert isinstance(premier_bloc[0], dict)
