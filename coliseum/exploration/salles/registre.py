"""Registre des salles : associe un type de salle à ce qui s'y passe quand on l'observe.

Un étage du donjon et le village fonctionnent de la même façon : une carte de
salles (le « blueprint »), chacune avec un type ("MONSTRE", "BANQUIER"...).
Quand le joueur observe la salle où il se trouve, `Floor.RevealRoom` demande au
registre la fonction correspondant à ce type et l'appelle. Le registre ne fait
aucune différence entre donjon et village : c'est ce qui permet au même système
de carte de servir aux deux.

PATTERN : registre rempli par décorateur (variante du pattern Strategy).
Chaque fonction décorée par `@salle_de_type("TYPE")` est une stratégie ; le registre est
le dictionnaire qui les range par type.

POURQUOI : `RevealRoom` était une chaîne de 65 `elif` sur 5 000 lignes. Pour
ajouter une salle il fallait retrouver le bon endroit dans cette chaîne. Avec le
registre, ajouter une salle = écrire une fonction décorée, dans le fichier de
son thème, sans toucher à `RevealRoom` (principe ouvert/fermé).
C'est le même mécanisme que les services taggés de Symfony : le décorateur joue
le rôle du tag, et le registre celui de l'itérateur de services taggés.

Ajouter une salle :

    @salle_de_type("FONTAINE")
    def reveler_fontaine(etage, salle):
        print("Une fontaine coule au centre de la pièce.")
        salle["terminé par joueur"] = True

puis donner ce type à une salle du blueprint (Floor.AttributingRoleToRoom pour
le donjon, PrepareTheVillage pour le village).
"""

_REVELATEURS = {}


def salle_de_type(*types_de_salle):
    """Décorateur : inscrit la fonction comme révélateur des types de salle donnés.

    CONCEPT : un décorateur avec arguments est une fonction qui fabrique un
    décorateur. `@salle_de_type("A", "B")` appelle d'abord `salle_de_type("A", "B")`, qui
    retourne `inscrire` ; Python appelle ensuite `inscrire(la_fonction)`.
    `inscrire` range la fonction dans le registre puis la rend telle quelle :
    elle reste appelable directement, ce dont se sert `reveler_ancien`.
    L'inscription a lieu à l'import du module : il suffit donc qu'un module de
    salles soit importé (voir salles/__init__.py) pour que ses salles existent.
    """

    def inscrire(reveler):
        for type_de_salle in types_de_salle:
            if type_de_salle in _REVELATEURS:
                raise ValueError(f"Le type de salle {type_de_salle!r} est déjà inscrit.")
            _REVELATEURS[type_de_salle] = reveler
        return reveler

    return inscrire


def reveler_la_salle(etage, salle):
    """Déroule ce qui se passe dans `salle`. Un type inconnu ne fait rien.

    `etage` est le Floor en cours (accès à la carte et aux mini-jeux),
    `salle` est le dictionnaire de la salle dans le blueprint.
    """
    reveler = _REVELATEURS.get(salle["type"])
    if reveler is not None:
        reveler(etage, salle)
