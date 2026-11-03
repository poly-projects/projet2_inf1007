"""Lecture, nettoyage des données et classes de variables.

À compléter : lecture du CSV (pandas), nettoyage, classes Variable /
VariableNumerique / VariableCategorielle (chapitres 9 à 11).
"""
import os

from exceptions import DonneeInvalideError


def verifier_fichier_existe(chemin: str) -> str:
    """Vérifie qu'un fichier existe avant de l'ouvrir.

    Reçoit : le chemin du fichier (str).
    Renvoie : le même chemin, si le fichier existe.
    Échoue : DonneeInvalideError si le fichier est introuvable.
    """
    if not os.path.isfile(chemin):
        raise DonneeInvalideError(f"Fichier introuvable : {chemin}")
    return chemin
