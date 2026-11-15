"""Boss des Limbes Flétrissants (boss rush) et leurs différentes phases."""

from coliseum.combat.bestiaire.fiche import FicheMonstre, monstre


def _finir_astonre(modele):
    modele.sorts.append("Faire fuir le Domovoï")
    modele.sorts.append("Faire fuir la Kikimora")


@monstre("AstonRe")
def astonre(combat):
    return FicheMonstre(
        stigma_positif="Gluantesque",
        stigma_negatif="Gluantin",
        force=0,
        intelligence=0,
        resistance=0,
        vies_supplementaires=0,
        vie_max=10,
        mana_max=30,
        actions={
            "Coup de Boule": "Technique",
            "Etranglement": "Technique", # rend muet
            "Soin": "Sort",
            "Flamme": "Sort"
        },
        recompense={"Vie max": 2, "Gold": 15 + combat.bonus_gold},
        tags=["Kikimora", "Domovoï"],
        finition=_finir_astonre,
    )


@monstre("Cauchemard")
def cauchemard(combat):
    return FicheMonstre(
        stigma_positif="Gluantesque",
        stigma_negatif="Gluantin",
        force=0,
        intelligence=0,
        resistance=0,
        vies_supplementaires=1,
        vie_max=10,
        mana_max=30,
        actions={
            "Coup de Boule": "Technique",
            "Etranglement": "Technique", # rend muet
            "Soin": "Sort",
            "Flamme": "Sort"
        },
        tags=["Terreur", "Super Etoile"],
        recompense={"Vie max": 2, "Gold": 15 + combat.bonus_gold},
    )


@monstre("Cauchemard (Affaibli)")
def cauchemard_affaibli(combat):
    return FicheMonstre(
        stigma_positif="Gluantesque",
        stigma_negatif="Gluantin",
        force=0,
        intelligence=0,
        resistance=0,
        vies_supplementaires=0,
        vie_max=10,
        mana_max=30,
        actions={
            "Coup de Boule": "Technique",
            "Etranglement": "Technique", # rend muet
            "Soin": "Sort",
            "Flamme": "Sort"
        },
        recompense={"Vie max": 2, "Gold": 15 + combat.bonus_gold},
    )


@monstre("Ahmed (Plat de résistance)")
def ahmed_plat_de_resistance(combat):
    return FicheMonstre(
        stigma_positif="Gluantesque",
        stigma_negatif="",
        force=0,
        intelligence=0,
        resistance=0,
        vies_supplementaires=1,
        vie_max=10,
        mana_max=30,
        actions={
            "Coup de Boule": "Technique",
            "Etranglement": "Technique", # rend muet
            "Soin": "Sort",
            "Flamme": "Sort"
        },
        recompense={"Vie max": 2, "Gold": 15 + combat.bonus_gold},
        tags=("Cuisine Infernale", "Plat"),
        etat_initial={"liste_cuisson": {}, "monstre_commande": {}},
    )


@monstre("Ahmed (Dessert)")
def ahmed_dessert(combat):
    return FicheMonstre(
        stigma_positif="Gluantesque",
        stigma_negatif="",
        force=0,
        intelligence=0,
        resistance=0,
        vies_supplementaires=0,
        vie_max=10,
        mana_max=30,
        actions={
            "Coup de Boule": "Technique",
            "Etranglement": "Technique", # rend muet
            "Soin": "Sort",
            "Flamme": "Sort"
        },
        recompense={"Vie max": 2, "Gold": 15 + combat.bonus_gold},
        tags=("Cuisine Infernale", "Dessert"),
        etat_initial={"liste_cuisson": {}, "monstre_commande": {}},
    )


@monstre("Spectre (Agonie)")
def spectre_agonie(combat):
    return FicheMonstre(
        stigma_positif="Gluantesque",
        stigma_negatif="Gluantin",
        force=0,
        intelligence=0,
        resistance=0,
        vies_supplementaires=0,
        vie_max=10,
        mana_max=30,
        actions={
            "Coup de Boule": "Technique",
            "Etranglement": "Technique", # rend muet
            "Soin": "Sort",
            "Flamme": "Sort"
        },
        recompense={"Vie max": 2, "Gold": 15 + combat.bonus_gold},
    )


def _finir_ahmed_entree(modele):
    modele.techniques.append("Cuisiner")


@monstre("Ahmed (Entrée)")
def ahmed_entree(combat):
    return FicheMonstre(
        stigma_positif="Gluantesque",
        stigma_negatif="",
        force=0,
        intelligence=0,
        resistance=0,
        vies_supplementaires=1,
        vie_max=10,
        mana_max=30,
        actions={
            "Coup de Boule": "Technique",
            "Etranglement": "Technique", # rend muet
            "Soin": "Sort",
            "Flamme": "Sort"
        },
        recompense={"Vie max": 2, "Gold": 15 + combat.bonus_gold},
        tags=("Cuisine Infernale", "Entrée"),
        finition=_finir_ahmed_entree,
    )


@monstre("Roi Gluant")
def roi_gluant(combat):
    return FicheMonstre(
        stigma_positif="Gluantesque",
        stigma_negatif="Gluantin",
        force=0,
        intelligence=0,
        resistance=0,
        vies_supplementaires=1,
        vie_max=10,
        mana_max=30,
        actions={
            "Coup de Boule": "Technique",
            "Etranglement": "Technique", # rend muet
            "Soin": "Sort",
            "Flamme": "Sort"
        },
        recompense={"Vie max": 2, "Gold": 15 + combat.bonus_gold},
    )


@monstre("Obo la Cryobarbare")
def obo_la_cryobarbare(combat):
    return FicheMonstre(
        stigma_positif="Gluantesque",
        stigma_negatif="Gluantin",
        force=0,
        intelligence=0,
        resistance=0,
        vies_supplementaires=2,
        vie_max=10,
        mana_max=30,
        actions={
            "Coup de Boule": "Technique",
            "Etranglement": "Technique", # rend muet
            "Soin": "Sort",
            "Flamme": "Sort"
        },
        recompense={"Vie max": 2, "Gold": 15 + combat.bonus_gold},
    )


@monstre("Mercenaire")
def mercenaire(combat):
    return FicheMonstre(
        stigma_positif="Gluantesque",
        stigma_negatif="Gluantin",
        force=0,
        intelligence=0,
        resistance=0,
        vies_supplementaires=0,
        vie_max=10,
        mana_max=30,
        actions={
            "Coup de Boule": "Technique",
            "Etranglement": "Technique", # rend muet
            "Soin": "Sort",
            "Flamme": "Sort"
        },
        recompense={"Vie max": 2, "Gold": 15 + combat.bonus_gold},
    )


@monstre("Volontée Immortelle")
def volontee_immortelle(combat):
    return FicheMonstre(
        stigma_positif="Gluantesque",
        stigma_negatif="Gluantin",
        force=0,
        intelligence=0,
        resistance=0,
        vies_supplementaires=4,
        vie_max=10,
        mana_max=30,
        actions={
            "Coup de Boule": "Technique",
            "Etranglement": "Technique", # rend muet
            "Soin": "Sort",
            "Flamme": "Sort"
        },
        recompense={"Vie max": 2, "Gold": 15 + combat.bonus_gold},
    )


@monstre("Eris (?)")
def eris(combat):
    return FicheMonstre(
        stigma_positif="Gluantesque",
        stigma_negatif="Gluantin",
        force=0,
        intelligence=0,
        resistance=0,
        vies_supplementaires=2,
        vie_max=10,
        mana_max=30,
        actions={
            "Coup de Boule": "Technique",
            "Etranglement": "Technique", # rend muet
            "Soin": "Sort",
            "Flamme": "Sort"
        },
        recompense={"Vie max": 2, "Gold": 15 + combat.bonus_gold},
    )


@monstre("Spectre")
def spectre(combat):
    return FicheMonstre(
        stigma_positif="Gluantesque",
        stigma_negatif="Gluantin",
        force=0,
        intelligence=0,
        resistance=0,
        vies_supplementaires=1,
        vie_max=10,
        mana_max=30,
        actions={
            "Coup de Boule": "Technique",
            "Etranglement": "Technique", # rend muet
            "Soin": "Sort",
            "Flamme": "Sort"
        },
        recompense={"Vie max": 2, "Gold": 15 + combat.bonus_gold},
    )


@monstre("Aurore")
def aurore(combat):
    return FicheMonstre(
        stigma_positif="Gluantesque",
        stigma_negatif="Gluantin",
        force=0,
        intelligence=0,
        resistance=0,
        vies_supplementaires=1,
        vie_max=10,
        mana_max=30,
        actions={
            "Coup de Boule": "Technique",
            "Etranglement": "Technique", # rend muet
            "Soin": "Sort",
            "Flamme": "Sort"
        },
        recompense={"Vie max": 2, "Gold": 15 + combat.bonus_gold},
    )
