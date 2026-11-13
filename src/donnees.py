import os
import csv
from typing import Dict, List, Tuple, Any
import pandas as pd

try:
    from exceptions import (
        DonneeInvalideError,
        FichierDonneesIntrouvableError,
        ReponseInvalideError
    )
except ImportError:
    from src.exceptions import (
        DonneeInvalideError,
        FichierDonneesIntrouvableError,
        ReponseInvalideError
    )


def verifier_fichier_existe(chemin: str) -> str:
    """Vérifie qu'un fichier existe avant de l'ouvrir."""
    if not os.path.isfile(chemin):
        raise DonneeInvalideError(f"Fichier introuvable : {chemin}")
    return chemin


def lire_lignes_blocs(chemin_csv: str, taille_bloc: int = 100):
    """Lit le fichier csv par morceaux avec yield pour pas tout charger d'un coup."""
    if not os.path.exists(chemin_csv):
        raise FichierDonneesIntrouvableError(f"Fichier introuvable : {chemin_csv}")

    with open(chemin_csv, mode="r", encoding="utf-8") as f:
        lecteur = csv.DictReader(f)
        bloc = []
        for ligne in lecteur:
            bloc.append(ligne)
            if len(bloc) >= taille_bloc:
                yield bloc
                bloc = []
        if bloc:
            yield bloc


class Variable:
    """Classe de base pour une variable."""

    def __init__(self, nom: str, description: str, type_var: str):
        self.nom = nom
        self.description = description
        self.type_var = type_var

    def valider(self, valeur: Any) -> Any:
        return valeur


class VariableNumerique(Variable):
    """Variable numérique avec bornes min et max."""

    def __init__(self, nom: str, description: str, min_val: float = 0.0, max_val: float = 100.0, est_entier: bool = False):
        super().__init__(nom, description, "numerique")
        self.min_val = float(min_val)
        self.max_val = float(max_val)
        self.est_entier = est_entier

    def valider(self, valeur: Any) -> float:
        if valeur is None or str(valeur).strip() == "":
            raise DonneeInvalideError(f"La valeur de '{self.description}' est vide.")

        try:
            nombre = float(valeur)
        except (ValueError, TypeError):
            raise DonneeInvalideError(f"'{valeur}' n'est pas un nombre valide pour '{self.description}'.")

        if nombre < self.min_val or nombre > self.max_val:
            raise DonneeInvalideError(
                f"Valeur {nombre} hors bornes ({self.min_val} à {self.max_val}) pour '{self.description}'."
            )

        return int(nombre) if self.est_entier else nombre


class VariableCategorielle(Variable):
    """Variable texte avec choix prédéfinis."""

    def __init__(self, nom: str, description: str, choix_possibles: List[str]):
        super().__init__(nom, description, "categorielle")
        self.choix_possibles = [c.lower() for c in choix_possibles]

    def valider(self, valeur: Any) -> str:
        if valeur is None:
            raise ReponseInvalideError(f"La réponse pour '{self.description}' est vide.")

        texte = str(valeur).strip().lower()
        if texte not in self.choix_possibles:
            raise ReponseInvalideError(
                f"Option '{texte}' invalide pour '{self.description}'. Choix possibles : {self.choix_possibles}."
            )
        return texte


class QuestionQuiz:
    """Stocke l'énoncé d'une question et les proportions de chaque réponse."""

    def __init__(
        self,
        identifiant: str,
        domaine: str,
        enonce: str,
        options: Dict[str, Tuple[str, float]]
    ):
        self.identifiant = identifiant
        self.domaine = domaine
        self.enonce = enonce
        self.options = options

    def calculer_points_rarete(self, cle_choix: str) -> float:
        """Calcule les points selon la rareté du choix."""
        if cle_choix not in self.options:
            raise ReponseInvalideError(f"Option inconnue : '{cle_choix}'")
        _, proportion = self.options[cle_choix]
        return round((1.0 - proportion) * 100, 1)

    def obtenir_pourcentage_population(self, cle_choix: str) -> int:
        if cle_choix not in self.options:
            return 0
        _, proportion = self.options[cle_choix]
        return int(round(proportion * 100))


# Liste des 8 questions du quiz
QUESTIONS_DU_JEU: List[QuestionQuiz] = [
    QuestionQuiz(
        identifiant="q_organisation",
        domaine="Méthode & Organisation",
        enonce="Quand tu as plusieurs trucs à faire dans ta journée, tu t'y prends comment ?",
        options={
            "priorites_urgentes": ("Je commence par le plus urgent ou difficile pour m'en débarrasser", 0.48),
            "ordre_chronologique": ("Je fais les choses dans l'ordre où elles arrivent, calmement", 0.34),
            "selon_inspiration": ("Je choisis selon mon énergie et mon envie du moment pour être efficace", 0.18),
        }
    ),
    QuestionQuiz(
        identifiant="q_conflit",
        domaine="Relations & Communication",
        enonce="Quand il y a une petite tension ou un désaccord avec un proche :",
        options={
            "discussion_immediate": ("J'en parle tout de suite posément en face à face pour crever l'abcès", 0.46),
            "laisser_reposer": ("J'attends le lendemain que tout le monde ait la tête froide pour en discuter", 0.38),
            "message_ecrit": ("J'envoie un message bien rédigé pour expliquer clairement ce que je ressens", 0.16),
        }
    ),
    QuestionQuiz(
        identifiant="q_decision",
        domaine="Prise de décision",
        enonce="Avant de faire un choix important (acheter un ordi, choisir un cours, etc.) :",
        options={
            "comparer_avis": ("Je regarde plusieurs comparatifs et avis en ligne pour vérifier", 0.56),
            "avis_entourage": ("Je demande conseil à des amis ou à des proches qui s'y connaissent", 0.28),
            "coup_de_coeur": ("Je fais confiance à mon intuition et à ma première impression", 0.16),
        }
    ),
    QuestionQuiz(
        identifiant="q_concentration",
        domaine="Environnement de travail",
        enonce="Pour réviser ou bosser sur un projet pendant quelques heures :",
        options={
            "musique_fond": ("Une musique douce, instrumentale ou des bruits d'ambiance en fond", 0.52),
            "silence_absolu": ("Le silence complet, besoin de calme absolu sans distraction", 0.33),
            "musique_paroles": ("Ma musique préférée habituelle, ça me motive et me donne du rythme", 0.15),
        }
    ),
    QuestionQuiz(
        identifiant="q_weekend",
        domaine="Temps libre & Social",
        enonce="Après une grosse semaine de cours ou de travail, ton vendredi soir idéal :",
        options={
            "petit_comite": ("Une soirée sympa à la maison avec 2 ou 3 amis proches", 0.54),
            "soiree_groupe": ("Une grande soirée animée, un bar ou une sortie avec du monde", 0.27),
            "chill_solo": ("Une soirée tranquille en solo (série, lecture, jeux vidéo ou repos)", 0.19),
        }
    ),
    QuestionQuiz(
        identifiant="q_reveil",
        domaine="Rythme du quotidien",
        enonce="Le matin en semaine, comment se passe ton réveil avec l'alarme ?",
        options={
            "snooze_court": ("Je repousse l'alarme une ou deux fois pour grappiller quelques minutes", 0.51),
            "lever_direct": ("Je sors du lit dès la première sonnerie pour ne pas traîner", 0.36),
            "reveil_naturel": ("Je me réveille souvent naturellement un peu avant que l'alarme ne sonne", 0.13),
        }
    ),
    QuestionQuiz(
        identifiant="q_franchise",
        domaine="Sincérité & Tact",
        enonce="Un ami te demande ton avis sincère sur une idée ou un projet pas très convaincant :",
        options={
            "tact_positif": ("Je valorise le positif d'abord, puis je suggère des pistes d'amélioration", 0.58),
            "franchise_directe": ("Je lui dis honnêtement et gentiment ce qui ne va pas pour l'aider", 0.29),
            "question_miroir": ("Je lui demande d'abord comment lui le sent avant de donner mon avis", 0.13),
        }
    ),
    QuestionQuiz(
        identifiant="q_imprevu",
        domaine="Gestion des imprévus",
        enonce="Si un plan sympa prévu ce soir est annulé au dernier moment :",
        options={
            "remplacement_rapide": ("Je trouve vite une autre activité ou je propose un plan B", 0.45),
            "soulagement_repos": ("Ça m'arrange un peu secrètement, ça me libère du temps pour moi", 0.38),
            "petite_deception": ("Je suis un peu déçu(e) sur le coup car j'avais calé ma journée dessus", 0.17),
        }
    )
]


class JeuDeDonnees:
    """Classe pour charger et préparer les données du csv."""

    def __init__(self, chemin_csv: str):
        self.chemin_csv = chemin_csv
        self._df: pd.DataFrame = pd.DataFrame()
        self.variables: Dict[str, Variable] = self._initialiser_variables()

    def _initialiser_variables(self) -> Dict[str, Variable]:
        vars_dict: Dict[str, Variable] = {}
        for q in QUESTIONS_DU_JEU:
            vars_dict[q.identifiant] = VariableCategorielle(
                nom=q.identifiant,
                description=q.enonce,
                choix_possibles=list(q.options.keys())
            )

        vars_dict["score_methode"] = VariableNumerique("score_methode", "Méthode", 0.0, 100.0)
        vars_dict["score_relations"] = VariableNumerique("score_relations", "Relations", 0.0, 100.0)
        vars_dict["score_choix"] = VariableNumerique("score_choix", "Choix", 0.0, 100.0)
        vars_dict["score_quotidien"] = VariableNumerique("score_quotidien", "Quotidien", 0.0, 100.0)
        vars_dict["score_total_rarete"] = VariableNumerique("score_total_rarete", "Score Global", 0.0, 100.0)
        vars_dict["choix_originaux"] = VariableNumerique("choix_originaux", "Choix Originaux", 0.0, 10.0, est_entier=True)
        return vars_dict

    def charger(self) -> pd.DataFrame:
        if not os.path.exists(self.chemin_csv):
            raise FichierDonneesIntrouvableError(f"Fichier inexistant : {self.chemin_csv}")

        self._df = pd.read_csv(self.chemin_csv)

        colonnes_attendues = list(self.variables.keys()) + ["cible_archetype"]
        manquantes = [c for c in colonnes_attendues if c not in self._df.columns]
        if manquantes:
            raise DonneeInvalideError(f"Colonnes manquantes : {manquantes}")

        self._df = self._df.dropna(subset=colonnes_attendues).copy()
        return self._df

    def extraire_caracteristiques_et_cible(self) -> Tuple[pd.DataFrame, pd.Series]:
        if self._df.empty:
            self.charger()

        cols_x = list(self.variables.keys())
        X = self._df[cols_x].copy()
        y = self._df["cible_archetype"].copy()
        return X, y
