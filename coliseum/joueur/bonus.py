"""Bonus accordés au joueur : livraisons du village, enchantements aléatoires, souvenirs de techniques et de sorts."""

import random

from coliseum import services
from coliseum.donnees.actions import LISTESORTS, LISTETECHNIQUES
from coliseum.donnees.personnages import UPPGRADESPOSSIBLES


def PasseDeLivraisonABonus():
    print("")
    liste_de_uppgrade_a_afficher = {}
    for uppgrade in UPPGRADESPOSSIBLES:
        level_de_luppgrade = services.Sove.ModifieLivraisonDansSove("Nombre", uppgrade, None)
        if level_de_luppgrade != 0:
            liste_de_uppgrade_a_afficher[uppgrade] = level_de_luppgrade

    if len(liste_de_uppgrade_a_afficher) != 0:
        for uppgrade in liste_de_uppgrade_a_afficher:
            if uppgrade not in ["Clé", "Carte", "Emblème de la Fin", "Sacoche"]:
                niveau_de_luppgrade = liste_de_uppgrade_a_afficher[uppgrade]
                print(f"{uppgrade} de niveau {niveau_de_luppgrade}")
                if uppgrade == "Chapeau":
                    gain = 4 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain} points d'intelligence !\n")
                    services.Player.points_dintelligence += gain
                elif uppgrade == "Boucles d'Oreille":
                    gain = 2 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain}% de chance supplémentaire de faire des sorts critiques !\n")
                    services.Player.taux_sort_critique += gain
                elif uppgrade == "Collier":
                    gain = 2 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain}% de chance supplémentaire de faire des techniques critiques !\n")
                    services.Player.taux_coup_critique += gain
                elif uppgrade == "Cotte de Maille":
                    gain = 4 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain} points de défence !\n")
                    services.Player.points_de_defence += gain
                elif uppgrade == "Bracelet":
                    gain = 4 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain} points de force !\n")
                    services.Player.points_de_force += gain
                elif uppgrade == "Gants":
                    gain = 3 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain} degats supplementaires lorsque vous effectuez un coup critique !\n")
                    services.Player.degat_coup_critique += gain
                elif uppgrade == "Anneau":
                    gain = 3 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain} degats supplementaires lorsque vous effectuez un sort critique !\n")
                    services.Player.degat_sort_critique += gain
                elif uppgrade == "Bottes":
                    gain = niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain}% de chance de faire une esquive !\n")
                    services.Player.taux_desquive += gain
                elif uppgrade == "Fiole de Sève":
                    gain = 5 * niveau_de_luppgrade
                    print(f"     *Vous buvez immédiatement la concoction et gagnez {gain} points de mana max !\n")
                    services.Player.points_de_vie_max += gain
                    services.Player.points_de_vie += gain
                elif uppgrade == "Fiole de Rosée":
                    gain = 5 * niveau_de_luppgrade
                    print(f"     *Vous buvez immédiatement la concoction et gagnez {gain} points de vie max !\n")
                    services.Player.points_de_mana_max += gain
                    services.Player.points_de_mana += gain
                elif uppgrade == "Tisane de Racine":
                    gain = 2 * niveau_de_luppgrade
                    print(f"     *Vous buvez immédiatement la concoction et votre corps récupere désormais {gain} points de mana supplémentaires lorsque il regagne des points de mana, et ce pour toute les sources !\n")
                    services.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Tisane de Racine"] = gain
                elif uppgrade == "Tisane d'Ecorce":
                    gain = 2 * niveau_de_luppgrade
                    print(f"     *Vous buvez immédiatement la concoction et votre corps récupere désormais {gain} points de vie supplémentaires lorsque il regagne des points de vie, et ce pour toute les sources !\n")
                    services.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Tisane d'Ecorce"] = gain
                elif uppgrade == "Charge de Feu":
                    gain = 5 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain}% de dégat supplémentaire pour vos attaques et sorts de feu !\n")
                    services.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Charge de Feu"] = gain
                elif uppgrade == "Charge de Glace":
                    gain = 5 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain}% de dégat supplémentaire pour vos attaques et sorts de glace !\n")
                    services.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Charge de Glace"] = gain
                elif uppgrade == "Charge de Foudre":
                    gain = 5 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain}% de dégat supplémentaire pour vos attaques et sorts de foudre !\n")
                    services.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Charge de Foudre"] = gain
                elif uppgrade == "Charge de Terre":
                    gain = 5 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain}% de dégat supplémentaire pour vos attaques et sorts de terre !\n")
                    services.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Charge de Terre"] = gain
                elif uppgrade == "Charge de Chair":
                    gain = 5 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain}% de dégat supplémentaire pour vos attaques et sorts physiques !\n")
                    services.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Charge de Chair"] = gain
                elif uppgrade == "Charge de Sang":
                    gain = 5 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain}% de dégat supplémentaire pour vos attaques et sorts de sang !\n")
                    services.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Charge de Sang"] = gain
                elif uppgrade == "Ration Jindagee":
                    gain = 2 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain} feuille(s) jindagee !\n")
                    services.Player.items_possedes["Feuille Jindagee"] += gain
                elif uppgrade == "Ration Jindagee Raffinée":
                    gain = niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain} fruit(s) jindagee !\n")
                    services.Player.items_possedes["Fruit Jindagee"] += gain
                elif uppgrade == "Ration Aatma":
                    gain = 2 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain} feuille(s) aatma !\n")
                    services.Player.items_possedes["Feuille Aatma"] += gain
                elif uppgrade == "Ration Aatma Rafinée":
                    gain = niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain} fruit(s) aatma !\n")
                    services.Player.items_possedes["Fruit Aatma"] += gain
                elif uppgrade == "Ration Cristalline":
                    gain = 2 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain} crystaux élémentaires !\n")
                    services.Player.items_possedes["Crystal Elémentaire"] += gain
                elif uppgrade == "Ration d'Hydromel":
                    gain = 2 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain} bouteille(s) d'hydromel !\n")
                    services.Player.items_possedes["Hydromel"] += gain
                elif uppgrade == "Ration Ambroisie":
                    gain = 2 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain} bouteille(s) d'ambroisie !\n")
                    services.Player.items_possedes["Ambroisie"] += gain
                elif uppgrade == "Ration Explosive":
                    gain = 2 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain} unité(s) de poudre explosive !\n")
                    services.Player.items_possedes["Poudre Explosive"] += gain
                elif uppgrade == "Ration Explosive Raffinée":
                    gain = niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain} unité(s) de roche explosive !\n")
                    services.Player.items_possedes["Roche Explosive"] += gain
                elif uppgrade == "Pack de Fléchettes":
                    gain = 2 * niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain} unité(s) de fléchettes bleues/rouges !\n")
                    services.Player.items_possedes["Fléchette Rouge"] += gain
                    services.Player.items_possedes["Fléchette Bleue"] += gain
                elif uppgrade == "Pack de Flèches":
                    gain = niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain} unité(s) de flèches bleues/rouge !\n")
                    services.Player.items_possedes["Flèche Rouge"] += gain
                    services.Player.items_possedes["Flèche Bleue"] += gain
                elif uppgrade == "Pack Premier Tour":
                    gain = niveau_de_luppgrade
                    print(f"     *Vous gagnez {gain} assemblage de plusieurs objets a utiliser au premier tour !\n")
                    services.Player.items_possedes["Fiole de Poison"] += gain
                    services.Player.items_possedes["Sève d'Exorcisme"] += gain
                    services.Player.items_possedes["Sève d'Absolution"] += gain
                    services.Player.items_possedes["Mutagène Rouge"] += gain
                    services.Player.items_possedes["Mutagène Vert"] += gain
                    services.Player.items_possedes["Mutagène Bleu"] += gain
                elif uppgrade == "Médaillon de Leprechaun":
                    gain = 5 * niveau_de_luppgrade
                    print(f"     *Vous obtenez {gain}% de chance supplémentaire de gagner un materiau a la fin d'un combat !\n")
                    services.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Médaillon de Leprechaun"] = gain
                elif uppgrade == "Noyau d'Aurelionite":
                    gain = 10 * niveau_de_luppgrade
                    print(f"     *Vos gains de gold augmentent de {gain}% !")
                    services.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Noyau d'Aurelionite"] = gain

    print("Une carte magique.\n")


def EnchantementAleatoire():
    liste_de_choix_possibles_sorts_ou_technique = [1, 2]

    liste_techniques_affixables = []
    for technique in services.Player.techniques_possedes:
        if technique in LISTETECHNIQUES or technique == "Attaque Lourde":
            liste_techniques_affixables.append(technique)
    if len(liste_techniques_affixables) == 0:
        liste_de_choix_possibles_sorts_ou_technique.remove(2)

    liste_sorts_affixables = []
    for sort in services.Player.sorts_possedes:
        if sort in LISTESORTS or sort == "Missile Arcanique":
            liste_sorts_affixables.append(sort)
    if len(liste_sorts_affixables) == 0:
        liste_de_choix_possibles_sorts_ou_technique.remove(1)
        

    if len(liste_de_choix_possibles_sorts_ou_technique) == 0:
        choix = 0
    else:
        choix = random.choice(liste_de_choix_possibles_sorts_ou_technique)

    
    if choix == 1:
        numero = 1
        for sort in liste_sorts_affixables :
            numero += 1
        choix = random.randint(2, numero)
        sort_choisie = liste_sorts_affixables[(choix - 2)]
        liste_affix = ["~Rouge~", # +2 vie
                    "~Carmin~", # +4 vie
                    "~Violet~", # +2 mana
                    "~Pourpre~", # +4 mana
                    "~Jaune~", # +2 endurance
                    "~Doré~", # +4 endurance
                    "~Lolipop~", # +1 vie mana endurance
                    "~Bubblegum~", # +2 vie mana endurance
                    "~Escargot~", # +1% degat technique
                    "~Limace~", # +1% degat sorts
                    "~Citronnier~", # +0.5 degat critique technique
                    "~Citron~", # +1 degat critique technique
                    "~Cerisier~", # +0.5 degat critique sort
                    "~Cerise~", # +1 degat critique sort
                    "~Mars~", # +0.5% chance de bruler
                    "~Neptune~", # +0.5% chance de geler
                    "~Pluton~", # +0.25% chance de paralyser
                    "~Lune~", # +0.5% chance de lapider
                    "~Mercure~", # +0.5% chance de drain
                    "~Ordre~", # peut bruler
                    "~Aveugle~", # peut geler
                    "~Limitation~", # peut lapider
                    "~Transcendance~", # peut paralyser
                    "~Eveil~", # peut drainer
                    "~Antithèse~", # 15% chance d'arreter le gel
                    "~Chaotique~", # 15% chance d'arreter la brulure
                    "~Tache~", # 15% chance d'arreter la blessure
                    "~Rature~", # 15% chance d'arreter la deconcentration
                    "~Brouillon~", # 15% chance d'arreter la confusion
                    "~Paragraphe~", # 6% chance d'enlever gel + brulure + blessure + deconcentration + confusion
                    "~Magnum-Opus~", # 6% chance de donner numero_etage * 5 golds
                    "~Agrume~", # 6% chance d'être béni
                    "~Raisin~", # 6% chance d'être en folie
                    "~Durian~", # 6% chance d'être en furie
                    "~Gingembre~", # 6% chance d'être jindagee 2 tours
                    "~Mandragore~", # 6% chance d'être aatma 2 tours
                    "~Nigredo~", # 2% chance reprendre full vie
                    "~Albédo~", # 2% chance reprendre full mana
                    "~Citrinitas~", # 2% chance reprendre full endurance
                    "~Chrysalide~", # 2% chance devenir invincible 2 tours
                    ]
        #enelever les effets elementaires en doublons
        sort_choisi_transformee_en_liste = list(sort_choisie.split())
        if "Faisceau" in sort_choisi_transformee_en_liste :
            liste_affix.remove("~Limitation~")
        elif "Thermosphère" in sort_choisi_transformee_en_liste :
            liste_affix.remove("~Ordre~")
        elif "Pic" in sort_choisi_transformee_en_liste :
            liste_affix.remove("~Aveugle~")
        elif "Création" in sort_choisi_transformee_en_liste :
            liste_affix.remove("~Transcendance~")
        elif "Dance" in sort_choisi_transformee_en_liste :
            liste_affix.remove("~Eveil~")

        nombre_aleatoire = random.randint(0, (len(liste_affix) - 1))
        affix_choisi = liste_affix[nombre_aleatoire]

        services.Player.sorts_possedes.remove(sort_choisie)
        sort_choisie += f" {affix_choisi}"
        services.Player.sorts_possedes.append(sort_choisie)
        services.Save.SaveTheGameSansAffichage()

    elif choix == 2 :
        numero = 1
        for tut in liste_techniques_affixables :
            numero += 1
        choix = random.randint(2, numero)
        technique_choisie = liste_techniques_affixables[(choix - 2)]
        liste_affix = ["~Rouge~", # +2 vie
                    "~Carmin~", # +4 vie
                    "~Violet~", # +2 mana
                    "~Pourpre~", # +4 mana
                    "~Jaune~", # +2 endurance
                    "~Doré~", # +4 endurance
                    "~Lolipop~", # +1 vie mana endurance
                    "~Bubblegum~", # +2 vie mana endurance
                    "~Escargot~", # +1% degat technique
                    "~Limace~", # +1% degat sorts
                    "~Citronnier~", # +0.5 degat critique technique
                    "~Citron~", # +1 degat critique technique
                    "~Cerisier~", # +0.5 degat critique sort
                    "~Cerise~", # +1 degat critique sort
                    "~Mars~", # +0.5% chance de bruler
                    "~Neptune~", # +0.5% chance de geler
                    "~Pluton~", # +0.25% chance de paralyser
                    "~Lune~", # +0.5% chance de lapider
                    "~Mercure~", # +0.5% chance de drain
                    "~Ordre~", # peut bruler
                    "~Aveugle~", # peut geler
                    "~Limitation~", # peut lapider
                    "~Transcendance~", # peut paralyser
                    "~Eveil~", # peut drainer
                    "~Antithèse~", # 15% chance d'arreter le gel
                    "~Chaotique~", # 15% chance d'arreter la brulure
                    "~Tache~", # 15% chance d'arreter la blessure
                    "~Rature~", # 15% chance d'arreter la deconcentration
                    "~Brouillon~", # 15% chance d'arreter la confusion
                    "~Paragraphe~", # 6% chance d'enlever gel + brulure + blessure + deconcentration + confusion
                    "~Magnum-Opus~", # 6% chance de donner numero_etage * 5 golds
                    "~Agrume~", # 6% chance d'être béni
                    "~Raisin~", # 6% chance d'être en folie
                    "~Durian~", # 6% chance d'être en furie
                    "~Gingembre~", # 6% chance d'être jindagee 2 tours
                    "~Mandragore~", # 6% chance d'être aatma 2 tours
                    "~Nigredo~", # 2% chance reprendre full vie
                    "~Albédo~", # 2% chance reprendre full mana
                    "~Citrinitas~", # 2% chance reprendre full endurance
                    "~Chrysalide~", # 2% chance devenir invincible 2 tours
                    ]
        #enelever les effets elementaires en doublons
        technique_choisie_transformee_en_liste = list(technique_choisie.split())
        if "Lance" in technique_choisie_transformee_en_liste :
            liste_affix.remove("~Limitation~")
        elif "Bô" in technique_choisie_transformee_en_liste :
            liste_affix.remove("~Ordre~")
        elif "Katana" in technique_choisie_transformee_en_liste :
            liste_affix.remove("~Aveugle~")
        elif "Corne" in technique_choisie_transformee_en_liste :
            liste_affix.remove("~Transcendance~")
        elif "Dague" in technique_choisie_transformee_en_liste :
            liste_affix.remove("~Eveil~")

        nombre_aleatoire = random.randint(0, (len(liste_affix) - 1))
        affix_choisi = liste_affix[nombre_aleatoire]
        services.Player.techniques_possedes.remove(technique_choisie)
        technique_choisie += f" {affix_choisi}"
        services.Player.techniques_possedes.append(technique_choisie)
        services.Save.SaveTheGameSansAffichage()


def DonneSouvenirsDeTechniqueEtSorts():
    liste_action_souvenues = services.Sove.ModifieActionsConnuesDansSove("Donne")
    if len(liste_action_souvenues) != 0:
        print("Vous prenez un instant pour vous souvenir de ce que vous avez vu dans le Colysée du Champ du Crépuscule...")
        services.Affichage.EntreePourContinuer()
        print("Vous vous rappelez...")
        for action in liste_action_souvenues:
            if action in LISTETECHNIQUES:
                print(f"...de la technique [{action}] !")
                services.Player.techniques_possedes.append(action)
            if action in LISTESORTS:
                print(f"...du sort [{action}] !")
                services.Player.sorts_possedes.append(action)
        services.Affichage.EntreePourContinuer()
