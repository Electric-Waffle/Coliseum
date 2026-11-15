"""Menu de debug : réglage des bonus d'équilibrage."""

from coliseum import services
from coliseum.audio import PlayMusic, PlayMusicDeLetage
from coliseum.console import ClearConsole
from coliseum.donnees.debug import DEBUG_OPTIONS


def ShowDebugMenu():
    PlayMusic("debug")

    while True:
        while True:
            try:
                print("Behind the screen : Debug Menu\n")
                print("0 - Quitter\n")
                print("1 - Réinitialiser les valeurs\n")
                for i, label in enumerate(DEBUG_OPTIONS, start=2):
                    attr = DEBUG_OPTIONS[label]
                    val = getattr(services.Player, attr)
                    print(f"{i} - Configurer [{label}] (Actuellement : {val}%)")
                print(f"\n{i+1} - Configurer les Caractéristiques du Joueur")
                choix = int(input("\nChoisissez une action avec son nombre correspondant : "))
                ClearConsole()
                if 0 <= choix <= (len(DEBUG_OPTIONS) + 2):
                    break
            except ValueError:
                ClearConsole()

        if choix == 0:
            PlayMusicDeLetage()
            break

        elif choix == 1:
            # réinitialisation a 0
            for attribute_name in DEBUG_OPTIONS:
                setattr(services.Player, DEBUG_OPTIONS[attribute_name], 0)

            # sauf pour certaines choses
            setattr(services.Player, "debug_bonus_equilibrage_technique", 35)
            setattr(services.Player, "debug_bonus_equilibrage_sort", 35)

        elif choix == (len(DEBUG_OPTIONS) + 2):
            attributs_modifiables = [
                ("points_de_vie", "Points de vie"),
                ("points_de_vie_max", "Points de vie max"),
                ("points_de_mana", "Points de mana"),
                ("points_de_mana_max", "Points de mana max"),
                ("points_dendurance", "Points d'endurance"),
                ("points_de_force", "Points de force"),
                ("points_dintelligence", "Points d'intelligence"),
                ("points_de_defence", "Points de défense"),
                ("nombre_de_gold", "Nombre de gold"),
                ("nombre_de_red_coin", "Nombre de redcoin"),
                ("nombre_de_monstres_tues", "Nombre d'âmes récupérées"),
                ("taux_coup_critique", "Chance de faire une technique critique"),
                ("degat_coup_critique", "Dégâts supplémentaires d'une technique critique"),
                ("taux_sort_critique", "Chance de faire un sort critique"),
                ("degat_sort_critique", "Dégâts supplémentaires d'un sort critique")
            ]

            while True:
                while True:
                    try:
                        print("Behind the screen : Character Values\n")
                        print("0 - Retourner au menu principal\n")
                        for i, (attr, nom_affichage) in enumerate(attributs_modifiables, start=1):
                            valeur_actuelle = getattr(services.Player, attr)
                            print(f"{i} - Configurer [{nom_affichage}] (Actuellement : {valeur_actuelle})")
                        choix = int(input("\nChoisissez une action avec son nombre correspondant : "))
                        ClearConsole()
                        if choix in range(0, len(attributs_modifiables) + 1):
                            break
                    except ValueError:
                        ClearConsole()

                if choix == 0:
                    break

                attr_name, nom_affichage = attributs_modifiables[choix - 1]

                while True:
                    try:
                        valeur_actuelle = getattr(services.Player, attr_name)
                        print(f"Behind the screen : Modifier {nom_affichage} (Actuellement : {valeur_actuelle})\n")
                        nouvelle_valeur = int(input("Entrez une nouvelle valeur (négative ou positive) : "))
                        setattr(services.Player, attr_name, nouvelle_valeur)
                        ClearConsole()
                        break
                    except ValueError:
                        ClearConsole()


            


        else:
            # Récupération dynamique de la variable choisie
            label = list(DEBUG_OPTIONS.keys())[choix - 2]
            attr = DEBUG_OPTIONS[label]

            while True:
                try:
                    val_actuel = getattr(services.Player, attr)
                    print(f"Configurer [{label}] (Actuellement : {val_actuel}%)\n\n")
                    nouveau_val = int(input("Nouveau pourcentage (positif ou négatif) : "))
                    setattr(services.Player, attr, nouveau_val)
                    ClearConsole()
                    break
                except ValueError:
                    ClearConsole()
