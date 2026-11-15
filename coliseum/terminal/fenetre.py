"""Terminal « fenêtre » : une seule fenêtre pour lire, répondre et voir la carte.

    ┌──────────────────────────────────────┬──────────────────┐
    │ texte du jeu (comme une console)     │ carte de l'étage │
    │                                      │ (dessin turtle)  │
    ├──────────────────────────────────────┤                  │
    │ > saisie du joueur                   │                  │
    └──────────────────────────────────────┴──────────────────┘

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
import queue
import sys
import threading
import time
import tkinter as tk
import tkinter.font
import turtle

TITRE = "Coliseum"
COULEUR_FOND = "#0c0c0c"
COULEUR_TEXTE = "#cccccc"
COULEUR_BORDURE = "#2b2b2b"
POLICES_PREFEREES = ("Consolas", "Cascadia Mono", "DejaVu Sans Mono", "Courier New")
TAILLE_DE_POLICE = 10
# Dimensions visées, pour un écran à 100 % d'échelle.
COLONNES = 104
HAUTEUR_SOUHAITEE = 760
COTE_DE_LA_CARTE = 560
# La fenêtre ne dépasse jamais ces parts de l'écran.
PART_MAX_DE_L_ECRAN_EN_LARGEUR = 0.94
PART_MAX_DE_L_ECRAN_EN_HAUTEUR = 0.82
PART_MAX_DE_LA_CARTE_EN_LARGEUR = 0.36
PERIODE_DE_LA_FILE_MS = 30


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

        _demander_un_affichage_net()
        self._racine = tk.Tk()
        self._racine.title(TITRE)
        self._racine.configure(background=COULEUR_FOND)
        self._racine.protocol("WM_DELETE_WINDOW", self._demander_la_fermeture)
        # CONCEPT : une variable tkinter peut réveiller du code qui l'attend
        # (`wait_variable`). Chaque ligne validée la modifie : c'est le signal
        # qui sort `lire_une_ligne` de son attente.
        self._signal_de_saisie = tk.IntVar(master=self._racine, value=0)

        police = tkinter.font.Font(family=self._choisir_la_police(), size=TAILLE_DE_POLICE)
        largeur, hauteur, cote_de_la_carte = self._calculer_les_dimensions(police)
        self._construire_la_zone_de_texte(police)
        self._construire_la_carte(cote_de_la_carte)
        self._placer_la_fenetre(largeur, hauteur)
        self._racine.columnconfigure(0, weight=1)
        self._racine.rowconfigure(0, weight=1)

        self._flux_d_origine = (sys.stdout, sys.stdin, sys.stderr)
        sortie = _FluxDeSortie(self)
        sys.stdout = sortie
        sys.stderr = sortie
        sys.stdin = _FluxDEntree(self)

        self._racine.after(PERIODE_DE_LA_FILE_MS, self._vider_la_file)
        self._champ.focus_set()
        self._racine.update()

    # ------------------------------------------------------------ construction

    def _calculer_les_dimensions(self, police):
        """Taille de la fenêtre et de la carte, bornées par celle de l'écran.

        La fenêtre vise COLONNES caractères de texte et une carte carrée, mais
        ne dépasse jamais l'écran : sur un petit écran c'est la zone de texte
        qui rétrécit (les lignes longues passent à la ligne).
        """
        # `winfo_fpixels("1i")` : nombre réel de pixels par pouce, donc
        # l'échelle de l'écran (96 = 100 %, 120 = 125 %...).
        echelle = self._racine.winfo_fpixels("1i") / 96
        largeur_ecran = self._racine.winfo_screenwidth()
        hauteur_ecran = self._racine.winfo_screenheight()

        hauteur = int(min(hauteur_ecran * PART_MAX_DE_L_ECRAN_EN_HAUTEUR, HAUTEUR_SOUHAITEE * echelle))
        marge_autour_de_la_carte = int(70 * echelle)
        cote = int(min(COTE_DE_LA_CARTE * echelle, hauteur - marge_autour_de_la_carte,
                       largeur_ecran * PART_MAX_DE_LA_CARTE_EN_LARGEUR))
        largeur_du_texte = police.measure("0") * COLONNES + int(50 * echelle)
        largeur = int(min(largeur_ecran * PART_MAX_DE_L_ECRAN_EN_LARGEUR, largeur_du_texte + cote + 30))
        return largeur, hauteur, cote

    def _placer_la_fenetre(self, largeur, hauteur):
        gauche = (self._racine.winfo_screenwidth() - largeur) // 2
        haut = (self._racine.winfo_screenheight() - hauteur) // 3
        self._racine.geometry(f"{largeur}x{hauteur}+{gauche}+{haut}")

    def _construire_la_zone_de_texte(self, police):
        cadre = tk.Frame(self._racine, background=COULEUR_FOND)
        cadre.grid(row=0, column=0, sticky="nsew")
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

    def _construire_la_carte(self, cote):
        cadre = tk.Frame(self._racine, background=COULEUR_BORDURE)
        cadre.grid(row=0, column=1, sticky="ns")
        tk.Label(cadre, text="Carte", background=COULEUR_BORDURE,
                 foreground=COULEUR_TEXTE).pack(pady=(6, 2))
        canevas = turtle.ScrolledCanvas(
            cadre, width=cote, height=cote, canvwidth=cote - 20, canvheight=cote - 20,
        )
        canevas.pack(padx=6, pady=(0, 6))
        ecran = _EcranDeCarte(canevas)

        # POURQUOI : le jeu dessine avec les fonctions globales de turtle
        # (`goto`, `forward`, `clear`...). Ces fonctions utilisent un écran et
        # un crayon uniques, créés au premier appel dans une fenêtre à part.
        # En installant les nôtres AVANT ce premier appel, tous les dessins du
        # jeu arrivent dans notre canevas, sans changer une ligne de dessin.
        turtle.Turtle._screen = ecran
        turtle.Turtle._pen = turtle.RawTurtle(ecran)

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

        Une ligne tapée en avance (pendant une pause du jeu) est gardée et
        servie à la saisie suivante, comme dans une console.
        """
        self._texte.see("end")
        while not self._lignes_saisies:
            self._arreter_si_la_fenetre_est_fermee()
            self._racine.wait_variable(self._signal_de_saisie)
        self._arreter_si_la_fenetre_est_fermee()
        return self._lignes_saisies.popleft()

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
