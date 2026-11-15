"""Gestion des erreurs : deux filets de sécurité, à deux niveaux différents.

1. `WriteErrorInErrorLog` : filet LOCAL. Un combat ou une salle a planté, mais le
   jeu peut continuer. On note l'erreur, on dédommage le joueur, la partie reprend.
2. `executer_avec_rapport_de_crash` : filet GLOBAL, posé une seule fois autour
   du jeu entier par Coliseum.py. Il ne se déclenche que si une erreur remonte
   jusqu'en haut, c'est à dire quand le jeu aurait planté.

POURQUOI : l'ancien Coliseum.py lançait main.py dans un sous-processus, puis
affichait toujours ses messages d'alerte, que le jeu ait planté ou que le joueur
ait simplement choisi « Quitter ». Il ne pouvait pas faire la différence : vu de
l'extérieur, un processus terminé est un processus terminé.
Ici, la différence est faite par le TYPE de l'exception (voir le CONCEPT plus bas).
"""

import time
import traceback

from coliseum import services
from coliseum.chemins import JOURNAL_DES_ERREURS

CODE_SORTIE_NORMALE = 0
CODE_SORTIE_CRASH = 1

_SEPARATEUR = "-" * 176


def ecrire_dans_le_journal():
    """Ajoute au journal la trace de l'exception en cours de traitement.

    ATTENTION : à appeler uniquement depuis un bloc `except`. C'est
    `traceback.format_exc()` qui retrouve l'exception en cours ; hors d'un
    `except`, il n'y en a pas et la trace serait vide.
    """
    date_et_heure = time.strftime("%Y-%m-%d %H:%M")
    with open(JOURNAL_DES_ERREURS, "a") as fichier:
        fichier.write(f"{_SEPARATEUR}\n{date_et_heure}\nDébut du Log\n\n")
        fichier.write(traceback.format_exc())
        fichier.write(f"\nFin du Log\n{_SEPARATEUR}\n")


def WriteErrorInErrorLog(erreur):
    """Filet local : note l'erreur, soigne et dédommage le joueur, la partie continue.

    Appelée depuis un `except Exception` autour d'un combat ou d'une salle.
    """
    ecrire_dans_le_journal()
    print("Une erreur est survenue pendant le déroulement du combat.")
    print(
        "L'écriture d'un rapport d'erreur est en cours dans le fichier ColiseumDependenciesErrorLog.txt."
    )
    print("Veuilez patienter 3 secondes...")
    time.sleep(3)
    services.Affichage.EntreePourContinuer()
    _dedommager_le_joueur()


def _dedommager_le_joueur():
    joueur = services.Player
    joueur.points_de_vie = joueur.points_de_vie_max
    joueur.points_de_mana = joueur.points_de_mana_max
    print("Vous avez récupéré tout vos pv.")
    print("Vous avez récupéré tout vos pm.")
    gold_gagne = joueur.AddGoldToPlayer(30 * joueur.numero_de_letage, True)
    print("Le nombre de monstres restant à l'étage n'a pas changé.")
    print(f"Nous vous donnons {gold_gagne} golds en guise de réparation.")
    print("Veuillez nous excuser pour le dérangement.")
    services.Affichage.EntreePourContinuer()


def executer_avec_rapport_de_crash(lancer):
    """Filet global : exécute `lancer()` et ne réagit que si le jeu plante.

    Retourne le code de sortie du programme (0 = tout va bien, 1 = crash).

    CONCEPT : la hiérarchie des exceptions Python fait le tri à notre place.

        BaseException
         ├── SystemExit          <- levée par sys.exit() : le joueur quitte
         ├── KeyboardInterrupt   <- Ctrl+C
         └── Exception           <- toutes les « vraies » erreurs (bugs)

    `except Exception` n'attrape donc PAS `sys.exit()` : quitter depuis le menu
    de sauvegarde traverse ce filet sans le déclencher, et la fenêtre se ferme.
    C'est pour ça qu'il ne faut jamais écrire un `except:` nu ou un
    `except BaseException:` ici : ils avaleraient aussi la sortie volontaire.
    """
    try:
        lancer()
    except KeyboardInterrupt:
        # Ctrl+C est une sortie volontaire, pas un bug : on ne journalise rien.
        return CODE_SORTIE_NORMALE
    except Exception:
        _rapporter_le_crash()
        return CODE_SORTIE_CRASH
    return CODE_SORTIE_NORMALE


def _rapporter_le_crash():
    trace = traceback.format_exc()
    journal_ecrit = _essayer_d_ecrire_dans_le_journal()
    print("\n\n" + "=" * 70)
    print("Le jeu a rencontré une erreur et doit se fermer.")
    print("=" * 70 + "\n")
    print(trace)
    if journal_ecrit:
        print(f"Ce rapport a été enregistré dans :\n{JOURNAL_DES_ERREURS}")
    else:
        print("Le rapport n'a pas pu être enregistré : copiez le texte ci-dessus.")
    _attendre_que_le_joueur_ait_lu()


def _essayer_d_ecrire_dans_le_journal():
    # POURQUOI : si le disque est plein ou le fichier verrouillé, l'écriture du
    # journal échoue à son tour. Cette seconde erreur ne doit pas masquer la
    # première, qui est celle que le joueur doit voir.
    try:
        ecrire_dans_le_journal()
    except OSError:
        return False
    return True


def _attendre_que_le_joueur_ait_lu():
    # Lancé par double-clic, le jeu tourne dans une console qui se ferme avec
    # lui : sans cette pause, le rapport disparaîtrait avant d'être lu.
    try:
        input("\nAppuyez sur entrée pour fermer la fenêtre : ")
    except (EOFError, KeyboardInterrupt):
        pass
