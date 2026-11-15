"""Emplacements des fichiers du jeu sur le disque.

POURQUOI : avant le découpage, chaque fonction recalculait son dossier avec
`os.path.dirname(os.path.realpath(__file__))`. Ça marchait tant que tout le code
vivait dans le même dossier que les musiques et les sauvegardes. Maintenant que
le code est réparti dans des sous-paquets, `__file__` ne désigne plus le bon
dossier : un seul module connaît donc la disposition du projet, et tous les
autres lui demandent. Déplacer les ressources = modifier ce fichier uniquement.
"""

import os
import sys


def _trouver_la_racine():
    # CONCEPT : un exécutable fabriqué par PyInstaller pose `sys.frozen`. Le
    # code n'est alors plus dans des fichiers .py : `__file__` désigne un
    # dossier interne à l'exécutable. Le seul repère fiable est l'emplacement
    # de l'exécutable lui-même, à côté duquel sont posées les ressources.
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.realpath(sys.executable))
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


DOSSIER_RACINE = _trouver_la_racine()

# Musiques, bruitages (sfx/), images secrètes et fichiers de sauvegarde.
DOSSIER_RESSOURCES = os.path.join(DOSSIER_RACINE, "ColiseumDependencies")

JOURNAL_DES_ERREURS = os.path.join(DOSSIER_RACINE, "ColiseumDependenciesErrorLog.txt")
