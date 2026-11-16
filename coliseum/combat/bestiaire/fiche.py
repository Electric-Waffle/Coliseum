"""Fiches de monstre et registre du bestiaire.

FLUX :
1. Chaque monstre est décrit par une fonction décorée `@monstre("Nom")` qui
   retourne une `FicheMonstre` (voir les autres fichiers du dossier).
2. Au début d'un combat, le contrôleur connaît le nom du monstre et appelle
   `fiche_du_monstre(nom, combat)`.
3. La fiche obtenue est recopiée dans le modèle par `fiche.appliquer(modele)`.

PATTERN : registre rempli par décorateur, comme pour les salles de l'étage
(coliseum/exploration/salles/registre.py).

POURQUOI des fonctions et pas un simple dictionnaire de fiches ?
Certaines valeurs dépendent du combat en cours : l'or gagné augmente avec
l'étage, la Mimique devient plus forte à chaque étage. Une fonction est
évaluée au moment du combat, avec le bon étage. Elle fabrique aussi des
dictionnaires neufs à chaque appel : un combat peut donc modifier la liste
d'actions de son monstre sans abîmer la fiche pour le combat suivant.

Ajouter un monstre :

    @monstre("Rat Géant")
    def rat_geant(combat):
        return FicheMonstre(
            stigma_positif="Gluantesque",
            stigma_negatif="Gluantin",
            force=3, intelligence=0, resistance=1,
            vies_supplementaires=0, vie_max=40, mana_max=10,
            actions={"Coup de Boule": "Technique", "Soin": "Sort"},
            recompense={"Vie max": 2, "Gold": 20 + combat.bonus_gold},
            image=r"images\monstres\rat_geant.png",
        )

puis faire apparaître son nom (listes de monstres dans combat/modele.py).
"""

_FICHES = {}

# champ de la fiche -> attribut du modèle de combat qu'il renseigne
_ATTRIBUT_DU_MODELE = {
    "stigma_positif": "stigma_monstre_positif",
    "stigma_negatif": "stigma_monstre_negatif",
    "stigma_bonus": "stigma_monstre_bonus",
    "force": "monstre_points_de_force",
    "intelligence": "monstre_points_de_intelligence",
    "resistance": "monstre_points_de_resistance",
    "vies_supplementaires": "monstre_nombre_de_vies_supplementaire",
    "vie_max": "monstre_points_de_vie_max",
    "mana_max": "monstre_points_de_mana_max",
    "actions": "monstre_liste_actions",
    "recompense": "monstre_recompense",
    "tags": "monstre_tags",
    "image": "monstre_image",
}


class ContexteDeCombat:
    """Ce qu'une fiche a le droit de savoir sur le combat en cours.

    POURQUOI des propriétés calculées à la demande : seule une poignée de
    fiches lit `vies_du_gardien` ou `numero_etage`. Les calculer uniquement
    quand une fiche les demande évite de lire le joueur pour rien.
    """

    def __init__(self, modele, joueur):
        self._modele = modele
        self._joueur = joueur

    @property
    def numero_etage(self):
        return self._modele.numero_de_letage

    @property
    def bonus_gold(self):
        return round(125 * (self.numero_etage / 9))

    @property
    def bonus_vie(self):
        return round(500 * (self.numero_etage / 8))

    @property
    def vies_du_gardien(self):
        return self._joueur.vies_du_gardien


class FicheMonstre:
    """Caractéristiques d'un monstre au début d'un combat.

    Un champ laissé à None n'est pas renseigné : le modèle garde alors sa
    valeur par défaut (par exemple `stigma_bonus`, que peu de monstres ont).

    - actions      : {nom de l'action: "Technique" ou "Sort"}
    - recompense   : {nom du gain: quantité}, donnée au joueur s'il gagne
    - tags         : marqueurs activant des mécaniques spéciales du combat
    - image        : chemin de l'image du monstre, à partir du dossier
                     ColiseumDependencies (PNG ou GIF), montrée dans le récap
                     du monstre. Sans image : « -- No Data Found -- ».
    - etat_initial : autres attributs du modèle à fixer, {attribut: valeur}
    - bonus_de_vie_de_l_etage : False si la vie ne doit pas grandir avec l'étage
    - finition     : fonction(modele) appelée après l'application de la fiche,
                     pour les rares monstres qu'une fiche ne suffit pas à décrire
    """

    def __init__(self, stigma_positif=None, stigma_negatif=None, stigma_bonus=None,
                 force=None, intelligence=None, resistance=None,
                 vies_supplementaires=None, vie_max=None, mana_max=None,
                 actions=None, recompense=None, tags=None, image=None,
                 etat_initial=None, bonus_de_vie_de_l_etage=True, finition=None):
        self.stigma_positif = stigma_positif
        self.stigma_negatif = stigma_negatif
        self.stigma_bonus = stigma_bonus
        self.force = force
        self.intelligence = intelligence
        self.resistance = resistance
        self.vies_supplementaires = vies_supplementaires
        self.vie_max = vie_max
        self.mana_max = mana_max
        self.actions = actions
        self.recompense = recompense
        self.tags = tags
        self.image = image
        self.etat_initial = etat_initial or {}
        self.bonus_de_vie_de_l_etage = bonus_de_vie_de_l_etage
        self.finition = finition

    def appliquer(self, modele):
        """Recopie la fiche dans le modèle de combat."""
        for champ, attribut in _ATTRIBUT_DU_MODELE.items():
            valeur = getattr(self, champ)
            if valeur is not None:
                setattr(modele, attribut, valeur)
        for attribut, valeur in self.etat_initial.items():
            setattr(modele, attribut, valeur)
        if self.finition is not None:
            self.finition(modele)


def monstre(nom):
    """Décorateur : inscrit la fonction comme fabrique de la fiche du monstre `nom`."""

    def inscrire(fabriquer_la_fiche):
        if nom in _FICHES:
            raise ValueError(f"Le monstre {nom!r} est déjà inscrit au bestiaire.")
        _FICHES[nom] = fabriquer_la_fiche
        return fabriquer_la_fiche

    return inscrire


def fiche_du_monstre(nom, combat):
    """Fabrique la fiche du monstre `nom` pour le combat en cours.

    Un nom absent du bestiaire donne une fiche vide : le monstre garde les
    valeurs par défaut du modèle, comme le faisait l'ancienne chaîne de elif.
    """
    fabriquer_la_fiche = _FICHES.get(nom)
    if fabriquer_la_fiche is None:
        return FicheMonstre()
    return fabriquer_la_fiche(combat)
