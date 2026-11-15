"""Point de passage unique entre le jeu et ce qui lui sert d'écran.

Le jeu parle à son écran de cinq façons :

    print(...)            afficher du texte
    input(...)            lire une ligne tapée par le joueur
    ClearConsole()        effacer l'écran
    attendre(secondes)    faire une pause
    montrer_image(chemin) afficher une image

PATTERN : Strategy. Ce module ne sait rien faire lui-même : il délègue à un
« terminal » interchangeable, choisi au lancement.
- `TerminalSysteme` (coliseum/terminal/systeme.py) : la vraie console.
- `TerminalFenetre` (coliseum/terminal/fenetre.py) : une fenêtre qui imite une
  console et contient aussi la carte.
Le reste du jeu ne sait pas lequel est actif. Ajouter un troisième écran
(navigateur, autre bibliothèque graphique) = écrire une classe avec ces mêmes
méthodes, sans toucher au jeu.

POURQUOI `print` et `input` ne sont pas dans cette liste de fonctions :
le jeu en contient 4 000, et Python offre déjà le point de branchement.
`print` écrit dans `sys.stdout`, `input` lit dans `sys.stdin` : il suffit que
le terminal remplace ces deux objets pour que tous les appels existants
passent par lui. `effacer` et `attendre`, eux, n'ont pas d'équivalent
standard : d'où ces fonctions.

ATTENTION : ne jamais appeler `time.sleep` directement dans le jeu. Pendant
un `time.sleep`, une fenêtre ne se redessine plus et ne répond plus ;
`attendre` continue de la faire vivre pendant la pause.
"""

from coliseum.terminal.systeme import TerminalSysteme

_terminal = TerminalSysteme()


def utiliser(terminal):
    """Choisit le terminal du jeu. À appeler une fois, avant de lancer le jeu."""
    global _terminal
    _terminal = terminal


def fermer():
    """Rend la main proprement à la fin du programme (ferme la fenêtre s'il y en a une)."""
    _terminal.fermer()


def ClearConsole():
    _terminal.effacer()


def attendre(secondes):
    """Pause de `secondes` secondes, pendant laquelle l'écran reste vivant."""
    _terminal.attendre(secondes)


def montrer_image(chemin_vers_limage):
    """Affiche une image et attend que le joueur la referme."""
    _terminal.montrer_image(chemin_vers_limage)
