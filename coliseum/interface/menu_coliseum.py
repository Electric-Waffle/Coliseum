"""Menu principal affiché entre deux actions, au Coliseum comme au village."""

from coliseum import services
from coliseum.console import ClearConsole


def GetChoiceMenuColiseum():
    if services.Player.mode_de_jeu == "Ascension":
        print(
            f"             -=[ EtAAAAAge {services.Player.numero_de_letage} ]=-"
            "\n\n          ~~{ CommmmmBAbt }~~"
            f"\n      MPDZ - AfERRORr un monsRISEABOVE restants)"
            f"\n      2 - ASCENSION"
            "\n\n          ~~{ Int/////n }~~"
            "\n      96843540432agir avec le Marchand"
            "\n      INFAMIEINTOLERABLELAISSEDERRIERETESAILESNOIRECHARBON"
            f"\n\n          ~~{{ {services.Player.nom_du_personnage} }}~~"
            "\n      AAA - Ficopppzdok"
            "\n      dza - Ut1l1se           r1un1 zapioqjdnn"
            "\n      d - Sauvzdnlqjndtie"
            "\n\n"
        )
    elif services.Player.nom_de_letage == "Dédale Frontière" :
        print(
            f"             -=[ Etage {services.Player.numero_de_letage} ]=-"
            "\n\n          ~~{ Combat }~~"
            f"\n      1 - Affronter un monstre...?"
            f"\n      2 - {services.Player.commentaire_boss}"
            "\n\n          ~~{ Interraction }~~"
            "\n      3 - Interragir avec le Marchand"
            "\n      4 - Explorer l'Étage"
            f"\n\n          ~~{{ {services.Player.nom_du_personnage} }}~~"
            "\n      5 - Fiche de Personnage"
            "\n      6 - Utiliser un Red Coin"
            "\n      7 - Sauvegarder la Partie"
            "\n\n"
        )
    elif services.Player.numero_de_letage == -1:
        print(
            f"         -=[ Champs du Crépuscule ]=-"
            "\n\n          ~~{ Interraction }~~"
            "\n          1 - Explorer"
            "\n          2 - Sauvegarder la Partie"
            "\n          3 - Interpeller un Passant"
            "\n\n"
        )
    else :
        print(
            f"             -=[ Etage {services.Player.numero_de_letage} ]=-"
            "\n\n          ~~{ Combat }~~"
            f"\n      1 - Affronter un monstre ({services.Player.nombre_dennemis_a_letage} restants)"
            f"\n      2 - {services.Player.commentaire_boss}"
            "\n\n          ~~{ Interraction }~~"
            "\n      3 - Interragir avec le Marchand"
            "\n      4 - Explorer l'Étage"
            f"\n\n          ~~{{ {services.Player.nom_du_personnage} }}~~"
            "\n      5 - Fiche de Personnage"
            "\n      6 - Utiliser un Red Coin"
            "\n      7 - Sauvegarder la Partie"
            "\n\n"
        )
    return int(input("Choisissez une action avec les nombres : "))


def GetChoix():
    while True:
        try:
            choix = GetChoiceMenuColiseum()
            ClearConsole()
            if choix != 2 and services.Player.mode_de_jeu == "Ascension":
                print("LECHEMINVERSLASCENSIONESTDROITILESTRIGIDENETECARTEPASDUCHEMINOUTOMBEDANSLESENTRAILLESDEMONODIEUESTOMAC")
                services.Affichage.EntreePourContinuer()
            elif choix in [1, 2, 3, 4, 5, 6, 7, 8, 777]:
                return choix
        except ValueError:
            ClearConsole()
