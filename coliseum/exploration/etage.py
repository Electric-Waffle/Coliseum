"""Carte d'un étage (donjon ou village) : génération, déplacement, observation des salles, mini-jeux."""

import ast
from pygame import mixer
import random
import threading
import time
from turtle import (
    setheading,
    setup,
    setworldcoordinates,
    speed,
    tracer,
)

from coliseum import services
from coliseum import audio
from coliseum.audio import PlayMusic, PlayMusicDeLetage, PlaySound, StopAllMusic
from coliseum.console import ClearConsole
from coliseum.donnees.artefacts import LISTEEFFETSARTEFACT
from coliseum.erreurs import WriteErrorInErrorLog
from coliseum.interface.dessin import ColiseumGoto
from coliseum.exploration.salles import reveler_la_salle
from coliseum.exploration.salles.icones import dessiner_l_icone


class Floor:

    def __init__(self):
        self.FloorBlueprint = {}
        self.DictionnaireAjout = {
            # direction : [ajout x, ajout y]
            "Haut": [0, 1],
            "Bas": [0, -1],
            "Gauche": [-1, 0],
            "Droite": [1, 0],
        }
        self.liste_sequence = []
        self.liste_des_salles_observées = []
        self.carte_ouverte = False
        self.ListeDePositionsInconstruisibles = [
            # position x position y
            [-2, -2],
            [-2, -1],
            [-2, 0],
            [-2, 1],
            [-2, 2],
            [-1, -2],
            [-1, -1],
            [-1, 0],
            [-1, 1],
            [-1, 2],
            [0, -2],
            [0, -1],
            [0, 0],
            [0, 1],
            [0, 2],
            [1, -2],
            [1, -1],
            [1, 0],
            [1, 1],
            [1, 2],
            [2, -2],
            [2, -1],
            [2, 0],
            [2, 1],
            [2, 2],
            [3, 2],
            [2, 3],
            [3, 3],
            [3, 4],
            [4, 3],
            [4, 4],
            [4, 5],
            [5, 4],
            [5, 5],
            [-3, -2],
            [-2, -3],
            [-3, -3],
            [-3, -4],
            [-4, -3],
            [-4, -4],
            [-4, -5],
            [-5, -4],
            [-5, -5],
            [-3, 2],
            [-2, 3],
            [-3, 3],
            [-3, 4],
            [-4, 3],
            [-4, 4],
            [-4, 5],
            [-5, 4],
            [-5, 5],
            [3, -2],
            [2, -3],
            [3, -3],
            [3, -4],
            [4, -3],
            [4, -4],
            [4, -5],
            [5, -4],
            [5, -5],
        ]

    def DoPeche(self, type_de_prise):
        if type_de_prise == "Monstre":
            attente_avant_catch = random.randint(35, 45)
            nombre_de_mini_jeu = 6
        elif type_de_prise == "Item":
            attente_avant_catch = random.randint(35, 55)
            nombre_de_mini_jeu = 7
        elif type_de_prise == "Poisson":
            attente_avant_catch = random.randint(45, 65)
            nombre_de_mini_jeu = 9
        elif type_de_prise == "Gros Poisson":
            attente_avant_catch = random.randint(55, 75)
            nombre_de_mini_jeu = 12
        elif type_de_prise == "Redcoin":
            attente_avant_catch = random.randint(55, 85)
            nombre_de_mini_jeu = 15
        elif type_de_prise == "Artefact":
            attente_avant_catch = random.randint(65, 100)
            nombre_de_mini_jeu = 20
        else:
            attente_avant_catch = random.randint(65, 100)
            nombre_de_mini_jeu = 0
        

        attente_avant_catch = random.randint(5, 25)
        #premiere étape : le catch. attendre le bon moment et retirer la ligne.
        PlayMusic("waves")
        etat_du_poisson = self.MechanismeAttentePourPeche(attente_avant_catch)
        ClearConsole()
        if etat_du_poisson == "Nothing":
            print("Vous n'avez pas assez attendu, et rien n'est au bout de l'hameçon !")
            services.Affichage.EntreePourContinuer()
            return "Pas assez attendu"

        elif etat_du_poisson == "Away":
            print("Vous avez trop attendu, et le poisson s'est en allé !")
            services.Affichage.EntreePourContinuer()
            return "Trop attendu"

        elif etat_du_poisson == "Catch":
            PlaySound("catch")
            print("Un poisson mort a l'hameçon !")
            time.sleep(2)
            services.Affichage.EntreePourContinuer()
            if nombre_de_mini_jeu == 0:
                print("Nan, je rigole.\nYa rien à pecher, vous vous souvenez ?")
                services.Affichage.EntreePourContinuer()
                return "Pas assez attendu"
            else:
                PlayMusic("fishing")
                self.limite_chronometre = 5
                self.debut_chronometre = time.time()
                for _ in range(0, (nombre_de_mini_jeu + 1)):
                    #faire 3 mini jeu different : mouvements opposé, attendre, spam 
                    numero_aleatoire = random.randint(1, 3)
                    if numero_aleatoire == 1:
                        resultat = self.DoOppose()
                    elif numero_aleatoire == 2:
                        resultat = self.DoWait()
                    elif numero_aleatoire == 3:
                        resultat = self.DoSpam()
                    if resultat == "Loupé":
                        PlaySound("escape")
                        print("Vous avez fait quelque chose de mal, et le poisson à laché l'hameçon !")
                        services.Affichage.EntreePourContinuer()
                        return resultat
                    elif resultat == "Trop de temps":
                        PlaySound("escape")
                        print("Vous avez mit trop de temps a ramener le poisson, et il a laché l'hameçon !")
                        services.Affichage.EntreePourContinuer()
                        return resultat
                PlaySound("battle_win")
                print("Attrapé !")
                temps_restant = self.CheckChronometre("temps")
                print(temps_restant)
                services.Affichage.EntreePourContinuer()
                return type_de_prise
            
    def CheckChronometre(self, parametre="None"):
        chronometre_actuel = time.time()
        temps_depuis_debut = chronometre_actuel - self.debut_chronometre
        if parametre == "temps":
            return (self.limite_chronometre - temps_depuis_debut)
        if temps_depuis_debut < self.limite_chronometre:
            return True
        return False
            
    def DoSpam(self):
        nombre_de_tir = random.randint(8, 15)
        self.limite_chronometre += (nombre_de_tir * 1.1)
        for tir in range(0, nombre_de_tir + 1):
            if tir < 8:
                print("Le poisson fait des petits mouvements !")
            elif tir < 4:
                print("Le poisson se fatigue !")
            else:
                print("Le poisson ne bouge presque plus !")
            if tir == nombre_de_tir:
                dummy = input("\n\nAppuyez sur entrée pour donner un grand coup sur la ligne ")
            else:
                dummy = input("\n\nAppuyez sur entrée pour tirer sur la ligne ")
            ClearConsole()
        if self.CheckChronometre() == False:
            return "Trop de temps"
        else:
            return "Continue"

            
    def DoOppose(self):
        nombre_aleatoire = random.randint(1, 3)
        for _ in range(1, (nombre_aleatoire + 1)):
            self.limite_chronometre += 2
            #type de mouvement du poisson
            numero_aleatoire = random.randint(1,2)
            if numero_aleatoire == 1 :
                type_de_mouvement = "fortement"
            elif numero_aleatoire == 2 :
                type_de_mouvement = "légèrement"

            #mouvement du poisson
            numero_aleatoire = random.randint(1,3)
            if numero_aleatoire == 1 :
                direction_du_mouvement = "la Gauche"
            elif numero_aleatoire == 2 :
                direction_du_mouvement = "la Droite"
            elif numero_aleatoire == 3 :
                direction_du_mouvement = "l'Arrière"

            #mouvement_a_effectuer
            if direction_du_mouvement == "la Gauche" and type_de_mouvement == "légèrement":
                mouvement_a_effectuer = "la Droite"
            elif direction_du_mouvement == "la Droite" and type_de_mouvement == "légèrement":
                mouvement_a_effectuer = "la Gauche"
            elif direction_du_mouvement == "l'Arrière" and type_de_mouvement == "légèrement":
                mouvement_a_effectuer = "l'Avant"
            else:
                mouvement_a_effectuer = direction_du_mouvement

            #liste de mouvements disponibles
            liste_mouvements_disponibles = ["la Gauche", "la Droite", "l'Arrière", "l'Avant"]
            random.shuffle(liste_mouvements_disponibles)

            #affichage
            while True:
                try :
                    print(f"Le poisson tire {type_de_mouvement} vers {direction_du_mouvement} !\n")
                    numero = 1
                    for action in liste_mouvements_disponibles:
                        print(f"{numero} - Tirer vers {action}")
                        numero += 1
                    choix = int(input("\nChoisir avec les nombres, vite ! : "))
                    ClearConsole()
                    if choix in range(1, 5):
                        break
                except ValueError:
                    ClearConsole()

            #verification
            mouvement_effectue = liste_mouvements_disponibles[choix - 1]
            if mouvement_a_effectuer != mouvement_effectue :
                return "Loupé"
            if self.CheckChronometre() == False:
                return "Trop de temps"
        return "Continue"
                
    def DoWait(self):
        attente = random.randint(3,6)
        self.limite_chronometre += attente + 1.25
        prise = self.MechanismeDoWait(attente)
        if prise == "Away":
            return "Trop de temps"
        else:
            return "Continue"

    def MechanismeDoWait(self, attente):
        self.poisson_se_calme = False
        self.ArretePecheAttente = threading.Event()

        # Démarre un thread qui attend le moment où le poisson mord
        self.PecheAttente = threading.Thread(target=self.AttentePourDoWait, args=(attente,))
        self.PecheAttente.start()


        # Attend que l'utilisateur appuie sur "Entrée"
        input("")

        # Arrête le thread d'attente
        self.ArretePecheAttente.set()
        self.PecheAttente.join()

        # Vérifie le résultat
        ClearConsole()
        if self.poisson_se_calme:
            if self.CheckChronometre() == False:
                return "Away"
            else:
                return "Catch"
        
    def AttentePourDoWait(self, attente):
        temps_attendu = 0
        print("Le poisson se débat comme un petit diable !\n\nAppuyer sur entrée pour remonter la ligne.")
        while not self.ArretePecheAttente.isSet():
            time.sleep(0.1)
            temps_attendu += 0.1
            if temps_attendu >= attente:
                ClearConsole()
                print("Le poisson commence à se calmer.\n\nAppuyer sur entrée pour remonter la ligne.")
                self.poisson_se_calme = True
                break

            ####################################################################################################

    def MechanismeAttentePourPeche(self, attente=2.5):
        self.poisson_a_hameçon = False
        self.ArretePecheAttente = threading.Event()

        # Démarre un thread qui attend le moment où le poisson mord
        self.PecheAttente = threading.Thread(target=self.AttentePourPeche, args=(attente,))
        self.PecheAttente.start()

        # Capture l'heure de début
        temps_de_debut_de_peche = time.time()

        # Attend que l'utilisateur appuie sur "Entrée"
        input("")

        # Enregistre l'heure de fin
        temps_de_fin_de_peche = time.time()
        temps_de_peche = temps_de_fin_de_peche - temps_de_debut_de_peche

        # Arrête le thread d'attente
        self.ArretePecheAttente.set()
        self.PecheAttente.join()

        # Vérifie le résultat
        if self.poisson_a_hameçon:
            if attente <= temps_de_peche <= (attente + 0.75):
                return "Catch"
            else:
                return "Away"
        else:
            return "Nothing"

    def AttentePourPeche(self, attente):
        temps_attendu = 0
        print("\n\n\n\nAppuyer sur entrée pour remonter la ligne.")
        while not self.ArretePecheAttente.isSet():
            time.sleep(0.1)
            temps_attendu += 0.1
            if temps_attendu >= attente:
                ClearConsole()
                print("         MAINTENANT\n\n\nAppuyer sur entrée pour remonter la ligne.")
                self.poisson_a_hameçon = True
                break

                



    def ReposDansJacuzzi(self):
        self.ArreteJacuzzi = threading.Event()
        self.Jacuzzi = threading.Thread(target=self.GainDansJacuzzi)
        self.Jacuzzi.start()
        input("")
        self.ArreteJacuzzi.set()
        time.sleep(2)
        ClearConsole()

    def GainDansJacuzzi(self):
        numero = 0
        temps_dattente = 30
        commentaire = ""
        while not self.ArreteJacuzzi.isSet():
            print("            -= Vous vous la coulez douce... =-")
            print(f"              Vos points de vie max : {services.Player.points_de_vie_max}")
            print(f"              Vos points de mana max : {services.Player.points_de_mana_max}")
            print("   Taux de conversion : +1 point de mana/vie max par 30 secondes.")
            print(commentaire)
            print("          Appuyez sur entree pour sortir du jacuzzi")
            time.sleep(temps_dattente)
            ClearConsole()
            numero += 1
            if numero > 4:
                commentaire = "\n*Vous devriez en profiter pour faire une pause, parler a votre famille, toucher de l'herbe, aller boire de l'eau...*\n"
            elif numero > 15:
                commentaire = "\n*Elle est bien la musique, hein ?*\n"
            if numero > 30:
                commentaire = "\n*Avec vos doigts completements fripés et vos lèvres violettes, vous n'êtes plus sûr de gagner quoi que ce soit en restant dans le jacuzzi...*\n"
            elif numero%2 == 1 :
                services.Player.points_de_vie_max += 1
            elif numero%2 == 0:
                services.Player.points_de_mana_max += 1
            

    def MakeFloorBlueprint(self, nombre_de_salles):
        self.FloorBlueprint = {}
        # faire le dictionnaire de salles, vide
        for numero_de_salle in range(1, (nombre_de_salles + 1)):
            self.FloorBlueprint[numero_de_salle] = {
                "position_x": 0,
                "position_y": 0,
                "marqué sur la carte": False,
                "terminé par joueur": False,
                "type": "None",
            }
        # remplir le dictionnaire avec les salles de base (arene + couloirs sur les cotés)
        if "Schmilblick" in services.Player.liste_dartefacts_optionels:
            marquage_sur_la_carte = True
        else:
            marquage_sur_la_carte = False
        if (services.Player.numero_de_letage == 0 and "Combattant le Gardien" not in services.Player.player_tags) or services.Player.nom_de_letage == "Limbes Flétrissants":
            fait_par_le_joueur = True
        else:
            fait_par_le_joueur = False
        self.FloorBlueprint[1] = {
            "position_x": 0,
            "position_y": 0,
            "marqué sur la carte": marquage_sur_la_carte,
            "terminé par joueur": False,
            "type": "ENTREE",
        }
        self.FloorBlueprint[2] = {
            "position_x": 2,
            "position_y": 0,
            "marqué sur la carte": marquage_sur_la_carte,
            "terminé par joueur": fait_par_le_joueur,
            "type": "None",
        }
        self.FloorBlueprint[3] = {
            "position_x": -2,
            "position_y": 0,
            "marqué sur la carte": marquage_sur_la_carte,
            "terminé par joueur": fait_par_le_joueur,
            "type": "None",
        }
        self.FloorBlueprint[4] = {
            "position_x": 0,
            "position_y": 2,
            "marqué sur la carte": marquage_sur_la_carte,
            "terminé par joueur": fait_par_le_joueur,
            "type": "None",
        }
        self.FloorBlueprint[5] = {
            "position_x": 0,
            "position_y": -2,
            "marqué sur la carte": marquage_sur_la_carte,
            "terminé par joueur": fait_par_le_joueur,
            "type": "None",
        }
        self.FloorBlueprint[6] = {
            "position_x": 3,
            "position_y": 0,
            "marqué sur la carte": marquage_sur_la_carte,
            "terminé par joueur": fait_par_le_joueur,
            "type": "None",
        }
        self.FloorBlueprint[7] = {
            "position_x": -3,
            "position_y": 0,
            "marqué sur la carte": marquage_sur_la_carte,
            "terminé par joueur": fait_par_le_joueur,
            "type": "None",
        }
        self.FloorBlueprint[8] = {
            "position_x": 0,
            "position_y": 3,
            "marqué sur la carte": marquage_sur_la_carte,
            "terminé par joueur": fait_par_le_joueur,
            "type": "None",
        }
        self.FloorBlueprint[9] = {
            "position_x": 0,
            "position_y": -3,
            "marqué sur la carte": marquage_sur_la_carte,
            "terminé par joueur": fait_par_le_joueur,
            "type": "None",
        }
        # genere aléatoirement une salle autour d'une salle déja posée
        for numero_de_salle in range(1, nombre_de_salles + 1):
            # skippe les salles 1 a 9 deja initialisées
            if numero_de_salle in range(1, 10):
                continue
            # selection de la salle origine, autour de laquelle va se rajouter une salle
            salle_ajoutee = False
            # print(numero_de_salle)
            # time.sleep(1)
            while not salle_ajoutee:
                # choisi une salle au hasard dans le blueprint
                salle_origine = random.randint(6, (numero_de_salle - 1))
                # regarde si il est possible de rajouter une salle autour de cette salle d'origine
                caracteristique_de_la_salle = self.FloorBlueprint[salle_origine]
                position_x_origine = caracteristique_de_la_salle["position_x"]
                position_y_origine = caracteristique_de_la_salle["position_y"]
                # print(position_x_origine)
                # print(position_y_origine)
                liste_de_directions_vide = []
                # test des directions ne possédant pas de salle, depuis l'origine
                for direction in self.DictionnaireAjout:
                    construction_possible = True
                    couple_dajout_sur_les_positions = self.DictionnaireAjout[direction]
                    position_x_potentielle_nouvelle_salle = (
                        position_x_origine + couple_dajout_sur_les_positions[0]
                    )
                    position_y_potentielle_nouvelle_salle = (
                        position_y_origine + couple_dajout_sur_les_positions[1]
                    )

                    # regarde si la position a déja été attribuée a une autre salle
                    for numero_de_salle_a_tester_si_elle_existe_a_la_position_potentielle in (
                        range(1, numero_de_salle)
                    ):
                        salle_a_tester = self.FloorBlueprint[
                            numero_de_salle_a_tester_si_elle_existe_a_la_position_potentielle
                        ]
                        if (
                            position_x_potentielle_nouvelle_salle
                            == salle_a_tester["position_x"]
                            and position_y_potentielle_nouvelle_salle
                            == salle_a_tester["position_y"]
                        ):
                            construction_possible = False
                            break

                    # regarde si la position se trouve dans la zone inconstruisible
                    for position in self.ListeDePositionsInconstruisibles:
                        # print(f"teste {position_x_potentielle_nouvelle_salle}:{position_y_potentielle_nouvelle_salle} | impossible  {position[0]}:{position[1]} ")
                        if (
                            position_x_potentielle_nouvelle_salle == position[0]
                            and position_y_potentielle_nouvelle_salle == position[1]
                        ):
                            construction_possible = False
                            break

                    # si la salle n'est pas sur une salle déja construite ou dans la limite inconstructible,
                    # on rajoute sa direction dans le dictionnaire
                    if construction_possible:
                        liste_de_directions_vide.append(direction)
                        break
                # liste_de_direction_vide contient toute les directions dans lesquelles
                #   on peut mettre une salle a partir de la salle origine sélectionnée.
                # on choisit donc parmis ces directions celle que l'on veut prendre, et on y crée une salle.
                if len(liste_de_directions_vide) != 0:
                    # selection de la direction prise
                    numero_de_la_direction_prise = random.randint(
                        0, (len(liste_de_directions_vide) - 1)
                    )
                    direction_prise = liste_de_directions_vide[
                        numero_de_la_direction_prise
                    ]
                    # selection des positions grace a la direction.
                    couple_dajout_sur_les_positions = self.DictionnaireAjout[direction_prise]
                    position_x_nouvelle_salle = (
                        position_x_origine + couple_dajout_sur_les_positions[0]
                    )
                    position_y_nouvelle_salle = (
                        position_y_origine + couple_dajout_sur_les_positions[1]
                    )
                    # construction salle (ajout au blueprint des position selectionnées)
                    salle_a_construire = self.FloorBlueprint[numero_de_salle]
                    salle_a_construire["position_x"] = position_x_nouvelle_salle
                    salle_a_construire["position_y"] = position_y_nouvelle_salle
                    if "Schmilblick" in services.Player.liste_dartefacts_optionels:
                        salle_a_construire["marqué sur la carte"] = True
                    if services.Player.nom_de_letage == "Limbes Flétrissants" or (services.Player.numero_de_letage == 0 and "Combattant le Gardien" not in services.Player.player_tags) :
                        salle_a_construire["terminé par joueur"] = True
                    salle_ajoutee = True

    def SetupFloorBlueprint(self):
        # prendre les numeros des salles vides (normalement, de 2 a nombre_salle)
        liste_de_salle_vide = []
        for numero_de_salle in range(2, len(self.FloorBlueprint)):
            # ajouter ces numéros dans une liste
            liste_de_salle_vide.append(numero_de_salle)
        while True:
            if len(liste_de_salle_vide) == 0:
                break
            # sortir un numéro de la liste (de maniere aléatoire, en utilisant les indexs)
            index_aleatoire = random.randint(0, (len(liste_de_salle_vide) - 1))
            salle_choisie = liste_de_salle_vide.pop(index_aleatoire)
            # attribuer une fonction a la salle affectée a ce numéro
            self.AttributingRoleToRoom(salle_choisie)
            # recommencer jusqu'à ce qu'il n'y aie plus de numéros dans la liste
        # pour une raison inconnue, la derniere salle n'est pas attribuée a une fonction
        self.AttributingRoleToRoom(len(self.FloorBlueprint))

    def PrintFloorBlueprint(self):
        tracer(0)
        self.nombre_de_bols = 1
        nombre_de_salle = len(self.FloorBlueprint)
        setup(width=800, height=800)
        setworldcoordinates(-200, -200, 200, 200)
        ColiseumGoto(0, 0)
        speed(0)
        for salle in range(1, (nombre_de_salle + 1)):
            # initialise les coordonnées de la salle
            caracteristique_de_la_salle = self.FloorBlueprint[salle]
            position_x = caracteristique_de_la_salle["position_x"] * 25
            position_y = caracteristique_de_la_salle["position_y"] * 25
            ColiseumGoto(position_x, position_y)

            # dessine la salle
            if caracteristique_de_la_salle["type"] == "ENTREE":
                services.Draw.entree()
            else:
                services.Draw.salle()

            # dessine le dessin de la salle, si il y a a le faire
            if caracteristique_de_la_salle["marqué sur la carte"]:
                ColiseumGoto(position_x, position_y)
                dessiner_l_icone(caracteristique_de_la_salle["type"], position_x, position_y)
        if "Combattant le Gardien" in services.Player.player_tags:
            self.UpdatePlayerPosition()
        else:
            ColiseumGoto(0, 0)
        setheading(90)
        tracer(1)
    def StopAllVillageChannels(self):
        try:
            if self.channel_rien:
                self.channel_rien.stop()
            if self.channel_rien2:
                self.channel_rien2.stop()
            if self.channel_retailer:
                self.channel_retailer.stop()
            if self.channel_hawker:
                self.channel_hawker.stop()
            if self.channel_banker:
                self.channel_banker.stop()
            if self.channel_witch:
                self.channel_witch.stop()
            if self.channel_blacksmith:
                self.channel_blacksmith.stop()
        except :
            ClearConsole()

    def InitialisationOfTownVariations(self):
        dir_path = services.Player.chemin_musique

        chemin_musique_rien = dir_path + f"\\nothing.mp3"
        chemin_musique_rien2 = dir_path + f"\\nothing.mp3"
        chemin_musique_retailer = dir_path + f"\\retailer_variation.mp3"
        chemin_musique_hawker = dir_path + f"\\hawker_variation.mp3"
        chemin_musique_banker = dir_path + f"\\banker_variation.mp3"
        chemin_musique_witch = dir_path + f"\\witch_variation.mp3"
        chemin_musique_blacksmith = dir_path + f"\\blacksmith_variation.mp3"

        music_rien = mixer.Sound(chemin_musique_rien)
        music_rien2 = mixer.Sound(chemin_musique_rien2)
        music_retailer = mixer.Sound(chemin_musique_retailer)
        music_hawker = mixer.Sound(chemin_musique_hawker)
        music_banker = mixer.Sound(chemin_musique_banker)
        music_witch = mixer.Sound(chemin_musique_witch)
        music_blacksmith = mixer.Sound(chemin_musique_blacksmith)

        music_rien.set_volume(1)
        music_rien2.set_volume(1)
        music_retailer.set_volume(1)
        music_hawker.set_volume(1)
        music_banker.set_volume(1)
        music_witch.set_volume(1)
        music_blacksmith.set_volume(1)

        self.channel_rien = music_rien.play(loops=-1)
        self.channel_rien2 = music_rien.play(loops=-1)
        self.channel_retailer = music_retailer.play(loops=-1)
        self.channel_hawker = music_hawker.play(loops=-1)
        self.channel_banker = music_banker.play(loops=-1)
        self.channel_witch = music_witch.play(loops=-1)
        self.channel_blacksmith = music_blacksmith.play(loops=-1)

        self.channel_rien.set_volume(0)
        self.channel_rien2.set_volume(0)
        self.channel_retailer.set_volume(0)
        self.channel_hawker.set_volume(0)
        self.channel_banker.set_volume(0)
        self.channel_witch.set_volume(0)
        self.channel_blacksmith.set_volume(0)


    def DoTransition(self, entree_ou_sortie, nom_du_trader):

        if nom_du_trader == "SORCIERE":
            channel_choisi = self.channel_witch
        elif nom_du_trader == "HERBORISTE":
            channel_choisi = self.channel_hawker
        elif nom_du_trader == "MAITRE_ARTEFACT":
            channel_choisi = self.channel_retailer
        elif nom_du_trader == "ARMURIER":
            channel_choisi = self.channel_blacksmith
        elif nom_du_trader == "BANQUIER":
            channel_choisi = self.channel_banker

        if entree_ou_sortie == "In":
            transition_time = 0.5  # Temps de transition en secondes
            steps = 100
            for i in range(steps + 1):
                volume_a = 1 - (i / steps)  # Réduire le volume de A
                volume_b = i / steps  # Augmenter le volume de B
                
                channel_choisi.set_volume(volume_b)
                audio.CHANNELMUSIQUEDEBASE.set_volume(volume_a)

                time.sleep(transition_time / steps)

        elif entree_ou_sortie == "Out":
            transition_time = 0.5  # Temps de transition en secondes
            steps = 100
            for i in range(steps + 1):
                volume_a = 1 - (i / steps)  # Réduire le volume de A
                volume_b = i / steps  # Augmenter le volume de B
                audio.CHANNELMUSIQUEDEBASE.set_volume(volume_b)
                channel_choisi.set_volume(volume_a)
                time.sleep(transition_time / steps)

    def WalkInFloor(self):
        while True:
            while True:
                try:
                    print(
                        f"             -=[ Observation de l'Etage {services.Player.numero_de_letage} ]=-"
                    )
                    print("")
                    print("4 - Aller à Gauche")
                    print("6 - Aller à Droite")
                    print("8 - Aller en Haut")
                    print("2 - Aller en Bas")
                    
                    if services.Player.numero_de_letage == -1:
                        print("5 - Observer l'endroit")
                        print("0 - Liste de Matériaux et autre")
                    else:
                        print("5 - Observer la Salle")
                        print("0 - Fiche de Personnage")
                    print("")
                    choix = int(input("Choisissez une action avec les nombres : "))
                    ClearConsole()
                    if choix in [4, 6, 8, 5, 2, 123, 0]:
                        break
                except ValueError:
                    ClearConsole()
            if choix == 4:
                self.WalkLeft()
            elif choix == 123:
                print(self.FloorBlueprint)
                services.Affichage.EntreePourContinuer()
            elif choix == 6:
                self.WalkRight()
            elif choix == 8:
                self.WalkUp()
            elif choix == 2:
                self.WalkDown()
            elif choix == 0 and services.Player.numero_de_letage != -1:
                if "Combattant le Gardien" in services.Player.player_tags:
                    print("Vous sortez votre sacoche, mais vous n'arrivez pas a vous souvenir comment utiliser vos objets ou vos sorts avec votre esprit confus, alors vous la raccrochez à sa place.")
                    services.Affichage.EntreePourContinuer()
                else:
                    services.Player.ShowPlayerCaracteristicsAndItems()
            elif choix == 0 and services.Player.numero_de_letage == -1:
                services.Player.ShowGarbage()
            elif choix == 5:
                try:
                    self.RevealRoom()
                except Exception as error:
                    WriteErrorInErrorLog(error)
                if not "Fantome" in services.Player.player_tags:
                    if services.Player.numero_de_la_salle == 1:
                        if "Sort du Combat contre le Gardien" in services.Player.player_tags:
                            services.Player.player_tags.remove("Sort du Combat contre le Gardien")
                        break
            if not "Fantome" in services.Player.player_tags:
                self.UpdatePlayerPosition()
                if "Passer La Porte Redcoin" in services.Player.player_tags:
                    services.Player.player_tags.remove("Passer La Porte Redcoin")
                    break
                elif "Sort du Combat contre le Gardien" in services.Player.player_tags:
                    services.Player.player_tags.remove("Sort du Combat contre le Gardien")
                    break
            else:
                break

    def UseMonocleDeVerite(self):
        if "Monocle de Vérité" in services.Player.liste_dartefacts_optionels:
            gain_gold = 5
            services.Player.AddGoldToPlayer(gain_gold)

    def TraderIncAnimationOpen(self):
        print("                       ||")
        time.sleep(0.05)
        print("                      ||||")
        time.sleep(0.05)
        print("                     ||  ||")
        time.sleep(0.05)
        print("                    ||||||||")
        time.sleep(0.05)
        print("                   |||    |||")
        time.sleep(0.05)
        print("                  || ||  || ||")
        time.sleep(0.05)
        print("                 ||   ||||   ||")
        time.sleep(0.05)
        print("                ||     ||     ||")
        time.sleep(0.05)
        print("               ||||||||||||||||||")
        time.sleep(0.05)
        print("")
        time.sleep(0.05)
        print("")
        time.sleep(0.05)
        print("              Traders Incorporated")
        time.sleep(0.05)
        print("                Fidelity Service")
        time.sleep(0.05)
        print("\n")
        time.sleep(0.05)
        print(f"Bonjour Trader, nous avons détecté {services.Player.jetons} jeton en votre possession.")
        time.sleep(0.05)
        print("\n")
        time.sleep(0.05)
        print("\n1 - Gagnez 5 items aléatoires pour seulement 1 Jeton !")
        time.sleep(0.05)
        print("2 - Achetez 1 Redcoin pour un prix misérable de 2 Jetons !")
        time.sleep(0.05)
        print("3 - Dépensez 3 Jetons et repartez chez vous avec un artefact !")
        time.sleep(0.05)
        print("4 - 4 Jetons, c'est le prix de la tranquilité avec notre service d'augmentation de la chair !")
        time.sleep(0.05)
        print("5 - Devenez un membre Platinium de notre service de Trading pour 5 Jetons !")
        time.sleep(0.05)
        print("\n6 - Eteindre le système.")
        time.sleep(0.05)
        print("\nFaites votre choix en touchant les nombres : ")
        time.sleep(0.05)
        ClearConsole()

    def TraderIncAnimationClose(self):
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
        time.sleep(0.05)
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
        print(f"Bonjour Trader, nous avons détecté {services.Player.jetons} jeton en votre possession.")
        print("\n")
        print("\n1 - Gagnez 5 items aléatoires pour seulement 1 Jeton !")
        print("2 - Achetez 1 Redcoin pour un prix misérable de 2 Jetons !")
        print("3 - Dépensez 3 Jetons et repartez chez vous avec un artefact !")
        print("4 - 4 Jetons, c'est le prix de la tranquilité avec notre service d'augmentation de la chair !")
        print("5 - Devenez un membre Platinium de notre service de Trading pour 5 Jetons !")
        time.sleep(0.05)
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
        print(f"Bonjour Trader, nous avons détecté {services.Player.jetons} jeton en votre possession.")
        print("\n")
        print("\n1 - Gagnez 5 items aléatoires pour seulement 1 Jeton !")
        print("2 - Achetez 1 Redcoin pour un prix misérable de 2 Jetons !")
        print("3 - Dépensez 3 Jetons et repartez chez vous avec un artefact !")
        time.sleep(0.05)
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
        print(f"Bonjour Trader, nous avons détecté {services.Player.jetons} jeton en votre possession.")
        print("\n")
        print("\n1 - Gagnez 5 items aléatoires pour seulement 1 Jeton !")
        print("2 - Achetez 1 Redcoin pour un prix misérable de 2 Jetons !")
        time.sleep(0.05)
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
        print(f"Bonjour Trader, nous avons détecté {services.Player.jetons} jeton en votre possession.")
        print("\n")
        print("\n1 - Gagnez 5 items aléatoires pour seulement 1 Jeton !")
        time.sleep(0.05)
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
        print(f"Bonjour Trader, nous avons détecté {services.Player.jetons} jeton en votre possession.")
        print("\n")
        time.sleep(0.05)
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
        time.sleep(0.05)
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
        time.sleep(0.05)
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
        time.sleep(0.05)
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
        time.sleep(0.05)
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
        time.sleep(0.05)
        ClearConsole()
        print("                       ||")
        print("                      ||||")
        print("                     ||  ||")
        print("                    ||||||||")
        print("                   |||    |||")
        print("                  || ||  || ||")
        print("                 ||   ||||   ||")
        print("                ||     ||     ||")
        time.sleep(0.05)
        ClearConsole()
        print("                       ||")
        print("                      ||||")
        print("                     ||  ||")
        print("                    ||||||||")
        print("                   |||    |||")
        print("                  || ||  || ||")
        print("                 ||   ||||   ||")
        time.sleep(0.05)
        ClearConsole()
        print("                       ||")
        print("                      ||||")
        print("                     ||  ||")
        print("                    ||||||||")
        print("                   |||    |||")
        print("                  || ||  || ||")
        time.sleep(0.05)
        ClearConsole()
        print("                       ||")
        print("                      ||||")
        print("                     ||  ||")
        print("                    ||||||||")
        print("                   |||    |||")
        time.sleep(0.05)
        ClearConsole()
        print("                       ||")
        print("                      ||||")
        print("                     ||  ||")
        print("                    ||||||||")
        time.sleep(0.05)
        ClearConsole()
        print("                       ||")
        print("                      ||||")
        print("                     ||  ||")
        time.sleep(0.05)
        ClearConsole()
        print("                       ||")
        print("                      ||||")
        time.sleep(0.05)
        ClearConsole()
        print("                       ||")
        time.sleep(0.05)
        ClearConsole()
        print("")
        time.sleep(0.05)
        ClearConsole()

    def RevealRoom(self):
        caracteristique_de_la_salle = self.FloorBlueprint[services.Player.numero_de_la_salle]
        if caracteristique_de_la_salle["terminé par joueur"] == True:
            print("La salle est sans interêt.")
            services.Affichage.EntreePourContinuer()
        else:
            reveler_la_salle(self, caracteristique_de_la_salle)

        #rajoute le numéro de la salle observée a la liste des dernieres salles observées
        self.liste_des_salles_observées.append(services.Player.numero_de_la_salle)
        if len(self.liste_des_salles_observées) > 4:
            self.liste_des_salles_observées.pop(0)
        
        #ajoute la description de la salle
        liste_salle_et_equivalent = { "ENTREE" : "L'Arene",
            "MONSTRE" : "Salle à Monstre",
            "MONSTRE_SUPERIEUR" : "Salle à Monstre Dopé",
            "GOLD" : "Tas de Gold",
            "RIEN" : "Salle Vide",
            "ITEM" : "Caisse à Item",
            "KEY" : "Salle à Clef",
            "LEY" : "Les Leys",
            "MIMIQUE" : "Mimique",
            "PIEGE" : "Piege",
            "SECRET" : "PLACEHOLDER",
            "COEUR" : "PLACEHOLDER",
            "PUIT" : "Puits à Souhaits",
            "LIANE" : "Coffret Végétal",
            "FAUX SPOT" : "Marque de Tromperie",
            "SPOT" : "Coffret de Pirate",
            "SEQUENCE" : "Coffret de l'Empereur",
            "DDR" : "Coffret de Folie",
            "BROKEN" : "Coffret Colatéral",
            "PLAQUE PRESSION" : "Mechanismes Anciens - Plaque de Pression",
            "ARBRE" : "Mechanismes Anciens - Arbre d'Abondance",
            "BOL" : "Mechanismes Anciens - Bol de Malchance",
            "JACCUZI" : "Mechanismes Anciens - Jaccuzi",
            "CHARGEUR" : "Mechanismes Anciens - Super-Chargeur",
            "AFFIXEUR_TECHNIQUE" : "Imbueur d'Experience",
            "AFFIXEUR_SORT" : "Imbueur de Connaissance",
            "DECHARGE" : "Décharge",
            "ARMURIER" : "Boutique des Armuriers",
            "SORCIERE" : "Boutique de la Sorciere",
            "HERBORISTE" : "Boutique de l'Herboriste",
            "BANQUIER" : "Banque du Village",
            "HOLLISTIQUE" : "Tour de la Mage Hollistique",
            "CARTOGRAPHE" : "Rue du Chuchoteur de Carte",
            "ARENE" : "Gradins des Ames",
            "FABRICATEUR" : "La Machine",
            "ANCIEN" : "Monticule de l'Ancien",
            "HOTEL" : "Saloon du Croissant de Lune",
            "ANCIENNE" : "Temple du Dieu Inconnu",
            "JARDIN" : "Jardin du Directeur",
            "MAITRE_ARTEFACT" : "Boutique du Voleur d'Artefacts",
            "WORKSHOP" : "Atelier",
            "LOTTERIE" : "Monolith Marchand",
            "BRAZIER_ROUGE" : "Brazier de Kókkinos",
            "BRAZIER_NOIR" : "Brazier de Mávros",
            "BRAZIER_BLEU" : "Brazier de Caeruleum",
            "PECHE" : "Trou Bleu",
            "BRAZIER_VERT" : "Brazier de Viridis",
            "BETE" : "Laboratoire",
            "ECLAIR" : "Colline aux Eclairs",
            "DISTRIBUTEUR" : "Mechanismes Anciens - Distributeur Coup-De-Pouce",
            "CHENIL" : "Mechanismes Anciens - Canigou",
            "BUFFET" : "Mechanismes Anciens - Buffet Equivalent",
            "SPAWNER" : "Mechanismes Anciens - Prison des Ames",
            "LEVIER" : "Mechanismes Anciens - Levier Insondable",
            "BOSS" : "Porte Divine",
            "RITUEL" : "Autel de l'Innomable",
            "OBELISQUE" : "Coffret de l'Obélisque" }

        liste_du_nom_de_la_salle_secrete_en_fonction_de_letage = ["PLACEHOLDER", "Ruine de la Cigogne Bleue", "Fontaine Pétrifiante", "Oasis de la Fortune", "Musée de la Magie", "Automate Rouillé", "Boutique de Mariette", "Cage de la Cigogne Noire", "Bibliothèque Royale", "Demeure d'Alfred", "PLACEHOLDER", "PLACEHOLDER"]
        liste_salle_et_equivalent["SECRET"] = liste_du_nom_de_la_salle_secrete_en_fonction_de_letage[services.Player.numero_de_letage]

        if services.Player.nom_de_letage == "Jungle Cruelle":
            liste_salle_et_equivalent["COEUR"] = "Lame dans la Pierre : Mirage"
        elif services.Player.nom_de_letage == "Forêt Désenchantée":
            liste_salle_et_equivalent["COEUR"] = "Lame dans la Pierre : Execution"
        elif services.Player.nom_de_letage == "Cachots de l'Immonde":
            liste_salle_et_equivalent["COEUR"] = "Joyau de l'âme : Haine"
        elif services.Player.nom_de_letage == "Douves du Pénitent":
            liste_salle_et_equivalent["COEUR"] = "Joyau de l'âme : Regret"
        elif services.Player.nom_de_letage == "Carnaval de Rouille":
            liste_salle_et_equivalent["COEUR"] = "Salle du Théâtre : Chaos"
        elif services.Player.nom_de_letage == "Le Lumisade":
            liste_salle_et_equivalent["COEUR"] = "Salle du Théâtre : Ordre"

        if caracteristique_de_la_salle["type"] in liste_salle_et_equivalent:
            services.Sove.RajouteEntreeAuLivreCigogneBlancheSiOnAPas("Les Salles", liste_salle_et_equivalent[caracteristique_de_la_salle["type"]])
        
    def DanceDanceRevolutionIntroduction(self):
        services.Save.SaveTheGameSansAffichage()
        services.Player.nombre_de_gold -= 75
        StopAllMusic()
        print("Vous inserez 75 golds dans la machine, et lancez le jeu.")
        services.Affichage.EntreePourContinuer()
        PlayMusic("tutorial")
        print("Un petit tutoriel s'affiche à l'écran.")
        services.Affichage.EntreePourContinuer()
        print("                   #####")
        print("Lorsque les notes  #####  rencontrent les encoches |_____| ,")
        print("                   #####")
        print("\nvous devez appuyer sur le nombre correspondant et le valider avec la touche entrée.\n")
        services.Affichage.EntreePourContinuer()
        print("Exemple:")
        services.Affichage.EntreePourContinuer()
        print("   #####")
        print("   #####      Attendez...")
        print("   #####")
        print("\n \n\n\n \n\n \n\n\n \n\n")
        print("  |_____|")
        print("     1   ")
        time.sleep(0.5)
        ClearConsole()
        print("\n \n\n\n")
        print("   #####")
        print("   #####      Pas encore....")
        print("   #####")
        print("\n \n\n\n \n\n")
        print("  |_____|")
        print("     1   ")
        time.sleep(0.5)
        ClearConsole()
        print("\n \n\n\n \n\n \n\n\n")
        print("   #####")
        print("   #####      Presque...")
        print("   #####")
        print("\n")
        print("  |_____|")
        print("     1   ")
        time.sleep(0.5)
        ClearConsole()
        print("\n\n \n\n\n \n\n \n\n\n \n\n")
        print("   #####")
        print("   #####      LA ! Il faut appuyer sur 1, puis entrée !")
        print("  |#####|")
        print("     1   ")
        services.Affichage.EntreePourContinuer()
        print("Rapelez vous, les notes n'avancent que si vous entrez un nombre et que vous appuyez sur entrée.")
        print("De plus, au bout de 4 erreurs, le jeu s'arrete !")
        services.Affichage.EntreePourContinuer()
        print("Finissez 260 notes avant les 180 secondes de musique, et vous gagnez !")
        services.Affichage.EntreePourContinuer()
        print("Prêt ?")
        services.Affichage.EntreePourContinuer()
        StopAllMusic()
        print("C'est parti !")
        services.Affichage.EntreePourContinuer()
        game_done = self.DanceDanceRevolution()
        return game_done

    def DanceDanceRevolution(self):
        #lance la musique
        PlaySound("dance")

        #condition de continuité du jeu
        game_over = False
        game_won = False
        essais_restant = 4

        #mise en place des toutes premieres notes
        ligne_1 = 1
        ligne_2 = 1
        ligne_3 = 1
        ligne_4 = 1
        ligne_5 = 1

        #commencement du timer
        time_start = time.time()

        #nombre de notes
        nombre_de_notes = 260

        #commencement de la boucle while
        while not game_over:

            #décompte du nombre de notes restantes
            nombre_de_notes -= 1

            #génération d'une note
            prochaine_note = random.randint(1,9)

            #affectation de la note aux lignes d'en dessous
            ligne_0 = ligne_1
            ligne_1 = ligne_2
            ligne_2 = ligne_3
            ligne_3 = ligne_4
            ligne_4 = ligne_5
            ligne_5 = prochaine_note

            #selon la valeur de la variable, l'affichage sera différent
            affichage_ligne_0 = self.MakeBottomDDRView(ligne_0)
            affichage_ligne_1 = self.MakeDDRView(ligne_1)
            affichage_ligne_2 = self.MakeDDRView(ligne_2)
            affichage_ligne_3 = self.MakeDDRView(ligne_3)
            affichage_ligne_4 = self.MakeDDRView(ligne_4)
            affichage_ligne_5 = self.MakeDDRView(ligne_5)

            while True:
                try:
                    #affiche la vue du joueur
                    print(f"{affichage_ligne_5}\n{affichage_ligne_4}\n{affichage_ligne_3}\n"
                        f"{affichage_ligne_2}\n{affichage_ligne_1}\n{affichage_ligne_0}")
                    print("    1      2      3      4      5      6      7      8      9  ")
                    
                    #affiche le nombre de vie restantes
                    if essais_restant == 4:
                        print("\n               [O]             [O]             [O] \n")
                    elif essais_restant == 3:
                        print("\n               [X]             [O]             [O] \n")
                    elif essais_restant == 2:
                        print("\n               [X]             [X]             [O] \n")
                    elif essais_restant == 1:
                        print("\n               [X]             [X]             [X] \n")
                    
                    #demande le numero au joueur
                    choix = int(input("                                "))
                    ClearConsole()

                    if choix in range(1, 10):
                        break
                except ValueError:
                    ClearConsole()

            #regarde si les notes sont finies
            if nombre_de_notes == 0 :
                game_over = True
                game_won = True

            #compare le numéro donné au numéro nécéssaire
            if not choix == ligne_0:
                essais_restant -= 1
                if essais_restant == 0:
                    game_over = True
                    game_won = False
                    cause = f"      -=Game Over=-\nVous avez fait 3 erreurs !\nDerniere faute : Numéro {choix} entré au lieu de {ligne_0}. "

            #regarde si le temps imparti est fini
            time_now = time.time()
            temps_limite = 180
            if (time_now - time_start) > temps_limite:
                game_over = True
                game_won = False
                cause = f"      -=Game Over=-\nLa musique est finie !\nIl vous restait {nombre_de_notes} notes a faire !"

        #regarde la cause de la défaite
        if not game_won:
            StopAllMusic()
            print("La musique s'arrête.")
            services.Affichage.EntreePourContinuer()
            print("L'écran se fige.")
            services.Affichage.EntreePourContinuer()
            print(cause)
            print()
            services.Affichage.EntreePourContinuer()
        else:
            StopAllMusic()
            print("La musique s'arrête.")
            services.Affichage.EntreePourContinuer()
            print("L'écran se fige.")
            services.Affichage.EntreePourContinuer()
            print("NOUVEAU HIGHSCORE !")
            print("Vous avez réussi !")
            PlaySound("questdone")
            services.Affichage.EntreePourContinuer()

        #retourne le résultat du jeu
        return game_won

    def MakeDDRView(self, valeur_de_ligne):
        espace_vide = "  "
        note_vide = "     "
        note = "#####"
        affichage = ""
        retour_a_la_ligne = "\n"
        for _ in range(1, 4):
            if valeur_de_ligne != 1 :
                for _ in range(0, valeur_de_ligne - 1):
                    affichage += espace_vide
                    affichage += note_vide
            affichage += espace_vide
            affichage += note
            affichage += retour_a_la_ligne
        return affichage

    def MakeBottomDDRView(self, valeur_de_ligne):
        espace_vide = "  "
        encoche_vide = "|_____|"
        note_vide = "     "
        note = "#####"
        note_dans_encoche = "|#####|"
        affichage = ""
        retour_a_la_ligne = "\n"
        #notes
        for _ in range(1, 3):
            if valeur_de_ligne != 1 :
                for _ in range(0, valeur_de_ligne - 1):
                    affichage += espace_vide
                    affichage += note_vide
            affichage += espace_vide
            affichage += note
            affichage += retour_a_la_ligne
        #encoches
        affichage += " "
        if valeur_de_ligne != 1 :
            for _ in range(0, valeur_de_ligne - 1):
                affichage += encoche_vide
        affichage += note_dans_encoche
        if valeur_de_ligne != 9 :
            for _ in range(0, 8 - (valeur_de_ligne - 1)):
                affichage += encoche_vide
        return affichage

    def GiveRandomArtefact(self, artefact_in_particular="None", type_douverture="None"):
        
        if services.Player.malediction == "Sparifique" and type_douverture != "Boss":
            print("...mais d'anciennes forces maudites vous empêchent d'ouvrir la boite.")
            services.Affichage.EntreePourContinuer()
        
        elif type_douverture == "Don" :
            services.Player.liste_dartefacts_optionels.append(artefact_in_particular)
            services.Sove.RajouteEntreeAuLivreCigogneBlancheSiOnAPas("Les Artefacts", artefact_in_particular)


        else:
            nombre_de_fois_a_donner_artefact = [1]
            if services.Player.death_divinity and artefact_in_particular == "None":
                nombre_de_fois_a_donner_artefact.append(2)

            for _ in nombre_de_fois_a_donner_artefact:
                if artefact_in_particular == "None":

                    # rajoute dans la liste les artefact debloqué au fur et a mesure des parties gagnees
                    donnees_de_s0ve = services.Observation.GetPermanentThingsFromS0ve() 
                    liste_dartefact_a_obtenir = ast.literal_eval(donnees_de_s0ve["Artefact Debloques"])

                    # enleve la liste les artefacts que l'on possède déja
                    for artefact in services.Player.liste_dartefacts_optionels:
                        if artefact in liste_dartefact_a_obtenir:
                            liste_dartefact_a_obtenir.remove(artefact)

                    if len(liste_dartefact_a_obtenir) == 0:
                        artefact_a_donner = "Hors Stock"

                    else:
                        # enleve vide interieur si on a voeu cristalisé, ou si on est pas Terah
                        if services.Player.nom_du_personnage != "Terah" and "Vide Interieur" in liste_dartefact_a_obtenir :
                            liste_dartefact_a_obtenir.remove("Vide Interieur")

                        if "Vide Interieur" in services.Player.liste_dartefacts_optionels:
                            liste_dartefact_a_obtenir.remove("Voeu Cristallisé")

                        if "Voeu Cristallisé" in services.Player.liste_dartefacts_optionels:
                            liste_dartefact_a_obtenir.remove("Vide Interieur")

                        # selectionne un artefact au pif
                        numero_artefact_aleatoire = random.randint(0, len(liste_dartefact_a_obtenir) - 1)
                        artefact_a_donner = liste_dartefact_a_obtenir[numero_artefact_aleatoire]

                else:
                    #donne un artefact particulier choisi a l'avance
                    artefact_a_donner = artefact_in_particular

                # donne l'artefact au joueur
                print(f"Vous gagnez l'artefact [{artefact_a_donner}] !")
                services.Player.liste_dartefacts_optionels.append(artefact_a_donner)

                # sauvegarde
                services.Save.SaveTheGameSansAffichage()

                # Applique les effets de l'artefact
                liste_recompense = LISTEEFFETSARTEFACT[artefact_a_donner]
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
                    elif cle == "Gold":
                        gain_gold = services.Player.AddGoldToPlayer(liste_recompense[cle], True)
                        commentaire = f"Vous gagnez {gain_gold} golds !"
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
                    elif cle == "Commentaire":
                        commentaire = liste_recompense[cle]
                    elif cle == "Red coin":
                        services.Player.nombre_de_red_coin += liste_recompense[cle]
                        commentaire = f"Vous gagnez {liste_recompense[cle]} Red Coin !"
                    print(commentaire)
                if artefact_a_donner == "Vide Interieur":
                    services.Player.stigma_negatif = "[Vidé]"
                    services.Player.points_de_mana_max -= 15
                    if services.Player.points_de_mana_max < 0:
                        services.Player.points_de_mana_max = 1
                    if services.Player.points_de_mana > services.Player.points_de_mana_max:
                        services.Player.points_de_mana = services.Player.points_de_mana_max
                if artefact_a_donner == "Voeu Cristallisé":
                    services.Player.stigma_negatif = "[Purifié]"
                services.Affichage.EntreePourContinuer()
                if artefact_a_donner == "Syra":
                    nombre_de_techniques = len(services.Player.techniques_possedes)
                    nombre_de_sorts = len(services.Player.sorts_possedes)
                    print(f"Vous connaissez déjà {nombre_de_techniques} techniques et {nombre_de_sorts} sorts.")
                    print(f"Vous gagnez ainsi {nombre_de_techniques * 10} pm et {nombre_de_sorts * 10} pv maximum !")
                    services.Player.points_de_vie_max += nombre_de_sorts * 10
                    services.Player.points_de_vie += nombre_de_sorts * 10
                    services.Player.points_de_mana_max += nombre_de_techniques * 10
                    services.Player.points_de_mana += nombre_de_techniques * 10
                    services.Affichage.EntreePourContinuer()
                services.Sove.RajouteEntreeAuLivreCigogneBlancheSiOnAPas("Les Artefacts", artefact_a_donner)

    def InitiateRoleToAttribute(self):
        self.liste_de_machines = ["ARBRE", "DISTRIBUTEUR", "LEVIER", "SPAWNER", "BUFFET", "CHENIL", "CHARGEUR", "JACCUZI"]
        if "Combattant le Gardien" in services.Player.player_tags:
            self.nombre_de_monstre = 0
            self.nombre_de_gold = 0
            self.nombre_de_item = 0
            self.nombre_de_mimique = 0
            self.nombre_de_piege = 0
            self.nombre_de_secret = 0
            self.nombre_de_cle = 0
            self.nombre_de_leys = 0
            self.nombre_de_petit_gardien = 5
            self.nombre_de_grand_gardien = 1
            self.nombre_de_rien = 5
            self.nombre_de_affixeur_technique = 0
            self.nombre_de_affixeur_sort = 0
            self.nombre_de_eclair = 0
            self.nombre_de_bete = 0
            self.nombre_de_monstre_superieur = 0
            self.nombre_de_lotterie = 0
            self.nombre_de_peche = 0
            self.nombre_de_workshop = 0
            self.nombre_de_brazier_bleu = 0
            self.nombre_de_brazier_rouge = 0
            self.nombre_de_brazier_noir = 0
            self.nombre_de_brazier_vert = 0
            self.nombre_de_hollistique = 0
        else:
            self.nombre_de_petit_gardien = 0
            self.nombre_de_grand_gardien = 0
            self.nombre_de_monstre = services.Player.numero_de_letage + 3
            self.nombre_de_gold = services.Player.numero_de_letage + 1
            self.nombre_de_item = services.Player.numero_de_letage // 2
            self.nombre_de_mimique = 0
            if services.Player.numero_de_letage in [2, 4, 6, 8, 10]:
                self.nombre_de_mimique = 1
            self.nombre_de_piege = services.Player.numero_de_letage + 2
            self.nombre_de_secret = 1
            self.nombre_de_cle = 0
            if  services.Sove.ModifieLivraisonDansSove("Limite", "Clé", services.Player.numero_de_letage - 3):
                self.nombre_de_cle = 1
            self.nombre_de_leys = services.Player.numero_de_letage // 3 + 1
            self.nombre_de_rien = 0
            self.nombre_de_lotterie = 0
            self.nombre_de_hollistique = 0
            if  services.Sove.ModifieTagsDansSove("Checke", "Symbole Vu") and not  services.Sove.ModifieTagsDansSove("Checke", "Mage Hollistique") and services.Player.numero_de_letage == 1:
                self.nombre_de_hollistique = 1
            if services.Player.numero_de_letage in [3, 5, 8, 10]:
                self.nombre_de_lotterie = 1
            self.nombre_de_peche = 0
            if services.Player.numero_de_letage in [2, 4, 6, 7, 9, 10]:
                self.nombre_de_peche = 1
            self.nombre_de_workshop = 0
            if services.Player.numero_de_letage in [1, 4, 8, 10]:
                self.nombre_de_workshop = 1
            nombre_aleatoire = random.randint(0,8)
            if nombre_aleatoire == 1:
                self.nombre_de_affixeur_sort = 1
                self.nombre_de_affixeur_technique = 1
                self.nombre_de_eclair = 0
            elif nombre_aleatoire == 2:
                self.nombre_de_affixeur_sort = 1
                self.nombre_de_affixeur_technique = 0
                self.nombre_de_eclair = 1
            elif nombre_aleatoire == 3:
                self.nombre_de_affixeur_sort = 0
                self.nombre_de_affixeur_technique = 1
                self.nombre_de_eclair = 1
            elif nombre_aleatoire == 4:
                self.nombre_de_affixeur_sort = 0
                self.nombre_de_affixeur_technique = 0
                self.nombre_de_eclair = 1
            elif nombre_aleatoire == 5:
                self.nombre_de_affixeur_sort = 0
                self.nombre_de_affixeur_technique = 1
                self.nombre_de_eclair = 0
            elif nombre_aleatoire == 6:
                self.nombre_de_affixeur_sort = 1
                self.nombre_de_affixeur_technique = 0
                self.nombre_de_eclair = 0
            elif nombre_aleatoire == 7:
                self.nombre_de_affixeur_sort = 0
                self.nombre_de_affixeur_technique = 0
                self.nombre_de_eclair = 0
            else:
                self.nombre_de_affixeur_technique = 1
                self.nombre_de_affixeur_sort = 1
                self.nombre_de_eclair = 1
            nombre_aleatoire = random.randint(0,9)
            self.nombre_de_bete = 0
            self.nombre_de_monstre_superieur = 0
            if nombre_aleatoire == 5 and "Regard de la Bête" not in services.Player.liste_dartefacts_optionels:
                self.nombre_de_bete = 1
                self.nombre_de_monstre_superieur = 1
            self.nombre_de_brazier_rouge = 0
            nombre_aleatoire = random.randint(0,100)
            if nombre_aleatoire <= 50:
                self.nombre_de_brazier_rouge = 1
            self.nombre_de_brazier_bleu = 0
            nombre_aleatoire = random.randint(0,100)
            if nombre_aleatoire <= 25:
                self.nombre_de_brazier_bleu = 1
            self.nombre_de_brazier_vert = 0
            nombre_aleatoire = random.randint(0,100)
            if nombre_aleatoire <= 12:
                self.nombre_de_brazier_vert = 1
            self.nombre_de_brazier_noir = 0
            nombre_aleatoire = random.randint(0,100)
            if nombre_aleatoire <= 4:
                self.nombre_de_brazier_noir = 1
            
        self.nombre_de_machine_bon = 0
        self.nombre_de_bol = 0
        self.nombre_de_plaque_pression = 0
        if services.Player.numero_de_letage in range (1, 5):
            self.nombre_de_machine_bon = 2
            self.nombre_de_bol = 1
            self.nombre_de_plaque_pression = 2
        elif services.Player.numero_de_letage in range (6, 10):
            self.nombre_de_machine_bon = 4
            self.nombre_de_bol = 2
            self.nombre_de_plaque_pression = 4
        elif services.Player.numero_de_letage == 10:
            self.nombre_de_machine_bon = 8
            self.nombre_de_bol = 3
            self.nombre_de_plaque_pression = 8
        #evenement de letage 1 : corrompre la foret pour gagner des trucs de magie
        self.nombre_de_puit = 0
        if services.Player.numero_de_letage in [1, 4, 6]:
            self.nombre_de_puit = 1
        # artefact de letage 2 (liane : besoin de machette rouillee)
        self.nombre_de_coffres_en_lianes = 0
        if services.Player.numero_de_letage == 2:
            self.nombre_de_coffres_en_lianes = 2
        # objet de letage 2 selon alt ou pas
        self.nombre_de_coeur = 0
        if services.Player.numero_de_letage in [2, 7, 5]:
            self.nombre_de_coeur = 1
        # artefact de letage 3 (5 spots, 2 artefacts, besoin de pelle rouillee pour ouvrir 1 spot)
        self.nombre_de_faux_spot = 0
        self.nombre_de_spot = 0
        if services.Player.numero_de_letage == 3:
            self.nombre_de_faux_spot = 3
        if services.Player.numero_de_letage == 3:
            self.nombre_de_spot = 2
        # artefact de letage 4 (1 livre avec 3 emplacements. si emplecements orbservés dans l'ordre, 1 artefact.)
        self.nombre_de_sequence = 0
        if services.Player.numero_de_letage in [4, 10]:
            self.nombre_de_sequence = 1
        # artefact de letage 5 (2 dance dance revolution. 50 commandes en 30 secondes pour avoir lartefact)
        self.nombre_de_ddr = 0
        if services.Player.numero_de_letage in [5, 10]:
            self.nombre_de_ddr = 2
        # artefact de letage 6 (1 coffre gratuit, énigme cassée.)
        self.nombre_de_broken = 0
        if services.Player.numero_de_letage == 6:
            self.nombre_de_broken = 1
        # artefact de letage 7 (1 rituel de sang : sacrifie 10 ennemis avec dague démoniaque (66 PE 25 DMG) pour 1 artefact et autre)
        self.nombre_de_rituel = 0
        if services.Player.numero_de_letage == 7:
            self.nombre_de_rituel = 1
        # artefact de letage 8 (2 obelisques : battre 5 ennemis a la suite sans mourir et sans gagner d'ame a la fin.)
        self.nombre_de_obelisque = 0
        if services.Player.numero_de_letage in [8, 10]:
            self.nombre_de_obelisque = 2
        # etgae 10, boss rush
        self.nombre_de_boss_rush = 0
        if services.Player.nom_de_letage == "Dédale Frontière":
            self.nombre_de_boss_rush = 1

        if services.Player.numero_de_letage in [10, 11]:
            self.nombre_de_secret = 0
        
    def AttributingRoleToRoom(self, salle_choisie):
        caracteristique_de_la_salle = self.FloorBlueprint[salle_choisie]
        if self.nombre_de_monstre != 0:
            caracteristique_de_la_salle["type"] = "MONSTRE"
            self.nombre_de_monstre -= 1
        elif self.nombre_de_gold != 0:
            caracteristique_de_la_salle["type"] = "GOLD"
            self.nombre_de_gold -= 1
        elif self.nombre_de_item != 0:
            caracteristique_de_la_salle["type"] = "ITEM"
            self.nombre_de_item -= 1
        elif self.nombre_de_mimique != 0:
            caracteristique_de_la_salle["type"] = "MIMIQUE"
            self.nombre_de_mimique -= 1
        elif self.nombre_de_piege != 0:
            caracteristique_de_la_salle["type"] = "PIEGE"
            self.nombre_de_piege -= 1
        elif self.nombre_de_secret != 0:
            caracteristique_de_la_salle["type"] = "SECRET"
            self.nombre_de_secret -= 1
        elif self.nombre_de_leys != 0:
            caracteristique_de_la_salle["type"] = "LEY"
            self.nombre_de_leys -= 1
        elif self.nombre_de_puit != 0:
            caracteristique_de_la_salle["type"] = "PUIT"
            self.nombre_de_puit -= 1
        elif self.nombre_de_coeur != 0:
            caracteristique_de_la_salle["type"] = "COEUR"
            self.nombre_de_coeur -= 1
        elif self.nombre_de_workshop != 0:
            caracteristique_de_la_salle["type"] = "WORKSHOP"
            self.nombre_de_workshop -= 1
        elif self.nombre_de_hollistique != 0:
            caracteristique_de_la_salle["type"] = "HOLLISTIQUE"
            self.nombre_de_hollistique -= 1
        elif self.nombre_de_coeur != 0:
            caracteristique_de_la_salle["type"] = "COEUR"
            self.nombre_de_coeur -= 1
        elif self.nombre_de_peche != 0:
            caracteristique_de_la_salle["type"] = "PECHE"
            self.nombre_de_peche -= 1
        elif self.nombre_de_brazier_rouge != 0:
            caracteristique_de_la_salle["type"] = "BRAZIER_ROUGE"
            self.nombre_de_brazier_rouge -= 1
        elif self.nombre_de_brazier_bleu != 0:
            caracteristique_de_la_salle["type"] = "BRAZIER_BLEU"
            self.nombre_de_brazier_bleu -= 1
        elif self.nombre_de_brazier_vert != 0:
            caracteristique_de_la_salle["type"] = "BRAZIER_VERT"
            self.nombre_de_brazier_vert -= 1
        elif self.nombre_de_brazier_noir != 0:
            caracteristique_de_la_salle["type"] = "BRAZIER_NOIR"
            self.nombre_de_brazier_noir -= 1
        elif self.nombre_de_lotterie != 0:
            caracteristique_de_la_salle["type"] = "LOTTERIE"
            self.nombre_de_lotterie -= 1
        elif self.nombre_de_bete != 0:
            caracteristique_de_la_salle["type"] = "BETE"
            self.nombre_de_bete -= 1
        elif self.nombre_de_monstre_superieur != 0:
            caracteristique_de_la_salle["type"] = "MONSTRE_SUPERIEUR"
            self.nombre_de_monstre_superieur -= 1
        elif self.nombre_de_affixeur_technique != 0:
            caracteristique_de_la_salle["type"] = "AFFIXEUR_TECHNIQUE"
            self.nombre_de_affixeur_technique -= 1
        elif self.nombre_de_affixeur_sort != 0:
            caracteristique_de_la_salle["type"] = "AFFIXEUR_SORT"
            self.nombre_de_affixeur_sort -= 1
        elif self.nombre_de_eclair != 0:
            caracteristique_de_la_salle["type"] = "ECLAIR"
            self.nombre_de_eclair -= 1
        elif self.nombre_de_cle != 0:
            caracteristique_de_la_salle["type"] = "KEY"
            if services.Player.numero_de_letage == 10 :
                caracteristique_de_la_salle["terminé par joueur"] = False
            self.nombre_de_cle -= 1
        elif self.nombre_de_coffres_en_lianes != 0:
            caracteristique_de_la_salle["type"] = "LIANE"
            self.nombre_de_coffres_en_lianes -= 1
        elif self.nombre_de_faux_spot != 0:
            caracteristique_de_la_salle["type"] = "FAUX SPOT"
            self.nombre_de_faux_spot -= 1
        elif self.nombre_de_spot != 0:
            caracteristique_de_la_salle["type"] = "SPOT"
            self.nombre_de_spot -= 1
        elif self.nombre_de_sequence != 0:
            caracteristique_de_la_salle["type"] = "SEQUENCE"
            self.nombre_de_sequence -= 1
        elif self.nombre_de_ddr != 0:
            caracteristique_de_la_salle["type"] = "DDR"
            self.nombre_de_ddr -= 1
        elif self.nombre_de_broken != 0:
            caracteristique_de_la_salle["type"] = "BROKEN"
            self.nombre_de_broken -= 1
        elif self.nombre_de_rituel != 0:
            caracteristique_de_la_salle["type"] = "RITUEL"
            self.nombre_de_rituel -= 1
        elif self.nombre_de_obelisque != 0:
            caracteristique_de_la_salle["type"] = "OBELISQUE"
            self.nombre_de_obelisque -= 1
        elif self.nombre_de_boss_rush != 0:
            caracteristique_de_la_salle["type"] = "BOSS"
            self.nombre_de_boss_rush -= 1
        elif self.nombre_de_petit_gardien != 0:
            caracteristique_de_la_salle["type"] = "PETIT GARDIEN"
            self.nombre_de_petit_gardien -= 1
        elif self.nombre_de_grand_gardien != 0:
            caracteristique_de_la_salle["type"] = "GRAND GARDIEN"
            self.nombre_de_grand_gardien -= 1
        elif self.nombre_de_rien != 0:
            caracteristique_de_la_salle["type"] = "RIEN"
            self.nombre_de_rien -= 1
        elif self.nombre_de_machine_bon != 0:
            numero_aleatoire = random.randint(0, len(self.liste_de_machines) - 1)
            type_de_machine = self.liste_de_machines[numero_aleatoire]
            caracteristique_de_la_salle["type"] = type_de_machine
            self.liste_de_machines.pop(numero_aleatoire)
            self.nombre_de_machine_bon -= 1
        elif self.nombre_de_bol != 0:
            caracteristique_de_la_salle["type"] = "BOL"
            self.nombre_de_bol -= 1
        elif self.nombre_de_plaque_pression != 0:
            caracteristique_de_la_salle["type"] = "PLAQUE PRESSION"
            self.nombre_de_plaque_pression -= 1
        else:
            nombre_aleatoire = random.randint(0, 5)
            if services.Player.nom_de_letage == "Dédale Frontière":
                if nombre_aleatoire == 0:
                    caracteristique_de_la_salle["type"] = "ITEM"
                elif nombre_aleatoire == 1:
                    caracteristique_de_la_salle["type"] = "GOLD"
                elif nombre_aleatoire in [2, 3]:
                    caracteristique_de_la_salle["type"] = "MONSTRE"
                elif nombre_aleatoire in [4, 5]:
                    caracteristique_de_la_salle["type"] = "PIEGE"
            else:
                if nombre_aleatoire == 0:
                    caracteristique_de_la_salle["type"] = "MONSTRE"
                elif nombre_aleatoire == 1:
                    caracteristique_de_la_salle["type"] = "GOLD"
                elif nombre_aleatoire in [2, 3]:
                    caracteristique_de_la_salle["type"] = "ITEM"
                elif nombre_aleatoire in [4, 5]:
                    caracteristique_de_la_salle["type"] = "PIEGE"

    def WalkLeft(self):
        if services.Player.position_x == 0 and services.Player.position_y == 0:
            services.Player.position_x = -2
        elif services.Player.position_x == 2 and services.Player.position_y == 0:
            services.Player.position_x = 0
        else:
            services.Player.position_x -= 1
        Valid = self.CheckPlayerPosition()
        if not Valid:
            services.Player.position_x += 1
            if services.Player.numero_de_letage == -1:
                print("Ca ne sert a rien d'aller par la bas.")
            else:
                print("Vous rentrez dans un mur.")
            services.Affichage.EntreePourContinuer()

    def WalkRight(self):
        if services.Player.position_x == 0 and services.Player.position_y == 0:
            services.Player.position_x = 2
        elif services.Player.position_x == -2 and services.Player.position_y == 0:
            services.Player.position_x = 0
        else:
            services.Player.position_x += 1
        Valid = self.CheckPlayerPosition()
        if not Valid:
            services.Player.position_x -= 1
            if services.Player.numero_de_letage == -1:
                print("Ca ne sert a rien d'aller par la bas.")
            else:
                print("Vous rentrez dans un mur.")
            services.Affichage.EntreePourContinuer()

    def WalkUp(self):
        if services.Player.position_x == 0 and services.Player.position_y == 0:
            services.Player.position_y = 2
        elif services.Player.position_x == 0 and services.Player.position_y == -2:
            services.Player.position_y = 0
        else:
            services.Player.position_y += 1
        Valid = self.CheckPlayerPosition()
        if not Valid:
            services.Player.position_y -= 1
            if services.Player.numero_de_letage == -1:
                print("Ca ne sert a rien d'aller par la bas.")
            else:
                print("Vous rentrez dans un mur.")
            services.Affichage.EntreePourContinuer()

    def WalkDown(self):
        if services.Player.position_x == 0 and services.Player.position_y == 0:
            services.Player.position_y = -2
        elif services.Player.position_x == 0 and services.Player.position_y == 2:
            services.Player.position_y = 0
        else:
            services.Player.position_y -= 1
        Valid = self.CheckPlayerPosition()
        if not Valid:
            services.Player.position_y += 1
            if services.Player.numero_de_letage == -1:
                print("Ca ne sert a rien d'aller par la bas.")
            else:
                print("Vous rentrez dans un mur.")
            services.Affichage.EntreePourContinuer()

    def UpdatePlayerPosition(self):
        ColiseumGoto(services.Player.position_x * 25, services.Player.position_y * 25)

    def CheckPlayerPosition(self):
        for numero_de_salle in range(1, len(self.FloorBlueprint) + 1):
            salle_a_tester = self.FloorBlueprint[numero_de_salle]
            if (
                services.Player.position_x == salle_a_tester["position_x"]
                and services.Player.position_y == salle_a_tester["position_y"]
            ):
                # le joueur se trouve sur une salle qui existe
                services.Player.numero_de_la_salle = numero_de_salle
                return True
        return False

    def SetupFloorLayout(self):
        # Initialise un dictionnaire avec les salles et leur position
        nombre_de_salles = 16 + (services.Player.numero_de_letage * 5)
        if services.Player.nom_de_letage == "Dédale Frontière":
            nombre_de_salles = 100
        elif services.Player.numero_de_letage == 11:
            nombre_de_salles = 10
        elif "Combattant le Gardien" in services.Player.player_tags:
            nombre_de_salles = 12
        self.MakeFloorBlueprint(nombre_de_salles)
       
        # détermine les nombres de roles a attribuer aux salles 
        self.InitiateRoleToAttribute()
        
        # attribue un role a chaque salles
        self.SetupFloorBlueprint()

        if not "Combattant le Gardien" in services.Player.player_tags:
            services.Save.SaveTheGameSansAffichage()


    def ShowFloor(self):
        if services.Player.numero_de_letage == -1:
            StopAllMusic()
            self.StopAllVillageChannels()
            self.InitialisationOfTownVariations()
            PlayMusicDeLetage()
        if not self.carte_ouverte and  services.Sove.ModifieLivraisonDansSove("Limite", "Carte", services.Player.numero_de_letage - 4) and  services.Sove.ModifieTagsDansSove("Checke","Livraison Terminée"):
            self.PrintFloorBlueprint()
            self.carte_ouverte = True
        self.UpdatePlayerPosition()
        self.WalkInFloor()
        if services.Player.numero_de_letage == -1:
            StopAllMusic()
            PlayMusic("wind")
