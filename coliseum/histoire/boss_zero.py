"""Étage 0 : le Sanctuaire du Sacrifice et son gardien."""

import os
import random
import sys

from coliseum import services
from coliseum.audio import PlayMusicDeLetage, StopAllMusic
from coliseum.chemins import DOSSIER_RESSOURCES
from coliseum.console import ClearConsole, attendre
from coliseum.erreurs import WriteErrorInErrorLog
from coliseum.exploration.progression import RemiseAZeroDesVariablesPourProchainEtage
from coliseum.combat.lancement import livrer_combat


def DoBossZero():
    if not "Combattant le Gardien" in services.Player.player_tags:
        while True:
            while True:
                try:
                    print("blablabla")
                    print("\n1 - J'y vais.")
                    print("2 - Qui es-tu ?")
                    print("3 - C'est quoi cet endroit ?")
                    print("4 - A propos des pages...")
                    print("5 - Pourquoi faire tout ca ?")
                    print("6 - Le véritable ennemi...")
                    print("7 - J'ai pas tellement envie de t'écouter parler, tu peux tout me résumer ?")
                    print("8 - J'ai très envie de t'écouter parler, tu peut tout me raconter dans les moindres détails ?")
                    print("9 - Tu as vu l'heure ? Il est temps de te sortir de là !")
                    choix = int(input("\nFaire votre choix avec les nombres : "))
                    ClearConsole()
                    if choix in range(1, 10):
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print("*Mais... mais non !*\n*Revient !*")
                services.Affichage.EntreePourContinuer()
                break
            elif choix == 2:
                pass
            elif choix == 3:
                pass
            elif choix == 4:
                pass
            elif choix == 5:
                pass
            elif choix == 6:
                pass
            elif choix == 7:
                pass
            elif choix == 8:
                pass
            elif choix == 9:
                print("*Eh bien...c'est parti alors.*")
                services.Affichage.EntreePourContinuer()
                services.Player.player_tags.append("Combattant le Gardien")

                services.Player.affronte_un_boss = True
                livrer_combat()
                RemiseAZeroDesVariablesPourProchainEtage()
                try:
                    services.FloorMaker.SetupFloorLayout()
                except Exception as error:
                    WriteErrorInErrorLog(error)
                PlayMusicDeLetage()
                print("Le monde se met a tourner, tourner, et vous ne reconnaissez plus l'étage dans lequel vous êtes.")
                print("La bombe fumigène vous a laissé confus, et vous en oubliez presque que le Gardien s'est enfui ! Allez le chercher dans l'étage !")
                services.Player.affronte_un_boss = False
                services.Affichage.EntreePourContinuer()
                break
    else:
        if services.Player.position_x == 0 and services.Player.position_y == 0:
            print("Le gardien n'est pas ici.")
            services.Affichage.EntreePourContinuer()
        else:
            print("Vous retrouvez le gardien entrain de soigner ses blessures, et votre confusion s'estompe !")
            print("Des petits êtres de lumière tournent autour de lui...")
            services.Affichage.EntreePourContinuer()
            print("Vous regardez ce spectacle attendrissant...")
            print("...et le gardien vous remarque.")
            services.Affichage.EntreePourContinuer()
            RemiseAZeroDesVariablesPourProchainEtage()
            services.Player.affronte_un_boss = True
            livrer_combat()

            try:
                services.FloorMaker.SetupFloorLayout()
            except Exception as error:
                WriteErrorInErrorLog(error)

            if services.Player.vies_du_gardien == 0:
                StopAllMusic()
                print("*Ca y est !*\n*Tu m'a absorbé !*")
                services.Observation.AddSoulToS0ve()
                dir_path = DOSSIER_RESSOURCES
                chemin_du_fichier_save = dir_path + "\\save.txt"
                os.remove(chemin_du_fichier_save)
                services.Affichage.EntreePourContinuer()
                print("*Je fais maintenant parti de toi...*")
                services.Affichage.EntreePourContinuer()
                print("*...")
                services.Affichage.EntreePourContinuer()
                print("*...on peut vous aider ?*")
                services.Affichage.EntreePourContinuer()
                print("Les esprits élémentaires flottent autour du gardien, et vous regardent en silence.")
                services.Affichage.EntreePourContinuer()
                print("Vous les regardez...")
                services.Affichage.EntreePourContinuer()
                print("Ils vous regardent...*")
                services.Affichage.EntreePourContinuer()
                print("Vous les regardez...")
                services.Affichage.EntreePourContinuer()
                print("Ils vous regardent...*")
                services.Affichage.EntreePourContinuer()
                print("Vous les regardez...")
                services.Affichage.EntreePourContinuer()
                print("Ils vous regardent...*")
                services.Affichage.EntreePourContinuer()
                print("Vous approchez votre main de votre arme...")
                services.Affichage.EntreePourContinuer()
                print("...et ils déguerpissent aussitôt en bas des escaliers de l'arène.")
                services.Affichage.EntreePourContinuer()
                print("*Oh. Je crois qu'ils viennent de se répandre dans les étages inferieurs.*\n*Tu risque de les recroiser assez souvent.*")
                services.Affichage.EntreePourContinuer()
                print("*Enfin bref.*")
                services.Affichage.EntreePourContinuer()
                print("*Je fais maintenant parti de toi...*")
                services.Affichage.EntreePourContinuer()
                print("*Mais pour éviter de disparaitre si tu meurs...*")
                services.Affichage.EntreePourContinuer()
                print("*...je vais devoir aller ailleurs.*")
                services.Affichage.EntreePourContinuer()
                print("*Dans le fichier de sauvegarde permanent.*")
                services.Affichage.EntreePourContinuer()
                print("*Je devrais pouvoir y arriver tout seul. J'ai juste besoin que...*")
                services.Affichage.EntreePourContinuer()
                print("*...*")
                services.Affichage.EntreePourContinuer()
                print("*...tu viens de louper le combat petit bonhomme.*")
                services.Affichage.EntreePourContinuer()
                print("*Un autre esprit, Voluntad Tin Tuukul, s'approche du gardien avec un air un peu groggy.*")
                services.Affichage.EntreePourContinuer()
                print("*Ils sont déjà partis en bas, tu devrais les suivre.*")
                services.Affichage.EntreePourContinuer()
                print("L'esprit fait quelques tours autour de Jean, puis file en direction des escaliers.")
                services.Affichage.EntreePourContinuer()
                print("*On a dela chance de pas l'avoir eu celui-là.*\n*C'est l'esprit de l'âme. Tu sais ce que ca signifie ?*")
                services.Affichage.EntreePourContinuer()
                print("*Magie illimitée*")
                services.Affichage.EntreePourContinuer()
                print("*Enfin bref.*")
                services.Affichage.EntreePourContinuer()
                print("*J'ai juste besoin que tu disparaisse quelques instants.*")
                services.Affichage.EntreePourContinuer()
                print("*Ca sera pas douloureux, promis juré !*")
                services.Affichage.EntreePourContinuer()
                print("*Et j'ai failli oublier : sans moi, le système d'ascension n'existe plus. Tu devrait renommer s1ve.txt en s0ve.txt, tu risque d'avoir une erreur sinon.*")
                attendre(10)
                sys.exit()
            else:
                #prendre les coordonnees d'une salle au pif
                salle_aleatoire = random.randint(1,6)
                caracteristique_de_la_salle = services.FloorMaker.FloorBlueprint[salle_aleatoire]

                #affecter ces coordonnéees au joueur
                services.Player.position_x = caracteristique_de_la_salle["position_x"]
                services.Player.position_y = caracteristique_de_la_salle["position_y"]
                services.Player.numero_de_la_salle = salle_aleatoire

                PlayMusicDeLetage()
                print("Le Gardien s'est enfui ! Allez le chercher dans l'étage !")
                services.Player.player_tags.append("Sort du Combat contre le Gardien")
                services.Player.affronte_un_boss = False
                services.Affichage.EntreePourContinuer()
