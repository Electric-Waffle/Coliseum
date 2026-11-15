"""Machines et services de l'étage : arbre, bols, jacuzzi, chargeur, affixeurs, distributeur..."""

import random

from coliseum import services
from coliseum.audio import PlayMusic, PlayMusicDeLetage, StopAllMusic
from coliseum.console import ClearConsole, attendre
from coliseum.donnees.actions import LISTESORTS, LISTETECHNIQUES
from coliseum.donnees.items import LISTEITEM
from coliseum.outils import GetRandomItemFromList
from coliseum.exploration.salles.registre import salle_de_type


@salle_de_type("ARBRE")
def reveler_arbre(etage, salle):
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
    print("...un grand arbre de métal !")
    services.Affichage.EntreePourContinuer()
    while True:
        try:
            print("Vous pouvez voir des choses pousser au niveau de la canopée.")
            print("\n1 - Donner un grand coup de pied dans l'arbre")
            print("2 - Partir")
            choix = int(input("\nFaites votre choix avec les nombres : "))
            ClearConsole()
            if choix in [1, 2]:
                break
        except ValueError:
            ClearConsole()
    if choix == 1:
        print("Vous donnez votre plus grand coup de pied dans l'arbre, et plusieurs choses tombent a terre.")
        services.Affichage.EntreePourContinuer()
        liste_de_choses = ["Feuille Jindagee", "Fruit Jindagee", "Feuille Aatma", "Fruit Aatma"]
        liste_de_choses_tombee = []
        for _ in range (1, 4):
            nombre_aleatoire = random.randint(0,100)
            if nombre_aleatoire <= 5 and "Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure" not in liste_de_choses_tombee:
                liste_de_choses_tombee.append("Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure")
            else:
                chose_aleatoire = random.randint(0, 3)
                liste_de_choses_tombee.append(liste_de_choses[chose_aleatoire])
        print(f"Vous récuperez les objets [{liste_de_choses_tombee[0]}] [{liste_de_choses_tombee[1]}] et [{liste_de_choses_tombee[2]}] !")
        for item in liste_de_choses_tombee:
            if item == "Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure":
                services.FloorMaker.GiveRandomArtefact("Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure","Don")
            else:
                services.Player.items_possedes[item] += 1
        services.Affichage.EntreePourContinuer()
        print("L'arbre n'a plus rien a offrir.")
        services.Affichage.EntreePourContinuer()
        # fait que l'event soit finit et ne peut ps etre relancé
        salle["terminé par joueur"] = True
    elif choix == 2:
        print("Vous laissez l'arbre tranquille et repartez dans un silence troublé seulement par le bruit du vent dans les feuilles et du bois qui se balance doucement.")
        services.Affichage.EntreePourContinuer()


@salle_de_type("BOL")
def reveler_bol(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.machine()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    if etage.nombre_de_bols == 1:
        s_ou_pas = ""
        des_ou_pas = "du"
    else:
        s_ou_pas = "s"
        des_ou_pas = "d'un des"
    print("Vous trouvez un méchanisme ancien !")
    services.Affichage.EntreePourContinuer()
    print("C'est...")
    services.Affichage.EntreePourContinuer()
    print(f"...{etage.nombre_de_bols} bol{s_ou_pas}.")
    services.Affichage.EntreePourContinuer()
    print(f"En dessous {des_ou_pas} bol{s_ou_pas}, il y a un petit écriteau sur lequel il est marqué :")
    if etage.nombre_de_bols == 1:
        print("*Si vous lisez ceci, veuillez mettre 50 golds dans le bol.*")
        services.Affichage.EntreePourContinuer()
    else:
        print("*Merci pour vos donations !*\n*Grâce à vous, nous avons pu investir dans l'acquisition d'un autre bol !*")
        services.Affichage.EntreePourContinuer()
        print("*Maintenant, veuillez mettre 50 golds dans chacun des bols.*")
        services.Affichage.EntreePourContinuer()
    if services.Player.nombre_de_gold < (etage.nombre_de_bols * 50):
        print(f"Mais vous n'avez même pas {(etage.nombre_de_bols * 50)} golds, alors vous mettez tout vos golds dans le{s_ou_pas} bol{s_ou_pas}.")
        services.Player.nombre_de_gold = 0
    else:
        print(f"Dépité, vous mettez {(etage.nombre_de_bols * 50)} golds dans le{s_ou_pas} bol{s_ou_pas}.")
        services.Player.nombre_de_gold -= (etage.nombre_de_bols * 50)
    etage.nombre_de_bols += 1
    services.Affichage.EntreePourContinuer()


@salle_de_type("JACCUZI")
def reveler_jaccuzi(etage, salle):
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
    print("...un jacuzzi ?")
    services.Affichage.EntreePourContinuer()
    print("La surface de l'eau est troublée par la présence d'un millier de bulles d'air.")
    print("Des volutes de vapeurs s'échappent du chaudron de bois....")
    print("...et des petits êtres jaunes en forme d'étoile paressent à la surface sur d'étranges ballon de baudruche en forme de donut.")
    services.Affichage.EntreePourContinuer()
    while True:
        try:
            print("L'eau chaude cristalline attire votre corps fatigué par ses blessures.")
            print("Votre esprit, lui, est attiré par une sorte de free-form jazz reposant chanté par les êtres dorés.")

            print("\n1 - Rentrer dans le Jacuzzi")
            print("2 - Repartir")
            choix = int(input("\nFaites votre choix avec les nombres : "))
            ClearConsole()
            if choix in [1, 2]:
                break
        except ValueError:
            ClearConsole()
    if choix == 1:
        StopAllMusic()
        print("Vous laissez vos habits dans un petit tas à coté, et rentrez doucement dans l'eau chaude du jacuzzi.")
        services.Affichage.EntreePourContinuer()
        PlayMusic("bathhouse")
        etage.ReposDansJacuzzi()
        PlayMusicDeLetage()
        ClearConsole()
        print("Vous sortez du jacuzzi, et vous rhabillez.")
        print("Vous vous sentez plus détendu que jamais !")
        services.Player.points_de_vie = services.Player.points_de_vie_max
        services.Player.points_de_mana = services.Player.points_de_mana_max
        services.Affichage.EntreePourContinuer()
        print("Le jacuzzi s'éteint et une étrange substance noire recouvre sa surface...")
        services.Affichage.EntreePourContinuer()
        print("Votre corps, débarrassé de ses toxines, semble avoir pollué l'eau de l'étrange méchanisme.")
        print("Vous ne pourrez pas revenir ici.")
        services.Affichage.EntreePourContinuer()
        # fait que l'event soit finit et ne peut ps etre relancé
        salle["terminé par joueur"] = True
    else:
        print("Vous laissez l'étrange structure et repartez d'ou vous venez.")
        services.Affichage.EntreePourContinuer()


@salle_de_type("CHARGEUR")
def reveler_chargeur(etage, salle):
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
    print("...une machine a soda ?")
    services.Affichage.EntreePourContinuer()
    while True:
        try:
            print("Vous pouvez vous servir un verre d'une des boissons proposées, sans savoir l'effet que cela aura.")
            print("\n1 - Boire une boisson aléatoire ")
            print("2 - Partir")
            choix = int(input("\nFaites votre choix avec les nombres : "))
            ClearConsole()
            if choix in [1, 2]:
                break
        except ValueError:
            ClearConsole()
    if choix == 2:
        print("Vous laissez la machine et repartez d'ou vous venez.")
        services.Affichage.EntreePourContinuer()
    elif choix == 1:
        print("Vous prenez un gobelet de plastique rouge et le remplissez avec une des boissons proposées.")
        services.Affichage.EntreePourContinuer()
        print("Vous avalez son contenu et...")
        services.Affichage.EntreePourContinuer()
        liste_de_charge_possible = {1: {"Description" : "...ca pétille dans la bouche !\nL'élément [Foudre] à plus de chance de paralyser !", "Effet" : "Element [Foudre] Surchargé"},
                                    2: {"Description" : "...ca pique comme pas possible !\nL'élément [Feu] à plus de chance de bruler !", "Effet" : "Element [Feu] Surchargé"},
                                    3: {"Description" : "...c'est chaud et chocolaté !\nL'élément [Terre] à plus de chance d'infliger la lapidation !", "Effet" : "Element [Terre] Surchargé"},
                                    4: {"Description" : "...un gout de menthe envahit votre palais !\nL'élément [Glace] à plus de chance de geler !", "Effet" : "Element [Glace] Surchargé"},
                                    5: {"Description" : "...ca a un bon gout d'orange !\nL'élément [Sang] à plus de chance de faire un drain !", "Effet" : "Element [Sang] Surchargé"},
                                    6: {"Description" : "...la texture épaisse et le gout de banane vous dégoute un peu.\nVous reprenez 4 points d'endurance supplémentaire quand vous ne faites pas de techniques !", "Effet" : "Element [Corps] Surchargé"},
                                    7: {"Description" : "...c'était alcoolisé. Beurk !\nGagner un combat fait augmenter le compteur de monstres tués de 2 !", "Effet" : "Element [Ame] Surchargé"},}
        nombre_de_charge_aleatoire = random.randint(1, 7)
        charge_actuelle = liste_de_charge_possible[nombre_de_charge_aleatoire]
        print(charge_actuelle["Description"])
        services.Affichage.EntreePourContinuer()
        services.FloorMaker.GiveRandomArtefact(charge_actuelle["Effet"],"Don")
        print("La machine fait un bruit bizarre, puis un indicateur sur lequel est marqué *EN PANNE* s'allume.")
        services.Affichage.EntreePourContinuer()
        # fait que l'event soit finit et ne peut ps etre relancé
        salle["terminé par joueur"] = True


@salle_de_type("AFFIXEUR_TECHNIQUE")
def reveler_affixeur_technique(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.affixeur_technique()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print("Vous entrez dans la salle, et trouvez une étrange table en plein milieu.")
    services.Affichage.EntreePourContinuer()
    print("Elle est faite dans un materiau proche de l'obsidienne, avec un élégant tapis rouge posé par dessus, quelques diamants encastrés dans ses coins, et un emplacement pour Zeroual au milieu.")
    services.Affichage.EntreePourContinuer()
    print("Vous avez l'impression que des symboles inconnus sortent des taillades tapissants les murs alentours, et viennent disparaitre autour de la table.")
    services.Affichage.EntreePourContinuer()
    liste_techniques_affixables = []
    for technique in services.Player.techniques_possedes:
        if technique in LISTETECHNIQUES or technique == "Attaque Lourde":
            liste_techniques_affixables.append(technique)
    while True:
        try:
            print("Alors que vous posez Zeroual au centre de la table, des visions de vous entrain d'effectuer des techniques envahissent votre esprit.")
            numero = 1
            print("\n1 - Partir")
            if services.Player.malediction == "Ordinaire":
                print("*D'anciennes forces maudites interfèrent avec vos pensées. Vous ne pouvez pas enchanter.*")
            else:
                for technique in liste_techniques_affixables :
                    numero += 1
                    print(f"{numero} - Penser à {technique}")
            choix = int(input("\nFaites votre choix avec les nombres : "))
            ClearConsole()
            if choix in range (1, (numero + 1)):
                break
        except ValueError:
            ClearConsole()
    if choix == 1:
        print("Vous retirez Zeroual et sortez de la salle.")
        services.Affichage.EntreePourContinuer()
    else:
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

        technique_choisie_a_afficher = technique_choisie
        services.Player.techniques_possedes.remove(technique_choisie)
        technique_choisie += f" {affix_choisi}"
        services.Player.techniques_possedes.append(technique_choisie)
        print("Vous approchez Zeroual du centre de la table, et celui ci se transforme en livre lévitant a quelques centimètres de celle ci.")
        services.Affichage.EntreePourContinuer()
        # fait que l'event soit finit et ne peut ps etre relancé
        salle["terminé par joueur"] = True
        services.Save.SaveTheGameSansAffichage()
        print(f"Vous pensez alors a la technique {technique_choisie_a_afficher}, et les symboles inconnus tout autours convergent vers une des pages de Zeroual.")
        services.Affichage.EntreePourContinuer()
        print(f"Votre technique gagne l'enchantement [{affix_choisi}] !")
        services.Affichage.EntreePourContinuer()
        print("Les symboles disparaissent, et Zeroual reprend sa forme de base.")
        services.Affichage.EntreePourContinuer()


@salle_de_type("AFFIXEUR_SORT")
def reveler_affixeur_sort(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.affixeur_sort()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print("Vous entrez dans la salle, et trouvez une étrange table en plein milieu.")
    services.Affichage.EntreePourContinuer()
    print("Elle est faite dans un materiau proche de l'obsidienne, avec un élégant tapis rouge posé par dessus, quelques diamants encastrés dans ses coins, et un emplacement pour Zeroual au milieu.")
    services.Affichage.EntreePourContinuer()
    print("Vous avez l'impression que des symboles inconnus sortent de livres posés négligemment tout autour, et viennent disparaitre autour de la table.")
    services.Affichage.EntreePourContinuer()
    liste_sorts_affixables = []
    for sort in services.Player.sorts_possedes :
        if sort in LISTESORTS or sort == "Missile Arcanique":
            liste_sorts_affixables.append(sort)
    while True:
        try:
            print("Alors que vous posez Zeroual au centre de la table, des visions de vous entrain d'effectuer des sorts envahissent votre esprit.")
            print("\n1 - Partir")
            numero = 1
            if services.Player.malediction == "Ordinaire":
                print("*D'anciennes forces maudites interfèrent avec vos pensées. Vous ne pouvez pas enchanter.*")
            else:
                for sort in liste_sorts_affixables :
                    numero += 1
                    print(f"{numero} - Penser à {sort}")
            choix = int(input("\nFaites votre choix avec les nombres : "))
            ClearConsole()
            if choix in range (1, (numero + 1)):
                break
        except ValueError:
            ClearConsole()
    if choix == 1:
        print("Vous retirez Zeroual et sortez de la salle.")
        services.Affichage.EntreePourContinuer()
    else:
        sort_choisie = liste_sorts_affixables[(choix - 2)]
        liste_affix = ["~Rouge~", # +2 vie
                       "~Carmin~", # +4 vie
                       "~Violet~", # +2 mana
                       "~Pourpre~", # +4 mana
                       "~Jaune~", # +2 endurance
                       "~Doré~", # +4 endurance
                       "~Lolipop~", # +1 vie mana endurance
                       "~Bubblegum~", # +3 vie mana endurance
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

        sort_choisie_a_afficher = sort_choisie
        services.Player.sorts_possedes.remove(sort_choisie)
        sort_choisie += f" {affix_choisi}"
        services.Player.sorts_possedes.append(sort_choisie)
        print("Vous approchez Zeroual du centre de la table, et celui ci se transforme en livre lévitant a quelques centimètres de celle ci.")
        services.Affichage.EntreePourContinuer()
        # fait que l'event soit finit et ne peut ps etre relancé
        salle["terminé par joueur"] = True
        services.Save.SaveTheGameSansAffichage()
        print(f"Vous pensez alors au sort {sort_choisie_a_afficher}, et les symboles inconnus tout autours convergent vers une des pages de Zeroual.")
        services.Affichage.EntreePourContinuer()
        print(f"Votre sort gagne l'enchantement [{affix_choisi}] !")
        services.Affichage.EntreePourContinuer()
        print("Les symboles disparaissent, et Zeroual reprend sa forme de base.")
        services.Affichage.EntreePourContinuer()


@salle_de_type("DISTRIBUTEUR")
def reveler_distributeur(etage, salle):
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
    print("...un distributeur !")
    services.Affichage.EntreePourContinuer()
    while True:
        while True:
            try:
                print("Vous pouvez voir une fente pour inserer de l'argent, et une jolie sélection d'artefacts derrière la vitre.")
                print("Un avertissement écrit en petit caractères prévient de la casse (presque) inévitable des artefacts présents a chaque changement d'étage.")
                print(f"Vous avez {services.Player.nombre_de_gold} golds sur vous.")
                print(f"\n1 - Acheter [Epée de Damocles] pour {services.Player.numero_de_letage * 30} golds") #15 % de dmg, 2% chance que ca brise et fasse 15% vie
                print(f"2 - Acheter [Morceau d'Ether Fragile] pour {services.Player.numero_de_letage * 30} golds") #15 % de sorts, 2% chance que ca brise et vide toute mana
                print(f"3 - Acheter [Eau Bénite] pour {services.Player.numero_de_letage * 60} golds") #5% chance d'etre béni pas tour
                print(f"4 - Acheter [Bandeau Catharsis] pour {services.Player.numero_de_letage * 45} golds") #5% cahnce esquive, prend 10% degat en plus
                print(f"5 - Acheter [Charbon Primordial] pour {services.Player.numero_de_letage * 50} golds") #+1 tour de brulure
                print(f"6 - Acheter [Saphir de Gel] pour {services.Player.numero_de_letage * 50} golds") #+1 tour de gel
                print(f"7 - Acheter [Fossile Figé] pour {services.Player.numero_de_letage * 50} golds") #+5% chance de faire lapidation
                print(f"8 - Acheter [Fiole des Eclairs] pour {services.Player.numero_de_letage * 50} golds") #+5% chance de faire paralysie
                print(f"9 - Acheter [Assurance Distributeur] pour {services.Player.numero_de_letage * 50} golds") #+garde les items 1 etage supplementaire
                print("10 - Partir")
                choix = int(input("\nFaites votre choix avec les nombres : "))
                ClearConsole()
                if choix in range(1, 11):
                    break
            except ValueError:
                ClearConsole()
        if choix == 10:
            print("Vous laissez le distributeur, non sans tenter de trouver des golds en dessous (Il n'y en avait pas).")
            services.Affichage.EntreePourContinuer()
            break
        else:
            dictionaire_item_distributeur = {1 : {"Nom" : "Epée de Damocles", "Prix" : (services.Player.numero_de_letage * 30), "Description" : "Une épée suintant l'anxiété, ayant appartenue a un ancien roi.\nLes dégâts de vos techniques augmentent de 25%, mais il y a une faible probabilité que l'artefact vous tombe dessus, se brisant sur votre crane et vous infligeant de lourds dégâts."},
                                             2 : {"Nom" : "Morceau d'Ether Fragile", "Prix" : (services.Player.numero_de_letage * 30), "Description" : "Un catalyste pour les sorts très fragile, extrait directement de la fabrique de la réalité.\nLes dégâts de vos sorts augmentent de 25%, mais il y a une faible probabilité que l'artefact se brise spontanément, vous vidant alors de tout vos points de mana."},
                                             3 : {"Nom" : "Eau Bénite", "Prix" : (services.Player.numero_de_letage * 60), "Description" : "Une fiole légendaire devant laquelle des papes dévoués ont prié jours et nuits pendant 50 ans d'affilée.\nVous avez une faible chance d'être béni par le Feu Divin à la fin de chaque tours."},
                                             4 : {"Nom" : "Bandeau Catharsis", "Prix" : (services.Player.numero_de_letage * 45), "Description" : "Un bandeau magique a se mettre devant les yeux, afin d'affuter les sens.\nVos chances d'esquive augmentent, ainsi que les dégats que l'on vous inflige."},
                                             5 : {"Nom" : "Charbon Primordial", "Prix" : (services.Player.numero_de_letage * 50), "Description" : "Un reste du tout premier feu de bois, enseigné par Promethée aux humains.\nL'effet Brulure que vous infligez dure 1 tour de plus."},
                                             6 : {"Nom" : "Saphir de Gel", "Prix" : (services.Player.numero_de_letage * 50), "Description" : "La culmination de millénaires de pression par la neige sur un morceau de neige du tout premier age glaciaire .\nL'effet Gel que vous infligez dure 1 tour de plus."},
                                             7 : {"Nom" : "Fossile Figé", "Prix" : (services.Player.numero_de_letage * 50), "Description" : "Le fossile d'un animal rare vivant il y a des millions d'années de ca, débordant de vitalité, que seul le processus de diagénèse autour de lui a su arrêter.\nL'effet Lapidation a un peu plus de chance de réussir."},
                                             8 : {"Nom" : "Fiole des Eclairs", "Prix" : (services.Player.numero_de_letage * 50), "Description" : "Un des éclairs de Zeus, jalousement gardé par un humain qui avait réussi a l'enfermer dans une amphore vide de vin, que le dieu de la foudre à oublié sur terre lors de sa dernière échappée avec la femme de l'humain en question.\nL'effet Paralysie a un peu plus de chance de réussir.  "},
                                             9 : {"Nom" : "Assurance Distributeur", "Prix" : (services.Player.numero_de_letage * 50), "Description" : "Un bout de papier assurant a son porteur que les artefacts qu'il a acheté au distributeur ne se briseront pas pour 1 changement d'étage.\nVous pouvez en acheter plusieurs bien sur !"}}
            item_choisi = dictionaire_item_distributeur[choix]
            if services.Player.nombre_de_gold < item_choisi["Prix"]:
                print("Vous n'avez pas assez d'argent !")
                services.Affichage.EntreePourContinuer()
            else:
                services.Player.nombre_de_gold -= item_choisi["Prix"]
                services.FloorMaker.GiveRandomArtefact(item_choisi["Nom"],"Don")
                print("Vous inserez l'argent dans la machine, tapez le code sur le clavier numérique, et patientez quelques instants.")
                attendre(10)
                services.Affichage.EntreePourContinuer()
                print("L'artefact tombe enfin dans la chute, et vous pouvez le récuperer.")
                services.Affichage.EntreePourContinuer()
                print(f"Vous obtenez l'artefact [{item_choisi['Nom']}] !")
                print(item_choisi["Description"])
                services.Affichage.EntreePourContinuer()


@salle_de_type("CHENIL")
def reveler_chenil(etage, salle):
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
    print("...une jolie niche rose fermée !")
    services.Affichage.EntreePourContinuer()
    while True:
        try:
            print("Vous pouvez voir une fente pour inserer de l'argent, et un panneau juste en dessous lit :\n* CHIEN AUTONOME de NACRE ININFLAMMABLE GARDANT et OBEISSANT son UTILISATEUR : 100 golds *")
            print("\n1 - Mettre les golds dans la fente")
            print("2 - Partir")
            choix = int(input("\nFaites votre choix avec les nombres : "))
            ClearConsole()
            if choix in [1, 2]:
                break
        except ValueError:
            ClearConsole()
    if choix == 2:
        print("Vous pensez a votre bourse et refusez cet achat compulsif.")
        services.Affichage.EntreePourContinuer()
    elif choix == 1:
        if services.Player.nombre_de_gold >= 100:
            print("Vous pensez a votre bourse et vous vous cédez à cet achat compulsif.")
            services.Affichage.EntreePourContinuer()
            print("Au bout du 100eme gold inséré, la porte de la niche s'ouvre et un chien bionique en sort !")
            services.Affichage.EntreePourContinuer()
            print("Ce dernier, relié a un tuyau greffé dans son cou, ouvre doucement les yeux et vous regarde d'un air exalté !")
            services.Affichage.EntreePourContinuer()
            print("Alors qu'il se frotte a vos jambes et a votre main, vous le décrochez de sa station de vie artificielle et trouvez un collier contenant son nom en lettres manuscriptes :")
            services.Affichage.EntreePourContinuer()
            print("C.A.N.I.G.O.U.")
            services.Affichage.EntreePourContinuer()
            print("Vous obtenez Canigou !")
            print("Ce chien a moitié cyborg fait des dégâts a vos ennemis a chaque fin de tour !")
            services.Player.nombre_de_gold -= 100
            services.FloorMaker.GiveRandomArtefact("Canigou","Don")
            services.Affichage.EntreePourContinuer()
            print("Vous sortez de la salle avec votre nouveau compagnon.")
            services.Affichage.EntreePourContinuer()
            # fait que l'event soit finit et ne peut ps etre relancé
            salle["terminé par joueur"] = True
        else:
            print("Vous regardez votre bourse avec insistance, mais aucun gold supplémentaire n'apparait.")
            services.Affichage.EntreePourContinuer()
            print("Décu, vous tournez les talons et sortez de la salle.")
            services.Affichage.EntreePourContinuer()


@salle_de_type("BUFFET")
def reveler_buffet(etage, salle):
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
    print("...un buffet a volonté !")
    services.Affichage.EntreePourContinuer()
    print("Ou plutot un faux buffet, vu que toute la nourriture est faite de plastique.")
    services.Affichage.EntreePourContinuer()
    while True:
        try:
            print("Au centre de la table, une réplique de la corne d'abondance semble attirer votre regard.")
            print("\n1 - Mettre votre main dans la corne")
            print("2 - Partir")
            choix = int(input("\nFaites votre choix avec les nombres : "))
            ClearConsole()
            if choix in [1, 2]:
                break
        except ValueError:
            ClearConsole()
    if choix == 2:
        print("Vous laissez la scène en place et repartez, une petite faim commencant a pointer le bout de son nez.")
        services.Affichage.EntreePourContinuer()
    elif choix == 1:
        print("Vous plongez votre main dans la corne d'abondance, et sentez votre énergie diminuer.")
        print("Vous perdez 10 points de vie et de mana max !")
        services.Affichage.EntreePourContinuer()
        print("Cepandant, vous arrivez à ressortir de la corne une suite d'objets aléatoires, accrochés les uns aux autres par un fil de laine rouge.")
        services.Affichage.EntreePourContinuer()
        liste_ditem_possibles = LISTEITEM
        liste_ditem_possibles.append("Redcoin")
        liste_ditem_recus = []
        for _ in range (1,6):
            nom_de_litem = GetRandomItemFromList(liste_ditem_possibles)
            if nom_de_litem == "Redcoin":
                services.Player.nombre_de_red_coin += 1
            else:
                services.Player.items_possedes[nom_de_litem] += 1
            liste_ditem_recus.append(nom_de_litem)
        print(f"Vous obtenez les objets {liste_ditem_recus} !")
        services.Affichage.EntreePourContinuer()
        print("La corne se brise alors subitement, et la nourriture sur la table semble pourrir de manière accélérée.")
        services.Affichage.EntreePourContinuer()
        # fait que l'event soit finit et ne peut ps etre relancé
        salle["terminé par joueur"] = True
        services.Player.points_de_mana_max -= 10
        if services.Player.points_de_mana_max < 0 :
            services.Player.points_de_mana_max = 0
        if services.Player.points_de_mana > services.Player.points_de_mana_max :
            services.Player.points_de_mana == services.Player.points_de_mana_max
        services.Player.points_de_vie_max -= 10
        if services.Player.points_de_vie_max < 1 :
            services.Player.points_de_vie_max = 1
        if services.Player.points_de_vie > services.Player.points_de_vie_max :
            services.Player.points_de_vie == services.Player.points_de_vie_max        
