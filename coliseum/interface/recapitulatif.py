"""Récapitulatifs du joueur et du monstre, montrés en haut de la fenêtre du jeu.

FLUX : la fenêtre (coliseum/terminal/fenetre.py) appelle `recap_du_joueur()`
et `recap_du_monstre()` plusieurs fois par seconde. Chaque appel relit l'état
du jeu et retourne un `Recap` : une simple description de ce qu'il faut
afficher. La fenêtre compare ce `Recap` au précédent et ne redessine que s'il
a changé. C'est ce qui donne le suivi « en temps réel ».

PATTERN : sondage (polling). Le jeu ne prévient pas l'écran quand une valeur
change : c'est l'écran qui vient lire.
POURQUOI : la vie du joueur est modifiée à plusieurs centaines d'endroits du
code. Prévenir l'écran à chaque fois (pattern Observer) demanderait de
retoucher chacun d'eux, et d'y penser à chaque nouvelle attaque. En relisant
l'état, aucun code existant ni futur n'a besoin de savoir que le récap existe.

POURQUOI ce module ne dessine rien : il connaît le jeu (joueur, combat) mais
pas tkinter. Le dessin est dans coliseum/terminal/panneau.py, qui connaît
tkinter mais pas le jeu. Les deux ne se parlent qu'à travers `Recap`.

Hors combat, les valeurs du joueur sont lues dans `services.Player`. Pendant
un combat, elles sont lues dans le modèle du combat : c'est lui que le combat
modifie, et il n'est recopié dans le joueur qu'à la fin.

Modifier ce qui est affiché = modifier `_recap_hors_combat`,
`_recap_en_combat` ou `recap_du_monstre`, plus bas.
"""

import collections
import os
import re

from coliseum import services
from coliseum.chemins import DOSSIER_RESSOURCES
from coliseum.donnees.personnages import IMAGES_DES_PERSONNAGES

# CONCEPT : `namedtuple` fabrique une petite classe non modifiable dont les
# valeurs se comparent champ par champ. Deux `Recap` au contenu identique sont
# donc égaux avec `==` : c'est ce qui permet à la fenêtre de savoir, d'une
# simple comparaison, si quelque chose a changé depuis le dernier dessin.

# Un cadre sur le côté de l'image. `jauge` : part remplie de 0 à 1, ou None.
Cadre = collections.namedtuple("Cadre", "etiquette valeur jauge couleur")
# Un bloc du bas de la fenêtre : un titre et une liste de courts textes.
Bloc = collections.namedtuple("Bloc", "titre elements")
Recap = collections.namedtuple("Recap", "titre sous_titre image gauche droite bas")

COULEUR_VIE = "#c0392b"
COULEUR_MANA = "#2f7fd1"
COULEUR_ENDURANCE = "#3d9a52"

_VALEURS_VIDES = ("", "Aucun", "None", None)
_ENTRE_CROCHETS = re.compile(r"\[([^\[\]]+)\]")

# Le contrôleur du combat en cours, ou None hors combat.
_combat = None


def suivre_le_combat(controle):
    """À appeler quand le monstre du combat est créé : son récap remplace la carte."""
    global _combat
    _combat = controle


def oublier_le_combat():
    """À appeler quand le combat est terminé : la carte revient."""
    global _combat
    _combat = None


# ------------------------------------------------------------------ le joueur

def recap_du_joueur():
    """Retourne le récap du joueur, ou None tant qu'aucun personnage n'est choisi."""
    joueur = services.Player
    if joueur is None or not joueur.nom_du_personnage:
        return None
    if _combat is not None:
        return _recap_en_combat(joueur, _combat)
    return _recap_hors_combat(joueur)


def _recap_hors_combat(joueur):
    gauche = (
        _cadre_a_jauge("Vie", joueur.points_de_vie, joueur.points_de_vie_max, COULEUR_VIE),
        _cadre_a_jauge("Mana", joueur.points_de_mana, joueur.points_de_mana_max, COULEUR_MANA),
        _cadre("Endurance", joueur.points_dendurance),
        _cadre("Golds", joueur.nombre_de_gold),
    )
    droite = _cadres_de_puissance(
        joueur.points_de_force, joueur.points_dintelligence, joueur.points_de_defence,
        joueur.taux_coup_critique, joueur.degat_coup_critique,
        joueur.taux_sort_critique, joueur.degat_sort_critique, joueur.taux_desquive,
    )
    bas = (
        Bloc("Stigmas", _sans_les_vides(joueur.stigma_positif, joueur.stigma_negatif, joueur.stigma_bonus)),
        Bloc("Objets", _objets_possedes(joueur.items_possedes)),
        Bloc("Artefacts", tuple(joueur.liste_dartefacts_optionels)),
    )
    return Recap(joueur.nom_du_personnage, _lieu(joueur), _image_du_personnage(joueur), gauche, droite, bas)


def _recap_en_combat(joueur, controle):
    modele = controle.modele
    gauche = (
        _cadre_a_jauge("Vie", modele.points_de_vie, modele.points_de_vie_max, COULEUR_VIE),
        _cadre_a_jauge("Mana", modele.points_de_mana, modele.points_de_mana_max, COULEUR_MANA),
        _cadre_a_jauge("Endurance", modele.points_de_endurance, modele.points_de_endurance_max, COULEUR_ENDURANCE),
        _cadre("Golds", modele.nombre_de_gold),
    )
    droite = _cadres_de_puissance(
        modele.points_de_force, modele.points_de_intelligence, modele.points_de_defence,
        modele.taux_de_coup_critique, modele.degat_de_coup_critique,
        modele.taux_de_sort_critique, modele.degat_de_sort_critique, modele.taux_de_esquive,
    )
    _, etats_du_joueur = _etats_du_combat(controle)
    bas = (
        Bloc("États", etats_du_joueur),
        Bloc("Stigmas", _sans_les_vides(
            modele.stigma_joueur_positif, modele.stigma_joueur_negatif, modele.stigma_joueur_bonus)),
        Bloc("Objets", _objets_possedes(modele.items)),
        Bloc("Artefacts", tuple(modele.liste_dartefacts_optionels)),
    )
    return Recap(joueur.nom_du_personnage, _lieu(joueur), _image_du_personnage(joueur), gauche, droite, bas)


def _cadres_de_puissance(force, intelligence, defence, taux_coup, degat_coup, taux_sort, degat_sort, esquive):
    return (
        _cadre("Force", force),
        _cadre("Intelligence", intelligence),
        _cadre("Défense", defence),
        _cadre("Coup critique", f"{taux_coup} %  +{degat_coup}"),
        _cadre("Sort critique", f"{taux_sort} %  +{degat_sort}"),
        _cadre("Esquive", f"{esquive} %"),
    )


def _lieu(joueur):
    return f"Étage {joueur.numero_de_letage}"


def _image_du_personnage(joueur):
    return _chemin_complet(IMAGES_DES_PERSONNAGES.get(joueur.nom_du_personnage))


def _objets_possedes(objets):
    """("Remède x5", "Fléchette Bleue x2"...) pour les objets possédés en au moins un exemplaire."""
    return tuple(
        f"{nom} x{quantite}"
        for nom, quantite in objets.items()
        if isinstance(quantite, int) and quantite > 0
    )


# ----------------------------------------------------------------- le monstre

def recap_du_monstre():
    """Retourne le récap du monstre combattu, ou None hors combat."""
    if _combat is None:
        return None
    modele = _combat.modele
    # Le jeu lui-même masque le mana d'un monstre en état de choc.
    mana = "ERROR" if modele.monstre_en_etat_de_choc else None
    gauche = (
        _cadre_a_jauge("Vie", modele.monstre_points_de_vie, modele.monstre_points_de_vie_max, COULEUR_VIE),
        _cadre_a_jauge("Mana", modele.monstre_points_de_mana, modele.monstre_points_de_mana_max,
                       COULEUR_MANA, valeur_affichee=mana),
        _cadre("Vies en plus", modele.monstre_nombre_de_vies_supplementaire),
    )
    droite = (
        _cadre("Force", modele.monstre_points_de_force),
        _cadre("Intelligence", modele.monstre_points_de_intelligence),
        _cadre("Résistance", modele.monstre_points_de_resistance),
    )
    etats_du_monstre, _ = _etats_du_combat(_combat)
    bas = (
        Bloc("États", etats_du_monstre),
        Bloc("Stigmas", _sans_les_vides(
            modele.stigma_monstre_positif, modele.stigma_monstre_negatif, modele.stigma_monstre_bonus)),
    )
    return Recap(
        modele.monstre_nom, f"Niveau {modele.monstre_level}",
        _chemin_complet(modele.monstre_image), gauche, droite, bas,
    )


def _etats_du_combat(controle):
    """Retourne (états du monstre, états du joueur), chacun en tuple de noms.

    POURQUOI passer par la phrase du combat : la liste des altérations d'état
    tient en une centaine de conditions dans `ConstruirePhraseAlterationEtatPourVue`,
    qui les met en forme pour la console (« | [Brûlure] | [Gelure] | »). Les
    recopier ici ferait deux listes à tenir à jour. On réutilise donc la
    phrase, dont on extrait ce qui est entre crochets.
    """
    phrase_du_monstre, phrase_du_joueur = controle.ConstruirePhraseAlterationEtatPourVue()
    return (
        tuple(_ENTRE_CROCHETS.findall(phrase_du_monstre)),
        tuple(_ENTRE_CROCHETS.findall(phrase_du_joueur)),
    )


# ------------------------------------------------------------------- la carte

def carte_possedee():
    """Retourne True si le joueur a le droit de voir la carte de l'étage.

    C'est exactement la condition que le jeu utilise déjà pour dessiner la
    carte (`ColiseumGoto` dans interface/dessin.py) : la livraison « Carte »
    couvre l'étage, et le marchand de l'étage 1 a remis la carte pendant
    cette partie (tag « Livraison Terminée »). Tant qu'elle est fausse, la
    fenêtre affiche « -- No Data Found -- » à la place de la carte.
    """
    joueur = services.Player
    if joueur is None or not joueur.nom_du_personnage:
        return False
    # ATTENTION : `carte_ouverte` d'abord. Le tag « Livraison Terminée » de la
    # partie précédente n'est retiré qu'à la fin de la création d'une
    # nouvelle partie : sans ce test, la carte apparaissait un instant au
    # début du jeu puis disparaissait. `carte_ouverte` n'est vrai qu'une fois
    # la carte de l'étage réellement dessinée (FloorMaker.ShowFloor).
    if services.FloorMaker is None or not services.FloorMaker.carte_ouverte:
        return False
    sauvegarde = services.Sove
    return bool(
        sauvegarde.ModifieLivraisonDansSove("Limite", "Carte", joueur.numero_de_letage - 4)
        and sauvegarde.ModifieTagsDansSove("Checke", "Livraison Terminée")
    )


# -------------------------------------------------------------------- commun

def _cadre(etiquette, valeur):
    return Cadre(etiquette, str(valeur), None, None)


def _cadre_a_jauge(etiquette, valeur, maximum, couleur, valeur_affichee=None):
    if valeur_affichee is None:
        valeur_affichee = f"{valeur} / {maximum}"
    part = 0 if maximum <= 0 else min(1, max(0, valeur / maximum))
    return Cadre(etiquette, valeur_affichee, part, couleur)


def _sans_les_vides(*valeurs):
    return tuple(valeur for valeur in valeurs if valeur not in _VALEURS_VIDES)


def _chemin_complet(chemin_relatif):
    """Transforme `images\\monstres\\rat.png` en chemin complet, ou retourne None.

    Le chemin donné dans une fiche part du dossier ColiseumDependencies. Les
    deux sens de barre sont acceptés, pour que le même chemin fonctionne sous
    Windows et ailleurs.
    """
    if not chemin_relatif:
        return None
    if os.path.isabs(chemin_relatif):
        return chemin_relatif
    morceaux = [morceau for morceau in re.split(r"[\\/]+", chemin_relatif) if morceau]
    return os.path.join(DOSSIER_RESSOURCES, *morceaux)
