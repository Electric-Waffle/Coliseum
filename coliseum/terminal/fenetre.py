"""Terminal « fenêtre » : une seule fenêtre pour lire, répondre, voir la carte et les récaps.

    ┌────────────────────────────┬────────────────────────────┐
    │ récap du joueur            │ carte de l'étage (turtle)  │
    │ (image + caractéristiques) │ ou, en combat, récap du    │
    │                            │ monstre                    │
    ├────────────────────────────┴────────────────────────────┤
    │ texte du jeu (comme une console)                        │
    │ > saisie du joueur                                      │
    └─────────────────────────────────────────────────────────┘

Chaque zone du haut occupe la moitié de la largeur ; le partage de la hauteur
entre le haut et la console est réglé par POIDS_DU_HAUT et POIDS_DE_LA_CONSOLE. Les récaps sont dessinés par
coliseum/terminal/panneau.py à partir des données que fournit
coliseum/interface/recapitulatif.py (voir `suivre`).

FLUX : le jeu est écrit comme un programme de console. Il appelle `input()`
et attend sur place la réponse, il appelle `attendre(2)` et patiente sur
place. Une interface graphique fonctionne à l'envers : une boucle d'événements
tourne en permanence et appelle le code quand il se passe quelque chose.

Pour brancher l'un sur l'autre sans réécrire le jeu, ce terminal garde le jeu
aux commandes, dans le fil principal, et fait tourner la boucle d'événements
de tkinter uniquement pendant que le jeu attend :
- pendant `input()`  -> `lire_une_ligne()` fait tourner la boucle jusqu'à ce
  que le joueur valide une ligne ;
- pendant une pause  -> `attendre()` fait tourner la boucle jusqu'à l'heure dite.
Entre deux attentes, la fenêtre ne bouge pas, mais le jeu n'y reste jamais
plus d'un instant : tout ce qui dure est une saisie ou une pause.

POURQUOI pas un fil d'exécution séparé pour le jeu : tkinter (et turtle, qui
dessine avec tkinter) n'accepte d'être manipulé que depuis un seul fil. Avec
le jeu dans un second fil, chaque `print` et chaque trait de la carte devrait
être renvoyé vers le fil de la fenêtre. Ici tout vit dans le même fil.

ATTENTION : quelques mini-jeux (pêche, jacuzzi, pierre de sang) lancent
eux-mêmes un fil secondaire qui affiche du texte pendant que le fil principal
attend la saisie. Ces écritures ne touchent pas la fenêtre directement : elles
sont déposées dans une file d'attente que le fil principal vide trente fois
par seconde (`_vider_la_file`).
"""

import collections
import os
import queue
import sys
import threading
import time
import tkinter as tk
import tkinter.font
import turtle

from coliseum.terminal.panneau import PanneauDeRecap

TITRE = "Coliseum"
COULEUR_FOND = "#0c0c0c"
COULEUR_TEXTE = "#cccccc"
COULEUR_BORDURE = "#2b2b2b"
COULEUR_DU_SEPARATEUR = "#5a5a5a"
POLICES_PREFEREES = ("Consolas", "Cascadia Mono", "DejaVu Sans Mono", "Courier New")
TAILLE_DE_POLICE = 10
TAILLE_DE_POLICE_DES_RECAPS = 9
# Dimensions visées, pour un écran à 100 % d'échelle.
LARGEUR_SOUHAITEE = 1400
HAUTEUR_SOUHAITEE = 900
# La fenêtre ne dépasse jamais ces parts de l'écran.
PART_MAX_DE_L_ECRAN_EN_LARGEUR = 0.94
PART_MAX_DE_L_ECRAN_EN_HAUTEUR = 0.88
# Partage de la hauteur entre le haut (récaps et carte) et la console.
# 2 et 3 : le haut prend 2/5 de la hauteur (40 %), la console 3/5 (60 %).
# Changer ces deux nombres suffit à déplacer la séparation.
POIDS_DU_HAUT = 2
POIDS_DE_LA_CONSOLE = 3
PERIODE_DE_LA_FILE_MS = 30
PERIODE_DES_RECAPS_MS = 150


def _demander_un_affichage_net():
    """Sous Windows, annonce que la fenêtre gère elle-même l'échelle de l'écran.

    POURQUOI : sur un écran réglé à 125 % ou 150 %, Windows agrandit comme
    une image les fenêtres qui ne disent rien, et le texte devient flou.
    Ailleurs que sous Windows, ou sur une version trop ancienne, l'appel
    n'existe pas : on garde alors l'affichage par défaut.
    """
    try:
        import ctypes

        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except (ImportError, AttributeError, OSError):
        pass


class _FluxDeSortie:
    """Se fait passer pour `sys.stdout` : tout ce que `print` écrit arrive ici."""

    encoding = "utf-8"

    def __init__(self, terminal):
        self._terminal = terminal

    def write(self, texte):
        self._terminal.ecrire(texte)
        return len(texte)

    def flush(self):
        pass

    def isatty(self):
        return False


class _FluxDEntree:
    """Se fait passer pour `sys.stdin` : `input()` vient y chercher sa ligne.

    CONCEPT : quand `sys.stdin` n'est pas la vraie console, `input(invite)`
    écrit l'invite dans `sys.stdout` puis appelle `sys.stdin.readline()`.
    Fournir ces deux objets suffit donc à détourner tous les `input` du jeu.
    """

    encoding = "utf-8"

    def __init__(self, terminal):
        self._terminal = terminal

    def readline(self):
        return self._terminal.lire_une_ligne() + "\n"

    def isatty(self):
        return False


class _EcranDeCarte(turtle.TurtleScreen):
    """Écran turtle logé dans la fenêtre du jeu au lieu d'ouvrir la sienne.

    Le jeu appelle `setup(800, 800)` pour dimensionner la fenêtre de turtle.
    Ici il n'y a plus de fenêtre à dimensionner : ces appels ne font rien.
    """

    def setup(self, *arguments, **options):
        pass

    def title(self, *arguments, **options):
        pass

    def bye(self):
        pass


class TerminalFenetre:

    def __init__(self):
        self._lignes_saisies = collections.deque()
        self._file_des_autres_fils = queue.Queue()
        self._fermeture_demandee = False
        self._attend_une_saisie = False
        self._source_du_joueur = None
        self._source_du_monstre = None
        self._monstre_visible = False
        self._source_de_la_carte = None
        self._carte_possedee = True     # sans source de carte, la carte est toujours montrée
        self._devant = None             # l'élément visible dans le quart haut-droit
        self._erreurs_de_recap_deja_notees = set()

        _demander_un_affichage_net()
        self._racine = tk.Tk()
        self._racine.title(TITRE)
        self._poser_l_icone()
        # Le fond de la fenêtre n'apparaît qu'entre les trois zones : il
        # dessine les traits qui les séparent.
        self._racine.configure(background=COULEUR_DU_SEPARATEUR)
        self._racine.protocol("WM_DELETE_WINDOW", self._demander_la_fermeture)
        # CONCEPT : une variable tkinter peut réveiller du code qui l'attend
        # (`wait_variable`). Chaque ligne validée la modifie : c'est le signal
        # qui sort `lire_une_ligne` de son attente.
        self._signal_de_saisie = tk.IntVar(master=self._racine, value=0)

        famille = self._choisir_la_police()
        police = tkinter.font.Font(family=famille, size=TAILLE_DE_POLICE)
        largeur, hauteur, cote_de_la_carte = self._calculer_les_dimensions()
        # CONCEPT : `uniform` range des lignes (ou des colonnes) dans un même
        # groupe ; tkinter leur donne alors des tailles proportionnelles à
        # leur `weight`, quelle que soit la taille que réclament les éléments
        # placés dedans. Poids égaux = moitié-moitié (les deux colonnes).
        self._racine.rowconfigure(0, weight=POIDS_DU_HAUT, uniform="hauteur")
        self._racine.rowconfigure(1, weight=POIDS_DE_LA_CONSOLE, uniform="hauteur")
        for colonne in (0, 1):
            self._racine.columnconfigure(colonne, weight=1, uniform="moitie_de_largeur")
        self._panneau_du_joueur = PanneauDeRecap(self._racine, famille, TAILLE_DE_POLICE_DES_RECAPS)
        self._panneau_du_joueur.widget.grid(row=0, column=0, sticky="nsew", padx=(0, 1), pady=(0, 1))
        self._construire_la_zone_de_droite(famille, cote_de_la_carte)
        self._construire_la_zone_de_texte(police)
        self._placer_la_fenetre(largeur, hauteur)

        self._flux_d_origine = (sys.stdout, sys.stdin, sys.stderr)
        sortie = _FluxDeSortie(self)
        sys.stdout = sortie
        sys.stderr = sortie
        sys.stdin = _FluxDEntree(self)

        self._racine.after(PERIODE_DE_LA_FILE_MS, self._vider_la_file)
        self._racine.after(PERIODE_DES_RECAPS_MS, self._rafraichir_les_recaps)
        self._champ.focus_set()
        self._racine.update()

    # ------------------------------------------------------------ construction

    def _calculer_les_dimensions(self):
        """Taille de la fenêtre et côté de la carte, bornés par la taille de l'écran.

        La carte est un carré logé dans le quart haut-droit de la fenêtre :
        son côté est limité par la moitié de la hauteur.
        """
        # `winfo_fpixels("1i")` : nombre réel de pixels par pouce, donc
        # l'échelle de l'écran (96 = 100 %, 120 = 125 %...).
        echelle = self._racine.winfo_fpixels("1i") / 96
        largeur_ecran = self._racine.winfo_screenwidth()
        hauteur_ecran = self._racine.winfo_screenheight()

        largeur = int(min(largeur_ecran * PART_MAX_DE_L_ECRAN_EN_LARGEUR, LARGEUR_SOUHAITEE * echelle))
        hauteur = int(min(hauteur_ecran * PART_MAX_DE_L_ECRAN_EN_HAUTEUR, HAUTEUR_SOUHAITEE * echelle))
        hauteur_du_haut = hauteur * POIDS_DU_HAUT // (POIDS_DU_HAUT + POIDS_DE_LA_CONSOLE)
        marge = int(12 * echelle)
        cote = min(hauteur_du_haut - marge, largeur // 2 - marge)
        return largeur, hauteur, cote

    def _poser_l_icone(self):
        """Icône de la fenêtre : ColiseumDependencies/icone.ico, si le fichier existe."""
        from coliseum.chemins import DOSSIER_RESSOURCES

        try:
            self._racine.iconbitmap(os.path.join(DOSSIER_RESSOURCES, "icone.ico"))
        except tk.TclError:
            pass  # pas d'icône, ou fichier illisible : on garde celle par défaut

    def _placer_la_fenetre(self, largeur, hauteur):
        gauche = (self._racine.winfo_screenwidth() - largeur) // 2
        haut = (self._racine.winfo_screenheight() - hauteur) // 3
        self._racine.geometry(f"{largeur}x{hauteur}+{gauche}+{haut}")

    def _construire_la_zone_de_texte(self, police):
        cadre = tk.Frame(self._racine, background=COULEUR_FOND)
        cadre.grid(row=1, column=0, columnspan=2, sticky="nsew")
        cadre.columnconfigure(0, weight=1)
        cadre.rowconfigure(0, weight=1)

        self._texte = tk.Text(
            # Taille demandée minimale : c'est la fenêtre qui fixe la place
            # disponible, et le texte s'étire pour la remplir.
            cadre, width=1, height=1, font=police, wrap="word",
            background=COULEUR_FOND, foreground=COULEUR_TEXTE, insertbackground=COULEUR_TEXTE,
            borderwidth=0, highlightthickness=0, padx=10, pady=8, state="disabled",
        )
        ascenseur = tk.Scrollbar(cadre, command=self._texte.yview)
        self._texte.configure(yscrollcommand=ascenseur.set)
        self._texte.grid(row=0, column=0, sticky="nsew")
        ascenseur.grid(row=0, column=1, sticky="ns")

        ligne_de_saisie = tk.Frame(cadre, background=COULEUR_BORDURE)
        ligne_de_saisie.grid(row=1, column=0, columnspan=2, sticky="ew")
        ligne_de_saisie.columnconfigure(1, weight=1)
        tk.Label(ligne_de_saisie, text=">", font=police, background=COULEUR_BORDURE,
                 foreground=COULEUR_TEXTE).grid(row=0, column=0, padx=(10, 4), pady=6)
        self._champ = tk.Entry(
            ligne_de_saisie, font=police, background=COULEUR_BORDURE, foreground="#ffffff",
            insertbackground="#ffffff", borderwidth=0, highlightthickness=0,
        )
        self._champ.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=6)
        self._champ.bind("<Return>", self._valider_la_saisie)
        self._champ.bind("<KP_Enter>", self._valider_la_saisie)
        # Un clic dans le texte ne doit pas faire perdre la saisie au clavier.
        self._texte.bind("<ButtonRelease-1>", lambda evenement: self._champ.focus_set())

    def _choisir_la_police(self):
        disponibles = set(tkinter.font.families(self._racine))
        for nom in POLICES_PREFEREES:
            if nom in disponibles:
                return nom
        return "TkFixedFont"

    def _construire_la_zone_de_droite(self, famille_de_police, cote_de_la_carte):
        """Quart haut-droit : la carte et le récap du monstre, l'un sur l'autre.

        Les deux sont posés dans la même case de la grille. `tkraise()` fait
        passer l'un devant l'autre : hors combat la carte, en combat le monstre.
        """
        zone = tk.Frame(self._racine, background=COULEUR_BORDURE)
        zone.grid(row=0, column=1, sticky="nsew", padx=(1, 0), pady=(0, 1))
        zone.rowconfigure(0, weight=1)
        zone.columnconfigure(0, weight=1)
        # POURQUOI `grid_propagate(False)` : sans lui, un cadre prend la
        # taille de son contenu, et la carte pourrait élargir sa moitié.
        zone.grid_propagate(False)

        self._panneau_du_monstre = PanneauDeRecap(zone, famille_de_police, TAILLE_DE_POLICE_DES_RECAPS)
        self._panneau_du_monstre.widget.grid(row=0, column=0, sticky="nsew")
        # Un panneau sans récap n'affiche que « -- No Data Found -- » : il
        # sert d'écran tant que le joueur n'a pas reçu la carte.
        self._panneau_sans_carte = PanneauDeRecap(zone, famille_de_police, TAILLE_DE_POLICE_DES_RECAPS)
        self._panneau_sans_carte.widget.grid(row=0, column=0, sticky="nsew")
        self._cadre_de_la_carte = tk.Frame(zone, background=COULEUR_BORDURE)
        self._cadre_de_la_carte.grid(row=0, column=0, sticky="nsew")
        self._construire_la_carte(self._cadre_de_la_carte, cote_de_la_carte)
        # Au lancement, le panneau vide est devant : la carte blanche ne doit
        # pas apparaître un instant avant le premier contrôle.
        tk.Misc.tkraise(self._panneau_sans_carte.widget)

    def _construire_la_carte(self, cadre, cote):
        canevas = turtle.ScrolledCanvas(
            cadre, width=cote, height=cote, canvwidth=cote - 20, canvheight=cote - 20,
        )
        # `expand=True` sans `fill` : la carte garde sa taille carrée et se
        # place au centre de la place restante.
        canevas.pack(expand=True)
        ecran = _EcranDeCarte(canevas)

        # POURQUOI : le jeu dessine avec les fonctions globales de turtle
        # (`goto`, `forward`, `clear`...). Ces fonctions utilisent un écran et
        # un crayon uniques, créés au premier appel dans une fenêtre à part.
        # En installant les nôtres AVANT ce premier appel, tous les dessins du
        # jeu arrivent dans notre canevas, sans changer une ligne de dessin.
        turtle.Turtle._screen = ecran
        turtle.Turtle._pen = turtle.RawTurtle(ecran)

    # ------------------------------------------------------------- les récaps

    def suivre(self, source_du_joueur, source_du_monstre, source_de_la_carte=None):
        """Branche les deux récaps sur le jeu.

        Chaque source est une fonction sans argument qui retourne un `Recap`
        ou None (voir coliseum/interface/recapitulatif.py). La fenêtre les
        appelle régulièrement ; quand la source du monstre retourne None,
        c'est la carte qui est montrée.

        `source_de_la_carte` retourne True si le joueur possède la carte.
        Tant qu'elle retourne False, « -- No Data Found -- » la remplace.

        PATTERN : injection de dépendances. La fenêtre ne sait pas d'où
        viennent les données : on lui donne de quoi les obtenir.
        """
        self._source_du_joueur = source_du_joueur
        self._source_du_monstre = source_du_monstre
        self._source_de_la_carte = source_de_la_carte
        self._verifier_la_carte()
        self._mettre_a_jour_les_recaps()

    def _verifier_la_carte(self):
        # POURQUOI seulement avant chaque saisie, et pas toutes les 150 ms
        # comme les récaps : savoir si la carte est possédée demande de
        # relire le fichier de sauvegarde permanente.
        if self._source_de_la_carte is not None:
            self._carte_possedee = bool(self._interroger(self._source_de_la_carte))

    def _rafraichir_les_recaps(self):
        # FLUX : `after` demande à tkinter de rappeler cette méthode plus
        # tard. Elle se reprogramme elle-même : c'est une boucle, exécutée
        # seulement quand la boucle d'événements tourne, donc pendant que le
        # jeu attend une saisie ou la fin d'une pause.
        if self._fermeture_demandee:
            return
        self._mettre_a_jour_les_recaps()
        self._racine.after(PERIODE_DES_RECAPS_MS, self._rafraichir_les_recaps)

    def _mettre_a_jour_les_recaps(self):
        if self._fermeture_demandee:
            return
        self._panneau_du_joueur.montrer(self._interroger(self._source_du_joueur))
        monstre = self._interroger(self._source_du_monstre)
        if monstre is not None:
            self._panneau_du_monstre.montrer(monstre)
        self._monstre_visible = monstre is not None
        # Trois éléments sont empilés dans le quart haut-droit ; un seul est
        # passé devant : le monstre en combat, sinon la carte si le joueur
        # la possède, sinon le panneau vide « -- No Data Found -- ».
        if self._monstre_visible:
            devant = self._panneau_du_monstre.widget
        elif self._carte_possedee:
            devant = self._cadre_de_la_carte
        else:
            devant = self._panneau_sans_carte.widget
        if devant is not self._devant:
            self._devant = devant
            # ATTENTION : pas `devant.tkraise()`. Sur un Canvas, `tkraise`
            # désigne autre chose (changer l'ordre des formes dessinées).
            # `tk.Misc.tkraise` est la version « passer ce widget devant ».
            tk.Misc.tkraise(devant)

    def _interroger(self, source):
        """Appelle une source de récap. Une erreur dedans ne doit jamais arrêter le jeu."""
        if source is None:
            return None
        try:
            return source()
        except Exception as erreur:
            # Notée une seule fois par type d'erreur : cette méthode est
            # appelée plusieurs fois par seconde.
            signature = repr(erreur)
            if signature not in self._erreurs_de_recap_deja_notees:
                self._erreurs_de_recap_deja_notees.add(signature)
                from coliseum.erreurs import ecrire_dans_le_journal

                ecrire_dans_le_journal()
            return None

    # ----------------------------------------------- appelé par coliseum.console

    def effacer(self):
        if self._dans_le_fil_principal():
            self._effacer_le_texte()
        else:
            self._file_des_autres_fils.put(("effacer", None))

    def attendre(self, secondes):
        if not self._dans_le_fil_principal():
            time.sleep(secondes)
            return
        fin = time.monotonic() + secondes
        while True:
            self._arreter_si_la_fenetre_est_fermee()
            self._racine.update()
            reste = fin - time.monotonic()
            if reste <= 0:
                return
            time.sleep(min(reste, 0.01))

    def montrer_image(self, chemin_vers_limage):
        fenetre = tk.Toplevel(self._racine)
        fenetre.title(TITRE)
        image = tk.PhotoImage(master=fenetre, file=chemin_vers_limage)
        canevas = tk.Canvas(fenetre, width=image.width(), height=image.height(), highlightthickness=0)
        canevas.pack()
        canevas.create_image(0, 0, anchor=tk.NW, image=image)
        # ATTENTION : tkinter n'affiche une image que tant qu'un objet Python
        # la référence. La garder sur la fenêtre l'empêche d'être libérée.
        fenetre.image = image
        self._racine.wait_window(fenetre)
        self._champ.focus_set()

    def fermer(self):
        sys.stdout, sys.stdin, sys.stderr = self._flux_d_origine
        self._fermeture_demandee = True
        try:
            self._racine.destroy()
        except tk.TclError:
            pass

    # ---------------------------------------- appelé par les faux flux standard

    def ecrire(self, texte):
        if self._dans_le_fil_principal():
            self._inserer(texte)
        else:
            self._file_des_autres_fils.put(("ecrire", texte))

    def lire_une_ligne(self):
        """Attend que le joueur valide une ligne et la retourne.

        Seule une ligne validée PENDANT cette attente compte. Les touches
        Entrée frappées avant (pendant une pause, ou pendant que le jeu
        calculait) sont jetées : marteler Entrée pendant une pause ne fait
        donc pas défiler les dialogues suivants sans les lire.
        """
        self._texte.see("end")
        # Le jeu vient de finir d'agir : les récaps sont remis à jour tout de
        # suite, sans attendre le prochain passage périodique.
        self._verifier_la_carte()
        self._mettre_a_jour_les_recaps()
        # FLUX : `update()` traite les frappes restées en attente dans
        # tkinter. Le drapeau `_attend_une_saisie` est encore faux : ces
        # frappes en avance sont donc ignorées par `_valider_la_saisie`.
        self._arreter_si_la_fenetre_est_fermee()
        self._racine.update()
        self._lignes_saisies.clear()
        self._attend_une_saisie = True
        try:
            while not self._lignes_saisies:
                self._arreter_si_la_fenetre_est_fermee()
                self._racine.wait_variable(self._signal_de_saisie)
            self._arreter_si_la_fenetre_est_fermee()
            return self._lignes_saisies.popleft()
        finally:
            self._attend_une_saisie = False

    # ---------------------------------------------------------------- interne

    def _dans_le_fil_principal(self):
        return threading.current_thread() is threading.main_thread()

    def _inserer(self, texte):
        if self._fermeture_demandee:
            return
        self._texte.configure(state="normal")
        self._texte.insert("end", texte)
        self._texte.configure(state="disabled")
        self._texte.see("end")

    def _effacer_le_texte(self):
        if self._fermeture_demandee:
            return
        self._texte.configure(state="normal")
        self._texte.delete("1.0", "end")
        self._texte.configure(state="disabled")

    def _valider_la_saisie(self, _evenement=None):
        if not self._attend_une_saisie:
            # Le jeu ne demande rien pour l'instant : cette validation est
            # ignorée. Le texte déjà tapé reste dans le champ.
            return
        ligne = self._champ.get()
        self._champ.delete(0, "end")
        # La console affiche ce que le joueur tape : on fait de même.
        self._inserer(ligne + "\n")
        self._lignes_saisies.append(ligne)
        self._reveiller_la_saisie()

    def _reveiller_la_saisie(self):
        self._signal_de_saisie.set(self._signal_de_saisie.get() + 1)

    def _vider_la_file(self):
        if self._fermeture_demandee:
            return
        while True:
            try:
                operation, texte = self._file_des_autres_fils.get_nowait()
            except queue.Empty:
                break
            if operation == "effacer":
                self._effacer_le_texte()
            else:
                self._inserer(texte)
        self._racine.after(PERIODE_DE_LA_FILE_MS, self._vider_la_file)

    def _demander_la_fermeture(self):
        # POURQUOI ne pas détruire la fenêtre ici : le jeu est en train
        # d'attendre quelque part dans son code. On note la demande, on le
        # réveille, et c'est lui qui s'arrête proprement à sa prochaine
        # attente, comme s'il avait appelé sys.exit().
        self._fermeture_demandee = True
        self._reveiller_la_saisie()

    def _arreter_si_la_fenetre_est_fermee(self):
        if self._fermeture_demandee:
            raise SystemExit(0)
