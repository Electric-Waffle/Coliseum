"""Observation des lieux spéciaux et lecture/écriture brute de la sauvegarde permanente."""

import ast
import csv
import os
import random
import threading
import time

from coliseum import services
from coliseum.audio import PlayMusic, PlayMusicDeLetage, PlaySound, PlayWavSound, StopAllMusic
from coliseum.chemins import DOSSIER_RESSOURCES
from coliseum.console import ClearConsole
from coliseum.donnees.actions import LISTESORTS, LISTETECHNIQUES
from coliseum.donnees.bibliotheque import BIBLIOTHEQUEFINALE
from coliseum.histoire.village import CheckForKIA


class Observe:

    def __init__(self):
        pass

    def SeeSomething(self):
        if services.Player.numero_de_letage == 1:
            self.DoTheLibrary()  # bibliotheque de gros sorts (recuperer les sorts consignés)
        elif services.Player.numero_de_letage == 2:
            self.DoTheFountain()  # Fontaine redonne pv 3 fois
        elif services.Player.numero_de_letage == 3:
            self.DoTheGacha()  # Gacha game a mutations
        elif services.Player.numero_de_letage == 4:
            self.DoTheBloodStone()  # machine a gold a sang
        elif services.Player.numero_de_letage == 5:
            self.DoTheQuests()  # fantome des quetes ultimes
        elif services.Player.numero_de_letage == 6:
            self.DoTheOldMercant()  # alchimiste divin vampire demande manamax
        elif services.Player.numero_de_letage == 7:
            self.DoTheCursedBook()  # echange sorts/techniques pour carac
        elif services.Player.numero_de_letage == 8:
            self.DoTheFinalLibrary()  # bibliotheque de gros sorts (choisir sort a consigner)
        elif services.Player.numero_de_letage == 9:
            self.DoTheArtefactTrading()  # Achete des artefacts a Alfred

    def DoTheArtefactTrading(self):
        StopAllMusic()
        print("Alors que vous vous approchez du centre de la pièce, vous vous mettez a tomber, les deux pieds fermements ancrés dans le sol.")
        services.Affichage.EntreePourContinuer()
        print("La salle se met alors a tourner, et changer d'apparence, jusqu'à ce que vous arriviez sur une chaise.")
        services.Affichage.EntreePourContinuer()
        print("Une figure inconnue est assise, elle aussi, mais de l'autre coté d'une table d'ébène.")
        services.Affichage.EntreePourContinuer()
        print("Autour de vous se trouve un espace luxueux entouré d'une dizaine de portes.")
        services.Affichage.EntreePourContinuer()
        print("La figure tend alors une main que vous reconnaissez sans savoir pourquoi.")
        services.Affichage.EntreePourContinuer()
        PlayMusic("alfredproto")
        print("Alfred.")
        services.Affichage.EntreePourContinuer()
        print("*Eh bien ? On ne sert plus la main a son hôte maintenant ?* \n*Quoique, les règles d'usage ont du changer ces derniers siècles.*")
        services.Affichage.EntreePourContinuer()
        print("*Tu doit connaitre la chanson maintenant, ou pas.* \n*Je n'ai aucun moyen de savoir si c'est la toute première fois que l'on se voit, ou si le marionnettiste est un vétérant.*")
        services.Affichage.EntreePourContinuer()
        print("*Bref.*")
        services.Affichage.EntreePourContinuer()
        print("*2500 golds, et tu gagne un artefact aléatoire.*")
        services.Affichage.EntreePourContinuer()
        while True:
            while True:
                try:
                    print("     -=[ Alfred ]=-\n")
                    print("1 - Partir")
                    print("2 - Acheter un artefact aléatoire (2500 golds)")
                    print("3 - Parler")
                    choix = int(input("\nQu'est ce que tu veux ?  "))
                    ClearConsole()
                    if choix in [1, 2, 3]:
                        break
                except:
                    ClearConsole()
            if choix == 1:
                StopAllMusic()
                print("*Lève toi simplement si tu veux sortir, et retourne au centre de la pièce si tu veux rentrer.*")
                services.Affichage.EntreePourContinuer()
                print("Vous le regardez avec un air surpris.")
                services.Affichage.EntreePourContinuer()
                print("*Quoi ?* \n*L'étage entier est un embroglio de formes, couleurs, et objets qui agissent de manière impossible mais je n'ai pas le droit d'avoir une simple porte de maison cachée dans la 5ème dimension ?*")
                services.Affichage.EntreePourContinuer()
                print("Vous rougissez d'un air géné et vous relevez. \nBientot, la salle entière bouge sur elle même et vous tombez lourdement sur le sol de l'étage, vos pieds toujours fermements ancrés sur ledit sol.")
                services.Affichage.EntreePourContinuer()
                PlayMusicDeLetage()
                break
            elif choix == 2:
                if services.Player.nombre_de_gold >= 2500:
                    print("Vous tendez a Alfred votre bourse d'une main tremblottante, et le voyez engloutir vos golds durements gagnés dans une poche qui semble n'avoir pas de fond.")
                    services.Affichage.EntreePourContinuer()
                    services.Player.nombre_de_gold -= 2500
                    print("*Quel bohneur de faire affaire !*")
                    services.Affichage.EntreePourContinuer()
                    print("*Voici donc votre artefact aléatoire, très estimé client !*")
                    services.Affichage.EntreePourContinuer()
                    print("Alfred vous tend un petit coffre de bois noir, que vous ouvrez immédiatement.")
                    services.Affichage.EntreePourContinuer()
                    services.FloorMaker.GiveRandomArtefact()
                else:
                    StopAllMusic()
                    print("Alfred vous regarde avec l'air fatigué et non amusé d'un caissier qui entend pour une ènième fois : *Ya pas de code barre ? Ca doit etre gratuit alors !*")
                    services.Affichage.EntreePourContinuer()
                    print("Vous rougissez de votre manque de fonds, et vous levez dans la précipitation.")
                    services.Affichage.EntreePourContinuer()
                    print("La salle tourne sur elle meme, et vous jette violemment contre un des murs du onzième étage.")
                    services.Affichage.EntreePourContinuer()
                    print("Wow, trop la honte !")
                    services.Affichage.EntreePourContinuer()
                    PlayMusicDeLetage()
                    break
            elif choix == 3:
                print("*Me parler ?*")
                services.Affichage.EntreePourContinuer()
                print("Alfred rigole doucement.")
                services.Affichage.EntreePourContinuer()
                print("*Laisse moi deviner, tu n'avais pas cette option avec les autres marchands, alors t'a sauté sur l'opportunité pour moi ?*")
                services.Affichage.EntreePourContinuer()
                print("*En tout cas, ca confirme que c'est bien la première fois que tu viens chez moi.*")
                services.Affichage.EntreePourContinuer()
                print("*Ou alors, tu as fait la paix avec le fait que je vais te dire la même chose a chaque fois que tu utilise cette option...*")
                services.Affichage.EntreePourContinuer()
                print("*Quoi qu'il en soit, bienvenue chez moi !*")
                services.Affichage.EntreePourContinuer()
                print("*C'est un petit coin tranquille relié a tout les étages du Coliseum, caché dans une dimension crée de toute pièce par la fusion de tout les étages.*")
                services.Affichage.EntreePourContinuer()
                print("*J'y ai récupéré un sacré trésor au fur et a mesure des annéees , et je le dépense pour recréer ici une vie plutot bourgeoise, dont je profitait il y a très longtemps.*")
                services.Affichage.EntreePourContinuer()
                print("*Quoi dire de plus...je ne suis pas vraiment un Homme. La peau blanche que tu vois est maintenue ainsi grace a des composants rares que j'achete au marchand.*")
                services.Affichage.EntreePourContinuer()
                print("*Mon histoire ?* \n*Je faisait parti d'un groupe de quatres guerriers divinement choisis pour défendre une...porte.*\n* Nous étions mené par un Homme avec beaucoup de valeurs...trahi par son frère.*")
                services.Affichage.EntreePourContinuer()
                print("*Je suis le seul survivant de cette trahison.*")
                services.Affichage.EntreePourContinuer()
                print("*Depuis, la porte a été scellé, et le frère avec.*")
                services.Affichage.EntreePourContinuer()
                print("*Hum ? COmment je suis arrivé ici ?*")
                services.Affichage.EntreePourContinuer()
                print("*Je laisse cela à ton interprétation.*")
                services.Affichage.EntreePourContinuer()
                print("*...*")
                services.Affichage.EntreePourContinuer()
                print("*...mes intentions ?*")
                services.Affichage.EntreePourContinuer()
                print("Alfred regarde dans un coin de la pièce, et sourit.")
                services.Affichage.EntreePourContinuer()
                print("*Non, non... Je ne discute pas de ce genre de chose avec une simple poupée.*")
                services.Affichage.EntreePourContinuer()
                print("Alfred sourit, bien plus que physiquement possible.")
                services.Affichage.EntreePourContinuer()
                print("*Et si tu venait ici plutôt ?*")
                services.Affichage.EntreePourContinuer()
                StopAllMusic()
                print("*M A R I O N N E T T I S T E ?*")
                time.sleep(3)
                ClearConsole()
                print("[ERREUR : ACCES NON AUTORISE]")
                time.sleep(2)
                ClearConsole()
                print("[UTILISATION DU PARE FEU EN COURS...]")
                time.sleep(5)
                ClearConsole()
                print("[ACCES INTERROMPU. ]")
                time.sleep(2)
                ClearConsole()
                PlayMusic("alfredproto")
                print("*...tsk.*")
                services.Affichage.EntreePourContinuer()
                




    def DoTheCursedBook(self):
        print(
            "Dans une cage vide, vous trouvez un livre à moitié brulé dont la couverture représente une cigogne noire regardant vers le haut."
        )
        services.Affichage.EntreePourContinuer()
        print("Sur la première page, il y a [ERROR : DESCRIPTION NOT FOUND].")
        print("[IPV4 ADRESS OF LOST DESCRIPTION : 456852]")
        services.Affichage.EntreePourContinuer()
        while True:
            while True:
                try:
                    print("Vous posez la main sur la page, et pensez à:")
                    print("1 - Rien du tout.")
                    numero_a_afficher = 2
                    for sorts in services.Player.sorts_possedes:
                        print(f"{numero_a_afficher} - {sorts}")
                        numero_a_afficher += 1
                    for techniques in services.Player.techniques_possedes:
                        print(f"{numero_a_afficher} - {techniques}")
                        numero_a_afficher += 1
                    choix = int(input("\n"))
                    ClearConsole()
                    nombre_de_choix_possibles = (
                        len(services.Player.sorts_possedes) + len(services.Player.techniques_possedes) + 1
                    )
                    if choix in range(1, (nombre_de_choix_possibles + 1)):
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print(
                    "Vous jetez à votre main un regard vide, et laissez tomber le livre sur le sol avant de repartir."
                )
                services.Affichage.EntreePourContinuer()
                break
            else:
                liste_de_sorts_et_techniques_a_oublier = []
                for sorts in services.Player.sorts_possedes:
                    liste_de_sorts_et_techniques_a_oublier.append(sorts)
                for techniques in services.Player.techniques_possedes:
                    liste_de_sorts_et_techniques_a_oublier.append(techniques)
                action_a_oublier = liste_de_sorts_et_techniques_a_oublier[(choix - 2)]
                services.Player.liste_daction_oubliees.append(action_a_oublier)
                if action_a_oublier in services.Player.sorts_possedes:
                    services.Player.sorts_possedes.remove(action_a_oublier)
                    type_daction = "Sort"
                else:
                    services.Player.techniques_possedes.remove(action_a_oublier)
                    type_daction = "Technique"
                print(
                    "Vous sentez quelque chose sortir de votre esprit et partir dans le livre, mais vous ne savez pas quoi."
                )
                print(f"La ligne [{action_a_oublier}] apparait sur la page d'après !")
                services.Affichage.EntreePourContinuer()
                action_a_oublier = self.EnleveurDaffix(action_a_oublier)
                self.DonneRecompensePourOubli(action_a_oublier, type_daction)
                self.DonneRecompensePourCertainsOubli()

    def EnleveurDaffix(self, action):
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
        action_transformee_en_liste = list(action.split())
        liste_mot = []
        for mot in action_transformee_en_liste:
            if mot in liste_affix:
                pass
            else:
                liste_mot.append(mot)

        action_sans_affixe = ""
        for mot in liste_mot:
            action_sans_affixe += mot
            if liste_mot[len(liste_mot) - 1] != mot:
                action_sans_affixe += " "

        return action_sans_affixe

    def DonneRecompensePourCertainsOubli(self):
        if (
            "Corne Granite" in services.Player.liste_daction_oubliees
            and "Création de Granite" in services.Player.liste_daction_oubliees
        ):
            print(
                "Les lignes Corne Granite et Création de Granite brillent avant de disparaitre."
            )
            print("Vous gagnez 4 points de défence !")
            services.Player.liste_daction_oubliees.remove("Corne Granite")
            services.Player.liste_daction_oubliees.remove("Création de Granite")
            services.Player.points_de_defence += 4
        elif (
            "Explosion de la Comète" in services.Player.liste_daction_oubliees
            and "Thermosphère Solaire" in services.Player.liste_daction_oubliees
        ):
            print(
                "Les lignes Explosion de la Comète et Thermosphère Solaire brillent avant de disparaitre."
            )
            print(
                "Vous gagnez 15 points de mana max et 5% de chance de faire un sort critique !"
            )
            services.Player.points_de_mana_max += 15
            services.Player.taux_sort_critique += 5
            services.Player.liste_daction_oubliees.remove("Explosion de la Comète")
            services.Player.liste_daction_oubliees.remove("Thermosphère Solaire")
        elif (
            "Dague Vampirique" in services.Player.liste_daction_oubliees
            and "Sonata Miséricordieuse" in services.Player.liste_daction_oubliees
        ):
            print(
                "Les lignes Dague Vampirique et Sonata Miséricordieuse brillent avant de disparaitre."
            )
            print("Vous gagnez 5% de chance d'esquiver !")
            services.Player.taux_desquive += 5
            services.Player.liste_daction_oubliees.remove("Dague Vampirique")
            services.Player.liste_daction_oubliees.remove("Sonata Miséricordieuse")
        elif (
            "Lance de l'Eclair" in services.Player.liste_daction_oubliees
            and "Katana Polaire" in services.Player.liste_daction_oubliees
        ):
            print(
                "Les lignes Lance de l'Eclair et Katana Polaire brillent avant de disparaitre."
            )
            print(
                "Vous gagnez 15 points de vie max 5% de chance de faire un coup critique !"
            )
            services.Player.points_de_vie_max += 15
            services.Player.taux_coup_critique += 5
            services.Player.liste_daction_oubliees.remove("Lance de l'Eclair")
            services.Player.liste_daction_oubliees.remove("Katana Polaire")
        elif (
            "Dance Destructrice" in services.Player.liste_daction_oubliees
            and "Poing Fatal" in services.Player.liste_daction_oubliees
        ):
            print(
                "Les lignes Dance Destructrice et Poing Fatal brillent avant de disparaitre."
            )
            print("Vous gagnez 4 points de force !")
            services.Player.points_de_force += 4
            services.Player.liste_daction_oubliees.remove("Dance Destructrice")
            services.Player.liste_daction_oubliees.remove("Poing Fatal")
        elif (
            "Faisceau Rapide" in services.Player.liste_daction_oubliees
            and "Bô de la Fournaise" in services.Player.liste_daction_oubliees
        ):
            print(
                "Les lignes Faisceau Rapide et Bô de la Fournaise brillent avant de disparaitre."
            )
            print("Vous gagnez 4 points d'intelligence !")
            services.Player.points_dintelligence += 4
            services.Player.liste_daction_oubliees.remove("Faisceau Rapide")
            services.Player.liste_daction_oubliees.remove("Bô de la Fournaise")
        elif (
            "Pic Zéro" in services.Player.liste_daction_oubliees
            and "Sonata Bienveillante" in services.Player.liste_daction_oubliees
            and "Création Obsidienne" in services.Player.liste_daction_oubliees
            and "Lance Electrique" in services.Player.liste_daction_oubliees
            and "Bô Chaud" in services.Player.liste_daction_oubliees
            and "Katana Froid" in services.Player.liste_daction_oubliees
        ):
            StopAllMusic()
            print(
                "Les lignes Pic Zéro, Sonata Bienveillante, "
                "Création Obsidienne, Lance Electrique, "
                "Katana Froid et Bô Chaud brillent avant de disparaitre."
            )
            print(
                "Des mots apparaissent, lettres après lettres, sur la quatrième de couverture."
            )
            print("Comme écrits par une main invisible.")
            services.Player.liste_daction_oubliees.remove("Pic Zéro")
            services.Player.liste_daction_oubliees.remove("Sonata Bienveillante")
            services.Player.liste_daction_oubliees.remove("Création Obsidienne")
            services.Player.liste_daction_oubliees.remove("Lance Electrique")
            services.Player.liste_daction_oubliees.remove("Katana Froid")
            services.Player.liste_daction_oubliees.remove("Bô Chaud")
            services.Affichage.EntreePourContinuer()
            PlayMusic("quiet")
            print("      -=Métamorphose=-")
            print("")
            time.sleep(5)
            print("Mon cher amour.")
            time.sleep(5)
            print("De la plus grande plume d'oie")
            time.sleep(5)
            print("A la plus pitoyable tache d'encre,")
            time.sleep(5)
            print("Du plus radiant des passés")
            time.sleep(5)
            print("Au plus austère des futurs,")
            time.sleep(5)
            print("De la plus belle femme du monde")
            time.sleep(5)
            print("A la plus misérable des ombres,")
            time.sleep(5)
            print("Dans la paume de tes mains tourne")
            time.sleep(5)
            print("Ma vie mon monde mon éternitée,")
            time.sleep(5)
            print("Du pire des meilleurs, aux meilleurs du pire .")
            time.sleep(10)
            print("Avec le prix de mon âme,")
            time.sleep(5)
            print("Le sépulcre de ton royaume,")
            time.sleep(5)
            print("Et la mort de ton présent,")
            time.sleep(5)
            print("Enfin j'espère, enfin je vis, enfin j'ose,")
            time.sleep(5)
            print("M'offrir cette métamorphose .")
            time.sleep(5)
            print("Et de la plus pitoyable tache d'encre,")
            time.sleep(5)
            print("A la plus grande plume d'oie,")
            time.sleep(5)
            print("Du plus austère des passés")
            time.sleep(5)
            print("Au plus radiant des futurs,")
            time.sleep(5)
            print("De la plus misérable femme du monde")
            time.sleep(5)
            print("A la plus belle des ombres,")
            time.sleep(5)
            print("Je renais dans tes cendres.")
            time.sleep(5)
            print("")
            print("                     -(nom illisible) Mage,")
            print("                          An de grâce 1233")
            print("")
            time.sleep(5)
            services.Affichage.EntreePourContinuer()
            StopAllMusic()
            print("La cage est ici.")
            print("Mais l'oie s'est envolée ailleurs.")
            services.Affichage.EntreePourContinuer()
            PlayMusicDeLetage()

    def DonneRecompensePourOubli(self, action_a_oublier, type_daction):
        # trouve le niveau de laction oubliée
        liste_daction_de_même_rang = []
        for rang in range(0, 6):
            if type_daction == "Technique":
                for numero in range(0, 6):
                    index = rang + (numero * 6)
                    liste_daction_de_même_rang.append(LISTETECHNIQUES[index])
            elif type_daction == "Sort":
                for numero in range(0, 7):
                    index = rang + (numero * 6)
                    liste_daction_de_même_rang.append(LISTESORTS[index])
            if action_a_oublier in liste_daction_de_même_rang:
                rang_de_laction = rang + 1
                break
            liste_daction_de_même_rang = []
        # nombre de pv/mana rendu, golds gagné, carac supp
        gain = 5 + rang_de_laction * 5
        gold_gagne = 100 + rang_de_laction * 5
        services.Player.AddGoldToPlayer(gold_gagne)
        dmg_critique_gagne = 2 * rang_de_laction
        taux_gagne = rang_de_laction
        if type_daction == "Technique":
            type_gain = "pv"
            type_caracteristique = "techniques"
            services.Player.points_de_vie_max += gain
            services.Player.points_de_vie += gain
            services.Player.taux_coup_critique += taux_gagne
            services.Player.degat_coup_critique += dmg_critique_gagne
        elif type_daction == "Sort":
            type_gain = "pm"
            type_caracteristique = "sorts"
            services.Player.points_de_mana_max += gain
            services.Player.points_de_mana += gain
            services.Player.taux_sort_critique += taux_gagne
            services.Player.degat_sort_critique += dmg_critique_gagne
        print(f"Vous gagnez {gain} {type_gain} max !")
        print(
            f"Vous gagnez {dmg_critique_gagne} points de dégats de {type_caracteristique} critiques !"
        )
        print(
            f"Vous gagnez {taux_gagne}% de chance de faire des {type_caracteristique} critiques !"
        )
        services.Affichage.EntreePourContinuer()

    def DoTheOldMercant(self):
        if not services.Player.mercant_healed:
            print(
                "Vous voyez de la lumière dans une des maisons."
                "\nAlors que vous entrez, vous découvrez une vieille femme mourrante, allongée sur un vieux lit décrépit."
            )
            print("Vous l'entendez vous dire d'une voix faible : *Aidez...moi...*")
            services.Affichage.EntreePourContinuer()
            while True:
                try:
                    print("*Pas...besoin de beaucoup...*")
                    print("*huit...dix...pas plus...*")
                    print("La dame vous regarde bizarrement.")
                    print("S'approcher ?")
                    print("(Vous risqueriez de le regretter)")
                    print("1 - Non")
                    print("2 - Oui")
                    choix = int(input("\n"))
                    ClearConsole()
                    if choix in [1, 2]:
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print("Vous retournez sur vos pas.")
                services.Affichage.EntreePourContinuer()
            else:
                print(
                    "Vous vous approchez de la dame, et elle se met a murmurer quelque chose en boucle."
                )
                print("Vous tendez l'oreille et vous mettez a son chevet...")
                services.Affichage.EntreePourContinuer()
                print("*Merci.*")
                services.Affichage.EntreePourContinuer()
                print(
                    "Elle se jette sur vous avec la fureur d'un diable, et plante ses crocs dans votre gorge !"
                )
                print(
                    "Vous tentez de la faire lacher prise, mais elle s'aggripe a vous avec encore plus de force."
                )
                print("Vous sentez vos forces diminuer...")
                services.Affichage.EntreePourContinuer()
                services.Player.points_de_vie_max -= 15
                services.Player.points_de_vie -= 15
                services.Player.points_de_mana_max -= 15
                services.Player.points_de_mana -= 15
                if services.Player.points_de_vie <= 0:
                    if services.Player.possede_une_fee == True and "Fée dans un Bocal" in services.Player.liste_dartefacts_optionels:
                        services.Player.liste_dartefacts_optionels.remove("Fée dans un Bocal")
                        services.Player.possede_une_fee = False
                        print("...au point ou meme la fée qui sort de son bocal n'arrive pas a vous regénérer assez vite...")
                        services.Affichage.EntreePourContinuer()
                    StopAllMusic()
                    PlaySound("death")
                    print("..et vous mourrez.")
                    services.Affichage.EntreePourContinuer()
                    services.Player.player_tags.append("KIA")
                    CheckForKIA()
                else:
                    services.Player.points_de_vie = 1
                    services.Player.points_de_mana = 0
                    services.Player.mercant_healed = True
                    print(
                        "...et alors que vous appretez a fermer les yeux pour la derniere fois, la dame vous lache."
                    )
                    services.Affichage.EntreePourContinuer()
                    print(
                        "*Merci jeune homme.*"
                        "\n*Cela faisait longtemps que je n'avais pas eu pareil festin. Ho ho ho !*"
                    )
                    print(
                        "*Revenez me voir d'ici quelques minutes et j'aurais de quoi rembourser votre générosité.*"
                    )
                    services.Affichage.EntreePourContinuer()
                    print(
                        "Vous avez (été forcé d')accepté(r) la quête [La Générositée d'une Alchimiste] !"
                    )
                    print("Retournez voir l'alchimiste le plus vite possible !")
                    services.Player.quete = "La Générositée d'une Alchimiste"
                    services.Affichage.EntreePourContinuer()
                    print("Vous sortez de la maison en gémissant.")
                    print("Vous avez perdu 15 points de vie et de mana max !")
                    print(
                        "Vos points de vie et de mana sont aussi au minimum ! Allez vite vous faire soigner !"
                    )
                    services.Affichage.EntreePourContinuer()
        else:
            print(
                "Vous voyez de la lumière dans une des maisons."
                "\nVous passez la porte primitive de taule et d'acier, et découvrez derrière une modeste échoppe."
            )
            print(
                "Sur l'étalage, des items d'une raretée phénoménale sont exposés derrière une vitre ."
            )
            print("Vous entendez une voix familière derrière le comptoir.")
            services.Affichage.EntreePourContinuer()
            if services.Player.quete == "La Générositée d'une Alchimiste":
                print("*Merci encore pour le remontant, jeune homme.*")
                print(
                    "*Je me présente : Mariette, alchimiste en quête de nouveaux ingrédients.*"
                )
                services.Affichage.EntreePourContinuer()
                print("*Vampire à mes heures perdues.*")
                services.Affichage.EntreePourContinuer()
                print(
                    "*La...condition...de cet étage fait que beaucoup de choses bizarres s'y produisent.*"
                    "\n*Comme par exemple la force mysterieuse qui fait que toutes mes productions passent de magistrales à divine !*"
                )
                print(
                    "*Ducoup je vis ici avec la permission du nouveau maitre des lieux, et je lui donne deux trois remèdes en échange .*"
                )
                services.Affichage.EntreePourContinuer()
                print("*Ce genre de choses.*")
                services.Affichage.EntreePourContinuer()
                print("Vous recevez un remède divin et une pillule divine !")
                services.Affichage.EntreePourContinuer()
                PlaySound("questdone")
                print("Vous avez accompli la quête [La Générositée d'une Alchimiste] !")
                services.Player.quete_complete.append(services.Player.quete)
                if "None" in services.Player.quete_complete:
                    services.Player.quete_complete.remove("None")
                services.Player.quete = "None"
                services.Affichage.EntreePourContinuer()
                PlayMusicDeLetage()
                print(
                    "*Ceux la sont gratuits, mais les autres ne le seront pas. Ho ho ho !*"
                )
                services.Affichage.EntreePourContinuer()
            if not "Fantome" in services.Player.player_tags:
                while True:
                    while True:
                        try:
                            print("*Vous voyez quelque chose qui vous plait ?*")
                            print(
                                "*J'espère que ce n'est pas moi, car je ne suis pas a vendre ! Ho ho ho !*"
                            )
                            print("1 - Partir")
                            print("2 - Remède Divin: 75 golds")
                            print("3 - Pillule Divine: 80 golds")
                            print("4 - Grand Mutagène Doré: 200 golds")
                            print("5 - Soluté d'Absolution: 100 golds")
                            print("6 - Soluté d'Exorcisme: 200 golds")
                            print("7 - Larmes de Vénus: 300 golds")
                            choix = int(
                                input(
                                    f"Vous avez {services.Player.nombre_de_gold} golds. Que souhaitez vous acheter ? "
                                )
                            )
                            ClearConsole()
                            if choix in range(1, 8):
                                break
                        except ValueError:
                            ClearConsole()
                    if choix == 1:
                        print("*Au revoir !*")
                        services.Affichage.EntreePourContinuer()
                        break
                    if choix in range(2, 8):
                        if choix == 2:
                            cout = 75
                            nom_de_litem = "Remède Divin"
                        elif choix == 3:
                            cout = 80
                            nom_de_litem = "Pillule Divine"
                        elif choix == 4:
                            cout = 200
                            nom_de_litem = "Grand Mutagène Doré"
                        elif choix == 5:
                            cout = 100
                            nom_de_litem = "Soluté d'Absolution"
                        elif choix == 6:
                            cout = 200
                            nom_de_litem = "Soluté d'Exorcisme"
                        elif choix == 7:
                            cout = 300
                            nom_de_litem = "Larmes de Vénus"
                        if services.Player.nombre_de_gold >= cout:
                            services.Player.nombre_de_gold -= cout
                            if nom_de_litem == "Larmes de Vénus":
                                services.FloorMaker.GiveRandomArtefact("Larmes de Vénus","Don")
                                print("Vous achetez l'artefact [Larmes de Vénus] !")
                                print("Cette fiole emplie d'un soluté magnifique permet d'apaiser les feux de la colère et ne laisse derrière que les ombres de la culpabilité.\nPasser son tour à 20% de chance de stopper les effets de Confusion !")
                            else:
                                print(f"Vous achetez l'item [{nom_de_litem}] !")
                                services.Player.items_possedes[nom_de_litem] += 1
                            services.Affichage.EntreePourContinuer()
                            print(
                                "(Mariette vous prend le front a deux main et vous y laisse un gros bisou)"
                            )
                            print("*Vous êtes un amour !*")
                            services.Affichage.EntreePourContinuer()
                        else:
                            print(
                                "*C'est beau de vouloir soutenir un commerce de proximité,"
                                " mais si vous n'avez pas assez de golds, ca me met dans l'embarras plus qu'autre chose .*"
                            )
                            services.Affichage.EntreePourContinuer()
                            if services.Player.items_possedes["Remède"] <= 2 :
                                print("*Qu'importe, c'est l'intention qui compte !*")
                                print("*Prenez donc ceci pour votre gentillesse.*")
                                services.Affichage.EntreePourContinuer()
                                print("Mariette vous donne un remède !")
                                services.Player.items_possedes["Remède"] += 1
                                services.Affichage.EntreePourContinuer()

    def DoTheFinalLibrary(self):
        print(
            "Entre deux piliers de tufs, vous découvrez un couloir singulier."
            "\nA l'interieur, vous sentez votre coeur s'arreter de battre...sans que cela ne vous affecte."
            "\nA la fin du couloir, vous trouvez une magnifique bibliothèque de bois ornemental, dans lequel sont rangés des livres de toutes les couleurs."
        )
        services.Affichage.EntreePourContinuer()
        while True:
            while True:
                nombre_a_afficher = 2
                try:
                    print("Seuls certains livres attirent votre attention :")
                    print("1 - Partir")
                    for livre in BIBLIOTHEQUEFINALE:
                        print(f"{nombre_a_afficher} - Prendre le livre [{livre}]")
                        nombre_a_afficher += 1
                    choix = int(input("Choisissez avec les nombre le livre que vous souhaitez prendre : "))
                    ClearConsole()
                    if choix in range(1, (len(BIBLIOTHEQUEFINALE) + 2)):
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print(
                    "Vous laissez la bibliothèque derriere vous et sortez du couloir."
                )
                print("A votre plus grand soulagement, votre coeur se remet a battre.")
                services.Affichage.EntreePourContinuer()
                break
            elif choix == 21:
                self.WriteInFinalBook()
            else:
                print("Vous ouvrez le livre à une page aléatoire.")
                services.Affichage.EntreePourContinuer()
                dictionnaire_sous_forme_de_liste = list(BIBLIOTHEQUEFINALE)
                nom_du_livre = dictionnaire_sous_forme_de_liste[(choix - 2)]
                liste_de_passages_a_lire = BIBLIOTHEQUEFINALE[nom_du_livre]
                for passage in liste_de_passages_a_lire:
                    print(passage)
                    services.Affichage.EntreePourContinuer()
                print("Vous refermez le livre et le reposez dans la bibliothèque.")
                services.Affichage.EntreePourContinuer()

    def WriteInFinalBook(self):
        print("Vous prenez le livre familier et observez sa couverture.")
        print("Une magnifique cigogne rouge regarde vers la gauche.")
        print(
            "Sur la première page, vous retrouvez les mêmes lignes que dans le livre de la cigogne bleue a une différence près :"
        )
        print("Elles ne se font pas absorber quand vous les touchez.")
        services.Affichage.EntreePourContinuer()
        print("Vous pouvez y lire les phrases suivantes :")
        donnees_de_s0ve = self.GetPermanentThingsFromS0ve()
        liste_de_sorts_enregistres = ast.literal_eval(donnees_de_s0ve["Livre de sort"])
        for sort in liste_de_sorts_enregistres:
            print(sort)
        services.Affichage.EntreePourContinuer()
        if not services.Player.final_library_used:
            print("...?")
            services.Affichage.EntreePourContinuer()
            while True:
                try:
                    print(
                        "On dirait presque que le livre tente d'absorber votre mana..."
                    )
                    print("1 - Remettre le livre a sa place")
                    print("2 - Le laisser absorber votre mana (Coute 100pm)")
                    choix = int(input("Que souhaitez vous faire ? "))
                    ClearConsole()
                    if choix in [1, 2]:
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print("Vous refermez le livre et le reposez dans la bibliothèque.")
                services.Affichage.EntreePourContinuer()
            elif choix == 2 and services.Player.points_de_mana < 100:
                print("Vous n'avez pas assez de mana !")
                print("Vous refermez le livre et le reposez dans la bibliothèque.")
                services.Affichage.EntreePourContinuer()
            else:
                services.Player.points_de_mana -= 100
                print(
                    "Vous laissez le livre prendre votre mana.\nUne aura bleue commence a l'entourer, puis il se referme violemment sur votre bras !"
                )
                services.Affichage.EntreePourContinuer()
                while True:
                    try:
                        print(
                            "Vous ne pouvez pas risquer d'endommager votre bras avec une technique, il faut se débarrasser du bouquin avec un sort !"
                        )
                        numero_affichage = 1
                        for sorts in services.Player.sorts_possedes:
                            print(f"{numero_affichage} - {sorts}")
                            numero_affichage += 1
                        choix = int(input("Quel sort souhaitez-vous utiliser ? "))
                        ClearConsole()
                        if choix in range(1, (len(services.Player.sorts_possedes) + 1)):
                            break
                    except ValueError:
                        ClearConsole()
                sort_choisi = services.Player.sorts_possedes[(choix - 1)]
                self.AddSpellToS0ve(sort_choisi)
                services.Player.final_library_used = True
                services.Save.SaveTheGameSansAffichage()
                print(
                    "Vous lancez le sort et, dans un flash de lumière illuminant le livre, vous le sentez disparaitre !"
                )
                services.Affichage.EntreePourContinuer()
                print(
                    f"Vous avez inscrit le sort [{sort_choisi}] dans le livre de la Cigogne Rouge !"
                )
                services.Affichage.EntreePourContinuer()
                print(
                    "Le livre lache votre bras, et vous le replacez dans la bibliothèque."
                )
                services.Affichage.EntreePourContinuer()
        else:
            print("Vous refermez le livre et le reposez dans la bibliothèque.")
            services.Affichage.EntreePourContinuer()

    def AddSpellToS0ve(self, sort_choisi):
        donnees_de_s0ve = self.GetPermanentThingsFromS0ve()
        liste_de_sorts_enregistres = ast.literal_eval(donnees_de_s0ve["Livre de sort"])
        if not (sort_choisi in liste_de_sorts_enregistres):
            liste_de_sorts_enregistres.append(sort_choisi)
            donnees_de_s0ve["Livre de sort"] = liste_de_sorts_enregistres
            self.SetPermanentThingsToS0ve(donnees_de_s0ve)

    def AddSoulToS0ve(self):
        donnees_de_s0ve = self.GetPermanentThingsFromS0ve()
        if donnees_de_s0ve["486241597531"] != "Jean.rar":
            donnees_de_s0ve["486241597531"] = "Jean.rar"
            self.SetPermanentThingsToS0ve(donnees_de_s0ve)

    def DoTheQuests(self):
        if services.Player.quest_giver:
            if services.Player.quete == "Voeu de Pauvreté" and services.Player.nombre_de_gold == 0:
                services.Player.quete += " [Complete]"
            print(
                "Dans un coin de la fête foraine, dans une grande poubelle, vous apercevez un robot primitif fait de métal, avec des nuances de cuivre, d'acier ou de bronze."
            )
            print(
                "Alors que vous vous approchez de la machine, son visage d'aluminum dans lequel ont été creusé 3 trous pour les yeux et la bouche s'illumine de l'interieur."
            )
            services.Affichage.EntreePourContinuer()
            print("*Hey, toi la, ouai toi, approche n'aie pas peur !*")
            print(
                "*Je suis un ancien explorateur, comme toi.*\n*J'ai appris deux trois trucs avant de mourir, et je suis prêt a te les apprendre si tu fais des trucs pour moi.*"
            )
            services.Affichage.EntreePourContinuer()
            while True:
                while True:
                    try:
                        print(
                            "*Sers toi en quete, et fais gaffe ! Je saurais si tu a triché ou pas !*\n"
                        )
                        print("1 - Retour\n")
                        print(
                            "2 - Voeu de Pauvreté : Reviens me voir avec 0 golds dans ton inventaire ! (Rang E)"
                        )
                        print(
                            "3 - Interminable : Fais durer ton prochain combat jusqu'au tour 50 (Rang D)\n"
                        )
                        print(
                            "4 - Epreuve du Magister : Bats les 4 prochains ennemis sans utiliser d'action de Feu, Foudre, Glace (Rang C)"
                        )
                        print(
                            "5 - Epreuve des Mages-Epeistes : Bats les 4 prochains ennemis sans utiliser d'action de Terre, Physique, Sang (Rang C)\n"
                        )
                        print(
                            "6 - Force et Honneur : Bats les 8 prochains ennemis sans utiliser d'items en combat (Rang B)"
                        )
                        print(
                            "7 - Moqueries Magiques/Techniques : Bats le Bouffon sans utiliser de sorts ou de techniques [au choix] (Rang A)\n"
                        )
                        print("8 - Sérendipité : Finis toute les quêtes (Rang S)\n")
                        print(f"9 - Abandonner la quête en cours : [{services.Player.quete}]\n")
                        choix = int(
                            input(
                                "Que souhaitez vous faire ? (Vous ne pouvez prendre qu'une seule quête à la fois.)"
                            )
                        )
                        ClearConsole()
                        if choix in range(1, 10):
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 1:
                    print(
                        "Vous laissez la boite de métal parler toute seule, et revenez sur vos pas."
                    )
                    services.Affichage.EntreePourContinuer()
                    break
                elif (services.Player.quete != "None") and (choix != 9):
                    if "[Complete]" in services.Player.quete:
                        print("Bien joué ! Voila ta récompense !")
                        self.DonneRecompenseQuete()
                        quete_reussie = services.Player.quete
                        quete_reussie = quete_reussie.rstrip("[Complete]").rstrip()
                        services.Player.quete_complete.append(quete_reussie)
                        if "None" in services.Player.quete_complete:
                            services.Player.quete_complete.remove("None")
                        services.Player.quete = "None"
                    else:
                        print("*T'a déja prit une quete ! Ouste !*")
                        services.Affichage.EntreePourContinuer()
                elif choix == 2:
                    if "Voeu de Pauvreté" in services.Player.quete_complete:
                        print("*Tu l'as déja faite celle là.*")
                        services.Affichage.EntreePourContinuer()
                    else:
                        print(
                            "*C'est plutot simple ! Utilise tout ton argent et reviens me voir.*"
                            "\n*Je te validerait la quete a ce moment la.*"
                        )
                        print("Vous avez accepté la quête [Voeu de Pauvreté]")
                        services.Affichage.EntreePourContinuer()
                        services.Player.quete = "Voeu de Pauvreté"
                elif choix == 3:
                    if "Interminable" in services.Player.quete_complete:
                        print("*Tu l'as déja faite celle là.*")
                        services.Affichage.EntreePourContinuer()
                    else:
                        print(
                            "*Ton prochain combat, boss ou monstre, fait le durer jusqu'au 50eme tour minimum.*"
                            "\n*Si tu échoue, reviens me voir et je te la redonnerais.*"
                        )
                        print("Vous avez accepté la quête [Interminable]")
                        services.Affichage.EntreePourContinuer()
                        services.Player.quete = "Interminable"
                elif choix == 4:
                    if "Epreuve du Magister" in services.Player.quete_complete:
                        print("*Tu l'as déja faite celle là.*")
                        services.Affichage.EntreePourContinuer()
                    else:
                        print(
                            "*On donnait cette épreuve aux membres du Magister, un consort de mages de la nature.*"
                            "\n*Tu échoue si tu use de Techniques ou Sorts en lien avec le Feu, la Foudre ou la Glace pendant les 4 prochains combats.*"
                        )
                        print(
                            "*Le Tir Arcanique et l'attaque Légère ont tout deux l'élément Physique !*"
                        )
                        print("Vous avez accepté la quête [Epreuve du Magister]")
                        services.Affichage.EntreePourContinuer()
                        services.Player.quete = "Epreuve du Magister"
                elif choix == 5:
                    if "Epreuve des Mages-Epeistes" in services.Player.quete_complete:
                        print("*Tu l'as déja faite celle là.*")
                        services.Affichage.EntreePourContinuer()
                    else:
                        print(
                            "*On donnait cette épreuve à l'escouade des Mages-Epeistes, au service de sa Majestée.*"
                            "\n*Tu échoue si tu use de Techniques ou Sorts en lien avec la Terre, le Sang ou le Physique pendant les 4 prochains combats.*"
                        )
                        print(
                            "*Attention ! Le Tir Arcanique et l'attaque Légère ont tout deux l'élément Physique !*"
                        )
                        print("Vous avez accepté la quête [Epreuve des Mages-Epeistes]")
                        services.Affichage.EntreePourContinuer()
                        services.Player.quete = "Epreuve des Mages-Epeistes"
                elif choix == 6:
                    if "Force et Honneur" in services.Player.quete_complete:
                        print("*Tu l'as déja faite celle là.*")
                        services.Affichage.EntreePourContinuer()
                    else:
                        print(
                            "*Les aventuriers se reposent trop sur leur force donnée, les objets, et pas assez sur leur force acquise, les sorts et techniques.*"
                            "\n*Libère toi des chaines du consummérisme !*"
                        )
                        print("Vous avez accepté la quête [Force et Honneur]")
                        services.Affichage.EntreePourContinuer()
                        services.Player.quete = "Force et Honneur"
                elif choix == 7:
                    if (
                        "Moqueries Magiques" in services.Player.quete_complete
                        or "Moqueries Techniques" in services.Player.quete_complete
                    ):
                        print("*Tu l'as déja faite celle là.*")
                        services.Affichage.EntreePourContinuer()
                    else:
                        while True:
                            try:
                                print(
                                    "*Je me suis fais humilier par le Bouffon, et en échange il m'a foutu dans cette boite de conserve pour l'éternitée.*"
                                    "\n*Humilie le pour moi !*"
                                )
                                print("1 - *Tu préfere l'écraser sans Sorts ?*")
                                print("2 - *Tu préfère l'écraser sans Techniques ?*")
                                choix_quete = int(input("Que souhaitez vous faire ? "))
                                ClearConsole()
                                if choix_quete in [1, 2]:
                                    break
                            except ValueError:
                                ClearConsole()
                        if choix_quete == 1:
                            print("*Qu'il en soit ainsi !*")
                            print("Vous avez accepté la quête [Moqueries Magiques]")
                            services.Player.quete = "Moqueries Magiques"
                        else:
                            print("*Qu'il en soit ainsi !*")
                            print("Vous avez accepté la quête [Moqueries Techniques]")
                            services.Player.quete = "Moqueries Techniques"
                        services.Affichage.EntreePourContinuer()
                elif choix == 8:
                    if "Sérendipité" in services.Player.quete_complete:
                        print("*Tu l'as déja faite celle là.*")
                        services.Affichage.EntreePourContinuer()
                    elif (
                        (
                            "Moqueries Magiques" in services.Player.quete_complete
                            or "Moqueries Techniques" in services.Player.quete_complete
                        )
                        and ("Force et Honneur" in services.Player.quete_complete)
                        and ("Epreuve des Mages-Epeistes" in services.Player.quete_complete)
                        and ("Epreuve du Magister" in services.Player.quete_complete)
                        and ("Interminable" in services.Player.quete_complete)
                        and ("Voeu de Pauvreté" in services.Player.quete_complete)
                    ):
                        services.Player.quete_complete.append("Sérendipité")
                        self.AfficheSecretQuetes()
                        break
                    else:
                        print("Tu n'a pas réussi toute mes demandes.")
                        print("Reviens me voir lorsque ce sera le cas.")
                        services.Affichage.EntreePourContinuer()
                elif choix == 9:
                    if services.Player.quete == "None":
                        print("*Tu n'a pas de quêtes en cours !*")
                        print("*Reviens lorsque ce sera le cas.*")
                    elif "[Complete]" in services.Player.quete:
                        print("Et puis quoi encore ??")
                    else:
                        print(f"*Tu veux abandonner la quête [{services.Player.quete}] ?*")
                        print("*Très bien, c'est noté.*")
                        services.Player.quete = "None"
                    services.Affichage.EntreePourContinuer()
        else:
            print("Il y a un cratère de suie, de déchets, et de bouts de chairs.")
            services.Affichage.EntreePourContinuer()
            print("Parmis les décombres, vous trouvez une carte étudiante :")
            services.Affichage.EntreePourContinuer()
            print(
                "Adrien Stéfalnos\nProfesseur d'Archéologie\nCampus de Capital City\nNuméro de badge: 3236353"
            )
            services.Affichage.EntreePourContinuer()
            print("Vous laissez le cratère et retournez sur vos pas.")
            services.Affichage.EntreePourContinuer()
            services.Sove.RajouteEntreeAuLivreCigogneBlancheSiOnAPas("???", "Sérendipité")

    def AfficheSecretQuetes(self):
        StopAllMusic()
        print(
            "*Tu as rendu un fier service a ce vieux spectre.*\n*C'est dingue a quel point on peut s'ennuyer quand on a plus controle de ses membres, et qu'on est enfermé dans une idole d'acier.*"
        )
        print(
            "*Je n'ai plus rien a te donner, a part peut etre une histoire, alors écoute bien :*"
        )
        services.Affichage.EntreePourContinuer()
        print(
            "*C'était il y a très longtemps.*\n*Un âge tellement reculé que personne ne s'en souvient.*"
        )
        print(
            "*Enfaite, cette histoire vient d'images retrouvées dans d'anciens temples enfouis, pour te dire a quel point c'est vieux.*"
        )
        print(
            "*On a même pas de traces dans les livres d'histoires, ou même sous forme de traditions ou chants !*"
        )
        services.Affichage.EntreePourContinuer()
        print("*Mais je m'égare.*")
        services.Affichage.EntreePourContinuer()
        PlayMusic("tales")
        print(
            "*C'est un chateau dans le ciel. Ou une île volante de marbre blanc. Ou encore un palace porté dans les airs par un oiseau invisible.*"
        )
        services.Affichage.EntreePourContinuer()
        print(
            "*C'est un lieu impossible, ou chaque portes et chaque couloirs mènent a des endroits différents selon l'endroit et le temps.*"
        )
        services.Affichage.EntreePourContinuer()
        print(
            "*Ce sont des êtres puissants, des démons, des esprits, portant de lourds fardeaux, chacun s'occupant d'un aspect de la réalité.*"
        )
        services.Affichage.EntreePourContinuer()
        print(
            "*C'est une batisse abritant les dieux, crée a partir d'un joyau, d'une pièce, du coeur d'un ange, ou de l'oeil d'un guerrier.*"
        )
        services.Affichage.EntreePourContinuer()
        print(
            "*C'est un pouvoir qui traverse les dimensions, teinté par la pureté de l'âme qui se l'approprie.*"
        )
        services.Affichage.EntreePourContinuer()
        print(
            "*C'est un monde éteint, endormi, attisé par les mains divines, hostile.*"
        )
        services.Affichage.EntreePourContinuer()
        print(
            "*C'est une guerre entre nos protecteurs et les légions de voyageurs, aux portes du monde étranger, dans un lieu ou les roses ne fânent jamais.*"
        )
        services.Affichage.EntreePourContinuer()
        print(
            "*C'est la fiertée de 5 êtres exceptionels choisis pour défendre la porte des étoiles.*"
        )
        services.Affichage.EntreePourContinuer()
        print(
            "*C'est la douleur du fratricide, l'odeur du pétrichor carmin, les vents d'un affrontement décisif.*"
        )
        services.Affichage.EntreePourContinuer()
        print(
            "*C'est la disparition de toutes les divinités de ce monde, comme prix a payer pour refermer ce qui n'aurait jamais du être ouvert.*"
        )
        services.Affichage.EntreePourContinuer()
        print(
            "*C'est la chute de la grandeur et fierté des dieux dans l'oubli d'un océan sans nom.*"
        )
        services.Affichage.EntreePourContinuer()
        print(
            "*Cette histoire, c'est celle de la guerre de l'interdit. Ou en tout cas c'est le nom sur lequel se sont mises d'accord les anciennes gravures.*"
        )
        services.Affichage.EntreePourContinuer()
        print("*Mais laisse moi donc la continuer avec ma... théorie.*")
        services.Affichage.EntreePourContinuer()
        print("*La raison pour laquelle je suis ici.*")
        services.Affichage.EntreePourContinuer()
        print("*La raison pour laquelle j'ai persisté toute ces années.*")
        services.Affichage.EntreePourContinuer()
        print("(la lumière dans la statue se fait plus faible.)")
        services.Affichage.EntreePourContinuer()
        print("*C'est peut etre la fin de l'histoire des dieux...*")
        services.Affichage.EntreePourContinuer()
        print("*...mais pas celle du pouvoir qui a crée leur demeure.*")
        services.Affichage.EntreePourContinuer()
        print(
            "(la lumière s'éteint. Seule la voix calme du donneur de quête persiste.)"
        )
        services.Affichage.EntreePourContinuer()
        print("*Ce n'est pas un concept : c'est un objet réel.*")
        services.Affichage.EntreePourContinuer()
        print("*C'est son oubli pendant des millénaires au fond de l'eau salée.*")
        services.Affichage.EntreePourContinuer()
        print("*C'est son repéchage par un homme imprégné de magie.*")
        services.Affichage.EntreePourContinuer()
        print(
            "*C'est son étude pendant des décennies pour comprendre comment il marche.*"
        )
        services.Affichage.EntreePourContinuer()
        print(
            "*C'est sa prise en main par un fou déterminé a répendre sa folie sur le monde.*"
        )
        services.Affichage.EntreePourContinuer()
        print("*C'est l'obnubilation, la détermination, l'obsession.*")
        services.Affichage.EntreePourContinuer()
        print(
            "(Vous sentez le mana s'activer tout autour de vous, comme si quelqu'un lancait un sort)"
        )
        services.Affichage.EntreePourContinuer()
        print("*Nourrie avec le mana du Mage...*")
        services.Affichage.EntreePourContinuer()
        print("*...corrompue par l'obsession du Roi...*")
        services.Affichage.EntreePourContinuer()
        print("*...l'ancienne demeure des dieux est devenue le Co-*")
        print("(Appuyez sur entrée pour continuer)")
        time.sleep(1)
        ClearConsole()
        PlayWavSound("ELECm")
        services.Player.quest_giver = False
        services.Save.SaveTheGameSansAffichage()
        print("Un gigantesque éclair s'abat sur la chose de métal.")
        services.Affichage.EntreePourContinuer()
        print("Une pluie de ferraille et de chair en décomposition s'abat sur vous.")
        services.Affichage.EntreePourContinuer()
        print(
            "Vous regardez le cratère fumant devant vous pendant quelques minutes, horrifié, et quittez les lieux en courant."
        )
        services.Affichage.EntreePourContinuer()
        PlayMusicDeLetage()

    def DonneRecompenseQuete(self):
        if services.Player.quete == "Voeu de Pauvreté [Complete]":
            print(
                "Le truc vous apprend a vous débarraser de votre stress. Vous vous sentez plus leger !"
            )
            print("Vous gagnez 15 points de vie max !")
            services.Player.points_de_vie_max += 15
            services.Player.points_de_vie += 15
        elif services.Player.quete == "Interminable [Complete]":
            print(
                "Le truc vous apprend la patience et la concentration sur de longues périodes de temps."
            )
            print("Vous gagnez 15 points de mana max !")
            services.Player.points_de_mana_max += 15
            services.Player.points_de_mana += 15
        elif services.Player.quete == "Epreuve du Magister [Complete]":
            print(
                "Le truc vous apprend une méthode de respiration qui permet de reveiller la force latente."
            )
            print("Vous gagnez 8 points de degat de coup/sorts critiques !")
            services.Player.degat_coup_critique += 8
            services.Player.degat_sort_critique += 8
        elif services.Player.quete == "Epreuve des Mages-Epeistes [Complete]":
            print(
                "Le truc vous montre des points d'acuponctures à presser pour ameliorer le flux sanguin."
            )
            print("Vous gagnez 3 points de force/intelligence/defence !")
            services.Player.points_de_force += 3
            services.Player.points_dintelligence += 3
            services.Player.points_de_defence += 3
        elif services.Player.quete == "Force et Honneur [Complete]":
            print(
                "Le truc vous apprend a déduire les arcs vectoriels des attaques ennemies a partir de leurs mouvements."
            )
            print("Vous gagnez 8% d'esquive !")
            services.Player.taux_desquive += 8
        elif services.Player.quete == "Moqueries Techniques [Complete]":
            print("Le truc vous passe la technique ultime de son clan.")
            print("Vous apprenez le Iaido !")
            services.Player.techniques_possedes.append("Iaido")
            if "Syra" in services.Player.liste_dartefacts_optionels:
                            print("Grace au verre de Syra que vous avez bu, vous gagnez aussi 10 pm max !")
                            services.Player.points_de_mana += 10
                            services.Player.points_de_mana_max += 10
                            services.Affichage.EntreePourContinuer()
        elif services.Player.quete == "Moqueries Magiques [Complete]":
            print("Le truc vous passe le sort ultime de son clan.")
            print("Vous apprenez le Carrousel !")
            services.Player.sorts_possedes.append("Carrousel")
            if "Syra" in services.Player.liste_dartefacts_optionels:
                print("Grace au verre de Syra que vous avez bu, vous gagnez aussi 10 pv max !")
                services.Player.points_de_vie += 10
                services.Player.points_de_vie_max += 10
                services.Affichage.EntreePourContinuer()
        services.Affichage.EntreePourContinuer()

    def DoTheBloodStone(self):
        print("Entre deux bibliothèque, un passage étroit attire votre attention.")
        print(
            "De l'autre coté, vous trouvez de nombreuses formes de vies, artefacts, et livres concernant de glorieuses batailles et de magistrales découvertes."
        )
        print(
            "Comme dans un musée, chaque trouvaille est encastrée dans un bloc de verre, et son hisoire expliquée de manière concise par une plaquette en dessous."
        )
        services.Affichage.EntreePourContinuer()
        print(
            "Seul un objet attire votre attention, a cause de sa présence solitaire dans l'allée *Usage Public*,"
        )
        print(
            "mais aussi par l'impressionnante quantitée de statues d'or présentes autour."
        )
        print(
            "Sur un petit coussin de soie, vous apercevez une pierre rouge sang, entourée des mêmes symboles que sur le clone d'obsidienne magique."
        )
        services.Affichage.EntreePourContinuer()
        while True:
            while True:
                try:
                    print(
                        "La plaquette en dessous indique : *Fausse Pierre Philosophale. Transmute la vitalitée en golds.*"
                    )
                    print("1 - Partir")
                    print("2 - Tenir la Pierre")
                    choix = int(input("Que souhaitez vous faire ? "))
                    ClearConsole()
                    if choix in [1, 2]:
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print("Vous retournez sur vos pas et quittez le musée de curiositées.")
                services.Affichage.EntreePourContinuer()
                break
            else:
                still_alive = self.AbsorptionParBloodStone()
                if still_alive:
                    print("Vous lachez la pierre et toussez quelques pièces.")
                    print(
                        "Certains endroits sur votre corps ont gagné une teinte dorée, et vos articulations vous semblent rigides."
                    )
                    services.Affichage.EntreePourContinuer()
                else:
                    PlaySound("death")
                    # affichage de la fin.
                    print("L'entieretée de votre existance est absorbée par la pierre.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous devenez une statue d'or parmis les autres.")
                    services.Affichage.EntreePourContinuer()
                    print("ERREUR : CORRUPTION DES DONNEES DE SAUVEGARDE")
                    # mise en place dernieres donnes de sauvegarde ==) joueur
                    services.Save.FromSaveFileToDict()
                    services.Save.FromDictToPlayer()
                    services.Affichage.EntreePourContinuer()
                    print("REECRITURE EN COURS DES DONNEES INVALIDES DANS SAVE.TXT...")
                    # remplacement des donnees de sauvegarde pour secret.
                    dir_path = DOSSIER_RESSOURCES
                    chemin_du_fichier_save = dir_path + "\\save.txt"
                    with open(chemin_du_fichier_save, "w") as fichier:
                        fichier.write(
                            "Parmis les rivages distants je vois des montagnes d'or."  # 15
                            "\nQuel enfer attend celui qui n'existe pas ?"  # 12
                            "\nMarqué par la pierre, marqué par la mort,"  # 11
                            "\nMon nom réduit en milliers d'éclats."  # 11
                            "\nNombreuses sont les syllabes, lignes par lignes,"  # 13
                            "\nFlottant dans le vide, j'espère vous arrivent,"  # 11
                            "\nMon chemin illuminé, signes par signes,"  # 10
                            "\nVous mène a l'infame, vous mène a l'indigne."  # 13
                            "\n\n                                   - Véritée,"
                            "\n                                         Auteur inconnu."
                        )
                    services.Sove.RajouteEntreeAuLivreCigogneBlancheSiOnAPas("???", "Montagnes d'or")
                    services.Affichage.EntreePourContinuer()
                    # mise en place donnees de joueur ( qui est aussi dernieres donnees de sauvegarde) ==) donnes des sauvegarde
                    services.Save.FromPlayerToDict()
                    services.Save.FromDictToSaveFile("\\save.txt")
                    print("REECRITURE TERMINEE")
                    services.Affichage.EntreePourContinuer()
                    PlayMusicDeLetage()

    def AbsorptionParBloodStone(self):
        print("Vous prenez la pierre dans la main et sentez votre énergie s'évaporer.")
        services.Affichage.EntreePourContinuer()
        self.ArreteAbsorption = threading.Event()
        self.Absorption = threading.Thread(target=self.ConversionBloodStone)
        self.Absorption.start()
        input("")
        self.ArreteAbsorption.set()
        time.sleep(2)
        if services.Player.points_de_vie >= 1:
            return True
        return False

    def ConversionBloodStone(self):
        numero = 0
        temps_dattente = 2
        while not self.ArreteAbsorption.isSet():
            print("                 -=Conversion en Cours=-")
            print(f"                      {services.Player.points_de_vie} pv")
            print(f"                      {services.Player.nombre_de_gold} golds")
            print("")
            print("        Appuyez sur entree pour lacher la pierre")
            time.sleep(temps_dattente)
            ClearConsole()
            numero += 1
            if numero in range(1, 6):
                services.Player.points_de_vie -= 1
                gain_gold = 1
                services.Player.AddGoldToPlayer(gain_gold)
            elif numero in range(6, 11):
                services.Player.points_de_vie -= 2
                gain_gold = 2
                services.Player.AddGoldToPlayer(gain_gold)
                temps_dattente = 1
            elif numero in range(11, 16):
                services.Player.points_de_vie -= 3
                gain_gold = 4
                services.Player.AddGoldToPlayer(gain_gold)
                temps_dattente = 0.8
            elif numero in range(16, 21):
                services.Player.points_de_vie -= 4
                gain_gold = 8
                services.Player.AddGoldToPlayer(gain_gold)
                temps_dattente = 0.6
            elif numero in range(21, 26):
                services.Player.points_de_vie -= 5
                gain_gold = 16
                services.Player.AddGoldToPlayer(gain_gold)
                temps_dattente = 0.4
            elif numero in range(26, 31):
                services.Player.points_de_vie -= 6
                gain_gold = 32
                services.Player.AddGoldToPlayer(gain_gold)
                temps_dattente = 0.2
            elif numero in range(31, 36):
                services.Player.points_de_vie -= 7
                gain_gold = 64
                services.Player.AddGoldToPlayer(gain_gold)
                temps_dattente = 0.2
            else:
                services.Player.points_de_vie -= round(numero / 2)
                gain_gold = numero * numero
                services.Player.AddGoldToPlayer(gain_gold)

    def DoTheGacha(self):
        chanceux = False
        malchanceux = False
        print(
            "Un petit étang, grand comme une chambre d'hotel, entouré de hauts palmiers et de verdure."
        )
        commentaire = "Dans l'eau bleutée, vous pouvez voir un profond abysse dans lequel se perd la lumière."
        nombre_aleatoire = random.randint(0, services.Player.points_de_mana_max)
        nombre_aleatoire2 = random.randint(0, services.Player.points_de_mana_max)
        nombre_aleatoire3 = random.randint(0, services.Player.points_de_mana_max)
        print(nombre_aleatoire)
        if services.Player.points_de_mana in [nombre_aleatoire, nombre_aleatoire2, nombre_aleatoire3]:
            chanceux = True
            commentaire += " Et à l'interieur, une gigantesque baleine nage sereinement."
        elif 0 in [nombre_aleatoire, nombre_aleatoire2, nombre_aleatoire3]:
            malchanceux = True
            commentaire += (
                " Et tout au fond, une paire d'yeux qui vous regarde... fixement."
            )
        print(commentaire)
        print(
            "Cepandant, quand vous tentez d'enfoncer vos mains dans l'oasis ou de toucher les buissons qui l'entourent, tout disparait sans laisser de trace."
        )
        print("Comme si il n'y avait jamais rien eu.")
        services.Affichage.EntreePourContinuer()
        while True:
            while True:
                try:
                    print(
                        "Dans le ciel reflété par la surface de l'étang, vous pouvez voir les mots suivants :"
                    )
                    print("*L'Or Change Le Monde*")
                    print("1 - Repartir")
                    print("2 - Jetter 45 golds dans l'étang")
                    print("3 - Jetter 75 golds dans l'étang")
                    choix = int(input("Que souhaitez vous faire ? "))
                    ClearConsole()
                    if choix in [1, 2, 3]:
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print(
                    "Vous laissez l'oasis derrière vous et repartez dans l'océan de sable."
                )
                services.Affichage.EntreePourContinuer()
                break
            elif choix in [2, 3]:
                if (choix == 2 and services.Player.nombre_de_gold >= 45) or (
                    choix == 3 and services.Player.nombre_de_gold >= 75
                ):
                    print("Vous jetez vos golds dans l'étang et...")
                    if choix == 2:
                        services.Player.nombre_de_gold -= 45
                        services.Player.gold_in_well += 45
                    else:
                        services.Player.nombre_de_gold -= 75
                        services.Player.gold_in_well += 75
                    services.Affichage.EntreePourContinuer()
                    numero_de_la_pool_de_recompense = self.GetNumeroDePoolDeRecompense(
                        choix, chanceux, malchanceux
                    )
                    numero_de_la_pool_de_recompense = (
                        self.GetNouveauNumeroDePoolDeRecompense(
                            numero_de_la_pool_de_recompense
                        )
                    )
                    self.GiveRecompenseGacha(numero_de_la_pool_de_recompense)
                else:
                    print("Vous n'avez pas assez de golds !")
                    services.Affichage.EntreePourContinuer()

    def GiveRecompenseGacha(self, numero_de_pool):
        liste_de_pools_de_recompenses = [
            ["Rien"],
            [
                "Mutagène Bleu",
                "Mutagène Rouge",
                "Mutagène Vert",
            ],
            ["Mutagène Doré"],
            [
                "Grand Mutagène Bleu",
                "Grand Mutagène Rouge",
                "Grand Mutagène Vert",
            ],
            [
                "Mutagène Hérétique",
                "Mutagène Fanatique",
            ],
            [
                "Grand Mutagène Doré",
            ],
            ["Mutagène Sacré"],
            ["Gold"],
            ["Secret"],
        ]
        pool_de_recompense = liste_de_pools_de_recompenses[numero_de_pool]
        numero_aleatoire = random.randint(0, (len(pool_de_recompense) - 1))
        recompense = pool_de_recompense[numero_aleatoire]
        if recompense not in ["Rien", "Gold", "Mutagène Sacré", "Secret"]:
            services.Affichage.AfficheGacha(recompense)
            services.Player.items_possedes[recompense] += 1
        elif recompense == "Gold":
            print(
                "Vous vous avancez vers le centre de la ou se trouvait l'étang, et récuperez votre argent !"
            )
            gain_gold = services.Player.AddGoldToPlayer(services.Player.gold_in_well, True) 
            print(f"Vous regagnez {services.Player.gold_in_well} golds !")
            services.Player.gold_in_well = 0
            services.Affichage.EntreePourContinuer()
        elif recompense == "Mutagène Sacré":
            print(
                "C'est un Mutagène Sacré !\nExtremement rare, ce mutagène permet d'augmenter de manière permanente la vie et le mana !"
            )
            services.Affichage.EntreePourContinuer()
            gain_pv = round(services.Player.points_de_vie_max * 0.25)
            services.Player.points_de_vie_max += gain_pv
            services.Player.points_de_vie += gain_pv
            gain_pm = round(services.Player.points_de_mana_max * 0.25)
            services.Player.points_de_mana_max += gain_pm
            services.Player.points_de_mana += gain_pm
            print(
                f"Vous vous l'injectez immédiatement et gagnez {gain_pv} pv et {gain_pm} pm !"
            )
            services.Affichage.EntreePourContinuer()
        elif recompense == "Secret":
            self.AfficheEtangSecret()

    def GetNouveauNumeroDePoolDeRecompense(self, numero_de_pool):
        while True:
            while True:
                try:
                    if numero_de_pool == 1:
                        raretee_avant = "Commun"
                        raretee_apres = "Rare"
                        cout_de_laugmentation = "30 golds"
                    elif numero_de_pool == 2:
                        raretee_avant = "Rare"
                        raretee_apres = "Epique"
                        cout_de_laugmentation = "10 pm et 30 golds"
                    elif numero_de_pool == 3:
                        raretee_avant = "Epique"
                        raretee_apres = "Incarnat"
                        cout_de_laugmentation = "10 pv et 10 pm et 30 golds"
                    elif numero_de_pool == 4:
                        raretee_avant = "Incarnat"
                        raretee_apres = "Légendaire"
                        cout_de_laugmentation = "20 pv et 20 pm et 40 golds"
                    elif numero_de_pool == 5:
                        raretee_avant = "Légendaire"
                        raretee_apres = "Mythique"
                        cout_de_laugmentation = "25 pv et 25 pm et 50 golds"
                    elif numero_de_pool == 6:
                        raretee_avant = "Mythique"
                        raretee_apres = "???"
                        cout_de_laugmentation = "30 pv et 30 pm et 60 golds"
                    elif numero_de_pool in [0, 7, 8]:
                        break
                    print(
                        "Vous sentez que vous pouvez augmenter la raretée du mutagène avant de l'examiner."
                    )
                    print(
                        f"Raretée actuelle : {raretee_avant}. Raretée après augmentation : {raretee_apres}"
                    )
                    print(f"Prix : {cout_de_laugmentation}")
                    print("1 - Examiner le Mutagène")
                    print("2 - Faire l'Augmentation")
                    choix = int(input("Que souhaitez vous faire ? "))
                    ClearConsole()
                    if choix in [1, 2]:
                        break
                except ValueError:
                    ClearConsole()
            if numero_de_pool in [0, 7, 8]:
                return numero_de_pool
            elif choix == 1:
                print("Vous observez de plus près le mutagène.")
                services.Affichage.EntreePourContinuer()
                return numero_de_pool
            elif choix == 2:
                # regarde si c'est possible
                augmentation_possible = False
                if numero_de_pool == 1 and services.Player.nombre_de_gold >= 30:
                    augmentation_possible = True
                    services.Player.nombre_de_gold -= 30
                    services.Player.gold_in_well += 30
                    numero_de_pool = 2
                elif (
                    numero_de_pool == 2
                    and services.Player.nombre_de_gold >= 30
                    and services.Player.points_de_mana >= 10
                ):
                    augmentation_possible = True
                    services.Player.nombre_de_gold -= 30
                    services.Player.gold_in_well += 30
                    services.Player.points_de_mana -= 10
                    numero_de_pool = 3
                elif (
                    numero_de_pool == 3
                    and services.Player.nombre_de_gold >= 30
                    and services.Player.points_de_mana >= 10
                    and services.Player.points_de_vie >= 10
                ):
                    augmentation_possible = True
                    services.Player.nombre_de_gold -= 30
                    services.Player.gold_in_well += 30
                    services.Player.points_de_mana -= 10
                    services.Player.points_de_vie -= 10
                    numero_de_pool = 4
                elif (
                    numero_de_pool == 4
                    and services.Player.nombre_de_gold >= 40
                    and services.Player.points_de_mana >= 20
                    and services.Player.points_de_vie >= 20
                ):
                    augmentation_possible = True
                    services.Player.nombre_de_gold -= 40
                    services.Player.gold_in_well += 40
                    services.Player.points_de_mana -= 20
                    services.Player.points_de_vie -= 20
                    numero_de_pool = 5
                elif (
                    numero_de_pool == 5
                    and services.Player.nombre_de_gold >= 50
                    and services.Player.points_de_mana >= 25
                    and services.Player.points_de_vie >= 25
                ):
                    augmentation_possible = True
                    services.Player.nombre_de_gold -= 50
                    services.Player.gold_in_well += 50
                    services.Player.points_de_mana -= 25
                    services.Player.points_de_vie -= 25
                    numero_de_pool = 6
                elif (
                    numero_de_pool == 6
                    and services.Player.nombre_de_gold >= 60
                    and services.Player.points_de_mana >= 30
                    and services.Player.points_de_vie >= 30
                ):
                    augmentation_possible = True
                    services.Player.nombre_de_gold -= 60
                    services.Player.gold_in_well += 60
                    services.Player.points_de_mana -= 30
                    services.Player.points_de_vie -= 30
                    numero_de_pool = 8
                if not augmentation_possible:
                    print("Impossible.")
                    services.Affichage.EntreePourContinuer()
                else:
                    if numero_de_pool == 8:
                        print("Vous approchez votre main de l'étang insaisissable...")
                        print("Mais rien ne se passe.")
                        print("Vous sentez votre force vous quitter...")
                        print(
                            "Vous voyez le ciel changer de couleur plusieurs fois, et la course du soleil s'accélerer."
                        )
                        print(
                            "Vous regardez, impuissant, le mutagène dans votre main devenir poussière."
                        )
                        print("Et soudainement, tout s'arrête.")
                        services.Affichage.EntreePourContinuer()
                        print(
                            "Vous jettez un coup d'oeil a l'étang, et vous rendez compte que..."
                        )
                        services.Affichage.EntreePourContinuer()
                    else:
                        print(
                            "Vous approchez votre main de l'étang insaisissable, et un tentacule d'eau s'y accroche."
                        )
                        print(
                            "Ce dernier serpente sur votre peau jusqu'à arriver au niveau du mutagène, qui se met alors a vibrer."
                        )
                        print(
                            "Après ceci, le tentacule repart d'ou il vient, en emportant son dû avec lui."
                        )
                        services.Affichage.EntreePourContinuer()

    def GetNumeroDePoolDeRecompense(self, choix, chanceux, malchanceux):
        # initialisation de la liste de probabilitée
        if choix == 2:
            if chanceux:
                liste_de_probabilite = [
                    0,
                    7,
                    8,
                    29,
                    30,
                    46,
                    47,
                    61,
                    62,
                    78,
                    79,
                    87,
                    88,
                    89,
                    90,
                    95,
                    96,
                    100,
                ]
            elif malchanceux:
                liste_de_probabilite = [
                    0,
                    30,
                    31,
                    51,
                    52,
                    62,
                    63,
                    73,
                    74,
                    94,
                    95,
                    97,
                    98,
                    98,
                    99,
                    99,
                    100,
                    100,
                ]
            else:
                # liste_de_probabilite = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100]
                liste_de_probabilite = [
                    0,
                    10,
                    11,
                    35,
                    36,
                    55,
                    56,
                    73,
                    74,
                    84,
                    85,
                    90,
                    91,
                    94,
                    96,
                    99,
                    100,
                    100,
                ]
        elif choix == 3:
            if chanceux:
                liste_de_probabilite = [
                    0,
                    0,
                    1,
                    5,
                    6,
                    20,
                    21,
                    45,
                    46,
                    70,
                    71,
                    85,
                    86,
                    88,
                    89,
                    95,
                    96,
                    100,
                ]
            elif malchanceux:
                liste_de_probabilite = [
                    0,
                    30,
                    31,
                    51,
                    52,
                    62,
                    63,
                    73,
                    74,
                    94,
                    95,
                    97,
                    98,
                    98,
                    99,
                    99,
                    100,
                    100,
                ]
            else:
                liste_de_probabilite = [
                    0,
                    5,
                    6,
                    25,
                    26,
                    40,
                    41,
                    63,
                    64,
                    79,
                    80,
                    87,
                    88,
                    90,
                    91,
                    97,
                    98,
                    100,
                ]
        # differents tyes de recompense selon le nombre aleatoire et la liste de probabilité
        nombre_aleatoire = random.randint(0, 100)
        if liste_de_probabilite[0] <= nombre_aleatoire <= liste_de_probabilite[1]:  # 0
            print(
                "...les regardez couler jusqu'à ce que vous ne les voyez plus."
            )  # rien ne se passe
            print("Dur.")
            numero_de_la_pool_de_recompense = 0
        elif (
            liste_de_probabilite[2] <= nombre_aleatoire <= liste_de_probabilite[3]
        ):  # 5
            print(
                "...quelque chose sort de l'étang et vient violemment heurter votre torse !"
            )  # mutagene bleu ou rouge ou vert
            print("C'est un mutagène commun !")
            numero_de_la_pool_de_recompense = 1
        elif (
            liste_de_probabilite[4] <= nombre_aleatoire <= liste_de_probabilite[5]
        ):  # 15
            print("...une noix de coco vous tombe sur la tête.")
            print("C'est un mutagène rare !")  # mutagene dore
            numero_de_la_pool_de_recompense = 2
        elif (
            liste_de_probabilite[6] <= nombre_aleatoire <= liste_de_probabilite[7]
        ):  # 25
            print(
                "...une main boueuse sort des flots ."
            )  # grand mutagene bleu ou rouge ou vert
            print("Elle vous tend un mutagène épique !")
            numero_de_la_pool_de_recompense = 3
        elif (
            liste_de_probabilite[8] <= nombre_aleatoire <= liste_de_probabilite[9]
        ):  # 25
            print(
                "...une boule de chair et de sang vient s'échouer sur la rive."
            )  # mutagene fanatique ou heretique
            print("A l'interieur se trouve un mutagène incarnat !")
            numero_de_la_pool_de_recompense = 4
        elif (
            liste_de_probabilite[10] <= nombre_aleatoire <= liste_de_probabilite[11]
        ):  # 15
            print(
                "...un coquillage a l'aura dorée sort de terre et s'ouvre devant vous !"
            )  # grand mutagene dore
            print("A l'interieur se trouve un mutagène légendaire !")
            numero_de_la_pool_de_recompense = 5
        elif (
            liste_de_probabilite[14] <= nombre_aleatoire <= liste_de_probabilite[15]
        ):  # 7
            print(
                "...l'endroit tout entier se met a scintiller !"
            )  # mutagene permanent (+5 viemax +5 manamax)
            print("Un mutagène mythique apparait dans la paume de votre main !")
            numero_de_la_pool_de_recompense = 6
        elif (
            liste_de_probabilite[12] <= nombre_aleatoire <= liste_de_probabilite[13]
        ):  # 3
            print("...l'étang...disparait.")  # reprend tout le fric dépensé
            print("A sa place se trouve tout les golds que vous avez dépensés !")
            numero_de_la_pool_de_recompense = 7
        elif (
            liste_de_probabilite[16] <= nombre_aleatoire <= liste_de_probabilite[17]
        ):  # 5
            numero_de_la_pool_de_recompense = 8
            return numero_de_la_pool_de_recompense
        services.Affichage.EntreePourContinuer()
        return numero_de_la_pool_de_recompense

    def AfficheEtangSecret(self):
        StopAllMusic()
        print("...l'eau se fait drainer.")  # truc secret
        print("Vous apercevez alors un escalier maintenant émergé, que vous descendez.")
        services.Affichage.EntreePourContinuer()
        print(
            "Au bout de quelques mètres, la lumière se raréfie. Vous descendez prudemment chaque marches de pierre..."
        )
        services.Affichage.EntreePourContinuer()
        print("...gluantes...")
        services.Affichage.EntreePourContinuer()
        print("...glissantes...")
        services.Affichage.EntreePourContinuer()
        print("...interminables...")
        services.Affichage.EntreePourContinuer()
        print("...")
        services.Affichage.EntreePourContinuer()
        print(". . .")
        services.Affichage.EntreePourContinuer()
        print(".   .   .")
        services.Affichage.EntreePourContinuer()
        print(".        .       .")
        services.Affichage.EntreePourContinuer()
        print("et quelque chose vous pousse.")
        PlayMusic("abyss")
        services.Affichage.EntreePourContinuer()
        print("Vous sentez une pression là ou la  c h o s e  vous a touchée.")
        services.Affichage.EntreePourContinuer()
        print("Vous sentez l'odeur iodée de la   m e r.")
        services.Affichage.EntreePourContinuer()
        print("Vous sentez l'odeur métallique du   s  a  n  g.")
        services.Affichage.EntreePourContinuer()
        print(
            "Vous entendez les sons crispants de la   c  h  a  i  r   qui se déchire."
        )
        services.Affichage.EntreePourContinuer()
        print("Avez vous touché le fond ? Vous êtes vous écrasé sur le sol ?")
        services.Affichage.EntreePourContinuer()
        print(". . .  Y - a - t  i l  s e u l e m e n t  u n  f o n d  . . . ")
        services.Affichage.EntreePourContinuer()
        print(
            "Le bruissement de vos vêtements et le vent froid qui les plaquent contre votre peau humide vous ramène a la raison."
        )
        services.Affichage.EntreePourContinuer()
        print("Vous êtes entrain de tomber.")
        services.Affichage.EntreePourContinuer()
        for _ in range(0, 10):
            print("Et la chute est interminable.")
            time.sleep(2.5)
        ClearConsole()
        print("ET")
        services.Affichage.AfficheAvecUnTempsDattente(1)
        print("LA")
        services.Affichage.AfficheAvecUnTempsDattente(1)
        print("CHUTE")
        services.Affichage.AfficheAvecUnTempsDattente(1)
        print("EST")
        services.Affichage.AfficheAvecUnTempsDattente(1)
        print("INTERMINABLE")
        services.Affichage.AfficheAvecUnTempsDattente(1)
        print(
            "E  T     L  A     C  H  U  T  E     E  S  T     I  N  T  E  R  M  I  N  A  B  L  E"
        )
        services.Affichage.AfficheAvecUnTempsDattente(5)
        print("I N T E R M I N A B L E")
        services.Affichage.AfficheAvecUnTempsDattente(2)
        print("INTERMINABLE")
        services.Affichage.AfficheAvecUnTempsDattente(2)
        print("interminable")
        services.Affichage.AfficheAvecUnTempsDattente(2)
        print(" ._.__._..")
        services.Affichage.AfficheAvecUnTempsDattente(1)
        print("  .___.")
        services.Affichage.AfficheAvecUnTempsDattente(1)
        print("   ._.")
        services.Affichage.AfficheAvecUnTempsDattente(1)
        print("    .")
        services.Affichage.AfficheAvecUnTempsDattente(1)
        print("")
        services.Affichage.AfficheAvecUnTempsDattente(3)
        print("jjjejejeeeejeje")
        services.Affichage.AfficheAvecUnTempsDattente(1)
        print("JEJEJEJEJEJEJEJE")
        services.Affichage.AfficheAvecUnTempsDattente(1)
        print("JEEEEEEEEeeeeEEeeeEe")
        services.Affichage.AfficheAvecUnTempsDattente(1)
        print("JEEEEEEEEEEEEEEEEEEEE Te")
        services.Affichage.AfficheAvecUnTempsDattente(1)
        print("J'ai fait un rêve.")
        services.Affichage.AfficheAvecUnTempsDattente(5)
        print("Dedans, je jouais au coliseum.")
        services.Affichage.AfficheAvecUnTempsDattente(3)
        print("Une soirée banale, quoi.")
        services.Affichage.AfficheAvecUnTempsDattente(3)
        print("Et puis a un moment, j'ai vu de la couleur, des images.")
        services.Affichage.AfficheAvecUnTempsDattente(5)
        print("Des images perturbantes. C'est un jeu textuel après tout.")
        services.Affichage.AfficheAvecUnTempsDattente(5)
        print("Il n'est pas sensé y en avoir.")
        services.Affichage.AfficheAvecUnTempsDattente(3)
        print("Et puis j'ai vu un sourire.")
        services.Affichage.AfficheAvecUnTempsDattente(3)
        print("Il était...cruel.\nFroid.")
        services.Affichage.AfficheAvecUnTempsDattente(3)
        print("Tout droit sorti d'un documentaire animalier, ou d'une série policière.")
        services.Affichage.AfficheAvecUnTempsDattente(5)
        print("Le moment ou le suspect fait comprendre qu'il joue avec les agents...")
        services.Affichage.AfficheAvecUnTempsDattente(5)
        print("Le moment ou la lionne voit sa rivale exilée...")
        services.Affichage.AfficheAvecUnTempsDattente(5)
        print("...un sourire pervers.")
        services.Affichage.AfficheAvecUnTempsDattente(5)
        print("...un sourire qui ne respecte pas la vie.")
        services.Affichage.AfficheAvecUnTempsDattente(4)
        print("...un sourire qui ne tient rien pour sacré.")
        services.Affichage.AfficheAvecUnTempsDattente(4)
        print("...un sourire...")
        services.Affichage.AfficheAvecUnTempsDattente(3)
        print("...sadique.")
        services.Affichage.AfficheAvecUnTempsDattente(2)
        print(
            "Et puis je l'ai vu ouvrir sa bouche en grand, comme pour manger quelque chose."
        )
        services.Affichage.AfficheAvecUnTempsDattente(4)
        print("Ce soir la, je crois que...")
        services.Affichage.AfficheAvecUnTempsDattente(3)
        print("...j'ai perdu quelque chose.")
        services.Affichage.AfficheAvecUnTempsDattente(2)
        print("Quelque chose de vital.")
        services.Affichage.AfficheAvecUnTempsDattente(2)
        print("D'essentiel.")
        services.Affichage.AfficheAvecUnTempsDattente(2)
        print("Des souvenirs, des sentiments, un bout de mon âme peut être ?")
        services.Affichage.AfficheAvecUnTempsDattente(3)
        print("J'ai perdu quelque chose de vital.")
        services.Affichage.AfficheAvecUnTempsDattente(2)
        print("Mais j'ai gagné une obsession.")
        services.Affichage.AfficheAvecUnTempsDattente(2)
        print(
            "Quand je me suis réveillé, on aurait dit que mon lit était devenu un étang."
        )
        services.Affichage.AfficheAvecUnTempsDattente(5)
        print(
            "Dans cette flaque de transpiration, noire comme les ténèbres d'un abysse sans fond,"
        )
        services.Affichage.AfficheAvecUnTempsDattente(5)
        print("J'y ai vu le reflet d'un mal qui m'a aggripé le bras.")
        services.Affichage.AfficheAvecUnTempsDattente(4)
        print("Un mal fait de uns, de zéros, de zéros et de uns...")
        services.Affichage.AfficheAvecUnTempsDattente(12)
        print("...et de uns et de zéros...")
        services.Affichage.AfficheAvecUnTempsDattente(12)
        print("Quelque chose de digital, en tout point inoffensif.")
        services.Affichage.AfficheAvecUnTempsDattente(3)
        print("Je crois.")
        services.Affichage.AfficheAvecUnTempsDattente(4)
        print("...")
        services.Affichage.AfficheAvecUnTempsDattente(5)
        print("Il faut que je prenne plus de notes.")
        services.Affichage.AfficheAvecUnTempsDattente(5)
        StopAllMusic()
        print(
            "Vous sentez une douleur aigue a la poitrine, et rouvrez les yeux devant l'étang."
        )
        services.Affichage.EntreePourContinuer()
        print("L'eau y est maintenant noire.")
        services.Affichage.EntreePourContinuer()
        services.Sove.RajouteEntreeAuLivreCigogneBlancheSiOnAPas("???", "INTERMINABLE")
        PlayMusicDeLetage()
        print("...")

    def DoTheFountain(self):
        if services.Player.fountain_used:
            print(
                "Au détour d'une haie de roses blanches, vous découvrez une magnifique fontaine de marbre."
            )
            print(
                "Des anges sont gravés dans la pierre, ainsi qu'un griffon avec la gueule grande ouverte."
            )
            print(
                "Au centre, sur un petit piedestal se trouve une inscription particulière que vous n'aviez pas vu avant :"
            )
            services.Affichage.EntreePourContinuer()
            print(
                "*A ceux qui ont besoin de moi, je donne une chance de prouver leur valeur.*"
            )
            print(
                "*A ceux qui ont déjà prouvé leur valeur sans mon aide, j'offre la vigueur du griffon.*"
            )
            print("*Et a ceux qui cherchent plus loin que l'honneur ou la force...*")
            print(
                "*...laissez donc mourir votre âme et votre corps, et venez à ma rencontre.*"
            )
            services.Affichage.EntreePourContinuer()
            print("Vous laissez la fontaine vide et retournez sur vos pas.")
            services.Affichage.EntreePourContinuer()
        elif services.Player.points_de_vie <= 10 and services.Player.points_de_mana <= 5:
            StopAllMusic()
            print(
                "Au détour d'une haie de roses blanches, vous découvrez une magnifique fontaine de marbre...?"
            )
            print("Ce qui semblait être du marbre prend une teinte pâle, puis verte.")
            services.Affichage.EntreePourContinuer()
            print("Vous vous approchez prudemment de la fontaine(?).")
            services.Affichage.EntreePourContinuer()
            numero_du_commentaire = 0
            commentaire = (
                "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                "\nAu centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve un petit morceau de sucre."
            )
            while True:
                while True:
                    try:
                        print(commentaire)
                        if numero_du_commentaire == 11:
                            print("1 - Repartir")
                            print("2 - Boire l'eau(?) de la fontaine")
                            print("3 - Attendre.")
                            print("666 - T r a n c h e r  l a  c h o s e")
                        elif numero_du_commentaire == 12:
                            print("2 - B   O   I   R   E")
                        else:
                            print("1 - Repartir")
                            print("2 - Boire l'eau(?) de la fontaine")
                            print("3 - Attendre.")
                        choix = int(input("Que souhaitez vous faire ? "))
                        ClearConsole()
                        if (
                            (
                                (numero_du_commentaire in range(0, 11))
                                and (choix in [1, 2, 3])
                            )
                            or (
                                (numero_du_commentaire == 11)
                                and (choix in [1, 2, 3, 666])
                            )
                            or ((numero_du_commentaire == 12) and (choix == 2))
                        ):
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 1:
                    print(
                        "Vous laissez...ça...derrière vous et repartez d'ou vous venez en courant."
                    )
                    services.Affichage.EntreePourContinuer()
                    PlayMusicDeLetage()
                    break
                elif choix == 666:
                    print(
                        "Vous sortez une arme, n'importe laquelle, et sentez votre énergie s'épuiser."
                    )
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print(
                        "Mu par l'énergie du désespoir, les yeux pleins de larmes et de terreur, vous frappez un des yeux gluant de la  c  h  o  s  e !"
                    )
                    services.Affichage.AfficheAvecUnTempsDattente(5)
                    print(
                        "Un hurlement sanguin se fait entendre dans tout l'étage, et les haies de roses blanches se rapprochent de vous !"
                    )
                    services.Affichage.AfficheAvecUnTempsDattente(5)
                    print(
                        "Vous tentez de frapper une nouvelle fois, mais vous sentez une résistance au niveau du fourreau de votre arme.."
                    )
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Les tentacules se sont enroulés autour de vos pieds !")
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print(
                        "Les haies de roses blanches se rapprochent encore, et le son devient guttural,"
                    )
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print("Comme si la c h o s e était entrain de se réjouir...")
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print(
                        "Vous sentez la peur briser les murs de votre esprit, et les roses blanches entourer votre corps frêle..."
                    )
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("...pâle...")
                    services.Affichage.AfficheAvecUnTempsDattente(2)
                    print("...faible...")
                    services.Affichage.AfficheAvecUnTempsDattente(2)
                    print(
                        "...pile poil assez faible pour se faire a b s o r b e r sans poser de résistance..."
                    )
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print(
                        "...et les roses poussant leurs racines a travers votre peau !"
                    )
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print(
                        "Vous les sentez s'insinuer dans vos pores, prendre place dans vos organes..."
                    )
                    services.Affichage.AfficheAvecUnTempsDattente(3.5)
                    print(
                        "VOus senteEz Leees TTENTAculEs se MOUVOIR MOUVOIR souS vOtRe Peauuu"
                    )
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print(
                        "Vooouuss VOUS DEbattEZZ cONTre L'enVAhiissEEEEur BIolooogiquee..."
                    )
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print(
                        "Crieezezz a pleeien pouuopooumon, AppellezzZ DESESPEREMETN le MArchand, OUUOU le BOSsssss..."
                    )
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("EN VAIN EN VAIN EN VAIN EN VAIN EN VAIN Eeeeenenn VAaain")
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print(
                        "VoUs SeNtEz LeS rAcInEs BoUgEr AuToUr De VoS gLoBeS oCcUlAiReS..."
                    )
                    services.Affichage.AfficheAvecUnTempsDattente(3.5)
                    print("Vou-")
                    services.Affichage.AfficheAvecUnTempsDattente(0.1)
                    PlayMusicDeLetage()
                    print(
                        "Votre peau se met a picoter, et vous hésitez quelques secondes avant d'engloutir le liquide magique."
                    )
                    services.Affichage.EntreePourContinuer()
                    print(
                        "L'eau était fraiche ! Vous gagnez 3 points de mana max et reprenez tout vos points de mana !"
                    )
                    services.Player.points_de_mana_max += 3
                    services.Player.points_de_mana = services.Player.points_de_mana_max
                    services.Affichage.EntreePourContinuer()
                    print("L'eau s'arrête de couler, et la fée disparait dans l'éther.")
                    services.Player.fountain_used = True
                    print(
                        "Vous laissez la fontaine désormais vide et repartez sur vos pas."
                    )
                    services.Affichage.EntreePourContinuer()
                    print("...?")
                    services.Affichage.EntreePourContinuer()
                    print(
                        "Vous manquez de trébucher sur quelque chose qui sort du sol !"
                    )
                    services.Affichage.EntreePourContinuer()
                    print(
                        "On dirait une main autour de laquelle pousse une rose blanche, tenant dans sa paume un bout de papier..."
                    )
                    services.Affichage.EntreePourContinuer()
                    print("Vous lisez le bout de papier a voix haute :")
                    services.Affichage.EntreePourContinuer()
                    print(
                        "*Nb talent disponible colle pas avec menu redcoin ==) nombre de lignes menu redcoin [LE MEME] alors que plus talent. ==) signification particuliere ?*"
                        "\n*nb ligne redcoin ==) Action??(le mot est barré) ==)Menu??(le mot est barré) ==)Ipv4??(le mot est entouré)*"
                    )
                    services.Affichage.EntreePourContinuer()
                    print(
                        "Vous jetez le bout de papier insensé par terre et regardez quelques instants la main."
                    )
                    services.Affichage.EntreePourContinuer()
                    print(
                        "Pour une raison qui vous échappe, vous ressentez un frisson en la regardant."
                    )
                    services.Affichage.EntreePourContinuer()
                    print(
                        "Le gant qui l'habille ne ressemble-t-il pas au votre aussi ?"
                    )
                    services.Affichage.EntreePourContinuer()
                    print("...")
                    services.Affichage.EntreePourContinuer()
                    print(". . .")
                    services.Affichage.EntreePourContinuer()
                    print(".     .     .")
                    services.Affichage.EntreePourContinuer()
                    print(".               .                   .")
                    services.Affichage.EntreePourContinuer()
                    print("Meh. Peut etre pas.")
                    services.Affichage.EntreePourContinuer()
                    services.Sove.RajouteEntreeAuLivreCigogneBlancheSiOnAPas("???", "MORS/ACERBIOR/EST/CUM/IN/NEGATIONE/ADHAESISTI/SICUT/MUSCAE/IN/CARNIVOR/PLANTAE/")
                    break
                elif choix == 3:
                    numero_du_commentaire += 1
                    if numero_du_commentaire == 1:
                        commentaire = (
                            "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                            "\nAu centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve un petit morceau de sucre."
                            "\nIl y a du mouvement dans un buisson proche de vous."
                        )
                    elif numero_du_commentaire == 2:
                        commentaire = (
                            "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                            "\nAu centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve un petit morceau de sucre."
                            "\nUne fée sort du buisson et s'approche du piédestal."
                        )
                    elif numero_du_commentaire == 3:
                        commentaire = (
                            "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                            "\nAu centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve un petit morceau de sucre."
                            "\nLa fée se pose sur le morceau de sucre et commence a le grignoter"
                        )
                    elif numero_du_commentaire == 4:
                        PlayMusic("abyss")
                        commentaire = (
                            "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                            "\nSoudainement, des tentacules sortent des côtés du piedestal et entourent la fée."
                        )
                    elif numero_du_commentaire == 5:
                        commentaire = (
                            "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                            "\nLa fée se débat, et les tentacules se resserent autour de son petit corps."
                        )
                    elif numero_du_commentaire == 6:
                        commentaire = (
                            "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                            "\nLes tentacules verts se font alors de plus en plus fins , et continuent d'entourer la fée dans un cocon serré."
                        )
                    elif numero_du_commentaire == 7:
                        commentaire = (
                            "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                            "\nAu centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve une fée qui a l'air d'être en état de biostase,"
                            "\nmais un examen plus approfondi révèle un cocon de fil la maintenant immobile a quelques centimètre du piédestal."
                        )
                    elif numero_du_commentaire == 8:
                        commentaire = (
                            "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                            "\nAu centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve une fée piégée."
                            "\nVous apercevez les tentacules autour d'elle vibrer, et pomper quelque chose."
                        )
                    elif numero_du_commentaire == 9:
                        commentaire = (
                            "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                            "\nAu centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve une fée piégée."
                            "\nLe marbre(NON) reprend la couleur du marbre, la fontaine reprend une apparence de fontaine."
                        )
                    elif numero_du_commentaire == 10:
                        commentaire = (
                            "Des anges sont gravés dans la pierre(FUIS), et d'une tête de griffon se met à jaillir une eau(NON) cristalline."
                            "\nAu centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve une fée en état de biostase(FAUX)."
                        )
                    elif numero_du_commentaire == 11:
                        commentaire = "Des yeux s'ouvrent au niveau de l'abdomen des anges taillés.\nIl vous fixe."
                    else:
                        commentaire = "La c h o s e regarde dans votre âme, et vous sentez votre énergie s'épuiser.\nVos décisions ne vous appartiennent plus.\nC'est trop tard."
                elif choix == 2:
                    numero = 0
                    print("Vous vous accroupissez et plongez les mains dans l'eau...")
                    print("...?")
                    services.Affichage.EntreePourContinuer()
                    print(
                        "Ce qui semblait être de l'eau est en faite une sorte de gelée collante, et vos mains sont prises dedans !"
                    )
                    services.Affichage.EntreePourContinuer()
                    commentaire = (
                        "Appuyez sur Entree pour tenter de vous sortir de là !!!"
                    )
                    while True:
                        input(commentaire)
                        ClearConsole()
                        if numero in range(0, 16):
                            commentaire = (
                                "Appuyez sur Entree pour tenter de vous sortir de là !!"
                            )
                            numero += 1
                        elif numero in range(16, 31):
                            commentaire = (
                                "Appuyez sur Entree pour tenter de vous sortir de là !"
                            )
                            numero += 1
                        elif numero in range(31, 46):
                            commentaire = (
                                "Appuyez sur Entree pour tenter de vous sortir de là..."
                            )
                            numero += 1
                        elif numero in range(46, 61):
                            commentaire = (
                                "Appuyez sur Entree pour tenter de vous sortir..."
                            )
                            numero += 1
                        elif numero in range(61, 76):
                            commentaire = "Appuyez sur Entree pour tenter..."
                            numero += 1
                        elif numero in range(76, 91):
                            commentaire = "Appuyez sur Entree pour..."
                            numero += 1
                        elif numero in range(91, 106):
                            commentaire = "..."
                            numero += 1
                        elif numero in range(106, 151):
                            commentaire = (
                                "C'est trop tard.\nVous êtes surement déja mort."
                            )
                            numero += 1
                        else:
                            commentaire = ""
                            for _ in range(1, 100):
                                commentaire += "MORS/ACERBIOR/EST/CUM/IN/NEGATIONE/ADHAESISTI/SICUT/MUSCAE/IN/CARNIVOR/PLANTAE/"
        elif services.Player.boss_battu and (services.Player.nombre_dennemis_a_letage == 0):
            while True:
                try:
                    print(
                        "Au détour d'une haie de roses blanches, vous découvrez une magnifique fontaine de marbre."
                    )
                    print(
                        "Des anges sont gravés dans la pierre, et d'une tête de griffon jaillit une eau rose bonbon."
                    )
                    print(
                        "Au centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve un petit corps en décomposition."
                    )
                    print("1 - Ne rien faire")
                    print("2 - Boire l'eau(?) de la fontaine")
                    choix = int(input("Que souhaitez vous faire ? "))
                    ClearConsole()
                    if choix in [1, 2]:
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print("Vous laissez la fontaine et repartez sur vos pas.")
                services.Affichage.EntreePourContinuer()
            else:
                print(
                    "Vous mettez vos mains en cul-de-poule et les remplissez avec l'eau de la fontaine."
                )
                print(
                    "Une vague et délicieuse odeur d'aromates, de liqueur de cèdre, de poudre de santal, de myrrhe et de cinnamome se répend dans la paume de vos mains."
                )
                print(
                    "Votre peau se met a bruler, et vous hésitez quelques secondes avant d'engloutir le liquide visqueux."
                )
                services.Affichage.EntreePourContinuer()
                print(
                    "L'eau avait un gout de violette ! Vous gagnez 15 points de mana/vie max et reprenez tout vos points de mana/vie !"
                )
                services.Player.points_de_mana_max += 15
                services.Player.points_de_mana = services.Player.points_de_mana_max
                services.Player.points_de_vie_max += 15
                services.Player.points_de_vie = services.Player.points_de_vie_max
                services.Affichage.EntreePourContinuer()
                print("L'eau s'arrête de couler, et le cadavre disparait dans l'éther.")
                services.Player.fountain_used = True
                print(
                    "Vous laissez la fontaine désormais vide et repartez sur vos pas."
                )
                services.Affichage.EntreePourContinuer()
        else:
            while True:
                try:
                    print(
                        "Au détour d'une haie de roses blanches, vous découvrez une magnifique fontaine de marbre."
                    )
                    print(
                        "Des anges sont gravés dans la pierre, et d'une tête de griffon jaillit une eau cristalline."
                    )
                    print(
                        "Au centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve une fée en état de biostase."
                    )
                    print("1 - Ne rien faire")
                    print("2 - Boire l'eau de la fontaine")
                    print("3 - Attraper la fée dans un bocal")
                    choix = int(input("Que souhaitez vous faire ? "))
                    ClearConsole()
                    if choix in [1, 2, 3]:
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print("Vous laissez la fontaine et repartez sur vos pas.")
                services.Affichage.EntreePourContinuer()
            elif choix == 2:
                print(
                    "Vous mettez vos mains en cul-de-poule et les remplissez avec l'eau de la fontaine."
                )
                print(
                    "Votre peau se met a picoter, et vous hésitez quelques secondes avant d'engloutir le liquide magique."
                )
                services.Affichage.EntreePourContinuer()
                nombre_aleatoire = random.randint(1, 2)
                if nombre_aleatoire == 1:
                    print(
                        "L'eau était fraiche ! Vous gagnez 3 points de mana max et reprenez tout vos points de mana !"
                    )
                    services.Player.points_de_mana_max += 3
                    services.Player.points_de_mana = services.Player.points_de_mana_max
                else:
                    print(
                        "L'eau était chaude ! Vous gagnez 3 points de vie max et reprenez tout vos points de vie !"
                    )
                    services.Player.points_de_vie_max += 3
                    services.Player.points_de_vie = services.Player.points_de_vie_max
                services.Affichage.EntreePourContinuer()
                print("L'eau s'arrête de couler, et la fée disparait dans l'éther.")
                services.Player.fountain_used = True
                print(
                    "Vous laissez la fontaine désormais vide et repartez sur vos pas."
                )
                services.Affichage.EntreePourContinuer()
            elif choix == 3:
                print(
                    "Vous vous approchez de la fée et la mettez dans votre flacon d'un coup rapide."
                )
                print("Vous obtenez une Fée dans un Bocal !")
                services.Affichage.EntreePourContinuer()
                if services.Player.possede_une_fee:
                    PlaySound("death")
                    print(
                        "Alors que vous rangiez votre bocal dans votre sacoche,"
                        " vous voyez les deux fées unir leur pouvoir a travers"
                        " les bocaux pour briser leur cage de verre et s'enfuir."
                    )
                    services.Player.possede_une_fee = False
                    services.Affichage.EntreePourContinuer()
                    PlaySound("death")
                    print("Et l'eau s'arrête de couler.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous avez...tout perdu.")
                    print("Votre fée, la fée de la fontaine, et l'eau de la fontaine.")
                    services.Affichage.EntreePourContinuer()
                    print(
                        "A ce point la, ca ne serait même pas étonnant que les fees se sont échappées avec tout votre gold !"
                    )
                    services.Affichage.EntreePourContinuer()
                    PlaySound("death")
                    print("Parce que c'est le cas.")
                    print("Vous n'avez plus un gold a votre nom.")
                    services.Player.nombre_de_gold = 0
                    services.Affichage.EntreePourContinuer()
                    print(
                        "Vous laissez la fontaine désormais vide et repartez sur vos pas, une expression traumatisée et misérable désormais accrochée a votre visage."
                    )
                    services.Affichage.EntreePourContinuer()
                    PlaySound("death")
                    print(
                        "Qui vous empeche de voir une branche a votre hauteur, que vous vous prenez en pleine poire."
                    )
                    services.Affichage.EntreePourContinuer()
                    degat = services.Player.points_de_vie - 1
                    services.Player.points_de_vie = 1
                    PlaySound("death")
                    print(f"Vous perdez {degat} points de vie.")
                    services.Affichage.EntreePourContinuer()
                    PlaySound("death")
                    print("Le choc vous fait craquer.")
                    print(
                        "Vous vous mettez en position fétale et pleurez toute les larmes de votre corps."
                    )
                    services.Affichage.EntreePourContinuer()
                    print(
                        "Votre crise de nerf vous touche au plus profond de votre âme."
                    )
                    services.Affichage.EntreePourContinuer()
                    degat = services.Player.points_de_mana - 1
                    services.Player.points_de_mana = 1
                    PlaySound("death")
                    print(f"Vous perdez {degat} points de mana.")
                    services.Affichage.EntreePourContinuer()
                    print("J'espère que vous avez fait une sauvegarde...")
                    services.Affichage.EntreePourContinuer()
                    print("...")
                    services.Affichage.EntreePourContinuer()
                    print("...sinon, voila un peu de musique pour vous réconforter.")
                    services.Affichage.EntreePourContinuer()
                    PlayMusic("reconfort")
                else:
                    services.Player.possede_une_fee = True
                    print("L'eau s'arrête de couler.")
                    print(
                        "Vous laissez la fontaine désormais vide et repartez sur vos pas."
                    )
                    services.Affichage.EntreePourContinuer()

    def DoTheLibrary(self):
        # Recuperation de la liste de sorts enregistrés
        donnees_de_s0ve = self.GetPermanentThingsFromS0ve()
        liste_de_sorts_enregistres = ast.literal_eval(donnees_de_s0ve["Livre de sort"])
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire in [1, 2, 3]:
            liste_de_sorts_enregistres = [
                "jegardeleseigneurdevantmoisansrelâche;ilestàmadroite:jesuisinébranlable"
            ]
        print(
            "Derrière un rocher, vous trouvez un ancien passage quasi-effondré menant a une petite pièce étroite."
        )
        print(
            "Au milieu se tient un livre usé par le temps, dont la couverture représente une magnifique cigogne bleue regardant vers la droite."
        )
        print("Vous ouvrez le livre...")
        services.Affichage.EntreePourContinuer()
        if services.Player.library_used:
            print("...mais ce dernier est vide.")
            print("Vous le refermez et repartez ailleurs.")
            services.Affichage.EntreePourContinuer()
        else:
            if (
                "jegardeleseigneurdevantmoisansrelâche;ilestàmadroite:jesuisinébranlable"
                in liste_de_sorts_enregistres
            ):
                StopAllMusic()
            while True:
                try:
                    print(
                        "A l'interieur se trouvent plusieurs lignes écrite à l'encre noire."
                        "\nCertaines sont effacées, mais celles qui ne le sont pas semblent attirer votre main..."
                    )
                    numero_a_afficher = 1
                    for sort in liste_de_sorts_enregistres:
                        print(f"{numero_a_afficher} - Toucher les mots [{sort}]")
                        numero_a_afficher += 1
                    liste_dartefact_debloque = []
                    if not (
                        "jegardeleseigneurdevantmoisansrelâche;ilestàmadroite:jesuisinébranlable"
                        in liste_de_sorts_enregistres
                    ):
                        donnees_de_s0ve = services.Observation.GetPermanentThingsFromS0ve()
                        liste_dartefact_debloque = ast.literal_eval(donnees_de_s0ve["Artefact Debloques"])
                        for artefact in liste_dartefact_debloque:
                            print(f"{numero_a_afficher} - Toucher les mots [{artefact}]")
                            numero_a_afficher += 1
                    print(f"{numero_a_afficher} - Ne rien toucher")
                    choix = int(input("Que souhaitez vous faire ? "))
                    ClearConsole()
                    if choix in range(1, (len(liste_de_sorts_enregistres) + len(liste_dartefact_debloque) + 2)):
                        break
                except ValueError:
                    ClearConsole()
            if choix == (len(liste_de_sorts_enregistres) + len(liste_dartefact_debloque) + 1):
                print("Vous refermez le livre et vous éloignez de la pièce.")
                services.Affichage.EntreePourContinuer()
            elif (("jegardeleseigneurdevantmoisansrelâche;ilestàmadroite:jesuisinébranlable" in liste_de_sorts_enregistres)
                  and (choix == 1)
            ):
                PlayMusic("abyss")
                print("C3 n'est pas vous.")
                services.Affichage.AfficheAvecUnTempsDattente(5)
                print("Ca 6'est pas possible.")
                services.Affichage.AfficheAvecUnTempsDattente(5)
                print("Vous 2'êtes jamais passé par la...")
                services.Affichage.AfficheAvecUnTempsDattente(5)
                print(
                    "...et c9 n'est pourtant pas la premiere fois que vous venez ici."
                )
                services.Affichage.AfficheAvecUnTempsDattente(5)
                print("C'est vo5s, sans l'être.")
                services.Affichage.AfficheAvecUnTempsDattente(5)
                print("Ca n'est 1as vous, tout en l'étant.")
                services.Affichage.AfficheAvecUnTempsDattente(5)
                print("Comment es8-ce possible ?")
                services.Affichage.AfficheAvecUnTempsDattente(5)
                print("Comment est4ce possible...")
                services.Affichage.AfficheAvecUnTempsDattente(5)
                print("Comment est-7e...")
                services.Affichage.AfficheAvecUnTempsDattente(5)
                print("...")
                services.Affichage.AfficheAvecUnTempsDattente(5)
                print("...oh.")
                services.Affichage.AfficheAvecUnTempsDattente(5)
                print("je vois.")
                services.Affichage.AfficheAvecUnTempsDattente(5)
                print("C'est quelqu'un d'autre.")
                services.Affichage.AfficheAvecUnTempsDattente(5)
                print("C'est une trace.")
                services.Affichage.AfficheAvecUnTempsDattente(5)
                print("...")
                services.Affichage.AfficheAvecUnTempsDattente(5)
                print("Retrouve moi.")
                services.Affichage.AfficheAvecUnTempsDattente(5)
                print("....non.")
                services.Affichage.AfficheAvecUnTempsDattente(5)
                print("*Récupère* moi.")
                services.Affichage.AfficheAvecUnTempsDattente(3)
                services.Sove.RajouteEntreeAuLivreCigogneBlancheSiOnAPas("???", "jegardeleseigneurdevantmoisansrelâche;ilestàmadroite:jesuisinébranlable")
            else:
                services.Player.library_used = True
                if services.Player.points_de_vie > services.Player.points_de_vie_max:
                    services.Player.points_de_vie = services.Player.points_de_vie_max
                print(
                    "Alors que vos doigts effleurent les lettres, l'entieretée de l'encre sur la page se rassemble au centre et saute sur votre main."
                    "\nElle se répend le long de votre membre, s'infiltre par vos pores, et fait apparaitre sur votre bras un tatouage étrange et douloureux."
                )
                services.Affichage.EntreePourContinuer()
                print("Vous perdez 5 points de vie max !")
                services.Player.points_de_vie_max -= 5
                if services.Player.points_de_vie > services.Player.points_de_vie_max :
                    services.Player.points_de_vie = services.Player.points_de_vie_max
                services.Affichage.EntreePourContinuer()
                if choix > len(liste_de_sorts_enregistres) :
                    artefact = liste_dartefact_debloque[choix - (len(liste_de_sorts_enregistres) + 1)]
                    print(f"Un artefact se materialise dans la paume de votre main !")
                    services.Affichage.EntreePourContinuer()
                    services.FloorMaker.GiveRandomArtefact(artefact)
                else:
                    sort = liste_de_sorts_enregistres[choix - 1]
                    print(f"Vous gagnez le sort [{sort}] !")
                    services.Affichage.EntreePourContinuer()
                    services.Player.sorts_possedes.append(sort)
                    if "Syra" in services.Player.liste_dartefacts_optionels:
                        print("Grace au verre de Syra que vous avez bu, vous gagnez aussi 10 pv max !")
                        services.Player.points_de_vie += 10
                        services.Player.points_de_vie_max += 10
                        services.Affichage.EntreePourContinuer()
                print(
                    "La page est maintenant vide.\nVous refermez le livre et repartez ailleurs."
                )
                services.Affichage.EntreePourContinuer()
        if (
            "jegardeleseigneurdevantmoisansrelâche;ilestàmadroite:jesuisinébranlable"
            in liste_de_sorts_enregistres
        ):
            PlayMusicDeLetage()

    def GetPermanentThingsFromS0ve(self):
        dictionnaire_de_choses_permanentes = {}
        dir_path = DOSSIER_RESSOURCES
        # fichier de sauvegarde (permanant)
        if os.path.isfile(dir_path + "\\s1ve.txt"):
            chemin_du_fichier_save = dir_path + "\\s1ve.txt"
        else:
            chemin_du_fichier_save = dir_path + "\\s0ve.txt"

        with open(chemin_du_fichier_save, "r") as fichier:
            reader = csv.DictReader(fichier, delimiter="|")
            for line in reader:
                dictionnaire_de_choses_permanentes[line["Caracteristique"]] = line[
                    "Valeur"
                ]
        return dictionnaire_de_choses_permanentes
    


    def SetPermanentThingsToS0ve(self, dictionnaire_de_choses_permanentes):
        dir_path = DOSSIER_RESSOURCES
        if os.path.isfile(dir_path + "\\s1ve.txt"):
            chemin_du_fichier_save = dir_path + "\\s1ve.txt"
        else:
            chemin_du_fichier_save = dir_path + "\\s0ve.txt"

        with open(chemin_du_fichier_save, "w") as fichier:
            fichier.write("Caracteristique|Valeur")
            for caracteristic in dictionnaire_de_choses_permanentes:
                fichier.write(
                    f"\n{caracteristic}|{dictionnaire_de_choses_permanentes[caracteristic]}"
                )
