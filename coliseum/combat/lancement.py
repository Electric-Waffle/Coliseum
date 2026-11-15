"""Lancement d'un combat depuis le reste du jeu.

FLUX : le jeu hors combat (arène, salles de l'étage, histoire) appelle
`livrer_combat()`. Le contrôleur de combat est créé avec les objets dont il a
besoin, la musique de l'étage est coupée, puis `Battle()` déroule le combat
jusqu'à la victoire, la fuite ou la mort. Le résultat est écrit par le combat
directement dans le joueur (vie, gold, tags comme "KIA").

POURQUOI : ce bloc existait en vingt exemplaires copiés-collés. Un seul
exemplaire, c'est un seul endroit à modifier quand le lancement change.
"""

from coliseum import audio, services
from coliseum.audio import PlayMusicDeLetage, StopAllMusic
from coliseum.combat import controleur
from coliseum.erreurs import WriteErrorInErrorLog
from coliseum.histoire.village import CheckForKIA


def combattre():
    """Livre un combat. Une erreur pendant le combat remonte à l'appelant."""
    # PATTERN : injection de dépendances par constructeur. Le combat ne va pas
    # chercher le joueur ou l'étage dans `services` : il les reçoit ici.
    control = controleur.Control(services.Player, services.Trader, services.FloorMaker, services.Sove)
    audio.couper_la_musique_de_fond()
    control.Battle()
    StopAllMusic()


def livrer_combat():
    """Livre un combat sous filet de sécurité. Retourne True s'il s'est déroulé sans erreur.

    Si le combat plante, l'erreur est journalisée, le joueur est dédommagé et
    la partie continue : l'appelant reçoit False et ne doit pas considérer le
    monstre comme vaincu.
    """
    try:
        combattre()
    except Exception as error:
        WriteErrorInErrorLog(error)
        return False
    return True


def DoFight():
    # combat contre ennemi
    if services.Player.nombre_dennemis_a_letage != 0:
        services.Affichage.AfficheIntroCombat()
        if livrer_combat():
            services.Player.nombre_dennemis_a_letage -= 1
        CheckForKIA()
        if not "Fantome" in services.Player.player_tags:
            PlayMusicDeLetage()
    # plus dennemi a combattre
    else:
        services.Affichage.AffichePlusDennemis()


def DoBossFight():
    if services.Player.possede_la_cle:
        if services.Player.nom_de_letage == "Dédale Frontière" :
            StopAllMusic()
            services.Player.boss_battu = True
            services.Player.commentaire_boss = "Descendre a l'étage inferieur"
            print("Vous vous approchez prudemment de la grille, attendant un boss a la hauteur du labyrinthe que vous venez de conquérir, cepandant...")
            services.Affichage.EntreePourContinuer()
            print("...personne ne vient.")
            services.Affichage.EntreePourContinuer()
            print("Vous entendez la voix de Jean dans votre esprit :")
            services.Affichage.EntreePourContinuer()
            print("*Ca aurait du être moi. Mais tu m'a libéré avant qu'il puisse me récolter.*")
            services.Affichage.EntreePourContinuer()
            print("*Prend donc cette pause comme un cadeau et prépare toi bien avant de descendre.*")
            services.Affichage.EntreePourContinuer()
            PlayMusicDeLetage()
        else:
            services.Affichage.AfficheIntroCombatBoss()
            services.Player.affronte_un_boss = True
            if livrer_combat():
                services.Player.affronte_un_boss = False
                services.Player.boss_battu = True
                services.Player.commentaire_boss = "Descendre a l'étage inferieur"
            if "Boss Blessé" in services.Player.player_tags:
                services.Player.player_tags.remove("Boss Blessé")
                
            CheckForKIA()
            if not "Fantome" in services.Player.player_tags:
                PlayMusicDeLetage()
    else:
        if services.Player.nom_de_letage == "Limbes Flétrissants":
            print("Vous cherchez un moyen de descendre , ou d'affronter un boss, mais ne trouvez rien.")
            services.Affichage.EntreePourContinuer()
            print("Peut être n'avez vous pas observé l'étage suffisamment ?")
            services.Affichage.EntreePourContinuer()
        else:
            print(
                "Vous rentrez dans l'arène et jettez un coup d'oeil aux tribunes vides, avant de donner un coup de pied sur le sol."
            )
            services.Affichage.EntreePourContinuer()
            print("Mais rien ne se produit.")
            services.Affichage.EntreePourContinuer()
            print(
                "Une grille de métal ancien a l'autre bout de l'arène attire votre regard."
            )
            print(
                "Derriere ses barreaux imposants, vous pouvez apercevoir un escalier s'enfoncant dans les ténèbres."
            )
            services.Affichage.EntreePourContinuer()
            print("Cepandant, la grille ne semble pas posséder de serrure.")
            print(
                "Peut-etre pourriez vous trouver, quelque part dans l'étage, un moyen de l'ouvrir ?"
            )
            services.Affichage.EntreePourContinuer()
