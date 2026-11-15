"""Boucle principale du jeu : tout ce qui se passe hors combat.

FLUX :
1. `lancer_le_jeu` ouvre l'audio, crée les objets uniques (services), lit les
   sauvegardes et affiche le menu de démarrage.
2. Puis, en boucle : le menu demande un numéro au joueur, et ce numéro est
   traduit en action.
3. Le joueur est soit au Coliseum (étages 0 à 11), soit au village (étage -1).
   Les deux lieux partagent la même carte à explorer (FloorMaker.ShowFloor) ;
   seul le menu autour change, d'où deux tables d'actions.

PATTERN : table de dispatch. Chaque menu est un dictionnaire
{numéro tapé: fonction à appeler}. Ajouter une entrée de menu = écrire une
fonction et l'inscrire dans la table, sans toucher à la boucle.
"""

import sys
import time

from coliseum import audio, services
from coliseum.audio import PlayMusic, PlayMusicDeLetage, StopAllMusic
from coliseum.combat.lancement import DoFight
from coliseum.console import ClearConsole
from coliseum.erreurs import WriteErrorInErrorLog
from coliseum.exploration.progression import DoBossOrGoDown
from coliseum.histoire.boss_zero import DoBossZero
from coliseum.histoire.village import PrepareTheVillage
from coliseum.interface.jukebox import DoJukebox
from coliseum.interface.menu_coliseum import GetChoix
from coliseum.interface.menu_debug import ShowDebugMenu
from coliseum.interface.menu_demarrage import MenuDeDemarrage
from coliseum.interface.secrets import AffichageSecretPage3
from coliseum.joueur.talents import DoRedcoin
from coliseum.sauvegarde.partie import GetNomEtageEtDebugValues, SetupGameMode

ETAGE_DU_VILLAGE = -1
ETAGE_DU_SACRIFICE = 0
ETAGE_DU_DEDALE = 10


def lancer_le_jeu():
    audio.initialiser()
    StopAllMusic()
    services.initialiser()

    SetupGameMode()
    AffichageSecretPage3()
    GetNomEtageEtDebugValues()
    if services.Player.mode_de_jeu == "Erreur":
        _signaler_sauvegarde_permanente_introuvable()
        sys.exit()

    MenuDeDemarrage()
    _lancer_la_musique_du_lieu()
    while True:
        _jouer_une_action()


def _signaler_sauvegarde_permanente_introuvable():
    print("ERREUR 404: FICHIER DE SAUVEGARDE PERMANENT INTROUVABLE")
    print("ASSUREZ VOUS D'AVOIR UN FICHIER NOMME S0VE.TXT DANS COLISEUMDEPENDENCIES")
    services.Affichage.EntreePourContinuer()


def _lancer_la_musique_du_lieu():
    if services.Player.numero_de_letage == ETAGE_DU_VILLAGE:
        StopAllMusic()
        PlayMusic("wind")
    else:
        PlayMusicDeLetage()


def _jouer_une_action():
    # ATTENTION : rappeler __init__ recalcule `can_draw` à partir de la
    # sauvegarde permanente, qui a pu changer pendant l'action précédente.
    services.Draw.__init__()
    choix = GetChoix()
    if services.Player.numero_de_letage == ETAGE_DU_VILLAGE:
        _executer(ACTIONS_DU_VILLAGE, choix)
    else:
        _executer(ACTIONS_DU_COLISEUM, choix)
        _envoyer_au_village_si_la_partie_est_terminee()


def _executer(table_des_actions, choix):
    action = table_des_actions.get(choix)
    if action is not None:
        action()


def _envoyer_au_village_si_la_partie_est_terminee():
    tags = services.Player.player_tags
    if "Fantome" in tags or "Jeu Fini" in tags:
        try:
            PrepareTheVillage()
        except Exception as error:
            WriteErrorInErrorLog(error)


# ---------------------------------------------------------------- village


def _parler_aux_villageois():
    if services.Sove.ModifieTagsDansSove("Checke", "Village Jour"):
        services.Affichage.ParleAuPnj()
    else:
        services.Affichage.ParleAuPnjNuit()


# --------------------------------------------------------------- coliseum


def _le_joueur_est_confus():
    """Pendant le combat contre le Gardien, la moitié du menu est inutilisable."""
    return "Combattant le Gardien" in services.Player.player_tags


def _raconter(*phrases):
    for phrase in phrases:
        print(phrase)
        services.Affichage.EntreePourContinuer()


def _combattre_dans_l_arene():
    joueur = services.Player
    if joueur.nom_de_letage == "Limbes Flétrissants":
        _raconter(
            "Vous cherchez une arène, ou quelque chose dans le genre, et ne trouvez que le champ de terre battu.",
            "Frapper le sol stérile ne fait rien apparaitre.",
        )
    elif joueur.numero_de_letage == ETAGE_DU_SACRIFICE:
        _raconter("Vous frappez le sol de l'arène, mais rien ne se passe.")
    elif joueur.numero_de_letage != ETAGE_DU_DEDALE:
        DoFight()
    else:
        DoJukebox()


def _affronter_le_boss_ou_descendre():
    joueur = services.Player
    if joueur.numero_de_letage == ETAGE_DU_SACRIFICE and not joueur.battu_le_sacrifie:
        DoBossZero()
    elif not DoBossOrGoDown():
        joueur.player_tags.append("Jeu Fini")
        services.Ending.DoEnding()


def _voir_le_marchand():
    joueur = services.Player
    if joueur.numero_de_letage == ETAGE_DU_SACRIFICE:
        print("Vous vous approchez de l'endroit ou se trouve le marchand...")
        print("...mais il n'y a personne.")
        services.Affichage.EntreePourContinuer()
    elif joueur.nom_de_letage == "Limbes Flétrissants":
        print("Vous cherchez le marchand...")
        print("...mais ne trouvez personne.")
        services.Affichage.EntreePourContinuer()
    else:
        services.Trader.DoTrading()


def _ouvrir_la_fiche_de_personnage():
    if _le_joueur_est_confus():
        _raconter(
            "Vous sortez votre sacoche, mais vous n'arrivez pas a vous souvenir comment utiliser vos objets "
            "ou vos sorts avec votre esprit confus, alors vous la raccrochez à sa place."
        )
    else:
        services.Player.ShowPlayerCaracteristicsAndItems()


def _depenser_les_redcoins():
    if _le_joueur_est_confus():
        _raconter("Vous cherchez vos redcoins, mais votre esprit confus vous empeche de trouver quoi que ce soit.")
    else:
        DoRedcoin()


def _sauvegarder():
    if _le_joueur_est_confus():
        _afficher_une_fausse_erreur()
    else:
        services.Save.SaveTheGame()


def _afficher_une_fausse_erreur():
    print("[ERREUR :", end=" ", flush=True)
    for _ in range(200):
        print("ERREUR :", end=" ", flush=True)
        time.sleep(0.01)
    print("]", flush=True)
    ClearConsole()


def _ouvrir_le_menu_de_debug():
    ShowDebugMenu()
    services.Save.SaveTheGameSansAffichage()


def _ouvrir_le_jukebox():
    if not services.Player.mode_jukebox:
        print("Mode Jukebox Activé")
        services.Player.mode_jukebox = True
        PlayMusicDeLetage()
        services.Affichage.EntreePourContinuer()
    DoJukebox()


# CONCEPT : `lambda` retarde la lecture de `services.X`. Écrire directement
# `services.FloorMaker.ShowFloor` ici lirait l'annuaire au chargement du module,
# alors que les objets ne sont créés que plus tard par `services.initialiser()`.
ACTIONS_DU_VILLAGE = {
    1: lambda: services.FloorMaker.ShowFloor(),
    2: lambda: services.Save.SaveTheGame(),
    3: _parler_aux_villageois,
}

ACTIONS_DU_COLISEUM = {
    1: _combattre_dans_l_arene,
    2: _affronter_le_boss_ou_descendre,
    3: _voir_le_marchand,
    4: lambda: services.FloorMaker.ShowFloor(),
    5: _ouvrir_la_fiche_de_personnage,
    6: _depenser_les_redcoins,
    7: _sauvegarder,
    8: _ouvrir_le_menu_de_debug,
    777: _ouvrir_le_jukebox,
}
