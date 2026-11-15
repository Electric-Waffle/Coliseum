"""Arrivée au village après la mort ou la fin d'une run."""

import random
import time
from turtle import (
    clear,
)

from coliseum import services
from coliseum.audio import PlaySound, StopAllMusic
from coliseum.commerce.materiaux import AugmenteMateriauDansDictionnaire
from coliseum.donnees.artefacts import ARTEFACTFATALITE, ARTEFACTMELIORATIF, ARTEFACTSOPHIQUE


def CheckForKIA():
    if "KIA" in services.Player.player_tags:
        services.Player.player_tags.remove("KIA")
        services.Affichage.ShowDeath()


def PrepareTheVillage():
    #affiche l'arrivée
    StopAllMusic()
    if "Fantome" in services.Player.player_tags:
        services.Player.player_tags.remove("Fantome")

        print("[AVATAR DETECTE]")
        print("[REPRISE DU SYSTEME]")
        services.Affichage.EntreePourContinuer()
        print("Vous avez l'impression de flotter dans le vide.")
        services.Affichage.EntreePourContinuer()
        print("Soudainement, vous vous sentez écrasé, frappé, jeté contre les barreaux gluants d'une cage invisible.")
        services.Affichage.EntreePourContinuer()
        if services.Player.stigma_negatif == "Indigérable":
            print("Vous commencez a sentir vos items et votre être tout entier être réduit en bouillie, transformés en déchets, mais parce que vous êtes Indigérable, tout est entièrement détruit.")
        else:
            print("Vous commencez a sentir vos items et votre être tout entier être réduit en bouillie, transformés en déchets.")
        services.Affichage.EntreePourContinuer()
        print("Et puis..")
        services.Affichage.EntreePourContinuer()
        print("..plus rien.")
        services.Affichage.EntreePourContinuer()
        print("Vous entendez alors un son particulier, celui du vent contre le sol, et le bruit de pas des gens qui déambulent.")
        services.Affichage.EntreePourContinuer()
        print("Alors, vous ouvrez les yeux.")
        services.Affichage.EntreePourContinuer()
        time.sleep(2)
    
    
    #changer le numero et nom de l'étage, amener les characteristiques du perso a 0.
    #garder artefacts, nombre de monstre vaincus, redcoin et gold, materiaux
    services.Player.numero_de_letage = -1
    services.Player.nom_de_letage = "Champs du Crépuscule"

    services.Player.points_de_vie = 0

    services.Player.points_de_mana = 0
    services.Player.points_dendurance = 0
    
    services.Player.taux_coup_critique = 0
    services.Player.taux_sort_critique = 0
    services.Player.degat_coup_critique = 0
    services.Player.degat_sort_critique = 0
    services.Player.taux_desquive = 0
    services.Player.sorts_possedes = []
    services.Player.techniques_possedes = []
    services.Player.talents_possedes = []
    services.Player.stigma_bonus = ""
    services.Player.stigma_negatif = ""
    services.Player.stigma_positif = ""
    services.Player.position_x = 0
    services.Player.position_y = 0


        
    services.Player.affronte_un_boss = False
    services.Player.quete = "None"
    services.Player.possede_la_cle = False
    if services.FloorMaker.carte_ouverte:
        clear()
    services.FloorMaker.FloorBlueprint = ({1: {'position_x': 0, 'position_y': 0, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'ENTREE'}, 
                            #base
                            2: {'position_x': 2, 'position_y': 0, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'VILLAGE_QUARTIERS'}, 
                            3: {'position_x': -2, 'position_y': 0, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'VILLAGE_CHAMPS'}, 
                            4: {'position_x': 0, 'position_y': 2, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'VILLAGE_ARENE'}, 
                            5: {'position_x': 0, 'position_y': -2, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'VILLAGE_COMMERCIAL'}, 
                            6: {'position_x': 3, 'position_y': 0, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_QUARTIERS'}, 
                            7: {'position_x': -3, 'position_y': 0, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_CHAMPS'}, 
                            8: {'position_x': 0, 'position_y': 3, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_ARENE'}, 
                            9: {'position_x': 0, 'position_y': -3, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_COMMERCIAL'}, 
                            #chamsp a louest
                            10: {'position_x': -4, 'position_y': 0, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_CHAMPS'}, 
                            11: {'position_x': -5, 'position_y': 0, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'FABRICATEUR'}, 
                            12: {'position_x': -6, 'position_y': 0, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_CHAMPS'}, 
                            13: {'position_x': -4, 'position_y': 1, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_CHAMPS'}, 
                            14: {'position_x': -5, 'position_y': 1, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_CHAMPS'}, 
                            15: {'position_x': -6, 'position_y': 1, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'ANCIEN'}, 
                            16: {'position_x': -4, 'position_y': -1, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_CHAMPS'}, 
                            17: {'position_x': -5, 'position_y': -1, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_CHAMPS'}, 
                            18: {'position_x': -6, 'position_y': -1, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_CHAMPS'}, 
                            19: {'position_x': -7, 'position_y': 0, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'DECHARGE'}, 
                            #arene au nord
                            20: {'position_x': 0, 'position_y': 4, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_ARENE'}, 
                            21: {'position_x': -1, 'position_y': 4, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_ARENE'}, 
                            22: {'position_x': -1, 'position_y': 5, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_ARENE'}, 
                            23: {'position_x': -2, 'position_y': 5, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_ARENE'}, 
                            24: {'position_x': -1, 'position_y': 6, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_ARENE'}, 
                            25: {'position_x': 1, 'position_y': 4, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_ARENE'}, 
                            26: {'position_x': 1, 'position_y': 5, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_ARENE'}, 
                            27: {'position_x': 2, 'position_y': 5, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_ARENE'}, 
                            28: {'position_x': 1, 'position_y': 6, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_ARENE'}, 
                            29: {'position_x': 0, 'position_y': 6, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_ARENE'}, 
                            30: {'position_x': 0, 'position_y': 7, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_ARENE'}, 
                            31: {'position_x': 0, 'position_y': 5, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'ARENE'}, 
                            #zone commerciale au sud
                            32: {'position_x': 0, 'position_y': -4, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_COMMERCIAL'},
                            33: {'position_x': 0, 'position_y': -5, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'BANQUIER'}, 
                            34: {'position_x': -1, 'position_y': -4, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_COMMERCIAL'}, 
                            35: {'position_x': -1, 'position_y': -5, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'SORCIERE'}, 
                            36: {'position_x': -2, 'position_y': -4, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_COMMERCIAL'}, 
                            37: {'position_x': -2, 'position_y': -5, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'ARMURIER'}, 
                            38: {'position_x': 1, 'position_y': -4, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_COMMERCIAL'}, 
                            39: {'position_x': 1, 'position_y': -5, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'MAITRE_ARTEFACT'}, 
                            40: {'position_x': 2, 'position_y': -4, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_COMMERCIAL'}, 
                            41: {'position_x': 2, 'position_y': -5, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'HERBORISTE'}, 
                            #quartiers a lest
                            42: {'position_x': 4, 'position_y': 0, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_QUARTIERS'}, 
                            43: {'position_x': 5, 'position_y': 0, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_QUARTIERS'}, 
                            44: {'position_x': 6, 'position_y': 0, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_QUARTIERS'}, 
                            45: {'position_x': 7, 'position_y': 0, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CHEMIN_QUARTIERS'}, 
                            46: {'position_x': 4, 'position_y': 1, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'MAGE'}, 
                            47: {'position_x': 5, 'position_y': -1, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'JARDIN'}, 
                            48: {'position_x': 6, 'position_y': 1, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'CARTOGRAPHE'}, 
                            49: {'position_x': 7, 'position_y': -1, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'HOTEL'},

                            50: {'position_x': 0, 'position_y': -6, 'marqué sur la carte': False, 'terminé par joueur': False, 'type': 'ANCIENNE'}})

    #transforme le personnage et ses artefacts en materiaux si ce n'est pas le Voyageur
    if services.Player.stigma_negatif != "Indigérable":
        services.Player.liste_de_materiaux["Essence de Vitalitée"] = services.Player.points_de_vie_max // 25
        services.Player.liste_de_materiaux["Essence de Magie"] = services.Player.points_de_mana_max // 25
        services.Player.liste_de_materiaux["Essence de Fortitude"] = services.Player.points_de_force // 25
        services.Player.liste_de_materiaux["Essence de Sagesse"] = services.Player.points_dintelligence // 25
        services.Player.liste_de_materiaux["Essence de Résistance"] = services.Player.points_de_defence // 15
        services.Player.liste_de_materiaux["Essence Dorée"] = services.Player.nombre_de_gold // 100
        services.Player.liste_de_materiaux["Essence Carmine"] = services.Player.nombre_de_red_coin // 5
        services.Player.liste_de_materiaux["Essence Astrale"] = services.Player.nombre_de_monstres_tues // 10

        for artefact in services.Player.liste_dartefacts_optionels:
            if artefact in ARTEFACTMELIORATIF:
                services.Player.liste_de_materiaux["Fragment Mélioratif"] += 1
            elif artefact in ARTEFACTFATALITE:
                services.Player.liste_de_materiaux["Fragment de Fatalité"] += 1
            elif artefact in ARTEFACTSOPHIQUE:
                services.Player.liste_de_materiaux["Fragment Sophiste"] += 1

        

    else:
        services.Player.BringBackListeMateriauxToZero()

    if "Jeu Fini" in services.Player.player_tags:
        services.Player.player_tags.remove("Jeu Fini")
        
        print("[ERREUR : IMPOSSIBLE DE SE CONECTER A AVATAR]")
        services.Affichage.EntreePourContinuer()
        print("[AVATAR EN DEHORS DU COLISEUM]")
        services.Affichage.EntreePourContinuer()
        print("[UTILISATION DES RESSOURCES ALLOUEES A ALGORITHME...]")
        services.Affichage.EntreePourContinuer()
        print("[CREATION D'UN AVATAR TEMPORAIRE POUR UTILISATION DES MATERIAUX RECUPERES...]")
        services.Affichage.EntreePourContinuer()
        if services.Player.stigma_negatif != "Indigérable":
            print("[PROBLEME RENCONTRE LORS DU REMPLISSAGE DE LA LISTE DE MATERIAU]")
            print(f"[DECOMPTE DU MATERIAU *{AugmenteMateriauDansDictionnaire(True)}* AUGMENTE]")
            if random.randint(1,2) == 1 :
                print(f"[DECOMPTE DU MATERIAU *{AugmenteMateriauDansDictionnaire(True)}* AUGMENTE]")
                if random.randint(1,4) == 1 :
                    print(f"[DECOMPTE DU MATERIAU *{AugmenteMateriauDansDictionnaire(True)}* AUGMENTE]")
                    if random.randint(1,8) == 1 :
                        print(f"[DECOMPTE DU MATERIAU *{AugmenteMateriauDansDictionnaire(True)}* AUGMENTE]")
            services.Affichage.EntreePourContinuer()
        else:
            print("[PROBLEME RENCONTRE LORS DU REMPLISSAGE DE LA LISTE DE MATERIAU]")
            services.Affichage.EntreePourContinuer()
            print("[TRAIT *Indigérable* DETECTE DANS LA SAUVEGARDE]")
            print("[LISTE DE MATERIAU VIDEE]")
            services.Affichage.EntreePourContinuer()
        print("[CREATION TERMINEE]")
        services.Affichage.EntreePourContinuer()
        print("[LES CHAMPS DU CREPUSCULE VOUS OUVRENT LEURS PORTES]")
        services.Affichage.EntreePourContinuer()
        print("Vous traversez en une seconde un torrent de sensation alors que tout les nerfs de votre nouveau corps se connectent entre eux.")
        print("Vous vous y habituez.")
        services.Affichage.EntreePourContinuer()
        print("Le vent sur votre peau, malgrès la protection d'une tenue simple au tissu synthétique, vous fait l'effet d'un désagréable et uniforme choc électrique.")
        print("Vous vous y habituez.")
        services.Affichage.EntreePourContinuer()
        print("Tout dans votre corps vous semble désordonné, pas a sa place. Comme si votre coeur était a gauche et que votre estomac n'était pas protégé par votre colonne vertébrale.")
        print("Vous vous y habituez.")
        services.Affichage.EntreePourContinuer()
        print("Une etrange sensation vous prend au torse... vous comprenez que c'est le manque d'oxygène qui vous fait l'effet d'une boule de feu dans les poumons.")
        print("Vous ne vous y habituez pas.")
        services.Affichage.EntreePourContinuer()
        print("Vous prenez alors une grande inspiration...")
        print("...et ouvrez les yeux.")
        services.Affichage.EntreePourContinuer()
        time.sleep(2)

    services.Player.liste_dartefacts_optionels = []
    services.Player.points_de_defence = 0
    services.Player.points_de_force = 0
    services.Player.points_dintelligence = 0
    services.Player.points_de_mana_max = 0
    services.Player.points_de_vie_max = 0
    services.Player.nombre_de_gold = 0
    services.Player.nombre_de_red_coin = 0
    services.Player.nombre_de_monstres_tues = 0

    if services.Sove.ModifieTagsDansSove("Checke","Livraison En Attente"):
        services.Sove.ModifieTagsDansSove("Enleve","Livraison En Attente")
        services.Sove.ModifieTagsDansSove("Ajout","Livraison Terminée")
    
    #sauvegarde
    services.Save.SaveTheGameSansAffichage()

    #fin
    PlaySound("wind")
