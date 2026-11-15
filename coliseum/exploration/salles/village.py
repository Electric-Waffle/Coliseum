"""Lieux du village (étage -1) : commerçants, quartiers, chemins et habitants."""

import random

from coliseum import services
from coliseum import audio
from coliseum.audio import PermanentPlaySFX
from coliseum.console import ClearConsole, attendre
from coliseum.exploration.salles.registre import salle_de_type


@salle_de_type("DECHARGE")
def reveler_decharge(etage, salle):
    if  services.Sove.ModifieTagsDansSove("Checke", "Village Jour"):
        print("Vous vous approchez d'un monticule de déchets.")
        services.Affichage.EntreePourContinuer()
        audio.CHANNELMUSIQUEDEBASE.set_volume(0.7)
        PermanentPlaySFX("garbage_ambiance")
        audio.CHANNELSFX.set_volume(0.5)
        print("L'odeur est putride, ce qui n'est pas peu dire au vu de votre manque de capacité olfactive en temps que fantome.")
        services.Affichage.EntreePourContinuer()
        print("Enfait, ce n'est pas vraiment l'odeur qui dérange, mais une énergie sinistre, putride, qui émane du tas de bric a brac et vous repousse de manière instinctive.")
        services.Affichage.EntreePourContinuer()
        while True:
            while True:
                liste_de_dechets = services.Player.PutMateriauxInList()
                try:
                    if len(liste_de_dechets) == 0:
                        print("Il n'y a rien d'utile ici.")
                        print("\n1 - Partir")
                    else:
                        print("Vous pouvez voir des materiaux utiles ressemblant a ce que vous aviez avant votre mort .")
                        print("\n1 - Partir")
                        print("2 - Recupérer vos materiaux")
                    choix = int(input("\nFaites votre choix avec les nombres : "))
                    ClearConsole()
                    if (choix in [1, 2] and len(liste_de_dechets) != 0) or (len(liste_de_dechets) == 0 and choix == 1):
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print("Vous laissez le tas nauséabond derriere vous.")
                services.Affichage.EntreePourContinuer()
                break
            else:
                print("Vous fouillez dans la déchetterie, et récuperez : ")

                for materiaux in services.Player.liste_de_materiaux:
                    if services.Player.liste_de_materiaux[materiaux] != 0:
                        services.Sove.ModifieDechetsDansSove("Ajout", materiaux, services.Player.liste_de_materiaux[materiaux])
                        print(f"{services.Player.liste_de_materiaux[materiaux]} {materiaux}")

                services.Player.BringBackListeMateriauxToZero()

                services.Save.SaveTheGameSansAffichage()

                services.Affichage.EntreePourContinuer()

                print("[SYSTEM OVERRIDE : SUCCESSFULL ACE EXECUTION]")
                print("[JOUEUR RECONNU]")
                print("[VOS MATERIAUX ONT ETE DEPLACE DANS VOTRE FICHIER DE SAUVEGARDE PERMANENT, ET SE CUMULERONT AU FIL DE VOS DESCENTE]")

                services.Affichage.EntreePourContinuer()

        audio.CHANNELSFX.set_volume(0)
        attendre(0.01)
        audio.CHANNELSFX.stop()
        audio.CHANNELMUSIQUEDEBASE.set_volume(1)

    else:
        print("Vous laissez votre regard se perdre dans les montagnes de dechets qui remplissent l'horizon de leur teinte gris/sapin.")
        services.Affichage.EntreePourContinuer()
        print("De nombreuses âmes errent sans but dans les monticules.")
        services.Affichage.EntreePourContinuer()


@salle_de_type("ARMURIER", "SORCIERE", "HERBORISTE")
def reveler_armurier(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if  services.Sove.ModifieTagsDansSove("Checke", "Village Jour"):
        print("Vous vous approchez de l'étal du marchand.")
        services.Affichage.EntreePourContinuer()
        etage.DoTransition("In", salle["type"])
        services.Trader.DoVillageTrading(salle["type"])
        print("Vous faites un signe de main et quittez l'étal.")
        services.Affichage.EntreePourContinuer()
        etage.DoTransition("Out", salle["type"])
    else:
        print("Les étals des marchands sont fermés.")
        services.Affichage.EntreePourContinuer()


@salle_de_type("MAGE")
def reveler_mage(etage, salle):
    if  services.Sove.ModifieTagsDansSove("Checke", "Village Jour"):
        print("Vous vous approchez d'une tour étrange, tordue, qui devrait s'écrouler mais ne le fait pas..")
        audio.CHANNELMUSIQUEDEBASE.set_volume(0.5)
        PermanentPlaySFX("mage_ambiance")
        services.Affichage.EntreePourContinuer()
        services.Trader.DoKeyTrading()
        print("Vous passez les portes de la tour, en veillant a ne pas taper votre tête sur le bas plafond.")
        services.Affichage.EntreePourContinuer()
        audio.CHANNELSFX.set_volume(0)
        attendre(0.01)
        audio.CHANNELSFX.stop()
        audio.CHANNELMUSIQUEDEBASE.set_volume(1)
    else:
        print("Vous regardez avec dépit les restes d'une tour écroulée au sol.")
        services.Affichage.EntreePourContinuer()
        print("De nombreux cristaux gisent dans les débris.")
        services.Affichage.EntreePourContinuer()


@salle_de_type("BANQUIER")
def reveler_banquier(etage, salle):
    # dessine la salle, si ce n'est pas fait 
    if  services.Sove.ModifieTagsDansSove("Checke", "Village Jour"):
        print("Vous vous approchez d'une batisse droite, propre, et en passez les portes.")
    else:
        print("Vous vous approchez d'une batisse droite, propre, et apercevez une pancarte accrochée a la poignée :")
        print("*Ouvert 24h/24*")
        services.Affichage.EntreePourContinuer()
        print("Vous rentrez dans la banque.")
    services.Affichage.EntreePourContinuer()
    etage.DoTransition("In", salle["type"])
    services.Trader.DoBankTrading()
    print("Vous repassez les portes de la banque.")
    services.Affichage.EntreePourContinuer()
    etage.DoTransition("Out", salle["type"])


@salle_de_type("HOLLISTIQUE")
def reveler_hollistique(etage, salle):
    # dessine la salle, si ce n'est pas fait 
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.bete()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print("Vous avancez dans les couloirs, et sursautez en entendant une voix derrière vous.")
    services.Affichage.EntreePourContinuer()
    print("*...hey..il y a quelqu'un ..?*")
    services.Affichage.EntreePourContinuer()
    print("Vous vous retournez, et trouvez une jeune femme en accoutrement léopard ridicule adossée contre le mur.")
    services.Affichage.EntreePourContinuer()
    print("*rigolez pas...je pensais que ca ferait fuir les monstres...*")
    services.Affichage.EntreePourContinuer()
    print("Vous aidez la jeune femme a se relever.")
    services.Affichage.EntreePourContinuer()
    print("*J'ai passé ma vie a faire des choses sans aucune raison, et bizarrement, c'était toujours la bonne idée. Mais la, je vois mal en quoi etre coincée dans un donjon mortel m'aiderait...*")
    services.Affichage.EntreePourContinuer()
    print("*Peut être pourriez vous m'aider a descendre ? Je peut lancer quelques sorts a chaque début de tour.*")
    services.Affichage.EntreePourContinuer()
    print("Vous commencez a réfléchir a la proposition, et un mal de dos venant de nulle part vous tord de douleur et vous fait baisser la tête.")
    services.Affichage.EntreePourContinuer()
    print("Le mal de dos disparait, et vous relevez la tête.")
    services.Affichage.EntreePourContinuer()
    print("*Oh merci ! Merci milles fois !*")
    services.Affichage.EntreePourContinuer()
    print("Vous avez l'impression que la mage a confondu votre mouvement pour un hochage de tête...M'enfin.")
    services.Affichage.EntreePourContinuer()
    print("Vous obtenez l'arte-, je veux dire, la Mage se bat avec vous !")
    services.Affichage.EntreePourContinuer()
    print("Elle enflamme ou gèle vos ennemis a chaque début de tour !")
    services.Affichage.EntreePourContinuer()
    print("Cepandant, si vos pv tombent en dessous de 10 pendant un combat, vous risquez de ne plus pouvoir la défendre d'un sort tragique.")
    services.Affichage.EntreePourContinuer()
    services.Player.liste_dartefacts_optionels.append("Mage")
    # fait que l'event soit finit et ne peut ps etre relancé
    salle["terminé par joueur"] = True


@salle_de_type("CARTOGRAPHE")
def reveler_cartographe(etage, salle):
    if  services.Sove.ModifieTagsDansSove("Checke", "Village Jour"):
        print("Vous avancez dans la rue et voyez un homme par terre, écrivant sur le sol diverses symboles mathématiques a l'aide d'une craie.")
        services.Affichage.EntreePourContinuer()
        audio.CHANNELMUSIQUEDEBASE.set_volume(0.5)
        PermanentPlaySFX("mapper_ambiance")
        services.Trader.DoMapTrader()
        print("Vous faites demi tour en veillant a ne pas marcher sur les symboles écrits a terre.")
        services.Affichage.EntreePourContinuer()
        audio.CHANNELSFX.set_volume(0)
        attendre(0.01)
        audio.CHANNELSFX.stop()
        audio.CHANNELMUSIQUEDEBASE.set_volume(1)
    else:
        print("Vous trouvez une maison dont le sol devant est couvert d'inscriptions a la craie.")
        services.Affichage.EntreePourContinuer()
        print("Un nombre est entouré a de multiples reprises :")
        services.Affichage.EntreePourContinuer()
        print("*42*")
        services.Affichage.EntreePourContinuer()


@salle_de_type("ARENE")
def reveler_arene(etage, salle):
    print("Vous avancez vers une réplique plus petite d'un colisée, comme on peut en voir a Rome.")
    print("Alors que vous arrivez au niveau de l'entrée, un homme habillé en punk vous arrête.")
    services.Affichage.EntreePourContinuer()
    audio.CHANNELMUSIQUEDEBASE.set_volume(0.7)
    PermanentPlaySFX("colysee_ambiance")
    services.Trader.DoColiseum()
    print("Vous laissez le coliseum derriere vous.")
    services.Affichage.EntreePourContinuer()
    audio.CHANNELSFX.set_volume(0)
    attendre(0.01)
    audio.CHANNELSFX.stop()
    audio.CHANNELMUSIQUEDEBASE.set_volume(1)


@salle_de_type("FABRICATEUR")
def reveler_fabricateur(etage, salle):
    if  services.Sove.ModifieTagsDansSove("Checke", "Village Jour"):
        audio.CHANNELMUSIQUEDEBASE.set_volume(0.7)
        PermanentPlaySFX("machine_ambiance")
        print("Vous approchez d'une petite maison de bois, style outback, dans un coin de la décharge.")
        print("A l'interieur, il y a une grosse machine avec une petite cabine nommée *INPUT*, une cabine *OUTPUT*, et un tube de cuivre qui relie les deux cabines au coeur de la machine.")
        services.Affichage.EntreePourContinuer()
        print("Il y a un panneau au milieu indiquant des catégories allant de Rugueux à Très Fin, en passant par Grossier, 2:1, et Fin.")
        print("La poignée sélecteur est bloquée sur la catégorie *2:1*.")
        services.Affichage.EntreePourContinuer()
        services.Trader.DoFabricator()
        print("Vous laissez la machine et sortez de la petite cabine.")
        services.Affichage.EntreePourContinuer()
        audio.CHANNELSFX.set_volume(0)
        attendre(0.01)
        audio.CHANNELSFX.stop()
        audio.CHANNELMUSIQUEDEBASE.set_volume(1)
    else:
        print("Vous cherchez la petite maison au fond de la décharge, mais ne trouvez rien.")
        services.Affichage.EntreePourContinuer()


@salle_de_type("VILLAGE_QUARTIERS")
def reveler_village_quartiers(etage, salle):
    print("Vous trouvez une pancarte en pierre rose, a moitié enfoncé dans le sol, sur lequel est gravé un message en grandes lettres :")
    print("*VERS : QUARTIER RESIDENTIEL*")
    services.Affichage.EntreePourContinuer()


@salle_de_type("CHEMIN_ARENE")
def reveler_chemin_arene(etage, salle):
    if  services.Sove.ModifieTagsDansSove("Checke", "Village Jour"):
        liste_descriptions_possibles = [
            "Vous entendez les sons et les cris venant du Colysée.",
            "Vous passez à côté d'un groupe de 4 frères habillés en tenue de prisonnier jaune et noire.\nLeur taille est différente.",
            "Vous prenez une grande inspiration.\nÇa sent la mandarine...",
            "Vous regardez au loin : les champs remplis d'âmes errantes continuent à perte de vue.",
            "Vous prenez une grande inspiration.\nUne odeur iodée remplit vos narines...",
            "Vous passez à côté d'un homme roux dans un grand kimono noir.\nL'épée qu'il traîne derrière lui est gigantesque !",
            "Vous regardez les bâtisses qui entourent le Colysée, au Nord.\nElles vendent toutes des pâtisseries.",
            "Vous regardez les bâtisses qui entourent le Colysée, au Sud.\nElles vendent toutes des boissons.",
            "Vous regardez les bâtisses qui entourent le Colysée, à l'Est.\nElles vendent toutes des chips.\nUn rapide coup d'œil vous indique que toutes les chips sont saveur poulet rôti et thym.",
            "Vous regardez les bâtisses qui entourent le Colysée, à l'Ouest.\nElles vendent des costumes sur des thèmes variés.",
            "Vous passez à côté d'un groupe habillé avec un kimono orange, et entendez un bout de leur conversation.\nQuelque chose à propos de boules de dragons ?",
            "Le sol est pavé de pierres anciennes, usées par des siècles de passages.",
            "Un homme joue de la flûte sur les marches du Colysée, attirant quelques curieux.",
            "Des marchands ambulants crient leurs prix, tentant de vendre des souvenirs.",
            "Des enfants courent autour d'une fontaine centrale, éclaboussant les passants avec leurs rires.",
            "Un sculpteur sur bois est assis au bord d'une fontaine, entrainant sa lame sur des morceaux de différentes couleur.\nDevant lui, vous voyez une vingtaine de bols."
            "Un artiste de rue fait des acrobaties près de la grande place, attirant l'attention de quelques âmes.",
            "Vous remarquez un marchand vendant des bijoux faits à la main avec des pierres colorées.\nJoli, mais terriblement inutile",
            "Un groupe de musiciens joue une mélodie entraînante, qui vous fait oublier pendant quelques instant ou vous êtes.",
            "Vous regardez le soleil et sentez sa chaleur sur votre âme.\nVous êtes bel et bien mort, mais vous sentez plus vivant que jamais.",
        ]
    else:
        liste_descriptions_possibles = [
            "Le Colysée est plongé dans l’obscurité, mais des murmures étranges s’échappent de ses entrailles.",
            "Vous entendez au loin des rires étouffés provenant d’un bar, tandis qu’un serveur glisse un cocktail fluorescent sur une table.",
            "Les fenêtres des maisons sont éclairées par des lueurs douces, projetant des ombres délicates sur les pavés.",
            "Un vent frais vous effleure, emportant avec lui des chuchotements venus de ruelles désertes.",
            "Une odeur de tabac et de menthe émane d’un groupe installé en terrasse, leur conversation basse se mêlant au silence nocturne.",
            "Les fontaines sont éteintes, mais le bruit d’un léger filet d’eau persiste, amplifiant le calme environnant.",
            "Les cris du Colysée sont étouffés par la nuit, presque mélodieux, comme un chant ancien qu’on ose à peine écouter.",
            "Les pavés sous vos pieds semblent plus froids maintenant que la nuit s’est installée.",
            "Une légère brume commence à se lever, enveloppant la place dans un voile mystique.",
            "Les enseignes lumineuses des bars clignotent doucement, attirant les rares noctambules vers leurs portes.",
            "Vous passez à côté d’une fenêtre ouverte et entendez un vieux vinyle grésiller une chanson d’un autre temps.",
            "Les lanternes suspendues au-dessus de la place diffusent une lumière tamisée, créant des halos jaunes et oranges dans l’air.",
            "Un chat noir traverse silencieusement la place, ses yeux brillant dans l’obscurité.",
            "L’air est frais et légèrement humide, apportant avec lui une odeur de terre et de végétation nocturne.",
            "Un homme seul joue quelques notes de guitare, sa musique flottant doucement dans le silence de la nuit.",
            "Le Colysée, sous la lumière des étoiles, semble plus imposant, comme une silhouette vigilante observant la ville endormie.",
            "Vous entendez le tintement discret de verres dans un bar, signe d’une soirée tranquille qui s’éternise.",
            "Des bougies allumées sur les terrasses créent des jeux de lumière et d’ombre sur les visages des clients attablés.",
            "Le ciel nocturne est d’un bleu profond, parsemé d’étoiles scintillantes qui semblent veiller sur la place.",
            "Un léger brouillard se lève autour du Colysée, le rendant presque irréel, comme s’il flottait au-dessus de la place.",
        ]

    description_a_afficher = random.choice(liste_descriptions_possibles)
    print(description_a_afficher)
    services.Affichage.EntreePourContinuer()


@salle_de_type("CHEMIN_QUARTIERS")
def reveler_chemin_quartiers(etage, salle):
    if  services.Sove.ModifieTagsDansSove("Checke", "Village Jour"):
        liste_descriptions_possibles = [
            "Les maisons qui longent l’artère principale sont aussi diverses que des sculptures exposées en plein air.",
            "Une maison à la forme d’un cube géant attire votre attention, son propriétaire, vêtu d'une tunique rouge, vante les mérites de son toit en forme de prisme.",
            "Un homme ajuste une étrange girouette en forme de dragon sur le toit de sa maison circulaire, lui donnant un air fantastique.",
            "Vous passez devant une maison haute et fine, presque tordue, ses fenêtres triangulaires brillent encore sous la lumière du jour.",
            "Les pavés sous vos pieds semblent légèrement irréguliers, ajoutant un charme ancien à cette rue moderne.",
            "Un enfant court entre deux maisons, son rire résonne tandis qu'il disparaît derrière une porte en bois sculpté.",
            "Les propriétaires d’une maison aux murs en mosaïque colorée sont assis sur le seuil, discutant avec des voisins curieux.",
            "Une maison ressemblant à une tour penchée projette une ombre démesurée sur la rue.",
            "Vous sentez l’odeur de pain chaud s’échapper de la fenêtre ouverte d’une maison à l’architecture massive, dont les murs semblent faits de blocs de pierre brute.",
            "Un passant s’arrête pour observer une maison en forme de dôme, en discutant avec l'architecte qui semble donner des détails techniques aux curieux.",
            "Les lanternes de la rue commencent à s’allumer, leur lumière orangée se reflétant sur les façades d’une maison aux motifs floraux.",
            "Une maison construite entièrement en bois sombre attire l’œil, avec ses sculptures minutieuses d’animaux qui décorent la façade.",
            "Une femme, vêtue de façon élégante, sort d’une maison aux allures de manoir gothique, le sommeil a son zénith accentue les contours sombres de l’édifice.",
            "Les maisons, si différentes les unes des autres, semblent être en compétition pour attirer les regards des passants.",
            "Vous passez devant une maison étrange, avec une porte minuscule et un toit démesurément grand, rappelant une maison de conte de fées.",
            "L’air est chaud, et les bruits des conversations des habitants se mêlent aux craquements du bois des maisons anciennes.",
            "Un vieil homme vous salue depuis son balcon, décoré de plantes grimpantes qui recouvrent presque toute la façade de sa maison en pierre.",
            "Une maison de forme hexagonale dégage une atmosphère mystérieuse, ses fenêtres sont éclairées d’une lueur douce et bleutée.",
            "Vous entendez des bruits de marteaux et d'outils : un artisan semble encore travailler dans son atelier, dont la porte est grande ouverte sur la rue.",
            "Le ciel au-dessus de l’artère se teinte d’orange et de violet, illuminant les toits des maisons avec une lumière magique."
        ]
    else:
        liste_descriptions_possibles = [
            "Le ciel étoilé s'étend au-dessus de l'artère principale, les lumières des maisons créant des halos doux dans la nuit.",
            "Les maisons sont silencieuses, seules leurs fenêtres éclairées témoignent de la présence des habitants à l'intérieur.",
            "Vous levez les yeux vers le ciel : des milliers d'étoiles brillent, offrant une sérénité que la journée ne connait pas.",
            "Les lanternes de la rue projettent des ombres longues et apaisantes sur le sol pavé, comme si la ville elle-même dormait.",
            "Le murmure lointain du vent dans les arbres et les toits donne l'impression que tout est en ordre, que tout est calme.",
            "Vous sentez une brise légère sur votre visage, et un sentiment de confort s'installe, comme si vous rentriez chez vous après une longue journée.",
            "Les fenêtres illuminées des maisons sont comme des phares, rappelant que même dans l'obscurité, il y a toujours de la chaleur et de la vie.",
            "Le silence est presque total, seulement interrompu par le doux crépitement d'un feu qu'on devine derrière une fenêtre entrouverte.",
            "Les étoiles semblent briller plus intensément ici, loin des bruits et des lumières de la ville, comme si elles veillaient sur la rue.",
            "Un chat se faufile silencieusement dans la rue, ses yeux luisant sous la lumière d'une lampe, ajoutant une touche de mystère à la tranquillité ambiante.",
            "Vous respirez profondément, l'air frais de la nuit est pur, presque revigorant, et vous donne cette sensation de paix qu'on ressent en rentrant chez soi après une belle journée.",
            "Les maisons semblent veiller sur l'artère principale, comme des gardiens silencieux, tandis que la lumière intérieure filtre à travers les rideaux épais.",
            "Vous entendez au loin le bruit discret d'une porte qui se ferme, signe que les derniers habitants sont rentrés chez eux pour la nuit.",
            "Le ciel, parsemé d’étoiles, est clair et profond, apportant une sensation d'infini qui contraste avec le calme rassurant de la rue.",
            "Les lumières des fenêtres sont chaleureuses, un doux rappel des maisons bien habitées où les familles s’apprêtent à se coucher.",
            "La rue semble endormie, et vous ressentez une douce mélancolie, un mélange de bonheur tranquille et de nostalgie d'enfance.",
            "Une odeur de bois brûlé flotte dans l’air, provenant sans doute d’une cheminée allumée quelque part, ajoutant à la douceur du moment.",
            "Le monde semble loin, ici, où seul le bruit de vos pas sur les pavés résonne doucement dans la nuit.",
            "Les étoiles, immobiles, semblent vous suivre du regard, comme si elles aussi veillaient à ce que la nuit reste paisible.",
            "Vous sentez une chaleur intérieure grandir, comme quand, enfant, vous rentriez chez vous après une longue journée de jeux, sachant que tout est à sa place, que tout ira bien.",
            "Vous manquez de trébucher sur quelqu'un.\nVous regardez alors a vos pieds et découvrez des miliers de personnes allongées sur le sol, admirant le ciel étoilé."
        ]

    description_a_afficher = random.choice(liste_descriptions_possibles)
    print(description_a_afficher)
    services.Affichage.EntreePourContinuer()


@salle_de_type("CHEMIN_COMMERCIAL")
def reveler_chemin_commercial(etage, salle):
    if  services.Sove.ModifieTagsDansSove("Checke", "Village Jour"):
        liste_descriptions_possibles = [
            "Les étals débordent de marchandises exotiques, des épices aux couleurs vives côtoient des objets étranges dont l’utilité est un mystère.",
            "Un groupe d’artistes de rue dessine des formes colorées sur le sol avec de la craie, tandis qu’un acrobate lance des jongles audacieuses à quelques mètres de là.",
            "Vous entendez le son rythmé d’un tambour, un musicien joue au centre d’un cercle de passants qui tapent des mains.",
            "Des vendeurs s’interpellent dans différentes langues, créant un mélange sonore aussi varié que les objets qu’ils vendent.",
            "Vous passez devant un marchand vendant des brosses à dents en bois sculpté, en face d'un étal d’armes finement décorées.",
            "Des bannières multicolores flottent au-dessus de la rue, ajoutant une touche festive à l’ambiance animée.",
            "Un groupe de personnes marchant la tête en bas passe à côté de vous, se dirigeant vers un temple caché, un peu plus loin au Sud.",
            "Des ballons flottent paresseusement dans le ciel, colorés et brillants sous la lumière éternelle du soleil au zénith.",
            "Un riche marchand, vêtu de soieries chatoyantes, discute avec un artisan qui tient entre ses mains une épée finement gravée.",
            "Les odeurs se mélangent : la friture d’un stand de nourriture côtoie le parfum doux d’encens brûlant devant une échoppe de talismans.",
            "Des reliques du monde réel, des objets familiers mais étrangement déplacés, trônent dans des vitrines : une montre, un téléphone, une clé de voiture rouillée.",
            "Un groupe de personnes, habillées en tenues d’époque, déambule lentement, attirant l’attention avec leurs capes ornées de bijoux.",
            "Les rires des enfants jouant autour d’un vendeur de bonbons remplissent l’air, créant une ambiance joyeuse au milieu de l’agitation.",
            "Un homme jongle avec des dagues étincelantes, ses mouvements rapides attirent une foule fascinée.",
            "Des boissons aux couleurs fluorescentes sont servies dans des verres étranges, aux formes impossibles, par un vendeur en costume de magicien.",
            "Un couple de riches nobles, vêtus de tenues extravagantes et dorées, passe entre les stands en observant les marchandises d’un œil critique.",
            "Vous remarquez un marchand à la peau tatouée, ses bras recouverts de symboles étranges, qui vend des cartes aux mystères insondables.",
            "Les gens circulent sans cesse, certains discutent bruyamment en négociant des prix, tandis que d’autres observent en silence les artistes de rue.",
            "Un enfant poursuit un ballon rouge qui s’élève lentement dans le ciel, passant devant une échoppe qui vend des reliques étranges du passé.",
            "Un cri retentit, et vous tournez la tête pour voir un groupe de danseurs acrobatiques exécuter des figures impressionnantes au milieu de la rue."
        ]

    else:
        liste_descriptions_possibles = [
            "Les étals sont vides, leurs toiles tirées, et seules les torches et lampadaires éclairent doucement la rue déserte.",
            "Un vent frais balaie la place, soulevant doucement des feuilles et quelques papiers abandonnés sur le sol pavé.",
            "Vous passez à côté de la banque, la seule bâtisse encore éclairée dans la rue endormie, ses fenêtres brillantes dans la nuit silencieuse.",
            "Deux marchands discutent à voix basse près d'un étal vide, une cigarette à la main, leurs visages éclairés par la lueur des lampadaires.",
            "Un groupe de personnes s'arrête devant chaque bâtiment, leurs murmures de prière résonnent faiblement dans l'air nocturne.",
            "Les rares sans-abris sont allongés sur des bancs en bois, enveloppés dans des couvertures, leurs silhouettes à peine visibles dans l'ombre.",
            "Un artiste, seul, assis sur un petit tabouret, peint en silence le ciel étoilé, ses pinceaux glissant délicatement sur la toile.",
            "Les lumières des boutiques fermées projettent des ombres longues et tranquilles, comme si la ville entière retenait son souffle.",
            "Vous entendez le léger bruit de l’eau couler à la laverie du village, où quelques hommes et femmes frottent leurs vêtements sur des planches de bois.",
            "Le claquement des planches de la laverie résonne doucement, accompagné par les murmures des quelques personnes qui travaillent encore si tard.",
            "Un lampadaire grésille faiblement avant de s’éteindre, ajoutant à la sensation d’une ville qui s’éteint lentement avec la nuit.",
            "L'air est frais, et une légère brume commence à s'élever au niveau des pavés, baignant la rue dans une lueur mystique.",
            "Les vitrines des boutiques sont obscures, mais des reflets de lumière dansent encore sur les fenêtres, créant des jeux d’ombre et de lumière.",
            "Un sans-abri tourne lentement sur un banc, cherchant un peu plus de confort sous sa couverture usée, tandis que les torches vacillent dans la nuit.",
            "Les portes des boutiques sont fermées et silencieuses, mais vous pouvez encore sentir l’écho de l’agitation du jour flotter dans l’air.",
            "Le ciel étoilé est clair, sans nuages, et semble veiller sur le quartier endormi comme un manteau protecteur.",
            "Les rares passants marchent tranquillement, le bruit de leurs pas résonnant faiblement dans la rue vide.",
            "Une enseigne de néon clignote encore faiblement, attirant l’attention dans la pénombre, seule source de mouvement dans cette rue figée.",
            "Vous entendez des rires étouffés en provenance d’un coin sombre, où deux marchands finissent leur conversation nocturne avant de rentrer.",
            "Le vent fait bruisser doucement les bannières abandonnées, leur présence fantomatique rappelant l’effervescence qui animait la rue plus tôt dans la journée."
        ]

    description_a_afficher = random.choice(liste_descriptions_possibles)
    print(description_a_afficher)
    services.Affichage.EntreePourContinuer()


@salle_de_type("CHEMIN_CHAMPS")
def reveler_chemin_champs(etage, salle):
    if  services.Sove.ModifieTagsDansSove("Checke", "Village Jour"):
        liste_descriptions_possibles = [
            "Les personnes autour de vous sont immobiles ou marchent sans but, leurs yeux vides, comme si elles attendaient une fin qui ne viendra jamais.",
            "Vous croisez un homme assis par terre, la tête baissée, ses mains recouvertes de poussière, son regard complètement vide.",
            "Un silence lourd règne ici, entrecoupé seulement par le bruit de pas traînants et le léger sifflement du vent sur la terre battue.",
            "À l'ouest, la gigantesque déchetterie s'étend à perte de vue, une abomination où des objets tombent du ciel dans une pluie lente et macabre.",
            "Des êtres sans âge fouillent les déchets avec des gestes mécaniques, comme s’ils cherchaient quelque chose qu’ils ne trouveront jamais.",
            "L'odeur des déchets flotte dans l'air, âcre et étouffante, comme si elle voulait s'infiltrer dans votre âme elle-même.",
            "Un homme passe à côté de vous, son corps courbé par le temps, mais son visage est figé dans une expression de vide absolu.",
            "Les objets qui tombent du ciel se mêlent aux déchets, certains encore brillants, d'autres déformés et grotesques, dégageant une aura profondément dérangeante.",
            "Les immenses tas de détritus semblent vous observer, leur présence insupportable comme une entité vivante et malveillante.",
            "Vous ressentez une répulsion instinctive à l’approche de la déchetterie, comme si quelque chose de profondément mauvais s’y trouvait, quelque chose d'invisible mais palpable.",
            "Les personnes dans le champ, allongées ou debout, ne semblent plus être là, physiquement présentes mais déjà disparues dans leur esprit.",
            "Un bruit sourd retentit à l'ouest, un autre objet vient de tomber du ciel dans les déchets, créant un écho sinistre dans cet espace déjà pesant.",
            "Les déchets, tordus et grotesques, semblent dégager une énergie sombre qui vous fait frissonner, comme si une partie de vous voulait fuir cet endroit.",
            "Certains des gens autour de vous fouillent dans les détritus sans aucune expression, comme des marionnettes manipulées par un désir inconscient.",
            "Vous regardez au loin, et le champ semble s'étendre à l'infini, avec ces silhouettes humaines figées dans une attente qui semble éternelle.",
            "Le ciel au-dessus de la déchetterie semble plus sombre, presque menaçant, comme si l'endroit lui-même corrompait la lumière qui passe à travers.",
            "Les visages des personnes que vous croisez n'ont plus d'émotion, juste une lassitude profonde, comme s'ils avaient perdu toute volonté de vivre.",
            "L'aura des déchets est presque palpable, une présence insidieuse qui semble s'accrocher à votre esprit, vous poussant à détourner le regard.",
            "À chaque fois que vous regardez vers la déchetterie, vous avez l’impression qu’elle vous attire, comme un gouffre sans fond prêt à vous engloutir.",
            "Les gens autour de vous errent comme des ombres, leurs corps présents mais leurs esprits déjà ailleurs, dans une sorte de non-existence dénuée de toute lumière."
        ]

    else:
        liste_descriptions_possibles = [
            "La nuit a enveloppé le champ, mais les silhouettes des gens immobiles sont toujours visibles, leurs yeux vides brillants dans la faible lueur des étoiles.",
            "Le silence est encore plus lourd la nuit, seulement brisé par des bruits lointains de pas et des murmures indistincts, comme des échos d'un autre monde.",
            "Dans l’obscurité, les silhouettes allongées sur la terre battue semblent être des ombres plus que des êtres vivants, figées dans leur attente sans fin.",
            "La déchetterie à l’ouest est encore plus effrayante la nuit, ses monticules d'ordures se dressant comme des monstres immobiles sous le ciel étoilé.",
            "Des objets continuent de tomber du ciel dans la déchetterie, mais la nuit rend leur chute presque fantomatique, comme s’ils se matérialisaient depuis l’obscurité elle-même.",
            "Les gens errants dans la nuit semblent plus proches d’esprits que d’humains, leurs mouvements lents et dénués de vie, comme des spectres prisonniers du temps.",
            "Un faible vent souffle, soulevant des volutes de poussière dans l'air nocturne, et vous donne l’impression que même l’air ici est vieux et fatigué.",
            "La lumière de la lune éclaire faiblement les déchets, révélant des formes tordues et monstrueuses qui dégagent toujours cette aura malveillante et repoussante.",
            "Les rares bruits venant de la déchetterie sont amplifiés par le silence de la nuit, des craquements étranges et des chutes qui résonnent comme des chuchotements sinistres.",
            "Les personnes dans le champ, immobiles ou errantes, sont enveloppées d'une ombre profonde, comme si elles faisaient partie intégrante de la nuit elle-même.",
            "L'obscurité semble rendre les déchets encore plus hostiles, chaque monticule prenant la forme de quelque chose de vivant, quelque chose de corrompu.",
            "Vous avez l'impression que l’air est plus lourd près de la déchetterie, comme si une présence invisible et oppressante se répandait depuis les tas d’ordures.",
            "Le ciel étoilé au-dessus du champ est vaste, mais les étoiles semblent lointaines et froides, indifférentes aux âmes perdues qui hantent ce lieu.",
            "Les ombres des gens errant près de la déchetterie se fondent presque avec les montagnes de détritus, créant des silhouettes indistinctes et inquiétantes dans la nuit.",
            "Le champ semble sans fin dans la nuit, chaque pas vous rapprochant d’un vide encore plus profond, où ni lumière ni vie ne subsistent.",
            "Un murmure sourd traverse le champ, un son que vous ne pouvez ni localiser ni comprendre, comme si les âmes errantes parlaient dans un langage oublié.",
            "Les objets qui tombent du ciel dans la nuit semblent plus menaçants, comme s’ils s’écrasaient dans la déchetterie avec une intention malveillante.",
            "La faible lumière de la lune fait briller certaines parties des ordures dans la déchetterie, créant des reflets malsains et déformés, presque vivants.",
            "Les yeux des gens que vous croisez dans la nuit sont vides, mais leur vide semble absorber la lumière, comme des puits sans fond dans lesquels toute clarté disparaît.",
            "Vous avez l’impression que même le temps ralentit ici la nuit, chaque seconde s'étirant à l’infini, laissant une trace de désespoir silencieux dans l’air froid.",
            "..?\nVous voyez un homme a l'extreme Nord-Ouest, sur un talus de déchet... "
        ]

    description_a_afficher = random.choice(liste_descriptions_possibles)
    print(description_a_afficher)
    services.Affichage.EntreePourContinuer()


@salle_de_type("VILLAGE_CHAMPS")
def reveler_village_champs(etage, salle):
    print("Vous trouvez un simple panneau de bois, a moitié enfoncé dans le sol, sur lequel est peint un message en grandes lettres :")
    print("*VERS : CHAMPS ET DECHETTERIE*")
    services.Affichage.EntreePourContinuer()


@salle_de_type("VILLAGE_ARENE")
def reveler_village_arene(etage, salle):
    print("Vous trouvez deux colonnades de marbres enserrant le chemin.")
    print("Accroché en hauteur, il y a une pancarte sur laquelle est peint un paysage dans lequel trone un Colysée.")
    services.Affichage.EntreePourContinuer()


@salle_de_type("VILLAGE_COMMERCIAL")
def reveler_village_commercial(etage, salle):
    print("Vous trouvez un panneau de métal, a moitié enfoncé dans le sol, sur lequel sont soudés plusieurs symboles.")
    print("On peut voir un marteau, une fiole, un dollars, une petite boite noire, et une feuille, entourant les mots *VERS : QUARTIER COMMERCIAL*.")
    services.Affichage.EntreePourContinuer()


@salle_de_type("ANCIEN")
def reveler_ancien(etage, salle):
    if services.Sove.ModifieTagsDansSove("Checke", "Village Jour"):
        # De jour, l'Ancien est aux champs : son emplacement se comporte comme le chemin.
        reveler_chemin_champs(etage, salle)
        return
    print("Vous trouvez un vieil homme habillé en plaid et beret traditionnel assis sur un tas de déchet, regardant la lune.")
    print("Après quelques efforts, vous arrivez en haut du monticule, et vous asseyez a coté de lui.")
    services.Affichage.EntreePourContinuer()
    services.Trader.DoAncien()
    print("Vous admirez la lune encore quelques instants, avant de dévaller la pente du tas de dechet sur les fesses, et de repartir.")
    services.Affichage.EntreePourContinuer()


@salle_de_type("HOTEL")
def reveler_hotel(etage, salle):
    print("Vous vous approchez d'une batisse de bois type Western, avec des portes a double battant.")
    print("A l'interieur, certaines figures fantomatiques boivent des liquides divers et variés alors que d'autre montent a l'étage pour y passer la nuit.")
    services.Affichage.EntreePourContinuer()
    audio.CHANNELMUSIQUEDEBASE.set_volume(0.5)
    PermanentPlaySFX("noise")
    services.Trader.DoHotel()
    audio.CHANNELSFX.set_volume(0)
    attendre(0.01)
    audio.CHANNELSFX.stop()
    audio.CHANNELMUSIQUEDEBASE.set_volume(1)
    print("Vous repassez dramatiquement les portes battantes du saloon. C'est a dire, en donnant un grand coup de pied dedans.")
    services.Affichage.EntreePourContinuer()


@salle_de_type("ANCIENNE")
def reveler_ancienne(etage, salle):
    print("Vous vous approchez d'une vieille batisse en ruine, style colonnades romaines...")
    if  services.Sove.ModifieTagsDansSove("Checke", "Village Jour"):
        print("...mais il n'y a personne.")
        services.Affichage.EntreePourContinuer()
    else:
        print("...et distinguez une forme dans la pénombre d'une des colonnes.")
        services.Affichage.EntreePourContinuer()
        services.Trader.DoChamane()
    print("...vous laissez le temple en ruine derrière vous.")
    services.Affichage.EntreePourContinuer()


@salle_de_type("JARDIN")
def reveler_jardin(etage, salle):
    if  services.Sove.ModifieTagsDansSove("Checke", "Village Jour"):
        audio.CHANNELMUSIQUEDEBASE.set_volume(0.5)
        PermanentPlaySFX("garden_ambiance")
        services.Affichage.ParlerAvecLeDirecteur()
        audio.CHANNELSFX.set_volume(0)
        attendre(0.01)
        audio.CHANNELSFX.stop()
        audio.CHANNELMUSIQUEDEBASE.set_volume(1)
    else:
        print("Le portail du jardin de la grande demeure est fermé.")
        services.Affichage.EntreePourContinuer()


@salle_de_type("MAITRE_ARTEFACT")
def reveler_maitre_artefact(etage, salle):
    if  services.Sove.ModifieTagsDansSove("Checke", "Village Jour"):
        print("Vous regardez à l'interieur de l'échoppe, et un vieil homme vous fait signe.")
        services.Affichage.EntreePourContinuer()
        etage.DoTransition("In", salle["type"])
        services.Trader.DoArtefactTrading()
        print("Vous saluez respectueusement le Maitre, et sortez de l'échoppe.")
        services.Affichage.EntreePourContinuer()
        etage.DoTransition("Out", salle["type"])
    else:
        print("Vous tentez d'ouvrir la porte de l'échoppe, mais elle résiste a tout vos efforts.")
        services.Affichage.EntreePourContinuer()
