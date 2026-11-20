"""Réduction des dégâts par la défense du joueur et la résistance des monstres.

CONCEPT : deux formes de bonus à ne pas confondre.
- un pourcentage s'applique au résultat : « -2 % par point de défense » retire
  2 % des dégâts, quelle que soit leur taille ;
- une valeur plate se soustrait au résultat : « -0,5 par point de défense »
  retire 0,5 point de dégâts à chaque coup, gros ou petit.

POURQUOI les deux : le pourcentage seul est trop fort contre les gros coups
(à 34 points de l'ancienne formule, on ne subissait plus rien) ; la valeur
plate seule annule tous les petits coups mais laisse passer les gros. Ensemble,
plafonnés, les petits coups deviennent négligeables sans que les gros ne
disparaissent jamais : un plancher garantit une part minimale du coup.

Défense du joueur, dans l'ordre :
    1. réduction en pourcentage : 2 % par point, 60 % au maximum ;
    2. réduction plate : 0,5 point par point de défense ;
    3. plancher : au moins 15 % du coup d'origine (et jamais moins de 1).

Résistance du monstre : 2 % par point, 60 % au maximum, sans partie plate.
POURQUOI sans partie plate : les coups du joueur grandissent avec sa force
(+10 % par point), une réduction plate serait négligeable en fin de partie et
neutraliserait ses premières attaques.

Les attaques qui retirent un pourcentage des PV du joueur (Rituel,
Lamentations...) ne passent pas par ici : elles ignorent la défense.
"""

# Au dessus de cette esquive, l'esquive ne protège plus davantage.
ESQUIVE_UTILE_MAX = 50
POURCENTAGE_PAR_POINT = 2
PLAFOND_DU_POURCENTAGE = 60
PLAT_PAR_POINT_DE_DEFENCE = 0.5
PLANCHER_EN_PART_DU_COUP = 0.15


def reduction_en_pourcentage(points):
    """Pourcentage de dégâts retiré par `points` de défense ou de résistance (0 à 60)."""
    return max(0, min(PLAFOND_DU_POURCENTAGE, POURCENTAGE_PAR_POINT * points))


def degats_apres_la_defence_du_joueur(degats, points_de_defence, avec_reduction_plate=True):
    """Dégâts que le joueur subit réellement, pour un coup de `degats` avant défense.

    `avec_reduction_plate=False` pour les dégâts sur la durée (brûlure) :
    ils sont déjà un pourcentage des PV max, la partie plate les annulerait.
    """
    if degats <= 0:
        return degats
    apres_le_pourcentage = degats * (100 - reduction_en_pourcentage(points_de_defence)) / 100.0
    if avec_reduction_plate:
        apres_le_pourcentage -= PLAT_PAR_POINT_DE_DEFENCE * max(0, points_de_defence)
    plancher = PLANCHER_EN_PART_DU_COUP * degats
    return max(1, round(max(plancher, apres_le_pourcentage)))
