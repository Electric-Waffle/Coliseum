"""Attractions : atelier, loterie, braziers et pêche."""

import random

from coliseum import services
from coliseum.audio import PlayMusicDeLetage
from coliseum.console import ClearConsole
from coliseum.donnees.actions import LISTESORTS, LISTETECHNIQUES
from coliseum.donnees.items import LISTEITEM, LISTEITEMAVANCE, LISTEITEMBASE, LISTEITEMUPPGRADE
from coliseum.combat.lancement import livrer_combat
from coliseum.histoire.village import CheckForKIA
from coliseum.exploration.salles.registre import salle_de_type


@salle_de_type("WORKSHOP")
def reveler_workshop(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.workshop()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print("Vous vous préparez a entrer dans la salle, et sentez une chaleur immense alors que votre arme vibre d'excitation.")
    services.Affichage.EntreePourContinuer()
    print("A l'interieur, vous voyez des cascades de lave en fusion s'écoulant des deux côtés d'une impressionante collection d'outils en tout genre, posé sur une grosse enclume.")
    services.Affichage.EntreePourContinuer()
    print("Alors que vous touchez les outils recouverts de poussière, des visions s'emparent de votre esprit.")
    print("Le bruit des marteaux sur l'enclume, la sensation de la sueur sur la peau, et plusieurs dizaines de personnes travaillant sur une petite boule blanche.")
    services.Affichage.EntreePourContinuer()
    print("Vous reconnaissez ici le berceau et lieu de fabrication de Zeroual, votre arme !")
    services.Affichage.EntreePourContinuer()
    while True:
        while True:
            try:
                print("Les visions vous donnent les capacités et connaissances nécessaires a la modification de votre arme.")
                print(f"\n            - Zeroual : {services.Player.nombre_de_monstres_tues} âmes -")
                print("\n1 - Changer l'ordre des techniques")
                print("2 - Changer l'ordre des sorts")
                print("\n            - Techniques -")
                print("3 - Enchanter une technique avec un mot de puissance aléatoire [15 âmes]")
                print("4 - Enchanter une technique avec un mot de puissance élémentaire [15 âmes + 5 cristaux élémentaires]")
                print("5 - Elever une technique au niveau superieur [25 âmes]")
                print("\n            - Sorts -")
                print("6 - Enchanter un sort avec un mot de puissance aléatoire [15 âmes]")
                print("7 - Enchanter un sort avec un mot de puissance élémentaire [15 âmes + 5 cristaux élémentaires]")
                print("8 - Elever un sort au niveau superieur [25 âmes]")
                print("\n            - Autre -")
                print("9 - Partir")
                choix = int(input("\nFaites votre choix avec les nombres : "))
                ClearConsole()
                if choix in range(1, 10):
                    break
            except ValueError:
                ClearConsole()
        if choix == 1 and len(services.Player.techniques_possedes) > 0:
            #liste_de_ techniques nouvellement ordonné, temporaire
            liste_technique_nouvel_ordre = []
            #liste de techniques disponibles
            liste_technique_disponibles = list(services.Player.techniques_possedes)
            while True:
                while True:
                    try:
                        print(f"Nouvel Ordre des techniques : {liste_technique_nouvel_ordre}\n")
                        numero = 1
                        for action in liste_technique_disponibles:
                            print(f"{numero} - {action}")
                            numero += 1
                        choix = int(input("\nChoisissez avec les nombres la prochaine technique de votre nouvelle liste : "))
                        ClearConsole()
                        if choix in range(1, len(liste_technique_disponibles) + 1):
                            break
                    except ValueError:
                        ClearConsole()
                technique_choisie = liste_technique_disponibles[choix - 1]
                liste_technique_disponibles.remove(technique_choisie)
                liste_technique_nouvel_ordre.append(technique_choisie)
                if len(liste_technique_disponibles) == 0 :
                    print("Vous posez Zeroual sur l'enclume et frappez dessus avec une masse rectangulaire à des points bien spécifiques.")
                    print("L'ordre avec lequel les techniques sont présentées a changé !")
                    services.Affichage.EntreePourContinuer()
                    services.Player.techniques_possedes = list(liste_technique_nouvel_ordre)
                    break
        elif choix == 2 and len(services.Player.sorts_possedes) > 0:
            #liste_de_ techniques nouvellement ordonné, temporaire
            liste_sort_nouvel_ordre = []
            #liste de techniques disponibles
            liste_sort_disponibles = list(services.Player.sorts_possedes)
            while True:
                while True:
                    try:
                        print(f"Nouvel Ordre des sorts : {liste_sort_nouvel_ordre}\n")
                        numero = 1
                        for action in liste_sort_disponibles:
                            print(f"{numero} - {action}")
                            numero += 1
                        choix = int(input("\nChoisissez avec les nombres le prochain sort de votre nouvelle liste : "))
                        ClearConsole()
                        if choix in range(1, len(liste_sort_disponibles) + 1):
                            break
                    except ValueError:
                        ClearConsole()
                sort_choisie = liste_sort_disponibles[choix - 1]
                liste_sort_disponibles.remove(sort_choisie)
                liste_sort_nouvel_ordre.append(sort_choisie)
                if len(liste_sort_disponibles) == 0 :
                    print("Vous posez Zeroual sur l'enclume et frappez dessus avec un étrange marteau à des points bien spécifiques.")
                    print("L'ordre avec lequel les sorts sont présentés a changé !")
                    services.Affichage.EntreePourContinuer()
                    services.Player.sorts_possedes = list(liste_sort_nouvel_ordre)
                    break  
        elif choix == 3 and services.Player.nombre_de_monstres_tues >= 15 and len(services.Player.techniques_possedes) > 0:
            print("Vous prenez Zeroual avec des pinces et le plongez dans la rivière de lave.")
            services.Affichage.EntreePourContinuer()
            liste_techniques_affixables = []
            for technique in services.Player.techniques_possedes:
                liste_techniques_affixables.append(technique)
            while True:
                while True:
                    try:
                        print("Puis, vous pensez a une technique.")
                        print("\n1 - Arreter")
                        numero = 1
                        if services.Player.malediction == "Ordinaire":
                            print("*D'anciennes forces maudites interfèrent avec vos pensées. Vous ne pouvez pas enchanter.*")
                        else:
                            for tut in liste_techniques_affixables :
                                numero += 1
                                print(f"{numero} - Penser à {tut}")
                        choix = int(input("\nFaites votre choix avec les nombres : "))
                        ClearConsole()
                        if choix in range (1, (numero + 1)):
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 1:
                    print("Vous retirez Zeroual de la lave.")
                    services.Affichage.EntreePourContinuer()
                    break
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
                    services.Player.nombre_de_monstres_tues -= 15
                    print("Vous sentez Zeroual vibrer, et le sortez de son bain de roche en fusion.")
                    print("Ensuite, vous le posez délicatement a terre, et le transpercez d'un coup sec avec une lame rouillée gravée de nombreuses inscriptions.")
                    services.Save.SaveTheGameSansAffichage()
                    services.Affichage.EntreePourContinuer()
                    print(f"Les inscriptions s'illuminent, puis descendent vers l'orbe.")
                    services.Affichage.EntreePourContinuer()
                    print(f"La technique {technique_choisie_a_afficher} gagne l'enchantement [{affix_choisi}] !")
                    services.Affichage.EntreePourContinuer()
                    print("Les inscriptions retournent dans la lame, et vous la retirez de l'orbe blanc.")
                    services.Affichage.EntreePourContinuer()
                    break
        elif choix == 4 and services.Player.nombre_de_monstres_tues >= 15 and services.Player.items_possedes["Crystal Elémentaire"] >= 5 and len(services.Player.techniques_possedes) > 0:
            print("Vous rapprochez vos crystaux élémentaires, prenez Zeroual avec des pinces, et le plongez dans la rivière de lave.")
            services.Affichage.EntreePourContinuer()
            liste_techniques_affixables = []
            for technique in services.Player.techniques_possedes:
                liste_techniques_affixables.append(technique)
            while True:
                while True:
                    try:
                        print("Puis, vous pensez a une technique.")
                        print("\n1 - Arreter")
                        numero = 1
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
                    print("Vous retirez Zeroual de la lave.")
                    services.Affichage.EntreePourContinuer()
                    break
                else:
                    technique_choisie = liste_techniques_affixables[(choix - 2)]
                    liste_affix = [
                                "~Ordre~", # peut bruler
                                "~Aveugle~", # peut geler
                                "~Limitation~", # peut lapider
                                "~Transcendance~", # peut paralyser
                                "~Eveil~", # peut drainer
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
                    services.Player.nombre_de_monstres_tues -= 15
                    services.Player.items_possedes["Crystal Elémentaire"] -= 5
                    print("Vous sentez Zeroual vibrer, mais le laissez dans son bain de roche en fusion.")
                    print("Vous en profitez pour réduire les crystaux en une poudre fine que vous mouillez avec un liquide nacré avant d'appliquer sur une lame rouillée gravée de nombreuses inscriptions.")
                    services.Save.SaveTheGameSansAffichage()
                    print("Vous entendez votre arme vibrer de plus en plus, et la sortez de la lave avant de la transpercer avec la lame rouillée.")
                    services.Save.SaveTheGameSansAffichage()
                    services.Affichage.EntreePourContinuer()
                    print(f"Les inscriptions s'illuminent, puis passent a travers la pate élémentaire en descendant vers l'orbe.")
                    services.Affichage.EntreePourContinuer()
                    print(f"La technique {technique_choisie_a_afficher} gagne l'enchantement [{affix_choisi}] !")
                    services.Affichage.EntreePourContinuer()
                    print("Les inscriptions retournent dans la lame, et vous la retirez de l'orbe blanc.")
                    print("La pate élémentaire se durcit, et vous passez quelques minutes a l'enlever de la lame.")
                    services.Affichage.EntreePourContinuer()
                    break
        elif choix == 5 and services.Player.nombre_de_monstres_tues >= 25 and len(services.Player.techniques_possedes) > 0:
            print("Vous ouvrez une boite noire chaude au toucher, et y rentrez Zeroual.")
            services.Affichage.EntreePourContinuer()
            #faire liste action evoluable
            liste_action_qui_peut_evoluer = [
                "Attaque Légère",
                "Lance Rapide",
                "Lance Statique",
                "Lance Electrique",
                "Lance de l'Eclair",
                "Lance Foudroyante",
                "Bô Chaud",  #
                "Bô Brulant",  #
                "Bô Enflammé",  #
                "Bô de la Fournaise",
                "Bô Magmatique",
                "Katana Bleu",
                "Katana Froid",
                "Katana Givré",
                "Katana Glacial",
                "Katana Polaire",
                "Corne Argile",  #
                "Corne Lapis",  #
                "Corne Granite",  #
                "Corne Obsidienne",
                "Corne de la Montagne",
                "Poing Léger",  #
                "Poing Renforcé",  #
                "Poing Lourd",  #
                "Poing Maitrisé",  #
                "Poing Fatal",  #
                "Dague Volevie",
                "Dague Siphoneuse",
                "Dague Vampirique",
                "Dague Parasite",
                "Dague Destructrice"]
            liste_action_en_possession = []
            for action in services.Player.techniques_possedes:
                if action in liste_action_qui_peut_evoluer:
                    liste_action_en_possession.append(action)

            while True:
                try:
                    print("Vous refermez la boite et pensez a une technique.")
                    print("\n1 - Arrêter")
                    numero = 2
                    for action in liste_action_en_possession:
                        print(f"{numero} - {action}")
                        numero += 1
                    choix = int(input("\nFaites votre choix avec les nombres : "))
                    ClearConsole()
                    if choix in range (1, (numero)):
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print("Vous sortez Zeroual de la boite.")
                services.Affichage.EntreePourContinuer()
            else:
                nom_action_a_evoluer = liste_action_en_possession[choix - 2]
                services.Player.nombre_de_monstres_tues -= 25

                #trouver son evolution
                if nom_action_a_evoluer == "Attaque Légère":
                    nom_nouvelle_action = "Attaque Lourde"
                    description = "La technique"
                    services.Player.techniques_possedes.remove(nom_action_a_evoluer)
                    services.Player.techniques_possedes.append(nom_nouvelle_action)
                elif nom_action_a_evoluer in LISTETECHNIQUES:
                    position_de_laction = LISTETECHNIQUES.index(nom_action_a_evoluer)
                    nom_nouvelle_action = LISTETECHNIQUES[position_de_laction + 1]
                    description = "La technique"
                    services.Player.techniques_possedes.remove(nom_action_a_evoluer)
                    services.Player.techniques_possedes.append(nom_nouvelle_action)

                print("La boite s'active alors, et un constant bourdonnement s'en échappe.")
                print("Vous pouvez soudainement voir a travers une des face teintée de la boite, et trouvez votre arme entrain de tourner sur elle même, éclairé par une lumière jaune.")
                print("Un nombre incalculable de minuscules éclairs percant sa surface. ")
                services.Affichage.EntreePourContinuer()
                print("La boite fait alors 4 bips stridents, et tout s'arrête.")
                services.Affichage.EntreePourContinuer()
                print(f"La technique [{nom_action_a_evoluer}] devient [{nom_nouvelle_action}] !")
                services.Affichage.EntreePourContinuer()
                print("Vous récuperez Zeroual.")
                print("Il est chaud au toucher !")
                services.Affichage.EntreePourContinuer()
        elif choix == 6 and services.Player.nombre_de_monstres_tues >= 15 and len(services.Player.sorts_possedes) > 0:
            print("Vous prenez Zeroual avec des pinces et le plongez dans la rivière de lave.")
            services.Affichage.EntreePourContinuer()
            liste_sorts_affixables = []
            for sort in services.Player.sorts_possedes:
                liste_sorts_affixables.append(sort)
            while True:
                while True:
                    try:
                        print("Puis, vous pensez a un sort.")
                        print("\n1 - Arreter")
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
                    print("Vous retirez Zeroual de la lave.")
                    services.Affichage.EntreePourContinuer()
                    break
                else:
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

                    sort_choisie_a_afficher = sort_choisie
                    services.Player.sorts_possedes.remove(sort_choisie)
                    sort_choisie += f" {affix_choisi}"
                    services.Player.sorts_possedes.append(sort_choisie)
                    services.Player.nombre_de_monstres_tues -= 15
                    print("Vous sentez Zeroual vibrer, et le sortez de son bain de roche en fusion.")
                    print("Ensuite, vous le posez délicatement a terre, et répétez en boucle une sort de formule magique, ou prière.")
                    services.Save.SaveTheGameSansAffichage()
                    services.Affichage.EntreePourContinuer()
                    print(f"Pendant de courts instants, des symboles apparaissent autour de votre arme.")
                    services.Affichage.EntreePourContinuer()
                    print(f"Le sort {sort_choisie_a_afficher} gagne l'enchantement [{affix_choisi}] !")
                    services.Affichage.EntreePourContinuer()
                    print("Vous hurlez un mot terrible, et le processus s'arrête brusquement.")
                    services.Affichage.EntreePourContinuer()
                    break
        elif choix == 7 and services.Player.nombre_de_monstres_tues >= 15 and len(services.Player.sorts_possedes) > 0:
            print("Vous prenez Zeroual avec des pinces, rassemblez vos crystaux élémentaires, et le plongez dans la rivière de lave.")
            services.Affichage.EntreePourContinuer()
            liste_sorts_affixables = []
            for sort in services.Player.sorts_possedes:
                liste_sorts_affixables.append(sort)
            while True:
                while True:
                    try:
                        print("Puis, vous pensez a un sort.")
                        print("\n1 - Arreter")
                        numero = 1
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
                    print("Vous retirez Zeroual de la lave.")
                    services.Affichage.EntreePourContinuer()
                    break
                else:
                    sort_choisie = liste_sorts_affixables[(choix - 2)]
                    liste_affix = [
                                "~Ordre~", # peut bruler
                                "~Aveugle~", # peut geler
                                "~Limitation~", # peut lapider
                                "~Transcendance~", # peut paralyser
                                "~Eveil~", # peut drainer
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
                    services.Player.nombre_de_monstres_tues -= 15
                    services.Player.items_possedes["Crystal Elémentaire"] -= 5
                    print("Vous sentez Zeroual vibrer, mais le laissez dans son bain de roche en fusion.")
                    print("A la place, vous sortez un vieux livre, et préparez une tasse de thé avec les crystaux réduits en poudre.")
                    print("Alors que votre thé se termine, vous le buvez d'un coup et observez les figures laissées au fond de la tasse par le reste de crystaux élémentaires.")
                    print("Vous vous servez ensuite du livre pous assigner un mot a chaque figure, et le notez sur un morceau de papier.")
                    services.Save.SaveTheGameSansAffichage()
                    services.Affichage.EntreePourContinuer()
                    print(f"Vous sortez votre arme de la lave alors qu'elle vibre sans ménagement, la posez a terre, et lisez seulement les mots que vous avez notés.")
                    print("Zeroual s'arrête alors de vibrer.")
                    services.Affichage.EntreePourContinuer()
                    print(f"Le sort {sort_choisie_a_afficher} gagne l'enchantement [{affix_choisi}] !")
                    services.Affichage.EntreePourContinuer()
                    print("Vous vous préparez une tasse de véritable thé en attendant que Zeroual refroidisse, pour enlever le gout de cailloux dans votre bouche.")
                    services.Affichage.EntreePourContinuer()
                    break
        elif choix == 8 and services.Player.nombre_de_monstres_tues >= 25 and len(services.Player.sorts_possedes) > 0:
            print("Vous ouvrez une boite blanche froide au toucher, et y rentrez Zeroual.")
            services.Affichage.EntreePourContinuer()
            #faire liste action evoluable
            liste_action_qui_peut_evoluer = [
                "Tir Arcanique",
                "Faisceau Rapide",
                "Faisceau Statique",
                "Faisceau Electrique",
                "Faisceau de l'Eclair",
                "Faisceau Foudroyant",
                "Thermosphère Chaude",
                "Thermosphère Brulante",
                "Thermosphère Enflammée",
                "Thermosphère de la Fournaise",
                "Thermosphère Magmatique",
                "Pic Bleu",
                "Pic Froid",
                "Pic Givré",
                "Pic Glacial",
                "Pic Polaire",
                "Création d'Argile",
                "Création de Lapis",
                "Création de Granite",
                "Création Obsidienne",
                "Création de la Montagne",
                "Explosion Légère",
                "Explosion Renforcée",
                "Explosion Lourde",
                "Explosion Maitrisée",
                "Explosion Fatale",
                "Dance Volevie",
                "Dance Siphoneuse",
                "Dance Vampirique",
                "Dance Parasite",
                "Dance Destructrice",
                "Sonata Pitoyable",  # 3% ou 8pv
                "Sonata Miséricordieuse",  # 5% ou 15pv
                "Sonata Empathique",  # 12% ou 20pv
                "Sonata Sincère",  # 17% ou 25pv
                "Sonata Bienveillante",  # 20% ou 33pv
                ]
            liste_action_en_possession = []
            for action in services.Player.sorts_possedes:
                if action in liste_action_qui_peut_evoluer:
                    liste_action_en_possession.append(action)

            while True:
                try:
                    print("Vous refermez la boite et pensez a un sort.")
                    print("\n1 - Arrêter")
                    numero = 2
                    for action in liste_action_en_possession:
                        print(f"{numero} - {action}")
                        numero += 1
                    choix = int(input("\nFaites votre choix avec les nombres : "))
                    ClearConsole()
                    if choix in range (1, (numero)):
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print("Vous sortez Zeroual de la boite.")
                services.Affichage.EntreePourContinuer()
            else:
                #trouver son evolution
                services.Player.nombre_de_monstres_tues -= 25
                nom_action_a_evoluer = liste_action_en_possession[choix - 2]

                if nom_action_a_evoluer == "Tir Arcanique":
                    nom_nouvelle_action = "Missile Arcanique"
                    services.Player.sorts_possedes.remove(nom_action_a_evoluer)
                    services.Player.sorts_possedes.append(nom_nouvelle_action)
                elif nom_action_a_evoluer in LISTESORTS:
                    position_de_laction = LISTESORTS.index(nom_action_a_evoluer)
                    nom_nouvelle_action = LISTESORTS[position_de_laction + 1]
                    services.Player.sorts_possedes.remove(nom_action_a_evoluer)
                    services.Player.sorts_possedes.append(nom_nouvelle_action)

                print("Vous sentez qu'un changement s'opère dans la boite, et un petit vent chaud se met a sortir de derrière.")
                print("Vous essayez d'ouvrir la boite, mais n'y arrivez pas.")
                services.Affichage.EntreePourContinuer()
                print("Vous vous installez confortablement et faites un petit somme.")
                services.Affichage.EntreePourContinuer()
                print("Quelques heures plus tard, un bruit de déclic vous réveille, et la porte de la boite s'ouvre d'elle même.")
                services.Affichage.EntreePourContinuer()
                print(f"La technique [{nom_action_a_evoluer}] devient [{nom_nouvelle_action}] !")
                services.Affichage.EntreePourContinuer()
                print("Vous récuperez Zeroual.")
                print("Il est froid au toucher !")
                services.Affichage.EntreePourContinuer()
        elif choix == 9:
            print("Vous sortez de la salle, et les visions disparaissent.")
            services.Affichage.EntreePourContinuer()
            break
        else:
            print("Impossible !")
            services.Affichage.EntreePourContinuer()


@salle_de_type("LOTTERIE")
def reveler_lotterie(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.lotterie()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print("Vous rentrez dans la salle et fermez les yeux.")
    services.Affichage.EntreePourContinuer()
    print("Devant vous, il y a des murs recouverts d'une tapisserie kitch de couleur rose, ainsi que des rubans verts accrochés au plafond, et des lumières aveuglantes provenant de différentes sources un peu partout.")
    services.Affichage.EntreePourContinuer()
    print("Alors que vos yeux s'habituent a l'horrible mélange de formes et couleurs qui compose la salle, vous arrivez a discerner les contour d'un bloc de roche complètement, absolument, totalement, noir.")
    print("Vous avez l'impression que même la lumière ne peut s'échapper du monolithe.")
    services.Affichage.EntreePourContinuer()
    print("Vous vous approchez de la chose, et des lettres de lumières apparaissent a sa surface.")
    services.Affichage.EntreePourContinuer()
    etage.TraderIncAnimationOpen()
    while True:
        while True:
            try:
                print("                       ||")
                print("                      ||||")
                print("                     ||  ||")
                print("                    ||||||||")
                print("                   |||    |||")
                print("                  || ||  || ||")
                print("                 ||   ||||   ||")
                print("                ||     ||     ||")
                print("               ||||||||||||||||||")
                print("")
                print("")
                print("              Traders Incorporated")
                print("                Fidelity Service")
                print("\n")
                print(f"Bonjour Trader, nous avons détecté {services.Player.jetons} jeton en votre possession.")
                print("\n")
                print("\n1 - Gagnez 5 items aléatoires pour seulement 1 Jeton !")
                print("2 - Achetez 1 Redcoin pour un prix misérable de 2 Jetons !")
                print("3 - Dépensez 3 Jetons et repartez chez vous avec un artefact !")
                print("4 - 4 Jetons, c'est le prix de la tranquilité avec notre service d'augmentation de la chair !")
                print("5 - Devenez un membre Platinium de notre service de Trading pour 5 Jetons !")
                print("\n6 - Eteindre le système.")
                choix = int(input("\nFaites votre choix en touchant les nombres : "))
                ClearConsole()
                if choix in [1, 2, 3, 4, 5, 6]:
                    break
            except ValueError:
                ClearConsole()
        if choix == 1 and services.Player.jetons >= 1:
            services.Player.jetons -= 1
            liste_item = []
            for _ in range(1, 6):
                nombre_aleatoire = random.randint(0, (len(LISTEITEM) - 1))
                item_obtenu = LISTEITEM[nombre_aleatoire]
                liste_item.append(item_obtenu)
                services.Player.items_possedes[item_obtenu] += 1
            print("                       ||")
            print("                      ||||")
            print("                     ||  ||")
            print("                    ||||||||")
            print("                   |||    |||")
            print("                  || ||  || ||")
            print("                 ||   ||||   ||")
            print("                ||     ||     ||")
            print("               ||||||||||||||||||")
            print("")
            print("")
            print("              Traders Incorporated")
            print("                Fidelity Service")
            print("\n")
            print("\nCher Trader, vous devriez trouver dans votre poche de nouveaux item a vendre aux aventuriers !")
            print(f"Nous vous avons donné les items [{liste_item[0]}], [{liste_item[1]}], [{liste_item[2]}], [{liste_item[3]}] et [{liste_item[4]}] !")
            input("\nTouchez Entrée pour Continuer ")
            ClearConsole()
        elif choix == 2 and services.Player.jetons >= 2:
            services.Player.jetons -= 2
            services.Player.nombre_de_red_coin += 1
            print("                       ||")
            print("                      ||||")
            print("                     ||  ||")
            print("                    ||||||||")
            print("                   |||    |||")
            print("                  || ||  || ||")
            print("                 ||   ||||   ||")
            print("                ||     ||     ||")
            print("               ||||||||||||||||||")
            print("")
            print("")
            print("              Traders Incorporated")
            print("                Fidelity Service")
            print("\n")
            print("\nCher Trader, vous devriez trouver dans votre poche un sublime Redcoin a vendre pour un prix exorbitant !")
            print("Rapellez vous la règle : 1 seul Redcoin par étage, mettez le deuxieme a un prix impossible pour dissuader les plus riche.")
            print("Nous avons un équilibre a garder, après tout !")
            input("\nTouchez Entrée pour Continuer ")
            ClearConsole()
        elif choix == 3 and services.Player.jetons >= 3:
            services.Player.jetons -= 3
            print("                       ||")
            print("                      ||||")
            print("                     ||  ||")
            print("                    ||||||||")
            print("                   |||    |||")
            print("                  || ||  || ||")
            print("                 ||   ||||   ||")
            print("                ||     ||     ||")
            print("               ||||||||||||||||||")
            print("")
            print("")
            print("              Traders Incorporated")
            print("                Fidelity Service")
            print("\n")
            print("\nCher Trader, vous devriez trouver dans votre poche une boite de chène noir, natif a notre monde.")
            print("Car ici, à Trader Incorporated, nous mettons un peu de noue même dans chaque transaction !")
            print("Bien entendu, il y a aussi un artefact a l'interieur.")
            print("Et vous, cher trader...")
            input("\nTouchez Entrée pour Continuer ")
            ClearConsole()
            print("                       ||")
            print("                      ||||")
            print("                     ||  ||")
            print("                    ||||||||")
            print("                   |||    |||")
            print("                  || ||  || ||")
            print("                 ||   ||||   ||")
            print("                ||     ||     ||")
            print("               ||||||||||||||||||")
            print("")
            print("")
            print("              Traders Incorporated")
            print("                Fidelity Service")
            print("\n")
            print("")
            etage.GiveRandomArtefact()
        elif choix == 4 and services.Player.jetons >= 4:
            services.Player.jetons -= 4
            print("                       ||")
            print("                      ||||")
            print("                     ||  ||")
            print("                    ||||||||")
            print("                   |||    |||")
            print("                  || ||  || ||")
            print("                 ||   ||||   ||")
            print("                ||     ||     ||")
            print("               ||||||||||||||||||")
            print("")
            print("")
            print("              Traders Incorporated")
            print("                Fidelity Service")
            print("\n")
            print("\nCher Trader, votre corps est votre plus grand outil pendant vos ventes.")
            print("Avec son language, vous pouvez planter des idées qui germent dans les têtes de nos consommateurs et les incitent à l'achat.")
            print("Avec sa forme, vous pouvez proteger vos marchandises des perfides qui peuplent votre dimension.")
            input("\nTouchez Entrée pour Continuer ")
            ClearConsole()
            print("                       ||")
            print("                      ||||")
            print("                     ||  ||")
            print("                    ||||||||")
            print("                   |||    |||")
            print("                  || ||  || ||")
            print("                 ||   ||||   ||")
            print("                ||     ||     ||")
            print("               ||||||||||||||||||")
            print("")
            print("")
            print("              Traders Incorporated")
            print("                Fidelity Service")
            print("\n")
            print("\nEt c'est dans cet optique là que nous avons modifié votre corps afin de rendre plus réceptif, le porte monnaie de nos investisseurs.")
            print("Vous gagnez ainsi 2 points de force, intelligence, defence, ainsi que 5 points de vie, mana, et endurance max, et bien sur 3% de chance de faire des coups/sorts critiques !")
            print("Sans oublier 1% de chance d'esquive.")
            input("\nTouchez Entrée pour Continuer ")
            services.Player.points_de_force += 2
            services.Player.points_dintelligence += 2
            services.Player.points_de_defence += 2
            services.Player.points_dendurance += 5
            services.Player.points_de_vie_max += 5
            services.Player.points_de_mana_max += 5
            services.Player.taux_sort_critique += 3
            services.Player.taux_coup_critique += 3
            services.Player.taux_desquive += 1
            ClearConsole()
        elif choix == 5 and services.Player.jetons >= 5:
            services.Player.jetons -= 5
            print("                       ||")
            print("                      ||||")
            print("                     ||  ||")
            print("                    ||||||||")
            print("                   |||    |||")
            print("                  || ||  || ||")
            print("                 ||   ||||   ||")
            print("                ||     ||     ||")
            print("               ||||||||||||||||||")
            print("")
            print("")
            print("              Traders Incorporated")
            print("                Fidelity Service")
            print("\n")
            print("\nCher Trader, notre entreprise est une grande famille.")
            print("Une grande famille intouchable, innacessible, et qui fait du commerce entre les mondes via des monolithes anciens seulement avec des personnes particulières, certe,")
            print("Mais c'est *votre* famille.")
            input("\nTouchez Entrée pour Continuer ")
            ClearConsole()
            print("                       ||")
            print("                      ||||")
            print("                     ||  ||")
            print("                    ||||||||")
            print("                   |||    |||")
            print("                  || ||  || ||")
            print("                 ||   ||||   ||")
            print("                ||     ||     ||")
            print("               ||||||||||||||||||")
            print("")
            print("")
            print("              Traders Incorporated")
            print("                Fidelity Service")
            print("\n")
            print("\nEt c'est pour cette raison, afin de vous récompenser de vos achats, que nous vous offrons ce Médaillon de Platine de haute qualité.")
            print("Avec lui, vous pourrez acquérir des biens chez les marchands de notre companie, vos frères et soeurs, pour des sommes bien moins élevées.")
            print("Nous vous remercions sincèrement de votre dévouement !")
            input("\nTouchez Entrée pour Continuer ")
            services.FloorMaker.GiveRandomArtefact("Médaillon de Platine","Don")
            ClearConsole()
        elif choix == 6:
            etage.TraderIncAnimationClose()
            print("Vous vous éloignez du systeme de fidélité de la guilde des marchands (tm).")
            services.Affichage.EntreePourContinuer()
            break
        else:
            print("                       ||")
            print("                      ||||")
            print("                     ||  ||")
            print("                    ||||||||")
            print("                   |||    |||")
            print("                  || ||  || ||")
            print("                 ||   ||||   ||")
            print("                ||     ||     ||")
            print("               ||||||||||||||||||")
            print("")
            print("")
            print("              Traders Incorporated")
            print("                Fidelity Service")
            print("\n")
            print("\nVous n'avez pas assez de [JETONS] !")
            input("\nTouchez Entrée pour Continuer ")
            ClearConsole()


@salle_de_type("BRAZIER_ROUGE")
def reveler_brazier_rouge(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.brazier()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    liste_items_sacrifiables_total = LISTEITEM

    print("Vous avancez dans la salle, et découvrez un gigantesque brasero orné de pierres précieuses .")
    services.Affichage.EntreePourContinuer()
    print("Sur ses côtés sont gravés des symboles anciens, montrant des populations en position de prière autour d'un objet similaire, sur lequel semble bruler un objet.")
    services.Affichage.EntreePourContinuer()
    print("Sans vraiment savoir comment, vous savez exactement ce que vous pouvez y bruler.")
    services.Affichage.EntreePourContinuer()
    while True:
        while True:
            try:
                if services.Player.flammes_rouge != 0:
                    print("Un brasier de couleur rouge danse dans le brasero.")
                else:
                    print("Il n'y a plus de feu dans le brasero.")
                print("\n1 - Faire une offrande")
                print("2 - Partir")
                choix = int(input("\nFaites votre choix avec les nombres : "))
                ClearConsole()
                if choix in [1, 2]:
                    break
            except ValueError:
                ClearConsole()
        if choix == 1:
            #faire la liste d'objet sacrifiable
            liste_items_sacrifiables_possedes = []
            for item in services.Player.items_possedes:
                if ((item in liste_items_sacrifiables_total) and
                    (services.Player.items_possedes[item] > 0)):
                    liste_items_sacrifiables_possedes.append(item)

            if services.Player.flammes_rouge == 0:
                print("Vous regardez les cendres remplissant désormais le brasero, et avez le sentiment que vous ne pouvez plus rien offrir.")
                services.Affichage.EntreePourContinuer()
            elif len(liste_items_sacrifiables_possedes) == 0:
                print("Vous ne pouvez rien offrir de valeur ici.")
                services.Affichage.EntreePourContinuer()
            else :
                while True:
                    try:
                        print("     -= Offrandes =-")
                        print("\n1 - Retour")
                        numero = 2
                        for item in liste_items_sacrifiables_possedes:
                            print(f"{numero} - {item} [{services.Player.items_possedes[item]} dans la sacoche]")
                            numero += 1
                        choix = int(input("\nFaites votre choix avec les nombres : "))
                        ClearConsole()
                        if choix in range(1, (len(liste_items_sacrifiables_possedes) + 2)):
                            break
                    except ValueError :
                        ClearConsole()
                if choix == 1:
                    pass
                else:
                    item_choisi = liste_items_sacrifiables_possedes[(choix - 2)]
                    nombre_aleatoire = random.randint(0, (len(LISTEITEM) - 1))
                    item_obtenu = LISTEITEM[nombre_aleatoire]
                    print(f"Vous jetez l'item [{item_choisi}] dans le brasero, et regardez les braises se disperser dans les airs.")
                    services.Affichage.EntreePourContinuer()
                    print("Au bout de quelques instant, quelque chose apparait a vos pieds.")
                    services.Affichage.EntreePourContinuer()
                    services.Player.flammes_rouge -= 1
                    services.Player.items_possedes[item_choisi] -= 1
                    services.Player.items_possedes[item_obtenu] += 1
                    services.Save.SaveTheGameSansAffichage()
                    print(f"Vous obtenez l'item [{item_obtenu}] !")
                    services.Affichage.EntreePourContinuer()
                    print("Le feu se fait plus faible.")
                    services.Affichage.EntreePourContinuer()
        elif choix == 2:
            print("Vous regardez, pensif, le feu gravé dans le réceptacle, avant de partir.")
            services.Affichage.EntreePourContinuer()
            break


@salle_de_type("BRAZIER_NOIR")
def reveler_brazier_noir(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.brazier()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    liste_items_sacrifiables_total = ["Fruit Jindagee", "Fruit Aatma", "Crystal Elémentaire"]

    print("Vous avancez dans la salle, et découvrez un gigantesque brasero orné de pierres précieuses .")
    services.Affichage.EntreePourContinuer()
    print("Sur ses côtés sont gravés des symboles anciens, montrant des populations en position de prière autour d'un objet similaire, sur lequel semble bruler un objet.")
    services.Affichage.EntreePourContinuer()
    print("Sans vraiment savoir comment, vous savez exactement ce que vous pouvez y bruler.")
    services.Affichage.EntreePourContinuer()
    while True:
        while True:
            try:
                if services.Player.flammes_noire != 0:
                    print("Un brasier de couleur noir danse dans le brasero.")
                else:
                    print("Il n'y a plus de feu dans le brasero.")
                print("\n1 - Faire une offrande")
                print("2 - Partir")
                choix = int(input("\nFaites votre choix avec les nombres : "))
                ClearConsole()
                if choix in [1, 2]:
                    break
            except ValueError:
                ClearConsole()
        if choix == 1:
            #faire la liste d'objet sacrifiable
            liste_items_sacrifiables_possedes = []
            for item in services.Player.items_possedes:
                if ((item in liste_items_sacrifiables_total) and
                    (services.Player.items_possedes[item] > 0)):
                    liste_items_sacrifiables_possedes.append(item)

            if services.Player.flammes_noire == 0:
                print("Vous regardez les cendres remplissant désormais le brasero, et avez le sentiment que vous ne pouvez plus rien offrir.")
                services.Affichage.EntreePourContinuer()
            elif len(liste_items_sacrifiables_possedes) == 0:
                print("Vous ne pouvez rien offrir de valeur ici.")
                services.Affichage.EntreePourContinuer()
            else :
                while True:
                    while True:
                        try:
                            print("     -= Offrandes =-")
                            print("\n1 - Retour")
                            numero = 2
                            for item in liste_items_sacrifiables_possedes:
                                print(f"{numero} - {item} [{services.Player.items_possedes[item]} dans la sacoche]")
                                numero += 1
                            choix = int(input("\nFaites votre choix avec les nombres : "))
                            ClearConsole()
                            if choix in range(1, (len(liste_items_sacrifiables_possedes) + 2)):
                                break
                        except ValueError :
                            ClearConsole()
                    if choix == 1:
                        break
                    elif choix == 2:
                        item_choisi = liste_items_sacrifiables_possedes[(choix - 2)]
                        if services.Player.items_possedes[item_choisi] < 20:
                            print("Vous n'avez pas assez de cet objet pour satisfaire la faim de ce terrible feu.")
                            services.Affichage.EntreePourContinuer()
                        else:
                            print(f"Vous jetez l'item [{item_choisi}] dans le brasero.\nPuis un autre.\nEt encore un autre.")
                            services.Affichage.EntreePourContinuer()
                            print(f"Au final, c'est une vingtaine de [{item_choisi}] que vous faites disparaitre dans les flammes et les braises.")
                            services.Affichage.EntreePourContinuer()
                            print("Au bout de quelques instants, le feu s'éteint.")
                            services.Affichage.EntreePourContinuer()
                            print("...?\nIl y a quelque chose dans les cendres...")
                            services.Affichage.EntreePourContinuer()
                            if item_choisi == "Fruit Jindagee":
                                item_obtenu = "Totem de la Force"
                                commentaire_sur_artefact = "Un totem en bois rouge, don divin d'un feu ancestral contre une offrande remplie de vitalité.\nVous commencez tout les combats avec l'effet [Jindagee] pendant 3 tours !"
                            elif item_choisi == "Fruit Aatma":
                                item_obtenu = "Totem de la Sagesse"
                                commentaire_sur_artefact = "Un totem en bois bleu, don divin d'un feu ancestral contre une offrande remplie de spiritualité.\nVous commencez tout les combats avec l'effet [Aatma] pendant 3 tours !"
                            elif item_choisi == "Crystal Elémentaire":
                                commentaire_sur_artefact = "Un totem en bois vert, don divin d'un feu ancestral contre une offrande remplie de défiance.\nVous commencez tout les combats avec une petite augmentation aléatoire d'appliquer un effet élémentaire !"
                                item_obtenu = "Totem du Courage"
                            services.FloorMaker.GiveRandomArtefact(item_obtenu,"Don")
                            services.Player.flammes_noire -= 1
                            services.Player.items_possedes[item_choisi] -= 20
                            services.Save.SaveTheGameSansAffichage()
                            print(f"Vous obtenez l'artefact [{item_obtenu}] !")
                            print(commentaire_sur_artefact)
                            services.Affichage.EntreePourContinuer()
                            break
        elif choix == 2:
            print("Vous regardez, pensif, le feu gravé dans le réceptacle, avant de partir.")
            services.Affichage.EntreePourContinuer()
            break


@salle_de_type("BRAZIER_BLEU")
def reveler_brazier_bleu(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.brazier()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    liste_items_sacrifiables_total = LISTEITEMBASE
    liste_items_quand_uppgrade = LISTEITEMAVANCE

    print("Vous avancez dans la salle, et découvrez un gigantesque brasero orné de pierres précieuses .")
    services.Affichage.EntreePourContinuer()
    print("Sur ses côtés sont gravés des symboles anciens, montrant des populations en position de prière autour d'un objet similaire, sur lequel semble bruler un objet.")
    services.Affichage.EntreePourContinuer()
    print("Sans vraiment savoir comment, vous savez exactement ce que vous pouvez y bruler.")
    services.Affichage.EntreePourContinuer()
    while True:
        while True:
            try:
                if services.Player.flammes_bleue != 0:
                    print("Un brasier de couleur bleu danse dans le brasero.")
                else:
                    print("Il n'y a plus de feu dans le brasero.")
                print("\n1 - Faire une offrande")
                print("2 - Partir")
                choix = int(input("\nFaites votre choix avec les nombres : "))
                ClearConsole()
                if choix in [1, 2]:
                    break
            except ValueError:
                ClearConsole()
        if choix == 1:
            #faire la liste d'objet sacrifiable
            liste_items_sacrifiables_possedes = []
            for item in services.Player.items_possedes:
                if ((item in liste_items_sacrifiables_total) and
                    (services.Player.items_possedes[item] > 0)):
                    liste_items_sacrifiables_possedes.append(item)

            if services.Player.flammes_bleue == 0:
                print("Vous regardez les cendres remplissant désormais le brasero, et avez le sentiment que vous ne pouvez plus rien offrir.")
                services.Affichage.EntreePourContinuer()
            elif len(liste_items_sacrifiables_possedes) == 0:
                print("Vous ne pouvez rien offrir de valeur ici.")
                services.Affichage.EntreePourContinuer()
            else :
                while True:
                    try:
                        print("     -= Offrandes =-")
                        print("\n1 - Retour")
                        numero = 2
                        for item in liste_items_sacrifiables_possedes:
                            print(f"{numero} - {item} [{services.Player.items_possedes[item]} dans la sacoche]")
                            numero += 1
                        choix = int(input("\nFaites votre choix avec les nombres : "))
                        ClearConsole()
                        if choix in range(1, (len(liste_items_sacrifiables_possedes) + 2)):
                            break
                    except ValueError :
                        ClearConsole()
                if choix == 1:
                    pass
                else:
                    item_choisi = liste_items_sacrifiables_possedes[(choix - 2)]
                    place_de_litem_choisi_dans_listeitem = LISTEITEMBASE.index(item_choisi)
                    item_obtenu = liste_items_quand_uppgrade[place_de_litem_choisi_dans_listeitem]
                    print(f"Vous jetez l'item [{item_choisi}] dans le brasero, et regardez les braises se disperser dans les airs.")
                    services.Affichage.EntreePourContinuer()
                    print("Au bout de quelques instant, quelque chose apparait a vos pieds.")
                    services.Affichage.EntreePourContinuer()
                    services.Player.flammes_bleue -= 1
                    services.Player.items_possedes[item_choisi] -= 1
                    services.Player.items_possedes[item_obtenu] += 1
                    services.Save.SaveTheGameSansAffichage()
                    print(f"Vous obtenez l'item [{item_obtenu}] !")
                    services.Affichage.EntreePourContinuer()
                    print("Le feu se fait plus faible.")
                    services.Affichage.EntreePourContinuer()
        elif choix == 2:
            print("Vous regardez, pensif, le feu gravé dans le réceptacle, avant de partir.")
            services.Affichage.EntreePourContinuer()
            break


@salle_de_type("PECHE")
def reveler_peche(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.peche()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print("Vous trébuchez sur quelque chose par terre, et finissez la tête dans de l'eau.")
    services.Affichage.EntreePourContinuer()
    print("Alors que vous vous relevez, vous voyez un trou dans le sol rempli d'une eau bleutée, comme un hublot dans un sous marin.\nEn vous retournant, vous comprenez que vous avez trébuché sur une canne a peche.")
    services.Affichage.EntreePourContinuer()
    print("On dirait que quelqu'un ici a pratiqué la peche blanche.\nEnfin, pas sur la glace mais dans le sol.")
    services.Affichage.EntreePourContinuer()
    while True:
        while True:
            try:
                if services.Player.poissons != 0:
                    print(f"Vous pouvez voir {services.Player.poissons} formes se baladant au fond de l'eau.")
                else:
                    print("Il n'y a plus rien a pêcher ici.")
                print("\n1 - Pecher")
                print("2 - Partir")
                choix = int(input("\nFaites votre choix avec les nombres : "))
                ClearConsole()
                if choix in [1, 2]:
                    break
            except ValueError:
                ClearConsole()
        if choix == 1:
            services.Player.poissons -= 1
            services.Save.SaveTheGameSansAffichage()
            #détermine le type de prise
            numero_aleatoire = random.randint(1,5)
            if numero_aleatoire == 1:
                type_de_prise = "Monstre"
            elif numero_aleatoire == 2:
                type_de_prise = "Item"
            elif numero_aleatoire == 3:
                type_de_prise = "Poisson"
            elif numero_aleatoire == 4:
                type_de_prise = "Gros Poisson"
            elif numero_aleatoire == 5:
                type_de_prise = "Redcoin"
            elif numero_aleatoire == 5:
                type_de_prise = "Artefact"
            if services.Player.poissons == -1:
                print("Si vous voulez....")
                services.Affichage.EntreePourContinuer()
                type_de_prise = "Rien"
            prise = etage.DoPeche(type_de_prise)
            if prise == "Pas assez attendu":
                services.Player.poissons += 1
            else:
                print("Vous sortez l'hameçon de l'eau...")
                services.Affichage.EntreePourContinuer()
                if prise == "Monstre":
                    print("...et découvrez un monstre accroché au bout.")
                    services.Affichage.EntreePourContinuer()
                    print("...")
                    services.Affichage.EntreePourContinuer()
                    print("...")
                    services.Affichage.EntreePourContinuer()
                    print("Le monstre vous regarde d'un air surpris.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous lui retournez le même regard.")
                    services.Affichage.EntreePourContinuer()
                    print("Le monstre machouille l'hameçon de manière lancinante.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous posez la canne et amenez la main a votre arme.")
                    services.Affichage.EntreePourContinuer()
                    livrer_combat()
                    CheckForKIA()
                    print("Ouf !")
                    PlayMusicDeLetage()
                    services.Affichage.EntreePourContinuer()
                elif prise == "Item":
                    print("...et décrochez une botte dans laquelle il s'était enfoncé.")
                    services.Affichage.EntreePourContinuer()
                    numero_aleatoire = random.randint(0, (len(LISTEITEM) - 1))
                    item_aleatoire_obtenu = LISTEITEM[numero_aleatoire]
                    services.Player.items_possedes[item_aleatoire_obtenu] += 1
                    print(f"A l'interieur de la botte, il y a l'item [{item_aleatoire_obtenu}] !")
                    services.Affichage.EntreePourContinuer()
                    print("Un déchet en moins dans les eaux !")
                    services.Affichage.EntreePourContinuer()
                elif prise == "Poisson":
                    numero_aleatoire = random.randint(1,5)
                    if numero_aleatoire == 1:
                        print("...et décrochez un joli poisson bleu, trop petit pour être mangé.")
                        services.Affichage.EntreePourContinuer()
                        print("Alors que vous remettez le poisson a l'eau, vous vous sentez en paix avec la nature.")
                        services.Affichage.EntreePourContinuer()
                        print("Vous gagnez 2 point d'intelligence !")
                        services.Player.points_dintelligence += 2
                        services.Affichage.EntreePourContinuer()
                    elif numero_aleatoire == 2:
                        print("...et décrochez un joli poisson rouge, trop petit pour être mangé.")
                        services.Affichage.EntreePourContinuer()
                        print("Alors que vous remettez le poisson a l'eau, vous vous sentez en paix avec vos convictions.")
                        services.Affichage.EntreePourContinuer()
                        print("Vous gagnez 2 point de force !")
                        services.Player.points_de_force += 2
                        services.Affichage.EntreePourContinuer()
                    elif numero_aleatoire == 3:
                        print("...et décrochez un joli poisson vert, trop petit pour être mangé.")
                        services.Affichage.EntreePourContinuer()
                        print("Alors que vous remettez le poisson a l'eau, vous vous sentez en paix avec vous même.")
                        services.Affichage.EntreePourContinuer()
                        print("Vous gagnez 5 points d'endurance' !")
                        services.Player.points_dendurance += 5
                        services.Affichage.EntreePourContinuer()
                    elif numero_aleatoire == 4:
                        print("...et décrochez un joli poisson jaune, trop petit pour être mangé.")
                        services.Affichage.EntreePourContinuer()
                        print("Alors que vous remettez le poisson a l'eau, vous vous sentez en paix avec votre coeur.")
                        services.Affichage.EntreePourContinuer()
                        print("Vous gagnez 1% de chance d'esquive !")
                        services.Player.taux_desquive += 1
                        services.Affichage.EntreePourContinuer()
                    elif numero_aleatoire == 5:
                        print("...et décrochez un joli poisson blanc, trop petit pour être mangé.")
                        services.Affichage.EntreePourContinuer()
                        print("Alors que vous remettez le poisson a l'eau, vous vous sentez en paix avec votre âme.")
                        services.Affichage.EntreePourContinuer()
                        print("Le nombre d'âme absorbées par votre arme augmente de 5 !")
                        services.Player.nombre_de_monstres_tues += 5
                        services.Affichage.EntreePourContinuer()
                    print("Belle prise !")
                    services.Affichage.EntreePourContinuer()
                elif prise == "Gros Poisson":
                    numero_aleatoire = random.randint(1,5)
                    if numero_aleatoire == 1:
                        print("...et décrochez un gros et vigoureux poisson bleu !")
                        services.Affichage.EntreePourContinuer()
                        print("Vous écaillez le poisson...\nLe videz de ses organes...\nPuis de son sang..\nEnlevez ses arêtes...\nLe découpez en filet...\nEt le faite cuire au dessus d'un feu vif.")
                        services.Affichage.EntreePourContinuer()
                        print("Alors que vous dégustez votre poisson, vous sentez des changements dans votre corps.")
                        services.Affichage.EntreePourContinuer()
                        print("Vous gagnez 4 points d'intelligence !")
                        services.Player.points_dintelligence += 4
                        services.Affichage.EntreePourContinuer()
                    elif numero_aleatoire == 2:
                        print("...et décrochez un gros et vigoureux poisson rouge !")
                        services.Affichage.EntreePourContinuer()
                        print("Vous écaillez le poisson...\nLe videz de ses organes...\nPuis de son sang..\nEnlevez ses arêtes...\nLe découpez en filet...\nEt le faite cuire au dessus d'un feu vif.")
                        services.Affichage.EntreePourContinuer()
                        print("Alors que vous dégustez votre poisson, vous sentez des changements dans votre corps.")
                        services.Affichage.EntreePourContinuer()
                        print("Vous gagnez 4 point de force !")
                        services.Player.points_de_force += 4
                        services.Affichage.EntreePourContinuer()
                    elif numero_aleatoire == 3:
                        print("...et décrochez un gros et vigoureux poisson vert !")
                        services.Affichage.EntreePourContinuer()
                        print("Vous écaillez le poisson...\nLe videz de ses organes...\nPuis de son sang..\nEnlevez ses arêtes...\nLe découpez en filet...\nEt le faite cuire au dessus d'un feu vif.")
                        services.Affichage.EntreePourContinuer()
                        print("Alors que vous dégustez votre poisson, vous sentez des changements dans votre corps.")
                        services.Affichage.EntreePourContinuer()
                        print("Vous gagnez 10 points d'endurance' !")
                        services.Player.points_dendurance += 10
                        services.Affichage.EntreePourContinuer()
                    elif numero_aleatoire == 4:
                        print("...et décrochez un gros et vigoureux poisson jaune !")
                        services.Affichage.EntreePourContinuer()
                        print("Vous écaillez le poisson...\nLe videz de ses organes...\nPuis de son sang..\nEnlevez ses arêtes...\nLe découpez en filet...\nEt le faite cuire au dessus d'un feu vif.")
                        services.Affichage.EntreePourContinuer()
                        print("Alors que vous dégustez votre poisson, vous sentez des changements dans votre corps.")
                        services.Affichage.EntreePourContinuer()
                        print("Vous gagnez 3% de chance d'esquive !")
                        services.Player.taux_desquive += 3
                        services.Affichage.EntreePourContinuer()
                    elif numero_aleatoire == 5:
                        print("...et décrochez un gros et vigoureux poisson blanc !")
                        services.Affichage.EntreePourContinuer()
                        print("Vous écaillez le poisson...\nLe videz de ses organes...\nPuis de son sang..\nEnlevez ses arêtes...\nLe découpez en filet...\nEt le faite cuire au dessus d'un feu vif.")
                        services.Affichage.EntreePourContinuer()
                        print("Alors que vous dégustez votre poisson, vous sentez des changements dans votre corps.")
                        services.Affichage.EntreePourContinuer()
                        print("Le nombre d'âme absorbées par votre arme augmente de 10 !")
                        services.Player.nombre_de_monstres_tues += 10
                        services.Affichage.EntreePourContinuer()
                    print("Miam !")
                    services.Affichage.EntreePourContinuer()
                elif prise == "Redcoin":
                    print("...et y trouvez une amulette accrochée par chaine.")
                    services.Affichage.EntreePourContinuer()
                    print(f"Un bien interessant anneau est rentré dans la chaine...")
                    services.Affichage.EntreePourContinuer()
                    print("...bien précieux...")
                    services.Affichage.EntreePourContinuer()
                    print("...*mon* précieux...")
                    services.Affichage.EntreePourContinuer()
                    print("...mais vous êtes plus attiré par le redcoin incrusté a l'arriere de l'amulette.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous obtenez un Redcoin !")
                    services.Player.nombre_de_red_coin += 1
                    services.Affichage.EntreePourContinuer()
                    print("Vous arrachez le redcoin de l'amulette, et la laissez couler au fond de l'eau, oubliée pour l'éternitée...")
                    print("...jusqu'à ce que l'anneau rentre en possession de quelqu'un d'autre.")
                    services.Affichage.EntreePourContinuer()
                elif prise == "Artefact":
                    print("...et regardez avec intensité la petite boite noire qui y est pendue.")
                    services.Affichage.EntreePourContinuer()
                    print(f"Vous arrachez l'hameçon du bois dans lequel il était rentré...")
                    services.Affichage.EntreePourContinuer()
                    print("...et ouvrez la boite avec beaucoup d'anticipation.")
                    services.Affichage.EntreePourContinuer()
                    etage.GiveRandomArtefact()
                    print("Incroyable Prise !\nMais comment une boite peut-elle donner autant de fil a retordre pour être remontée...?")
                    services.Affichage.EntreePourContinuer()
            PlayMusicDeLetage()
        elif choix == 2:
            print("Vous n'avez jamais aimé la pêche de toute manière.")
            services.Affichage.EntreePourContinuer()
            break


@salle_de_type("BRAZIER_VERT")
def reveler_brazier_vert(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.brazier()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    liste_items_sacrifiables_total = LISTEITEM

    print("Vous avancez dans la salle, et découvrez un gigantesque brasero orné de pierres précieuses .")
    services.Affichage.EntreePourContinuer()
    print("Sur ses côtés sont gravés des symboles anciens, montrant des populations en position de prière autour d'un objet similaire, sur lequel semble bruler un objet.")
    services.Affichage.EntreePourContinuer()
    print("Sans vraiment savoir comment, vous savez exactement ce que vous pouvez y bruler.")
    services.Affichage.EntreePourContinuer()
    while True:
        while True:
            try:
                if services.Player.flammes_verte != 0:
                    print("Un brasier de couleur vert danse dans le brasero.")
                else:
                    print("Il n'y a plus de feu dans le brasero.")
                print("\n1 - Faire une offrande")
                print("2 - Partir")
                choix = int(input("\nFaites votre choix avec les nombres : "))
                ClearConsole()
                if choix in [1, 2]:
                    break
            except ValueError:
                ClearConsole()
        if choix == 1:
            #faire la liste d'objet sacrifiable
            liste_items_sacrifiables_possedes = []
            for item in services.Player.items_possedes:
                if ((item in liste_items_sacrifiables_total) and
                    (services.Player.items_possedes[item] > 0)):
                    liste_items_sacrifiables_possedes.append(item)

            if services.Player.flammes_verte == 0:
                print("Vous regardez les cendres remplissant désormais le brasero, et avez le sentiment que vous ne pouvez plus rien offrir.")
                services.Affichage.EntreePourContinuer()
            elif len(liste_items_sacrifiables_possedes) == 0:
                print("Vous ne pouvez rien offrir de valeur ici.")
                services.Affichage.EntreePourContinuer()
            else :
                while True:
                    try:
                        print("     -= Offrandes =-")
                        print("\n1 - Retour")
                        numero = 2
                        for item in liste_items_sacrifiables_possedes:
                            print(f"{numero} - {item} [{services.Player.items_possedes[item]} dans la sacoche]")
                            numero += 1
                        choix = int(input("\nFaites votre choix avec les nombres : "))
                        ClearConsole()
                        if choix in range(1, (len(liste_items_sacrifiables_possedes) + 2)):
                            break
                    except ValueError :
                        ClearConsole()
                if choix == 1:
                    pass
                else:
                    item_choisi = liste_items_sacrifiables_possedes[(choix - 2)]
                    print(f"Vous jetez l'item [{item_choisi}] dans le brasero, et regardez les braises se disperser dans les airs.")
                    services.Affichage.EntreePourContinuer()
                    print("Au bout de quelques instant, un changement se produit dans votre corps.")
                    services.Affichage.EntreePourContinuer()
                    services.Player.flammes_verte -= 1
                    services.Player.items_possedes[item_choisi] -= 1
                    liste_recompense = LISTEITEMUPPGRADE[item_choisi]
                    for cle in liste_recompense:
                        if cle == "Attaque":
                            services.Player.points_de_force += liste_recompense[cle]
                            commentaire = f"Vous gagnez {liste_recompense[cle]} points de force !"
                        elif cle == "Defence":
                            services.Player.points_de_defence += liste_recompense[cle]
                            commentaire = f"Vous gagnez {liste_recompense[cle]} points de défence !"
                        elif cle == "Intelligence":
                            services.Player.points_dintelligence += liste_recompense[cle]
                            commentaire = (
                                f"Vous gagnez {liste_recompense[cle]} points d'intelligence !"
                            )
                        elif cle == "Vie":
                            services.Player.points_de_vie_max += liste_recompense[cle]
                            services.Player.points_de_vie += liste_recompense[cle]
                            commentaire = (
                                f"Vous gagnez {liste_recompense[cle]} points de vie maximum !"
                            )
                        elif cle == "Mana":
                            services.Player.points_de_mana_max += liste_recompense[cle]
                            services.Player.points_de_mana += liste_recompense[cle]
                            commentaire = (
                                f"Vous gagnez {liste_recompense[cle]} points de mana maximum !"
                            )
                        elif cle == "Endurance":
                            services.Player.points_dendurance += liste_recompense[cle]
                            commentaire = (
                                f"Vous gagnez {liste_recompense[cle]} points d'endurance maximum !"
                            )
                        elif cle == "Taux coup critique":
                            services.Player.taux_coup_critique += liste_recompense[cle]
                            commentaire = f"Vous gagnez {liste_recompense[cle]}% de chance de faire un coup critique !"
                        elif cle == "Degat coup critique":
                            services.Player.degat_coup_critique += liste_recompense[cle]
                            commentaire = f"Vous gagnez {liste_recompense[cle]} points de degats de coup critique !"
                        elif cle == "Taux sort critique":
                            services.Player.taux_sort_critique += liste_recompense[cle]
                            commentaire = f"Vous gagnez {liste_recompense[cle]}% de chance de faire un sort critique !"
                        elif cle == "Taux esquive":
                            services.Player.taux_desquive += liste_recompense[cle]
                            commentaire = (
                                f"Vous gagnez {liste_recompense[cle]}% de chance d'esquiver !"
                            )
                        elif cle == "Degat sort critique":
                            services.Player.degat_sort_critique += liste_recompense[cle]
                            commentaire = f"Vous gagnez {liste_recompense[cle]} points de degats de sort critique !"
                        elif cle == "Red coin":
                            services.Player.nombre_de_red_coin += liste_recompense[cle]
                            commentaire = f"{liste_recompense[cle]} Red Coin apparait dans votre poche !"
                        print(commentaire)
                    services.Save.SaveTheGameSansAffichage()
                    services.Affichage.EntreePourContinuer()
                    print("Le feu se fait plus faible.")
                    services.Affichage.EntreePourContinuer()
        elif choix == 2:
            print("Vous regardez, pensif, le feu gravé dans le réceptacle, avant de partir.")
            services.Affichage.EntreePourContinuer()
            break
