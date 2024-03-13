import controleur
import os
from pygame import mixer
import random
import sys
import csv
import ast
import time
import tkinter as tk
from tkinter import PhotoImage


# 0nom 1description 2stigma+ 3stigma- 4stigma* 5techniques 
# 6sorts 7items 8talents 9vie 10mana 11force
# 12inteligence 13defence 14tauxcoupcrit
# 15degatcoupcrit 16tauxsortcrit 17degatsortcrit
# 18tauxesquive 19gold

ANNUAIRESORTSSOIN = {  # cout moins élevé quand utilise sort en dehors combat
    "Sonata Pitoyable": 6, 
    "Sonata Miséricordieuse": 13,
    "Sonata Empathique": 18,
    "Sonata Sincère": 23,
    "Sonata Bienveillante": 18,
    "Sonata Absolutrice": 38
}
ANNUAIREDESCRIPTIONSORTSSOIN = {
    "Sonata Pitoyable": "Un bruit pathétique vous enveloppe et apaise la douleur de vos blessures.",
    "Sonata Miséricordieuse": "Un son a peine apréciable se plaque contre votre peau et referme vos blessures.",
    "Sonata Empathique": "Une musique potable soulage votre âme et vos blessures.",
    "Sonata Sincère": "Un chant cristallin inspire votre esprit et revigore votre corps.",
    "Sonata Bienveillante": "Une chorale glorieuse vous fait oublier les problèmes de votre situation et cicatrise vos blessures.",
    "Sonata Absolutrice": "Une mélodie féerique ramène votre être tout entier a un état optimal."
}
POURCENTAGESORTSOIN = {
    "Sonata Pitoyable": 5,
    "Sonata Miséricordieuse": 7,
    "Sonata Empathique": 14,
    "Sonata Sincère": 19,
    "Sonata Bienveillante": 22,
    "Sonata Absolutrice": 27,
}
SOINMINIMUMSORTSOIN = {
    "Sonata Pitoyable": 10,
    "Sonata Miséricordieuse": 17,
    "Sonata Empathique": 22,
    "Sonata Sincère": 27,
    "Sonata Bienveillante": 35,
    "Sonata Absolutrice": 42,
}
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
        "Incompatible",  # char stigma -
        "Aucun",  # char stigma *
        [
            "Attaque Légère",
        ],  # char list technic
        [
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
            "Katana Bleu"
        ],  # char list technic
        [
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
LISTEITEMDEFENCE = [
    "Feuille Jindagee",
    "Fruit Jindagee",
    "Feuille Aatma",
    "Fruit Aatma",
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
]
LISTEITEMATTAQUE = [
    "Crystal Elémentaire",
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
]
LISTEITEMDEBUTTOUR = [
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
]
LISTEITEM = [
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
]
LISTEDEMUSIQUE = [
    "Gigantomachie",
    "Endorphines",
    "Dangereuses Mélancolies",
    "L'Orage avant la Tempête",
    "Fanfare",
    "Prosopagnosie",
    "Pluie d'Automne",
    "Exploratio",
    "Les Joies du Combat",
    "Revenant",
    "Conte de Fée",
    "Epineuses Rencontres",
    "Le Chevalier Qu'on Ne Veut Pas Rencontrer",
    "Ruines d'Antan",
    "Sables Mouvants",
    "Euthanasie Régalienne",
    "Pāramitā",
    "Nerd Party",
    "Jeux d'Enfants",
    "Pantomime",
    "Carnaval",
    "Piñata",
    "Tragicomique",
    "Combler les Vides",
    "Systèmes Défaillants",
    "Sa Majesté Des Mouches",
    "Divin Karma",
    "Folie Furieuse",
    "Comment Tuer le Grand Méchant Loup",
    "Ossuaire",
    "Dissonance Cognitive",
    "Faux semblants",
    "La Hache et le Grimoire",
    "Contradictions",
    "Arythmie",
    "Au Détour D’un Sentier Une Charogne Infâme",
    "La Divine Comédie",
    "Apogée Inversée",
    "Pénultima",
    "Théorie du Chaos"


]
LISTECARACTERISTIQUEMUSIQUE = [
    ["start", "Vous écoutez "],
    ["tutorial", "Vous écoutez "],
    ["alfredproto", "Vous écoutez "],
    ["boss_introV2", "Vous écoutez "],
    ["battle_win", "Vous écoutez "],
    ["abyss", "Vous écoutez "],
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
        self.modificateur += ((Player.numero_de_letage / 10) - 0.1)
        self.annuaire_des_prix = {
            "Feuille Jindagee": round(15*self.modificateur),
            "Fruit Jindagee": round(40 * self.modificateur),
            "Feuille Aatma": round(25 * self.modificateur),
            "Fruit Aatma": round(60 * self.modificateur),
            "Crystal Elémentaire": round(40 * self.modificateur),
            "Ambroisie": round(40 * self.modificateur),
            "Hydromel": round(40 * self.modificateur),
            "Orbe de Furie": round(40 * self.modificateur),
            "Orbe de Folie": round(40 * self.modificateur),
            "Remède": round(20 * self.modificateur),
            "Remède Superieur": round(50 * self.modificateur),
            "Remède Divin": round(100 * self.modificateur),
            "Pillule": round(30 * self.modificateur),
            "Pillule Superieure": round(60 * self.modificateur),
            "Pillule Divine": round(110 * self.modificateur),
            "Fléchette Rouge": round(20 * self.modificateur),
            "Flèche Rouge": round(55 * self.modificateur),
            "Fléchette Bleue": round(20 * self.modificateur),
            "Flèche Bleue": round(55 * self.modificateur),
            "Poudre Explosive": round(30 * self.modificateur),
            "Roche Explosive": round(50 * self.modificateur),
            "Bombe Explosive": round(70 * self.modificateur),
            "Fiole de Poison": round(50 * self.modificateur),  # [debutTour]
            "Gourde de Poison": round(110 * self.modificateur),  # [debutTour]
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
            "Méga Tirage": 777
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
            "Méga Tirage",
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
            "Méga Tirage",
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
            "Méga Tirage",
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
            "Méga Tirage",
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
            self.annuaire_des_prix["Red Coin"] = 9999999
        else:
            self.annuaire_des_prix["Red Coin"] = round(Player.numero_de_letage * 100)
        self.annuaire_des_prix["Tirage"] = round((Player.numero_de_letage * 50) + (Player.number_of_tirage * (Player.numero_de_letage * 15)))
        self.annuaire_des_prix["Fée dans un Bocal"] = round(((Player.numero_de_letage * 50) + 25) * self.modificateur)

    def UseMegaTirage(self):
        #double tirage des recompenses 
        element_tirage = []
        for _ in range(0, 2):
            nombre_aleatoire = random.randint(1, 16)
            if nombre_aleatoire == 1:
                element_tirage.append("Feu")
            if nombre_aleatoire == 3:
                element_tirage.append("Foudre")
            if nombre_aleatoire == 5:
                element_tirage.append("Glace")
            if nombre_aleatoire == 7:
                element_tirage.append("Terre")
            if nombre_aleatoire == 9:
                element_tirage.append("Physique")
            if nombre_aleatoire == 11:
                element_tirage.append("Sang")
            if nombre_aleatoire == 13:
                element_tirage.append("Effort")
            if nombre_aleatoire == 15:
                element_tirage.append("Maitrise")
            else:
                element_tirage.append("Vide")
        #choix du joueur
        while True:
            try:
                if Player.affronte_un_boss:
                    print(f"A l'endroit ou se tenait l'ennemi, il y a maintenant une petite boite en métal bleu ornée d'un grand *POW*.\nVous y plongez la main à l'interieur.")
                else:
                    print(f"Le marchand vous laisse plonger la main dans une boite en carton bleue ornée d'un grand *POW*.")
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
        if element_tirage[choix - 1] == "Feu":
            type_du_tirage = "le sort"
            nom_du_tirage = "Explosion de Feu Sacré"
        elif element_tirage[choix - 1] == "Foudre":
            nom_du_tirage = "Combo Electrique"
            type_du_tirage = "la technique"
        elif element_tirage[choix - 1] == "Glace":
            nom_du_tirage = "Mirroir d'Eau"
            type_du_tirage = "le sort"
        elif element_tirage[choix - 1] == "Terre":
            nom_du_tirage = "Position du Massif"
            type_du_tirage = "la technique"
        elif element_tirage[choix - 1] == "Physique":
            nom_du_tirage = "Poussée d'Adrénaline"
            type_du_tirage = "la technique"
        elif element_tirage[choix - 1] == "Sang":
            nom_du_tirage = "Brume de Sang"
            type_du_tirage = "le sort"
        elif element_tirage[choix - 1] == "Effort":
            nom_du_tirage = "Iaido"
            type_du_tirage = "la technique"
        elif element_tirage[choix - 1] == "Maitrise":
            nom_du_tirage = "Carrousel"
            type_du_tirage = "le sort"
        if (element_tirage[choix - 1] != "Vide") and (nom_du_tirage not in Player.sorts_possedes) and (nom_du_tirage not in Player.techniques_possedes) :
            commentaire = f"Vous obtenez {type_du_tirage} {nom_du_tirage} !"
            if type_du_tirage == "le sort":
                Player.sorts_possedes.append(nom_du_tirage)
            elif type_du_tirage == "la technique":
                Player.techniques_possedes.append(nom_du_tirage)
        else:
            commentaire = "Vous sortez la masse, et elle disparait dans les airs.\nMauvaise Pioche !"
        Affichage.AfficheMegaTirage(commentaire)

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
            if type_tirage == "le sort":
                nombre_aleatoire = random.randint(1, 7)
            else:
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
            if nombre_aleatoire == 6:
                element_tirage.append("Sang")
            if nombre_aleatoire == 7:
                element_tirage.append("Divin")
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
            elif element_tirage[choix - 1] == "Divin":
                nom_du_tirage = "Sonata"
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
            elif element_tirage[choix - 1] == "Divin":
                nom_du_tirage += " Pitoyable"
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
            elif element_tirage[choix - 1] == "Divin":
                nom_du_tirage += " Miséricordieuse"
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
            elif element_tirage[choix - 1] == "Divin":
                nom_du_tirage += " Empathique"
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
            elif element_tirage[choix - 1] == "Divin":
                if sort_attaque_forte_pour_etage_7_8:
                    nom_du_tirage += " Sincère"
                else:
                    nom_du_tirage += " Bienveillante"
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
            elif element_tirage[choix - 1] == "Divin":
                nom_du_tirage += " Absolutrice"
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
        self.MiseAJourDesPrix()
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
                    elif nom_de_litem == "Méga Tirage":
                        Trader.UseMegaTirage()
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

    def MiseAJourDesPrix(self):
        self.__init__()


class Affiche:

    def __init__(self):
        pass

    def EntreePourContinuer(self):
        input("(Appuyez sur entrée pour continuer)")
        ClearConsole()

    def IntroBoss(self, commentaire):
        print(commentaire)
        self.EntreePourContinuer()

    def AfficheMegaTirage(self, commentaire):
        print(commentaire)
        self.EntreePourContinuer()

    def AfficheLongChargement(self):
        print("Récupération en cours, veuillez patienter...")
        print("(Temps d'attente estimé a 1 minute)")
        time.sleep(60)
        ClearConsole()

    def AfficheIntroCombat(self):
        if Player.stigma_positif == "Débrouillarde":
            print("Vous vous approchez de l'arène et trouvez des déchets et autres bidules sur le sol...")
            self.EntreePourContinuer()
            nombre_aleatoire = random.randint(0, 100)
            if nombre_aleatoire <= 20:
                nom_de_litem = GetRandomItemFromList(LISTEITEM)
                print("...et une idée germe dans votre esprit !"
                      f"\nVous rassemblez alors les objets entre eux et créez l'objet : {nom_de_litem} !")
                Player.items_possedes[nom_de_litem] += 1
            else:
                print("...mais aucune idée ne vous vient a l'esprit.")
            self.EntreePourContinuer()
        if Player.stigma_positif == "Cueilleuse":
            print("Vous vous approchez de l'arène et trouvez de curieuses plantes dans les interstices entre les briques...")
            self.EntreePourContinuer()
            nombre_aleatoire = random.randint(0, 100)
            if nombre_aleatoire <= 50:
                nom_de_litem = GetRandomItemFromList(LISTEITEMDEFENCE)
                print("...et une idée germe dans votre esprit !"
                      f"\nVous cueillez alors les monceaux biologiques, appliquez vos techniques de druidesses, et créez l'objet : {nom_de_litem} !")
                Player.items_possedes[nom_de_litem] += 1
            else:
                print("...mais rien ne peut etre fait avec.")
            self.EntreePourContinuer()
        print("Vous rentrez dans l'arène et jettez un coup d'oeil aux tribunes vides, avant de frapper le sol de votre pied."
              "\nAussitôt, une vague bruyante de spectateurs fantomatiques apparaissent, et un ennemi apparait devant vous.")
        self.EntreePourContinuer()

    def AffichePlusDennemis(self):
        print("Vous rentrez dans l'arène et jettez un coup d'oeil aux tribunes vides, avant de frapper le sol de votre pied."
              "\nMais rien ne se passe.\nIl n'y a plus personne pour vous affronter, a part le boss.")
        if not Player.red_coin_recu_par_extermination and Player.boss_battu:
            print("Un spectateur fantomatique amusé par votre désir d'extermination vous envoie un cadeau depuis les gradins, avant de disparaitre.")
            self.EntreePourContinuer()
            print("Vous gagnez un Red Coin !")
            self.EntreePourContinuer()
            Player.nombre_de_red_coin += 1
            Player.red_coin_recu_par_extermination = True
        self.EntreePourContinuer()

    def AfficheIntroCombatBoss(self):
        print("Vous rentrez dans l'arène et jettez un coup d'oeil aux tribunes vides, avant de frapper le sol de votre pied."
              "\nAussitôt, une vague silencieuse de spectateurs fantomatiques apparaissent, et la grille de métal ancien à l'autre bout de l'arène s'ouvre.")
        self.EntreePourContinuer()
        if Player.numero_de_letage != 8:
            PlayMusic("boss_introV2")
        liste_commentaire = []
        if Player.numero_de_letage == 1:
            commentaire = ("Une boule d'obsidienne flotte jusqu'à votre niveau, et une voix artificielle remplit l'arène.")
            liste_commentaire.append(commentaire)
            commentaire = ("*SENTIENCE RECONNUE. INITIATION DU PROTOCOLE D'EXPLIQUATION ENCLENCHE*"
                           "\n*POUR LES CRIMES SUIVANT CONTRE VOTRE ROI MALGRES SES ANNEES DE BONS ET LOYAUX SERVICES, VOUS VOILA CONDAMNE A LA PEINE DE MORT :*"
                           "\n*TENTATIVE DE TRAHISON, TENTATIVE DE REGICIDE, TENTATIVE DE REBELLION, TENTATIVE DE REVOLUTION,*"
                           "\n*AVOIR CRACHE SUR UN TABLEAU DU ROI, AVOIR EXPRIME DE LA DISSATISFACTION ENVERS LE ROI ACTUEL,*"
                           "\n*AVOIR UN COMPORTEMENT SUSPECT PROCHE DE LA RESIDENCE DU ROI, AVOIR UN COMPORTEMENT SUSPECT PROCHE DE LA CAPITALE DU ROI,"
                           "\n*AVOIR UN COMPORTEMENT SUSPECT DANS LE ROYAUME DIRIGE PAR LE ROI, ET ENCORE 2324 AUTRES INFRACTIONS NON CITEE.")
            liste_commentaire.append(commentaire)
            commentaire = ("*QUESTIONS SOUVENT POSEES :"
                           "\n* - MAIS JE N'AI JAMAIS FAIT CELA !*"
                           "\n* - CELA DOIT ETRE UNE ERREUR !*"
                           "\n* - COMMENT PEUT ON SORTIR D'ICI ?*"
                           "\n*UNE SEULE REPONSE : UN ROI JUSTE NE PUNIT PAS LES INNOCENTS."
                           "\n*CONSIDEREZ VOTRE PRESENCE ICI COMME UNE PREUVE IRREFUTABLE DE VOTRE CULPABILITE.*"
                           "\n\n*PROTOCOLE DEXPLIQUATION TERMINE*"
                           "\n*PROTOCOLE DE COMBAT ENCLENCHE*")
            liste_commentaire.append(commentaire)
            commentaire = ("La sphère bouge et se transforme en une copie conforme de vous, puis se met a parler :"
                           "\n*J'ai toujours dit qu'il fallait combattre le feu avec le feu !*")
            liste_commentaire.append(commentaire)
        elif Player.numero_de_letage == 2:
            commentaire = ("Un chevalier en armure violette saute depuis le sommet de la tour et atterit en plein milieu de l'arène."
                           "\n*C'est toi le prochain traitre ?*"
                           "\nVous le regardez avec étonnement.")
            liste_commentaire.append(commentaire)
            commentaire = ("*Fais pas semblant, je suis une bonne personne, je sais reconnaitre qui n'est ou n'est pas une menace pour le chateau.*"
                           f"\n*Toi par exemple, tu a du sang de monstre sur les mains.*\n*Je dirais que tu a massacré...{Player.nombre_de_monstres_tues} monstres.*")
            liste_commentaire.append(commentaire)
            commentaire = ("*Tu a gouté aux joies du combat, et tu en veux plus, toujours plus.*\n*Je fais confiance a mon flair pour ca. Il m'a sauvé la mise de très nombreuses fois.*"
                           "\n*Tu es une menace pour mon roi et sa sécuritée.*\n*Tu es une menace pour le royaume et son épanouissement.*"
                           "\n*Tu es une menace pour tout ceux que tu croisera sur ton chemin.*"
                           "\nIl se tourne alors vers les spectateurs.")
            liste_commentaire.append(commentaire)
            commentaire = ("*Et quel piètre chevalier je serais si je n'arretais pas une vermine dans son genre, hein ?*"
                           "\nLe chevalier pourpre se tourne vers vous et sort une lame rongée par la rouille et la souillure."
                           "\n*Laisse tomber, l'affreux. La justice et le bien sont de mon coté. Tu n'a aucune chance de gagner.*")
            liste_commentaire.append(commentaire)
            commentaire = ("*Car tu vois...*")
            liste_commentaire.append(commentaire)
            commentaire = ("*...je suis le Chevalier que les gens comme toi ne veulent pas rencontrer.*")
            liste_commentaire.append(commentaire)
        elif Player.numero_de_letage == 3:
            commentaire = ("L'arène se met alors a trembler, et le sable commence a s'écouler par les cotés."
                           "\nDes blocs de roche, de bois et d'or commencent alors a apparaitre, et au milieu de tout ca, une bien étrange structure pentagonale surmontée d'un sarcophage et de 5 vases canopes.")
            liste_commentaire.append(commentaire)
            commentaire = ("Un examen plus approfondi de la salle révèle aussi des têtes empaillées et accrochées sur tous les murs de l'arène."
                           "\n*Il faut toujours rendre la chose plus spectaculaire. Plus incroyable. C'est du travail, empailler les têtes. Tu aime ?*")
            liste_commentaire.append(commentaire)
            commentaire = ("Le sarcophage se souleve alors et une forme vaguement humaine zébrée de lignes de coutures avec un masque de pharaon en sort."
                           "\n*Le roi, dans sa folie, s'est emparé des cadavres de ses soi-disants ennemis qu'il a cousut entre eux. puis il a mit l'âme de son frère a l'interieur.*"
                           "\n*Je suis un monstre, une atrocitée, mais sur laquelle il avait enfin le controle que son esprit malade requit.\nUn Roi des sables du sud que l'on a enfermé dans ce corps....* ")
            liste_commentaire.append(commentaire)
            commentaire = ("Les vases canopes commencent alors a leviter."
                           "\n*Vois ce qu'il reste de la grande lignée qui précédait ce fou : des morceaux de chairs dans des vases magiques.*\n\n\n*Pitoyable.*\n\n"
                           "\n*Mais bon. Trêve de bavardage. Il est temps que je t'acceuille comme il se doit.* ")
            liste_commentaire.append(commentaire)
            commentaire = ("Le roi-monstre jette un coup d'oeil inquiet vers les spectateurs avant de se retourner vers vous et de prendre une pose extravagante.")
            liste_commentaire.append(commentaire)
            commentaire = ("*Je te souhaite la bienvenue dans mon antre voyageur.*\n*Devant toi se trouve une folie engendrée par le plus malade des esprits : Moi même ! Le grand roi Amonrê !*"
                           "\n*JE SUIS NE HOMME ET SI TU EST ASSEZ FORT, C'EST AUJOURDHUI QUE JE MOURRAI MONSTRE !*\n*APPROCHE DONC ET MONTRE MOI L'ETENDUE DE TA PUISSANCE !* ")
            liste_commentaire.append(commentaire)
        elif Player.numero_de_letage == 4:
            commentaire = ("Vous entendez le son d'un livre qui se ferme fort, et l'apparence de l'arène change brusquement. "
                           "\nVous observez alors un bureau finement décoré et rempli d'étagères sur lesquelles sont négligement placés des livres de magie et de sortillèges."
                           "\nAu milieu, un adolescent d'une quinzaine d'année vous regarde fixement, coincé entre deux piles de livre plus haute que lui.")
            liste_commentaire.append(commentaire)
            commentaire = ("*C'est l'heure pas vrai ?*\n*Bon, ben me fout pas la honte hein !*\n*Ya un endroit qu'il faut pas taper, c'est là.*")
            liste_commentaire.append(commentaire)
            commentaire = ("L'ennemi tapote son torse, ou repose une amulette a l'aspect ancien.")
            liste_commentaire.append(commentaire)
            commentaire = ("*Allez, bonne chance !*"
                           "\nVous vous retrouvez alors dans l'arène, avec l'enfant mage en face de vous.")
            liste_commentaire.append(commentaire)
            commentaire = ("*Vous voulez aller plus loin ?*\n*Vous souhaitez sortir du Coliseum avec la gloire, l'argent, et la vie sauve ?*"
                           "\n*Dommage pour vous !*\n*Car vous êtes tombé sur le disciple du grand...*")
            liste_commentaire.append(commentaire)
            commentaire = ("*Du puissant...*")
            liste_commentaire.append(commentaire)
            commentaire = ("*Du musculeux...*")
            liste_commentaire.append(commentaire)
            commentaire = ("*Maitre Mage ! Créateur des ces lieux !*")
            liste_commentaire.append(commentaire)
            commentaire = ("Votre expression s'assombrit.\n*Bah alors ? Fait pas cette tête ! Tu va pas l'affronter maintenant !*\n*Il n'est pas avec moi car...il est en...*")
            liste_commentaire.append(commentaire)
            commentaire = ("Son expression s'assombrit.\n*...en réclusion. Quelque part. Pour devenir plus fort. Surement.*")
            liste_commentaire.append(commentaire)
            commentaire = ("*...*")
            liste_commentaire.append(commentaire)
            commentaire = ("*...amène toi.*")
            liste_commentaire.append(commentaire)
        elif Player.numero_de_letage == 5:
            commentaire = ("Vous entendez du bruit vers un stand de chamboule-tout, et voyez une clochette dépasser d'une poubelle proche.")
            liste_commentaire.append(commentaire)
            commentaire = ("L'ennemi sort alors de sa cachette."
                           "\nIl est habillé avec des vêtements colorés déchirés, de grandes chaussures rouges trouées, "
                           "et un masque sur lequel est représenté un sourire béant."
                           "\nVous frissonnez en voyant la folie sanguinaire dans les yeux de l'ennemi, a travers un trou dans le costume.")
            liste_commentaire.append(commentaire)
            commentaire = ("*BONJOUR-JOUR VOYAGEUR ! JE SUIS LE BOUFFON BOUFFON ! JE SUIS ICI-CI POUR AMUSER-MUSER MON ROI !*")
            liste_commentaire.append(commentaire)
            commentaire = ("*ET TU SAIS CE QUI L'AMUSERAIT BEAUCOUP ? MOI JE SAIS ! MOI JE SAIS !*")
            liste_commentaire.append(commentaire)
            commentaire = ("*CA SERAIT TA TETE AU BOUT D'UN PIQUE ET TES TRIPES DANS UN GATEAU !*")
            liste_commentaire.append(commentaire)
            commentaire = ("*ET PUIS SI JE FAIT CA IL ME LAISSERA SUREMENT-REMENT REMONTER DANS LE CHATEAU PAS VRAI ? ET PUIS IL ME LAISSERA MANGER AUTRE CHOSE QUE CES VOYAGEURS SANS RIEN SUR LES OS !*")
            liste_commentaire.append(commentaire)
            commentaire = ("*JOUONS ! JOUONS ! YAHAHAHA !*")
            liste_commentaire.append(commentaire)
        elif Player.numero_de_letage == 6:
            commentaire = "Vous entendez des bruits de pas venant de derriere vous.\nAlors que vous vous retournez, vous les entendez encore derriere vous."
            liste_commentaire.append(commentaire)
            commentaire = "*Bienvenue dans mon domaine, voyageur.*"
            liste_commentaire.append(commentaire)
            commentaire = ("Finalement, vous vous retournez une dernière fois et trouvez un enfant petit, mais d'allure robuste.\nUn chapeau de pirate est vissé sur sa tête."
                          "\nAutour de lui se trouvent des batisses faites de vêtements et autres monceaux de métal.\nDe part et d'autres, des ossements humains jonchent le sol.")
            liste_commentaire.append(commentaire)
            commentaire = ("*Enfin, mon domaine, plutot celui du Roi.*"
                           "\n*Mais avec quelques amis, nous sommes arrivés a battre celui qui dominait cet étage.*"
                           "\n*Il est d'ailleurs en plein changement de propriétaire !*"
                           "\n*Je pense que c'est assez pour pouvoir dire que c'est le mien maintenant*."
                           "\n*N'est-ce pas ?*")
            liste_commentaire.append(commentaire)
            commentaire = ("Vous le regardez, pensif. Cet enfant serait donc si agé ?")
            liste_commentaire.append(commentaire)
            commentaire = ("*Pas de réponses ?*"
                           "\n*Tu dois être déterminé a en finir avec cet endroit.*"
                           "\n*Mais regarde donc : Ici repose toutes les personnes qui m'ont suivie.*"
                           "\n*Nous avons tenté de nous installer ici, mais le manque d'eau et de lumière nous a rendu fou.*"
                           "\n*Enfin, nous...*")
            liste_commentaire.append(commentaire)
            commentaire = ("*Eux plutot. L'espèce de pendule vivante qui vivait ici possédait plusieurs reliques qui m'ont aidé a survivre.*"
                           "\n*Mais que je suis impoli ! Je ne me suis même pas présenté.*")
            liste_commentaire.append(commentaire)
            commentaire = ("*Je suis le Prince des voleurs !*")
            liste_commentaire.append(commentaire)
            commentaire = ("*Intemporel, Plus riche que le plus riche des hommes, Libéré des chaines de la soif et de la satiété !*")
            liste_commentaire.append(commentaire)
            commentaire = ("*Et afin de conserver tout ces privilèges, je vais me battre contre toi voyageur.*")
            liste_commentaire.append(commentaire)
            commentaire = ("Le Prince des Voleurs se tourne alors vers un des membres fantomatiques de l'audience, qui a presque l'air de..."
                           "\n...sourire ?")
            liste_commentaire.append(commentaire)
            commentaire = ("*Trop de blabla...pas assez envoutant...*")
            liste_commentaire.append(commentaire)
            commentaire = ("Il commence a marmoner en regardant le sol, puis vous regarde brusquement.")
            liste_commentaire.append(commentaire)
            commentaire = ("*Pas grave ! Alors ? On commence ?*")
            liste_commentaire.append(commentaire)
        elif Player.numero_de_letage == 7:
            commentaire = ("Vous voyez un vieillard aux joues creusées et aux bras tailladés."
                           "\nSon apparence ressemble a ces descriptions que l'on fait des ames damnées, tourmentées en enfer pour l'éternité."
                           "\nCe n'est plus qu'une trace de lui meme maintenant.")
            liste_commentaire.append(commentaire)
            commentaire = ("*T-t-t-TOI !*\n*Tu est venu me TUER c'est ca ?*\n*Comme tout le monde dans ce foutu trou a rat !*\n*Quoique je ne me rapelle pas t'avoir fait jeter ici..*")
            liste_commentaire.append(commentaire)
            commentaire = ("En le voyant vous parler, deux expressions vous viennent a l'esprit : En plein burnout, et Roi de pacotille."
                           "\nSait il seulement qu'il ne parle pas a un des spectres qui hante ses cauchemards ?"
                           "\nQu'il ne parle pas a une création de son cerveau malade, mais a une vraie personne ?")
            liste_commentaire.append(commentaire)
            commentaire = ("*MAIS!*\n*Tu ne vas RIEN me faire !*\n*héhé... CLONE D'OBSIDIENNE ! VIENS A MOI !*")
            liste_commentaire.append(commentaire)
            commentaire = ("Mais personne ne vient.")
            liste_commentaire.append(commentaire)
            commentaire = ("*Tu... l'a tué ?*\n*HAHAHAHA ! TU ES FORT ! MAIS CELA NE SUFFIRA PAS !*\n*TOUS MES GENERAUX SONT SOUS MON COMMANDEMENT !*"
                           "\n*ROI AMONRE ! MON FRERE ! VIENS ICI DEFENDRE TA FAMILLE !*")
            liste_commentaire.append(commentaire)
            commentaire = ("Mais personne ne vient.                                            Seul le bruit des flammes répond a ses supplications.")
            liste_commentaire.append(commentaire)
            commentaire = ("*Ah.... Ah... Je t'avais tout donné mon frère...misérable...*\n*CHEVALIER POURPRE !*\n*RIGOR MORTEX !*\n*AMENEZ VOUS BON SANG !*")
            liste_commentaire.append(commentaire)
            commentaire = ("Mais personne ne vient.                              Répéter les mêmes actions en s'attendant a un résultat différent...")
            liste_commentaire.append(commentaire)
            commentaire = ("*Ah...AH....AH... STUPIDE CHEVALIER ! ET STUPIDE HORLOGE MAGIQUE !*\n\n*bouffon...s'il te plait...*")
            liste_commentaire.append(commentaire)
            commentaire = ("Mais personne ne vient.                                                ...n'est-ce pas là la définition de la folie ? :)")
            liste_commentaire.append(commentaire)
            commentaire = ("*m-m-mon bouffon n'est pas mort, i-i-il est trop fort pour ca...*\n*Il se sont tous retournés contre moi c'est ça ?*"
                           "\n*HEIN ?*\n*JE ME SUIS FAIT TRAHIR ENCORE UNE FOIS ! HAHAHAHAHAHHHHHHH *")
            liste_commentaire.append(commentaire)
            commentaire = ("*MAGE ! TU M'A CREE CET ENDROIT !*\n*NE ME TOURNE PAS LE DOS TOI AUSSI !*")
            liste_commentaire.append(commentaire)
            commentaire = ("Une voix se met à résonner a l'interieur de la salle.")
            liste_commentaire.append(commentaire)
            commentaire = ("*Ce type a tué mon apprenti. Je m'occuperais personnellement de son cas. Débrouillez vous avec ca.*")
            liste_commentaire.append(commentaire)
            commentaire = ("Une armure d'or et de rubis magiques apparait sur le Roi Déchu. Une épée apparait a ses pieds.")
            liste_commentaire.append(commentaire)
            commentaire = ("*HAHAHA!*\n*A nous deux maintenant ASSASSIN !* ")
            liste_commentaire.append(commentaire)
        elif Player.numero_de_letage == 8:
            commentaire = "Le vieil homme à la barbe blanche se lève et vient se positionner à quelques mètres de vous,\nHache de guerre dans une main, Grimoire dans l'autre."
            liste_commentaire.append(commentaire)
            commentaire = ("*Sincèrement...*\n*Que dire de plus que ce qui n'a pas déjà été dit ?*")
            liste_commentaire.append(commentaire)
            commentaire = ("*Tu as tué tout le monde ici.*")
            liste_commentaire.append(commentaire)
            commentaire = ("*Tu a affronté la quintessence de gardes loyaux, fusionnés en une conscience collective, figés dans l'éternité d'un rêve couleur encre...*")
            liste_commentaire.append(commentaire)
            commentaire = ("*...d'un mercenaire devenu chevalier par peur de la mort, bercé d'idéaux souillés par la triste réalitée de sa condition...*")
            liste_commentaire.append(commentaire)
            commentaire = ("*...d'un roi dur mais juste, tranformé en monstre a son insu, gardé captif par les liens de la famille...*")
            liste_commentaire.append(commentaire)
            commentaire = ("*...d'un faux génie, un trésor d'efforts sans résultats, un apprenti loyal brisé par ses propres démons...*")
            liste_commentaire.append(commentaire)
            commentaire = ("*...d'un homme du nord portant un masque de faux sourires, porté par l'espoir de revoir ses contrées...*")
            liste_commentaire.append(commentaire)
            commentaire = ("*...d'un représentant du peuple des bas-fonds du royaume, sacrifié au nom d'une loi brimée par le sang et l'injustice...*")
            liste_commentaire.append(commentaire)
            commentaire = ("*...et enfin d'un pitoyable Roi qui a, dans sa folie, changé le destin de millions de pauvre gens.*")
            liste_commentaire.append(commentaire)
            commentaire = ("*Tu as usé de ta lame sur la quasi-entieretée de la cour du Roi Déchu...*")
            liste_commentaire.append(commentaire)
            commentaire = ("*...et maintenant il ne te reste plus que le magicien, l'outil sans qui tout cela n'aurait été possible.*")
            liste_commentaire.append(commentaire)
            commentaire = ("*Alors gardons cette conversation simple.*")
            liste_commentaire.append(commentaire)
            commentaire = ("*le Maitre Mage prend une grande inspiration.*"
                           "\n*JE SUIS LE MAITRE MAGE, CREATEUR DE CES LIEUX. MA MAGIE COULE EN CHACUN DE CES MURS.*"
                           "\n*JE SUIS L'APOGEE DE TA QUETE, L'OBJECTIF FINAL DE TA DESTINEE !*")
            liste_commentaire.append(commentaire)
            commentaire = ("Les hauts murs de l'arène se détruisent pour réveler les autres étages flottant dans un vide pourpre nacré, tournés vers vous deux."
                           "\nLa foule fantomatique silencieuse se met a s'agiter dans tout les sens,"
                           "\net sur un claquement de doigt du Maitre Mage, s'autorise a exprimer leur excitation de manière verbale."
                           "\nElle se met a scander votre nom, et celui du Maitre Mage, dans un chaos et un brouhaha sans nom !"
                           "\nLes spectateurs sont en pleine ébulition !\nVous reconnaissez les figures fantomatiques des différents boss dans les gradins !")
            liste_commentaire.append(commentaire)
            commentaire = ("*NE FAISONS PAS ATTENDRE NOTRE PUBLIC !*")
            liste_commentaire.append(commentaire)
            commentaire = ("*ROCK AND ROLL !*")
            liste_commentaire.append(commentaire)
        elif Player.numero_de_letage == 9:
            commentaire = (""
                           "\n"
                           "\n")
        elif Player.numero_de_letage == 10:
            commentaire = (""
                           "\n"
                           "\n")
        for commentaire in liste_commentaire:
            Affichage.IntroBoss(commentaire)

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

    def AfficheSauvegarde(self):
        for nombre in range(1, 7):
            if nombre in [1, 4]:
                print("Sauvegarde en cours.")
            elif nombre in [2, 5]:
                print("Sauvegarde en cours..")
            elif nombre in [3, 6]:
                print("Sauvegarde en cours...")
            time.sleep(0.3)
            ClearConsole()
        print("Sauvegarde Terminé !")
        self.EntreePourContinuer()
    
    def AfficheAvecUnTempsDattente(self, temps):
        time.sleep(temps)
        ClearConsole()

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
            commentaire = ("Vous laissez derrière vous les cris de désespoirs, et vous concentrez sur votre but."
                           "\nDes murs propres, neufs, ornés de torches. Un sol de marbre, dépassant les gradins, montant au plafond.\nEt une place au dessus de la sortie,"
                           " sur laquelle se trouve un vieil homme à la barbe blanche, soignée.\nVoila ce que vous trouvez en bas."
                           "\nVous voici au huitième étage du Coliseum , une arène digne de ce nom pour un affrontement avec son créateur.")
        elif Player.numero_de_letage == 9 and not Player.invitation_received:
            print("Derrière, vous voyez un long couloir.\nUne vieille porte rouillée a votre gauche vous intrigue,"
                           " mais pas plus que ca.")
            Affichage.EntreePourContinuer()
            print("Sur le chemin menant a la fin du couloir, vous voyez un petit trou dans les murs."
                           "\nA l'interieur, vous apercevez le mot coliseum reposant sur une sorte d'épée,\navec un genre de scintillement au dessus du i."
                           "\nEn dessous, le mot O B S E R V A T O R I U M est gravé au couteau, et un nombre en dessous de chaques lettre."
                           "\nCa fait un nombre sacrément long !")
            Affichage.EntreePourContinuer()
            commentaire = ("Mais vos pensées sont interrompues par le chant des oiseaux que vous entendez a quelques metres."
                           "\nVous courrez en direction de la sortie, et retrouvez l'herbe verte, les batiments au loin, et le grillage"
                           " caractéristique entourant le Coliseum.\nVous êtes sorti vivant !")
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
        self.library_used = False
        self.number_of_tirage = 0
        self.invitation_received = False
        self.chemin_musique = os.path.dirname(os.path.realpath(__file__))

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
        numero_de_laffichage = Player.AffichageItem()
        numero_de_laffichage = Player.AffichageSortSoin(numero_de_laffichage)
        return numero_de_laffichage, int(input("\nChoisissez une action avec les nombres : "))

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
        return numero_de_laffichage
    
    def AffichageSortSoin(self, numero_de_laffichage):
        numero_a_afficher = numero_de_laffichage
        for sort in Player.sorts_possedes:
            if sort in ANNUAIRESORTSSOIN:
                if numero_a_afficher == numero_de_laffichage:
                    print("\n     -={{ Sorts de Soin }}=-\n")
                print(f"{numero_a_afficher} - {sort} [{ANNUAIRESORTSSOIN[sort]}pm]")
                numero_a_afficher += 1
                break
        return numero_a_afficher
            



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
                    limite_de_choix, choix = Player.ShowcaseCaracteristics()
                    ClearConsole()
                    if choix in range(1, (limite_de_choix)):
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                ClearConsole()
                dans_le_menu = False
            else:
                if choix in range(2, (len(self.liste_ditem_a_afficher) + 2)):
                    item_a_utiliser = self.liste_ditem_a_afficher[choix - 2]
                    Player.UseItem(item_a_utiliser)
                else:
                    position_du_sort = choix - ((len(self.liste_ditem_a_afficher) + 1))
                    Player.UseHealingMagic(position_du_sort)

    def UseHealingMagic(self, position_du_sort):
        # prendre le sort en question
        liste_de_sorts_de_soin = []
        for sort in Player.sorts_possedes:
            if sort in ANNUAIRESORTSSOIN:
                liste_de_sorts_de_soin.append(sort)
        sort_de_soin_a_utiliser = liste_de_sorts_de_soin[(position_du_sort - 1)]
        # voir si on peux utiliser le sort
        cout_du_sort = ANNUAIRESORTSSOIN[sort_de_soin_a_utiliser]
        if Player.points_de_mana >= cout_du_sort:
            # utilisation du sort
            Player.points_de_mana -= cout_du_sort
            print(f"Vous prenez le temps de vous concentrer pour lancer le sort [{sort_de_soin_a_utiliser}], ce qui réduit son cout en mana et augmente son efficacité.")
            print(ANNUAIREDESCRIPTIONSORTSSOIN[sort_de_soin_a_utiliser])
            soin = round((((POURCENTAGESORTSOIN[sort_de_soin_a_utiliser]) + (self.points_dintelligence // 2)) / 100) * self.points_de_vie_max)
            if soin < SOINMINIMUMSORTSOIN[sort_de_soin_a_utiliser]:
                soin = SOINMINIMUMSORTSOIN[sort_de_soin_a_utiliser]
            soin += self.points_dintelligence
            self.points_de_vie += soin
            if self.points_de_vie > self.points_de_vie_max:
                self.points_de_vie = self.points_de_vie_max
            print(f"Vous reprenez {soin} points de vie !")
        else:
            # pas assez de mana
            print("Vous condensez le mana pour invoquer le sort...mais pas assez ne se réunit pour terminer l'invoquation.")
        Affichage.EntreePourContinuer()
        ClearConsole()

    def UseItem(self, item):
        if item in ["Feuille Jindagee", "Fruit Jindagee"]:
            Player.items_possedes[item] -= 1
            if item == "Feuille Jindagee":
                soin = 5 + round(Player.points_de_vie_max * 0.05)
                if soin < 8:
                    soin = 8
            elif item == "Fruit Jindagee":
                soin = 10 + round(Player.points_de_vie_max * 0.1)
                if soin < 13:
                    soin = 13
            if self.stigma_positif == "Pharmacodynamisme":
                soin += soin
            soin_final = soin * 3
            self.points_de_vie += soin_final
            if Player.points_de_vie > Player.points_de_vie_max:
                Player.points_de_vie = Player.points_de_vie_max
            print(f"Vous utilisez l'item [{item}], et regagnez {soin_final} points de vie en peu de temps !")
        elif item in ["Feuille Aatma", "Fruit Aatma"]:
            Player.items_possedes[item] -= 1
            if item == "Feuille Aatma":
                soin = 5 + round(Player.points_de_mana_max * 0.05)
                if soin < 8:
                    soin = 8
            elif item == "Fruit Aatma":
                soin = 10 + round(Player.points_de_mana_max * 0.1)
                if soin < 13:
                    soin = 13
            if self.stigma_positif == "Pharmacodynamisme":
                soin += soin
            soin_final = soin * 3
            self.points_de_mana += soin_final
            if Player.points_de_mana > Player.points_de_mana_max:
                Player.points_de_mana = Player.points_de_mana_max
            print(f"Vous utilisez l'item [{item}], et regagnez {soin_final} points de mana en peu de temps !")
        elif item in ["Remède", "Remède Superieur", "Remède Divin"]:
            Player.items_possedes[item] -= 1
            if item == "Remède":
                soin = round(Player.points_de_vie_max*0.1)
                if soin < 17:
                    soin = 17
            elif item == "Remède Superieur":
                soin = round(Player.points_de_vie_max*0.2)
                if soin < 27:
                    soin = 27
            elif item == "Remède Divin":
                soin = round(Player.points_de_vie_max*0.3)
                if soin < 39:
                    soin = 39
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
                if soin < 17:
                    soin = 17
            elif item == "Pillule Superieure":
                soin = round(Player.points_de_mana_max*0.2)
                if soin < 27:
                    soin = 27
            elif item == "Pillule Divine":
                soin = round(Player.points_de_mana_max*0.3)
                if soin < 39:
                    soin = 39
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
        if Player.numero_de_letage == 1:
            self.DoTheLibrary()  # bibliotheque de gros sorts (recuperer les sorts consignés)
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

    def DoTheLibrary(self):
        # Recuperation de la liste de sorts enregistrés
        donnees_de_s0ve = self.GetPermanentThingsFromS0ve()
        liste_de_sorts_enregistres = ast.literal_eval(donnees_de_s0ve["Livre de sort"])
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire == 1:
            liste_de_sorts_enregistres = ["jegardeleseigneurdevantmoisansrelâche;ilestàmadroite:jesuisinébranlable"]
        print("...et quelque chose attire votre attention !")
        Affichage.EntreePourContinuer()
        print("Derrière un rocher, vous trouvez un ancien passage quasi-effondré menant a une petite pièce étroite.")
        print("Au milieu se tient un livre usé par le temps, dont la couverture représente une magnifique cigogne bleue regardant vers la droite.")
        print("Vous ouvrez le livre...")
        Affichage.EntreePourContinuer()
        if Player.library_used:
            print("...mais ce dernier est vide.")
            print("Vous le refermez et repartez ailleurs.")
            Affichage.EntreePourContinuer()
        else:
            if "jegardeleseigneurdevantmoisansrelâche;ilestàmadroite:jesuisinébranlable" in liste_de_sorts_enregistres:
                mixer.quit()
            while True:
                try:
                    print("A l'interieur se trouvent plusieurs lignes écrite à l'encre noire."
                        "\nCertaines sont effacées, mais celles qui ne le sont pas semblent attirer votre main...")
                    numero_a_afficher = 1
                    for sort in liste_de_sorts_enregistres:
                        print(f"{numero_a_afficher} - Toucher les mots [{sort}]")
                        numero_a_afficher += 1
                    print(f"{numero_a_afficher} - Ne rien toucher")
                    choix = int(input("Que souhaitez vous faire ? "))
                    ClearConsole()
                    if choix in range(1, (len(liste_de_sorts_enregistres) + 2)):
                        break
                except ValueError:
                    ClearConsole()
            if choix == (len(liste_de_sorts_enregistres) + 1):
                print("Vous refermez le livre et vous éloignez de la pièce.")
                Affichage.EntreePourContinuer()
            elif liste_de_sorts_enregistres[choix-1] == "jegardeleseigneurdevantmoisansrelâche;ilestàmadroite:jesuisinébranlable":
                PlayMusic("abyss")
                print("C3 n'est pas vous.")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("Ca 6'est pas possible.")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("Vous 2'êtes jamais passé par la...")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("...et c9 n'est pourtant pas la premiere fois que vous venez ici.")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("C'est vo5s, sans l'être.")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("Ca n'est 1as vous, tout en l'étant.")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("Comment es8-ce possible ?")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("Comment est4ce possible...")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("Comment est-7e...")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("...")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("...oh.")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("je vois.")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("C'est quelqu'un d'autre.")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("C'est une trace.")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("...")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("Retrouve moi.")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("....non.")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("*Récupère* moi.")
                Affichage.AfficheAvecUnTempsDattente(3)
            else:
                Player.library_used = True
                Player.sorts_possedes.append(liste_de_sorts_enregistres[choix-1])
                Player.points_de_vie_max -= 5
                if Player.points_de_vie > Player.points_de_vie_max :
                    Player.points_de_vie = Player.points_de_vie_max
                print("Alors que vos doigts effleurent les lettres, l'entieretée de l'encre sur la page se rassemble au centre et saute sur votre main."
                      "\nElle se répend le long de votre membre, s'infiltre par vos pores, et fait apparaitre sur votre bras un tatouage étrange et douloureux.")
                print("Vous perdez 5 points de vie max !")
                print(f"Vous gagnez le sort [{liste_de_sorts_enregistres[choix-1]}]")
                Affichage.EntreePourContinuer()
                print("La page est maintenant vide.\nVous refermez le livre et repartez ailleurs.")
                Affichage.EntreePourContinuer()
        if "jegardeleseigneurdevantmoisansrelâche;ilestàmadroite:jesuisinébranlable" in liste_de_sorts_enregistres:
            PlayMusic(f"etage_{Player.numero_de_letage}")

    def GetPermanentThingsFromS0ve(self):
        dictionnaire_de_choses_permanentes = {}
        dir_path = os.path.dirname(os.path.realpath(__file__))
        #fichier de sauvegarde (temporaire)
        chemin_du_fichier_save = dir_path + "\\s0ve.txt"
        with open(chemin_du_fichier_save, "r") as fichier:
            reader = csv.DictReader(fichier, delimiter="|")
            for line in reader:
                dictionnaire_de_choses_permanentes[line["Caracteristique"]] = line["Valeur"]
        return dictionnaire_de_choses_permanentes


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
            "Nombre d'ennemis restant a l'étage": "",
            "Le Redcoin d'extermination a ete recu": "",
            "Le livre de sort a ete utilise": "",
            "Le Redcoin du marchand a ete achete": "",
            "Nombre de Tirage acheté": "",
            "Possede une gemme de vie": "",
            "Possede une gemme de mana": "",
            "Possede une fée": "",
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
        self.dictionnaire_de_sauvegarde["Nombre d'ennemis restant a l'étage"] = Player.nombre_dennemis_a_letage
        self.dictionnaire_de_sauvegarde["Le Redcoin d'extermination a ete recu"] = Player.red_coin_recu_par_extermination
        self.dictionnaire_de_sauvegarde["Le Redcoin du marchand a ete achete"] = Player.redcoin_bought
        self.dictionnaire_de_sauvegarde["Nombre de Tirage acheté"] = Player.number_of_tirage
        self.dictionnaire_de_sauvegarde["Possede une gemme de vie"] = Player.gemme_de_vie
        self.dictionnaire_de_sauvegarde["Possede une gemme de mana"] = Player.gemme_de_mana
        self.dictionnaire_de_sauvegarde["Possede une fée"] = Player.possede_une_fee
        self.dictionnaire_de_sauvegarde["Le livre de sort a ete utilise"] = Player.library_used

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
        Player.nombre_dennemis_a_letage = int(self.dictionnaire_de_sauvegarde["Nombre d'ennemis restant a l'étage"])
        Player.red_coin_recu_par_extermination = ast.literal_eval(self.dictionnaire_de_sauvegarde["Le Redcoin d'extermination a ete recu"])
        Player.redcoin_bought = ast.literal_eval(self.dictionnaire_de_sauvegarde["Le Redcoin du marchand a ete achete"])
        Player.number_of_tirage = int(self.dictionnaire_de_sauvegarde["Nombre de Tirage acheté"])
        if "Invitation Recue" in self.dictionnaire_de_sauvegarde:
            Player.invitation_received = ast.literal_eval(self.dictionnaire_de_sauvegarde["Invitation Recue"])
        Player.library_used = ast.literal_eval(self.dictionnaire_de_sauvegarde["Le livre de sort a ete utilise"])

    def FromDictToSaveFile(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        chemin_du_fichier_save = dir_path + "\\save.txt"
        with open(chemin_du_fichier_save, "w") as fichier:
            fichier.write("Caracteristique|Valeur")
            for caracteristic in self.dictionnaire_de_sauvegarde:
                fichier.write(f"\n{caracteristic}|{self.dictionnaire_de_sauvegarde[caracteristic]}")

    def FromSaveFileToDict(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        #fichier de sauvegarde (temporaire)
        chemin_du_fichier_save = dir_path + "\\save.txt"
        with open(chemin_du_fichier_save, "r") as fichier:
            reader = csv.DictReader(fichier, delimiter="|")
            for line in reader:
                self.dictionnaire_de_sauvegarde[line["Caracteristique"]] = line["Valeur"]
        #autre sauvegarde (permanente)
        chemin_du_fichier_save = dir_path + "\\s0ve.txt"
        with open(chemin_du_fichier_save, "r") as fichier:
            reader = csv.DictReader(fichier, delimiter="|")
            for line in reader:
                self.dictionnaire_de_sauvegarde[line["Caracteristique"]] = line["Valeur"]

    def SaveTheGame(self):
        self.FromPlayerToDict()
        self.FromDictToSaveFile()
        Affichage.AfficheSauvegarde()
        while True:
            try:
                print("Voulez vous quitter la partie ?")
                print("\n1 - Oui")
                print("2 - Non")
                choix = int(input("\n"))
                ClearConsole()
                if choix == 1:
                    sys.exit()
                elif choix == 2:
                    break
            except ValueError:
                ClearConsole()

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
    dir_path = Player.chemin_musique
    musique = dir_path + f"\\{musique}.mp3"
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


def GetRandomItemFromList(liste):
    number_of_item = len(liste)
    numero_aleatoire = random.randint(0, (number_of_item - 1))
    return liste[numero_aleatoire]


def open_image(chemin_vers_limage):
    # Créer une fenêtre Tkinter
    root = tk.Tk()

    # Créer une image Tkinter à partir du fichier
    image = PhotoImage(file=chemin_vers_limage)

    # Créer un canevas pour afficher l'image
    canvas = tk.Canvas(root, width=image.width(), height=image.height())
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=image)

    # Boucle principale Tkinter
    root.mainloop()


def GetChoiceRecup():
    print("     -=[ Outil de Récupération de Données ]=-")
    print("\nInserez le numéro de l'adresse de l'information souhaitée,\net laissez notre programme récuperer ces données pour vous !")
    print("Plus besoin de paniquer lorsque l'on supprime d'anciennes données sans le vouloir !")
    print("Vos données n'auront plus de secret pour vous !")
    return int(input("\nNuméro de l'adresse ipv4 : "))


def ShowRecup():
    # images doivent etre en png
    while True:
        try:
            choix = GetChoiceRecup()
            ClearConsole()
            break
        except ValueError:
            ClearConsole()
    Affichage.AfficheLongChargement()
    if choix in [362951847]:
        if choix == 1:
            nom_de_limage = "Feu"
        elif choix == 1:
            nom_de_limage = "Foudre"
        elif choix == 2:
            nom_de_limage = "Glace"
        elif choix == 3:
            nom_de_limage = "Terre"
        elif choix == 4:
            nom_de_limage = "Physique"
        elif choix == 5:
            nom_de_limage = "Sang"
        elif choix == 6:
            nom_de_limage = "Ame"
        elif choix == 362951847:
            nom_de_limage = "python_properties_Anox"
        elif choix == 8:
            nom_de_limage = "Indice2"
        elif choix == 9:
            nom_de_limage = "Indice3"
        elif choix == 10:
            nom_de_limage = "Invitation"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        chemin_de_limage = dir_path + "\\"
        open_image(f"{chemin_de_limage}{nom_de_limage}.xldr")
    else:
        print("                           Donnée Récupérée :")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15szfdaqsxsdfadza33e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5fzr59168126s1ef6s5g12r65313s0fe6zfesrfesrgfefsef16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15zadazdzadzsdz6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6adzdazdadazda3e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3th4d9hd1g6e6d52u964kj,9u8njgh6fd5r1s6j1gu85yhe653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wgseh8g71sr6hju9i6mo1ikh6ugjhy1tdg9rs6f216rrj82tu9j61i9r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
        print("zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5")
    Affichage.EntreePourContinuer()


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


def ShowTutorial():
    PlayMusic("tutorial")
    print("                    { Tutoriel }")
    print("             { Partie 1 : Introduction }")
    print("\nBienvenue dans le Coliseum ! Prononcé Co-li-zé-oum, ca veut dire Colisée en Latin.")
    print("Vous êtes sans doute excités a l'idée de vous plonger dans les méandres de cette batisse légendaire !")
    print("Mais avant toute chose, quelques bases à connaitre.")
    print("\n\n")
    Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("              { Partie 2 : Histoire }")
    print("\nLe coliseum est une batisse ancienne, commandée par un roi fou a son magicien pour enfermer")
    print("les gens de son peuple qu'il croyait dangereux. Au fur et a mesure des années, de plus en plus")
    print("d'innoncent se sont retrouvé dans les arènes sordides, a combattre des créations monstrueuses de chair et de sang.")
    print("Jusqu'à un beau matin de printemps ou le Roi, dans un généreux élan de folie et de paranoïa, décida de se jeter dans")
    print("sa création, accompagnée de toute sa cour."
          "\nDes années plus tard, la batisse sera déclarée dangereuse par les gouvernements,")
    print("et plus personne ne se frottera aux étages malicieux du Coliseum, qui changera alors de nom et de structure...")
    print("...mais c'est une histoire pour plus tard :)")
    print("En attendant, plusieurs personnages se seront attaqué au tombeau du Roi fou, pour diverses raisons,"
          "\net c'est eux que vous allez pouvoir controller !")
    print("\n\n")
    Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("             { Partie 3 : Bien Commencer }")
    print("\nLe coliseum se compose de plusieurs étages. Pour naviguer dans les étages inferieurs, vous devez")
    print("d'abord battre le boss de l'étage en cours. Seulement, c'est le plus souvent un individu sacrément puissant !")
    print("Comment faire ? Eh bien... devenir plus fort !")
    print("Chaques monstres tués vous rapoorte une amélioration de certaines de vos caractéristiques, et un peu de golds.")
    print("Vous pouvez ensuite échanger vos gold contre des objets chez le marchand de l'étage.")
    print("Et une fois que vous serez dotés de meilleurs objets, améliorés avec de meilleurs caractéristiques, et")
    print("équ00000ipés de meilleqdznqdurs tttAAAaaaalEnnnttsss...z,lqnd.......")
    print("Vous verrez que le boss de l'étage ne sera plus un mur, mais un simple obstacle sur votree chemin ! ")
    print("Ainsi, il faut tuer des monstres, acheter des objets, tuer le boss, descendre, et répéter l'opération jusqu'au")
    print("dernier étage : le HdUiIxTiIèEmMeE !")
    print("\n\n")
    Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("         { Partie 4a : Les menus : Navigation }")
    print("\nVous pouvez vous diriger dans les menus a l'aide des nombres, qui sont affectés a chaques actions.")
    print("Par exemple, dans le menu principal, vous pouvez commencer une nouvelle aventure avec 1,")
    print("et continuer une partie déja sauvegardée avec 2. Vous pouvez aussi lancer le tutoriel avec 3")
    print("(ce que vous avez faitpl ou ezdnore landzd leefnzos pefisp avevevevc WWWWXXXWWW.")
    print("\nEnfin bref, chaque actions sont affectées a un numéro.")
    print("Et n'ayez pas peur ! Si vous rentrez un mauvais numéro, , une chaine de caractère ou même rien du tout,")
    print("le programme continuera normalement sans planter, et se contentera de vous redemander votre choix !")
    print("\n\n")
    Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("          { Partie 4b : Les menus: Utilité }")
    print("\nGrace aux menus, vous pouvez naviguer dans vos options possibles pour chaques situations.")
    print("Le menu de l'étage actuel du Coliseum permet ainsi de:")
    print(" - Combattre un monstre (attention, le nombre de monstre par étage est limité ! ne fuyez pas tout vos commbats !)"
          "\n- Combattre un boss / Descendre a l'étage inferieur (si le boss est battu)"
          "\n- Acheter des items chez le marchand "
          "\n- etc")
    print("Un même nombre change d'action effectuée selon la situation actuelle.")
    print("\n\n")
    Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("            { Partie 5 : Les Combats }")
    print("\nLe Coliseum s'explore en deux temps : "
          "\nLe temps de repos, ou menu d'étage, qui permet de choisir ses actions"
          "\nLe temps de combat, pour devenir plus fort ou battre le boss.")
    print("\nEn temps de combat, tout se déroule au tour par tour.")
    print("En premier lieu s'effectuent les actions de début de combat.")
    print("Ensuite, vous choisissez un menu parmis ceux disponibles.")
    print("Juste après, vous choisissez une action dans le menu affiché.")
    print("Votre action est effectuée, puis celle de l'ennemi a la suite.")
    print("Les différents effets d'altérations d'états s'appliquent")
    print("Et on recommence jusqu'a ce qu'un des deux participant meure ou fuie.")
    print("\ngardez a l'esprit que vos points de vie représentent la vitalité qu'il vous reste,"
          "\nEt que si ils tombent a zéro, c'est terminé.\nCepandant, les points de mana servent juste"
          "a lancer des sorts, et peuvent descendre a zéro sans réelles conséquences.")
    print("\n\n")
    Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("         { Partie 6a : Foire aux Questions }")
    print("\n*Dans le menu de choix des personnage, il y a des stigmas. C'est quoi ?*")
    print(" - Ce sont des passifs intrinsèques aux personnages, liés a leur situation ou leur experience,"
          " qui s'activent avant, pendant, ou apres un combat.")
    print("\n*J'ai vu qu'on pouvait utiliser des redcoins dans le menu d'étage. C'est quoi ? Ca fait quoi ?*")
    print("˙ǝɹı̣ɹɔ́ǝp ǝp zǝuǝʌ snoʌ ǝnb nuǝɯ ǝן suɐp ́ǝʇou ʇsǝ uı̣oɔpǝꓤ uǝ ʇnoɔ uos ǝnb ı̣suı̣ɐ sʇuǝןɐʇ ǝnbɐɥɔ ǝp ǝpoɔ ǝ"
          "ן ʇƎ ˙ǝɹʇnɐ ʇǝ 'sǝpnʇı̣ʇdɐ ' sǝnbɐʇʇɐ sǝןןǝʌnou ǝp ɹǝnboןq́ǝp ʇuǝʌnǝd sʇuǝןɐʇ sǝƆ ˙npı̣ʌı̣puı̣'ן ǝp sdɹoɔ ǝן suɐp"
          " 'sʇuǝןɐʇ sǝ́ǝןǝddɐ 'sǝןɐı̣ɔ́ǝds sǝɔuǝʇ́ǝdɯoɔ sǝp ǝɹʇı̣ɐu ʇı̣ɐɟ ')sǝɹɟɟı̣ɥɔ ǝp ǝʇı̣ns ǝun ɹɐd ́ǝnbı̣puı̣ 'ןɐɹ́ǝúǝƃ uǝ("
          " sı̣ɔ́ǝɹd ǝɹpɹo un suɐp ɐuɐɯ np uoı̣ʇɐןnɔɹı̣ɔ ɐן ɐ sǝ́ǝןdnoɔ ' ʇǝ sdɹoɔ np sǝuoz sǝp ɹǝןnɯı̣ʇs ǝp ʇǝɯɹǝd ǝpı̣nbı̣ן ǝƆ"
          " ˙uı̣ǝs uos uǝ nuǝʇuoɔ ǝɹoןoɔuı̣ ǝpı̣nbı̣ן np ʇuǝı̣ʌ ʇǝ 'ǝɹı̣ɐןı̣ɯı̣s ʇsǝ suı̣oƆpǝꓤ un'p ɹnǝןɐʌ ɐꓶ ˙sǝʇı̣ɐɟ ʇuǝı̣ɐʇ́ǝ sǝןןǝ"
          " sǝןןǝnbsǝן suɐp nɐı̣ɹ́ǝʇɐɯ np ́ǝʇı̣soı̣ɔ́ǝɹd ɐן ǝp ʇı̣ɐuǝʌ ǝnbı̣ʇuɐ ǝɯoꓤ ɐן ǝp sǝɔ̀ǝı̣d sǝp ɹnǝןɐʌ ɐꓶ")
    print("\n\n")
    Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("        { Partie 6b : Foire aux Questions }")
    print("\n*Ya un type bizarre qui execute les rochemikazes. C'est qui ?*")
    print(" - C'est Alfred.")
    print("\n*Ya des types de sorts et de techniques différentes qui inflige des effets élémentaires différents, non ?*")
    print(" - C'est exact. Par exemple, la glace peut geler, ce qui fait qu'une ennemi prendra 50% de dégâts supplémentaire.")
    print("\n*...et le reste ? Les autres altérations d'états ? Et les effets des talents ? Et les effets des stigmas ?\nVous n'avez rien expliqué !*")
    print(" - C'est aussi exact ! Le fun du Coliseum viens du fait que vous êtes lachés dans un environnement étranger, sans guide,")
    print("et avec le moins d'expliquations possibles !"
          "\nAlors prenez un papier, un crayon, et notez au fur et a mesure les informations que vous découvrirez !")
    print("\n\n")
    Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("            { Partie 7 : Bonne chance ! }")
    print("\nMaintenant, vous savez tout ce qu'il y a a savoir pour débuter une partie.")
    print("Alors qu'attendez vous ? Ne soyez pas timide ! Il y a une montagne de chose a faire et a découvrir !")
    print("Lancez donc une partie sans attendre, et dans l'échec apprenez a réussir !")
    print("\n\n")
    Affichage.EntreePourContinuer()
    PlayMusic("start")
    


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
                if choix in [1, 2, 3, 24, 1521951822120151892113]:
                    break
            except ValueError:
                ClearConsole()

        # choix du personnage
        if choix == 1:
            personnage_a_ete_choisi = ChoseCharacter(Player)
            if personnage_a_ete_choisi:
                # personnage choisi
                in_menu_principal = False
                #sauvegarde et charge le personnage choisi
                Save.FromPlayerToDict()
                Save.FromDictToSaveFile()
                Save.FromSaveFileToDict()
                Save.FromDictToPlayer()
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

        elif choix == 24:
            mixer.quit()
            ShowRecup()
            PlayMusic("start")


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
          f"\n      1 - Affronter un monstre ({Player.nombre_dennemis_a_letage} restants)"
          f"\n      2 - {Player.commentaire_boss}"
          "\n\n          ~~{ Interraction }~~"
          "\n      3 - Interragir avec le Marchand"
          "\n      4 - Observer l'Etage (WIP)"
          f"\n\n          ~~{{ {Player.nom_du_personnage} }}~~"
          "\n      5 - Fiche de Personnage"
          "\n      6 - Utiliser un Red Coin"
          "\n      7 - Sauvegarder la Partie"
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
    if Player.numero_de_letage == 11 or (Player.numero_de_letage == 9 and not Player.invitation_received) :
        game_in_session = False
    else:
        game_in_session = True
    return game_in_session


def DoRedcoin():
    while True:
        while True:
            try:
                print("     -={ RedCoin }=-   /925435351305251SERVICEDERECUPERATIONDEDONNEES7117764")
                print("                      /7420952721321625369856321569852156AOUVRIRVIALEMENU556")
                print("1 - Retour           /981265161565513513513165050742315698522685256PRINCIPAL")
                print(" ____/1233232311579764382419683214618568246856824565546532854663243615463745")
                print(" \95363541653155641654135641459565415631612952955265653959562413153556163153")
                print("Code -       Nom       -    Prix    /128243165325615323235106506863236550325")
                print("1257 - Affinité de Feu - 1 Redcoin /52565265163512ERRORERRORERRORERORERROR98")
                print("5675 - Affinité de Foudre - 1 Red/487965651268416535498165319651965ERRORROOR")
                print("9731 - Affinité de Sang - 1 Redc/789ERREUR:DONNESMANQUANTES96515866519651988")
                print("7563 - Af/7845123553213506516896652565167841961561653163165ERRORERRORERROR58")
                print("8240 - A/7845621365265216532561517VEUILLEZCONTACTERLESERVICEINFORMATIQUE9465")
                print("6______/789OUUTILISEZNOTRESERVICE65235216513351DERECUPERATIONDEDONNEES313135")
                print("/5698994524527/==================================\9AU5NUMERO5612353105151588")
                print("1569899452452/Talent à débloquer avec le nombre corresponda\_35168SUIVANT:24")
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
            if Player.stigma_negatif != "Incompatible":
                Player.talents_possedes.append(talent)
                Player.nombre_de_red_coin -= cout_du_talent
                print("Vous buvez le liquide incolore contenu dans les redcoins et faites circuler votre mana comme indiqué par le code .")
                print(f"Vous gagnez le talent [{talent}] !")
                Affichage.EntreePourContinuer()
                CheckForFusionOfTalent(talent)
            else:
                Player.nombre_de_red_coin -= cout_du_talent
                print("Vous buvez le liquide incolore contenu dans les redcoins et faites circuler votre mana comme indiqué par le code...")
                print("...avant de vomir violemment tout le contenu de votre estomac.")
                print("On dirait que votre corps n'est pas compatible avec les redcoins.")
                Affichage.EntreePourContinuer()

    
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
        if (
                ("Rapide" in Player.talents_possedes) and
                ("Grand Froid" in Player.talents_possedes) and
                ("Réflex" in Player.talents_possedes) and
                ("Conditions Limites" in Player.talents_possedes) and
                ("Aura de Feu" in Player.talents_possedes) and
                ("Poussière de Diamants" in Player.talents_possedes)
        ):
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
        DoFight()
    elif choix == 2:
        #combat contre boss
        if not Player.boss_battu:
            DoBossFight()
        #descente au niveau inferieur
        else:
            game_in_session = GoDown() 
            if game_in_session:
                PlayMusic(f"etage_{Player.numero_de_letage}")
    elif choix == 3:
        Trader.DoTrading() #DONE
    elif choix == 4:
        print("Vous vous baladez dans l'étage...")
        if Player.numero_de_letage == 1 :
            Observation.SeeSomething()
        else:
            print("...et ne trouvez rien d'interressant.")
        Affichage.EntreePourContinuer()
    elif choix == 5:
        Player.ShowPlayerCaracteristicsAndItems() #DONE
    elif choix == 6:
        DoRedcoin() #DONE
    elif choix == 7:
        Save.SaveTheGame() #DONE
PlayMusic("battle_win")
print("Vous avez gagné le jeu !")
Affichage.EntreePourContinuer()





# Lance un debug pour la méthode GetUserChoice du controlleur
#control.DebugGetUserChoice()
#control.PatternDesignConstantUpdater()
#control.Cat_astrophe()





