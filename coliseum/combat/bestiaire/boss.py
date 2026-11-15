"""Boss de fin d'étage, versions normales et alternatives."""

from coliseum.combat.bestiaire.fiche import FicheMonstre, monstre


@monstre("Clone d'Obsidienne")
def clone_d_obsidienne(combat):
    return FicheMonstre(
        stigma_positif="Roche Ténébreuse",
        stigma_negatif="Flocon de Neige",
        stigma_bonus="Hyallo-Réflection",
        force=3,
        intelligence=3,
        resistance=2,
        vies_supplementaires=0,
        vie_max=165,
        mana_max=35,
        actions={
            "Attaque Lourde": "Technique",
            "Durcissement Calcaire": "Technique", # augmente def
            "Bombe Arcanique": "Sort",
            "Sonata Pitoyable": "Sort", #soin
            "Eveil de Runes": "Sort", # differents effet selon la rune invoquée [x]
            "Coup de Boule": "Technique",
            "Froideur d'Outretombe": "Sort", # gele
        },
        recompense={"Red coin": 1, "Tirage": 1, "Gold": 50 + combat.bonus_gold, "Defence": 1, "Attaque": 2, "Intelligence": 2, "Degat sort critique": 8, "Endurance": 8, "Vie max": 16, "Mana max": 16},
    )


@monstre("Chevalier Pourpre")
def chevalier_pourpre(combat):
    return FicheMonstre(
        stigma_positif="Armure de Plates",
        stigma_negatif="Trauma de Guerre",
        stigma_bonus="Corps d'Acier",
        force=6,
        intelligence=3,
        resistance=8,
        vies_supplementaires=0,
        vie_max=220,
        mana_max=30,
        actions={
            "Lame de Feu": "Technique", #brule
            "Lame de Gel": "Technique", #gele
            "Lame Pourpre": "Technique", #draine
            "Lame Courageuse": "Technique", #gros degats
            "Medecine de Guerre": "Technique", #soin
            "Lamentations": "Sort", #blesse et maudit plus mana [x]
        },
        recompense={"Red coin": 1, "Tirage": 1, "Gold": 100 + combat.bonus_gold, "Vie max": 25, "Endurance": 10},
    )


@monstre("Coquille Vide")
def coquille_vide(combat):
    return FicheMonstre(
        stigma_positif="Odeur Putride",
        stigma_negatif="",
        stigma_bonus="Corps d'Acier",
        force=6,
        intelligence=3,
        resistance=8,
        vies_supplementaires=0,
        vie_max=300,
        mana_max=15,
        actions={
            "Coup Anti-Magie": "Technique", #attaaque meme si protection [x]
            "Lame de Feu": "Technique", #brule
            "Lame de Gel": "Technique", #gele
            "Lame Pourpre": "Technique", #draine
        },
        recompense={"Red coin": 1, "Tirage": 1, "Gold": 100 + combat.bonus_gold, "Mana max": 25, "Endurance": 10},
    )


@monstre("Roi Amonrê")
def roi_amonre(combat):
    return FicheMonstre(
        stigma_positif="Bénédiction Divine",
        stigma_negatif="Patchwork",
        stigma_bonus="Apotre de Râ",
        force=2,
        intelligence=10,
        resistance=0,
        vies_supplementaires=1,
        vie_max=320,
        mana_max=45,
        actions={
            "Invoquation Canope": "Sort", #invoque vase canope, peut echouer [x]
            "Rejuvenation": "Sort", #gros soin
            "Jugement": "Sort", #degat = monstre tue [x]
            "Combo Misérable": "Technique" #combo electrique , mais maudit [x]
        },
        recompense={"Red coin": 1, "Tirage": 1, "Gold": 150 + combat.bonus_gold, "Taux sort critique": 5, "Endurance": 17 },
    )


@monstre("Apprentie")
def apprentie(combat):
    return FicheMonstre(
        stigma_positif="Sort Chanceux",
        stigma_negatif="Anxiété Sociale",
        stigma_bonus="Mal Jaune",
        force=3,
        intelligence=12,
        resistance=5,
        vies_supplementaires=1,
        vie_max=200,
        mana_max=45,
        actions={
            "Faisceau Statique": "Sort",  #paralyse
            "Thermosphère Brulante": "Sort", #brule
            "Pic Froid": "Sort", #gele
            "Création de Lapis": "Sort", #lapide
            "Explosion Renforcée": "Sort", #gros dégats
            "Dance Siphoneuse": "Sort", #saigne
            "Sonata Miséricordieuse": "Sort", #soigne
            "Magie Noire": "Sort" #blesse et hausse cout mana [x]
        },
        recompense={"Red coin": 1, "Méga Tirage": 1, "Gold": 200 + combat.bonus_gold, },
    )


@monstre("Bouffon")
def bouffon(combat):
    return FicheMonstre(
        stigma_positif="Plus d'un Tour",
        stigma_negatif="Arlequin",
        stigma_bonus="Nordique",
        force=10,
        intelligence=10,
        resistance=15,
        vies_supplementaires=0,
        vie_max=750,
        mana_max=50,
        actions={
            "Tournicoti": "Sort", #reprend vie
            "Tournicota": "Sort", #envoie boule a renvoyer ou esquiver [x]
            "Tournicotons": "Sort", #vague a esquiver [x]
            "Tournicotez": "Sort", #queston a repondre [x]
        },
        recompense={"Red coin": 1, "Tirage": 1, "Gold": 250 + combat.bonus_gold, "Taux coup critique": 5, "Taux sort critique": 5, "Vie max": 15, "Mana max": 15, "Endurance": 10},
    )


@monstre("Le Pianiste")
def le_pianiste(combat):
    return FicheMonstre(
        stigma_positif="Coeur Inferno",
        stigma_negatif="Inconsolable Rage",
        stigma_bonus="Nordique",
        force=5,
        intelligence=15,
        resistance=12,
        vies_supplementaires=1,
        vie_max=750,
        mana_max=100,
        actions={
            "Do": "Sort", # reprend vie
            "Ré": "Sort", # met le feu
            "Mi": "Sort", # met la glace
            "Fa": "Sort", # met la foudre 
            "Sol": "Sort", # met le sang
            "La": "Sort", # met le dégat
            "Si": "Sort", # rend confus
            "Symphonie": "Sort", # met feu glace sang degat
            "Déchiquetage": "Technique", # Blesse énormément
        },
        recompense={"Red coin": 1, "Tirage": 1, "Gold": 250 + combat.bonus_gold, "Taux sort critique": 5, "Vie max": 15, "Mana max": 15, "Endurance": 10},
    )


@monstre("Prince des Voleurs")
def prince_des_voleurs(combat):
    return FicheMonstre(
        stigma_positif="Bomberman",
        stigma_negatif="Hautain",
        stigma_bonus="Intemporel",
        force=18,
        intelligence=18,
        resistance=20,
        vies_supplementaires=0,
        vie_max=1100,
        mana_max=30,
        actions={
            "Attaque Titanesque": "Technique", #utilise orbe furie et attaque
            "Remede Divin": "Technique", #soin
            "Fleche Rouge": "Technique", #brule
            "Fleche Bleue": "Technique", #gele
            "Crystal Elémentaire": "Technique",  # inflige lourd brule ou gele [x]
            "Pendule Etrange": "Technique", #paralysie
            "Panacée Universelle": "Technique", #soigne toute les altérations d'état [x]
            "Missile Arcanique": "Sort", #utilise orbe folie et sort
            "Tome de Salomon": "Sort", #draine mp [x]
            "Houken": "Sort", #draine vie
            
        },
        recompense={"Red coin": 1, "Tirage": 1, "Gold": 300 + combat.bonus_gold, "Degat coup critique": 10, "Degat sort critique": 10, "Endurance": 10},
    )


@monstre("Roi Déchu")
def roi_dechu(combat):
    return FicheMonstre(
        stigma_positif="Lignée Royale",
        stigma_negatif="Divinement Renié",
        stigma_bonus="Paranoïa",
        force=5,
        intelligence=5,
        resistance=25,
        vies_supplementaires=0,
        vie_max=432,
        mana_max=15,
        actions={
            "Durcissement Calcaire": "Technique", # augmente def
            "Lame Ultime": "Technique", #gros degats
            "Attaque Titanesque": "Technique", #utilise orbe furie et attaque
            "Magie Noire": "Sort", #blesse et hausse cout mana [x]
            "Création Obsidienne": "Sort", #lapide
            "Lame de Gel": "Technique", #gele
            "Bouclier Ultime": "Technique", #reprend beaucoup de vie
            "Panacée Universelle": "Technique", #soigne toute les altérations d'état [x]
            "Laser Ultime": "Technique", #moyen degat et feu
            "Sort Ultime": "Sort", #gros degat, perd mana [x]
            "Ultime Ultime": "Sort", # impossible d'utiliser sorts et techniques [x]
            "Ultima": "Sort", #ramene la vie du joueur a 10% [x]
        },
        recompense={"Red coin": 1, "Tirage": 1, "Gold": 350 + combat.bonus_gold, "Defence": 5, "Attaque": 5, "Degat coup critique": 10, "Endurance": 10},
    )


@monstre("Roi Damné")
def roi_damne(combat):
    return FicheMonstre(
        stigma_positif="Odeur Putride",  # 15% de chance de faire tomber en endurance [x]
        stigma_negatif="Conductivité Thermique" ,  # +25% de se faire geler [x]
        stigma_bonus="Aura Corrosive",  # blessé deconcentré tout le temps [x]
        force=2,
        intelligence=1,
        resistance=30,
        vies_supplementaires=0,
        vie_max=664,
        mana_max=60,
        actions={
            "Lame Ultime": "Technique", #gros degats
            "Attaque Titanesque": "Technique", #utilise orbe furie et attaque
            "Eveil de Runes": "Sort", # differents effet selon la rune invoquée [x]
            "Lame de Gel": "Technique", #gele
            "Bouclier Ultime": "Technique", #reprend beaucoup de vie
            "Panacée Universelle": "Technique", #soigne toute les altérations d'état [x]
            "Giga Gel": "Sort", # peut geler sur longtemps
            "Laser Ultime": "Technique", #moyen degat et feu
            "Sort Ultime": "Sort", #gros degat, perd mana [x]
            "Ultime Ultime": "Sort", # impossible d'utiliser sorts et techniques [x]
            "Ultima": "Sort", #ramene la vie du joueur a 10% [x]
        },
        recompense={"Red coin": 1, "Tirage": 1, "Gold": 350 + combat.bonus_gold, "Taux sort critique": 5, "Intelligence": 5, "Degat sort critique": 10, "Endurance": 10},
    )


@monstre("Maitre Mage")
def maitre_mage(combat):
    return FicheMonstre(
        stigma_positif="Hardi",
        stigma_negatif="Aucun",
        stigma_bonus="Ministre de la Magie",
        force=15,
        intelligence=25,
        resistance=14,
        vies_supplementaires=1,
        vie_max=600,
        mana_max=70,
        actions={
            "Ascension Runique": "Technique", #seulement la rune du drain de vie
            "Lame Vaillante": "Technique", #grosse attaque
            "Sables du Temps": "Technique", #paralysie 3 tour, monstre perd 5% vie [x]
            "Faisceau Foudroyant": "Sort", #paralyse
            "Thermosphère Magmatique": "Sort", #brule
            "Pic Polaire": "Sort", #gele
            "Création de la Montagne": "Sort", #lapide
            "Explosion Fatale": "Sort", #gros degats
            "Dance Destructrice": "Sort", #drain
            "Sonata Bienveillante": "Sort" #soigne
        },
        recompense={
            "Red coin": 1, "Tirage": 1,
            "Gold": 400 + combat.bonus_gold},
    )


def _finir_ah_kin(modele):
    if modele.monstre_nombre_de_vies_supplementaire == 9:
        modele.monstre_tags.append("Voluntad Káak")
        modele.monstre_tags.append("Voluntad Hielo")
        modele.monstre_tags.append("Voluntad Le Rayo")
    elif modele.monstre_nombre_de_vies_supplementaire == 6:
        modele.monstre_tags.append("Voluntad Le Luumo")
        modele.monstre_tags.append("Voluntad U Kiikel")
        modele.monstre_tags.append("Voluntad U Wíinkilal")
    elif modele.monstre_nombre_de_vies_supplementaire == 3:
        modele.monstre_tags.append("Voluntad Káak") #feu
        modele.monstre_tags.append("Voluntad Hielo") #glace
        modele.monstre_tags.append("Voluntad Le Rayo") #foudre
        modele.monstre_tags.append("Voluntad Le Luumo") #terre
        modele.monstre_tags.append("Voluntad U Kiikel") #sang
        modele.monstre_tags.append("Voluntad U Wíinkilal") #physique | Voluntad Tin Tuukul pour ame


@monstre("Ah Kin")
def ah_kin(combat):
    return FicheMonstre(
        stigma_positif="Aucun",
        stigma_negatif="Aucun",
        stigma_bonus="Aucun",
        force=30,
        intelligence=38,
        resistance=24,
        vies_supplementaires=combat.vies_du_gardien,
        vie_max=800,
        mana_max=50,
        actions={
            "Attaque Lourde": "Technique",
            "Lame Courageuse": "Technique", #gros degats
            "Crystal Elémentaire": "Technique",  # inflige lourd brule ou gele [x]
            "Remede Divin": "Technique", #soin
            "Combo Misérable": "Technique", #combo electrique , mais maudit [x]
        },
        recompense={},
        finition=_finir_ah_kin,
    )


@monstre("Amalgame")
def amalgame(combat):
    return FicheMonstre(
        stigma_positif="Bomberman",
        stigma_negatif="Inflammable",
        stigma_bonus="Hyallo-Réflection",
        force=30,
        intelligence=30,
        resistance=15,
        vies_supplementaires=8,
        vie_max=1,
        mana_max=50,
        actions={
            "Attaque Lourde": "Technique",
            "Durcissement Calcaire": "Technique", # augmente def
            "Bombe Arcanique": "Sort",
            "Sonata": "Sort", #soin
            "Eveil de Runes": "Sort", # differents effet selon la rune invoquée [x]
            "Lame de Feu": "Technique", #brule
            "Lame de Gel": "Technique", #gele
            "Lame Pourpre": "Technique", #draine
            "Lame Courageuse": "Technique", #gros degats
            "Medecine de Guerre": "Technique", #soin
            "Lamentations": "Sort", #blesse et maudit plus mana [x]
            "Invoquation Canope": "Sort", #invoque vase canope, peut echouer [x]
            "Rejuvenation": "Sort", #gros soin
            "Jugement": "Sort", #degat = monstre tue
            "Combo Misérable": "Technique", #combo electrique , mais maudit [x]
            "Faisceau Statique": "Sort",  #paralyse
            "Thermosphère Brulante": "Sort", #brule
            "Pic Froid": "Sort", #gele
            "Création de Lapis": "Sort", #lapide
            "Explosion Renforcée": "Sort", #gros dégats
            "Dance Siphoneuse": "Sort", #saigne
            "Sonata Miséricordieuse": "Sort", #soigne
            "Magie Noire": "Sort", #blesse et hausse cout mana [x]
            "Faisceau de l'Eclair": "Sort",  #paralyse
            "Thermosphère de la Fournaise": "Sort", #brule
            "Pic Glacial": "Sort", #gele
            "Création Obsidienne": "Sort", #lapide
            "Explosion Maitrisée": "Sort", #gros dégats
            "Dance Parasite": "Sort", #saigne
            "Sonata Sincère": "Sort", #soigne
            "Magie Ténébreuse": "Sort", #empeche sort et technique [x]
            "Tournicoti": "Sort", #reprend vie
            "Tournicota": "Sort", #envoie boule a renvoyer ou esquiver [x]
            "Tournicotons": "Sort", #vague a esquiver [x]
            "Tournicotez": "Sort", #queston a repondre [x]
            "Attaque Titanesque": "Technique", #utilise orbe furie et attaque
            "Remede Divin": "Technique", #soin
            "Fleche Rouge": "Technique", #brule
            "Fleche Bleue": "Technique", #gele
            "Crystal Elémentaire": "Technique",  # inflige lourd brule ou gele [x]
            "Pendule Etrange": "Technique", #paralysie
            "Panacée Universelle": "Technique", #soigne toute les altérations d'état [x]
            "Missile Arcanique": "Sort", #utilise orbe folie et sort
            "Tome de Salomon": "Sort", #draine mp [x]
            "Houken": "Sort", #draine vie
            "Lame Ultime": "Technique", #gros degats
            "Bouclier Ultime": "Technique", #reprend beaucoup de vie
            "Laser Ultime": "Technique", #moyen degat et feu
            "Sort Ultime": "Sort", #gros degat, perd mana [x]
            "Ultime Ultime": "Sort", # impossible d'utiliser sorts et techniques [x]
            "Ultima": "Sort", #ramene la vie du joueur a 10% [x]
            "Ascension Runique": "Technique", #seulement la rune du drain de vie
            "Lame Vaillante": "Technique", #grosse attaque
            "Sables du Temps": "Technique", #paralysie 3 tour, monstre perd 5% vie [x]
            "Faisceau Foudroyant": "Sort", #paralyse
            "Thermosphère Magmatique": "Sort", #brule
            "Pic Polaire": "Sort", #gele
            "Création de la Montagne": "Sort", #lapide
            "Explosion Fatale": "Sort", #gros degats
            "Dance Destructrice": "Sort", #drain
            "Sonata Bienveillante": "Sort", #soigne
            "Dragon Ascendant": "Sort", #attaque par vague a esquiver [x]
            "Rituel Canope": "Sort", #seulement le canope de la paralysie 
            "Magie Abyssale": "Sort", #scelle sort et technique, draine 10% pm [x]
            "Faisceau de la Mort Blanche": "Sort", #paralyse
            "Thermosphère Solaire": "Sort", #brule
            "Pic Zéro": "Sort", #gele
            "Création Continentale": "Sort", #lapide
            "Explosion de la Comète": "Sort", #gros degats
            "Dance Créatrice": "Sort", #drain
            "Sonata Absolutrice": "Sort" #soin
        },
        recompense={"Red coin": 1, "Tirage": 1, "Gold": 500 + combat.bonus_gold, 
                                   "Defence": 2, "Attaque": 2, "Intelligence": 2, 
                                   "Taux coup critique": 2, "Degat coup critique": 2, 
                                   "Taux sort critique": 2, "Degat sort critique": 2, "Endurance": 10},
    )


@monstre("Coliseum")
def coliseum(combat):
    return FicheMonstre(
        stigma_positif="Aucun",
        stigma_negatif="Aucun",
        stigma_bonus="Aucun",
        force=40,
        intelligence=40,
        resistance=10,
        vies_supplementaires=1,
        vie_max=700,
        mana_max=100,
        actions={
            "Lame Ultime": "Technique", #gros degats
            "Bouclier Ultime": "Technique", #reprend beaucoup de vie
            "Laser Ultime": "Technique", #moyen degat et feu
            "Sort Ultime": "Sort", #gros degat, perd mana [x]
            "Ultime Ultime": "Sort", # impossible d'utiliser sor
        },
        recompense={"Red coin": 1, "Tirage": 1, "Gold": 99999, 
                                   "Attaque": 99999, "Intelligence": 99999},
    )
