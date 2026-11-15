"""Personnages jouables, objets de départ, améliorations possibles et choix offerts par les redcoins."""

UPPGRADESPOSSIBLES = {
    "Chapeau" : 0,
    "Boucles d'Oreille" : 0,
    "Collier" : 0,
    "Cotte de Maille" : 0,
    "Bracelet" : 0,
    "Gants" : 0,
    "Anneau" : 0,
    "Bottes" : 0,
    "Fiole de Sève" : 0,
    "Fiole de Rosée" : 0,
    "Tisane d'Ecorce" : 0,
    "Tisane de Racine" : 0,
    "Charge de Feu" : 0,
    "Charge de Glace" : 0,
    "Charge de Foudre" : 0,
    "Charge de Terre" : 0,
    "Charge de Chair" : 0,
    "Charge de Sang" : 0,
    "Ration Jindagee" : 0,
    "Ration Jindagee Raffinée" : 0,
    "Ration Aatma" : 0,
    "Ration Aatma Rafinée" : 0,
    "Ration Cristalline" : 0,
    "Ration d'Hydromel" : 0,
    "Ration Ambroisie" : 0,
    "Ration Explosive" : 0,
    "Ration Explosive Raffinée" : 0,
    "Pack de Fléchettes" : 0,
    "Pack de Flèches" : 0,
    "Pack Premier Tour" : 0,
    "Médaillon de Leprechaun" : 0,
    "Noyau d'Aurelionite" : 0,
    "Sacoche" : 0,
    "Emblème de la Fin" : 0,
    "Clé" : 0,
    "Carte" : 0
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
        "Monsieur Loyal",  # char stigma +
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
            "Affinitée de Foudre"
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
    "Voyageur": [  # char
        "Voyageur",
        (
            "Une existance superieure, intriguée par les histoires se déroulant dans le Coliseum, venue en faire partie le temps d'un souffle."
            "\n           Elle s'est dotée d'une armure impénétrable afin de profiter de tout ca sans se prendre la tête avec les combats."
            "\n           Nuisant a l'Equilibre Karmique, le voyageur n'est pas très apprécié par le système..."
        ),  # char
        "Féerique",  # char stigma +
        "Indigérable",  # char stigma -
        "Musculeux",  # char stigma *
        ["Attaque Légère"],  # char list technic
        ["Tir Arcanique"
        ],  # char list sorts
        {
            "Crystal Elémentaire": 10
        },  # char dict of int items
        [],  # char list
        20,  # int vie
        20,  # int mana
        1,  # int force
        1,  # int intelligence
        999999,  # int defence
        1,  # int taux coup crit
        1,  # int degat coup crit
        1,  # int taux sort crit
        1,  # int degat sort crit
        1,  # int taux esquive
        11111,  # int gold
        ["Armure de Vibranium"]  # char artefact
    ],
    "Ahti": [  # char
        "Ahti",
        (
            "L'homme d'entretien du Coliseum, une entité mystérieuse qui peut aller et venir a sa guise dans la batisse."
            "\n           Son sang froid légendaire, sa sagesse infinie, et son fidèle walkman ne servent qu'un seul maitre :"
            "\n           La propreté."
        ),  # char
        "Esprit bien rangé, esprit libéré",  # char stigma +
        "Trouble Obsessionnel Compulsif",  # char stigma -
        "Scripte",  # char stigma *
        ["Attaque Légère"],  # char list technic
        [],  # char list sorts
        {
            "Bombe Explosive" : 10,
            "Gourde de Poison" : 10,
            "Mutagène Bleu" : 10,
            "Mutagène Rouge" : 10,
            "Mutagène Vert" : 10,
            "Mutagène Doré" : 3,
        },  # char dict of int items
        [],  # char list
        30,  # int vie
        60,  # int mana
        2,  # int force
        7,  # int intelligence
        2,  # int defence
        7,  # int taux coup crit
        2,  # int degat coup crit
        7,  # int taux sort crit
        7,  # int degat sort crit
        0,  # int taux esquive
        25,  # int gold
        ["Walkman v.777"]  # char artefact
    ],
    "Alex": [  # char
        "Alex",
        (
            "Individu non binaire remplacant Philippidès après sa dernière course entre Athènes et Sparte."
            "\n           Iel est rentré dans le Coliseum pour s'abriter de la pluie,"
            "\n           et cherche à en sortir le plus vite possible pour apporter un message urgent."
        ),  # char
        "Second Souffle",  # char stigma +
        "Fatigue Chronique",  # char stigma -
        "Aucun",  # char stigma *
        ["Attaque Légère", "Poing Renforcé"],  # char list technic
        [],  # char list sorts
        {
            "Remède" : 10,
            "Pillule" : 10
        },  # char dict of int items
        [],  # char list
        40,  # int vie
        10,  # int mana
        6,  # int force
        2,  # int intelligence
        3,  # int defence
        10,  # int taux coup crit
        10,  # int degat coup crit
        0,  # int taux sort crit
        0,  # int degat sort crit
        10,  # int taux esquive
        0,  # int gold
        ["Message Scellé"]  # char artefact
    ],
    "Terrance": [  # char
        "Terrance",
        (
            "Un Chef Cuisinier gras et glouton qui peut transformer le gout des aliments en mana pur."
            "\n           Venu chercher de nouveaux ingrédients : la viande de monstre."
        ),  # char
        "Recharge Rapide",  # char stigma +
        "Pause Repas",  # char stigma -
        "Démanteleur",  # char stigma *
        ["Attaque Légère"],  # char list technic
        ["Thermosphère Chaude", "Pic Bleu"],  # char list sorts
        {
            "Remède" : 5,
            "Gourde de Poison" : 5,
        },  # char dict of int items
        ["Pharmacodynamisme"],  # char list
        45,  # int vie
        45,  # int mana
        0,  # int force
        1,  # int intelligence
        0,  # int defence
        0,  # int taux coup crit
        0,  # int degat coup crit
        0,  # int taux sort crit
        0,  # int degat sort crit
        0,  # int taux esquive
        100,  # int gold
        []  # char artefact
    ],
    "Cassandra": [  # char
        "Cassandra",
        (
            "Cassandra Jekyll est une chercheuse en transhumanisme qui a hérité de son pere"
            "\nl'incontrollable faculté de se transformer en la plus méchante partie d'elle meme :"
            "\nMiss Hyde."
            "\n           Cherche un antidote au soluté que son père s'est injecté, source de"
            "\n           tout ses problèmes."
        ),  # char
        "Transhumanisme",  # char stigma +
        "Miss Hyde",  # char stigma -
        "Aucun",  # char stigma *
        ["Attaque Légère","Corne Argile"],  # char list technic
        ["Dance Volevie"],  # char list sorts
        {
            "Bombe Explosive" : 10,
            "Gourde de Poison" : 10,
            "Mutagène Bleu" : 10,
            "Mutagène Rouge" : 10,
            "Mutagène Vert" : 10,
            "Mutagène Doré" : 3,
        },  # char dict of int items
        [],  # char list
        20,  # int vie
        20,  # int mana
        5,  # int force
        5,  # int intelligence
        6,  # int defence
        51,  # int taux coup crit
        0,  # int degat coup crit
        0,  # int taux sort crit
        15,  # int degat sort crit
        11,  # int taux esquive
        0,  # int gold
        []  # char artefact
    ],
    "Neil": [  # char
        "Neil",
        (
            "Une experience non terminée, oubliée dans sa capsule après la chute des Dieux qui travaillaient dessus."
            "\n           Ne cherche qu'une seule chose : le bohneur."
        ),  # char
        "Aucun",  # char stigma +
        "Aucun",  # char stigma -
        "Aucun",  # char stigma *
        ["Attaque Légère"],  # char list technic
        [],  # char list sorts
        {
            "Pillule" : 10,
            "Mutagène Bleu" : 3,
            "Mutagène Rouge" : 3,
            "Mutagène Vert" : 3,
            "Mutagène Doré" : 1,
        },  # char dict of int items
        [],  # char list
        40,  # int vie
        10,  # int mana
        6,  # int force
        1,  # int intelligence
        2,  # int defence
        0,  # int taux coup crit
        8,  # int degat coup crit
        0,  # int taux sort crit
        5,  # int degat sort crit
        4,  # int taux esquive
        0,  # int gold
        []  # char artefact
    ],
}


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
