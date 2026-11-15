"""Petites fonctions utilitaires sans lien avec une partie précise du jeu."""

import random


def GetRandomItemFromList(liste):
    number_of_item = len(liste)
    numero_aleatoire = random.randint(0, (number_of_item - 1))
    return liste[numero_aleatoire]
