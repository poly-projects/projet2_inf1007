import os
import sys
import tkinter as tk

try:
    from donnees import JeuDeDonnees
    from modele import ModelePredictif
    from interface import ApplicationEtesVousSpecial
except ImportError:
    from src.donnees import JeuDeDonnees
    from src.modele import ModelePredictif
    from src.interface import ApplicationEtesVousSpecial


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(script_dir) == "src":
        base_dir = os.path.dirname(script_dir)
    else:
        base_dir = script_dir

    chemin_csv = os.path.join(base_dir, "donnees", "etes_vous_special.csv")
    chemin_modele = os.path.join(base_dir, "modeles", "modele_special.joblib")
    chemin_metadata = os.path.join(base_dir, "modeles", "metadata_special.json")

    # Si le modèle n'existe pas encore, on l'entraîne
    if not os.path.exists(chemin_modele) or not os.path.exists(chemin_metadata):
        print("Entraînement du modèle...")
        jeu = JeuDeDonnees(chemin_csv)
        modele = ModelePredictif(jeu)
        scores = modele.entrainer(test_size=0.20, random_state=42)
        modele.sauvegarder(chemin_modele, chemin_metadata)
        print(f"Modèle prêt (exactitude : {scores['score_test'] * 100:.1f} %)")

    # Option pour juste tester sans ouvrir la fenêtre
    if "--train" in sys.argv:
        return

    # Lancement de l'application
    racine = tk.Tk()
    app = ApplicationEtesVousSpecial(racine, chemin_modele, chemin_metadata)
    racine.mainloop()


if __name__ == "__main__":
    main()
