"""Écrans cachés : récupérateur de secrets, Observatorium, page secrète."""

import csv
import os
import time
import tkinter as tk
from tkinter import PhotoImage

from coliseum import services
from coliseum.audio import PlayMusic, StopAllMusic
from coliseum.chemins import DOSSIER_RESSOURCES
from coliseum.console import ClearConsole
from coliseum.donnees.musiques import MUSIQUES_OBSERVATORIUM


def open_image(chemin_vers_limage):
    # Créer une fenêtre Tkinter
    root = tk.Tk()

    # Créer une image Tkinter à partir du fichier
    image = PhotoImage(file=chemin_vers_limage)

    # Créer un canevas pour afficher l'image
    canvas = tk.Canvas(root, width=image.width(), height=image.height())
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=image)

    # Boucle principale Tkinter
    root.mainloop()


def GetChoiceRecup():
    print("     -=[ Outil de Récupération de Données ]=-")
    print(
        "\nInserez le numéro de l'adresse de l'information souhaitée,                                                             8"
        "\net laissez notre programme récuperer ces données pour vous !                                                           6"
    )
    print(
        "Plus besoin de paniquer lorsque l'on supprime d'anciennes données sans le vouloir !                                    2"
    )
    print(
        "Vos données n'auront plus de secret pour vous !                                                                        4"
    )
    return int(input("\nNuméro de l'adresse ipv4 : "))


def ShowRecup():
    # images doivent etre en png
    while True:
        try:
            choix = GetChoiceRecup()
            ClearConsole()
            break
        except ValueError:
            ClearConsole()
    services.Affichage.AfficheLongChargement()
    if choix in [
        362951847,
        14,
        100110,
        8624,
        151211913131214,
        1342,
        1233,
        456852,
        3236353,
        313,
        26,
        935284761,
        5321139741,
        7415321139,
        9353918170,
    ]:
        if choix == 8624:
            nom_de_limage = "python_properties_vue"  # table des matieres -

        elif choix == 456852:
            nom_de_limage = "python_properties_main_Thread"  # image observation e7 -

        elif choix == 362951847:
            nom_de_limage = "python_properties_Anox_init"  # page 1 (e1) -
        elif choix == 100110:
            nom_de_limage = "python_properties_controleur"  # page 2 (e3) a faire #
        elif choix == 313:
            nom_de_limage = "python_properties_Thread_init"  # page 3 (arret roi, par matiere) a faire lore #
        elif choix == 25:
            nom_de_limage = "python_properties_controleur_Thread"  # page 4 (observatorium, par matiere) a faire secrets des observations #
        elif choix == 935284761:
            nom_de_limage = "python_properties_modele_Thread"  # page 5 (par tout talent combo talents) -
        elif choix == 9353918170:
            PlayMusic("abyss")
            print("Ce n'est pas encore l'heure.")
            services.Affichage.EntreePourContinuer()
            print("Contente toi de ceci pour l'instant.")
            services.Affichage.EntreePourContinuer()
            print("Menu Coliseum(OBSERVATORIUM) = Musiques")
            print("Menu Coliseum(OBSERVATORIUM(KEY)) = Plus de Musiques")
            services.Affichage.EntreePourContinuer()
            nom_de_limage = "python_properties_vue_Thread"  # page 13 (combo toutes pages donne seulement etage 0, etage 0 donne invitation.) a faire #
        elif choix == 14:
            nom_de_limage = "python_properties_modele"  # talent feu (e2) -
        elif choix == 151211913131214:
            nom_de_limage = "python_properties_modele_Anox"  # talent glace (e4) -
        elif choix == 1233:
            nom_de_limage = "python_properties_main"  # talent foudre (e7) -
        elif choix == 3236353:
            nom_de_limage = (
                "python_properties_main_Anox"  # talent terre (e5) quete ult -
            )
        elif choix == 1342:
            nom_de_limage = "python_properties_controleur_Anox"  # talent sang (e6) -
        elif choix in [5321139741, 7415321139]:
            nom_de_limage = "python_properties_vue_Anox"  # talent physique (e8) livre + notes de table des matières -   faire page 13 ==) pas maintenant

        dir_path = DOSSIER_RESSOURCES
        chemin_de_limage = dir_path + "\\__py.property__\\"
        open_image(f"{chemin_de_limage}{nom_de_limage}.xldr")
    else:
        print("                           Donnée Récupérée :")
        for _ in range (0, 21):
            print(
                "zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5"
            )
    services.Affichage.EntreePourContinuer()


def ShowObservatorium():
    """
    Affiche le menu de l'Observatorium et joue la musique choisie.
    Les musiques cachées sont débloquées via des codes secrets.
    """
    codes_deblocus = []
    LISTE_CODES_SECRETS = [11525, 2831805]
    PlayMusic("observatorium")

    # Construction du menu
    musiques_disponibles = construire_choix_observatorium(codes_deblocus)

    while True:

        # AFFICHAGE

        # Affichage du menu
        print("  ~~{ Observatorium }~~\n")
        for m in musiques_disponibles:
            print(f"{m['index']} - {m['nom_affiche']}")

        choix_str = input("\nChoisissez la musique avec le numéro ou entrez un code secret : ")
        ClearConsole()

        #--------------------------------------------------------------------------------------------
        #CONSEQUENCES DU CHOIX JOUEUR

        # vérifier que le joueur aie donné un nombre
        try:
            choix = int(choix_str)
        except ValueError:
            ClearConsole()
            continue

        # Vérifier si le joueur entre un code secret
        if choix in LISTE_CODES_SECRETS:
            if choix not in codes_deblocus:
                codes_deblocus.append(choix)
                StopAllMusic()
                if choix == 11525 :
                    print(
                        "Les confins de l'observatorium s'ouvrent a vous, voyageurs sur une mer d'encre a la recherche de la véritée.\nPrenez seulement garde a ne pas couler entre les lignes du code qui régit ce monde, ou vous pourriez bien ne jamais remonter à la surface."
                    )
                    services.Affichage.EntreePourContinuer()
                    PlayMusic("darkness")
                elif choix == 2831805 :
                    print(
                        "Les souvenirs de la mort emplissent la salle et font jaillir le sol impur d'une terre aride.\nSeuls celles et ceux qui ont foulé cette terre peuvent entendre le vide raconter avec entrain les combats auxquel il a assisté."
                    )
                    services.Affichage.EntreePourContinuer()
                    PlayMusic("alt_6_phase_1")
                musiques_disponibles = construire_choix_observatorium(codes_deblocus)
            continue

        # Retour
        if choix == 1:
            PlayMusic("start")
            break

        # Jouer la musique choisie
        musique_choisie = next((m for m in musiques_disponibles if m["index"] == choix), None)
        if musique_choisie and musique_choisie["fichier"]:
            PlayMusic(musique_choisie["fichier"])
            print(musique_choisie["description"])
            services.Affichage.EntreePourContinuer()
            if codes_deblocus[-1] == 11525:
                PlayMusic("darkness")
            if codes_deblocus[-1] == 2831805:
                PlayMusic("alt_6_phase_1")
            else:
                PlayMusic("observatorium")

        else:
            ClearConsole()


def construire_choix_observatorium(codes_deblocus):
    ClearConsole()
    # Construire la liste des musiques disponibles
    musiques_disponibles = [{"index": 1, "nom_affiche": "Retour", "fichier": None}]
        
    index = 2
    for musique in MUSIQUES_OBSERVATORIUM:
        code_secret = musique.get("code_deblocage")
        # Si pas de code secret ou code déjà débloqué, on l'affiche
        if code_secret is None or code_secret in codes_deblocus:
            musiques_disponibles.append({
                "index": index,
                "nom_affiche": musique["nom_affiche"],
                "fichier": musique["fichier"],
                "description": musique["description"]
            })
            index += 1

    return musiques_disponibles


def AffichageSecretPage3():
    try:
        dummy = {}
        dir_path = DOSSIER_RESSOURCES
        chemin_du_fichier_save = dir_path + "\\error.txt"
        with open(chemin_du_fichier_save, "r") as fichier:
            reader = csv.DictReader(fichier, delimiter="|")
            for line in reader:
                dummy[line["Caracteristique"]] = line["Valeur"]
        if dummy["error"] == "error":
            PlayMusic("abyss")
            numero = 0
            while True:
                print("ERREUR : VARIABLE VIE NON TROUVEE")
                print("ANCIENNES DONNEES TROUVEES, CHARGEMENT EN COURS...")
                print("ERREUR : ANCIENNES DONNEES EN COURS DUTILISATION")
                print("UTILISATION DES DONNEES AVEC UNE AUTRE VARIABLE VIE...")
                print(
                    "ERREUR : TEMPS DE JEU DES ANCIENNES DONNEES DEPASSE MEMOIRE VIVE DE LA MACHINE"
                )
                print("REBOOT DU PROGRAMME EN COURS....")
                print(
                    f"TENTATIVE NUMERO {numero} DE RESOLUTIONS DES (ERROR : OVERDRIVE) ERREURS EN COURS..."
                )
                if numero == 313:
                    break
                time.sleep(0.01)
                ClearConsole()
                numero += 1
            print("SOLUTION TROUVEE")
            print("SUPPRESSION DES DONNEES CORROMPUE TERMINEE")
            print("MESSAGE DE [ERROR : UNKNOWN] : continue. rapproche toi. bientôt.")
            services.Sove.RajouteEntreeAuLivreCigogneBlancheSiOnAPas("???", "ERRORLOG")
            services.Affichage.EntreePourContinuer()
            dir_path = DOSSIER_RESSOURCES
            chemin_du_fichier = dir_path + "\\error.txt"
            os.remove(chemin_du_fichier)
            ClearConsole()
    except FileNotFoundError:
        ClearConsole()
