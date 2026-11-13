# Script pour générer le jeu de données du quiz (3 000 participants)

import os
import random
import numpy as np
import pandas as pd

np.random.seed(42)
random.seed(42)

QUESTIONS = {
    "q_organisation": {
        "domaine": "Organisation",
        "enonce": "Quand tu as plusieurs trucs à faire dans ta journée, tu t'y prends comment ?",
        "choix": {
            "priorites_urgentes": 0.48,
            "ordre_chronologique": 0.34,
            "selon_inspiration": 0.18
        }
    },
    "q_conflit": {
        "domaine": "Relationnel",
        "enonce": "Quand il y a une tension ou un désaccord avec un proche, tu as plutôt tendance à :",
        "choix": {
            "discussion_immediate": 0.46,
            "laisser_reposer": 0.38,
            "message_ecrit": 0.16
        }
    },
    "q_decision": {
        "domaine": "Décision",
        "enonce": "Avant de faire un choix important (acheter un ordi, choisir un cours, etc.) :",
        "choix": {
            "comparer_avis": 0.56,
            "avis_entourage": 0.28,
            "coup_de_coeur": 0.16
        }
    },
    "q_concentration": {
        "domaine": "Travail",
        "enonce": "Pour réviser ou bosser sur un projet pendant plusieurs heures :",
        "choix": {
            "musique_fond": 0.52,
            "silence_absolu": 0.33,
            "musique_paroles": 0.15
        }
    },
    "q_weekend": {
        "domaine": "Vie sociale",
        "enonce": "Après une grosse semaine de cours ou de boulot, ton vendredi soir idéal :",
        "choix": {
            "petit_comite": 0.54,
            "soiree_groupe": 0.27,
            "chill_solo": 0.19
        }
    },
    "q_reveil": {
        "domaine": "Quotidien",
        "enonce": "Quand ton alarme sonne le matin en semaine :",
        "choix": {
            "snooze_court": 0.51,
            "lever_direct": 0.36,
            "reveil_naturel": 0.13
        }
    },
    "q_franchise": {
        "domaine": "Philosophie",
        "enonce": "Un ami te demande ton avis sincère sur un projet ou une tenue qui ne lui va pas trop :",
        "choix": {
            "tact_positif": 0.58,
            "franchise_directe": 0.29,
            "question_miroir": 0.13
        }
    },
    "q_imprevu": {
        "domaine": "Imprévus",
        "enonce": "Si une sortie prévue depuis longtemps est annulée 30 minutes avant :",
        "choix": {
            "remplacement_rapide": 0.45,
            "soulagement_repos": 0.38,
            "petite_deception": 0.17
        }
    }
}


def calculer_points_rarete(cle_question: str, choix: str) -> float:
    p = QUESTIONS[cle_question]["choix"].get(choix, 0.5)
    return round((1.0 - p) * 100, 1)


def determiner_archetype(score_total: float, nb_rares: int) -> str:
    if score_total >= 64.0 or nb_rares >= 3:
        return "Profil Spontané & Intuitif"
    elif score_total <= 56.5 and nb_rares <= 1:
        return "Profil Structuré & Collectif"
    else:
        return "Profil Équilibré & Pragmatique"


def generer_echantillon(n: int = 3000) -> pd.DataFrame:
    lignes = []
    types_participants = np.random.choice([0, 1, 2], size=n, p=[0.48, 0.36, 0.16])

    for i, t in enumerate(types_participants):
        reponses = {}
        points_par_domaine = {
            "Organisation": [], "Relationnel": [], "Décision": [], "Travail": [],
            "Vie sociale": [], "Quotidien": [], "Philosophie": [], "Imprévus": []
        }
        nb_rares = 0

        for q_nom, q_info in QUESTIONS.items():
            choix_noms = list(q_info["choix"].keys())
            probas_base = np.array(list(q_info["choix"].values()))

            if t == 0:
                poids = probas_base ** 1.6
            elif t == 2:
                poids = (1.05 - probas_base) ** 1.6
            else:
                poids = probas_base

            poids = poids / poids.sum()
            choix_fait = np.random.choice(choix_noms, p=poids)
            reponses[q_nom] = choix_fait

            pts = calculer_points_rarete(q_nom, choix_fait)
            points_par_domaine[q_info["domaine"]].append(pts)
            if pts >= 75:
                nb_rares += 1

        s_methode = round(float(np.mean([points_par_domaine["Organisation"][0], points_par_domaine["Travail"][0]])), 1)
        s_relations = round(float(np.mean([points_par_domaine["Relationnel"][0], points_par_domaine["Vie sociale"][0]])), 1)
        s_choix = round(float(np.mean([points_par_domaine["Décision"][0], points_par_domaine["Imprévus"][0]])), 1)
        s_quotidien = round(float(np.mean([points_par_domaine["Quotidien"][0], points_par_domaine["Philosophie"][0]])), 1)

        score_total = round(float(np.mean([s_methode, s_relations, s_choix, s_quotidien])), 1)
        cible = determiner_archetype(score_total + np.random.normal(0, 1.2), nb_rares)

        ligne = {
            "id_repondant": i + 1,
            **reponses,
            "score_methode": s_methode,
            "score_relations": s_relations,
            "score_choix": s_choix,
            "score_quotidien": s_quotidien,
            "score_total_rarete": score_total,
            "choix_originaux": nb_rares,
            "cible_archetype": cible
        }
        lignes.append(ligne)

    return pd.DataFrame(lignes)


if __name__ == "__main__":
    dossier = os.path.join(os.path.dirname(os.path.abspath(__file__)), "donnees")
    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, "etes_vous_special.csv")
    df = generer_echantillon(3000)
    df.to_csv(chemin, index=False, encoding="utf-8")
    print(f"Dataset créé : {chemin}")
