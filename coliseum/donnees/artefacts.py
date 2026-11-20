"""Artefacts : effets et familles (sophiques, mélioratifs, fatalité)."""

LISTEEFFETSARTEFACT = {
    "Graine de Grenade": {"Commentaire": "Cette graine d'un fruit apprécié des dieux augmente votre vitalité.",
                           "Vie": 15},  # vie t
    "Eau du Styx": {"Commentaire": "Cette fiole imprégnée de l'essence des morts augmente votre réservoir de mana.",
                             "Mana": 15},  # mana t
    "Aile de Cire d'Icare": {"Commentaire": "Ce bout du chef d'oeuvre de Dédale augmente votre capacité a esquiver les attaques.",
                              "Taux esquive": 6},  # esquive t
    "Griffe de Lion": {"Commentaire": "Cette griffe contient l'essence d'une bête féroce abattue par le Roi Singe, et augmente votre attaque.",
                        "Attaque": 8},  # attaque t
    "Statue d'Angerona": {"Commentaire": "Angerona, la déesse de la Concentration, veille sur tout ses fidèles, et vous octroie la vue qui discerne les faiblesses.",
                           "Taux coup critique": 6, "Taux sort critique": 6},  # taux critique t
    "Collier de Mithril": {"Commentaire": "Ce collier est le tout premier artefact crée par les tout premiers nains, pour résister aux attaques des tout premiers monstres pendant l'Age du Chaos.",
                            "Defence": 8},  # defence t
    "Elixir du Sage": {"Commentaire": "Cette bouteille contient toutes les réalisations du doyen de la Grande Bibliothèque d'Alexandrie, sous forme liquide.",
                        "Intelligence": 8},  # intelligence
    "Petite Pierre Philosophale": {"Commentaire": "Ce prototype permet de transmuter une quantitée limitée de choses en or.",
                                    "Gold": 1000},  # gold t
    "Anneau Cramoisi": {"Commentaire": "Cet anneau forgé pendant la Guerre de l'Interdit a bu le sang de nombreux dieux et déesses afin de conferer leur endurance a son porteur.",
                         "Endurance": 20},  # endurance t
    "Orbe de Disruption": {
        "Commentaire": "Cet orbe vient de l'Ains Terra Net, le monde des voyageurs, et perturbe le mana environnant.\nLes monstres avec un réservoir de mana brisé perdent en plus 6 pv par numéro d'étage a chaque tour !",
    },  # degat quand ennemi plus mana
    "Plume de Munin": {"Commentaire": "Cette plume vient de Munin, un des corbeaux d'Odin qui voyage a travers les neufs mondes, et confère a son porteur une certaine aisance a esquiver les attaques.",
                        "Taux esquive": 6},  # esquive t
    "Collier des Brísingar": {"Commentaire": "Ce collier porté par Freya élève le corps et son réservoir de mana a une condition optimale pour le rendre plus charismatique.",
                               "Vie": 8, "Mana": 8},  # vie et mana t
    "Draupnir": {"Commentaire": "D'après les légendes, cet anneau est sensé se multiplier par 9 toute les 9 nuits.\nIl n'a pas l'air de réagir pour le moment..."},  # gold t
    "Magatama": {
        "Commentaire": "Cette perle passée de générations en générations par les plus grands empereurs du monde contient une partie de leur âme et confère a son porteur de multiples augmentations.",
        "Attaque": 2, "Defence": 2, "Intelligence": 2, "Vie": 4, "Mana": 4, "Endurance": 5
    },  # attaque, intelligence, defence, vie, mana, endurance
    "Voile de Ino": {"Commentaire": "Le voile porté brièvement par Ulysse, et qui protege des attaques (permanent) et de la mort (une seule fois).",
                     "Defence": 2},  # defence t
    "Megingjord": {"Commentaire": "La ceinture de Thor qui lui donne une grande puissance pendant les moments critiques, ainsi que la capacité de soulever son marteau.",
                    "Degat coup critique": 10, "Degat sort critique": 10},  # degat critiques t
    "Manne Céleste": {"Commentaire": "La seule source de nourriture des hébreux pendant 40 ans, gracieusement offerte par le Ciel, et qui leur a permit de marcher jusqu'à trouver leur terre d'adoption.",
                       "Endurance": 10, "Vie": 10},  # endurance + vie t
    "Nœud Gordien": {"Commentaire": "Le cordage compliqué défait seulement par le Maitre de l'Asie, mais finalement tranché par Alexandre le Grand, et qui a gardé depuis une partie de sa force.",
                      "Attaque": 5},  # attaque t
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
                      "Intelligence": 5},  # intelligence t
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
        "Commentaire": "L'écaille d'un divin serpent signifiant le renouveau et l'infini.\nVous regagnez 1,5 point de vie par numéro d'étage (arrondi) a chaque utilisation de sorts."
    },  # Rend 2 pv par utilisation de sort
    "Serment d'Heimdall": {
        "Commentaire": "La marque du serment d'un dieu omniscient envers le peuple qui a continué a le prier dans le pire des moments.\nIl y a de très faibles chance qu'un sort utilise son mana au lieu du votre."
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
        "Commentaire": "La graine d'une plante monstreuse amenant son planteur dans une dimension remplie de ses semblables, affamés et en manque de nutriments, cachée dans les nuages.\nSes racines tentaculaires cherchant le sang ne peuvent être stoppées que par une lame plantée dans la graine originelle.\nInvoque des roches depuis sa dimension d'origine, ajoutant +25% de dégâts bonus a l'effet [Lapidation]."
    },  # 20% de degats supplémentaires par lapidation
    "Miette de Pain Congelée": {
        "Commentaire": "La seule trace d'enfants emmenés dans les sombres forêts du continent pour y être perdus par leurs parents en manque d'argent.\nLa rancoeur d'âmes pures englouties par ce qui se cache dans les bois fait durer l'altération d'état [Gelure] pendant 2 tours supplémentaires."
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
                    "\nChaque ennemi tué augmente de 0.5% votre bonus de dégâts total.")
    },
    "Schmilblick": {
        "Commentaire": ("Un bidule bizarre crée par une inventrice farfelue."
                    "\nA l'entrée d'un nouvel étage, toutes ses salles sont directement dessinées sur la carte (annule les effets du Monocle de Vérité)")
    },
    "Contrat de Travail": {
        "Commentaire": ("Un bout de papier promettant la puissance aux économes afin qu'ils ne se fassent plus martyriser par le système."
                    "\nVotre bonus de dégâts total augmente de 1% par paquet de 50 pièces possédé (maximum +100%).")
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
                    "\nLorsque l'effet Brulûre se termine, redonne 2 pv et 1,5 pm par numéro d'étage.")
    },
    "Bandeau Teinté": {
        "Commentaire": ("Une relique de Thémis, l'esprit de la Justice, marqué d'un curieux éclat doré."
                        "\nEn combat, vous gagnez 1 pièce a chaque tours.")
    },        
    "Ecaille de la Bête": {
        "Commentaire": ("Le dernier témoin de l'existence d'une bête féroce dans le Coliseum, laissée derriere a la poursuite de la liberté."),
                        "Defence": 10
    },        
    "Hors Stock": {
        "Commentaire": ("Un petit bout de papier sur lequel est écrit *Plus d'artefact a donner*.\nNe fait rien."),
    },        
}


ARTEFACTSOPHIQUE = [
    "Orbe de Disruption",
    "Draupnir",
    "Voile de Ino",
    "Couronne Sacrée",
    "Gant de Midas",
    "Gant d'Héphaïstos",
    "Plaquette du Souvenir",
    "Monocle de Vérité",
    "Sabre du Roi de Glace",
    "Bocle de Philoctète",
    "Ecaille d'Ouroboros",
    "Serment d'Heimdall",
    "Masque d'Oblivion",
    "Chapelet de Moine",
    "Oeuil de Phénix",
    "Echarde de Pinocchio",
    "Voeu Cristallisé",
    "Haricot Magique",
    "Miette de Pain Congelée",
    "Chaperon Rouge",
    "Morceau de Plomb",
    "Bague de l'Âne",
    "Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure",
    "Assurance Distributeur",
    "Hors Stock"
]


ARTEFACTMELIORATIF = [
    "Graine de Grenade",
    "Eau du Styx",
    "Aile de Cire d'Icare",
    "Griffe de Lion",
    "Statue d'Angerona",
    "Collier de Mithril",
    "Elixir du Sage",
    "Petite Pierre Philosophale",
    "Anneau Cramoisi",
    "Plume de Munin",
    "Collier des Brísingar",
    "Magatama",
    "Voile de Ino",
    "Megingjord",
    "Manne Céleste",
    "Nœud Gordien",
    "Don de Terre",
    "Don de Foudre",
    "Don de Feu",
    "Don de Glace",
    "Don Sanguin",
    "Don Physique",
    "Don Astral",
    "Nimbe Divine",
    "Ecaille de la Bête",
    "Âme de la Bête",
    "Regard de la Bête",
    "Epée de Damocles", 
    "Morceau d'Ether Fragile", 
    "Eau Bénite", 
    "Bandeau Catharsis", 
    "Charbon Primordial", 
    "Saphir de Gel", 
    "Fossile Figé", 
    "Fiole des Eclairs"
]


ARTEFACTFATALITE = [
    "Pièce Fondue",
    "Tiare de Suie",
    "Chaine de Main",
    "Larme d'Yggdrasil",
    "Collier de Nephilim",
    "Cape Victorieuse",
    "Schmilblick",
    "Contrat de Travail",
    "Dessin Nostalgique",
    "Vide Interieur",
    "Badge Terni",
    "Perle de Pluie",
    "Syra",
    "Pin's Extincteur",
    "Bandeau Teinté",
]
