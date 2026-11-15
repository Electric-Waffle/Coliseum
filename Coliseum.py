"""Point d'entrée du jeu : `python Coliseum.py`.

Ce fichier ne fait qu'une chose : lancer le jeu sous le filet de sécurité
global (voir coliseum/erreurs.py). Si le joueur quitte normalement, la fenêtre
se ferme. Si le jeu plante, le rapport d'erreur s'affiche et est enregistré.
"""

import sys

from coliseum.erreurs import executer_avec_rapport_de_crash


def lancer():
    # POURQUOI : l'import est fait ici et non en haut du fichier. Charger
    # `application` charge tout le jeu (et pygame) : si ce chargement échoue,
    # par exemple parce que pygame n'est pas installé, l'erreur se produit
    # ainsi à l'intérieur du filet de sécurité et le joueur voit un rapport.
    from coliseum.application import lancer_le_jeu

    lancer_le_jeu()


if __name__ == "__main__":
    sys.exit(executer_avec_rapport_de_crash(lancer))
