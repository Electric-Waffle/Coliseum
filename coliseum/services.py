"""Annuaire des objets uniques du jeu (joueur, affichage, étage, marchand...).

PATTERN : Service Locator. Chaque module qui a besoin du joueur écrit
`services.Player` au lieu de recevoir le joueur en paramètre.

POURQUOI : dans l'ancien main.py, ces neuf objets étaient des variables globales
créées en bas du fichier, et toutes les classes se les partageaient. Elles se
connaissent toutes mutuellement (le joueur affiche, l'affichage lit le joueur,
l'étage appelle le marchand qui appelle l'étage...). L'injection par constructeur,
plus propre, est impossible tant que ces cycles existent : pour construire A il
faudrait B, et pour construire B il faudrait A.
C'est le même compromis que d'appeler `$container->get('service')` dans Symfony
au lieu d'utiliser l'autowiring : ça fonctionne, mais les dépendances d'une classe
ne se lisent plus dans sa signature. Le combat, lui, reçoit déjà ses dépendances
par constructeur (voir combat/lancement.py) : c'est la direction à suivre quand
une classe sera découplée des autres.

ATTENTION : il faut écrire `services.Player.x`, jamais `from coliseum.services
import Player`. La seconde forme copie la valeur au moment de l'import, c'est à
dire `None`, et ne verrait jamais l'objet créé ensuite par `initialiser()`.
"""

Sove = None
Save = None
Observation = None
Player = None
Draw = None
Affichage = None
FloorMaker = None
Ending = None
Trader = None


def initialiser():
    """Crée les objets uniques. Appelée une seule fois, au lancement du jeu.

    ATTENTION : l'ordre de création compte. Certains constructeurs lisent des
    objets créés avant eux (le marchand lit l'étage du joueur pour fixer ses
    prix, le dessin lit la sauvegarde permanente). Chaque objet est donc publié
    dans l'annuaire dès sa création, sans attendre la fin de la fonction.
    """
    global Sove, Save, Observation, Player, Draw, Affichage, FloorMaker, Ending, Trader

    # CONCEPT : imports faits dans la fonction et non en haut du fichier. Ces
    # modules importent eux-mêmes `services` ; les importer ici, au moment de
    # l'appel, évite un import circulaire au chargement.
    from coliseum.commerce.marchand import TraderUsage
    from coliseum.exploration.etage import Floor
    from coliseum.exploration.observation import Observe
    from coliseum.histoire.fin import EndingAndGift
    from coliseum.interface.affichage import Affiche
    from coliseum.interface.dessin import DrawInTurtle
    from coliseum.joueur.caracteristiques import PlayerCaracteristics
    from coliseum.sauvegarde.partie import SaveManagement
    from coliseum.sauvegarde.permanente import SoveManagement

    Sove = SoveManagement()
    Save = SaveManagement()
    Observation = Observe()
    Player = PlayerCaracteristics()
    Draw = DrawInTurtle()
    Affichage = Affiche()
    FloorMaker = Floor()
    Ending = EndingAndGift()
    Trader = TraderUsage()
