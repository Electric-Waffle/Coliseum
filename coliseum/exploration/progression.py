"""Passage d'un étage à l'autre : descente, montée, remise à zéro, nom de l'étage."""

from turtle import (
    clear,
)

from coliseum import services
from coliseum.audio import PlayMusicDeLetage, StopAllMusic
from coliseum.combat.lancement import DoBossFight
from coliseum.console import ClearConsole
from coliseum.erreurs import WriteErrorInErrorLog
from coliseum.exploration.plan_etage import RegardeSiEtageCompletementObserve


def RemiseAZeroDesVariablesPourProchainEtage():
    services.Player.affronte_un_boss = False
    services.Player.boss_battu = False
    services.Player.redcoin_bought = False
    services.Player.red_coin_recu_par_extermination = False
    services.Player.nombre_dennemis_a_letage = 5 + services.Player.numero_de_letage * 2
    services.Player.flammes_rouge = 5
    services.Player.flammes_bleue = 3
    services.Player.flammes_verte = 2
    services.Player.flammes_noire = 1
    services.Player.poissons = 5
    services.Player.commentaire_boss = "Affronter le Boss"
    services.Player.quete = "None"
    services.Player.possede_la_cle = False
    if services.FloorMaker.carte_ouverte:
        clear()
    services.FloorMaker.__init__()
    if services.Player.numero_de_letage == 0:
        services.Player.nombre_dennemis_a_letage = 0
        services.Player.possede_la_cle = True
    elif services.Player.numero_de_letage in [10, 11]:
        services.Player.nombre_dennemis_a_letage = 0


def GoDown():
    services.Affichage.AfficheDescente()
    services.Player.numero_de_letage += 1
    DefinitNomEtage()
    RemiseAZeroDesVariablesPourProchainEtage()
    services.Affichage.AffichageDescriptionEtage()
    if services.Player.numero_de_letage == 12 or (
        services.Player.numero_de_letage == 9 and not ("Marque du Sacrifice" in services.Player.liste_dartefacts_optionels)
    ):
        game_in_session = False
    else:
        game_in_session = True

    return game_in_session


def GoUp():
    print("Vous remontez les marches du Coliseum.")
    services.Affichage.EntreePourContinuer()
    services.Player.numero_de_letage -= 1
    if services.Player.numero_de_letage == 0:
        services.Player.mode_de_jeu = "Descente"
        
        StopAllMusic()
        print("Vous arrivez a votre destination.")
        services.Affichage.EntreePourContinuer()
    RemiseAZeroDesVariablesPourProchainEtage()
    DefinitNomEtage()
    game_in_session = True
    if game_in_session:
        PlayMusicDeLetage()
        try:
            services.FloorMaker.SetupFloorLayout()
            services.Save.SaveTheGameSansAffichage()
        except Exception as error:
            WriteErrorInErrorLog(error)


def DoBossOrGoDown():
    game_in_session = True

    # arrivage a la fin de l'étage sans clé
    level_de_la_cle =  services.Sove.ModifieLivraisonDansSove("Nombre", "Clé")
    if RegardeSiEtageCompletementObserve(services.FloorMaker.FloorBlueprint) and (level_de_la_cle+4)==services.Player.numero_de_letage:
        print("Vous avez observé chaque salles de l'étage, sans trouver de clé.")
        services.Affichage.EntreePourContinuer()
        print("Vous regardez , impuissant, les horribles grilles de l'arène.")
        services.Affichage.EntreePourContinuer()
        print("I L  N ' Y  A  P L U S  R I E N  A  F A I R E")
        services.Affichage.EntreePourContinuer()
        print("Vous envisagez de rogner le métal, mais celui ci reste stoique face a vos efforts.")
        services.Affichage.EntreePourContinuer()
        print("Vous envisagez de remonter, mais ne retrouvez pas les marches que vous avez emprunté.")
        services.Affichage.EntreePourContinuer()
        print("Vous envisagez de demander de l'aide au marchand, mais celui-ci n'est trouvable nulle part.")
        services.Affichage.EntreePourContinuer()
        print("Vous cherchez a nouveau dans toute les salles de l'étage, mais ces dernieres sont vides.")
        services.Affichage.EntreePourContinuer()
        print("Et alors que vous revenez à l'Arène au centre de l'étage...")
        services.Affichage.EntreePourContinuer()
        print("...vous trouvez un carré de pierre alien, parsemé de trous depuis lesquels vous pouvez aperçevoir le scintillement de pieux de métal.")
        services.Affichage.EntreePourContinuer()
        print("Un simple piège.")
        services.Affichage.EntreePourContinuer()
        print("Une mort rapide.")
        services.Affichage.EntreePourContinuer()
        print("La plus douce pitiée du Coliseum.")
        services.Affichage.EntreePourContinuer()
        print("...")
        services.Affichage.EntreePourContinuer()
        print("...")
        services.Affichage.EntreePourContinuer()
        print("...")
        services.Affichage.EntreePourContinuer()
        print("...vous n'aurez pas saigné bien longtemps.")
        services.Affichage.EntreePourContinuer()
        services.Affichage.ShowDeath()

    if services.Player.mode_de_jeu == "Ascension":
        GoUp()

    elif not "Fantome" in services.Player.player_tags:
        # combat contre boss
        if not services.Player.boss_battu and not "Passe La Porte Redcoin" in services.Player.player_tags:
            DoBossFight()
                
        # descente au niveau inferieur
        else:
            if services.Player.mode_de_jeu == "Véritable Descente" and services.Player.numero_de_letage == 0:
                GiveChoiceRealEndingOrNot()
            if services.Player.nom_de_letage == "Limbes Flétrissants" and services.Player.numero_boss_alt in range(1, 11) and not "Passe La Porte Redcoin" in services.Player.player_tags:
                services.Player.numero_de_letage -= 1
                services.Player.etage_alternatif = True
                services.Player.numero_boss_alt += 1
            game_in_session = GoDown()
            if game_in_session:
                PlayMusicDeLetage()
                try:
                    services.FloorMaker.SetupFloorLayout()
                except Exception as error:
                    WriteErrorInErrorLog(error)

        
    return game_in_session


def GiveChoiceRealEndingOrNot():
    print("Vous vous approchez du centre de l'arène.")
    services.Affichage.EntreePourContinuer()
    print("Vous pouvez absorber la Marque du Sacrifice de Jean afin d'entrer dans les profondeurs du Coliseum...")
    services.Affichage.EntreePourContinuer()
    print("...ou la laisser pour n'aller qu'à la fin de l'histoire de votre personnage.")
    services.Affichage.EntreePourContinuer()
    print("Le choix est votre.")
    services.Affichage.EntreePourContinuer()
    while True :
        try:
            print("1 - Absorber la Marque du Sacrifice")
            print("2 - Descendre ")
            choix = int(input("\nFaites votre choix avec les numéros :"))
            ClearConsole()
            if choix in [1, 2]:
                break
        except ValueError:
            ClearConsole()
    if choix == 1:
        print("Vous approchez votre main de la masse argentée, et celle ci fonce sur votre épaule.")
        services.Affichage.EntreePourContinuer()
        print("Vous sentez une agréable chaleur émettre du point d'impact.")    
        services.Affichage.EntreePourContinuer()
        print("Vous obtenez la Marque du Sacrifice !")
        services.Affichage.EntreePourContinuer()
        services.FloorMaker.GiveRandomArtefact("Marque du Sacrifice","Don")
    print("Vous continuez votre chemin.")
    services.Affichage.EntreePourContinuer()


def DefinitNomEtage():
    if services.Player.numero_de_letage == 0:
        services.Player.nom_de_letage = "Sanctuaire du Sacrifice"
    elif services.Player.numero_de_letage == 1:
        services.Player.nom_de_letage = "Ruines Abandonnées"
    elif services.Player.numero_de_letage == 2:
        services.Player.nom_de_letage = "Forêt Désenchantée"
        if services.Player.etage_alternatif:
            services.Player.nom_de_letage = "Jungle Cruelle"
    elif services.Player.numero_de_letage == 3:
        services.Player.nom_de_letage = "Champs de Sables"
    elif services.Player.numero_de_letage == 4:
        services.Player.nom_de_letage = "Tour de l'Esprit"
    elif services.Player.numero_de_letage == 5:
        services.Player.nom_de_letage = "Carnaval de Rouille"
        if services.Player.etage_alternatif:
            services.Player.nom_de_letage = "Le Lumisade"
    elif services.Player.numero_de_letage == 6:
        services.Player.nom_de_letage = "Bidonville du Clocher"
    elif services.Player.numero_de_letage == 7:
        services.Player.nom_de_letage = "Cachots de l'Immonde"
        if services.Player.etage_alternatif:
            services.Player.nom_de_letage = "Douves du Pénitent"
    elif services.Player.numero_de_letage == 8:
        services.Player.nom_de_letage = "Arène du Zénith"
    elif services.Player.numero_de_letage == 9:
        services.Player.nom_de_letage = "Chemins Coalescents"
    elif services.Player.numero_de_letage == 10:
        services.Player.nom_de_letage = "Dédale Frontière"
        if services.Player.etage_alternatif:
            services.Player.nom_de_letage = "Limbes Flétrissants"
    elif services.Player.numero_de_letage == 11:
        services.Player.nom_de_letage = "Rivages Distants"
    services.Player.etage_alternatif = False
