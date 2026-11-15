"""Le bestiaire : la fiche de chaque monstre du jeu.

ATTENTION : comme pour les salles, c'est l'import d'un module de fiches qui
inscrit ses monstres. Un nouveau fichier de fiches doit être ajouté ici.
"""

from coliseum.combat.bestiaire import boss, boss_rush, monstres_des_etages, speciaux  # noqa: F401
from coliseum.combat.bestiaire.fiche import ContexteDeCombat, fiche_du_monstre  # noqa: F401
