"""Tirage du matériau lâché par un monstre, avec compteur de malchance.

PROBLÈME : un monstre ne lâche que SON matériau, avec environ 25,7 % de chance
(26 tirages gagnants sur 101). Chaque étage a cinq monstres : pour un matériau
précis, la chance par combat est d'environ 5 %. Sans correctif, 45 % des
joueurs n'en voient aucun en 15 combats.

SOLUTION : chaque type de monstre a son compteur d'échecs consécutifs. La chance
du tirage suivant vaut `(échecs + 1) x C`, et retombe à zéro au drop.
- C est choisie pour que la chance MOYENNE reste celle d'origine
  (25,7 % : C = 8,95 % ; avec le Médaillon de Leprechaun niveau 5, 50,5 % :
  C = 30,7 %) : on ne donne pas plus de matériaux, on les répartit mieux ;
- au pire, 12 échecs de suite (4 avec le Médaillon niveau 5).

PATTERN : distribution pseudo-aléatoire. Le hasard reste (le premier tirage
vaut seulement 8,95 %) mais n'est plus sans mémoire.
"""

import random
from functools import lru_cache

# Chance d'origine : `randint(0, 100) <= 25 + bonus` gagne dans (26 + bonus) cas sur 101.
POSSIBILITES_GAGNANTES_DE_BASE = 26
NOMBRE_DE_POSSIBILITES = 101


def chance_moyenne(bonus_de_leprechaun):
    return min(1.0, (POSSIBILITES_GAGNANTES_DE_BASE + bonus_de_leprechaun) / float(NOMBRE_DE_POSSIBILITES))


def _chance_moyenne_obtenue(c):
    """Chance moyenne à long terme d'un compteur de constante `c` (inverse de l'attente moyenne)."""
    attente, survie, n = 0.0, 1.0, 0
    while survie > 1e-12 and n < 1000:
        n += 1
        attente += survie          # probabilité d'avoir besoin d'un n-ième tirage
        survie *= 1 - min(1.0, n * c)
    return 1.0 / attente


@lru_cache(maxsize=None)
def constante_de_malchance(chance_voulue):
    """Cherche C par dichotomie : la plus grande constante donne la plus grande chance moyenne."""
    if chance_voulue >= 1.0:
        return 1.0
    bas, haut = 0.0, 1.0
    for _ in range(60):
        milieu = (bas + haut) / 2
        if _chance_moyenne_obtenue(milieu) < chance_voulue:
            bas = milieu
        else:
            haut = milieu
    return bas


def chance_du_prochain_tirage(echecs_consecutifs, chance_voulue):
    c = constante_de_malchance(round(chance_voulue, 4))
    return min(1.0, (echecs_consecutifs + 1) * c)


def le_materiau_tombe(echecs_consecutifs, chance_voulue):
    return random.random() < chance_du_prochain_tirage(echecs_consecutifs, chance_voulue)
