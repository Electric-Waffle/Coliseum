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
import threading
import traceback
from turtle import *
import math


# 0nom 1description 2stigma+ 3stigma- 4stigma* 5techniques
# 6sorts 7items 8talents 9vie 10mana 11force
# 12inteligence 13defence 14tauxcoupcrit
# 15degatcoupcrit 16tauxsortcrit 17degatsortcrit
# 18tauxesquive 19gold
LISTETECHNIQUES = [
    "Lance Rapide",
    "Lance Statique",
    "Lance Electrique",
    "Lance de l'Eclair",
    "Lance Foudroyante",
    "Lance de la Mort Blanche",
    "Bô Chaud",  #
    "Bô Brulant",  #
    "Bô Enflammé",  #
    "Bô de la Fournaise",
    "Bô Magmatique",
    "Bô Solaire",
    "Katana Bleu",
    "Katana Froid",
    "Katana Givré",
    "Katana Glacial",
    "Katana Polaire",
    "Katana Zéro",
    "Corne Argile",  #
    "Corne Lapis",  #
    "Corne Granite",  #
    "Corne Obsidienne",
    "Corne de la Montagne",
    "Corne Continentale",
    "Poing Léger",  #
    "Poing Renforcé",  #
    "Poing Lourd",  #
    "Poing Maitrisé",  #
    "Poing Fatal",  #
    "Poing de la Comète",
    "Dague Volevie",
    "Dague Siphoneuse",
    "Dague Vampirique",
    "Dague Parasite",
    "Dague Destructrice",
    "Dague Créatrice",
]
LISTESORTS = [
    "Faisceau Rapide",
    "Faisceau Statique",
    "Faisceau Electrique",
    "Faisceau de l'Eclair",
    "Faisceau Foudroyant",
    "Faisceau de la Mort Blanche",
    "Thermosphère Chaude",
    "Thermosphère Brulante",
    "Thermosphère Enflammée",
    "Thermosphère de la Fournaise",
    "Thermosphère Magmatique",
    "Thermosphère Solaire",
    "Pic Bleu",
    "Pic Froid",
    "Pic Givré",
    "Pic Glacial",
    "Pic Polaire",
    "Pic Zéro",
    "Création d'Argile",
    "Création de Lapis",
    "Création de Granite",
    "Création Obsidienne",
    "Création de la Montagne",
    "Création Continentale",
    "Explosion Légère",
    "Explosion Renforcée",
    "Explosion Lourde",
    "Explosion Maitrisée",
    "Explosion Fatale",
    "Explosion de la Comète",
    "Dance Volevie",
    "Dance Siphoneuse",
    "Dance Vampirique",
    "Dance Parasite",
    "Dance Destructrice",
    "Dance Créatrice",
    "Sonata Pitoyable",  # 3% ou 8pv
    "Sonata Miséricordieuse",  # 5% ou 15pv
    "Sonata Empathique",  # 12% ou 20pv
    "Sonata Sincère",  # 17% ou 25pv
    "Sonata Bienveillante",  # 20% ou 33pv
    "Sonata Absolutrice",  # 25% ou 40pv
]
ANNUAIRESORTSSOIN = {  # cout moins élevé quand utilise sort en dehors combat
    "Sonata Pitoyable": 6,
    "Sonata Miséricordieuse": 13,
    "Sonata Empathique": 18,
    "Sonata Sincère": 23,
    "Sonata Bienveillante": 18,
    "Sonata Absolutrice": 38,
}
ANNUAIREDESCRIPTIONSORTSSOIN = {
    "Sonata Pitoyable": "Un bruit pathétique vous enveloppe et apaise la douleur de vos blessures.",
    "Sonata Miséricordieuse": "Un son a peine apréciable se plaque contre votre peau et referme vos blessures.",
    "Sonata Empathique": "Une musique potable soulage votre âme et vos blessures.",
    "Sonata Sincère": "Un chant cristallin inspire votre esprit et revigore votre corps.",
    "Sonata Bienveillante": "Une chorale glorieuse vous fait oublier les problèmes de votre situation et cicatrise vos blessures.",
    "Sonata Absolutrice": "Une mélodie féerique ramène votre être tout entier a un état optimal.",
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
        (
            "Chasseur hermite, ancien esclave pour un bourgeois fanatique de l'argent."
            "\n           Parti dans le Coliseum pour devenir plus fort afin de prendre sa revanche."
        ),  # char
        "Solide",  # char stigma +
        "Chrometophobia",  # char stigma -
        "Aucun",  # char stigma *
        ["Attaque Légère"],  # char list technic
        ["Explosion Légère"],  # char list sorts
        {
            "Feuille Jindagee": 3,
            "Fruit Jindagee": 1,
            "Feuille Aatma": 2,
            "Remède": 5,
            "Fléchette Bleue": 2,
            "Mutagène Rouge": 1,
        },  # char dict of int items
        ["Affinitée Physique"],  # char list
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
        []  # char artefact
    ],
    "Elma": [  # char
        "Elma",
        (
            "Quinquagénère, Voleuse inarrêtable, surnommée Princesse de Suie, a la tête d'un gang de sans-abris."
            "\n           Jetée dans le Colliseum par le prétendant au titre de chef, plus jeune et plus soutenu."
            "\n           Son corps brisé à trempé dans une fontaine de fée, et l'a assez revigoré pour qu'elle tente de sortir pour reprendre sa place à la surface."
        ),  # char
        "Bénie par les Fées",  # char stigma +
        "Famine",  # char stigma -
        "Aucun",  # char stigma *
        ["Attaque Légère", "Dague Volevie"],  # char list technic
        [],  # char list sorts
        {},  # char dict of int items
        [],  # char list
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
        []  # char artefact
    ],
    "Auguste": [  # char
        "Auguste",
        (
            "Un écrivain brillant ayant perdu ses mains dans un accident de voiture."
            "\n           Parti dans le Coliseum après avoir entendu parler de la puissance qu'on peut y acquérir."
            "\n           Pense pouvoir y trouver un moyen de retrouver des mains biologiques, artificielles ou...magiques."
        ),  # char
        "Diligent",  # char stigma +
        "Manchot",  # char stigma -
        "Aucun",  # char stigma *
        [
            "Attaque Légère",
        ],  # char list technic
        ["Thermosphère Chaude", "Sonata Pitoyable"],  # char list sorts
        {},  # char dict of int items
        [],  # char list
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
        []  # char artefact
    ],
    "Saria": [  # char
        "Saria",
        (
            "Une des dernières druidesses encore en vie pendant les affres de L'inquisition espagnole"
            "\n           Est venue se cacher des buchers et des horreurs dans le seul endroit ou on la considererait morte sans l'être vraiment : le Coliseum."
            "\n           S'étonne que son lien avec la nature dans cet endroit sordide ne soit pas brisé, malgrès l'omniprésence de la mort."
        ),  # char
        "Cueilleuse",  # char stigma +
        "Incompatible",  # char stigma -
        "Aucun",  # char stigma *
        [
            "Attaque Légère",
        ],  # char list technic
        ["Sonata Miséricordieuse"],  # char list sorts
        {
            "Feuille Jindagee": 5,
            "Fruit Jindagee": 5,
            "Feuille Aatma": 5,
            "Fruit Aatma": 5,
        },  # char dict of int items
        ["Affinitée de Terre"],  # char list
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
        []  # char artefact
    ],
    "Vesperum": [  # char
        "Vesperum",
        (
            "Un homme devenu démon par amour et ayant échappé aux enfers, à la recherche de pouvoir afin de prendre le controle de l'Au-Dela."
            "\n           A été attiré au Coliseum par l'odeur de mort qui s'en échappe, et le son de millions d'âmes emprisonnées entre ses murs."
            "\n           Ne sait pas pourquoi, mais les troupes du Paradis et de l'Enfer à ses trousses ne viennent pas le chercher ici."
        ),  # char
        "Forces Obscures",  # char stigma +
        "Maudit",  # char stigma -
        "Aucun",  # char stigma *
        ["Attaque Légère", "Katana Bleu"],  # char list technic
        ["Dance Volevie"],  # char list sorts
        {},  # char dict of int items
        ["Affinitée de Sang"],  # char list
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
        []  # char artefact
    ],
    "Lucien": [  # char
        "Lucien",
        (
            "Descendant du mage qui à crée le Coliseum, brillant magicien toujours comparé a son ancêtre."
            "\n           Venu régler ses comptes avec le grand Maitre Mage afin de décider qui des deux est le meilleur."
            "\n           Revient de 5 ans a écumer les mers aux coté de son fidèle équipage de pirate"
        ),  # char
        "Grande Connaissance",  # char stigma +
        "Colérique",  # char stigma -
        "Logique au dessus des Cieux",  # char stigma *
        ["Attaque Légère", "Poing Renforcé"],  # char list technic
        [
            "Faisceau Statique",
            "Thermosphère Brulante",
            "Pic Froid",
            "Création de Lapis",
            "Explosion Renforcée",
            "Dance Siphoneuse",
            "Sonata Miséricordieuse",
        ],  # char list sorts
        {},  # char dict of int items
        [],  # char list
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
        ["Vieux Couteau Rouillé"]  # char artefact
    ],
    "Élémia": [  # char
        "Élémia",
        (
            "Inventeuse, créatrice, artiste, elle à tout fait, à part peut être suivre le destin qu'on lui à donné."
            "\n           Venue tester sa toute dernière invention en condition réelle : une armure de Deus-ex-machinium."
            "\n           On dit du dernier héros ayant besoin d'une inventrice dans son"
            " équipe pour sauver le monde... "
            "\n           ...qu'il est ressorti de son village avec un bras en moins a cause d'une des inventions ratée d'élémia."
        ),  # char
        "Débrouillarde",  # char stigma +
        "Flemme",  # char stigma -
        "Emotion au dessus des Cieux",  # char stigma *
        [
            "Attaque Légère",
        ],  # char list technic
        [],  # char list sorts
        {},  # char dict of int items
        [],  # char list
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
        []  # char artefact
    ],
    "Samantha": [  # char
        "Samantha",
        (
            "Une doctoresse diplomée de l'Universitée Prestigieuse de Prestige-City. Endettée jusque au cou **grâce** a son prêt etudiant."
            "\n           Entre payer sa detter sur les 50 prochaines années de sa vie ou entrer dans le Coliseum pour gagner des richesses, elle à fait son choix."
            "\n           Elle a pillée les réserves médicales de son école avant de venir ici."
        ),  # char
        "Pharmacodynamisme",  # char stigma +
        "Serment d'Hyppocrate",  # char stigma -
        "Aucun",  # char stigma *
        [
            "Attaque Légère",
        ],  # char list technic
        [],  # char list sorts
        {
            "Remède": 15,
            "Pillule": 15,
            "Grand Mutagène Doré": 1,
        },  # char dict of int items
        [],  # char list
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
        []  # char artefact
    ],
    "Emy": [  # char
        "Emy",
        (
            "Une ancienne Louve de glace devenue humaine, prise d'affection pour un vieil homme tombé par hasard dans le Coliseum."
            "\n           Après sa transformation, sentant naitre de nouvelles émotions et sensations, elle a paniquée et s'est retrouvée au premier étage."
            "\n           On dit qu'elle est devenue humaine lorsque le vieil homme dont elle s'occupait, se sentant mourir, lui à offert son coeur plein de compassion."
            "\n           Littéralement."
        ),  # char
        "Conception du Mana",  # char stigma +
        "Attache Physique",  # char stigma -
        "Chaos Emotionel",  # char stigma *
        ["Attaque Légère", "Katana Bleu"],  # char list technic
        ["Pic Bleu", "Pic Froid"],  # char list sorts
        {},  # char dict of int items
        ["Affinitée de Glace", "Ere Glaciaire"],  # char list
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
        ["Demi-Marque du ???"]  # char artefact
    ],
    "Terah": [  # char
        "Terah",
        (
            "Un adolescent sans histoire, sans famille, sans amis. Surnommé *Enfant Maudit* sans qu'il ne sache pourquoi, tout son village l'évite."
            "\n           Il n'a aucune attache au monde des vivant. Alors quand il a entendu la voix des morts qui l'appelait, il n'a pas hésité une seconde a rentrer dans le Coliseum."
            "\n           Amenez le moi."
        ),  # char
        "Endurci",  # char stigma +
        "Incontrolable",  # char stigma -
        "Sanjiva",  # char stigma *
        ["Attaque Légère", "Lance Rapide"],  # char list technic
        [],  # char list sorts
        {},  # char dict of int items
        [],  # char list
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
        []  # char artefact
    ],
    "Peralta": [  # char
        "Peralta",
        (
            "Une policière sous couverture, accusée a tort par un collègue corrompu, attendant son procès."
            "\n           Enlevée de la prison par le gang qu'elle infiltrait, jetée dans le Coliseum pour éviter qu'elle ne parle, déterminée a sortir de là."
            "\n           Elle à un caractère bien trempée, et est connue dans son service pour son coup de boule phénoménal."
        ),  # char
        "Bergentruckung",  # char stigma +
        "Mauvaise Réputation",  # char stigma -
        "Aucun",  # char stigma *
        ["Attaque Légère", "Lance Rapide"],  # char list technic
        [],  # char list sorts
        {},  # char dict of int items
        [],  # char list
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
        []  # char artefact
    ],
    "Redde": [  # char
        "Redde",
        (
            "Un streamer de jeux vidéo en burnout total, perdu dans son propre monde et persuadé d'être le personnage principal d'une histoire dont seul lui connait le déroulement."
            "\n           Entre dans le Coliseum pour vivre **l'aventure ultime**."
            "\n           Est connu pour son sens du showmanship inégalé."
        ),  # char
        "Dernier Choix",  # char stigma +
        "Pas d'Echappatoire",  # char stigma -
        "Aucun",  # char stigma *
        [
            "Attaque Légère",
        ],  # char list technic
        [],  # char list sorts
        {},  # char dict of int items
        [],  # char list
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
        []  # char artefact
    ],
    "Valfreya": [  # char
        "Valfreya",
        (
            "Une Valkirie envoyée prouver sa valeur dans le Coliseum après que Thor aie critiqué Odin pour s'entourer d'un harem de femmes inutiles au combat."
            "\n           Entre dans le Coliseum dans une envellope charnelle trop faible, en poussant un long soupir."
            "\n           On dit qu'elle aurait renversé un gobelet de bière sur le pantalon d'Odin il y a des millénaires de cela,"
            "\n           et que c'est pour ca qu'elle aurait été choisie."
        ),  # char
        "Manteau de Faucon",  # char stigma +
        "Ange Déchue",  # char stigma -
        "Faveurs d'Odin",  # char stigma *
        [
            "Attaque Légère",
        ],  # char list technic
        [],  # char list sorts
        {
            "Ambroisie": 10,
            "Hydromel": 10,
            "Fruit Jindagee": 10,
        },  # char dict of int items
        [
            "Affinitée de Foudre",
            "Affinitée de Glace",
            "Affinitée de Terre",
            "Affinitée de Sang",
            "Affinitée Physique",
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
        []  # char artefact
    ],
    "Bob": [  # char
        "Bob",
        (
            "Un pyrobarbare bruyant à l'allure fière, agent sur terre d'une ancienne divinitée du feu."
            "\n           Venu chercher la gloire a coup de hache, de feu, et de grands cris dans les couloirs du Coliseum."
            "\n           Que dire de plus ? Il est musculeux !"
        ),  # char
        "Ange de Feu",  # char stigma +
        "Fair Play",  # char stigma -
        "Musculeux",  # char stigma *
        ["Attaque Légère", "Bô Brulant"],  # char list technic
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
        ["Affinitée de Feu", "Pyrophile"],  # char list
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
        ["Grand Sac A Dos"]  # char artefact
    ],
    "Bob Doré": [  # char
        "Bob Doré",
        (
            "Un golem dorée représentant un pyrobarbare bruyant à l'allure fière."
            "\n           Venu tester les codes du Coliseum sans avoir a se taper 1h de gameplay a chaque fois."
            "\n           Que dire de plus ? Il est doré ! Bling-Bling !"
        ),  # char
        "Ange de Feu",  # char stigma +
        "Aucun, voyons",  # char stigma -
        "Musculeux",  # char stigma *
        ["Attaque Légère", "Bô Brulant"],  # char list technic
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
        ["Affinitée de Feu", "Pyrophile"],  # char list
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
        []  # char artefact
    ],
}
BIBLIOTHEQUEFINALE = {
    "The Presence": [
        "Its hands push at the seams\nLike a drowning animal\nTrying to get out from beneath\nBut the surface is of ice",
        "It can see the world outside\nHe's in a soon-to-be corpse\nKinda state, all the time,",
        "Born from the ripple in the laws\nUnder the shadow of the waves\nA parasite of untold years\nGrown around the noosphere",
        "Divine in shape, Devil in form\nDreaming the freedom his fate stole\nLurking right outside your mind\nBehind the art block you despise",
    ],
    "Analyse de la Réaction Chimique du Métamorphoseur Volcanique": [
        "L'échantillon de métamorphoseur volcanique, prélevé à une profondeur de 2000 mètres sous le cratère actif, présentait une composition minérale complexe.",
        "Lorsqu'il a été exposé à des conditions de température et de pression similaires à celles du milieu d'origine, une réaction exothermique s'est produite, accompagnée d'une émission de gaz.",
        "L'observation au microscope électronique a révélé des changements structuraux significatifs, avec la formation de cristaux de silicate à la surface de l'échantillon.",
        "L'analyse spectroscopique a identifié la présence de composés sulfurés dans les émanations gazeuses, suggérant une réaction catalytique impliquant des éléments volatils.",
        "Ces résultats suggèrent un mécanisme de transformation complexe impliquant des interactions entre les minéraux et les fluides magmatiques, ouvrant de nouvelles perspectives sur la compréhension des processus géochimiques dans les environnements volcaniques.",
    ],
    "Texte Incohérent": [
        "Le vent soufflait doucement à travers les arbres, caressant les feuilles "
        "et créant une symphonie apaisante.\n",
        "Les oiseaux chantaient leur mélodie matinale, remplissant l'air de leur "
        "joie contagieuse.\n",
        "Les nuages dérivaient paresseusement dans le ciel, prenant des formes "
        "fantaisistes et changeantes.\n",
        "Soudain, un lapin blanc surgit de derrière un buisson, agitant "
        "frénétiquement une montre de poche.\n",
        "Il sembla hésiter un instant, puis se précipita dans un terrier à "
        "proximité, disparaissant dans l'obscurité.\n",
        "Un sourire énigmatique se dessina sur le visage d'un chat rayé qui "
        "observait la scène, perché sur une branche basse.\n",
        "Il ouvrit la bouche pour dire quelque chose, mais aucun son ne sortit.\n",
        "Puis, réalisant qu'il était seul, il se mit à miauler de manière "
        "répétitive, comme s'il cherchait désespérément une réponse à une "
        "question invisible.\n",
        "La forêt écouta en silence, absorbant les bruits étranges qui "
        "remplissaient l'air.\n",
        "Finalement, le silence retomba, et la scène reprit son cours habituel, "
        "comme si rien d'étrange ne s'était jamais produit.",
    ],
    "Journal Personnel du Capitaine James Thompson, US Navy, 1943": [
        (
            "- 3 Juillet 1943 :\nLa tension est palpable à bord du navire. \nNous sommes en route vers la Méditerranée pour participer à l'opération Husky,"
            " le débarquement en Sicile. \nLes hommes sont nerveux, mais je dois rester fort pour maintenir la confiance de l'équipage. "
            "\nC'est une mission cruciale, et nous devons être prêts à affronter l'ennemi à tout moment."
        ),
        (
            "- 15 Juillet 1943 :\nL'opération Husky est lancée. \nLes premiers échanges de tirs avec les batteries côtières ennemies ont été intenses. "
            "\nNotre formation est sous un feu nourri, mais nos défenses tiennent bon. \nLes jeunes marins font preuve d'un courage admirable. \nJe suis fier de les commander."
        ),
        (
            "- 26 Juillet 1943 :\nAprès des jours de combats acharnés, la Sicile est enfin entre nos mains. \nLes sacrifices consentis ont été lourds,"
            " mais la victoire est notre. \nNous entamons maintenant des opérations de nettoyage et de sécurisation de l'île. \nC'est un soulagement de voir nos"
            " efforts porter leurs fruits, mais nous savons que de nouveaux défis nous attendent."
        ),
        (
            "- 5 Septembre 1943 :\nDes nouvelles choquantes nous parviennent du front. \nL'Italie a signé un armistice avec les Alliés."
            " \nC'est une tournure inattendue des événements, et cela change considérablement la dynamique du conflit en Méditerranée. "
            "\nNous devons rester vigilants et prêts à réagir à toute éventualité."
        ),
        (
            "- 18 Octobre 1943 :\nLes opérations de convoi dans l'Atlantique Nord deviennent de plus en plus périlleuses. "
            "\nLes attaques de sous-marins ennemis se multiplient, mettant en danger nos convois de ravitaillement essentiels. \nNous devons"
            " redoubler de vigilance et d'ingéniosité pour protéger nos navires contre cette menace sournoise."
        ),
        (
            "- 25 Décembre 1943 :\nNoël en mer est une expérience singulière. \nMalgré les conditions difficiles et l'éloignement de nos proches,"
            " l'esprit de camaraderie règne à bord. \nNous avons organisé une modeste célébration pour remonter le moral de l'équipage."
            " \nCes moments de répit sont rares, mais précieux."
        ),
    ],
    "Recettes Divines": [
        "Les meilleurs cookies du monde !\n\n300g Farine\n120g sucre semoule\n120g sucre cassonade\n6g levure\n1 oeuf\n175g beurre\n2 tablettes chocolats",
        "Mélanger farine, sucres semoule et cassonade, levure, chocolat.\nRajouter beurre fondu et oeuf",
        "Pétrir\nLaisser reposer 30 min au frigo",
        "10 minutes a 170°",
    ],
    "Naissance du Monde": [
        "Notre univers a été crée en deux temps par une force suprême, ou simplement par hasard.",
        "Qui, ou quoi, que ce soit, on a réussit a analyser le *fond sonore* de l'univers et a le comparer aux spectrographes de certains sorts.\nVoici ce que l'on a pu conclure :",
        "L'ordre naturel des choses, c'est a dire leur ordre de *naissance*, se base sur le temps, qui est une constante inéluctable présente bien avant le vide, au début de toute choses.",
        "Ainsi, on a pu construire le sceau (idéologique) des éléments, et les mettre a leur place, en commencant par le Divin, en haut, et en suivant le sens des aiguilles d'une montre.",
        "Ensuite, la vie est arrivée.\nSeule l'intention fait partie des éléments, car elle a une conscience superieure, indestructible mais très instable.\nC'est la raison pour laquelle on la laisse avec les éléments.",
        "Mais le reste de ce qui fait de nous, des êtres vivants, ne fait pas parti des éléments.\nCe sont des principes anarchiques, mais qui possèdent cepandant un ordre d'apparition, commencant par l'intention et continuant a l'inverse de l'ordre naturel des choses.",
        "En effet, si l'état normal de l'univers c'est la mort, alors la vie est a l'inverse de cet état normal et de ce qu'il le fait avancer : le temps.",
        "Cela voudrait il dire que la vie est la seule chose qui peut aller a l'encontre du temps ?\nDans ce cas, elle a peut etre existé avant tout le reste ?",
        "Cette question de savoir qui de la Vie ou de la Mort est arrivée en premier, c'est un problème qui élude depuis toujours les scientifiques.",
        "Je dirais cepandant que cette question n'a aucune importance.\nLes deux ont besoin l'un de l'autre pour interragir a notre niveau de réalité.",
    ],
    "Description d'une femme se levant": [
        "Dans une pièce baignée par la douce lumière du matin, une femme est "
        "assise dans un fauteuil rembourré de velours. Sa silhouette est définie "
        "par la clarté tamisée qui filtre à travers les rideaux, enveloppant la "
        "pièce d'une ambiance chaleureuse. Son visage, éclairé par les premiers "
        "rayons du soleil, révèle des traits délicats et une expression paisible, "
        "trahissant à la fois la quiétude du sommeil et l'anticipation d'une "
        "nouvelle journée.",
        "Lentement, elle glisse ses mains le long des accoudoirs du fauteuil, "
        "sentant la texture luxueuse du tissu sous ses doigts. Elle prend une "
        "profonde inspiration, remplissant ses poumons d'air frais matinal, et se "
        "redresse avec grâce. Ses muscles s'étirent paresseusement, comme si elle "
        "savourait chaque sensation de son corps en mouvement après une nuit de "
        "repos bien méritée.",
        "Ses pieds, chaussés de chaussons moelleux, rencontrent le sol avec une "
        "légèreté presque imperceptible. Elle se lève, dévoilant une silhouette "
        "élégante enveloppée dans une robe fluide qui glisse sur ses courbes avec "
        "fluidité. La lumière du matin danse sur le tissu, créant des motifs "
        "d'ombre et de lumière qui accentuent sa grâce naturelle.",
        "Un sourire doux se dessine sur ses lèvres alors qu'elle se tourne vers "
        "la fenêtre, accueillant pleinement les premiers rayons du soleil qui "
        "inondent la pièce. Prête à affronter les défis de la journée, elle quitte "
        "son fauteuil avec une assurance tranquille, prête à embrasser le monde "
        "qui l'attend à l'extérieur.",
    ],
    "Les Aventures de l'Explorateur Perdu": [
        "Le soleil brûlant battait implacablement sur le désert aride, faisant onduler l'air dans des mirages trompeurs.",
        "Parmi les dunes de sable doré, un explorateur solitaire avançait, son visage protégé par un voile contre les grains abrasifs.",
        "Des ruines anciennes surgissaient soudainement de l'horizon, témoins silencieux d'une civilisation disparue depuis des siècles.",
        "Les murmures du vent semblaient porter des histoires oubliées, évoquant les jours de gloire et de décadence de ce peuple autrefois prospère.",
        "Au cœur du temple effondré, une relique sacrée reposait, attendant d'être découverte par celui qui oserait défier les épreuves du désert.",
    ],
    "Foi": [
        "(le livre contient la phrase *Gary vous aime* en boucle.)",
    ],
    "Céleste": [
        "Madeline réouvra ses yeux.\nDevant elle se trouvait le directeur, sous une forme monstrueuse.\nCorrompu par son anxiété, ou peut être était-ce sa solitude ?",
        "Elle laissa ses questions sans réponses et se retourna.\nSur le toit de l'hotel, elle pouvait se déplacer jusqu'a l'autre coté sans se faire bloquer par les monticules de valises.",
        "C'était maintenant ou jamais.\nElle prit son élan et s'élanca dans les airs, avant de dasher sur une plateforme en contrebas.\nElle évita le directeur foncant sur elle, puis sauta sur le mur devant elle.",
        "Elle grimpa le mur et se mit a dasher vers le haut.",
        "Se prenant ainsi un ennemi en pleine tronche.",
    ],
    "Analyse du Monstre Trienun et de son Pouvoir de Manifestation du Bandit Manchot": [
        (
            "- Origine et Caractéristiques Physiques :\nLe monstre Trienun, découvert dans une région isolée des montagnes, présente une apparence reptilienne unique avec des écailles iridescentes"
            " et des cornes acérées. Sa silhouette imposante mesure environ 3 mètres de haut et est dotée de membres puissants, lui conférant une agilité remarquable malgré sa taille. Les analyses "
            "anatomiques révèlent une constitution robuste et une capacité de régénération cellulaire accélérée, caractéristiques communes aux prédateurs de haut niveau."
        ),
        (
            "- Capacité de Manifestation du Bandit Manchot :\nTrienun démontre une aptitude extraordinaire à invoquer un Bandit Manchot, un dispositif semblable à ceux utilisés dans les casinos,"
            " mais modifié pour des desseins mystérieux. Lorsque le Bandit Manchot est activé, il génère une combinaison aléatoire de symboles élémentaires. Ces symboles déterminent les effets"
            " élémentaires infligés aux individus à proximité de Trienun."
        ),
        (
            "- Effets Élémentaires :\nSelon les symboles arrêtés sur le Bandit Manchot, différents effets élémentaires sont observés chez les individus environnants :\n  - Symbole de glace : Les "
            "sujets sont enveloppés dans un halo de gel, provoquant une sensation de froid intense et des engourdissements.\n  - Symbole de feu : Des flammes émergent brusquement autour des cibles,"
            " leur infligeant des brûlures sévères.\n  - Symbole de foudre : Des décharges électriques parcourent le corps des sujets, entraînant des spasmes musculaires et des dommages nerveux.\n "
            " - Symbole de terre : Des éclats de roche et de terre se matérialisent, projetant les individus au sol avec force.\n  - Symbole d'eau : Une vague d'eau puissante submerge les cibles, "
            "les entraînant dans un tourbillon aquatique."
        ),
        (
            "- Conclusion :\nLe pouvoir de manifestation du Bandit Manchot par Trienun représente une capacité extraordinaire qui combine la manipulation d'énergies élémentaires et des phénomènes"
            " de chance aléatoires. Cette capacité soulève des questions fascinantes sur l'origine et la nature profonde de Trienun, ainsi que sur les implications de son existence pour notre "
            "compréhension de la magie et de l'énergie dans notre monde."
        ),
    ],
    "Kya-san loves me ??! Chapitre 6534": [
        "Le soleil couchant teintait le ciel de nuances chaudes, créant une "
        "toile de fond parfaite pour ce moment tendu entre les deux amoureux.\n",
        "Ils se tenaient face à face, à quelques centimètres l'un de l'autre, "
        "captivés par l'intensité du moment.\n",
        "Chaque détail de l'autre semblait amplifié par l'excitation et "
        "l'anticipation qui imprégnaient l'air.\n",
        "Leurs regards se croisèrent, et dans les yeux de chacun, on pouvait "
        "voir la profondeur de leurs émotions.\n",
        "Un frisson électrique parcourut leur peau au moindre contact, comme si "
        "l'air lui-même vibrait d'une énergie palpable.\n",
        "Leurs cœurs battaient à l'unisson, rythmant le tempo de ce moment "
        "suspendu dans le temps.\n",
        "Leurs mains, presque instinctivement, se tendirent l'une vers l'autre, "
        "attirées par une force magnétique irrésistible.\n",
        "Les doigts effleurèrent à peine, créant une sensation de chaleur qui se "
        "propagea à travers leurs corps.\n",
        "Chaque souffle était lourd de désir, emplissant l'espace entre eux "
        "d'une tension presque palpable.\n",
        "Ils se rapprochèrent lentement, leurs respirations se mêlant dans un "
        "doux ballet synchronisé.\n",
        "Leurs lèvres étaient si proches qu'ils pouvaient presque sentir le "
        "frisson d'anticipation parcourir leur peau.\n",
        "Le monde entier semblait s'effacer autour d'eux, ne laissant place "
        "qu'à l'autre et à cette connexion électrique qui les liait.",
        "Leurs lèvres se rapprochèrent, leurs yeux se fermèrent, ils pensèrent a "
        "tout ce qu'ils avaient traversé ensemble, prêt a oficialiser leur "
        "union en scellant leur désirs par leur premier baiser, tant attendu.",
        "Quelques millimètres, quelques centièmes de secondes, séparaient les deux amoureux de leur destin, et",
        "(Le livre s'arrête la.)",
    ],
    "Lettre d'Amour": [
        (
            "(nombre de cartes) (numéro de la carte) (nom du pouvoir) (effet du pouvoir)\n(5)1 et joker:fou: devinez la carte d'un type. Si vous reeussisez il meurt "
            "(sauf si c'est un autre fou) \n(4)2:chevalier: voir la carte de l'autre\n(4)3:tour: comparer sa carte avec celle de l'autre. La plus petite carte perd\n"
            "(3)4:la dame: vous protège de tout les cartes pendant un tours\n(3)5:scribe:fait poser la carte de quelqu'un \n(2)6:sorcier: échange sa carte avec celle "
            "d'un autre\n(2)7:Le chasseur: Annonce deux nombres. Ceux qui possèdent une carte dont la valeur se situe entre les deux nombres (ou est égale à l'un des "
            "nombres) doivent lever la main.\n(3)8:la servante: fais passer le tour de quelqu'un ou change le sens du jeu\n(1)9:magistrat: si en additionnant vos 2 cartes "
            "ça fait 15 ou + vous mourrez\n(1)10:la princesse:si vous posez cette carte vous mourrez (même par le scribe) \n(1)valet:le bourreau : désigne une personne. "
            "Si la personne a une carte avec un nombre pair, il meurt. \n(1)dame:l'imperatrice: permet de gagner de tromper la mort une seule fois (gagne une vie qui dure "
            "jusqu'à la fin de la partie)\n(1)roi :enfant empereur: aucun effet. Mais quand on l'a, on doit la poser la carte face retournée sur le front pour que tout le"
            "monde la voie."
        ),
        "A chaque tour, les joueurs prennent une carte, et en jettent une.\nLe pouvoir de la carte jetée s'active.\nLe jeu continue jusqu'a ce qu'il n'y aie plus qu'une personne.\nSi il n'y a plus qu'une seule carte, c'est celui qui a la plus grande carte qui gagne.",
    ],
    "Les Secrets du Manoir Hanté": [
        "La nuit était tombée sur le vieux manoir, enveloppant ses murs de mystère et de silence.",
        "À travers les fenêtres poussiéreuses, la lueur de la lune révélait des ombres dansantes, semblant murmurer des secrets oubliés.",
        "Au détour d'un couloir sombre, une porte grinça sinistrement, révélant une pièce plongée dans l'obscurité.",
        "Des échos lointains semblaient résonner dans les murs, comme si les pierres elles-mêmes avaient une histoire à raconter.",
        "Dans un coin obscur de la pièce, une vieille malle en bois renfermait des artefacts anciens, témoins silencieux des événements passés.",
    ],
    "Confession d'une Horreur des Abysses": [
        "Mon esprit est pareil au mouvement d'une rocking chair\nPensées tantôt sombre tantôt claires, quel enfer\nAucune constance, tout dans l'original",
        "Je m'attaque à la vie comme un homme de Néandertal \nArmé de mots, d'expérience , et d'un mental de fer\nD'un humour de bout d'chandelle trempé dans vie amère",
        "Je regarde les étoiles briller et vit au travers\nLes histoires des hommes passionné sont mes plus beau salaires\nRongé, le vide se sert sur mon corps",
        "Prend l'amour et la haine,et la rancoeur et la mort\nEntre ses ongles , ma peau fatiguée s'orne\nDes griffures sur mes poignets , je sens couler l'ychor ",
    ],
    "Rapport : Mirroir de Culte": [
        "L'appelation *Miroir de Culte* désigne un miroir rectangulaire mesurant approximativement 47 cm par 43 cm.\nLa bordure de ce miroir est encadrée par les vertèbres de quatre individus supposés être"
        "les membres fondateurs d'un culte de petite taille connu sous le nom de l'Ordre du Reflet.",
        "Le *Miroir de Culte* possède un léger effet de danger-cognitif contraignant les individus à éprouver une dévotion religieuse directe envers le *Miroir de Culte*.\nLa"
        " nature de cette dévotion varie en fonction des individus, sa manifestation étant basée sur leurs notions préconçues de la prière, du culte et"
        " d'autres activités connexes. \nCet effet augmente proportionnellement en fonction du temps que l'individu passe en présence du *Miroir de Culte*. \nCependant"
        ", un déni actif de la croyance en le *Miroir de Culte* semble empêcher cet effet, et l'administration d'amnésiques s'est montrée efficace pour inverser toute modification"
        " psychologique de long terme.",
        "Les individus regardant le *Miroir de Culte* en exprimant activement une dévotion religieuse rapportent voir une entité non identifiée à la place de leur reflet. "
        "\nLa caractérisation de cette anomalie est décrite comme une fusion des diverses conceptions du divin de l'adorateur. \nL'entité semble se nourrir de"
        " la dévotion religieuse qu'elle reçoit, exprimant des motivations entièrement déterminées par l'intention du culte qui lui est voué et disposant de "
        "capacités de pliage de réalité qui s'accroîent proportionnellement en fonction de la quantité nette de cette adoration. Aucune limite supérieure de "
        "ces capacités n'a pour l'instant été déterminée.",
    ],
    "Moi et mes Barils": [
        "Les barils. Ce ne sont pas juste des contenants. Ils ont une histoire riche.",
        "Certains barils étaient utilisés pour transporter du poisson, du hareng plus précisément.",
        "D'autres, de la mélasse. Ce qui, comme nous le savons tous, a été la chute de l'administration Coolidge.",
        "Il ne l'a pas vu venir, mais c'est arrivé. Ne laissez pas cela vous arriver.",
        "En conclusion, la prochaine fois que vous verrez un baril, pensez à ceci : Qu'est-ce qu'il contient ?",
        "Ce n'est ni du poisson ni de la mélasse. C'est du savoir. Et c'est le plus grand trésor de tous.",
        "Et ce n'est que le début. Les Romains utilisaient des barils pour transporter de l'huile d'olive.",
        "Les Celtes, de la bière. Et oui, même l'homme lui-même.",
        "L'homme, qui est sorti de l'océan et s'est dressé pour la première fois, l'a fait près d'un baril.",
        "J'ai toujours eu une préférence pour l'histoire de Sir Francis Drake qui a fait le tour du monde.",
        "Savez-vous comment il a empêché ses hommes de mourir du scorbut ? Des barils. Pleins de bière.",
        "Alors levons nos barils à Sir Francis Drake et à tous les explorateurs marins qui ont suivi.",
        "Des Vikings à Marco Polo en passant par Magellan.",
        "Et s'ils étaient là aujourd'hui, j'aimerais penser qu'ils lèveraient tous une pinte en mon honneur.",
        "À l'avenir !",
    ],
    "Cigogne Rouge": [
        "Extrait",
        "Extrait",
        "Extrait",
    ],
    "La Métaphysique Quantique Très Sérieuse": [
        "Karakai Jouzu No (Moto) Takagi-San\nKarakai Jouzu No Takagi-San\nBoku No Kanojo Ga Majime Sugiru Shojo Bitch Na Ken\nFechippuru ~Our Innocent Love~",
        "We Never Learn\nKakkou No Linazuke\nOnizuka-Chan And Sawarida-Kun\nSeishun Buta Yarou Wa Bunny Girl Senpai No Yume Wo Minai",
        "Komi-San Wa Komyushou Desu\nKubo san wa Boku\nUzaki-Chan Wa Asobitai!\nZutto Otokonoko da to Omotte ita Gakitaishou ga Onnanoko deshita",
        "Manga Sakourasou No Pet Na Kanojo\nDo chokkyuu kareshi x kanojo\nMaou no ore GA dorei elf Wo home ni shitanda GA d'où medereba li",
        "(La liste de noms de mangas de romance continue sur 463 pages.)",
    ],
    "Analyse du Mana : Une Étude des Principes Fondamentaux de l'Énergie Magique": [
        (
            "- Nature du Mana :\nLe mana est une forme d'énergie magique omniprésente dans l'univers, perceptible mais insaisissable pour la plupart des individus."
            " Il réside dans les flux éthérés qui traversent le monde et peut être canalisé par ceux qui maîtrisent les arts de la magie."
        ),
        (
            "- Intention et Concentration :\nL'utilisation efficace du mana repose sur l'intention et la concentration de l'utilisateur. L'intention détermine le but de l'acte magique,"
            " tandis que la concentration permet de canaliser le mana avec précision vers cet objectif. Une intention claire et une concentration soutenue sont essentielles pour obtenir"
            " des résultats magiques cohérents et puissants."
        ),
        (
            "- Utilisation du Mana :\nUne fois canalisé, le mana peut être utilisé pour réaliser une variété d'effets magiques, allant de simples sortilèges à des rituels complexes."
            " La nature et l'étendue de ces effets dépendent de plusieurs facteurs, notamment la quantité de mana disponible, la compétence de l'utilisateur et la spécificité de l'intention."
        ),
        (
            "- Réservoir de Mana :\nLe mana peut être stocké dans un réservoir personnel, souvent situé à l'intérieur de l'individu pratiquant la magie. Ce réservoir agit comme une"
            " réserve d'énergie magique, permettant à l'utilisateur d'accéder au mana quand il en a besoin. La capacité du réservoir varie d'un individu à l'autre et peut être augmentée"
            " par des techniques d'entraînement magique."
        ),
        (
            "- Absorption du Mana :\nEn plus d'être stocké dans un réservoir interne, le mana peut être absorbé de différentes sources externes, telles que des cristaux magiques,"
            " des artefacts enchantés ou même l'énergie environnante. L'absorption du mana nécessite souvent une connexion mentale et spirituelle avec la source, ainsi qu'une compréhension"
            " profonde des flux énergétiques."
        ),
        (
            "- Conclusion :\nLe mana représente une force vitale dans la pratique de la magie, reliant l'intention de l'utilisateur à la réalité de ses manifestations."
            " Comprendre ses principes fondamentaux d'intention, de concentration, d'utilisation, de réservoir et d'absorption est essentiel pour tout praticien de la magie"
            " souhaitant maîtriser cette énergie mystique et puissante."
        ),
    ],
    "Comprendre la Noosphère": [
        (
            "La noosphère est un concept philosophique et scientifique introduit par le théologien et philosophe français Pierre Teilhard"
            " de Chardin dans les années 1920.\nIl décrit la sphère de la pensée humaine et de la conscience collective qui englobe la biosphère"
            " (l'environnement biologique de la Terre).\nSelon Teilhard de Chardin, la noosphère est le stade ultime de l'évolution terrestre,"
            " où la pensée et la conscience deviennent des forces dominantes et où l'humanité est interconnectée à un niveau global par le biais"
            " de la communication et de la technologie.\nC'est une notion qui englobe les idées de conscience collective, d'interconnexion et de transformation sociale et spirituelle."
        ),
        "Testez votre connexion avec la conscience collective théorisée par Pierre avec ces nombres !\nSi vous n'êtes d'accord avec aucune de ces associations, alors il avait peut etre tort...",
        "Mortalité : 11 (stabilité, temporaire)",
        "Étoile : 12 (guidance, illumination)" "Positif : 9 (passion, transformation)",
        "Négatif : 2 (froid, dualité)",
        "Intention : 7 (spiritualité, introspection)",
        "Energie : 3 (mouvement, émotion)",
        "Masse : 1 (individualité, manifestation physique)",
        "Ciel : 8 (expansion, vision)",
        "Divin : 5 (omniscient, innaretable)",
        "Forêt : 10 (abondance, mystère)",
        "Vent : 6 (liberté, changement)",
        "Chaleur : 4 (vitalité, lien familial)",
    ],
    "Cette fois-ci je vais réussir !": [
        "Réaction= le temps que l'info arrive a mon cerveau (dizaine de la vitesse x3)\nFreinage= force cinétique, le temps que les freins fassent effet (dizaine de la vitesse au carre)",
        (
            "Arrêt: réaction +freinage\nautoroute: voie de droite est pour poids lourds et véhicules a -  de 60kmh\nBcp d'infraction: 8points max.\n1 infraction: 6 points max"
            "Taux alcoolémie + = 6 points\nQuand QQ veut se mettre alors qu'il a pas la prio, change de voie\nRègle générale: 0,50"
        ),
        "Proba: 0,20\nEthylotest de marché:  pour probatoire et débutants\nQuand on rétrograde, faire attention au surégime. Ne pas rétrograder a tout bout de champ.\nRefus de prio a un piéton: amande et -4 points",
        "(Le reste du livre est composé de notes sur le code de la route.)\n(La plupart sont évidentes, certaines sont fausses.)",
    ],
    "Les Échos du Temps": [
        "L'épais brouillard enveloppait la forêt de ses tentacules opaques, étouffant les bruits du monde extérieur.",
        "Entre les arbres tordus et les buissons épais, une silhouette solitaire se fraya un chemin, ses pas écrasant les feuilles mortes sous ses bottes.",
        "Le poids de l'obscurité était palpable, mais quelque chose dans l'air semblait annoncer un changement imminent.",
        "Les murmures lointains des ancêtres semblaient résonner à travers les arbres, comme des échos du passé, appelant à la mémoire des temps oubliés.",
        "Au cœur de cette clairière oubliée, une lueur faible émergeait, éclairant un objet mystérieux enfoui dans le sol depuis des siècles.",
    ],
    "Mémoires de Géologue": [
        "Les montagnes verdoyantes se perdent dans les barres brumeuse, se mouvant tel des cavaliers de l'éther affrontant l'éphémère de leur existance.",
        "Ça et la, le ciel saigne des mares de lumières et de bleu, répondant aux arbres teintés de jai et d'ecrin. ",
        "Et au milieu de ce spectacle de couleurs...",
        "...nous on prend des notes sous la flotte.",
    ],
    "Havre : Rapport": [
        "*Havre* est la désignation provisoire de la dimension 882R53, un plan extradimensionnel de taille inconnue. "
        "\nLe *Havre* a l'apparence d'un désert de sel à la surface solide avec une réflectivité quasi parfaite. "
        "\nIl a été remarqué que la surface a également un goût salé.",
        "Les entités à l'intérieur du *Havre* ne semblent pas souffrir d'une quelconque forme de perte énergétique ni de décomposition,"
        " puisque plusieurs appareils électroniques introduits dans le *Havre* fonctionnent continuellement depuis au moins 296 561 années sans défaillance,"
        " et que les personnes à l'intérieur ne semblent pas vieillir ni avoir besoin de se nourrir, ce qui les rend biologiquement immortelles.",
        "Le *Havre* est entièrement monotone, à l'exception d'un unique arbre (désigné *Havre:Arbre* ci-après) comportant un danger-sensitif :"
        " l'observateur est toujours conscient de sa localisation, peu importe la distance ou la visibilité.",
        "Le corps du Dr Charles Gears a été découvert affaissé contre la base de *Havre:Arbre*. \nLa date de la dernière mise"
        " à jour de ce document, ainsi que le rapport d'autopsie et les 1 779 095 vidéos retrouvées sur son lecteur indiquent "
        "qu'il est mort à l'âge d'environ 450 000 ans de causes naturelles.",
    ],
}
LISTEEFFETSARTEFACT = {
    "Graine de Grenade": {"Commentaire": "Cette graine d'un fruit apprécié des dieux augmente votre vitalité.",
                           "Vie": 15},  # vie t
    "Fiole d'Eau du Styx": {"Commentaire": "Cette fiole imprégnée de l'essence des morts augmente votre réservoir de mana.",
                             "Mana": 15},  # mana t
    "Aile de Cire d'Icare": {"Commentaire": "Ce bout du chef d'oeuvre de Dédale augmente votre capacité a esquiver les attaques.",
                              "Taux esquive": 6},  # esquive t
    "Griffe de Lion": {"Commentaire": "Cette griffe contient l'essence d'une bête féroce abattue par le Roi Singe, et augmente votre attaque.",
                        "Attaque": 4},  # attaque t
    "Statue d'Angerona": {"Commentaire": "Angerona, la déesse de la Concentration, veille sur tout ses fidèles, et vous octroie la vue qui discerne les faiblesses.",
                           "Taux coup critique": 6, "Taux sort critique": 6},  # taux critique t
    "Collier de Mithril": {"Commentaire": "Ce collier est le tout premier artefact crée par les tout premiers nains, pour résister aux attaques des tout premiers monstres pendant l'Age du Chaos.",
                            "Defence": 4},  # defence t
    "Elixir du Sage": {"Commentaire": "Cette bouteille contient toutes les réalisations du doyen de la Grande Bibliothèque d'Alexandrie, sous forme liquide.",
                        "Intelligence": 4},  # intelligence
    "Petite Pierre Philosophale": {"Commentaire": "Ce prototype permet de transmuter une quantitée limitée de choses en or.",
                                    "Gold": 1000},  # gold t
    "Anneau Cramoisi": {"Commentaire": "Cet anneau forgé pendant la Guerre de l'Interdit a bu le sang de nombreux dieux et déesses afin de conferer leur endurance a son porteur.",
                         "Endurance": 20},  # endurance t
    "Orbe de Disruption": {
        "Commentaire": "Cet orbe vient de l'Ains Terra Net, le monde des voyageurs, et perturbe le mana environnant.\nLes monstres avec un réservoir de mana brisé perdent 10 pv supplémentaires par tour !",
    },  # degat quand ennemi plus mana
    "Plume de Munin": {"Commentaire": "Cette plume vient de Munin, un des corbeaux d'Odin qui voyage a travers les neufs mondes, et confère a son porteur une certaine aisance a esquiver les attaques.",
                        "Taux esquive": 6},  # esquive t
    "Collier des Brísingar": {"Commentaire": "Ce collier porté par Freya élève le corps et son réservoir de mana a une condition optimale pour le rendre plus charismatique.",
                               "Vie": 8, "Mana": 8},  # vie et mana t
    "Draupnir": {"Commentaire": "D'après les légendes, cet anneau est sensé se multiplier par 9 toute les 9 nuits.\nIl n'a pas l'air de réagir pour le moment..."},  # gold t
    "Magatama": {
        "Commentaire": "Cette perle passée de générations en générations par les plus grands empereurs du monde contient une partie de leur âme et confère a son porteur de multiple augmentations.",
        "Attaque": 2, "Defence": 2, "Intelligence": 2, "Vie": 4, "Mana": 4, "Endurance": 5
    },  # attaque, intelligence, defence, vie, mana, endurance
    "Voile de Ino": {"Commentaire": "Le voile porté brièvement par Ulysse, et qui protege des attaques (permanent) et de la mort (une seule fois).",
                     "Defence": 2},  # defence t
    "Megingjord": {"Commentaire": "La ceinture de Thor qui lui donne une grande puissance pendant les moments critiques, ainsi que la capacité de soulever son marteau.",
                    "Degat coup critique": 10, "Degat sort critique": 10},  # degat critiques t
    "Manne Céleste": {"Commentaire": "La seule source de nourriture des hébreux pendant 40 ans, gracieusement offerte par le Ciel, et qui leur a permit de marcher jusqu'a trouver leur terre d'adoption.",
                       "Endurance": 10, "Vie": 10},  # endurance + vie t
    "Nœud Gordien": {"Commentaire": "Le cordage compliqué défait seulement par le Maitre de l'Asie, mais finalement tranché par Alexandre le Grand, et qui a gardé depuis une partie de sa force.",
                      "Attaque": 4},  # attaque t
    "Don de Terre": {"Commentaire": "Un simple sac contenant les Redcoins d'une divinité de la Terre.",
                      "Red coin": 2},  # donne redcoin
    "Don de Foudre": {"Commentaire": "Un simple sac contenant les Redcoins d'une divinité de la Foudre.",
                      "Red coin": 2},  # donne redcoin
    "Don de Feu": {"Commentaire": "Un simple sac contenant les Redcoins d'une divinité du Feu.",
                      "Red coin": 2},  # donne redcoin
    "Don de Glace": {"Commentaire": "Un simple sac contenant les Redcoins d'une divinité de Glace.",
                      "Red coin": 2},  # donne redcoin
    "Don Sanguin": {"Commentaire": "Un simple sac contenant les Redcoins d'une divinité de Sang.",
                      "Red coin": 2},  # donne redcoin
    "Don Physique": {"Commentaire": "Un simple sac contenant les Redcoins d'une divinité de l'Effort.",
                      "Red coin": 2},  # donne redcoin
    "Don Astral": {"Commentaire": "Un simple sac contenant les Redcoins d'une divinité de l'Ame.",
                      "Red coin": 2},  # donne redcoin
    "Nimbe Divine": {"Commentaire": "Un cadeau des dieux symbolisant la divinité et la sacralité de ceux qui ont accomplit de grandes choses.",
                      "Intelligence": 4},  # intelligence t
    "Couronne Sacrée": {
        "Commentaire": "La Couronne d'Epine de Jésus, un symbole absolu de dévotion, l'incarnation de l'esprit au dessus du corps.\nVos points d'endurance peuvent maintenant aller dans le négatif."
    },  # endurance peut aller dans le négatifs
    "Gant de Midas": {
        "Commentaire": "Le gant isolant d'un roi de Phrygie qui transformait tout ce qu'il touche en or.\nRéagit à la magie dans un crystal élémentaire pour enlever l'altération d'état [Gelure]."
    },  # enleve la gelure quand utilise un crystal élémentaire
    "Gant d'Héphaïstos": {
        "Commentaire": "Le gant isolant d'un dieu des Arts de la Forge.\nRéagit à la magie dans un crystal élémentaire pour enlever l'altération d'état [Brulure]."
    },  # enleve la brulure quand utilise un crystal élémentaire
    "Plaquette du Souvenir": {
        "Commentaire": "Une plaquette sur laquelle sont inscrites les postures d'une ancienne version de l'attaque légère, trop forte pour son propre bien.\nL'Attaque Légère fait maintenant bien plus de dégâts."
    },  # degats de l'attaque légère * 3
    "Monocle de Vérité": {
        "Commentaire": "Une race de servants royaux travaillant dans l'ombre, surentrainés, et massacrés par leurs maitres apeurés.\nCe bijou magique né de leur torture vous fait trouver 5 golds par nouvelle salle observée (incompatible avec le Schmilblick.)"
    },  # gagne 5 gold quand observe salle
    "Sabre du Roi de Glace": {
        "Commentaire": "Un bout de glace a moitié fondu, ayant appartenu a un Roi reposant dans sa tombe, inutilisable en combat.\nSa magie vous protège cepandant des pièges."
    },  # immunisé face aux pièges
    "Bocle de Philoctète": {
        "Commentaire": "Un petit bouclier a fixer au niveau de la paume, ayant appartenu a un faiseur de légende.\nVotre défence augmente encore plus lorsque vous vous protégez."
    },  # defence quand se protege * 1.5
    "Ecaille d'Ouroboros": {
        "Commentaire": "L'écaille d'un divin serpant signifiant le renouveau et l'infini.\nVous regagnez 2 points de vie a chaque utilisation de sorts."
    },  # Rend 2 pv par utilisation de sort
    "Serment d'Heimdall": {
        "Commentaire": "La marque du serment d'un dieu omniscient envers le peuple qui a continué a le prier dans le pire des moments.\nIl y a de très faibles chance qu'un sort utilise le mana de quelqu'un d'autre au lieu du votre."
    },  # 3% de chance de ne pas utiliser de mana quand jette un sort
    "Masque d'Oblivion": {
        "Commentaire": "Un masque blanc, sans expressions, qui semble faire oublier la présence même de son porteur.\nLa fuite d'un combat normal est garantie."
    },  # fuite garantie
    "Chapelet de Moine": {
        "Commentaire": "Le chapelet ayant appartenu a un pelerin faisant route vers l'Ouest, accompagné d'un roi singe, un porc-démon, et un moine de sable.\nVous gagnez l'altération d'état [Béni] après avoir passé votre tour. La prochaine attaque sera alors critique."
    },  # beni quand on passe son tour
    "Oeuil de Phénix": {
        "Commentaire": "Une gemme représentant l'oeil d'un phénix, dans lequel on peut voir une tempête de feu noir figée.\nVous reprenez tout vos points de mana lors d'une résurrection."
    },  # Reprend 100% mana quand resurection
    "Echarde de Pinocchio": {
        "Commentaire": "Un éclat de la poupée de bois qui trompe la réalitée elle même avec ses mensonges.\nVous avez une très très faible chance de revenir a la vie lorsque vous mourrez, même sans objet pour."
    },  # Faible pourcentage de chance de ne pas mourir
    "Voeu Cristallisé": {
        "Commentaire": "La forme cristallisée du voeu du plus monstreux des hommes qui n'a formulé qu'une seule demande au génie en face de lui : Devenir une meilleure personne.\nVotre stigma négatif disparait a son contact."
    },  # Efface le stigma négatif
    "Haricot Magique": {
        "Commentaire": "La graine d'une plante monstreuse amenant son planteur dans une dimension remplie de ses semblables, affamés et en manque de nutriments, cachée dans les nuages.\nSes racines tentaculaires cherchant le sang ne peuvent être stoppées que par une lame plantée dans la graine originelle.\nInvoque des roches depuis sa dimension d'origine, augmentant les dégâts de l'effet [Lapidation]."
    },  # 20% de degats supplémentaires par lapidation
    "Miette de Pain Congelée": {
        "Commentaire": "Les seules traces d'enfants emmenés dans les sombres forêts du continent pour y être perdus par leurs parents en manque d'argent.\nLa rancoeur d'âmes pures englouties par ce qui se cache dans les bois fait durer l'altération d'état [Gelure] pendant 2 tours supplémentaires."
    },  # gelure reste 2 tours de plus
    "Chaperon Rouge": {
        "Commentaire": "Un vêtement traditionnel médiéval, dont l'interieur est marqués de profondes griffures.\nRéduit le cout en vie des techniques lorsque vous êtes sous l'effet de altération d'état [Blessé]."
    },  # Cout en vie reduit quad on est blessé
    "Morceau de Plomb": {
        "Commentaire": "Un morceau de plomb en forme de goutte, appartenant a un soldat de plomb lancé dans les braises du feu qui a brulé son amante : une danseuse de papier.\nLes échos de l'amour profond qu'il a ressenti dans ses derniers moments aident a rester concentré, et réduit le malus de mana de l'altération d'état [Déconcentré]."
    },  # Cout en mana reduit quand déconcentré
    "Bague de l'Âne": {
        "Commentaire": "La bague d'une princesse fiancée a son propre père a son insu, que ce dernier a pu reconnaitre avant de finaliser l'union incestueuse.\nVos pensées s'éclaircissent lorsque vous tenez l'anneau, et l'altération d'état [Confus] ne vous affecte plus."
    },  # Confusion s'arrete en 1 tour
    "Pièce Fondue": {
        "Commentaire": ("Une pièce de monnaie représentant la vengeance, maudissant les ennemis de son porteur."
                    "\nLes coups critiques maudissent les ennemis, les ennemis maudits perdent 2 pm par tour.")
    },
    "Tiare de Suie": {
        "Commentaire": ("Un bibelot vénéré par un clan de voleur, porté par sa dernière cheffe pendant un régicide."
                    "\nAccorde la bénédiction du feu sacré a son porteur pour chaque coups esquivés.")
    },
    "Chaine de Main": {
        "Commentaire": ("Un bijou magique qui se porte au niveau des mains, et qui transforme une prothèse en véritable main connectée au système nerveux."
                    "\nLes sorts critiques font deux fois plus de dégâts.")
    },
    "Larme d'Yggdrasil": {
        "Commentaire": ("Une perle de sève venant d'un arbre magestueux qui communique une grande tristesse a ceux qui dorment sous ses branches."
                    "\nEn combat, les feuilles et fruits Jindagee et Aatma durent 2 fois plus longtemps")
    },
    "Collier de Nephilim": {
        "Commentaire": ("Un artefact témoignant de l'amour entre un paysant devenu démon et une papesse devenue ange, laissée a leur enfant avant de mourir."
                    "\nRecouvrir des pm permet de recouvrir des pv, avec un ratio 2/1 (2pm regagnés ==) 1 pv regagné en plus)")
    },
    "Cape Victorieuse": {
        "Commentaire": ("Une cape macabre cousue avec les fils d'un drapeau pirate et les ailes du Ministre du Mana."
                    "\nChaque ennemi tué augmente de 0.5% les dégâts totaux.")
    },
    "Schmilblick": {
        "Commentaire": ("Un bidule bizarre crée par une inventrice farfelue."
                    "\nA l'entrée d'un nouvel étage, toutes ses salles sont directement dessinées sur la carte (annule les effets du Monocle de Vérité)")
    },
    "Contrat de Travail": {
        "Commentaire": ("Un bout de papier promettant la puissance aux économes afin qu'ils ne se fassent plus martyriser par le système."
                    "\nVous gagnez 2% de dégâts totaux supplementaire par paquets de 50 pièces possédé.")
    },
    "Dessin Nostalgique": {
        "Commentaire": ("Un dessin au charbon d'un vieil homme en plein sommeil, adossé contre une louve."
                    "\nPasser son tour donne l'altération d'état *Concentration* pendant 2 tours, qui réduit le nombre de pm nécéssaire pour chaque sorts.")
    },
    "Vide Interieur": {
        "Commentaire": ("Un sentiment de malaise, comme si vous étiez passé a coté de quelque chose, et que votre aventure avec ce personnage n'a pas livré tout ses secrets."
                    "\nEnlève le stigma négatif [Incontrollable], ainsi que 15 points de mana maximum.")
    },
    "Badge Terni": {
        "Commentaire": ("Un morceau de métal terni par le temps, les éléments, et les tentations, mais qui reste solide et droit."
                    "\nRéduit les prix du marchand de 30%, lorsque il ne reste plus d'ennemis a affronter dans l'arène de l'étage en cours (boss compris).")
    },
    "Perle de Pluie": {
        "Commentaire": ("Un crystal serein, symbole de la libération des chaines de l'esprit."
                    "\nChance de faire un sort critique : +33%."),
                    "Taux sort critique": 33
    },
    "Syra": {
        "Commentaire": ("Une verre divin de lait fermenté apprécié par un certain dieu nordique jeté hors de son throne par une ""valkyrie inutile au combat""."
                    "\nLes nouvelles techniques apprises donnent 10pm max supplémentaires."
                    "\nLes nouveaux sorts appris donnent 10pv max supplémentaires.")
    },
    "Pin's Extincteur": {
        "Commentaire": ("Un joli pin's a accrocher sur un vêtement, représentant un extincteur rouge."
                    "\nLorsque l'effet Brulûre se termine, redonne 10pv et 10pm.")
    },
    "Bandeau Teinté": {
        "Commentaire": ("Une relique de Thémis, l'esprit de la Justice, marqué d'un curieux éclat doré."
                        "\nEn combat, vous gagnez 1 pièce a chaque tours.")
    },          
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
    "Sillages Sur Une Mer de Rêves",
    "Pluie d'Automne",
    "Bêtise Humaine",
    "Exploratio",
    "Les Joies du Combat",
    "Revenant",
    "Conte de Fée",
    "Epineuses Rencontres",
    "Le Chevalier Qu'on Ne Veut Pas Rencontrer",
    "Affreux Fertile",
    "Clair de Sang",
    "Néophobie Alimentaire",
    "Ruines d'Antan",
    "Sables Mouvants",
    "Euthanasie Régalienne",
    "Pareísaktos",
    "Pāramitā",
    "Nerd Party",
    "Jeux d'Enfants",
    "Pantomime",
    "Carnaval",
    "Fièvre du Samedi Soir",
    "Piñata",
    "Tragicomique",
    "Combler les Vides",
    "Systèmes Défaillants",
    "Sa Majesté Des Mouches",
    "Divin Karma",
    "Folie Furieuse",
    "Comment Tuer le Grand Méchant Loup",
    "Ossuaire Immaculé",
    "Dissonance Cognitive",
    "Faux Semblants",
    "La Hache et le Grimoire",
    "Gr4c1euse Nécr0log1e",
    "Plum5 d'0ie",
    "Pr0s0pagn0sie",
    "Mach1n3 Inf3rn4le",
    "S1mul4crum",
    "V3tus S4nct0rum",
    "Cruc1fix1on",
    "Réarr4ng3ment L1m1nal",
    "4rythm1e",
    "Au Dé7our D’un S3nti3r Une Ch4rogn3 Infâme",
    "La D1v1ne Coméd1e",
    "Ap0gé3 Inv3rsée",
    "Thé0r1e du Ch40s",
    "Pénult1me",
]
LISTECARACTERISTIQUEMUSIQUE = [
    ["start", "Vous écoutez "],
    ["tutorial", "Vous écoutez "],
    ["alfredproto", "Vous écoutez "],
    ["boss_introV2", "Vous écoutez "],
    ["battle_win", "Vous écoutez "],
    ["gravestone", "Vous écoutez "],
    ["ending", "Vous écoutez "],
    ["reconfort", "Vous écoutez "],
    ["etage_1", "Vous écoutez "],
    ["battle_theme_1", "Vous écoutez "],
    ["boss_1", "Vous écoutez "],
    ["etage_2", "Vous écoutez "],
    ["battle_theme_2", "Vous écoutez "],
    ["boss_2", "Vous écoutez "],
    ["etage_2_alt", "Vous écoutez "],
    ["battle_theme_2_alt", "Vous écoutez "],
    ["boss_2_alt", "Vous écoutez "],
    ["etage_3", "Vous écoutez "],
    ["battle_theme_3", "Vous écoutez "],
    ["boss_3", "Vous écoutez "],
    ["darkness", "Vous écoutez "],
    ["etage_4", "Vous écoutez "],
    ["battle_theme_4", "Vous écoutez "],
    ["boss_4", "Vous écoutez "],
    ["boss_4_phase_2", "Vous écoutez "],
    ["etage_5", "Vous écoutez "],
    ["dance", "Vous écoutez "],
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
    ["observatorium", "Vous écoutez "],
    ["quiet", "Vous écoutez "],
    ["abyss", "Vous écoutez "],
    ["tales", "Vous écoutez "],
    ["etage_0", "Vous écoutez "],
    ["battle_theme_0", "Vous écoutez "],
    ["boss_0", "Vous écoutez "],
    ["etage_9", "Vous écoutez "],
    ["battle_theme_9", "Vous écoutez "],
    ["boss_9", "Vous écoutez "],
    ["etage_11", "Vous écoutez "],
    ["battle_theme_11", "Vous écoutez "],
    ["boss_11", "Vous écoutez "],
    ["boss_11_phase_2", "Vous écoutez "],
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
    # branche du feu
    1257: ["Affinitée de Feu", 1, "None"],
    98654: ["Surchauffe", 2, "Affinitée de Feu"],
    42381: ["Aura de Feu", 3, "Surchauffe"],
    35867: ["Rafale", 4, "Aura de Feu"],
    685486: ["Pyrophile", 2, "Affinitée de Feu"],
    537895: ["Pyrosorcier", 3, "Pyrophile"],
    243537: ["Pyromage", 4, "Pyrosorcier"],
    # branche de foudre
    5675: ["Affinitée de Foudre", 1, "None"],
    977785: ["Anti-Neurotransmitteurs", 2, "Affinitée de Foudre"],
    935761: ["Energiseur", 3, "Anti-Neurotransmitteurs"],
    932624: ["Facture", 4, "Energiseur"],
    876431: ["Rapide", 2, "Affinitée de Foudre"],
    353548: ["Electro", 3, "Rapide"],
    768943: ["Luciole", 4, "Electro"],
    # branche de glace
    7563: ["Affinitée de Glace", 1, "None"],
    646752: ["Ere Glaciaire", 2, "Affinitée de Glace"],
    347852: ["Eclats de Glace", 3, "Ere Glaciaire"],
    376895: ["Grand Froid", 4, "Eclats de Glace"],
    248651: ["Choc Thermique", 2, "Affinitée de Glace"],
    179356: ["Coeur de Glace", 3, "Choc Thermique"],
    785020: ["Cycle Glaciaire", 4, "Coeur de Glace"],
    # branche de terre
    1221: ["Affinitée de Terre", 1, "None"],
    867342: ["Patience", 2, "Affinitée de Terre"],
    159753: ["Rigueur", 3, "Patience"],
    764325: ["Fracturation", 4, "Rigueur"],
    114865: ["Poussière de Diamants", 2, "Affinitée de Terre"],
    335785: ["Richesses Souterraines", 3, "Poussière de Diamants"],
    241053: ["Eboulis", 4, "Richesses Souterraines"],
    # branche physique
    8240: ["Affinitée Physique", 1, "None"],
    758427: ["Peau de Fer", 2, "Affinitée Physique"],
    963741: ["Bluff", 3, "Peau de Fer"],
    123789: ["Réflex", 4, "Bluff"],
    455668: ["Carte du Gout", 2, "Affinitée Physique"],
    2557711: ["Connaissance", 3, "Carte du Gout"],
    7661394: ["Oeuil Magique", 4, "Connaissance"],
    # branche de sang
    9731: ["Affinitée de Sang", 1, "None"],
    9485921: ["Nectar", 2, "Affinitée de Sang"],
    9050607: ["Anémie", 3, "Nectar"],
    2419687: ["Baron Rouge", 4, "Anémie"],
    33054865: ["Suroxygénation", 2, "Affinitée de Sang"],
    71546593: ["Conditions Limites", 3, "Suroxygénation"],
    93654517: ["Anticoagulants", 4, "Conditions Limites"],
    # branche ame
    7093815768: ["Pira", 5, "None"],
    7513590556: ["Elektron", 5, "None"],
    6598328725: ["Tsumeta-Sa", 5, "None"],
    124578953756: ["Mathair", 5, "None"],
    25583669867: ["Fos", 5, "None"],
    255814477582: ["Haddee", 5, "None"],
}


class TraderUsage:

    def __init__(self):
        self.modificateur = 1
        if Player.stigma_negatif == "Mauvaise Réputation":
            self.modificateur = 1.5
        self.modificateur += (Player.numero_de_letage / 10) - 0.1
        self.modificateur_badge_terni = 1
        if "Badge Terni" in Player.liste_dartefacts_optionels and Player.nombre_dennemis_a_letage == 0:
            self.modificateur_badge_terni = 0.7
        self.annuaire_des_prix = {
            "Feuille Jindagee": round(round(15 * self.modificateur)) * self.modificateur_badge_terni,
            "Fruit Jindagee": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,
            "Feuille Aatma": round(round(20 * self.modificateur)) * self.modificateur_badge_terni,
            "Fruit Aatma": round(round(50 * self.modificateur)) * self.modificateur_badge_terni,
            "Crystal Elémentaire": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,
            "Ambroisie": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,
            "Hydromel": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,
            "Orbe de Furie": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,
            "Orbe de Folie": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,
            "Remède": round(round(20 * self.modificateur)) * self.modificateur_badge_terni,
            "Remède Superieur": round(round(50 * self.modificateur)) * self.modificateur_badge_terni,
            "Remède Divin": round(round(100 * self.modificateur)) * self.modificateur_badge_terni,
            "Pillule": round(round(30 * self.modificateur)) * self.modificateur_badge_terni,
            "Pillule Superieure": round(round(60 * self.modificateur)) * self.modificateur_badge_terni,
            "Pillule Divine": round(round(110 * self.modificateur)) * self.modificateur_badge_terni,
            "Fléchette Rouge": round(round(20 * self.modificateur)) * self.modificateur_badge_terni,
            "Flèche Rouge": round(round(55 * self.modificateur)) * self.modificateur_badge_terni,
            "Fléchette Bleue": round(round(20 * self.modificateur)) * self.modificateur_badge_terni,
            "Flèche Bleue": round(round(55 * self.modificateur)) * self.modificateur_badge_terni,
            "Poudre Explosive": round(round(30 * self.modificateur)) * self.modificateur_badge_terni,
            "Roche Explosive": round(round(50 * self.modificateur)) * self.modificateur_badge_terni,
            "Bombe Explosive": round(round(70 * self.modificateur)) * self.modificateur_badge_terni,
            "Fiole de Poison": round(round(50 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Gourde de Poison": round(round(110 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Sève d'Absolution": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Larme d'Absolution": round(round(70 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Soluté d'Absolution": round(round(100 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Sève d'Exorcisme": round(round(20 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Larme d'Exorcisme": round(round(45 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Soluté d'Exorcisme": round(round(70 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Mutagène Bleu": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Grand Mutagène Bleu": round(round(80 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Mutagène Rouge": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Grand Mutagène Rouge": round(round(80 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Mutagène Vert": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Grand Mutagène Vert": round(round(80 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Mutagène Doré": round(round(90 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Grand Mutagène Doré": round(round(150 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Mutagène Hérétique": round(round(100 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Mutagène Fanatique": round(round(100 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Red Coin": 0,
            "Tirage": 0,
            "Machette Rouillée": 150,
            "Vieille Pelle": 200,
            "Gemme de Vie": round(round(300 * self.modificateur)) * self.modificateur_badge_terni,
            "Gemme d'Esprit": round(round(300 * self.modificateur)) * self.modificateur_badge_terni,
            "Fée dans un Bocal": 0,
            "Méga Tirage": 777,
        }
        self.liste_item_etage_1 = [
            "Feuille Jindagee",
            "Feuille Aatma",
            "Crystal Elémentaire",
            "Pillule",
            "Poudre Explosive",
            "Tirage",
            "Red Coin",
            "Fée dans un Bocal",
        ]
        self.liste_item_etage_2 = [
            "Feuille Jindagee",
            "Feuille Aatma",
            "Crystal Elémentaire",
            "Remède",
            "Poudre Explosive",
            "Machette Rouillée",
            "Tirage",
            "Red Coin",
            "Fée dans un Bocal",
        ]
        self.liste_item_etage_3 = [
            "Feuille Jindagee",
            "Feuille Aatma",
            "Crystal Elémentaire",
            "Pillule",
            "Poudre Explosive",
            "Vieille Pelle",
            "Tirage",
            "Méga Tirage",
            "Red Coin",
            "Gemme de Vie",
        ]
        self.liste_item_etage_4 = [
            "Feuille Jindagee",
            "Feuille Aatma",
            "Crystal Elémentaire",
            "Pillule",
            "Poudre Explosive",
            "Tirage",
            "Méga Tirage",
            "Red Coin",
            "Gemme de Vie",
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
            "Fée dans un Bocal",
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
            "Gemme d'Esprit",
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
            "Fée dans un Bocal",
        ]
        self.liste_dartefact_optionels = ["Machette Rouillée", "Vieille Pelle"]
        self.liste_item_actuelle = []

    def SetItemList(self):
        if Player.numero_de_letage == 1:
            self.liste_item_actuelle = self.liste_item_etage_1
        elif Player.numero_de_letage == 2:
            self.liste_item_actuelle = self.liste_item_etage_2
        elif Player.numero_de_letage == 3:
            self.liste_item_actuelle = self.liste_item_etage_3
        elif Player.numero_de_letage == 4:
            self.liste_item_actuelle = self.liste_item_etage_4
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
            self.annuaire_des_prix["Red Coin"] = round(round(Player.numero_de_letage * 100) * self.modificateur_badge_terni)
        self.annuaire_des_prix["Tirage"] = round(round(
            (Player.numero_de_letage * 50)
            + (Player.number_of_tirage * (Player.numero_de_letage * 15)) * self.modificateur_badge_terni)
        )
        self.annuaire_des_prix["Fée dans un Bocal"] = round(round(
            ((Player.numero_de_letage * 50) + 25) * self.modificateur) * self.modificateur_badge_terni
        )

    def UseMegaTirage(self):
        # double tirage des recompenses
        element_tirage = []
        for _ in range(0, 2):
            nombre_aleatoire = random.randint(1, 13)
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
            else:
                element_tirage.append("Vide")
        # choix du joueur
        while True:
            try:
                if Player.affronte_un_boss:
                    print(
                        f"A l'endroit ou se tenait l'ennemi, il y a maintenant une petite boite en métal bleu ornée d'un grand *POW*.\nVous y plongez la main à l'interieur."
                    )
                else:
                    print(
                        f"Le marchand vous laisse plonger la main dans une boite en carton bleue ornée d'un grand *POW*."
                    )
                print(
                    "A l'interieur, vous pouvez toucher le contour de deux masses étranges, rugueuse."
                    f"\nEn les palpant, vous ressentez une connection avec l'élément [{element_tirage[0]}] et l'élement [{element_tirage[1]}]."
                    f"\n1 - Retirer le [{element_tirage[0]}]"
                    f"\n2 - Retirer le [{element_tirage[1]}]"
                )
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
        if (
            (element_tirage[choix - 1] != "Vide")
            and (nom_du_tirage not in Player.sorts_possedes)
            and (nom_du_tirage not in Player.techniques_possedes)
        ):
            commentaire = f"Vous obtenez {type_du_tirage} {nom_du_tirage} !"
            if type_du_tirage == "le sort":
                Player.sorts_possedes.append(nom_du_tirage)
                if "Syra" in Player.liste_dartefacts_optionels:
                    commentaire += ("Grace au verre de Syra que vous avez bu, vous gagnez aussi 10 pv max !")
                    Player.points_de_vie += 10
                    Player.points_de_vie_max += 10
                    Affichage.EntreePourContinuer()
            elif type_du_tirage == "la technique":
                Player.techniques_possedes.append(nom_du_tirage)
                if "Syra" in Player.liste_dartefacts_optionels:
                    commentaire += ("\nGrace au verre de Syra que vous avez bu, vous gagnez aussi 10 pm max !")
                    Player.points_de_mana += 10
                    Player.points_de_mana_max += 10
                    Affichage.EntreePourContinuer()
        else:
            commentaire = "Vous sortez la masse, et elle disparait dans les airs.\nMauvaise Pioche !"
        Affichage.AfficheMegaTirage(commentaire)

    def UseTirage(self):
        # sort ou technique ?
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 50:
            type_tirage = "le sort"
        else:
            type_tirage = "la technique"
        # element ?
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
        # choix du joueur
        while True:
            try:
                if Player.affronte_un_boss:
                    print(
                        f"A l'endroit ou se tenait l'ennemi, il y a maintenant une petite boite en métal jaune ornée d'un grand *?*.\nVous y plongez la main à l'interieur."
                    )
                else:
                    print(
                        f"Le marchand vous laisse plonger la main dans une boite en carton jaune ornée d'un grand *?*."
                    )
                print(
                    "A l'interieur, vous pouvez toucher le contour de deux masses étranges, rugueuse."
                    f"\nEn les palpant, vous ressentez une connection avec l'élément [{element_tirage[0]}] et l'élement [{element_tirage[1]}]."
                    f"\n1 - Retirer le [{element_tirage[0]}]"
                    f"\n2 - Retirer le [{element_tirage[1]}]"
                )
                choix = int(input("Choisissez avec les nombres : "))
                ClearConsole()
                if choix in [1, 2]:
                    break
            except ValueError:
                ClearConsole()
        # construction de la récompense
        # nom commun
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
        # Adjectif
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
        # Accord au féminin, si besoin
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
        # affichage de la récompense
        if (nom_du_tirage in Player.sorts_possedes) or (
            nom_du_tirage in Player.techniques_possedes
        ):
            print(
                "Vous retirez un bout de papier !"
                "\nIl y est écrit : Des fois on gagne, des fois on perd. L'important, c'est de participer !"
            )
            Affichage.EntreePourContinuer()
        else:
            print(f"Vous retirez {type_tirage} {nom_du_tirage} !")
            Affichage.EntreePourContinuer()
            # application de la recompense
            if type_tirage == "le sort":
                Player.sorts_possedes.append(nom_du_tirage)
                if "Syra" in Player.liste_dartefacts_optionels:
                    print("Grace au verre de Syra que vous avez bu, vous gagnez aussi 10 pv max !")
                    Player.points_de_vie += 10
                    Player.points_de_vie_max += 10
                    Affichage.EntreePourContinuer()
            else:
                Player.techniques_possedes.append(nom_du_tirage)
                if "Syra" in Player.liste_dartefacts_optionels:
                    print("Grace au verre de Syra que vous avez bu, vous gagnez aussi 10 pm max !")
                    Player.points_de_mana += 10
                    Player.points_de_mana_max += 10
                    Affichage.EntreePourContinuer()
            

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
                    choix = int(
                        input("\nChoisissez l'item a prendre avec les nombres : ")
                    )
                    if choix in range(1, (len(Trader.liste_item_actuelle) + 2)):
                        break
                except ValueError:
                    ClearConsole()
            if choix in range(2, (len(Trader.liste_item_actuelle) + 2)):
                nom_de_litem = Trader.liste_item_actuelle[choix - 2]
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
                            print(
                                "Alors que vous rangiez votre bocal dans votre sacoche,"
                                " vous voyez les deux fées unir leur pouvoir a travers"
                                " les bocaux pour briser leur cage de verre et s'enfuir."
                                "\nUne bonne lecon d'apprise : Jamais plus de deux fées sur soi !"
                            )
                            Affichage.EntreePourContinuer()
                            Player.possede_une_fee = False
                        else:
                            Player.possede_une_fee = True
                    elif nom_de_litem in Trader.liste_dartefact_optionels:
                        Player.liste_dartefacts_optionels.append(nom_de_litem)
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

    def ShowDeath(self, game_is_over=False):
        if not game_is_over:
            mixer.quit()
            print("[AVENTURE TERMINE]")
            Affichage.EntreePourContinuer()
            print("[CALCUL DE LA CONTRIBUTION DU PERSONNAGE EN COURS...]")
            Affichage.AfficheAvecUnTempsDattente(3)
            print("[CALCUL TERMINE]")
            Affichage.EntreePourContinuer()
            print("[CONTRIBUTION DU PERSONNAGE INSUFFISANTE]")
            Affichage.EntreePourContinuer()
            print("[REALISATION DU DESIR REFUSEE]")
            Affichage.EntreePourContinuer()
            print("[MORT VALIDEE]")
            Affichage.EntreePourContinuer()
        PlayMusic("ending")
        print(
            "|                                                                                         "
        )
        print(
            "|       .-.             .                                                                 "
        )
        print(
            "|      (0.0)                                 +                 .               _.._       "
        )
        print(
            "|       |m|                                                                  .' .-'`      "
        )
        print(
            "|       |=|                                                                 /  /          "
        )
        print(
            "|       |=|                x                       +                     x  |  |          "
        )
        print(
            "|   /|__|_|__|\                                                             \  '.___.;    "
        )
        print(
            "|  (    ( )    )  *                                        x                 '._  _./     "
        )
        print(
            "|   \|\/\\'/\/|/         .                    .                                  ``        "
        )
        print(
            "|     |  Y  |                                                                             "
        )
        print(
            "|     |  |  |                          .                        *                         "
        )
        print(
            "|     |  |  |                                                                             "
        )
        print(
            "|    _|  |  |___________         .                              __________________________"
        )
        print(
            "| __/ |  |  |\          \             _________________________/                          "
        )
        print(
            "|/  \ |  |  |  \         \  _________/                                  88888888          "
        )
        print(
            "|   __|  |  |   |__       \/                                          888888888888        "
        )
        print(
            "|/\/  |  |  |   |\ |______/                                          88888\88/88888       "
        )
        print(
            "| <   +\ |  |\ />  \\'                         ______ ______          888888yy888888       "
        )
        print(
            "|  >   + \  |  \    |                       _/      Y      \_         88888||88888        "
        )
        print(
            "|        + \|+  \  < \                     // Game  | ~~ ~  \\\         88  ||  88         "
        )
        print(
            "|  (O)      +    |    )                   // ~ ~ ~~ |   Over \\\            ||             "
        )
        print(
            "|   |             \  /\                  //________.|.________\\\           ||             "
        )
        print(
            "| ( | )   (o)      \/  )                `----------`-'----------'          ||             "
        )
        print(
            "|_\\\|//__( | )______)_/                                                    ||             "
        )
        print(
            "|        \\\|//                                        Appuyez sur entrée pour terminer.  "
        )
        input(
            "|_________________________________________________________________________________________"
        )
        sys.exit()

    def AfficheGacha(self, recompense):
        PlaySound("gacha")
        print("Le mutagène se révèle...")
        Affichage.AfficheAvecUnTempsDattente(1.7)
        print("Le mutagène se révèle être...")
        Affichage.AfficheAvecUnTempsDattente(1.7)
        print("Le mutagène se révèle être un...")
        Affichage.AfficheAvecUnTempsDattente(1.5)
        time.sleep(0.9)
        print(f"Le mutagène se révèle être un [{recompense}] !")
        self.EntreePourContinuer()
        PlayMusicDeLetage()

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
            print(
                "Vous vous approchez de l'arène et trouvez des déchets et autres bidules sur le sol..."
            )
            self.EntreePourContinuer()
            nombre_aleatoire = random.randint(0, 100)
            if nombre_aleatoire <= 20:
                nom_de_litem = GetRandomItemFromList(LISTEITEM)
                print(
                    "...et une idée germe dans votre esprit !"
                    f"\nVous rassemblez alors les objets entre eux et créez l'objet : {nom_de_litem} !"
                )
                Player.items_possedes[nom_de_litem] += 1
            else:
                print("...mais aucune idée ne vous vient a l'esprit.")
            self.EntreePourContinuer()
        if Player.stigma_positif == "Cueilleuse":
            print(
                "Vous vous approchez de l'arène et trouvez de curieuses plantes dans les interstices entre les briques..."
            )
            self.EntreePourContinuer()
            nombre_aleatoire = random.randint(0, 100)
            if nombre_aleatoire <= 50:
                nom_de_litem = GetRandomItemFromList(LISTEITEMDEFENCE)
                print(
                    "...et une idée germe dans votre esprit !"
                    f"\nVous cueillez alors les monceaux biologiques, appliquez vos techniques de druidesses, et créez l'objet : {nom_de_litem} !"
                )
                Player.items_possedes[nom_de_litem] += 1
            else:
                print("...mais rien ne peut etre fait avec.")
            self.EntreePourContinuer()
        print(
            "Vous rentrez dans l'arène et jettez un coup d'oeil aux tribunes vides, avant de frapper le sol de votre pied."
            "\nAussitôt, une vague bruyante de spectateurs fantomatiques apparaissent, et un ennemi apparait devant vous."
        )
        self.EntreePourContinuer()

    def AffichePlusDennemis(self):
        print(
            "Vous rentrez dans l'arène et jettez un coup d'oeil aux tribunes vides, avant de frapper le sol de votre pied."
            "\nMais rien ne se passe.\nIl n'y a plus personne pour vous affronter."
        )
        if not Player.boss_battu:
            print("A part le boss.")
        if not Player.red_coin_recu_par_extermination and Player.boss_battu:
            print(
                "Un spectateur fantomatique amusé par votre désir d'extermination vous envoie un cadeau depuis les gradins, avant de disparaitre."
            )
            self.EntreePourContinuer()
            print("Vous gagnez un Red Coin !")
            Player.nombre_de_red_coin += 1
            Player.red_coin_recu_par_extermination = True
        self.EntreePourContinuer()

    def AfficheIntroCombatBoss(self):
        if Player.nom_de_letage == "Limbes Flétrissants":
            print("Vous vous approchez du terrain vide, et votre tatouage réagit.")
            self.EntreePourContinuer()
            print("Quelqu'un s'approche.")
            self.EntreePourContinuer()
        else:
            print(
                "Vous rentrez dans l'arène et jettez un coup d'oeil aux tribunes vides."
                "\nVotre tatouage en forme de clé se met a briller.\nVous tendez votre main en direction de la grille de métal ancien, et celle ci brille a son tour."
                "\nAussitôt, une vague silencieuse de spectateurs fantomatiques apparaissent."
            )
            self.EntreePourContinuer()
            print("La grille s'ouvre.\nLe Maitre des lieux s'approche.")
            self.EntreePourContinuer()
        if (Player.numero_de_letage != 8) and (Player.nom_de_letage not in ["Jungle Cruelle"]):
            PlayMusic("boss_introV2")
        liste_commentaire = []
        if Player.numero_de_letage == 1:
            commentaire = "Une boule d'obsidienne flotte jusqu'à votre niveau, et une voix artificielle remplit l'arène."
            liste_commentaire.append(commentaire)
            commentaire = (
                "*SENTIENCE RECONNUE. INITIATION DU PROTOCOLE D'EXPLIQUATION ENCLENCHE*"
                "\n*POUR LES CRIMES SUIVANT CONTRE VOTRE ROI MALGRES SES ANNEES DE BONS ET LOYAUX SERVICES, VOUS VOILA CONDAMNE A LA PEINE DE MORT :*"
                "\n*TENTATIVE DE TRAHISON, TENTATIVE DE REGICIDE, TENTATIVE DE REBELLION, TENTATIVE DE REVOLUTION,*"
                "\n*AVOIR CRACHE SUR UN TABLEAU DU ROI, AVOIR EXPRIME DE LA DISSATISFACTION ENVERS LE ROI ACTUEL,*"
                "\n*AVOIR UN COMPORTEMENT SUSPECT PROCHE DE LA RESIDENCE DU ROI, AVOIR UN COMPORTEMENT SUSPECT PROCHE DE LA CAPITALE DU ROI,"
                "\n*AVOIR UN COMPORTEMENT SUSPECT DANS LE ROYAUME DIRIGE PAR LE ROI, ET ENCORE 2324 AUTRES INFRACTIONS NON CITEE."
            )
            liste_commentaire.append(commentaire)
            commentaire = (
                "*QUESTIONS SOUVENT POSEES :"
                "\n* - MAIS JE N'AI JAMAIS FAIT CELA !*"
                "\n* - CELA DOIT ETRE UNE ERREUR !*"
                "\n* - COMMENT PEUT ON SORTIR D'ICI ?*"
                "\n*UNE SEULE REPONSE : UN ROI JUSTE NE PUNIT PAS LES INNOCENTS."
                "\n*CONSIDEREZ VOTRE PRESENCE ICI COMME UNE PREUVE IRREFUTABLE DE VOTRE CULPABILITE.*"
                "\n\n*PROTOCOLE DEXPLIQUATION TERMINE*"
                "\n*PROTOCOLE DE COMBAT ENCLENCHE*"
            )
            liste_commentaire.append(commentaire)
            commentaire = (
                "La sphère bouge et se transforme en une copie conforme de vous, puis se met a parler :"
                "\n*Nous avions toujours dit qu'il fallait combattre le feu avec le feu !*"
            )
            liste_commentaire.append(commentaire)
        elif Player.numero_de_letage == 0:
            commentaire = "LOREM IPSUM"
            liste_commentaire.append(commentaire)
            commentaire = ("LOREM IPSUM")
            liste_commentaire.append(commentaire)
            commentaire = "LOREM IPSUM"
            liste_commentaire.append(commentaire)
            commentaire = ("LOREM IPSUM")
            liste_commentaire.append(commentaire)
            commentaire = "LOREM IPSUM"
            liste_commentaire.append(commentaire)
            commentaire = ("LOREM IPSUM")
            liste_commentaire.append(commentaire)
        elif Player.numero_de_letage == 9:
            commentaire = "LOREM IPSUM"
            liste_commentaire.append(commentaire)
            commentaire = ("LOREM IPSUM")
            liste_commentaire.append(commentaire)
            commentaire = "LOREM IPSUM"
            liste_commentaire.append(commentaire)
            commentaire = ("LOREM IPSUM")
            liste_commentaire.append(commentaire)
            commentaire = "LOREM IPSUM"
            liste_commentaire.append(commentaire)
            commentaire = ("LOREM IPSUM")
            liste_commentaire.append(commentaire)
        elif Player.numero_de_letage == 2:
            if Player.nom_de_letage == "Jungle Cruelle":
                mixer.quit()
                commentaire = ("L'armure vide se rapproche de vous, et se met en position de combat.")
                liste_commentaire.append(commentaire)
                commentaire = ("Vous jettez un coup d'oeil au tentacule accroché a l'ennemi,"
                               " et vous rendez compte qu'elle n'est pas seulement accrochée, mais fusionnée avec l'armure et son précédent occupant...")
                liste_commentaire.append(commentaire)
                if "Lame Spectrale" in Player.liste_dartefacts_optionels:
                    commentaire = ("...que vous pouvez voir a peine respirer.\nLaisser le coeur de bois mourir n'aura donc pas suffit a sauver le pauvre homme.")
                    liste_commentaire.append(commentaire)
                    commentaire = ("...")
                    liste_commentaire.append(commentaire)
                    commentaire = ("Vous entendez une petite voix sortir avec peine du casque de l'ennemi :")
                    liste_commentaire.append(commentaire)
                    commentaire = (" . . . t  u  e   z     m      o       i      .       .            .            .")
                    liste_commentaire.append(commentaire)
                else:
                    commentaire = ("...dont vous apercevez les restes asséchés. La racine a pompé toute l'énergie du pauvre homme.")
                    liste_commentaire.append(commentaire)
                    commentaire = ("Ce n'est qu'une poupée de chair controllée par un systeme biologique malicieux.")
                    liste_commentaire.append(commentaire)
                    commentaire = ("Une simple...")
                    liste_commentaire.append(commentaire)
                    commentaire = ("...Coquille...")
                    liste_commentaire.append(commentaire)
                    commentaire = ("......vide.")
                    liste_commentaire.append(commentaire)
            else:
                commentaire = (
                    "Un chevalier en armure violette saute depuis le sommet de la tour et atterit en plein milieu de l'arène."
                    "\n*C'est toi le prochain traitre ?*"
                    "\nVous le regardez avec étonnement."
                )
                liste_commentaire.append(commentaire)
                commentaire = (
                    "*Fais pas semblant, je suis une bonne personne, je sais reconnaitre qui n'est ou n'est pas une menace pour le chateau.*"
                    f"\n*Toi par exemple, tu a du sang de monstre sur les mains.*\n*Je dirais que tu a massacré...{Player.nombre_de_monstres_tues} monstres.*"
                )
                liste_commentaire.append(commentaire)
                commentaire = (
                    "*Tu a gouté aux joies du combat, et tu en veux plus, toujours plus.*\n*Je fais confiance a mon flair pour ca. Il m'a sauvé la mise de très nombreuses fois.*"
                    "\n*Tu es une menace pour mon roi et sa sécuritée.*\n*Tu es une menace pour le royaume et son épanouissement.*"
                    "\n*Tu es une menace pour tout ceux que tu croisera sur ton chemin.*"
                    "\nIl se tourne alors vers les spectateurs."
                )
                liste_commentaire.append(commentaire)
                commentaire = (
                    "*Et quel piètre chevalier je serais si je n'arretais pas une vermine dans son genre, hein ?*"
                    "\nLe chevalier pourpre se tourne vers vous et sort une lame rongée par la rouille et la souillure."
                    "\n*Laisse tomber, l'affreux. La justice et le bien sont de mon coté. Tu n'a aucune chance de gagner.*"
                )
                liste_commentaire.append(commentaire)
                commentaire = "*Car tu vois...*"
                liste_commentaire.append(commentaire)
                commentaire = "*...je suis le Chevalier que les gens comme toi ne veulent pas rencontrer.*"
                liste_commentaire.append(commentaire)
        elif Player.numero_de_letage == 3:
            commentaire = (
                "L'arène se met alors a trembler, et le sable commence a s'écouler par les cotés."
                "\nDes blocs de roche, de bois et d'or commencent alors a apparaitre, et au milieu de tout ca, une bien étrange structure pentagonale surmontée d'un sarcophage et de 5 vases canopes."
            )
            liste_commentaire.append(commentaire)
            commentaire = (
                "Un examen plus approfondi de la salle révèle aussi des têtes empaillées et accrochées sur tous les murs de l'arène."
                "\n*Il faut toujours rendre la chose plus spectaculaire. Plus incroyable. C'est du travail, empailler les têtes. Tu aime ?*"
            )
            liste_commentaire.append(commentaire)
            commentaire = (
                "Le sarcophage se souleve alors et une forme vaguement humaine zébrée de lignes de coutures avec un masque de pharaon en sort."
                "\n*Le roi, dans sa folie, s'est emparé des cadavres de ses soi-disants ennemis qu'il a cousut entre eux. puis il a mit l'âme de son frère a l'interieur.*"
                "\n*Je suis un monstre, une atrocitée, mais sur laquelle il avait enfin le controle que son esprit malade requit.*\n*Un Roi des sables du sud que l'on a enfermé dans ce corps....* "
            )
            liste_commentaire.append(commentaire)
            commentaire = (
                "Les vases canopes commencent alors a leviter."
                "\n*Vois ce qu'il reste de la grande lignée qui précédait ce fou : des morceaux de chairs dans des vases magiques.*\n\n\n*Pitoyable.*\n\n"
                "\n*Mais bon. Trêve de bavardage. Il est temps que je t'acceuille comme il se doit.* "
            )
            liste_commentaire.append(commentaire)
            commentaire = "Le roi-monstre jette un coup d'oeil inquiet vers les spectateurs avant de se retourner vers vous et de prendre une pose extravagante."
            liste_commentaire.append(commentaire)
            commentaire = (
                "*Je te souhaite la bienvenue dans mon antre voyageur.*\n*Devant toi se trouve une folie engendrée par le plus malade des esprits : Moi même ! Le grand roi Amonrê !*"
                "\n*JE SUIS NE HOMME ET SI TU EST ASSEZ FORT, C'EST AUJOURDHUI QUE JE MOURRAI MONSTRE !*\n*APPROCHE DONC ET MONTRE MOI L'ETENDUE DE TA PUISSANCE !* "
            )
            liste_commentaire.append(commentaire)
        elif Player.numero_de_letage == 4:
            commentaire = (
                "Vous entendez le son d'un livre qui se ferme fort, et l'apparence de l'arène change brusquement. "
                "\nVous observez alors un bureau finement décoré et rempli d'étagères sur lesquelles sont négligement placés des livres de magie et de sortillèges."
                "\nAu milieu, un adolescent d'une quinzaine d'année vous regarde fixement, coincé entre deux piles de livre plus haute que lui."
            )
            liste_commentaire.append(commentaire)
            commentaire = "*C'est l'heure pas vrai ?*\n*Bon, ben me fout pas la honte hein !*\n*Ya un endroit qu'il faut pas taper, c'est là.*"
            liste_commentaire.append(commentaire)
            commentaire = (
                "L'ennemi tapote son torse, ou repose une amulette a l'aspect ancien."
            )
            liste_commentaire.append(commentaire)
            commentaire = (
                "*Allez, bonne chance !*"
                "\nVous vous retrouvez alors dans l'arène, avec l'enfant mage en face de vous."
            )
            liste_commentaire.append(commentaire)
            commentaire = (
                "*Vous voulez aller plus loin ?*\n*Vous souhaitez sortir du Coliseum avec la gloire, l'argent, et la vie sauve ?*"
                "\n*Dommage pour vous !*\n*Car vous êtes tombé sur le disciple du grand...*"
            )
            liste_commentaire.append(commentaire)
            commentaire = "*Du puissant...*"
            liste_commentaire.append(commentaire)
            commentaire = "*Du musculeux...*"
            liste_commentaire.append(commentaire)
            commentaire = "*Maitre Mage ! Créateur des ces lieux !*"
            liste_commentaire.append(commentaire)
            commentaire = "Votre expression s'assombrit.\n*Bah alors ? Fait pas cette tête ! Tu va pas l'affronter maintenant !*\n*Il n'est pas avec moi car...il est en...*"
            liste_commentaire.append(commentaire)
            commentaire = "Son expression s'assombrit.\n*...en réclusion. Quelque part. Pour devenir plus fort. Surement.*"
            liste_commentaire.append(commentaire)
            commentaire = "*...*"
            liste_commentaire.append(commentaire)
            commentaire = "*...amène toi.*"
            liste_commentaire.append(commentaire)
        elif Player.numero_de_letage == 5:
            commentaire = "Vous entendez du bruit vers un stand de chamboule-tout, et voyez une clochette dépasser d'une poubelle proche."
            liste_commentaire.append(commentaire)
            commentaire = (
                "L'ennemi sort alors de sa cachette."
                "\nIl est habillé avec des vêtements colorés déchirés, de grandes chaussures rouges trouées, "
                "et un masque sur lequel est représenté un sourire béant."
                "\nVous frissonnez en voyant la folie sanguinaire dans les yeux de l'ennemi, a travers un trou dans le costume."
            )
            liste_commentaire.append(commentaire)
            commentaire = "*BONJOUR-JOUR VOYAGEUR ! JE SUIS LE BOUFFON BOUFFON ! JE SUIS ICI-CI POUR AMUSER-MUSER MON ROI !*"
            liste_commentaire.append(commentaire)
            commentaire = (
                "*ET TU SAIS CE QUI L'AMUSERAIT BEAUCOUP ? MOI JE SAIS ! MOI JE SAIS !*"
            )
            liste_commentaire.append(commentaire)
            commentaire = (
                "*CA SERAIT TA TETE AU BOUT D'UN PIQUE ET TES TRIPES DANS UN GATEAU !*"
            )
            liste_commentaire.append(commentaire)
            commentaire = "*ET PUIS SI JE FAIT CA IL ME LAISSERA SUREMENT-REMENT REMONTER DANS LE CHATEAU PAS VRAI ? ET PUIS IL ME LAISSERA MANGER AUTRE CHOSE QUE CES VOYAGEURS SANS RIEN SUR LES OS !*"
            liste_commentaire.append(commentaire)
            commentaire = "*JOUONS ! JOUONS ! YAHAHAHA !*"
            liste_commentaire.append(commentaire)
        elif Player.numero_de_letage == 6:
            commentaire = "Vous entendez des bruits de pas venant de derriere vous.\nAlors que vous vous retournez, vous les entendez encore derriere vous."
            liste_commentaire.append(commentaire)
            commentaire = "*Bienvenue dans mon domaine, voyageur.*"
            liste_commentaire.append(commentaire)
            commentaire = (
                "Finalement, vous vous retournez une dernière fois et trouvez un enfant petit, mais d'allure robuste.\nUn chapeau de pirate est vissé sur sa tête."
                "\nAutour de lui se trouvent des batisses faites de vêtements et autres monceaux de métal.\nDe part et d'autres, des ossements humains jonchent le sol."
            )
            liste_commentaire.append(commentaire)
            commentaire = (
                "*Enfin, mon domaine, plutot celui du Roi.*"
                "\n*Mais avec quelques amis, nous sommes arrivés a battre celui qui dominait cet étage.*"
                "\n*Il est d'ailleurs en plein changement de propriétaire !*"
                "\n*Je pense que c'est assez pour pouvoir dire que c'est le mien maintenant*."
                "\n*N'est-ce pas ?*"
            )
            liste_commentaire.append(commentaire)
            commentaire = "Vous le regardez, pensif. Cet enfant serait donc si agé ?"
            liste_commentaire.append(commentaire)
            commentaire = (
                "*Pas de réponses ?*"
                "\n*Tu dois être déterminé a en finir avec cet endroit.*"
                "\n*Mais regarde donc : Ici repose toutes les personnes qui m'ont suivie.*"
                "\n*Nous avons tenté de nous installer ici, mais le manque d'eau et de lumière nous a rendu fou.*"
                "\n*Enfin, nous...*"
            )
            liste_commentaire.append(commentaire)
            commentaire = (
                "*Eux plutot. L'espèce de pendule vivante qui vivait ici possédait plusieurs reliques qui m'ont aidé a survivre.*"
                "\n*Mais que je suis impoli ! Je ne me suis même pas présenté.*"
            )
            liste_commentaire.append(commentaire)
            commentaire = "*Je suis le Prince des voleurs !*"
            liste_commentaire.append(commentaire)
            commentaire = "*Intemporel, Plus riche que le plus riche des hommes, Libéré des chaines de la soif et de la satiété !*"
            liste_commentaire.append(commentaire)
            commentaire = "*Et afin de conserver tout ces privilèges, je vais me battre contre toi voyageur.*"
            liste_commentaire.append(commentaire)
            commentaire = (
                "Le Prince des Voleurs se tourne alors vers un des membres fantomatiques de l'audience, qui a presque l'air de..."
                "\n...sourire ?"
            )
            liste_commentaire.append(commentaire)
            commentaire = "*Trop de blabla...pas assez envoutant...*"
            liste_commentaire.append(commentaire)
            commentaire = "Il commence a marmoner en regardant le sol, puis vous regarde brusquement."
            liste_commentaire.append(commentaire)
            commentaire = "*Pas grave ! Alors ? On commence ?*"
            liste_commentaire.append(commentaire)
        elif Player.numero_de_letage == 7:
            if Player.nom_de_letage == "Douves du Pénitent":
                commentaire = (
                    "Vous voyez un vieillard aux joues creusées et aux bras tailladés."
                    "\nSon apparence ressemble a ces descriptions que l'on fait des ames damnées, tourmentées en enfer pour l'éternité."
                    "\nCe n'est plus qu'une trace de lui meme maintenant."
                )
                liste_commentaire.append(commentaire)
                commentaire = "*...qui es tu ?*"
                liste_commentaire.append(commentaire)
                commentaire = (
                    "Il n'y a pas une once de curiosité dans sa voix.\nIl ne vous considère pas comme une personne, seulement comme un spectateur monté sur scène pour parler a un acteur."
                )
                liste_commentaire.append(commentaire)
                commentaire = "*Il n'y a plus rien a faire ici. Plus rien a voir. Personne ne viendra à mon secours.*"
                liste_commentaire.append(commentaire)
                commentaire = "Vous le voyez marcher en rond, ses pas laissant un sillage a peine visible dans l'eau sale."
                liste_commentaire.append(commentaire)
                commentaire = (
                    "*J'ai tué mes fidèles serviteurs, fait d'eux un golem suivant mes ordres a la lettre.*"
                )
                liste_commentaire.append(commentaire)
                commentaire = "*J'ai jeté un chevalier qui ne voulait que mon bien dans un affreux paysage. Découpé mon frère pour creer un garde cacpable de me défendre de mes propres démons.*"
                liste_commentaire.append(commentaire)
                commentaire = "*Fusionné mes ministres avec la fabrique du temps, pour me protéger d'invisibles et tout-puissants ennemis. Contaminé de ma folie le plus drole des Hommes du nord.*"
                liste_commentaire.append(commentaire)
                commentaire = "*J'ai tant blessé, pour ne pas être blessé a mon tour.*"
                liste_commentaire.append(commentaire)
                commentaire = "*Ce n'est pas de mes ennemis que j'aurais du me proteger, mais de moi même.*"
                liste_commentaire.append(commentaire)
                commentaire = "Le Roi vous regarde, intensément."
                liste_commentaire.append(commentaire)
                commentaire = (
                    "*Ca y est, tu a eu ce que tu voulait ? Tu connait mon histoire et maintenant tu sais ce que j'en pense ?*"
                )
                liste_commentaire.append(commentaire)
                commentaire = "Une lueur de folie commence a perler dans les yeux du Roi."
                liste_commentaire.append(commentaire)
                commentaire = "*Tu sais que je suis désolé ? Tu sais que je m'en veut énormément ???*"
                liste_commentaire.append(commentaire)
                commentaire = "Des larmes commencent a couler sur ses joues."
                liste_commentaire.append(commentaire)
                commentaire = "*ALORS SORS MOI DE LA !! ARRETE LA TORTURE ! ACCORDE MOI TON PARDON ET LAISSE MOI VIVRE !*"
                liste_commentaire.append(commentaire)
                commentaire = "*TU SAIS QUE RIEN N'EST DE MA FAUTE !! C'EST PAS JUSTE ! CA N'ARRIVE QU'A MOI !*"
                liste_commentaire.append(commentaire)
                commentaire = "Le Roi récupère des objets rouillés en dessous de l'eau, et se prépare au combat."
                liste_commentaire.append(commentaire)
                commentaire = "*RIEN N'EST DE MA FAUTE !! MEURT EN MON NOM POUR QUE JE PUISSE SORTIR ET RETROUVER MA DIGNITE !*"
                liste_commentaire.append(commentaire)
                commentaire = "*MAITRE MAGE ! VALIDE MES CONVICTIONS !*"
                liste_commentaire.append(commentaire)
                commentaire = "Une aura dorée enveloppe le Roi."
                liste_commentaire.append(commentaire)
                commentaire = "*AHAHAHA !! TU VOIS ? MEME LUI EST D'ACCORD !! J'AI TOUJOURS DES GENS DE MON COTE !!! RIEN N'EST DE MA FAUTE !!*"
                liste_commentaire.append(commentaire)
                commentaire = "*ALORS...*"
                liste_commentaire.append(commentaire)
                commentaire = "*MEURT POUR QUE JE PUISSE VIVRE !!!*"
                liste_commentaire.append(commentaire)
            else:
                commentaire = (
                    "Vous voyez un vieillard aux joues creusées et aux bras tailladés."
                    "\nSon apparence ressemble a ces descriptions que l'on fait des ames damnées, tourmentées en enfer pour l'éternité."
                    "\nCe n'est plus qu'une trace de lui meme maintenant."
                )
                liste_commentaire.append(commentaire)
                commentaire = "*T-t-t-TOI !*\n*Tu est venu me TUER c'est ca ?*\n*Comme tout le monde dans ce foutu trou a rat !*\n*Quoique je ne me rapelle pas t'avoir fait jeter ici..*"
                liste_commentaire.append(commentaire)
                commentaire = (
                    "En le voyant vous parler, deux expressions vous viennent a l'esprit : En plein burnout, et Roi de pacotille."
                    "\nSait il seulement qu'il ne parle pas a un des spectres qui hante ses cauchemards ?"
                    "\nQu'il ne parle pas a une création de son cerveau malade, mais a une vraie personne ?"
                )
                liste_commentaire.append(commentaire)
                commentaire = "*MAIS!*\n*Tu ne vas RIEN me faire !*\n*héhé... CLONE D'OBSIDIENNE ! VIENS A MOI !*"
                liste_commentaire.append(commentaire)
                commentaire = "Mais personne ne vient."
                liste_commentaire.append(commentaire)
                commentaire = (
                    "*Tu... l'a tué ?*\n*HAHAHAHA ! TU ES FORT ! MAIS CELA NE SUFFIRA PAS !*\n*TOUS MES GENERAUX SONT SOUS MON COMMANDEMENT !*"
                    "\n*ROI AMONRE ! MON FRERE ! VIENS ICI DEFENDRE TA FAMILLE !*"
                )
                liste_commentaire.append(commentaire)
                commentaire = "Mais personne ne vient.                                            Seul le bruit des flammes répond a ses supplications."
                liste_commentaire.append(commentaire)
                commentaire = "*Ah.... Ah... Je t'avais tout donné mon frère...misérable...*\n*CHEVALIER POURPRE !*\n*RIGOR MORTEX !*\n*AMENEZ VOUS BON SANG !*"
                liste_commentaire.append(commentaire)
                commentaire = "Mais personne ne vient.                              Répéter les mêmes actions en s'attendant a un résultat différent..."
                liste_commentaire.append(commentaire)
                commentaire = "*Ah...AH....AH... STUPIDE CHEVALIER ! ET STUPIDE HORLOGE MAGIQUE !*\n\n*bouffon...s'il te plait...*"
                liste_commentaire.append(commentaire)
                commentaire = "Mais personne ne vient.                                                ...n'est-ce pas là la définition de la folie ? :)"
                liste_commentaire.append(commentaire)
                commentaire = (
                    "*m-m-mon bouffon n'est pas mort, i-i-il est trop fort pour ca...*\n*Il se sont tous retournés contre moi c'est ça ?*"
                    "\n*HEIN ?*\n*JE ME SUIS FAIT TRAHIR ENCORE UNE FOIS ! HAHAHAHAHAHHHHHHH *"
                )
                liste_commentaire.append(commentaire)
                commentaire = "*MAGE ! TU M'A CREE CET ENDROIT !*\n*NE ME TOURNE PAS LE DOS TOI AUSSI !*"
                liste_commentaire.append(commentaire)
                commentaire = "Une voix se met à résonner a l'interieur de la salle."
                liste_commentaire.append(commentaire)
                commentaire = "*Ce type a tué mon apprenti. Je m'occuperais personnellement de son cas. Débrouillez vous avec ca.*"
                liste_commentaire.append(commentaire)
                commentaire = "Une armure d'or et de rubis magiques apparait sur le Roi Déchu. Une épée apparait a ses pieds."
                liste_commentaire.append(commentaire)
                commentaire = "*HAHAHA!*\n*A nous deux maintenant ASSASSIN !* "
                liste_commentaire.append(commentaire)
        elif Player.numero_de_letage == 8:
            commentaire = "Le vieil homme à la barbe blanche se lève et vient se positionner à quelques mètres de vous,\nHache de guerre dans une main, Grimoire dans l'autre."
            liste_commentaire.append(commentaire)
            commentaire = (
                "*Sincèrement...*\n*Que dire de plus que ce qui n'a pas déjà été dit ?*"
            )
            liste_commentaire.append(commentaire)
            commentaire = "*Tu as tué tout le monde ici.*"
            liste_commentaire.append(commentaire)
            commentaire = "*Tu a affronté la quintessence de gardes loyaux, fusionnés en une conscience collective, figés dans l'éternité d'un rêve couleur encre...*"
            liste_commentaire.append(commentaire)
            commentaire = "*...d'un mercenaire devenu chevalier par peur de la mort, bercé d'idéaux souillés par la triste réalitée de sa condition...*"
            liste_commentaire.append(commentaire)
            commentaire = "*...d'un roi dur mais juste, tranformé en monstre a son insu, gardé captif par les liens de la famille...*"
            liste_commentaire.append(commentaire)
            commentaire = "*...d'un faux génie, un trésor d'efforts sans résultats, un apprenti loyal brisé par ses propres démons...*"
            liste_commentaire.append(commentaire)
            commentaire = "*...d'un homme du nord portant un masque de faux sourires, porté par l'espoir de revoir ses contrées...*"
            liste_commentaire.append(commentaire)
            commentaire = "*...d'un représentant du peuple des bas-fonds du royaume, sacrifié au nom d'une loi brimée par le sang et l'injustice...*"
            liste_commentaire.append(commentaire)
            commentaire = "*...et enfin d'un pitoyable Roi qui a, dans sa folie, changé le destin de millions de pauvre gens.*"
            liste_commentaire.append(commentaire)
            commentaire = "*Tu as usé de ta lame sur la quasi-entieretée de la cour du Roi Déchu...*"
            liste_commentaire.append(commentaire)
            commentaire = "*...et maintenant il ne te reste plus que le magicien, l'outil sans qui tout cela n'aurait été possible.*"
            liste_commentaire.append(commentaire)
            commentaire = "*Alors gardons cette conversation simple.*"
            liste_commentaire.append(commentaire)
            commentaire = (
                "*le Maitre Mage prend une grande inspiration.*"
                "\n*JE SUIS LE MAITRE MAGE, CREATEUR DE CES LIEUX. MA MAGIE COULE EN CHACUN DE CES MURS.*"
                "\n*JE SUIS L'APOGEE DE TA QUETE, L'OBJECTIF FINAL DE TA DESTINEE !*"
            )
            liste_commentaire.append(commentaire)
            commentaire = (
                "Les hauts murs de l'arène se détruisent pour réveler les autres étages flottant dans un vide pourpre nacré, tournés vers vous deux."
                "\nLa foule fantomatique silencieuse se met a s'agiter dans tout les sens,"
                "\net sur un claquement de doigt du Maitre Mage, s'autorise a exprimer leur excitation de manière verbale."
                "\nElle se met a scander votre nom, et celui du Maitre Mage, dans un chaos et un brouhaha sans nom !"
                "\nLes spectateurs sont en pleine ébulition !\nVous reconnaissez les figures fantomatiques des différents boss dans les gradins !"
            )
            liste_commentaire.append(commentaire)
            commentaire = "*NE FAISONS PAS ATTENDRE NOTRE PUBLIC !*"
            liste_commentaire.append(commentaire)
            commentaire = "*ROCK AND ROLL !*"
            liste_commentaire.append(commentaire)
        elif Player.numero_de_letage == 9:
            commentaire = "" "\n" "\n"
        elif Player.nom_de_letage == "Dédale Frontière" :
            commentaire = "" "\n" "\n"
        elif Player.nom_de_letage == "Limbes Flétrissants" :
            if Player.numero_boss_alt == 1:
                commentaire = "" "\n" "\n"
            elif Player.numero_boss_alt == 2:
                commentaire = "" "\n" "\n"
            elif Player.numero_boss_alt == 3:
                commentaire = "" "\n" "\n"
            elif Player.numero_boss_alt == 4:
                commentaire = "" "\n" "\n"
            elif Player.numero_boss_alt == 5:
                commentaire = "" "\n" "\n"
            elif Player.numero_boss_alt == 6:
                commentaire = "" "\n" "\n"
            elif Player.numero_boss_alt == 7:
                commentaire = "" "\n" "\n"
            elif Player.numero_boss_alt == 8:
                commentaire = "" "\n" "\n"
            elif Player.numero_boss_alt == 9:
                commentaire = "" "\n" "\n"
            elif Player.numero_boss_alt == 10:
                commentaire = "" "\n" "\n"
        for commentaire in liste_commentaire:
            Affichage.IntroBoss(commentaire)

    def AfficheDescente(self):
        if Player.nom_de_letage == "Limbes Flétrissants" and Player.numero_boss_alt != 11:
            print("L'ennemi battu, vous entendez quelque chose s'ouvrir.")
            self.EntreePourContinuer()
            print("C'est la porte de la ferme en ruine.")
            self.EntreePourContinuer()
            print("A l'interieur, vous ne voyez pas grand chose d'interressant.")
            print("Le bois vermoulu crisse et plie sous vos pas, et seul le son du vent a travers les planches semble vous accompagner.")
            self.EntreePourContinuer()
            print("Dans un coin proche de l'entrée, vous trouvez un vieil escalier de bois, descendant dans l'obscurité.")
            self.EntreePourContinuer()
        elif Player.nom_de_letage == "Limbes Flétrissants" and Player.numero_boss_alt == 11:
            mixer.quit()
            print("Vous vous approchez de la maison en ruine.")
            self.EntreePourContinuer()
            print("La porte s'ouvre lentement.")
            self.EntreePourContinuer()
            print("Derrière, vous trouvez une commode en ruine surmontée d'un coffret de bois d'olivier.")
            if Player.death_divinity :
                print("A l'interieur, il y a plusieurs boites de bois noir !")
                FloorMaker.GiveRandomArtefact()
                FloorMaker.GiveRandomArtefact()
                FloorMaker.GiveRandomArtefact()
                print("Après avoir récupéré les artefacts, vous regardez autour de vous pour trouver une sortie.")
                self.EntreePourContinuer()
                print("Au niveau de la cuisine, vous voyez une faille, ou une fracture a hauteur de tête.")
                self.EntreePourContinuer()
                print("Comme si quelqu'un ou quelque chose était passé par là, mais avait rebroussé chemin après n'avoir rien trouvé.")
                self.EntreePourContinuer()
                print("Vous entrez dans la faille, et vous retrouvez dans un escalier de pierre.")
                Player.numero_de_letage = 10
                Player.etage_alternatif = False

            else:
                self.EntreePourContinuer()
                print("A l'interieur, vous trouvez une photo jaunie par le temps, sur laquelle une centaine de figures différentes, toutes drapées de chitons, se tiennent par les épaules et sourient.")
                self.EntreePourContinuer()
                print("Derriere, il est écrit : *Dans la vie comme dans la mort, je ne fait qu'envier votre sort.*")
                self.EntreePourContinuer()
                print("...")
                self.EntreePourContinuer()
                donnees_de_s0ve = Observation.GetPermanentThingsFromS0ve()
                donnees_de_s0ve["77454135415415"] = "Divinité de la Mort"
                Observation.SetPermanentThingsToS0ve(donnees_de_s0ve)
                dir_path = os.path.dirname(os.path.realpath(__file__))
                chemin_du_fichier_save = dir_path + "\\save.txt"
                os.remove(chemin_du_fichier_save)
                PlaySound("questdone")
                print("Vous obtenez la Divinité de la Mort !")
                print("\nC'est une photo du dernier panthéon des dieux, il y a bien longtemps.\nElle est imprégnée de la culpabilité du Dieu de la Mort, seul survivant de la Guerre de l'Interdit.")
                print("\n - Vous pouvez désormais utiliser les méchanismes anciens a leurs plein potentiel !")
                print(" - Terah gagne le Deuxieme Stigma Positif [Réceptacle de la Mort] !")
                print(" - Vous pouvez désormais utiliser l'élément de la Mort ! Vous pouvez retrouver la liste des talents Ames dans le fichi[ERREUR : FICHIER INTROUVABLE] ")
                print("[FICHIER NOM:122367325 ADDRESSE IPV4:(XXX) INTROUVABLE]")
                print(" - La porte aux redcoins s'ouvre désormais pour tout les personnages jouables ! Finissez le boss rush a nouveau pour gagner 5 artefacts et sortez directement a l'étage 11 !")
                self.EntreePourContinuer()
                print("...?")
                self.EntreePourContinuer()
                print("Une présence immonde s'approche.")
                self.EntreePourContinuer()
                print("La pierre du désir vient vous récolter.")
                self.EntreePourContinuer()
                print("Mais Terah sourit.")
                self.EntreePourContinuer()
                print("Il avait trouvé son chemin.")
                self.EntreePourContinuer()
                print("Et il en profiterait dans une autre vie.")
                self.EntreePourContinuer()
                print("Terah sentit la pierre de désir fracturer l'espace pour venir jusqu'a lui.")
                self.EntreePourContinuer()
                print("Il vit une ombre affreuse venir de la cuisine.")
                self.EntreePourContinuer()
                print("Terah ignora la voix tordue de la chose en face, ferma les yeux, et compta jusqu'a quatre.")
                time.sleep(2.5)
                ClearConsole()
                print("[B0NJ0uR PeTITT5 FL5URR !!§§:;/ 1L EST T3MPsss D- ]")
                time.sleep(1.5)
                sys.exit()
        elif "Passe a Porte Redcoin" not in Player.player_tags :
            print(
                "Vous pressez votre main contre la grille autrefois fermée."
                "\nAlors que la clé incrustée s'efface de votre main, la grille s'ouvre lentement."
            )
            self.EntreePourContinuer()
        if "Draupnir" in Player.liste_dartefacts_optionels and "Passe La Porte Redcoin" not in Player.player_tags :
            print("...?")
            self.EntreePourContinuer()
            print("Vous sentez Draupnir vibrer dans votre poche, et entendez un son de gold tombant par terre...")
            self.EntreePourContinuer()
            print("Puis un autre...")
            self.EntreePourContinuer()
            print("Et encore un autre !")
            self.EntreePourContinuer()
            print("Bientot, c'est une brève pluie de gold qui s'abat sur vous, et dévale les marches de l'escalier !")
            self.EntreePourContinuer()
            gain_gold = Player.nombre_de_gold
            Player.nombre_de_gold += gain_gold
            print(f"Après une petite heure a tout ramasser, vous vous retrouvez avec {gain_gold} golds supplémentaires !")
            self.EntreePourContinuer()
        if "Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure" in Player.liste_dartefacts_optionels:
            print("Alors que vous avancez, vous trébuchez sur votre propre pied et tombez sur le sol.")
            self.EntreePourContinuer()
            print("Votre Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure tombe de votre inventaire et se brise en plusieurs centaines de morceaux !")
            self.EntreePourContinuer()
            Player.liste_dartefacts_optionels.remove("Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure")
            print("Vous faites le deuil de votre Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure et continuez d'avancer, une larme perlant à l'oeuil et les meilleurs souvenirs passés avec votre Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure passant en boucle dans votre mémoire...")
            self.EntreePourContinuer()
        for artefact in Player.liste_dartefacts_optionels:
            if artefact in ["Element [Ame] Surchargé", "Element [Foudre] Surchargé", "Element [Feu] Surchargé", "Element [Terre] Surchargé", "Element [Glace] Surchargé", "Element [Sang] Surchargé", "Element [Corps] Surchargé"]:
                Player.liste_dartefacts_optionels.remove(artefact)
                print("Vous sentez l'appel de la nature et vous soulagez sur place.")
                print(f"Vous perdez l'effet [{artefact}] de la boisson que vous aviez bu !")
                self.EntreePourContinuer()
        if "Assurance Distributeur" in Player.liste_dartefacts_optionels:
            print(f"L'artefact [Assurance Distributeur] part en fumée, protégeant ainsi les artefacts achetés au distributeur !")
            Player.liste_dartefacts_optionels.remove("Assurance Distributeur")
            self.EntreePourContinuer()
        else:
            for artefact in Player.liste_dartefacts_optionels:
                if artefact in ["Epée de Damocles", "Morceau d'Ether Fragile", "Eau Bénite", "Bandeau Catharsis", "Charbon Primordial", "Saphir de Gel", "Fossile Figé", "Fiole d'Eclair"]:
                    Player.liste_dartefacts_optionels.remove(artefact)
                    print(f"L'artefact [{artefact}] disparait de votre inventaire !\nLes artefacts achetés au distributeurs ne tiennent vraiment pas dans la durée...")
                    self.EntreePourContinuer()
        if "Canigou" in Player.liste_dartefacts_optionels:
            Player.liste_dartefacts_optionels.remove("Canigou")
            print("Alors que vous avancez, Canigou fait des petits gémissements de douleur.")
            self.EntreePourContinuer()
            print("Vous saviez qu'un chien modifié ne survivrait pas longtemps en dehors d'un habitat spécifiquement désigné pour lui.")
            print("Vous regardez Canigou avec des larmes dans vos yeux, le caressez une dernière fois, et le laissez repartir dans la niche d'ou il vient.")
            self.EntreePourContinuer()
            print("Adieu, petit chien. On se reverra dans une autre partie.")
            self.EntreePourContinuer()
        print("Vous vous enfoncez encore plus profondément dans le Coliseum.")
        self.EntreePourContinuer()

    def AfficheRentrerChezMarchand(self):
        print(
            "Vous passez une porte primitive de tissu et rentrez dans une salle miteuse.\n"
            "Devant vous, une figure drapée vous propose des items placés sur un bout de chiffon sale... pour un prix."
        )
        self.EntreePourContinuer()

    def AffichePasAssezDargent(self):
        print("Vous n'avez pas assez de golds !")
        self.EntreePourContinuer()

    def AffichePartirMarchand(self):
        print("Vous faites un signe au marchand et repassez la porte de tissu.")
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire == 50:
            print(
                "...? Vous jureriez reconnaitre l'embleme cousu sur le chiffon sale."
                "\nUn griffon a trois tête, cinq ailes, et un bec...le même que celui a l'entrée du coliseum..."
            )
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
        if Player.numero_de_letage == 0:
            commentaire = (
                "Vous ouvrez les yeux en bas d'un escalier monumental dont les marches semblent s'effondrer sur elle même."
                "\nEn vous retournant, vous découvrez un espace sali par le sang et la poussière, jonchés de constructions humaines faites d'os et de terre."
                "\nLa grille est grande ouverte, et une masse argentée semble flotter au milieu de l'arène."
                "\nVous voici a l'étage zéro du Coliseum , la cage mélancolique d'une âme brisée."
            )
            Player.boss_battu = True
        elif Player.numero_de_letage == 1:
            commentaire = (
                "Vous descendez les marches de l'escalier en spirale, et sentez une odeur acre de moisissure monter a vos narines."
                "\nDes murs crasseux, des gradins en ruine, et un sol de gravier et d'os mélangés vous attendent a la fin."
                "\nVous voici au premier étage du Coliseum , une ruine mal entretenue."
            )
        elif Player.numero_de_letage == 2:
            if Player.nom_de_letage == "Jungle Cruelle" :
                commentaire = (
                    "Vous laissez derrière vous le donjon de pierre fragile, et voyez perler sur le plafond des gouttes de...sang ?"
                    "\nUne masse horrible de plantes aux aspects repoussants s'infiltrant dans les moindres interstices,"
                    "\ndes fleurs sur lequelles se dessinent des visages de mort et des yeux percants,"
                    "\nune arène envahie par des racines mouvantes, pulsantes, et des monceaux de briques éclatés vous attendent en bas."
                    "\nAu centre de tout cela, une armure de chevalier maintenue dans les airs par un puissant tentacule de bois semble attendre que vous croisez sa route."
                    "\nVous voici au deuxieme étage du Coliseum , une jungle assassine, assoifée de sang."
                )
            else:
                commentaire = (
                    "Vous laissez derrière vous le donjon de pierre fragile, et voyez perler sur le plafond des gouttes d'eau."
                    "\nUne masse informe de plantes extravagantes poussant dans les interstices entre les briques,"
                    "\nune arène envahie par les mauvaises herbes, et une tour de chateau au dessus de la sortie vous attendent en bas."
                    "\nVous voici au deuxieme étage du Coliseum , une forêt (dés)enchantée."
                )
        elif Player.numero_de_letage == 3:
            commentaire = (
                "Vous laissez derrière vous l'humiditée excessive, et entendez un bruissement sourd."
                "\nUn sol jaune granuleux dans lequel on s'enfonce, un étage sans mur, un soleil artificiel et "
                "\nun vent impossible battant le sable dans vos yeux vous attendent en bas."
                "\nVous voici au troisième étage du Coliseum , un océan de sable."
            )
        elif Player.numero_de_letage == 4:
            commentaire = (
                "Vous laissez derrière vous la sécheresse, et revenez a un environement plus comfortable."
                "\nDes murs infiniment haut sur lesquels reposent des étagères remplies d'un nombre impossible de livres, "
                "\ndes plateaux remplis de bouquins volant d'un bout a l'autre de l'arene, et un sol couvert de moquette douce au toucher vous attendent en bas."
                "\nVous voici au quatrième étage du Coliseum , une tour dédiée a l'étude de la magie."
            )
        elif Player.numero_de_letage == 5:
            commentaire = (
                "Vous laissez derrière vous les livres, et entendez une musique entêtante."
                "\nDes clowns peints sur le mur, des manequins souriants simulant une foule désoeuvrée,"
                "\ndes fausses attractions fabriquées a la hâte avec quelques bouts de carton ,"
                "\net de vieilles enceintes crachant une musique joyeuse en boucle vous attendent en bas."
                "\nVous voici au cinquième étage du Coliseum , une misérable fête foraine."
            )
        elif Player.numero_de_letage == 6:
            commentaire = (
                "Vous laissez derrière vous la fête, et ressentez une présence particulière."
                "\nUn bidonville vide de monde, dans lequel sont parsemés horloges montres et alarmes brisées, "
                "\ndes vieilles banderoles trouées accrochées au plafond, et une gigantesque tour d'horloge au milieu de l'arène vous attendent en bas."
                "\nVous entendez le tic particulier d'un mécanisme, mais l'aiguille des secondes est coincée sur 13h42."
                "\nVous voici au sixième étage du Coliseum , une fracture entre temps et société de quartiers pauvres."
            )
        elif Player.numero_de_letage == 7:
            if Player.nom_de_letage == "Douves du Pénitent":
                commentaire = (
                    "Vous laissez derrière vous le royaume du prince des voleurs, et entendez le sons de quelques clapotis."
                    "\nDes murs de pierre nus, trainés dans la boue, des grilles protégeants quelques culs de sacs des rares personnes a s'aventurer ici, "
                    "\net une peu profonde mais omniprésente couche d'eau tapissant le sol d'un étage qui ressemble plus a une prison qu'a un lieu de vie."
                    "\nVous voici au septieme étage du Coliseum , la bulle de confort d'un esprit torturé par ses propres décisions, pleurant a jamais un pardon qui ne peut être accordé."
                )
            else:
                commentaire = (
                    "Vous laissez derrière vous le royaume du prince des voleurs, et sentez la température augmenter."
                    "\nDes flammes inextinguibles, des cris sans réponses venant de nulle part, des cadavres accrochés a différents instruments de torture, "
                    "\net le mot *Traitre* écrit a l'aide de différents type **d'encre** sur tout les murs de l'arène, telle est la vision qui vous attend en bas."
                    "\nVous voici au septieme étage du Coliseum , le bac à sable d'un esprit fou, torturé, paranoïaque."
                )
        elif Player.numero_de_letage == 8:
            commentaire = (
                "Vous laissez derrière vous les cris de désespoirs, et vous concentrez sur votre but."
                "\nDes murs propres, neufs, ornés de torches. Un sol de marbre, dépassant les gradins, montant au plafond.\nEt une place au dessus de la sortie,"
                " sur laquelle se trouve un vieil homme à la barbe blanche, soignée.\nVoila ce que vous trouvez en bas."
                "\nVous voici au huitième étage du Coliseum , une arène digne de ce nom pour un affrontement avec son créateur."
            )
        elif Player.numero_de_letage == 9 and not ("Marque du Sacrifice" in Player.liste_dartefacts_optionels):
            print(
                "Derrière, vous voyez un long couloir.\nUne vieille porte rouillée a votre gauche vous intrigue,"
                " mais pas plus que ca."
            )
            Affichage.EntreePourContinuer()
            print(
                "Sur le chemin menant a la fin du couloir, vous voyez un petit trou dans les murs."
                "\nA l'interieur, vous apercevez le mot coliseum reposant sur une sorte d'épée,\navec un genre de scintillement au dessus du i."
                "\nEn dessous, le mot O B S E R V A T O R I U M est gravé au couteau, et un nombre en dessous de chaques lettre."
                "\nCa fait un nombre sacrément long !"
            )
            Affichage.EntreePourContinuer()
            commentaire = (
                "Mais vos pensées sont interrompues par le chant des oiseaux que vous entendez a quelques metres."
                "\nVous courrez en direction de la sortie, et retrouvez l'herbe verte, les batiments au loin, et le grillage"
                " caractéristique entourant le Coliseum.\nVous êtes sorti vivant !"
            )
        elif Player.numero_de_letage == 9:
            print("Vous arrivez au couloir de la sortie, mais vos yeux sont fixé sur l'étrange porte rouillée a votre gauche.")
            Affichage.EntreePourContinuer()
            print("La marque sur votre épaule chauffe un peu, et la porte s'ouvre en grand.")
            Affichage.EntreePourContinuer()
            print("Vous descendez les escaliers derrière la porte.")
            Affichage.EntreePourContinuer()
            commentaire = (
                "Vous laissez derrière vous la sortie et les promesses de vie facile à la poursuite de la véritée."
                "\nUn étage étrange, ou la fabrique de la réalitée semble venir mourir a vos pied."
                "\nVous pouvez retrouver un élément de chaque étages sur le sol froid de l'arène, et quand ce n'est pas leur couleur, c'est leur proportion qui varie."
                "\nCertaines banderolles sont encastrés dans le mur, des carrés de sables sortent ca et la de nulle part, "
                "\net vous êtes a peu pres sur que la géométrie des lieux est non euclidienne vu que vous pouvez traverser la salle en un pas si vous passez au bon endroit."
                "\nVous voici au neuvième étage du Coliseum , une poubelle ou viennent reposer les concepts oubliés."
            )
        elif Player.numero_de_letage == 10:
            if Player.nom_de_letage == "Limbes Flétrissants" and Player.numero_boss_alt == 1:
                commentaire = (
                    "Vous passez la porte, qui se referme derriere vous."
                    "\nDevant vous s'étend un vide noir pourpre qui semble ne jamais finir, et en vous retournant vous ne voyez plus la porte."
                    "\nA la place, vous voyez une batisse de bois décrépite, comme une ferme, entourés par des champs labourés stériles, le tout sur une ile qui semble flotter dans le vide."
                    "\nUne entité vous attend devant la porte de la ferme, la même qui vous a attiré ici vous en êtes sûr."
                    "\nVous voici Là ou les Fleurs viennent Fâner, quelque part dans le Coliseum."
                )
            elif Player.nom_de_letage == "Limbes Flétrissants" and Player.numero_boss_alt != 1:
                commentaire = (
                    "Vous avancez à tâton dans le noir, et finissez par trouver un rayon de lumière qui semble percer l'obscurité."
                    "\nVous vous en approchez, et tendez le bras pour toucher la lumière..."
                    "\n...mais a la place votre main pousse une porte de vieux bois, et vous vous retrouvez devant la ferme en ruine et les champs de poussière."
                )
            else:
                commentaire = (
                    "Vous laissez derrière vous l'étage instable et sentez la température baisser."
                    "\nArrivé en bas de l'escalier, vous trouvez un étage d'apparence similaire au premier, mais plus propre ; presque neuf."
                    "\nLa pierre qui constitue les murs est solide, complète, et le sable du sol de l'arène est fin, sans aucune impuretée."
                    "\nCepandant, le son de vos pas semble se perdre dans le néant, alors qu'un écho quasi constant accompagné de courants d'air remplit l'étage."
                    "\nVous regardez à travers l'une des ouvertures de l'arène, et votre regard disparait dans des couloirs qui semblent ne jamais finir, déservant tout autant de salles."
                    "\nVous voici dans la dernière idée de la Pierre de Désir : l'étage aux 100 salles."
                )
        elif Player.numero_de_letage == 11:
            commentaire = (
                "Vous laissez enfin les marches de l'étage interminable et avancez vers la fin de votre voyage."
                "\nUne salle blanche vous attend en bas. Tout est blanc, et vous n'arrivez pas a définir les limites de la salle. Il n'y a que le nécessaire."
                "\nVous voici au onzième étage du Coliseum , la pénultième vision."
            )
        elif Player.numero_de_letage == 12:
            commentaire = (
                "Derrière, vous retrouvez le chant des oiseaux, l'herbe verte, et le grillage"
                " caractéristique entourant le Coliseum.\nVous êtes sorti vivant, riche, et puissant !"
            )
        print(commentaire)
        Affichage.EntreePourContinuer()


class PlayerCaracteristics:

    def __init__(self):
        self.musique_etage_10 = "etage_1"
        self.musique_combat_10 = "battle_theme_1"
        self.mode_de_jeu = "Normal"
        self.gemme_de_vie = False
        self.gemme_de_mana = False
        self.possede_une_fee = False
        self.nom_du_personnage = ""
        self.stigma_positif = ""
        self.stigma_negatif = ""
        self.stigma_bonus = ""
        self.techniques_possedes = []
        self.sorts_possedes = []
        self.items_possedes = DICTIONNAIREITEMINITIAL
        self.talents_possedes = ""
        self.points_de_vie_max = 0
        self.points_de_vie = 0
        self.points_de_mana_max = 0
        self.points_de_mana = 0
        self.points_de_force = 0
        self.points_dendurance = 0
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
        self.commence_le_combat_confus = False
        self.affronte_une_mimique = False
        self.quete = "None"
        self.quete_complete = ["None"]
        self.boss_battu = False
        self.commentaire_boss = "Affronter le Boss"
        self.nombre_dennemis_a_letage = 15
        self.red_coin_recu_par_extermination = False
        self.redcoin_bought = False
        self.library_used = False
        self.liste_daction_oubliees = []
        self.final_library_used = False
        self.quest_giver = True
        self.mercant_healed = False
        self.fountain_used = False
        self.number_of_tirage = 0
        self.invitation_received = False
        self.gold_in_well = 50
        self.chemin_musique = os.path.dirname(os.path.realpath(__file__))
        self.position_y = 0
        self.position_x = 0
        self.numero_de_la_salle = 1
        self.possede_la_cle = False
        self.liste_dartefacts_optionels = []
        self.nombre_de_sacrifices = 0
        self.affronte_obelisque = False
        self.affronte_fin_histoire = False
        self.nom_de_letage = "Aucunes Données Utilisables"
        self.etage_alternatif = False
        self.numero_boss_alt = 1
        self.player_tags = []
        self.death_divinity = False
        donnees_de_s0ve = Observation.GetPermanentThingsFromS0ve()
        if donnees_de_s0ve["77454135415415"] == "Divinité de la Mort":
            self.death_divinity = True
        self.battu_le_sacrifie = False
        self.vies_du_gardien = 12

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
        self.liste_dartefacts_optionels = caracteristiques[20]
        self.points_dendurance = 20

    def ShowcaseCaracteristics(self):
        liste_artefacts = self.PutArtefactInList()
        print(f"          -={{ {Player.nom_du_personnage} }}=-")
        print(
            f"\nPoints de vie : {Player.points_de_vie}/{Player.points_de_vie_max}"
            f"\nPoints de mana : {Player.points_de_mana}/{Player.points_de_mana_max}"
            f"\nEndurance maximale : {Player.points_dendurance}"
            f"\nPoints de force : {Player.points_de_force} | Points d'intelligence : {Player.points_dintelligence}"
            f"\nPoints de defence : {Player.points_de_defence}"
            f"\nChance de coup critique : {Player.taux_coup_critique}% | Degats de coup critique : {Player.degat_coup_critique}"
            f"\nChance de sort critique : {Player.taux_sort_critique}% | Degats de sort critique : {Player.degat_sort_critique}"
            f"\nChance d'esquive : {Player.taux_desquive}%"
            f"\nNombre de Golds : {Player.nombre_de_gold} | Nombre de Redcoins : {Player.nombre_de_red_coin}"
            f"\nNombre d'âmes absorbées : {Player.nombre_de_monstres_tues}"
            f"\nQuête en cours : {Player.quete}"
            f"\nQuêtes réalisées : {Player.quete_complete}"
            f"\nTechniques apprises : {Player.techniques_possedes}"
            f"\nSorts appris : {Player.sorts_possedes}"
            f"\nTalents possédés : {Player.talents_possedes}"
            f"\nArtefacts : {liste_artefacts}"
            f"\nStigmas + : {Player.stigma_positif} | Stigmas - : {Player.stigma_negatif} | Stigmas * : {Player.stigma_bonus}"
        )
        if "Griffes du Démon" in Player.techniques_possedes:
            print(f"S4CR1F1CES R1TU3LS P0UR L'1NN0M4BLE : {Player.nombre_de_sacrifices}")
        print(" \n          -={{ Items }}=-"
              "\n1 - Retour"
        )
        numero_de_laffichage = Player.AffichageItem()
        numero_de_laffichage = Player.AffichageSortSoin(numero_de_laffichage)
        return numero_de_laffichage, int(
            input("\nChoisissez une action avec les nombres : ")
        )

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
        return numero_a_afficher

    def PutArtefactInList(self):
        liste_artefact = []
        if Player.gemme_de_vie:
            liste_artefact.append("Gemme de Vie")
        if Player.gemme_de_mana:
            liste_artefact.append("Gemme d'Esprit")
        if Player.possede_une_fee:
            liste_artefact.append("Fée dans un Bocal")
        if Player.possede_la_cle:
            liste_artefact.append("Clé Incrustée")
        for artefact in Player.liste_dartefacts_optionels:
            liste_artefact.append(artefact)
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
            print(
                f"Vous prenez le temps de vous concentrer pour lancer le sort [{sort_de_soin_a_utiliser}], ce qui réduit son cout en mana et augmente son efficacité."
            )
            print(ANNUAIREDESCRIPTIONSORTSSOIN[sort_de_soin_a_utiliser])
            soin = round(
                (
                    (
                        (POURCENTAGESORTSOIN[sort_de_soin_a_utiliser])
                        + (self.points_dintelligence // 4)
                    )
                    / 100
                )
                * self.points_de_vie_max
            )
            if soin < SOINMINIMUMSORTSOIN[sort_de_soin_a_utiliser]:
                soin = SOINMINIMUMSORTSOIN[sort_de_soin_a_utiliser]
            soin += self.points_dintelligence
            self.points_de_vie += soin
            if self.points_de_vie > self.points_de_vie_max:
                self.points_de_vie = self.points_de_vie_max
            print(f"Vous reprenez {soin} points de vie !")
        else:
            # pas assez de mana
            print(
                "Vous condensez le mana pour invoquer le sort...mais pas assez ne se réunit pour terminer l'invoquation."
            )
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
            bonus_soin = 0
            if self.stigma_positif == "Pharmacodynamisme":
                bonus_soin += 1
            if "Carte du Gout" in Player.talents_possedes:
                bonus_soin += 0.5
            soin += round(bonus_soin * soin)
            nombre_tour = 3
            if "Larme d'Yggdrasil" in Player.liste_dartefacts_optionels:
                nombre_tour += 3
            soin_final = soin * nombre_tour
            self.points_de_vie += soin_final
            if Player.points_de_vie > Player.points_de_vie_max:
                Player.points_de_vie = Player.points_de_vie_max
            print(
                f"Vous utilisez l'item [{item}], et regagnez {soin_final} points de vie en peu de temps !"
            )
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
            bonus_soin = 0
            if self.stigma_positif == "Pharmacodynamisme":
                bonus_soin += 1
            if "Carte du Gout" in Player.talents_possedes:
                bonus_soin += 0.5
            soin += round(bonus_soin * soin)
            nombre_tour = 3
            if "Larme d'Yggdrasil" in Player.liste_dartefacts_optionels:
                nombre_tour += 3
            soin_final = soin * nombre_tour
            self.points_de_mana += soin_final
            if Player.points_de_mana > Player.points_de_mana_max:
                Player.points_de_mana = Player.points_de_mana_max
            print(
                f"Vous utilisez l'item [{item}], et regagnez {soin_final} points de mana en peu de temps !"
            )
        elif item in ["Remède", "Remède Superieur", "Remède Divin"]:
            Player.items_possedes[item] -= 1
            if item == "Remède":
                soin = round(Player.points_de_vie_max * 0.1)
                if soin < 17:
                    soin = 17
            elif item == "Remède Superieur":
                soin = round(Player.points_de_vie_max * 0.2)
                if soin < 27:
                    soin = 27
            elif item == "Remède Divin":
                soin = round(Player.points_de_vie_max * 0.3)
                if soin < 39:
                    soin = 39
            bonus_soin = 0
            if self.stigma_positif == "Pharmacodynamisme":
                bonus_soin += 1
            if "Carte du Gout" in Player.talents_possedes:
                bonus_soin += 0.5
            soin += round(bonus_soin * soin)
            Player.points_de_vie += soin
            if Player.points_de_vie > Player.points_de_vie_max:
                Player.points_de_vie = Player.points_de_vie_max
            print(
                f"Vous appliquez le remède sur vos blessures et regagnez {soin} points de vie !"
            )
        elif item in ["Pillule", "Pillule Superieure", "Pillule Divine"]:
            Player.items_possedes[item] -= 1
            if item == "Pillule":
                soin = round(Player.points_de_mana_max * 0.1)
                if soin < 17:
                    soin = 17
            elif item == "Pillule Superieure":
                soin = round(Player.points_de_mana_max * 0.2)
                if soin < 27:
                    soin = 27
            elif item == "Pillule Divine":
                soin = round(Player.points_de_mana_max * 0.3)
                if soin < 39:
                    soin = 39
            bonus_soin = 0
            if self.stigma_positif == "Pharmacodynamisme":
                bonus_soin += 1
            if "Carte du Gout" in Player.talents_possedes:
                bonus_soin += 0.5
            soin += round(bonus_soin * soin)
            Player.points_de_mana += soin
            if Player.points_de_mana > Player.points_de_mana_max:
                Player.points_de_mana = Player.points_de_mana_max
            print(f"Vous avalez la pillule et regagnez {soin} points de mana !")
        else:
            print(f"Vous preferez garder l'item [{item}] pour les combats.")
        Affichage.EntreePourContinuer()


class DrawInTurtle:

    def __init__(self):
        pass

    def monstre(self):
        down()
        right(45)
        forward(10)
        backward(20)
        forward(10)
        left(90)
        forward(10)
        backward(20)
        forward(10)
        right(45)
        right(90)
        up()
        forward(7)
        left(90)
        down()
        circle(7)
        up()
        left(90)
        forward(7)
        right(90)

    def gold(self):
        forward(7)
        left(90)
        down()
        circle(7)
        up()
        left(90)
        forward(7)
        right(180)

    def puit(self):
        forward(12)
        left(90)
        down()
        circle(12)
        up()
        left(90)
        forward(12)
        right(180)

    def piege(self):
        down()
        right(45)
        forward(10)
        backward(20)
        forward(10)
        left(90)
        forward(10)
        backward(20)
        forward(10)
        right(45)
        up()

    def docs(self):
        down()
        up()
        forward(7)
        left(90)
        down()
        circle(7)
        up()
        left(90)
        forward(7)
        right(90)
        right(90)
        up()

    def salle(self):
        up()
        forward(12.5)
        left(90)
        down()
        forward(12.5)
        left(90)
        forward(25)
        left(90)
        forward(25)
        left(90)
        forward(25)
        left(90)
        forward(12.5)
        right(90)
        up()

    def entree(self):
        up()
        left(90)
        forward(37.5)
        right(90)
        forward(12.5)
        down()
        for _ in range(1, 5):
            hypothenuse = math.sqrt(22656.25)
            #hypothenuse2 = math.sqrt(2031.35) hypothénuse pour des pics moins grands, au cas ou
            angle = 131.65
            #angle2 = 124.62 angle pour des pics moins grands, au cas ou
            remise_a_zero_de_langle = angle - 90
            right(90)
            forward(12.5)
            left(angle)
            forward(hypothenuse)
            up()
            goto(0, 0)
            right(remise_a_zero_de_langle)
            forward(37.5)
            left(90)
            down()
            forward(12.5)
            left(90)
            forward(12.5)
            right(angle)
            forward(hypothenuse)
            up()
            goto(0, 0)
            left(remise_a_zero_de_langle)
            right(90)
            forward(37.5)
            right(90)
            down()
            forward(12.5)

        up()
        backward(12.5)
        right(90)
        forward(37.5)
        left(180)

    def key(self):
        down()
        forward(6)
        left(90)
        forward(2)
        right(90)
        forward(4)
        right(90)
        forward(4)
        right(90)
        forward(4)
        right(90)
        forward(2)
        left(90)
        forward(6)
        right(180)
        forward(3)
        left(90)
        forward(1)
        backward(1)
        left(90)
        forward(3)
        right(90)
        forward(2)
        backward(2)
        right(90)
        up()

    def item(self):
        up()
        left(90)
        forward(8)
        left(90)
        forward(10)
        right(180)
        down()
        forward(20)
        right(90)
        forward(16)
        right(90)
        forward(20)
        right(90)
        forward(16)
        up()
        right(90)
        forward(10)
        right(90)
        forward(8)
        left(90)

    def boss(self):
        up()
        left(90)
        forward(8)
        left(90)
        forward(10)
        right(180)
        down()
        forward(20)
        right(90)
        forward(16)
        right(90)
        forward(20)
        right(90)
        forward(16)
        up()
        right(90)
        forward(10)
        right(90)
        forward(8)
        left(90)
        right(90)
        forward(5)
        left(90)
        down()
        circle(5)
        up()
        left(90)
        forward(5)
        right(90)
        down()
        forward(10)
        backward(20)
        forward(10)
        up()

    def liane(self):
        self.item()
        self.piege()

    def broken(self):
        down()
        left(90)
        forward(8)
        backward(16)
        forward(8)
        right(45)
        forward(6)
        backward(12)
        forward(6)
        right(45)
        forward(8)
        backward(16)
        forward(8)
        right(45)
        forward(6)
        backward(12)
        forward(6)
        left(45)
        up()

    def E(self):
        up()
        backward(25)
        down()
        right(90)
        forward(5)
        backward(5)
        right(90)
        forward(4)
        left(90)
        forward(3)
        backward(3)
        right(90)
        forward(4)
        left(90)
        forward(6)
        up()

    def sequence(self):
        up()
        right(90)
        forward(6.125)
        left(90)
        forward(8)
        left(90)
        forward(10.5)
        right(90)
        down()
        right(90)
        forward(8)
        backward(8)
        right(90)
        forward(8)
        left(90)
        forward(6)
        backward(6)
        right(90)
        forward(7)
        left(90)
        forward(9)
        up()
        left(90)

    def T(self):
        forward(4)
        left(90)
        down()
        forward(7)
        backward(2)
        right(90)
        forward(3)
        backward(3)
        left(90)
        backward(5)
        right(90)
        up()

    def A(self):
        forward(7)
        left(90)
        down()
        forward(4)
        right(45)
        forward(0.5)
        right(45)
        forward(4)
        right(45)
        forward(0.5)
        left(135)
        forward(1.5)
        backward(1.5)
        backward(4.5)
        forward(0.5)
        left(90)
        left(45)
        forward(0.8)
        right(45)
        forward(4.5)
        up()
        right(180)
        forward(5)
        left(90)
        forward(0.5)
        right(90)

    def coeur(self):
        down()
        forward(10)
        backward(5)
        left(90)
        forward(4)
        backward(8)
        forward(4)
        left(90)
        forward(7)
        right(120) #
        forward(7)
        left(150)
        forward(12)
        backward(12)
        right(150)
        backward(7)
        left(120)
        left(120) #
        forward(7)
        right(150)
        forward(12)
        backward(12)
        left(150)
        backward(7)
        right(120)
        right(180)
        up()




    def machine(self):
        forward(2)
        down()
        left(90)
        forward(3)
        backward(6)
        forward(3)
        right(90)
        forward(5)
        left(90)
        forward(10)
        left(90)
        forward(15)
        left(90)
        forward(10)
        left(90)
        forward(3)
        left(90)
        forward(3)
        backward(6)
        forward(3)
        right(90)
        backward(5)
        right(90)
        forward(10)
        left(90)
        forward(15)
        left(90)
        forward(10)
        up()
        setheading(90)

    def e(self):
        forward(5)
        down()
        forward(4)
        backward(4)
        left(90)
        forward(5)
        right(90)
        forward(5)
        right(90)
        forward(3)
        right(90)
        forward(5)
        left(90)
        forward(2)
        left(90)
        forward(5)
        up()

    def un(self):
        forward(10)
        down()
        forward(5)
        backward(2.5)
        left(90)
        forward(6)
        left(90)
        left(35)
        forward(4)
        right(35)
        right(90)
        up()

    def deux(self):
        forward(10)
        down()
        forward(5)
        backward(5)
        left(45)
        forward(4)
        left(45)
        forward(2)
        left(90)
        forward(3)
        left(45)
        forward(2)
        right(45)
        right(90)
        up()

    def trois(self):
        forward(10)
        down()
        forward(5)
        left(90)
        forward(3)
        left(90)
        forward(3)
        backward(3)
        right(90)
        forward(3)
        left(90)
        forward(5)
        right(90)
        up()

    def quatre(self):
        forward(10)
        forward(2.5)
        left(90)
        forward(2)
        down()
        backward(2)
        forward(8)
        left(90)
        left(55)
        forward(6)
        left(35)
        left(90)
        forward(6)
        left(90)
        up()

    def cinq(self):
        forward(10)
        down()
        forward(5)
        left(90)
        forward(2.5)
        left(90)
        forward(5)
        right(90)
        forward(2.5)
        right(90)
        forward(5)
        left(90)
        up()

    def six(self):
        forward(10)
        down()
        left(90)
        forward(2.5)
        backward(2.5)
        right(90)
        forward(5)
        left(90)
        forward(2.5)
        left(90)
        forward(5)
        right(90)
        forward(2.5)
        right(90)
        forward(5)
        left(90)
        up()

    def neuf(self):
        forward(10)
        down()
        forward(5)
        left(90)
        forward(5)
        forward(3)
        left(90)
        forward(5)
        left(90)
        forward(3)
        left(90)
        forward(5)
        left(90)
        up()

    def sept(self):
        right(45)
        backward(6.25)
        down()
        forward(12.5)
        left(135)
        forward(5)
        up()
        setheading(90)

    def obelisque(self, posx, posy):
        self.sept()
        goto(posx, posy)
        right(45)
        self.sept()
        goto(posx, posy)
        right(90)
        self.sept()
        goto(posx, posy)
        right(135)
        self.sept()
        goto(posx, posy)
        right(180)
        self.sept()
        goto(posx, posy)
        left(45)
        self.sept()
        goto(posx, posy)
        left(90)
        self.sept()
        goto(posx, posy)
        left(135)
        self.sept()
        goto(posx, posy)
        left(180)
        self.sept()
        goto(posx, posy)

    def ddr(self):
        backward(6)
        down()
        circle(4)
        forward(15)
        right(90)
        forward(7)
        right(90)
        forward(5)
        right(90)
        forward(7)
        right(90)
        up()
        backward(4)

    def Af(self):
        forward(4)
        left(90)
        down()
        forward(4)
        right(45)
        forward(0.5)
        right(45)
        forward(4)
        right(45)
        forward(0.5)
        left(135)
        forward(1.5)
        backward(1.5)
        backward(4.5)
        forward(0.5)
        left(90)
        left(45)
        forward(0.8)
        right(45)
        forward(4.5)
        up(self)
        right(180)
        forward(5)
        left(90)
        forward(0.5)
        right(90)

    def spot(self):
        up()
        left(90)
        forward(2)
        right(45)
        down()
        forward(7)
        right(90)
        forward(4)
        right(90)
        forward(7)
        left(90)
        forward(7)
        right(90)
        forward(4)
        right(90)
        forward(7)
        left(90)
        forward(7)
        right(90)
        forward(4)
        right(90)
        forward(7)
        left(90)
        forward(7)
        right(90)
        forward(4)
        right(90)
        forward(7)
        up()
        forward(2)
        left(90)
        right(45)

    def mimique(self):
        longueur = 12.25 / 2
        largeur = 6.125 / 2
        up()
        forward(largeur)
        left(90)
        forward(largeur)
        down()
        forward(longueur)
        right(90)
        forward(largeur)
        right(90)
        forward(longueur)
        right(90)
        forward(largeur)
        left(90)
        up()
        forward(longueur)
        down()
        forward(longueur)
        left(90)
        forward(largeur)
        left(90)
        forward(longueur)
        left(90)
        forward(largeur)
        right(90)
        up()
        forward(largeur)
        right(90)
        backward(largeur)
        left(140)
        down()
        forward(3)
        up()
        backward(3)
        left(80)
        down()
        forward(3)
        up()
        backward(3)
        left(140)
        self.item()

    def rituel(self):
        down()
        up()
        left(90)
        forward(5)
        right(90)
        down()
        forward(3)
        backward(6)
        forward(3)
        right(90)
        forward(10)
        left(90)
        forward(3)
        backward(6)
        forward(3)
        left(90)
        forward(5)
        left(90)
        forward(10)
        right(90)
        forward(3)
        backward(6)
        forward(3)
        right(90)
        forward(10)
        up()

    def ley(self):
        down()
        left(90)
        forward(2)
        right(90)
        forward(12.5)
        backward(12.5)
        right(90)
        forward(4)
        right(90)
        forward(12.5)
        backward(12.5)
        right(90)
        forward(2)
        right(90)
        up()

    def secret(self):
        down()
        left(35)
        forward(10)
        right(125)
        forward(11.47)
        right(125)
        forward(20)
        left(125)
        forward(11.47)
        left(125)
        forward(10)
        right(35)
        up()


class Floor:

    def __init__(self):
        self.FloorBlueprint = {}
        self.DictionnaireAjout = {
            # direction : [ajout x, ajout y]
            "Haut": [0, 1],
            "Bas": [0, -1],
            "Gauche": [-1, 0],
            "Droite": [1, 0],
        }
        self.liste_sequence = []
        self.liste_des_salles_observées = []
        self.carte_ouverte = False
        self.ListeDePositionsInconstruisibles = [
            # position x position y
            [-2, -2],
            [-2, -1],
            [-2, 0],
            [-2, 1],
            [-2, 2],
            [-1, -2],
            [-1, -1],
            [-1, 0],
            [-1, 1],
            [-1, 2],
            [0, -2],
            [0, -1],
            [0, 0],
            [0, 1],
            [0, 2],
            [1, -2],
            [1, -1],
            [1, 0],
            [1, 1],
            [1, 2],
            [2, -2],
            [2, -1],
            [2, 0],
            [2, 1],
            [2, 2],
            [3, 2],
            [2, 3],
            [3, 3],
            [3, 4],
            [4, 3],
            [4, 4],
            [4, 5],
            [5, 4],
            [5, 5],
            [-3, -2],
            [-2, -3],
            [-3, -3],
            [-3, -4],
            [-4, -3],
            [-4, -4],
            [-4, -5],
            [-5, -4],
            [-5, -5],
            [-3, 2],
            [-2, 3],
            [-3, 3],
            [-3, 4],
            [-4, 3],
            [-4, 4],
            [-4, 5],
            [-5, 4],
            [-5, 5],
            [3, -2],
            [2, -3],
            [3, -3],
            [3, -4],
            [4, -3],
            [4, -4],
            [4, -5],
            [5, -4],
            [5, -5],
        ]

    def MakeFloorBlueprint(self, nombre_de_salles):
        self.FloorBlueprint = {}
        # faire le dictionnaire de salles, vide
        for numero_de_salle in range(1, (nombre_de_salles + 1)):
            self.FloorBlueprint[numero_de_salle] = {
                "position_x": 0,
                "position_y": 0,
                "marqué sur la carte": False,
                "terminé par joueur": False,
                "type": "None",
            }
        # remplir le dictionnaire avec les salles de base (arene + couloirs sur les cotés)
        if "Schmilblick" in Player.liste_dartefacts_optionels:
            marquage_sur_la_carte = True
        else:
            marquage_sur_la_carte = False
        if (Player.numero_de_letage == 0 and "Combattant le Gardien" not in Player.player_tags) or Player.nom_de_letage == "Limbes Flétrissants":
            fait_par_le_joueur = True
        else:
            fait_par_le_joueur = False
        self.FloorBlueprint[1] = {
            "position_x": 0,
            "position_y": 0,
            "marqué sur la carte": marquage_sur_la_carte,
            "terminé par joueur": False,
            "type": "ENTREE",
        }
        self.FloorBlueprint[2] = {
            "position_x": 2,
            "position_y": 0,
            "marqué sur la carte": marquage_sur_la_carte,
            "terminé par joueur": fait_par_le_joueur,
            "type": "None",
        }
        self.FloorBlueprint[3] = {
            "position_x": -2,
            "position_y": 0,
            "marqué sur la carte": marquage_sur_la_carte,
            "terminé par joueur": fait_par_le_joueur,
            "type": "None",
        }
        self.FloorBlueprint[4] = {
            "position_x": 0,
            "position_y": 2,
            "marqué sur la carte": marquage_sur_la_carte,
            "terminé par joueur": fait_par_le_joueur,
            "type": "None",
        }
        self.FloorBlueprint[5] = {
            "position_x": 0,
            "position_y": -2,
            "marqué sur la carte": marquage_sur_la_carte,
            "terminé par joueur": fait_par_le_joueur,
            "type": "None",
        }
        self.FloorBlueprint[6] = {
            "position_x": 3,
            "position_y": 0,
            "marqué sur la carte": marquage_sur_la_carte,
            "terminé par joueur": fait_par_le_joueur,
            "type": "None",
        }
        self.FloorBlueprint[7] = {
            "position_x": -3,
            "position_y": 0,
            "marqué sur la carte": marquage_sur_la_carte,
            "terminé par joueur": fait_par_le_joueur,
            "type": "None",
        }
        self.FloorBlueprint[8] = {
            "position_x": 0,
            "position_y": 3,
            "marqué sur la carte": marquage_sur_la_carte,
            "terminé par joueur": fait_par_le_joueur,
            "type": "None",
        }
        self.FloorBlueprint[9] = {
            "position_x": 0,
            "position_y": -3,
            "marqué sur la carte": marquage_sur_la_carte,
            "terminé par joueur": fait_par_le_joueur,
            "type": "None",
        }
        # genere aléatoirement une salle autour d'une salle déja posée
        for numero_de_salle in range(1, nombre_de_salles + 1):
            # skippe les salles 1 a 9 deja initialisées
            if numero_de_salle in range(1, 10):
                continue
            # selection de la salle origine, autour de laquelle va se rajouter une salle
            salle_ajoutee = False
            # print(numero_de_salle)
            # time.sleep(1)
            while not salle_ajoutee:
                # choisi une salle au hasard dans le blueprint
                salle_origine = random.randint(6, (numero_de_salle - 1))
                # regarde si il est possible de rajouter une salle autour de cette salle d'origine
                caracteristique_de_la_salle = self.FloorBlueprint[salle_origine]
                position_x_origine = caracteristique_de_la_salle["position_x"]
                position_y_origine = caracteristique_de_la_salle["position_y"]
                # print(position_x_origine)
                # print(position_y_origine)
                liste_de_directions_vide = []
                # test des directions ne possédant pas de salle, depuis l'origine
                for direction in self.DictionnaireAjout:
                    construction_possible = True
                    couple_dajout_sur_les_positions = self.DictionnaireAjout[direction]
                    position_x_potentielle_nouvelle_salle = (
                        position_x_origine + couple_dajout_sur_les_positions[0]
                    )
                    position_y_potentielle_nouvelle_salle = (
                        position_y_origine + couple_dajout_sur_les_positions[1]
                    )

                    # regarde si la position a déja été attribuée a une autre salle
                    for numero_de_salle_a_tester_si_elle_existe_a_la_position_potentielle in (
                        range(1, numero_de_salle)
                    ):
                        salle_a_tester = self.FloorBlueprint[
                            numero_de_salle_a_tester_si_elle_existe_a_la_position_potentielle
                        ]
                        if (
                            position_x_potentielle_nouvelle_salle
                            == salle_a_tester["position_x"]
                            and position_y_potentielle_nouvelle_salle
                            == salle_a_tester["position_y"]
                        ):
                            construction_possible = False
                            break

                    # regarde si la position se trouve dans la zone inconstruisible
                    for position in self.ListeDePositionsInconstruisibles:
                        # print(f"teste {position_x_potentielle_nouvelle_salle}:{position_y_potentielle_nouvelle_salle} | impossible  {position[0]}:{position[1]} ")
                        if (
                            position_x_potentielle_nouvelle_salle == position[0]
                            and position_y_potentielle_nouvelle_salle == position[1]
                        ):
                            construction_possible = False
                            break

                    # si la salle n'est pas sur une salle déja construite ou dans la limite inconstructible,
                    # on rajoute sa direction dans le dictionnaire
                    if construction_possible:
                        liste_de_directions_vide.append(direction)
                        break
                # liste_de_direction_vide contient toute les directions dans lesquelles
                #   on peut mettre une salle a partir de la salle origine sélectionnée.
                # on choisit donc parmis ces directions celle que l'on veut prendre, et on y crée une salle.
                if len(liste_de_directions_vide) != 0:
                    # selection de la direction prise
                    numero_de_la_direction_prise = random.randint(
                        0, (len(liste_de_directions_vide) - 1)
                    )
                    direction_prise = liste_de_directions_vide[
                        numero_de_la_direction_prise
                    ]
                    # selection des positions grace a la direction.
                    couple_dajout_sur_les_positions = self.DictionnaireAjout[direction_prise]
                    position_x_nouvelle_salle = (
                        position_x_origine + couple_dajout_sur_les_positions[0]
                    )
                    position_y_nouvelle_salle = (
                        position_y_origine + couple_dajout_sur_les_positions[1]
                    )
                    # construction salle (ajout au blueprint des position selectionnées)
                    salle_a_construire = self.FloorBlueprint[numero_de_salle]
                    salle_a_construire["position_x"] = position_x_nouvelle_salle
                    salle_a_construire["position_y"] = position_y_nouvelle_salle
                    if "Schmilblick" in Player.liste_dartefacts_optionels:
                        salle_a_construire["marqué sur la carte"] = True
                    if Player.nom_de_letage == "Limbes Flétrissants" or (Player.numero_de_letage == 0 and "Combattant le Gardien" not in Player.player_tags) :
                        salle_a_construire["terminé par joueur"] = True
                    salle_ajoutee = True

    def SetupFloorBlueprint(self):
        # prendre les numeros des salles vides (normalement, de 2 a nombre_salle)
        liste_de_salle_vide = []
        for numero_de_salle in range(2, len(self.FloorBlueprint)):
            # ajouter ces numéros dans une liste
            liste_de_salle_vide.append(numero_de_salle)
        while True:
            if len(liste_de_salle_vide) == 0:
                break
            # sortir un numéro de la liste (de maniere aléatoire, en utilisant les indexs)
            index_aleatoire = random.randint(0, (len(liste_de_salle_vide) - 1))
            salle_choisie = liste_de_salle_vide.pop(index_aleatoire)
            # attribuer une fonction a la salle affectée a ce numéro
            self.AttributingRoleToRoom(salle_choisie)
            # recommencer jusqu'a ce qu'il n'y aie plus de numéros dans la liste
        # pour une raison inconnue, la derniere salle n'est pas attribuée a une fonction
        self.AttributingRoleToRoom(len(self.FloorBlueprint))

    def PrintFloorBlueprint(self):
        self.nombre_de_bols = 1
        nombre_de_salle = len(self.FloorBlueprint)
        setup(width=800, height=800)
        setworldcoordinates(-200, -200, 200, 200)
        goto(0, 0)
        speed(0)
        for salle in range(1, (nombre_de_salle + 1)):
            # initialise les coordonnées de la salle
            caracteristique_de_la_salle = self.FloorBlueprint[salle]
            position_x = caracteristique_de_la_salle["position_x"] * 25
            position_y = caracteristique_de_la_salle["position_y"] * 25
            goto(position_x, position_y)

            # dessine la salle
            if caracteristique_de_la_salle["type"] == "ENTREE":
                Draw.entree()
            else:
                Draw.salle()

            # dessine le dessin de la salle, si il y a a le faire
            if caracteristique_de_la_salle["marqué sur la carte"]:
                goto(position_x, position_y)
                if caracteristique_de_la_salle["type"] == "MONSTRE":
                    Draw.monstre()
                elif caracteristique_de_la_salle["type"] == "GOLD":
                    Draw.gold()
                elif caracteristique_de_la_salle["type"] == "ITEM":
                    Draw.item()
                elif caracteristique_de_la_salle["type"] == "KEY":
                    Draw.key()
                elif caracteristique_de_la_salle["type"] == "LEY":
                    Draw.ley()
                elif caracteristique_de_la_salle["type"] == "MIMIQUE":
                    Draw.mimique()
                elif caracteristique_de_la_salle["type"] == "PIEGE":
                    Draw.piege()
                elif caracteristique_de_la_salle["type"] == "SECRET":
                    Draw.secret()
                elif caracteristique_de_la_salle["type"] == "LIANE":
                    Draw.liane()
                elif caracteristique_de_la_salle["type"] == "BOSS":
                    Draw.boss()
                elif caracteristique_de_la_salle["type"] == "BROKEN":
                    Draw.broken()
                elif (caracteristique_de_la_salle["type"] == "FAUX SPOT" or
                      caracteristique_de_la_salle["type"] == "SPOT"):
                    Draw.spot()
                elif caracteristique_de_la_salle["type"] == "SEQUENCE":
                    Draw.sequence()
                elif caracteristique_de_la_salle["type"] == "DDR":
                    Draw.ddr()
                elif caracteristique_de_la_salle["type"] == "PUIT":
                    Draw.puit()
                elif caracteristique_de_la_salle["type"] == "COEUR":
                    Draw.coeur()
                elif caracteristique_de_la_salle["type"] in ["ARBRE", "CHENIL", "CHARGEUR","JACCUZI", "DISTRIBUTEUR",  "BUFFET", "SPAWNER", "LEVIER"]:
                    Draw.machine()
                elif caracteristique_de_la_salle["type"] == "RITUEL":
                    Draw.rituel()
                elif caracteristique_de_la_salle["type"] == "OBELISQUE":
                    Draw.obelisque(position_x, position_y)
        if "Combattant le Gardien" in Player.player_tags:
            self.UpdatePlayerPosition()
        else:
            goto(0, 0)
        setheading(90)

    def WalkInFloor(self):
        while True:
            while True:
                try:
                    print(
                        f"             -=[ Observation de l'Etage {Player.numero_de_letage} ]=-"
                    )
                    print("")
                    print("4 - Aller à Gauche")
                    print("6 - Aller à Droite")
                    print("8 - Aller en Haut")
                    print("2 - Aller en Bas")
                    print("5 - Observer la Salle")
                    print("")
                    choix = int(input("Choisissez une action avec les nombres : "))
                    ClearConsole()
                    if choix in [4, 6, 8, 5, 2, 123]:
                        break
                except ValueError:
                    ClearConsole()
            if choix == 4:
                self.WalkLeft()
            elif choix == 123:
                print(self.FloorBlueprint)
                Affichage.EntreePourContinuer()
            elif choix == 6:
                self.WalkRight()
            elif choix == 8:
                self.WalkUp()
            elif choix == 2:
                self.WalkDown()
            elif choix == 5:
                try:
                    self.RevealRoom()
                except Exception as error:
                    WriteErrorInErrorLog(error)
                if Player.numero_de_la_salle == 1:
                    if "Sort du Combat contre le Gardien" in Player.player_tags:
                        Player.player_tags.remove("Sort du Combat contre le Gardien")
                    break
            self.UpdatePlayerPosition()
            if "Passer La Porte Redcoin" in Player.player_tags:
                Player.player_tags.remove("Passer La Porte Redcoin")
                break
            elif "Sort du Combat contre le Gardien" in Player.player_tags:
                Player.player_tags.remove("Sort du Combat contre le Gardien")
                break

    def UseMonocleDeVerite(self):
        if "Monocle de Vérité" in Player.liste_dartefacts_optionels:
            Player.nombre_de_gold += 5

    def ReposDansJacuzzi(self):
        self.ArreteJacuzzi = threading.Event()
        self.Jacuzzi = threading.Thread(target=self.GainDansJacuzzi)
        self.Jacuzzi.start()
        input("")
        self.ArreteJacuzzi.set()
        time.sleep(2)

    def GainDansJacuzzi(self):
        numero = 0
        temps_dattente = 30
        commentaire = ""
        while not self.ArreteJacuzzi.isSet():
            print("            -= Vous vous la coulez douce... =-")
            print(f"              Vos points de vie max : {Player.points_de_vie_max}")
            print(f"              Vos points de mana max : {Player.points_de_mana_max}")
            print("   Taux de conversion : +1 point de mana/vie max par 30 secondes.")
            print(commentaire)
            print("          Appuyez sur entree pour sortir du jacuzzi")
            time.sleep(temps_dattente)
            ClearConsole()
            numero += 1
            if numero > 4:
                commentaire = "\n*Vous devriez en profiter pour faire une pause, parler a votre famille, toucher de l'herbe, aller boire de l'eau...*\n"
            elif numero > 15:
                commentaire = "\n*Elle est bien la musique, hein ?*\n"
            if numero > 30:
                commentaire = "\n*Avec vos doigts completements fripés et vos lèvres violettes, vous n'êtes plus sûr de gagner quoi que ce soit en restant dans le jacuzzi...*\n"
            elif numero%2 == 1 :
                Player.points_de_vie_max += 1
            elif numero%2 == 0:
                Player.points_de_mana_max += 1
            

    def RevealRoom(self):
        caracteristique_de_la_salle = self.FloorBlueprint[Player.numero_de_la_salle]
        if caracteristique_de_la_salle["terminé par joueur"] == True:
            print("La salle est sans interêt.")
            Affichage.EntreePourContinuer()
        else:
            if caracteristique_de_la_salle["type"] == "ENTREE":  # DONE
                print("Vous retournez dans l'Arène au centre de l'étage.")
                goto(0, -12.5)
                Affichage.EntreePourContinuer()
            elif caracteristique_de_la_salle["type"] == "MONSTRE":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.monstre()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                # lance le combat
                print("Vous entendez un bruit derrière vous, et découvrez un monstre !")
                Affichage.EntreePourContinuer()
                control = controleur.Control(Player, Trader)
                # lance la bataille
                try:
                    control.Battle()
                except Exception as error:
                    WriteErrorInErrorLog(error)
                PlayMusicDeLetage()

                # fait que l'event soit finit et ne peut ps etre relancé
                caracteristique_de_la_salle["terminé par joueur"] = True
            elif caracteristique_de_la_salle["type"] == "GOLD":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.gold()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True
                print("Vous trouvez un sac de gold caché sous une table.")
                gain_gold = 50 * Player.numero_de_letage
                Player.nombre_de_gold += gain_gold
                print(f"Vous gagnez {gain_gold} golds !")
                Affichage.EntreePourContinuer()
                # fait que l'event soit finit et ne peut ps etre relancé
                caracteristique_de_la_salle["terminé par joueur"] = True
            elif caracteristique_de_la_salle["type"] == "RIEN":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print("Rien que des autels en ruine et des casiers à documents remplis de poussière.")
                Affichage.EntreePourContinuer()

                # fait que l'event soit finit et ne peut ps etre relancé
                caracteristique_de_la_salle["terminé par joueur"] = True
            elif caracteristique_de_la_salle["type"] == "GRAND GARDIEN":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.broken()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                DoBossZero()

            elif caracteristique_de_la_salle["type"] == "PETIT GARDIEN":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.monstre()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                # lance le combat
                print("Vous entendez un bruit derrière vous, et découvrez un monstre !")
                Affichage.EntreePourContinuer()
                control = controleur.Control(Player, Trader)
                # lance la bataille
                try:
                    control.Battle()
                except Exception as error:
                    WriteErrorInErrorLog(error)
                PlayMusicDeLetage()

                # fait que l'event soit finit et ne peut ps etre relancé
                caracteristique_de_la_salle["terminé par joueur"] = True
            elif caracteristique_de_la_salle["type"] == "ITEM":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.item()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print("Vous trouvez une vieille caisse de provision.")
                print(
                    "La plupart des objets sont irrécupérables, a peine des amas de rouille et de pourriture."
                )
                print(
                    "Seul un sac de plastique vert fermé hermétiquement attire votre attention."
                )
                Affichage.EntreePourContinuer()
                nom_de_litem = GetRandomItemFromList(LISTEITEM)
                print(f"A l'interieur se trouve l'objet : {nom_de_litem} !")
                Affichage.EntreePourContinuer()
                Player.items_possedes[nom_de_litem] += 1
                # fait que l'event soit finit et ne peut ps etre relancé
                caracteristique_de_la_salle["terminé par joueur"] = True
            elif caracteristique_de_la_salle["type"] == "KEY":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.key()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print(
                    "Vous trouvez une salle vide, sauf pour une étrange substance flottant dans les airs."
                )
                print(
                    "Alors que vous approchez votre main de la substance, cette dernière fonce d'un coup sur votre paume ouverte et y imprime un tatouage particulier."
                )
                Affichage.EntreePourContinuer()
                print("Vous obtenez la Clé Incrustée !")
                Affichage.EntreePourContinuer()
                Player.possede_la_cle = True

                if Player.nom_de_letage == "Limbes Flétrissants" :
                    Ending.PrintEtEntreePourContinuer("..?")
                    Ending.PrintEtEntreePourContinuer("Vous entendez une voix résonner autour de vous :")
                    if Player.numero_boss_alt == 1:
                        Ending.PrintEtEntreePourContinuer("*Bienvenue enfant maudit.*")
                        Ending.PrintEtEntreePourContinuer("*Je ne peux pas vraiment te parler librement, alors je vais être brève.*\n*Laisse moi te parler du contexte et de ta situation.*")
                        Ending.PrintEtEntreePourContinuer("*Premièrement, j'espère que tu maitrise le combat, car ce que tu va vivre va tester tes compétences dans tout les domaines du combat.*")
                        Ending.PrintEtEntreePourContinuer("*Tu te trouve dans un endroit oublié, là ou on enferme ce que l'on ne peut pas controller, pour affronter 10 terribles existances.* ")
                        Ending.PrintEtEntreePourContinuer("*Dernièrement,*")
                        Ending.PrintEtEntreePourContinuer("*Celui que tu vas affronter ici se nomme Cauchemard.*\n*C'est le résidu de ce qui s'est introduit dans l'esprit du roi pour le rendre fou.*")
                        Ending.PrintEtEntreePourContinuer("*Prend ton mal en patience et attend.*\n*Cette chose est intuable tant que l'on ne chante pas les mélodies qui appaisent l'esprit jeune.*")
                        Ending.PrintEtEntreePourContinuer("*Et crois moi, celui qui l'a jeté dans ce cachot de poussière s'est assuré que ces mélodies soient chantées a un moment ou un autre.*")
                        Ending.PrintEtEntreePourContinuer("*IL ne peut pas se permettre de voir Cauchemard s'échapper, encore.*")
                        Ending.PrintEtEntreePourContinuer("*Fais attention a son influence, il peut altérer ton état d'un claquement de doigts, et ce pendant longtemps.*")
                          #  voix dit que c'est elle qui a appelé, parle de Cauchemard
                    elif Player.numero_boss_alt == 2:
                        Ending.PrintEtEntreePourContinuer("*Bien. Tu as conquis un des nombreux obstacles qui t'attendent.*")
                        Ending.PrintEtEntreePourContinuer("*Premièrement, laisse moi te parler un peu de moi.*")
                        Ending.PrintEtEntreePourContinuer("*Je suis une ombre, un souffle, une présence.*")
                        Ending.PrintEtEntreePourContinuer("*Je suis ton futur, tout comme tu es mon passé.*")
                        Ending.PrintEtEntreePourContinuer("*Je suis le réceptacle de la Mort, après qu'elle ait été laissée tombée par le Dieu de la Mort il y a bien longtemps de cela, dans une guerre sanglante.*")
                        Ending.PrintEtEntreePourContinuer("*Dernièrement,*")
                        Ending.PrintEtEntreePourContinuer("*Celui que tu vas affronter est un enfant royal, venu des sables chauds.*\n*Mais aux yeux de celui qui l'a mutilé, C'etait un matériau.*")
                        Ending.PrintEtEntreePourContinuer("*Une partie de lui vit avec son père, le reste a été condamné a une existance terrible, vivre sans être vivant.*")
                        Ending.PrintEtEntreePourContinuer("*Cepandant, a force de perseverance, il s'est réparé avec l'aide de la science et de la magie.*")
                        Ending.PrintEtEntreePourContinuer("*C'est maintenant un adversaire redoutable, aidé par 2 gardiens de chair et d'âme.*")
                        Ending.PrintEtEntreePourContinuer("*Fais bien attention a ta liste de techniques, de nouvelles actions pourraient t'aider a le vaincre.*")
                        pass  #  voix dit comment arrivé là, parle de astonre
                    elif Player.numero_boss_alt == 3:
                        Ending.PrintEtEntreePourContinuer("*Hey, encore là ? C'est bien.*")
                        Ending.PrintEtEntreePourContinuer("*Premièrement, je pense que je peut t'en dire un peu plus sur l'endroit ou tu te trouve.*")
                        Ending.PrintEtEntreePourContinuer("*Le Coliseum à produit de nombreux guerriers et guerrières au fur et a mesure des années, mais aucuns n'arrivent a la cheville de ceux qui ont un lien avec sa création.*")
                        Ending.PrintEtEntreePourContinuer("*Ces âmes là sont puissantes. Très puissantes. Trop puissantes.*")
                        Ending.PrintEtEntreePourContinuer("*En clair, la Pierre de Désir les a rangés dans un coin inacessible, destiné a être oublié par le temps dans un coin du grand livre de l'Histoire.*")
                        Ending.PrintEtEntreePourContinuer("*Destinés a pourrir dans le plus pur des or.*")
                        Ending.PrintEtEntreePourContinuer("*Dernièrement,*")
                        Ending.PrintEtEntreePourContinuer("*Il n'y a ici que des épitomes de puissance, pas seulement des guerriers et monarques.*")
                        Ending.PrintEtEntreePourContinuer("*Tu affrontera ainsi Ahmed, le cuisinier du Roi Fou.*")
                        Ending.PrintEtEntreePourContinuer("*Il doit y avoir quelque part un livre de recette pour t'expliquer comment fonctionne la cuisine via Mots de Pouvoir.*")
                        Ending.PrintEtEntreePourContinuer("*Pourquoi lire un livre de recette ?*")
                        Ending.PrintEtEntreePourContinuer("*Car ce combat te demandera de jongler entre combat normal et cuisine.*")
                        Ending.PrintEtEntreePourContinuer("*Assure toi de suivre ses demandes de plats à la lettre, ou tu pourrais bien perdre ta vie.*")
                        Ending.PrintEtEntreePourContinuer("*Car Ahmed est un maitre de la magie de visualisation, et après des années a servir dans la plus grande anxiétée un capricieux petit tyrant, il se peut que les règles avec lesquelles tu devras jouer pendant ce combat soient... tordues.*")
                        pass  #  voix dit que font les autres ici, parle de Ahmed
                    elif Player.numero_boss_alt == 4:
                        Ending.PrintEtEntreePourContinuer("*Tu te débrouille bien, enfant maudit. Je suis fier de toi.*")
                        Ending.PrintEtEntreePourContinuer("*Premièrement, parlons de ce que je fait ici.*")
                        Ending.PrintEtEntreePourContinuer("*J'ai été attirée ici par la présence d'âmes puissantes, en attente de passer a la Vie d'Après.*")
                        Ending.PrintEtEntreePourContinuer("*Et je suis tombée prisonnière de cet endroit, appelant avec ferveur quelqu'un comme toi.*")
                        Ending.PrintEtEntreePourContinuer("*Exactement comme toi.*")
                        Ending.PrintEtEntreePourContinuer("*Tu dois donc te demander ce qui se passe en dehors si la Grande Faucheuse est coincée ici ?*")
                        Ending.PrintEtEntreePourContinuer("*Et bien... rien du tout.*\n*Et c'est bien ca le problème.*")
                        Ending.PrintEtEntreePourContinuer("*Pour résumer assez rapidement, dis toi que je ne suis pas la pour briser le lien qui relie les corps et les esprit.*")
                        Ending.PrintEtEntreePourContinuer("*Donc toutes les personnes décédées depuis un bon millénaire sont encore là, coincées dans leurs corps, incapable de bouger ou de s'exprimer, mais ressentant tout.*")
                        Ending.PrintEtEntreePourContinuer("*L'enfer n'est rien à coté d'un millénaire déprivé de sensations et de mouvements.")
                        Ending.PrintEtEntreePourContinuer("*Dernièrement,*")
                        Ending.PrintEtEntreePourContinuer("*L'adversaire que tu vas affronter ici est... délicat.*")
                        Ending.PrintEtEntreePourContinuer("*Quand je suis arrivée là, c'était un monstre terrible a l'apparence trompeuse, maitrisant une armée incroyable.*")
                        Ending.PrintEtEntreePourContinuer("*Mais aujourd'hui, je ne suis pas sûre.*")
                        Ending.PrintEtEntreePourContinuer("*Fais juste attention a sa technique ancestrale, que seul lui peut reproduire malgrès les efforts constants de sa race.*")
                        Ending.PrintEtEntreePourContinuer("*Lorsqu'il...*")
                        Ending.PrintEtEntreePourContinuer("*...se remue comme un flanc.*")
                        Ending.PrintEtEntreePourContinuer("*De plus, c'était a l'époque un berserker, doté d'une capacité inouie a maitriser sa rage.*")
                        Ending.PrintEtEntreePourContinuer("*En clair, plus le temps passe, plus sa rage augmente, et plus il fait de dégâts.*")
                        Ending.PrintEtEntreePourContinuer("*Note bien : je n'ai pas parlé de tours, mais bien de temps passé, secondes minutes et companie.*\n*Je sais que le temps passe différemment pour toi, mais dans ce combat vous êtes au même niveau.*")
                        pass  #  voix dit enfermé par pierre, parle de roi gluant
                    elif Player.numero_boss_alt == 5:
                        Ending.PrintEtEntreePourContinuer("*Bon, je vois que tu es qualifié, il est maintenant temps de parler de mon plan.*")
                        Ending.PrintEtEntreePourContinuer("*Premièrement, pour rentrer ici, il faut 50 redcoins.*\n*Mais sais tu ce que sont les redcoins ?*")
                        Ending.PrintEtEntreePourContinuer("*C'est une accumulation de l'énergie des anciens dieux sous forme liquide.*\n*A donner aux mortels pour leur courage, ou a avaler en cas de pépin pour retrouver toute sa force divine.*")
                        Ending.PrintEtEntreePourContinuer("*C'est une extention du pouvoir divin, une sorte de batterie rechargeable pour les Dieux.*")
                        Ending.PrintEtEntreePourContinuer("*Et au vu de leur disparition, il n'en existe PAS, cinquantes en circulation.*")
                        Ending.PrintEtEntreePourContinuer("*C'est pour ca que cette porte existe, car dans le système créé par la Pierre de Désir, il faut une condition pour tout, afin d'avoir un système équilibré et juste.*")
                        Ending.PrintEtEntreePourContinuer("*En clair, on satisfait les conditions du système en te permettant de passer la porte, mais on empeche tout le monde de la passer en mettant des conditions impossibles a remplir.*")
                        Ending.PrintEtEntreePourContinuer("*On obtient alors une porte infranchissable derriere laquelle enfermer ceux que l'on ne peut pas controller, entièrement.*")
                        Ending.PrintEtEntreePourContinuer("*Sauf que tu as franchit cette porte.*")
                        Ending.PrintEtEntreePourContinuer("*Parlons en au prochain étage.*")
                        Ending.PrintEtEntreePourContinuer("*Dernièrement,*")
                        Ending.PrintEtEntreePourContinuer("*Tu va affronter une personne bien singulière, en aucun cas lié au Coliseum.*")
                        Ending.PrintEtEntreePourContinuer("*Sa présence est due a un problème impossible :*")
                        Ending.PrintEtEntreePourContinuer("*Quelqu'un est rentré dans ce monde, en venant d'ailleurs.*")
                        Ending.PrintEtEntreePourContinuer("*Je ne parle pas de Jean, mais d'un certain Pyrobarbare en quete d'aventure.*")
                        Ending.PrintEtEntreePourContinuer("*Et comme le système est juste et equilibré, il faut une existence pour contrer sa présence.*")
                        Ending.PrintEtEntreePourContinuer("*Voici comment est née Obo la Cryobarbare.*")
                        Ending.PrintEtEntreePourContinuer("*C'est une création artificielle, je n'ai donc pas beaucoup d'informations sur elle.*")
                        Ending.PrintEtEntreePourContinuer("*Je sais juste que la Pierre du Désir a eue beaucoup de mal a la mette la bas, non pas a cause de sa force...*")
                        Ending.PrintEtEntreePourContinuer("*...mais parce qu'elle est vraiment énervante a combattre.*")
                        pass  #  voix dit redcoin dupe, parle de Obo
                    elif Player.numero_boss_alt == 6:
                        Ending.PrintEtEntreePourContinuer("*Toujours là ?*\n*Toujours motivé ?*")
                        Ending.PrintEtEntreePourContinuer("*Continuons.*")
                        Ending.PrintEtEntreePourContinuer("*J'ai vu la manière dont tu as passé la porte.*")
                        Ending.PrintEtEntreePourContinuer("*Tu t'es avancé , et il y avait déja quelques redcoins enfoncés dedans.*")
                        Ending.PrintEtEntreePourContinuer("*Et parmis ces redcoins, il y en avait des identiques.*")
                        Ending.PrintEtEntreePourContinuer("*Comment la porte que personne n'a jamais approché pouvait contenir des redcoins avec la même énergie ?*")
                        Ending.PrintEtEntreePourContinuer("*Tu as, d'une certiane manière, dupliqué des redcoins.*")
                        Ending.PrintEtEntreePourContinuer("*Je dirais même plus :*")
                        Ending.PrintEtEntreePourContinuer("*Tu les as posé, avant.*")
                        Ending.PrintEtEntreePourContinuer("*Il y a quelque chose en toi qui te pousse dans une direction inconnue, mais qui pourtant est toujours la bonne.*")
                        Ending.PrintEtEntreePourContinuer("*Je me suis battue contre la Pierre de Désir, et ma divinité me permet de comprendre certaines choses qui sont...compliquées.*\n*C'est pour cette raison que je suis au courant pour le système ainsi que son administrateur.*")
                        Ending.PrintEtEntreePourContinuer("*Mais il y a quelqu'un qui fait des choses incroyables, et qui utilise le sytème a son avantage pour tenter de battre celui qui l'a construit.*")
                        Ending.PrintEtEntreePourContinuer("*Et ce quelqu'un...*")
                        Ending.PrintEtEntreePourContinuer("*...peut garder certaines choses entre chaque tentatives ratées.")
                        Ending.PrintEtEntreePourContinuer("*C'est littéralement impossible, inconcevable, se dire qu'après une remise a zéro complète du Coliseum, certaines choses restent.*")
                        Ending.PrintEtEntreePourContinuer("*Mais c'est la seule explication possible.*")
                        Ending.PrintEtEntreePourContinuer("*En quoi ca m'aide ? Parlons en tout a l'heure.*")
                        Ending.PrintEtEntreePourContinuer("*Dernièrement,*")
                        Ending.PrintEtEntreePourContinuer("*J'ai déja utilisé tout mon temps de parole ici.*")
                        Ending.PrintEtEntreePourContinuer("*Cette personne est un camarade mort avant la création du Coliseum, et je ne sais pas ce qu'il fait ici.*")
                        Ending.PrintEtEntreePourContinuer("*Un camarade a qui ?*")
                        Ending.PrintEtEntreePourContinuer("*Au Chevalier que l'on ne veut pas rencontrer.*")
                        pass  #  voix dit objectif avec divinité, parle de Mercenaire
                    elif Player.numero_boss_alt == 7:
                        Ending.PrintEtEntreePourContinuer("*...*")
                        Ending.PrintEtEntreePourContinuer("*...*")
                        Ending.PrintEtEntreePourContinuer("*...*")
                        Ending.PrintEtEntreePourContinuer("*bon.*")
                        Ending.PrintEtEntreePourContinuer("*Parlons d'autres choses.*")
                        Ending.PrintEtEntreePourContinuer("*Premièrement, j'espère que tu es familier avec l'histoire de la Guerre de l'Interdit*")
                        Ending.PrintEtEntreePourContinuer("*Si tu ne l'es pas, un petit récapitulatif :*")
                        Ending.PrintEtEntreePourContinuer("*Les Dieux fabriquent des machines qui utilisent leur divinité, pour voir jusqu'ou ils peuvent aller.*")
                        Ending.PrintEtEntreePourContinuer("*Ils construisent une machine pour travers les dimensions, arrivent dans un monde et rentrent en guerre avec lui.*")
                        Ending.PrintEtEntreePourContinuer("*Grosse bataille, ils recrutent un héros humain et 4 héros de quatres races différentes pour garder la porte vers ce nouveau monde, jusqu'a trouver un moyen de l'arreter ou de gagner la guerre.*")
                        Ending.PrintEtEntreePourContinuer("*Re-Grosse bataille, ils envoient la machine et leurs gardiens dans une autre dimension, mais voila : le frere jaloux du leader s'accrochent au groupe pendant son transfert.*")
                        Ending.PrintEtEntreePourContinuer("*Et...on en sait pas plus.*")
                        Ending.PrintEtEntreePourContinuer("*Par contre, ca fait sortir toutes les troupes de lautre monde, Re-Re-Grosse bataille, et tout les dieux meurent, mais ils referment la porte.*")
                        Ending.PrintEtEntreePourContinuer("*Cet endroit la, c'est un peu la soeur de la ou se trouve la machine.*")
                        Ending.PrintEtEntreePourContinuer("*Il a juste prit cette apparence parce que c'est le domaine de la Mort, et il reflete toujours l'endroit ou y il a eu le plus de massacres.*")
                        Ending.PrintEtEntreePourContinuer("*Si tu veut, on se trouve dans l'ancienne maison du Dieu de la Mort.*")
                        Ending.PrintEtEntreePourContinuer("*Sacré endroit pour emprisonner le réceptacle de la Divinité de la Mort, hein ?*")
                        Ending.PrintEtEntreePourContinuer("*Dernièrement,*")
                        Ending.PrintEtEntreePourContinuer("*Le héros des humains, gardien de la porte interdite, est mort.*")
                        Ending.PrintEtEntreePourContinuer("*Mais sa volontée a persistée.*")
                        Ending.PrintEtEntreePourContinuer("*L'essence même de son sens du devoir, cristalisé dans un être plutot faible, mais qui n'abandonne jamais.*")
                        Ending.PrintEtEntreePourContinuer("*Fais attention, a chaque fois qu'il revient a la vie, tu subira un effet élémentaire très fort !*")
                        pass  #  voix dit histoire de l'endroit avec portail et tt, parle de Volontée Immortelle
                    elif Player.numero_boss_alt == 8:
                        Ending.PrintEtEntreePourContinuer("*Oui, revenons en au plan maintenant.*")
                        Ending.PrintEtEntreePourContinuer("*Lorsque j'ai été capturé, on m'a enlevé ma divinité de la Mort, et on l'a placée quelque part ici.*")
                        Ending.PrintEtEntreePourContinuer("*A la fin des Limbes.*")
                        Ending.PrintEtEntreePourContinuer("*C'est plutot malin de la part de la Pierre de Désir, mettre un pouvoir absolu derriere une congrégation de 10 être extremement puissants, derriere une porte impossible a ouvrir.*")
                        Ending.PrintEtEntreePourContinuer("*En plus, vu que l'on est dans un endroit qui représente une dimension dont laquelle rien ne devait sortir, même si quelqu'un récupère la divinité, il restera coincé ici a jamais.*")
                        Ending.PrintEtEntreePourContinuer("*Ou jusqu'a ce que la Pierre de Désir vienne jeter un coup d'oeuil et récupère le pauvre individu pour en faire un autre de ses boss.*")
                        Ending.PrintEtEntreePourContinuer("*Sauf que tu n'es pas un individu normal.*")
                        Ending.PrintEtEntreePourContinuer("*Tu peut prendre des objets appartenant aux dieux et faire comme si tu les avait toujours possédés.*")
                        Ending.PrintEtEntreePourContinuer("*Et une fois que tu recommence la descente du Coliseum...*")
                        Ending.PrintEtEntreePourContinuer("*...notre monde sera affecté de telle sorte que tu aura eu, d'aussi loin qu'on puisse se souvenir, la divinité en ta possession.*")
                        Ending.PrintEtEntreePourContinuer("*On peut faire sortir la Mort de cette cage pour que les gens puissent recommencer a mourir proprement !*")
                        Ending.PrintEtEntreePourContinuer("*Et vu que lorsque tu commence ton aventure, tu descend les marches du Coliseum...*")
                        Ending.PrintEtEntreePourContinuer("*...alors tant que tu ne la commence pas, tu est en dehors du Coliseum !*")
                        Ending.PrintEtEntreePourContinuer("*Tu ne comprend pas ?*\n*La mort reprend son cours tant que tu ne lance pas le système , car la mort ne sera plus piégée dans le Coliseum, mais en dehors !*")
                        Ending.PrintEtEntreePourContinuer("*Je te dirait plus au prochain étage.*")
                        Ending.PrintEtEntreePourContinuer("*Dernièrement,*")
                        Ending.PrintEtEntreePourContinuer("*La combattante a cet étage s'appelle Eris.*")
                        Ending.PrintEtEntreePourContinuer("*C'est la forme corporelle de la Déesse du chaos.*")
                        Ending.PrintEtEntreePourContinuer("*Mais vu que la Déesse du Chaos est déjà morte il y a longtemps, je ne comprend pas ce que son corps divin fait là...*")
                        Ending.PrintEtEntreePourContinuer("*...*")
                        Ending.PrintEtEntreePourContinuer("*...*")
                        Ending.PrintEtEntreePourContinuer("*Je comprend pas.*")
                        Ending.PrintEtEntreePourContinuer("*Si elle est morte pendant la Guerre de l'Interdit, alors il ne devrait plus y avoir aucune trace d'elle, sauf pour sa divinité qui aurait rejoint un réceptacle adapté.*")
                        Ending.PrintEtEntreePourContinuer("*Ca voudrait dire que...*")
                        Ending.PrintEtEntreePourContinuer("*...*")
                        Ending.PrintEtEntreePourContinuer("*Non.*")
                        Ending.PrintEtEntreePourContinuer("*On arrête là.*")
                        pass  #  voix dit Eris ? bizarre !, parle de Eris
                    elif Player.numero_boss_alt == 9:
                        Ending.PrintEtEntreePourContinuer("*...*")
                        Ending.PrintEtEntreePourContinuer("*Voila ta tache.*")
                        Ending.PrintEtEntreePourContinuer("*Bat les deux derniers combattants, récupère la divinité de la Mort, puis remet a zéro cette... ligne temporelle ?*\n*Ce monde ?*\n*Je ne sais pas.*")
                        Ending.PrintEtEntreePourContinuer("*J'imagine que tu voudrais quand même une récompense pour cette quête ?*")
                        Ending.PrintEtEntreePourContinuer("*Sache que posséder la divinité de la Mort sur toi te permettrait deux choses.*")
                        Ending.PrintEtEntreePourContinuer("*Déja, tu vois les méchanismes anciens ?*")
                        Ending.PrintEtEntreePourContinuer("*Ce sont en fait des méchanismes divin, créés par les Dieux pour tester les limites de leur pouvoir.*\n*En ayant la même aura que les dieux, tu possèdera la capacité de les utiliser a leurs plein potentiel.*")
                        Ending.PrintEtEntreePourContinuer("*Un exemple parmis tant d'autres, tu as déja remarqué le double fond dans les coffres a artefacts ?*\n*Non ?*")
                        Ending.PrintEtEntreePourContinuer("*C'est normal. Tu n'es pas un dieu. Car les dieux savent que les meilleurs artefacts sont dans le double fond de la boite a artefact.")
                        Ending.PrintEtEntreePourContinuer("*Enfin, tu pourras aussi utiliser l'élément Ame.*\n*J'imagine que tu a déja vu le sigil des éléments, non ?*")
                        Ending.PrintEtEntreePourContinuer("*Ca ne t'a jamais fait bizarre de pouvoir utiliser des talents pour tout les éléments, sauf pour l'élément Ame ?*")
                        Ending.PrintEtEntreePourContinuer("*Et puis, en vrai, vu que toi, Terah, tu est le réceptacle de cette Divinité, je suis sur que tu pourrais débloquer un joli stigma si tu le possédait.*")
                        Ending.PrintEtEntreePourContinuer("*...*")
                        Ending.PrintEtEntreePourContinuer("*Ca ne suffit pas ?*")
                        Ending.PrintEtEntreePourContinuer("*Alors je te le demande formellement.*")
                        Ending.PrintEtEntreePourContinuer("*S'il te plait, Oh entité supérieure qui guide les pas des gens tombés dans le piège du Coliseum...*")
                        Ending.PrintEtEntreePourContinuer("*Ramène la mort parmis ce monde.*")
                        Ending.PrintEtEntreePourContinuer("*...*")
                        Ending.PrintEtEntreePourContinuer("*S'il te plait.*")
                        Ending.PrintEtEntreePourContinuer("*...*")
                        Ending.PrintEtEntreePourContinuer("*Dernièrement,*")
                        Ending.PrintEtEntreePourContinuer("*Tu a ici un amalgame de la souffrance des âmes retenues prisonnières dans le Coliseum.*")
                        Ending.PrintEtEntreePourContinuer("*C'est la que la Pierre de Désir vient jeter les souffrances psychiques et émotionnelles de celles et ceux qui sont piégés.*")
                        Ending.PrintEtEntreePourContinuer("*C'est un véritable spectre en quête de libertée.*")
                        Ending.PrintEtEntreePourContinuer("*Il possède toutes les techniques et sorts que l'on peut gagner dans le Coliseum.*")
                        Ending.PrintEtEntreePourContinuer("*Bonne chance.*")
                        pass  #  voix dit histoire de l'endroit, pour elle, parle de Spectre
                    elif Player.numero_boss_alt == 10:
                        Ending.PrintEtEntreePourContinuer("...")
                        Ending.PrintEtEntreePourContinuer("...")
                        Ending.PrintEtEntreePourContinuer("...")
                        Ending.PrintEtEntreePourContinuer("Je n'ai pas le choix.")
                        pass  #  voix dit rien, parle pas
                    Ending.PrintEtEntreePourContinuer("*C'est tout pour maintenant.*\n*Que la divinité de la mort emplisse ton coeur de sa puissance, enfant maudit.*")
                    Ending.PrintEtEntreePourContinuer("Vous sentez l'énergie du vide tout autour s'infiltrer par vos pores, et gagnez 10 points de vie max ainsi que 10 points de mana max !")
                    Player.points_de_mana_max += 5
                    Player.points_de_mana += 5
                    Player.points_de_vie_max += 10
                    Player.points_de_vie += 10
                # fait que l'event soit finit et ne peut ps etre relancé
                caracteristique_de_la_salle["terminé par joueur"] = True
            elif caracteristique_de_la_salle["type"] == "LEY":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.ley()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print(
                    "Alors que vous fouillez la pièce, vous ressentez une immense puissance dans le sol."
                )
                print(
                    "Vous avez trouvé un ley !\nC'est un chemin que l'énergie de la nature parcourt."
                )
                Affichage.EntreePourContinuer()
                while True:
                    try:
                        print(
                            "Vous pouvez cultiver votre corps ou votre esprit sur un ley, et il deviendra bien plus puissant !"
                        )
                        print("\n1 - Cultiver votre corps")
                        print("2 - Cultiver votre esprit")
                        choix = int(
                            input("\nChoisissez votre action avec les nombres : ")
                        )
                        ClearConsole()
                        if choix in [1, 2]:
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 1:
                    print(
                        "Vous tentez par tout les moyens de vous épuiser, mais l'énergie du ley vous revigore a chaque fois."
                    )
                    Affichage.EntreePourContinuer()
                    print(
                        "Au bout de plusieurs heures de sport intensif, votre corps gagne en puissance alors que votre vitalité est au max."
                    )
                    Affichage.EntreePourContinuer()
                    print("Vous gagnez 4 points de vie max !")
                    print("Vous reprenez tout vos points de vie !")
                    print("Vous gagnez 1 point d'endurance ! ")
                    Player.points_de_vie_max += 4
                    Player.points_de_vie = Player.points_de_vie_max
                    Player.points_dendurance += 1
                    Affichage.EntreePourContinuer()
                else:
                    print(
                        "Vous faites la position du lotus au dessus du ley, et meditez."
                    )
                    print(
                        "Votre esprit se faire remplir de sons, couleurs, et souvenirs que vous n'aviez jamais experiencé auparavant."
                    )
                    Affichage.EntreePourContinuer()
                    print(
                        "Au bout de lusieurs heures, vous arrivez a dompter la mémoire de la Terre, et votre réservoir de mana s'en trouve aggrandit."
                    )
                    Affichage.EntreePourContinuer()
                    print("Vous gagnez 5 points de mana max !")
                    print("Vous reprenez tout vos points de mana !")
                    Player.points_de_mana_max += 5
                    Player.points_de_mana = Player.points_de_mana_max
                    Affichage.EntreePourContinuer()
                print("Le ley s'assèche, et disparait.")
                print("L'énergie a du trouver un autre endroit pour passer.")
                Affichage.EntreePourContinuer()

                # fait que l'event soit finit et ne peut ps etre relancé
                caracteristique_de_la_salle["terminé par joueur"] = True
            elif caracteristique_de_la_salle["type"] == "MIMIQUE":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.mimique()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print("Vous trouvez un coffre !")
                print(
                    "Ses reliures de cuivres, ses gravures de bois noble, ses contours en or fin vous attirent"
                    " et remplissent votre coeur de cupidité !"
                )
                Affichage.EntreePourContinuer()
                print(
                    "Seul bémol : une respiration sourde, saccadée, qui résonne dans toute la salle et dont les échos masquent l'origine."
                )
                print("Le trésor est peut-être gardé, après tout.")
                Affichage.EntreePourContinuer()
                while True:
                    try:
                        print("Que faire ?")
                        print("\n1 - Approcher le coffre")
                        print("2 - Partir")
                        choix = int(
                            input("\nChoisissez votre action avec les nombres : ")
                        )
                        ClearConsole()
                        if choix in [1, 2]:
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 1:
                    # lance le combat
                    print(
                        "Vous vous approchez du coffre, et il prend soudainement vie !"
                    )
                    Affichage.EntreePourContinuer()
                    Player.affronte_une_mimique = True
                    control = controleur.Control(Player, Trader)
                    # lance la bataille
                    try:
                        control.Battle()
                    except Exception as error:
                        WriteErrorInErrorLog(error)
                    Player.affronte_une_mimique = False
                    PlayMusicDeLetage()

                    # fait que l'event soit finit et ne peut ps etre relancé
                    caracteristique_de_la_salle["terminé par joueur"] = True
                else:
                    print("Vous reculez prudemment.")
                    Affichage.EntreePourContinuer()
            elif caracteristique_de_la_salle["type"] == "PIEGE":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.piege()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print(
                    "Vous fouillez la salle...et déclenchez un piège en déplacant un meuble."
                )
                print(
                    "Aussitot, des arbalètes sournoises, cachées dans les murs, vous criblent de flèches !"
                )
                Affichage.EntreePourContinuer()
                if not ("Sabre du Roi de Glace" in Player.liste_dartefacts_optionels):
                    degat = round(Player.points_de_vie_max * 0.33)
                    Player.points_de_vie -= degat
                    print(f"Vous perdez {degat} points de vie.")
                    Affichage.EntreePourContinuer()
                    if Player.points_de_vie <= 0:
                        mixer.quit()
                        PlaySound("death")
                        print("Vous échouez a stopper le saignement, et perdez la vie.")
                        Affichage.EntreePourContinuer()
                        Affichage.ShowDeath()
                    print(
                        "Le piège se ré-enclenche.\nEvitez de fouiller cette salle dans le futur !"
                    )
                    Affichage.EntreePourContinuer()
                else:
                    print("Cepandant, des éclats de glace se forment aux endroits ou les flèches auraient du se planter.")
                    print("De plus, avant que les arbalettes ne puissent battre en retraite dans les murs de la salle, un froid glacial les éclate par gélifraction.")
                    Affichage.EntreePourContinuer()
                    print("Vous n'aurez plus a vous soucier de cette salle désormais !")
                    Affichage.EntreePourContinuer()
                    # fait que l'event soit finit et ne peut ps etre relancé
                    caracteristique_de_la_salle["terminé par joueur"] = True
            elif caracteristique_de_la_salle["type"] == "SECRET":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.secret()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                Observation.SeeSomething()
            elif caracteristique_de_la_salle["type"] == "COEUR":
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.coeur()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                if Player.numero_de_letage == 2 :
                    print("Vous arrivez dans une clairière artificielle, au centre de laquelle se tient une lame magnifique encastrée dans un rocher.")
                    print("Loin au dessus du rocher, vous apercevez une ouverture cerclée de vieille pierre.")
                    Affichage.EntreePourContinuer()
                    print("Les racines des arbres environnant semblent converger au niveau du rocher.")
                    Affichage.EntreePourContinuer()
                    while True:
                        try:
                            print("Que faire ?")
                            print("\n1 - S'éloigner\n2 - Retirer la lame")
                            choix = int(
                                input("\nChoisissez votre action avec les nombres : ")
                            )
                            ClearConsole()
                            if choix in [1, 2]:
                                break
                        except ValueError:
                            ClearConsole()
                    if choix == 1:
                        print("Vous vous éloignez de la clairière.")
                        Affichage.EntreePourContinuer()
                    else:
                        print("Vous vous approchez de la roche, et posez vos main sur le paumeau de l'épée.")
                        if Player.nom_de_letage == "Jungle Cruelle":
                            print("Aussitot, les sons de la forêt se taisent.")
                            Affichage.EntreePourContinuer()
                            print("Vous sentez les arbres pale étendre les racines sous la surface du sol, comme pour tenter de vous attraper, ou de vous arreter.")
                            Affichage.EntreePourContinuer()
                            print("Des cris a glacer le sang émanent de tout les cotés, et vous remarquez enfin la grosse tache de sang tout autour du rocher, a moitié absorbée.")
                            Affichage.EntreePourContinuer()
                            print("Votre poul s'accélère, et vous tirez de toutes vos forces sur la lame...")
                            Affichage.EntreePourContinuer()
                            print("..qui finit enfin par sortir de son fourreau de pierre, révélant en dessous un coeur de bois se vidant d'une sève couleur cendre.")
                            Affichage.EntreePourContinuer()
                            print("Les cris se taisent, et la forêt meurt.")
                            Affichage.EntreePourContinuer()
                            print("Alors que vous prenez enfin toute la gravité de vos actions, vous observez la lame, qui luit doucement dans votre main.")
                            print("Son apparence trompeuse a laissé place a un artefact rongé par la rouille, mais qui semble attirer le mana.")
                            Affichage.EntreePourContinuer()
                            print("Vous obtenez l'artefact [Lame Spectrale] !")
                            print("Lorsqu'un ennemi brise son réservoir de mana, vous retrouvez jusqu'à 30% de vos points de mana maximum !")
                            caracteristique_de_la_salle["terminé par joueur"] = True
                            Player.liste_dartefacts_optionels.append("Lame Spectrale")
                            Affichage.EntreePourContinuer()
                            print("Vous vous éloignez de la clairière.")
                            Affichage.EntreePourContinuer()
                        else:
                            print("Aussitot, les sons de la forêt se taisent.")
                            Affichage.EntreePourContinuer()
                            print("Un vent violent se lève, alors que vous soulevez la lame de son piédestal.")
                            Affichage.EntreePourContinuer()
                            print("Vous finissez par sortir entièrement l'épée de son rocher, et découvrez en dessous un coeur de bois désséché dans lequel le métal était planté.")
                            Affichage.EntreePourContinuer()
                            print("Et alors que vous observez votre nouvelle arme...")
                            Affichage.EntreePourContinuer()
                            print("...Zeroual grandit...")
                            Affichage.EntreePourContinuer()
                            print("...enveloppe l'arme...")
                            Affichage.EntreePourContinuer()
                            print("...et l'avale d'un coup.")
                            Affichage.EntreePourContinuer()
                            print("La ou se tenait auparavant un artefact splendide arraché a un lieu magique, il y a maintenant une marque ésotérique gravée sur la peaume de votre main.")
                            Affichage.EntreePourContinuer()
                            print("Vous obtenez l'artefact [Marque du Tyrant] !")
                            print("Lorsque vous finissez un combat avec toute votre vie, vous gagnez un point de vie max supplémentaire !")
                            print("De plus, le nombre de monstre que vous avez tué augmente de 5, pour une raison quelquonque !")
                            caracteristique_de_la_salle["terminé par joueur"] = True
                            Player.liste_dartefacts_optionels.append("Marque du Tyrant")
                            Player.nombre_de_monstres_tues += 5
                            Affichage.EntreePourContinuer()
                            print("Vous vous éloignez de la clairière.")
                            Affichage.EntreePourContinuer()
                elif Player.numero_de_letage == 7:
                    print("Vous arrivez dans une salle circulaire, contenant en son centre un piedestal griffoné de centaines de messages sans queue ni tête.")
                    print("Loin au dessus du piedestal, vous apercevez une ouverture cerclée de vieille pierre.")
                    Affichage.EntreePourContinuer()
                    print("Une roche est posée sur le piedestal.")
                    if Player.nom_de_letage != "Douves du Pénitent":
                        print("Elle est enflammée, des dizaines de spectres de feu virevoltant autour d'elle dans une cacophonie de lamentations et d'accusations.")
                    else:
                        print("Elle est en dessous une cascade émanant de l'ouverture de pierre plus haut, et répandant ses eaux sur la totalité de l'étage, noire comme le charbon.")
                    Affichage.EntreePourContinuer()
                    while True:
                        try:
                            print("Que faire ?")
                            print("\n1 - S'éloigner\n2 - Prendre la pierre")
                            choix = int(
                                input("\nChoisissez votre action avec les nombres : ")
                            )
                            ClearConsole()
                            if choix in [1, 2]:
                                break
                        except ValueError:
                            ClearConsole()
                    if choix == 1:
                        print("Vous vous éloignez de la salle.")
                        Affichage.EntreePourContinuer()
                    else:
                        print("Vous vous approchez de la pierre, et posez votre main dessus.")
                        Affichage.EntreePourContinuer()
                        if Player.nom_de_letage == "Douves du Pénitent":
                            print("Alors que vous la sortez de l'eau, sa couleur disparait comme si elle n'était qu'un simple rêve.")
                            Affichage.EntreePourContinuer()
                            print("Vous observez la simple pierre, qui se révèle être un jade intrigant contenant une plus petite roche dorée.")
                            Affichage.EntreePourContinuer()
                            print("Alors que vous la tenez dans votre main, vous jureriez entendre des sanglots autour de vous.")
                            Affichage.EntreePourContinuer()
                            print("Vous obtenez l'artefact [Jade Impardonnable] !")
                            print("La cristallisation de centaines d'années de culpabilité.\nLorsque vous passez votre tour avec tout vos points de mana, vous entrez dans un état de folie pendant 1 tour !")
                            caracteristique_de_la_salle["terminé par joueur"] = True
                            Player.liste_dartefacts_optionels.append("Jade Impardonnable")
                            Affichage.EntreePourContinuer()
                            print("Vous vous éloignez de la salle.")
                            Affichage.EntreePourContinuer()
                        else:
                            print("Alors que vous commencez a grimacer sous l'effet du feu qui enveloppe la pierre....")
                            Affichage.EntreePourContinuer()
                            print("...vous vous rendez compte qu'il ne vous brule pas.")
                            Affichage.EntreePourContinuer()
                            print("Au contraire, il semble apaiser quelque chose de singulier, de primitif, enfoui a l'interieur de votre ADN.")
                            Affichage.EntreePourContinuer()
                            print("Vous sentez en vous un plaisir coupable, ressentit seulement après la réalisation d'une vengence.")
                            Affichage.EntreePourContinuer()
                            print("Un plaisir couplé a une colère grandissante, comme un besoin de prouver une quelquonque supériorité?")
                            Affichage.EntreePourContinuer()
                            print("Vous vous indulgez dans le confort de fortes émotions, et commencez un rire maniaque alors que les spectres de feu dansent autour de vous !")
                            Affichage.EntreePourContinuer()
                            print("...")
                            Affichage.EntreePourContinuer()
                            print("Quand vous reprenez vos esprits, vous êtes a terre, sans vêtements, des marques de brulures scarifiants les murs de la salle comme de la peau sur laquelle on défoulerait ses émotions.")
                            Affichage.EntreePourContinuer()
                            print("Dans votre main gauche, Zeroual avec 10 âmes aborbées d'on ne sait ou.")
                            Affichage.EntreePourContinuer()
                            print("Dans votre main droite, la pierre calcinée du piedestal.")
                            Affichage.EntreePourContinuer()
                            print("Plus aucun feu ne brule dans la salle.")
                            print("Plus aucun spectre ne répandent leur colère.")
                            Affichage.EntreePourContinuer()
                            print("La salle est vide.")
                            Affichage.EntreePourContinuer()
                            print("Vous obtenez l'artefact [Basalte Immonde] !")
                            print("Une roche impure, ayant absorbée les joies d'une colère sans limite pendant des centaines d'années.\nLorsque vous passez votre tour avec tout vos points de mana, vous entrez dans un état de furie pendant 1 tour !")
                            print("De plus, le nombre de monstre que vous avez tué augmente de 10, pour une raison quelquonque !")
                            caracteristique_de_la_salle["terminé par joueur"] = True
                            Player.liste_dartefacts_optionels.append("Basalte Immonde")
                            Player.nombre_de_monstres_tues += 10
                            Affichage.EntreePourContinuer()
                            print("Vous vous rhabillez, et vous éloignez de la salle.")
                            Affichage.EntreePourContinuer()

            elif caracteristique_de_la_salle["type"] == "PUIT":
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.puit()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print("Vous apercevez un puit singulier, fait de vieille pierre.")
                Affichage.EntreePourContinuer()
                if Player.numero_de_letage == 1:
                    print("Au fond de celui-ci, vous apercevez les contours d'un rocher entouré d'un tapis de verdure")
                    Affichage.EntreePourContinuer()
                    print("Dans le seau porté au dessus du précipice par une corde solide se trouve un liquide carmin, visqueux.")
                    Affichage.EntreePourContinuer()
                    while True:
                        try:
                            print("Que faire ?")
                            print("\n1 - S'éloigner du puit\n2 - Boire le contenu du seau\n3 - Vider le seau dans le puit")
                            choix = int(
                                input("\nChoisissez votre action avec les nombres : ")
                            )
                            ClearConsole()
                            if choix in [1, 2, 3]:
                                break
                        except ValueError:
                            ClearConsole()
                    if choix == 1:
                        print("Vous vous éloignez du puit.")
                        Affichage.EntreePourContinuer()
                    elif choix == 2:
                        print("Vous approchez le seau de vos lèvres, et vos narines sont assaillies par une puissante odeur métallique.")
                        Affichage.EntreePourContinuer()
                        print("Vous persévérez, et bientôt le liquide froid coule dans votre gorge...")
                        Affichage.EntreePourContinuer()
                        print("...et c'était très nutritif !\nVous gagnez 5 points de vie max !")
                        caracteristique_de_la_salle["terminé par joueur"] = True
                        Player.points_de_vie += 5
                        Player.points_de_vie_max += 5
                        Affichage.EntreePourContinuer()
                        print("Vous vous éloignez du puit.")
                        Affichage.EntreePourContinuer()
                    elif choix == 3:
                        print("Vous prenez le seau a deux mains, et déversez son contenu dans le puit.")
                        Affichage.EntreePourContinuer()
                        print("Tout au fond, vous apercevez le tapis de verdure se teindre de rouge.")
                        Affichage.EntreePourContinuer()
                        print("Tout a coup, de grandes secousses et un cri a glacer le sang se fait entendre, alors que des racines jaillissent des murs du puit pour en obstruer la vue !")
                        Affichage.EntreePourContinuer()
                        print("Vous avez le terrible sentiment que quelque chose de végétal, en dessous, vient de se réveiller.")
                        Affichage.EntreePourContinuer()
                        print("L E  P R O C H A I N  E T A G E  C H A N G E  D E  P R O P R I E T A I R E\n")
                        caracteristique_de_la_salle["terminé par joueur"] = True
                        Player.etage_alternatif = True
                        Affichage.EntreePourContinuer()
                        print("Vous vous éloignez du puit.")
                        Affichage.EntreePourContinuer()
                elif Player.numero_de_letage == 6:
                    print("Au fond de celui-ci, vous apercevez les contours d'un feu entouré de petites flamelettes qui virevoltent, et entendez des murmures colériques remontant le long des parois du puit.")
                    Affichage.EntreePourContinuer()
                    while True:
                        while True:
                            try:
                                print("Que faire ?")
                                print("\n1 - S'éloigner du puit\n2 - Verser quelque chose dans le puit")
                                choix = int(
                                    input("\nChoisissez votre action avec les nombres : ")
                                )
                                ClearConsole()
                                if choix in [1, 2]:
                                    break
                            except ValueError:
                                ClearConsole()
                        if choix == 1:
                            print("Vous vous éloignez du puit.")
                            Affichage.EntreePourContinuer()
                            break
                        elif choix == 2 and "Larmes de Vénus" in Player.liste_dartefacts_optionels:
                            print("Vous prenez la petite fiole d'eau dans votre main, et la regardez briller doucement.")
                            Affichage.EntreePourContinuer()
                            print("Une fiole de Larme de Vénus permet *d'apaiser les feux de la colère et ne laisse derrière que les ombres de la culpabilité*, hein ?")
                            print("La description n'a pas beaucoup de sens, mais juste le fait de la tenir apaise votre esprit combatif.")
                            Affichage.EntreePourContinuer()
                            print("Vous devissez le joli bouchon de cristal, et versez le contenu de la fiole dans le puit, en essayant de viser le feu tout en bas.")
                            Player.liste_dartefacts_optionels.remove("Larmes de Vénus")
                            Affichage.EntreePourContinuer()
                            print("Vous voyez le feu s'éteindre, les flamelettes disparaitre, et un terrible cri de douleur émaner de tout en bas.")
                            print("Alors que vous vous bouchez les oreille, le bruit se mue en de douloureux sanglots.")
                            print("En même temps, d'épais barreaux de fer sortent des parois du puit, interdisant la descente.")
                            Affichage.EntreePourContinuer()
                            print("Vous avez le sentiment d'avoir changé quelque chose d'immuable, en dessous.")
                            Affichage.EntreePourContinuer()
                            print("L E  P R O C H A I N  E T A G E  C H A N G E  D E  P R O P R I E T A I R E\n")
                            caracteristique_de_la_salle["terminé par joueur"] = True
                            Player.etage_alternatif = True
                            Affichage.EntreePourContinuer()
                            print("Vous vous éloignez du puit.")
                            Affichage.EntreePourContinuer()
                            break
                        else:
                            print("Vous regardez votre inventaire, mais n'avez rien a vider dans le puit.")
                            Affichage.EntreePourContinuer()

            elif caracteristique_de_la_salle["type"] == "LIANE":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.liane()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print(
                    "Parmis les herbes hautes et les racines d'arbres, vous trouvez un petit coffre de bois noir."
                )
                print("Celui-ci est enserré de lianes épaisses.")
                Affichage.EntreePourContinuer()
                # si on a la machette rouillee, on peut liberer le coffre
                if "Machette Rouillée" in Player.liste_dartefacts_optionels:
                    Player.liste_dartefacts_optionels.remove("Machette Rouillée")
                    print(
                        "Vous utilisez une Machette Rouillée sur les lianes, et réussissez"
                        " a en trancher assez pour liberer le coffre, juste avant que la machette ne se brise!"
                    )
                    Affichage.EntreePourContinuer()
                    print("Vous ouvrez le coffre...")
                    Affichage.EntreePourContinuer()
                    # fait que l'event soit finit et ne peut ps etre relancé
                    caracteristique_de_la_salle["terminé par joueur"] = True
                    self.GiveRandomArtefact()
                else:
                    print(
                        "Vous tirez de toutes vos forces sur les lianes, mais elles restent accrochées au coffre."
                    )
                    print("Vous laissez tomber.")
                    Affichage.EntreePourContinuer()
            elif (caracteristique_de_la_salle["type"] == "FAUX SPOT" or  #DONE
                  caracteristique_de_la_salle["type"] == "SPOT"):  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.spot()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print(
                    "Vous pouvez apercevoir, dans le sable, une croix rouge."
                    "\nElle ressemble à ce que l'on peut trouver sur une carte aux trésors !"
                )
                Affichage.EntreePourContinuer()
                # si on a la Vieille Pelle, on peut liberer le coffre
                if "Vieille Pelle" in Player.liste_dartefacts_optionels:
                    Player.liste_dartefacts_optionels.remove("Vieille Pelle")
                    # fait que l'event soit finit et ne peut ps etre relancé
                    caracteristique_de_la_salle["terminé par joueur"] = True
                    Save.SaveTheGameSansAffichage()
                    print(
                        "Vous utilisez une Vieille Pelle pour creuser au centre de la croix, et..."
                    )
                    Affichage.EntreePourContinuer()
                    if caracteristique_de_la_salle["type"] == "SPOT":
                        print("...la brisez sur un petit coffre de bois noir, que vous ouvrez immédiatement !")
                        Affichage.EntreePourContinuer()
                        self.GiveRandomArtefact()
                    else:
                        print("...la brisez sur un morceau de roche dure.")
                        print("Il n'y avait donc rien à trouver ici.")
                        Affichage.EntreePourContinuer()
                else:
                    print(
                        "Vous commencez a creuser avec vos mains, "
                        "mais la chaleur du sable et la difficultée de la tache vous vous convainc d'arrêter."
                    )
                    print("Vous laissez tomber.")
                    Affichage.EntreePourContinuer()
            elif caracteristique_de_la_salle["type"] == "SEQUENCE":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.sequence()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                # determine une sequence aléatoire si yen a pas deja une
                if len(self.liste_sequence) == 0:
                    for _ in range (1, 5):
                        numero_de_salle_aleatoire = random.randint(5, len(self.FloorBlueprint))
                        self.liste_sequence.append(numero_de_salle_aleatoire)
                #print(self.liste_sequence)
                #Affichage.EntreePourContinuer()

                #compare la sequence aux dernieres salles observées par le joueur
                sequence_realisee = False
                if len(self.liste_des_salles_observées) == 4:
                    sequence_realisee = True
                    for numero_de_salle in range(0, 4):
                        if self.liste_des_salles_observées[numero_de_salle] == self.liste_sequence[numero_de_salle]:
                            continue
                        sequence_realisee = False
                
                print("Vous trouvez un des plateaux volants gisant sur le sol, son métal devenu noir comme du charbon.")
                Affichage.EntreePourContinuer()    
                if sequence_realisee:
                    #la main passe a travers les mots du parchemin et retire un artefact 
                    print("Dessus, un parchemin dépictant une allée de bibliothèque aux rangées droites, et dans"
                          " laquelle se trouve un garde qui se prosterne.")
                    print("Vous pouvez apercevoir un petit coffre de bois noir devant lui.")
                    Affichage.EntreePourContinuer()
                    print("Vous tendez la main pour touchez le papier, et vos doigts passent a travers l'image.")
                    Affichage.EntreePourContinuer()
                    print("Vous retirez un coffre du parchemin, et ce dernier s'enflamme !")
                    Affichage.EntreePourContinuer()
                    print("Vous lachez brusquement le parchemin qui disparait alors dans l'air, et ouvrez le coffre...")
                    Affichage.EntreePourContinuer()
                    caracteristique_de_la_salle["terminé par joueur"] = True
                    self.GiveRandomArtefact()
                else:
                    # montre le parchemin avec la séquence
                    print("Dessus, un parchemin dépictant une allée de bibliothèque aux rangées droites, et dans"
                          " laquelle se trouve un garde dont le visage ferme et les bras croisés évoque la rigueur.")
                    print("Vous pouvez apercevoir un petit coffre de bois noir entre ses jambes.")
                    Affichage.EntreePourContinuer()
                    print("En bas du parchemin, il est écrit un poême :")
                    Affichage.EntreePourContinuer()
                    print("*L'Empereur se promène dans son pavillon.*")

                    #position de la premiere salle de la sequence
                    position_x = self.FloorBlueprint[self.liste_sequence[0]]["position_x"]
                    if position_x < 0:
                        commentaire_x = f"moins de {abs(position_x)}"
                    elif position_x == 0:
                        commentaire_x = "son manque de"
                    else:
                        commentaire_x = position_x
                    position_y = self.FloorBlueprint[self.liste_sequence[0]]["position_y"]
                    if position_y < 0:
                        commentaire_y = f"moins de {abs(position_y)}"
                    elif position_y == 0:
                        commentaire_y = "son manque de"
                    else:
                        commentaire_y = position_y
                    print(f"*Il va observer {commentaire_x} carpes et {commentaire_y} roseaux de son étang.*")

                    #position de la deuxieme salle de la sequence
                    position_x = self.FloorBlueprint[self.liste_sequence[1]]["position_x"]
                    if position_x < 0:
                        commentaire_x = f"moins de {abs(position_x)}"
                    elif position_x == 0:
                        commentaire_x = "son manque de"
                    else:
                        commentaire_x = position_x
                    position_y = self.FloorBlueprint[self.liste_sequence[1]]["position_y"]
                    if position_y < 0:
                        commentaire_y = f"moins de {abs(position_y)}"
                    elif position_y == 0:
                        commentaire_y = "son manque de"
                    else:
                        commentaire_y = position_y
                    print(f"*Il va regarder travailler {commentaire_x} cuisiniers et {commentaire_y} servantes dans sa cuisine.*")

                    #position de la troisieme salle de la sequence
                    position_x = self.FloorBlueprint[self.liste_sequence[2]]["position_x"]
                    if position_x < 0:
                        commentaire_x = f"moins de {abs(position_x)}"
                    elif position_x == 0:
                        commentaire_x = "son manque de"
                    else:
                        commentaire_x = position_x
                    position_y = self.FloorBlueprint[self.liste_sequence[2]]["position_y"]
                    if position_y < 0:
                        commentaire_y = f"moins de {abs(position_y)} "
                    elif position_y == 0:
                        commentaire_y = "son manque d'"
                    else:
                        commentaire_y = f"{position_y} "
                    print(f"*Il va admirer {commentaire_x} fleurs et {commentaire_y}arbres dans son jardin.*")

                    #position de la derniere salle de la sequence
                    position_x = self.FloorBlueprint[self.liste_sequence[3]]["position_x"]
                    if position_x < 0:
                        commentaire_x = f"moins de {abs(position_x)}"
                    elif position_x == 0:
                        commentaire_x = "son manque de"
                    else:
                        commentaire_x = position_x
                    position_y = self.FloorBlueprint[self.liste_sequence[3]]["position_y"]
                    if position_y < 0:
                        commentaire_y = f"moins de {abs(position_y)}"
                    elif position_y == 0:
                        commentaire_y = "son manque de"
                    else:
                        commentaire_y = position_y
                    print(f"*Il va lire {commentaire_x} livres et {commentaire_y} comptes-rendus dans sa bibliothèque.*")

                    print("*Puis il jette un oeil a son garde, qui le reconnait et lui offre une preuve de sa fidélité.*")
                    Affichage.EntreePourContinuer()
                    print("Vous reposez le parchemin sur le plateau et repartez.")
                    Affichage.EntreePourContinuer()
            elif caracteristique_de_la_salle["type"] == "DDR":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.ddr()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print("La salle est remplie de jeux d'arcades aux thêmes divers et variés, mais les carcasses de métal et de peinture sont presque toutes inopérables.")
                print("Seule une machine affiche fièrement ses couleurs et son nom en lettres de néon :")
                Affichage.EntreePourContinuer()
                print("""Dance Dance Revolution MAXIMUM OUTPUT!!!""")
                Affichage.EntreePourContinuer()
                print("Sur l'écran, vous pouvez voir plusieurs images de boites de nuits à l'ambiance endiablée "
                          "dans lesquelles sont modélisés des personnages banals aux visages radieux.")
                print("Seul un jeune homme en costume à paillette et pattes d'éléphant se déhanche furieusement sur le dancefloor, un regard vide plaqué sur le visage.")
                Affichage.EntreePourContinuer()
                print("Les scores des différents joueurs se mettent alors a défiler, et a la fin, un message indiquant que celui qui bat le score du joueur en tête sera récompensé.")
                Affichage.EntreePourContinuer()
                print("L'image de profil du joueur n°1 ressemble trait pour trait a celui de l'homme aux pattes d'éléphants.")
                Affichage.EntreePourContinuer()
                while True:
                    try:
                        print("Jouer ? (75 Golds)")
                        print("\n1 - Oui")
                        print("2 - Non")
                        choix = int(
                            input("\nChoisissez votre action avec les nombres : ")
                        )
                        ClearConsole()
                        if choix in [1, 2]:
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 1:
                    if Player.nombre_de_gold >= 75:
                        game_done = self.DanceDanceRevolutionIntroduction()
                        if game_done:
                            mixer.quit()
                            print("La machine explose !")
                            Affichage.EntreePourContinuer()
                            print("Vous faites attention aux morceaux de verre brisés et aux étincelles, et regardez derriere l'écran.")
                            Affichage.EntreePourContinuer()
                            print("Vous trouvez un squelette habillé avec un costume a pailette et des pattes d'éléphants.")
                            Affichage.EntreePourContinuer()
                            print("Entre ses doigts squelettiques, il tient un petit coffre de bois noir.")
                            Affichage.EntreePourContinuer()
                            print("Vous arrachez le coffre du sac d'os et vous empressez de l'ouvrir.")
                            Affichage.EntreePourContinuer()
                            caracteristique_de_la_salle["terminé par joueur"] = True
                            self.GiveRandomArtefact()
                        else:
                            print("Vous vous éloignez de la machine et reprenez votre souffle.")
                            Affichage.EntreePourContinuer()
                        PlayMusicDeLetage()
                    else:
                        print("Vous videz vos poches, mais ne trouvez pas assez d'argent pour jouer.")
                        Affichage.EntreePourContinuer()
                        print("Rapelez vous : L'addiction aux jeux d'argents, c'est une maladie reconnue par l'Association américaine de psychiatrie !")
                        Affichage.EntreePourContinuer()
                        print("Gardez toujours un oeil sur ce qui est véritablement important :")
                        Affichage.EntreePourContinuer()
                        print("L'hydratation.")
                        Affichage.EntreePourContinuer()
                        print("Vous avez bu un verre d'eau ces dernières dix minutes ?")
                        Affichage.EntreePourContinuer()
                        print("Exactement.")
                        Affichage.EntreePourContinuer()
                        print("Allez boire de l'eau.")
                        Affichage.EntreePourContinuer()
                        print(f"Pendant ce temps, {Player.nom_du_personnage} sort de la salle pour éviter les tentations.")
                        Affichage.EntreePourContinuer()
                else:
                    print("Vous regardez les images défiler, et continuez votre chemin.")
                    Affichage.EntreePourContinuer()
            elif caracteristique_de_la_salle["type"] == "BROKEN":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.broken()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print("Vous trouvez une... bien étrange machine.")
                Affichage.EntreePourContinuer()
                print("D'un côté, une jolie horloge de parquet annotée de nombres et références.")
                print("De l'autre, un morceau de taule plié de manière artistique, qui représente un nombre différent selon le point de vue.")
                print("Et au milieu, une sépraration nette, comme si on avait coupé en deux "
                      "les deux machines et qu'on avait recollé ensemble deux bouts de machines différentes.")
                Affichage.EntreePourContinuer()
                print("...?")
                Affichage.EntreePourContinuer()
                print("Ah non.")
                Affichage.EntreePourContinuer()
                print("Pas *collé*.")
                Affichage.EntreePourContinuer()
                print("Juste posé l'un contre l'autre.")
                Affichage.EntreePourContinuer()
                print("Vous poussez le morceau de taule sur le coté, et rentrez votre main dans la cavité derriere le cadran de l'horloge.")
                print("Vous en ressortez un petit coffre de bois noir !")
                Affichage.EntreePourContinuer()
                print("Vous remerciez le manque d'inspiration du développeur, et ouvrez votre coffre gratuit.")
                Affichage.EntreePourContinuer()
                self.GiveRandomArtefact()

                # fait que l'event soit finit et ne peut ps etre relancé
                caracteristique_de_la_salle["terminé par joueur"] = True
            elif caracteristique_de_la_salle["type"] == "PLAQUE PRESSION":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.machine()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print("Vous trouvez un méchanisme ancien !")
                Affichage.EntreePourContinuer()
                print("C'est...")
                Affichage.EntreePourContinuer()
                print("...une plaque de pression.")
                Affichage.EntreePourContinuer()
                print("Vous jettez un regard désespéré à votre pied enfoncé de quelques centimètres dans le sol, et croisez les doigts.")
                Affichage.EntreePourContinuer()
                print(
                    "Aussitot, des arbalètes sournoises, cachées dans les murs, vous criblent de flèches !"
                )
                Affichage.EntreePourContinuer()
                if not ("Sabre du Roi de Glace" in Player.liste_dartefacts_optionels):
                    degat = round(Player.points_de_vie_max * 0.33)
                    Player.points_de_vie -= degat
                    print(f"Vous perdez {degat} points de vie.")
                    Affichage.EntreePourContinuer()
                    if Player.points_de_vie <= 0:
                        mixer.quit()
                        PlaySound("death")
                        print("Vous échouez a stopper le saignement, et perdez la vie.")
                        Affichage.EntreePourContinuer()
                        Affichage.ShowDeath()
                else:
                    print("Cepandant, des éclats de glace se forment aux endroits ou les flèches auraient du se planter.")
                    Affichage.EntreePourContinuer()
                print("Avant que vous n'ayez le temps de comprendre ce qu'il vient de se passer, un gaz violet remplit la salle, vous rendant confus !")
                Affichage.EntreePourContinuer()
                print("Enfin, un monstre tombe du plafond.")
                Affichage.EntreePourContinuer()
                Player.commence_le_combat_confus = True
                control = controleur.Control(Player, Trader)
                # lance la bataille
                try:
                    control.Battle()
                except Exception as error:
                    WriteErrorInErrorLog(error)
                Player.commence_le_combat_confus = False
                PlayMusicDeLetage()
                print("Vous entendez un crissement irrégulier, et la plaque de pression se retrouve bloquée dans sa position.")
                print("Vous n'aurez pas a vous soucier de cette salle davantage.")
                Affichage.EntreePourContinuer()

                # fait que l'event soit finit et ne peut ps etre relancé
                caracteristique_de_la_salle["terminé par joueur"] = True
            elif caracteristique_de_la_salle["type"] == "BOL":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.machine()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                if self.nombre_de_bols == 1:
                    s_ou_pas = ""
                    des_ou_pas = "du"
                else:
                    s_ou_pas = "s"
                    des_ou_pas = "d'un des"
                print("Vous trouvez un méchanisme ancien !")
                Affichage.EntreePourContinuer()
                print("C'est...")
                Affichage.EntreePourContinuer()
                print(f"...{self.nombre_de_bols} bol{s_ou_pas}.")
                Affichage.EntreePourContinuer()
                print(f"En dessous {des_ou_pas} bol{s_ou_pas}, il y a un petit écriteau sur lequel il est marqué :")
                if self.nombre_de_bols == 1:
                    print("*Si vous lisez ceci, veuillez mettre 50 golds dans le bol.*")
                    Affichage.EntreePourContinuer()
                else:
                    print("*Merci pour vos donations !*\n*Grâce à vous, nous avons pu investir dans l'acquisition d'un autre bol !*")
                    Affichage.EntreePourContinuer()
                    print("*Maintenant, veuillez mettre 50 golds dans chacun des bols.*")
                    Affichage.EntreePourContinuer()
                if Player.nombre_de_gold < (self.nombre_de_bols * 50):
                    print(f"Mais vous n'avez même pas {(self.nombre_de_bols * 50)} golds, alors vous mettez tout vos golds dans le{s_ou_pas} bol{s_ou_pas}.")
                    Player.nombre_de_gold = 0
                else:
                    print(f"Dépité, vous mettez {(self.nombre_de_bols * 50)} golds dans le{s_ou_pas} bol{s_ou_pas}.")
                    Player.nombre_de_gold -= (self.nombre_de_bols * 50)
                self.nombre_de_bols += 1
                Affichage.EntreePourContinuer()


            elif caracteristique_de_la_salle["type"] == "JACCUZI":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.machine()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print("Vous trouvez un méchanisme ancien !")
                Affichage.EntreePourContinuer()
                print("C'est...")
                Affichage.EntreePourContinuer()
                print("...un jacuzzi ?")
                Affichage.EntreePourContinuer()
                print("La surface de l'eau est troublée par la présence d'un millier de bulles d'air.")
                print("Des volutes de vapeurs s'échappent du chaudron de bois....")
                print("...et des petits êtres jaunes en forme d'étoile paressent à la surface sur d'étranges ballon de baudruche en forme de donut.")
                Affichage.EntreePourContinuer()
                while True:
                    try:
                        print("L'eau chaude cristalline attire votre corps fatigué par ses blessures.")
                        print("Votre esprit, lui, est attiré par une sorte de free-form jazz reposant chanté par les êtres dorés.")

                        print("\n1 - Rentrer dans le Jacuzzi")
                        print("2 - Repartir")
                        choix = int(input("\nFaites votre choix avec les nombres : "))
                        ClearConsole()
                        if choix in [1, 2]:
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 1:
                    mixer.quit()
                    print("Vous laissez vos habits dans un petit tas à coté, et rentrez doucement dans l'eau chaude du jacuzzi.")
                    Affichage.EntreePourContinuer()
                    PlayMusic("bathhouse")
                    self.ReposDansJacuzzi()
                    PlayMusicDeLetage()
                    print("Vous sortez du jacuzzi, et vous rhabillez.")
                    print("Vous vous sentez plus détendu que jamais !")
                    Player.points_de_vie = Player.points_de_vie_max
                    Player.points_de_mana = Player.points_de_mana_max
                    Affichage.EntreePourContinuer()
                    print("Le jacuzzi s'éteint et une étrange substance noire recouvre sa surface...")
                    Affichage.EntreePourContinuer()
                    print("Votre corps, débarrassé de ses toxines, semble avoir pollué l'eau de l'étrange méchanisme.")
                    print("Vous ne pourrez pas revenir ici.")
                    Affichage.EntreePourContinuer()
                    # fait que l'event soit finit et ne peut ps etre relancé
                    caracteristique_de_la_salle["terminé par joueur"] = True
                else:
                    print("Vous laissez l'étrange structure et repartez d'ou vous venez.")
                    Affichage.EntreePourContinuer()

            elif caracteristique_de_la_salle["type"] == "CHARGEUR":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.machine()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print("Vous trouvez un méchanisme ancien !")
                Affichage.EntreePourContinuer()
                print("C'est...")
                Affichage.EntreePourContinuer()
                print("...une machine a soda ?")
                Affichage.EntreePourContinuer()
                while True:
                    try:
                        print("Vous pouvez vous servir un verre d'une des boissons proposées, sans savoir l'effet que cela aura.")
                        print("\n1 - Boire une boisson aléatoire ")
                        print("2 - Partir")
                        choix = int(input("\nFaites votre choix avec les nombres : "))
                        ClearConsole()
                        if choix in [1, 2]:
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 2:
                    print("Vous laissez la machine et repartez d'ou vous venez.")
                    Affichage.EntreePourContinuer()
                elif choix == 1:
                    print("Vous prenez un gobelet de plastique rouge et le remplissez avec une des boissons proposées.")
                    Affichage.EntreePourContinuer()
                    print("Vous avalez son contenu et...")
                    Affichage.EntreePourContinuer()
                    liste_de_charge_possible = {1: {"Description" : "...ca pétille dans la bouche !\nL'élément [Foudre] à plus de chance de paralyser !", "Effet" : "Element [Foudre] Surchargé"},
                                                2: {"Description" : "...ca pique comme pas possible !\nL'élément [Feu] à plus de chance de bruler !", "Effet" : "Element [Feu] Surchargé"},
                                                3: {"Description" : "...c'est chaud et chocolaté !\nL'élément [Terre] à plus de chance d'infliger la lapidation !", "Effet" : "Element [Terre] Surchargé"},
                                                4: {"Description" : "...un gout de menthe envahit votre palais !\nL'élément [Glace] à plus de chance de geler !", "Effet" : "Element [Glace] Surchargé"},
                                                5: {"Description" : "...ca a un bon gout d'orange !\nL'élément [Sang] à plus de chance de faire un drain !", "Effet" : "Element [Sang] Surchargé"},
                                                6: {"Description" : "...la texture épaisse et le gout de banane vous dégoute un peu.\nVous reprenez 4 points d'endurance supplémentaire quand vous ne faites pas de techniques !", "Effet" : "Element [Corps] Surchargé"},
                                                7: {"Description" : "...c'était alcoolisé. Beurk !\nGagner un combat fait augmenter le compteur de monstres tués de 2 !", "Effet" : "Element [Ame] Surchargé"},}
                    nombre_de_charge_aleatoire = random.randint(1, 7)
                    charge_actuelle = liste_de_charge_possible[nombre_de_charge_aleatoire]
                    print(charge_actuelle["Description"])
                    Affichage.EntreePourContinuer()
                    Player.liste_dartefacts_optionels.append(charge_actuelle["Effet"])
                    print("La machine fait un bruit bizarre, puis un indicateur sur lequel est marqué *EN PANNE* s'allume.")
                    Affichage.EntreePourContinuer()
                    # fait que l'event soit finit et ne peut ps etre relancé
                    caracteristique_de_la_salle["terminé par joueur"] = True

                
            elif caracteristique_de_la_salle["type"] == "ARBRE":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.machine()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print("Vous trouvez un méchanisme ancien !")
                Affichage.EntreePourContinuer()
                print("C'est...")
                Affichage.EntreePourContinuer()
                print("...un grand arbre de métal !")
                Affichage.EntreePourContinuer()
                while True:
                    try:
                        print("Vous pouvez voir des choses pousser au niveau de la canopée.")
                        print("\n1 - Donner un grand coup de pied dans l'arbre")
                        print("2 - Partir")
                        choix = int(input("\nFaites votre choix avec les nombres : "))
                        ClearConsole()
                        if choix in [1, 2]:
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 1:
                    print("Vous donnez votre plus grand coup de pied dans l'arbre, et plusieurs choses tombent a terre.")
                    Affichage.EntreePourContinuer()
                    liste_de_choses = ["Feuille Jindagee", "Fruit Jindagee", "Feuille Aatma", "Fruit Aatma"]
                    liste_de_choses_tombee = []
                    for _ in range (1, 4):
                        nombre_aleatoire = random.randint(0,100)
                        if nombre_aleatoire <= 5 and "Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure" not in liste_de_choses_tombee:
                            liste_de_choses_tombee.append("Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure")
                        else:
                            chose_aleatoire = random.randint(0, 3)
                            liste_de_choses_tombee.append(liste_de_choses[chose_aleatoire])
                    print(f"Vous récuperez les objets [{liste_de_choses_tombee[0]}] [{liste_de_choses_tombee[1]}] et [{liste_de_choses_tombee[2]}] !")
                    for item in liste_de_choses_tombee:
                        if item == "Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure":
                            Player.liste_dartefacts_optionels.append("Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure")
                        else:
                            Player.items_possedes[item] += 1
                    Affichage.EntreePourContinuer()
                    print("L'arbre n'a plus rien a offrir.")
                    Affichage.EntreePourContinuer()
                    # fait que l'event soit finit et ne peut ps etre relancé
                    caracteristique_de_la_salle["terminé par joueur"] = True
                elif choix == 2:
                    print("Vous laissez l'arbre tranquille et repartez dans un silence troublé seulement par le bruit du vent dans les feuilles et du bois qui se balance doucement.")
                    Affichage.EntreePourContinuer()
                
            elif caracteristique_de_la_salle["type"] == "DISTRIBUTEUR":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.machine()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print("Vous trouvez un méchanisme ancien !")
                Affichage.EntreePourContinuer()
                print("C'est...")
                Affichage.EntreePourContinuer()
                print("...un distributeur !")
                Affichage.EntreePourContinuer()
                while True:
                    while True:
                        try:
                            print("Vous pouvez voir une fente pour inserer de l'argent, et une jolie sélection d'artefacts derrière la vitre.")
                            print("Un avertissement écrit en petit caractères prévient de la casse (presque) inévitable des artefacts présents a chaque changement d'étage.")
                            print(f"Vous avez {Player.nombre_de_gold} golds sur vous.")
                            print(f"\n1 - Acheter [Epée de Damocles] pour {Player.numero_de_letage * 30} golds") #15 % de dmg, 2% chance que ca brise et fasse 15% vie
                            print(f"2 - Acheter [Morceau d'Ether Fragile] pour {Player.numero_de_letage * 30} golds") #15 % de sorts, 2% chance que ca brise et vide toute mana
                            print(f"3 - Acheter [Eau Bénite] pour {Player.numero_de_letage * 60} golds") #5% chance d'etre béni pas tour
                            print(f"4 - Acheter [Bandeau Catharsis] pour {Player.numero_de_letage * 45} golds") #5% cahnce esquive, prend 10% degat en plus
                            print(f"5 - Acheter [Charbon Primordial] pour {Player.numero_de_letage * 50} golds") #+1 tour de brulure
                            print(f"6 - Acheter [Saphir de Gel] pour {Player.numero_de_letage * 50} golds") #+1 tour de gel
                            print(f"7 - Acheter [Fossile Figé] pour {Player.numero_de_letage * 50} golds") #+5% chance de faire lapidation
                            print(f"8 - Acheter [Fiole d'Eclair] pour {Player.numero_de_letage * 50} golds") #+5% chance de faire paralysie
                            print(f"9 - Acheter [Assurance Distributeur] pour {Player.numero_de_letage * 50} golds") #+garde les items 1 etage supplementaire
                            print("10 - Partir")
                            choix = int(input("\nFaites votre choix avec les nombres : "))
                            ClearConsole()
                            if choix in range(1, 11):
                                break
                        except ValueError:
                            ClearConsole()
                    if choix == 10:
                        print("Vous laissez le distributeur, non sans tenter de trouver des golds en dessous (Il n'y en avait pas).")
                        Affichage.EntreePourContinuer()
                        break
                    else:
                        dictionaire_item_distributeur = {1 : {"Nom" : "Epée de Damocles", "Prix" : (Player.numero_de_letage * 30), "Description" : "Une épée suintant l'anxiété, ayant appartenue a un ancien roi.\nLes dégâts de vos techniques augmentent de 25%, mais il y a une faible probabilité que l'artefact vous tombe dessus, se brisant sur votre crane et vous infligeant de lourds dégâts."},
                                                         2 : {"Nom" : "Morceau d'Ether Fragile", "Prix" : (Player.numero_de_letage * 30), "Description" : "Un catalyste pour les sorts très fragile, extrait directement de la fabrique de la réalité.\nLes dégâts de vos sorts augmentent de 25%, mais il y a une faible probabilité que l'artefact se brise spontanément, vous vidant alors de tout vos points de mana."},
                                                         3 : {"Nom" : "Eau Bénite", "Prix" : (Player.numero_de_letage * 60), "Description" : "Une fiole légendaire devant laquelle des papes dévoués ont prié jours et nuits pendant 50 ans d'affilée.\nVous avez une faible chance d'être béni par le Feu Divin à la fin de chaque tours."},
                                                         4 : {"Nom" : "Bandeau Catharsis", "Prix" : (Player.numero_de_letage * 45), "Description" : "Un bandeau magique a se mettre devant les yeux, afin d'affuter les sens.\nVos chances d'esquive augmentent, ainsi que les dégats que l'on vous inflige."},
                                                         5 : {"Nom" : "Charbon Primordial", "Prix" : (Player.numero_de_letage * 50), "Description" : "Un reste du tout premier feu de bois, enseigné par Promethée aux humains.\nL'effet Brulure que vous infligez dure 1 tour de plus."},
                                                         6 : {"Nom" : "Saphir de Gel", "Prix" : (Player.numero_de_letage * 50), "Description" : "La culmination de millénaires de pression par la neige sur un morceau de neige du tout premier age glaciaire .\nL'effet Gel que vous infligez dure 1 tour de plus."},
                                                         7 : {"Nom" : "Fossile Figé", "Prix" : (Player.numero_de_letage * 50), "Description" : "Le fossile d'un animal rare vivant il y a des millions d'années de ca, débordant de vitalité, que seul le processus de diagénèse autour de lui a su arrêter.\nL'effet Lapidation a un peu plus de chance de réussir."},
                                                         8 : {"Nom" : "Fiole d'Eclair", "Prix" : (Player.numero_de_letage * 50), "Description" : "Un des éclairs de Zeus, jalousement gardé par un humain qui avait réussi a l'enfermer dans une amphore vide de vin, que le dieu de la foudre à oublié sur terre lors de sa dernière échappée avec la femme de l'humain en question.\nL'effet Paralysie a un peu plus de chance de réussir.  "},
                                                         9 : {"Nom" : "Assurance Distributeur", "Prix" : (Player.numero_de_letage * 50), "Description" : "Un bout de papier assurant a son porteur que les artefacts qu'il a acheté au distributeur ne se briseront pas pour 1 changement d'étage.\nVous pouvez en acheter plusieurs bien sur !"}}
                        item_choisi = dictionaire_item_distributeur[choix]
                        if Player.nombre_de_gold < item_choisi["Prix"]:
                            print("Vous n'avez pas assez d'argent !")
                            Affichage.EntreePourContinuer()
                        else:
                            Player.nombre_de_gold -= item_choisi["Prix"]
                            Player.liste_dartefacts_optionels.append(item_choisi["Nom"])
                            print("Vous inserez l'argent dans la machine, tapez le code sur le clavier numérique, et patientez quelques instants.")
                            time.sleep(10)
                            Affichage.EntreePourContinuer()
                            print("L'artefact tombe enfin dans la chute, et vous pouvez le récuperer.")
                            Affichage.EntreePourContinuer()
                            print(f"Vous obtenez l'artefact [{item_choisi['Nom']}] !")
                            print(item_choisi["Description"])
                            Affichage.EntreePourContinuer()

            elif caracteristique_de_la_salle["type"] == "CHENIL":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.machine()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print("Vous trouvez un méchanisme ancien !")
                Affichage.EntreePourContinuer()
                print("C'est...")
                Affichage.EntreePourContinuer()
                print("...une jolie niche rose fermée !")
                Affichage.EntreePourContinuer()
                while True:
                    try:
                        print("Vous pouvez voir une fente pour inserer de l'argent, et un panneau juste en dessous lit :\n* CHIEN AUTONOME de NACRE ININFLAMMABLE GARDANT et OBEISSANT son UTILISATEUR : 100 golds *")
                        print("\n1 - Mettre les golds dans la fente")
                        print("2 - Partir")
                        choix = int(input("\nFaites votre choix avec les nombres : "))
                        ClearConsole()
                        if choix in [1, 2]:
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 2:
                    print("Vous pensez a votre bourse et refusez cet achat compulsif.")
                    Affichage.EntreePourContinuer()
                elif choix == 1:
                    if Player.nombre_de_gold >= 100:
                        print("Vous pensez a votre bourse et vous indulgez dans cet achat compulsif.")
                        Affichage.EntreePourContinuer()
                        print("Au bout du 100eme goold inséré, la porte de la niche s'ouvre et un chien bionique en sort !")
                        Affichage.EntreePourContinuer()
                        print("Ce dernier, relié a un tuyau greffé dans son cou, ouvre doucement les yeux et vous regarde d'un air exalté !")
                        Affichage.EntreePourContinuer()
                        print("Alors qu'il se frotte a vos jambes et a votre main, vous le décrochez de sa station de vie artificielle et trouvez un collier contenant son nom en lettres manuscriptes :")
                        Affichage.EntreePourContinuer()
                        print("C.A.N.I.G.O.U.")
                        Affichage.EntreePourContinuer()
                        print("Vous obtenez Canigou !")
                        print("Ce chien a moitié cyborg fait des dégâts a vos ennemis a chaque fin de tour !")
                        Player.nombre_de_gold -= 100
                        Player.liste_dartefacts_optionels.append("Canigou")
                        Affichage.EntreePourContinuer()
                        print("Vous sortez de la salle avec votre nouveau compagnon.")
                        Affichage.EntreePourContinuer()
                        # fait que l'event soit finit et ne peut ps etre relancé
                        caracteristique_de_la_salle["terminé par joueur"] = True
                    else:
                        print("Vous regardez votre bourse avec insistance, mais aucun gold supplémentaire n'apparait.")
                        Affichage.EntreePourContinuer()
                        print("Décu, vous tournez les talons et sortez de la salle.")
                        Affichage.EntreePourContinuer()

            elif caracteristique_de_la_salle["type"] == "BUFFET":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.machine()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print("Vous trouvez un méchanisme ancien !")
                Affichage.EntreePourContinuer()
                print("C'est...")
                Affichage.EntreePourContinuer()
                print("...un buffet a volonté !")
                Affichage.EntreePourContinuer()
                print("Ou plutot un faux buffet, vu que toute la nourriture est faite de plastique.")
                Affichage.EntreePourContinuer()
                while True:
                    try:
                        print("Au centre de la table, une réplique de la corne d'abondance semble attirer votre regard.")
                        print("\n1 - Mettre votre main dans la corne")
                        print("2 - Partir")
                        choix = int(input("\nFaites votre choix avec les nombres : "))
                        ClearConsole()
                        if choix in [1, 2]:
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 2:
                    print("Vous laissez la scène en place et repartez, une petite faim commencant a pointer le bout de son nez.")
                    Affichage.EntreePourContinuer()
                elif choix == 1:
                    print("Vous plongez votre main dans la corne d'abondance, et sentez votre énergie diminuer.")
                    print("Vous perdez 10 points de vie et de mana max !")
                    Affichage.EntreePourContinuer()
                    print("Cepandant, vous arrivez à ressortir de la corne une suite d'objets aléatoires, accrochés les uns aux autres par un fil de laine rouge.")
                    Affichage.EntreePourContinuer()
                    liste_ditem_possibles = LISTEITEM
                    liste_ditem_possibles.append("Redcoin")
                    liste_ditem_recus = []
                    for _ in range (1,6):
                        nom_de_litem = GetRandomItemFromList(liste_ditem_possibles)
                        if nom_de_litem == "Redcoin":
                            Player.nombre_de_red_coin += 1
                        else:
                            Player.items_possedes[nom_de_litem] += 1
                        liste_ditem_recus.append(nom_de_litem)
                    print(f"Vous obtenez les objets {liste_ditem_recus} !")
                    Affichage.EntreePourContinuer()
                    print("La corne se brise alors subitement, et la nourriture sur la table semble pourrir de manière accélérée.")
                    Affichage.EntreePourContinuer()
                    # fait que l'event soit finit et ne peut ps etre relancé
                    caracteristique_de_la_salle["terminé par joueur"] = True
                    Player.points_de_mana_max -= 10
                    if Player.points_de_mana_max < 0 :
                        Player.points_de_mana_max = 0
                    if Player.points_de_mana > Player.points_de_mana_max :
                        Player.points_de_mana == Player.points_de_mana_max
                    Player.points_de_vie_max -= 10
                    if Player.points_de_vie_max < 1 :
                        Player.points_de_vie_max = 1
                    if Player.points_de_vie > Player.points_de_vie_max :
                        Player.points_de_vie == Player.points_de_vie_max
                    
            elif caracteristique_de_la_salle["type"] == "SPAWNER":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.machine()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print("Vous trouvez un méchanisme ancien !")
                Affichage.EntreePourContinuer()
                print("C'est...")
                Affichage.EntreePourContinuer()
                print("...difficile à décrire...")
                Affichage.EntreePourContinuer()
                print("On dirait une cage de métal dans laquelle dansent des flammes.\nIl y a une fente dessus, et vous sentez les âmes absorbées par Zeroual réagir au méchanisme.")
                Affichage.EntreePourContinuer()
                while True:
                    while True:
                        try:
                            print(f"Vous pouvez dépenser une partie de vos {Player.nombre_de_monstres_tues} âmes pour faire... quelque chose ?")
                            print("\n1 - Dépenser 5 âmes")
                            print("2 - Dépenser 12 âmes")
                            print("3 - Dépenser 20 âmes")
                            print("4 - Partir")
                            choix = int(input("\nFaites votre choix avec les nombres : "))
                            ClearConsole()
                            if choix in range(1, 5):
                                break
                        except ValueError:
                            ClearConsole()
                    if ((choix == 1 and Player.nombre_de_monstres_tues >= 5) or 
                        (choix == 2 and Player.nombre_de_monstres_tues >= 12) or 
                        (choix == 3 and Player.nombre_de_monstres_tues >= 20)):
                        if choix == 1 :
                            Player.nombre_de_monstres_tues -= 5
                            Player.nombre_dennemis_a_letage += 5
                        elif choix == 2 :
                            Player.nombre_dennemis_a_letage += 10
                            Player.nombre_de_monstres_tues -= 12 
                        elif choix == 3 :
                            Player.nombre_dennemis_a_letage += 17
                            Player.nombre_de_monstres_tues -= 20
                        print("Vous approchez Zeroual de la fente, et l'arme prend la forme d'une clé a motif de crâne.")
                        print("Vous insérez la clé dans la fente et...")
                        Affichage.EntreePourContinuer()
                        print("...vous la tournez.")
                        Affichage.EntreePourContinuer()
                        print("Vous sentez quelque chose sortir de Zeroual, et rejoindre les flammes a l'interieur de la cage.")
                        print("Dans le plus grand des silences, la cage s'ouvre de tout les côtés, comme un cube de papier pour laquelle la colle n'aurait pas tenue, et les flammes sortent de la salle en virevoltant !")
                        Affichage.EntreePourContinuer()
                        print("Une idée résonne alors dans votre esprit, comme induite par Zeroual :")
                        Affichage.EntreePourContinuer()
                        print("*ARENE*")
                        Affichage.EntreePourContinuer()
                        # fait que l'event soit finit et ne peut ps etre relancé
                        caracteristique_de_la_salle["terminé par joueur"] = True
                        break
                    elif choix == 4:
                        print("Vous regardez, comme hypnotisé, la danse magestueuse des flammes dans la cage, et décidez de vous en aller.")
                        Affichage.EntreePourContinuer()
                        break
                    else:
                        print("Vous approchez Zeroual de la fente, et l'arme prend la forme d'une clé a motif de crâne.")
                        print("Vous insérez la clef dans la fente et...")
                        Affichage.EntreePourContinuer()
                        print("...rien ne se passe.")
                        Affichage.EntreePourContinuer()
                        print("On dirait que vous n'aviez pas assez d'âmes.")
                        Affichage.EntreePourContinuer()
            elif caracteristique_de_la_salle["type"] == "LEVIER":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.machine()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                print("Vous trouvez un méchanisme ancien !")
                Affichage.EntreePourContinuer()
                print("C'est...")
                Affichage.EntreePourContinuer()
                print("...un levier !")
                Affichage.EntreePourContinuer()
                print("Littéralement.\nUn simple levier placé au centre de la salle, sur un piedestal de verre.")
                Affichage.EntreePourContinuer()
                while True:
                    try:
                        print("Tout peut arriver.")
                        print("\n1 - Tirer le levier")
                        print("2 - Partir")
                        choix = int(input("\nFaites votre choix avec les nombres : "))
                        ClearConsole()
                        if choix in [1, 2]:
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 2:
                    print("Il n'y a aucune raison de tirer ce levier suspicieux.\nVraiment.\nAucune.\nEn plus c'est surement un piège.")
                    Affichage.EntreePourContinuer()
                    print("Vous laissez ce levier tranquille, rempli de cette assurance sur vos choix et actions, vous sentant intelligent comme personne !")
                    Affichage.EntreePourContinuer()
                    print("Et si vous aviez tiré le levier ?\nVous auriez pu avoir tant de choses...\nPlus tard, sur votre lit de mort, c'est la dernière pensée qui traversera votre esprit.")
                    Affichage.EntreePourContinuer()
                    print("Ou pas ?\nQui sait.\nPas vous en tout cas, vu que vous n'avez pas tiré le levier.")
                    Affichage.EntreePourContinuer()
                if choix == 1:
                    print("Vous avancez gaiement, sautillant de pas en pas, jusqu'à atteindre le magnifique et tentateur levier au milieu de la salle.")
                    Affichage.EntreePourContinuer()
                    print("Qui sait ce qui se serait passé si vous ne l'aviez pas tiré ?\nVous l'auriez sans doute regretté sur votre lit de mort.")
                    Affichage.EntreePourContinuer()
                    print("Ou pas ?\nQui sait.\nPas vous en tout cas, vu que vous allez tirer le levier !")
                    Affichage.EntreePourContinuer()
                    print("Vous posez fermement vos mains sur le levier, tirez dessus, et...")
                    Affichage.EntreePourContinuer()
                    effet_aleatoire = random.randint(1, 10)
                    if effet_aleatoire == 1 :
                        print("...rien ne se passe.")
                        Affichage.EntreePourContinuer()
                        print("C'est vraiment nul.")
                        Affichage.EntreePourContinuer()
                    elif effet_aleatoire == 2:
                        print("...le sol s'ouvre sous vos pieds !\nCa devait être le mauvais levier !")
                        Affichage.EntreePourContinuer()
                        print("Vous tombez dans le trou béant, glissez sur la pierre fraiche pendant une vingtaine de minute, et atterissez...")
                        Affichage.EntreePourContinuer()
                        print("...au centre de l'arène !")
                        Player.position_x = 0
                        Player.position_y = 0
                        Player.numero_de_la_salle = 1
                        self.UpdatePlayerPosition()
                        Affichage.EntreePourContinuer()
                    elif effet_aleatoire == 3:
                        print("...un monstre de niveau superieur apparait !")
                        Affichage.EntreePourContinuer()
                        Player.player_tags.append("Monstre De Niveau Superieur")
                        control = controleur.Control(Player, Trader)
                        # lance la bataille
                        try:
                            control.Battle()
                        except Exception as error:
                            WriteErrorInErrorLog(error)
                        Player.player_tags.remove("Monstre De Niveau Superieur")
                        PlayMusicDeLetage()
                    elif effet_aleatoire == 4:
                        print(
                            "...des arbalètes sournoises, cachées dans les murs, vous criblent de flèches !"
                        )
                        Affichage.EntreePourContinuer()
                        if not ("Sabre du Roi de Glace" in Player.liste_dartefacts_optionels):
                            degat = round(Player.points_de_vie_max * 0.33)
                            Player.points_de_vie -= degat
                            print(f"Vous perdez {degat} points de vie.")
                            Affichage.EntreePourContinuer()
                            if Player.points_de_vie <= 0:
                                mixer.quit()
                                PlaySound("death")
                                print("Vous échouez a stopper le saignement, et perdez la vie.")
                                Affichage.EntreePourContinuer()
                                Affichage.ShowDeath()
                        else:
                            print("Cepandant, des éclats de glace se forment aux endroits ou les flèches auraient du se planter.")
                            Affichage.EntreePourContinuer()
                    elif effet_aleatoire == 5:
                        print("...un petit coffre tombe du plafond et rebondit sur le sol !")
                        Affichage.EntreePourContinuer()
                        print("Enfin, sur votre tête, puis sur le sol.")
                        Affichage.EntreePourContinuer()
                        nom_de_litem = GetRandomItemFromList(LISTEITEM)
                        Player.items_possedes[nom_de_litem] += 1
                        print(f"A l'interieur, vous trouvez l'objet {nom_de_litem}")
                        Affichage.EntreePourContinuer()
                    elif effet_aleatoire == 6:
                        print("...rien ne se passe.")
                        Affichage.EntreePourContinuer()
                        print("C'est vraiment nul.")
                        Affichage.EntreePourContinuer()
                        print("Au moment ou vous tournez le dos au méchanisme, vous voyez une figure fantomatique s'approcher de vous !")
                        Affichage.EntreePourContinuer()
                        print("La chose porte un casque de chantier jaune, un pantalon bleu a bretelle, et un visage pâle et fatigué.")
                        Affichage.EntreePourContinuer()
                        print("*Ouai, ouai, je sais.*")
                        Affichage.EntreePourContinuer()
                        print("L'ingénieur se rapproche de vous et vous tend quelque chose.")
                        print("*C'était sensé faire tomber des araignées du plafond, mais, héhé, elles sont toutes mortes. Prend ca comme compensation.*")
                        Affichage.EntreePourContinuer()
                        print("Vous obtenez un Redcoin !")
                        Affichage.EntreePourContinuer()
                        print("Aussitot, un souffle de vent vous pousse en dehors de la salle.")
                        print("*Fiche moi le camp pronto, j'ai un truc à réparer.*")
                        Affichage.EntreePourContinuer()
                    elif effet_aleatoire == 7:
                        print("...une petite boite noire se materialise *dans* le piedestal !")
                        print("Vous brisez le verre pour récuperer la boite, et l'ouvrez.")
                        Affichage.EntreePourContinuer()
                        self.GiveRandomArtefact()
                    elif effet_aleatoire == 8:
                        print("...un monstre apparait !")
                        Affichage.EntreePourContinuer()
                        control = controleur.Control(Player, Trader)
                        # lance la bataille
                        try:
                            control.Battle()
                        except Exception as error:
                            WriteErrorInErrorLog(error)
                        PlayMusicDeLetage()
                    elif effet_aleatoire == 9:
                        print("...un orbe bleu apparait !")
                        print("Il flotte jusqu'à vous, et rentre dans votre poitrine.")
                        Affichage.EntreePourContinuer()
                        print("Vous gagnez 7 points de vie/mana max !")
                        Player.points_de_vie_max += 7
                        Player.points_de_mana_max += 7
                        Affichage.EntreePourContinuer()
                    elif effet_aleatoire == 10:
                        print("...vous entendez le son caractéristique d'une mèche d'explosif qui s'allume !")
                        print("Vous sortez de la salle en courant, et bientot cette dernière disparait dans l'explosion d'une ccentaine de paquets de tnt !")
                        print("Pris dans l'explosion, vous êtes projetés de plusieurs mètres en avant dans un mur, laissant sur ce dernier une indentation en forme de vous !")
                        if not ("Sabre du Roi de Glace" in Player.liste_dartefacts_optionels):
                            degat = round(Player.points_de_vie_max * 0.66)
                            Player.points_de_vie -= degat
                            print(f"Vous perdez {degat} points de vie.")
                            Affichage.EntreePourContinuer()
                            if Player.points_de_vie <= 0:
                                mixer.quit()
                                PlaySound("death")
                                print("Vous ne vous releverez jamais de cette explosion.")
                                Affichage.EntreePourContinuer()
                                Affichage.ShowDeath()
                        else:
                            print("Cepandant, alors que vous vous relevez, vous vous rendez compte que votre corps tout entier était recouvert d'une épaisse armure de glace qui a absorbé le choc.")
                            Affichage.EntreePourContinuer()
                    print("Au final, est ce que ca valait le coup de tirer le levier ?")
                    Affichage.EntreePourContinuer()
                    print("Seul vous peut en décider.")
                    Affichage.EntreePourContinuer()
                    # fait que l'event soit finit et ne peut ps etre relancé
                    caracteristique_de_la_salle["terminé par joueur"] = True
            elif caracteristique_de_la_salle["type"] == "BOSS":
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    print("Vous rentrez dans une salle bien plus grande que d'habitude, tapissée de verdure et d'arbres, comme si vous étiez dehors, et...")
                    Affichage.EntreePourContinuer()
                    print("...")
                    Affichage.EntreePourContinuer()
                    print("...")
                    Affichage.EntreePourContinuer()
                    print("Il y a une cascade.")
                    Affichage.EntreePourContinuer()
                    print("...")
                    Affichage.EntreePourContinuer()
                    print("...")
                    Affichage.EntreePourContinuer()
                    print("Vous allez bien evidemment derrière la cascade.")
                    Affichage.EntreePourContinuer()
                    Draw.boss()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True
                print("Vous trouvez une porte de pierre taillée derrière une cascade.")
                Affichage.EntreePourContinuer()
                print("Vous pouvez y voir des symboles différents dans des cercles de pierre, tous reliés a un cercle plus grand, en hauteur.")
                Affichage.EntreePourContinuer()
                print("En dessous, 50 emplacements de taille bien plus petite, ressemblant a des redcoins.")
                Affichage.EntreePourContinuer()
                donnees_de_s0ve = Observation.GetPermanentThingsFromS0ve() 
                redcoins_inseres = ast.literal_eval(donnees_de_s0ve["Redcoins Inseres"])

                while True:
                    while True:
                        try:
                            print(f"{redcoins_inseres} redcoins sont dans leurs emplacements.")
                            if ((redcoins_inseres == 50 and Player.nom_du_personnage == "Terah")
                                or
                                Player.death_divinity
                            ):
                                print("La porte est ouverte.")
                                print("\n1 - Passer la porte.")
                            else:
                                print("La porte est fermée.")
                                print(f"\n1 - Poser tout les redcoins dans leurs emplacements [{Player.nombre_de_red_coin}]")
                            print("2 - Observer la porte")
                            print("3 - Partir")
                            choix = int(input("\nFaire votre choix avec les nombres : "))
                            ClearConsole()
                            if choix in range(1, 4):
                                break
                        except ValueError:
                            ClearConsole()
                    if choix == 3:
                        print("Vous laissez la porte et retournez sur vos pas.")
                        Affichage.EntreePourContinuer()
                        break
                    elif choix == 2:
                        Ending.PrintEtEntreePourContinuer("Vous regardez les symboles de plus près :")
                        Ending.PrintEtEntreePourContinuer("Un nuage de fumée s'échappant d'un personnage fou.")
                        Ending.PrintEtEntreePourContinuer("Une petite cane de pharaon entourée de 2 totems.")
                        Ending.PrintEtEntreePourContinuer("Un couteau de cuisine.")
                        Ending.PrintEtEntreePourContinuer("Un gluant avec une couronne.")
                        Ending.PrintEtEntreePourContinuer("Une hache prise dans la glace.")
                        Ending.PrintEtEntreePourContinuer("Une figure encapuchonnée.")
                        Ending.PrintEtEntreePourContinuer("Un personnage entouré de 4 autres.")
                        Ending.PrintEtEntreePourContinuer("Un personnage similaire, avec un sourire sanguinaire.")
                        Ending.PrintEtEntreePourContinuer("Une boule sur laquelle se trouve plusieurs visages en peine.")
                        Ending.PrintEtEntreePourContinuer("Et ces symboles sont relié a un grand levé/couché de soleil surmonté de vagues.")
                        Ending.PrintEtEntreePourContinuer("?")
                        Ending.PrintEtEntreePourContinuer("Vous pouvez voir, dans un coin de la porte, un message gravé a la hate :")
                        Ending.PrintEtEntreePourContinuer("*Entend ma voix, enfant maudit.*")
                    elif choix == 1:
                        if (redcoins_inseres == 50 and Player.nom_du_personnage == "Terah") or Player.death_divinity:
                            while True:
                                while True:
                                    try:
                                        print("Êtes vous sûr ?\n(La difficultée augmente drastiquement, et vous ne pourrez pas revenir en arrière.)")
                                        print("\n1 - Oui")
                                        print("2 - Non")
                                        choix = int(input("Faites votre choix avec les nombres : "))
                                        ClearConsole()
                                        if choix in [1, 2]:
                                            break
                                    except ValueError:
                                        ClearConsole()
                                if choix == 1:
                                    Player.position_x = 0
                                    Player.position_y = 0
                                    self.UpdatePlayerPosition()
                                    Player.numero_de_la_salle = 1
                                    Player.etage_alternatif = True
                                    Player.numero_de_letage -= 1
                                    Player.player_tags.append("Passe La Porte Redcoin")
                                    DoBossOrGoDown()
                                    break
                                else:
                                    break
                            if "Passe La Porte Redcoin" in Player.player_tags :
                                break
                        elif redcoins_inseres != 50:
                            redcoins_inseres += Player.nombre_de_red_coin
                            if redcoins_inseres > 50:
                                redcoins_inseres = 50
                            

                            donnees_de_s0ve["Redcoins Inseres"] = redcoins_inseres
                            Observation.SetPermanentThingsToS0ve(donnees_de_s0ve)
                            

                            print(f"Vous posez {Player.nombre_de_red_coin} redcoins dans les emplacements.")
                            Player.nombre_de_red_coin = 0
                            Save.SaveTheGameSansAffichage()
                            Affichage.EntreePourContinuer()

                        else:
                            print("Les redcoins sont déja tous placés.")
                            Affichage.EntreePourContinuer()
                    if "Passe La Porte Redcoin" in Player.player_tags :
                        break
                        
                        

            elif caracteristique_de_la_salle["type"] == "RITUEL":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.rituel()
                    self.UseMonocleDeVerite()
                    caracteristique_de_la_salle["marqué sur la carte"] = True

                if not "Griffes du Démon" in Player.techniques_possedes:
                    print("Vous trouvez un autel de pierre tailladée, sur lequel repose un gobelet doré.")
                    print("Alors que vous prenez le gobelet dans vos mains, vous entendez une voix résonner dans votre tête :")
                    Affichage.EntreePourContinuer()
                    print("*Met en jeu ton âme.*")
                    print("*Exécute avec les mains de l'Innomable.*")
                    print("*J'ornerais ton corps avec celui des morts.*")
                    Affichage.EntreePourContinuer()
                    print("...")
                    Affichage.EntreePourContinuer()
                    print("Le gobelet se remplit de #???!!## .")
                    Affichage.EntreePourContinuer()
                    while True:
                        try:
                            print("Boire le contenu du gobelet ?")
                            print("\n1 - Oui")
                            print("2 - Non")
                            choix = int(
                            input("\nChoisissez votre action avec les nombres : ")
                            )
                            ClearConsole()
                            if choix in [1, 2]:
                                break
                        except ValueError:
                            ClearConsole()
                    if choix == 1:
                        print("Vous avalez le contenu du gobelet.")
                        print("Votre main devient plus sombre, et une énergie noire sort de vos ongles.")
                        Affichage.EntreePourContinuer()
                        print("Vous apprenez la technique [Griffes du Démon] !")
                        Player.techniques_possedes.append("Griffes du Démon")
                        Affichage.EntreePourContinuer()
                        if "Syra" in Player.liste_dartefacts_optionels:
                            print("Grace au verre de Syra que vous avez bu, vous gagnez aussi 10 pm max !")
                            Player.points_de_mana += 10
                            Player.points_de_mana_max += 10
                            Affichage.EntreePourContinuer()
                        print("Vous sentez quelque chose fretiller dans votre abdomen, puis planter ses griffes dans les parois de votre estomac.")
                        Affichage.EntreePourContinuer()
                        print("Vous perdez 20 points de vie et mana max !")
                        Player.points_de_vie_max -= 20
                        if Player.points_de_vie_max <= 0:
                            Player.points_de_vie_max = 1
                        if Player.points_de_vie > Player.points_de_vie_max:
                            Player.points_de_vie = Player.points_de_vie_max
                        Player.points_de_mana_max -= 20
                        if Player.points_de_mana_max <= 0:
                            Player.points_de_mana_max = 1
                        if Player.points_de_mana > Player.points_de_mana_max:
                            Player.points_de_mana = Player.points_de_mana_max
                        Affichage.EntreePourContinuer()
                        print("*Chaines.*")
                        Affichage.EntreePourContinuer()
                        print("*Confitions de ta libération ?*")
                        print("*Reviens dans quelques instants.*")
                        Affichage.EntreePourContinuer()
                        print("Vous vous éloignez de l'autel, mais le sentez changer derrière votre dos.")
                        Affichage.EntreePourContinuer()
                    else:
                        print("Vous reposez le gobelet sur l'autel, et vous en éloignez.")
                        Affichage.EntreePourContinuer()
                else:
                    print("Vous vous approchez de l'autel, et posez votre main dessus.")
                    print("Des lettres apparaissent alors dans les airs, tremblottantes comme une flamme devant la tempête.")
                    Affichage.EntreePourContinuer()
                    while True:
                        while True:
                            try:
                                print("        -{ AUTEL DEMONIAQUE }-")
                                print("     -= Offrande de Sacrifices =-")
                                print(f"\n        SACRIFICES ? {Player.nombre_de_sacrifices}.\n")
                                print("       1 - RICHESSE ? 3.")
                                print("            2 - VIE ? 3.")
                                print("           3 - SANG ? 5.")
                                print("         4 - DESTIN ? 5")
                                print("        5 - POUVOIR ? 10.")
                                print("        6 - LÂCHETÉ ? 0.")
                                print("     7 - LIBERATION ? 5.")
                                choix = int(
                                input("\nChoisissez votre action avec les nombres : ")
                                )
                                ClearConsole()
                                if choix in range(1, 8):
                                    break
                            except ValueError:
                                ClearConsole()
                        if choix == 1:
                            if Player.nombre_de_sacrifices >= 3:
                                Player.nombre_de_sacrifices -= 3
                                print("L'INNOMABLE VOUS REMERCIE.")
                                Affichage.EntreePourContinuer()
                                print("Une lueur bleue sort de votre poignet tandis que votre poche s'alourdit.")
                                Affichage.EntreePourContinuer()
                                print("Vous perdez 3 Sacrifices, et gagnez 225 golds !")
                                Player.nombre_de_gold += 225
                                Affichage.EntreePourContinuer()
                            else:
                                print("BLAGUE ?")
                                Affichage.EntreePourContinuer()
                        elif choix == 2:
                            if Player.nombre_de_sacrifices >= 3:
                                Player.nombre_de_sacrifices -= 3
                                print("L'INNOMABLE VOUS REMERCIE.")
                                Affichage.EntreePourContinuer()
                                print("Une lueur bleue sort de votre poignet tandis que quelque chose pose sa main sur votre torse et appuie fortement.")
                                Affichage.EntreePourContinuer()
                                print("Vous perdez 3 Sacrifices, gagnez 5 points de vie/mana max, et regagnez toute votre vie et votre mana !")
                                Player.points_de_vie_max += 5
                                Player.points_de_vie = Player.points_de_vie_max
                                Player.points_de_mana_max += 5
                                Player.points_de_mana = Player.points_de_mana_max
                                Affichage.EntreePourContinuer()
                            else:
                                print("BLAGUE ?")
                                Affichage.EntreePourContinuer()
                        elif choix == 3:
                            if Player.nombre_de_sacrifices >= 5:
                                Player.nombre_de_sacrifices -= 5
                                print("L'INNOMABLE VOUS REMERCIE.")
                                Affichage.EntreePourContinuer()
                                print("Une lueur bleue sort de votre poignet, et une énergie étrangère parcourt les veines de votre corps.")
                                Affichage.EntreePourContinuer()
                                print("Vous perdez 5 Sacrifices, gagnez 2 points de force/intelligence !")
                                Player.points_de_force += 2
                                Player.points_dintelligence += 2
                                Affichage.EntreePourContinuer()
                            else:
                                print("BLAGUE ?")
                                Affichage.EntreePourContinuer()
                        elif choix == 4:
                            if Player.nombre_de_sacrifices >= 5:
                                Player.nombre_de_sacrifices -= 5
                                print("L'INNOMABLE VOUS REMERCIE.")
                                Affichage.EntreePourContinuer()
                                print("Une lueur bleue sort de votre poignet tandis que quelque chose souffle au dessus de votre tête.")
                                Affichage.EntreePourContinuer()
                                print("Vous perdez 5 Sacrifices, gagnez 3 pourcents de chance de faire un coup/sort critiques, et 1 pourcent de chance d'esquive !")
                                Player.taux_coup_critique += 3
                                Player.taux_sort_critique += 3
                                Player.taux_desquive += 1
                                Affichage.EntreePourContinuer()
                            else:
                                print("BLAGUE ?")
                                Affichage.EntreePourContinuer()
                        elif choix == 5:
                            if Player.nombre_de_sacrifices >= 10:
                                Player.nombre_de_sacrifices -= 10
                                print("L'INNOMABLE VOUS REMERCIE.")
                                Affichage.EntreePourContinuer()
                                print("Une lueur bleue sort de votre poignet, et un petit coffre de bois noir apparait sur l'autel.")
                                Affichage.EntreePourContinuer()
                                print("Vous perdez 10 Sacrifices, et ouvrez le coffre.")
                                Affichage.EntreePourContinuer()
                                self.GiveRandomArtefact()
                            else:
                                print("BLAGUE ?")
                                Affichage.EntreePourContinuer()
                        elif choix == 6:
                            print("Vous enlevez votre main de l'autel.")
                            Affichage.EntreePourContinuer()
                            break
                        elif choix == 7:
                            if Player.nombre_de_sacrifices >= 5:
                                Player.nombre_de_sacrifices -= 5
                                print("L'INNOMABLE VOUS REMERCIE.")
                                Affichage.EntreePourContinuer()
                                print("L'énergie noire sort de votre main.")
                                print("Vous oubliez la technique [Griffes du Démon] !")
                                print("Vous regagnez 20 points de vie et mana max !")
                                Player.techniques_possedes.remove("Griffes du Démon")
                                Player.points_de_vie_max += 20
                                Player.points_de_mana_max += 20
                                Affichage.EntreePourContinuer()
                                print("L'autel s'écroule sur lui même.")
                                Affichage.EntreePourContinuer()
                                caracteristique_de_la_salle["terminé par joueur"] = True
                                break
                            else:
                                print("BLAGUE ?")
                                Affichage.EntreePourContinuer()
            elif caracteristique_de_la_salle["type"] == "OBELISQUE":  # DONE
                # dessine la salle, si ce n'est pas fait
                if not caracteristique_de_la_salle["marqué sur la carte"]:
                    Draw.obelisque(caracteristique_de_la_salle["position_x"] * 25, caracteristique_de_la_salle["position_y"] * 25)
                    caracteristique_de_la_salle["marqué sur la carte"] = True
                    self.UseMonocleDeVerite()

                print("Vous trouvez un bien étrange obélisque au centre d'une pièce plus grande que les autres.")
                print("Construit en verre, vous pouvez apercevoir un petit coffre de bois noir au milieu.")
                Affichage.EntreePourContinuer()
                print("De plus, sur chaque faces de l'obélisque, il y a une encoche profonde et 5 mots écrits dans une langue que vous ne connaissez pas.")
                Affichage.EntreePourContinuer()
                print("Zeroual semble réagir à l'encoche.")
                Affichage.EntreePourContinuer()

                while True:
                    try:
                        print("Approcher Zeroual de l'encoche ?")
                        print("(Assurez vous d'être prêt.)")
                        print("\n1 - Non\n2 - Oui")
                        choix = int(
                            input("\nChoisissez votre action avec les nombres : ")
                        )
                        ClearConsole()
                        if choix in [1, 2]:
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 1:
                    print("Vous vous éloignez de la salle de l'obélisque.")
                    Affichage.EntreePourContinuer()

                else:
                    mixer.quit()
                    print("Vous approchez Zeroual de l'encoche."
                          "\nL'arme prend alors la forme d'une épée a la lame rouillée et au design particulier, et vous l'insérez dans l'encoche.")
                    Affichage.EntreePourContinuer()
                    print("Les portes de la salle se ferment.")
                    Affichage.EntreePourContinuer()
                    print("Des runes apparaissent dans les airs, flottant sur un axe invisible et encerclant le vide.")
                    print("Quelque chose résonne en vous, comme une idée que l'on aurait mit de force dans votre crane, et qui émane de votre arme.")
                    Affichage.EntreePourContinuer()
                    print("*Retire.*")
                    print("*Prouver. Valeur.*")
                    Affichage.EntreePourContinuer()
                    print("Une terrible présence se fait sentir, et vous retirez Zeroual de l'encoche alors qu'un bruit se fait entendre derriere vous.")
                    Affichage.EntreePourContinuer()
                    Player.affronte_obelisque = True
                    vague = 5
                    while vague != 0:
                        control = controleur.Control(Player, Trader)
                        control.Battle()
                        print("Alors que l'ennemi disparait, une des lignes de l'obélisque s'efface.")
                        Affichage.EntreePourContinuer()
                        vague -= 1
                        if vague != 0:
                            print(f"Il n'y a maintenant plus que {vague} mots.")
                            Affichage.EntreePourContinuer()
                            print("Vous voyez une des runes se briser, et quelque chose apparait.")
                            Affichage.EntreePourContinuer()
                    Player.affronte_obelisque = False
                    print("L'obélisque, maintenant vide de mots, éclate en plusieurs morceaux."
                          "\nMais au lieu de tomber, ils restent en place quelques secondes avant d'aller sur votre arme, qui les absorbe.")
                    Affichage.EntreePourContinuer()
                    print("Vous sentez que le nombre de monstre que vous avez tué a soudainement augmenté de 15 !")
                    Player.nombre_de_monstres_tues += 15
                    Affichage.EntreePourContinuer()
                    print("Vous laissez vos questions de coté, et récuperez le petit coffre de bois noir, que vous ouvrez immédiatement.")
                    Affichage.EntreePourContinuer()
                    caracteristique_de_la_salle["terminé par joueur"] = True
                    self.GiveRandomArtefact()
                    print("Les portes de la salle se rouvrent.")
                    Affichage.EntreePourContinuer()
                    PlayMusicDeLetage()

        #rajoute le numéro de la salle observée a la liste des dernieres salles observées
        self.liste_des_salles_observées.append(Player.numero_de_la_salle)
        if len(self.liste_des_salles_observées) > 4:
            self.liste_des_salles_observées.pop(0)

    def DanceDanceRevolutionIntroduction(self):
        Save.SaveTheGameSansAffichage()
        Player.nombre_de_gold -= 75
        mixer.quit()
        print("Vous inserez 75 golds dans la machine, et lancez le jeu.")
        Affichage.EntreePourContinuer()
        PlayMusic("tutorial")
        print("Un petit tutoriel s'affiche à l'écran.")
        Affichage.EntreePourContinuer()
        print("                   #####")
        print("Lorsque les notes  #####  rencontrent les encoches |_____| ,")
        print("                   #####")
        print("\nvous devez appuyer sur le nombre correspondant et le valider avec la touche entrée.\n")
        Affichage.EntreePourContinuer()
        print("Exemple:")
        Affichage.EntreePourContinuer()
        print("   #####")
        print("   #####      Attendez...")
        print("   #####")
        print("\n \n\n\n \n\n \n\n\n \n\n")
        print("  |_____|")
        print("     1   ")
        time.sleep(0.5)
        ClearConsole()
        print("\n \n\n\n")
        print("   #####")
        print("   #####      Pas encore....")
        print("   #####")
        print("\n \n\n\n \n\n")
        print("  |_____|")
        print("     1   ")
        time.sleep(0.5)
        ClearConsole()
        print("\n \n\n\n \n\n \n\n\n")
        print("   #####")
        print("   #####      Presque...")
        print("   #####")
        print("\n")
        print("  |_____|")
        print("     1   ")
        time.sleep(0.5)
        ClearConsole()
        print("\n\n \n\n\n \n\n \n\n\n \n\n")
        print("   #####")
        print("   #####      LA ! Il faut appuyer sur 1, puis entrée !")
        print("  |#####|")
        print("     1   ")
        Affichage.EntreePourContinuer()
        print("Rapelez vous, les notes n'avancent que si vous entrez un nombre et que vous appuyez sur entrée.")
        print("De plus, au bout de 4 erreurs, le jeu s'arrete !")
        Affichage.EntreePourContinuer()
        print("Finissez 260 notes avant les 180 secondes de musique, et vous gagnez !")
        Affichage.EntreePourContinuer()
        print("Prêt ?")
        Affichage.EntreePourContinuer()
        mixer.quit()
        print("C'est parti !")
        Affichage.EntreePourContinuer()
        game_done = self.DanceDanceRevolution()
        return game_done

    def DanceDanceRevolution(self):
        #lance la musique
        PlaySound("dance")

        #condition de continuité du jeu
        game_over = False
        game_won = False
        essais_restant = 4

        #mise en place des toutes premieres notes
        ligne_1 = 1
        ligne_2 = 1
        ligne_3 = 1
        ligne_4 = 1
        ligne_5 = 1

        #commencement du timer
        time_start = time.time()

        #nombre de notes
        nombre_de_notes = 260

        #commencement de la boucle while
        while not game_over:

            #décompte du nombre de notes restantes
            nombre_de_notes -= 1

            #génération d'une note
            prochaine_note = random.randint(1,9)

            #affectation de la note aux lignes d'en dessous
            ligne_0 = ligne_1
            ligne_1 = ligne_2
            ligne_2 = ligne_3
            ligne_3 = ligne_4
            ligne_4 = ligne_5
            ligne_5 = prochaine_note

            #selon la valeur de la variable, l'affichage sera différent
            affichage_ligne_0 = self.MakeBottomDDRView(ligne_0)
            affichage_ligne_1 = self.MakeDDRView(ligne_1)
            affichage_ligne_2 = self.MakeDDRView(ligne_2)
            affichage_ligne_3 = self.MakeDDRView(ligne_3)
            affichage_ligne_4 = self.MakeDDRView(ligne_4)
            affichage_ligne_5 = self.MakeDDRView(ligne_5)

            while True:
                try:
                    #affiche la vue du joueur
                    print(f"{affichage_ligne_5}\n{affichage_ligne_4}\n{affichage_ligne_3}\n"
                        f"{affichage_ligne_2}\n{affichage_ligne_1}\n{affichage_ligne_0}")
                    print("    1      2      3      4      5      6      7      8      9  ")
                    
                    #affiche le nombre de vie restantes
                    if essais_restant == 4:
                        print("\n               [O]             [O]             [O] \n")
                    elif essais_restant == 3:
                        print("\n               [X]             [O]             [O] \n")
                    elif essais_restant == 2:
                        print("\n               [X]             [X]             [O] \n")
                    elif essais_restant == 1:
                        print("\n               [X]             [X]             [X] \n")
                    
                    #demande le numero au joueur
                    choix = int(input("                                "))
                    ClearConsole()

                    if choix in range(1, 10):
                        break
                except ValueError:
                    ClearConsole()

            #regarde si les notes sont finies
            if nombre_de_notes == 0 :
                game_over = True
                game_won = True

            #compare le numéro donné au numéro nécéssaire
            if not choix == ligne_0:
                essais_restant -= 1
                if essais_restant == 0:
                    game_over = True
                    game_won = False
                    cause = f"      -=Game Over=-\nVous avez fait 3 erreurs !\nDerniere faute : Numéro {choix} entré au lieu de {ligne_0}. "

            #regarde si le temps imparti est fini
            time_now = time.time()
            temps_limite = 180
            if (time_now - time_start) > temps_limite:
                game_over = True
                game_won = False
                cause = f"      -=Game Over=-\nLa musique est finie !\nIl vous restait {nombre_de_notes} notes a faire !"

        #regarde la cause de la défaite
        if not game_won:
            mixer.quit()
            print("La musique s'arrête.")
            Affichage.EntreePourContinuer()
            print("L'écran se fige.")
            Affichage.EntreePourContinuer()
            print(cause)
            print()
            Affichage.EntreePourContinuer()
        else:
            mixer.quit()
            print("La musique s'arrête.")
            Affichage.EntreePourContinuer()
            print("L'écran se fige.")
            Affichage.EntreePourContinuer()
            print("NOUVEAU HIGHSCORE !")
            print("Vous avez réussi !")
            PlaySound("questdone")
            Affichage.EntreePourContinuer()

        #retourne le résultat du jeu
        return game_won

    def MakeDDRView(self, valeur_de_ligne):
        espace_vide = "  "
        note_vide = "     "
        note = "#####"
        affichage = ""
        retour_a_la_ligne = "\n"
        for _ in range(1, 4):
            if valeur_de_ligne != 1 :
                for _ in range(0, valeur_de_ligne - 1):
                    affichage += espace_vide
                    affichage += note_vide
            affichage += espace_vide
            affichage += note
            affichage += retour_a_la_ligne
        return affichage

    def MakeBottomDDRView(self, valeur_de_ligne):
        espace_vide = "  "
        encoche_vide = "|_____|"
        note_vide = "     "
        note = "#####"
        note_dans_encoche = "|#####|"
        affichage = ""
        retour_a_la_ligne = "\n"
        #notes
        for _ in range(1, 3):
            if valeur_de_ligne != 1 :
                for _ in range(0, valeur_de_ligne - 1):
                    affichage += espace_vide
                    affichage += note_vide
            affichage += espace_vide
            affichage += note
            affichage += retour_a_la_ligne
        #encoches
        affichage += " "
        if valeur_de_ligne != 1 :
            for _ in range(0, valeur_de_ligne - 1):
                affichage += encoche_vide
        affichage += note_dans_encoche
        if valeur_de_ligne != 9 :
            for _ in range(0, 8 - (valeur_de_ligne - 1)):
                affichage += encoche_vide
        return affichage

    def GiveRandomArtefact(self, artefact_in_particular="None"):
        nombre_de_fois_a_donner_artefact = [1]
        if Player.death_divinity and artefact_in_particular == "None":
            nombre_de_fois_a_donner_artefact.append(2)

        for _ in nombre_de_fois_a_donner_artefact:
            if artefact_in_particular == "None":
                liste_artefact_optionnels = [
                    "Voile de Ino",  # defence + resurrection t (IMPLEMENTé)
                    "Graine de Grenade",  # vie t
                    "Fiole d'Eau du Styx",  # mana t
                    "Aile de Cire d'Icare",  # esquive t
                    "Griffe de Lion",  # attaque t
                    "Statue d'Angerona",  # taux critique t
                    "Collier de Mithril",  # defence t
                    "Elixir du Sage",  # intelligence
                    "Petite Pierre Philosophale",  # gold t
                    "Anneau Cramoisi",  # endurance t
                    "Orbe de Disruption",  # degat quand ennemi plus mana (IMPLEMENTé)
                    "Plume de Munin",  # esquive t
                    "Collier des Brísingar",  # vie et mana t
                    "Draupnir",  # gold*2 a chaque changements d'étages (IMPLEMENTé) t 
                    "Magatama",  # attaque, intelligence, defence, vie, mana, endurance
                    "Megingjord",  # degat critiques t
                    "Manne Céleste",  # endurance t
                    "Nœud Gordien",  # attaque t
                    "Nimbe Divine",  # intelligence t
                    "Couronne Sacrée",  # endurance peut aller dans le négatif (IMPLEMENTé)
                    "Don de Terre",  # redcoin x2
                    "Don de Foudre",  # redcoin x2
                    "Don de Feu",  # redcoin x2
                    "Don de Glace",  # redcoin x2
                    "Don Sanguin",  # redcoin x2
                    "Don Physique",  # redcoin x2
                    "Don Astral",  # redcoin x2
                    "Gant de Midas", # enleve la gelure quand utilise un crystal élémentaire
                    "Gant d'Héphaïstos", # enleve la brulure quand utilise un crystal élémentaire
                    "Plaquette du Souvenir", # degats de l'attaque légère * 3
                    "Monocle de Vérité",  # gagne 5 gold quand observe salle
                    "Sabre du Roi de Glace", # immunisé face aux pièges
                    "Bocle de Philoctète",  # defence quand se protege * 1.5
                    "Ecaille d'Ouroboros",  # Rend 2 pv par utilisation de sort
                    "Serment d'Heimdall",  # 3% de chance de ne pas utiliser de mana quand jette un sort
                    "Masque d'Oblivion",  # fuite garantie
                    "Chapelet de Moine",  # beni quand on passe son tour
                    "Oeuil de Phénix",  # Reprend 100% mana quand resurection
                    "Echarde de Pinocchio",  # Faible pourcentage de chance de ne pas mourir
                    "Voeu Cristallisé",  # Efface le stigma négatif
                    "Haricot Magique",  # 20% de degats supplémentaires par lapidation
                    "Miette de Pain Congelée",  # gelure reste 2 tours de plus
                    "Chaperon Rouge",  # Cout en vie reduit quad on est blessé
                    "Morceau de Plomb",  # Cout en mana reduit quand déconcentré
                    "Bague de l'Âne",  # Confusion s'arrete en 1 tour
                ]

                # rajoute dans la liste les artefact debloqué au fur et a mesure des parties gagnees
                donnees_de_s0ve = Observation.GetPermanentThingsFromS0ve() 
                liste_dartefact_debloque = ast.literal_eval(donnees_de_s0ve["Artefact Debloques"])
                for artefact in liste_dartefact_debloque :
                    liste_artefact_optionnels.append(artefact)

                # enleve la liste les artefacts que l'on possède déja
                for artefact in Player.liste_dartefacts_optionels:
                    if artefact in liste_artefact_optionnels:
                        liste_artefact_optionnels.remove(artefact)

                # enleve vide interieur si on a voeu cristalisé, ou si on est pas Terah
                if Player.nom_du_personnage != "Terah" and "Vide Interieur" in liste_artefact_optionnels :
                    liste_artefact_optionnels.remove("Vide Interieur")

                if "Vide Interieur" in Player.liste_dartefacts_optionels:
                    liste_artefact_optionnels.remove("Voeu Cristallisé")

                if "Voeu Cristallisé" in Player.liste_dartefacts_optionels:
                    liste_artefact_optionnels.remove("Vide Interieur")

                # selectionne un artefact au pif
                numero_artefact_aleatoire = random.randint(0, len(liste_artefact_optionnels) - 1)
                artefact_a_donner = liste_artefact_optionnels[numero_artefact_aleatoire]

            else:
                #donne un artefact particulier choisi a l'avance
                artefact_a_donner = artefact_in_particular

            # donne l'artefact au joueur
            print(f"Vous gagnez l'artefact [{artefact_a_donner}] !")
            Player.liste_dartefacts_optionels.append(artefact_a_donner)

            # sauvegarde
            Save.SaveTheGameSansAffichage()

            # Applique les effets de l'artefact
            liste_recompense = LISTEEFFETSARTEFACT[artefact_a_donner]
            for cle in liste_recompense:
                if cle == "Attaque":
                    Player.points_de_force += liste_recompense[cle]
                    commentaire = f"Vous gagnez {liste_recompense[cle]} points de force !"
                elif cle == "Defence":
                    Player.points_de_defence += liste_recompense[cle]
                    commentaire = f"Vous gagnez {liste_recompense[cle]} points de défence !"
                elif cle == "Intelligence":
                    Player.points_dintelligence += liste_recompense[cle]
                    commentaire = (
                        f"Vous gagnez {liste_recompense[cle]} points d'intelligence !"
                    )
                elif cle == "Gold":
                    Player.nombre_de_gold += liste_recompense[cle]
                    commentaire = f"Vous gagnez {liste_recompense[cle]} golds !"
                elif cle == "Vie":
                    Player.points_de_vie_max += liste_recompense[cle]
                    Player.points_de_vie += liste_recompense[cle]
                    commentaire = (
                        f"Vous gagnez {liste_recompense[cle]} points de vie maximum !"
                    )
                elif cle == "Mana":
                    Player.points_de_mana_max += liste_recompense[cle]
                    Player.points_de_mana += liste_recompense[cle]
                    commentaire = (
                        f"Vous gagnez {liste_recompense[cle]} points de mana maximum !"
                    )
                elif cle == "Endurance":
                    Player.points_dendurance += liste_recompense[cle]
                    commentaire = (
                        f"Vous gagnez {liste_recompense[cle]} points d'endurance maximum !"
                    )
                elif cle == "Taux coup critique":
                    Player.taux_coup_critique += liste_recompense[cle]
                    commentaire = f"Vous gagnez {liste_recompense[cle]}% de chance de faire un coup critique !"
                elif cle == "Degat coup critique":
                    Player.degat_coup_critique += liste_recompense[cle]
                    commentaire = f"Vous gagnez {liste_recompense[cle]} points de degats de coup critique !"
                elif cle == "Taux sort critique":
                    Player.taux_sort_critique += liste_recompense[cle]
                    commentaire = f"Vous gagnez {liste_recompense[cle]}% de chance de faire un sort critique !"
                elif cle == "Taux esquive":
                    Player.taux_desquive += liste_recompense[cle]
                    commentaire = (
                        f"Vous gagnez {liste_recompense[cle]}% de chance d'esquiver !"
                    )
                elif cle == "Degat sort critique":
                    Player.degat_sort_critique += liste_recompense[cle]
                    commentaire = f"Vous gagnez {liste_recompense[cle]} points de degats de sort critique !"
                elif cle == "Commentaire":
                    commentaire = liste_recompense[cle]
                elif cle == "Red coin":
                    Player.nombre_de_red_coin += liste_recompense[cle]
                    commentaire = f"Vous gagnez {liste_recompense[cle]} Red Coin !"
                print(commentaire)
            if artefact_a_donner == "Vide Interieur":
                Player.stigma_negatif = "[Vidé]"
                Player.points_de_mana_max -= 15
                if Player.points_de_mana_max < 0:
                    Player.points_de_mana_max = 1
                if Player.points_de_mana > Player.points_de_mana_max:
                    Player.points_de_mana = Player.points_de_mana_max
            if artefact_a_donner == "Voeu Cristallisé":
                Player.stigma_negatif = "[Purifié]"
            Affichage.EntreePourContinuer()
            if artefact_a_donner == "Syra":
                nombre_de_techniques = len(Player.techniques_possedes)
                nombre_de_sorts = len(Player.sorts_possedes)
                print(f"Vous connaissez déjà {nombre_de_techniques} techniques et {nombre_de_sorts} sorts.")
                print(f"Vous gagnez ainsi {nombre_de_techniques * 10} pm et {nombre_de_sorts * 10} pv maximum !")
                Player.points_de_vie_max += nombre_de_sorts * 10
                Player.points_de_vie += nombre_de_sorts * 10
                Player.points_de_mana_max += nombre_de_techniques * 10
                Player.points_de_mana += nombre_de_techniques * 10
                Affichage.EntreePourContinuer()

    def InitiateRoleToAttribute(self):
        self.liste_de_machines = ["ARBRE", "DISTRIBUTEUR", "LEVIER", "SPAWNER", "BUFFET", "CHENIL", "CHARGEUR", "JACCUZI"]
        if "Combattant le Gardien" in Player.player_tags:
            self.nombre_de_monstre = 0
            self.nombre_de_gold = 0
            self.nombre_de_item = 0
            self.nombre_de_mimique = 0
            self.nombre_de_piege = 0
            self.nombre_de_secret = 0
            self.nombre_de_cle = 0
            self.nombre_de_leys = 0
            self.nombre_de_petit_gardien = 5
            self.nombre_de_grand_gardien = 1
            self.nombre_de_rien = 5
        else:
            self.nombre_de_petit_gardien = 0
            self.nombre_de_grand_gardien = 0
            self.nombre_de_monstre = Player.numero_de_letage + 3
            self.nombre_de_gold = Player.numero_de_letage + 1
            self.nombre_de_item = Player.numero_de_letage // 2
            self.nombre_de_mimique = 2
            self.nombre_de_piege = Player.numero_de_letage + 2
            self.nombre_de_secret = 1
            self.nombre_de_cle = 1
            self.nombre_de_leys = Player.numero_de_letage // 3 + 1
            self.nombre_de_rien = 0
        self.nombre_de_machine_bon = 0
        self.nombre_de_bol = 0
        self.nombre_de_plaque_pression = 0
        if Player.numero_de_letage in range (1, 5):
            self.nombre_de_machine_bon = 2
            self.nombre_de_bol = 1
            self.nombre_de_plaque_pression = 2
        elif Player.numero_de_letage in range (6, 10):
            self.nombre_de_machine_bon = 4
            self.nombre_de_bol = 2
            self.nombre_de_plaque_pression = 4
        elif Player.numero_de_letage == 10:
            self.nombre_de_machine_bon = 8
            self.nombre_de_bol = 3
            self.nombre_de_plaque_pression = 8
        #evenement de letage 1 : corrompre la foret pour gagner des trucs de magie
        self.nombre_de_puit = 0
        if Player.numero_de_letage in [1, 6]:
            self.nombre_de_puit = 1
        # artefact de letage 2 (liane : besoin de machette rouillee)
        self.nombre_de_coffres_en_lianes = 0
        if Player.numero_de_letage == 2:
            self.nombre_de_coffres_en_lianes = 2
        # objet de letage 2 selon alt ou pas
        self.nombre_de_coeur = 0
        if Player.numero_de_letage in [2, 7]:
            self.nombre_de_coeur = 1
        # artefact de letage 3 (5 spots, 2 artefacts, besoin de pelle rouillee pour ouvrir 1 spot)
        self.nombre_de_faux_spot = 0
        self.nombre_de_spot = 0
        if Player.numero_de_letage == 3:
            self.nombre_de_faux_spot = 3
        if Player.numero_de_letage == 3:
            self.nombre_de_spot = 2
        # artefact de letage 4 (1 livre avec 3 emplacements. si emplecements orbservés dans l'ordre, 1 artefact.)
        self.nombre_de_sequence = 0
        if Player.numero_de_letage in [4, 10]:
            self.nombre_de_sequence = 1
        # artefact de letage 5 (2 dance dance revolution. 50 commandes en 30 secondes pour avoir lartefact)
        self.nombre_de_ddr = 0
        if Player.numero_de_letage in [5, 10]:
            self.nombre_de_ddr = 2
        # artefact de letage 6 (1 coffre gratuit, énigme cassée.)
        self.nombre_de_broken = 0
        if Player.numero_de_letage == 6:
            self.nombre_de_broken = 1
        # artefact de letage 7 (1 rituel de sang : sacrifie 10 ennemis avec dague démoniaque (66 PE 25 DMG) pour 1 artefact et autre)
        self.nombre_de_rituel = 0
        if Player.numero_de_letage == 7:
            self.nombre_de_rituel = 1
        # artefact de letage 8 (2 obelisques : battre 5 ennemis a la suite sans mourir et sans gagner d'ame a la fin.)
        self.nombre_de_obelisque = 0
        if Player.numero_de_letage in [8, 10]:
            self.nombre_de_obelisque = 2
        # etgae 10, boss rush
        self.nombre_de_boss_rush = 0
        if Player.nom_de_letage == "Dédale Frontière":
            self.nombre_de_boss_rush = 1

        if Player.numero_de_letage in [10, 11]:
            self.nombre_de_secret = 0
        
    def AttributingRoleToRoom(self, salle_choisie):
        caracteristique_de_la_salle = self.FloorBlueprint[salle_choisie]
        if self.nombre_de_monstre != 0:
            caracteristique_de_la_salle["type"] = "MONSTRE"
            self.nombre_de_monstre -= 1
        elif self.nombre_de_gold != 0:
            caracteristique_de_la_salle["type"] = "GOLD"
            self.nombre_de_gold -= 1
        elif self.nombre_de_item != 0:
            caracteristique_de_la_salle["type"] = "ITEM"
            self.nombre_de_item -= 1
        elif self.nombre_de_mimique != 0:
            caracteristique_de_la_salle["type"] = "MIMIQUE"
            self.nombre_de_mimique -= 1
        elif self.nombre_de_piege != 0:
            caracteristique_de_la_salle["type"] = "PIEGE"
            self.nombre_de_piege -= 1
        elif self.nombre_de_secret != 0:
            caracteristique_de_la_salle["type"] = "SECRET"
            self.nombre_de_secret -= 1
        elif self.nombre_de_leys != 0:
            caracteristique_de_la_salle["type"] = "LEY"
            self.nombre_de_leys -= 1
        elif self.nombre_de_puit != 0:
            caracteristique_de_la_salle["type"] = "PUIT"
            self.nombre_de_puit -= 1
        elif self.nombre_de_coeur != 0:
            caracteristique_de_la_salle["type"] = "COEUR"
            self.nombre_de_coeur -= 1
        elif self.nombre_de_cle != 0:
            caracteristique_de_la_salle["type"] = "KEY"
            if Player.numero_de_letage == 10 :
                caracteristique_de_la_salle["terminé par joueur"] = False
            self.nombre_de_cle -= 1
        elif self.nombre_de_coffres_en_lianes != 0:
            caracteristique_de_la_salle["type"] = "LIANE"
            self.nombre_de_coffres_en_lianes -= 1
        elif self.nombre_de_faux_spot != 0:
            caracteristique_de_la_salle["type"] = "FAUX SPOT"
            self.nombre_de_faux_spot -= 1
        elif self.nombre_de_spot != 0:
            caracteristique_de_la_salle["type"] = "SPOT"
            self.nombre_de_spot -= 1
        elif self.nombre_de_sequence != 0:
            caracteristique_de_la_salle["type"] = "SEQUENCE"
            self.nombre_de_sequence -= 1
        elif self.nombre_de_ddr != 0:
            caracteristique_de_la_salle["type"] = "DDR"
            self.nombre_de_ddr -= 1
        elif self.nombre_de_broken != 0:
            caracteristique_de_la_salle["type"] = "BROKEN"
            self.nombre_de_broken -= 1
        elif self.nombre_de_rituel != 0:
            caracteristique_de_la_salle["type"] = "RITUEL"
            self.nombre_de_rituel -= 1
        elif self.nombre_de_obelisque != 0:
            caracteristique_de_la_salle["type"] = "OBELISQUE"
            self.nombre_de_obelisque -= 1
        elif self.nombre_de_boss_rush != 0:
            caracteristique_de_la_salle["type"] = "BOSS"
            self.nombre_de_boss_rush -= 1
        elif self.nombre_de_petit_gardien != 0:
            caracteristique_de_la_salle["type"] = "PETIT GARDIEN"
            self.nombre_de_petit_gardien -= 1
        elif self.nombre_de_grand_gardien != 0:
            caracteristique_de_la_salle["type"] = "GRAND GARDIEN"
            self.nombre_de_grand_gardien -= 1
        elif self.nombre_de_rien != 0:
            caracteristique_de_la_salle["type"] = "RIEN"
            self.nombre_de_rien -= 1
        elif self.nombre_de_machine_bon != 0:
            numero_aleatoire = random.randint(0, len(self.liste_de_machines) - 1)
            type_de_machine = self.liste_de_machines[numero_aleatoire]
            caracteristique_de_la_salle["type"] = type_de_machine
            self.liste_de_machines.pop(numero_aleatoire)
            self.nombre_de_machine_bon -= 1
        elif self.nombre_de_bol != 0:
            caracteristique_de_la_salle["type"] = "BOL"
            self.nombre_de_bol -= 1
        elif self.nombre_de_plaque_pression != 0:
            caracteristique_de_la_salle["type"] = "PLAQUE PRESSION"
            self.nombre_de_plaque_pression -= 1
        else:
            nombre_aleatoire = random.randint(0, 5)
            if Player.nom_de_letage == "Dédale Frontière":
                if nombre_aleatoire == 0:
                    caracteristique_de_la_salle["type"] = "ITEM"
                elif nombre_aleatoire == 1:
                    caracteristique_de_la_salle["type"] = "GOLD"
                elif nombre_aleatoire in [2, 3]:
                    caracteristique_de_la_salle["type"] = "MONSTRE"
                elif nombre_aleatoire in [4, 5]:
                    caracteristique_de_la_salle["type"] = "PIEGE"
            else:
                if nombre_aleatoire == 0:
                    caracteristique_de_la_salle["type"] = "MONSTRE"
                elif nombre_aleatoire == 1:
                    caracteristique_de_la_salle["type"] = "GOLD"
                elif nombre_aleatoire in [2, 3]:
                    caracteristique_de_la_salle["type"] = "ITEM"
                elif nombre_aleatoire in [4, 5]:
                    caracteristique_de_la_salle["type"] = "PIEGE"

    def WalkLeft(self):
        if Player.position_x == 0 and Player.position_y == 0:
            Player.position_x = -2
        elif Player.position_x == 2 and Player.position_y == 0:
            Player.position_x = 0
        else:
            Player.position_x -= 1
        Valid = self.CheckPlayerPosition()
        if not Valid:
            Player.position_x += 1
            print("Vous rentrez dans un mur.")
            Affichage.EntreePourContinuer()

    def WalkRight(self):
        if Player.position_x == 0 and Player.position_y == 0:
            Player.position_x = 2
        elif Player.position_x == -2 and Player.position_y == 0:
            Player.position_x = 0
        else:
            Player.position_x += 1
        Valid = self.CheckPlayerPosition()
        if not Valid:
            Player.position_x -= 1
            print("Vous rentrez dans un mur.")
            Affichage.EntreePourContinuer()

    def WalkUp(self):
        if Player.position_x == 0 and Player.position_y == 0:
            Player.position_y = 2
        elif Player.position_x == 0 and Player.position_y == -2:
            Player.position_y = 0
        else:
            Player.position_y += 1
        Valid = self.CheckPlayerPosition()
        if not Valid:
            Player.position_y -= 1
            print("Vous rentrez dans un mur.")
            Affichage.EntreePourContinuer()

    def WalkDown(self):
        if Player.position_x == 0 and Player.position_y == 0:
            Player.position_y = -2
        elif Player.position_x == 0 and Player.position_y == 2:
            Player.position_y = 0
        else:
            Player.position_y -= 1
        Valid = self.CheckPlayerPosition()
        if not Valid:
            Player.position_y += 1
            print("Vous rentrez dans un mur.")
            Affichage.EntreePourContinuer()

    def UpdatePlayerPosition(self):
        goto(Player.position_x * 25, Player.position_y * 25)

    def CheckPlayerPosition(self):
        for numero_de_salle in range(1, len(self.FloorBlueprint) + 1):
            salle_a_tester = self.FloorBlueprint[numero_de_salle]
            if (
                Player.position_x == salle_a_tester["position_x"]
                and Player.position_y == salle_a_tester["position_y"]
            ):
                # le joueur se trouve sur une salle qui existe
                Player.numero_de_la_salle = numero_de_salle
                return True
        return False

    def SetupFloorLayout(self):
        # Initialise un dictionnaire avec les salles et leur position
        nombre_de_salles = 16 + (Player.numero_de_letage * 5)
        if Player.nom_de_letage == "Dédale Frontière":
            nombre_de_salles = 100
        elif Player.numero_de_letage == 11:
            nombre_de_salles = 10
        elif "Combattant le Gardien" in Player.player_tags:
            nombre_de_salles = 12
        self.MakeFloorBlueprint(nombre_de_salles)
       
        # détermine les nombres de roles a attribuer aux salles 
        self.InitiateRoleToAttribute()
        
        # attribue un role a chaque salles
        self.SetupFloorBlueprint()

        if not "Combattant le Gardien" in Player.player_tags:
            Save.SaveTheGameSansAffichage()


    def ShowFloor(self):
        if not self.carte_ouverte:
            self.PrintFloorBlueprint()
            self.carte_ouverte = True
        self.UpdatePlayerPosition()
        self.WalkInFloor()


class Observe:

    def __init__(self):
        pass

    def SeeSomething(self):
        if Player.numero_de_letage == 1:
            self.DoTheLibrary()  # bibliotheque de gros sorts (recuperer les sorts consignés)
        elif Player.numero_de_letage == 2:
            self.DoTheFountain()  # Fontaine redonne pv 3 fois
        elif Player.numero_de_letage == 3:
            self.DoTheGacha()  # Gacha game a mutations
        elif Player.numero_de_letage == 4:
            self.DoTheBloodStone()  # machine a gold a sang
        elif Player.numero_de_letage == 5:
            self.DoTheQuests()  # fantome des quetes ultimes
        elif Player.numero_de_letage == 6:
            self.DoTheOldMercant()  # alchimiste divin vampire demande manamax
        elif Player.numero_de_letage == 7:
            self.DoTheCursedBook()  # echange sorts/techniques pour carac
        elif Player.numero_de_letage == 8:
            self.DoTheFinalLibrary()  # bibliotheque de gros sorts (choisir sort a consigner)
        elif Player.numero_de_letage == 9:
            self.DoTheArtefactTrading()  # Achete des artefacts a Alfred

    def DoTheArtefactTrading(self):
        mixer.quit()
        print("Alors que vous vous approchez du centre de la pièce, vous vous mettez a tomber, les deux pieds fermements ancrés dans le sol.")
        Affichage.EntreePourContinuer()
        print("La salle se met alors a tourner, et changer d'apparence, jusqu'a ce que vous arriviez sur une chaise.")
        Affichage.EntreePourContinuer()
        print("Une figure inconnue est assise, elle aussi, mais de l'autre coté d'une table d'ébène.")
        Affichage.EntreePourContinuer()
        print("Autour de vous se trouve un espace luxueux entouré d'une dizaine de portes.")
        Affichage.EntreePourContinuer()
        print("La figure tend alors une main que vous reconnaissez sans savoir pourquoi.")
        Affichage.EntreePourContinuer()
        PlayMusic("alfredproto")
        print("Alfred.")
        Affichage.EntreePourContinuer()
        print("*Eh bien ? On ne sert plus la main a son hôte maintenant ?* \n*Quoique, les règles d'usage ont du changer ces derniers siècles.*")
        Affichage.EntreePourContinuer()
        print("*Tu doit connaitre la chanson maintenant, ou pas.* \n*Je n'ai aucun moyen de savoir si c'est la toute première fois que l'on se voit, ou si le marionnettiste est un vétérant.*")
        Affichage.EntreePourContinuer()
        print("*Bref.*")
        Affichage.EntreePourContinuer()
        print("*2500 golds, et tu gagne un artefact aléatoire.*")
        Affichage.EntreePourContinuer()
        while True:
            while True:
                try:
                    print("     -=[ Alfred ]=-\n")
                    print("1 - Partir")
                    print("2 - Acheter un artefact aléatoire (2500 golds)")
                    print("3 - Parler")
                    choix = int(input("\nQu'est ce que tu veux ?  "))
                    ClearConsole()
                    if choix in [1, 2, 3]:
                        break
                except:
                    ClearConsole()
            if choix == 1:
                mixer.quit()
                print("*Lève toi simplement si tu veux sortir, et retourne au centre de la pièce si tu veux rentrer.*")
                Affichage.EntreePourContinuer()
                print("Vous le regardez avec un air surpris.")
                Affichage.EntreePourContinuer()
                print("*Quoi ?* \n*L'étage entier est un embroglio de formes, couleurs, et objets qui agissent de manière impossible mais je n'ai pas le droit d'avoir une simple porte de maison cachée dans la 5ème dimension ?*")
                Affichage.EntreePourContinuer()
                print("Vous rougissez d'un air géné et vous relevez. \nBientot, la salle entière bouge sur elle même et vous tombez lourdement sur le sol de l'étage, vos pieds toujours fermements ancrés sur ledit sol.")
                Affichage.EntreePourContinuer()
                PlayMusicDeLetage()
                break
            elif choix == 2:
                if Player.nombre_de_gold >= 2500:
                    print("Vous tendez a Alfred votre bourse d'une main tremblottante, et le voyez engloutir vos golds durements gagnés dans une poche qui semble n'avoir pas de fond.")
                    Affichage.EntreePourContinuer()
                    Player.nombre_de_gold -= 2500
                    print("*Quel bohneur de faire affaire !*")
                    Affichage.EntreePourContinuer()
                    print("*Voici donc votre artefact aléatoire, très estimé client !*")
                    Affichage.EntreePourContinuer()
                    print("Alfred vous tend un petit coffre de bois noir, que vous ouvrez immédiatement.")
                    Affichage.EntreePourContinuer()
                    FloorMaker.GiveRandomArtefact()
                else:
                    mixer.quit()
                    print("Alfred vous regarde avec l'air fatigué et non amusé d'un caissier qui entend pour une ènième fois : *Ya pas de code barre ? Ca doit etre gratuit alors !*")
                    Affichage.EntreePourContinuer()
                    print("Vous rougissez de votre manque de fonds, et vous levez dans la précipitation.")
                    Affichage.EntreePourContinuer()
                    print("La salle tourne sur elle meme, et vous jette violemment contre un des murs du onzième étage.")
                    Affichage.EntreePourContinuer()
                    print("Wow, trop la honte !")
                    Affichage.EntreePourContinuer()
                    PlayMusicDeLetage()
                    break
            elif choix == 3:
                print("*Me parler ?*")
                Affichage.EntreePourContinuer()
                print("Alfred rigole doucement.")
                Affichage.EntreePourContinuer()
                print("*Laisse moi deviner, tu n'avais pas cette option avec les autres marchands, alors t'a sauté sur l'opportunité pour moi ?*")
                Affichage.EntreePourContinuer()
                print("*En tout cas, ca confirme que c'est bien la première fois que tu viens chez moi.*")
                Affichage.EntreePourContinuer()
                print("*Ou alors, tu as fait la paix avec le fait que je vais te dire la même chose a chaque fois que tu utilise cette option...*")
                Affichage.EntreePourContinuer()
                print("*Quoi qu'il en soit, bienvenue chez moi !*")
                Affichage.EntreePourContinuer()
                print("*C'est un petit coin tranquille relié a tout les étages du Coliseum, caché dans une dimension crée de toute pièce par la fusion de tout les étages.*")
                Affichage.EntreePourContinuer()
                print("*J'y ai récupéré un sacré trésor au fur et a mesure des annéees , et je le dépense pour recréer ici une vie plutot bourgeoise, dont je profitait il y a très longtemps.*")
                Affichage.EntreePourContinuer()
                print("*Quoi dire de plus...je ne suis pas vraiment un Homme. La peau blanche que tu vois est maintenue ainsi grace a des composants rares que j'achete au marchand.*")
                Affichage.EntreePourContinuer()
                print("*Mon histoire ?* \n*Je faisait parti d'un groupe de quatres guerriers divinement choisis pour défendre une...porte.*\n* Nous étions mené par un Homme avec beaucoup de valeurs...trahi par son frère.*")
                Affichage.EntreePourContinuer()
                print("*Je suis le seul survivant de cette trahison.*")
                Affichage.EntreePourContinuer()
                print("*Depuis, la porte a été scellé, et le frère avec.*")
                Affichage.EntreePourContinuer()
                print("*Hum ? COmment je suis arrivé ici ?*")
                Affichage.EntreePourContinuer()
                print("*Je laisse cela à ton interprétation.*")
                Affichage.EntreePourContinuer()
                print("*...*")
                Affichage.EntreePourContinuer()
                print("*...mes intentions ?*")
                Affichage.EntreePourContinuer()
                print("Alfred regarde dans un coin de la pièce, et sourit.")
                Affichage.EntreePourContinuer()
                print("*Non, non... Je ne discute pas de ce genre de chose avec une simple poupée.*")
                Affichage.EntreePourContinuer()
                print("Alfred sourit, bien plus que physiquement possible.")
                Affichage.EntreePourContinuer()
                print("*Et si tu venait ici plutôt ?*")
                Affichage.EntreePourContinuer()
                mixer.quit()
                print("*M A R I O N N E T T I S T E ?*")
                time.sleep(3)
                ClearConsole()
                print("[ERREUR : ACCES NON AUTORISE]")
                time.sleep(2)
                ClearConsole()
                print("[UTILISATION DU PARE FEU EN COURS...]")
                time.sleep(5)
                ClearConsole()
                print("[ACCES INTERROMPU. ]")
                time.sleep(2)
                ClearConsole()
                PlayMusic("alfredproto")
                print("*...tsk.*")
                Affichage.EntreePourContinuer()
                




    def DoTheCursedBook(self):
        print(
            "Dans une cage vide, vous trouvez un livre à moitié brulé dont la couverture représente une cigogne noire regardant vers le haut."
        )
        Affichage.EntreePourContinuer()
        print("Sur la première page, il y a [ERROR : DESCRIPTION NOT FOUND].")
        print("[IPV4 ADRESS OF LOST DESCRIPTION : 456852]")
        Affichage.EntreePourContinuer()
        while True:
            while True:
                try:
                    print("Vous posez la main sur la page, et pensez à:")
                    print("1 - Rien du tout.")
                    numero_a_afficher = 2
                    for sorts in Player.sorts_possedes:
                        print(f"{numero_a_afficher} - {sorts}")
                        numero_a_afficher += 1
                    for techniques in Player.techniques_possedes:
                        print(f"{numero_a_afficher} - {techniques}")
                        numero_a_afficher += 1
                    choix = int(input("\n"))
                    ClearConsole()
                    nombre_de_choix_possibles = (
                        len(Player.sorts_possedes) + len(Player.techniques_possedes) + 1
                    )
                    if choix in range(1, (nombre_de_choix_possibles + 1)):
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print(
                    "Vous jetez à votre main un regard vide, et laissez tomber le livre sur le sol avant de repartir."
                )
                Affichage.EntreePourContinuer()
                break
            else:
                liste_de_sorts_et_techniques_a_oublier = []
                for sorts in Player.sorts_possedes:
                    liste_de_sorts_et_techniques_a_oublier.append(sorts)
                for techniques in Player.techniques_possedes:
                    liste_de_sorts_et_techniques_a_oublier.append(techniques)
                action_a_oublier = liste_de_sorts_et_techniques_a_oublier[(choix - 2)]
                Player.liste_daction_oubliees.append(action_a_oublier)
                if action_a_oublier in Player.sorts_possedes:
                    Player.sorts_possedes.remove(action_a_oublier)
                    type_daction = "Sort"
                else:
                    Player.techniques_possedes.remove(action_a_oublier)
                    type_daction = "Technique"
                print(
                    "Vous sentez quelque chose sortir de votre esprit et partir dans le livre, mais vous ne savez pas quoi."
                )
                print(f"La ligne [{action_a_oublier}] apparait sur la page d'après !")
                Affichage.EntreePourContinuer()
                self.DonneRecompensePourOubli(action_a_oublier, type_daction)
                self.DonneRecompensePourCertainsOubli()

    def DonneRecompensePourCertainsOubli(self):
        if (
            "Corne Granite" in Player.liste_daction_oubliees
            and "Création de Granite" in Player.liste_daction_oubliees
        ):
            print(
                "Les lignes Corne Granite et Création de Granite brillent avant de disparaitre."
            )
            print("Vous gagnez 4 points de défence !")
            Player.liste_daction_oubliees.remove("Corne Granite")
            Player.liste_daction_oubliees.remove("Création de Granite")
            Player.points_de_defence += 4
        elif (
            "Explosion de la Comète" in Player.liste_daction_oubliees
            and "Thermosphère Solaire" in Player.liste_daction_oubliees
        ):
            print(
                "Les lignes Explosion de la Comète et Thermosphère Solaire brillent avant de disparaitre."
            )
            print(
                "Vous gagnez 15 points de mana max et 5% de chance de faire un sort critique !"
            )
            Player.points_de_mana_max += 15
            Player.taux_sort_critique += 5
            Player.liste_daction_oubliees.remove("Explosion de la Comète")
            Player.liste_daction_oubliees.remove("Thermosphère Solaire")
        elif (
            "Dague Vampirique" in Player.liste_daction_oubliees
            and "Sonata Miséricordieuse" in Player.liste_daction_oubliees
        ):
            print(
                "Les lignes Dague Vampirique et Sonata Miséricordieuse brillent avant de disparaitre."
            )
            print("Vous gagnez 5% de chance d'esquiver !")
            Player.taux_desquive += 5
            Player.liste_daction_oubliees.remove("Dague Vampirique")
            Player.liste_daction_oubliees.remove("Sonata Miséricordieuse")
        elif (
            "Lance de l'Eclair" in Player.liste_daction_oubliees
            and "Katana Polaire" in Player.liste_daction_oubliees
        ):
            print(
                "Les lignes Lance de l'Eclair et Katana Polaire brillent avant de disparaitre."
            )
            print(
                "Vous gagnez 15 points de vie max 5% de chance de faire un coup critique !"
            )
            Player.points_de_vie_max += 15
            Player.taux_coup_critique += 5
            Player.liste_daction_oubliees.remove("Lance de l'Eclair")
            Player.liste_daction_oubliees.remove("Katana Polaire")
        elif (
            "Dance Destructrice" in Player.liste_daction_oubliees
            and "Poing Fatal" in Player.liste_daction_oubliees
        ):
            print(
                "Les lignes Dance Destructrice et Poing Fatal brillent avant de disparaitre."
            )
            print("Vous gagnez 4 points de force !")
            Player.points_de_force += 4
            Player.liste_daction_oubliees.remove("Dance Destructrice")
            Player.liste_daction_oubliees.remove("Poing Fatal")
        elif (
            "Faisceau Rapide" in Player.liste_daction_oubliees
            and "Bô de la Fournaise" in Player.liste_daction_oubliees
        ):
            print(
                "Les lignes Faisceau Rapide et Bô de la Fournaise brillent avant de disparaitre."
            )
            print("Vous gagnez 4 points d'intelligence !")
            Player.points_dintelligence += 4
            Player.liste_daction_oubliees.remove("Faisceau Rapide")
            Player.liste_daction_oubliees.remove("Bô de la Fournaise")
        elif (
            "Pic Zéro" in Player.liste_daction_oubliees
            and "Sonata Bienveillante" in Player.liste_daction_oubliees
            and "Création Obsidienne" in Player.liste_daction_oubliees
            and "Lance Electrique" in Player.liste_daction_oubliees
            and "Bô Chaud" in Player.liste_daction_oubliees
            and "Katana Froid" in Player.liste_daction_oubliees
        ):
            mixer.quit()
            print(
                "Les lignes Pic Zéro, Sonata Bienveillante, "
                "Création Obsidienne, Lance Electrique, "
                "Katana Froid et Bô Chaud brillent avant de disparaitre."
            )
            print(
                "Des mots apparaissent, lettres après lettres, sur la quatrième de couverture."
            )
            print("Comme écrits par une main invisible.")
            Player.liste_daction_oubliees.remove("Pic Zéro")
            Player.liste_daction_oubliees.remove("Sonata Bienveillante")
            Player.liste_daction_oubliees.remove("Création Obsidienne")
            Player.liste_daction_oubliees.remove("Lance Electrique")
            Player.liste_daction_oubliees.remove("Katana Froid")
            Player.liste_daction_oubliees.remove("Bô Chaud")
            Affichage.EntreePourContinuer()
            PlayMusic("quiet")
            print("      -=Métamorphose=-")
            print("")
            time.sleep(5)
            print("Mon cher amour.")
            time.sleep(5)
            print("De la plus grande plume d'oie")
            time.sleep(5)
            print("A la plus pitoyable tache d'encre,")
            time.sleep(5)
            print("Du plus radiant des passés")
            time.sleep(5)
            print("Au plus austère des futurs,")
            time.sleep(5)
            print("De la plus belle femme du monde")
            time.sleep(5)
            print("A la plus misérable des ombres,")
            time.sleep(5)
            print("Dans la paume de tes mains tourne")
            time.sleep(5)
            print("Ma vie mon monde mon éternitée,")
            time.sleep(5)
            print("Du pire des meilleurs, aux meilleurs du pire .")
            time.sleep(10)
            print("Avec le prix de mon âme,")
            time.sleep(5)
            print("Le sépulcre de ton royaume,")
            time.sleep(5)
            print("Et la mort de ton présent,")
            time.sleep(5)
            print("Enfin j'espère, enfin je vis, enfin j'ose,")
            time.sleep(5)
            print("M'offrir cette métamorphose .")
            time.sleep(5)
            print("Et de la plus pitoyable tache d'encre,")
            time.sleep(5)
            print("A la plus grande plume d'oie,")
            time.sleep(5)
            print("Du plus austère des passés")
            time.sleep(5)
            print("Au plus radiant des futurs,")
            time.sleep(5)
            print("De la plus misérable femme du monde")
            time.sleep(5)
            print("A la plus belle des ombres,")
            time.sleep(5)
            print("Je renais dans tes cendres.")
            time.sleep(5)
            print("")
            print("                     -(nom illisible) Mage,")
            print("                          An de grâce 1233")
            print("")
            time.sleep(5)
            Affichage.EntreePourContinuer()
            mixer.quit()
            print("La cage est ici.")
            print("Mais l'oie s'est envolée ailleurs.")
            Affichage.EntreePourContinuer()
            PlayMusicDeLetage()

    def DonneRecompensePourOubli(self, action_a_oublier, type_daction):
        # trouve le niveau de laction oubliée
        liste_daction_de_même_rang = []
        for rang in range(0, 6):
            if type_daction == "Technique":
                for numero in range(0, 6):
                    index = rang + (numero * 6)
                    liste_daction_de_même_rang.append(LISTETECHNIQUES[index])
            elif type_daction == "Sort":
                for numero in range(0, 7):
                    index = rang + (numero * 6)
                    liste_daction_de_même_rang.append(LISTESORTS[index])
            if action_a_oublier in liste_daction_de_même_rang:
                rang_de_laction = rang + 1
                break
            liste_daction_de_même_rang = []
        # nombre de pv/mana rendu, golds gagné, carac supp
        gain = 5 + rang_de_laction * 5
        gold_gagne = 100 + rang_de_laction * 5
        Player.nombre_de_gold += gold_gagne
        dmg_critique_gagne = 2 * rang_de_laction
        taux_gagne = rang_de_laction
        if type_daction == "Technique":
            type_gain = "pv"
            type_caracteristique = "techniques"
            Player.points_de_vie_max += gain
            Player.points_de_vie += gain
            Player.taux_coup_critique += taux_gagne
            Player.degat_coup_critique += dmg_critique_gagne
        elif type_daction == "Sort":
            type_gain = "pm"
            type_caracteristique = "sorts"
            Player.points_de_mana_max += gain
            Player.points_de_mana += gain
            Player.taux_sort_critique += taux_gagne
            Player.degat_sort_critique += dmg_critique_gagne
        print(f"Vous gagnez {gain} {type_gain} max !")
        print(
            f"Vous gagnez {dmg_critique_gagne} points de dégats de {type_caracteristique} critiques !"
        )
        print(
            f"Vous gagnez {taux_gagne}% de chance de faire des {type_caracteristique} critiques !"
        )
        Affichage.EntreePourContinuer()

    def DoTheOldMercant(self):
        if not Player.mercant_healed:
            print(
                "Vous voyez de la lumière dans une des maisons."
                "\nAlors que vous entrez, vous découvrez une vieille femme mourrante, allongée sur un vieux lit décrépit."
            )
            print("Vous l'entendez vous dire d'une voix faible : *Aidez...moi...*")
            Affichage.EntreePourContinuer()
            while True:
                try:
                    print("*Pas...besoin de beaucoup...*")
                    print("*huit...dix...pas plus...*")
                    print("La dame vous regarde bizarrement.")
                    print("S'approcher ?")
                    print("(Vous risqueriez de le regretter)")
                    print("1 - Non")
                    print("2 - Oui")
                    choix = int(input("\n"))
                    ClearConsole()
                    if choix in [1, 2]:
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print("Vous retournez sur vos pas.")
                Affichage.EntreePourContinuer()
            else:
                print(
                    "Vous vous approchez de la dame, et elle se met a murmurer quelque chose en boucle."
                )
                print("Vous tendez l'oreille et vous mettez a son chevet...")
                Affichage.EntreePourContinuer()
                print("*Merci.*")
                Affichage.EntreePourContinuer()
                print(
                    "Elle se jette sur vous avec la fureur d'un diable, et plante ses crocs dans votre gorge !"
                )
                print(
                    "Vous tentez de la faire lacher prise, mais elle s'aggripe a vous avec encore plus de force."
                )
                print("Vous sentez vos forces diminuer...")
                Affichage.EntreePourContinuer()
                Player.points_de_vie_max -= 15
                Player.points_de_vie -= 15
                Player.points_de_mana_max -= 15
                Player.points_de_mana -= 15
                if Player.points_de_vie <= 0:
                    mixer.quit()
                    PlaySound("death")
                    print("..et vous mourrez.")
                    Affichage.EntreePourContinuer()
                    Affichage.ShowDeath()
                else:
                    Player.points_de_vie = 1
                    Player.points_de_mana = 0
                    Player.mercant_healed = True
                    print(
                        "...et alors que vous appretez a fermer les yeux pour la derniere fois, la dame vous lache."
                    )
                    Affichage.EntreePourContinuer()
                    print(
                        "*Merci jeune homme.*"
                        "\n*Cela faisait longtemps que je n'avais pas eu pareil festin. Ho ho ho !*"
                    )
                    print(
                        "*Revenez me voir d'ici quelques minutes et j'aurais de quoi rembourser votre générosité.*"
                    )
                    Affichage.EntreePourContinuer()
                    print(
                        "Vous avez (été forcé d')accepté(r) la quête [La Générositée d'une Alchimiste] !"
                    )
                    print("Retournez voir l'alchimiste le plus vite possible !")
                    Player.quete = "La Générositée d'une Alchimiste"
                    Affichage.EntreePourContinuer()
                    print("Vous sortez de la maison en gémissant.")
                    print("Vous avez perdu 15 points de vie et de mana max !")
                    print(
                        "Vos points de vie et de mana sont aussi au minimum ! Allez vite vous faire soigner !"
                    )
                    Affichage.EntreePourContinuer()
        else:
            print(
                "Vous voyez de la lumière dans une des maisons."
                "\nVous passez la porte primitive de taule et d'acier, et découvrez derrière une modeste échoppe."
            )
            print(
                "Sur l'étalage, des items d'une raretée phénoménale sont exposés derrière une vitre ."
            )
            print("Vous entendez une voix familière derrière le comptoir.")
            Affichage.EntreePourContinuer()
            if Player.quete == "La Générositée d'une Alchimiste":
                print("*Merci encore pour le remontant, jeune homme.*")
                print(
                    "*Je me présente : Mariette, alchimiste en quête de nouveaux ingrédients.*"
                )
                Affichage.EntreePourContinuer()
                print("*Vampire à mes heures perdues.*")
                Affichage.EntreePourContinuer()
                print(
                    "*La...condition...de cet étage fait que beaucoup de choses bizarres s'y produisent.*"
                    "\n*Comme par exemple la force mysterieuse qui fait que toutes mes productions passent de magistrales à divine !*"
                )
                print(
                    "*Ducoup je vis ici avec la permission du nouveau maitre des lieux, et je lui donne deux trois remèdes en échange .*"
                )
                Affichage.EntreePourContinuer()
                print("*Ce genre de choses.*")
                Affichage.EntreePourContinuer()
                PlaySound("questdone")
                print("Vous recevez un remède divin et une pillule divine !")
                print("Vous avez accompli la quête [La Générositée d'une Alchimiste] !")
                Player.quete_complete.append(Player.quete)
                if "None" in Player.quete_complete:
                    Player.quete_complete.remove("None")
                Player.quete = "None"
                Affichage.EntreePourContinuer()
                PlayMusicDeLetage()
                print(
                    "*Ceux la sont gratuits, mais les autres ne le seront pas. Ho ho ho !*"
                )
                Affichage.EntreePourContinuer()
            while True:
                while True:
                    try:
                        print("*Vous voyez quelque chose qui vous plait ?*")
                        print(
                            "*J'espère que ce n'est pas moi, car je ne suis pas a vendre ! Ho ho ho !*"
                        )
                        print("1 - Partir")
                        print("2 - Remède Divin: 150 golds")
                        print("3 - Pillule Divine: 170 golds")
                        print("4 - Grand Mutagène Doré: 200 golds")
                        print("5 - Soluté d'Absolution: 100 golds")
                        print("6 - Soluté d'Exorcisme: 200 golds")
                        print("7 - Larmes de Vénus: 300 golds")
                        choix = int(
                            input(
                                f"Vous avez {Player.nombre_de_gold} golds. Que souhaitez vous acheter ? "
                            )
                        )
                        ClearConsole()
                        if choix in range(1, 8):
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 1:
                    print("*Au revoir !*")
                    Affichage.EntreePourContinuer()
                    break
                if choix in range(2, 8):
                    if choix == 2:
                        cout = 150
                        nom_de_litem = "Remède Divin"
                    elif choix == 3:
                        cout = 170
                        nom_de_litem = "Pillule Divine"
                    elif choix == 4:
                        cout = 200
                        nom_de_litem = "Grand Mutagène Doré"
                    elif choix == 5:
                        cout = 100
                        nom_de_litem = "Soluté d'Absolution"
                    elif choix == 6:
                        cout = 200
                        nom_de_litem = "Soluté d'Exorcisme"
                    elif choix == 7:
                        cout = 300
                        nom_de_litem = "Larmes de Vénus"
                    if Player.nombre_de_gold >= cout:
                        Player.nombre_de_gold -= cout
                        if nom_de_litem == "Larmes de Vénus":
                            Player.liste_dartefacts_optionels.append("Larmes de Vénus")
                            print("Vous achetez l'artefact [Larmes de Vénus] !")
                            print("Cette fiole emplie d'un soluté magnifique permet d'apaiser les feux de la colère et ne laisse derrière que les ombres de la culpabilité.\nLes effets des orbes de folie et furie durent un tour de plus !")
                        else:
                            print(f"Vous achetez l'item [{nom_de_litem}] !")
                            Player.items_possedes[nom_de_litem] += 1
                        Affichage.EntreePourContinuer()
                        print(
                            "(Mariette vous prend le front a deux main et vous y laisse un gros bisou)"
                        )
                        print("*Vous êtes un amour !*")
                        Affichage.EntreePourContinuer()
                    else:
                        print(
                            "*C'est beau de vouloir soutenir un commerce de proximité,"
                            " mais si vous n'avez pas assez de golds, ca me met dans l'embarras plus qu'autre chose .*"
                        )
                        Affichage.EntreePourContinuer()
                        print("*Qu'importe, c'est l'intention qui compte !*")
                        print("*Prenez donc ceci pour votre gentillesse.*")
                        Affichage.EntreePourContinuer()
                        print("Mariette vous donne un remède !")
                        Player.items_possedes["Remède"] += 1
                        Affichage.EntreePourContinuer()

    def DoTheFinalLibrary(self):
        print(
            "Entre deux piliers de tufs, vous découvrez un couloir singulier."
            "\nA l'interieur, vous sentez votre coeur s'arreter de battre...sans que cela ne vous affecte."
            "\nA la fin du couloir, vous trouvez une magnifique bibliothèque de bois ornemental, dans lequel sont rangés des livres de toutes les couleurs."
        )
        Affichage.EntreePourContinuer()
        while True:
            while True:
                nombre_a_afficher = 2
                try:
                    print("Seuls certains livres attirent votre attention :")
                    print("1 - Partir")
                    for livre in BIBLIOTHEQUEFINALE:
                        print(f"{nombre_a_afficher} - Prendre le livre [{livre}]")
                        nombre_a_afficher += 1
                    choix = int(input("Que souhaitez vous faire ?"))
                    ClearConsole()
                    if choix in range(1, (len(BIBLIOTHEQUEFINALE) + 2)):
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print(
                    "Vous laissez la bibliothèque derriere vous et sortez du couloir."
                )
                print("A votre plus grand soulagement, votre coeur se remet a battre.")
                Affichage.EntreePourContinuer()
                break
            elif choix == 19:
                self.WriteInFinalBook()
            else:
                print("Vous ouvrez le livre à une page aléatoire.")
                Affichage.EntreePourContinuer()
                dictionnaire_sous_forme_de_liste = list(BIBLIOTHEQUEFINALE)
                nom_du_livre = dictionnaire_sous_forme_de_liste[(choix - 2)]
                liste_de_passages_a_lire = BIBLIOTHEQUEFINALE[nom_du_livre]
                for passage in liste_de_passages_a_lire:
                    print(passage)
                    Affichage.EntreePourContinuer()
                print("Vous refermez le livre et le reposez dans la bibliothèque.")
                Affichage.EntreePourContinuer()

    def WriteInFinalBook(self):
        print("Vous prenez le livre familier et observez sa couverture.")
        print("Une magnifique cigogne rouge regarde vers la gauche.")
        print(
            "Sur la première page, vous retrouvez les mêmes lignes que dans le livre de la cigogne bleue a une différence près :"
        )
        print("Elles ne se font pas absorber quand vous les touchez.")
        Affichage.EntreePourContinuer()
        print("Vous pouvez y lire les phrases suivantes :")
        donnees_de_s0ve = self.GetPermanentThingsFromS0ve()
        liste_de_sorts_enregistres = ast.literal_eval(donnees_de_s0ve["Livre de sort"])
        for sort in liste_de_sorts_enregistres:
            print(sort)
        Affichage.EntreePourContinuer()
        if not Player.final_library_used:
            print("...?")
            Affichage.EntreePourContinuer()
            while True:
                try:
                    print(
                        "On dirait presque que le livre tente d'absorber votre mana..."
                    )
                    print("1 - Remettre le livre a sa place")
                    print("2 - Le laisser absorber votre mana (Coute 100pm)")
                    choix = int(input("Que souhaitez vous faire ? "))
                    ClearConsole()
                    if choix in [1, 2]:
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print("Vous refermez le livre et le reposez dans la bibliothèque.")
                Affichage.EntreePourContinuer()
            elif choix == 2 and Player.points_de_mana < 100:
                print("Vous n'avez pas assez de mana !")
                print("Vous refermez le livre et le reposez dans la bibliothèque.")
                Affichage.EntreePourContinuer()
            else:
                Player.points_de_mana -= 100
                print(
                    "Vous laissez le livre prendre votre mana.\nUne aura bleue commence a l'entourer, puis il se referme violemment sur votre bras !"
                )
                Affichage.EntreePourContinuer()
                while True:
                    try:
                        print(
                            "Vous ne pouvez pas risquer d'endommager votre bras avec une technique, il faut se débarrasser du bouquin avec un sort !"
                        )
                        numero_affichage = 1
                        for sorts in Player.sorts_possedes:
                            print(f"{numero_affichage} - {sorts}")
                            numero_affichage += 1
                        choix = int(input("Quel sort souhaitez-vous utiliser ? "))
                        ClearConsole()
                        if choix in range(1, (len(Player.sorts_possedes) + 1)):
                            break
                    except ValueError:
                        ClearConsole()
                sort_choisi = Player.sorts_possedes[(choix - 1)]
                self.AddSpellToS0ve(sort_choisi)
                Player.final_library_used = True
                Save.SaveTheGameSansAffichage()
                print(
                    "Vous lancez le sort et, dans un flash de lumière illuminant le livre, vous le sentez disparaitre !"
                )
                Affichage.EntreePourContinuer()
                print(
                    f"Vous avez inscrit le sort [{sort_choisi}] dans le livre de la Cigogne Rouge !"
                )
                Affichage.EntreePourContinuer()
                print(
                    "Le livre lache votre bras, et vous le replacez dans la bibliothèque."
                )
                Affichage.EntreePourContinuer()
        else:
            print("Vous refermez le livre et le reposez dans la bibliothèque.")
            Affichage.EntreePourContinuer()

    def AddSpellToS0ve(self, sort_choisi):
        donnees_de_s0ve = self.GetPermanentThingsFromS0ve()
        liste_de_sorts_enregistres = ast.literal_eval(donnees_de_s0ve["Livre de sort"])
        if not (sort_choisi in liste_de_sorts_enregistres):
            liste_de_sorts_enregistres.append(sort_choisi)
            donnees_de_s0ve["Livre de sort"] = liste_de_sorts_enregistres
            self.SetPermanentThingsToS0ve(donnees_de_s0ve)

    def AddSoulToS0ve(self):
        donnees_de_s0ve = self.GetPermanentThingsFromS0ve()
        if donnees_de_s0ve["486241597531"] != "Jean.rar":
            donnees_de_s0ve["486241597531"] = "Jean.rar"
            self.SetPermanentThingsToS0ve(donnees_de_s0ve)

    def DoTheQuests(self):
        if Player.quest_giver:
            if Player.quete == "Voeu de Pauvreté" and Player.nombre_de_gold == 0:
                Player.quete += " [Complete]"
            print(
                "Dans un coin de la fête foraine, dans une grande poubelle, vous apercevez un robot primitif fait de métal, avec des nuances de cuivre, d'acier ou de bronze."
            )
            print(
                "Alors que vous vous approchez de la machine, son visage d'aluminum dans lequel ont été creusé 3 trous pour les yeux et la bouche s'illumine de l'interieur."
            )
            Affichage.EntreePourContinuer()
            print("*Hey, toi la, ouai toi, approche n'aie pas peur !*")
            print(
                "*Je suis un ancien explorateur, comme toi.*\n*J'ai appris deux trois trucs avant de mourir, et je suis prêt a te les apprendre si tu fais des trucs pour moi.*"
            )
            Affichage.EntreePourContinuer()
            while True:
                while True:
                    try:
                        print(
                            "*Sers toi en quete, et fais gaffe ! Je saurais si tu a triché ou pas !*\n"
                        )
                        print("1 - Retour\n")
                        print(
                            "2 - Voeu de Pauvreté : Reviens me voir avec 0 golds dans ton inventaire ! (Rang E)"
                        )
                        print(
                            "3 - Interminable : Fais durer ton prochain combat jusqu'au tour 50 (Rang D)\n"
                        )
                        print(
                            "4 - Epreuve du Magister : Bats les 4 prochains ennemis sans utiliser d'action de Feu, Foudre, Glace (Rang C)"
                        )
                        print(
                            "5 - Epreuve des Mages-Epeistes : Bats les 4 prochains ennemis sans utiliser d'action de Terre, Physique, Sang (Rang C)\n"
                        )
                        print(
                            "6 - Force et Honneur : Bats les 8 prochains ennemis sans utiliser d'items en combat (Rang B)"
                        )
                        print(
                            "7 - Moqueries Magiques/Techniques : Bats le Bouffon sans utiliser de sorts ou de techniques [au choix] (Rang A)\n"
                        )
                        print("8 - Sérendipité : Finis toute les quêtes (Rang S)\n")
                        print(f"9 - Abandonner la quête en cours : [{Player.quete}]\n")
                        choix = int(
                            input(
                                "Que souhaitez vous faire ? (Vous ne pouvez prendre qu'une seule quête à la fois.)"
                            )
                        )
                        ClearConsole()
                        if choix in range(1, 10):
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 1:
                    print(
                        "Vous laissez la boite de métal parler toute seule, et revenez sur vos pas."
                    )
                    Affichage.EntreePourContinuer()
                    break
                elif (Player.quete != "None") and (choix != 9):
                    if "[Complete]" in Player.quete:
                        print("Bien joué ! Voila ta récompense !")
                        self.DonneRecompenseQuete()
                        quete_reussie = Player.quete
                        quete_reussie = quete_reussie.rstrip("[Complete]").rstrip()
                        Player.quete_complete.append(quete_reussie)
                        if "None" in Player.quete_complete:
                            Player.quete_complete.remove("None")
                        Player.quete = "None"
                    else:
                        print("*T'a déja prit une quete ! Ouste !*")
                        Affichage.EntreePourContinuer()
                elif choix == 2:
                    if "Voeu de Pauvreté" in Player.quete_complete:
                        print("*Tu l'as déja faite celle là.*")
                        Affichage.EntreePourContinuer()
                    else:
                        print(
                            "*C'est plutot simple ! Utilise tout ton argent et reviens me voir.*"
                            "\n*Je te validerait la quete a ce moment la.*"
                        )
                        print("Vous avez accepté la quête [Voeu de Pauvreté]")
                        Affichage.EntreePourContinuer()
                        Player.quete = "Voeu de Pauvreté"
                elif choix == 3:
                    if "Interminable" in Player.quete_complete:
                        print("*Tu l'as déja faite celle là.*")
                        Affichage.EntreePourContinuer()
                    else:
                        print(
                            "*Ton prochain combat, boss ou monstre, fait le durer jusqu'au 50eme tour minimum.*"
                            "\n*Si tu échoue, reviens me voir et je te la redonnerais.*"
                        )
                        print("Vous avez accepté la quête [Interminable]")
                        Affichage.EntreePourContinuer()
                        Player.quete = "Interminable"
                elif choix == 4:
                    if "Epreuve du Magister" in Player.quete_complete:
                        print("*Tu l'as déja faite celle là.*")
                        Affichage.EntreePourContinuer()
                    else:
                        print(
                            "*On donnait cette épreuve aux membres du Magister, un consort de mages de la nature.*"
                            "\n*Tu échoue si tu use de Techniques ou Sorts en lien avec le Feu, la Foudre ou la Glace pendant les 4 prochains combats.*"
                        )
                        print(
                            "*Le Tir Arcanique et l'attaque Légère ont tout deux l'élément Physique !*"
                        )
                        print("Vous avez accepté la quête [Epreuve du Magister]")
                        Affichage.EntreePourContinuer()
                        Player.quete = "Epreuve du Magister"
                elif choix == 5:
                    if "Epreuve des Mages-Epeistes" in Player.quete_complete:
                        print("*Tu l'as déja faite celle là.*")
                        Affichage.EntreePourContinuer()
                    else:
                        print(
                            "*On donnait cette épreuve à l'escouade des Mages-Epeistes, au service de sa Majestée.*"
                            "\n*Tu échoue si tu use de Techniques ou Sorts en lien avec la Terre, le Sang ou le Physique pendant les 4 prochains combats.*"
                        )
                        print(
                            "*Attention ! Le Tir Arcanique et l'attaque Légère ont tout deux l'élément Physique !*"
                        )
                        print("Vous avez accepté la quête [Epreuve des Mages-Epeistes]")
                        Affichage.EntreePourContinuer()
                        Player.quete = "Epreuve des Mages-Epeistes"
                elif choix == 6:
                    if "Force et Honneur" in Player.quete_complete:
                        print("*Tu l'as déja faite celle là.*")
                        Affichage.EntreePourContinuer()
                    else:
                        print(
                            "*Les aventuriers se reposent trop sur leur force donnée, les objets, et pas assez sur leur force acquise, les sorts et techniques.*"
                            "\n*Libère toi des chaines du consummérisme !*"
                        )
                        print("Vous avez accepté la quête [Force et Honneur]")
                        Affichage.EntreePourContinuer()
                        Player.quete = "Force et Honneur"
                elif choix == 7:
                    if (
                        "Moqueries Magiques" in Player.quete_complete
                        or "Moqueries Techniques" in Player.quete_complete
                    ):
                        print("*Tu l'as déja faite celle là.*")
                        Affichage.EntreePourContinuer()
                    else:
                        while True:
                            try:
                                print(
                                    "*Je me suis fais humilier par le Bouffon, et en échange il m'a foutu dans cette boite de conserve pour l'éternitée.*"
                                    "\n*Humilie le pour moi !*"
                                )
                                print("1 - *Tu préfere l'écraser sans Sorts ?*")
                                print("2 - *Tu préfère l'écraser sans Techniques ?*")
                                choix_quete = int(input("Que souhaitez vous faire ? "))
                                ClearConsole()
                                if choix_quete in [1, 2]:
                                    break
                            except ValueError:
                                ClearConsole()
                        if choix_quete == 1:
                            print("*Qu'il en soit ainsi !*")
                            print("Vous avez accepté la quête [Moqueries Magiques]")
                            Player.quete = "Moqueries Magiques"
                        else:
                            print("*Qu'il en soit ainsi !*")
                            print("Vous avez accepté la quête [Moqueries Techniques]")
                            Player.quete = "Moqueries Techniques"
                        Affichage.EntreePourContinuer()
                elif choix == 8:
                    if "Sérendipité" in Player.quete_complete:
                        print("*Tu l'as déja faite celle là.*")
                        Affichage.EntreePourContinuer()
                    elif (
                        (
                            "Moqueries Magiques" in Player.quete_complete
                            or "Moqueries Techniques" in Player.quete_complete
                        )
                        and ("Force et Honneur" in Player.quete_complete)
                        and ("Epreuve des Mages-Epeistes" in Player.quete_complete)
                        and ("Epreuve du Magister" in Player.quete_complete)
                        and ("Interminable" in Player.quete_complete)
                        and ("Voeu de Pauvreté" in Player.quete_complete)
                    ):
                        Player.quete_complete.append("Sérendipité")
                        self.AfficheSecretQuetes()
                        break
                    else:
                        print("Tu n'a pas réussi toute mes demandes.")
                        print("Reviens me voir lorsque ce sera le cas.")
                        Affichage.EntreePourContinuer()
                elif choix == 9:
                    if Player.quete == "None":
                        print("*Tu n'a pas de quêtes en cours !*")
                        print("*Reviens lorsque ce sera le cas.*")
                    elif "[Complete]" in Player.quete:
                        print("Et puis quoi encore ??")
                    else:
                        print(f"*Tu veux abandonner la quête [{Player.quete}] ?*")
                        print("*Très bien, c'est noté.*")
                        Player.quete = "None"
                    Affichage.EntreePourContinuer()
        else:
            print("Il y a un cratère de suie, de déchets, et de bouts de chairs.")
            Affichage.EntreePourContinuer()
            print("Parmis les décombres, vous trouvez une carte étudiante :")
            Affichage.EntreePourContinuer()
            print(
                "Adrien Stéfalnos\nProfesseur d'Archéologie\nCampus de Capital City\nNuméro de badge: 3236353"
            )
            Affichage.EntreePourContinuer()
            print("Vous laissez le cratère et retournez sur vos pas.")
            Affichage.EntreePourContinuer()

    def AfficheSecretQuetes(self):
        mixer.quit()
        print(
            "*Tu as rendu un fier service a ce vieux spectre.*\n*C'est dingue a quel point on peut s'ennuyer quand on a plus controle de ses membres, et qu'on est enfermé dans une idole d'acier.*"
        )
        print(
            "*Je n'ai plus rien a te donner, a part peut etre une histoire, alors écoute bien :*"
        )
        Affichage.EntreePourContinuer()
        print(
            "*C'était il y a très longtemps.*\n*Un âge tellement reculé que personne ne s'en souvient.*"
        )
        print(
            "*Enfaite, cette histoire vient d'images retrouvées dans d'anciens temples enfouis, pour te dire a quel point c'est vieux.*"
        )
        print(
            "*On a même pas de traces dans les livres d'histoires, ou même sous forme de traditions ou chants !*"
        )
        Affichage.EntreePourContinuer()
        print("*Mais je m'égare.*")
        Affichage.EntreePourContinuer()
        PlayMusic("tales")
        print(
            "*C'est un chateau dans le ciel. Ou une île volante de marbre blanc. Ou encore un palace porté dans les airs par un oiseau invisible.*"
        )
        Affichage.EntreePourContinuer()
        print(
            "*C'est un lieu impossible, ou chaque portes et chaque couloirs mènent a des endroits différents selon l'endroit et le temps.*"
        )
        Affichage.EntreePourContinuer()
        print(
            "*Ce sont des êtres puissants, des démons, des esprits, portant de lourds fardeaux, chacun s'occupant d'un aspect de la réalité.*"
        )
        Affichage.EntreePourContinuer()
        print(
            "*C'est une batisse abritant les dieux, crée a partir d'un joyau, d'une pièce, du coeur d'un ange, ou de l'oeil d'un guerrier.*"
        )
        Affichage.EntreePourContinuer()
        print(
            "*C'est un pouvoir qui traverse les dimensions, teinté par la pureté de l'âme qui se l'approprie.*"
        )
        Affichage.EntreePourContinuer()
        print(
            "*C'est un monde éteint, endormi, attisé par les mains divines, hostile.*"
        )
        Affichage.EntreePourContinuer()
        print(
            "*C'est une guerre entre nos protecteurs et les légions de voyageurs, aux portes du monde étranger, dans un lieu ou les roses ne fânent jamais.*"
        )
        Affichage.EntreePourContinuer()
        print(
            "*C'est la fiertée de 5 êtres exceptionels choisis pour défendre la porte des étoiles.*"
        )
        Affichage.EntreePourContinuer()
        print(
            "*C'est la douleur du fratricide, l'odeur du pétrichor carmin, les vents d'un affrontement décisif.*"
        )
        Affichage.EntreePourContinuer()
        print(
            "*C'est la disparition de toutes les divinités de ce monde, comme prix a payer pour refermer ce qui n'aurait jamais du être ouvert.*"
        )
        Affichage.EntreePourContinuer()
        print(
            "*C'est la chute de la grandeur et fierté des dieux dans l'oubli d'un océan sans nom.*"
        )
        Affichage.EntreePourContinuer()
        print(
            "*Cette histoire, c'est celle de la guerre de l'interdit. Ou en tout cas c'est le nom sur lequel se sont mises d'accord les anciennes gravures.*"
        )
        Affichage.EntreePourContinuer()
        print("*Mais laisse moi donc la continuer avec ma... théorie.*")
        Affichage.EntreePourContinuer()
        print("*La raison pour laquelle je suis ici.*")
        Affichage.EntreePourContinuer()
        print("*La raison pour laquelle j'ai persisté toute ces années.*")
        Affichage.EntreePourContinuer()
        print("(la lumière dans la statue se fait plus faible.)")
        Affichage.EntreePourContinuer()
        print("*C'est peut etre la fin de l'histoire des dieux...*")
        Affichage.EntreePourContinuer()
        print("*...mais pas celle du pouvoir qui a crée leur demeure.*")
        Affichage.EntreePourContinuer()
        print(
            "(la lumière s'éteint. Seule la voix calme du donneur de quête persiste.)"
        )
        Affichage.EntreePourContinuer()
        print("*Ce n'est pas un concept : c'est un objet réel.*")
        Affichage.EntreePourContinuer()
        print("*C'est son oubli pendant des millénaires au fond de l'eau salée.*")
        Affichage.EntreePourContinuer()
        print("*C'est son repéchage par un homme imprégné de magie.*")
        Affichage.EntreePourContinuer()
        print(
            "*C'est son étude pendant des décennies pour comprendre comment il marche.*"
        )
        Affichage.EntreePourContinuer()
        print(
            "*C'est sa prise en main par un fou déterminé a répendre sa folie sur le monde.*"
        )
        Affichage.EntreePourContinuer()
        print("*C'est l'obnubilation, la détermination, l'obsession.*")
        Affichage.EntreePourContinuer()
        print(
            "(Vous sentez le mana s'activer tout autour de vous, comme si quelqu'un lancait un sort)"
        )
        Affichage.EntreePourContinuer()
        print("*Nourrie avec le mana du Mage...*")
        Affichage.EntreePourContinuer()
        print("*...corrompue par l'obsession du Roi...*")
        Affichage.EntreePourContinuer()
        print("*...l'ancienne demeure des dieux est devenue le Co-*")
        print("(Appuyez sur entrée pour continuer)")
        time.sleep(1)
        ClearConsole()
        PlayWavSound("ELECm")
        Player.quest_giver = False
        Save.SaveTheGameSansAffichage()
        print("Un gigantesque éclair s'abat sur la chose de métal.")
        Affichage.EntreePourContinuer()
        print("Une pluie de ferraille et de chair en décomposition s'abat sur vous.")
        Affichage.EntreePourContinuer()
        print(
            "Vous regardez le cratère fumant devant vous pendant quelques minutes, horrifié, et quittez les lieux en courant."
        )
        Affichage.EntreePourContinuer()
        PlayMusicDeLetage()

    def DonneRecompenseQuete(self):
        if Player.quete == "Voeu de Pauvreté [Complete]":
            print(
                "Le truc vous apprend a vous débarraser de votre stress. Vous vous sentez plus leger !"
            )
            print("Vous gagnez 15 points de vie max !")
            Player.points_de_vie_max += 15
            Player.points_de_vie += 15
        elif Player.quete == "Interminable [Complete]":
            print(
                "Le truc vous apprend la patience et la concentration sur de longues périodes de temps."
            )
            print("Vous gagnez 15 points de mana max !")
            Player.points_de_mana_max += 15
            Player.points_de_mana += 15
        elif Player.quete == "Epreuve du Magister [Complete]":
            print(
                "Le truc vous apprend une méthode de respiration qui permet de reveiller la force latente."
            )
            print("Vous gagnez 8 points de degat de coup/sorts critiques !")
            Player.degat_coup_critique += 8
            Player.degat_sort_critique += 8
        elif Player.quete == "Epreuve des Mages-Epeistes [Complete]":
            print(
                "Le truc vous montre des points d'acuponctures à presser pour ameliorer le flux sanguin."
            )
            print("Vous gagnez 3 points de force/intelligence/defence !")
            Player.points_de_force += 3
            Player.points_dintelligence += 3
            Player.points_de_defence += 3
        elif Player.quete == "Force et Honneur [Complete]":
            print(
                "Le truc vous apprend a déduire les arcs vectoriels des attaques ennemies a partir de leurs mouvements."
            )
            print("Vous gagnez 8% d'esquive !")
            Player.taux_desquive += 8
        elif Player.quete == "Moqueries Techniques [Complete]":
            print("Le truc vous passe la technique ultime de son clan.")
            print("Vous apprenez le Iaido !")
            Player.techniques_possedes.append("Iaido")
            if "Syra" in Player.liste_dartefacts_optionels:
                            print("Grace au verre de Syra que vous avez bu, vous gagnez aussi 10 pm max !")
                            Player.points_de_mana += 10
                            Player.points_de_mana_max += 10
                            Affichage.EntreePourContinuer()
        elif Player.quete == "Moqueries Magiques [Complete]":
            print("Le truc vous passe le sort ultime de son clan.")
            print("Vous apprenez le Carrousel !")
            Player.sorts_possedes.append("Carrousel")
            if "Syra" in Player.liste_dartefacts_optionels:
                print("Grace au verre de Syra que vous avez bu, vous gagnez aussi 10 pv max !")
                Player.points_de_vie += 10
                Player.points_de_vie_max += 10
                Affichage.EntreePourContinuer()
        Affichage.EntreePourContinuer()

    def DoTheBloodStone(self):
        print("Entre deux bibliothèque, un passage étroit attire votre attention.")
        print(
            "De l'autre coté, vous trouvez de nombreuses formes de vies, artefacts, et livres concernant de glorieuses batailles et de magistrales découvertes."
        )
        print(
            "Comme dans un musée, chaque trouvaille est encastrée dans un bloc de verre, et son hisoire expliquée de manière concise par une plaquette en dessous."
        )
        Affichage.EntreePourContinuer()
        print(
            "Seul un objet attire votre attention, a cause de sa présence solitaire dans l'allée *Usage Public*,"
        )
        print(
            "mais aussi par l'impressionnante quantitée de statues d'or présentes autour."
        )
        print(
            "Sur un petit coussin de soie, vous apercevez une pierre rouge sang, entourée des mêmes symboles que sur le clone d'obsidienne magique."
        )
        Affichage.EntreePourContinuer()
        while True:
            while True:
                try:
                    print(
                        "La plaquette en dessous indique : *Fausse Pierre Philosophale. Transmute la vitalitée en golds.*"
                    )
                    print("1 - Partir")
                    print("2 - Tenir la Pierre")
                    choix = int(input("Que souhaitez vous faire ? "))
                    ClearConsole()
                    if choix in [1, 2]:
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print("Vous retournez sur vos pas et quittez le musée de curiositées.")
                Affichage.EntreePourContinuer()
                break
            else:
                still_alive = self.AbsorptionParBloodStone()
                if still_alive:
                    print("Vous lachez la pierre et toussez quelques pièces.")
                    print(
                        "Certains endroits sur votre corps ont gagné une teinte dorée, et vos articulations vous semblent rigides."
                    )
                    Affichage.EntreePourContinuer()
                else:
                    PlaySound("death")
                    # affichage de la fin.
                    print("L'entieretée de votre existance est absorbée par la pierre.")
                    Affichage.EntreePourContinuer()
                    print("Vous devenez une statue d'or parmis les autres.")
                    Affichage.EntreePourContinuer()
                    print("ERREUR : CORRUPTION DES DONNEES DE SAUVEGARDE")
                    # mise en place dernieres donnes de sauvegarde ==) joueur
                    Save.FromSaveFileToDict()
                    Save.FromDictToPlayer()
                    Affichage.EntreePourContinuer()
                    print("REECRITURE EN COURS...")
                    # remplacement des donnees de sauvegarde pour secret.
                    dir_path = os.path.dirname(os.path.realpath(__file__))
                    chemin_du_fichier_save = dir_path + "\\save.txt"
                    with open(chemin_du_fichier_save, "w") as fichier:
                        fichier.write(
                            "Parmis les rivages distants je vois des montagnes d'or."  # 15
                            "\nQuel enfer attend celui qui n'existe pas ?"  # 12
                            "\nMarqué par la pierre, marqué par la mort,"  # 11
                            "\nMon nom réduit en milliers d'éclats."  # 11
                            "\nNombreuses sont les syllabes, lignes par lignes,"  # 13
                            "\nFlottant dans le vide, j'espère vous arrivent,"  # 11
                            "\nMon chemin illuminé, signes par signes,"  # 10
                            "\nVous mène a l'infame, vous mène a l'indigne."  # 13
                            "\n\n                                   - Véritée,"
                            "\n                                         Auteur inconnu."
                        )
                    Affichage.EntreePourContinuer()
                    # mise en place donnees de joueur ( qui est aussi dernieres donnees de sauvegarde) ==) donnes des sauvegarde
                    Save.FromPlayerToDict()
                    Save.FromDictToSaveFile("\\save.txt")
                    print("REECRITURE TERMINEE")
                    Affichage.EntreePourContinuer()
                    PlayMusicDeLetage()

    def AbsorptionParBloodStone(self):
        print("Vous prenez la pierre dans la main et sentez votre énergie s'évaporer.")
        Affichage.EntreePourContinuer()
        self.ArreteAbsorption = threading.Event()
        self.Absorption = threading.Thread(target=self.ConversionBloodStone)
        self.Absorption.start()
        input("")
        self.ArreteAbsorption.set()
        time.sleep(2)
        if Player.points_de_vie >= 1:
            return True
        return False

    def ConversionBloodStone(self):
        numero = 0
        temps_dattente = 2
        while not self.ArreteAbsorption.isSet():
            print("                 -=Conversion en Cours=-")
            print(f"                      {Player.points_de_vie} pv")
            print(f"                      {Player.nombre_de_gold} golds")
            print("")
            print("        Appuyez sur entree pour lacher la pierre")
            time.sleep(temps_dattente)
            ClearConsole()
            numero += 1
            if numero in range(1, 6):
                Player.points_de_vie -= 1
                Player.nombre_de_gold += 1
            elif numero in range(6, 11):
                Player.points_de_vie -= 2
                Player.nombre_de_gold += 2
                temps_dattente = 1
            elif numero in range(11, 16):
                Player.points_de_vie -= 3
                Player.nombre_de_gold += 4
                temps_dattente = 0.8
            elif numero in range(16, 21):
                Player.points_de_vie -= 4
                Player.nombre_de_gold += 8
                temps_dattente = 0.6
            elif numero in range(21, 26):
                Player.points_de_vie -= 5
                Player.nombre_de_gold += 16
                temps_dattente = 0.4
            elif numero in range(26, 31):
                Player.points_de_vie -= 6
                Player.nombre_de_gold += 32
                temps_dattente = 0.2
            elif numero in range(31, 36):
                Player.points_de_vie -= 7
                Player.nombre_de_gold += 64
                temps_dattente = 0.2
            else:
                Player.points_de_vie -= round(numero / 2)
                Player.nombre_de_gold += numero * numero

    def DoTheGacha(self):
        chanceux = False
        malchanceux = False
        print(
            "Un petit étang, grand comme une chambre d'hotel, entouré de hauts palmiers et de verdure."
        )
        commentaire = "Dans l'eau bleutée, vous pouvez voir un profond abysse dans lequel se perd la lumière."
        nombre_aleatoire = random.randint(0, Player.points_de_mana_max)
        if nombre_aleatoire == Player.points_de_mana:
            chanceux = True
            commentaire += "Et à l'interieur, une gigantesque baleine nage sereinement."
        elif nombre_aleatoire == 0:
            malchanceux = True
            commentaire += (
                "Et tout au fond, une paire d'yeux qui vous regarde... fixement."
            )
        print(commentaire)
        print(
            "Cepandant, quand vous tentez d'enfoncer vos mains dans l'oasis ou de toucher les buissons qui l'entourent, tout disparait sans laisser de trace."
        )
        print("Comme si il n'y avait jamais rien eu.")
        Affichage.EntreePourContinuer()
        while True:
            while True:
                try:
                    print(
                        "Dans le ciel reflété par la surface de l'étang, vous pouvez voir les mots suivants :"
                    )
                    print("*L'Or Change Le Monde*")
                    print("1 - Repartir")
                    print("2 - Jetter 45 golds dans l'étang")
                    print("3 - Jetter 75 golds dans l'étang")
                    choix = int(input("Que souhaitez vous faire ? "))
                    ClearConsole()
                    if choix in [1, 2, 3]:
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print(
                    "Vous laissez l'oasis derrière vous et repartez dans l'océan de sable."
                )
                Affichage.EntreePourContinuer()
                break
            elif choix in [2, 3]:
                if (choix == 2 and Player.nombre_de_gold >= 45) or (
                    choix == 3 and Player.nombre_de_gold >= 75
                ):
                    print("Vous jetez vos golds dans l'étang et...")
                    if choix == 2:
                        Player.nombre_de_gold -= 45
                        Player.gold_in_well += 45
                    else:
                        Player.nombre_de_gold -= 75
                        Player.gold_in_well += 75
                    Affichage.EntreePourContinuer()
                    numero_de_la_pool_de_recompense = self.GetNumeroDePoolDeRecompense(
                        choix, chanceux, malchanceux
                    )
                    numero_de_la_pool_de_recompense = (
                        self.GetNouveauNumeroDePoolDeRecompense(
                            numero_de_la_pool_de_recompense
                        )
                    )
                    self.GiveRecompenseGacha(numero_de_la_pool_de_recompense)
                else:
                    print("Vous n'avez pas assez de golds !")
                    Affichage.EntreePourContinuer()

    def GiveRecompenseGacha(self, numero_de_pool):
        liste_de_pools_de_recompenses = [
            ["Rien"],
            [
                "Mutagène Bleu",
                "Mutagène Rouge",
                "Mutagène Vert",
            ],
            ["Mutagène Doré"],
            [
                "Grand Mutagène Bleu",
                "Grand Mutagène Rouge",
                "Grand Mutagène Vert",
            ],
            [
                "Mutagène Hérétique",
                "Mutagène Fanatique",
            ],
            [
                "Grand Mutagène Doré",
            ],
            ["Mutagène Sacré"],
            ["Gold"],
            ["Secret"],
        ]
        pool_de_recompense = liste_de_pools_de_recompenses[numero_de_pool]
        numero_aleatoire = random.randint(0, (len(pool_de_recompense) - 1))
        recompense = pool_de_recompense[numero_aleatoire]
        if recompense not in ["Rien", "Gold", "Mutagène Sacré", "Secret"]:
            Affichage.AfficheGacha(recompense)
            Player.items_possedes[recompense] += 1
        elif recompense == "Gold":
            print(
                "Vous vous avancez vers le centre de la ou se trouvait l'étang, et récuperez votre argent !"
            )
            print(f"Vous regagnez {Player.gold_in_well} golds !")
            Player.nombre_de_gold += Player.gold_in_well
            Player.gold_in_well = 0
            Affichage.EntreePourContinuer()
        elif recompense == "Mutagène Sacré":
            print(
                "C'est un Mutagène Sacré !\nExtremement rare, ce mutagène permet d'augmenter de manière permanente la vie et le mana !"
            )
            Affichage.EntreePourContinuer()
            gain_pv = round(Player.points_de_vie_max * 0.25)
            Player.points_de_vie_max += gain_pv
            Player.points_de_vie += gain_pv
            gain_pm = round(Player.points_de_mana_max * 0.25)
            Player.points_de_mana_max += gain_pm
            Player.points_de_mana += gain_pm
            print(
                f"Vous vous l'injectez immédiatement et gagnez {gain_pv} pv et {gain_pm} pm !"
            )
            Affichage.EntreePourContinuer()
        elif recompense == "Secret":
            self.AfficheEtangSecret()

    def GetNouveauNumeroDePoolDeRecompense(self, numero_de_pool):
        while True:
            while True:
                try:
                    if numero_de_pool == 1:
                        raretee_avant = "Commun"
                        raretee_apres = "Rare"
                        cout_de_laugmentation = "30 golds"
                    elif numero_de_pool == 2:
                        raretee_avant = "Rare"
                        raretee_apres = "Epique"
                        cout_de_laugmentation = "10 pm et 30 golds"
                    elif numero_de_pool == 3:
                        raretee_avant = "Epique"
                        raretee_apres = "Incarnat"
                        cout_de_laugmentation = "10 pv et 10 pm et 30 golds"
                    elif numero_de_pool == 4:
                        raretee_avant = "Incarnat"
                        raretee_apres = "Légendaire"
                        cout_de_laugmentation = "20 pv et 20 pm et 40 golds"
                    elif numero_de_pool == 5:
                        raretee_avant = "Légendaire"
                        raretee_apres = "Mythique"
                        cout_de_laugmentation = "25 pv et 25 pm et 50 golds"
                    elif numero_de_pool == 6:
                        raretee_avant = "Mythique"
                        raretee_apres = "???"
                        cout_de_laugmentation = "30 pv et 30 pm et 60 golds"
                    elif numero_de_pool in [0, 7, 8]:
                        break
                    print(
                        "Vous sentez que vous pouvez augmenter la raretée du mutagène avant de l'examiner."
                    )
                    print(
                        f"Raretée actuelle : {raretee_avant}. Raretée après augmentation : {raretee_apres}"
                    )
                    print(f"Prix : {cout_de_laugmentation}")
                    print("1 - Examiner le Mutagène")
                    print("2 - Faire l'Augmentation")
                    choix = int(input("Que souhaitez vous faire ? "))
                    ClearConsole()
                    if choix in [1, 2]:
                        break
                except ValueError:
                    ClearConsole()
            if numero_de_pool in [0, 7, 8]:
                return numero_de_pool
            elif choix == 1:
                print("Vous observez de plus près le mutagène.")
                Affichage.EntreePourContinuer()
                return numero_de_pool
            elif choix == 2:
                # regarde si c'est possible
                augmentation_possible = False
                if numero_de_pool == 1 and Player.nombre_de_gold >= 30:
                    augmentation_possible = True
                    Player.nombre_de_gold -= 30
                    Player.gold_in_well += 30
                    numero_de_pool = 2
                elif (
                    numero_de_pool == 2
                    and Player.nombre_de_gold >= 30
                    and Player.points_de_mana >= 10
                ):
                    augmentation_possible = True
                    Player.nombre_de_gold -= 30
                    Player.gold_in_well += 30
                    Player.points_de_mana -= 10
                    numero_de_pool = 3
                elif (
                    numero_de_pool == 3
                    and Player.nombre_de_gold >= 30
                    and Player.points_de_mana >= 10
                    and Player.points_de_vie >= 10
                ):
                    augmentation_possible = True
                    Player.nombre_de_gold -= 30
                    Player.gold_in_well += 30
                    Player.points_de_mana -= 10
                    Player.points_de_vie -= 10
                    numero_de_pool = 4
                elif (
                    numero_de_pool == 4
                    and Player.nombre_de_gold >= 40
                    and Player.points_de_mana >= 20
                    and Player.points_de_vie >= 20
                ):
                    augmentation_possible = True
                    Player.nombre_de_gold -= 40
                    Player.gold_in_well += 40
                    Player.points_de_mana -= 20
                    Player.points_de_vie -= 20
                    numero_de_pool = 5
                elif (
                    numero_de_pool == 5
                    and Player.nombre_de_gold >= 50
                    and Player.points_de_mana >= 25
                    and Player.points_de_vie >= 25
                ):
                    augmentation_possible = True
                    Player.nombre_de_gold -= 50
                    Player.gold_in_well += 50
                    Player.points_de_mana -= 25
                    Player.points_de_vie -= 25
                    numero_de_pool = 6
                elif (
                    numero_de_pool == 6
                    and Player.nombre_de_gold >= 60
                    and Player.points_de_mana >= 30
                    and Player.points_de_vie >= 30
                ):
                    augmentation_possible = True
                    Player.nombre_de_gold -= 60
                    Player.gold_in_well += 60
                    Player.points_de_mana -= 30
                    Player.points_de_vie -= 30
                    numero_de_pool = 8
                if not augmentation_possible:
                    print("Impossible.")
                    Affichage.EntreePourContinuer()
                else:
                    if numero_de_pool == 8:
                        print("Vous approchez votre main de l'étang insaisissable...")
                        print("Mais rien ne se passe.")
                        print("Vous sentez votre force vous quitter...")
                        print(
                            "Vous voyez le ciel changer de couleur plusieurs fois, et la course du soleil s'accélerer."
                        )
                        print(
                            "Vous regardez, impuissant, le mutagène dans votre main devenir poussière."
                        )
                        print("Et soudainement, tout s'arrête.")
                        Affichage.EntreePourContinuer()
                        print(
                            "Vous jettez un coup d'oeil a l'étang, et vous rendez compte que..."
                        )
                        Affichage.EntreePourContinuer()
                    else:
                        print(
                            "Vous approchez votre main de l'étang insaisissable, et un tentacule d'eau s'y accroche."
                        )
                        print(
                            "Ce dernier serpente sur votre peau jusqu'à arriver au niveau du mutagène, qui se met alors a vibrer."
                        )
                        print(
                            "Après ceci, le tentacule repart d'ou il vient, en emportant son dû avec lui."
                        )
                        Affichage.EntreePourContinuer()

    def GetNumeroDePoolDeRecompense(self, choix, chanceux, malchanceux):
        # initialisation de la liste de probabilitée
        if choix == 2:
            if chanceux:
                liste_de_probabilite = [
                    0,
                    7,
                    8,
                    29,
                    30,
                    46,
                    47,
                    61,
                    62,
                    78,
                    79,
                    87,
                    88,
                    89,
                    90,
                    95,
                    96,
                    100,
                ]
            elif malchanceux:
                liste_de_probabilite = [
                    0,
                    30,
                    31,
                    51,
                    52,
                    62,
                    63,
                    73,
                    74,
                    94,
                    95,
                    97,
                    98,
                    98,
                    99,
                    99,
                    100,
                    100,
                ]
            else:
                # liste_de_probabilite = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100]
                liste_de_probabilite = [
                    0,
                    10,
                    11,
                    35,
                    36,
                    55,
                    56,
                    73,
                    74,
                    84,
                    85,
                    90,
                    91,
                    94,
                    96,
                    99,
                    100,
                    100,
                ]
        elif choix == 3:
            if chanceux:
                liste_de_probabilite = [
                    0,
                    0,
                    1,
                    5,
                    6,
                    20,
                    21,
                    45,
                    46,
                    70,
                    71,
                    85,
                    86,
                    88,
                    89,
                    95,
                    96,
                    100,
                ]
            elif malchanceux:
                liste_de_probabilite = [
                    0,
                    30,
                    31,
                    51,
                    52,
                    62,
                    63,
                    73,
                    74,
                    94,
                    95,
                    97,
                    98,
                    98,
                    99,
                    99,
                    100,
                    100,
                ]
            else:
                liste_de_probabilite = [
                    0,
                    5,
                    6,
                    25,
                    26,
                    40,
                    41,
                    63,
                    64,
                    79,
                    80,
                    87,
                    88,
                    90,
                    91,
                    97,
                    98,
                    100,
                ]
        # differents tyes de recompense selon le nombre aleatoire et la liste de probabilité
        nombre_aleatoire = random.randint(0, 100)
        if liste_de_probabilite[0] <= nombre_aleatoire <= liste_de_probabilite[1]:  # 0
            print(
                "...les regardez couler jusqu'à ce que vous ne les voyez plus."
            )  # rien ne se passe
            print("Dur.")
            numero_de_la_pool_de_recompense = 0
        elif (
            liste_de_probabilite[2] <= nombre_aleatoire <= liste_de_probabilite[3]
        ):  # 5
            print(
                "...quelque chose sort de l'étang et vient violemment heurter votre torse !"
            )  # mutagene bleu ou rouge ou vert
            print("C'est un mutagène commun !")
            numero_de_la_pool_de_recompense = 1
        elif (
            liste_de_probabilite[4] <= nombre_aleatoire <= liste_de_probabilite[5]
        ):  # 15
            print("...une noix de coco vous tombe sur la tête.")
            print("C'est un mutagène rare !")  # mutagene dore
            numero_de_la_pool_de_recompense = 2
        elif (
            liste_de_probabilite[6] <= nombre_aleatoire <= liste_de_probabilite[7]
        ):  # 25
            print(
                "...une main boueuse sort des flots ."
            )  # grand mutagene bleu ou rouge ou vert
            print("Elle vous tend un mutagène épique !")
            numero_de_la_pool_de_recompense = 3
        elif (
            liste_de_probabilite[8] <= nombre_aleatoire <= liste_de_probabilite[9]
        ):  # 25
            print(
                "...une boule de chair et de sang vient s'échouer sur la rive."
            )  # mutagene fanatique ou heretique
            print("A l'interieur se trouve un mutagène incarnat !")
            numero_de_la_pool_de_recompense = 4
        elif (
            liste_de_probabilite[10] <= nombre_aleatoire <= liste_de_probabilite[11]
        ):  # 15
            print(
                "...un coquillage a l'aura dorée sort de terre et s'ouvre devant vous !"
            )  # grand mutagene dore
            print("A l'interieur se trouve un mutagène légendaire !")
            numero_de_la_pool_de_recompense = 5
        elif (
            liste_de_probabilite[14] <= nombre_aleatoire <= liste_de_probabilite[15]
        ):  # 7
            print(
                "...l'endroit tout entier se met a scintiller !"
            )  # mutagene permanent (+5 viemax +5 manamax)
            print("Un mutagène mythique apparait dans la paume de votre main !")
            numero_de_la_pool_de_recompense = 6
        elif (
            liste_de_probabilite[12] <= nombre_aleatoire <= liste_de_probabilite[13]
        ):  # 3
            print("...l'étang...disparait.")  # reprend tout le fric dépensé
            print("A sa place se trouve tout les golds que vous avez dépensés !")
            numero_de_la_pool_de_recompense = 7
        elif (
            liste_de_probabilite[16] <= nombre_aleatoire <= liste_de_probabilite[17]
        ):  # 5
            numero_de_la_pool_de_recompense = 8
            return numero_de_la_pool_de_recompense
        Affichage.EntreePourContinuer()
        return numero_de_la_pool_de_recompense

    def AfficheEtangSecret(self):
        mixer.quit()
        print("...l'eau se fait drainer.")  # truc secret
        print("Vous apercevez alors un escalier maintenant émergé, que vous descendez.")
        Affichage.EntreePourContinuer()
        print(
            "Au bout de quelques mètres, la lumière se raréfie. Vous descendez prudemment chaque marches de pierre..."
        )
        Affichage.EntreePourContinuer()
        print("...gluantes...")
        Affichage.EntreePourContinuer()
        print("...glissantes...")
        Affichage.EntreePourContinuer()
        print("...interminables...")
        Affichage.EntreePourContinuer()
        print("...")
        Affichage.EntreePourContinuer()
        print(". . .")
        Affichage.EntreePourContinuer()
        print(".   .   .")
        Affichage.EntreePourContinuer()
        print(".        .       .")
        Affichage.EntreePourContinuer()
        print("et quelque chose vous pousse.")
        PlayMusic("abyss")
        Affichage.EntreePourContinuer()
        print("Vous sentez une pression là ou la  c h o s e  vous a touchée.")
        Affichage.EntreePourContinuer()
        print("Vous sentez l'odeur iodée de la   m e r.")
        Affichage.EntreePourContinuer()
        print("Vous sentez l'odeur métallique du   s  a  n  g.")
        Affichage.EntreePourContinuer()
        print(
            "Vous entendez les sons crispants de la   c  h  a  i  r   qui se déchire."
        )
        Affichage.EntreePourContinuer()
        print("Avez vous touché le fond ? Vous êtes vous écrasé sur le sol ?")
        Affichage.EntreePourContinuer()
        print(". . .  Y - a - t  i l  s e u l e m e n t  u n  f o n d  . . . ")
        Affichage.EntreePourContinuer()
        print(
            "Le bruissement de vos vêtements et le vent froid qui les plaquent contre votre peau humide vous ramène a la raison."
        )
        Affichage.EntreePourContinuer()
        print("Vous êtes entrain de tomber.")
        Affichage.EntreePourContinuer()
        for _ in range(0, 10):
            print("Et la chute est interminable.")
            time.sleep(2.5)
        ClearConsole()
        print("ET")
        Affichage.AfficheAvecUnTempsDattente(3)
        print("LA")
        Affichage.AfficheAvecUnTempsDattente(3)
        print("CHUTE")
        Affichage.AfficheAvecUnTempsDattente(3)
        print("EST")
        Affichage.AfficheAvecUnTempsDattente(3)
        print("INTERMINABLE")
        Affichage.AfficheAvecUnTempsDattente(3)
        print(
            "E  T     L  A     C  H  U  T  E     E  S  T     I  N  T  E  R  M  I  N  A  B  L  E"
        )
        Affichage.AfficheAvecUnTempsDattente(5)
        print("I N T E R M I N A B L E")
        Affichage.AfficheAvecUnTempsDattente(3)
        print("INTERMINABLE")
        Affichage.AfficheAvecUnTempsDattente(3)
        print("interminable")
        Affichage.AfficheAvecUnTempsDattente(3)
        print(" ._.__._..")
        Affichage.AfficheAvecUnTempsDattente(3)
        print("  .___.")
        Affichage.AfficheAvecUnTempsDattente(3)
        print("   ._.")
        Affichage.AfficheAvecUnTempsDattente(3)
        print("    .")
        Affichage.AfficheAvecUnTempsDattente(3)
        print("")
        Affichage.AfficheAvecUnTempsDattente(3)
        print("jjjejejeeeejeje")
        Affichage.AfficheAvecUnTempsDattente(1)
        print("JEJEJEJEJEJEJEJE")
        Affichage.AfficheAvecUnTempsDattente(1)
        print("JEEEEEEEEeeeeEEeeeEe")
        Affichage.AfficheAvecUnTempsDattente(1)
        print("JEEEEEEEEEEEEEEEEEEEE Te")
        Affichage.AfficheAvecUnTempsDattente(1)
        print("J'ai fait un rêve.")
        Affichage.AfficheAvecUnTempsDattente(10)
        print("Dedans, je jouais au coliseum.")
        Affichage.AfficheAvecUnTempsDattente(7)
        print("Une soirée banale, quoi.")
        Affichage.AfficheAvecUnTempsDattente(7)
        print("Et puis a un moment, j'ai vu de la couleur, des images.")
        Affichage.AfficheAvecUnTempsDattente(7)
        print("Des images perturbantes. C'est un jeu textuel après tout.")
        Affichage.AfficheAvecUnTempsDattente(7)
        print("Il n'est pas sensé y en avoir.")
        Affichage.AfficheAvecUnTempsDattente(7)
        print("Et puis j'ai vu un sourire.")
        Affichage.AfficheAvecUnTempsDattente(7)
        print("Il était...cruel.\nFroid.")
        Affichage.AfficheAvecUnTempsDattente(7)
        print("Tout droit sorti d'un documentaire animalier, ou d'une série policière.")
        Affichage.AfficheAvecUnTempsDattente(8)
        print("Le moment ou le suspect fait comprendre qu'il joue avec les agents...")
        Affichage.AfficheAvecUnTempsDattente(8)
        print("Le moment ou la lionne comprend qu'elle a gagnée contre sa proie...")
        Affichage.AfficheAvecUnTempsDattente(8)
        print("...un sourire pervers.")
        Affichage.AfficheAvecUnTempsDattente(7)
        print("...un sourire qui ne respecte pas la vie.")
        Affichage.AfficheAvecUnTempsDattente(7)
        print("...un sourire qui ne tient rien pour sacré.")
        Affichage.AfficheAvecUnTempsDattente(7)
        print("...un sourire...")
        Affichage.AfficheAvecUnTempsDattente(5)
        print("...sadique.")
        Affichage.AfficheAvecUnTempsDattente(5)
        print(
            "Et puis je l'ai vu ouvrir sa bouche en grand, comme pour manger quelque chose."
        )
        Affichage.AfficheAvecUnTempsDattente(8)
        print("Ce soir la, je crois que...")
        Affichage.AfficheAvecUnTempsDattente(8)
        print("...j'ai perdu quelque chose.")
        Affichage.AfficheAvecUnTempsDattente(7)
        print("Quelque chose de vital.")
        Affichage.AfficheAvecUnTempsDattente(7)
        print("D'essentiel.")
        Affichage.AfficheAvecUnTempsDattente(7)
        print("Des souvenirs, des sentiments, un bout de mon âme peut être ?")
        Affichage.AfficheAvecUnTempsDattente(7)
        print("J'ai perdu quelque chose de vital.")
        Affichage.AfficheAvecUnTempsDattente(7)
        print("Mais j'ai gagné une obsession.")
        Affichage.AfficheAvecUnTempsDattente(7)
        print(
            "Quand je me suis réveillé, on aurait dit que mon lit était devenu un étang."
        )
        Affichage.AfficheAvecUnTempsDattente(7)
        print(
            "Dans cette flaque de transpiration, noire comme les ténèbres d'un abysse sans fond,"
        )
        Affichage.AfficheAvecUnTempsDattente(8)
        print("J'y ai vu le reflet d'un mal qui m'a aggripé le bras.")
        Affichage.AfficheAvecUnTempsDattente(8)
        print("Un mal fait de uns, de zéros, de zéros et de uns...")
        Affichage.AfficheAvecUnTempsDattente(12)
        print("...et de uns et de zéros...")
        Affichage.AfficheAvecUnTempsDattente(12)
        print("Quelque chose de digital, en tout point inoffensif.")
        Affichage.AfficheAvecUnTempsDattente(7)
        print("Je crois.")
        Affichage.AfficheAvecUnTempsDattente(7)
        print("...")
        Affichage.AfficheAvecUnTempsDattente(15)
        print("Il faut que je prenne plus de notes.")
        Affichage.AfficheAvecUnTempsDattente(5)
        mixer.quit()
        print(
            "Vous sentez une douleur aigue a la poitrine, et rouvrez les yeux devant l'étang."
        )
        Affichage.EntreePourContinuer()
        print("L'eau y est maintenant noire.")
        Affichage.EntreePourContinuer()
        PlayMusicDeLetage()
        print("...")

    def DoTheFountain(self):
        if Player.fountain_used:
            print(
                "Au détour d'une haie de roses blanches, vous découvrez une magnifique fontaine de marbre."
            )
            print(
                "Des anges sont gravés dans la pierre, ainsi qu'un griffon avec la gueule grande ouverte."
            )
            print(
                "Au centre, sur un petit piedestal se trouve une inscription particulière que vous n'aviez pas vu avant :"
            )
            Affichage.EntreePourContinuer()
            print(
                "*A ceux qui ont besoin de moi, je donne une chance de prouver leur valeur.*"
            )
            print(
                "*A ceux qui ont déjà prouvé leur valeur sans mon aide, j'offre la vigueur du griffon.*"
            )
            print("*Et a ceux qui cherchent plus loin que l'honneur ou la force...*")
            print(
                "*...laissez donc mourir votre âme et votre corps, et venez à ma rencontre.*"
            )
            Affichage.EntreePourContinuer()
            print("Vous laissez la fontaine vide et retournez sur vos pas.")
            Affichage.EntreePourContinuer()
        elif Player.points_de_vie == 1 and Player.points_de_mana == 0:
            mixer.quit()
            print(
                "Au détour d'une haie de roses blanches, vous découvrez une magnifique fontaine de marbre...?"
            )
            print("Ce qui semblait être du marbre prend une teinte pâle, puis verte.")
            Affichage.EntreePourContinuer()
            print("Vous vous approchez prudemment de la fontaine(?).")
            Affichage.EntreePourContinuer()
            numero_du_commentaire = 0
            commentaire = (
                "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                "\nAu centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve un petit morceau de sucre."
            )
            while True:
                while True:
                    try:
                        print(commentaire)
                        if numero_du_commentaire == 11:
                            print("1 - Repartir")
                            print("2 - Boire l'eau(?) de la fontaine")
                            print("3 - Attendre.")
                            print("666 - T r a n c h e r  l a  c h o s e")
                        elif numero_du_commentaire == 12:
                            print("2 - B   O   I   R   E")
                        else:
                            print("1 - Repartir")
                            print("2 - Boire l'eau(?) de la fontaine")
                            print("3 - Attendre.")
                        choix = int(input("Que souhaitez vous faire ? "))
                        ClearConsole()
                        if (
                            (
                                (numero_du_commentaire in range(0, 11))
                                and (choix in [1, 2, 3])
                            )
                            or (
                                (numero_du_commentaire == 11)
                                and (choix in [1, 2, 3, 666])
                            )
                            or ((numero_du_commentaire == 12) and (choix == 2))
                        ):
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 1:
                    print(
                        "Vous laissez...ça...derrière vous et repartez d'ou vous venez en courant."
                    )
                    Affichage.EntreePourContinuer()
                    PlayMusicDeLetage()
                    break
                elif choix == 666:
                    print(
                        "Vous sortez une arme, n'importe laquelle, et sentez votre énergie s'épuiser."
                    )
                    Affichage.AfficheAvecUnTempsDattente(4)
                    print(
                        "Mu par l'énergie du désespoir, les yeux pleins de larmes et de terreur, vous frappez un des yeux gluant de la  c  h  o  s  e !"
                    )
                    Affichage.AfficheAvecUnTempsDattente(5)
                    print(
                        "Un hurlement sanguin se fait entendre dans tout l'étage, et les haies de roses blanches se rapprochent de vous !"
                    )
                    Affichage.AfficheAvecUnTempsDattente(5)
                    print(
                        "Vous tentez de frapper une nouvelle fois, mais vous sentez une résistance au niveau du fourreau de votre arme.."
                    )
                    Affichage.AfficheAvecUnTempsDattente(4)
                    print("Les tentacules se sont enroulés autour de vos pieds !")
                    Affichage.AfficheAvecUnTempsDattente(3)
                    print(
                        "Les haies de roses blanches se rapprochent encore, et le son devient guttural,"
                    )
                    Affichage.AfficheAvecUnTempsDattente(3)
                    print("Comme si la c h o s e était entrain de se réjouir...")
                    Affichage.AfficheAvecUnTempsDattente(3)
                    print(
                        "Vous sentez la peur briser les murs de votre esprit, et les roses blanches entourer votre corps frêle..."
                    )
                    Affichage.AfficheAvecUnTempsDattente(4)
                    print("...pâle...")
                    Affichage.AfficheAvecUnTempsDattente(2)
                    print("...faible...")
                    Affichage.AfficheAvecUnTempsDattente(2)
                    print(
                        "...pile poil assez faible pour se faire a b s o r b e r sans poser de résistance..."
                    )
                    Affichage.AfficheAvecUnTempsDattente(4)
                    print(
                        "...et les roses poussant leurs racines a travers votre peau !"
                    )
                    Affichage.AfficheAvecUnTempsDattente(3)
                    print(
                        "Vous les sentez s'insinuer dans vos pores, prendre place dans vos organes..."
                    )
                    Affichage.AfficheAvecUnTempsDattente(3.5)
                    print(
                        "VOus senteEz Leees TTENTAculEs se MOUVOIR MOUVOIR souS vOtRe Peauuu"
                    )
                    Affichage.AfficheAvecUnTempsDattente(3)
                    print(
                        "Vooouuss VOUS DEbattEZZ cONTre L'enVAhiissEEEEur BIolooogiquee..."
                    )
                    Affichage.AfficheAvecUnTempsDattente(3)
                    print(
                        "Crieezezz a pleeien pouuopooumon, AppellezzZ DESESPEREMETN le MArchand, OUUOU le BOSsssss..."
                    )
                    Affichage.AfficheAvecUnTempsDattente(4)
                    print("EN VAIN EN VAIN EN VAIN EN VAIN EN VAIN Eeeeenenn VAaain")
                    Affichage.AfficheAvecUnTempsDattente(3)
                    print(
                        "VoUs SeNtEz LeS rAcInEs BoUgEr AuToUr De VoS gLoBeS oCcUlAiReS..."
                    )
                    Affichage.AfficheAvecUnTempsDattente(3.5)
                    print("Vou-")
                    Affichage.AfficheAvecUnTempsDattente(0.1)
                    PlayMusicDeLetage()
                    print(
                        "Votre peau se met a picoter, et vous hésitez quelques secondes avant d'engloutir le liquide magique."
                    )
                    Affichage.EntreePourContinuer()
                    print(
                        "L'eau était fraiche ! Vous gagnez 3 points de mana max et reprenez tout vos points de mana !"
                    )
                    Player.points_de_mana_max += 3
                    Player.points_de_mana = Player.points_de_mana_max
                    Affichage.EntreePourContinuer()
                    print("L'eau s'arrête de couler, et la fée disparait dans l'éther.")
                    Player.fountain_used = True
                    print(
                        "Vous laissez la fontaine désormais vide et repartez sur vos pas."
                    )
                    Affichage.EntreePourContinuer()
                    print("...?")
                    Affichage.EntreePourContinuer()
                    print(
                        "Vous manquez de trébucher sur quelque chose qui sort du sol !"
                    )
                    Affichage.EntreePourContinuer()
                    print(
                        "On dirait une main autour de laquelle pousse une rose blanche, tenant dans sa paume un bout de papier..."
                    )
                    Affichage.EntreePourContinuer()
                    print("Vous lisez le bout de papier a voix haute :")
                    Affichage.EntreePourContinuer()
                    print(
                        "*Nb talent disponible colle pas avec menu redcoin ==) nombre de lignes menu redcoin [LE MEME] alors que plus talent. ==) signification particuliere ?*"
                        "\n*nb ligne redcoin ==) Action??(le mot est barré) ==)Menu??(le mot est barré) ==)Ipv4??(le mot est entouré)*"
                    )
                    Affichage.EntreePourContinuer()
                    print(
                        "Vous jetez le bout de papier insensé par terre et regardez quelques instants la main."
                    )
                    Affichage.EntreePourContinuer()
                    print(
                        "Pour une raison qui vous échappe, vous ressentez un frisson en la regardant."
                    )
                    Affichage.EntreePourContinuer()
                    print(
                        "Le gant qui l'habille ne ressemble-t-il pas au votre aussi ?"
                    )
                    Affichage.EntreePourContinuer()
                    print("...")
                    Affichage.EntreePourContinuer()
                    print(". . .")
                    Affichage.EntreePourContinuer()
                    print(".     .     .")
                    Affichage.EntreePourContinuer()
                    print(".               .                   .")
                    Affichage.EntreePourContinuer()
                    print("Meh. Peut etre pas.")
                    Affichage.EntreePourContinuer()
                    break
                elif choix == 3:
                    numero_du_commentaire += 1
                    if numero_du_commentaire == 1:
                        commentaire = (
                            "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                            "\nAu centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve un petit morceau de sucre."
                            "\nIl y a du mouvement dans un buisson proche de vous."
                        )
                    elif numero_du_commentaire == 2:
                        commentaire = (
                            "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                            "\nAu centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve un petit morceau de sucre."
                            "\nUne fée sort du buisson et s'approche du piédestal."
                        )
                    elif numero_du_commentaire == 3:
                        commentaire = (
                            "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                            "\nAu centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve un petit morceau de sucre."
                            "\nLa fée se pose sur le morceau de sucre et commence a le grignoter"
                        )
                    elif numero_du_commentaire == 4:
                        PlayMusic("abyss")
                        commentaire = (
                            "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                            "\nSoudainement, des tentacules sortent des côtés du piedestal et entourent la fée."
                        )
                    elif numero_du_commentaire == 5:
                        commentaire = (
                            "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                            "\nLa fée se débat, et les tentacules se resserent autour de son petit corps."
                        )
                    elif numero_du_commentaire == 6:
                        commentaire = (
                            "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                            "\nLes tentacules verts se font alors de plus en plus fins , et continuent d'entourer la fée dans un cocon serré."
                        )
                    elif numero_du_commentaire == 7:
                        commentaire = (
                            "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                            "\nAu centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve une fée qui a l'air d'être en état de biostase,"
                            "\nmais un examen plus approfondi révèle un cocon de fil la maintenant immobile a quelques centimètre du piédestal."
                        )
                    elif numero_du_commentaire == 8:
                        commentaire = (
                            "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                            "\nAu centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve une fée piégée."
                            "\nVous apercevez les tentacules autour d'elle vibrer, et pomper quelque chose."
                        )
                    elif numero_du_commentaire == 9:
                        commentaire = (
                            "Des anges sont gravés dans la pierre(?), et d'une tête de griffon jaillit une eau(?) noire."
                            "\nAu centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve une fée piégée."
                            "\nLe marbre(NON) reprend la couleur du marbre, la fontaine reprend une apparence de fontaine."
                        )
                    elif numero_du_commentaire == 10:
                        commentaire = (
                            "Des anges sont gravés dans la pierre(FUIS), et d'une tête de griffon se met à jaillir une eau(NON) cristalline."
                            "\nAu centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve une fée en état de biostase(FAUX)."
                        )
                    elif numero_du_commentaire == 11:
                        commentaire = "Des yeux s'ouvrent au niveau de l'abdomen des anges taillés.\nIl vous fixe."
                    else:
                        commentaire = "La c h o s e regarde dans votre âme, et vous sentez votre énergie s'épuiser.\nVos décisions ne vous appartiennent plus.\nC'est trop tard."
                elif choix == 2:
                    numero = 0
                    print("Vous vous accroupissez et plongez les mains dans l'eau...")
                    print("...?")
                    Affichage.EntreePourContinuer()
                    print(
                        "Ce qui semblait être de l'eau est en faite une sorte de gelée collante, et vos mains sont prises dedans !"
                    )
                    Affichage.EntreePourContinuer()
                    commentaire = (
                        "Appuyez sur Entree pour tenter de vous sortir de la !!!"
                    )
                    while True:
                        input(commentaire)
                        ClearConsole()
                        if numero in range(0, 16):
                            commentaire = (
                                "Appuyez sur Entree pour tenter de vous sortir de la !!"
                            )
                            numero += 1
                        elif numero in range(16, 31):
                            commentaire = (
                                "Appuyez sur Entree pour tenter de vous sortir de la !"
                            )
                            numero += 1
                        elif numero in range(31, 46):
                            commentaire = (
                                "Appuyez sur Entree pour tenter de vous sortir de la..."
                            )
                            numero += 1
                        elif numero in range(46, 61):
                            commentaire = (
                                "Appuyez sur Entree pour tenter de vous sortir..."
                            )
                            numero += 1
                        elif numero in range(61, 76):
                            commentaire = "Appuyez sur Entree pour tenter..."
                            numero += 1
                        elif numero in range(76, 91):
                            commentaire = "Appuyez sur Entree pour..."
                            numero += 1
                        elif numero in range(91, 106):
                            commentaire = "..."
                            numero += 1
                        elif numero in range(106, 151):
                            commentaire = (
                                "C'est trop tard.\nVous êtes surement déja mort."
                            )
                            numero += 1
                        else:
                            commentaire = ""
                            for _ in range(1, 100):
                                commentaire += "MORS|ACERBIOR|EST|CUM|IN|NEGATIONE|ADHAESISTI|SICUT|MUSCAE|IN|CARNIVOR|PLANTAE|"
        elif Player.boss_battu and (Player.nombre_dennemis_a_letage == 0):
            while True:
                try:
                    print(
                        "Au détour d'une haie de roses blanches, vous découvrez une magnifique fontaine de marbre."
                    )
                    print(
                        "Des anges sont gravés dans la pierre, et d'une tête de griffon jaillit une eau rose bonbon."
                    )
                    print(
                        "Au centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve un petit corps en décomposition."
                    )
                    print("1 - Ne rien faire")
                    print("2 - Boire l'eau(?) de la fontaine")
                    choix = int(input("Que souhaitez vous faire ? "))
                    ClearConsole()
                    if choix in [1, 2]:
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print("Vous laissez la fontaine et repartez sur vos pas.")
                Affichage.EntreePourContinuer()
            else:
                print(
                    "Vous mettez vos mains en cul-de-poule et les remplissez avec l'eau de la fontaine."
                )
                print(
                    "Une vague et délicieuse odeur d'aromates, de liqueur de cèdre, de poudre de santal, de myrrhe et de cinnamome se répend dans la paume de vos mains."
                )
                print(
                    "Votre peau se met a bruler, et vous hésitez quelques secondes avant d'engloutir le liquide visqueux."
                )
                Affichage.EntreePourContinuer()
                print(
                    "L'eau avait un gout de violette ! Vous gagnez 15 points de mana/vie max et reprenez tout vos points de mana/vie !"
                )
                Player.points_de_mana_max += 15
                Player.points_de_mana = Player.points_de_mana_max
                Player.points_de_vie_max += 15
                Player.points_de_vie = Player.points_de_vie_max
                Affichage.EntreePourContinuer()
                print("L'eau s'arrête de couler, et le cadavre disparait dans l'éther.")
                Player.fountain_used = True
                print(
                    "Vous laissez la fontaine désormais vide et repartez sur vos pas."
                )
                Affichage.EntreePourContinuer()
        else:
            while True:
                try:
                    print(
                        "Au détour d'une haie de roses blanches, vous découvrez une magnifique fontaine de marbre."
                    )
                    print(
                        "Des anges sont gravés dans la pierre, et d'une tête de griffon jaillit une eau cristalline."
                    )
                    print(
                        "Au centre, sur un petit piedestal enfoncé a mi-hauteur dans l'eau, se trouve une fée en état de biostase."
                    )
                    print("1 - Ne rien faire")
                    print("2 - Boire l'eau de la fontaine")
                    print("3 - Attraper la fée dans un bocal")
                    choix = int(input("Que souhaitez vous faire ? "))
                    ClearConsole()
                    if choix in [1, 2, 3]:
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print("Vous laissez la fontaine et repartez sur vos pas.")
                Affichage.EntreePourContinuer()
            elif choix == 2:
                print(
                    "Vous mettez vos mains en cul-de-poule et les remplissez avec l'eau de la fontaine."
                )
                print(
                    "Votre peau se met a picoter, et vous hésitez quelques secondes avant d'engloutir le liquide magique."
                )
                Affichage.EntreePourContinuer()
                nombre_aleatoire = random.randint(1, 2)
                if nombre_aleatoire == 1:
                    print(
                        "L'eau était fraiche ! Vous gagnez 3 points de mana max et reprenez tout vos points de mana !"
                    )
                    Player.points_de_mana_max += 3
                    Player.points_de_mana = Player.points_de_mana_max
                else:
                    print(
                        "L'eau était chaude ! Vous gagnez 3 points de vie max et reprenez tout vos points de vie !"
                    )
                    Player.points_de_vie_max += 3
                    Player.points_de_vie = Player.points_de_vie_max
                Affichage.EntreePourContinuer()
                print("L'eau s'arrête de couler, et la fée disparait dans l'éther.")
                Player.fountain_used = True
                print(
                    "Vous laissez la fontaine désormais vide et repartez sur vos pas."
                )
                Affichage.EntreePourContinuer()
            elif choix == 3:
                print(
                    "Vous vous approchez de la fée et la mettez dans votre flacon d'un coup rapide."
                )
                print("Vous obtenez une Fée dans un Bocal !")
                Affichage.EntreePourContinuer()
                if Player.possede_une_fee:
                    PlaySound("death")
                    print(
                        "Alors que vous rangiez votre bocal dans votre sacoche,"
                        " vous voyez les deux fées unir leur pouvoir a travers"
                        " les bocaux pour briser leur cage de verre et s'enfuir."
                    )
                    Player.possede_une_fee = False
                    Affichage.EntreePourContinuer()
                    PlaySound("death")
                    print("Et l'eau s'arrête de couler.")
                    Affichage.EntreePourContinuer()
                    print("Vous avez...tout perdu.")
                    print("Votre fée, la fée de la fontaine, et l'eau de la fontaine.")
                    Affichage.EntreePourContinuer()
                    print(
                        "A ce point la, ca ne serait même pas étonnant que les fees se sont échappées avec tout votre gold !"
                    )
                    Affichage.EntreePourContinuer()
                    PlaySound("death")
                    print("Parce que c'est le cas.")
                    print("Vous n'avez plus un gold a votre nom.")
                    Player.nombre_de_gold = 0
                    Affichage.EntreePourContinuer()
                    print(
                        "Vous laissez la fontaine désormais vide et repartez sur vos pas, une expression traumatisée et misérable désormais accrochée a votre visage."
                    )
                    Affichage.EntreePourContinuer()
                    PlaySound("death")
                    print(
                        "Qui vous empeche de voir une branche a votre hauteur, que vous vous prenez en pleine poire."
                    )
                    Affichage.EntreePourContinuer()
                    degat = Player.points_de_vie - 1
                    Player.points_de_vie = 1
                    PlaySound("death")
                    print(f"Vous perdez {degat} points de vie.")
                    Affichage.EntreePourContinuer()
                    PlaySound("death")
                    print("Le choc vous fait craquer.")
                    print(
                        "Vous vous mettez en position fétale et pleurez toute les larmes de votre corps."
                    )
                    Affichage.EntreePourContinuer()
                    print(
                        "Votre crise de nerf vous touche au plus profond de votre âme."
                    )
                    Affichage.EntreePourContinuer()
                    degat = Player.points_de_mana - 1
                    Player.points_de_mana = 1
                    PlaySound("death")
                    print(f"Vous perdez {degat} points de mana.")
                    Affichage.EntreePourContinuer()
                    print("J'espère que vous avez fait une sauvegarde...")
                    Affichage.EntreePourContinuer()
                    print("...")
                    Affichage.EntreePourContinuer()
                    print("...sinon, voila un peu de musique pour vous réconforter.")
                    Affichage.EntreePourContinuer()
                    PlayMusic("reconfort")
                else:
                    Player.possede_une_fee = True
                    print("L'eau s'arrête de couler.")
                    print(
                        "Vous laissez la fontaine désormais vide et repartez sur vos pas."
                    )
                    Affichage.EntreePourContinuer()

    def DoTheLibrary(self):
        # Recuperation de la liste de sorts enregistrés
        donnees_de_s0ve = self.GetPermanentThingsFromS0ve()
        liste_de_sorts_enregistres = ast.literal_eval(donnees_de_s0ve["Livre de sort"])
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire in [1, 2, 3]:
            liste_de_sorts_enregistres = [
                "jegardeleseigneurdevantmoisansrelâche;ilestàmadroite:jesuisinébranlable"
            ]
        print(
            "Derrière un rocher, vous trouvez un ancien passage quasi-effondré menant a une petite pièce étroite."
        )
        print(
            "Au milieu se tient un livre usé par le temps, dont la couverture représente une magnifique cigogne bleue regardant vers la droite."
        )
        print("Vous ouvrez le livre...")
        Affichage.EntreePourContinuer()
        if Player.library_used:
            print("...mais ce dernier est vide.")
            print("Vous le refermez et repartez ailleurs.")
            Affichage.EntreePourContinuer()
        else:
            if (
                "jegardeleseigneurdevantmoisansrelâche;ilestàmadroite:jesuisinébranlable"
                in liste_de_sorts_enregistres
            ):
                mixer.quit()
            while True:
                try:
                    print(
                        "A l'interieur se trouvent plusieurs lignes écrite à l'encre noire."
                        "\nCertaines sont effacées, mais celles qui ne le sont pas semblent attirer votre main..."
                    )
                    numero_a_afficher = 1
                    for sort in liste_de_sorts_enregistres:
                        print(f"{numero_a_afficher} - Toucher les mots [{sort}]")
                        numero_a_afficher += 1
                    liste_dartefact_debloque = []
                    if not (
                        "jegardeleseigneurdevantmoisansrelâche;ilestàmadroite:jesuisinébranlable"
                        in liste_de_sorts_enregistres
                    ):
                        donnees_de_s0ve = Observation.GetPermanentThingsFromS0ve()
                        liste_dartefact_debloque = ast.literal_eval(donnees_de_s0ve["Artefact Debloques"])
                        for artefact in liste_dartefact_debloque:
                            print(f"{numero_a_afficher} - Toucher les mots [{artefact}]")
                            numero_a_afficher += 1
                    print(f"{numero_a_afficher} - Ne rien toucher")
                    choix = int(input("Que souhaitez vous faire ? "))
                    ClearConsole()
                    if choix in range(1, (len(liste_de_sorts_enregistres) + len(liste_dartefact_debloque) + 2)):
                        break
                except ValueError:
                    ClearConsole()
            if choix == (len(liste_de_sorts_enregistres) + len(liste_dartefact_debloque) + 1):
                print("Vous refermez le livre et vous éloignez de la pièce.")
                Affichage.EntreePourContinuer()
            elif (("jegardeleseigneurdevantmoisansrelâche;ilestàmadroite:jesuisinébranlable" in liste_de_sorts_enregistres)
                  and (choix == 1)
            ):
                PlayMusic("abyss")
                print("C3 n'est pas vous.")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("Ca 6'est pas possible.")
                Affichage.AfficheAvecUnTempsDattente(5)
                print("Vous 2'êtes jamais passé par la...")
                Affichage.AfficheAvecUnTempsDattente(5)
                print(
                    "...et c9 n'est pourtant pas la premiere fois que vous venez ici."
                )
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
                if Player.points_de_vie > Player.points_de_vie_max:
                    Player.points_de_vie = Player.points_de_vie_max
                print(
                    "Alors que vos doigts effleurent les lettres, l'entieretée de l'encre sur la page se rassemble au centre et saute sur votre main."
                    "\nElle se répend le long de votre membre, s'infiltre par vos pores, et fait apparaitre sur votre bras un tatouage étrange et douloureux."
                )
                Affichage.EntreePourContinuer()
                print("Vous perdez 5 points de vie max !")
                Player.points_de_vie_max -= 5
                Affichage.EntreePourContinuer()
                if choix > len(liste_de_sorts_enregistres) :
                    artefact = liste_dartefact_debloque[choix - (len(liste_de_sorts_enregistres) + 1)]
                    print(f"Un artefact se materialise dans la paume de votre main !")
                    Affichage.EntreePourContinuer()
                    FloorMaker.GiveRandomArtefact(artefact)
                else:
                    sort = liste_de_sorts_enregistres[choix - 1]
                    print(f"Vous gagnez le sort [{sort}] !")
                    Affichage.EntreePourContinuer()
                    Player.sorts_possedes.append(sort)
                    if "Syra" in Player.liste_dartefacts_optionels:
                        print("Grace au verre de Syra que vous avez bu, vous gagnez aussi 10 pv max !")
                        Player.points_de_vie += 10
                        Player.points_de_vie_max += 10
                        Affichage.EntreePourContinuer()
                print(
                    "La page est maintenant vide.\nVous refermez le livre et repartez ailleurs."
                )
                Affichage.EntreePourContinuer()
        if (
            "jegardeleseigneurdevantmoisansrelâche;ilestàmadroite:jesuisinébranlable"
            in liste_de_sorts_enregistres
        ):
            PlayMusicDeLetage()

    def GetPermanentThingsFromS0ve(self):
        dictionnaire_de_choses_permanentes = {}
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # fichier de sauvegarde (permanant)
        if os.path.isfile(dir_path + "\\s1ve.txt"):
            chemin_du_fichier_save = dir_path + "\\s1ve.txt"
        else:
            chemin_du_fichier_save = dir_path + "\\s0ve.txt"
        with open(chemin_du_fichier_save, "r") as fichier:
            reader = csv.DictReader(fichier, delimiter="|")
            for line in reader:
                dictionnaire_de_choses_permanentes[line["Caracteristique"]] = line[
                    "Valeur"
                ]
        return dictionnaire_de_choses_permanentes
    


    def SetPermanentThingsToS0ve(self, dictionnaire_de_choses_permanentes):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        if os.path.isfile(dir_path + "\\s1ve.txt"):
            chemin_du_fichier_save = dir_path + "\\s1ve.txt"
        else:
            chemin_du_fichier_save = dir_path + "\\s0ve.txt"
        with open(chemin_du_fichier_save, "w") as fichier:
            fichier.write("Caracteristique|Valeur")
            for caracteristic in dictionnaire_de_choses_permanentes:
                fichier.write(
                    f"\n{caracteristic}|{dictionnaire_de_choses_permanentes[caracteristic]}"
                )


class SaveManagement:

    def __init__(self):
        self.dictionnaire_de_sauvegarde = {}

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
        self.dictionnaire_de_sauvegarde["Points de mana max"] = (
            Player.points_de_mana_max
        )
        self.dictionnaire_de_sauvegarde["Points de mana"] = Player.points_de_mana
        self.dictionnaire_de_sauvegarde["Points d'endurance"] = Player.points_dendurance
        self.dictionnaire_de_sauvegarde["Points de force"] = Player.points_de_force
        self.dictionnaire_de_sauvegarde["Points d'intelligence"] = (
            Player.points_dintelligence
        )
        self.dictionnaire_de_sauvegarde["Points de defence"] = Player.points_de_defence
        self.dictionnaire_de_sauvegarde["Chance de coup critique"] = (
            Player.taux_coup_critique
        )
        self.dictionnaire_de_sauvegarde["Degat de coup critique"] = (
            Player.degat_coup_critique
        )
        self.dictionnaire_de_sauvegarde["Chance de sort critique"] = (
            Player.taux_sort_critique
        )
        self.dictionnaire_de_sauvegarde["Degat de sort critique"] = (
            Player.degat_sort_critique
        )
        self.dictionnaire_de_sauvegarde["Chance d'esquive"] = Player.taux_desquive
        self.dictionnaire_de_sauvegarde["Nombre de gold"] = Player.nombre_de_gold
        self.dictionnaire_de_sauvegarde["Nombre de Redcoins"] = (
            Player.nombre_de_red_coin
        )
        self.dictionnaire_de_sauvegarde["Nombre de monstres tués"] = (
            Player.nombre_de_monstres_tues
        )
        self.dictionnaire_de_sauvegarde["Numéro de l'etage"] = Player.numero_de_letage
        self.dictionnaire_de_sauvegarde["Quete en cours"] = Player.quete
        self.dictionnaire_de_sauvegarde["Quete complétées"] = Player.quete_complete
        self.dictionnaire_de_sauvegarde["Le Boss a ete Battu"] = Player.boss_battu
        self.dictionnaire_de_sauvegarde[
            "Commentaire pour l'affichage du Boss dans le menu"
        ] = Player.commentaire_boss
        self.dictionnaire_de_sauvegarde["Nombre d'ennemis restant a l'étage"] = (
            Player.nombre_dennemis_a_letage
        )
        self.dictionnaire_de_sauvegarde["Le Redcoin d'extermination a ete recu"] = (
            Player.red_coin_recu_par_extermination
        )
        self.dictionnaire_de_sauvegarde["Le Redcoin du marchand a ete achete"] = (
            Player.redcoin_bought
        )
        self.dictionnaire_de_sauvegarde["Nombre de Tirage acheté"] = (
            Player.number_of_tirage
        )
        self.dictionnaire_de_sauvegarde["Possede une gemme de vie"] = (
            Player.gemme_de_vie
        )
        self.dictionnaire_de_sauvegarde["Possede une gemme de mana"] = (
            Player.gemme_de_mana
        )
        self.dictionnaire_de_sauvegarde["Possede une fée"] = Player.possede_une_fee
        self.dictionnaire_de_sauvegarde["Le livre de sort a ete utilise"] = (
            Player.library_used
        )
        self.dictionnaire_de_sauvegarde["Actions oubliées"] = (
            Player.liste_daction_oubliees
        )
        self.dictionnaire_de_sauvegarde["Le livre de sort final a ete utilise"] = (
            Player.final_library_used
        )
        self.dictionnaire_de_sauvegarde["La vieille dame a été soignée"] = (
            Player.mercant_healed
        )
        self.dictionnaire_de_sauvegarde["La fontaine a ete utilise"] = (
            Player.fountain_used
        )
        self.dictionnaire_de_sauvegarde["Nombre de Gold dans l'étang"] = (
            Player.gold_in_well
        )
        self.dictionnaire_de_sauvegarde["Donneur de quetes"] = Player.quest_giver
        self.dictionnaire_de_sauvegarde["Possede la clé"] = Player.possede_la_cle
        self.dictionnaire_de_sauvegarde["Etage alternatif"] = Player.etage_alternatif
        self.dictionnaire_de_sauvegarde["Blueprint de l'étage"] = (
            FloorMaker.FloorBlueprint
        )
        self.dictionnaire_de_sauvegarde["Liste d'artefacts optionnels"] = (
            Player.liste_dartefacts_optionels
        )
        self.dictionnaire_de_sauvegarde["Nombre de Sacrifices"] = (
            Player.nombre_de_sacrifices
        )
        self.dictionnaire_de_sauvegarde["Nom de l'étage"] = (
            Player.nom_de_letage
        )
        self.dictionnaire_de_sauvegarde["Musique Etage 10"] = (
            Player.musique_etage_10
        )
        self.dictionnaire_de_sauvegarde["Musique Combat 10"] = (
            Player.musique_combat_10
        )
        self.dictionnaire_de_sauvegarde["Numéro du boss Alt"] = (
            Player.numero_boss_alt
        )

    def FromDictToPlayer(self):
        Player.nom_du_personnage = (self.dictionnaire_de_sauvegarde["Nom"]).strip('"')
        Player.stigma_positif = (
            self.dictionnaire_de_sauvegarde["Stigma Positif"]
        ).strip('"')
        Player.stigma_negatif = (
            self.dictionnaire_de_sauvegarde["Stigma Négatif"]
        ).strip('"')
        Player.musique_etage_10 = (
            self.dictionnaire_de_sauvegarde["Musique Etage 10"]
        ).strip('"')
        Player.musique_combat_10 = (
            self.dictionnaire_de_sauvegarde["Musique Combat 10"]
        ).strip('"')
        Player.stigma_bonus = (self.dictionnaire_de_sauvegarde["Stigma Bonus"]).strip(
            '"'
        )
        chaine_de_caractere = self.dictionnaire_de_sauvegarde["Techniques"]
        liste_de_technique = ast.literal_eval(chaine_de_caractere)
        Player.techniques_possedes = liste_de_technique
        chaine_de_caractere = self.dictionnaire_de_sauvegarde["Sorts"]
        liste_de_sorts = ast.literal_eval(chaine_de_caractere)
        Player.sorts_possedes = liste_de_sorts
        chaine_de_caractere = self.dictionnaire_de_sauvegarde["Actions oubliées"]
        liste_dactions = ast.literal_eval(chaine_de_caractere)
        Player.liste_daction_oubliees = liste_dactions
        chaine_de_caractere = self.dictionnaire_de_sauvegarde["Items"]
        dictionaire_de_item = ast.literal_eval(chaine_de_caractere)
        Player.items_possedes = dictionaire_de_item
        chaine_de_caractere = self.dictionnaire_de_sauvegarde["Talents"]
        liste_de_talent = ast.literal_eval(chaine_de_caractere)
        Player.talents_possedes = liste_de_talent
        Player.points_de_vie_max = int(
            self.dictionnaire_de_sauvegarde["Points de vie max"]
        )
        Player.numero_boss_alt = int(
            self.dictionnaire_de_sauvegarde["Numéro du boss Alt"]
        )
        Player.points_de_vie = int(self.dictionnaire_de_sauvegarde["Points de vie"])
        Player.points_de_mana_max = int(
            self.dictionnaire_de_sauvegarde["Points de mana max"]
        )
        Player.points_de_mana = int(self.dictionnaire_de_sauvegarde["Points de mana"])
        Player.points_dendurance = int(
            self.dictionnaire_de_sauvegarde["Points d'endurance"]
        )
        Player.points_de_force = int(self.dictionnaire_de_sauvegarde["Points de force"])
        Player.points_dintelligence = int(
            self.dictionnaire_de_sauvegarde["Points d'intelligence"]
        )
        Player.points_de_defence = int(
            self.dictionnaire_de_sauvegarde["Points de defence"]
        )
        Player.taux_coup_critique = int(
            self.dictionnaire_de_sauvegarde["Chance de coup critique"]
        )
        Player.degat_coup_critique = int(
            self.dictionnaire_de_sauvegarde["Degat de coup critique"]
        )
        Player.taux_sort_critique = int(
            self.dictionnaire_de_sauvegarde["Chance de sort critique"]
        )
        Player.degat_sort_critique = int(
            self.dictionnaire_de_sauvegarde["Degat de sort critique"]
        )
        Player.taux_desquive = int(self.dictionnaire_de_sauvegarde["Chance d'esquive"])
        Player.nombre_de_gold = int(self.dictionnaire_de_sauvegarde["Nombre de gold"])
        Player.nombre_de_red_coin = int(
            self.dictionnaire_de_sauvegarde["Nombre de Redcoins"]
        )
        Player.nombre_de_monstres_tues = int(
            self.dictionnaire_de_sauvegarde["Nombre de monstres tués"]
        )
        Player.numero_de_letage = int(
            self.dictionnaire_de_sauvegarde["Numéro de l'etage"]
        )
        Player.affronte_un_boss = False
        Player.affronte_une_mimique = False
        Player.gemme_de_vie = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Possede une gemme de vie"]
        )
        Player.gemme_de_mana = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Possede une gemme de mana"]
        )
        Player.possede_une_fee = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Possede une fée"]
        )
        Player.quete = (self.dictionnaire_de_sauvegarde["Quete en cours"]).strip('"')
        Player.quete_complete = self.dictionnaire_de_sauvegarde["Quete complétées"]
        chaine_de_caractere = self.dictionnaire_de_sauvegarde["Quete complétées"]
        liste_de_quete_complete = ast.literal_eval(chaine_de_caractere)
        Player.quete_complete = liste_de_quete_complete
        Player.boss_battu = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Le Boss a ete Battu"]
        )
        Player.commentaire_boss = (
            self.dictionnaire_de_sauvegarde[
                "Commentaire pour l'affichage du Boss dans le menu"
            ]
        ).strip('"')
        Player.nom_de_letage = (
            self.dictionnaire_de_sauvegarde[
                "Nom de l'étage"
            ]
        ).strip('"')
        Player.nombre_dennemis_a_letage = int(
            self.dictionnaire_de_sauvegarde["Nombre d'ennemis restant a l'étage"]
        )
        Player.red_coin_recu_par_extermination = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Le Redcoin d'extermination a ete recu"]
        )
        Player.redcoin_bought = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Le Redcoin du marchand a ete achete"]
        )
        Player.number_of_tirage = int(
            self.dictionnaire_de_sauvegarde["Nombre de Tirage acheté"]
        )
        Player.nombre_de_sacrifices = int(
            self.dictionnaire_de_sauvegarde["Nombre de Sacrifices"]
        )
        Player.library_used = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Le livre de sort a ete utilise"]
        )
        Player.final_library_used = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Le livre de sort final a ete utilise"]
        )
        Player.quest_giver = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Donneur de quetes"]
        )
        Player.mercant_healed = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["La vieille dame a été soignée"]
        )
        Player.fountain_used = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["La fontaine a ete utilise"]
        )
        Player.possede_la_cle = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Possede la clé"]
        )
        Player.etage_alternatif = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Etage alternatif"]
        )
        Player.gold_in_well = int(
            self.dictionnaire_de_sauvegarde["Nombre de Gold dans l'étang"]
        )
        chaine_de_caractere = self.dictionnaire_de_sauvegarde["Blueprint de l'étage"]
        dictionaire_de_letage = ast.literal_eval(chaine_de_caractere)
        FloorMaker.FloorBlueprint = dictionaire_de_letage
        chaine_de_caractere = self.dictionnaire_de_sauvegarde[
            "Liste d'artefacts optionnels"
        ]
        liste_de_artefacts_option = ast.literal_eval(chaine_de_caractere)
        Player.liste_dartefacts_optionels = liste_de_artefacts_option

    def FromDictToSaveFile(self, nom_du_fichier):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        chemin_du_fichier_save = dir_path + nom_du_fichier
        with open(chemin_du_fichier_save, "w") as fichier:
            fichier.write("Caracteristique|Valeur")
            for caracteristic in self.dictionnaire_de_sauvegarde:
                fichier.write(
                    f"\n{caracteristic}|{self.dictionnaire_de_sauvegarde[caracteristic]}"
                )

    def FromSaveFileToDict(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # fichier de sauvegarde (temporaire)
        chemin_du_fichier_save = dir_path + "\\save.txt"
        with open(chemin_du_fichier_save, "r") as fichier:
            reader = csv.DictReader(fichier, delimiter="|")
            for line in reader:
                self.dictionnaire_de_sauvegarde[line["Caracteristique"]] = line[
                    "Valeur"
                ]
        # autre sauvegarde (permanente)
        if Player.mode_de_jeu == "Ascension":
            chemin_du_fichier_save = dir_path + "\\s1ve.txt"
        else:
            chemin_du_fichier_save = dir_path + "\\s0ve.txt"
        with open(chemin_du_fichier_save, "r") as fichier:
            reader = csv.DictReader(fichier, delimiter="|")
            for line in reader:
                if line["Caracteristique"] in ["Invitation Recue"]:
                    self.dictionnaire_de_sauvegarde[line["Caracteristique"]] = line[
                        "Valeur"
                    ]

    def SaveTheGame(self):
        self.FromPlayerToDict()
        self.FromDictToSaveFile("\\save.txt")
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

    def SaveTheGameSansAffichage(self):
        if Player.mode_de_jeu != "Ascension":
            self.FromPlayerToDict()
            self.FromDictToSaveFile("\\save.txt")

    def LoadTheGame(self):
        self.FromSaveFileToDict()
        self.FromDictToPlayer()
        return True

class EndingAndGift:

    def __init__(self):
        pass

    def DoEnding(self):
        #utilise showstory, dolastfight et givegift pour montrer la fin d'un personnage en particulier.
        
        #affiche l'histoire de ceux qui ont finit
        self.ShowStory(Player.nom_du_personnage, True)

        
        # pour ceux qui ont des combats a faire : fait le combat et affiche un autre bout d'histoire.
        if Player.nom_du_personnage in ["Saumel", "Elma", "Vesperum", "Peralta", "Bob Doré"]:
            self.DoLastFight()
            self.ShowStory(Player.nom_du_personnage, False)

        # donne l'artefact récompense, si il y a a faire
        self.GiveGift()

        PlayMusic("battle_win")
        print("Vous avez terminé le jeu !")
        Affichage.EntreePourContinuer()
        print("Changez de personnage et retentez l'aventure !")
        print("Qui sait combien d'artefacts il reste à débloquer, ou de secrets a découvrir...")
        Affichage.EntreePourContinuer()
        Affichage.ShowDeath(True)


    def ShowStory(self, nom, avant_le_combat):
        #lance une introduction
        if avant_le_combat:
            self.ShowBeginingOfEnding()
        else:
            PlayMusic("finale")

        #print ce qu'il faut print
        if nom == "Saumel":
            if avant_le_combat:
                print("")
                Affichage.EntreePourContinuer()
            else:
                print("")
                Affichage.EntreePourContinuer()
        elif nom == "Elma":  # DONE
            if avant_le_combat:
                self.PrintEtEntreePourContinuer("Elma sortit du Coliseum, la tête haute.")
                self.PrintEtEntreePourContinuer("Son corps brisé , maintenu par la magie regénératrice des fées, avait tenu pendant tout le périple...")
                self.PrintEtEntreePourContinuer("...mais elle savait qu'il ne tiendrait pas longtemps en dehors des murs saturés de mana.")
                self.PrintEtEntreePourContinuer("Elle pourrait peut etre se refugier ailleurs ? Finir sa vie dans un hopital ?")
                self.PrintEtEntreePourContinuer("Après tout, elle avait gagné bien plus d'argent qu'en une vie de fouinage et cambriolage intempestif.")
                self.PrintEtEntreePourContinuer("Elle pourrait très bien s'acheter la pièce la plus luxueuse du service geriatrie d'un hopital privé quelquonque.")
                self.PrintEtEntreePourContinuer("Ensuite, elle pourrait acheter toute les gourmandises dont elle révait, étant enfant.")
                self.PrintEtEntreePourContinuer("Peut etre aussi engager un écrivain fantome, pour pouvoir laisser une marque de son passage.")
                self.PrintEtEntreePourContinuer("Elma avait tant de choses a raconter..")
                self.PrintEtEntreePourContinuer("Tant d'histoires, d'alliés tombés, de trahisons...")
                self.PrintEtEntreePourContinuer("...d'un amour interdit avec un capitaine de garde...")
                self.PrintEtEntreePourContinuer("Elle avait survécu a tout ce que l'être humain a de meilleur et de pire a offrir.")
                self.PrintEtEntreePourContinuer("Et comme tant d'autre personnes de son âge, elle avait...")
                self.PrintEtEntreePourContinuer("...tant de choses...")
                self.PrintEtEntreePourContinuer("...a raconter...")
                self.PrintEtEntreePourContinuer("...")
                self.PrintEtEntreePourContinuer("Mais ce n'est pas comme ca que la Princesse de Suie finirait sa vie.")
                self.PrintEtEntreePourContinuer("Elle marcha d'un pas lent, furtif, vers la ville la plus proche.")
                self.PrintEtEntreePourContinuer("Tap, Tap.")
                self.PrintEtEntreePourContinuer("Elle s'approcha d'un magasin miteux, et sussurra un message codé a l'oreille du commercant incrédule.")
                self.PrintEtEntreePourContinuer("Tap, Tap.")
                self.PrintEtEntreePourContinuer("Elle prit des informations utiles dans un stand de journal particulier.")
                self.PrintEtEntreePourContinuer("Tap, Tap.")
                self.PrintEtEntreePourContinuer("Elle vola un portefeuille rempli a un couple qui passait par la.")
                self.PrintEtEntreePourContinuer("Tap, Tap.")
                self.PrintEtEntreePourContinuer("Elle attendit l'heure fatidigue dans une chambre d'hotel a trois pas d'une décharge municipale.")
                self.PrintEtEntreePourContinuer("Tap, Tap.")
                self.PrintEtEntreePourContinuer("Elle se faufila en plein coeur de la nuit, dans un espace ouvert entre deux planches.")
                self.PrintEtEntreePourContinuer("Tap, Tap.")
                self.PrintEtEntreePourContinuer("Elle s'approcha d'une masse informe d'individu difformes, éclairés seulement par la lueur irrégulière de quelques bidons enflammés.")
                self.PrintEtEntreePourContinuer("Tap, Tap.")
                self.PrintEtEntreePourContinuer("Elle se présenta devant le nouveau Prince des Voleurs, dont la couronne de plastique reposait dans les mains du prêtre qui devait la lui remettre.")
                self.PrintEtEntreePourContinuer("Tap, Tap.")
                self.PrintEtEntreePourContinuer("Yvan vit la terreur dans les yeux des anciens et anciennes du Clan, autour de lui.")
                self.PrintEtEntreePourContinuer("Tap, Tap.")
                self.PrintEtEntreePourContinuer("Il fit volte face, et tomba nez à nez avec celle qu'il avait jeté dans les griffes de la mort, quelques heures auparavant.")
                self.PrintEtEntreePourContinuer("Tap, Tap.")
                self.PrintEtEntreePourContinuer("*Tu... n'as pas la force de triompher.*")
                self.PrintEtEntreePourContinuer("*C'est vrai Yvan.*")
                self.PrintEtEntreePourContinuer("*Alors... comment ?*")
                self.PrintEtEntreePourContinuer("Tap, Tap.")
                self.PrintEtEntreePourContinuer("*Tu semble avoir oublié quelque chose, Yvan.*")
                self.PrintEtEntreePourContinuer("*Faire parti du Clan, ce n'est pas chasser la force, ou la gloire.*")
                self.PrintEtEntreePourContinuer("*C'est s'allier pour survivre, nous qui sommes trop faible.*")
                self.PrintEtEntreePourContinuer("*Et être la régente d'un tel Clan...*")
                self.PrintEtEntreePourContinuer("Elma se frappa deux fois le torse, pour faire battre son misérable coeur que la force avait déserté.")
                self.PrintEtEntreePourContinuer("*...c'est savoir survivre, quoi qu'il en coute.*")
                self.PrintEtEntreePourContinuer("Yvan laissa s'échapper un sourire tordu.")
                self.PrintEtEntreePourContinuer("*Un cadavre ambulant ? Un cafard sans vie ? Voila ce qu'était la fameuse Princesse de Suie ???*")
                self.PrintEtEntreePourContinuer("*Je vais régner sur le Clan d'une main de fer, et utiliser la force pour le rendre invincible !*")
                mixer.quit()
                self.PrintEtEntreePourContinuer("Elma regarda Yvan avec la tendresse que seule une mère pourrait ressentir.")
                PlaySound("intro_story_final")
                self.PrintEtEntreePourContinuerIntro("*Alors...*", 3.5)
                self.PrintEtEntreePourContinuerIntro("*...cette force vide, sans rien pour la soutenir...*", 3.5)
                self.PrintEtEntreePourContinuerIntro("Tap, Tap.", 3.5)
                self.PrintEtEntreePourContinuerIntro("*...elle te coutera la vie.*", 4)
            else:
                self.PrintEtEntreePourContinuer("Du sang sortit de la bouche d'Yvan.")
                self.PrintEtEntreePourContinuer("Toute la puissance du monde n'aurait pas suffit a battre Elma, mais ca il ne le savait pas.")
                self.PrintEtEntreePourContinuer("Il regarda ses mains écorchées, temoignant d'un entrainement répétitif devenu inutile en quelques instants.")
                self.PrintEtEntreePourContinuer("Sans importance.")
                self.PrintEtEntreePourContinuer("*Tu... veux... quoi a la fin ??*")
                self.PrintEtEntreePourContinuer("Les yeux d'Elma renvoyèrent l'hostilité dans la voix d'Yvan.")
                self.PrintEtEntreePourContinuer("*T'es jalouse hein ?? Je suis jeune, vigoureux, soutenu par les membres du conseil, et toi tu... t'as fait ton temps !*")
                self.PrintEtEntreePourContinuer("Un sourire se dessina sur le visage d'Elma.")
                self.PrintEtEntreePourContinuer("*Ce !! Ca !!! J'en était sur !!*")
                self.PrintEtEntreePourContinuer("*Vois tu...*")
                self.PrintEtEntreePourContinuer("La froideur dans la voix d'Elma mit fin au piaillement d'Yvan.")
                self.PrintEtEntreePourContinuer("*...si tu veux prendre la couronne, libre a toi d'essayer.*")
                self.PrintEtEntreePourContinuer("*Cepandant...*")
                self.PrintEtEntreePourContinuer("*...t'a interet a aller jusqu'au bout.*")
                self.PrintEtEntreePourContinuer("Yvan cru déceller une note de douleur dans les paroles de son ancienne régente.")
                self.PrintEtEntreePourContinuer("*Toi...tu t'en sortira pas. C'est la fin.")
                self.PrintEtEntreePourContinuer("Tap.")
                self.PrintEtEntreePourContinuer("*Hey, c'est dingue que tu dise ca !*")
                self.PrintEtEntreePourContinuer("Tap.")
                self.PrintEtEntreePourContinuer("*PARCE QUE TOI NON PLUS.*")
                self.PrintEtEntreePourContinuer("D'un geste fin, rapide dans son execution, Elma décapita le Prince.")
                self.PrintEtEntreePourContinuer("Ainsi que les mains du prêtre.")
                self.PrintEtEntreePourContinuer("Puis...")
                self.PrintEtEntreePourContinuer("...")
                self.PrintEtEntreePourContinuer("Mourut.")
                self.PrintEtEntreePourContinuer("On dit que la Tiare qui représentait la Princesse de Suie tomba des moignons du prêtre pour venir se planter sur la tête de la vieille voleuse.")
                self.PrintEtEntreePourContinuer("On dit que ce n'est qu'un simple jouet en plastique, acheté avec le premier vol de sa défunte propriétaire.")
                self.PrintEtEntreePourContinuer("On dit enfin, que le Clan de voleur disparut dans la nuit, mettant fin a son Ordre après les évennements de la décharge.")
                self.PrintEtEntreePourContinuer("Il n'y a maintenant plus de vol organisé dans la ville de Carcassonne.")
                print("[FIN]")
                Affichage.EntreePourContinuer()
        elif nom == "Vesperum":
            if avant_le_combat:
                self.PrintEtEntreePourContinuer("Vesperum senti toute la puissance qu'il avait accumulé courir dans ses veines.")
                self.PrintEtEntreePourContinuer("Il regarda a l'Est, vers le soleil levant et s'accorda enfin un moment de pause.")
                self.PrintEtEntreePourContinuer("Des années durant, il n'avait pas arrêté d'avancer vers un but ancré dans son esprit :")
                self.PrintEtEntreePourContinuer("La récuperer.")
                self.PrintEtEntreePourContinuer("Recupérer qui ? Même Vesperum avait oublié son prénom.")
                self.PrintEtEntreePourContinuer("Au fur et a mesure des millénaires passés a servir le roi des enfers...")
                self.PrintEtEntreePourContinuer("Alors que les coups infligés et les horreurs percues s'accumulaient dans l'esprit du pauvre paysan...")
                self.PrintEtEntreePourContinuer("Il perdait petit a petit son indentité, ses émotions, ses souvenirs.")
                self.PrintEtEntreePourContinuer("Mais il se souvenait de sa chaleur...")
                self.PrintEtEntreePourContinuer("De son visage. De ses éclats de rire cristallins. De la manière dont elle se baissait a son niveau quand il était assis.")
                self.PrintEtEntreePourContinuer("Il se souvenait du contour régulier de son visage, éclairé par la lumière qui perlait a travers les vitraux colorés.")
                self.PrintEtEntreePourContinuer("Il se souvenait de son regard percant, dans l'obscurité des secrets, éclairé seulement par la lumière d'une bougie portéee par Vesperum.")
                self.PrintEtEntreePourContinuer("Il... se souvenait aussi du jour ou on lui a enlevé.")
                self.PrintEtEntreePourContinuer("Et la douleur ancrait en sa chair des montagnes de puissance, pour le seul objectif de la retrouver.")
                self.PrintEtEntreePourContinuer("De la.. récuperer.")
                self.PrintEtEntreePourContinuer("Vesperum tut les voix anxieuses des jours passés et laissa courir son regard sur le long des nuages.")
                self.PrintEtEntreePourContinuer("Ca et la, des cavaliers de l'éther se mirent a sortir des nuages nacrés avec l'obectif barbare de parcourir la distance les séparant de l'être immonde.")
                self.PrintEtEntreePourContinuer("A peine sorti, les armées du paradis avaient retrouvé sa trace et se précipitaient sur sa position.")
                self.PrintEtEntreePourContinuer("Mais ca ne déreangait plus Vesperum qui avait acquit le pouvoir de leur résister, apres des centaines d'années passées a les fuir encore et toujours.")
                self.PrintEtEntreePourContinuer("De plus, il savait que les gardiens des portes divines étaient un obstacle indispensable a son plan, et qu'il devait les affronter un moment ou un autre.")
                self.PrintEtEntreePourContinuer("Non, ce qui faisait trembler les jambes du démon, c'était l'excitation de pouvoir enfin laisser libre court a sa bestialité.")
                self.PrintEtEntreePourContinuer("Alors que les chevaux ailés s'approchèrent de Vesperum, ce dernier se mit a se rapeller quelque chose.")
                self.PrintEtEntreePourContinuer("Quelque chose d'autre, non pas sur elle, mais sur lui.")
                self.PrintEtEntreePourContinuer("Il s'était souvent demandé si en changeant comme il l'a fait, il pouvait trop changer, et finir par la perdre.")
                self.PrintEtEntreePourContinuer("Savoir, si, il était déja devenu un monstre qui ne pourrait rien faire de plus même après avoir réussi sa quete.")
                self.PrintEtEntreePourContinuer("Mais a ce moment, il se souvenu de ce qu'il ressentait au quotidien, quand c'était encore un mortel fermier.")
                mixer.quit()
                self.PrintEtEntreePourContinuer("Et il en tira une conclusion logique, qui le rassura avant que le combat ne commenca.")
                PlaySound("intro_story_final")
                self.PrintEtEntreePourContinuerIntro("*Au final, c'est bien la dernière chose qui me relie au mortel que j'était.*", 3.5)
                self.PrintEtEntreePourContinuerIntro("*Cette hargne, cette détermination, cette force de me battre contre mon avenir...*", 3.5)
                self.PrintEtEntreePourContinuerIntro("Vesperum... non. Emilien, soupira longuement.", 3.5)
                self.PrintEtEntreePourContinuerIntro("*Je suis encore humain.*", 4)

            else:
                self.PrintEtEntreePourContinuer("WIP[]")
                self.PrintEtEntreePourContinuer("")
                self.PrintEtEntreePourContinuer("")
                self.PrintEtEntreePourContinuer("")
                self.PrintEtEntreePourContinuer("")
                self.PrintEtEntreePourContinuer("")
                self.PrintEtEntreePourContinuer("")
                self.PrintEtEntreePourContinuer("")


        elif nom == "Peralta":
            if avant_le_combat:
                print("")
                Affichage.EntreePourContinuer()
            else:
                print("")
                Affichage.EntreePourContinuer()
        elif nom == "Bob Doré":
            if avant_le_combat:
                print("")
                Affichage.EntreePourContinuer()
            else:
                print("")
                Affichage.EntreePourContinuer()
        elif nom == "Auguste":  # DONE
            self.PrintEtEntreePourContinuer("[RETOUR EN ARRIERE]")
            self.PrintEtEntreePourContinuer("[IL Y A 2 HEURES]")
            self.PrintEtEntreePourContinuer("Après le dernier combat, Auguste s'effondra sur le sol, haletant.")
            self.PrintEtEntreePourContinuer("Il venait d'affronter un être divin, dépassant largement les capacités des etres humains.")
            self.PrintEtEntreePourContinuer("Serait il capable, un jour, d'exhiber une telle puissance ?")
            self.PrintEtEntreePourContinuer("Peut etre, mais ce n'était pas son but.")
            self.PrintEtEntreePourContinuer("Auguste laissa un sourir fendre son visage.")
            self.PrintEtEntreePourContinuer("Il avait abbatu un des plus puissants mages de l'histoire dans sa quête de main.")
            self.PrintEtEntreePourContinuer("A ce point, il aurait peut etre été plus simple de télécharger un logiciel de *text-to-speach* pour écrire son prochain roman...")
            self.PrintEtEntreePourContinuer("...mais il serait passé a côté de cette histoire incroyable qui survivait a grand peine dans ce donjon extravagant.")
            self.PrintEtEntreePourContinuer("*Son* histoire.")
            self.PrintEtEntreePourContinuer("*Ca ferait un truc incroyable a raconter !* dit-il tout haut. ")
            self.PrintEtEntreePourContinuer("Auguste reprit ses esprits et se dirigea vers la sortie, comme emporté par cette force qui guidait chacun de ses pas depuis son entrée dans le coliseum.")
            self.PrintEtEntreePourContinuer("Puis il s'arrêta tout net.")
            self.PrintEtEntreePourContinuer("Une pensée étrangère venait de parcourir son esprit, comme si ses neurones avaient été activés dans un ordre précis par une main divine, donnant ainsi naissance a cette idée farfelue.")
            self.PrintEtEntreePourContinuer("Une épiphanie divine, comme il n'en avait jamais eu auparavant.")
            self.PrintEtEntreePourContinuer("Et si le Maitre Mage avait un établi ?")
            self.PrintEtEntreePourContinuer("Un endroit dans lequel il fabriquait toute sorte de bidule magique aux fonctionnalités sordide, tel le sablier magique dont il laissait s'échapper du sable pendant leur combat ?")
            self.PrintEtEntreePourContinuer("Car, pour Auguste, tout ce qui touchait a la magie était un mélange confus de bric a brac sans logique propre qui , de temps en temps, faisait des miracles.")
            self.PrintEtEntreePourContinuer("Et des miracles, il en avait besoin d'un seul.")
            self.PrintEtEntreePourContinuer("Ou plutot de deux.")
            self.PrintEtEntreePourContinuer("Il se mit a fouiller l'étage, évitant de justesse les pièges mécaniques et les combats superflus, cherchant une porte invisible ou le livre suspect d'une bibliothèque encore plus suspecte.")
            self.PrintEtEntreePourContinuer("Puis il trouva ce qu'il cherchait.")
            self.PrintEtEntreePourContinuer("Sur la carte, c'était un mur. Mais devant lui s'étandait une boutique de farce et attrape grandeur nature, dans laquelle régnait un désordre qui faisait tache dans l'étage de marble blanc immaculé.")
            self.PrintEtEntreePourContinuer("Sur une des tables, il trouva un de ces tas de feuille empilé qui occupe une grande partie de son bureau, a la maison.")
            self.PrintEtEntreePourContinuer("Un cimetière d'idées refoulées, farfelues, ou inutiles.")
            self.PrintEtEntreePourContinuer("Sauf dans son cas.")
            self.PrintEtEntreePourContinuer("Entre un griffonage de gemme ornée de deux yeux, et le plan d'un étage dont les salles dépassait la centaine, il attrapa un morceau de papier griffoné a la hate.")
            self.PrintEtEntreePourContinuer("Les idées inutiles.")
            self.PrintEtEntreePourContinuer("Sur la deuxième ligne s'étandait une formule magique et une liste d'ingrédients pour fabriquer un bijou singulier.")
            self.PrintEtEntreePourContinuer("Une de ces chaines de main composée de plusieurs anneaux qui se glissent dans les doigts, reliés par un assemblage de maillon a un bracelet qui orne le poignet.")
            self.PrintEtEntreePourContinuer("Pour une raison obscure, alienne a tout ce qui a traversé son esprit imaginatif depuis l'adolescence, il savait que c'était la solution a son problème.")
            self.PrintEtEntreePourContinuer("Auguste empoignat le papier avec ses deux moignons, qu'il glissa dans sa poche avant de reprendre son chemin.")
            self.PrintEtEntreePourContinuer("Il aurait pu prendre tout ce qui se trouvait dans le bureau du Maitre Mage, et peut être vendre ses connaissances au prix fort, mais...")
            self.PrintEtEntreePourContinuer("...il sentait que quelque chose de terrible se serait passé.")
            self.PrintEtEntreePourContinuer("Le prix a payer pour avoir quelque chose de bien est souvent bien plus élevé que ce que l'on gagne.")
            self.PrintEtEntreePourContinuer("Il ne connaissait que trop bien ce genre de conséquence, lui qui avait perdu ses membres après avoir sorti son roman a succès mondial.")
            self.PrintEtEntreePourContinuer("Auguste était venu pour trouver des mains, et maintenant qu'il les avait, il était temps de sortir.")
            self.PrintEtEntreePourContinuer("Dehors.")
            self.PrintEtEntreePourContinuer("[TEMPS PRESENT]")
            self.PrintEtEntreePourContinuer("[ARTICLE DE JOURNAL : LE SUN]")
            self.PrintEtEntreePourContinuer("[PAGE 1]")
            self.PrintEtEntreePourContinuer("*Il l'a fait ! Auguste Wake le retour !*")
            self.PrintEtEntreePourContinuer("*Le célèbre auteur a succcès écrit la suite de son roman le plus connu a l'aide de deux prothèses de main dernier cri !*")
            self.PrintEtEntreePourContinuer("*Rapellons les faits : il y a quelques années en arrière, Wake perdit ses mains dans un accident de voiture, en pleine tournée de dédicace.*")
            self.PrintEtEntreePourContinuer("*L'auteur aurait alors exprimé un désespoir profond et un blocage psychologique l'empechant d'écrire quoi que ce soit.*")
            self.PrintEtEntreePourContinuer("*Mais quelques mois plus tard, il revient avec deux prothèses de main de la Fondation Élémia qui l'aurait aidé a surpasser ce blocage !*")
            self.PrintEtEntreePourContinuer("*Wake nous déclare alors : ""J'ai l'impression de n'avoir jamais perdu mes mains ! Je ressens comme avant, et je suis plus habile que jamais !""* ")
            self.PrintEtEntreePourContinuer("*Affublé de magnifiques chaines de main, ses prothèses permettent le retour de l'un des auteurs les plus proéminents de notre siècle, un miracle !* ")
            self.PrintEtEntreePourContinuer("*Dans la deuxieme page, une étude du cours des actions de la Fondation Élémia, en hausse depuis la sortie du livre...*")
            print("[FIN]")
            Affichage.EntreePourContinuer()
        elif nom == "Saria":  # DONE
            self.PrintEtEntreePourContinuer("Saria s'avanca dans la lumière.")
            self.PrintEtEntreePourContinuer("Peu de temps s'était écoulé depuis qu'elle était rentrée dans le coliseum, par la même porte, mais elle se sentait prête.")
            self.PrintEtEntreePourContinuer("*On arrête la fuite, et maintenant on se bat* pensa elle en son for interieur.")
            self.PrintEtEntreePourContinuer("Le coliseum avait été un bien piètre endroit pour attendre la chute de l'inquisition espagnole, mais il lui avait donné une chose essentielle : le pouvoir.")
            self.PrintEtEntreePourContinuer("En temps que druidesse, Saria avait été formée aux arcanes de la nature, et aux diverses facons d'utiliser ce qu'elle produit pour soigner, proteger la vie elle même.")
            self.PrintEtEntreePourContinuer("Elle n'avait jamais appris a se proteger, elle.")
            self.PrintEtEntreePourContinuer("La notion d'altruisme est un prérequis pour celle qui cherche la connaissance de la vie...")
            self.PrintEtEntreePourContinuer("...mais dans tant d'altruisme, on finit souvent par perdre la notion de soi dans un mélange de puissance et de dédication aux autres.")
            self.PrintEtEntreePourContinuer("On perd aussi ses possessions, au nom de la haine et de la peur.")
            self.PrintEtEntreePourContinuer("On perd aussi son héritage, dans un feu destructeur.")
            self.PrintEtEntreePourContinuer("On perd aussi ses confrères et consoeurs, dont les nouvelles disparaissent tel la fumée dans le vent.")
            self.PrintEtEntreePourContinuer("Et on finit par perdre une partie de son humanité, dans un méandre de tristesse et d'incompréhension.")
            self.PrintEtEntreePourContinuer("Mais aujourd'hui, Saria avait retrouvée quelque chose d'essentiel :")
            self.PrintEtEntreePourContinuer("La passion. La détermination.")
            self.PrintEtEntreePourContinuer("Son désir avait changé.")
            self.PrintEtEntreePourContinuer("Elle ne voulait plus se cacher, elle voulait se battre.")
            self.PrintEtEntreePourContinuer("[CIBLE DU DESIR CHANGEE]")
            self.PrintEtEntreePourContinuer("[INTERRUPTION DE LA FIN OPTIMALE]")
            self.PrintEtEntreePourContinuer("A la seconde ou elle prit cette décision, elle senti la force qui l'avait guidée jusque là s'évanouir.")
            self.PrintEtEntreePourContinuer("Mais elle avait la foi, et se mit en quete de ses pairs, pour former une résistance contre cette peur qui consumme les gens normaux !")
            self.PrintEtEntreePourContinuer("De Paris a Dublin...")
            self.PrintEtEntreePourContinuer("De Madrid a Moscou...")
            self.PrintEtEntreePourContinuer("De Johanesbourg a Kyoto...")
            self.PrintEtEntreePourContinuer("Elle fit le tour du monde grace a la fortune ammassée dans le Colyseum...")
            self.PrintEtEntreePourContinuer("Evita de peu la mort grâce a ses nouveaux pouvoirs...")
            self.PrintEtEntreePourContinuer("Et rassembla tout les adeptes de la magie dans une grande communautée qui ne voyait ni la couleur de la peau, ni la classe sociale, ni le pays d'origine !")
            self.PrintEtEntreePourContinuer("Et ainsi son organisation grandit...")
            self.PrintEtEntreePourContinuer("Elle passa de 1...")
            self.PrintEtEntreePourContinuer("A 2.....")
            self.PrintEtEntreePourContinuer("....")
            self.PrintEtEntreePourContinuer("....a 1...")
            self.PrintEtEntreePourContinuer("............a 1...")
            self.PrintEtEntreePourContinuer(".....")
            self.PrintEtEntreePourContinuer("..")
            self.PrintEtEntreePourContinuer(".")
            self.PrintEtEntreePourContinuer("")
            self.PrintEtEntreePourContinuer("Elle était arrivée trop tard.")
            self.PrintEtEntreePourContinuer("Les seules visions qui l'attendait...")
            self.PrintEtEntreePourContinuer("...étaient des cadavre brulés et les pleurs des familles.")
            self.PrintEtEntreePourContinuer("Les rois catholiques avaient gagnés.")
            self.PrintEtEntreePourContinuer("Le Pape Sixte IV détenait l'autoritée sur toute les religions du Monde.")
            self.PrintEtEntreePourContinuer("Il n'y avait plus rien a sauver.")
            self.PrintEtEntreePourContinuer("Il n'y avait plus rien a sauver.")
            self.PrintEtEntreePourContinuer("Il n'y avait plus rien a sauver.")
            self.PrintEtEntreePourContinuer("Il n'y avait plus rien a sauver.")
            self.PrintEtEntreePourContinuer("Il n'y avait plus rien a sauver.")
            self.PrintEtEntreePourContinuer("...")
            self.PrintEtEntreePourContinuer("Saria s'effondra dans une forêt sans nom pour pleurer a chaude larmes.")
            self.PrintEtEntreePourContinuer("Dans la solitude d'un cauchemard anonyme, elle laissa couler toute les émotions que peuvent contenir l'esprit et l'âme.")
            self.PrintEtEntreePourContinuer("Et a la réalité mordante...")
            self.PrintEtEntreePourContinuer("...elle préféra la chaleur des rêves qui ne finissent pas.")
            print("[FIN]")
            Affichage.EntreePourContinuer()
        elif nom == "Lucien":  # DONE
            self.PrintEtEntreePourContinuer("[RETOUR EN ARRIERE]")
            self.PrintEtEntreePourContinuer("[IL Y A QUELQUES MINUTES]")
            self.PrintEtEntreePourContinuer("*Alors, ca y est.*")
            self.PrintEtEntreePourContinuer("Le corps du Maitre Mage gisait là, sur le sol, mais il semblait pourtant plus vivant que jamais.")
            self.PrintEtEntreePourContinuer("Dans ses yeux brulait une flamme que l'on aurait crue inextinguible, et pourtant son sourire trahissait une attitude joueuse de ceux qui ont encore un as dans leur manche.")
            self.PrintEtEntreePourContinuer("*Quoi, tu en doutait ? Tout les hommes qui ont un jour laissé leur marque sur la terre ont une dette a regler. Mage, Ministre, Roi, ou Paysans, qu'importe.*")
            self.PrintEtEntreePourContinuer("*Et aujourd'hui...*")
            self.PrintEtEntreePourContinuer("La voix de Lucien se fit froide, mais légèrement tremblottante. L'émotion peut etre ?")
            self.PrintEtEntreePourContinuer("*...il est temps de la payer.*")
            self.PrintEtEntreePourContinuer("Maitre se releva.")
            self.PrintEtEntreePourContinuer("*J'ai un établi quelque part à l'étage, qui ne s'ouvre que quand je le souhaite. Tu peux aller chercher un symbole de ta victoire là-bas et...*")
            self.PrintEtEntreePourContinuer("Lucien fit un pas vers son predecesseur.")
            self.PrintEtEntreePourContinuer("*...et tu cherche quelque chose d'autre.*")
            self.PrintEtEntreePourContinuer("Lucien sorti un vieux couteau rouillé de sa poche, et l'empoigna fermement avant de fredonner un air de marin.")
            self.PrintEtEntreePourContinuer("*Vogue, vogue, pour l'éternité...*")
            self.PrintEtEntreePourContinuer("*Sur l'océan, les yeux, rivés...*")
            self.PrintEtEntreePourContinuer("*Vogue, vogue, la mer a tes pieds...*")
            self.PrintEtEntreePourContinuer("*Le ciel ne peut juger une lame émoussée.*")
            self.PrintEtEntreePourContinuer("Lucien aggripa l'épaule du Maitre Mage.")
            self.PrintEtEntreePourContinuer("*Tangue, tangue, la mer agitée...*")
            self.PrintEtEntreePourContinuer("*Une vie de pirate, une vie de libertée...*")
            self.PrintEtEntreePourContinuer("*Tangue, tangue, la mer a nos pieds...*")
            self.PrintEtEntreePourContinuer("*Nous risquons l'enfer sur le fil de l'épée.*")
            self.PrintEtEntreePourContinuer("Lucien fit retourner sans mal son adversaire à l'article de la mort.")
            self.PrintEtEntreePourContinuer("*La mort et les algues sur le ponton briqué...*")
            self.PrintEtEntreePourContinuer("*Les rires et les pleurs sur la planche du vicié.*")
            self.PrintEtEntreePourContinuer("Lucien aggripa les ailes du Maitre Mage d'un main...")
            self.PrintEtEntreePourContinuer("*Je vois que j'ai lancé une lignée de psychopathe, hein ?*")
            self.PrintEtEntreePourContinuer("...et leva son couteau de l'autre.")
            self.PrintEtEntreePourContinuer("*Les armes et l'argent dans un coffre d'acier...*")
            self.PrintEtEntreePourContinuer("*L'esprit et le corps comme une union soudée.*")
            self.PrintEtEntreePourContinuer("Lucien trancha dans la chair du Maitre Mage et retira l'aile gauche.")
            self.PrintEtEntreePourContinuer("*Vogue, vogue pour l'éternité...*")
            self.PrintEtEntreePourContinuer("Le Maitre Mage retenu un cri de douleur.")
            self.PrintEtEntreePourContinuer("*Ma vie et la tienne nous avons tout risqué...*")
            self.PrintEtEntreePourContinuer("Lucien trancha la deuxieme aile et la retira.")
            self.PrintEtEntreePourContinuer("*Je garde, un peu, de ta douce libertée*")
            self.PrintEtEntreePourContinuer("Le maitre Mage ne put retenir un hurlement de douleur.")
            self.PrintEtEntreePourContinuer("*Car le ciel ne peut juger lame...*")
            self.PrintEtEntreePourContinuer("Le Maitre Mage tomba a terre.")
            self.PrintEtEntreePourContinuer("*...émoussée.*")
            self.PrintEtEntreePourContinuer("Lucien jetta un regard aux deux ailes de mana.")
            self.PrintEtEntreePourContinuer("*Une partie de toi voguera a mes côtés, loin de cet endroit sordide.*")
            self.PrintEtEntreePourContinuer("*Et moi je pourrais montrer a tout le monde qui est le nouveau standard de puissance auquel il faut se comparer.*")
            self.PrintEtEntreePourContinuer("Le Maitre Mage s'éteignit dans une flaque de sang bleuté.")
            self.PrintEtEntreePourContinuer("Lucien jetta un dernier regard a celui dont l'ombre englobait autrefois tout ses efforts, avant de sortir du Coliseum.")
            self.PrintEtEntreePourContinuer("Il avait un navire a retrouver, et un objet a fabriquer.")
            self.PrintEtEntreePourContinuer("Et il savait parfaitement ce qu'il allait faire.")
            self.PrintEtEntreePourContinuer("*Vogue...vogue...pour l'éternitée....*")
            print("[FIN]")
            Affichage.EntreePourContinuer()
        elif nom == "Élémia":  # DONE
            self.PrintEtEntreePourContinuer("Élémia sortit du Coliseum.")
            self.PrintEtEntreePourContinuer("Elle passa en revu tout ce qui s'était passé depuis son entrée.")
            self.PrintEtEntreePourContinuer("Un truc noir qui parle bizarrement..")
            self.PrintEtEntreePourContinuer("Un chevalier aux grands airs...")
            self.PrintEtEntreePourContinuer("Une amalgamation de bout de monstre encore vivante...")
            self.PrintEtEntreePourContinuer("Un petit garcon en pleine puberté...")
            self.PrintEtEntreePourContinuer("Un type completement cinglé...")
            self.PrintEtEntreePourContinuer("Un autre enfant (ca commencait a faire beaucoup d'enfants quand meme)...")
            self.PrintEtEntreePourContinuer("Un autre type completement cinglé (la encore, ca commencait a faire beaucoup de cinglé)...")
            self.PrintEtEntreePourContinuer("Et un vieillard en pleine forme.")
            self.PrintEtEntreePourContinuer("Ils ont tous blablaté a propos d'un royaume et de trucs de cinglé qui n'interressait pas Élémia.")
            self.PrintEtEntreePourContinuer("Car Élémia était venue tester son armure.")
            self.PrintEtEntreePourContinuer("Et Élémia avait finit de la tester à l'étage, genre, deux.")
            self.PrintEtEntreePourContinuer("Quelques coups de monstres, quelques sorts aléatoires, et peut etre un peu de jogging dans son armure pour voir comment elle se comportait en situation réelle, c'est tout.")
            self.PrintEtEntreePourContinuer("Au final, si elle avait pu partir juste après, ca aurait été cool.")
            self.PrintEtEntreePourContinuer("Alors Élémia se mit a penser.")
            self.PrintEtEntreePourContinuer("*Ca serait quand même vachement plus pratique si je pouvais juste voir ou se trouve la clé a chaque étage, au lieu de me perdre en combats et en pièges même pas originaux.*")
            self.PrintEtEntreePourContinuer("Alors Élémia rentra chez elle et fariqua un truc pour juste voir ou se trouve la clé a chaque étage.")
            self.PrintEtEntreePourContinuer("Et comme d'habitude, elle ne réussit pas a faire son truc...")
            self.PrintEtEntreePourContinuer("...et créa a la place un truc encore plus incroyable.")
            self.PrintEtEntreePourContinuer("Mais Élémia retourna elle dans le Coliseum pour tester son truc ?")
            self.PrintEtEntreePourContinuer("Naaaan.")
            self.PrintEtEntreePourContinuer("Trop de types bizarre.")
            self.PrintEtEntreePourContinuer("C'est une vraie maison de fou là-bas !")
            self.PrintEtEntreePourContinuer("A la place, elle fit tester son armure au héros qui était passé la voir ya quelques temps de cela.")
            self.PrintEtEntreePourContinuer("Après tout, il avait plus grand chose a perdre !")
            self.PrintEtEntreePourContinuer("A part son autre bras.")
            self.PrintEtEntreePourContinuer("Et quand l'armure explosa au contact de la peau du héros..")
            self.PrintEtEntreePourContinuer("...et que son autre bras vola d'un bout a l'autre de la pièce...")
            self.PrintEtEntreePourContinuer("...Élémia se dit que, peut etre...")
            self.PrintEtEntreePourContinuer("...potentiellement...")
            self.PrintEtEntreePourContinuer("...elle avait eu beaucoup beaucoup beaucoup beaucoup de chance pendant son aventure.")
            self.PrintEtEntreePourContinuer("Alors Élémia arreta d'inventer des trucs.")
            self.PrintEtEntreePourContinuer("Et se mit au dessin !")
            self.PrintEtEntreePourContinuer("Mais on garde les horreurs lovecraftiennes invoquées accidentellement par ses gribouillis pour une autre histoire.")
            self.PrintEtEntreePourContinuer("Ah !")
            self.PrintEtEntreePourContinuer("Coucou Cat-Astrophe !")
            print("[FIN]")
            Affichage.EntreePourContinuer()
        elif nom == "Samantha":  # DONE
            self.PrintEtEntreePourContinuer("Samantha plongea les mains dans ses poches.")
            self.PrintEtEntreePourContinuer("Les pièces d'or pur étaient froide au toucher, et pourtant elle avait l'impression qu'elles lui brulaient les mains.")
            self.PrintEtEntreePourContinuer("Elle prit une profonde inspiration, tentant en vain de chasser la boule de chaleur qui lui entravait le torse.")
            self.PrintEtEntreePourContinuer("Qui aurait cru que cette pauvre étudiante en medecine allait survivre au donjon le plus meurtrier de toute l'Europe (si ce n'est le monde) ?")
            self.PrintEtEntreePourContinuer("Pas elle, en tout cas.")
            self.PrintEtEntreePourContinuer("Elle était désormais riche, et fit un rapide calcul dans sa tête.")
            self.PrintEtEntreePourContinuer("Les gratte-papiers de la trésorerie ne lui acheteraient pas ses pièces sans savoir d'ou elles viennent.")
            self.PrintEtEntreePourContinuer("Et si ils savaient, elle était sûre qu'ils trouveraient une manière de lui prendre ses biens, citant une loi d'appropriation des biens du Coliseum, ou quelque chose dans le genre.")
            self.PrintEtEntreePourContinuer("Elle retrouva le sac qu'elle avait cachée dans un buisson, près du grillage qui entoure le Coliseum, et vida ses poches dedans.")
            self.PrintEtEntreePourContinuer("Elle en profita aussi pour allumer son portable et lancer une recherche rapide :")
            self.PrintEtEntreePourContinuer("*Impot sur le revenu année en cours*")
            self.PrintEtEntreePourContinuer("Pour des revenus superieur a 177 016e, l'etat prend 45% des revenus.")
            self.PrintEtEntreePourContinuer("Dans sa tête, ca devenait clair : elle ne pouvait pas passer par le cheminement légal.")
            self.PrintEtEntreePourContinuer("Mais qui sait ce qu'il se passerait si elle vendait ses biens en passant par le marché noir ?")
            self.PrintEtEntreePourContinuer("Elle avait confiance en ses capacités a se défendre, mais on pouvait toujours lui voler ses biens.")
            self.PrintEtEntreePourContinuer("Elle fit alors le choix qui s'imposait :")
            self.PrintEtEntreePourContinuer("Elle lanca une demande sur reddit, et attendit ces gens qui s'y connaissent trop bien en des sujets particuliers, et qui donnent des réponses étrangement précises.")
            self.PrintEtEntreePourContinuer("En suivant les instructions, elle pourrait gagner assez d'argent pour rembourser ses dettes, et...")
            self.PrintEtEntreePourContinuer("et...")
            self.PrintEtEntreePourContinuer("et quoi ?")
            self.PrintEtEntreePourContinuer("Travailler pour le restant de ses jours dans des hopitaux miteux en manque de fond ?")
            self.PrintEtEntreePourContinuer("Ou alors dans un bureau petit en plein désert médical, a traiter des personnes a l'état toujours plus déplorable ?")
            self.PrintEtEntreePourContinuer("Lorsque c'était une étudiante, elle pouvait rever d'un job stable apportant un salaire faible, mais régulier.")
            self.PrintEtEntreePourContinuer("Mais se faire exploiter par des directeurs corrompus qui gardent l'argent destiné a l'amélioration des soins ?")
            self.PrintEtEntreePourContinuer("Alors qu'elle avait tant d'argent a sa disposition ?")
            self.PrintEtEntreePourContinuer("Impensable.")
            self.PrintEtEntreePourContinuer("Si elle voulait faire docteur, c'est avant tout pour aider ceux qui en ont besoin a voir la beautée de la vie pendant le plus de temps possible.")
            self.PrintEtEntreePourContinuer("Mais elle voulait aussi avoir une vie, une personne avec qui la partager, et une jolie maison dans laquelle elle pourrait, elle aussi, profiter de sa vie.")
            self.PrintEtEntreePourContinuer("Profiter de sa condition, profiter de ses... hobbies.")
            self.PrintEtEntreePourContinuer("Samantha réfléchit longtemps, sur le chemin qui le ramena chez elle.")
            self.PrintEtEntreePourContinuer("Elle continua de réflechir, alors qu'elle allait a l'université pour récuperer les papiers attestant de son master.")
            self.PrintEtEntreePourContinuer("Et elle finit par arriver a une conclusion qui allait changer le cours de sa vie.")
            self.PrintEtEntreePourContinuer("Samantha vendit ses golds par quelques moyens obscurs que seuls ceux qui sont dans le secret connaissent.")
            self.PrintEtEntreePourContinuer("Elle remboursa son prêt étudiant.")
            self.PrintEtEntreePourContinuer("Et...")
            self.PrintEtEntreePourContinuer("...elle disparut de la face du monde.")
            self.PrintEtEntreePourContinuer("On dit qu'une docteur enseigne a celles et ceux qui le veulent les joies de la medecine, quelque part sur une plage thailandaise.")
            self.PrintEtEntreePourContinuer("On dit que sous le toit rouge de la maison qu'elle habite, les malades trouvent les medicaments chers qui soignent les plus coriaces des maladies.")
            self.PrintEtEntreePourContinuer("On dit qu'entre ses mains expertes et son regard bienveillant, on trouverait même le courage d'affronter la mort.")
            self.PrintEtEntreePourContinuer("On dit que ses apprentis sont liés a elle par un contrat sévère, mais juste, qui leur permet de vivre leur vie sans être enchainé par des clauses et des pièges légaux.")
            self.PrintEtEntreePourContinuer("...")
            self.PrintEtEntreePourContinuer("On dit aussi que c'est la joueuse de League of Legends la plus toxique de la décennie.")
            print("[FIN]")
            Affichage.EntreePourContinuer()
        elif nom == "Emy":  # DONE
            self.PrintEtEntreePourContinuer("Emy fit un pas de plus vers la sortie.")
            self.PrintEtEntreePourContinuer("C'était un pas comme les autres, un de ces pas déterminés qu'elle avait déjà tant effectués, vers un futur précis, prédéterminé.")
            self.PrintEtEntreePourContinuer("Et au fond du long couloir de pierre, elle vit quelque chose d'incroyable :")
            self.PrintEtEntreePourContinuer("Du vert.")
            self.PrintEtEntreePourContinuer("Pas le vert brun et mauve du deuxieme étage, pas ce vert toxique et malsain.")
            self.PrintEtEntreePourContinuer("Non.")
            self.PrintEtEntreePourContinuer("Sa vision fut remplie d'un vert éclatant, et puis d'un gris qui s'étendait a perte de vue aussi.")
            self.PrintEtEntreePourContinuer("Sa peau réagit au froid d'une pluie battante, mais sereine.")
            self.PrintEtEntreePourContinuer("Elle qui avait vécue toute sa vie dans le coliseum, pendant de longues années, enterrée dans ce tombeau putride a travers des milliers de cycles de réincarnation,")
            self.PrintEtEntreePourContinuer("Elle qui avait tuée et s'était faite tuée, encore et encore, et dont la vie se résumait a des murs de pierre et les échos d'un ordre terrible dans son esprit.")
            self.PrintEtEntreePourContinuer("Elle voyait ce qu'il y avait en dehors, au dela.")
            self.PrintEtEntreePourContinuer("Et c'était magnifique !")
            self.PrintEtEntreePourContinuer("Emy se laissa emporter ses émotions et imprima chaque centimètres de cette vue dans son esprit.")
            self.PrintEtEntreePourContinuer("Elle se mit au seuil de la sortie et huma les odeurs étrangères que le vent lui apportèrent...")
            self.PrintEtEntreePourContinuer("Puis elle se retourna.")
            self.PrintEtEntreePourContinuer("Aussi beau que tout cela puisse paraitre, elle était enchainée au Colyseum.")
            self.PrintEtEntreePourContinuer("Elle ne le savait que trop bien.")
            self.PrintEtEntreePourContinuer("L'être corrompu qui dirige tout ce qui se trouve dans les arènes est un tyrant qui appose sa marque sur ses créations.")
            self.PrintEtEntreePourContinuer("La marque du sacrifice.")
            self.PrintEtEntreePourContinuer("Elle permet de revenir a la vie et de gagner en puissance tant que l'on est dans le coliseum...")
            self.PrintEtEntreePourContinuer("...cepandant vous ne pouvez désobéir a aucun de ses ordres.")
            self.PrintEtEntreePourContinuer("Vous ne pouvez pas quitter cet endroit.")
            self.PrintEtEntreePourContinuer("Et si vous ne voulez pas passer votre temps en état de non-existance...")
            self.PrintEtEntreePourContinuer("...vous devez plaire au public.")
            self.PrintEtEntreePourContinuer("Les armées de fantomes qui se trouvent dans les gradins, anciens combattants ayant perdus la vie ici, doivent assister a des combats dramatiqeus et saisissants, ou alors...")
            self.PrintEtEntreePourContinuer("...?")
            self.PrintEtEntreePourContinuer("La marque...")
            self.PrintEtEntreePourContinuer("L'humiditée de dehors avait fait perler des gouttes d'eau sur le plafond.")
            self.PrintEtEntreePourContinuer("Et dans la flaque d'eau en dessous, Emy vit la marque du sacrifice sur son cou.")
            self.PrintEtEntreePourContinuer("Cette dernière était a moitiée effacée, a la séparation entre son corps de loup et son corps d'Homme.")
            self.PrintEtEntreePourContinuer("Se pourrait-il que la transformation l'aie libérée de cette malédiction ??")
            self.PrintEtEntreePourContinuer("Emy jetta un autre coup d'oeil dehors.")
            self.PrintEtEntreePourContinuer("Ce monde l'attirait, lui chuchotait a l'oreille de magnifiques proses, et promettait un avenir radieux.")
            self.PrintEtEntreePourContinuer("Au contraire, les murs froids ne la repoussait que davantage.")
            self.PrintEtEntreePourContinuer("Elle prit une décision.")
            self.PrintEtEntreePourContinuer("Emy se réapprocha du seuil de la sortie...")
            self.PrintEtEntreePourContinuer("...")
            self.PrintEtEntreePourContinuer("...et subissa une violente réaction.")
            self.PrintEtEntreePourContinuer("On aurait dit que son corps tout entier était parcouru d'électricité.")
            self.PrintEtEntreePourContinuer("La voix de son créateur retentit dans don esprit :")
            self.PrintEtEntreePourContinuer("*TU NE QUITTERA PAS LE COLISEUM*")
            self.PrintEtEntreePourContinuer("Emy répondit par la négative a la voix désincarnée qui la faisait tant souffrir.")
            self.PrintEtEntreePourContinuer("*TU NE QUITTERA PAS LE COLISEUM*")
            self.PrintEtEntreePourContinuer("Emy avait déja ressenti cela lorsque elle avait laissée le vieil homme en vie, et avait tuée un autre voyageur pour faire taire cette douleur qui la transpercait.")
            self.PrintEtEntreePourContinuer("*TU NE QUITTERA PAS LE COLISEUM*")
            self.PrintEtEntreePourContinuer("Cepandant...")
            self.PrintEtEntreePourContinuer("*TU NE QUITTERA PAS LE COLISEUM*")
            self.PrintEtEntreePourContinuer("...c'était quand même bien plus fort ? Cela faisait bien plus mal ? Et elle n'avait pas le luxe de penser a tout ca car son corps réagissait de lui même ?")
            self.PrintEtEntreePourContinuer("*TU NE QUITTERA PAS LE COLISEUM*")
            self.PrintEtEntreePourContinuer("Emy regarda l'herbe verte et les arbres au loin.")
            self.PrintEtEntreePourContinuer("*TU NE QUITTERA PAS LE COLISEUM*")
            self.PrintEtEntreePourContinuer("Emy fit un pas de plus vers la sortie.")
            self.PrintEtEntreePourContinuer("*TU NE QUITTERA PAS LE COLISEUM*")
            self.PrintEtEntreePourContinuer("Emy fit un pas de plus vers la sortie.")
            self.PrintEtEntreePourContinuer("*TU NE QUITTERA PAS LE COLISEUM*")
            self.PrintEtEntreePourContinuer("Emy fit un pas de plus vers la sortie.")
            self.PrintEtEntreePourContinuer("*TU NE QUITTERA PAS LE COLISEUM*")
            self.PrintEtEntreePourContinuer("Emy fit un pas du plus vers la sortie.")
            self.PrintEtEntreePourContinuer("*TU NE QUITTERA PAS L-*")
            self.PrintEtEntreePourContinuer("Emy traversa le seuil de la porte et s'effondra sur le gazon.")
            self.PrintEtEntreePourContinuer("La marque permettait de controler, tant que l'on était encore dans le Coliseum.")
            self.PrintEtEntreePourContinuer("Tant que l'on était encore dans le Coliseum.")
            self.PrintEtEntreePourContinuer("Emy senti une chaleur étrange au niveau de son cou, et se regarda dans une flaque.")
            self.PrintEtEntreePourContinuer("La marque du sacrifice avait disparue, et avec elle , toute les parties de son corps liées avec sa vie de louve.")
            self.PrintEtEntreePourContinuer("Emy...")
            self.PrintEtEntreePourContinuer("...était enfin devenue humaine.")
            self.PrintEtEntreePourContinuer("On dit qu'une dessinatrice de talent s'est installée dans la maison de l'ancien capitaine de la garde de Carcassonne.")
            self.PrintEtEntreePourContinuer("On dit que c'est un proche parent, avec le même coeur vaillant et remplit de bonté.")
            self.PrintEtEntreePourContinuer("On dit qu'elle parcourt le monde pour le mettre en image, mais qu'elle revient toujours à sa maison.")
            self.PrintEtEntreePourContinuer("On dit...")
            self.PrintEtEntreePourContinuer("...que le plus beau dessin du monde est un portrait du capitaine adossé contre un loup, tout deux en plein sommeil.")
            self.PrintEtEntreePourContinuer("Et Emy ne s'en séparera pour rien au monde.")
            print("[FIN]")
            Affichage.EntreePourContinuer()
        elif nom == "Terah":  # DONE
            self.PrintEtEntreePourContinuer("Terah regarda au dehors.")
            self.PrintEtEntreePourContinuer("Le Monde exterieur.")
            self.PrintEtEntreePourContinuer("La société.")
            self.PrintEtEntreePourContinuer("La vie.")
            self.PrintEtEntreePourContinuer("Il était venu au coliseum parce qu'une voix l'avait attiré.")
            self.PrintEtEntreePourContinuer("C'était peut etre la premiere fois que quelqu'un l'avait appelé par son prénom, non pas pour lui faire du mal...")
            self.PrintEtEntreePourContinuer("...mais parce que quelqu'un désirait sa présence.")
            self.PrintEtEntreePourContinuer("Et Terah avait beau avoir fouillé le Coliseum dans son entieretée, il n'avait pas trouvé cette présence qui voulait bien de lui.")
            self.PrintEtEntreePourContinuer("Cette.. émotion étrangère... qui l'avait amenée là.")
            self.PrintEtEntreePourContinuer("Et maintenant ?")
            self.PrintEtEntreePourContinuer("La force qui poussait chacun de ses pas était toujours là, en lui.")
            self.PrintEtEntreePourContinuer("Cette chose qui pouvait répondre a ses désirs, et le pousser dans la bonne direction...")
            self.PrintEtEntreePourContinuer("...elle s'était arrétée.")
            self.PrintEtEntreePourContinuer("Il n'avait pourtant pas changé son désir, et voulait réellement rencontrer le propriétaire de la Voix.")
            self.PrintEtEntreePourContinuer("Mais elle restait immobile.")
            self.PrintEtEntreePourContinuer("Muette.")
            self.PrintEtEntreePourContinuer("Comme une idole devant laquelle on prie pendant toute une vie.")
            self.PrintEtEntreePourContinuer("Comme le cadavre d'un parent a qui on demande de répondre.")
            self.PrintEtEntreePourContinuer("Comme les insectes putrides d'une fosse dans laquelle on est jetée par d'autres enfants.")
            self.PrintEtEntreePourContinuer("Terah se retrouvait a nouveau seul, devant une batisse étrangère, dans un pays étranger, sans même plus rien pour vivre a par la puissance.")
            self.PrintEtEntreePourContinuer("Il comprit que sa seule chance de survie était de mettre cette nouvelle puissance a l'oeuvre, dans des endroits ou on voudrait bien de lui.")
            self.PrintEtEntreePourContinuer("Mais a quoi bon ?")
            self.PrintEtEntreePourContinuer("A la croisée des chemins et des décisions, a la fin de son périple, Terah ressentit quelque chose de terrible, qui lui déchira les entrailles et abbatu toute volontée de se battre.")
            self.PrintEtEntreePourContinuer("Ce genre d'émotion qui abat un homme et le ramène a lui même,")
            self.PrintEtEntreePourContinuer("A sa place dans le monde.")
            self.PrintEtEntreePourContinuer("Une deppression fulgurante, une tristesse insondable,")
            self.PrintEtEntreePourContinuer("Il avait l'impression d'avoir raté quelque chose.")
            self.PrintEtEntreePourContinuer("Il avait l'impression d'avoir manqué un chemin, et que ce qu'il ressentait lui permettrait de le trouver.")
            self.PrintEtEntreePourContinuer("Comme une porte dont la serrure était si complexe, qu'il fallait échouer a l'ouvrir au moins une fois pour comprendre comment elle marche.")
            self.PrintEtEntreePourContinuer("Ce qu'il ressentait maintenant était un puissant coup de poing dans son âme, mais lui permettait de reprendre le controle de son corps.")
            self.PrintEtEntreePourContinuer("Mais c'était trop tard pour l'utiliser.")
            self.PrintEtEntreePourContinuer("Ce Vide Interieur.")
            self.PrintEtEntreePourContinuer("Terah regarda alors le paysage en dehors du couloir.")
            self.PrintEtEntreePourContinuer("Rien ne l'attendait dehors.")
            self.PrintEtEntreePourContinuer("Alors...")
            self.PrintEtEntreePourContinuer("...")
            self.PrintEtEntreePourContinuer("...Terah retourna dans le coliseum.")
            self.PrintEtEntreePourContinuer("Et disparut pour toujours.")
            self.PrintEtEntreePourContinuer("[FIN?]")
        elif nom == "Redde":  # DONE
            self.PrintEtEntreePourContinuer("*Et voila le travail !*")
            self.PrintEtEntreePourContinuer("Redde s'exprima auprès d'un public invisible.")
            self.PrintEtEntreePourContinuer("*J'ai affronté les terribles étages du coliseum, conquit chacun des boss avec l'aide de l'amour et de l'amitié, et...*")
            self.PrintEtEntreePourContinuer("*...vaincu le plus grand mage de tout les temps !*")
            self.PrintEtEntreePourContinuer("*Nous venons de vivre...*")
            self.PrintEtEntreePourContinuer("*..l'aventure ULTIME !*")
            self.PrintEtEntreePourContinuer("Redde prit une grand inspiration.")
            self.PrintEtEntreePourContinuer("*JE SUIS INVINCIBLE !*")
            self.PrintEtEntreePourContinuer("Redde laissa courir le bruit pendant quelques instants, avant de se reprendre.")
            self.PrintEtEntreePourContinuer("*LA JUSTICE TRIOMPHE ENCORE !*")
            self.PrintEtEntreePourContinuer("la phrase flotta quelques instants dans les airs, mais elle ne convainquit pas Redde.")
            self.PrintEtEntreePourContinuer("*Grace a moi, nous entrons dans une ère de paix !*")
            self.PrintEtEntreePourContinuer("Ca sonnait mieux, mais encore un peu trop...centré sur lui.")
            self.PrintEtEntreePourContinuer("C'était un héros, pas une star de cinéma.")
            self.PrintEtEntreePourContinuer("*Et c'est ainsi que mon.. que l'aventure...*")
            self.PrintEtEntreePourContinuer("Redde avait du mal a faire sortir les mots coincés au fond de sa gorge.")
            self.PrintEtEntreePourContinuer("*...se finit.*")
            self.PrintEtEntreePourContinuer("Voila. Il l'avait enfin dit.")
            self.PrintEtEntreePourContinuer("Il avait mit fin a son aventure, a sa quête, a sa légende.")
            self.PrintEtEntreePourContinuer("Accompagnés par la pensée par ses amis et son petit ami qui l'attendait surement a la maison...")
            self.PrintEtEntreePourContinuer("Ils ferait une grande soirée pour célébrer sa victoire...")
            self.PrintEtEntreePourContinuer("Et il pourrait revoir toutes les personnes qu'il avait aidé pendant sa quête...")
            self.PrintEtEntreePourContinuer("...avant de vivre sa vie heureuse.")
            self.PrintEtEntreePourContinuer("Sa vraie vie.")
            self.PrintEtEntreePourContinuer("Sa vie ennuyeuse.")
            self.PrintEtEntreePourContinuer("Son existance...")
            self.PrintEtEntreePourContinuer("...banale.")
            self.PrintEtEntreePourContinuer("Alors que la pluie tombait, Redde regarda vers l'Horizon.")
            self.PrintEtEntreePourContinuer("Il n'y avait plus rien a faire.")
            self.PrintEtEntreePourContinuer("Il n'arrivait plus a inventer d'autres histoires dont il était le héros.")
            self.PrintEtEntreePourContinuer("Il n'arrivait plus a visualiser les douces formes de sa ou son interet romantique.")
            self.PrintEtEntreePourContinuer("Il n'arrivait plus a imaginer de situation ou il les sauve d'une attaque incroyable...")
            self.PrintEtEntreePourContinuer("...ou il les surprend dans un moment génant...")
            self.PrintEtEntreePourContinuer("...ou il passe un moment léger en companie de ses amis factices.")
            self.PrintEtEntreePourContinuer("Il n'arrivait plus a se projeter hors de cette réalitée terriblement banale.")
            self.PrintEtEntreePourContinuer("Et il était fatigué de faire ce spectacle ou chaque actions est amplifiée.")
            self.PrintEtEntreePourContinuer("Il était fatigué de toujours devoir faire semblant pour échapper a son ombre.")
            self.PrintEtEntreePourContinuer("Redde..")
            self.PrintEtEntreePourContinuer("...s'asseya sur le sol trempé.")
            self.PrintEtEntreePourContinuer("Il savait que le rêve avait touché a sa fin...")
            self.PrintEtEntreePourContinuer("...et pleura les bons moments qu'il avait vécu dans sa fantaisie onirique.")
            self.PrintEtEntreePourContinuer("Il pleura a chaude larmes la fin de Redde le streamer héros, et le début de Jérémy l'adulte incapable d'appeler un dentiste.")
            self.PrintEtEntreePourContinuer("Il avait fuit cette réalitée, ses responsabilités, et ce bagage d'adulte remplit de connaissances et de choses vécues.")
            self.PrintEtEntreePourContinuer("Et aujourd'hui, il devait y faire face.")
            self.PrintEtEntreePourContinuer("Jérémy devait grandir, et cette idée devenait de plus en plus insupportable.")
            self.PrintEtEntreePourContinuer("C'était peut etre son plus grand défi.")
            self.PrintEtEntreePourContinuer("Et la pluie continuait de faire écho a ses lamentations.")
            self.PrintEtEntreePourContinuer("Alors Jérémy finit de faire son deuil,")
            self.PrintEtEntreePourContinuer("Et regarda la pluie tomber.")
            self.PrintEtEntreePourContinuer("...")
            self.PrintEtEntreePourContinuer("*Si d'autres personnes peuvent le faire...pourquoi pas moi ?*")
            self.PrintEtEntreePourContinuer("*Ca doit pas etre si terrible une fois qu'on s'y met.*")
            self.PrintEtEntreePourContinuer("*Et puis je peux toujours demander conseil a celles et ceux qui m'entourent*")
            self.PrintEtEntreePourContinuer("...")
            self.PrintEtEntreePourContinuer("Les gouttes perlaient sur son front.")
            self.PrintEtEntreePourContinuer("Le bruit remplissait ses oreilles et apaisait son esprit.")
            self.PrintEtEntreePourContinuer("Il avait affronté un mage, il pouvait affronter la vie.")
            self.PrintEtEntreePourContinuer("Alors Jérémy prononca des mots qu'il n'avait jamais prononcé devant cette terrible chose, cette monumentale tache qui l'attendait.")
            self.PrintEtEntreePourContinuer("C'était des mots vrais, qui venaient tout droit du coeur.")
            self.PrintEtEntreePourContinuer("Des mots qui ne vivaient pas dans sa tête, et qui aurait un véritable impact sur sa vie.")
            self.PrintEtEntreePourContinuer("Alors que la pluie tombait.")
            self.PrintEtEntreePourContinuer("Indéfiniment.")
            self.PrintEtEntreePourContinuer("...")
            self.PrintEtEntreePourContinuer("*Je vais y arriver.*")
            self.PrintEtEntreePourContinuer("Et Redde sourit.")
            print("[FIN]")
            Affichage.EntreePourContinuer()
        elif nom == "Valfreya":  # DONE
            self.PrintEtEntreePourContinuer("Valfreya. Fière Valkirie.")
            self.PrintEtEntreePourContinuer("Décide de qui survit aux batailles.")
            self.PrintEtEntreePourContinuer("Sert les boissons aux guerriers dans le halle du valr.")
            self.PrintEtEntreePourContinuer("Absolument PAS une guerriere.")
            self.PrintEtEntreePourContinuer("Et pourtant elle avait, dans une fragile enveloppe charnelle, terrassé l'un des endroits le plus meurtrier du monde !")
            self.PrintEtEntreePourContinuer("Pour prouver a des machos qu'elle n'était pas inutile.")
            self.PrintEtEntreePourContinuer("Penser a l'absurdité de tout ceci ternit un peu son enthousiasme.")
            self.PrintEtEntreePourContinuer("La condition de la femme au paradis des guerriers n'est guère plus terrible qu'ici bas, alors que la nature des habitants des deux royaumes sont à l'opposée...")
            self.PrintEtEntreePourContinuer("Il fallait que ca change !")
            self.PrintEtEntreePourContinuer("Valfreya leva alors les mains vers le ciel, afin de signifier sa réussite, mais surtout pour qu'on envoie des gens pour la chercher.")
            self.PrintEtEntreePourContinuer("Après tout, le chemin jusqu'au royaume perché dans les hautes branches de l'Yggdrasil était long et ardu, et elle voulait rentrer au plus vite pour jeter un bon verre d'hydromel a la tête de Odin !")
            self.PrintEtEntreePourContinuer("Et quand les heures passèrent, et que rien ne vint...")
            self.PrintEtEntreePourContinuer("...elle comprit qu'elle allait devoir se le farcir, le chemin ardu.")
            self.PrintEtEntreePourContinuer("Alors Valfreya se mit en route.")
            self.PrintEtEntreePourContinuer("Elle fit d'abord une invocation afin de descendre a Svartalfheim, le royaume des nain, pour y chercher une autorisation de passage.")
            self.PrintEtEntreePourContinuer("L'invocation lui permit de passer Jötunheim, le royaume des géants, ce qui était un gain de temps considérable.")
            self.PrintEtEntreePourContinuer("Ensuite, elle retourna au Midgard, le royaume des hommes, afin de chercher les derniers druides qui l'emmeneraient à Álfheim, le royaume des elfes.")
            self.PrintEtEntreePourContinuer("Mais elle ne trouva personne, et dut se débrouiller dans la forêt magique de Brocéliande avec quelques vieux manuscrits écrits par la dernière druidesse.")
            self.PrintEtEntreePourContinuer("Arrivée chez les elfes, elle utilisa son autorisation pour monter vers le prochain royaume (après une petite cinquantaine d'année pour vérifier l'authenticité du papier : les elfes ne sont pas pressés.)")
            self.PrintEtEntreePourContinuer("Au royaume des Vanes, elle se fit discrète et demanda rapidement a ce qu'on l'emmène a Asgard.")
            self.PrintEtEntreePourContinuer("Problème : Les Vanes n'étaient pas contentes du dernier échange de divinités avec les Ases, et se mirent à se défouler sur Valfreya...")
            self.PrintEtEntreePourContinuer("...avant que cette dernière, emplie de sa nouvelle force et un peu énervée de son périple, les envoya a travers une montagne.")
            self.PrintEtEntreePourContinuer("Et une autre.")
            self.PrintEtEntreePourContinuer("Et encore une autre.")
            self.PrintEtEntreePourContinuer("Cette démonstration de force fit rapidement décider Hoenir a aider la Valkirie a rentrer a la maison.")
            self.PrintEtEntreePourContinuer("Arrivée a Asgard, elle put rejoindre le Valhalla, et retrouva Odin et Thor, en pleine discussion sur la cuisson du prochain repas.")
            self.PrintEtEntreePourContinuer("Ces derniers furent bien étonné de la revoir vivante, et se confondirent en excuses.")
            self.PrintEtEntreePourContinuer("Mais Valfreya avait consommée l'entieretée de sa patience, et hurla sur les deux dieux nordiques.")
            self.PrintEtEntreePourContinuer("Toute la haine de son mauvais traitement s'était mélangée a la terreur qu'elle avait ressentie dans le Coliseum.")
            self.PrintEtEntreePourContinuer("Et elle en avait marre.")
            self.PrintEtEntreePourContinuer("Odin reconnut ses tords, et offrit a Valfreya d'aller lui chercher a boire, avant de parler récompenses.")
            self.PrintEtEntreePourContinuer("Et apporta a Valfreya...")
            self.PrintEtEntreePourContinuer("...un verre de Syra.")
            self.PrintEtEntreePourContinuer("Du lait.")
            self.PrintEtEntreePourContinuer("...")
            self.PrintEtEntreePourContinuer("On dit que Valfreya prit un tonneau d'Hydromel et le balanca a la tête d'Odin si fort...")
            self.PrintEtEntreePourContinuer("...qu'il dégringola l'entieretée de l'Yggdrasil et tomba à Helheim, le royaume des morts.")
            self.PrintEtEntreePourContinuer("Quand a Thor ?")
            self.PrintEtEntreePourContinuer("Lui et les guerriers du Valhalla servirent sa bière a Valfreya et les autres valkyries pendant tout un millénaire.")
            self.PrintEtEntreePourContinuer("De nos jours, les Valkyrie servent un mois sur deux, et se font servir le reste du temps.")
            self.PrintEtEntreePourContinuer("Un petit pas pour la cause !")
            print("[FIN]")
            Affichage.EntreePourContinuer()
        elif nom == "Bob":  # DONE
            self.PrintEtEntreePourContinuer("Bob fit quelques pas dans les herbes vertes de la plaine ou se situe le Coliseum.")
            self.PrintEtEntreePourContinuer("*AH-AH ! JE SUIS RESSORTI VAINQUEUR DU COLISEUM ! ENCORE UNE VICTOIRE A AJOUTER A MA BIBLIOGRAPHIE, BILLY !*")
            self.PrintEtEntreePourContinuer("La tête d'un enfant roux, pas plus agé que 13 ans, sorti du grand sac a dos de Bob. Ses joues constellées de taches de rousseur s'activèrent.")
            self.PrintEtEntreePourContinuer("*Bob, Bob ! Tu n'as pas de bibliographie voyons ! Tu brule tout les livres qui parlent de toi en hurlant que les droits d'auteurs ne sont pas respectés !*")
            self.PrintEtEntreePourContinuer("*SILENCE, BILLY ! TU N'ES BIEN EVIDEMMENT PAS ASSEZ INTELLIGENT POUR COMPRENDRE CE QUE JE FAIS AU QUOTIDIEN !*")
            self.PrintEtEntreePourContinuer("*M-m-mais, Bob..*")
            self.PrintEtEntreePourContinuer("*SILENCE JE DIS, MON CORPS CONTIENT ASSEZ DE MUUUUUSCLE POUR T'ENVOYER AU SEPTIEME CIEL D'UNE SIMPLE FLEXION DE MON POIGNET ! HAAAANNN !*")
            self.PrintEtEntreePourContinuer("*J'imagine... et que va tu faire de cette puissance, bob ?*")
            self.PrintEtEntreePourContinuer("*JE VAIS...*")
            self.PrintEtEntreePourContinuer("*Oui ?*")
            self.PrintEtEntreePourContinuer("*JE... VAIS..*")
            self.PrintEtEntreePourContinuer("*Oui ??*")
            self.PrintEtEntreePourContinuer("*JE !!!! VAIS !!!*")
            self.PrintEtEntreePourContinuer("*Oui ???!!!*")
            self.PrintEtEntreePourContinuer("*TOUT !!! DONNER !!! A MA DIVINITE !!!*")
            self.PrintEtEntreePourContinuer("*Ah ben non alors ! Pas encore !*")
            self.PrintEtEntreePourContinuer("*VOYONS BILLY, CA SERAIT TROP SIMPLE DE TOUT REUSSIR AVEC CETTE FORCE !*")
            self.PrintEtEntreePourContinuer("*Bah ! Justement !*")
            self.PrintEtEntreePourContinuer("*COMMENT UN PYROBARBARE PEUT ETRE BARBARE SI TOUT EST FACILE ?*")
            self.PrintEtEntreePourContinuer("*Ta logique fait aucun sens, bob !*")
            self.PrintEtEntreePourContinuer("*ET PUIS DE TOUTE FACON C'EST DECIDE.*")
            self.PrintEtEntreePourContinuer("Bob prononca un mot ancien, empli de sagesse, comme ceux qui appartiennent aux divinités oubliées.")
            self.PrintEtEntreePourContinuer("Vous perdez 99% de toute la puissance que vous avez obtenue !")
            self.PrintEtEntreePourContinuer("Cette derniere part dans les airs et disparait, devenant le copieux diner de la divinité protectrice de Bob.")
            self.PrintEtEntreePourContinuer("*Bon... bah si c'est déja fait alors...*")
            self.PrintEtEntreePourContinuer("*NE T'INQUIETE PAS BILLY !! JE SUIS ASSEZ MUSCULEUX POUR REUSSIR TOUT CE QUE J'ENTREPREND, MEME SANS CETTE PUISSANCE SUPERFLUE !*")
            self.PrintEtEntreePourContinuer("*Je te fait confiance Bob. Et puis j'imagine qu'elle a du te donner quelque chose en échange hein ?*")
            self.PrintEtEntreePourContinuer("*BIEN SUR !*")
            self.PrintEtEntreePourContinuer("*...*")
            self.PrintEtEntreePourContinuer("*...*")
            self.PrintEtEntreePourContinuer("*C'est...encore un pin's ?*")
            self.PrintEtEntreePourContinuer("*AH AH BILLY ! TU AS L'OEUIL !*")
            self.PrintEtEntreePourContinuer("*Mais Bob ! Voyons ! C'est le 20 eme pins que tu recois ! Et je te parle meme pas de ceux qui sont a la maison !*")
            self.PrintEtEntreePourContinuer("*MAIS !*")
            self.PrintEtEntreePourContinuer("*Ya aussi le tee-shirt avec un pin's imprimé dessus...*")
            self.PrintEtEntreePourContinuer("*MAIS !*")
            self.PrintEtEntreePourContinuer("*Et puis cette fois ou elle t'a offert un anneau avec un pin's dessus en échange du réceptacle de vie d'une Reine Liche...*")
            self.PrintEtEntreePourContinuer("*MAIS !*")
            self.PrintEtEntreePourContinuer("*Et puis, et puis, le pin's en forme de pin's ! Je sais même pas comment c'est possible !*")
            self.PrintEtEntreePourContinuer("*MAIS !*")
            self.PrintEtEntreePourContinuer("*Mais ! Quoi a la fin ?*")
            self.PrintEtEntreePourContinuer("*MAIS BILLY ! VOYONS ! CELUI LA EST EN FORME D'EXTINCTEUR ! C'EST A LA FOIS UN CADEAU MIGNON, TENDANCE, MAIS EN PLUS C'EST TERRRRRRRIBLEMENT MARRANT !*")
            self.PrintEtEntreePourContinuer("*Ahhh ! Un extincteur ! Un truc qui éteint le feu ! Alors que tu maitrise le feu ! C'est vrai que c'est vachement... sagace !*")
            self.PrintEtEntreePourContinuer("*AH AH ! TU VOIS BILLY !*")
            self.PrintEtEntreePourContinuer("*Oui !!! Je !!! Vois !!!*")
            self.PrintEtEntreePourContinuer("*AH AH ! ALORS PARTONS MAINTENANT !*")
            self.PrintEtEntreePourContinuer("Bob commenca a partir vers le Nord, a la recherche de nouvelles aventures, et d'autres mondes qui lui les fournirait.")
            self.PrintEtEntreePourContinuer("*AU FAIT, BILLY...*")
            self.PrintEtEntreePourContinuer("*Oui, Bob ?*")
            self.PrintEtEntreePourContinuer("*TU...SAIS CE QUE CA VEUT DIRE... SAGACE ?*")
            self.PrintEtEntreePourContinuer("*Bien sur, Bob !*")
            self.PrintEtEntreePourContinuer("C'était bien évidemment un mensonge.")
            print("[FIN]")
            Affichage.EntreePourContinuer()


    def PrintEtEntreePourContinuer(self, message):
        print(message)
        Affichage.EntreePourContinuer()

    def PrintEtEntreePourContinuerIntro(self, message, temps):
        print(message)
        time.sleep(temps)
        ClearConsole()

    def ShowBeginingOfEnding(self):
        #print le début de l'explication de la fin de chaque personnage
        mixer.quit()
        print("[AVENTURE TERMINE]")
        Affichage.EntreePourContinuer()
        print("[CALCUL DE LA CONTRIBUTION DU PERSONNAGE EN COURS...]")
        Affichage.AfficheAvecUnTempsDattente(3)
        print("[CALCUL TERMINE]")
        Affichage.EntreePourContinuer()
        print("[CONTRIBUTION DU PERSONNAGE SUFFISANTE]")
        Affichage.EntreePourContinuer()
        print("[D E S I R  A C C O R D E]")
        Affichage.EntreePourContinuer()
        print("[ALTERATION DES LOIS DE L'UNIVERS EN COURS...]")
        Affichage.AfficheAvecUnTempsDattente(3)
        print("[AJOUT DE KARMA POSITIF EN COURS...]")
        Affichage.AfficheAvecUnTempsDattente(3)
        print("[CHARGEMENT D'UNE FIN OPTIMALE...]")
        Affichage.AfficheAvecUnTempsDattente(3)
        print("[CHARGEMENT TERMINE]")
        Affichage.EntreePourContinuer()
        print("[VEUILLEZ OBSERVER LA CONSEQUENCE DES CHOIX DE CELLES ET CEUX QUI VOUS ONT PRETE LEUR CORPS]")
        Affichage.EntreePourContinuer()
        PlayMusic("finale")

    def DoLastFight(self):
        #lance un combat avec certains prerequis
        Player.affronte_fin_histoire = True
        control = controleur.Control(Player, Trader)
        # lance la bataille
        while True:
            try:
                control.Battle()
                Player.affronte_fin_histoire = False
                mixer.quit()
                self.PrintEtEntreePourContinuer("[COMBAT TERMINE]")
                break
            except Exception as error:
                WriteErrorInErrorLog(error)

    def GiveGift(self):
        #donne un artefact, si il n'a pas déja été donné
        ARTEFACTETDESCRIPTION = {"Saumel" : ["Pièce Fondue",  # ajout
                                              ("Une pièce de monnaie représentant la vengeance, maudissant les ennemis de son porteur."
                                              "\nLes coups critiques maudissent les ennemis, les ennemis maudits perdent 2 pm par tour.")],
                                "Elma" : ["Tiare de Suie",  # ajout
                                              ("Un bibelot vénéré par un clan de voleur, porté par sa dernière cheffe pendant un régicide."
                                              "\nAccorde la bénédiction du feu sacré a son porteur pour chaque coups esquivés.")],
                                "Auguste" : ["Chaine de Main",  # ajout
                                              ("Un bijou magique qui se porte au niveau des mains, et qui transforme une prothèse en véritable main connectée au système nerveux."
                                              "\nLes sorts critiques font deux fois plus de dégâts.")],
                                "Saria" : ["Larme d'Yggdrasil",  # ajout
                                              ("Une perle de sève venant d'un arbre magestueux qui communique une grande tristesse a ceux qui dorment sous ses branches."
                                              "\nEn combat, les feuilles et fruits Jindagee et Aatma durent 2 fois plus longtemps")],
                                "Vesperum" : ["Collier de Nephilim",  # ajout
                                              ("Un artefact témoignant de l'amour entre un paysant devenu démon et une papesse devenue ange, laissée a leur enfant avant de mourir."
                                              "\nRecouvrir des pm permet de recouvrir des pv, avec un ratio 2/1 (2pm regagnés ==) 1 pv regagné en plus)")],
                                "Lucien" : ["Cape Victorieuse",  # ajout
                                              ("Une cape macabre cousue avec les fils d'un drapeau pirate et les ailes du Ministre du Mana."
                                              "\nChaque ennemi tué augmente de 0.5% les dégâts totaux.")],
                                "Élémia" : ["Schmilblick",  # ajout  
                                              ("Un bidule bizarre crée par une inventrice farfelue."
                                              "\nA l'entrée d'un nouvel étage, toutes ses salles sont directement dessinées sur la carte (annule les effets du Monocle de Vérité)")],
                                "Samantha" : ["Contrat de Travail",  # ajout
                                              ("Un bout de papier promettant la puissance aux économes afin qu'ils ne se fassent plus martyriser par le système."
                                              "\nVous gagnez 2% de dégâts totaux supplementaire par paquets de 50 pièces possédé.")],
                                "Emy" : ["Dessin Nostalgique",  # ajout
                                              ("Un dessin au charbon d'un vieil homme en plein sommeil, adossé contre une louve."
                                              "\nPasser son tour donne l'altération d'état *Concentration* pendant 2 tours, qui réduit le nombre de pm nécéssaire pour chaque sorts.")],
                                "Terah" : ["Vide Interieur",  # ajout
                                              ("Un sentiment de malaise, comme si vous étiez passé a coté de quelque chose, et que votre aventure avec ce personnage n'a pas livré tout ses secrets."
                                              "\nEnlève le stigma négatif [Incontrollable], ainsi que 15 points de mana maximum.")],
                                "Peralta" : ["Badge Terni",  # ajout
                                              ("Un morceau de métal terni par le temps, les éléments, et les tentations, mais qui reste solide et droit."
                                              "\nRéduit les prix du marchand de 30%, lorsque il ne reste plus d'ennemis a affronter dans l'arène de l'étage en cours (boss compris).")],
                                "Redde" : ["Perle de Pluie",  # ajout
                                              ("Un crystal serein, symbole de la libération des chaines de l'esprit."
                                              "\nChance de faire un sort critique : +33%.")],
                                "Valfreya" : ["Syra",  # ajout
                                              ("Une verre divin de lait fermenté apprécié par un certain dieu nordique jeté hors de son throne par une ""valkyrie inutile au combat""."
                                              "\nLes nouvelles techniques apprises donnent 10pm max supplémentaires."
                                              "\nLes nouveaux sorts appris donnent 10pv max supplémentaires.")],
                                "Bob" : ["Pin's Extincteur",  # ajout
                                              ("Un joli pin's a accrocher sur un vêtement, représentant un extincteur rouge."
                                              "\nLorsque l'effet Brulûre se termine, redonne 10pv et 10pm.")],
                                "Bob Doré" : ["Bandeau Teinté",  # ajout
                                              ("Une relique de Thémis, l'esprit de la Justice, marqué d'un curieux éclat doré."
                                              "\nEn combat, vous gagnez 1 pièce a chaque tours.")]}

        # creer une liste avec tout les artefacts de personnage deja debloque
        donnees_de_s0ve = Observation.GetPermanentThingsFromS0ve()
        liste_artefact_deja_debloque = ast.literal_eval(donnees_de_s0ve["Artefact Debloques"])

        # sortir les informations de l'artefact a donner depuis le dictionnaire au dessus
        informations_artefact_a_donner = ARTEFACTETDESCRIPTION[Player.nom_du_personnage]
        nom_de_artefact_a_donner = informations_artefact_a_donner[0]
        description_de_artefact_a_donner = informations_artefact_a_donner[1]

        if not (nom_de_artefact_a_donner in liste_artefact_deja_debloque):
            print(f"Vous avez terminé l'histoire de {Player.nom_du_personnage} pour la première fois !")
            PlaySound("questdone")
            Affichage.EntreePourContinuer()
            print("Un nouvel artefact est désormais disponible dans le livre de la cigogne bleue !")
            liste_artefact_deja_debloque.append(nom_de_artefact_a_donner)
            donnees_de_s0ve["Artefact Debloques"] = liste_artefact_deja_debloque
            Observation.SetPermanentThingsToS0ve(donnees_de_s0ve)
            Affichage.EntreePourContinuer()
            print(f"[{nom_de_artefact_a_donner}]")
            print(f"[{description_de_artefact_a_donner}]")
            Affichage.EntreePourContinuer()

        
        



def ClearConsole():
    # Vérifier le système d'exploitation pour déterminer la commande appropriée
    os.system("cls" if os.name == "nt" else "clear")


def GetMenuPrincipalChoice():
    print("                                    \            / ")
    print("                                     \          / ")
    print("                                      \        / ")
    print("                                       \      / ")
    print("                      ||||||||||||||    \    /  ")
    print("                    ||||||||||||         \  /  ")
    print("                 ||||||||                 \/ ")
    print(
        "_______________||||||||___________________/\_______________________________________________ "
    )
    print("               ||||||||                   \/ ")
    print("               ||||||||                   /\ ")
    print("               ||||||||                  /  \  ____    ____ ")
    print(
        "               ||||||||     ||||    ||  / || \||      ||     ||  ||    ||  || "
    )
    print(
        "     _,---,_   ||||||||   |||  |||  || /  ||  \||||   |===   ||  ||  ||  ||  || "
    )
    print(
        "   /'_______`\ |||||||||    ||||    \|||  ||  ____||  ||___   ||||   ||  ||  || "
    )
    print(
        '  (/\'       `\|__||||||||||--------------------""""""""""""""""""""""---------------------, '
    )
    print(
        "  *\#########||__________                                                               /' "
    )
    print(
        '  * ^^^^^^^^^||          """"""""""""------------____________                         /\' '
    )
    print(
        '              \                   /                \          """"""""""""-----_____/\' '
    )
    print("                                 /                  \ ")
    print("                                /                    \ ")
    print("                               /     1 - Nouvelle Partie")
    print(f"                              /      2 - Continuer : [{Player.nom_de_letage}] ")
    print("                             /       3 - Tutoriel       \ ")
    print("                            /                            \ ")
    print("                           /                              \ ")
    return int(
        input(
            "Choisissez une action avec le numéro correspondant, et appuyez sur Entrée pour continuer : "
        )
    )


def PlayMusic(musique):
    dir_path = Player.chemin_musique
    musique = dir_path + f"\\{musique}.mp3"
    mixer.init()
    mixer.music.load(musique)
    mixer.music.play(-1)


def PlaySound(musique):
    dir_path = Player.chemin_musique
    musique = dir_path + f"\\{musique}.mp3"
    mixer.init()
    mixer.music.load(musique)
    mixer.music.play()


def PlayWavSound(musique):
    dir_path = Player.chemin_musique
    musique = dir_path + f"\\sfx\\{musique}.wav"
    mixer.init()
    mixer.music.load(musique)
    mixer.music.play()


def ChoseCharacter():
    ClearConsole()
    # recommence jusqu'a ce que le choix soit fait
    while True:
        # Choix du personnage
        while True:
            try:
                choix = GetChoixPersonnageChoice()
                ClearConsole()
                if choix == 1:
                    # retour
                    return False
                elif choix in range(2, (len(LISTEDEPERSONNAGE) + 2)):
                    # personnage a afficher
                    break
            except ValueError:
                ClearConsole()
        # Initilaisation des informations du personage selectionné
        nom_du_personnage = DICTIONNAIREDEPERSONNAGEAAFFICHER[choix]
        caracteristiques_du_personnage = LISTEDEPERSONNAGE[nom_du_personnage]
        # Affichage du personnage et validation
        while True:
            try:
                validation_du_personnage = GetPersonnageValideChoice(
                    caracteristiques_du_personnage
                )
                ClearConsole()
                if validation_du_personnage == 2:
                    # personnage selectionné
                    Player.UseCharacterForInitCaracteristics(
                        caracteristiques_du_personnage
                    )
                    return True
                elif validation_du_personnage == 1:
                    # retour
                    break
            except ValueError:
                ClearConsole()


def GetPersonnageValideChoice(caracteristiques):
    # 0nom 1description 2stigma+ 3stigma- 4stigma* 5techniques
    # 6sorts 7items 8talents 9vie 10mana 11force
    # 12inteligence 13defence 14tauxcoupcrit
    # 15degatcoupcrit 16tauxsortcrit 17degatsortcrit
    # 18tauxesquive 19gold
    print(
        f"     -= {caracteristiques[0]} =-"
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
        f"\nArtefacts : {caracteristiques[20]}"
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
    print(
        "\nInserez le numéro de l'adresse de l'information souhaitée,                                                             8"
        "\net laissez notre programme récuperer ces données pour vous !                                                           6"
    )
    print(
        "Plus besoin de paniquer lorsque l'on supprime d'anciennes données sans le vouloir !                                    2"
    )
    print(
        "Vos données n'auront plus de secret pour vous !                                                                        4"
    )
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
    if choix in [
        362951847,
        14,
        100110,
        8624,
        1512111113111013,
        1342,
        1233,
        456852,
        3236353,
        313,
        22,
        935284761,
        5321139741,
        7415321139,
        9353918170,
    ]:
        if choix == 8624:
            nom_de_limage = "python_properties_vue"  # table des matieres -

        elif choix == 456852:
            nom_de_limage = "python_properties_main_Thread"  # image observation e7 -

        elif choix == 362951847:
            nom_de_limage = "python_properties_Anox_init"  # page 1 (e1) -
        elif choix == 100110:
            nom_de_limage = "python_properties_controleur"  # page 2 (e3) a faire #
        elif choix == 313:
            nom_de_limage = "python_properties_Thread_init"  # page 3 (arret roi, par matiere) a faire lore #
        elif choix == 19:
            nom_de_limage = "python_properties_controleur_Thread"  # page 4 (observatorium, par matiere) a faire secrets des observations #
        elif choix == 935284761:
            nom_de_limage = "python_properties_modele_Thread"  # page 5 (par tout talent combo talents) -
        elif choix == 9353918170:
            PlayMusic("abyss")
            print("Ce n'est pas encore l'heure.")
            Affichage.EntreePourContinuer()
            print("Contente toi de ceci pour l'instant.")
            Affichage.EntreePourContinuer()
            print("Menu Coliseum(OBSERVATORIUM) = Musiques")
            print("Menu Coliseum(OBSERVATORIUM(KEY)) = Plus de Musiques")
            Affichage.EntreePourContinuer()
            nom_de_limage = "python_properties_vue_Thread"  # page 13 (combo toutes pages donne seulement etage 0, etage 0 donne invitation.) a faire #
        elif choix == 14:
            nom_de_limage = "python_properties_modele"  # talent feu (e2) -
        elif choix == 1512111113111013:
            nom_de_limage = "python_properties_modele_Anox"  # talent glace (e4) -
        elif choix == 1233:
            nom_de_limage = "python_properties_main"  # talent foudre (e7) -
        elif choix == 3236353:
            nom_de_limage = (
                "python_properties_main_Anox"  # talent terre (e5) quete ult -
            )
        elif choix == 1342:
            nom_de_limage = "python_properties_controleur_Anox"  # talent sang (e6) -
        elif choix in [5321139741, 7415321139]:
            nom_de_limage = "python_properties_vue_Anox"  # talent physique (e8) livre + notes de table des matières -   faire page 13 ==) pas maintenant

        dir_path = os.path.dirname(os.path.realpath(__file__))
        chemin_de_limage = dir_path + "\\__py.property__\\"
        open_image(f"{chemin_de_limage}{nom_de_limage}.xldr")
    else:
        print("                           Donnée Récupérée :")
        for _ in range (0, 21):
            print(
                "zq4f15sr6wz3f5qe1fs6533e5.2f6e53s1f65ze1qe1fz6f12q6ef531ze653f16r84g61esf5"
            )
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
    print(
        "\nBienvenue dans le Coliseum ! Prononcé Co-li-zé-oum, ca veut dire Colisée en Latin."
    )
    print(
        "Vous êtes sans doute excités a l'idée de vous plonger dans les méandres de cette batisse légendaire !"
    )
    print("Mais avant toute chose, quelques bases à connaitre.")
    print("\n\n")
    Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("              { Partie 2 : Histoire }")
    print(
        "\nLe coliseum est une batisse ancienne, commandée par un roi fou a son magicien pour enfermer"
    )
    print(
        "les gens de son peuple qu'il croyait dangereux. Au fur et a mesure des années, de plus en plus"
    )
    print(
        "d'innoncents se sont retrouvé dans les arènes sordides, a combattre des créations monstrueuses de chair et de sang."
    )
    print(
        "Jusqu'à un beau matin de printemps ou le Roi, dans un généreux élan de folie et de paranoïa, décida de se jeter dans"
    )
    print(
        "sa création, accompagnée de toute sa cour."
        "\nDes années plus tard, la batisse sera déclarée dangereuse par les gouvernements,"
    )
    print(
        "et plus personne ne se frottera aux étages malicieux du Coliseum, qui changera alors de nom et de structure..."
    )
    print("...mais c'est une histoire pour plus tard :)")
    print(
        "En attendant, plusieurs personnages auront bravés les interdits et se seront attaqués au tombeau du Roi fou, pour diverses raisons,"
        "\net c'est eux que vous allez pouvoir controller !"
    )
    print("\n\n")
    Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("             { Partie 3 : Bien Commencer }")
    print(
        "\nLe coliseum se compose de plusieurs étages. Pour naviguer dans les étages inferieurs, vous devez"
    )
    print(
        "d'abord battre le boss de l'étage en cours. Seulement, c'est le plus souvent un individu sacrément puissant !"
    )
    print("Comment faire ? Eh bien... devenir plus fort !")
    print(
        "Chaques monstres tués vous rapoorte une amélioration de certaines de vos caractéristiques, et un peu de golds."
    )
    print(
        "Vous pouvez ensuite échanger vos golds contre des objets chez le marchand de l'étage."
    )
    print(
        "Et une fois que vous serez dotés de meilleurs objets, améliorés avec de meilleurs caractéristiques, et"
    )
    print("équ00000ipés de meilleqdznqdurs tttAAAaaaalEnnnttsss...z,lqnd.......")
    print(
        "Vous verrez que le boss de l'étage ne sera plus un mur, mais un simple obstacle sur votre chemin ! "
    )
    print(
        "Ainsi, il faut tuer des monstres, acheter des objets, tuer le boss, descendre, et répéter l'opération jusqu'au"
    )
    print("dernier étage : le HdUiIxTiIèEmMeE !")
    print("\n\n")
    Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("         { Partie 4a : Les menus : Navigation }")
    print(
        "\nVous pouvez vous diriger dans les menus a l'aide des nombres, qui sont affectés a chaques actions."
    )
    print(
        "Par exemple, dans le menu principal, vous pouvez commencer une nouvelle aventure avec 1,"
    )
    print(
        "et continuer une partie déja sauvegardée avec 2. Vous pouvez aussi lancer le tutoriel avec 3"
    )
    print(
        "(ce que vous avez faitpl ou ezdnore landzd leefnzos pefisp avevevevc WWWWXXXWWW."
    )
    print("\nEnfin bref, chaque actions sont affectées a un numéro.")
    print(
        "Et n'ayez pas peur ! Si vous rentrez un mauvais numéro, une chaine de caractère ou même rien du tout,"
    )
    print(
        "le programme continuera normalement sans planter, et se contentera de vous redemander votre choix !"
    )
    print("\n\n")
    Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("          { Partie 4b : Les menus: Utilité }")
    print(
        "\nGrace aux menus, vous pouvez naviguer dans vos options possibles pour chaques situations."
    )
    print("Le menu de l'étage actuel du Coliseum permet ainsi de:")
    print(
        "- Combattre un monstre (attention, le nombre de monstre par étage est limité ! ne fuyez pas tout vos commbats !)"
        "\n- Combattre un boss / Descendre a l'étage inferieur (si le boss est battu)"
        "\n- Acheter des items chez le marchand "
        "\n- etc"
    )
    print(
        "Un même nombre (genre 1) change d'action effectuée (Choisir un personnage, Affronter un monstre) selon le contexte (Menu Principal, Menu d'Etage)."
    )
    print("\n\n")
    Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("            { Partie 5 : Les Combats }")
    print(
        "\nLe Coliseum s'explore en trois temps : "
        "\nLe temps de repos, ou menu d'étage, qui permet de choisir ses actions"
        "\nLe temps d'observation, afin d'observer toute les salles de l'étage pour trouver objets, artefacts, et salles particulières."
        "\nLe temps de combat, pour devenir plus fort ou battre le boss."
    )
    print("\nEn temps de combat, tout se déroule au tour par tour.")
    print("En premier lieu s'effectuent les actions de début de combat.")
    print("Ensuite, vous choisissez un menu parmis ceux disponibles.")
    print("Juste après, vous choisissez une action dans le menu affiché.")
    print("Votre action est effectuée, puis celle de l'ennemi a la suite.")
    print("Les différents effets d'altérations d'états s'appliquent")
    print("Et on recommence jusqu'a ce qu'un des deux participant meure ou fuie.")
    print(
        "\nGardez a l'esprit que vos points de vie (PV) représentent la vitalité qu'il vous reste,"
        "\net que si ils tombent a zéro, c'est terminé.\nCepandant, les points de mana (PM) servent juste"
        "a lancer des sorts, et peuvent descendre a zéro sans réelles conséquences."
        "\nMême chose pour les points d'endurance (PE) qui servent a utiliser des techniques et remontent naturellement."
    )
    print("\n\n")
    Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("         { Partie 6a : Foire aux Questions }")
    print("\n*Dans le menu de choix des personnage, il y a des stigmas. C'est quoi ?*")
    print(
        " - Ce sont des passifs intrinsèques aux personnages, liés a leur situation ou leur experience,"
        " qui s'activent avant, pendant, ou apres un combat."
    )
    print(
        "\n*J'ai vu qu'on pouvait utiliser des redcoins dans le menu d'étage. C'est quoi ? Ca fait quoi ?*"
    )
    print(
        "˙ǝɹı̣ɹɔ́ǝp ǝp zǝuǝʌ snoʌ ǝnb nuǝɯ ǝן suɐp ́ǝʇou ʇsǝ uı̣oɔpǝꓤ uǝ ʇnoɔ uos ǝnb ı̣suı̣ɐ sʇuǝןɐʇ ǝnbɐɥɔ ǝp ǝpoɔ ǝ"
        "ן ʇƎ ˙ǝɹʇnɐ ʇǝ 'sǝpnʇı̣ʇdɐ ' sǝnbɐʇʇɐ sǝןןǝʌnou ǝp ɹǝnboןq́ǝp ʇuǝʌnǝd sʇuǝןɐʇ sǝƆ ˙npı̣ʌı̣puı̣'ן ǝp sdɹoɔ ǝן suɐp"
        " 'sʇuǝןɐʇ sǝ́ǝןǝddɐ 'sǝןɐı̣ɔ́ǝds sǝɔuǝʇ́ǝdɯoɔ sǝp ǝɹʇı̣ɐu ʇı̣ɐɟ ')sǝɹɟɟı̣ɥɔ ǝp ǝʇı̣ns ǝun ɹɐd ́ǝnbı̣puı̣ 'ןɐɹ́ǝúǝƃ uǝ("
        " sı̣ɔ́ǝɹd ǝɹpɹo un suɐp ɐuɐɯ np uoı̣ʇɐןnɔɹı̣ɔ ɐן ɐ sǝ́ǝןdnoɔ ' ʇǝ sdɹoɔ np sǝuoz sǝp ɹǝןnɯı̣ʇs ǝp ʇǝɯɹǝd ǝpı̣nbı̣ן ǝƆ"
        " ˙uı̣ǝs uos uǝ nuǝʇuoɔ ǝɹoןoɔuı̣ ǝpı̣nbı̣ן np ʇuǝı̣ʌ ʇǝ 'ǝɹı̣ɐןı̣ɯı̣s ʇsǝ suı̣oƆpǝꓤ un'p ɹnǝןɐʌ ɐꓶ ˙sǝʇı̣ɐɟ ʇuǝı̣ɐʇ́ǝ sǝןןǝ"
        " sǝןןǝnbsǝן suɐp nɐı̣ɹ́ǝʇɐɯ np ́ǝʇı̣soı̣ɔ́ǝɹd ɐן ǝp ʇı̣ɐuǝʌ ǝnbı̣ʇuɐ ǝɯoꓤ ɐן ǝp sǝɔ̀ǝı̣d sǝp ɹnǝןɐʌ ɐꓶ"
    )
    print("\n\n")
    Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("        { Partie 6b : Foire aux Questions }")
    print("\n*Ya un type bizarre qui execute les rochemikazes. C'est qui ?*")
    print(" - C'est Alfred.")
    print(
        "\n*Ya des types de sorts et de techniques différentes qui inflige des effets élémentaires différents, non ?*"
    )
    print(
        " - C'est exact. Par exemple, la glace peut geler, ce qui applique l'effet gelure sur la cible, qui prendra alors 50% de dégâts supplémentaire."
    )
    print(
        "\n*...et le reste ? Les autres altérations d'états ? Et les effets des talents ? Et les effets des stigmas ?\nVous n'avez rien expliqué !*"
    )
    print(
        " - C'est aussi exact ! Le fun du Coliseum viens du fait que vous êtes lachés dans un environnement étranger, sans guide,"
    )
    print(
        "et avec le moins d'expliquations possibles !"
        "\nAlors prenez un papier, un crayon, et notez au fur et a mesure les informations que vous découvrirez !"
    )
    print("\n\n")
    Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("            { Partie 7 : Bonne chance ! }")
    print(
        "\nMaintenant, vous savez tout ce qu'il y a a savoir pour débuter une partie."
    )
    print(
        "Alors qu'attendez vous ? Ne soyez pas timide ! Il y a une montagne de chose a faire et a découvrir !"
    )
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
            personnage_a_ete_choisi = ChoseCharacter()
            if personnage_a_ete_choisi:
                try:
                    # sauvegarde et charge le personnage choisi
                    if Player.mode_de_jeu == "Véritable Descente":
                        Player.nom_de_letage = "Sanctuaire du Sacrifice"
                        Player.numero_de_letage = 0
                        Player.nombre_dennemis_a_letage = 0
                    else:
                        Player.nom_de_letage = "Ruines Abandonnées"
                    Save.FromPlayerToDict()
                    Save.FromDictToSaveFile("\\save.txt")
                    Save.FromSaveFileToDict()
                    Save.FromDictToPlayer()
                    Affichage.AffichageDescriptionEtage()
                    FloorMaker.SetupFloorLayout()
                    # personnage choisi
                    in_menu_principal = False
                except Exception as error:
                    WriteErrorInErrorLog(error)

        # continuer une partie sauvegardee
        elif choix == 2:
            personnage_a_ete_choisi = Save.LoadTheGame()
            if personnage_a_ete_choisi:
                # sauvegarde chargée dans la classe Joueur
                in_menu_principal = False
                Affichage.AfficheChargement()
                if Player.mode_de_jeu == "Ascension" and (Player.numero_de_letage == 0):
                    Player.mode_de_jeu = "Descente"  

        # tutorial
        elif choix == 3:
            ShowTutorial()

        # Observatoire de musique
        elif choix == 1521951822120151892113:
            ShowObservatorium()

        elif choix == 24:
            PlayMusic("gravestone")
            ShowRecup()
            PlayMusic("start")


def ShowObservatorium():
    PlayMusic("observatorium")
    observatorium_complet = False
    while True:
        while True:
            try:
                # affiche le menu
                choix = ShowMenuObservatorium(observatorium_complet)
                ClearConsole()
                if observatorium_complet:
                    if choix in range(1, (len(LISTEDEMUSIQUE)) + 2):
                        break
                else:
                    if choix in range(1, 41) or choix == 11525:
                        break
            except ValueError:
                ClearConsole()
        if choix == 1:
            PlayMusic("start")
            break
        elif choix == 11525:
            mixer.quit()
            observatorium_complet = True
            print(
                "Les confins de l'observatorium s'ouvrent a vous, voyageurs sur une mer d'encre a la recherche de la véritée."
            )
            Affichage.EntreePourContinuer()
        else:
            caracteristique_musique = LISTECARACTERISTIQUEMUSIQUE[choix - 2]
            PlayMusic(f"{caracteristique_musique[0]}")
            print(caracteristique_musique[1])
            print("\n\n\n")
            Affichage.EntreePourContinuer()
            ClearConsole()
        if observatorium_complet:
            PlayMusic("darkness")
        else:
            PlayMusic("observatorium")


def ShowMenuObservatorium(observatorium_complet):
    numero_affichage = 2
    print("  ~~{ Observatorium }~~")
    print("\n1 - Retour")
    for nom_musique in LISTEDEMUSIQUE:
        print(f"{numero_affichage} - {nom_musique}")
        numero_affichage += 1
        if numero_affichage == 41 and not observatorium_complet:
            break
    return int(input("\nChoisissez la musique avec les nombres : "))


def GetChoiceMenuColiseum():
    if Player.mode_de_jeu == "Ascension":
        print(
            f"             -=[ EtAAAAAge {Player.numero_de_letage} ]=-"
            "\n\n          ~~{ CommmmmBAbt }~~"
            f"\n      MPDZ - AfERRORr un monsRISEABOVE restants)"
            f"\n      2 - ASCENSION"
            "\n\n          ~~{ Int/////n }~~"
            "\n      96843540432agir avec le Marchand"
            "\n      INFAMIEINTOLERABLELAISSEDERRIERETESAILESNOIRECHARBON"
            f"\n\n          ~~{{ {Player.nom_du_personnage} }}~~"
            "\n      AAA - Ficopppzdok"
            "\n      dza - Ut1l1se           r1un1 zapioqjdnn"
            "\n      d - Sauvzdnlqjndtie"
            "\n\n"
        )
    elif Player.nom_de_letage == "Dédale Frontière" :
        print(
            f"             -=[ Etage {Player.numero_de_letage} ]=-"
            "\n\n          ~~{ Combat }~~"
            f"\n      1 - Affronter un monstre...?"
            f"\n      2 - {Player.commentaire_boss}"
            "\n\n          ~~{ Interraction }~~"
            "\n      3 - Interragir avec le Marchand"
            "\n      4 - Observer l'Étage"
            f"\n\n          ~~{{ {Player.nom_du_personnage} }}~~"
            "\n      5 - Fiche de Personnage"
            "\n      6 - Utiliser un Red Coin"
            "\n      7 - Sauvegarder la Partie"
            "\n\n"
        )
    else :
        print(
            f"             -=[ Etage {Player.numero_de_letage} ]=-"
            "\n\n          ~~{ Combat }~~"
            f"\n      1 - Affronter un monstre ({Player.nombre_dennemis_a_letage} restants)"
            f"\n      2 - {Player.commentaire_boss}"
            "\n\n          ~~{ Interraction }~~"
            "\n      3 - Interragir avec le Marchand"
            "\n      4 - Observer l'Étage"
            f"\n\n          ~~{{ {Player.nom_du_personnage} }}~~"
            "\n      5 - Fiche de Personnage"
            "\n      6 - Utiliser un Red Coin"
            "\n      7 - Sauvegarder la Partie"
            "\n\n"
        )
    return int(input("Choisissez une action avec les nombres : "))


def RemiseAZeroDesVariablesPourProchainEtage():
    Player.affronte_un_boss = False
    Player.boss_battu = False
    Player.redcoin_bought = False
    Player.red_coin_recu_par_extermination = False
    Player.nombre_dennemis_a_letage = 10 + Player.numero_de_letage * 2
    Player.commentaire_boss = "Affronter le Boss"
    Player.quete = "None"
    Player.possede_la_cle = False
    if FloorMaker.carte_ouverte:
        clear()
    FloorMaker.__init__()
    if Player.numero_de_letage == 0:
        Player.nombre_dennemis_a_letage = 0
        Player.possede_la_cle = True
    elif Player.numero_de_letage in [10, 11]:
        Player.nombre_dennemis_a_letage = 0
    


def DoFight():
    # combat contre ennemi
    if Player.nombre_dennemis_a_letage != 0:
        Affichage.AfficheIntroCombat()
        # initialise la classe controleur, et par extention la classe
        #       vue et modele
        control = controleur.Control(Player, Trader)
        # lance la bataille
        try:
            control.Battle()
            Player.nombre_dennemis_a_letage -= 1
        except Exception as error:
            WriteErrorInErrorLog(error)
        PlayMusicDeLetage()
    # plus dennemi a combattre
    else:
        Affichage.AffichePlusDennemis()


def WriteErrorInErrorLog(erreur):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    chemin_du_fichier = dir_path + "ErrorLog.txt"
    date_et_heure = time.strftime("%Y-%m-%d %H:%M")
    erreur = traceback.format_exc()
    with open(chemin_du_fichier, "a") as fichier:
        fichier.write(
            "-----------------------------------------"
            "------------------------------------------"
            "------------------------------------------"
            "------------------------------------------"
            f"---------\n{date_et_heure}\nDébut du Log\n\n"
        )
        fichier.write(f"{erreur}")
        fichier.write(
            "\nFin du Log\n-----------------------------"
            "-------------------------------------------"
            "-------------------------------------------"
            "-------------------------------------------"
            "------------------\n"
        )
    print("Une erreur est survenue pendant le déroulement du combat.")
    print(
        "L'écriture d'un rapport d'erreur est en cours dans le fichier ColiseumDependenciesErrorLog.txt."
    )
    print("Veuilez patienter 3 secondes...")
    time.sleep(3)
    Affichage.EntreePourContinuer()
    Player.points_de_vie = Player.points_de_vie_max
    Player.points_de_mana = Player.points_de_mana_max
    print("Vous avez récupéré tout vos pv.")
    print("Vous avez récupéré tout vos pm.")
    gold_gagne = 30 * Player.numero_de_letage
    Player.nombre_de_gold += gold_gagne
    print("Le nombre de monstres restant à l'étage n'a pas changé.")
    print(f"Nous vous donnons {gold_gagne} en guise de réparation.")
    print("Veuillez nous excuser pour le dérangement.")
    Affichage.EntreePourContinuer()


def DoBossFight():
    if Player.possede_la_cle:
        if Player.nom_de_letage == "Dédale Frontière" :
            mixer.quit()
            Player.boss_battu = True
            Player.commentaire_boss = "Descendre a l'étage inferieur"
            print("Vous vous approchez prudemment de la grille, attendant un boss a la hauteur du labyrinthe que vous venez de conquérir, cepandant...")
            Affichage.EntreePourContinuer()
            print("...personne ne vient.")
            Affichage.EntreePourContinuer()
            print("Vous entendez la voix de Jean dans votre esprit :")
            Affichage.EntreePourContinuer()
            print("*Ca aurait du être moi. Mais tu m'a libéré avant qu'il puisse me récolter.*")
            Affichage.EntreePourContinuer()
            print("*Prend donc cette pause comme un cadeau et prépare toi bien avant de descendre.*")
            Affichage.EntreePourContinuer()
            PlayMusicDeLetage()
        else:
            Affichage.AfficheIntroCombatBoss()
            Player.affronte_un_boss = True
            control = controleur.Control(Player, Trader)
            try:
                control.Battle()
                Player.affronte_un_boss = False
                Player.boss_battu = True
                Player.commentaire_boss = "Descendre a l'étage inferieur"
                

            except Exception as error:
                WriteErrorInErrorLog(error)
            PlayMusicDeLetage()
    else:
        if Player.nom_de_letage == "Limbes Flétrissants":
            print("Vous cherchez un moyen de descendre , ou d'affronter un boss, mais ne trouvez rien.")
            Affichage.EntreePourContinuer()
            print("Peut être n'avez vous pas observé l'étage suffisamment ?")
            Affichage.EntreePourContinuer()
        else:
            print(
                "Vous rentrez dans l'arène et jettez un coup d'oeil aux tribunes vides, avant de donner un coup de pied sur le sol."
            )
            Affichage.EntreePourContinuer()
            print("Mais rien ne se produit.")
            Affichage.EntreePourContinuer()
            print(
                "Une grille de métal ancien a l'autre bout de l'arène attire votre regard."
            )
            print(
                "Derriere ses barreaux imposants, vous pouvez apercevoir un escalier s'enfoncant dans les ténèbres."
            )
            Affichage.EntreePourContinuer()
            print("Cepandant, la grille ne semble pas posséder de serrure.")
            print(
                "Peut-etre pourriez vous trouver, quelque part dans l'étage, un moyen de l'ouvrir ?"
            )
            Affichage.EntreePourContinuer()

def GoDown():
    Affichage.AfficheDescente()
    Player.numero_de_letage += 1
    DefinitNomEtage()
    RemiseAZeroDesVariablesPourProchainEtage()
    Affichage.AffichageDescriptionEtage()
    if Player.numero_de_letage == 12 or (
        Player.numero_de_letage == 9 and not ("Marque du Sacrifice" in Player.liste_dartefacts_optionels)
    ):
        game_in_session = False
    else:
        game_in_session = True
    return game_in_session


def DoRedcoin():
    while True:
        while True:
            try:
                print(
                    "     -={ RedCoin }=-   /925435351305251SERVICEDERECUPERATIONDEDONNEES7117764"
                )
                print(
                    "                      /7420952721321625369856321569852156AOUVRIRVIALEMENU556"
                )
                print(
                    "1 - Retour           /981265161565513513513165050742315698522685256PRINCIPAL"
                )
                print(
                    " ____/1233232311579764382419683214618568246856824565546532854663243615463745"
                )
                print(
                    " \95363541653155641654135641459565415631612952955265653959562413153556163153"
                )
                print(
                    "Code -       Nom       -    Prix    /128243165325615323235106506863236550325"
                )
                print(
                    "1257 - Affinité de Feu - 1 Redcoin /52565265163512ERRORERRORERRORERORERROR98"
                )
                print(
                    "5675 - Affinité de Foudre - 1 Red/487965651268416535498165319651965ERRORROOR"
                )
                print(
                    "9731 - Affinité de Sang - 1 Redc/789ERREUR:DONNESMANQUANTES96515866519651988"
                )
                print(
                    "7563 - Af/7845123553213506516896652565167841961561653163165ERRORERRORERROR58"
                )
                print(
                    "8240 - A/7845621365265216532561517VEUILLEZCONTACTERLESERVICEINFORMATIQUE9465"
                )
                print(
                    "6______/789OUUTILISEZNOTRESERVICE65235216513351DERECUPERATIONDEDONNEES313135"
                )
                print(
                    "/5698994524527/==================================\9AU5NUMERO5612353105151588"
                )
                print(
                    "1569899452452/Talent à débloquer avec le nombre corresponda\_35168SUIVANT:24"
                )
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
            (Player.nombre_de_red_coin >= cout_du_talent)
            and (talent_necessaire_pour_obtention == "None")
            and (talent not in Player.talents_possedes)
            or (Player.nombre_de_red_coin >= cout_du_talent)
            and (talent_necessaire_pour_obtention in Player.talents_possedes)
            and (talent not in Player.talents_possedes)
        ):
            if Player.stigma_negatif != "Incompatible":
                Player.talents_possedes.append(talent)
                Player.nombre_de_red_coin -= cout_du_talent
                print(
                    "Vous buvez le liquide incolore contenu dans les redcoins et faites circuler votre mana comme indiqué par le code ."
                )
                print(f"Vous gagnez le talent [{talent}] !")
                Affichage.EntreePourContinuer()
                CheckForFusionOfTalent(talent)
            else:
                Player.nombre_de_red_coin -= cout_du_talent
                print(
                    "Vous buvez le liquide incolore contenu dans les redcoins et faites circuler votre mana comme indiqué par le code..."
                )
                print("...avant de vomir violemment tout le contenu de votre estomac.")
                print(
                    "On dirait que votre corps n'est pas compatible avec les redcoins."
                )
                Affichage.EntreePourContinuer()


def CheckForFusionOfTalent(talent):
    commentaire = "...?"
    if talent in [
        "Oeuil Magique",
        "Pira",
        "Elektron",
        "Tsumeta-Sa",
        "Mathair",
        "Fos",
        "Haddee",
    ]:
        if "Oeuil Magique" in Player.talents_possedes:
            if "Pira" in Player.talents_possedes:
                commentaire += "\nLes talents Oeuil Magique et Pira interragissent dans votre corps et donnent naissance a un nouveau talent !"
                talent = "Oculus Ignis"
                Player.talents_possedes.append(talent)
                commentaire += f"\nVous gagnez le talent [{talent}] !"
            if "Elektron" in Player.talents_possedes:
                commentaire += "\nLes talents Oeuil Magique et Elektron interragissent dans votre corps et donnent naissance a un nouveau talent !"
                talent = "Oculus de Caelo"
                Player.talents_possedes.append(talent)
                commentaire += f"\nVous gagnez le talent [{talent}] !"
            if "Tsumeta-Sa" in Player.talents_possedes:
                commentaire += "\nLes talents Oeuil Magique et Tsumeta-Sa interragissent dans votre corps et donnent naissance a un nouveau talent !"
                talent = "Oculus Glacies"
                Player.talents_possedes.append(talent)
                commentaire += f"\nVous gagnez le talent [{talent}] !"
            if "Mathair" in Player.talents_possedes:
                commentaire += "\nLes talents Oeuil Magique et Mathair interragissent dans votre corps et donnent naissance a un nouveau talent !"
                talent = "Oculus Terrae"
                Player.talents_possedes.append(talent)
                commentaire += f"\nVous gagnez le talent [{talent}] !"
            if "Fos" in Player.talents_possedes:
                commentaire += "\nLes talents Oeuil Magique et Fos interragissent dans votre corps et donnent naissance a un nouveau talent !"
                talent = "Corporalis Oculus"
                Player.talents_possedes.append(talent)
                commentaire += f"\nVous gagnez le talent [{talent}] !"
            if "Haddee" in Player.talents_possedes:
                commentaire += "\nLes talents Oeuil Magique et Haddee interragissent dans votre corps et donnent naissance a un nouveau talent !"
                talent = "Sanguis Oculus"
                Player.talents_possedes.append(talent)
                commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in ["Eboulis", "Grand Froid"]:
        if ("Eboulis" in Player.talents_possedes) and (
            "Grand Froid" in Player.talents_possedes
        ):
            commentaire += "\nLes talents Eboulis et Grand Froid interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Avalanche"
            Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in ["Oeuil Magique", "Connaissance"]:
        if ("Oeuil Magique" in Player.talents_possedes) and (
            "Connaissance" in Player.talents_possedes
        ):
            commentaire += "\nLes talents Oeuil Magique et Connaissance interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Metamorphosis"
            Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in ["Luciole", "Pyromage"]:
        if ("Luciole" in Player.talents_possedes) and (
            "Pyromage" in Player.talents_possedes
        ):
            commentaire += "\nLes talents Luciole et Pyromage interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Bougie Magique"
            Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in ["Suroxygenation", "Réflex"]:
        if ("Suroxygenation" in Player.talents_possedes) and (
            "Réflex" in Player.talents_possedes
        ):
            commentaire += "\nLes talents Suroxygenation et Réflex interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Ultra-Instinct"
            Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in ["Cycle Glaciaire", "Pyromage", "Patience", "Carte du Gout", "Nectar"]:
        if (
            ("Cycle Glaciaire" in Player.talents_possedes)
            and ("Pyromage" in Player.talents_possedes)
            and ("Patience" in Player.talents_possedes)
            and ("Carte du Gout" in Player.talents_possedes)
            and ("Nectar" in Player.talents_possedes)
        ):
            commentaire += "\nLes talents Cycle Glaciaire, Pyromage, Patience, Carte du Gout et Nectar interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Réjuvénation"
            Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in [
        "Affinitée de Feu",
        "Affinitée de Foudre",
        "Affinitée de Glace",
        "Affinitée de Terre",
        "Affinitée Physique",
        "Affinitée de Sang",
    ]:
        if (
            ("Affinitée de Feu" in Player.talents_possedes)
            and ("Affinitée de Foudre" in Player.talents_possedes)
            and ("Affinitée de Glace" in Player.talents_possedes)
            and ("Affinitée de Terre" in Player.talents_possedes)
            and ("Affinitée de Sang" in Player.talents_possedes)
            and ("Affinitée Physique" in Player.talents_possedes)
        ):
            commentaire += (
                "\nLes talents Affinitée de Feu, Affinitée de Foudre,"
                " Affinitée de Glace, Affinitée de Terre, Affinitée Physique"
                " et Affinitée de Sang interragissent dans votre corps et "
                "donnent naissance a un nouveau talent !"
            )
            talent = "Elémento-Réceptif"
            Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in [
        "Rapide",
        "Grand Froid",
        "Réflex",
        "Conditions Limites",
        "Aura de Feu",
        "Poussière de Diamants",
    ]:
        if (
            ("Rapide" in Player.talents_possedes)
            and ("Grand Froid" in Player.talents_possedes)
            and ("Réflex" in Player.talents_possedes)
            and ("Conditions Limites" in Player.talents_possedes)
            and ("Aura de Feu" in Player.talents_possedes)
            and ("Poussière de Diamants" in Player.talents_possedes)
        ):
            commentaire += (
                "\nLes talents Rapide, Grand Froid,"
                " Réflex, Conditions Limites, Aura de Feu"
                " et Poussière de Diamants interragissent dans votre corps et "
                "donnent naissance a un nouveau talent !"
            )
            talent = "Grand Pandémonium Elémentaire"
            Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in ["Baron Rouge", "Pyrosorcier", "Connaissance"]:
        if (
            ("Baron Rouge" in Player.talents_possedes)
            and ("Pyrosorcier" in Player.talents_possedes)
            and ("Connaissance" in Player.talents_possedes)
        ):
            commentaire += "\nLes talents Baron Rouge, Pyrosorcier et Connaissance interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Maitre du Mana"
            Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in ["Pira", "Pyromage", "Rafale"]:
        if (
            ("Pira" in Player.talents_possedes)
            and ("Pyromage" in Player.talents_possedes)
            and ("Rafale" in Player.talents_possedes)
        ):
            commentaire += "\nLes talents Pira, Pyromage et Rafale interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Libération de Feu"
            Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"

    if talent in ["Elektron", "Facture", "Luciole"]:
        if (
            ("Elektron" in Player.talents_possedes)
            and ("Facture" in Player.talents_possedes)
            and ("Luciole" in Player.talents_possedes)
        ):
            commentaire += "\nLes talents Elektron, Facture et Luciole interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Libération de Foudre"
            Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in ["Tsumeta-Sa", "Cycle Glaciaire", "Grand Froid"]:
        if (
            ("Tsumeta-Sa" in Player.talents_possedes)
            and ("Cycle Glaciaire" in Player.talents_possedes)
            and ("Grand Froid" in Player.talents_possedes)
        ):
            commentaire += "\nLes talents Tsumeta-Sa, Cycle Glaciaire et Grand Froid interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Libération de Glace"
            Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"

    if talent in ["Mathair", "Fracturation", "Eboulis"]:
        if (
            ("Mathair" in Player.talents_possedes)
            and ("Fracturation" in Player.talents_possedes)
            and ("Eboulis" in Player.talents_possedes)
        ):
            commentaire += "\nLes talents Mathair, Fracturation et Eboulis interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Libération de Terre"
            Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"

    if talent in ["Fos", "Oeuil Magique", "Réflex"]:
        if (
            ("Fos" in Player.talents_possedes)
            and ("Oeuil Magique" in Player.talents_possedes)
            and ("Réflex" in Player.talents_possedes)
        ):
            commentaire += "\nLes talents Fos, Oeuil Magique et Réflex interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Libération Physique"
            Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"

    if talent in ["Haddee", "Anticoagulants", "Baron Rouge"]:
        if (
            ("Haddee" in Player.talents_possedes)
            and ("Anticoagulants" in Player.talents_possedes)
            and ("Baron Rouge" in Player.talents_possedes)
        ):
            commentaire += "\nLes talents Haddee, Anticoagulants et Baron Rouge interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Libération de Sang"
            Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if commentaire != "...?":
        print(commentaire)
        Affichage.EntreePourContinuer()


def AffichageSecretPage3():
    try:
        dummy = {}
        dir_path = os.path.dirname(os.path.realpath(__file__))
        chemin_du_fichier_save = dir_path + "\\error.txt"
        with open(chemin_du_fichier_save, "r") as fichier:
            reader = csv.DictReader(fichier, delimiter="|")
            for line in reader:
                dummy[line["Caracteristique"]] = line["Valeur"]
        if dummy["error"] == "error":
            PlayMusic("abyss")
            numero = 0
            while True:
                print("ERREUR : VARIABLE VIE NON TROUVEE")
                print("ANCIENNES DONNEES TROUVEES, CHARGEMENT EN COURS...")
                print("ERREUR : ANCIENNES DONNEES EN COURS DUTILISATION")
                print("UTILISATION DES DONNEES AVEC UNE AUTRE VARIABLE VIE...")
                print(
                    "ERREUR : TEMPS DE JEU DES ANCIENNES DONNEES DEPASSE MEMOIRE VIVE DE LA MACHINE"
                )
                print("REBOOT DU PROGRAMME EN COURS....")
                print(
                    f"TENTATIVE NUMERO {numero} DE RESOLUTIONS DES (ERROR : OVERDRIVE) ERREURS EN COURS..."
                )
                if numero == 313:
                    break
                time.sleep(0.01)
                ClearConsole()
                numero += 1
            print("SOLUTION TROUVEE")
            print("SUPPRESSION DES DONNEES CORROMPUE TERMINEE")
            print("MESSAGE DE [ERROR : UNKNOWN] : continue. rapproche toi. bientôt.")
            Affichage.EntreePourContinuer()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            chemin_du_fichier = dir_path + "\\error.txt"
            os.remove(chemin_du_fichier)
            ClearConsole()
    except FileNotFoundError:
        ClearConsole()

def GoUp():
    print("Vous remontez les marches du Coliseum.")
    Affichage.EntreePourContinuer()
    Player.numero_de_letage -= 1
    if Player.numero_de_letage == 0:
        Player.mode_de_jeu = "Descente"
        mixer.quit()
        print("Vous arrivez a votre destination.")
        Affichage.EntreePourContinuer()
    RemiseAZeroDesVariablesPourProchainEtage()
    DefinitNomEtage()
    game_in_session = True
    if game_in_session:
        PlayMusicDeLetage()
        try:
            FloorMaker.SetupFloorLayout()
            Save.SaveTheGameSansAffichage()
        except Exception as error:
            WriteErrorInErrorLog(error)

def DoBossOrGoDown():
    game_in_session = True

    if Player.mode_de_jeu == "Ascension":
        GoUp()

    else:
        # combat contre boss
        if not Player.boss_battu and not "Passe La Porte Redcoin" in Player.player_tags:
            DoBossFight()
                
        # descente au niveau inferieur
        else:
            if Player.mode_de_jeu == "Véritable Descente" and Player.numero_de_letage == 0:
                GiveChoiceRealEndingOrNot()
            if Player.nom_de_letage == "Limbes Flétrissants" and Player.numero_boss_alt in range(1, 11) and not "Passe La Porte Redcoin" in Player.player_tags:
                Player.numero_de_letage -= 1
                Player.etage_alternatif = True
                Player.numero_boss_alt += 1
            game_in_session = GoDown()
            if game_in_session:
                PlayMusicDeLetage()
                try:
                    FloorMaker.SetupFloorLayout()
                except Exception as error:
                    WriteErrorInErrorLog(error)
    return game_in_session
            
def GiveChoiceRealEndingOrNot():
    print("Vous vous approchez du centre de l'arène.")
    Affichage.EntreePourContinuer()
    print("Vous pouvez absorber la Marque du Sacrifice de Jean afin d'entrer dans les profondeurs du Coliseum...")
    Affichage.EntreePourContinuer()
    print("...ou la laisser pour n'aller qu'a la fin de l'histoire de votre personnage.")
    Affichage.EntreePourContinuer()
    print("Le choix est votre.")
    Affichage.EntreePourContinuer()
    while True :
        try:
            print("1 - Absorber la Marque du Sacrifice")
            print("2 - Descendre ")
            choix = int(input("\nFaites votre choix avec les numéros :"))
            ClearConsole()
            if choix in [1, 2]:
                break
        except ValueError:
            ClearConsole()
    if choix == 1:
        print("Vous approchez votre main de la masse argentée, et celle ci fonce sur votre épaule.")
        Affichage.EntreePourContinuer()
        print("Vous sentez une agréable chaleur émettre du point d'impact.")    
        Affichage.EntreePourContinuer()
        print("Vous obtenez la Marque du Sacrifice !")
        Affichage.EntreePourContinuer()
        Player.liste_dartefacts_optionels.append("Marque du Sacrifice")
    print("Vous continuez votre chemin.")
    Affichage.EntreePourContinuer()

def GetChoix():
    while True:
        try:
            choix = GetChoiceMenuColiseum()
            ClearConsole()
            if choix != 2 and Player.mode_de_jeu == "Ascension":
                print("LECHEMINVERSLASCENSIONESTDROITILESTRIGIDENETECARTEPASDUCHEMINOUTOMBEDANSLESENTRAILLESDEMONODIEUESTOMAC")
                Affichage.EntreePourContinuer()
            elif choix in range(1, 8):
                return choix
        except ValueError:
            ClearConsole()


def DefinitNomEtage():
    if Player.numero_de_letage == 0:
        Player.nom_de_letage = "Sanctuaire du Sacrifice"
    elif Player.numero_de_letage == 1:
        Player.nom_de_letage = "Ruines Abandonnées"
    elif Player.numero_de_letage == 2:
        Player.nom_de_letage = "Forêt Désenchantée"
        if Player.etage_alternatif:
            Player.nom_de_letage = "Jungle Cruelle"
    elif Player.numero_de_letage == 3:
        Player.nom_de_letage = "Champs de Sables"
    elif Player.numero_de_letage == 4:
        Player.nom_de_letage = "Tour de l'Esprit"
    elif Player.numero_de_letage == 5:
        Player.nom_de_letage = "Carnaval de Rouille"
    elif Player.numero_de_letage == 6:
        Player.nom_de_letage = "Bidonville du Clocher"
    elif Player.numero_de_letage == 7:
        Player.nom_de_letage = "Cachots de l'Immonde"
        if Player.etage_alternatif:
            Player.nom_de_letage = "Douves du Pénitent"
    elif Player.numero_de_letage == 8:
        Player.nom_de_letage = "Arène du Zénith"
    elif Player.numero_de_letage == 9:
        Player.nom_de_letage = "Chemins Coalescents"
    elif Player.numero_de_letage == 10:
        Player.nom_de_letage = "Dédale Frontière"
        if Player.etage_alternatif:
            Player.nom_de_letage = "Limbes Flétrissants"
    elif Player.numero_de_letage == 11:
        Player.nom_de_letage = "Rivages Distants"
    Player.etage_alternatif = False


def PlayMusicDeLetage():
    nom_de_la_musique = str(Player.numero_de_letage)
    if Player.nom_de_letage in ["Jungle Cruelle", "Limbes Flétrissants", "Douves du Pénitent"]:
        nom_de_la_musique += "_alt"
    if Player.nom_de_letage == "Dédale Frontière" :
        PlayMusic(Player.musique_etage_10)
    else:
        PlayMusic(f"etage_{nom_de_la_musique}")


def GetNomEtage():
    try:
        dictionnaire = {}
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # fichier de sauvegarde (temporaire)
        chemin_du_fichier_save = dir_path + "\\save.txt"
        with open(chemin_du_fichier_save, "r") as fichier:
            reader = csv.DictReader(fichier, delimiter="|")
            for line in reader:
                dictionnaire[line["Caracteristique"]] = line[
                    "Valeur"
                ]
        Player.nom_de_letage = dictionnaire["Nom de l'étage"]
    except KeyError:
        pass
    except FileNotFoundError:
        pass

def SetupGameMode():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    chemin_sove = dir_path + "\\s0ve.txt"
    chemin_sive = dir_path + "\\s1ve.txt"

    dictionnaire_de_choses_permanentes = {}
    # fichier de sauvegarde (permanant)
    if os.path.isfile(chemin_sive):
        chemin_du_fichier_save = dir_path + "\\s1ve.txt"
    else:
        chemin_du_fichier_save = dir_path + "\\s0ve.txt"
    with open(chemin_du_fichier_save, "r") as fichier:
        reader = csv.DictReader(fichier, delimiter="|")
        for line in reader:
            dictionnaire_de_choses_permanentes[line["Caracteristique"]] = line[
                "Valeur"
            ]
    
    if dictionnaire_de_choses_permanentes["486241597531"] == "Jean.rar":
        Player.battu_le_sacrifie = True

    if Player.battu_le_sacrifie and os.path.isfile(chemin_sove):
        Player.mode_de_jeu = "Véritable Descente"
    elif not Player.battu_le_sacrifie and os.path.isfile(chemin_sive):
        Player.mode_de_jeu = "Ascension"
    elif not Player.battu_le_sacrifie and os.path.isfile(chemin_sove):
        Player.mode_de_jeu = "Descente"
    else:
        Player.mode_de_jeu = "Erreur"

    







def DoJukebox():
    dictionnaire_musiques_jukebox = {
        1 : {"Nom" : "Exploratio", "Nom Réel" : "etage_1"},
        2 : {"Nom" : "Les Joies du Combat", "Nom Réel" : "battle_theme_1"},
        3 : {"Nom" : "Revenant", "Nom Réel" : "boss_1"},
        4 : {"Nom" : "Conte de Fée", "Nom Réel" : "etage_2"},
        5 : {"Nom" : "Epineuses Rencontres", "Nom Réel" : "battle_theme_2"},
        6 : {"Nom" : "Le Chevalier Qu'on Ne Veut Pas Rencontrer", "Nom Réel" : "boss_2"},
        7 : {"Nom" : "Affreux Fertile", "Nom Réel" : "etage_2_alt"},
        8 : {"Nom" : "Clair de Sang", "Nom Réel" : "battle_theme_2_alt"},
        9 : {"Nom" : "Néophobie Alimentaire", "Nom Réel" : "boss_2_alt"},
        10 : {"Nom" : "Ruines d'Antan", "Nom Réel" : "etage_3"},
        11 : {"Nom" : "Sables Mouvants", "Nom Réel" : "battle_theme_3"},
        12 : {"Nom" : "Euthanasie Régalienne", "Nom Réel" : "boss_3"},
        13 : {"Nom" : "Pāramitā", "Nom Réel" : "etage_4"},
        14 : {"Nom" : "Nerd Party", "Nom Réel" : "battle_theme_4"},
        15 : {"Nom" : "Jeux d'Enfants", "Nom Réel" : "boss_4"},
        16 : {"Nom" : "Pantomime", "Nom Réel" : "boss_4_phase_2"},
        17 : {"Nom" : "Carnaval", "Nom Réel" : "etage_5"},
        18 : {"Nom" : "Piñata", "Nom Réel" : "battle_theme_5"},
        19 : {"Nom" : "Tragicomique", "Nom Réel" : "boss_5"},
        20 : {"Nom" : "Combler les Vides", "Nom Réel" : "etage_6"},
        21 : {"Nom" : "Systèmes Défaillants", "Nom Réel" : "battle_theme_6"},
        22 : {"Nom" : "Sa Majesté Des Mouches", "Nom Réel" : "boss_6"},
        23 : {"Nom" : "Divin Karma", "Nom Réel" : "etage_7"},
        24 : {"Nom" : "Folie Furieuse", "Nom Réel" : "battle_theme_7"},
        25 : {"Nom" : "Comment Tuer le Grand Méchant Loup", "Nom Réel" : "boss_7"},
        26 : {"Nom" : "Ossuaire Immaculé", "Nom Réel" : "etage_8"},
        27 : {"Nom" : "Dissonance Cognitive", "Nom Réel" : "battle_theme_8"},
        28 : {"Nom" : "Faux Semblants", "Nom Réel" : "boss_8"},
        29 : {"Nom" : "La Hache et le Grimoire", "Nom Réel" : "boss_8_phase_2"},
        30 : {"Nom" : "Fièvre du Samedi Soir", "Nom Réel" : "dance"},
        31 : {"Nom" : "S1mul4crum", "Nom Réel" : "etage_0"},
        32 : {"Nom" : "Cruc1fix1on", "Nom Réel" : "boss_0"},
        33 : {"Nom" : "V3tus S4nct0rum", "Nom Réel" : "battle_theme_0"},
        34 : {"Nom" : "Réarr4ng3ment L1m1nal", "Nom Réel" : "etage_9"},
        35 : {"Nom" : "4rythm1e", "Nom Réel" : "battle_theme_9"},
        36 : {"Nom" : "Au Dé7our D’un S3nti3r Une Ch4rogn3 Infâme", "Nom Réel" : "boss_9"},
        37 : {"Nom" : "Endorphines", "Nom Réel" : "tutorial"},
        38 : {"Nom" : "Dangereuses Mélancolies", "Nom Réel" : "alfredproto"},
        39 : {"Nom" : "L'Orage avant la Tempête", "Nom Réel" : "boss_introV2"},
        40 : {"Nom" : "Sillages Sur Une Mer de Rêves", "Nom Réel" : "gravestone"},
        41 : {"Nom" : "Bêtise Humaine", "Nom Réel" : "reconfort"},
        
    }
    print("Vous frappez le sol de l'arène, et au lieu de monstres, une étrange machine sort du sol.")
    Affichage.EntreePourContinuer()
    print("Sur sa devanture, vous pouvez observer deux cadres régulant respectivement la musique actuelle de l'étage et sa musique de combat, ainsi qu'une vitre en dessous.")
    print("Placardé sur un des côtés de la machine, vous trouvez un papier jaunissant sur laquelle se trouve une liste de musiques ainsi que des codes qui leurs sont associés.")
    Affichage.EntreePourContinuer()
    print("Vous pouvez changer les musiques en sélectionnant un cadre et en entrant un code sur un pavé numérique a coté.")
    Affichage.EntreePourContinuer()
    
    while True:
        while True:
            try:
                # attribue le code actuel a un nom
                for cle in dictionnaire_musiques_jukebox:
                    if dictionnaire_musiques_jukebox[cle]["Nom Réel"] == Player.musique_etage_10:
                        nom_musique_etage = dictionnaire_musiques_jukebox[cle]["Nom"]
                        break
                for cle in dictionnaire_musiques_jukebox:
                    if dictionnaire_musiques_jukebox[cle]["Nom Réel"] == Player.musique_combat_10:
                        nom_musique_combat = dictionnaire_musiques_jukebox[cle]["Nom"]
                        break

                # affichage
                print(f"Musique de l'étage : [{nom_musique_etage}]")
                print(f"Musique des combats : [{nom_musique_combat}]")
                print("\n1 - Changer la musique de l'étage")
                print("2 - Changer la musique des combats")
                print("3 - Partir")
                choix = int(input("(Faites votre choix avec les numéros :) "))
                ClearConsole()

                if choix in range (1,4):
                    break
            except ValueError:
                ClearConsole()
        
        if choix == 3:
            print("Vous laissez le jukebox derrière vous, et il retourne dans le sol de l'arène.")
            Affichage.EntreePourContinuer()
            break

        elif choix == 2:
            choix_effectue = False
            while not choix_effectue:
                while True:
                    try:
                        print("Choix de la musique des combats :")
                        for numero in dictionnaire_musiques_jukebox:
                            print(f"{numero} - {dictionnaire_musiques_jukebox[numero]['Nom']}")
                        choix = int(input("\n(Faites votre choix avec les numéros :) "))
                        ClearConsole()
                        if choix in range (1, 41):
                            break
                    except ValueError:
                        ClearConsole()
                PlayMusic(dictionnaire_musiques_jukebox[choix]['Nom Réel'])
                while True:
                    try:
                        print(f"Vous avez choisi la musique de combat suivante : [{dictionnaire_musiques_jukebox[choix]['Nom']}]")
                        print("\nValidez-vous votre choix ?")
                        print("1 - Oui")
                        print("2 - Non")
                        choix_validation = int(input("(Faites votre choix avec les numéros :) "))
                        ClearConsole()
                        if choix_validation == 1 :
                            choix_effectue = True
                            Player.musique_combat_10 = dictionnaire_musiques_jukebox[choix]["Nom Réel"]
                            PlayMusicDeLetage()
                            print("A travers la vitre, vous voyez un bras méchanique prendre un disque noir comme le charbon et le poser sous la plaque.")
                            print("Une pointe venue d'en bas se pose dessus.")
                            print("Mais curieusement, le disque ne tourne pas.")
                            Affichage.EntreePourContinuer()
                            break
                        elif choix_validation == 2:
                            PlayMusicDeLetage()
                            break
                    except ValueError:
                        ClearConsole()
                    
        elif choix == 1:
            choix_effectue = False
            while not choix_effectue:
                while True:
                    try:
                        print("Choix de la musique de l'étage :")
                        for numero in dictionnaire_musiques_jukebox:
                            print(f"{numero} - {dictionnaire_musiques_jukebox[numero]['Nom']}")
                        choix = int(input("(Faites votre choix avec les numéros :) "))
                        ClearConsole()
                        if choix in range (1, 41):
                            break
                    except ValueError:
                        ClearConsole()
                PlayMusic(dictionnaire_musiques_jukebox[choix]["Nom Réel"])
                while True:
                    try:
                        print(f"Vous avez choisi la musique d'étage suivante : [{dictionnaire_musiques_jukebox[choix]['Nom']}]")
                        print("\nValidez-vous votre choix ?")
                        print("1 - Oui")
                        print("2 - Non")
                        choix_validation = int(input("(Faites votre choix avec les numéros :) "))
                        ClearConsole()
                        if choix_validation == 1 :
                            choix_effectue = True
                            Player.musique_etage_10 = dictionnaire_musiques_jukebox[choix]["Nom Réel"]
                            print("A travers la vitre, vous voyez un bras méchanique prendre un disque noir comme le charbon et le poser sur la plaque.")
                            print("Le disque tourne, et une pointe se pose dessus.")
                            print("La musique remplit alors l'étage.")
                            Affichage.EntreePourContinuer()
                            break
                        elif choix_validation == 2:
                            PlayMusicDeLetage()
                            break
                    except ValueError:
                        ClearConsole()

            
Save = SaveManagement()
Draw = DrawInTurtle()
Affichage = Affiche()
Observation = Observe()
FloorMaker = Floor()
Ending = EndingAndGift()
Player = PlayerCaracteristics()
Trader = TraderUsage()

SetupGameMode()
AffichageSecretPage3()
GetNomEtage()
if Player.mode_de_jeu == "Erreur":
    print("ERREUR 404: FICHIER DE SAUVEGARDE PERMANENT INTROUVABLE")
    print("ASSUREZ VOUS D'AVOIR UN FICHIER NOMME S0VE.TXT DANS COLISEUMDEPENDENCIES")
    Affichage.EntreePourContinuer()
    sys.exit()
else:
    MenuDeDemarrage(Player)
    game_in_session = True

def DoBossZero():
    if not "Combattant le Gardien" in Player.player_tags:
        while True:
            while True:
                try:
                    print("blablabla")
                    print("\n1 - J'y vais.")
                    print("2 - Qui es-tu ?")
                    print("3 - C'est quoi cet endroit ?")
                    print("4 - A propos des pages...")
                    print("5 - Pourquoi faire tout ca ?")
                    print("6 - Le véritable ennemi...")
                    print("7 - J'ai pas tellement envie de t'écouter parler, tu peux tout me résumer ?")
                    print("8 - J'ai très envie de t'écouter parler, tu peut tout me raconter dans les moindres détails ?")
                    print("9 - Tu as vu l'heure ? Il est temps de te sortir de là !")
                    choix = int(input("\nFaire votre choix avec les nombres : "))
                    ClearConsole()
                    if choix in range(1, 10):
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print("*Mais... mais non !*\n*Revient !*")
                Affichage.EntreePourContinuer()
                break
            elif choix == 2:
                pass
            elif choix == 3:
                pass
            elif choix == 4:
                pass
            elif choix == 5:
                pass
            elif choix == 6:
                pass
            elif choix == 7:
                pass
            elif choix == 8:
                pass
            elif choix == 9:
                print("*Eh bien...c'est parti alors.*")
                Affichage.EntreePourContinuer()
                Player.player_tags.append("Combattant le Gardien")

                Player.affronte_un_boss = True
                control = controleur.Control(Player, Trader)
                try:
                    control.Battle()
                except Exception as error:
                    WriteErrorInErrorLog(error)
                RemiseAZeroDesVariablesPourProchainEtage()
                try:
                    FloorMaker.SetupFloorLayout()
                except Exception as error:
                    WriteErrorInErrorLog(error)
                PlayMusicDeLetage()
                print("Le monde se met a tourner, tourner, et vous ne reconnaissez plus l'étage dans lequel vous êtes.")
                print("La bombe fumigène vous a laissé confus, et vous en oubliez presque que le Gardien s'est enfui ! Allez le chercher dans l'étage !")
                Player.affronte_un_boss = False
                Affichage.EntreePourContinuer()
                break
    else:
        if Player.position_x == 0 and Player.position_y == 0:
            print("Le gardien n'est pas ici.")
            Affichage.EntreePourContinuer()
        else:
            print("Vous retrouvez le gardien entrain de soigner ses blessures, et votre confusion s'estompe !")
            print("Des petits êtres de lumière tournent autour de lui...")
            Affichage.EntreePourContinuer()
            print("Vous regardez ce spectacle attendrissant...")
            print("...et le gardien vous remarque.")
            Affichage.EntreePourContinuer()
            RemiseAZeroDesVariablesPourProchainEtage()
            Player.affronte_un_boss = True
            control = controleur.Control(Player, Trader)

            try:
                control.Battle()
            except Exception as error:
                WriteErrorInErrorLog(error)

            try:
                FloorMaker.SetupFloorLayout()
            except Exception as error:
                WriteErrorInErrorLog(error)

            if Player.vies_du_gardien == 0:
                mixer.quit()
                print("*Ca y est !*\n*Tu m'a absorbé !*")
                Observation.AddSoulToS0ve()
                dir_path = os.path.dirname(os.path.realpath(__file__))
                chemin_du_fichier_save = dir_path + "\\save.txt"
                os.remove(chemin_du_fichier_save)
                Affichage.EntreePourContinuer()
                print("*Je fais maintenant parti de toi...*")
                Affichage.EntreePourContinuer()
                print("*...")
                Affichage.EntreePourContinuer()
                print("*...on peut vous aider ?*")
                Affichage.EntreePourContinuer()
                print("Les esprits élémentaires flottent autour du gardien, et vous regardent en silence.")
                Affichage.EntreePourContinuer()
                print("Vous les regardez...")
                Affichage.EntreePourContinuer()
                print("Ils vous regardent...*")
                Affichage.EntreePourContinuer()
                print("Vous les regardez...")
                Affichage.EntreePourContinuer()
                print("Ils vous regardent...*")
                Affichage.EntreePourContinuer()
                print("Vous les regardez...")
                Affichage.EntreePourContinuer()
                print("Ils vous regardent...*")
                Affichage.EntreePourContinuer()
                print("Vous approchez votre main de votre arme...")
                Affichage.EntreePourContinuer()
                print("...et ils déguerpissent aussitôt en bas des escaliers de l'arène.")
                Affichage.EntreePourContinuer()
                print("*Oh. Je crois qu'ils viennent de se répandre dans les étages inferieurs.*\n*Tu risque de les recroiser assez souvent.*")
                Affichage.EntreePourContinuer()
                print("*Enfin bref.*")
                Affichage.EntreePourContinuer()
                print("*Je fais maintenant parti de toi...*")
                Affichage.EntreePourContinuer()
                print("*Mais pour éviter de disparaitre si tu meurs...*")
                Affichage.EntreePourContinuer()
                print("*...Je vais devoir aller ailleurs.*")
                Affichage.EntreePourContinuer()
                print("*Dans le fichier de sauvegarde permanent.*")
                Affichage.EntreePourContinuer()
                print("*Je devrais pouvoir y arriver tout seul. J'ai juste besoin que...*")
                Affichage.EntreePourContinuer()
                print("*...*")
                Affichage.EntreePourContinuer()
                print("*...tu viens de louper le combat petit bonhomme.*")
                Affichage.EntreePourContinuer()
                print("*Un autre esprit, Voluntad Tin Tuukul, s'approche du gardien avec un air un peu groggy.*")
                Affichage.EntreePourContinuer()
                print("*Ils sont déjà partis en bas, tu devrais les suivre.*")
                Affichage.EntreePourContinuer()
                print("L'esprit fait quelques tours autour de Jean, puis file en direction des escaliers.")
                Affichage.EntreePourContinuer()
                print("*On a dela chance de pas l'avoir eu celui-là.*\n*C'est l'esprit de l'âme. Tu sais ce que ca signifie ?*")
                Affichage.EntreePourContinuer()
                print("*Magie illimitée*")
                Affichage.EntreePourContinuer()
                print("*JEnfin bref.*")
                Affichage.EntreePourContinuer()
                print("*J'ai juste besoin que tu disparaisse quelques instants.*")
                Affichage.EntreePourContinuer()
                print("*Ca sera pas douloureux, promis juré !*")
                Affichage.EntreePourContinuer()
                print("*Et j'ai failli oublier : sans moi, le système d'ascension n'existe plus. Tu devrait renommer s1ve.txt en s0ve.txt, tu risque d'avoir une erreur sinon.*")
                time.sleep(10)
                sys.exit()
            else:
                #prendre les coordonnees d'une salle au pif
                salle_aleatoire = random.randint(1,6)
                caracteristique_de_la_salle = FloorMaker.FloorBlueprint[salle_aleatoire]

                #affecter ces coordonnéees au joueur
                Player.position_x = caracteristique_de_la_salle["position_x"]
                Player.position_y = caracteristique_de_la_salle["position_y"]
                Player.numero_de_la_salle = salle_aleatoire

                PlayMusicDeLetage()
                print("Le Gardien s'est enfui ! Allez le chercher dans l'étage !")
                Player.player_tags.append("Sort du Combat contre le Gardien")
                Player.affronte_un_boss = False
                Affichage.EntreePourContinuer()

            

    #si ya pas "Combattant le Gardien" dans les tags:
    #   -faire le menu ou on peut parler et tt
    #   -faire option pour combattre
    #   - clear la map de letage, mettre "Combattant le Gardien" dans les tags, commencer le combat
    #   - quand le combat se finit, pas oublier de garder la variable "nombre de vie du gardien"
    #   - quand le combat se finit, on reset le layout de l'étage, sans afficher de description ou autre
    #sinon :
    #   -si on est aux coordonnees 0 0,:
    #       on lance r (ya personne, va chercher le mob)
    #   -sinon:
    #       -on clear la map
    #       -on relance le fight avec les vies du gardien et tout.
    #       -quand combat finit, si les vies du mob == 0:
    #           -fin combat, explications, et puis kaboom.
    #       -sinon:
    #           - on reset la map, on change les coordonnnées du joueur, on l'amène aux nouvelles coordonnées.
    #
    #a faire;
    # -interdire le combat de mob, combat de boss, marchand, sauvegarde, item, recoin, quand tag dans les tags.
    # -bien setup genre 6 salles avec 5 monstres et 1 boss si on tente de screer un etage alors que ya tag dans tags
    # -setup les mobs basiques 



#Player.techniques_possedes = LISTETECHNIQUES
#Player.sorts_possedes = LISTESORTS
#Ending.DoEnding()
PlayMusicDeLetage()
while game_in_session:
    # choix de laction
    choix = GetChoix()
    # application de l'action
    if choix == 1:
        if Player.nom_de_letage == "Limbes Flétrissants":
            print("Vous cherchez une arène, ou quelque chose dans le genre, et ne trouvez que le champ de terre battu.")
            Affichage.EntreePourContinuer()
            print("Frapper le sol stérile ne fait rien apparaitre.")
            Affichage.EntreePourContinuer()
        elif Player.numero_de_letage == 0 :
            print("Vous frappez le sol de l'arène, mais rien ne se passe.")
            Affichage.EntreePourContinuer()
        elif Player.numero_de_letage != 10:
            DoFight()  # DONE
        else:
            DoJukebox()
    elif choix == 2:
        if Player.numero_de_letage == 0 and not Player.battu_le_sacrifie:
            DoBossZero()
        else:
            game_in_session = DoBossOrGoDown()  # DONE
    elif choix == 3:
        if Player.numero_de_letage == 0 :
            print("Vous vous approchez de l'endroit ou se trouve le marchand...")
            print("...mais il n'y a personne.")
            Affichage.EntreePourContinuer()
        elif Player.nom_de_letage == "Limbes Flétrissants" : 
            print("Vous cherchez le marchand...")
            print("...mais ne trouvez personne.")
            Affichage.EntreePourContinuer()
        else:
            Trader.DoTrading()  # DONE
    elif choix == 4:
        FloorMaker.ShowFloor()
    elif choix == 5:
        if "Combattant le Gardien" in Player.player_tags:
            print("Vous sortez votre sacoche, mais vous n'arrivez pas a vous souvenir comment utiliser vos objets ou vos sorts avec votre esprit confus, alors vous la raccrochez à sa place.")
            Affichage.EntreePourContinuer()
        else:
            Player.ShowPlayerCaracteristicsAndItems()  # DONE
    elif choix == 6:
        if "Combattant le Gardien" in Player.player_tags:
            print("Vous cherchez vos redcoins, mais votre esprit confus vous empeche de trouver quoi que ce soit.")
            Affichage.EntreePourContinuer()
        else:
            DoRedcoin()  # DONE
    elif choix == 7:
        if "Combattant le Gardien" in Player.player_tags:
            print("[ERREUR :", end=' ', flush=True)
            for i in range(200):
                print("ERREUR :", end=' ', flush=True)
                time.sleep(0.01)
            print("]", flush=True)
            ClearConsole()
        else:
            Save.SaveTheGame()  # DONE
Ending.DoEnding()




# Lance un debug pour la méthode GetUserChoice du controlleur
# control.DebugGetUserChoice()
# control.PatternDesignConstantUpdater()
# control.Cat_astrophe()
