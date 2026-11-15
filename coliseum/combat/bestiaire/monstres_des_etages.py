"""Monstres ordinaires rencontrés dans l'arène et les salles des étages."""

from coliseum.combat.bestiaire.fiche import FicheMonstre, monstre


@monstre("Gluant")
def gluant(combat):
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
        recompense={"Vie max": 2, "Gold": 15 + combat.bonus_gold, "Materiau": "Coeur Gravitaire"},
    )


@monstre("Feu Follet")
def feu_follet(combat):
    return FicheMonstre(
        stigma_positif="Siphon de Mana",
        stigma_negatif="Pyrolien",
        force=0,
        intelligence=2,
        resistance=0,
        vies_supplementaires=0,
        vie_max=10,
        mana_max=30,
        actions={
            "Tout Feu Tout Flamme": "Sort", # combo electrique, pour le feu [x]
            "Feu Regénérateur": "Sort", # soin
            "Poing de Feu": "Technique", # brule
            "Brulevent": "Technique" # rend muet
        },
        recompense={"Mana max": 2, "Gold": 10 + combat.bonus_gold, "Materiau": "Ectoplasme Chaud"},
    )


@monstre("Golem de Terre")
def golem_de_terre(combat):
    return FicheMonstre(
        stigma_positif="Géodynamisme",
        stigma_negatif="Corps Massif",
        force=2,
        intelligence=0,
        resistance=2,
        vies_supplementaires=0,
        vie_max=15,
        mana_max=30,
        actions={
            "Frappe Lourde": "Technique",  # gros degat, peu chance toucher
            "Poing Eclat": "Technique",  # rend blesse
            "Durcissement Argilite": "Technique",  # plus de defence  [x]
            "Eboulis": "Technique",  # peux lapider
            "Poing de Mana": "Sort"
        },
        recompense={"Vie max": 1, "Degat coup critique": 1, "Gold": 20 + combat.bonus_gold, "Materiau": "Poussière Animée"},
    )


@monstre("Ombre Tangible")
def ombre_tangible(combat):
    return FicheMonstre(
        stigma_positif="Malédiction",
        stigma_negatif="Astralien",
        force=0,
        intelligence=2,
        resistance=0,
        vies_supplementaires=0,
        vie_max=10,
        mana_max=30,
        actions={
            "Froideur d'Outretombe": "Sort", # gele
            "Claquement de Foudre": "Sort", # paralyse
            "Confusion": "Sort", # confond
            "Poing de Mana": "Sort"
        },
        recompense={"Mana max": 1, "Degat sort critique": 1, "Gold": 15 + combat.bonus_gold, "Materiau": "Ether Non-Newtonien"},
    )


@monstre("Clone de Verre")
def clone_de_verre(combat):
    return FicheMonstre(
        stigma_positif="Brisures",
        stigma_negatif="Fragile",
        force=2,
        intelligence=2,
        resistance=0,
        vies_supplementaires=1,
        vie_max=10,
        mana_max=30,
        actions={
            "Attaque Légère": "Technique",
            "Durcissement Argilite": "Technique", # augmente def
            "Tir Arcanique": "Sort"
        },
        recompense={"Vie max": 1, "Vie": 15, "Mana max": 1, "Mana": 15, "Gold": 15 + combat.bonus_gold, "Materiau": "Eclat de Verre"},
    )


@monstre("Métroïde")
def metroide(combat):
    return FicheMonstre(
        stigma_positif="Xénoanatomie",
        stigma_negatif="Cryophobia",
        force=0,
        intelligence=0,
        resistance=15,
        vies_supplementaires=0,
        vie_max=150,
        mana_max=40,
        actions={
            "Accrochage": "Technique", # paralyse et degat
            "Drain": "Technique", # draine vie
            "Impact": "Technique", # degat
        },
        recompense={"Taux sort critique": 1, "Mana max": 3, "Gold": 35 + combat.bonus_gold, "Materiau": "Fluide Alien"},
    )


@monstre("Trienun")
def trienun(combat):
    return FicheMonstre(
        stigma_positif="Fièvre du Jeu",
        stigma_negatif="Addict",
        force=5,
        intelligence=5,
        resistance=2,
        vies_supplementaires=0,
        vie_max=140,
        mana_max=40,
        actions={
            "Réglages d'Usine": "Sort", #soin
            "Volepièce": "Sort", # prend golds [x]
            "Bandit Manchot": "Sort", # lance 3 symbole. feu, glace ou paralysie ou les trois, pour lui ou joueur  [x]
            "Ruée vers l'or": "Sort" # donne mal jaune
        },
        recompense={"Taux sort critique": 1,"Taux coup critique": 1, "Gold": 50 + combat.bonus_gold, "Materiau": "Morceau de Cloche"},
    )


@monstre("Phénix Juvénile")
def phenix_juvenile(combat):
    return FicheMonstre(
        stigma_positif="Cendres du Renouveau",
        stigma_negatif="Faible Hematopoïèse",
        force=6,
        intelligence=0,
        resistance=8,
        vies_supplementaires=1,
        vie_max=100,
        mana_max=20,
        actions={
            "Souffle de Feu": "Technique",
            "Envol": "Technique", #reduit les chances de toucher de 30%  [x]
            "Coup du Foie": "Technique", # rend bléssé
            "Possession du mana": "Sort", # sorts coutent plus cher
            "Feu Regénérateur": "Sort",
            "Vents du Sud": "Sort",
        },
        recompense={"Taux coup critique": 1, "Vie max": 3, "Gold": 35 + combat.bonus_gold, "Materiau": "Ecaille de Phénix"},
    )


@monstre("Rochemikaze")
def rochemikaze(combat):
    return FicheMonstre(
        stigma_positif="Faveurs Explosives",
        stigma_negatif="Surveillé",
        force=5,
        intelligence=0,
        resistance=8,
        vies_supplementaires=0,
        vie_max=130,
        mana_max=40,
        actions={
            "Roulé-Boulet": "Technique", # confond
            "Jet de Magma": "Technique", # enflamme
            "Tomberoche": "Technique", # lapide
            "Regénération Basaltique": "Sort", # peut rendre bcp pv
            "Explosion": "Sort",
        },
        recompense={"Attaque": 1, "Vie": 20, "Gold": 35 + combat.bonus_gold, "Materiau": "Roche Glycérine"},
    )


@monstre("Loup de Glace")
def loup_de_glace(combat):
    return FicheMonstre(
        stigma_positif="Instincts de Bête",
        stigma_negatif="Cryolien",
        force=8,
        intelligence=8,
        resistance=6,
        vies_supplementaires=0,
        vie_max=125,
        mana_max=40,
        actions={
            "Morsure de Givre": "Technique", #peux geler
            "Coup de Griffe": "Technique", #peu degat, gros degat crit
            "Hurlement": "Technique", #pas de technique, pas de sorts  [x]
            "Cercueil de Neige": "Sort", # gele
        },
        recompense={"Degat coup critique": 2, "Vie max": 2, "Gold": 35 + combat.bonus_gold, "Materiau": "Poil Gelé"},
    )


@monstre("Voleur Félin")
def voleur_felin(combat):
    return FicheMonstre(
        stigma_positif="Auromancie",
        stigma_negatif="Copycat",
        force=8,
        intelligence=12,
        resistance=10,
        vies_supplementaires=0,
        vie_max=150,
        mana_max=50,
        actions={
            "Attire-Gold": "Technique", #prend du gold [x]
            "Lèche-Blessure": "Technique", # soin
            "Cat-astrophe": "Sort", #gele,enflamme,draine en mm temps [x]
            "Attaque Légère": "Technique",
            "Confusion": "Sort", # confond
            "Point Vital": "Sort", # gros degat critiques
            "Ruée vers l'or": "Sort", # donne mal jaune
            "Bombe Arcanique": "Sort",
        },
        recompense={"Mana max": 4, "Gold": 45 + combat.bonus_gold, "Degat sort critique": 2, "Materiau": "Moustache de Chat"},
    )


@monstre("Siffloteur")
def siffloteur(combat):
    return FicheMonstre(
        stigma_positif="Extinction de Voix",
        stigma_negatif="Sang Doré",
        force=0,
        intelligence=15,
        resistance=12,
        vies_supplementaires=0,
        vie_max=175,
        mana_max=50,
        actions={
            "Vents du Nord": "Sort", #gele
            "Vents du Sud": "Sort", #brule
            "Vents de l'Est": "Sort", #paralyse
            "Vents de l'Ouest": "Sort", #draine
            "Son Rapide": "Sort", #Fais perdre bcp pv
            "Son Lent": "Sort" #fais perdre bcp mana [x]
        },
        recompense={"Mana max": 4, "Gold": 45 + combat.bonus_gold, "Materiau": "Fragment Osseux"},
    )


@monstre("Lapin du Désastre")
def lapin_du_desastre(combat):
    return FicheMonstre(
        stigma_positif="Fertilité",
        stigma_negatif="Violence",
        force=14,
        intelligence=12,
        resistance=9,
        vies_supplementaires=1,
        vie_max=200,
        mana_max=50,
        actions={
            "Morsure": "Technique", #gros degats
            "Gel": "Sort", # gele
            "Giga Gel": "Sort", # peut geler sur longtemps
            "Oeuil Maudit": "Sort", #augmente cout mana
            "Carotte Magique": "Sort", #soin
            "Tout Feu Tout Flamme": "Sort", # combo electrique, pour le feu [x]
        },
        recompense={"Vie max": 4, "Gold": 45 + combat.bonus_gold, "Materiau": "Iris du Malheur"},
    )


@monstre("Cerf Voleur")
def cerf_voleur(combat):
    return FicheMonstre(
        stigma_positif="Rituel Vaudoo",
        stigma_negatif="Hématophobe",
        force=15,
        intelligence=15,
        resistance=14,
        vies_supplementaires=0,
        vie_max=150,
        mana_max=50,
        actions={
            "Coup Anti-Magie": "Technique", #attaaque meme si protection [x]
            "Attire-Magie": "Technique", #perd pm [x]
            "Coup de pierre": "Technique", # lapide
            "Vole-Ame": "Sort", # perd viemax [x]
            "Coup de Foudre": "Sort", # paralyse
            "Frappe Lourde": "Technique",  # gros degat, peu chance toucher
            "Poing Eclat": "Technique",  # rend blesse
            "Lèche-Blessure": "Technique", # soin
            "Ruée vers l'or": "Sort", # donne mal jaune
        },
        recompense={"Mana max": 4, "Gold": 45 + combat.bonus_gold, "Taux sort critique": 1, "Materiau": "Velour de Cervidé"},
    )


@monstre("Aspiratrésor Blindé")
def aspiratresor_blinde(combat):
    return FicheMonstre(
        stigma_positif="Circuits Logique",
        stigma_negatif="Surcharge Processeur",
        force=0,
        intelligence=0,
        resistance=15,
        vies_supplementaires=0,
        vie_max=50,
        mana_max=50,
        actions={
            "Aspiration": "Technique" # prend gold, mana + vie, manamax + viemax, taux critique sort+ attaque, force + intelligence, defence [x]
        },
        recompense={"Gold": 60 + combat.bonus_gold, "Intelligence": 1, "Defence": 1, "Taux sort critique": 1, "Taux coup critique":1, "Materiau": "Composants Electroniques"},
    )


@monstre("Gluant de Crystal")
def gluant_de_crystal(combat):
    return FicheMonstre(
        stigma_positif="Esotéricisme",
        stigma_negatif="Anisotropie",
        force=25,
        intelligence=25,
        resistance=25,
        vies_supplementaires=0,
        vie_max=300,
        mana_max=60,
        actions={
            "Gros Coup de Boule": "Technique",
            "Corruption": "Technique", #drain
            "Laser": "Technique",  # laser brule vie + mana [x]
            "Soin Avancé": "Sort", #soin
            "Flamme Avancée": "Sort", #brule
            "Rituel": "Sort", #perd vie, malediction vie + mana + item 2 tours [x]
        },
        recompense={"Mana max": 3, "Vie max": 3, "Materiau": "Eclat de Crystal"},
    )


@monstre("Sixenun")
def sixenun(combat):
    return FicheMonstre(
        stigma_positif="Carrousel Chanceux",
        stigma_negatif="Consummé",
        force=15,
        intelligence=0,
        resistance=22,
        vies_supplementaires=0,
        vie_max=200,
        mana_max=60,
        actions={
            "Roulette": "Technique", #lance roulette. mise ou pas = critique ou pas. si rouge, foule d'effet sur joueur. si vert, foule d'effet sur ennemi. [x]
            "Jet d'Argent": "Technique", #jette piece passe a travers sorts, 75% gros degats , 25% attrape gold. [x]
        },
        recompense={"Mana": 100, "Vie": 100, "Attaque": 1, "Gold": 60 + combat.bonus_gold, "Materiau": "Pilules de Roulette"},
    )


@monstre("Siffloteur de Jade")
def siffloteur_de_jade(combat):
    return FicheMonstre(
        stigma_positif="Bouclier Acoustique",
        stigma_negatif="Mégalovania",
        force=0,
        intelligence=25,
        resistance=12,
        vies_supplementaires=0,
        vie_max=220,
        mana_max=60,
        actions={
            "Tempêtes du Nord": "Sort", #gele + 50% plus de sorts [x]
            "Tempêtes du Sud": "Sort", #brule + 50% plus de techniques [x]
            "Tempêtes de l'Est": "Sort", #paralyse + 50% confus (plus item) [x]
            "Tempêtes de l'Ouest": "Sort", #draine + 50% mal jaune (action coute gold) [x]
            "Vacarme Rapide": "Sort", #Fais perdre bcp pv + 50% blesse [x]
            "Vacarme Lent": "Sort" #fais perdre bcp mana + 50% instable (plus de mana par sorts) [x]
        },
        recompense={"Degat sort critique": 2, "Degat coup critique": 2, "Gold": 30 + combat.bonus_gold, "Materiau": "Fragment de Jade"},
    )


@monstre("Aurelionite")
def aurelionite(combat):
    return FicheMonstre(
        stigma_positif="Toucher de Midas",
        stigma_negatif="Aveuglé",
        force=35,
        intelligence=35,
        resistance=0,
        vies_supplementaires=2,
        vie_max=250,
        mana_max=60,
        actions={
            "Lame Dorée": "Technique", #peut donner mal jaune
            "Ultralaser": "Technique", #peut bruler
            "Constructions du Zénith": "Technique", #soin
            "Oméga Gelure": "Sort", #gele
            "Oméga Lapidation": "Sort", #degat +lapide
            "Oméga Saignée": "Sort", # drain vie
        },
        recompense={"Defence": 2, "Gold": 100 + combat.bonus_gold, "Materiau": "Poussière Dorée Animée"},
    )


@monstre("Sacatrésor")
def sacatresor(combat):
    return FicheMonstre(
        stigma_positif="Manipulation",
        stigma_negatif="Inflammable",
        force=0,
        intelligence=0,
        resistance=10,
        vies_supplementaires=0,
        vie_max=300,
        mana_max=60,
        actions={
            "Gemme Rouge": "Technique", #soin
            "Gemme Bleue": "Technique", #vol mana [x]
        },
        recompense={"Vie max": 4, "Mana max": 4, "Taux sort critique": 1, "Taux coup critique":1, "Gold": 150 + combat.bonus_gold, "Materiau": "Gemme Bleue"},
    )


@monstre("Drone de Sécurité YucaTech Inc.")
def drone_de_securite_yucatech_inc(combat):
    return FicheMonstre(
        stigma_positif="Aucun",
        stigma_negatif="Aucun",
        stigma_bonus="Aucun",
        force=30,
        intelligence=38,
        resistance=24,
        vies_supplementaires=0,
        vie_max=200,
        mana_max=50,
        actions={
            "Laser Anti-Personnel": "Sort", # 5% de vie
            "Systeme de Support": "Sort", # soigne 50 pv
            "Protocole Supernova": "Sort",  # perd 10% de vie, inflige 10% de vie
            "Flash Bang": "Sort", # déconcentre
        },
        recompense={"Vie" : 75, "Mana": 25},
        etat_initial={"est_maudit_par_les_items": True, "est_maudit_par_les_items_nombre_tour": 999},
    )
