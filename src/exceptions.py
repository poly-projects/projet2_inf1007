# Exceptions du projet

class ErreurEtesVousSpecial(Exception):
    """Exception de base."""
    pass


class DonneeInvalideError(ErreurEtesVousSpecial):
    """Pour les valeurs invalides ou hors bornes."""
    pass


class ReponseInvalideError(DonneeInvalideError):
    """Pour une réponse qui ne fait pas partie des options."""
    pass


class FichierDonneesIntrouvableError(ErreurEtesVousSpecial):
    """Si le fichier csv ou le modèle est introuvable."""
    pass


class ModeleNonChargeError(ErreurEtesVousSpecial):
    """Si on appelle predict sans avoir chargé le modèle."""
    pass
