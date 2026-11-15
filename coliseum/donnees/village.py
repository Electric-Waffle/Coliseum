"""Données du village : matériaux, rumeurs, recettes de fusion et prix des améliorations permanentes."""

MATERIAUXRANG1 = [
    "Coeur Gravitaire",
    "Ectoplasme Chaud",
    "Poussière Animée",
    "Ether Non-Newtonien",
    "Eclat de Verre",
]


MATERIAUXRANG2 = [
    "Fluide Alien",
    "Morceau de Cloche",
    "Ecaille de Phénix",
    "Roche Glycérine",
    "Poil Gelé",
]


MATERIAUXRANG3 = [
    "Moustache de Chat", 
    "Fragment Osseux",
    "Iris du Malheur",
    "Velour de Cervidé",
    "Composants Electroniques", 
]


MATERIAUXRANG4 = [
    "Eclat de Crystal",
    "Pilules de Roulette",
    "Fragment de Jade",
    "Poussière Dorée Animée",
    "Gemme Bleue",
]


MATERIAUXRANG5 = [
    "Essence de Vitalitée",
    "Essence de Magie",
    "Essence de Fortitude",
    "Essence de Sagesse",
    "Essence de Résistance",
]


MATERIAUXRANG6 = [
    "Fragment Mélioratif",
    "Fragment Sophiste",
    "Fragment de Fatalité",
    "Fragment Insatiable", 
]


MATERIAUXRANG7 = [
    "Essence Dorée",
    "Essence Astrale",
    "Essence Carmine",
    "Hors Stock",

    "Clochette",
    "Oeuf de Fabergé",
    "Néphrite Brut",
    "Nitroglycérine",
    "Feu Grégorien",
    "Perle de Chance",
    "Réceptacle Anastral",
    "Orbe Convergeant",
    "Gemme Prismatique",
    "Fluide Nutritif",
    "Ecaille Chitineuse",
    "Antenne de Cérémonie",
    "Circuit Biomécanique",
    "Encre de Pouvoir",
    "Tissu Perceptif",
    "Ichor Divin"
]


LISTERUMEURS = [
    "ACE, la magie utilisée pour faire venir la nuit, voudrait dire *Arbitrary Code Execution*.",
    "Le maitre des artefacts situé dans le quartier commercial possèderait tout les artefacts du Coliseumn qu'il aurait réussi a emmener avec lui aux champs du Crépuscules a sa mort. Tant qu'il ne les redonne pas a celui qui livre les objets aux nouveaux aventuriers, personne ne peut les avoir dans les boites a artefact.",
    "Un homme passerait son temps à observer la lune, quelque part dans les champs a l'ouest le soir. Et la clé pour comprendre quels objets fusionner dans le fabricateur se trouverait dans ses histoires.",
    "Il existe une bibliothèque au 8eme étage qui contient toute sortes d'informations, y compris la manière de pécher dans les trous au sol !",
    "Les redcoins, on peut en avoir en pêchant ! Mais c'est très très dur apparemment...",
    "On gagne une essence pour chaque paquet de 25 points de force ou intelligence qu'on avait a notre mort.",
    "On gagne une essence pour chaque paquet de 15 points de défence qu'on avait a notre mort.",
    "On gagne une essence pour chaque paquet de 10 âmes absorbées qu'on avait a notre mort.",
    "On gagne une essence pour chaque paquet de 25 points de vie max ou mana max qu'on avait a notre mort.",
    "Les artefacts qui augmentent les caractéristiques donnent des Fragments Mélioratifs a notre mort.",
    "Les artefacts qui changent les mécaniques de combat donnent des Fragments Sophistes a notre mort.",
    "Un certain monstre qui prend l'apparence d'un coffre lache des Fragments Insatiable a sa mort.",
    "On ne peut échanger des materiaux obtenus a un étage que contre des materiaux du même étage a la Banque.",
    "Certaines personnes ont vu une salle étrange dans le Coliseum, avec une bête figée en son milieu. Ces personnes parlent aussi d'un monstre deux étages plus fort possédant une Carte de même forme que les machines devant la Bête.",
    "On peut obtenir un artefact extrêmement utile en secouant les arbres méchaniques des méchanismes anciens. Seul bémol : l'artefact se brise en changeant d'étage.",
    "Acheter plein de certificats vendu par la machine d'un des méchanismes anciens permet de garder les artefacts temporaire vendus par la machine pendant très longtemps. ",
    "Re-observer une salle avec des bols permet de faire apparaitre plus de bols, sans aucune limite. Pratique si vous voulez perdre votre argent !",
    "Il existe une très faible chance de récuperer tout l'argent jeté dans l'oasis du troisieme étage, lorsque l'on jette son argent dedans.",
    "Utiliser l'artefact Larmes de Vénus dans le puit du 6eme étage fait complètement changer l'ambiance du 7eme étage.",
    "Le deuxieme étage contient un artefact qui peut aider les aventuriers orientés Force ou les aventuriers orientés Magie, selon si vous avez changé son ambiance avec le puit du premier étage, ou pas.\nCette logique s'applique a tout les étages qui peuvent changer de propriétaire, et force les aventuriers a réflechir avant d'agir : quel artefact leur est le plus utile selon leurs charactéristiques ? Cela vaut il le coup de chnager l'étage ou pas ?",
    "Il y existe un lien entre le piano de la salle du théatre du 5eme étage et le clavecin de la salle du puit du 4eme étage. L'un fait de la musique sans corde, l'autre a des cordes mais ne fait aucun son. Si seulement on pouvait jouer la musique du piano sur le clavecin...",
    "La salle à artefact du quatrieme étage contient une énigme assez complexe. Mais il faudrait apparemment faire attention aux nombres, qui signifieraient des positions de salles spécifiques à observer dans un ordre spécifique.",
    "Les chercheurs d'artefacts se servant des positions des salles oublient souvent que l'arene prend un carré de 3x3 au centre de la carte. Par exemple : la première salle a droite de l'arène n'est pas aux coordonnées x=1 y=0, mais x=2 y=0.",
    "On peut rencontrer 4 couleurs de brazier differents dans les salles : bleu vert rouge ou noir. Il y a 3 artefacts que l'on peut obtenir en sacrifiant un gros nombre du bon item au brazier noir, et l'un de ces items sacrifiables est le fruit jindagee.",
    "Sacrifier un item dans le brazier vert permet d'augmenter une de ses caractéristiques, en référence avec l'item sacrifié.",
    "Sacrifier un item dans le brazier rouge permet d'en avoir un autre de manière aléatoire. Sacrifiez le dans le brazier bleu, et vous aurez la version améliorée de cet item.", # moitié des rumeurs
    "Il y à un Tout-Premier qui passe son temps a observer la lune dans la décharge à l'Ouest.\nApparemment, il avait trouvé toute les recettes du fabricateur et les auraient mises de manière cryptique, dans des histoires comme moyen mémo-technique, afin de s'en rapeller.",
    "Si il y a un monstre dopé a un étage, alors il y a aussi une salle étrange dans laquelle une bête féroce dort.\nLa corrélation entre les deux est incertaines, mais ce qui est sur, c'est que la bête n'est pas assez forte pour battre le boss toute seule.",
    "Certaines personnes auraient vu des symboles étranges sur le livre de la cigogne bleue au premier étage.\nElles sont sorties pour voir si elles étaient dans la bonne salle, et quand elles sont re-rentrées, les symboles avaient disparus.\nEt si on rentrait et sortait de la salle jusqu'à voir les symboles ?",
    "Il y aurait un aventurier qui a vu une baleine dans l'oasis du troisième étage.\nEt alors qu'il jetait des pièces dedans, il a eu la meilleure chance possible dans ses gains !",
    "Un aventurier prometteur aurait disparu au deuxieme étage.\nLorsque des gens ont demandé au majordome qui prend les commandes et les emmene au premier étage ce qui s'était passé, il a simplement répondu qu'il est allé étancher sa soif a la fontaine alors qu'il était a l'article de la mort, et sans magie.",
    "Apparemment, si on arrive a augmenter le rang de son gain à ??? , a l'oasis du troisieme étage, quelque chose de terrifiant se passe.\nTellement terrifiant, que la seule aventuriere a avoir tenté l'experience a fuit l'étage sans se retourner.",
    "La pierre philosophale, Magnum Opus de tout les alchimistes, ne se trouve pas au quatrieme étage.\nLa bas, il n'y a qu'une prototype qui peut transformer un aventurier en or si il touche la pierre trop longtemps.\nCa doit être bizarre de se tranformer en or...",
    "La tour d'horloge du cinquième étage est coincée sur un nombre particulier. Tous s'accordent a dire qu'il a une signification, mais personne ne sait oû quelqu'un pourrait utiliser ce nombre secret.",
    "La quête de rang S de l'automate du sixieme étage est tellement dure que personne ne l'a jamais réussie.\nMais d'apres lui, c'est une bonne chose, car il ne pourrait plus la donner si quelqu'un la réussissait.",
    "Il existe un livre a l'étage sept qui permet d'oublier des technique en échange de caractéristiques.\nMais si on oublie un groupe de certaines caractéristiques, on gagne des effets supplémentaires.\nCes groupes seraient indiqués sur la page du livre par des symboles similaires...",
    "Seul les plus curieux arriveront a trouver la bibliothèque personnelle du Maitre Mage à l'étage huit.\nParmis la tonne d'information qui y est contenue, un nom particulier y revient deux fois, gravé dans le cuir : Jean. Ces deux livres sont : Naissance du Monde et Comprendre la Noosphère.\n Peut etre que ce Jean y aurait laissé un message codé déchiffrable seulement avec les informations de ces deux livres ?",
    "Il existe une personne qui revient souvent dans le Coliseum, pour l'entretenir.\nCe qui est impressionant, c'est qu'il est le seul a pouvoir retenir des informations qu'il arrive à glaner sur les monstres, en pleine bataille.\nSi tout le monde notent les informations des salles ou des objets qu'ils utilisent, celui là est le seul a pouvoir noter des informations sur les monstres.\nDommage qu'on ne puisse pas extraire ces informations dans un livre pour les garder quelque part...",
    "Le Brasier Noir accepte les fruits aatma, les fruits jindagee, et les crystaux élémentaires.\nMais pour qu'il donne un artefact en échange, il faut sacrifier un bon nombre de ces objets là.",
    "Les Méchanismes Anciens sont enfaite des machines avec lesquelles les Dieux et Déesse experimentaient, pour voir les différentes applications que leurs pouvoirs divins pourraient avoir.\nUtilisés par des humains, les machines ont tendance a avoir des effets négatifs.\nMais si on pouvait prouver à ces machines que nous somme des Dieux, ces effets pourraient bien disparaitre...",
    "Les marchand du quartier commercial ont pour ordre de ne pas vendre leurs plus précieux produits, car ils pourraient être perdus si l'aventurier sponsorisé mourrait avant le troisieme étage.\nCepandant, il peuvent prodiguer ces services aux détenteurs d'un Emblème de la Fin, un emblème porté par les Tout-Premiers et qui confère une authorité sans faille.",
    "Il existe 4 livres de la Cigogne.\nLa Cigogne Rouge du 8ème étage absorbe les sorts.\nLa Cigogne Bleue du 1er étage permet d'apprendre les sorts absorbés par la Cigogne Rouge, et peut donner certains artefacts spéciaux.\nLa Cigogne Noire du 7ème étage permet d'oublier les sorts et techniques en échange de plus de pouvoir.\nLa Cigogne Blanche est un glossaire qui se lierait a un individu et écrirait ses pensées a chaque fois qu'il se synchronise avec lui, cepandant ce livre a été perdu quelque part dans les Champs du Crépuscule.",
    "Les mimiques sont des monstres surpuissants qui utilisent les sorts et techniques de tout les montres de leur étage.\nElle seraient enfaite des dieux cupides nés des prières de plusieurs cultes dans le Coliseum, auquel aurait été donné un corps composé des cadavres des monstres cousus a un coffre d'artefact.",
    "Des fresques apparaissent dans le Coliseum, parce que quelque chose veut que l'on connaisse les évenements qui ont donné naissance au donjon maudit.\nSi quelqu'un les regarde toute, il pourrait etre récompensé.",
    "De mystérieux obélisques a écran tactile se sont implantés dans certaines salles.\nC'est par eux que le marchand peut avoir tout les objets qu'il vend, et il peut donner des tokens a utiliser là bas si l'on dépense plein de golds en une seule fois dans son magasin.",
    "La Chamane dans le Temple au Sud ne serait pas une Tout-Première, mais un avatar créé par les supplications des Tout-Premier quand ils sont arrivé ici.\nElle possederait ainsi l'entiereté des malédictions et de la misère de celles et ceux qui l'ont priée, mais aussi les bénédictions nées du bohneur des gens qui ont trouvé une nouvelle vie dans les Champs du Crépuscule.",
    "Le Maitre Mage ne serait pas un véritable Maitre, ni un véritable Mage.\nD'après les Tout-Premiers, l'appelation Mage pour les sorciers de haut niveaux ou même Maitre pour les plus grands de leur domaine n'est apparue qu'après la naissance de l'individu.\nEnfaite, Maitre Mage, c'est juste son nom et son prénom, et son apétance a la magie est telle, que l'on a utilisé son identité comme un adjectif.",
    "Le Roi Déchu n'est pas intrinsèquement paranoïaque et sociopathe.\nC'était une ordure, mais il est devenu fou soudainement, après une manifestation des paysans contre lui.",
    "Après le jour ou il s'est jeté dans le Coliseum, plus personne n'a entendu parler de la femme du Roi : la Reine.\nLe bruit court qu'elle aurait été fait prisonniere dans une cage du 7eme étage, mais on ne trouve la bas que des barreaux défoncés et le livre de la Cigogne Noire.",
    "Le Marchand du Coliseum serait le fils de la Reine.\nCertains disent que son visage est déformé a cause de la concentration de mana, d'autre pense que la Reine a été battue quand elle était en période de grossesse, mais tout les Tout-Premiers s'accordent sur une chose :\nLe chiffon sale sur lequel sont disposé ses produit porte l'embleme du Royaume du Roi Déchu, et n'a pu appartenir qu'à la Reine.",
    ]


LISTERECETTES = [
    "...le signal des messes, et l'or dans son état primitif...",
    "...la fenetre d'une âme de malchance, et l'éclat d'une promesse : celle de devenir meilleur...",
    "...un bout du fils et un bout du père, unis dans le vert de la jalousie et le blanc de la puretée...",
    "...celui qui ne suit pas les règles de la physique et son compagnon au tempérament explosif...",
    "...la chaleur qui venait d'ailleurs, la couleur dans laquelle finiront par baigner nos coeurs...",
    "...petite bille, réceptacle de nos peines et bohneurs, objet de notre contemplation, animée par un éclat arraché au destin par des mains suppliantes...",
    "...une volontée prise dans la roche, a laquelle on donne le pouvoir de conception des ames artificielles...",
    "...autour du coeur orbite la magie et l'émerveillement...",
    "...ordonné et non-ordonné, silice et maille, fait par l'homme et fait par la nature : un prisme de ce qui est possible...",
    "...un reflet de nos vie, venu d'ailleurs, déformé par l'espace, mais quand même porteur des mêmes énergies qui nous font se mouvoir...",
    "...pourquoi protéger ce qui revient a la vie , si ce n'est pour renforcer une idée de *résister a la mort*...",
    "...ils atterissent tout le temps sur le sol, du même coté, comme guidés par des petites antennes sur leurs levres, ou peut être la connaissance de la position du sol...",
    "...ils mangent, ils avalent, ils engloutissent, comme des animaux programmés a la naissance pour la satisfaction a l'excès : electroniquement imparfaits...",
    "...on reconnait à la force du lion, la douceur de son poil. Pourquoi donc la nature mélange autant de contradictions....",
    "...quand on les entend parler pour rien dire, faisant des illogismes a chaque tournure de phrase, amenant la logique dans des coins obscurs ou elle se fait confondre par de grossières erreurs, l'homme avisé entendra le brâme d'un animal sans capacité de raisonnement...",
    "...pourquoi donc les dieux aimeraient-ils le doré si il coule dans leurs veines, comme mué, animé, par la force de leur lignée et les défauts de leurs personnalitées ? Le sang me parait, pour de tels êtres, un materiau bien plus précieux...",
]


DICTIONNAIREMATERIAUFUSION = {
    "Clochette" : ["Morceau de Cloche","Essence Dorée"],
    "Oeuf de Fabergé" : ["Iris du Malheur","Fragment Mélioratif"],
    "Néphrite Brut" : ["Fragment de Jade","Fragment Osseux"],
    "Nitroglycérine" : ["Ether Non-Newtonien","Roche Glycérine"],
    "Feu Grégorien" : ["Ectoplasme Chaud","Gemme Bleue"],
    "Perle de Chance" : ["Pilules de Roulette","Fragment de Fatalité"],
    "Réceptacle Anastral" : ["Essence Astrale","Poussière Animée"],
    "Orbe Convergeant" : ["Coeur Gravitaire","Essence de Magie"],
    "Gemme Prismatique" : ["Eclat de Verre","Eclat de Crystal"],
    "Fluide Nutritif" : ["Fluide Alien","Essence de Vitalitée"],
    "Ecaille Chitineuse" : ["Ecaille de Phénix","Essence de Résistance"],
    "Antenne de Cérémonie" : ["Moustache de Chat","Essence de Sagesse"],
    "Circuit Biomécanique" : ["Fragment Insatiable","Composants Electroniques"],
    "Encre de Pouvoir" : ["Poil Gelé","Essence de Fortitude"],
    "Tissu Perceptif" : ["Velour de Cervidé","Fragment Sophiste"],
    "Ichor Divin" : ["Poussière Dorée Animée","Essence Carmine"]
}


ANNUAIREPRIXVILLAGE = {

    # forgeron

    "Chapeau": [
        {  # Niveau 1
            "Eclat de Verre": 4,  # Rang 1
            "Poussière Animée": 2,  # Rang 1
        },
        {  # Niveau 2
            "Fluide Alien": 3,  # Rang 2
            "Ectoplasme Chaud": 2,  # Rang 1
        },
        {  # Niveau 3
            "Ecaille de Phénix": 4,  # Rang 2
            "Coeur Gravitaire": 3,  # Rang 1
        },
        {  # Niveau 4
            "Fragment Osseux": 3,  # Rang 3
            "Velour de Cervidé": 2,  # Rang 3
            "Ether Non-Newtonien": 2,  # Rang 1
        },
        {  # Niveau 5
            "Iris du Malheur": 3,  # Rang 3
            "Poil Gelé": 3,  # Rang 2
            "Poussière Animée": 1,  # Rang 1
        },
        {  # Niveau 6
            "Fragment de Jade": 2,  # Rang 4
            "Gemme Bleue": 1,  # Rang 4
            "Moustache de Chat": 2,  # Rang 3
        },
        {  # Niveau 7
            "Poussière Dorée Animée": 2,  # Rang 4
            "Roche Glycérine": 2,  # Rang 2
            "Fragment Osseux": 3,  # Rang 3
        },
        {  # Niveau 8
            "Essence de Magie": 5,  # Rang 5
            "Fragment de Jade": 5,  # Rang 4
        },
        {  # Niveau 9
            "Essence de Fortitude": 8,  # Rang 5
            "Pilules de Roulette": 6,  # Rang 4
        },
        {  # Niveau 10
            "Emblème de la Fin": 1,
            "Fragment Sophiste": 3,  # Rang 6
            "Essence de Sagesse": 4,  # Rang 5
        },
        {  # Niveau 11
            "Fragment Insatiable": 5,  # Rang 6
            "Essence de Résistance": 6,  # Rang 5
        },
        {  # Niveau 12
            "Circuit Biomécanique": 4,  # Rang 7
            "Encre de Pouvoir": 5,  # Rang 7
        },
        {  # Niveau 13
            "Ichor Divin": 7,  # Rang 7
            "Gemme Prismatique": 7,  # Rang 7
            "Essence Astrale": 7,  # Rang 7
        },
    ],

    "Boucles d'Oreille": [  # taux sort critique
        {  # Niveau 1
            "Morceau de Cloche": 2,  # Rang 2
            "Fluide Alien": 3,       # Rang 2
            "Ether Non-Newtonien": 5,  # Rang 1
        },
        {  # Niveau 2
            "Morceau de Cloche": 5,  # Rang 2
            "Iris du Malheur": 2,    # Rang 3
            "Ecaille de Phénix": 6,  # Rang 2
        },
        {  # Niveau 3
            "Composants Electroniques": 3,  # Rang 3
            "Poil Gelé": 4,                 # Rang 2
            "Ectoplasme Chaud": 2,          # Rang 1
        },
        {  # Niveau 4
            "Fragment Osseux": 4,      # Rang 3
            "Velour de Cervidé": 2,    # Rang 3
            "Poussière Animée": 3,     # Rang 1
        },
        {  # Niveau 5
            "Eclat de Crystal": 3,        # Rang 4
            "Fragment de Jade": 2,        # Rang 4
            "Moustache de Chat": 2,       # Rang 3
        },
        {  # Niveau 6
            "Poussière Dorée Animée": 2,  # Rang 4
            "Fluide Alien": 3,            # Rang 2
            "Coeur Gravitaire": 2,        # Rang 1
        },
        {  # Niveau 7
            "Essence de Vitalitée": 1,    # Rang 5
            "Essence de Magie": 1,        # Rang 5
            "Gemme Bleue": 1,             # Rang 4
        },
        {  # Niveau 8
            "Essence de Fortitude": 2,     # Rang 5
            "Pilules de Roulette": 2,      # Rang 4
            "Poil Gelé": 2,                # Rang 2
        },
        {  # Niveau 9
            "Fragment Mélioratif": 2,      # Rang 6
            "Essence de Résistance": 1,    # Rang 5
        },
        {  # Niveau 10
            "Emblème de la Fin": 1,
            "Fragment Sophiste": 2,        # Rang 6
            "Essence de Sagesse": 1,       # Rang 5
            "Velour de Cervidé": 1,        # Rang 3
        },
        {  # Niveau 11
            "Essence Astrale": 1,              # Rang 7
            "Clochette": 1,                    # Rang 7
            "Circuit Biomécanique": 1,         # Rang 7
        },
        {  # Niveau 12
            "Perle de Chance": 2,              # Rang 7
            "Tissu Perceptif": 5,              # Rang 7
            "Essence Carmine": 3,              # Rang 7
        },
        {  # Niveau 13
            "Ichor Divin": 7,                  # Rang 7
            "Encre de Pouvoir": 3,             # Rang 7
            "Orbe Convergeant": 7,             # Rang 7
        },
    ],

    "Collier": [  # taux coup critique
        {  # Niveau 1
            "Morceau de Cloche": 2,           # Rang 2
            "Eclat de Verre": 4,              # Rang 1
            "Coeur Gravitaire": 5,            # Rang 1
        },
        {  # Niveau 2
            "Morceau de Cloche": 6,           # Rang 2
            "Ether Non-Newtonien": 4,         # Rang 1
            "Poil Gelé": 5,                   # Rang 2
        },
        {  # Niveau 3
            "Ecaille de Phénix": 4,           # Rang 2
            "Ectoplasme Chaud": 3,            # Rang 1
            "Fluide Alien": 3,                # Rang 2
        },
        {  # Niveau 4
            "Iris du Malheur": 2,             # Rang 3
            "Composants Electroniques": 2,    # Rang 3
            "Eclat de Verre": 2,              # Rang 1
        },
        {  # Niveau 5
            "Velour de Cervidé": 3,           # Rang 3
            "Fragment Osseux": 2,             # Rang 3
            "Roche Glycérine": 2,             # Rang 2
        },
        {  # Niveau 6
            "Fragment de Jade": 2,            # Rang 4
            "Poussière Dorée Animée": 2,      # Rang 4
            "Poil Gelé": 2,                   # Rang 2
        },
        {  # Niveau 7
            "Eclat de Crystal": 3,            # Rang 4
            "Moustache de Chat": 5,           # Rang 3
            "Ether Non-Newtonien": 5,         # Rang 1
        },
        {  # Niveau 8
            "Essence de Magie": 6,            # Rang 5
            "Fragment de Jade": 4,            # Rang 4
            "Ectoplasme Chaud": 10,            # Rang 1
        },
        {  # Niveau 9
            "Essence de Sagesse": 3,          # Rang 5
            "Gemme Bleue": 8,                 # Rang 4
            "Composants Electroniques": 2,    # Rang 3
        },
        {  # Niveau 10
            "Emblème de la Fin": 1,
            "Fragment Mélioratif": 4,         # Rang 6
            "Essence de Fortitude": 5,        # Rang 5
            "Poussière Animée": 5,            # Rang 1
        },
        {  # Niveau 11
            "Fragment Sophiste": 6,           # Rang 6
            "Essence de Résistance": 6,       # Rang 5
            "Fluide Alien": 15,                # Rang 2
        },
        {  # Niveau 12
            "Essence Astrale": 4,             # Rang 7
            "Clochette": 5,                   # Rang 7
            "Essence de Magie": 9,            # Rang 5
        },
        {  # Niveau 13
            "Ichor Divin": 7,                 # Rang 7
            "Perle de Chance": 7,             # Rang 7
            "Orbe Convergeant": 7,            # Rang 7
        },
    ],

    "Cotte de Maille": [  # défense
        {  # Niveau 1
            "Coeur Gravitaire": 2,              # Rang 1
            "Essence de Résistance": 2,          # Rang 5
            "Poussière Animée": 5,               # Rang 1
        },
        {  # Niveau 2
            "Eclat de Verre": 8,                # Rang 1
            "Coeur Gravitaire": 1,              # Rang 1
            "Ecaille de Phénix": 3,              # Rang 2
        },
        {  # Niveau 3
            "Poil Gelé": 6,                      # Rang 2
            "Fluide Alien": 5,                   # Rang 2
            "Poussière Animée": 4,               # Rang 1
        },
        {  # Niveau 4
            "Fragment Osseux": 4,                # Rang 3
            "Velour de Cervidé": 3,              # Rang 3
            "Roche Glycérine": 4,                # Rang 2
        },
        {  # Niveau 5
            "Composants Electroniques": 3,       # Rang 3
            "Iris du Malheur": 2,                # Rang 3
            "Ectoplasme Chaud": 5,               # Rang 1
        },
        {  # Niveau 6
            "Eclat de Crystal": 3,               # Rang 4
            "Fragment de Jade": 3,               # Rang 4
            "Poil Gelé": 6,                      # Rang 2
        },
        {  # Niveau 7
            "Poussière Dorée Animée": 4,         # Rang 4
            "Fragment Osseux": 5,                # Rang 3
            "Ether Non-Newtonien": 5,            # Rang 1
        },
        {  # Niveau 8
            "Essence de Résistance": 4,          # Rang 5
            "Essence de Fortitude": 3,           # Rang 5
            "Moustache de Chat": 5,              # Rang 3
        },
        {  # Niveau 9
            "Gemme Bleue": 6,                    # Rang 4
            "Essence de Sagesse": 3,             # Rang 5
            "Composants Electroniques": 4,       # Rang 3
        },
        {  # Niveau 10
            "Emblème de la Fin": 1,
            "Fragment Mélioratif": 3,            # Rang 6
            "Essence de Résistance": 5,          # Rang 5
            "Poil Gelé": 10,                     # Rang 2
        },
        {  # Niveau 11
            "Fragment Sophiste": 5,              # Rang 6
            "Essence de Fortitude": 6,           # Rang 5
            "Ectoplasme Chaud": 12,              # Rang 1
        },
        {  # Niveau 12
            "Essence Astrale": 5,                # Rang 7
            "Circuit Biomécanique": 4,           # Rang 7
            "Essence de Résistance": 7,          # Rang 5
        },
        {  # Niveau 13
            "Ichor Divin": 7,                    # Rang 7
            "Gemme Prismatique": 7,              # Rang 7
            "Orbe Convergeant": 7,               # Rang 7
        },
    ],

    "Bracelet": [  # force
        {  # Niveau 1
            "Ectoplasme Chaud": 4,               # Rang 1
            "Poussière Animée": 5,               # Rang 1
            "Essence de Fortitude": 2,           # Rang 5
        },
        {  # Niveau 2
            "Roche Glycérine": 5,                # Rang 2
            "Ectoplasme Chaud": 2,              # Rang 1
            "Essence de Fortitude": 3,           # Rang 5
        },
        {  # Niveau 3
            "Poil Gelé": 5,                      # Rang 2
            "Fluide Alien": 5,                   # Rang 2
            "Eclat de Verre": 6,                 # Rang 1
        },
        {  # Niveau 4
            "Iris du Malheur": 3,                # Rang 3
            "Fragment Osseux": 3,                # Rang 3
            "Poussière Animée": 4,               # Rang 1
        },
        {  # Niveau 5
            "Velour de Cervidé": 3,              # Rang 3
            "Moustache de Chat": 4,              # Rang 3
            "Roche Glycérine": 4,                # Rang 2
        },
        {  # Niveau 6
            "Fragment de Jade": 3,               # Rang 4
            "Poussière Dorée Animée": 2,         # Rang 4
            "Fluide Alien": 6,                   # Rang 2
        },
        {  # Niveau 7
            "Eclat de Crystal": 3,               # Rang 4
            "Fragment Osseux": 5,                # Rang 3
            "Ectoplasme Chaud": 6,               # Rang 1
        },
        {  # Niveau 8
            "Essence de Fortitude": 4,           # Rang 5
            "Essence de Résistance": 2,          # Rang 5
            "Coeur Gravitaire": 10,              # Rang 1
        },
        {  # Niveau 9
            "Gemme Bleue": 7,                    # Rang 4
            "Fragment de Jade": 4,               # Rang 4
            "Ether Non-Newtonien": 8,            # Rang 1
        },
        {  # Niveau 10
            "Emblème de la Fin": 1,
            "Fragment Mélioratif": 3,            # Rang 6
            "Essence de Fortitude": 6,           # Rang 5
            "Roche Glycérine": 8,                # Rang 2
        },
        {  # Niveau 11
            "Fragment Sophiste": 5,              # Rang 6
            "Essence de Résistance": 6,          # Rang 5
            "Poil Gelé": 10,                     # Rang 2
        },
        {  # Niveau 12
            "Essence Carmine": 5,                # Rang 7
            "Perle de Chance": 5,                # Rang 7
            "Essence de Fortitude": 7,           # Rang 5
        },
        {  # Niveau 13
            "Ichor Divin": 7,                    # Rang 7
            "Feu Grégorien": 7,                  # Rang 7
            "Essence Astrale": 7,                # Rang 7
        },
    ],

    "Gants": [  # dégâts coup critique
        {  # Niveau 1
            "Roche Glycérine": 3,                # Rang 2
            "Poussière Animée": 8,              # Rang 1
        },
        {  # Niveau 2
            "Roche Glycérine": 7,                # Rang 2
            "Ectoplasme Chaud": 5,              # Rang 1
            "Essence de Fortitude": 2,           # Rang 5
        },
        {  # Niveau 3
            "Ecaille de Phénix": 6,              # Rang 2
            "Eclat de Verre": 5,                 # Rang 1
            "Poil Gelé": 4,                      # Rang 2
        },
        {  # Niveau 4
            "Iris du Malheur": 3,                # Rang 3
            "Moustache de Chat": 4,              # Rang 3
            "Ether Non-Newtonien": 6,            # Rang 1
        },
        {  # Niveau 5
            "Fragment Osseux": 3,                # Rang 3
            "Velour de Cervidé": 3,              # Rang 3
            "Fluide Alien": 5,                   # Rang 2
        },
        {  # Niveau 6
            "Eclat de Crystal": 3,               # Rang 4
            "Fragment de Jade": 2,               # Rang 4
            "Poussière Animée": 5,               # Rang 1
        },
        {  # Niveau 7
            "Gemme Bleue": 3,                    # Rang 4
            "Moustache de Chat": 5,              # Rang 3
            "Coeur Gravitaire": 10,              # Rang 1
        },
        {  # Niveau 8
            "Essence de Fortitude": 4,           # Rang 5
            "Composants Electroniques": 3,       # Rang 3
            "Ectoplasme Chaud": 8,               # Rang 1
        },
        {  # Niveau 9
            "Essence de Magie": 3,               # Rang 5
            "Fragment de Jade": 5,               # Rang 4
            "Poil Gelé": 5,                      # Rang 2
        },
        {  # Niveau 10
            "Emblème de la Fin": 1,
            "Fragment de Fatalité": 3,           # Rang 6
            "Essence de Fortitude": 5,           # Rang 5
            "Eclat de Verre": 10,                # Rang 1
        },
        {  # Niveau 11
            "Fragment Sophiste": 5,              # Rang 6
            "Essence de Résistance": 5,          # Rang 5
            "Fluide Alien": 12,                  # Rang 2
        },
        {  # Niveau 12
            "Essence Dorée": 4,                  # Rang 7
            "Clochette": 4,                      # Rang 7
            "Essence de Magie": 7,               # Rang 5
        },
        {  # Niveau 13
            "Tissu Perceptif": 7,                # Rang 7
            "Encre de Pouvoir": 7,               # Rang 7
            "Orbe Convergeant": 7,               # Rang 7
        },
    ],

    "Anneau": [  # dégâts sort critique
        {  # Niveau 1 (total 7)
            "Ether Non-Newtonien": 4,         # Rang 1
            "Poussière Animée": 3,            # Rang 1
        },
        {  # Niveau 2 (total 7)
            "Ecaille de Phénix": 5,           # Rang 2
            "Essence de Magie": 2,            # Rang 5
        },
        {  # Niveau 3 (total 6)
            "Fluide Alien": 4,                # Rang 2
            "Eclat de Verre": 2,              # Rang 1
        },
        {  # Niveau 4
            "Moustache de Chat": 3,           # Rang 3
            "Iris du Malheur": 2,             # Rang 3
            "Ectoplasme Chaud": 3,            # Rang 1
        },
        {  # Niveau 5
            "Composants Electroniques": 4,    # Rang 3
            "Poil Gelé": 3,                   # Rang 2
            "Roche Glycérine": 3,             # Rang 2
        },
        {  # Niveau 6
            "Fragment de Jade": 3,            # Rang 4
            "Poussière Dorée Animée": 3,      # Rang 4
            "Moustache de Chat": 3,           # Rang 3
        },
        {  # Niveau 7
            "Eclat de Crystal": 4,            # Rang 4
            "Ether Non-Newtonien": 6,         # Rang 1
            "Ecaille de Phénix": 5,           # Rang 2
        },
        {  # Niveau 8
            "Essence de Magie": 5,            # Rang 5
            "Essence de Sagesse": 3,          # Rang 5
            "Fragment de Jade": 5,            # Rang 4
        },
        {  # Niveau 9
            "Gemme Bleue": 6,                 # Rang 4
            "Velour de Cervidé": 5,           # Rang 3
            "Ectoplasme Chaud": 5,            # Rang 1
        },
        {  # Niveau 10
            "Emblème de la Fin": 1,
            "Fragment Mélioratif": 4,         # Rang 6
            "Essence de Magie": 6,            # Rang 5
            "Poil Gelé": 10,                  # Rang 2
        },
        {  # Niveau 11
            "Fragment Sophiste": 6,           # Rang 6
            "Essence de Sagesse": 6,          # Rang 5
            "Ether Non-Newtonien": 10,        # Rang 1
        },
        {  # Niveau 12
            "Essence Astrale": 5,             # Rang 7
            "Clochette": 5,                   # Rang 7
            "Essence de Magie": 7,            # Rang 5
        },
        {  # Niveau 13
            "Ichor Divin": 7,                 # Rang 7
            "Gemme Prismatique": 7,           # Rang 7
            "Orbe Convergeant": 7,            # Rang 7
        },
    ],

    "Bottes": [  # taux esquive
        {  # Niveau 1 (total 6)
            "Coeur Gravitaire": 3,            # Rang 1
            "Ectoplasme Chaud": 2,            # Rang 1
            "Poussière Animée": 1,            # Rang 1
        },
        {  # Niveau 2 (total 6)
            "Essence de Vitalitée": 2,        # Rang 5
            "Essence de Fortitude": 2,        # Rang 5
            "Eclat de Verre": 2,              # Rang 1
        },
        {  # Niveau 3 (total 7)
            "Fluide Alien": 3,                # Rang 2
            "Poil Gelé": 3,                   # Rang 2
            "Ether Non-Newtonien": 1,         # Rang 1
        },
        {  # Niveau 4
            "Fragment Osseux": 3,             # Rang 3
            "Velour de Cervidé": 2,           # Rang 3
            "Ectoplasme Chaud": 3,            # Rang 1
        },
        {  # Niveau 5
            "Roche Glycérine": 4,             # Rang 2
            "Moustache de Chat": 3,           # Rang 3
            "Poussière Animée": 4,            # Rang 1
        },
        {  # Niveau 6
            "Fragment de Jade": 3,            # Rang 4
            "Gemme Bleue": 3,                 # Rang 4
            "Ether Non-Newtonien": 4,         # Rang 1
        },
        {  # Niveau 7
            "Poussière Dorée Animée": 3,      # Rang 4
            "Iris du Malheur": 3,             # Rang 3
            "Fluide Alien": 5,                # Rang 2
        },
        {  # Niveau 8
            "Essence de Vitalitée": 5,        # Rang 5
            "Essence de Résistance": 3,       # Rang 5
            "Fragment de Jade": 4,            # Rang 4
        },
        {  # Niveau 9
            "Gemme Bleue": 6,                 # Rang 4
            "Poil Gelé": 6,                   # Rang 2
            "Ectoplasme Chaud": 4,            # Rang 1
        },
        {  # Niveau 10
            "Emblème de la Fin": 1,
            "Fragment Mélioratif": 4,         # Rang 6
            "Essence de Fortitude": 6,        # Rang 5
            "Coeur Gravitaire": 10,           # Rang 1
        },
        {  # Niveau 11
            "Fragment Sophiste": 5,           # Rang 6
            "Essence de Résistance": 5,       # Rang 5
            "Poussière Animée": 12,           # Rang 1
        },
        {  # Niveau 12
            "Essence Dorée": 5,               # Rang 7
            "Perle de Chance": 5,             # Rang 7
            "Essence de Fortitude": 7,        # Rang 5
        },
        {  # Niveau 13
            "Ichor Divin": 7,                 # Rang 7
            "Feu Grégorien": 7,               # Rang 7
            "Tissu Perceptif": 7,             # Rang 7
        },
    ],


    # sorciere

    "Fiole de Sève": [  # + mana
        {  # Niveau 1 (total 6)
            "Poussière Animée": 3,            # Rang 1
            "Eclat de Verre": 2,              # Rang 1
            "Ether Non-Newtonien": 1,         # Rang 1
        },
        {  # Niveau 2 (total 6)
            "Ectoplasme Chaud": 4,            # Rang 1
            "Fluide Alien": 2,                # Rang 2
        },
        {  # Niveau 3 (total 7)
            "Ecaille de Phénix": 4,           # Rang 2
            "Poil Gelé": 3,                   # Rang 2
        },
        {  # Niveau 4
            "Iris du Malheur": 3,             # Rang 3
            "Composants Electroniques": 3,    # Rang 3
            "Eclat de Verre": 3,              # Rang 1
        },
        {  # Niveau 5
            "Velour de Cervidé": 3,           # Rang 3
            "Fluide Alien": 5,                # Rang 2
            "Ether Non-Newtonien": 4,         # Rang 1
        },
        {  # Niveau 6
            "Fragment de Jade": 3,            # Rang 4
            "Poussière Dorée Animée": 2,      # Rang 4
            "Poil Gelé": 6,                   # Rang 2
        },
        {  # Niveau 7
            "Eclat de Crystal": 3,            # Rang 4
            "Moustache de Chat": 4,           # Rang 3
            "Essence de Magie": 2,            # Rang 5
        },
        {  # Niveau 8
            "Essence de Sagesse": 5,          # Rang 5
            "Essence de Vitalitée": 4,        # Rang 5
            "Fragment de Jade": 4,            # Rang 4
        },
        {  # Niveau 9
            "Gemme Bleue": 6,                 # Rang 4
            "Velour de Cervidé": 5,           # Rang 3
            "Ectoplasme Chaud": 5,            # Rang 1
        },
        {  # Niveau 10
            "Emblème de la Fin": 1,
            "Fragment Sophiste": 3,           # Rang 6
            "Essence de Magie": 6,            # Rang 5
            "Fluide Alien": 10,               # Rang 2
        },
        {  # Niveau 11
            "Fragment Mélioratif": 5,         # Rang 6
            "Essence de Sagesse": 6,          # Rang 5
            "Poussière Animée": 12,           # Rang 1
        },
        {  # Niveau 12
            "Essence Astrale": 5,             # Rang 7
            "Clochette": 5,                   # Rang 7
            "Essence de Magie": 7,            # Rang 5
        },
        {  # Niveau 13
            "Ichor Divin": 7,                 # Rang 7
            "Orbe Convergeant": 7,            # Rang 7
            "Essence Dorée": 7,               # Rang 7
        },
    ],

    "Fiole de Rosée": [
        {  # Niveau 1 (total 6)
            "Poussière Animée": 3,           # Rang 1
            "Coeur Gravitaire": 3,           # Rang 1
        },
        {  # Niveau 2 (total 6)
            "Ectoplasme Chaud": 3,           # Rang 1
            "Fluide Alien": 3,               # Rang 2
        },
        {  # Niveau 3 (total 7)
            "Ecaille de Phénix": 4,          # Rang 2
            "Poil Gelé": 3,                  # Rang 2
        },
        {  # Niveau 4
            "Velour de Cervidé": 3,          # Rang 3
            "Iris du Malheur": 3,            # Rang 3
            "Eclat de Verre": 3,             # Rang 1
        },
        {  # Niveau 5
            "Composants Electroniques": 4,   # Rang 3
            "Moustache de Chat": 4,          # Rang 3
            "Ether Non-Newtonien": 2,        # Rang 1
        },
        {  # Niveau 6
            "Fragment de Jade": 3,           # Rang 4
            "Gemme Bleue": 2,                # Rang 4
            "Poussière Dorée Animée": 3,     # Rang 4
        },
        {  # Niveau 7
            "Eclat de Crystal": 4,           # Rang 4
            "Essence de Vitalitée": 5,       # Rang 5
            "Ectoplasme Chaud": 6,           # Rang 1
        },
        {  # Niveau 8
            "Essence de Résistance": 5,      # Rang 5
            "Poil Gelé": 6,                  # Rang 2
            "Fragment de Jade": 4,           # Rang 4
        },
        {  # Niveau 9
            "Gemme Bleue": 6,                # Rang 4
            "Velour de Cervidé": 5,          # Rang 3
            "Ether Non-Newtonien": 6,        # Rang 1
        },
        {  # Niveau 10
            "Emblème de la Fin": 1,
            "Fragment Mélioratif": 4,        # Rang 6
            "Essence de Fortitude": 6,       # Rang 5
            "Fluide Alien": 10,              # Rang 2
        },
        {  # Niveau 11
            "Fragment Sophiste": 5,          # Rang 6
            "Essence de Résistance": 5,      # Rang 5
            "Poussière Animée": 12,          # Rang 1
        },
        {  # Niveau 12
            "Essence Astrale": 5,            # Rang 7
            "Clochette": 5,                  # Rang 7
            "Essence de Vitalitée": 7,       # Rang 5
        },
        {  # Niveau 13
            "Ichor Divin": 7,                # Rang 7
            "Orbe Convergeant": 7,           # Rang 7
            "Gemme Prismatique": 7,          # Rang 7
        },
    ],

    "Tisane d'Ecorce": [
        {  # Niveau 1 (total 6)
            "Ectoplasme Chaud": 3,           # Rang 1
            "Poussière Animée": 3,           # Rang 1
        },
        {  # Niveau 2 (total 7)
            "Coeur Gravitaire": 4,           # Rang 1
            "Poil Gelé": 3,                  # Rang 2
        },
        {  # Niveau 3 (total 7)
            "Ecaille de Phénix": 3,          # Rang 2
            "Eclat de Verre": 2,             # Rang 1
            "Ether Non-Newtonien": 2,        # Rang 1
        },
        {  # Niveau 4
            "Moustache de Chat": 3,          # Rang 3
            "Iris du Malheur": 3,            # Rang 3
            "Poussière Animée": 3,           # Rang 1
        },
        {  # Niveau 5
            "Composants Electroniques": 4,   # Rang 3
            "Fluide Alien": 4,               # Rang 2
            "Roche Glycérine": 3,            # Rang 2
        },
        {  # Niveau 6
            "Fragment de Jade": 3,           # Rang 4
            "Poussière Dorée Animée": 3,     # Rang 4
            "Essence de Vitalitée": 2,       # Rang 5
        },
        {  # Niveau 7
            "Gemme Bleue": 4,                # Rang 4
            "Velour de Cervidé": 4,          # Rang 3
            "Poussière Animée": 5,           # Rang 1
        },
        {  # Niveau 8
            "Essence de Résistance": 5,      # Rang 5
            "Essence de Fortitude": 4,       # Rang 5
            "Fragment de Jade": 4,           # Rang 4
        },
        {  # Niveau 9
            "Eclat de Crystal": 6,           # Rang 4
            "Ether Non-Newtonien": 6,        # Rang 1
            "Poil Gelé": 6,                  # Rang 2
        },
        {  # Niveau 10
            "Emblème de la Fin": 1,
            "Fragment Mélioratif": 4,        # Rang 6
            "Essence de Vitalitée": 6,       # Rang 5
            "Fluide Alien": 10,              # Rang 2
        },
        {  # Niveau 11
            "Fragment Sophiste": 6,          # Rang 6
            "Essence de Fortitude": 6,       # Rang 5
            "Poussière Animée": 12,          # Rang 1
        },
        {  # Niveau 12
            "Essence Astrale": 5,            # Rang 7
            "Clochette": 5,                  # Rang 7
            "Essence de Résistance": 7,      # Rang 5
        },
        {  # Niveau 13
            "Ichor Divin": 7,                # Rang 7
            "Orbe Convergeant": 7,           # Rang 7
            "Essence Dorée": 7,              # Rang 7
        },
    ],

    "Tisane de Racine": [
        {  # Niveau 1 (total 6)
            "Ether Non-Newtonien": 3,        # Rang 1
            "Poussière Animée": 3,           # Rang 1
        },
        {  # Niveau 2 (total 6)
            "Ectoplasme Chaud": 3,           # Rang 1
            "Fluide Alien": 3,               # Rang 2
        },
        {  # Niveau 3 (total 7)
            "Ecaille de Phénix": 4,          # Rang 2
            "Eclat de Verre": 3,             # Rang 1
        },
        {  # Niveau 4
            "Poil Gelé": 3,                  # Rang 2
            "Iris du Malheur": 3,            # Rang 3
            "Composants Electroniques": 2,   # Rang 3
        },
        {  # Niveau 5
            "Roche Glycérine": 4,            # Rang 2
            "Moustache de Chat": 4,          # Rang 3
            "Poussière Animée": 3,           # Rang 1
        },
        {  # Niveau 6
            "Fragment de Jade": 3,           # Rang 4
            "Poussière Dorée Animée": 3,     # Rang 4
            "Essence de Magie": 2,           # Rang 5
        },
        {  # Niveau 7
            "Eclat de Crystal": 4,           # Rang 4
            "Velour de Cervidé": 4,          # Rang 3
            "Fluide Alien": 5,               # Rang 2
        },
        {  # Niveau 8
            "Essence de Sagesse": 5,         # Rang 5
            "Essence de Magie": 4,           # Rang 5
            "Fragment de Jade": 4,           # Rang 4
        },
        {  # Niveau 9
            "Gemme Bleue": 6,                # Rang 4
            "Ether Non-Newtonien": 6,        # Rang 1
            "Ecaille de Phénix": 5,          # Rang 2
        },
        {  # Niveau 10
            "Emblème de la Fin": 1,
            "Fragment Mélioratif": 4,        # Rang 6
            "Essence de Magie": 6,           # Rang 5
            "Poil Gelé": 10,                 # Rang 2
        },
        {  # Niveau 11
            "Fragment Sophiste": 6,          # Rang 6
            "Essence de Sagesse": 6,         # Rang 5
            "Poussière Animée": 12,          # Rang 1
        },
        {  # Niveau 12
            "Essence Astrale": 5,            # Rang 7
            "Clochette": 5,                  # Rang 7
            "Essence de Magie": 7,           # Rang 5
        },
        {  # Niveau 13
            "Ichor Divin": 7,                # Rang 7
            "Orbe Convergeant": 7,           # Rang 7
            "Gemme Prismatique": 7,          # Rang 7
        },
    ],


    "Charge de Feu": [
        {  # Niveau 1 (6 ingrédients)
            "Poussière Animée": 3,            # Rang 1
            "Ether Non-Newtonien": 3,         # Rang 1
        },
        {  # Niveau 2 (6 ingrédients)
            "Ectoplasme Chaud": 3,            # Rang 1
            "Ecaille de Phénix": 4,          # Rang 2
        },
        {  # Niveau 3 (7 ingrédients)
            "Ecaille de Phénix": 15,          # Rang 2
        },
        {  # Niveau 4
            "Iris du Malheur": 4,             # Rang 3
            "Velour de Cervidé": 3,           # Rang 3
            "Poussière Animée": 3,            # Rang 1
        },
        {  # Niveau 5
            "Roche Glycérine": 4,         # Rang 3
            "Essence de Magie": 8,            # Rang 5
        },
        {  # Niveau 6
            "Fragment de Jade": 3,            # Rang 4
            "Poussière Dorée Animée": 3,      # Rang 4
            "Essence de Fortitude": 2,        # Rang 5
        },
        {  # Niveau 7
            "Essence de Magie": 4,            # Rang 5
            "Ether Non-Newtonien": 5,         # Rang 1
        },
        {  # Niveau 8
            "Essence de Sagesse": 14,          # Rang 5
            "Fragment de Jade": 4,            # Rang 4
        },
        {  # Niveau 9
            "Eclat de Crystal": 16,            # Rang 4
            "Essence de Fortitude": 4,        # Rang 5
        },
        {  # Niveau 10
            "Emblème de la Fin": 1,
            "Fragment Mélioratif": 4,         # Rang 6
            "Essence de Magie": 6,            # Rang 5
            "Roche Glycérine": 6,         # Rang 3
        },
        {  # Niveau 11
            "Fragment Sophiste": 6,           # Rang 6
            "Essence de Sagesse": 6,          # Rang 5
            "Poussière Dorée Animée": 6,         # Rang 6
        },
        {  # Niveau 12
            "Essence Astrale": 5,             # Rang 7
            "Clochette": 5,                   # Rang 7
            "Essence de Magie": 7,            # Rang 5
        },
        {  # Niveau 13
            "Ichor Divin": 7,                 # Rang 7
            "Orbe Convergeant": 7,            # Rang 7
            "Gemme Prismatique": 7,           # Rang 7
        },
    ],

    "Charge de Glace": [
        {  # Niveau 1
            "Poussière Animée": 3,
            "Ether Non-Newtonien": 3,
        },
        {  # Niveau 2
            "Poil Gelé": 3,
            "Fluide Alien": 3,
        },
        {  # Niveau 3
            "Eclat de Verre": 13,
        },
        {  # Niveau 4
            "Iris du Malheur": 7,
            "Poussière Animée": 3,
        },
        {  # Niveau 5
            "Moustache de Chat": 4,
            "Velour de Cervidé": 4,
            "Essence de Sagesse": 2,
        },
        {  # Niveau 6
            "Fragment de Jade": 3,
            "Poussière Dorée Animée": 3,
            "Essence de Résistance": 2,
        },
        {  # Niveau 7
            "Gemme Bleue": 4,
            "Essence de Sagesse": 4,
            "Poil Gelé": 5,
        },
        {  # Niveau 8
            "Velour de Cervidé": 4,
            "Essence de Résistance": 4,
            "Essence Astrale": 5,
        },
        {  # Niveau 9
            "Eclat de Crystal": 5,
            "Fragment de Jade": 5,
            "Essence de Magie": 4,
        },
        {  # Niveau 10
            "Emblème de la Fin": 1,
            "Fragment Mélioratif": 4,
            "Essence de Résistance": 6,
            "Poil Gelé": 8,
        },
        {  # Niveau 11
            "Fragment Sophiste": 6,
            "Essence de Sagesse": 6,
            "Fluide Alien": 10,
        },
        {  # Niveau 12
            "Essence Astrale": 5,
            "Clochette": 5,
            "Essence de Résistance": 7,
        },
        {  # Niveau 13
            "Ichor Divin": 7,
            "Orbe Convergeant": 7,
            "Gemme Prismatique": 7,
        },
    ],

    "Charge de Foudre": [
        {  # Niveau 1
            "Ether Non-Newtonien": 3,
            "Poussière Animée": 3,
        },
        {  # Niveau 2
            "Coeur Gravitaire": 12,
        },
        {  # Niveau 3
            "Ecaille de Phénix": 3,
            "Eclat de Verre": 2,
            "Roche Glycérine": 2,
        },
        {  # Niveau 4
            "Iris du Malheur": 3,
            "Composants Electroniques": 4,
            "Poussière Animée": 3,
        },
        {  # Niveau 5
            "Velour de Cervidé": 4,
            "Essence de Fortitude": 13,
        },
        {  # Niveau 6
            "Fragment de Jade": 3,
            "Poussière Dorée Animée": 3,
            "Essence de Sagesse": 2,
        },
        {  # Niveau 7
            "Essence de Fortitude": 8,
            "Poil Gelé": 5,
        },
        {  # Niveau 8
            "Essence de Magie": 4,
            "Ecaille de Phénix": 5,
            "Fragment de Jade": 4,
        },
        {  # Niveau 9
            "Eclat de Crystal": 6,
            "Ether Non-Newtonien": 5,
            "Composants Electroniques": 5,
        },
        {  # Niveau 10
            "Emblème de la Fin": 1,
            "Fragment Mélioratif": 4,
            "Essence de Sagesse": 6,
            "Poil Gelé": 5,
        },
        {  # Niveau 11
            "Fragment Sophiste": 6,
            "Essence de Fortitude": 6,
            "Poussière Animée": 12,
        },
        {  # Niveau 12
            "Essence Astrale": 5,
            "Clochette": 5,
            "Essence de Sagesse": 7,
        },
        {  # Niveau 13
            "Ichor Divin": 7,
            "Orbe Convergeant": 7,
            "Gemme Prismatique": 7,
        },
    ],

    "Charge de Terre": [
        {  # Niveau 1
            "Roche Glycérine": 3,              # Rang 1
            "Poussière Animée": 3,             # Rang 1
        },
        {  # Niveau 2
            "Ectoplasme Chaud": 10,             # Rang 1
        },
        {  # Niveau 3
            "Morceau de Cloche": 3,            # Rang 2
            "Poil Gelé": 3,                    # Rang 2
        },
        {  # Niveau 4
            "Ecaille de Phénix": 4,            # Rang 3
            "Velour de Cervidé": 3,            # Rang 3
            "Fluide Alien": 2,                 # Rang 2
        },
        {  # Niveau 5
            "Fragment de Jade": 3,             # Rang 4
            "Essence de Fortitude": 2,         # Rang 5
        },
        {  # Niveau 6
            "Essence de Résistance": 3,        # Rang 5
            "Eclat de Crystal": 3,             # Rang 4
            "Poil Gelé": 4,                    # Rang 2
        },
        {  # Niveau 7
            "Roche Glycérine": 6,
            "Essence de Fortitude": 4,
            "Fragment de Jade": 4,
        },
        {  # Niveau 8
            "Essence de Magie": 4,
            "Velour de Cervidé": 4,
            "Ecaille de Phénix": 5,
        },
        {  # Niveau 9
            "Essence de Résistance": 11,
            "Poussière Animée": 6,
        },
        {  # Niveau 10
            "Emblème de la Fin": 1,
            "Fragment Mélioratif": 4,
            "Essence de Sagesse": 5,
        },
        {  # Niveau 11
            "Fragment Sophiste": 6,
            "Poil Gelé": 8,
            "Essence de Fortitude": 6,
        },
        {  # Niveau 12
            "Essence Astrale": 5,
            "Clochette": 5,
            "Essence de Magie": 7,
        },
        {  # Niveau 13
            "Ichor Divin": 7,
            "Orbe Convergeant": 7,
            "Gemme Prismatique": 7,
        },
    ],

    "Charge de Chair": [
    {  # Niveau 1
        "Ectoplasme Chaud": 3,
        "Poussière Animée": 3,
    },
    {  # Niveau 2
        "Fluide Alien": 3,
        "Poil Gelé": 3,
    },
    {  # Niveau 3
        "Essence de Fortitude": 2,
        "Roche Glycérine": 4,
    },
    {  # Niveau 4
        "Ecaille de Phénix": 4,
        "Iris du Malheur": 3,
        "Eclat de Verre": 3,
    },
    {  # Niveau 5
        "Essence de Fortitude": 3,
        "Velour de Cervidé": 3,
    },
    {  # Niveau 6
        "Roche Glycérine": 5,
        "Poil Gelé": 4,
        "Essence de Résistance": 3,
    },
    {  # Niveau 7
        "Fragment de Jade": 4,
        "Essence de Fortitude": 4,
        "Ectoplasme Chaud": 6,
    },
    {  # Niveau 8
        "Essence de Magie": 4,
        "Essence de Sagesse": 4,
    },
    {  # Niveau 9
        "Eclat de Crystal": 5,
        "Velour de Cervidé": 5,
        "Essence de Fortitude": 5,
    },
    {  # Niveau 10
        "Emblème de la Fin": 1,
        "Fragment Mélioratif": 4,
        "Essence de Résistance": 6,
        "Poil Gelé": 6,
    },
    {  # Niveau 11
        "Fragment Sophiste": 6,
        "Essence de Fortitude": 6,
        "Roche Glycérine": 8,
    },
    {  # Niveau 12
        "Essence Astrale": 5,
        "Clochette": 5,
        "Essence de Magie": 7,
    },
    {  # Niveau 13
        "Ichor Divin": 7,
        "Orbe Convergeant": 7,
        "Gemme Prismatique": 7,
    },
],

    "Charge de Sang": [
    {  # Niveau 1
        "Fluide Alien": 3,
        "Poussière Animée": 3,
    },
    {  # Niveau 2
        "Ectoplasme Chaud": 3,
        "Ether Non-Newtonien": 3,
    },
    {  # Niveau 3
        "Poil Gelé": 3,
        "Essence de Résistance": 2,
    },
    {  # Niveau 4
        "Iris du Malheur": 3,
        "Roche Glycérine": 3,
    },
    {  # Niveau 5
        "Ecaille de Phénix": 4,
        "Essence de Magie": 3,
    },
    {  # Niveau 6
        "Velour de Cervidé": 4,
        "Essence de Sagesse": 3,
        "Eclat de Verre": 4,
    },
    {  # Niveau 7
        "Fragment de Jade": 8,
        "Essence de Résistance": 4,
    },
    {  # Niveau 8
        "Essence de Fortitude": 4,
        "Poil Gelé": 5,
        "Ecaille de Phénix": 5,
    },
    {  # Niveau 9
        "Eclat de Crystal": 5,
        "Essence de Magie": 5,
    },
    {  # Niveau 10
        "Emblème de la Fin": 1,
        "Fragment Mélioratif": 4,
        "Essence de Sagesse": 15,
    },
    {  # Niveau 11
        "Fragment Sophiste": 6,
        "Essence de Fortitude": 6,
        "Roche Glycérine": 7,
    },
    {  # Niveau 12
        "Essence Astrale": 5,
        "Clochette": 5,
        "Essence de Magie": 7,
    },
    {  # Niveau 13
        "Ichor Divin": 7,
        "Orbe Convergeant": 7,
        "Gemme Prismatique": 7,
    },
],


    # herboriste

    "Ration Jindagee": [
        {  # Niveau 1
            "Eclat de Verre": 3,              # Rang 1
            "Ether Non-Newtonien": 3,         # Rang 1
            "Poil Gelé": 1,                   # Rang 2
        },
        {  # Niveau 2
            "Fluide Alien": 3,                # Rang 2
            "Poussière Animée": 3,            # Rang 1
            "Ecaille de Phénix": 2,           # Rang 2
        },
        {  # Niveau 3
            "Velour de Cervidé": 2,           # Rang 3
            "Composants Electroniques": 2,    # Rang 3
            "Iris du Malheur": 1,             # Rang 3
        },
        {  # Niveau 4
            "Gemme Bleue": 2,                 # Rang 4
            "Fragment de Jade": 2,            # Rang 4
            "Moustache de Chat": 3,           # Rang 3
        },
        {  # Niveau 5
            "Essence de Vitalitée": 3,        # Rang 5
            "Fragment Sophiste": 2,           # Rang 6
            "Poussière Animée": 4,            # Rang 1
        },
    ],
    "Ration Jindagee Raffinée": [
        {  # Niveau 1
            "Emblème de la Fin": 1,
            "Coeur Gravitaire": 3,            # Rang 1
            "Ectoplasme Chaud": 2,            # Rang 1
            "Roche Glycérine": 2,             # Rang 2
        },
        {  # Niveau 2
            "Ecaille de Phénix": 3,           # Rang 2
            "Fluide Alien": 2,                # Rang 2
            "Essence de Magie": 2,            # Rang 5
        },
        {  # Niveau 3
            "Fragment Osseux": 3,             # Rang 3
            "Velour de Cervidé": 2,           # Rang 3
            "Eclat de Crystal": 1,            # Rang 4
        },
        {  # Niveau 4
            "Poussière Dorée Animée": 3,      # Rang 4
            "Fragment Mélioratif": 2,         # Rang 6
            "Essence de Fortitude": 3,        # Rang 5
        },
        {  # Niveau 5
            "Clochette": 5,                   # Rang 7
            "Perle de Chance": 5,             # Rang 7
            "Essence de Magie": 6,            # Rang 5
        },
    ],
    "Ration Aatma": [
        {  # Niveau 1
            "Poussière Animée": 4,            # Rang 1
            "Ectoplasme Chaud": 3,            # Rang 1
        },
        {  # Niveau 2
            "Fluide Alien": 3,                # Rang 2
            "Morceau de Cloche": 2,           # Rang 2
            "Ether Non-Newtonien": 2,         # Rang 1
        },
        {  # Niveau 3
            "Fragment Osseux": 2,             # Rang 3
            "Composants Electroniques": 2,    # Rang 3
            "Poil Gelé": 3,                   # Rang 2
        },
        {  # Niveau 4
            "Gemme Bleue": 2,                 # Rang 4
            "Eclat de Crystal": 2,            # Rang 4
            "Velour de Cervidé": 3,           # Rang 3
        },
        {  # Niveau 5
            "Fragment Sophiste": 2,           # Rang 6
            "Essence de Résistance": 4,       # Rang 5
            "Poussière Animée": 5,            # Rang 1
        },
    ],

    "Ration Aatma Rafinée": [
        {  # Niveau 1
            "Emblème de la Fin": 1,
            "Ether Non-Newtonien": 3,         # Rang 1
            "Poil Gelé": 2,                   # Rang 2
            "Eclat de Verre": 2,              # Rang 1
        },
        {  # Niveau 2
            "Ecaille de Phénix": 3,           # Rang 2
            "Essence de Sagesse": 2,          # Rang 5
            "Fluide Alien": 3,                # Rang 2
        },
        {  # Niveau 3
            "Moustache de Chat": 2,           # Rang 3
            "Fragment de Jade": 2,            # Rang 4
            "Fragment Osseux": 2,             # Rang 3
        },
        {  # Niveau 4
            "Essence de Fortitude": 4,        # Rang 5
            "Poussière Dorée Animée": 3,      # Rang 4
            "Fragment de Fatalité": 2,        # Rang 6
        },
        {  # Niveau 5
            "Tissu Perceptif": 5,             # Rang 7
            "Ichor Divin": 5,                 # Rang 7
            "Essence de Magie": 6,            # Rang 5
        },
    ],
    "Ration Cristalline": [
        {  # Niveau 1
            "Eclat de Verre": 3,              # Rang 1
            "Ether Non-Newtonien": 3,         # Rang 1
            "Eclat de Crystal": 1,            # Rang 4
        },
        {  # Niveau 2
            "Eclat de Crystal": 3,            # Rang 4
            "Gemme Bleue": 2,                 # Rang 4
            "Poil Gelé": 2,                   # Rang 2
        },
        {  # Niveau 3
            "Fragment Mélioratif": 2,         # Rang 6
            "Poussière Dorée Animée": 3,      # Rang 4
            "Velour de Cervidé": 3,           # Rang 3
        },
        {  # Niveau 4
            "Emblème de la Fin": 1,
            "Essence de Sagesse": 3,          # Rang 5
            "Fragment Sophiste": 2,           # Rang 6
            "Composants Electroniques": 3,    # Rang 3
        },
        {  # Niveau 5
            "Gemme Prismatique": 5,           # Rang 7
            "Orbe Convergeant": 5,            # Rang 7
            "Essence de Magie": 6,            # Rang 5
        },
    ],
    "Ration d'Hydromel": [
        {  # Niveau 1
            "Ectoplasme Chaud": 4,            # Rang 1
            "Ether Non-Newtonien": 2,         # Rang 1
        },
        {  # Niveau 2
            "Morceau de Cloche": 3,           # Rang 2
            "Roche Glycérine": 3,             # Rang 2
            "Poussière Animée": 2,            # Rang 1
        },
        {  # Niveau 3
            "Composants Electroniques": 3,    # Rang 3
            "Iris du Malheur": 2,             # Rang 3
            "Ecaille de Phénix": 3,           # Rang 2
        },
        {  # Niveau 4
            "Fragment de Jade": 3,            # Rang 4
            "Poussière Dorée Animée": 2,      # Rang 4
            "Essence de Fortitude": 3,        # Rang 5
        },
        {  # Niveau 5
            "Encre de Pouvoir": 5,            # Rang 7
            "Circuit Biomécanique": 5,        # Rang 7
            "Essence de Vitalitée": 6,        # Rang 5
        },
    ],
    "Ration Ambroisie": [
        {  # Niveau 1
            "Ether Non-Newtonien": 3,         # Rang 1
            "Ectoplasme Chaud": 3,            # Rang 1
            "Eclat de Verre": 2,              # Rang 1
        },
        {  # Niveau 2
            "Fluide Alien": 3,                # Rang 2
            "Ecaille de Phénix": 2,           # Rang 2
            "Essence de Sagesse": 2,          # Rang 5
        },
        {  # Niveau 3
            "Velour de Cervidé": 3,           # Rang 3
            "Fragment Osseux": 2,             # Rang 3
            "Fragment de Jade": 2,            # Rang 4
        },
        {  # Niveau 4
            "Essence de Magie": 4,            # Rang 5
            "Fragment Mélioratif": 2,         # Rang 6
            "Poil Gelé": 4,                   # Rang 2
        },
        {  # Niveau 5
            "Ichor Divin": 5,                 # Rang 7
            "Réceptacle Anastral": 5,         # Rang 7
            "Essence de Sagesse": 6,          # Rang 5
        },
    ],
    "Ration Explosive": [
        {  # Niveau 1
            "Poussière Animée": 3,              # Rang 1
            "Eclat de Verre": 2,                # Rang 1
            "Poil Gelé": 2,                     # Rang 2
        },
        {  # Niveau 2
            "Fluide Alien": 3,                  # Rang 2
            "Ecaille de Phénix": 3,             # Rang 2
            "Ether Non-Newtonien": 1,           # Rang 1
        },
        {  # Niveau 3
            "Fragment Osseux": 3,               # Rang 3
            "Velour de Cervidé": 2,             # Rang 3
            "Composants Electroniques": 2,      # Rang 3
        },
        {  # Niveau 4
            "Fragment de Jade": 3,              # Rang 4
            "Poussière Dorée Animée": 2,        # Rang 4
            "Essence de Fortitude": 2,          # Rang 5
        },
        {  # Niveau 5
            "Fragment Sophiste": 2,             # Rang 6
            "Essence de Résistance": 4,         # Rang 5
            "Perle de Chance": 5,               # Rang 7
        },
    ],
    "Ration Explosive Raffinée": [
        {  # Niveau 1
            "Emblème de la Fin": 1,
            "Ether Non-Newtonien": 3,           # Rang 1
            "Coeur Gravitaire": 3,              # Rang 1
            "Roche Glycérine": 1,               # Rang 2
        },
        {  # Niveau 2
            "Fluide Alien": 2,                  # Rang 2
            "Morceau de Cloche": 2,             # Rang 2
            "Ecaille de Phénix": 2,             # Rang 2
        },
        {  # Niveau 3
            "Fragment Osseux": 2,               # Rang 3
            "Composants Electroniques": 2,      # Rang 3
            "Iris du Malheur": 2,               # Rang 3
        },
        {  # Niveau 4
            "Fragment de Fatalité": 2,          # Rang 6
            "Poussière Dorée Animée": 3,        # Rang 4
            "Essence de Magie": 2,              # Rang 5
        },
        {  # Niveau 5
            "Encre de Pouvoir": 5,              # Rang 7
            "Tissu Perceptif": 5,               # Rang 7
            "Essence de Fortitude": 4,          # Rang 5
        },
    ],
    "Pack de Fléchettes": [
        {  # Niveau 1
            "Ether Non-Newtonien": 2,           # Rang 1
            "Poussière Animée": 3,              # Rang 1
            "Eclat de Verre": 2,                # Rang 1
        },
        {  # Niveau 2
            "Morceau de Cloche": 3,             # Rang 2
            "Poil Gelé": 2,                     # Rang 2
            "Roche Glycérine": 2,               # Rang 2
        },
        {  # Niveau 3
            "Velour de Cervidé": 2,             # Rang 3
            "Composants Electroniques": 2,      # Rang 3
            "Ecaille de Phénix": 3,             # Rang 2
        },
        {  # Niveau 4
            "Essence de Vitalitée": 3,          # Rang 5
            "Fragment Mélioratif": 2,           # Rang 6
            "Gemme Bleue": 2,                   # Rang 4
        },
        {  # Niveau 5
            "Ichor Divin": 5,                   # Rang 7
            "Clochette": 5,                     # Rang 7
            "Essence de Sagesse": 4,            # Rang 5
        },
    ],
    "Pack de Flèches": [
        {  # Niveau 1
            "Emblème de la Fin": 1,
            "Ether Non-Newtonien": 3,           # Rang 1
            "Ectoplasme Chaud": 3,              # Rang 1
            "Eclat de Verre": 1,                # Rang 1
        },
        {  # Niveau 2
            "Fluide Alien": 2,                  # Rang 2
            "Poil Gelé": 2,                     # Rang 2
            "Roche Glycérine": 2,               # Rang 2
        },
        {  # Niveau 3
            "Fragment Osseux": 2,               # Rang 3
            "Iris du Malheur": 2,               # Rang 3
            "Velour de Cervidé": 2,             # Rang 3
        },
        {  # Niveau 4
            "Essence de Fortitude": 3,          # Rang 5
            "Poussière Dorée Animée": 2,        # Rang 4
            "Fragment Sophiste": 2,             # Rang 6
        },
        {  # Niveau 5
            "Gemme Prismatique": 5,             # Rang 7
            "Orbe Convergeant": 5,              # Rang 7
            "Essence de Résistance": 4,         # Rang 5
        },
    ],
    "Pack Premier Tour": [
        {  # Niveau 1
            "Poussière Animée": 3,              # Rang 1
            "Ether Non-Newtonien": 2,           # Rang 1
            "Ectoplasme Chaud": 2,              # Rang 1
        },
        {  # Niveau 2
            "Emblème de la Fin": 1,
            "Fluide Alien": 3,                  # Rang 2
            "Poil Gelé": 2,                     # Rang 2
            "Morceau de Cloche": 2,             # Rang 2
        },
        {  # Niveau 3
            "Velour de Cervidé": 2,             # Rang 3
            "Fragment Osseux": 2,               # Rang 3
            "Ecaille de Phénix": 3,             # Rang 2
        },
    ],

    # banque

    "Médaillon de Leprechaun": [
        {  # Niveau 1
            "Coeur Gravitaire": 3,              # Rang 1
            "Poussière Animée": 3,                # Rang 1
            "Eclat de Verre": 3,                     # Rang 1
        },
        {  # Niveau 2
            "Fluide Alien": 3,             # Rang 2
            "Ecaille de Phénix": 3,                  # Rang 2
            "Poil Gelé": 3,               # Rang 2
        },
        {  # Niveau 3
            "Moustache de Chat": 3,             # Rang 3
            "Iris du Malheur": 3,                  # Rang 3
            "Composants Electroniques": 3,              # Rang 3
        },
        {  # Niveau 4
            "Emblème de la Fin": 1,
            "Eclat de Crystal": 3,      # Rang 4
            "Fragment de Jade": 3,             # Rang 4
            "Gemme Bleue": 3,                   # Rang 4
        },
        {  # Niveau 5
            "Essence de Vitalitée": 3,      # Rang 5
            "Essence de Fortitude": 3,             # Rang 5
            "Essence de Résistance": 3,                   # Rang 5
            "Fragment Insatiable": 3,                   # Rang 6
        },
    ],


    "Noyau d'Aurelionite": [
        {  # Niveau 1
            "Ectoplasme Chaud": 3,           # Rang 1
            "Poussière Animée": 3,              # Rang 1
            "Eclat de Verre": 3,                # Rang 1
        },
        {  # Niveau 2
            "Ether Non-Newtonien": 4,                  # Rang 1
            "Ectoplasme Chaud": 4,                     # Rang 1
            "Ecaille de Phénix": 3,             # Rang 2
        },
        {  # Niveau 3
            "Fluide Alien": 3,             # Rang 2
            "Morceau de Cloche": 3,             # Rang 2
            "Poil Gelé": 3,               # Rang 2
        },
        {  # Niveau 4
            "Poil Gelé": 4,      # Rang 2
            "Roche Glycérine": 4,                   # Rang 2
            "Fragment Osseux": 3,              # Rang 3
        },
        {  # Niveau 5
            "Velour de Cervidé": 3,          # Rang 3
            "Iris du Malheur": 3,           # Rang 3
            "Moustache de Chat": 3,          # Rang 3
        },
        {  # Niveau 6
            "Moustache de Chat": 4,               # Rang 3
            "Composants Electroniques": 4,                   # Rang 3
            "Pilules de Roulette": 3,              # Rang 4
        },
        {  # Niveau 7
            "Eclat de Crystal": 3,           # Rang 4
            "Poussière Dorée Animée": 3,                     # Rang 4
            "Gemme Bleue": 3,         # Rang 4
        },
        {  # Niveau 8
            "Emblème de la Fin": 1,
            "Gemme Bleue": 4,              # Rang 4
            "Fragment de Jade": 4,               # Rang 4
            "Essence de Vitalitée": 3,            # Rang 5
        },
        {  # Niveau 9
            "Essence de Sagesse": 3,              # Rang 5
            "Essence de Fortitude": 3,             # Rang 5
            "Essence de Résistance": 3,          # Rang 5
        },
        {  # Niveau 10
            "Essence de Magie": 4,             # Rang 5
            "Essence de Vitalitée": 4,          # Rang 5
            "Fragment Sophiste": 3,         # Rang 6
        },
        {  # Niveau 11
            "Fragment de Fatalité": 3,        # Rang 6
            "Fragment Mélioratif": 3,      # Rang 6
            "Fragment Insatiable": 3,                   # Rang 6
        },
        {  # Niveau 12
            "Fragment Insatiable": 4,        # Rang 6
            "Fragment Sophiste": 4,      # Rang 6
            "Essence Carmine": 3,                   # Rang 7
        },
        {  # Niveau 13
            "Clochette": 3,        # Rang 7
            "Perle de Chance": 3,      # Rang 7
            "Antenne de Cérémonie": 3,                   # Rang 7
        },
        {  # Niveau 14
            "Encre de Pouvoir": 4,        # Rang 7
            "Tissu Perceptif": 4,      # Rang 7
            "Ichor Divin": 3,                   # Rang 7
        },
        {  # Niveau 15
            "Essence Dorée": 50,        # Rang 7
        },
        
    ],


    # ancien

    "Sacoche" : [ # garde redcoin
        {
            "Essence Dorée" : 50 ,
        },
    ],
    "Emblème de la Fin" : [ # + d'objets chez marchand
        {
            "Essence Dorée" : 1 ,
            "Essence Astrale" : 1 ,
            "Essence Carmine" : 1 ,
            "Clochette" : 1 ,
            "Oeuf de Fabergé" : 1 ,
            "Néphrite Brut" : 1 ,
            "Nitroglycérine" : 1 ,
            "Feu Grégorien" : 1 ,
            "Perle de Chance" : 1 ,
            "Réceptacle Anastral" : 1 ,
            "Orbe Convergeant" : 1 ,
            "Gemme Prismatique" : 1 ,
            "Fluide Nutritif" : 1 ,
            "Ecaille Chitineuse" : 1 ,
            "Antenne de Cérémonie" : 1 ,
            "Circuit Biomécanique" : 1 ,
            "Encre de Pouvoir" : 1 ,
            "Tissu Perceptif" : 1,
            "Ichor Divin" : 1
        },
    ],

    # Mage Hollistique

    "Clé" : [ # clé des étages
        {
            "Fluide Alien" : 3,
            "Roche Glycérine" : 3,
            "Poil Gelé" : 3,
            "Fragment Insatiable" : 2
        },
        {
            "Moustache de Chat" : 3,
            "Fragment Osseux" : 2,
            "Iris du Malheur" : 3,
            "Essence Astrale" : 15,
        },
        {
            "Coeur Gravitaire" : 15,
            "Poil Gelé" : 10,
            "Iris du Malheur" : 8,
        },
        {
            "Composants Electroniques" : 7,
            "Eclat de Crystal" : 7,
            "Poussière Dorée Animée" : 7
        },
        {
            "Eclat de Crystal" : 5,
            "Pilules de Roulette" : 4,
            "Fragment de Jade" : 5,
            "Poussière Dorée Animée" : 6,
            "Gemme Bleue" : 4,
        },
        {
            "Fragment Mélioratif" : 10,
            "Fragment Sophiste" : 10,
            "Fragment de Fatalité" : 10,
            "Fragment Insatiable" : 10,
        },
    ],
    
    # Chuchoteur de carte

    "Carte" : [ # carte des étages
        {
            "Carte Mentale" : 5
        },
        {
            "Carte Mentale" : 7
        },
        {
            "Carte Mentale" : 9
        },
        {
            "Carte Mentale" : 11
        },
        {
            "Carte Mentale" : 13
        },
        {
            "Carte Mentale" : 15
        },
        {
            "Carte Mentale" : 17
        },
    ],
}
