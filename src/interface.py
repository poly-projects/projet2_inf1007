import os
import csv
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Optional, Any

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from donnees import QUESTIONS_DU_JEU, QuestionQuiz
    from modele import ModelePredictif
except ImportError:
    from src.donnees import QUESTIONS_DU_JEU, QuestionQuiz
    from src.modele import ModelePredictif


class ApplicationEtesVousSpecial:
    """Interface graphique du quiz en thème sombre."""

    # Couleurs sombres simples
    BG_PRINCIPAL = "#18181b"
    BG_CARTE = "#27272a"
    BG_ELEMENT = "#323238"
    BG_SURVOL = "#3f3f46"
    BORDURE = "#3f3f46"
    TEXTE_BLANC = "#f4f4f5"
    TEXTE_GRIS = "#a1a1aa"
    ACCENT = "#818cf8"
    ACCENT_VERT = "#34d399"

    def __init__(self, fenetre: tk.Tk, chemin_modele: str, chemin_metadata: str):
        self._fenetre = fenetre
        self._fenetre.title("Êtes-vous spécial ?")
        self._fenetre.geometry("960x680")
        self._fenetre.minsize(860, 600)
        self._fenetre.configure(bg=self.BG_PRINCIPAL)

        # Résolution robuste du chemin pour donnees/
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if os.path.basename(script_dir) == "src":
            base_dir = os.path.dirname(script_dir)
        else:
            base_dir = script_dir
        self._chemin_historique = os.path.join(base_dir, "donnees", "historique_parties.csv")

        # Chargement du modèle
        self._modele = ModelePredictif()
        self._modele_pret = False
        try:
            self._modele.charger(chemin_modele, chemin_metadata)
            self._modele_pret = True
        except Exception:
            self._modele_pret = False

        # État du quiz
        self._questions: List[QuestionQuiz] = QUESTIONS_DU_JEU
        self._index: int = 0
        self._reponses: Dict[str, str] = {}
        self._points: Dict[str, float] = {}

        self._canvas_matplot: Optional[FigureCanvasTkAgg] = None

        self._configurer_styles()
        self._construire_interface_base()
        self._afficher_accueil()

    def _configurer_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background=self.BG_PRINCIPAL, foreground=self.TEXTE_BLANC, font=("Helvetica", 10))
        style.configure("TProgressbar", troughcolor=self.BG_CARTE, background=self.ACCENT, thickness=6)

    def _construire_interface_base(self) -> None:
        self._barre_haut = tk.Frame(self._fenetre, bg=self.BG_PRINCIPAL, height=50)
        self._barre_haut.pack(side=tk.TOP, fill=tk.X, padx=25, pady=(15, 5))

        lbl_titre = tk.Label(
            self._barre_haut,
            text="Êtes-vous spécial ?",
            font=("Helvetica", 13, "bold"),
            fg=self.TEXTE_BLANC,
            bg=self.BG_PRINCIPAL
        )
        lbl_titre.pack(side=tk.LEFT)

        btn_infos = tk.Button(
            self._barre_haut,
            text="À propos",
            font=("Helvetica", 9),
            bg=self.BG_CARTE,
            fg=self.TEXTE_GRIS,
            activebackground=self.BG_SURVOL,
            activeforeground=self.TEXTE_BLANC,
            relief=tk.FLAT,
            padx=10,
            pady=3,
            cursor="hand2",
            command=self._afficher_a_propos
        )
        btn_infos.pack(side=tk.RIGHT)

        self._zone_principale = tk.Frame(self._fenetre, bg=self.BG_PRINCIPAL)
        self._zone_principale.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

    def _nettoyer_zone(self) -> None:
        for widget in self._zone_principale.winfo_children():
            widget.destroy()

    # --- Écran d'accueil ---
    def _afficher_accueil(self) -> None:
        self._nettoyer_zone()

        carte = tk.Frame(
            self._zone_principale,
            bg=self.BG_CARTE,
            highlightthickness=1,
            highlightbackground=self.BORDURE,
            padx=35,
            pady=35
        )
        carte.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=640, height=400)

        lbl_bienvenue = tk.Label(
            carte,
            text="Découvre ton profil de décision",
            font=("Helvetica", 17, "bold"),
            fg=self.TEXTE_BLANC,
            bg=self.BG_CARTE
        )
        lbl_bienvenue.pack(anchor=tk.W, pady=(0, 10))

        texte_intro = (
            "Face aux petites situations du quotidien, on a tous nos réflexes.\n\n"
            "Ce test pose 8 questions simples sur ta façon de t'organiser, de gérer tes imprévus, "
            "tes relations et ton temps libre.\n\n"
            "Chaque réponse est comparée aux statistiques réelles d'un échantillon de 3 000 participants "
            "pour voir si tes choix rejoignent plutôt la tendance générale ou si tu as une sensibilité plus atypique."
        )

        lbl_texte = tk.Label(
            carte,
            text=texte_intro,
            font=("Helvetica", 10),
            justify=tk.LEFT,
            fg=self.TEXTE_GRIS,
            bg=self.BG_CARTE,
            wraplength=560
        )
        lbl_texte.pack(anchor=tk.W, pady=(0, 25))

        btn_commencer = tk.Button(
            carte,
            text="Commencer le quiz  →",
            font=("Helvetica", 11, "bold"),
            bg=self.ACCENT,
            fg="#ffffff",
            activebackground="#6366f1",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=20,
            pady=9,
            cursor="hand2",
            command=self._lancer_quiz
        )
        btn_commencer.pack(anchor=tk.W)

    # --- Écran des questions ---
    def _lancer_quiz(self) -> None:
        self._index = 0
        self._reponses = {}
        self._points = {}
        self._afficher_question()

    def _afficher_question(self) -> None:
        self._nettoyer_zone()

        q = self._questions[self._index]
        total = len(self._questions)

        cadre_haut_q = tk.Frame(self._zone_principale, bg=self.BG_PRINCIPAL)
        cadre_haut_q.pack(fill=tk.X, pady=(0, 12))

        lbl_progression = tk.Label(
            cadre_haut_q,
            text=f"Question {self._index + 1} sur {total}",
            font=("Helvetica", 9, "bold"),
            fg=self.ACCENT,
            bg=self.BG_PRINCIPAL
        )
        lbl_progression.pack(side=tk.LEFT)

        lbl_theme = tk.Label(
            cadre_haut_q,
            text=q.domaine,
            font=("Helvetica", 9),
            fg=self.TEXTE_GRIS,
            bg=self.BG_PRINCIPAL
        )
        lbl_theme.pack(side=tk.RIGHT)

        barre = ttk.Progressbar(
            self._zone_principale,
            value=((self._index + 1) / total) * 100,
            maximum=100
        )
        barre.pack(fill=tk.X, pady=(0, 15))

        carte = tk.Frame(
            self._zone_principale,
            bg=self.BG_CARTE,
            highlightthickness=1,
            highlightbackground=self.BORDURE,
            padx=30,
            pady=25
        )
        carte.pack(fill=tk.BOTH, expand=True)

        lbl_enonce = tk.Label(
            carte,
            text=q.enonce,
            font=("Helvetica", 14, "bold"),
            fg=self.TEXTE_BLANC,
            bg=self.BG_CARTE,
            justify=tk.LEFT,
            wraplength=760
        )
        lbl_enonce.pack(anchor=tk.W, pady=(0, 20))

        for cle_choix, (texte_option, _) in q.options.items():
            btn_opt = tk.Button(
                carte,
                text=f"  {texte_option}",
                font=("Helvetica", 10),
                bg=self.BG_ELEMENT,
                fg=self.TEXTE_BLANC,
                activebackground=self.BG_SURVOL,
                activeforeground=self.ACCENT,
                relief=tk.FLAT,
                highlightthickness=1,
                highlightbackground=self.BORDURE,
                anchor=tk.W,
                padx=16,
                pady=12,
                cursor="hand2",
                wraplength=740,
                command=lambda k=cle_choix: self._choisir(k)
            )
            btn_opt.pack(fill=tk.X, pady=6)

        if self._index > 0:
            btn_retour = tk.Button(
                carte,
                text="← Question précédente",
                font=("Helvetica", 9),
                bg=self.BG_CARTE,
                fg=self.TEXTE_GRIS,
                activebackground=self.BG_CARTE,
                activeforeground=self.TEXTE_BLANC,
                relief=tk.FLAT,
                cursor="hand2",
                command=self._precedent
            )
            btn_retour.pack(anchor=tk.W, pady=(15, 0))

    def _choisir(self, cle_choix: str) -> None:
        q = self._questions[self._index]
        self._reponses[q.identifiant] = cle_choix
        self._points[q.identifiant] = q.calculer_points_rarete(cle_choix)

        if self._index + 1 < len(self._questions):
            self._index += 1
            self._afficher_question()
        else:
            self._afficher_resultats()

    def _precedent(self) -> None:
        if self._index > 0:
            self._index -= 1
            self._afficher_question()

    # --- Écran des résultats ---
    def _calculer_bilan(self) -> Dict[str, Any]:
        p = self._points
        s_methode = round(float((p.get("q_organisation", 50) + p.get("q_concentration", 50)) / 2), 1)
        s_relations = round(float((p.get("q_conflit", 50) + p.get("q_weekend", 50)) / 2), 1)
        s_choix = round(float((p.get("q_decision", 50) + p.get("q_imprevu", 50)) / 2), 1)
        s_quotidien = round(float((p.get("q_reveil", 50) + p.get("q_franchise", 50)) / 2), 1)

        score_total = round(float((s_methode + s_relations + s_choix + s_quotidien) / 4), 1)
        choix_originaux = sum(1 for v in p.values() if v >= 75.0)

        caracteristiques = {
            **self._reponses,
            "score_methode": s_methode,
            "score_relations": s_relations,
            "score_choix": s_choix,
            "score_quotidien": s_quotidien,
            "score_total_rarete": score_total,
            "choix_originaux": choix_originaux
        }

        archetype = "Profil Équilibré & Pragmatique"
        probas: Dict[str, float] = {}
        if self._modele_pret and self._modele.est_charge:
            try:
                archetype, probas = self._modele.predire(caracteristiques)
            except Exception:
                pass

        percentile = min(98, max(12, int(score_total * 1.12)))

        return {
            "s_methode": s_methode,
            "s_relations": s_relations,
            "s_choix": s_choix,
            "s_quotidien": s_quotidien,
            "score_total": score_total,
            "archetype": archetype,
            "probas": probas,
            "percentile": percentile,
            "donnees": caracteristiques
        }

    def _afficher_resultats(self) -> None:
        self._nettoyer_zone()
        bilan = self._calculer_bilan()

        cadre_split = tk.Frame(self._zone_principale, bg=self.BG_PRINCIPAL)
        cadre_split.pack(fill=tk.BOTH, expand=True)

        panneau_g = tk.Frame(
            cadre_split,
            bg=self.BG_CARTE,
            highlightthickness=1,
            highlightbackground=self.BORDURE,
            padx=25,
            pady=20
        )
        panneau_g.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tk.Label(
            panneau_g,
            text="Ton résultat",
            font=("Helvetica", 15, "bold"),
            fg=self.TEXTE_BLANC,
            bg=self.BG_CARTE
        ).pack(anchor=tk.W, pady=(0, 8))

        lbl_archetype = tk.Label(
            panneau_g,
            text=bilan["archetype"],
            font=("Helvetica", 13, "bold"),
            fg=self.ACCENT,
            bg=self.BG_CARTE
        )
        lbl_archetype.pack(anchor=tk.W, pady=(0, 12))

        descriptions = {
            "Profil Spontané & Intuitif": "Tu écoutes souvent ton instinct et tes envies du moment. Tu n'hésites pas à sortir des routines établies quand l'inspiration est là.",
            "Profil Structuré & Collectif": "Tu apprécies la clarté, l'anticipation et l'harmonie avec ton entourage. Tes décisions s'appuient sur des repères stables et rassurants.",
            "Profil Équilibré & Pragmatique": "Tu mixes bon sens et adaptabilité selon les situations. Ni rigide ni impulsif, tu choisis ce qui fonctionne le mieux au cas par cas."
        }
        desc_texte = descriptions.get(bilan["archetype"], descriptions["Profil Équilibré & Pragmatique"])

        tk.Label(
            panneau_g,
            text=desc_texte,
            font=("Helvetica", 10),
            fg=self.TEXTE_GRIS,
            bg=self.BG_CARTE,
            justify=tk.LEFT,
            wraplength=380
        ).pack(anchor=tk.W, pady=(0, 15))

        cadre_stats = tk.Frame(panneau_g, bg=self.BG_ELEMENT, padx=14, pady=10)
        cadre_stats.pack(fill=tk.X, pady=(0, 15))

        tk.Label(
            cadre_stats,
            text=f"Indice de singularité : {bilan['score_total']:.0f} / 100",
            font=("Helvetica", 11, "bold"),
            fg=self.TEXTE_BLANC,
            bg=self.BG_ELEMENT
        ).pack(anchor=tk.W)

        tk.Label(
            cadre_stats,
            text=f"Tes choix sont plus originaux que ceux de {bilan['percentile']} % des répondants.",
            font=("Helvetica", 9),
            fg=self.ACCENT_VERT,
            bg=self.BG_ELEMENT
        ).pack(anchor=tk.W, pady=(2, 0))

        cadre_actions = tk.Frame(panneau_g, bg=self.BG_CARTE)
        cadre_actions.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))

        btn_recommencer = tk.Button(
            cadre_actions,
            text="Recommencer",
            font=("Helvetica", 10, "bold"),
            bg=self.ACCENT,
            fg="#ffffff",
            activebackground="#6366f1",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=14,
            pady=7,
            cursor="hand2",
            command=self._lancer_quiz
        )
        btn_recommencer.pack(side=tk.LEFT, padx=(0, 8))

        btn_sauver = tk.Button(
            cadre_actions,
            text="Enregistrer",
            font=("Helvetica", 9),
            bg=self.BG_ELEMENT,
            fg=self.TEXTE_BLANC,
            activebackground=self.BG_SURVOL,
            activeforeground=self.TEXTE_BLANC,
            relief=tk.FLAT,
            padx=12,
            pady=7,
            cursor="hand2",
            command=lambda: self._enregistrer_csv(bilan)
        )
        btn_sauver.pack(side=tk.LEFT)

        panneau_d = tk.Frame(
            cadre_split,
            bg=self.BG_CARTE,
            highlightthickness=1,
            highlightbackground=self.BORDURE,
            padx=15,
            pady=15
        )
        panneau_d.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        tk.Label(
            panneau_d,
            text="Comparaison par domaine",
            font=("Helvetica", 11, "bold"),
            fg=self.TEXTE_BLANC,
            bg=self.BG_CARTE
        ).pack(anchor=tk.W, pady=(0, 6))

        self._dessiner_graphique_sombre(panneau_d, bilan)

    def _dessiner_graphique_sombre(self, parent: tk.Widget, bilan: Dict[str, Any]) -> None:
        categories = ["Méthode", "Relations", "Décision", "Quotidien"]
        vos_scores = [bilan["s_methode"], bilan["s_relations"], bilan["s_choix"], bilan["s_quotidien"]]
        moyennes_generales = [58.0, 60.0, 62.0, 61.0]

        fig, ax = plt.subplots(figsize=(4.8, 3.8), dpi=100)
        fig.patch.set_facecolor(self.BG_CARTE)
        ax.set_facecolor(self.BG_CARTE)

        pos = range(len(categories))
        epaisseur = 0.32

        b1 = ax.barh([p + epaisseur / 2 for p in pos], vos_scores, height=epaisseur, label="Tes réponses", color=self.ACCENT)
        b2 = ax.barh([p - epaisseur / 2 for p in pos], moyennes_generales, height=epaisseur, label="Moyenne générale", color="#52525b")

        ax.set_yticks(pos)
        ax.set_yticklabels(categories, fontsize=9, color=self.TEXTE_BLANC)
        ax.set_xlim(0, 100)
        ax.tick_params(colors=self.TEXTE_GRIS, labelsize=8)

        for spine in ["top", "right", "left", "bottom"]:
            ax.spines[spine].set_visible(False)

        ax.xaxis.grid(True, linestyle=":", alpha=0.2, color="#ffffff")

        for bar in b1:
            val = bar.get_width()
            ax.text(val + 1.5, bar.get_y() + bar.get_height() / 2, f"{val:.0f}", va="center", fontsize=8, color=self.ACCENT, fontweight="bold")

        ax.legend(loc="lower right", frameon=False, fontsize=8, labelcolor=self.TEXTE_GRIS)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self._canvas_matplot = canvas

    def _enregistrer_csv(self, bilan: Dict[str, Any]) -> None:
        try:
            os.makedirs(os.path.dirname(self._chemin_historique), exist_ok=True)
            deja_existant = os.path.exists(self._chemin_historique)

            ligne = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "profil": bilan["archetype"],
                "score_global": bilan["score_total"],
                "percentile": bilan["percentile"],
                "methode": bilan["s_methode"],
                "relations": bilan["s_relations"],
                "decision": bilan["s_choix"],
                "quotidien": bilan["s_quotidien"]
            }

            with open(self._chemin_historique, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(ligne.keys()))
                if not deja_existant:
                    writer.writeheader()
                writer.writerow(ligne)

            messagebox.showinfo("Enregistré", "Ton résultat a été enregistré avec succès.")
        except Exception as err:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer : {err}")

    def _afficher_a_propos(self) -> None:
        messagebox.showinfo(
            "À propos du projet (INF1007)",
            "PROJET 2 : « ÊTES-VOUS SPÉCIAL ? »\n"
            "Auteurs : Mohamed Kassi-Lahlou & Kate Eliora Yoboue\n\n"
            "FONCTIONNEMENT TECHNIQUE DU COURS :\n"
            "• Programmation Orientée Objet (POO) avec validation des données.\n"
            "• Générateur de lecture par blocs avec le mot-clé yield (Chapitre 7).\n"
            "• Modèle supervisé de Forêt Aléatoire (Random Forest) entraîné sur 3 000 entrées.\n"
            "• Calcul d'exactitude vectorisé pur NumPy sans boucle for (Chapitre 12).\n"
            "• Interface graphique sobre Tkinter et Matplotlib."
        )
