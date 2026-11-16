"""Point d'entrée du jeu.

    python Coliseum.py             joue dans la fenêtre du jeu (récaps, carte, texte)
    python Coliseum.py --console   joue dans le terminal, comme à l'origine

Ce fichier ne fait que deux choses : choisir l'écran du jeu, puis lancer le
jeu sous le filet de sécurité global (voir coliseum/erreurs.py). Si le joueur
quitte normalement, tout se ferme. Si le jeu plante, le rapport d'erreur
s'affiche et est enregistré.
"""

import sys

from coliseum import console
from coliseum.erreurs import executer_avec_rapport_de_crash

OPTION_CONSOLE = "--console"


def lancer():
    # POURQUOI : ces imports sont faits ici et non en haut du fichier. Charger
    # la fenêtre ou `application` peut échouer (tkinter ou pygame absent) :
    # l'erreur se produit ainsi à l'intérieur du filet de sécurité, et le
    # joueur voit un rapport au lieu d'une fenêtre qui se ferme toute seule.
    if OPTION_CONSOLE not in sys.argv:
        from coliseum.terminal.fenetre import TerminalFenetre

        from coliseum.interface.recapitulatif import carte_possedee, recap_du_joueur, recap_du_monstre

        fenetre = TerminalFenetre()
        console.utiliser(fenetre)
        # La fenêtre vient lire ces deux fonctions plusieurs fois par seconde
        # pour tenir à jour les récaps du joueur et du monstre.
        fenetre.suivre(recap_du_joueur, recap_du_monstre, carte_possedee)

    from coliseum.application import lancer_le_jeu

    lancer_le_jeu()


def principal():
    # CONCEPT : `try / finally` sans `except`. Le bloc `finally` s'exécute dans
    # tous les cas, y compris quand le jeu s'arrête par sys.exit() : c'est ce
    # qui garantit que la fenêtre est refermée quelle que soit la sortie.
    try:
        return executer_avec_rapport_de_crash(lancer)
    finally:
        console.fermer()


if __name__ == "__main__":
    sys.exit(principal())
