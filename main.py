import controleur
import os
from pygame import mixer
import random
import sys
import csv
import ast
import time

# 0nom 1description 2stigma+ 3stigma- 4stigma* 5techniques 
# 6sorts 7items 8talents 9vie 10mana 11force
# 12inteligence 13defence 14tauxcoupcrit
# 15degatcoupcrit 16tauxsortcrit 17degatsortcrit
# 18tauxesquive 19gold
LISTEDEPERSONNAGE = {
    "Saumel": [  # char
        "Saumel",
        ("Chasseur hermite, ancien esclave pour un bourgeois fanatique de l'argent."
         "\n           Parti dans le Coliseum pour devenir plus fort afin de prendre sa revanche."),  # char
        "Solide",  # char stigma +
        "Chrometophobia",  # char stigma -
        "Aucun",  # char stigma *
        [
            "Attaque Légère"
        ],  # char list technic
        [
            "Tir Arcanique",
            "Explosion Légère"
        ],  # char list sorts
        {
            "Feuille Jindagee": 3,
            "Fruit Jindagee": 1,
            "Feuille Aatma": 2,
            "Remède": 5,
            "Fléchette Bleue": 2,
            "Mutagène Rouge": 1
        },  # char dict of int items
        [
            "Affinitée Physique"
        ],  # char list
        40,  # int vie
        15,  # int mana
        2,  # int force
        2,  # int intelligence
        2,  # int defence
        15,  # int taux coup crit
        5,  # int degat coup crit
        10,  # int taux sort crit
        10,  # int degat sort crit
        8,  # int taux esquive
        0,  # int gold
    ],
    "Elma": [  # char
        "Elma",
        ("Quinquagénère, Voleuse inarrêtable, surnommée Princesse de Suie, a la tête d'un gang de sans-abris."
         "\n           Jetée dans le Colliseum par le prétendant au titre de chef, plus jeune et plus soutenu."
         "\n           Son corps brisé à trempé dans une fontaine de fée, et l'a assez revigoré pour qu'elle tente de sortir pour reprendre sa place à la surface."),  # char
        "Bénie par les Fées",  # char stigma +
        "Famine",  # char stigma -
        "Aucun",  # char stigma *
        [
            "Attaque Légère",
            "Dague Volevie"
        ],  # char list technic
        [
            "Tir Arcanique",
        ],  # char list sorts
        {
        },  # char dict of int items
        [
        ],  # char list
        35,  # int vie
        10,  # int mana
        1,  # int force
        2,  # int intelligence
        0,  # int defence
        20,  # int taux coup crit
        10,  # int degat coup crit
        20,  # int taux sort crit
        10,  # int degat sort crit
        10,  # int taux esquive
        0,  # int gold
    ],
    "Auguste": [  # char
        "Auguste",
        ("Un écrivain brillant ayant perdu ses mains dans un accident de voiture."
         "\n           Parti dans le Coliseum après avoir entendu parler de la puissance qu'on peut y acquérir."
         "\n           Pense pouvoir y trouver un moyen de retrouver des mains biologiques, artificielles ou...magiques."),  # char
        "Diligent",  # char stigma +
        "Manchot",  # char stigma -
        "Aucun",  # char stigma *
        [
            "Attaque Légère",
        ],  # char list technic
        [
            "Tir Arcanique",
            "Thermosphère Chaude",
            "Sonata Pitoyable"
        ],  # char list sorts
        {
        },  # char dict of int items
        [
        ],  # char list
        30,  # int vie
        20,  # int mana
        1,  # int force
        4,  # int intelligence
        0,  # int defence
        10,  # int taux coup crit
        5,  # int degat coup crit
        25,  # int taux sort crit
        0,  # int degat sort crit
        0,  # int taux esquive
        20,  # int gold
    ],
    "Saria": [  # char
        "Saria",
        ("Une des dernières druidesses encore en vie pendant les affres de L'inquisition espagnole"
         "\n           Est venue se cacher des buchers et des horreurs dans le seul endroit ou on la considererait morte sans l'être vraiment : le Coliseum."
         "\n           S'étonne que son lien avec la nature dans cet endroit sordide ne soit pas brisé, malgrès l'omniprésence de la mort."),  # char
        "Cueilleuse",  # char stigma +
        "Coeur Pur",  # char stigma -
        "Aucun",  # char stigma *
        [
            "Attaque Légère",
        ],  # char list technic
        [
            "Tir Arcanique",
            "Sonata Miséricordieuse"
        ],  # char list sorts
        {   
            "Feuille Jindagee": 5,
            "Fruit Jindagee": 5,
            "Feuille Aatma": 5,
            "Fruit Aatma": 5,
        },  # char dict of int items
        [
            "Affinitée de Terre"
        ],  # char list
        30,  # int vie
        17,  # int mana
        0,  # int force
        4,  # int intelligence
        1,  # int defence
        10,  # int taux coup crit
        2,  # int degat coup crit
        10,  # int taux sort crit
        2,  # int degat sort crit
        8,  # int taux esquive
        20,  # int gold
    ],
    "Vesperum": [  # char
        "Vesperum",
        ("Un homme devenu démon par amour ayant échappé aux enfers, à la recherche de pouvoir afin de prendre le controle de l'Au-Dela."
         "\n           A été attiré au Coliseum par l'odeur de mort qui s'en échappe, et le son de millions d'âmes emprisonnées entre ses murs."
         "\n           Ne sait pas pourquoi, mais les troupes du Paradis et de l'Enfer à ses trousses ne viennet pas le chercher ici."),  # char
        "Forces Obscures",  # char stigma +
        "Maudit",  # char stigma -
        "Aucun",  # char stigma *
        [
            "Attaque Légère",
            "Katana Bleu"
        ],  # char list technic
        [
            "Tir Arcanique",
            "Dance Volevie"
        ],  # char list sorts
        {
        },  # char dict of int items
        [
            "Affinitée de Sang"
        ],  # char list
        35,  # int vie
        10,  # int mana
        2,  # int force
        2,  # int intelligence
        1,  # int defence
        0,  # int taux coup crit
        5,  # int degat coup crit
        0,  # int taux sort crit
        15,  # int degat sort crit
        5,  # int taux esquive
        0,  # int gold
    ],
    "Lucien": [  # char
        "Lucien",
        ("Descendant du mage qui à crée le Coliseum, brillant magicien toujours comparé a son ancêtre."
         "\n           Venu régler ses comptes avec le grand Maitre Mage afin de décider qui des deux est le meilleur."
         "\n           Revient de 5 ans a écumer les mers aux coté de son fidèle équipage de pirate"),  # char
        "Grande Connaissance",  # char stigma +
        "Colérique",  # char stigma -
        "Logique au dessus des Cieux",  # char stigma *
        [
            "Attaque Légère",
            "Poing Renforcé"
        ],  # char list technic
        [
            "Tir Arcanique",
            "Faisceau Statique",
            "Thermosphère Brulante",
            "Pic Froid",
            "Création de Lapis",
            "Explosion Renforcée",
            "Dance Siphoneuse",
            "Sonata Miséricordieuse",
        ],  # char list sorts
        {
        },  # char dict of int items
        [
        ],  # char list
        25,  # int vie
        25,  # int mana
        0,  # int force
        5,  # int intelligence
        0,  # int defence
        0,  # int taux coup crit
        0,  # int degat coup crit
        0,  # int taux sort crit
        0,  # int degat sort crit
        0,  # int taux esquive
        0,  # int gold
    ],
    "Élémia": [  # char
        "Élémia",
        ("Inventeuse, créatrice, artiste, elle à tout fait, à part peut être suivre le destin qu'on lui à donné."
         "\n           Venue tester sa toute dernière invention en condition réelle : une armure de Deus-ex-machinium."
         "\n           On dit du dernier héros ayant besoin d'une inventrice dans son"
         " équipe pour sauver le monde... "
         "\n           ...qu'il est ressorti de son village avec un bras en moins a cause d'une des inventions ratée d'élémia."),  # char
        "Débrouillarde",  # char stigma +
        "Flemme",  # char stigma -
        "Emotion au dessus des Cieux",  # char stigma *
        [
            "Attaque Légère",
        ],  # char list technic
        [
            "Tir Arcanique",
        ],  # char list sorts
        {
        },  # char dict of int items
        [
        ],  # char list
        35,  # int vie
        25,  # int mana
        2,  # int force
        2,  # int intelligence
        5,  # int defence
        40,  # int taux coup crit
        0,  # int degat coup crit
        40,  # int taux sort crit
        0,  # int degat sort crit
        0,  # int taux esquive
        50,  # int gold
    ],
    "Samantha": [  # char
        "Samantha",
        ("Une doctoresse diplomée de l'Universitée Prestigieuse de Prestige-City. Endettée jusque au cou grâce a son prêt etudiant."
         "\n           Entre payer sa detter sur les 50 prochaines années de sa vie ou entrer dans le Coliseum pour gagner des richesses, elle à fait son choix."
         "\n           Elle a pillée les réserves médicales de son école avant de venir ici."),  # char
        "Pharmacodynamisme",  # char stigma +
        "Serment d'Hyppocrate",  # char stigma -
        "Aucun",  # char stigma *
        [
            "Attaque Légère",
        ],  # char list technic
        [
            "Tir Arcanique",
        ],  # char list sorts
        {
            "Remède": 15,
            "Pillule": 15,
            "Grand Mutagène Doré": 1
        },  # char dict of int items
        [
        ],  # char list
        30,  # int vie
        5,  # int mana
        1,  # int force
        4,  # int intelligence
        1,  # int defence
        20,  # int taux coup crit
        8,  # int degat coup crit
        20,  # int taux sort crit
        8,  # int degat sort crit
        5,  # int taux esquive
        0,  # int gold
    ],
    "Emy": [  # char
        "Emy",
        ("Une ancienne Louve de glace devenue humaine, prise d'affection pour un vieil homme tombé par hasard dans le Coliseum."
         "\n           Après sa transformation, sentant naitre de nouvelles émotions et sensations, elle a paniquée et s'est retrouvée au premier étage."
         "\n           On dit qu'elle est devenue humaine lorsque le vieil homme dont elle s'occupait, se sentant mourir, lui à offert son coeur plein de compassion."
         "\n           Littéralement."),  # char
        "Conception du Mana",  # char stigma +
        "Attache Physique",  # char stigma -
        "Chaos Emotionel",  # char stigma *
        [
            "Attaque Légère",
            "Katana Froid"
        ],  # char list technic
        [
            "Tir Arcanique",
            "Pic Bleu",
            "Pic Froid"
        ],  # char list sorts
        {
        },  # char dict of int items
        [
            "Affinitée de Glace",
            "Ere Glaciaire"
        ],  # char list
        25,  # int vie
        0,  # int mana
        2,  # int force
        5,  # int intelligence
        0,  # int defence
        15,  # int taux coup crit
        15,  # int degat coup crit
        15,  # int taux sort crit
        15,  # int degat sort crit
        14,  # int taux esquive
        0,  # int gold
    ],
    "Terah": [  # char
        "Terah",
        ("Un adolescent sans histoire, sans famille, sans amis. Surnommé *Enfant Maudit* sans qu'il ne sache pourquoi, tout son village l'évite."
         "\n           Il n'a aucune attache au monde des vivant. Alors quand il a entendu la voix des morts qui l'appelait, il n'a pas hésité une seconde a rentrer dans le Coliseum."
         "\n           Amenez le moi."),  # char
        "Endurci",  # char stigma +
        "Incontrolable",  # char stigma -
        "Sanjiva",  # char stigma *
        [
            "Attaque Légère",
            "Lance Rapide"
        ],  # char list technic
        [
            "Tir Arcanique",
        ],  # char list sorts
        {
        },  # char dict of int items
        [
        ],  # char list
        33,  # int vie
        23,  # int mana
        2,  # int force
        2,  # int intelligence
        2,  # int defence
        13,  # int taux coup crit
        13,  # int degat coup crit
        13,  # int taux sort crit
        13,  # int degat sort crit
        13,  # int taux esquive
        13,  # int gold
    ],
    "Peralta": [  # char
        "Peralta",
        ("Une policière sous couverture, accusée a tort par un collègue corrompu, attendant son procès."
         "\n           Enlevée de la prison par le gang qu'elle inflitrait, jetée dans le Coliseum pour éviter qu'elle ne parle, déterminée a sortir de là."
         "\n           Elle à un caractère bien trempée, et est connue dans son service pour son coup de boule phénoménal."),  # char
        "Bergentruckung",  # char stigma +
        "Mauvaise Réputation",  # char stigma -
        "Aucun",  # char stigma *
        [
            "Attaque Légère",
            "Lance Rapide"
        ],  # char list technic
        [
            "Tir Arcanique",
        ],  # char list sorts
        {
        },  # char dict of int items
        [
        ],  # char list
        36,  # int vie
        16,  # int mana
        5,  # int force
        0,  # int intelligence
        4,  # int defence
        5,  # int taux coup crit
        15,  # int degat coup crit
        0,  # int taux sort crit
        8,  # int degat sort crit
        10,  # int taux esquive
        0,  # int gold
    ],
    "Redde": [  # char
        "Redde",
        ("Un streamer de jeux vidéo en burnout total, perdu dans son propre monde et persuadé d'être le personnage principal d'une histoire dont seul lui connait le déroulement."
         "\n           Entre dans le Coliseum pour vivre l'aventure ultime."
         "\n           Est connu pour son sens du showmanship inégalé."),  # char
        "Dernier Choix",  # char stigma +
        "Pas d'Echappatoire",  # char stigma -
        "Aucun",  # char stigma *
        [
            "Attaque Légère",
        ],  # char list technic
        [
            "Tir Arcanique",
        ],  # char list sorts
        {
        },  # char dict of int items
        [
        ],  # char list
        30,  # int vie
        10,  # int mana
        1,  # int force
        1,  # int intelligence
        1,  # int defence
        10,  # int taux coup crit
        10,  # int degat coup crit
        10,  # int taux sort crit
        10,  # int degat sort crit
        9,  # int taux esquive
        250,  # int gold
    ],
    "Valfreya": [  # char
        "Valfreya",
        ("Une Valkirie envoyée prouver sa valeur dans le Coliseum après que Thor aie critiqué Odin pour s'entourer d'un harem de femmes inutiles au combat."
         "\n           Entre dans le Coliseum dans une envellope charnelle trop faible, en poussant un long soupir."
         "\n           On dit qu'elle aurait renversé un gobelet de bière sur le pantalon d'Odin il y a des millénaires de cela,"
         "\n           et que c'est pour ca qu'elle aurait été choisie."),  # char
        "Manteau de Faucon",  # char stigma +
        "Ange Déchue",  # char stigma -
        "Aucun",  # char stigma *
        [
            "Attaque Légère",
        ],  # char list technic
        [
            "Tir Arcanique",
        ],  # char list sorts
        {
            "Ambroisie": 10,
            "Hydromel": 10,
            "Fruit Jindagee": 10
        },  # char dict of int items
        [
            "Affinitée de Foudre",
            "Affinitée de Glace",
            "Affinitée de Terre",
            "Affinitée de Sang",
            "Affinitée Physique"
        ],  # char list
        20,  # int vie
        25,  # int mana
        1,  # int force
        3,  # int intelligence
        0,  # int defence
        25,  # int taux coup crit
        10,  # int degat coup crit
        25,  # int taux sort crit
        10,  # int degat sort crit
        25,  # int taux esquive
        100,  # int gold
    ],
    "Bob": [  # char
        "Bob",
        ("Un pyrobarbare bruyant à l'allure fière, agent sur terre d'une ancienne divinitée du feu."
         "\n           Venu chercher la gloire a coup de hache, de feu, et de grands cris dans les couloirs du Coliseum."
         "\n           Que dire de plus ? Il est musculeux !"),  # char
        "Ange de Feu",  # char stigma +
        "Fair Play",  # char stigma -
        "Musculeux",  # char stigma *
        [
            "Attaque Légère",
            "Bô Brulant"
        ],  # char list technic
        [
            "Tir Arcanique",
            "Thermosphère Chaude",
            "Thermosphère Brulante",
        ],  # char list sorts
        {
            "Crystal Elémentaire": 2,
            "Hydromel": 3,
            "Orbe de Furie": 1,
            "Fléchette Bleue": 4,
        },  # char dict of int items
        [
            "Affinitée de Feu",
            "Pyrophile"
        ],  # char list
        40,  # int vie
        20,  # int mana
        2,  # int force
        2,  # int intelligence
        2,  # int defence
        15,  # int taux coup crit
        5,  # int degat coup crit
        15,  # int taux sort crit
        5,  # int degat sort crit
        0,  # int taux esquive
        25,  # int gold
    ],
    "Bob Doré": [  # char
        "Bob Doré",
        ("Une poupée dorée représentant un pyrobarbare bruyant à l'allure fière."
         "\n           Venu tester les codes du Coliseum sans avoir a se taper 1h de gameplay a chaque fois."
         "\n           Que dire de plus ? Il est doré ! Bling-Bling !"),  # char
        "Ange de Feu",  # char stigma +
        "Aucun, voyons",  # char stigma -
        "Musculeux",  # char stigma *
        [
            "Attaque Légère",
            "Bô Brulant"
        ],  # char list technic
        [
            "Tir Arcanique",
            "Thermosphère Chaude",
            "Thermosphère Brulante",
        ],  # char list sorts
        {
            "Crystal Elémentaire": 2,
            "Hydromel": 3,
            "Orbe de Furie": 1,
            "Fléchette Bleue": 4,
        },  # char dict of int items
        [
            "Affinitée de Feu",
            "Pyrophile"
        ],  # char list
        4000,  # int vie
        2000,  # int mana
        200,  # int force
        200,  # int intelligence
        200,  # int defence
        15,  # int taux coup crit
        5,  # int degat coup crit
        15,  # int taux sort crit
        5,  # int degat sort crit
        0,  # int taux esquive
        2500000,  # int gold
    ],
}
LISTEDEMUSIQUE = [
    "Nouveaux Départs",
    "Dangereuses Mélancolies",
    "Le Calme avant la Tempête",
    "Fanfare",
    "Pluie d'Automne",
    "Exploratio",
    "Les Joies du Combat",
    "Revenant",
    "Conte de Fée",
    "Epineuses Rencontres",
    "Le Chevalier Qu'on Ne Veut Pas Rencontrer",
    "Ruines d'Antan",
    "Sables Mouvants",
    "Golem de Chair",
    "Puit de Connaisance",
    "Nerd Party",
    "Jeux d'Enfants",
    "Pantomime",
    "Carnaval",
    "Piñata",
    "Tragicomique",
    "Combler les Vides",
    "Systèmes Défaillants",
    "Seigneur des Mouches",
    "Divin Karma",
    "Folie Furieuse",
    "Comment Tuer le Grand Méchant Loup",
    "Ossuaire",
    "Dissonance Cognitive",
    "Faux semblants",
    "La Hache et le Grimoire",
    "Contradictions",
    "Pas encore trouvée",
    "Au Détour D’un Sentier Une Charogne Infâme",
    "La Divine Comédie",
    "Apogée Inversée",
    "Pénultima",
    "Théorie du Chaos"


]
LISTECARACTERISTIQUEMUSIQUE = [
    ["start", "Vous écoutez "],
    ["alfredproto", "Vous écoutez "],
    ["boss_intro", "Vous écoutez "],
    ["battle_win", "Vous écoutez "],
    ["ending", "Vous écoutez "],
    ["etage_1", "Vous écoutez "],
    ["battle_theme_1", "Vous écoutez "],
    ["boss_1", "Vous écoutez "],
    ["etage_2", "Vous écoutez "],
    ["battle_theme_2", "Vous écoutez "],
    ["boss_2", "Vous écoutez "],
    ["etage_3", "Vous écoutez "],
    ["battle_theme_3", "Vous écoutez "],
    ["boss_3", "Vous écoutez "],
    ["etage_4", "Vous écoutez "],
    ["battle_theme_4", "Vous écoutez "],
    ["boss_4", "Vous écoutez "],
    ["boss_4_phase_2", "Vous écoutez "],
    ["etage_5", "Vous écoutez "],
    ["battle_theme_5", "Vous écoutez "],
    ["boss_5", "Vous écoutez "],
    ["etage_6", "Vous écoutez "],
    ["battle_theme_6", "Vous écoutez "],
    ["boss_6", "Vous écoutez "],
    ["etage_7", "Vous écoutez "],
    ["battle_theme_7", "Vous écoutez "],
    ["boss_7", "Vous écoutez "],
    ["etage_8", "Vous écoutez "],
    ["battle_theme_8", "Vous écoutez "],
    ["boss_8", "Vous écoutez "],
    ["boss_8_phase_2", "Vous écoutez "],
    ["etage_9", "Vous écoutez "],
    ["battle_theme_9", "Vous écoutez "],
    ["boss_9", "Vous écoutez "],
    ["etage_10", "Vous écoutez "],
    ["battle_theme_10", "Vous écoutez "],
    ["boss_10", "Vous écoutez "],
    ["boss_10_phase_2", "Vous écoutez "],
]
DICTIONNAIREDEPERSONNAGEAAFFICHER = {}
DICTIONNAIREITEMINITIAL = {
            "Feuille Jindagee": 0,
            "Fruit Jindagee": 0,
            "Feuille Aatma": 0,
            "Fruit Aatma": 0,
            "Crystal Elémentaire": 0,
            "Ambroisie": 0,
            "Hydromel": 0,
            "Orbe de Furie": 0,
            "Orbe de Folie": 0,
            "Remède": 0,
            "Remède Superieur": 0,
            "Remède Divin": 0,
            "Pillule": 0,
            "Pillule Superieure": 0,
            "Pillule Divine": 0,
            "Fléchette Rouge": 0,
            "Flèche Rouge": 0,
            "Fléchette Bleue": 0,
            "Flèche Bleue": 0,
            "Poudre Explosive": 0,
            "Roche Explosive": 0,
            "Bombe Explosive": 0,
            "Fiole de Poison": 0,  # [debutTour]
            "Gourde de Poison": 0,  # [debutTour]
            "Sève d'Absolution": 0,  # [debutTour]
            "Larme d'Absolution": 0,  # [debutTour]
            "Soluté d'Absolution": 0,  # [debutTour]
            "Sève d'Exorcisme": 0,  # [debutTour]
            "Larme d'Exorcisme": 0,  # [debutTour]
            "Soluté d'Exorcisme": 0,  # [debutTour]
            "Mutagène Bleu": 0,  # [debutTour]
            "Grand Mutagène Bleu": 0,  # [debutTour]
            "Mutagène Rouge": 0,  # [debutTour]
            "Grand Mutagène Rouge": 0,  # [debutTour]
            "Mutagène Vert": 0,  # [debutTour]
            "Grand Mutagène Vert": 0,  # [debutTour]
            "Mutagène Doré": 0,  # [debutTour]
            "Grand Mutagène Doré": 0,  # [debutTour]
            "Mutagène Hérétique": 0,  # [debutTour]
            "Mutagène Fanatique": 0,  # [debutTour]
        }
ANNUAIREDECHOIXPOURREDCOIN = {
    #branche du feu
    1257: [
        "Affinitée de Feu",
        1,
        "None"
    ],
    98654: [
        "Surchauffe",
        2,
        "Affinitée de Feu"
    ],
    42381: [
        "Aura de Feu",
        3,
        "Surchauffe"
    ],
    35867: [
        "Rafale",
        4,
        "Aura de Feu"
    ],
    685486: [
        "Pyrophile",
        2,
        "Affinitée de Feu"
    ],
    537895: [
        "Pyrosorcier",
        3,
        "Pyrophile"
    ],
    243537: [
        "Pyromage",
        4,
        "Pyrosorcier"
    ],
    #branche de foudre
    5675: [
        "Affinitée de Foudre",
        1,
        "None"
    ],
    977785: [
        "Anti-Neurotransmitteurs",
        2,
        "Affinitée de Foudre"
    ],
    935761: [
        "Energiseur",
        3,
        "Anti-Neurotransmitteurs"
    ],
    932624: [
        "Facture",
        4,
        "Energiseur"
    ],
    876431: [
        "Rapide",
        2,
        "Affinitée de Foudre"
    ],
    353548: [
        "Electro",
        3,
        "Rapide"
    ],
    768943: [
        "Luciole",
        4,
        "Electro"
    ],
    #branche de glace
    7563: [
        "Affinitée de Glace",
        1,
        "None"
    ],
    646752: [
        "Ere Glaciaire",
        2,
        "Affinitée de Glace"
    ],
    347852: [
        "Eclats de Glace",
        3,
        "Ere Glaciaire"
    ],
    376895: [
        "Grand Froid",
        4,
        "Eclats de Glace"
    ],
    248651: [
        "Choc Thermique",
        2,
        "Affinitée de Glace"
    ],
    179356: [
        "Coeur de Glace",
        3,
        "Choc Thermique"
    ],
    785020: [
        "Cycle Glaciaire",
        4,
        "Coeur de Glace"
    ],
    #branche de terre
    1221: [
        "Affinitée de Terre",
        1,
        "None"
    ],
    867342: [
        "Patience",
        2,
        "Affinitée de Terre"
    ],
    159753: [
        "Rigueur",
        3,
        "Patience"
    ],
    764325: [
        "Fracturation",
        4,
        "Rigueur"
    ],
    114865: [
        "Poussière de Diamants",
        2,
        "Affinitée de Terre"
    ],
    335785: [
        "Richesses Souterraines",
        3,
        "Poussière de Diamants"
    ],
    241053: [
        "Eboulis",
        4,
        "Richesses Souterraines"
    ],
    # branche physique
    8240: [
        "Affinitée Physique",
        1,
        "None"
    ],
    758427: [
        "Peau de Fer",
        2,
        "Affinitée Physique"
    ],
    963741: [
        "Bluff",
        3,
        "Peau de Fer"
    ],
    123789: [
        "Réflex",
        4,
        "Bluff"
    ],
    455668: [
        "Carte du Gout",
        2,
        "Affinitée Physique"
    ],
    2557711: [
        "Connaissance",
        3,
        "Carte du Gout"
    ],
    7661394: [
        "Oeuil Magique",
        4,
        "Connaissance"
    ],
    #branche de sang
    9731: [
        "Affinitée de Sang",
        1,
        "None"
    ],
    9485921: [
        "Nectar",
        2,
        "Affinitée de Sang"
    ],
    9050607: [
        "Anémie",
        3,
        "Nectar"
    ],
    2419687: [
        "Baron Rouge",
        4,
        "Anémie"
    ],
    33054865: [
        "Suroxygénation",
        2,
        "Affinitée de Sang"
    ],
    71546593: [
        "Conditions Limites",
        3,
        "Suroxygénation"
    ],
    93654517: [
        "Anticoagulants",
        4,
        "Conditions Limites"
    ],
    #branche ame
    7093815768: [
        "Pira",
        5,
        "None"
    ],
    7513590556: [
        "Elektron",
        5,
        "None"
    ],
    6598328725: [
        "Tsumeta-Sa",
        5,
        "None"
    ],
    124578953756: [
        "Mathair",
        5,
        "None"
    ],
    25583669867: [
        "Fos",
        5,
        "None"
    ],
    255814477582: [
        "Haddee",
        5,
        "None"
    ],
}



class TraderUsage:

    def __init__(self):
        self.modificateur = 1
        if Player.stigma_negatif == "Mauvaise Réputation":
            self.modificateur = 1.5
        self.annuaire_des_prix = {
            "Feuille Jindagee": round(15*self.modificateur),
            "Fruit Jindagee": round(35 * self.modificateur),
            "Feuille Aatma": round(15 * self.modificateur),
            "Fruit Aatma": round(35 * self.modificateur),
            "Crystal Elémentaire": round(50 * self.modificateur),
            "Ambroisie": round(30 * self.modificateur),
            "Hydromel": round(30 * self.modificateur),
            "Orbe de Furie": round(50 * self.modificateur),
            "Orbe de Folie": round(50 * self.modificateur),
            "Remède": round(10 * self.modificateur),
            "Remède Superieur": round(20 * self.modificateur),
            "Remède Divin": round(30 * self.modificateur),
            "Pillule": round(10 * self.modificateur),
            "Pillule Superieure": round(20 * self.modificateur),
            "Pillule Divine": round(30 * self.modificateur),
            "Fléchette Rouge": round(30 * self.modificateur),
            "Flèche Rouge": round(65 * self.modificateur),
            "Fléchette Bleue": round(30 * self.modificateur),
            "Flèche Bleue": round(65 * self.modificateur),
            "Poudre Explosive": round(30 * self.modificateur),
            "Roche Explosive": round(40 * self.modificateur),
            "Bombe Explosive": round(50 * self.modificateur),
            "Fiole de Poison": round(40 * self.modificateur),  # [debutTour]
            "Gourde de Poison": round(80 * self.modificateur),  # [debutTour]
            "Sève d'Absolution": round(40 * self.modificateur),  # [debutTour]
            "Larme d'Absolution": round(70 * self.modificateur),  # [debutTour]
            "Soluté d'Absolution": round(100 * self.modificateur),  # [debutTour]
            "Sève d'Exorcisme": round(20 * self.modificateur),  # [debutTour]
            "Larme d'Exorcisme": round(45 * self.modificateur),  # [debutTour]
            "Soluté d'Exorcisme": round(70 * self.modificateur),  # [debutTour]
            "Mutagène Bleu": round(40 * self.modificateur),  # [debutTour]
            "Grand Mutagène Bleu": round(80 * self.modificateur),  # [debutTour]
            "Mutagène Rouge": round(40 * self.modificateur),  # [debutTour]
            "Grand Mutagène Rouge": round(80 * self.modificateur),  # [debutTour]
            "Mutagène Vert": round(40 * self.modificateur),  # [debutTour]
            "Grand Mutagène Vert": round(80 * self.modificateur),  # [debutTour]
            "Mutagène Doré": round(90 * self.modificateur),  # [debutTour]
            "Grand Mutagène Doré": round(150 * self.modificateur),  # [debutTour]
            "Mutagène Hérétique": round(100 * self.modificateur),  # [debutTour]
            "Mutagène Fanatique": round(100 * self.modificateur),  # [debutTour]
            "Red Coin": 0,
            "Tirage": 0,
            "Gemme de Vie": round(300 * self.modificateur),
            "Gemme d'Esprit": round(300 * self.modificateur),
            "Fée dans un Bocal": 0,
        }
        self.liste_item_etage_1_2 = [
            "Feuille Jindagee",
            "Feuille Aatma",
            "Crystal Elémentaire",
            "Pillule",
            "Poudre Explosive",
            "Tirage",
            "Red Coin",
            "Fée dans un Bocal"
        ]
        self.liste_item_etage_3_4 = [
            "Feuille Jindagee",
            "Feuille Aatma",
            "Crystal Elémentaire",
            "Pillule",
            "Poudre Explosive",
            "Tirage",
            "Red Coin",
            "Gemme de Vie"
        ]
        self.liste_item_etage_5_6 = [
            "Feuille Jindagee",
            "Feuille Aatma",
            "Crystal Elémentaire",
            "Pillule",
            "Poudre Explosive",
            "Tirage",
            "Red Coin",
            "Gemme d'Esprit",
            "Fée dans un Bocal"
        ]
        self.liste_item_etage_7_8 = [
            "Feuille Jindagee",
            "Feuille Aatma",
            "Crystal Elémentaire",
            "Pillule",
            "Poudre Explosive",
            "Tirage",
            "Red Coin",
            "Gemme de Vie",
            "Gemme d'Esprit"
        ]
        self.liste_item_etage_9_10 = [
            "Feuille Jindagee",
            "Fruit Jindagee",
            "Feuille Aatma",
            "Fruit Aatma",
            "Crystal Elémentaire",
            "Ambroisie",
            "Hydromel",
            "Orbe de Furie",
            "Orbe de Folie",
            "Remède",
            "Remède Superieur",
            "Remède Divin",
            "Pillule",
            "Pillule Superieure",
            "Pillule Divine",
            "Fléchette Rouge",
            "Flèche Rouge",
            "Fléchette Bleue",
            "Flèche Bleue",
            "Poudre Explosive",
            "Roche Explosive",
            "Bombe Explosive",
            "Fiole de Poison",
            "Gourde de Poison",
            "Sève d'Absolution",
            "Larme d'Absolution",
            "Soluté d'Absolution",
            "Sève d'Exorcisme",
            "Larme d'Exorcisme",
            "Soluté d'Exorcisme",
            "Mutagène Bleu",
            "Grand Mutagène Bleu",
            "Mutagène Rouge",
            "Grand Mutagène Rouge",
            "Mutagène Vert",
            "Grand Mutagène Vert",
            "Mutagène Doré",
            "Grand Mutagène Doré",
            "Mutagène Hérétique",
            "Mutagène Fanatique",
            "Tirage",
            "Red Coin",
            "Fée dans un Bocal"
        ]
        self.liste_item_actuelle = []

    def SetItemList(self):
        if Player.numero_de_letage in [1, 2]:
            self.liste_item_actuelle = self.liste_item_etage_1_2
        elif Player.numero_de_letage in [3, 4]:
            self.liste_item_actuelle = self.liste_item_etage_3_4
        elif Player.numero_de_letage in [5, 6]:
            self.liste_item_actuelle = self.liste_item_etage_5_6
        elif Player.numero_de_letage in [7, 8]:
            self.liste_item_actuelle = self.liste_item_etage_7_8
        else:
            self.liste_item_actuelle = self.liste_item_etage_9_10
        
    def ShowItems(self):
        print("1 - Retour")
        numero_a_afficher = 2
        for item in self.liste_item_actuelle:
            print(f"{numero_a_afficher} - {item} : {self.PriceOfItem(item)}")
            numero_a_afficher += 1

    def PriceOfItem(self, item):
        return self.annuaire_des_prix[item]
    
    def SetRedCoinPrice(self):
        if Player.redcoin_bought:
            self.annuaire_des_prix["Red Coin"] = 99999
        else:
            self.annuaire_des_prix["Red Coin"] = Player.numero_de_letage * 100
        self.annuaire_des_prix["Tirage"] = (Player.numero_de_letage * 75) + (Player.number_of_tirage * 100)
        self.annuaire_des_prix["Fée dans un Bocal"] = ((Player.numero_de_letage * 50) + 50) * self.modificateur

    def UseTirage(self):
        #sort ou technique ?
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 50:
            type_tirage = "le sort"
        else:
            type_tirage = "la technique"
        #element ?
        element_tirage = []
        for _ in range(0, 2):
            nombre_aleatoire = random.randint(1, 6)
            if nombre_aleatoire == 1:
                element_tirage.append("Feu")
            if nombre_aleatoire == 2:
                element_tirage.append("Foudre")
            if nombre_aleatoire == 3:
                element_tirage.append("Glace")
            if nombre_aleatoire == 4:
                element_tirage.append("Terre")
            if nombre_aleatoire == 5:
                element_tirage.append("Physique")
            else:
                element_tirage.append("Sang")
        #choix du joueur
        while True:
            try:
                if Player.affronte_un_boss:
                    print(f"A l'endroit ou se tenait l'ennemi, il y a maintenant une petite boite en métal jaune ornée d'un grand *?*.\nVous y plongez la main à l'interieur.")
                else:
                    print(f"Le marchand vous laisse plonger la main dans une boite en carton jaune ornée d'un grand *?*.")
                print("A l'interieur, vous pouvez toucher le contour de deux masses étranges, rugueuse."
                      f"\nEn les palpant, vous ressentez une connection avec l'élément [{element_tirage[0]}] et l'élement [{element_tirage[1]}]."
                      f"\n1 - Retirer le [{element_tirage[0]}]"
                      f"\n2 - Retirer le [{element_tirage[1]}]")
                choix = int(input("Choisissez avec les nombres : "))
                ClearConsole()
                if choix in [1, 2]:
                    break
            except ValueError:
                ClearConsole()
        #construction de la récompense
        #nom commun
        if type_tirage == "le sort":
            if element_tirage[choix - 1] == "Feu":
                nom_du_tirage = "Thermosphère"
            elif element_tirage[choix - 1] == "Foudre":
                nom_du_tirage = "Faisceau"
            elif element_tirage[choix - 1] == "Glace":
                nom_du_tirage = "Pic"
            elif element_tirage[choix - 1] == "Terre":
                nom_du_tirage = "Création"
            elif element_tirage[choix - 1] == "Physique":
                nom_du_tirage = "Explosion"
            elif element_tirage[choix - 1] == "Sang":
                nom_du_tirage = "Dance"
        elif type_tirage == "la technique":
            if element_tirage[choix - 1] == "Feu":
                nom_du_tirage = "Bô"
            elif element_tirage[choix - 1] == "Foudre":
                nom_du_tirage = "Lance"
            elif element_tirage[choix - 1] == "Glace":
                nom_du_tirage = "Katana"
            elif element_tirage[choix - 1] == "Terre":
                nom_du_tirage = "Corne"
            elif element_tirage[choix - 1] == "Physique":
                nom_du_tirage = "Poing"
            elif element_tirage[choix - 1] == "Sang":
                nom_du_tirage = "Dague"
        # bon ou mauvais tirage (seulement etage 7,8)
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 70:
            sort_attaque_forte_pour_etage_7_8 = False
        else:
            sort_attaque_forte_pour_etage_7_8 = True
        #Adjectif
        if Player.numero_de_letage in [1, 2]:
            if element_tirage[choix - 1] == "Feu":
                nom_du_tirage += " Chaud"
            elif element_tirage[choix - 1] == "Foudre":
                nom_du_tirage += " Rapide"
            elif element_tirage[choix - 1] == "Glace":
                nom_du_tirage += " Bleu"
            elif element_tirage[choix - 1] == "Terre":
                nom_du_tirage += " Argile"
            elif element_tirage[choix - 1] == "Physique":
                nom_du_tirage += " Léger"
            elif element_tirage[choix - 1] == "Sang":
                nom_du_tirage += " Volevie"
        elif Player.numero_de_letage in [3, 4]:
            if element_tirage[choix - 1] == "Feu":
                nom_du_tirage += " Brulant"
            elif element_tirage[choix - 1] == "Foudre":
                nom_du_tirage += " Statique"
            elif element_tirage[choix - 1] == "Glace":
                nom_du_tirage += " Froid"
            elif element_tirage[choix - 1] == "Terre":
                nom_du_tirage += " Lapis"
            elif element_tirage[choix - 1] == "Physique":
                nom_du_tirage += " Renforcé"
            elif element_tirage[choix - 1] == "Sang":
                nom_du_tirage += " Siphoneuse"
        elif Player.numero_de_letage in [5, 6]:
            if element_tirage[choix - 1] == "Feu":
                nom_du_tirage += " Enflammé"
            elif element_tirage[choix - 1] == "Foudre":
                nom_du_tirage += " Electrique"
            elif element_tirage[choix - 1] == "Glace":
                nom_du_tirage += " Givré"
            elif element_tirage[choix - 1] == "Terre":
                nom_du_tirage += " Granite"
            elif element_tirage[choix - 1] == "Physique":
                nom_du_tirage += " Lourd"
            elif element_tirage[choix - 1] == "Sang":
                nom_du_tirage += " Vampirique"
        elif Player.numero_de_letage in [7, 8]:
            if element_tirage[choix - 1] == "Feu":
                if sort_attaque_forte_pour_etage_7_8:
                    nom_du_tirage += " de la Fournaise"
                else:
                    nom_du_tirage += " Magmatique"
            elif element_tirage[choix - 1] == "Foudre":
                if sort_attaque_forte_pour_etage_7_8:
                    nom_du_tirage += " de l'Eclair"
                else:
                    nom_du_tirage += " Foudroyante"
            elif element_tirage[choix - 1] == "Glace":
                if sort_attaque_forte_pour_etage_7_8:
                    nom_du_tirage += " GLacial"
                else:
                    nom_du_tirage += " Polaire"
            elif element_tirage[choix - 1] == "Terre":
                if sort_attaque_forte_pour_etage_7_8:
                    nom_du_tirage += " Obsidienne"
                else:
                    nom_du_tirage += " de la Montagne"
            elif element_tirage[choix - 1] == "Physique":
                if sort_attaque_forte_pour_etage_7_8:
                    nom_du_tirage += "Maitrisé"
                else:
                    nom_du_tirage += "Fatal"
            elif element_tirage[choix - 1] == "Sang":
                if sort_attaque_forte_pour_etage_7_8:
                    nom_du_tirage += " Parasite"
                else:
                    nom_du_tirage += " Destructrice"
        elif Player.numero_de_letage in [9, 10]:
            if element_tirage[choix - 1] == "Feu":
                nom_du_tirage += " Solaire"
            elif element_tirage[choix - 1] == "Foudre":
                nom_du_tirage += "de la Mort Blanche"
            elif element_tirage[choix - 1] == "Glace":
                nom_du_tirage += " Zéro"
            elif element_tirage[choix - 1] == "Terre":
                nom_du_tirage += " Continentale"
            elif element_tirage[choix - 1] == "Physique":
                nom_du_tirage += " de la Comète"
            elif element_tirage[choix - 1] == "Sang":
                nom_du_tirage += " Créatrice"
        #Accord au féminin, si besoin
        if nom_du_tirage == "Faisceau Foudroyante":
            nom_du_tirage = "Faisceau Foudroyant"
        elif nom_du_tirage == "Thermosphère Chaud":
            nom_du_tirage = "Thermosphère Chaude"
        elif nom_du_tirage == "Thermosphère Brulant":
            nom_du_tirage = "Thermosphère Brulante"
        elif nom_du_tirage == "Thermosphère Enflammé":
            nom_du_tirage = "Thermosphère Enflammée"
        elif nom_du_tirage == "Création Argile":
            nom_du_tirage = "Création d'Argile"
        elif nom_du_tirage == "Création Lapis":
            nom_du_tirage = "Création de Lapis"
        elif nom_du_tirage == "Création Granite":
            nom_du_tirage = "Création de Granite"
        elif nom_du_tirage == "Explosion Léger":
            nom_du_tirage = "Explosion Légère"
        elif nom_du_tirage == "Explosion Renforcé":
            nom_du_tirage = "Explosion Renforcée"
        elif nom_du_tirage == "Explosion Lourd":
            nom_du_tirage = "Explosion Lourde"
        elif nom_du_tirage == "Explosion Maitrisé":
            nom_du_tirage = "Explosion Maitrisée"
        elif nom_du_tirage == "Explosion Fatal":
            nom_du_tirage = "Explosion Fatale"
        #affichage de la récompense
        if (nom_du_tirage in Player.sorts_possedes) or (nom_du_tirage in Player.techniques_possedes):
            print("Vous retirez un bout de papier !\nIl y est écrit : Des fois on gagne, des fois on perd. L'important, c'est de participer !")
            Affichage.EntreePourContinuer()
        else:
            print(f"Vous retirez {type_tirage} {nom_du_tirage} !")
            Affichage.EntreePourContinuer()
            #application de la recompense
            if type_tirage == "le sort":
                Player.sorts_possedes.append(nom_du_tirage)
            else:
                Player.techniques_possedes.append(nom_du_tirage)

    def DoTrading(self):
        # marchand
        Affichage.AfficheRentrerChezMarchand()
        Trader.SetItemList()
        while True:
            while True:
                try:
                    ClearConsole()
                    Trader.SetRedCoinPrice()
                    print("     -=[ Marchand ]=-")
                    print(f"   Vous avez {Player.nombre_de_gold} golds. ")
                    Trader.ShowItems()
                    choix = int(input("\nChoisissez l'item a prendre avec les nombres : "))
                    if choix in range(1, (len(Trader.liste_item_actuelle) + 2)):
                        break
                except ValueError:
                    ClearConsole()
            if choix in range(2, (len(Trader.liste_item_actuelle) + 2)):
                nom_de_litem = Trader.liste_item_actuelle[choix-2]
                if Player.nombre_de_gold >= Trader.PriceOfItem(nom_de_litem):
                    Player.nombre_de_gold -= Trader.PriceOfItem(nom_de_litem)
                    print(f"Vous avez acheté [{nom_de_litem}] !")
                    Affichage.EntreePourContinuer()
                    if nom_de_litem == "Red Coin":
                        Player.redcoin_bought = True
                        Player.nombre_de_red_coin += 1
                    elif nom_de_litem == "Tirage":
                        Player.number_of_tirage += 1
                        Trader.UseTirage()
                    elif nom_de_litem == "Gemme de Vie":
                        if Player.gemme_de_vie:
                            print("Mais vous en aviez déjà une...\nTant pis.")
                            Affichage.EntreePourContinuer()
                        else:
                            Player.gemme_de_vie = True
                    elif nom_de_litem == "Gemme d'Esprit":
                        if Player.gemme_de_mana:
                            print("Mais vous en aviez déjà une...\nTant pis.")
                            Affichage.EntreePourContinuer()
                        else:
                            Player.gemme_de_mana = True
                    elif nom_de_litem == "Fée dans un Bocal":
                        if Player.possede_une_fee:
                            print("Alors que vous rangiez votre bocal dans votre sacoche,"
                                  " vous voyez les deux fées unir leur pouvoir a travers"
                                  " les bocaux pour briser leur cage de verre et s'enfuir."
                                  "\nUne bonne lecon d'apprise : Jamais plus de deux fées sur soi !")
                            Affichage.EntreePourContinuer()
                            Player.possede_une_fee = False
                        else:
                            Player.possede_une_fee = True
                    else:
                        Player.items_possedes[nom_de_litem] += 1
                else:
                    Affichage.AffichePasAssezDargent()
            elif choix == 1:
                Affichage.AffichePartirMarchand()
                break
            ClearConsole()



class Affiche:

    def __init__(self):
        pass

    def EntreePourContinuer(self):
        input("(Appuyez sur entrée pour continuer)")
        ClearConsole()

    def AfficheIntroCombat(self):
        print("Vous rentrez dans l'arène et jettez un coup d'oeil aux tribunes vides, avant de frapper le sol de votre pied."
              "\nAussitôt, une vague bruyante de spectateurs fantomatiques apparaissent, et un ennemi apparait devant vous.")
        self.EntreePourContinuer()

    def AffichePlusDennemis(self):
        print("Vous rentrez dans l'arène et jettez un coup d'oeil aux tribunes vides, avant de frapper le sol de votre pied."
              "\nMais rien ne se passe.\nIl n'y a plus personne pour vous affronter, a part le boss.")
        if Player.red_coin_recu_par_extermination:
            print("Un spectateur fantomatique amusé par votre désir d'extermination vous envoie un cadeau depuis les gradins, avant de disparaitre.")
            self.EntreePourContinuer()
            print("Vous gagnez un Red Coin !")
            self.EntreePourContinuer()
            Player.nombre_de_red_coin += 1
        self.EntreePourContinuer()

    def AfficheIntroCombatBoss(self):
        print("Vous rentrez dans l'arène et jettez un coup d'oeil aux tribunes vides, avant de frapper le sol de votre pied."
              "\nAussitôt, une vague silencieuse de spectateurs fantomatiques apparaissent, et la grille de métal ancien à l'autre bout de l'arène s'ouvre.")
        self.EntreePourContinuer()
        PlayMusic("boss_intro")
        if Player.numero_de_letage == 1:
            commentaire = (""
                           "\n"
                           "\n")
        elif Player.numero_de_letage == 2:
            commentaire = (""
                           "\n"
                           "\n")
        elif Player.numero_de_letage == 3:
            commentaire = (""
                           "\n"
                           "\n")
        elif Player.numero_de_letage == 4:
            commentaire = (""
                           "\n"
                           "\n")
        elif Player.numero_de_letage == 5:
            commentaire = (""
                           "\n"
                           "\n")
        elif Player.numero_de_letage == 6:
            commentaire = (""
                           "\n"
                           "\n")
        elif Player.numero_de_letage == 7:
            commentaire = (""
                           "\n"
                           "\n")
        elif Player.numero_de_letage == 8:
            commentaire = (""
                           "\n"
                           "\n")
        elif Player.numero_de_letage == 9:
            commentaire = (""
                           "\n"
                           "\n")
        elif Player.numero_de_letage == 10:
            commentaire = (""
                           "\n"
                           "\n")
        print(commentaire)
        Affichage.EntreePourContinuer()

    def AfficheDescente(self):
        print("Vous passez la grille autrefois fermée et vous enfoncez encore plus profondément dans le Coliseum.")
        self.EntreePourContinuer()

    def AfficheRentrerChezMarchand(self):
        print("Vous passez une porte primitive de tissu et rentrez dans une salle miteuse.\n"
              "Devant vous, une figure drapée vous propose des items placés sur un bout de chiffon sale... pour un prix.")
        self.EntreePourContinuer()

    def AffichePasAssezDargent(self):
        print("Vous n'avez pas assez de golds !")
        self.EntreePourContinuer()

    def AffichePartirMarchand(self):
        print("Vous faites un signe au marchand et repassez la porte de tissu.")
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire == 50:
            print("...? Vous jureriez reconnaitre l'embleme cousu sur le chiffon sale."
                  "\nUn griffon a trois tête, cinq ailes, et un bec...le même que celui a l'entrée du coliseum...")
        self.EntreePourContinuer()

    def AfficheChargement(self):
        for nombre in range(1, 7):
            if nombre in [1, 4]:
                print("Chargement en cours.")
            elif nombre in [2, 5]:
                print("Chargement en cours..")
            elif nombre in [3, 6]:
                print("Chargement en cours...")
            time.sleep(0.3)
            ClearConsole()
        print("Chargement Terminé !")
        self.EntreePourContinuer()

    def AffichageDescriptionEtage(self):
        mixer.quit()
        if Player.numero_de_letage == 1:
            commentaire = ("Vous descendez les marches de l'escalier en spirale, et sentez une odeur acre de moisissure monter a vos narines."
                           "\nDes murs crasseux, des gradins en ruine, et un sol de gravier et d'os mélangés vous attendent a la fin."
                           "\nVous voici au premier étage du Coliseum , une ruine mal entretenue.")
        elif Player.numero_de_letage == 2:
            commentaire = ("Vous laissez derrière vous le donjon de pierre fragile, et voyez perler sur le plafond des gouttes d'eau."
                           "\nUne masse informe de plantes extravagantes poussant dans les interstices entre les briques,"
                           "\nune arène envahie par les mauvaises herbes, et une tour de chateau au dessus de la sortie vous attendent en bas."
                           "\nVous voici au deuxieme étage du Coliseum , une forêt (dés)enchantée.")
        elif Player.numero_de_letage == 3:
            commentaire = ("Vous laissez derrière vous l'humiditée excessive, et entendez un bruissement sourd."
                           "\nUn sol jaune granuleux dans lequel on s'enfonce, un étage sans mur, un soleil artificiel et "
                           "\nun vent impossible battant le sable dans vos yeux vous attendent en bas."
                           "\nVous voici au troisième étage du Coliseum , un océan de sable.")
        elif Player.numero_de_letage == 4:
            commentaire = ("Vous laissez derrière vous la sécheresse, et revenez a un environement plus comfortable."
                           "\nDes murs infiniment haut sur lesquels reposent des étagères remplies d'un nombre impossible de livres, "
                           "\ndes plateaux remplis de bouquins volant d'un bout a l'autre de l'arene, et un sol couvert de moquette douce au toucher vous attendent en bas."
                           "\nVous voici au quatrième étage du Coliseum , une tour dédiée a l'étude de la magie.")
        elif Player.numero_de_letage == 5:
            commentaire = ("Vous laissez derrière vous les livres, et entendez une musique entêtante."
                           "\nDes clowns peints sur le mur, des manequins souriants simulant une foule désoeuvrée,"
                           "\ndes fausses attractions fabriquées a la hâte avec quelques bouts de carton ,"
                           "\net de vieilles enceintes crachant une musique joyeuse en boucle vous attendent en bas."
                           "\nVous voici au cinquième étage du Coliseum , une misérable fête foraine.")
        elif Player.numero_de_letage == 6:
            commentaire = ("Vous laissez derrière vous la fête, et ressentez une présence particulière."
                           "\nUn bidonville vide de monde, dans lequel sont parsemés horloges montres et alarmes brisées, "
                           "\ndes vieilles banderoles trouées accrochées au plafond, et une gigantesque tour d'horloge au milieu de l'arène vous attendent en bas."
                           "\nVous entendez le tic particulier d'un mécanisme, mais l'aiguille des secondes est coincée sur 13h42."
                           "\nVous voici au sixième étage du Coliseum , une fracture entre temps et société de quartiers pauvres.")
        elif Player.numero_de_letage == 7:
            commentaire = ("Vous laissez derrière vous le royaume du prince des voleurs, et sentez la température augmenter."
                           "\nDes flammes inextinguibles, des cris sans réponses venant de nulle part, des cadavres accrochés a différents instruments de torture, "
                           "\net le mot *Traitre* écrit a l'aide de différents type **d'encre** sur tout les murs de l'arène, telle est la vision qui vous attend en bas."
                           "\nVous voici au septieme étage du Coliseum , le bac à sable d'un esprit fou, torturé, paranoïaque.")
        elif Player.numero_de_letage == 8:
            commentaire = ("Vous laissez derrière vous les cris de désespoirs, et vous concentrez sur le but."
                           "\nDes murs propres, neufs, ornés de torches. Un sol de marbre, dépassant les gradins, montant au plafond. Et une place au dessus de la sortie,"
                           "\nsur laquelle se trouve un vieil homme à la barbe blanche, soignée. Voila ce que vous trouvez en bas."
                           "\nVous voici au huitième étage du Coliseum , une arène digne de ce nom pour un affrontement avec son créateur.")
        elif Player.numero_de_letage == 9:
            commentaire = ("Vous laissez derrière vous la sortie et les promesses de vie facile à la poursuite de la véritée."
                           "\nUn étage étrange, ou la fabrique de la réalitée semble venir mourir a vos pied."
                           "\nVous pouvez retrouver un élément de chaque étages sur le sol froid de l'arène, et quand ce n'est pas leur couleur, c'est leur proportion qui varie."
                           "\nCertaines banderolles sont encastrés dans le mur, des carrés de sables sortent ca et la de nulle part, "
                           "\net vous êtes a peu pres sur que la géométrie des lieux est non euclidienne vu que vous pouvez traverser la salle en un pas si vous passez au bon endroit."
                           "\nVous voici au neuvième étage du Coliseum , une poubelle ou viennent reposer les concepts oubliés.")
        elif Player.numero_de_letage == 10:
            commentaire = ("Vous laissez derrière vous le cimetière erroné et avancez vers la fin de votre voyage."
                           "\nUne salle blanche vous attend en bas. Tout est blanc, et vous n'arrivez pas a définir les limites de la salle. Il n'y a que le nécessaire."
                           "\nVous voici au dixième étage du Coliseum , la pénultième vision.")
        elif Player.numero_de_letage == 11:
            commentaire = ("Derrière, vous retrouvez le chant des oiseaux, l'herbe verte, et le grillage"
                           " caractéristique entourant le Coliseum.\nVous êtes sorti vivant, riche, et puissant !")
        print(commentaire)
        Affichage.EntreePourContinuer()

     

class PlayerCaracteristics:

    def __init__(self):
        self.gemme_de_vie = False
        self.gemme_de_mana = False
        self.possede_une_fee = False
        self.nom_du_personnage = ""
        self.stigma_positif = ""
        self.stigma_negatif = ""
        self.stigma_bonus = ""
        self.techniques_possedes = ""
        self.sorts_possedes = ""
        self.items_possedes = DICTIONNAIREITEMINITIAL
        self.talents_possedes = ""
        self.points_de_vie_max = 0
        self.points_de_vie = 0
        self.points_de_mana_max = 0
        self.points_de_mana = 0
        self.points_de_force = 0
        self.points_dintelligence = 0
        self.points_de_defence = 0
        self.taux_coup_critique = 0
        self.degat_coup_critique = 0
        self.taux_sort_critique = 0
        self.degat_sort_critique = 0
        self.taux_desquive = 0
        self.nombre_de_gold = 0
        self.nombre_de_red_coin = 0
        self.nombre_de_monstres_tues = 0
        self.numero_de_letage = 1
        self.affronte_un_boss = False
        self.affronte_une_mimique = False
        self.quete = "None"
        self.boss_battu = False
        self.commentaire_boss = "Affronter le Boss"
        self.nombre_dennemis_a_letage = 15
        self.red_coin_recu_par_extermination = False
        self.redcoin_bought = False
        self.number_of_tirage = 0

    def UseCharacterForInitCaracteristics(self, caracteristiques):
        self.nom_du_personnage = caracteristiques[0]
        self.stigma_positif = caracteristiques[2]
        self.stigma_negatif = caracteristiques[3]
        self.stigma_bonus = caracteristiques[4]
        self.techniques_possedes = caracteristiques[5]
        self.sorts_possedes = caracteristiques[6]
        liste_item_a_mettre_a_jour = caracteristiques[7]
        for item in liste_item_a_mettre_a_jour:
            self.items_possedes[item] = liste_item_a_mettre_a_jour[item]
        self.talents_possedes = caracteristiques[8]
        self.points_de_vie_max = caracteristiques[9]
        self.points_de_vie = caracteristiques[9]
        self.points_de_mana_max = caracteristiques[10]
        self.points_de_mana = caracteristiques[10]
        self.points_de_force = caracteristiques[11]
        self.points_dintelligence = caracteristiques[12]
        self.points_de_defence = caracteristiques[13]
        self.taux_coup_critique = caracteristiques[14]
        self.degat_coup_critique = caracteristiques[15]
        self.taux_sort_critique = caracteristiques[16]
        self.degat_sort_critique = caracteristiques[17]
        self.taux_desquive = caracteristiques[18]
        self.nombre_de_gold = caracteristiques[19]

    def ShowcaseCaracteristics(self):
        liste_artefacts = self.PutArtefactInList()
        print(f"          -={{ {Player.nom_du_personnage} }}=-")
        print( f"\nPoints de vie : {Player.points_de_vie}/{Player.points_de_vie_max}"
              f"\nPoints de mana : {Player.points_de_mana}/{Player.points_de_mana_max}"
              f"\nPoints de force : {Player.points_de_force} | Points d'intelligence : {Player.points_dintelligence}"
              f"\nPoints de defence : {Player.points_de_defence}"
              f"\nChance de coup critique : {Player.taux_coup_critique}% | Degats de coup critique : {Player.degat_coup_critique}"
              f"\nChance de sort critique : {Player.taux_sort_critique}% | Degats de sort critique : {Player.degat_sort_critique}"
              f"\nChance d'esquive : {Player.taux_desquive}%"
              f"\nNombre de Golds : {Player.nombre_de_gold} | Nombre de Redcoins : {Player.nombre_de_red_coin}"
              f"\nNombre de monstres tués : {Player.nombre_de_monstres_tues}"
              f"\nQuête en cours : {Player.quete}"
              f"\nTechniques apprises : {Player.techniques_possedes}"
              f"\nSorts appris : {Player.sorts_possedes}"
              f"\nTalents possédés : {Player.talents_possedes}"
              f"\nArtefacts : {liste_artefacts}"
              f"\nStigmas + : {Player.stigma_positif} | Stigmas - : {Player.stigma_negatif} | Stigmas * : {Player.stigma_bonus}"
              "\n \n          -={{ Items }}=-"
              "\n1 - Retour")
        Player.AffichageItem()
        return int(input("\nChoisissez une action avec les nombres : "))

    def AffichageItem(self):
        self.liste_ditem_a_afficher = []
        for item in Player.items_possedes:
            if Player.items_possedes[item] == 0:
                continue
            self.liste_ditem_a_afficher.append(item)
        numero_de_laffichage = 2
        for item in self.liste_ditem_a_afficher:
            print(f"{numero_de_laffichage} - {item} : {Player.items_possedes[item]}")
            numero_de_laffichage += 1

    def PutArtefactInList(self):
        liste_artefact = []
        if Player.gemme_de_vie:
            liste_artefact.append("Gemme de Vie")
        if Player.gemme_de_mana:
            liste_artefact.append("Gemme d'Esprit")
        if Player.possede_une_fee:
            liste_artefact.append("Fée dans un Bocal")
        if len(liste_artefact) == 0:
            liste_artefact.append("Aucun")
        return liste_artefact

    def ShowPlayerCaracteristicsAndItems(self):
        ClearConsole()
        dans_le_menu = True
        while dans_le_menu:
            while True:
                try:
                    choix = Player.ShowcaseCaracteristics()
                    ClearConsole()
                    if choix in range(1, (len(self.liste_ditem_a_afficher) + 2)):
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                ClearConsole()
                dans_le_menu = False
            else:
                item_a_utiliser = self.liste_ditem_a_afficher[choix - 2]
                Player.UseItem(item_a_utiliser)

    def UseItem(self, item):
        if item in ["Feuille Jindagee", "Fruit Jindagee"]:
            Player.items_possedes[item] -= 1
            if item == "Feuille Jindagee":
                soin = 5 * round(self.points_de_vie_max * 0.03)
            elif item == "Fruit Jindagee":
                soin = 5 * round(self.points_de_vie_max * 0.06)
            if self.stigma_positif == "Pharmacodynamisme":
                soin += soin
            self.points_de_vie += soin
            if Player.points_de_vie > Player.points_de_vie_max:
                Player.points_de_vie = Player.points_de_vie_max
            print(f"Vous utilisez l'item [{item}], et regagnez {soin} points de vie en peu de temps !")
        elif item in ["Feuille Aatma", "Fruit Aatma"]:
            Player.items_possedes[item] -= 1
            if item == "Feuille Aatma":
                soin = 5 * round(self.points_de_mana_max * 0.03)
            elif item == "Fruit Aatma":
                soin = 5 * round(self.points_de_mana_max * 0.06)
            if self.stigma_positif == "Pharmacodynamisme":
                soin += soin
            self.points_de_mana += soin
            if Player.points_de_mana > Player.points_de_mana_max:
                Player.points_de_mana = Player.points_de_mana_max
            print(f"Vous utilisez l'item [{item}], et regagnez {soin} points de mana en peu de temps !")
        elif item in ["Remède", "Remède Superieur", "Remède Divin"]:
            Player.items_possedes[item] -= 1
            if item == "Remède":
                soin = round(Player.points_de_vie_max*0.1)
                if soin < 10:
                    soin = 10
            elif item == "Remède Superieur":
                soin = round(Player.points_de_vie_max*0.2)
                if soin < 20:
                    soin = 20
            elif item == "Remède Divin":
                soin = round(Player.points_de_vie_max*0.3)
                if soin < 30:
                    soin = 30
            if self.stigma_positif == "Pharmacodynamisme":
                soin += soin
            Player.points_de_vie += soin
            if Player.points_de_vie > Player.points_de_vie_max:
                Player.points_de_vie = Player.points_de_vie_max
            print(f"Vous appliquez le remède sur vos blessures et regagnez {soin} points de vie !")
        elif item in ["Pillule", "Pillule Superieure", "Pillule Divine"]:
            Player.items_possedes[item] -= 1
            if item == "Pillule":
                soin = round(Player.points_de_mana_max*0.1)
                if soin < 10:
                    soin = 10
            elif item == "Pillule Superieure":
                soin = round(Player.points_de_mana_max*0.2)
                if soin < 20:
                    soin = 20
            elif item == "Pillule Divine":
                soin = round(Player.points_de_mana_max*0.3)
                if soin < 30:
                    soin = 30
            if self.stigma_positif == "Pharmacodynamisme":
                soin += soin
            Player.points_de_mana += soin
            if Player.points_de_mana > Player.points_de_mana_max:
                Player.points_de_mana = Player.points_de_mana_max
            print(f"Vous avalez la pillule et regagnez {soin} points de mana !")
        else:
            print(f"Vous preferez garder l'item [{item}] pour les combats.")
        Affichage.EntreePourContinuer()



class Observe:

    def __init__(self):
        pass

    def SeeSomething(self):
        if Player.numero_de_letage==1:
            DoTheThing()  # bibliotheque de gros sorts (recuperer les sorts consignés)
        elif Player.numero_de_letage == 2:
            DoTheThing()  # Fontaine redonne pv 3 fois
        elif Player.numero_de_letage == 3:
            DoTheThing()  # Gacha game a mutations
        elif Player.numero_de_letage == 4:
            DoTheThing()  # machine a gold a sang
        elif Player.numero_de_letage == 5:
            DoTheThing()  # bibliotheque de gros sorts (choisir sort a apprendre, choisir sort a consigner)
        elif Player.numero_de_letage == 6:
            DoTheThing()  # fantome des quetes ultimes
        elif Player.numero_de_letage == 7:
            DoTheThing()  # alchimiste divin demande manamax
        elif Player.numero_de_letage == 8:
            DoTheThing()  # rituels de sang pour chance critiques
        elif Player.numero_de_letage == 9:
            DoTheThing()  # Porte demande 100 red coins pour etre ouverte (reste par partie), débloque un gauntlet de 50 ennemis pour avoir ame
        elif Player.numero_de_letage == 10:
            DoTheThing()  # Affronte Alfred pour plein de récompenses


class SaveManagement:

    def __init__(self):
        self.dictionnaire_de_sauvegarde = {
            "Nom": "",
            "Stigma Positif": "",
            "Stigma Négatif": "",
            "Stigma Bonus": "",
            "Techniques": "",
            "Sorts": "",
            "Items": "",
            "Talents": "",
            "Points de vie max": "",
            "Points de vie": "",
            "Points de mana max": "",
            "Points de mana": "",
            "Points de force": "",
            "Points d'intelligence": "",
            "Points de defence": "",
            "Chance de coup critique": "",
            "Degat de coup critique": "",
            "Chance de sort critique": "",
            "Degat de sort critique": "",
            "Chance d'esquive": "",
            "Nombre de gold": "",
            "Nombre de Redcoins": "",
            "Nombre de monstres tués": "",
            "Numéro de l'etage": "",
            "Quete en cours": "",
            "Le Boss a ete Battu": "",
            "Commentaire pour l'affichage du Boss dans le menu": "",
            "Nombre_d'ennemis restant a l'étage": "",
            "Le Redcoin d'extermination a ete recu": "",
            "Le Redcoin du marchand a ete achete": "",
            "Nombre de Tirage acheté": "",
            "Possede une gemme de vie": "",
            "Possede une gemme de mana": "",
            "Possede une fée": ""
        }

    def FromPlayerToDict(self):
        self.dictionnaire_de_sauvegarde["Nom"] = Player.nom_du_personnage
        self.dictionnaire_de_sauvegarde["Stigma Positif"] = Player.stigma_positif
        self.dictionnaire_de_sauvegarde["Stigma Négatif"] = Player.stigma_negatif
        self.dictionnaire_de_sauvegarde["Stigma Bonus"] = Player.stigma_bonus
        self.dictionnaire_de_sauvegarde["Techniques"] = Player.techniques_possedes
        self.dictionnaire_de_sauvegarde["Sorts"] = Player.sorts_possedes
        self.dictionnaire_de_sauvegarde["Items"] = Player.items_possedes
        self.dictionnaire_de_sauvegarde["Talents"] = Player.talents_possedes
        self.dictionnaire_de_sauvegarde["Points de vie max"] = Player.points_de_vie_max
        self.dictionnaire_de_sauvegarde["Points de vie"] = Player.points_de_vie
        self.dictionnaire_de_sauvegarde["Points de mana max"] = Player.points_de_mana_max
        self.dictionnaire_de_sauvegarde["Points de mana"] = Player.points_de_mana
        self.dictionnaire_de_sauvegarde["Points de force"] = Player.points_de_force
        self.dictionnaire_de_sauvegarde["Points d'intelligence"] = Player.points_dintelligence
        self.dictionnaire_de_sauvegarde["Points de defence"] = Player.points_de_defence
        self.dictionnaire_de_sauvegarde["Chance de coup critique"] = Player.taux_coup_critique
        self.dictionnaire_de_sauvegarde["Degat de coup critique"] = Player.degat_coup_critique
        self.dictionnaire_de_sauvegarde["Chance de sort critique"] = Player.taux_sort_critique
        self.dictionnaire_de_sauvegarde["Degat de sort critique"] = Player.degat_sort_critique
        self.dictionnaire_de_sauvegarde["Chance d'esquive"] = Player.taux_desquive
        self.dictionnaire_de_sauvegarde["Nombre de gold"] = Player.nombre_de_gold
        self.dictionnaire_de_sauvegarde["Nombre de Redcoins"] = Player.nombre_de_red_coin
        self.dictionnaire_de_sauvegarde["Nombre de monstres tués"] = Player.nombre_de_monstres_tues
        self.dictionnaire_de_sauvegarde["Numéro de l'etage"] = Player.numero_de_letage
        self.dictionnaire_de_sauvegarde["Quete en cours"] = Player.quete
        self.dictionnaire_de_sauvegarde["Le Boss a ete Battu"] = Player.boss_battu
        self.dictionnaire_de_sauvegarde["Commentaire pour l'affichage du Boss dans le menu"] = Player.commentaire_boss
        self.dictionnaire_de_sauvegarde["Nombre_d'ennemis restant a l'étage"] = Player.nombre_dennemis_a_letage
        self.dictionnaire_de_sauvegarde["Le Redcoin d'extermination a ete recu"] = Player.red_coin_recu_par_extermination
        self.dictionnaire_de_sauvegarde["Le Redcoin du marchand a ete achete"] = Player.redcoin_bought
        self.dictionnaire_de_sauvegarde["Nombre de Tirage acheté"] = Player.number_of_tirage
        self.dictionnaire_de_sauvegarde["Possede une gemme de vie"] = Player.gemme_de_vie
        self.dictionnaire_de_sauvegarde["Possede une gemme de mana"] = Player.gemme_de_mana
        self.dictionnaire_de_sauvegarde["Possede une fée"] = Player.possede_une_fee

    def FromDictToPlayer(self):
        Player.nom_du_personnage = ((self.dictionnaire_de_sauvegarde["Nom"]).strip('"'))
        Player.stigma_positif = ((self.dictionnaire_de_sauvegarde["Stigma Positif"]).strip('"'))
        Player.stigma_negatif = ((self.dictionnaire_de_sauvegarde["Stigma Négatif"]).strip('"'))
        Player.stigma_bonus = ((self.dictionnaire_de_sauvegarde["Stigma Bonus"]).strip('"'))
        chaine_de_caractere = (self.dictionnaire_de_sauvegarde["Techniques"])
        liste_de_technique = ast.literal_eval(chaine_de_caractere)
        Player.techniques_possedes = liste_de_technique
        chaine_de_caractere = (self.dictionnaire_de_sauvegarde["Sorts"])
        liste_de_sorts = ast.literal_eval(chaine_de_caractere)
        Player.sorts_possedes = liste_de_sorts
        chaine_de_caractere = (self.dictionnaire_de_sauvegarde["Items"])
        dictionaire_de_item = ast.literal_eval(chaine_de_caractere)
        Player.items_possedes = dictionaire_de_item
        chaine_de_caractere = (self.dictionnaire_de_sauvegarde["Talents"])
        liste_de_talent = ast.literal_eval(chaine_de_caractere)
        Player.talents_possedes = liste_de_talent
        Player.points_de_vie_max = int(self.dictionnaire_de_sauvegarde["Points de vie max"])
        Player.points_de_vie = int(self.dictionnaire_de_sauvegarde["Points de vie"])
        Player.points_de_mana_max = int(self.dictionnaire_de_sauvegarde["Points de mana max"])
        Player.points_de_mana = int(self.dictionnaire_de_sauvegarde["Points de mana"])
        Player.points_de_force = int(self.dictionnaire_de_sauvegarde["Points de force"])
        Player.points_dintelligence = int(self.dictionnaire_de_sauvegarde["Points d'intelligence"])
        Player.points_de_defence = int(self.dictionnaire_de_sauvegarde["Points de defence"])
        Player.taux_coup_critique = int(self.dictionnaire_de_sauvegarde["Chance de coup critique"])
        Player.degat_coup_critique = int(self.dictionnaire_de_sauvegarde["Degat de coup critique"])
        Player.taux_sort_critique = int(self.dictionnaire_de_sauvegarde["Chance de sort critique"])
        Player.degat_sort_critique = int(self.dictionnaire_de_sauvegarde["Degat de sort critique"])
        Player.taux_desquive = int(self.dictionnaire_de_sauvegarde["Chance d'esquive"])
        Player.nombre_de_gold = int(self.dictionnaire_de_sauvegarde["Nombre de gold"])
        Player.nombre_de_red_coin = int(self.dictionnaire_de_sauvegarde["Nombre de Redcoins"])
        Player.nombre_de_monstres_tues = int(self.dictionnaire_de_sauvegarde["Nombre de monstres tués"])
        Player.numero_de_letage = int(self.dictionnaire_de_sauvegarde["Numéro de l'etage"])
        Player.affronte_un_boss = False
        Player.affronte_une_mimique = False
        Player.gemme_de_vie = ast.literal_eval(self.dictionnaire_de_sauvegarde["Possede une gemme de vie"])
        Player.gemme_de_mana = ast.literal_eval(self.dictionnaire_de_sauvegarde["Possede une gemme de mana"])
        Player.possede_une_fee = ast.literal_eval(self.dictionnaire_de_sauvegarde["Possede une fée"])
        Player.quete = ((self.dictionnaire_de_sauvegarde["Quete en cours"]).strip('"'))
        Player.boss_battu = ast.literal_eval(self.dictionnaire_de_sauvegarde["Le Boss a ete Battu"])
        Player.commentaire_boss = ((self.dictionnaire_de_sauvegarde["Commentaire pour l'affichage du Boss dans le menu"]).strip('"'))
        Player.nombre_dennemis_a_letage = int(self.dictionnaire_de_sauvegarde["Nombre_d'ennemis restant a l'étage"])
        Player.red_coin_recu_par_extermination = ast.literal_eval(self.dictionnaire_de_sauvegarde["Le Redcoin d'extermination a ete recu"])
        Player.redcoin_bought = ast.literal_eval(self.dictionnaire_de_sauvegarde["Le Redcoin du marchand a ete achete"])
        Player.number_of_tirage = int(self.dictionnaire_de_sauvegarde["Nombre de Tirage acheté"])


    def FromDictToSaveFile(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        chemin_du_fichier_save = dir_path + "\\stuff\\save.txt"
        with open(chemin_du_fichier_save, "w") as fichier:
            fichier.write("Caracteristique|Valeur")
            for caracteristic in self.dictionnaire_de_sauvegarde:
                fichier.write(f"\n{caracteristic}|{self.dictionnaire_de_sauvegarde[caracteristic]}")

    def FromSaveFileToDict(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        chemin_du_fichier_save = dir_path + "\\stuff\\save.txt"
        with open(chemin_du_fichier_save, "r") as fichier:
            reader = csv.DictReader(fichier, delimiter="|")
            for line in reader:
                self.dictionnaire_de_sauvegarde[line["Caracteristique"]] = line["Valeur"]

    def SaveTheGame(self):
        self.FromPlayerToDict()
        self.FromDictToSaveFile()
        sys.exit()

    def LoadTheGame(self):
        self.FromSaveFileToDict()
        self.FromDictToPlayer()
        return True
    
    


def ClearConsole():
    # Vérifier le système d'exploitation pour déterminer la commande appropriée
    os.system('cls' if os.name == 'nt' else 'clear')


def GetMenuPrincipalChoice():
    print("                                    \            / ")
    print("                                     \          / ")
    print("                                      \        / ")
    print("                                       \      / ")
    print("                      ||||||||||||||    \    /  ")
    print("                    ||||||||||||         \  /  ")
    print("                 ||||||||                 \/ ")
    print("_______________||||||||___________________/\_______________________________________________ ")
    print("               ||||||||                   \/ ")
    print("               ||||||||                   /\ ")
    print("               ||||||||                  /  \  ____    ____ ")
    print("               ||||||||     ||||    ||  / || \||      ||     ||  ||    ||  || ")
    print("     _,---,_   ||||||||   |||  |||  || /  ||  \||||   |===   ||  ||  ||  ||  || ")
    print("   /'_______`\ |||||||||    ||||    \|||  ||  ____||  ||___   ||||   ||  ||  || ")
    print("  (/'       `\|__||||||||||--------------------\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"---------------------, ")
    print("  *\#########||__________                                                               /' ")
    print("  * ^^^^^^^^^||          \"\"\"\"\"\"\"\"\"\"\"\"------------____________                         /' ")
    print("              \                   /                \          \"\"\"\"\"\"\"\"\"\"\"\"-----_____/' ")
    print("                                 /                  \ ")
    print("                                /                    \ ")
    print("                               /     1 - Nouvelle Partie")
    print("                              /      2 - Continuer     \ ")
    print("                             /       3 - Tutoriel       \ ")
    print("                            /                            \ ")
    print("                           /                              \ ")
    return int(input("Choisissez une action avec le numéro correspondant, et appuyez sur Entrée pour continuer : "))


def PlayMusic(musique):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    musique = dir_path + f"\\stuff\\{musique}.mp3"
    mixer.init()
    mixer.music.load(musique)
    mixer.music.play(-1)


def ChoseCharacter(Player):
    ClearConsole()
    #recommence jusqu'a ce que le choix soit fait
    while True:
        #Choix du personnage
        while True:
            try:
                choix = GetChoixPersonnageChoice()
                ClearConsole()
                if choix == 1:
                    #retour
                    return False
                elif choix in range(2, (len(LISTEDEPERSONNAGE) + 2)):
                    # personnage a afficher
                    break
            except ValueError:
                ClearConsole()
        #Initilaisation des informations du personage selectionné
        nom_du_personnage = DICTIONNAIREDEPERSONNAGEAAFFICHER[choix]
        caracteristiques_du_personnage = LISTEDEPERSONNAGE[nom_du_personnage]
        #Affichage du personnage et validation
        while True:
            try:
                validation_du_personnage = GetPersonnageValideChoice(caracteristiques_du_personnage)
                ClearConsole()
                if validation_du_personnage == 2:
                    #personnage selectionné
                    Player.UseCharacterForInitCaracteristics(caracteristiques_du_personnage)
                    return True
                elif validation_du_personnage == 1:
                    #retour
                    break
            except ValueError:
                ClearConsole()


# 0nom 1description 2stigma+ 3stigma- 4stigma* 5techniques 
# 6sorts 7items 8talents 9vie 10mana 11force
# 12inteligence 13defence 14tauxcoupcrit
# 15degatcoupcrit 16tauxsortcrit 17degatsortcrit
# 18tauxesquive 19gold
def GetPersonnageValideChoice(caracteristiques):
    print(f"     -= {caracteristiques[0]} =-"
          "\n"
          f"\nHistoire : {caracteristiques[1]}"
          f"\nStigma positif : {caracteristiques[2]}"
          f"\nStigma négatif: {caracteristiques[3]}"
          f"\nStigma bonus : {caracteristiques[4]}"
          f"\nTechniques : {caracteristiques[5]}"
          f"\nSorts : {caracteristiques[6]}"
          f"\nItems : {caracteristiques[7]}"
          f"\nTalents : {caracteristiques[8]}"
          f"\nVie : {caracteristiques[9]} Mana : {caracteristiques[10]}"
          f"\nForce : {caracteristiques[11]} Intelligence : {caracteristiques[12]} Défence : {caracteristiques[13]}"
          f"\nChance bonus de coup critique : {caracteristiques[14]} Dégats bonus de coup critique : {caracteristiques[15]}"
          f"\nChance bonus de sort critique : {caracteristiques[16]} Dégats bonus de sort critique : {caracteristiques[17]}"
          f"\nChance d'esquive : {caracteristiques[18]}"
          f"\nNombre de Gold : {caracteristiques[19]}"
          "\n \n1 - Retour"
          "\n2 - Choisir ce personnage"
          "\n"
    )
    return int(input("\nChoisissez une action avec le nombre correspondant : "))


def GetChoixPersonnageChoice():
    print("     -={ Personnages }=-")
    print("\n1 - Retour")
    for numero in DICTIONNAIREDEPERSONNAGEAAFFICHER:
        print(f"{numero} - {DICTIONNAIREDEPERSONNAGEAAFFICHER[numero]}")
    return int(input("\nChoisissez un personnage avec le nombre correspondant : "))


def InitialiseDictionnaireDePersonnageAAfficher():
    numero_du_personnage = 2
    for nom_personnage in LISTEDEPERSONNAGE:
        DICTIONNAIREDEPERSONNAGEAAFFICHER[numero_du_personnage] = nom_personnage
        numero_du_personnage += 1


def MenuDeDemarrage(Player):
    ClearConsole()
    InitialiseDictionnaireDePersonnageAAfficher()
    in_menu_principal = True
    PlayMusic("start")
    while in_menu_principal:
        while True:
            try:
                # affiche le menu
                choix = GetMenuPrincipalChoice()
                ClearConsole()
                if choix in [1, 2, 3, 1521951822120151892113]:
                    break
            except ValueError:
                ClearConsole()

        # choix du personnage
        if choix == 1:
            personnage_a_ete_choisi = ChoseCharacter(Player)
            if personnage_a_ete_choisi:
                # personnage choisi
                in_menu_principal = False
                Affichage.AffichageDescriptionEtage()

        # continuer une partie sauvegardee
        elif choix == 2:
            personnage_a_ete_choisi = Save.LoadTheGame()
            if personnage_a_ete_choisi:
                # sauvegarde chargée dans la classe Joueur
                in_menu_principal = False
                Affichage.AfficheChargement()

        # tutorial
        elif choix == 3:
            ShowTutorial()

        #Observatoire de musique
        elif choix == 1521951822120151892113:
            ShowObservatorium()


def ShowObservatorium():
    PlayMusic("observatorium")
    while True:
        while True:
            try:
                # affiche le menu
                choix = ShowMenuObservatorium()
                ClearConsole()
                if choix in range(1, (len(LISTEDEMUSIQUE)) + 2):
                    break
            except ValueError:
                ClearConsole()
        if choix == 1:
            PlayMusic("start")
            break
        else:
            caracteristique_musique = LISTECARACTERISTIQUEMUSIQUE[choix - 2]
            PlayMusic(f"{caracteristique_musique[0]}")
            print(caracteristique_musique[1])
            print("\n\n\n")
            Affichage.EntreePourContinuer()
            ClearConsole()
        PlayMusic("observatorium")


def ShowMenuObservatorium():
    numero_affichage = 2
    print("  ~~{ Observatorium }~~")
    print("\n1 - Retour")
    for nom_musique in LISTEDEMUSIQUE:
        print(f"{numero_affichage} - {nom_musique}")
        numero_affichage += 1
    return int(input("\nChoisissez la musique avec les nombres : "))


def GetChoiceMenuColiseum():
    print(f"             -=[ Etage {Player.numero_de_letage} ]=-"
          "\n\n          ~~{ Combat }~~"
          f"\n     1 - Affronter un monstre ({Player.nombre_dennemis_a_letage} restants)"
          f"\n     2 - {Player.commentaire_boss}"
          "\n\n          ~~{ Interraction }~~"
          "\n      3 - Interragir avec le Marchand"
          "\n      4 - Observer l'Etage (WIP)"
          f"\n\n          ~~{{ {Player.nom_du_personnage} }}~~"
          "\n      5 - Fiche de Personnage"
          "\n      6 - Utiliser un Red Coin"
          "\n      7 - Sauvegarder et Quitter"
          "\n\n")
    return int(input("Choisissez une action avec les nombres : "))


def RemiseAZeroDesVariablesPourProchainEtage():
    Player.affronte_un_boss = False
    Player.boss_battu = False
    Player.redcoin_bought = False
    Player.red_coin_recu_par_extermination = False
    Player.nombre_dennemis_a_letage = 15 + Player.numero_de_letage * 2
    Player.commentaire_boss = "Affronter le Boss"
    Player.quete = "None"


def DoFight():
    #combat contre ennemi
    if Player.nombre_dennemis_a_letage != 0:
        Affichage.AfficheIntroCombat()
        # initialise la classe controleur, et par extention la classe
        #       vue et modele
        control = controleur.Control(Player, Trader)
        # lance la bataille
        control.Battle()
        PlayMusic(f"etage_{Player.numero_de_letage}")
        Player.nombre_dennemis_a_letage -= 1
    #plus dennemi a combattre
    else:
        Affichage.AffichePlusDennemis()
        Player.red_coin_recu_par_extermination = True


def DoBossFight():
    Affichage.AfficheIntroCombatBoss()
    Player.affronte_un_boss = True
    control = controleur.Control(Player, Trader)
    control.Battle()
    PlayMusic(f"etage_{Player.numero_de_letage}")
    Player.affronte_un_boss = False
    Player.boss_battu = True
    Player.commentaire_boss = "Descendre a l'étage inferieur"


def GoDown():
    Affichage.AfficheDescente()
    Player.numero_de_letage += 1
    RemiseAZeroDesVariablesPourProchainEtage()
    Affichage.AffichageDescriptionEtage()
    if Player.numero_de_letage == 11 :
        game_in_session = False
    else:
        game_in_session = True
    return game_in_session


def DoRedcoin():
    while True:
        while True:
            try:
                print("     -={ RedCoin }=-   /96219874637545247624572858712286971176")
                print("                      /742698563215698521568521585215656256665     ")
                print("1 - Retour           /7896545685698742315698522685256985632596   ")
                print("1257 - Affinité de F/52565265163512ERRORERRORERRORERRORERROR98 ")
                print("5675 - Affinité de /487965651268416535498165319651965ERRORROOR  ")
                print("9731 - Affi_______/7895412156985116484156341653196516519651988  ")
                print("7563 - Af/78451235896652567841961561653163165ERRORERRORERROR58   ")
                print("8240 - A/78456213657898456532698562598416368416358614896589465 ")
                print("6______/789528935651468251534253465131651650165100651651313135 ")
                print("/5698994524527/==================================\9885ERRORE88 ")
                print("1569899452452/alent à débloquer avec le nombre cor\84522456852")
                choix = int(input("                              "))
                ClearConsole()
                if choix in ANNUAIREDECHOIXPOURREDCOIN or choix == 1:
                    break
            except ValueError:
                ClearConsole()
        if choix == 1:
            break
        caracteristique_du_talent = ANNUAIREDECHOIXPOURREDCOIN[choix]
        talent = caracteristique_du_talent[0]
        cout_du_talent = caracteristique_du_talent[1]
        talent_necessaire_pour_obtention = caracteristique_du_talent[2]
        if (
            (Player.nombre_de_red_coin >= cout_du_talent) and (talent_necessaire_pour_obtention == "None") and (talent not in Player.talents_possedes)
            or
            (Player.nombre_de_red_coin >= cout_du_talent) and (talent_necessaire_pour_obtention in Player.talents_possedes) and (talent not in Player.talents_possedes)
        ):
            Player.talents_possedes.append(talent)
            Player.nombre_de_red_coin -= cout_du_talent
            print("Vous buvez le liquide incolore contenu dans les redcoins et faites circuler votre mana comme indiqué par le code .")
            print(f"Vous gagnez le talent [{talent}] !")
            Affichage.EntreePourContinuer()
            CheckForFusionOfTalent(talent)

    
def CheckForFusionOfTalent(talent):
    commentaire = "...?"
    if talent in ["Oeuil Magique", "Pira", "Elektron", "Tsumeta-Sa", "Mathair", "Fos", "Haddee"]:
        if "Oeuil Magique" in Player.talents_possedes:
            if "Pira" in Player.talents_possedes:
                commentaire += "\nLes talents Oeuil Magique et Pira interragissent dans votre corps et donnent naissance a un nouveau talent !"
                talent = "Oculus Ignis"
                Player.talents_possedes.append(talent)
                commentaire += (f"\nVous gagnez le talent [{talent}] !")
            if "Elektron" in Player.talents_possedes:
                commentaire += "\nLes talents Oeuil Magique et Elektron interragissent dans votre corps et donnent naissance a un nouveau talent !"
                talent = "Oculus de Caelo"
                Player.talents_possedes.append(talent)
                commentaire += (f"\nVous gagnez le talent [{talent}] !")
            if "Tsumeta-Sa" in Player.talents_possedes:
                commentaire += "\nLes talents Oeuil Magique et Tsumeta-Sa interragissent dans votre corps et donnent naissance a un nouveau talent !"
                talent = "Oculus Glacies"
                Player.talents_possedes.append(talent)
                commentaire += (f"\nVous gagnez le talent [{talent}] !")
            if "Mathair" in Player.talents_possedes:
                commentaire += "\nLes talents Oeuil Magique et Mathair interragissent dans votre corps et donnent naissance a un nouveau talent !"
                talent = "Oculus Terrae"
                Player.talents_possedes.append(talent)
                commentaire += (f"\nVous gagnez le talent [{talent}] !")
            if "Fos" in Player.talents_possedes:
                commentaire += "\nLes talents Oeuil Magique et Fos interragissent dans votre corps et donnent naissance a un nouveau talent !"
                talent = "Corporalis Oculus"
                Player.talents_possedes.append(talent)
                commentaire += (f"\nVous gagnez le talent [{talent}] !")
            if "Haddee" in Player.talents_possedes:
                commentaire += "\nLes talents Oeuil Magique et Haddee interragissent dans votre corps et donnent naissance a un nouveau talent !"
                talent = "Sanguis Oculus"
                Player.talents_possedes.append(talent)
                commentaire += (f"\nVous gagnez le talent [{talent}] !")
    if talent in ["Eboulis", "Grand Froid"]:
        if ("Eboulis" in Player.talents_possedes) and ("Grand Froid" in Player.talents_possedes):
            commentaire += "\nLes talents Eboulis et Grand Froid interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Avalanche"
            Player.talents_possedes.append(talent)
            commentaire += (f"\nVous gagnez le talent [{talent}] !")
    if talent in ["Oeuil Magique", "Connaissance"]:
        if ("Oeuil Magique" in Player.talents_possedes) and ("Connaissance" in Player.talents_possedes):
            commentaire += "\nLes talents Oeuil Magique et Connaissance interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Metamorphosis"
            Player.talents_possedes.append(talent)
            commentaire += (f"\nVous gagnez le talent [{talent}] !")
    if talent in ["Luciole", "Pyromage"]:
        if ("Luciole" in Player.talents_possedes) and ("Pyromage" in Player.talents_possedes):
            commentaire += "\nLes talents Luciole et Pyromage interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Bougie Magique"
            Player.talents_possedes.append(talent)
            commentaire += (f"\nVous gagnez le talent [{talent}] !")
    if talent in ["Suroxygenation", "Réflex"]:
        if ("Suroxygenation" in Player.talents_possedes) and ("Réflex" in Player.talents_possedes):
            commentaire += "\nLes talents Suroxygenation et Réflex interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Ultra-Instinct"
            Player.talents_possedes.append(talent)
            commentaire += (f"\nVous gagnez le talent [{talent}] !")
    if talent in ["Cycle Glaciaire", "Pyromage", "Patience", "Carte du Gout", "Nectar"]:
        if (("Cycle Glaciaire" in Player.talents_possedes) and
            ("Pyromage" in Player.talents_possedes) and
            ("Patience" in Player.talents_possedes) and
            ("Carte du Gout" in Player.talents_possedes) and
            ("Nectar" in Player.talents_possedes)):
            commentaire += "\nLes talents Cycle Glaciaire, Pyromage, Patience, Carte du Gout et Nectar interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Réjuvénation"
            Player.talents_possedes.append(talent)
            commentaire += (f"\nVous gagnez le talent [{talent}] !")        
    if talent in ["Affinitée de Feu", "Affinitée de Foudre", "Affinitée de Glace", "Affinitée de Terre", "Affinitée Physique", "Affinitée de Sang"]:
        if (("Affinitée de Feu" in Player.talents_possedes) and
            ("Affinitée de Foudre" in Player.talents_possedes) and
            ("Affinitée de Glace" in Player.talents_possedes) and
            ("Affinitée de Terre" in Player.talents_possedes) and
            ("Affinitée de Sang" in Player.talents_possedes) and
            ("Affinitée Physique" in Player.talents_possedes)):
            commentaire += ("\nLes talents Affinitée de Feu, Affinitée de Foudre,"
                            " Affinitée de Glace, Affinitée de Terre, Affinitée Physique"
                            " et Affinitée de Sang interragissent dans votre corps et "
                            "donnent naissance a un nouveau talent !")
            talent = "Elémento-Réceptif"
            Player.talents_possedes.append(talent)
            commentaire += (f"\nVous gagnez le talent [{talent}] !")  
    if talent in ["Rapide", "Grand Froid", "Réflex", "Conditions Limites", "Aura de Feu", "Poussière de Diamants"]:
        if (("Rapide" in Player.talents_possedes) and
            ("Grand Froid" in Player.talents_possedes) and
            ("Réflex" in Player.talents_possedes) and
            ("Conditions Limites" in Player.talents_possedes) and
            ("Aura de Feu" in Player.talents_possedes) and
            ("Poussière de Diamants" in Player.talents_possedes)):
            commentaire += ("\nLes talents Rapide, Grand Froid,"
                            " Réflex, Conditions Limites, Aura de Feu"
                            " et Poussière de Diamants interragissent dans votre corps et "
                            "donnent naissance a un nouveau talent !")
            talent = "Grand Pandémonium Elémentaire"
            Player.talents_possedes.append(talent)
            commentaire += (f"\nVous gagnez le talent [{talent}] !") 
    if talent in ["Baron Rouge", "Pyrosorcier", "Connaissance"]:
        if ("Baron Rouge" in Player.talents_possedes) and ("Pyrosorcier" in Player.talents_possedes) and ("Connaissance" in Player.talents_possedes):
            commentaire += "\nLes talents Baron Rouge, Pyrosorcier et Connaissance interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Maitre du Mana"
            Player.talents_possedes.append(talent)
            commentaire += (f"\nVous gagnez le talent [{talent}] !")
    if talent in ["Pira", "Pyromage", "Rafale"]:
        if ("Pira" in Player.talents_possedes) and ("Pyromage" in Player.talents_possedes) and ("Rafale" in Player.talents_possedes):
            commentaire += "\nLes talents Pira, Pyromage et Rafale interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Libération de Feu"
            Player.talents_possedes.append(talent)
            commentaire += (f"\nVous gagnez le talent [{talent}] !")

    if talent in ["Elektron", "Facture", "Luciole"]:
        if ("Elektron" in Player.talents_possedes) and ("Facture" in Player.talents_possedes) and ("Luciole" in Player.talents_possedes):
            commentaire += "\nLes talents Elektron, Facture et Luciole interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Libération de Foudre"
            Player.talents_possedes.append(talent)
            commentaire += (f"\nVous gagnez le talent [{talent}] !")
    if talent in ["Tsumeta-Sa", "Cycle Glaciaire", "Grand Froid"]:
        if ("Tsumeta-Sa" in Player.talents_possedes) and ("Cycle Glaciaire" in Player.talents_possedes) and ("Grand Froid" in Player.talents_possedes):
            commentaire += "\nLes talents Tsumeta-Sa, Cycle Glaciaire et Grand Froid interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Libération de Glace"
            Player.talents_possedes.append(talent)
            commentaire += (f"\nVous gagnez le talent [{talent}] !")

    if talent in ["Mathair", "Fracturation", "Eboulis"]:
        if ("Mathair" in Player.talents_possedes) and ("Fracturation" in Player.talents_possedes) and ("Eboulis" in Player.talents_possedes):
            commentaire += "\nLes talents Mathair, Fracturation et Eboulis interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Libération de Terre"
            Player.talents_possedes.append(talent)
            commentaire += (f"\nVous gagnez le talent [{talent}] !")

    if talent in ["Fos", "Oeuil Magique", "Réflex"]:
        if ("Fos" in Player.talents_possedes) and ("Oeuil Magique" in Player.talents_possedes) and ("Réflex" in Player.talents_possedes):
            commentaire += "\nLes talents Fos, Oeuil Magique et Réflex interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Libération Physique"
            Player.talents_possedes.append(talent)
            commentaire += (f"\nVous gagnez le talent [{talent}] !")

    if talent in ["Haddee", "Anticoagulants", "Baron Rouge"]:
        if ("Haddee" in Player.talents_possedes) and ("Anticoagulants" in Player.talents_possedes) and ("Baron Rouge" in Player.talents_possedes):
            commentaire += "\nLes talents Haddee, Anticoagulants et Baron Rouge interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Libération de Sang"
            Player.talents_possedes.append(talent)
            commentaire += (f"\nVous gagnez le talent [{talent}] !")
    if commentaire != "...?":
        print(commentaire)
        Affichage.EntreePourContinuer()










Save = SaveManagement()
Player = PlayerCaracteristics()
Trader = TraderUsage()
Affichage = Affiche()
Observation = Observe()
# debut
      
# fin
MenuDeDemarrage(Player)
game_in_session = True
PlayMusic(f"etage_{Player.numero_de_letage}")
while game_in_session:
    # choix de laction
    while True:
        try:
            choix = GetChoiceMenuColiseum()
            ClearConsole()
            if choix in range(1, 8):
                break
        except ValueError:
            ClearConsole()
    # application de l'action
    if choix == 1:
        DoFight() #Have to hook up to Battle
    elif choix == 2:
        #combat contre boss
        if not Player.boss_battu:
            DoBossFight() #Have to hook up to Battle
        #descente au niveau inferieur
        else:
            game_in_session = GoDown() 
            if game_in_session:
                PlayMusic(f"etage_{Player.numero_de_letage}")
    elif choix == 3:
        Trader.DoTrading() #DONE
    elif choix == 4:
        #Observation.SeeSomething()
        print("Vous vous baladez dans l'étage...")
        print("...et ne trouvez rien d'interressant.")
        Affichage.EntreePourContinuer()
    elif choix == 5:
        Player.ShowPlayerCaracteristicsAndItems() #DONE
    elif choix == 6:
        DoRedcoin() #DONE
    elif choix == 7:
        Save.SaveTheGame() #DONE
PlayMusic("battle_win")
print("Vous avez gagné !")
Affichage.EntreePourContinuer()



 

# Lance un debug pour la méthode GetUserChoice du controlleur
#control.DebugGetUserChoice()
#control.PatternDesignConstantUpdater()
#control.Cat_astrophe()



# faire tutorial
# moyen d'afficher les cartes de redcoins
# description etage
# descrpition boss

# faire les observations (non)où
