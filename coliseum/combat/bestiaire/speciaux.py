"""Rencontres particulières : mimiques, boss d'histoire, gardien, obélisque..."""

from coliseum.combat.bestiaire.fiche import FicheMonstre, monstre


@monstre("Pierre")
def pierre(combat):
    return FicheMonstre(
        stigma_positif="Plus d'un Tour",
        stigma_negatif="Gluantin",
        force=2,
        intelligence=10,
        resistance=3,
        vies_supplementaires=99,
        vie_max=100,
        mana_max=50,
        actions={
            "Sables du Temps": "Technique",
            "Coup de Boule": "Technique",
            "Etranglement": "Technique", # rend muet
            "Soin": "Sort",
            "Flamme": "Sort"
        },
        recompense={"Vie max": 2},
    )


@monstre("???")
def inconnu(combat):
    return FicheMonstre(
        recompense={"Attaque": 2, "Defence": 2, "Intelligence": 2, "Gold": 100 + combat.bonus_gold},
    )


@monstre("Gluantcelot")
def gluantcelot(combat):
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


@monstre("Volontée Persistante")
def volontee_persistante(combat):
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


@monstre("Volontée Instable")
def volontee_instable(combat):
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


@monstre("Volontée Indomptable")
def volontee_indomptable(combat):
    return FicheMonstre(
        stigma_positif="Gluantesque",
        stigma_negatif="Gluantin",
        force=0,
        intelligence=0,
        resistance=0,
        vies_supplementaires=1,
        vie_max=3000,
        mana_max=30,
        actions={
            "Coup de Boule": "Technique",
            "Etranglement": "Technique", # rend muet
            "Soin": "Sort",
            "Flamme": "Sort"
        },
        recompense={"Vie max": 2, "Gold": 15 + combat.bonus_gold},
    )


@monstre("Divine Faucheuse")
def divine_faucheuse(combat):
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


def _finir_mimique(modele):
    liste_action_supplementaire = {}
    if modele.numero_de_letage == 2:
        modele.monstre_nom = "Mimique du Massacre : Ymir"
        modele.stigma_monstre_bonus = "Berserker"
        liste_action_supplementaire = {
            "Coup de Boule": "Technique",
            "Etranglement": "Technique", # rend muet
            "Soin": "Sort",
            "Flamme": "Sort",
            "Tout Feu Tout Flamme": "Sort", # combo electrique, pour le feu [x]
            "Feu Regénérateur": "Sort", # soin
            "Poing de Feu": "Technique", # brule
            "Brulevent": "Technique", # rend muet
            "Frappe Lourde": "Technique",  # gros degat, peu chance toucher
            "Poing Eclat": "Technique",  # rend blesse
            "Durcissement Argilite": "Technique",  # plus de defence  [x]
            "Eboulis": "Technique",  # peux lapider
            "Poing de Mana": "Sort",
            "Froideur d'Outretombe": "Sort", # gele
            "Claquement de Foudre": "Sort", # paralyse
            "Confusion": "Sort", # confond
            "Poing de Mana": "Sort",
            "Attaque Légère": "Technique",
            "Durcissement Argilite": "Technique", # augmente def
            "Tir Arcanique": "Sort"
        }
    elif modele.numero_de_letage == 4:
        modele.monstre_nom = "Mimique de l'Evolution : Frankenstein"
        modele.stigma_monstre_bonus = "Concoctions"
        liste_action_supplementaire = {
            "Accrochage": "Technique", # paralyse et degat
            "Drain": "Technique", # draine vie
            "Impact": "Technique", # degat
            "Réglages d'Usine": "Sort", #soin
            "Volepièce": "Sort", # prend golds [x]
            "Bandit Manchot": "Sort", # lance 3 symbole. feu, glace ou paralysie ou les trois, pour lui ou joueur  [x]
            "Ruée vers l'or": "Sort", # donne mal jaune
            "Souffle de Feu": "Technique",
            "Envol": "Technique", #reduit les chances de toucher de 30%  [x]
            "Coup du Foie": "Technique", # rend bléssé
            "Possession du mana": "Sort", # sorts coutent plus cher
            "Roulé-Boulet": "Technique", # confond
            "Jet de Magma": "Technique", # enflamme
            "Tomberoche": "Technique", # lapide
            "Regénération Basaltique": "Sort", # peut rendre bcp pv
            "Explosion": "Sort",
            "Morsure de Givre": "Technique", #peux geler
            "Coup de Griffe": "Technique", #peu degat, gros degat crit
            "Hurlement": "Technique", #pas de technique, pas de sorts  [x]
            "Cercueil de Neige": "Sort", # gele
        }
    elif modele.numero_de_letage == 6:
        modele.monstre_nom = "Mimique de l'Exaltation : Nostalgia Gaïus"
        modele.stigma_monstre_bonus = "Apathie"
        liste_action_supplementaire = {
            "Attire-Gold": "Technique", #prend du gold [x]
            "Lèche-Blessure": "Technique", # soin
            "Cat-astrophe": "Sort", #gele,enflamme,draine en mm temps [x]
            "Point Vital": "Sort", # gros degat critiques
            "Vents du Nord": "Sort", #gele
            "Vents du Sud": "Sort", #brule
            "Vents de l'Est": "Sort", #paralyse
            "Vents de l'Ouest": "Sort", #draine
            "Son Rapide": "Sort", #Fais perdre bcp pv
            "Son Lent": "Sort", #fais perdre bcp mana [x]
            "Morsure": "Technique", #gros degats
            "Gel": "Sort", # gele
            "Giga Gel": "Sort", # peut geler sur longtemps
            "Oeuil Maudit": "Sort", #augmente cout mana
            "Carotte Magique": "Sort", #soin
            "Coup Anti-Magie": "Technique", #attaaque meme si protection [x]
            "Attire-Magie": "Technique", #perd pm [x]
            "Coup de pierre": "Technique", # lapide
            "Vole-Ame": "Sort", # perd viemax [x]
            "Coup de Foudre": "Sort", # paralyse
            "Aspiration": "Technique" # prend gold, mana + vie, manamax + viemax, taux critique sort+ attaque, force + intelligence, defence [x]
        }
    elif modele.numero_de_letage in [8, 10]:
        modele.monstre_nom = "Mimique du Déïcide : Lucifer"
        modele.stigma_monstre_bonus = "Etoile"
        if modele.numero_de_letage == 10:
            modele.monstre_nom = "Mimique du Désir : Géhenna"
            modele.stigma_monstre_bonus = "Flammes du Désir"
        liste_action_supplementaire = {
            "Gros Coup de Boule": "Technique",
            "Corruption": "Technique", #drain
            "Laser": "Technique",  # laser brule vie + mana [x]
            "Soin Avancé": "Sort", #soin
            "Flamme Avancée": "Sort", #brule
            "Rituel": "Sort", #perd vie, malediction vie + mana + item 2 tours [x]
            "Roulette": "Technique", #lance roulette. mise ou pas = critique ou pas. si rouge, foule d'effet sur joueur. si vert, foule d'effet sur ennemi. [x]
            "Jet d'Argent": "Technique", #jette piece passe a travers sorts, 75% gros degats , 25% attrape gold. [x]
            "Tempêtes du Nord": "Sort", #gele + 50% plus de sorts [x]
            "Tempêtes du Sud": "Sort", #brule + 50% plus de techniques [x]
            "Tempêtes de l'Est": "Sort", #paralyse + 50% confus (plus item) [x]
            "Tempêtes de l'Ouest": "Sort", #draine + 50% mal jaune (action coute gold) [x]
            "Vacarme Rapide": "Sort", #Fais perdre bcp pv + 50% blesse [x]
            "Vacarme Lent": "Sort", #fais perdre bcp mana + 50% instable (plus de mana par sorts) [x]
            "Lame Dorée": "Technique", #peut donner mal jaune
            "Ultralaser": "Technique", #peut bruler
            "Constructions du Zénith": "Technique", #soin
            "Oméga Gelure": "Sort", #gele
            "Oméga Lapidation": "Sort", #degat +lapide
            "Oméga Saignée": "Sort", # drain vie
            "Gemme Rouge": "Technique", #soin
            "Gemme Bleue": "Technique", #vol mana [x]
        }
    for action in liste_action_supplementaire:
        modele.monstre_liste_actions[action] = liste_action_supplementaire[action]


@monstre("Mimique")
def mimique(combat):
    return FicheMonstre(
        stigma_positif="Abomination",
        stigma_negatif="Homoncule",
        force=round(10 * combat.numero_etage),
        intelligence=round(10 * combat.numero_etage),
        resistance=round(10 * combat.numero_etage),
        vies_supplementaires=0,
        vie_max=round((60 * combat.numero_etage) + 100),
        mana_max=100,
        actions={
            "Avale": "Technique", #bcp degat
            "Vide": "Sort", # plus technique plus sorts plus item [x]
            "Engloutis": "Sort", #soin
            "Mache": "Sort", #drain saignee
        },
        recompense={"Taux esquive": 1, "Mana max": 10, 
                                          "Vie max": 10, "Degat sort critique": 10, 
                                          "Degat coup critique": 10, "Gold": 25 + combat.bonus_gold, "Materiau": "Fragment Insatiable"},
        finition=_finir_mimique,
    )


@monstre("Minaraï")
def minarai(combat):
    return FicheMonstre(
        stigma_positif="Sort Chanceux",
        stigma_negatif="Anxiété Sociale",
        stigma_bonus="Mal Jaune",
        force=10,
        intelligence=20,
        resistance=12,
        vies_supplementaires=1,
        vie_max=300,
        mana_max=75,
        actions={
            "Faisceau de l'Eclair": "Sort",  #paralyse
            "Thermosphère de la Fournaise": "Sort", #brule
            "Pic Glacial": "Sort", #gele
            "Création Obsidienne": "Sort", #lapide
            "Explosion Maitrisée": "Sort", #gros dégats
            "Dance Parasite": "Sort", #saigne
            "Sonata Sincère": "Sort", #soigne
            "Magie Ténébreuse": "Sort" #empeche sort et technique [x]
        },
        recompense={"Red coin": 1, "Méga Tirage": 1, "Gold": 200 + combat.bonus_gold, "Taux sort critique": 5, "Intelligence": 5, "Endurance": 10},
    )


@monstre("Noa")
def noa(combat):
    return FicheMonstre(
        stigma_positif="Coeur Inferno",
        stigma_negatif="Inconsolable Rage",
        stigma_bonus="Nordique",
        force=0,
        intelligence=0,
        resistance=0,
        vies_supplementaires=0,
        vie_max=1,
        mana_max=1,
        actions={
            "Rien": "Technique", 
        },
        recompense={"Red coin": 1, "Tirage": 1, "Taux sort critique": 12, "Taux coup critique": 12},
        bonus_de_vie_de_l_etage=False,
    )


@monstre("Ministre du Mana")
def ministre_du_mana(combat):
    return FicheMonstre(
        stigma_positif="Hardi",
        stigma_negatif="Fatigue",
        stigma_bonus="Ministre de la Magie",
        force=30,
        intelligence=38,
        resistance=24,
        vies_supplementaires=1,
        vie_max=488,
        mana_max=100,
        actions={
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
        recompense={"Red coin": 1, "Méga Tirage": 1, "Vie max": 20, 
                                   "Mana max": 20, "Gold": 400 + combat.bonus_gold, "Endurance": 10},
    )


@monstre("Yvan")
def yvan(combat):
    return FicheMonstre(
        stigma_positif="Aucun",
        stigma_negatif="Aucun",
        stigma_bonus="Aucun",
        force=30,
        intelligence=38,
        resistance=24,
        vies_supplementaires=0,
        vie_max=800,
        mana_max=1,
        actions={
            "Attaque Lourde": "Technique",
            "Lame Courageuse": "Technique", #gros degats
            "Crystal Elémentaire": "Technique",  # inflige lourd brule ou gele [x]
            "Remede Divin": "Technique", #soin
            "Combo Misérable": "Technique", #combo electrique , mais maudit [x]
        },
        recompense={"Red coin": 1, "Méga Tirage": 1, "Vie max": 20, 
                                   "Mana max": 20, "Gold": 400 + combat.bonus_gold, "Endurance": 10},
    )


@monstre("Armée des Anges")
def armee_des_anges(combat):
    return FicheMonstre(
        stigma_positif="Aucun",
        stigma_negatif="Aucun",
        stigma_bonus="Aucun",
        force=30,
        intelligence=38,
        resistance=24,
        vies_supplementaires=5,
        vie_max=150,
        mana_max=20,
        actions={
            "Attaque Lourde": "Technique",
            "Lame Courageuse": "Technique", #gros degats
            "Crystal Elémentaire": "Technique",  # inflige lourd brule ou gele [x]
            "Remede Divin": "Technique", #soin
            "Combo Misérable": "Technique", #combo electrique , mais maudit [x]
            "Houken": "Sort", #draine vie
            "Sonata Sincère": "Sort", #soigne

        },
        recompense={"Red coin": 1, "Méga Tirage": 1, "Vie max": 20, 
                                   "Mana max": 20, "Gold": 400 + combat.bonus_gold, "Endurance": 10},
    )


@monstre("Armée de la Fin")
def armee_de_la_fin(combat):
    return FicheMonstre(
        stigma_positif="Aucun",
        stigma_negatif="Aucun",
        stigma_bonus="Aucun",
        force=30,
        intelligence=38,
        resistance=24,
        vies_supplementaires=3,
        vie_max=250,
        mana_max=1,
        actions={
            "Attaque Lourde": "Technique",
            "Lame Courageuse": "Technique", #gros degats
            "Crystal Elémentaire": "Technique",  # inflige lourd brule ou gele [x]
            "Remede Divin": "Technique", #soin
            "Combo Misérable": "Technique", #combo electrique , mais maudit [x]
            "Houken": "Sort", #draine vie
            "Sonata Sincère": "Sort", #soigne
            "Magie Abyssale": "Sort", #scelle sort et technique, draine 10% pm [x]
            "Eveil de Runes": "Sort", # differents effet selon la rune invoquée [x]
        },
        recompense={"Red coin": 1, "Méga Tirage": 1, "Vie max": 20, 
                                   "Mana max": 20, "Gold": 400 + combat.bonus_gold, "Endurance": 10},
    )


@monstre("Archange Michael")
def archange_michael(combat):
    return FicheMonstre(
        stigma_positif="Aucun",
        stigma_negatif="Aucun",
        stigma_bonus="Aucun",
        force=30,
        intelligence=38,
        resistance=24,
        vies_supplementaires=0,
        vie_max=600,
        mana_max=1,
        actions={
            "Attaque Lourde": "Technique",
            "Lame Courageuse": "Technique", #gros degats
            "Crystal Elémentaire": "Technique",  # inflige lourd brule ou gele [x]
            "Remede Divin": "Technique", #soin
            "Combo Misérable": "Technique", #combo electrique , mais maudit [x]
            "Houken": "Sort", #draine vie
            "Sonata Sincère": "Sort", #soigne
            "Faisceau de la Mort Blanche": "Sort", #paralyse
            "Magie Abyssale": "Sort", #scelle sort et technique, draine 10% pm [x]
            "Eveil de Runes": "Sort", # differents effet selon la rune invoquée [x]
            "Dance Créatrice": "Sort", #drain
        },
        recompense={"Red coin": 1, "Méga Tirage": 1, "Vie max": 20, 
                                   "Mana max": 20, "Gold": 400 + combat.bonus_gold, "Endurance": 10},
    )


@monstre("Pierre de Désir")
def pierre_de_desir(combat):
    return FicheMonstre(
        stigma_positif="",
        stigma_negatif="",
        stigma_bonus="",
        force=50,
        intelligence=50,
        resistance=20,
        vies_supplementaires=2,
        vie_max=1500,
        mana_max=9999,
        actions={
            "Lame Ultime": "Technique", #gros degats
            "Bouclier Ultime": "Technique", #reprend beaucoup de vie
            "Laser Ultime": "Technique", #moyen degat et feu
            "Sort Ultime": "Sort", #gros degat, perd mana [x]
            "Ultime Ultime": "Sort", # impossible d'utiliser sor
        },
        recompense={"Red coin": 1, "Tirage": 1, "Gold": 99999, 
                                   "Attaque": 99999, "Intelligence": 99999, "Endurance": 99999},
    )
