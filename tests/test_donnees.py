import pytest

from donnees import verifier_fichier_existe
from exceptions import DonneeInvalideError


def test_fichier_existant(tmp_path):
    fichier = tmp_path / "exemple.csv"
    fichier.write_text("a,b\n1,2\n")
    assert verifier_fichier_existe(str(fichier)) == str(fichier)


def test_fichier_introuvable():
    with pytest.raises(DonneeInvalideError):
        verifier_fichier_existe("n_existe_pas.csv")
