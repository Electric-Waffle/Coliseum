"""Salles de combats particuliers : gardiens, bête, boss caché, rituel, obélisque."""

import ast
import time

from coliseum import services
from coliseum.audio import PlayMusicDeLetage, StopAllMusic
from coliseum.console import ClearConsole
from coliseum.exploration.progression import DoBossOrGoDown
from coliseum.histoire.boss_zero import DoBossZero
from coliseum.combat.lancement import combattre, livrer_combat
from coliseum.exploration.salles.registre import salle_de_type


@salle_de_type("GRAND GARDIEN")
def reveler_grand_gardien(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.broken()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    DoBossZero()


@salle_de_type("PETIT GARDIEN")
def reveler_petit_gardien(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.monstre()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    # lance le combat
    print("Vous entendez un bruit derrière vous, et découvrez un monstre !")
    services.Affichage.EntreePourContinuer()
    livrer_combat()
    PlayMusicDeLetage()

    # fait que l'event soit finit et ne peut ps etre relancé
    salle["terminé par joueur"] = True


@salle_de_type("BETE")
def reveler_bete(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.bete()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print("Vous avancez dans la salle, et vous retrouvez devant une bien étrange scène.")
    services.Affichage.EntreePourContinuer()
    print("Ca et la, de grandes machines de métal ronronnent doucement, et affichent des nombres et mots dans une langue que vous ne comprenez pas.")
    print("Le sol est recouvert d'un métal blanc, percé a distance régulière par de petites lumières.")
    services.Affichage.EntreePourContinuer()
    print("Et au centre, trone une créature de chair et de kératine dans une capsule transparente.")
    services.Affichage.EntreePourContinuer()
    while True:
        while True:
            try:
                print("La respiration de la créature est régulière, comme si elle était endormie.")
                print("Devant la capsule, il y a une fente rectangulaire, affublée du mot *OPEN* en grosses lettres rouge.")
                print("\n1 - Insérer quelque chose dans la fente")
                print("2 - Partir")
                choix = int(input("\nFaites votre choix avec les nombres : "))
                ClearConsole()
                if choix in [1, 2]:
                    break
            except ValueError:
                ClearConsole()
        if choix == 1:
            if "Carte de Sécurité" in services.Player.liste_dartefacts_optionels:
                services.Player.liste_dartefacts_optionels.remove("Carte de Sécurité")
                print("Vous insérez la Carte de Sécurité dans la fente, et la salle se retrouve plongée dans une obscurité percée seulement par la lumière rouge de quelques alarmes.")
                services.Affichage.EntreePourContinuer()
                print("Vous entendez un craquement sinistre, et la capsule transparente s'ouvre lentement.")
                services.Affichage.EntreePourContinuer()
                StopAllMusic()
                print("Tout à coup, les alarmes éclatent et vous vous retrouvez plongé dans le noir.")
                time.sleep(3)
                ClearConsole()
                print("Vous entendez un craquement.")
                time.sleep(3)
                ClearConsole()
                print("Puis un autre.")
                time.sleep(3)
                ClearConsole()
                print("Deux points verts apparaissent en face de vous.")
                time.sleep(3)
                ClearConsole()
                print("Ils vous fixent intensément.")
                time.sleep(3)
                ClearConsole()
                print("Vous sentez quelque chose de chaud sur votre visage.")
                time.sleep(3)
                ClearConsole()
                print("Quelque chose est proche de vous.")
                time.sleep(3)
                ClearConsole()
                print("Vous fermez les yeux, et attendez votre fin.")
                time.sleep(6)
                ClearConsole()
                print("Mais rien ne vient.")
                time.sleep(3)
                ClearConsole()
                PlayMusicDeLetage()
                print("Quand vous rouvrez vos yeux, l'obscurité a laissé place a la fine lumière qui passe a travers la porte éventrée de la salle.")
                services.Affichage.EntreePourContinuer()
                print("Il n'y a plus rien dans la capsule.")
                services.Affichage.EntreePourContinuer()
                print("Vous gagnez l'artefact [Regard de la Bête] !")
                print("La marque psychologique indélébile d'un prédateur sur sa proie. \nCe n'est pas vraiment un artefact, mais le stress a fait battre votre coeur tellement vite que vous gagnez 4 points d'endurance !")
                services.FloorMaker.GiveRandomArtefact("Regard de la Bête","Don")
                services.Player.points_dendurance += 4
                services.Affichage.EntreePourContinuer()
                # fait que l'event soit finit et ne peut ps etre relancé
                salle["terminé par joueur"] = True
                break
            else:
                print("Vous n'avez rien a insérer.")
                services.Affichage.EntreePourContinuer()
        elif choix == 2:
            print("Vous quittez la salle tout droit tirée d'un film de science fiction.")
            services.Affichage.EntreePourContinuer()
            break


@salle_de_type("SPAWNER")
def reveler_spawner(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.machine()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print("Vous trouvez un méchanisme ancien !")
    services.Affichage.EntreePourContinuer()
    print("C'est...")
    services.Affichage.EntreePourContinuer()
    print("...difficile à décrire...")
    services.Affichage.EntreePourContinuer()
    print("On dirait une cage de métal dans laquelle dansent des flammes.\nIl y a une fente dessus, et vous sentez les âmes absorbées par Zeroual réagir au méchanisme.")
    services.Affichage.EntreePourContinuer()
    while True:
        while True:
            try:
                print(f"Vous pouvez dépenser une partie de vos {services.Player.nombre_de_monstres_tues} âmes pour faire... quelque chose ?")
                print("\n1 - Dépenser 5 âmes")
                print("2 - Dépenser 12 âmes")
                print("3 - Dépenser 20 âmes")
                print("4 - Partir")
                choix = int(input("\nFaites votre choix avec les nombres : "))
                ClearConsole()
                if choix in range(1, 5):
                    break
            except ValueError:
                ClearConsole()
        if ((choix == 1 and services.Player.nombre_de_monstres_tues >= 5) or 
            (choix == 2 and services.Player.nombre_de_monstres_tues >= 12) or 
            (choix == 3 and services.Player.nombre_de_monstres_tues >= 20)):
            if choix == 1 :
                services.Player.nombre_de_monstres_tues -= 5
                services.Player.nombre_dennemis_a_letage += 5
            elif choix == 2 :
                services.Player.nombre_dennemis_a_letage += 10
                services.Player.nombre_de_monstres_tues -= 12 
            elif choix == 3 :
                services.Player.nombre_dennemis_a_letage += 17
                services.Player.nombre_de_monstres_tues -= 20
            print("Vous approchez Zeroual de la fente, et l'arme prend la forme d'une clé a motif de crâne.")
            print("Vous insérez la clé dans la fente et...")
            services.Affichage.EntreePourContinuer()
            print("...vous la tournez.")
            services.Affichage.EntreePourContinuer()
            print("Vous sentez quelque chose sortir de Zeroual, et rejoindre les flammes a l'interieur de la cage.")
            print("Dans le plus grand des silences, la cage s'ouvre de tout les côtés, comme un cube de papier pour laquelle la colle n'aurait pas tenue, et les flammes sortent de la salle en virevoltant !")
            services.Affichage.EntreePourContinuer()
            print("Une idée résonne alors dans votre esprit, comme induite par Zeroual :")
            services.Affichage.EntreePourContinuer()
            print("*ARENE*")
            services.Affichage.EntreePourContinuer()
            # fait que l'event soit finit et ne peut ps etre relancé
            salle["terminé par joueur"] = True
            break
        elif choix == 4:
            print("Vous regardez, comme hypnotisé, la danse magestueuse des flammes dans la cage, et décidez de vous en aller.")
            services.Affichage.EntreePourContinuer()
            break
        else:
            print("Vous approchez Zeroual de la fente, et l'arme prend la forme d'une clé a motif de crâne.")
            print("Vous insérez la clef dans la fente et...")
            services.Affichage.EntreePourContinuer()
            print("...rien ne se passe.")
            services.Affichage.EntreePourContinuer()
            print("On dirait que vous n'aviez pas assez d'âmes.")
            services.Affichage.EntreePourContinuer()


@salle_de_type("BOSS")
def reveler_boss(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        print("Vous rentrez dans une salle bien plus grande que d'habitude, tapissée de verdure et d'arbres, comme si vous étiez dehors, et...")
        services.Affichage.EntreePourContinuer()
        print("...")
        services.Affichage.EntreePourContinuer()
        print("...")
        services.Affichage.EntreePourContinuer()
        print("Il y a une cascade.")
        services.Affichage.EntreePourContinuer()
        print("...")
        services.Affichage.EntreePourContinuer()
        print("...")
        services.Affichage.EntreePourContinuer()
        print("Vous allez bien evidemment derrière la cascade.")
        services.Affichage.EntreePourContinuer()
        services.Draw.boss()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True
    print("Vous trouvez une porte de pierre taillée derrière une cascade.")
    services.Affichage.EntreePourContinuer()
    print("Vous pouvez y voir des symboles différents dans des cercles de pierre, tous reliés a un cercle plus grand, en hauteur.")
    services.Affichage.EntreePourContinuer()
    print("En dessous, 50 emplacements de taille bien plus petite, ressemblant a des redcoins.")
    services.Affichage.EntreePourContinuer()
    donnees_de_s0ve = services.Observation.GetPermanentThingsFromS0ve() 
    redcoins_inseres = ast.literal_eval(donnees_de_s0ve["Redcoins Inseres"])

    while True:
        while True:
            try:
                print(f"{redcoins_inseres} redcoins sont dans leurs emplacements.")
                if ((redcoins_inseres == 50 and services.Player.nom_du_personnage == "Terah")
                    or
                    services.Player.death_divinity
                ):
                    print("La porte est ouverte.")
                    print("\n1 - Passer la porte.")
                else:
                    print("La porte est fermée.")
                    print(f"\n1 - Poser tout les redcoins dans leurs emplacements [{services.Player.nombre_de_red_coin}]")
                print("2 - Observer la porte")
                print("3 - Partir")
                choix = int(input("\nFaire votre choix avec les nombres : "))
                ClearConsole()
                if choix in range(1, 4):
                    break
            except ValueError:
                ClearConsole()
        if choix == 3:
            print("Vous laissez la porte et retournez sur vos pas.")
            services.Affichage.EntreePourContinuer()
            break
        elif choix == 2:
            services.Ending.PrintEtEntreePourContinuer("Vous regardez les symboles de plus près :")
            services.Ending.PrintEtEntreePourContinuer("Un nuage de fumée s'échappant d'un personnage fou.")
            services.Ending.PrintEtEntreePourContinuer("Une petite cane de pharaon entourée de 2 totems.")
            services.Ending.PrintEtEntreePourContinuer("Un couteau de cuisine.")
            services.Ending.PrintEtEntreePourContinuer("Un gluant avec une couronne.")
            services.Ending.PrintEtEntreePourContinuer("Une hache prise dans la glace.")
            services.Ending.PrintEtEntreePourContinuer("Une figure encapuchonnée.")
            services.Ending.PrintEtEntreePourContinuer("Un personnage entouré de 4 autres.")
            services.Ending.PrintEtEntreePourContinuer("Un personnage similaire, avec un sourire sanguinaire.")
            services.Ending.PrintEtEntreePourContinuer("Une boule sur laquelle se trouve plusieurs visages en peine.")
            services.Ending.PrintEtEntreePourContinuer("Et ces symboles sont relié a un grand levé/couché de soleil surmonté de vagues.")
            services.Ending.PrintEtEntreePourContinuer("?")
            services.Ending.PrintEtEntreePourContinuer("Vous pouvez voir, dans un coin de la porte, un message gravé a la hate :")
            services.Ending.PrintEtEntreePourContinuer("*Entend ma voix, enfant maudit.*")
        elif choix == 1:
            if (redcoins_inseres == 50 and services.Player.nom_du_personnage == "Terah") or services.Player.death_divinity:
                while True:
                    while True:
                        try:
                            print("Êtes vous sûr ?\n(La difficultée augmente drastiquement, et vous ne pourrez pas revenir en arrière.)")
                            print("\n1 - Oui")
                            print("2 - Non")
                            choix = int(input("Faites votre choix avec les nombres : "))
                            ClearConsole()
                            if choix in [1, 2]:
                                break
                        except ValueError:
                            ClearConsole()
                    if choix == 1:
                        services.Player.position_x = 0
                        services.Player.position_y = 0
                        etage.UpdatePlayerPosition()
                        services.Player.numero_de_la_salle = 1
                        services.Player.etage_alternatif = True
                        services.Player.numero_de_letage -= 1
                        services.Player.player_tags.append("Passe La Porte Redcoin")
                        DoBossOrGoDown()
                        break
                    else:
                        break
                if "Passe La Porte Redcoin" in services.Player.player_tags :
                    break
            elif redcoins_inseres != 50:
                redcoins_inseres += services.Player.nombre_de_red_coin
                if redcoins_inseres > 50:
                    redcoins_inseres = 50


                donnees_de_s0ve["Redcoins Inseres"] = redcoins_inseres
                services.Observation.SetPermanentThingsToS0ve(donnees_de_s0ve)


                print(f"Vous posez {services.Player.nombre_de_red_coin} redcoins dans les emplacements.")
                services.Player.nombre_de_red_coin = 0
                services.Save.SaveTheGameSansAffichage()
                services.Affichage.EntreePourContinuer()

            else:
                print("Les redcoins sont déja tous placés.")
                services.Affichage.EntreePourContinuer()
        if "Passe La Porte Redcoin" in services.Player.player_tags :
            break


@salle_de_type("RITUEL")
def reveler_rituel(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.rituel()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    if not "Griffes du Démon" in services.Player.techniques_possedes:
        print("Vous trouvez un autel de pierre tailladée, sur lequel repose un gobelet doré.")
        print("Alors que vous prenez le gobelet dans vos mains, vous entendez une voix résonner dans votre tête :")
        services.Affichage.EntreePourContinuer()
        print("*Met en jeu ton âme.*")
        print("*Exécute avec les mains de l'Innomable.*")
        print("*J'ornerais ton corps avec celui des morts.*")
        services.Affichage.EntreePourContinuer()
        print("...")
        services.Affichage.EntreePourContinuer()
        print("Le gobelet se remplit de #???!!## .")
        services.Affichage.EntreePourContinuer()
        while True:
            try:
                print("Boire le contenu du gobelet ?")
                print("\n1 - Oui")
                print("2 - Non")
                choix = int(
                input("\nChoisissez votre action avec les nombres : ")
                )
                ClearConsole()
                if choix in [1, 2]:
                    break
            except ValueError:
                ClearConsole()
        if choix == 1:
            print("Vous avalez le contenu du gobelet.")
            print("Votre main devient plus sombre, et une énergie noire sort de vos ongles.")
            services.Affichage.EntreePourContinuer()
            print("Vous apprenez la technique [Griffes du Démon] !")
            services.Player.techniques_possedes.append("Griffes du Démon")
            services.Affichage.EntreePourContinuer()
            if "Syra" in services.Player.liste_dartefacts_optionels:
                print("Grace au verre de Syra que vous avez bu, vous gagnez aussi 10 pm max !")
                services.Player.points_de_mana += 10
                services.Player.points_de_mana_max += 10
                services.Affichage.EntreePourContinuer()
            print("Vous sentez quelque chose fretiller dans votre abdomen, puis planter ses griffes dans les parois de votre estomac.")
            services.Affichage.EntreePourContinuer()
            print("Vous perdez 20 points de vie et mana max !")
            services.Player.points_de_vie_max -= 20
            if services.Player.points_de_vie_max <= 0:
                services.Player.points_de_vie_max = 1
            if services.Player.points_de_vie > services.Player.points_de_vie_max:
                services.Player.points_de_vie = services.Player.points_de_vie_max
            services.Player.points_de_mana_max -= 20
            if services.Player.points_de_mana_max <= 0:
                services.Player.points_de_mana_max = 1
            if services.Player.points_de_mana > services.Player.points_de_mana_max:
                services.Player.points_de_mana = services.Player.points_de_mana_max
            services.Affichage.EntreePourContinuer()
            print("*Chaines.*")
            services.Affichage.EntreePourContinuer()
            print("*Confitions de ta libération ?*")
            print("*Reviens dans quelques instants.*")
            services.Affichage.EntreePourContinuer()
            print("Vous vous éloignez de l'autel, mais le sentez changer derrière votre dos.")
            services.Affichage.EntreePourContinuer()
        else:
            print("Vous reposez le gobelet sur l'autel, et vous en éloignez.")
            services.Affichage.EntreePourContinuer()
    else:
        print("Vous vous approchez de l'autel, et posez votre main dessus.")
        print("Des lettres apparaissent alors dans les airs, tremblottantes comme une flamme devant la tempête.")
        services.Affichage.EntreePourContinuer()
        while True:
            while True:
                try:
                    print("        -{ AUTEL DEMONIAQUE }-")
                    print("     -= Offrande de Sacrifices =-")
                    print(f"\n        SACRIFICES ? {services.Player.nombre_de_sacrifices}.\n")
                    print("       1 - RICHESSE ? 3.")
                    print("            2 - VIE ? 3.")
                    print("           3 - SANG ? 5.")
                    print("         4 - DESTIN ? 5")
                    print("        5 - POUVOIR ? 10.")
                    print("        6 - LÂCHETÉ ? 0.")
                    print("     7 - LIBERATION ? 5.")
                    choix = int(
                    input("\nChoisissez votre action avec les nombres : ")
                    )
                    ClearConsole()
                    if choix in range(1, 8):
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                if services.Player.nombre_de_sacrifices >= 3:
                    services.Player.nombre_de_sacrifices -= 3
                    print("L'INNOMABLE VOUS REMERCIE.")
                    services.Affichage.EntreePourContinuer()
                    print("Une lueur bleue sort de votre poignet tandis que votre poche s'alourdit.")
                    services.Affichage.EntreePourContinuer()
                    gain_gold = 255
                    gain_gold = services.Player.AddGoldToPlayer(gain_gold, True)
                    print(f"Vous perdez 3 Sacrifices, et gagnez {gain_gold} golds !")
                    services.Affichage.EntreePourContinuer()
                else:
                    print("BLAGUE ?")
                    services.Affichage.EntreePourContinuer()
            elif choix == 2:
                if services.Player.nombre_de_sacrifices >= 3:
                    services.Player.nombre_de_sacrifices -= 3
                    print("L'INNOMABLE VOUS REMERCIE.")
                    services.Affichage.EntreePourContinuer()
                    print("Une lueur bleue sort de votre poignet tandis que quelque chose pose sa main sur votre torse et appuie fortement.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous perdez 3 Sacrifices, gagnez 5 points de vie/mana max, et regagnez toute votre vie et votre mana !")
                    services.Player.points_de_vie_max += 5
                    services.Player.points_de_vie = services.Player.points_de_vie_max
                    services.Player.points_de_mana_max += 5
                    services.Player.points_de_mana = services.Player.points_de_mana_max
                    services.Affichage.EntreePourContinuer()
                else:
                    print("BLAGUE ?")
                    services.Affichage.EntreePourContinuer()
            elif choix == 3:
                if services.Player.nombre_de_sacrifices >= 5:
                    services.Player.nombre_de_sacrifices -= 5
                    print("L'INNOMABLE VOUS REMERCIE.")
                    services.Affichage.EntreePourContinuer()
                    print("Une lueur bleue sort de votre poignet, et une énergie étrangère parcourt les veines de votre corps.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous perdez 5 Sacrifices, gagnez 2 points de force/intelligence !")
                    services.Player.points_de_force += 2
                    services.Player.points_dintelligence += 2
                    services.Affichage.EntreePourContinuer()
                else:
                    print("BLAGUE ?")
                    services.Affichage.EntreePourContinuer()
            elif choix == 4:
                if services.Player.nombre_de_sacrifices >= 5:
                    services.Player.nombre_de_sacrifices -= 5
                    print("L'INNOMABLE VOUS REMERCIE.")
                    services.Affichage.EntreePourContinuer()
                    print("Une lueur bleue sort de votre poignet tandis que quelque chose souffle au dessus de votre tête.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous perdez 5 Sacrifices, gagnez 3 pourcents de chance de faire un coup/sort critiques, et 1 pourcent de chance d'esquive !")
                    services.Player.taux_coup_critique += 3
                    services.Player.taux_sort_critique += 3
                    services.Player.taux_desquive += 1
                    services.Affichage.EntreePourContinuer()
                else:
                    print("BLAGUE ?")
                    services.Affichage.EntreePourContinuer()
            elif choix == 5:
                if services.Player.nombre_de_sacrifices >= 10:
                    services.Player.nombre_de_sacrifices -= 10
                    print("L'INNOMABLE VOUS REMERCIE.")
                    services.Affichage.EntreePourContinuer()
                    print("Une lueur bleue sort de votre poignet, et un petit coffre de bois noir apparait sur l'autel.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous perdez 10 Sacrifices, et ouvrez le coffre.")
                    services.Affichage.EntreePourContinuer()
                    etage.GiveRandomArtefact()
                else:
                    print("BLAGUE ?")
                    services.Affichage.EntreePourContinuer()
            elif choix == 6:
                print("Vous enlevez votre main de l'autel.")
                services.Affichage.EntreePourContinuer()
                break
            elif choix == 7:
                if services.Player.nombre_de_sacrifices >= 5:
                    services.Player.nombre_de_sacrifices -= 5
                    print("L'INNOMABLE VOUS REMERCIE.")
                    services.Affichage.EntreePourContinuer()
                    print("L'énergie noire sort de votre main.")
                    print("Vous oubliez la technique [Griffes du Démon] !")
                    print("Vous regagnez 20 points de vie et mana max !")
                    services.Player.techniques_possedes.remove("Griffes du Démon")
                    services.Player.points_de_vie_max += 20
                    services.Player.points_de_mana_max += 20
                    services.Affichage.EntreePourContinuer()
                    print("L'autel s'écroule sur lui même.")
                    services.Affichage.EntreePourContinuer()
                    salle["terminé par joueur"] = True
                    break
                else:
                    print("BLAGUE ?")
                    services.Affichage.EntreePourContinuer()


@salle_de_type("OBELISQUE")
def reveler_obelisque(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.obelisque(salle["position_x"] * 25, salle["position_y"] * 25)
        salle["marqué sur la carte"] = True
        etage.UseMonocleDeVerite()

    print("Vous trouvez un bien étrange obélisque au centre d'une pièce plus grande que les autres.")
    print("Construit en verre, vous pouvez apercevoir un petit coffre de bois noir au milieu.")
    services.Affichage.EntreePourContinuer()
    print("De plus, sur chaque faces de l'obélisque, il y a une encoche profonde et 5 mots écrits dans une langue que vous ne connaissez pas.")
    services.Affichage.EntreePourContinuer()
    print("Zeroual semble réagir à l'encoche.")
    services.Affichage.EntreePourContinuer()

    while True:
        try:
            print("Approcher Zeroual de l'encoche ?")
            print("(Assurez vous d'être prêt.)")
            print("\n1 - Non\n2 - Oui")
            choix = int(
                input("\nChoisissez votre action avec les nombres : ")
            )
            ClearConsole()
            if choix in [1, 2]:
                break
        except ValueError:
            ClearConsole()
    if choix == 1:
        print("Vous vous éloignez de la salle de l'obélisque.")
        services.Affichage.EntreePourContinuer()

    else:
        StopAllMusic()
        print("Vous approchez Zeroual de l'encoche."
              "\nL'arme prend alors la forme d'une épée a la lame rouillée et au design particulier, et vous l'insérez dans l'encoche.")
        services.Affichage.EntreePourContinuer()
        print("Les portes de la salle se ferment.")
        services.Affichage.EntreePourContinuer()
        print("Des runes apparaissent dans les airs, flottant sur un axe invisible et encerclant le vide.")
        print("Quelque chose résonne en vous, comme une idée que l'on aurait mit de force dans votre crane, et qui émane de votre arme.")
        services.Affichage.EntreePourContinuer()
        print("*Retire.*")
        print("*Prouver. Valeur.*")
        services.Affichage.EntreePourContinuer()
        print("Une terrible présence se fait sentir, et vous retirez Zeroual de l'encoche alors qu'un bruit se fait entendre derriere vous.")
        services.Affichage.EntreePourContinuer()
        services.Player.affronte_obelisque = True
        vague = 5
        while vague != 0:
            combattre()
            print("Alors que l'ennemi disparait, une des lignes de l'obélisque s'efface.")
            services.Affichage.EntreePourContinuer()
            vague -= 1
            if vague != 0:
                print(f"Il n'y a maintenant plus que {vague} mots.")
                services.Affichage.EntreePourContinuer()
                print("Vous voyez une des runes se briser, et quelque chose apparait.")
                services.Affichage.EntreePourContinuer()
        services.Player.affronte_obelisque = False
        print("L'obélisque, maintenant vide de mots, éclate en plusieurs morceaux."
              "\nMais au lieu de tomber, ils restent en place quelques secondes avant d'aller sur votre arme, qui les absorbe.")
        services.Affichage.EntreePourContinuer()
        print("Vous sentez que le nombre de monstre que vous avez tué a soudainement augmenté de 15 !")
        services.Player.nombre_de_monstres_tues += 15
        services.Affichage.EntreePourContinuer()
        print("Vous laissez vos questions de coté, et récuperez le petit coffre de bois noir, que vous ouvrez immédiatement.")
        services.Affichage.EntreePourContinuer()
        salle["terminé par joueur"] = True
        etage.GiveRandomArtefact()
        print("Les portes de la salle se rouvrent.")
        services.Affichage.EntreePourContinuer()
        PlayMusicDeLetage()
