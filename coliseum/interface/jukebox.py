"""Jukebox de l'étage 10 et piano."""

from collections import deque

from coliseum import services
from coliseum.audio import PlayMusic, PlayMusicDeLetage
from coliseum.console import ClearConsole


def DoJukebox():
    dictionnaire_musiques_jukebox = {
        1 : {"Nom" : "Exploratio", "Nom Réel" : "etage_1"},
        2 : {"Nom" : "Les Joies du Combat", "Nom Réel" : "battle_theme_1"},
        3 : {"Nom" : "Revenant", "Nom Réel" : "boss_1"},
        4 : {"Nom" : "Conte de Fée", "Nom Réel" : "etage_2"},
        5 : {"Nom" : "Epineuses Rencontres", "Nom Réel" : "battle_theme_2"},
        6 : {"Nom" : "Le Chevalier Qu'on Ne Veut Pas Rencontrer", "Nom Réel" : "boss_2"},
        7 : {"Nom" : "Affreux Fertile", "Nom Réel" : "etage_2_alt"},
        8 : {"Nom" : "Clair de Sang", "Nom Réel" : "battle_theme_2_alt"},
        9 : {"Nom" : "Néophobie Alimentaire", "Nom Réel" : "boss_2_alt"},
        10 : {"Nom" : "Loi de la Jungle", "Nom Réel" : "mimique_1"},
        11 : {"Nom" : "Ruines d'Antan", "Nom Réel" : "etage_3"},
        12 : {"Nom" : "Sables Mouvants", "Nom Réel" : "battle_theme_3"},
        13 : {"Nom" : "Euthanasie Régalienne", "Nom Réel" : "boss_3"},
        14 : {"Nom" : "Pāramitā", "Nom Réel" : "etage_4"},
        15 : {"Nom" : "Nerd Party", "Nom Réel" : "battle_theme_4"},
        16 : {"Nom" : "Jeux d'Enfants", "Nom Réel" : "boss_4"},
        17 : {"Nom" : "Pantomime", "Nom Réel" : "boss_4_phase_2"},
        18 : {"Nom" : "Sciences Infusées", "Nom Réel" : "mimique_2"},
        19 : {"Nom" : "Carnaval", "Nom Réel" : "etage_5"},
        20 : {"Nom" : "Piñata", "Nom Réel" : "battle_theme_5"},
        21 : {"Nom" : "Tragicomique", "Nom Réel" : "boss_5"},
        22 : {"Nom" : "Obituaire de Morphée", "Nom Réel" : "etage_5_alt"},
        23 : {"Nom" : "Chasseur D'Etoiles", "Nom Réel" : "battle_theme_5_alt"},
        24 : {"Nom" : "Memory Lane", "Nom Réel" : "boss_5_alt_intro"},
        25 : {"Nom" : "Symphonie des Coeurs Immolés", "Nom Réel" : "boss_5_alt"},
        26 : {"Nom" : "Combler les Vides", "Nom Réel" : "etage_6"},
        27 : {"Nom" : "Systèmes Défaillants", "Nom Réel" : "battle_theme_6"},
        28 : {"Nom" : "Sa Majesté Des Mouches", "Nom Réel" : "boss_6"},
        29 : {"Nom" : "Sauce au Poivre", "Nom Réel" : "mimique_3"},
        30 : {"Nom" : "Divin Karma", "Nom Réel" : "etage_7"},
        31 : {"Nom" : "Folie Furieuse", "Nom Réel" : "battle_theme_7"},
        32 : {"Nom" : "Comment Tuer le Grand Méchant Loup", "Nom Réel" : "boss_7"},
        33 : {"Nom" : "Le Prix des Larmes", "Nom Réel" : "etage_7_alt"},
        34 : {"Nom" : "Noblesse Oblige", "Nom Réel" : "battle_theme_7_alt"},
        35 : {"Nom" : "Coeur, Ego, Tango", "Nom Réel" : "boss_7_alt"},
        36 : {"Nom" : "Ossuaire Immaculé", "Nom Réel" : "etage_8"},
        37 : {"Nom" : "Dissonance Cognitive", "Nom Réel" : "battle_theme_8"},
        38 : {"Nom" : "Le Vieux Fourneau", "Nom Réel" : "boss_8"},
        39 : {"Nom" : "La Hache et le Grimoire", "Nom Réel" : "boss_8_phase_2"},
        40 : {"Nom" : "Révolution", "Nom Réel" : "boss_8_phase_2"},
        41 : {"Nom" : "Fièvre du Samedi Soir", "Nom Réel" : "dance"},
        42 : {"Nom" : "S1mul4crum", "Nom Réel" : "etage_0"},
        43 : {"Nom" : "Cruc1fix1on", "Nom Réel" : "boss_0"},
        44 : {"Nom" : "V3tus S4nct0rum", "Nom Réel" : "battle_theme_0"},
        45 : {"Nom" : "Réarr4ng3ment L1m1nal", "Nom Réel" : "etage_9"},
        46 : {"Nom" : "4rythm1e", "Nom Réel" : "battle_theme_9"},
        47 : {"Nom" : "Au Dé7our D’un S3nti3r Une Ch4rogn3 Infâme", "Nom Réel" : "boss_9"},
        48 : {"Nom" : "Th3 L4byr1nth Génés1s", "Nom Réel" : "etage_10"},
        49 : {"Nom" : "Sur l3 S3nt1er de l4 Gu3rr3", "Nom Réel" : "battle_theme_10"},
        50 : {"Nom" : "Ad Inf1n1tum", "Nom Réel" : "etage_10_alt"},
        51 : {"Nom" : "H0m0nculus", "Nom Réel" : "mimique_5"},
        52 : {"Nom" : "Endorphines", "Nom Réel" : "tutorial"},
        53 : {"Nom" : "Dangereuses Mélancolies", "Nom Réel" : "alfredproto"},
        54 : {"Nom" : "L'Orage avant la Tempête", "Nom Réel" : "boss_introV2"},
        55 : {"Nom" : "Sillages Sur Une Mer de Rêves", "Nom Réel" : "gravestone"},
        56 : {"Nom" : "Bêtise Humaine", "Nom Réel" : "reconfort"},
        57 : {"Nom" : "Esotériques Réflexions", "Nom Réel" : "debug"},
        
    }
    print("Vous frappez le sol de l'arène, et au lieu de monstres, une étrange machine sort du sol.")
    services.Affichage.EntreePourContinuer()
    print("Sur sa devanture, vous pouvez observer deux cadres régulant respectivement la musique actuelle de l'étage et sa musique de combat, ainsi qu'une vitre en dessous.")
    print("Placardé sur un des côtés de la machine, vous trouvez un papier jaunissant sur laquelle se trouve une liste de musiques ainsi que des codes qui leurs sont associés.")
    services.Affichage.EntreePourContinuer()
    print("Vous pouvez changer les musiques en sélectionnant un cadre et en entrant un code sur un pavé numérique a coté.")
    services.Affichage.EntreePourContinuer()
    
    while True:
        while True:
            try:
                # attribue le code actuel a un nom
                for cle in dictionnaire_musiques_jukebox:
                    if dictionnaire_musiques_jukebox[cle]["Nom Réel"] == services.Player.musique_etage_10:
                        nom_musique_etage = dictionnaire_musiques_jukebox[cle]["Nom"]
                        break
                for cle in dictionnaire_musiques_jukebox:
                    if dictionnaire_musiques_jukebox[cle]["Nom Réel"] == services.Player.musique_combat_10:
                        nom_musique_combat = dictionnaire_musiques_jukebox[cle]["Nom"]
                        break

                # affichage
                print(f"Musique de l'étage : [{nom_musique_etage}]")
                print(f"Musique des combats : [{nom_musique_combat}]")
                print("\n1 - Changer la musique de l'étage")
                print("2 - Changer la musique des combats")
                print("3 - Partir")
                print("4 - Désactiver le mode jukebox et partir")
                choix = int(input("(Faites votre choix avec les numéros :) "))
                ClearConsole()

                if choix in [1, 2, 3, 4]:
                    break
            except ValueError:
                ClearConsole()
        
        if choix == 3:
            print("Vous laissez le jukebox derrière vous, et il retourne dans le sol de l'arène.")
            services.Affichage.EntreePourContinuer()
            break

        elif choix == 4:
            print("Mode Jukebox Désactivé")
            services.Player.mode_jukebox = False
            PlayMusicDeLetage()
            print("Vous laissez le jukebox derrière vous, et il retourne dans le sol de l'arène.")
            services.Affichage.EntreePourContinuer()
            break

        elif choix == 2:
            choix_effectue = False
            while not choix_effectue:
                while True:
                    try:
                        print("Choix de la musique des combats :")
                        for numero in dictionnaire_musiques_jukebox:
                            print(f"{numero} - {dictionnaire_musiques_jukebox[numero]['Nom']}")
                        choix = int(input("\n(Faites votre choix avec les numéros :) "))
                        ClearConsole()
                        if choix in range (1, len(dictionnaire_musiques_jukebox)+1):
                            break
                    except ValueError:
                        ClearConsole()
                PlayMusic(dictionnaire_musiques_jukebox[choix]['Nom Réel'])
                while True:
                    try:
                        print(f"Vous avez choisi la musique de combat suivante : [{dictionnaire_musiques_jukebox[choix]['Nom']}]")
                        print("\nValidez-vous votre choix ?")
                        print("1 - Oui")
                        print("2 - Non")
                        choix_validation = int(input("(Faites votre choix avec les numéros :) "))
                        ClearConsole()
                        if choix_validation == 1 :
                            choix_effectue = True
                            services.Player.musique_combat_10 = dictionnaire_musiques_jukebox[choix]["Nom Réel"]
                            PlayMusicDeLetage()
                            print("A travers la vitre, vous voyez un bras méchanique prendre un disque noir comme le charbon et le poser sous la plaque.")
                            print("Une pointe venue d'en bas se pose dessus.")
                            print("Mais curieusement, le disque ne tourne pas.")
                            services.Affichage.EntreePourContinuer()
                            break
                        elif choix_validation == 2:
                            PlayMusicDeLetage()
                            break
                    except ValueError:
                        ClearConsole()
                    
        elif choix == 1:
            choix_effectue = False
            while not choix_effectue:
                while True:
                    try:
                        print("Choix de la musique de l'étage :")
                        for numero in dictionnaire_musiques_jukebox:
                            print(f"{numero} - {dictionnaire_musiques_jukebox[numero]['Nom']}")
                        choix = int(input("(Faites votre choix avec les numéros :) "))
                        ClearConsole()
                        if choix in range (1, len(dictionnaire_musiques_jukebox)+1):
                            break
                    except ValueError:
                        ClearConsole()
                PlayMusic(dictionnaire_musiques_jukebox[choix]["Nom Réel"])
                while True:
                    try:
                        print(f"Vous avez choisi la musique d'étage suivante : [{dictionnaire_musiques_jukebox[choix]['Nom']}]")
                        print("\nValidez-vous votre choix ?")
                        print("1 - Oui")
                        print("2 - Non")
                        choix_validation = int(input("(Faites votre choix avec les numéros :) "))
                        ClearConsole()
                        if choix_validation == 1 :
                            choix_effectue = True
                            services.Player.musique_etage_10 = dictionnaire_musiques_jukebox[choix]["Nom Réel"]
                            print("A travers la vitre, vous voyez un bras méchanique prendre un disque noir comme le charbon et le poser sur la plaque.")
                            print("Le disque tourne, et une pointe se pose dessus.")
                            print("La musique remplit alors l'étage.")
                            services.Affichage.EntreePourContinuer()
                            break
                        elif choix_validation == 2:
                            PlayMusicDeLetage()
                            break
                    except ValueError:
                        ClearConsole()


def doPiano():
    """
    Attend que l'utilisateur entre une lettre de A à Z (majuscule ou minuscule)
    ou le chiffre '1' pour quitter. Stocke les entrées dans une FIFO de taille 36.
    Retourne True si la séquence des dernières lettres correspond à target_sequence.
    Retourne False si l'utilisateur tape '1'.
    """
    # Normaliser la séquence cible en minuscules
    target_sequence = list("pbvpopxyixciopozppbvpnmmnmvcpccvbn")

    # FIFO de taille max 36
    buffer = deque(maxlen=len(target_sequence))

    while True:
        # Demande à l'utilisateur
        entry = input("Tapez une lettre correspondant à la note à jouer, ou 1 pour quitter : ").strip()

        # Quitter si '1'
        if entry == "1":
            return False

        # Vérifier que c'est bien une lettre A-Z
        if len(entry) == 1 and entry.isalpha():
            buffer.append(entry.lower())  # On stocke en minuscule
        else:
            ClearConsole()
            print("Vous tapez dans le vide sur une touche inexistante.")
            print("Vous avez l'air stupide.")
            print("Vous devriez laisser le clavecin à quelqu'un qui s'y connait mieux.")
            services.Affichage.EntreePourContinuer()
            continue

        # Vérifier si la séquence correspond
        if list(buffer) == target_sequence:
            return True
