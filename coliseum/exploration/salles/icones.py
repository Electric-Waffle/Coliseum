"""Icône dessinée sur la carte pour chaque type de salle déjà découverte.

Une salle absente de la table n'a simplement pas d'icône (c'est le cas de
toutes les salles du village, dont la carte n'est pas annotée).
"""

from coliseum import services

# type de salle -> nom de la méthode de DrawInTurtle qui dessine son icône
ICONE_PAR_TYPE_DE_SALLE = {
    "MONSTRE": "monstre",
    "GOLD": "gold",
    "ITEM": "item",
    "KEY": "key",
    "LEY": "ley",
    "MIMIQUE": "mimique",
    "PIEGE": "piege",
    "SECRET": "secret",
    "LIANE": "liane",
    "ECLAIR": "eclair",
    "BETE": "bete",
    "HOLLISTIQUE": "bete",
    "MONSTRE_SUPERIEUR": "monstre",
    "AFFIXEUR_TECHNIQUE": "affixeur_technique",
    "AFFIXEUR_SORT": "affixeur_sort",
    "BOSS": "boss",
    "BROKEN": "broken",
    "FAUX SPOT": "spot",
    "SPOT": "spot",
    "SEQUENCE": "sequence",
    "DDR": "ddr",
    "PUIT": "puit",
    "COEUR": "coeur",
    "ARBRE": "machine",
    "CHENIL": "machine",
    "CHARGEUR": "machine",
    "JACCUZI": "machine",
    "DISTRIBUTEUR": "machine",
    "BUFFET": "machine",
    "SPAWNER": "machine",
    "LEVIER": "machine",
    "BOL": "machine",
    "PLAQUE PRESSION": "machine",
    "RITUEL": "rituel",
    "PECHE": "peche",
    "LOTTERIE": "lotterie",
    "WORKSHOP": "workshop",
    "BRAZIER_ROUGE": "brazier",
    "BRAZIER_VERT": "brazier",
    "BRAZIER_BLEU": "brazier",
    "BRAZIER_NOIR": "brazier",
}


def dessiner_l_icone(type_de_salle, position_x, position_y):
    if type_de_salle == "OBELISQUE":
        # Seule icône qui a besoin de savoir où elle se trouve sur la carte.
        services.Draw.obelisque(position_x, position_y)
        return
    nom_de_l_icone = ICONE_PAR_TYPE_DE_SALLE.get(type_de_salle)
    if nom_de_l_icone is not None:
        # CONCEPT : getattr(objet, "nom") équivaut à objet.nom, mais avec un nom
        # connu seulement à l'exécution. Ici il retrouve la méthode de dessin.
        dessiner = getattr(services.Draw, nom_de_l_icone)
        dessiner()
