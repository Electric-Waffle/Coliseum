"""Les salles que le joueur peut observer, au donjon comme au village.

ATTENTION : les imports ci-dessous ne sont pas décoratifs. C'est en important
un module de salles que ses fonctions `@salle_de_type(...)` s'inscrivent dans le
registre. Un nouveau fichier de salles doit donc être ajouté à cette liste,
sinon ses salles n'existeront pas.
"""

from coliseum.exploration.salles import attractions, base, enigmes, machines, rencontres, village  # noqa: F401
from coliseum.exploration.salles.registre import reveler_la_salle  # noqa: F401
