"""Salles à énigme ou à mécanisme : séquences, leviers, plaques, puits, mini-jeux."""

import random

from coliseum import services
from coliseum.audio import PlayMusic, PlayMusicDeLetage, PlaySound, StopAllMusic
from coliseum.console import ClearConsole
from coliseum.donnees.actions import LISTESORTS, LISTETECHNIQUES
from coliseum.donnees.items import LISTEITEM
from coliseum.histoire.village import CheckForKIA
from coliseum.interface.jukebox import doPiano
from coliseum.outils import GetRandomItemFromList
from coliseum.combat.lancement import livrer_combat
from coliseum.exploration.salles.registre import salle_de_type


@salle_de_type("COEUR")
def reveler_coeur(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.coeur()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    if services.Player.numero_de_letage == 2 :
        print("Vous arrivez dans une clairière artificielle, au centre de laquelle se tient une lame magnifique encastrée dans un rocher.")
        print("Loin au dessus du rocher, vous apercevez une ouverture cerclée de vieille pierre.")
        services.Affichage.EntreePourContinuer()
        print("Les racines des arbres environnant semblent converger au niveau du rocher.")
        services.Affichage.EntreePourContinuer()
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
            services.Affichage.EntreePourContinuer()
        else:
            print("Vous vous approchez de la roche, et posez vos main sur le paumeau de l'épée.")
            if services.Player.nom_de_letage == "Jungle Cruelle":
                print("Aussitot, les sons de la forêt se taisent.")
                services.Affichage.EntreePourContinuer()
                print("Vous sentez les arbres pale étendre les racines sous la surface du sol, comme pour tenter de vous attraper, ou de vous arreter.")
                services.Affichage.EntreePourContinuer()
                print("Des cris a glacer le sang émanent de tout les cotés, et vous remarquez enfin la grosse tache de sang tout autour du rocher, a moitié absorbée.")
                services.Affichage.EntreePourContinuer()
                print("Votre poul s'accélère, et vous tirez de toutes vos forces sur la lame...")
                services.Affichage.EntreePourContinuer()
                print("..qui finit enfin par sortir de son fourreau de pierre, révélant en dessous un coeur de bois se vidant d'une sève couleur cendre.")
                services.Affichage.EntreePourContinuer()
                print("Les cris se taisent, et la forêt meurt.")
                services.Affichage.EntreePourContinuer()
                print("Alors que vous prenez enfin toute la gravité de vos actions, vous observez la lame, qui luit doucement dans votre main.")
                print("Son apparence trompeuse a laissé place a un artefact rongé par la rouille, mais qui semble attirer le mana.")
                services.Affichage.EntreePourContinuer()
                print("Vous obtenez l'artefact [Lame Spectrale] !")
                print("Lorsqu'un ennemi brise son réservoir de mana, vous retrouvez jusqu'à 30% de vos points de mana maximum !")
                salle["terminé par joueur"] = True
                services.FloorMaker.GiveRandomArtefact("Lame Spectrale","Don")
                services.Affichage.EntreePourContinuer()
                print("Vous vous éloignez de la clairière.")
                services.Affichage.EntreePourContinuer()
            else:
                print("Aussitot, les sons de la forêt se taisent.")
                services.Affichage.EntreePourContinuer()
                print("Un vent violent se lève, alors que vous soulevez la lame de son piédestal.")
                services.Affichage.EntreePourContinuer()
                print("Vous finissez par sortir entièrement l'épée de son rocher, et découvrez en dessous un coeur de bois désséché dans lequel le métal était planté.")
                services.Affichage.EntreePourContinuer()
                print("Et alors que vous observez votre nouvelle arme...")
                services.Affichage.EntreePourContinuer()
                print("...Zeroual grandit...")
                services.Affichage.EntreePourContinuer()
                print("...enveloppe l'arme...")
                services.Affichage.EntreePourContinuer()
                print("...et l'avale d'un coup.")
                services.Affichage.EntreePourContinuer()
                print("La ou se tenait auparavant un artefact splendide arraché a un lieu magique, il y a maintenant une marque ésotérique gravée sur la peaume de votre main.")
                services.Affichage.EntreePourContinuer()
                print("Vous obtenez l'artefact [Marque du Tyrant] !")
                print("Lorsque vous finissez un combat avec toute votre vie, vous gagnez un point de vie max supplémentaire !")
                print("De plus, le nombre de monstre que vous avez tué augmente de 5, pour une raison quelquonque !")
                salle["terminé par joueur"] = True
                services.FloorMaker.GiveRandomArtefact("Marque du Tyrant","Don")
                services.Player.nombre_de_monstres_tues += 5
                services.Affichage.EntreePourContinuer()
                print("Vous vous éloignez de la clairière.")
                services.Affichage.EntreePourContinuer()
    elif services.Player.numero_de_letage == 7:
        print("Vous arrivez dans une salle circulaire, contenant en son centre un piedestal griffoné de centaines de messages sans queue ni tête.")
        print("Loin au dessus du piedestal, vous apercevez une ouverture cerclée de vieille pierre.")
        services.Affichage.EntreePourContinuer()
        print("Une roche est posée sur le piedestal.")
        if services.Player.nom_de_letage != "Douves du Pénitent":
            print("Elle est enflammée, des dizaines de spectres de feu virevoltant autour d'elle dans une cacophonie de lamentations et d'accusations.")
        else:
            print("Elle est en dessous d'une cascade émanant de l'ouverture de pierre plus haut qui répand ses eaux sur la totalité de l'étage, et se pare d'une couleur sombre comme le charbon.")
        services.Affichage.EntreePourContinuer()
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
            services.Affichage.EntreePourContinuer()
        else:
            print("Vous vous approchez de la pierre, et posez votre main dessus.")
            services.Affichage.EntreePourContinuer()
            if services.Player.nom_de_letage == "Douves du Pénitent":
                print("Alors que vous la sortez de l'eau, sa couleur disparait comme si elle n'était qu'un simple rêve.")
                services.Affichage.EntreePourContinuer()
                print("Vous observez la simple pierre, qui se révèle être un jade intrigant contenant une plus petite roche dorée.")
                services.Affichage.EntreePourContinuer()
                print("Alors que vous la tenez dans votre main, vous jureriez entendre des sanglots autour de vous.")
                services.Affichage.EntreePourContinuer()
                print("Vous obtenez l'artefact [Jade Impardonnable] !")
                print("La cristallisation de centaines d'années de culpabilité.\nLorsque vous passez votre tour avec tout vos points de mana, vous entrez dans un état de folie pendant 1 tour !")
                salle["terminé par joueur"] = True
                services.FloorMaker.GiveRandomArtefact("Jade Impardonnable","Don")
                services.Affichage.EntreePourContinuer()
                print("Vous vous éloignez de la salle.")
                services.Affichage.EntreePourContinuer()
            else:
                print("Alors que vous commencez a grimacer sous l'effet du feu qui enveloppe la pierre....")
                services.Affichage.EntreePourContinuer()
                print("...vous vous rendez compte qu'il ne vous brule pas.")
                services.Affichage.EntreePourContinuer()
                print("Au contraire, il semble apaiser quelque chose de singulier, de primitif, enfoui a l'interieur de votre ADN.")
                services.Affichage.EntreePourContinuer()
                print("Vous sentez en vous un plaisir coupable, ressentit seulement après la réalisation d'une vengence.")
                services.Affichage.EntreePourContinuer()
                print("Un plaisir couplé a une colère grandissante, comme un besoin de prouver une quelquonque supériorité?")
                services.Affichage.EntreePourContinuer()
                print("Vous vous réfugez dans le confort de fortes émotions, et commencez un rire maniaque alors que les spectres de feu dansent autour de vous !")
                services.Affichage.EntreePourContinuer()
                print("...")
                services.Affichage.EntreePourContinuer()
                print("Quand vous reprenez vos esprits, vous êtes a terre, sans vêtements, des marques de brulures scarifiants les murs de la salle comme de la peau sur laquelle on défoulerait ses émotions.")
                services.Affichage.EntreePourContinuer()
                print("Dans votre main gauche, Zeroual avec 10 âmes aborbées d'on ne sait ou.")
                services.Affichage.EntreePourContinuer()
                print("Dans votre main droite, la pierre calcinée du piedestal.")
                services.Affichage.EntreePourContinuer()
                print("Plus aucun feu ne brule dans la salle.")
                print("Plus aucun spectres ne répandent leur colère.")
                services.Affichage.EntreePourContinuer()
                print("La salle est vide.")
                services.Affichage.EntreePourContinuer()
                print("Vous obtenez l'artefact [Basalte Immonde] !")
                print("Une roche impure, ayant absorbée les joies d'une colère sans limite pendant des centaines d'années.\nLorsque vous passez votre tour avec tout vos points de mana, vous entrez dans un état de furie pendant 1 tour !")
                print("De plus, le nombre de monstre que vous avez tué augmente de 10, pour une raison quelquonque !")
                salle["terminé par joueur"] = True
                services.FloorMaker.GiveRandomArtefact("Basalte Immonde","Don")
                services.Affichage.EntreePourContinuer()
                print("Vous vous rhabillez, et vous éloignez de la salle.")
                services.Affichage.EntreePourContinuer()
    elif services.Player.numero_de_letage == 5:
        StopAllMusic()
        PlayMusic("wind")
        print("Vous arrivez sur un sol de bois noir, grinçant sous le pied.\nDe part et d'autres de ce sol se trouvent des rangées de sièges qui découpent l'horizon en infinis de satins et d'obscurité.\nBien au dessus de votre tête, vous apercevez la sortie d'un puit de pierre.")
        services.Affichage.EntreePourContinuer()
        print("Un piano au centre de la scène semble pleurer une vieille mélodie.\nVous vous approchez plus près pour observer la partition jouée par l'instrument, mais a sa place...")
        if services.Player.nom_de_letage != "Carnaval de Rouille" and "Demi-Masque de l'Ordre" not in services.Player.liste_dartefacts_optionels:
            print("... se trouve un demi-masque triste, en équilibre sur le pupitre.")
        elif services.Player.nom_de_letage == "Carnaval de Rouille" and "Demi-Masque du Chaos" not in services.Player.liste_dartefacts_optionels:
            print("... se trouve un demi-masque souriant, en équilibre sur le pupitre.")
        else:
            print("... il n'y a rien.")
        services.Affichage.EntreePourContinuer()
        while True:
            while True:
                try:
                    print("Que faire ?")
                    print("\n1 - S'éloigner\n2 - Ecouter le piano")
                    if "Demi-Masque du Chaos" not in services.Player.liste_dartefacts_optionels and "Demi-Masque de l'Ordre" not in services.Player.liste_dartefacts_optionels :
                        print("3 - Prendre le demi-masque")
                    else :
                        print("")
                    choix = int(
                        input("\nChoisissez votre action avec les nombres : ")
                    )
                    ClearConsole()
                    if (("Demi-Masque du Chaos" not in services.Player.liste_dartefacts_optionels and "Demi-Masque de l'Ordre" not in services.Player.liste_dartefacts_optionels and choix in [1, 2, 3]) or choix in [1, 2]):
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print("Vous vous éloignez de la salle.")
                services.Affichage.EntreePourContinuer()
                PlayMusicDeLetage()
                break
            elif choix == 2:
                StopAllMusic()
                print("Vous fermez les yeux, et vous concentrez sur la faible mélodie qui émane du piano.")
                PlayMusic("lumisade")
                services.Affichage.EntreePourContinuer()
                if services.Player.nom_de_letage != "Carnaval de Rouille" :
                    print("...vous pouvez maintenant dire que le tempo est bizarre, comme si la performance était faite d'une main mal assurée.\nCelle d'un débutant.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous avez bien mieux joué sur le clavecin.")
                    services.Affichage.EntreePourContinuer()
                    print("Satisfait de votre découverte, vous laissez derrière vous le piano mélancolique.")
                else:
                    print("Vous tentez alors de reproduire la mélodie en posant vos doigt sur les touches, mais aucun son ne sort.")
                    services.Affichage.EntreePourContinuer()
                    print("A l'interieur du piano, il n'y a aucune corde.")
                    services.Affichage.EntreePourContinuer()
                    print("Bizarre. C'est peut etre un piano d'agrément, construit pour la décoration plus que le divertissement.")
                    services.Affichage.EntreePourContinuer()
                    print("Quel est donc le nom de ce piano sans corde et qui émet quand même du son ?")
                    services.Affichage.EntreePourContinuer()
                    print("Vous penchez la tête et trouvez une référence...singulière.")
                    services.Affichage.EntreePourContinuer()
                    print("Sur le coté du piano, se trouve une étiquette jaunie par le temps, sur laquelle on peut lire les mots\n\n[https://www.onlinepianist.com/virtual-piano]\n\n")
                    services.Affichage.EntreePourContinuer()
                    print("C'est quoi ce nom bizarre ?")
                    services.Affichage.EntreePourContinuer()
                    print("Vous laissez le piano bizarre tranquille.")
                StopAllMusic()
                PlayMusic("wind")
                services.Affichage.EntreePourContinuer()
            else:
                print("Vous vous approchez du demi-masque, et posez votre main dessus.")
                services.Affichage.EntreePourContinuer()
                if services.Player.nom_de_letage == "Carnaval de Rouille":
                    print("Des rires emplissent votre esprit.\nEtrangers, comme le chuchotement d'une rivière oubliée... ")
                    services.Affichage.EntreePourContinuer()
                    print("...mais devenant vite familier, comme un vetement neuf qui s'adapte trop lentement a la forme du corps.")
                    services.Affichage.EntreePourContinuer()
                    print("Comme une réaction inconfortable que l'on apprend au fur et a mesure.\nUne manière de réfléchir, de penser, d'être, acquise dans la panique et l'anxiété.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous tentez de retirer votre main de l'artefact, mais vous rendez compte que celui ci a disparu.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous cherchez partout, mais t- ne trouvera rien. Pas la moindre once de pitié.")
                    services.Affichage.AfficheAvecUnTempsDattente(2)
                    print("Les tribunes sont vides, pour qui donc performez-vous pareil acte ?")
                    services.Affichage.AfficheAvecUnTempsDattente(1.9)
                    print("Un chien. Vous êtes un chien. Et tu sais ce qu'on dit d'un chien qui n'arrivent pas a apprendre de nouveaux tours ?")
                    services.Affichage.AfficheAvecUnTempsDattente(1.8)
                    print("Ou se trouvent donc ces lignes que vous lisez d'une voix tremblotante ?")
                    services.Affichage.AfficheAvecUnTempsDattente(1.7)
                    print("Encore ! Encore ! Que diable, enfin un peu de divertisement dans ce chateau miteux !")
                    services.Affichage.AfficheAvecUnTempsDattente(1.6)
                    print("Il ne doit rien savoir. Mais ce n'est pas les gens du chateau qui te trahiront, ils sont déja au courant et il ne s'est toujours rien passé.")
                    services.Affichage.AfficheAvecUnTempsDattente(1.5)
                    print("Je sais qui tu es.")
                    services.Affichage.AfficheAvecUnTempsDattente(2)
                    print("Ne trouve donc tu  pas ca hilarant, la manière qu'à le destin de rapprocher les opposés ..? Les gens qui ne doivent pas etre ensembles ?")
                    services.Affichage.AfficheAvecUnTempsDattente(1.4)
                    print("Tu ne peut pas venir ? A cause de ta famille ? Eh bien...")
                    services.Affichage.AfficheAvecUnTempsDattente(1.3)
                    print("Les gens qui ne peuvent pas être ensemble ..?")
                    services.Affichage.AfficheAvecUnTempsDattente(1.2)
                    print("...voila ! Tu n'as maintenant plus de famille. Allez, en route !")
                    services.Affichage.AfficheAvecUnTempsDattente(1.1)
                    print("Les gens qui ne doivent pas etre ensembles ..?")
                    services.Affichage.AfficheAvecUnTempsDattente(1)
                    print("Plus vite , que diable. Il fait froid !")
                    services.Affichage.AfficheAvecUnTempsDattente(1)
                    print("Tu peut poser tes doigts sur ces touches pour avoir plus de mobilité sur le piano.")
                    services.Affichage.AfficheAvecUnTempsDattente(1.2)
                    print("Et alors ? Tu était si drole la bas ! Et maintenant, c'est a peine si...")
                    services.Affichage.AfficheAvecUnTempsDattente(1.6)
                    print("Représentation ce soir a vingt-heures. J'espère pour toi que tu as d'autres blagues en stock, sinon...")
                    services.Affichage.AfficheAvecUnTempsDattente(1.9)
                    print("C'est ça ! Tu es prodigieux !")
                    services.Affichage.AfficheAvecUnTempsDattente(0.9)
                    print("...tu arrive a esquisser un sourire.")
                    services.Affichage.AfficheAvecUnTempsDattente(0.8)
                    print("...tu passera sur le fil de la guillotine. Désolé. Ordres du roi.")
                    services.Affichage.AfficheAvecUnTempsDattente(0.9)
                    print("Ces blagues là marcheront bien sur lui, mais le reste...")
                    services.Affichage.AfficheAvecUnTempsDattente(0.9)
                    print("Eh bien ! Sacré changement comparé a hier !")
                    services.Affichage.AfficheAvecUnTempsDattente(1.3)
                    print("Mais qu'as tu donc écrit ? Je sais que l'humour est subjectif, mais tu t'approche trop près de...")
                    services.Affichage.AfficheAvecUnTempsDattente(1.9)
                    print("Hillarant ! J'en veux de nouvelles comme ca pour demain meme heure. Non ! Tu as une heure ! J'en veux d'autres maintenant !")
                    services.Affichage.AfficheAvecUnTempsDattente(1.9)
                    print("Ce n'est pas drôle.")
                    services.Affichage.AfficheAvecUnTempsDattente(0.8)
                    print("C'est génial !")
                    services.Affichage.AfficheAvecUnTempsDattente(0.8)
                    print("Tu es fou .")
                    services.Affichage.AfficheAvecUnTempsDattente(0.7)
                    print("Tu es incroyable !")
                    services.Affichage.AfficheAvecUnTempsDattente(0.7)
                    print("Reprend toi bon sang ! Ne le laisse pas te...")
                    services.Affichage.AfficheAvecUnTempsDattente(0.8)
                    print("Ah non hein, j'aimais bien ton nouveau répertorie, remet y un peu de gore pardis ! Sinon...")
                    services.Affichage.AfficheAvecUnTempsDattente(0.9)
                    print("Il faut que tu parte. Que tu fuie.")
                    services.Affichage.AfficheAvecUnTempsDattente(0.7)
                    print("Attention, ca manque de concret, de dangereux, de sale. Bourreau, faites donc aiguiser...")
                    services.Affichage.AfficheAvecUnTempsDattente(1)
                    print("S'il te plait, tu es la seule personne ici qui...")
                    services.Affichage.AfficheAvecUnTempsDattente(0.8)
                    print("Oh ?")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("J'aime ta motivation.")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Ca doit faire mal , non ?")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Mais le timing était parfait. Et c'est le plus important dans la comédie !")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Souriez, bouseux. Vous venez d'assurer votre place au sein du chateau...")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("...mais bouseux, ca fait trop bizarre. Voyons, il faudrait un nom avec la même sonorité...")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Ah ! Je l'ai !")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Tu t'apellera Bouffon. C'est ton nouveau nom de scène.")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("-rouvez rien. Mais c'est pas grave, car les voix dans votre esprit se sont enfin tues.")
                    services.Affichage.EntreePourContinuer()
                    print("Et le masque ?")
                    services.Affichage.EntreePourContinuer()
                    print("Vous le portez déja.")
                    services.Affichage.EntreePourContinuer()
                    print("En vous.")
                    services.Affichage.EntreePourContinuer()
                    print("Sur votre coeur.")
                    services.Affichage.EntreePourContinuer()
                    print("Pour que p e r s o n n e ne puisse le voir.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous obtenez l'artefact [Demi-Masque du Chaos] !")
                    print("Une séparation opaque entre votre coeur et une folie particulière, née dans la fracturation de l'âme, et baignant dans un nauséabond liquide ammniotique de pure anxiété.\nLes orbes de folie agissent pendant un tour supplémentaire !")
                    services.FloorMaker.GiveRandomArtefact("Demi-Masque du Chaos","Don")
                    services.Affichage.EntreePourContinuer()
                    print("Un masque ? Cacher un masque ? Le truc que l'on crée pour cacher la personne qui le porte ?")
                    services.Affichage.EntreePourContinuer()
                    print("Cacher le masque plutot que la personne...")
                    services.Affichage.EntreePourContinuer()
                    print("H I L A R A N T")
                    services.Affichage.AfficheAvecUnTempsDattente(0.8)
                else:
                    print("Des paroles emplissent votre esprit.\nElles rayonnent de sagesse, et ont le gout de la fiertée du père.")
                    services.Affichage.EntreePourContinuer()
                    print("Des mots doux, réconfortants, qui réchauffent le corps fatigué par la neige environnante...")
                    services.Affichage.EntreePourContinuer()
                    print("?\nD'ou vient cette neige ?")
                    services.Affichage.EntreePourContinuer()
                    print("Vous regardez , impuissant, une neige surnaturelle tomber autour de vous !")
                    services.Affichage.EntreePourContinuer()
                    print("Vos pas s'enfoncent et crissent, vous cherchez désespérément l'entrée de la salle, et tombez nez a nez devant une falaise impossiblement grande !")
                    services.Affichage.EntreePourContinuer()
                    print("La montagne tout autour de vous se met a rugir, et vous ne pouvez que vous proteger alors qu'une gigantesque avalanche s'écrase sur votre frèle corps..")
                    services.Affichage.EntreePourContinuer()
                    print("...et vous emporte profondément dans le froid...")
                    services.Affichage.EntreePourContinuer()
                    print("...plus profondément encore...")
                    services.Affichage.EntreePourContinuer()
                    print("......plus....profondément....encore....")
                    services.Affichage.EntreePourContinuer()
                    print("..............plus.............profondément..............encore..........")
                    services.Affichage.EntreePourContinuer()
                    print("...")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Tu peux poser tes mains ici.")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Voila, tu vois ? Si tu les écartes de cette manière, tu va pouvoir toucher toute ces touches en meme temps.")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Quoi ?")
                    services.Affichage.AfficheAvecUnTempsDattente(2)
                    print("Bien sûr que ca te servira plus tard ! Les invités de notre hotel ne se contenteront pas de ces petites musiques que tu as appris !")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Les véritables chefs ont composé des mélodies si complexes, meme ton vieux pere ne saurait comment les jouer.")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Mais ce n'est pas grave, va. Pour l'instant, c'est suffisant. Tu es encore jeune, et je ne vais pas mourir demain !")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Je veux juste que tu sois prêt.")
                    services.Affichage.AfficheAvecUnTempsDattente(2)
                    print("Vois tu, un homme ne peut se contenter d'une seule corde a son arc.")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Tu te débrouille très bien avec la gestion du personnel, des clients, et du materiel. Mais vois tu, c'est dans les détails que se cachent les choses les plus importantes.")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Imagine donc, tu rentre dans un hotel, et le patron descend te souhaiter la bienvenue.\nLes chambres sont propres.\nLes services proposés sont a la hauteur de ce a quoi tu t'attend.")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Et alors que tu t'assoie a une table pour prendre un diner de haute qualité...")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("...le patron s'assoie sur le piano au centre de la pièce...")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("...et se met a jouer une symphonie ravissante.")
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print("Crois moi mon grand, si la surprise ne se lira pas sur ton visage, c'est parce que tu sera trop occupé a parler de l'experience a tes amis !")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Et puis, de manière plus générale, c'est satisfaisant d'apprendre.\nDe changer, sans se changer.")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Qui sait, ton talent au piano, ca sera peut etre la chose qui te fera rencontrer ton âme soeur !")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Je rigole, je rigole. Ne me regarde donc pas comme ca, voyons !")
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print("...")
                    services.Affichage.AfficheAvecUnTempsDattente(2)
                    print("...dis moi, fiston.")
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print("Le roi a préparé une visite pour dans quelques semaines.")
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print("Apparemment, son comportement est aussi détestable que l'hiver est froid en ces montagnes.")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Et il déteste le froid encore plus qu'il n'est détestable.")
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print("Quand il sera la, il se défoulera surement sur de pauvres gens.")
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print("Promet moi...")
                    services.Affichage.AfficheAvecUnTempsDattente(1)
                    print("Promet moi d'être fort.")
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print("Promet moi de respecter sa volontée, quoi qu'elle soit.")
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print("Promet moi de faire tout ce qu'il demande, sans broncher.")
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print("Ne te met pas en danger, ne te met pas en avant, reste donc tranquille, et souris.")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Je ne veux pas qu'il salisse ton talent ou qu'il viole ton héritage.")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Je veux que tu devienne un talentueux pianiste et un fier directeur d'hotel.")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("J'ai peur pour toi tu sais, plus que j'ai peur pour ces vieux os.")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Mais j'aime ta motivation.")
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print("Ca doit faire mal de devoir supporter un tel fardeau , non ?")
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print("Mais ton futur est parfait. Et c'est le plus important dans la ce cruel monde !")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Souris, fiston. Tu va assurer ta place au sein du Lumisade...")
                    services.Affichage.AfficheAvecUnTempsDattente(3)
                    print("...mais avec ton nom, tu risque de t'attirer des ennuis. Voyons, il faudrait quelque chose qui ne fasse pas penser a ce pays...")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Ah ! Je l'ai !")
                    services.Affichage.AfficheAvecUnTempsDattente(2)
                    print("Tu t'apellera *Le Pianiste*. C'est ton nouveau nom de scène.")
                    services.Affichage.AfficheAvecUnTempsDattente(4)
                    print("Vous ouvrez les yeux devant un cadavre calciné, au milieu d'une batisse en ruine.")
                    services.Affichage.EntreePourContinuer()
                    print("Une voix âcre comme le charbon résonne dans votre crâne :")
                    services.Affichage.EntreePourContinuer()
                    print("*C'est bon, tu n'as plus rien qui te retient ici désormais. Allez, viens avec moi maintenant.*")
                    services.Affichage.EntreePourContinuer()
                    print("*On retourne au Chateau.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Et plus vite que ca.*")
                    services.Affichage.EntreePourContinuer()
                    print("*J e  d é t e s t e  l e  f r o i d .*")
                    services.Affichage.EntreePourContinuer()
                    print("Vous obtenez l'artefact [Demi-Masque de l'Ordre] !")
                    print("Une amère muraille faite d'amour et de morale qui protège votre coeur contre la colère d'un futur brulé par la haine et le pêcher.\nLes orbes de furie agissent pendant un tour supplémentaire !")
                    services.FloorMaker.GiveRandomArtefact("Demi-Masque de l'Ordre","Don")
                    services.Affichage.EntreePourContinuer()
                    print("Vous sentez votre nouveau masque s'accrocher désespérément a votre coeur battant, et la scène ne vous met plus en colère.")
                    services.Affichage.EntreePourContinuer()
                    print("Alors, les murs de la batisse tombent comme le carton d'un faux décor que l'on a mal installé.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous êtes de retour sur la scène, comme si il ne s'était rien passé.")
                    services.Affichage.EntreePourContinuer()
                    print("La seule chose qui a changé, c'est que votre colère repose désormais avec le talent salit et l'héritage violé...")
                    services.Affichage.EntreePourContinuer()
                    print("...sous la neige.")
                    services.Affichage.EntreePourContinuer()


@salle_de_type("PUIT")
def reveler_puit(etage, salle):
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.puit()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print("Vous apercevez un puit singulier, fait de vieille pierre.")
    services.Affichage.EntreePourContinuer()
    if services.Player.numero_de_letage == 1:
        print("Au fond de celui-ci, vous apercevez les contours d'un rocher entouré d'un tapis de verdure")
        services.Affichage.EntreePourContinuer()
        print("Dans le seau porté au dessus du précipice par une corde solide se trouve un liquide carmin, visqueux.")
        services.Affichage.EntreePourContinuer()
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
            services.Affichage.EntreePourContinuer()
        elif choix == 2:
            print("Vous approchez le seau de vos lèvres, et vos narines sont assaillies par une puissante odeur métallique.")
            services.Affichage.EntreePourContinuer()
            print("Vous persévérez, et bientôt le liquide froid coule dans votre gorge...")
            services.Affichage.EntreePourContinuer()
            print("...et c'était très nutritif !\nVous gagnez 5 points de vie max !")
            salle["terminé par joueur"] = True
            services.Player.points_de_vie += 5
            services.Player.points_de_vie_max += 5
            services.Affichage.EntreePourContinuer()
            print("Vous vous éloignez du puit.")
            services.Affichage.EntreePourContinuer()
        elif choix == 3:
            print("Vous prenez le seau a deux mains, et déversez son contenu dans le puit.")
            services.Affichage.EntreePourContinuer()
            print("Tout au fond, vous apercevez le tapis de verdure se teindre de rouge.")
            services.Affichage.EntreePourContinuer()
            print("Tout a coup, de grandes secousses et un cri a glacer le sang se fait entendre, alors que des racines jaillissent des murs du puit pour en obstruer la vue !")
            services.Affichage.EntreePourContinuer()
            print("Vous avez le terrible sentiment que quelque chose de végétal, en dessous, vient de se réveiller.")
            services.Affichage.EntreePourContinuer()
            print("L E  P R O C H A I N  E T A G E  C H A N G E  D E  P R O P R I E T A I R E\n")
            salle["terminé par joueur"] = True
            services.Player.etage_alternatif = True
            services.Affichage.EntreePourContinuer()
            print("Vous vous éloignez du puit.")
            services.Affichage.EntreePourContinuer()
    elif services.Player.numero_de_letage == 4:
        print("Au fond de celui-ci, vous apercevez un sol de bois noir, cerclé par des chaises de satin rouge.\n Et a coté du puit, un petit clavecin.")
        services.Affichage.EntreePourContinuer()
        while True:
            while True:
                try:
                    print("Que faire ?")
                    print("\n1 - S'éloigner du puit\n2 - Jouer un air au clavecin")
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
                services.Affichage.EntreePourContinuer()
                break
            elif choix == 2 :
                StopAllMusic()
                print("Vos doigts s'enfoncent sur le clavier, mais aucun son de sort.\nBizarre, il y a pourtant des cordes a l'interieur...")
                services.Affichage.EntreePourContinuer()
                print("Vous tentez quand meme de jouer quelque chose, en vous servant des lettres inscrites sur les touches comme référence :")
                services.Affichage.EntreePourContinuer()
                result = doPiano()
                ClearConsole()
                PlayMusicDeLetage()
                if result :
                    print("La mélodie retentit dans la pièce, jusque au fond du puit.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous sentez un tremblement venant d'en dessous, et jetez un coup d'oeuil dans l'ouverture de pierre.")
                    services.Affichage.EntreePourContinuer()
                    print("En bas, les couleurs chatoyantes qui dansaient dans le vide ont laissées place à un blanc immaculé, propre...")
                    services.Affichage.EntreePourContinuer()
                    print("...depuis lequel un puissant courant d'air empêche toute descente.")
                    services.Affichage.EntreePourContinuer()
                    print("...")
                    services.Affichage.EntreePourContinuer()
                    print("...")
                    services.Affichage.EntreePourContinuer()
                    print("...il commence a faire froid...")
                    services.Affichage.EntreePourContinuer()
                    print("L E  P R O C H A I N  E T A G E  C H A N G E  D E  P R O P R I E T A I R E\n")
                    salle["terminé par joueur"] = True
                    services.Player.etage_alternatif = True
                    services.Affichage.EntreePourContinuer()
                    print("Vous vous éloignez du puit.")
                    services.Affichage.EntreePourContinuer()
                    break
                else :
                    print("Rien ne se passe.")
                    services.Affichage.EntreePourContinuer()
    elif services.Player.numero_de_letage == 6:
        print("Au fond de celui-ci, vous apercevez les contours d'un feu entouré de petites flamelettes qui virevoltent, et entendez des murmures colériques remontant le long des parois du puit.")
        services.Affichage.EntreePourContinuer()
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
                services.Affichage.EntreePourContinuer()
                break
            elif choix == 2 and "Larmes de Vénus" in services.Player.liste_dartefacts_optionels:
                print("Vous prenez la petite fiole d'eau dans votre main, et la regardez briller doucement.")
                services.Affichage.EntreePourContinuer()
                print("Une fiole de Larme de Vénus permet *d'apaiser les feux de la colère et ne laisse derrière que les ombres de la culpabilité*, hein ?")
                print("La description n'a pas beaucoup de sens, mais juste le fait de la tenir apaise votre esprit combatif.")
                services.Affichage.EntreePourContinuer()
                print("Vous devissez le joli bouchon de cristal, et versez le contenu de la fiole dans le puit, en essayant de viser le feu tout en bas.")
                services.Player.liste_dartefacts_optionels.remove("Larmes de Vénus")
                services.Affichage.EntreePourContinuer()
                print("Vous voyez le feu s'éteindre, les flamelettes disparaitre, et un terrible cri de douleur émaner de tout en bas.")
                print("Alors que vous vous bouchez les oreille, le bruit se mue en de douloureux sanglots.")
                print("En même temps, d'épais barreaux de fer sortent des parois du puit, interdisant la descente.")
                services.Affichage.EntreePourContinuer()
                print("Vous avez le sentiment d'avoir changé quelque chose d'immuable, en dessous.")
                services.Affichage.EntreePourContinuer()
                print("L E  P R O C H A I N  E T A G E  C H A N G E  D E  P R O P R I E T A I R E\n")
                salle["terminé par joueur"] = True
                services.Player.etage_alternatif = True
                services.Affichage.EntreePourContinuer()
                print("Vous vous éloignez du puit.")
                services.Affichage.EntreePourContinuer()
                break
            else:
                print("Vous regardez votre inventaire, mais n'avez rien a vider dans le puit.")
                services.Affichage.EntreePourContinuer()


@salle_de_type("LIANE")
def reveler_liane(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.liane()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print(
        "Parmis les herbes hautes et les racines d'arbres, vous trouvez un petit coffre de bois noir."
    )
    print("Celui-ci est enserré de lianes épaisses.")
    services.Affichage.EntreePourContinuer()
    # si on a la machette rouillee, on peut liberer le coffre
    if "Machette Rouillée" in services.Player.liste_dartefacts_optionels:
        services.Player.liste_dartefacts_optionels.remove("Machette Rouillée")
        print(
            "Vous utilisez une Machette Rouillée sur les lianes, et réussissez"
            " a en trancher assez pour liberer le coffre, juste avant que la machette ne se brise!"
        )
        services.Affichage.EntreePourContinuer()
        print("Vous ouvrez le coffre...")
        services.Affichage.EntreePourContinuer()
        # fait que l'event soit finit et ne peut ps etre relancé
        salle["terminé par joueur"] = True
        etage.GiveRandomArtefact()
    else:
        print(
            "Vous tirez de toutes vos forces sur les lianes, mais elles restent accrochées au coffre."
        )
        print("Vous laissez tomber.")
        services.Affichage.EntreePourContinuer()


@salle_de_type("FAUX SPOT", "SPOT")
def reveler_faux_spot(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.spot()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print(
        "Vous pouvez apercevoir, dans le sable, une croix rouge."
        "\nElle ressemble à ce que l'on peut trouver sur une carte aux trésors !"
    )
    services.Affichage.EntreePourContinuer()
    # si on a la Vieille Pelle, on peut liberer le coffre
    if "Vieille Pelle" in services.Player.liste_dartefacts_optionels:
        services.Player.liste_dartefacts_optionels.remove("Vieille Pelle")
        # fait que l'event soit finit et ne peut ps etre relancé
        salle["terminé par joueur"] = True
        services.Save.SaveTheGameSansAffichage()
        print(
            "Vous utilisez une Vieille Pelle pour creuser au centre de la croix, et..."
        )
        services.Affichage.EntreePourContinuer()
        if salle["type"] == "SPOT":
            print("...la brisez sur un petit coffre de bois noir, que vous ouvrez immédiatement !")
            services.Affichage.EntreePourContinuer()
            etage.GiveRandomArtefact()
        else:
            print("...la brisez sur un morceau de roche dure.")
            print("Il n'y avait donc rien à trouver ici.")
            services.Affichage.EntreePourContinuer()
    else:
        print(
            "Vous commencez a creuser avec vos mains, "
            "mais la chaleur du sable et la difficultée de la tache vous vous convainc d'arrêter."
        )
        print("Vous laissez tomber.")
        services.Affichage.EntreePourContinuer()


@salle_de_type("SEQUENCE")
def reveler_sequence(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.sequence()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    # determine une sequence aléatoire si yen a pas deja une
    if len(etage.liste_sequence) == 0:
        for _ in range (1, 5):
            numero_de_salle_aleatoire = random.randint(5, len(etage.FloorBlueprint))
            etage.liste_sequence.append(numero_de_salle_aleatoire)
    #print(self.liste_sequence)
    #Affichage.EntreePourContinuer()

    #compare la sequence aux dernieres salles observées par le joueur
    sequence_realisee = False
    if len(etage.liste_des_salles_observées) == 4:
        sequence_realisee = True
        for numero_de_salle in range(0, 4):
            if etage.liste_des_salles_observées[numero_de_salle] == etage.liste_sequence[numero_de_salle]:
                continue
            sequence_realisee = False

    print("Vous trouvez un des plateaux volants gisant sur le sol, son métal devenu noir comme du charbon.")
    services.Affichage.EntreePourContinuer()    
    if sequence_realisee:
        #la main passe a travers les mots du parchemin et retire un artefact 
        print("Dessus, un parchemin montrant une allée de bibliothèque aux rangées droites, et dans"
              " laquelle se trouve un garde qui se prosterne.")
        print("Vous pouvez apercevoir un petit coffre de bois noir devant lui.")
        services.Affichage.EntreePourContinuer()
        print("Vous tendez la main pour touchez le papier, et vos doigts passent a travers l'image.")
        services.Affichage.EntreePourContinuer()
        print("Vous retirez un coffre du parchemin, et ce dernier s'enflamme !")
        services.Affichage.EntreePourContinuer()
        print("Vous lachez brusquement le parchemin qui disparait alors dans l'air, et ouvrez le coffre...")
        services.Affichage.EntreePourContinuer()
        salle["terminé par joueur"] = True
        etage.GiveRandomArtefact()
    else:
        # montre le parchemin avec la séquence
        print("Dessus, un parchemin dépictant une allée de bibliothèque aux rangées droites, et dans"
              " laquelle se trouve un garde dont le visage ferme et les bras croisés évoque la rigueur.")
        print("Vous pouvez apercevoir un petit coffre de bois noir entre ses jambes.")
        services.Affichage.EntreePourContinuer()
        print("En bas du parchemin, il est écrit un poême :")
        services.Affichage.EntreePourContinuer()
        print("*L'Empereur se promène dans son pavillon.*")

        #position de la premiere salle de la sequence
        position_x = etage.FloorBlueprint[etage.liste_sequence[0]]["position_x"]
        if position_x < 0:
            commentaire_x = f"moins de {abs(position_x)}"
        elif position_x == 0:
            commentaire_x = "son manque de"
        else:
            commentaire_x = position_x
        position_y = etage.FloorBlueprint[etage.liste_sequence[0]]["position_y"]
        if position_y < 0:
            commentaire_y = f"moins de {abs(position_y)}"
        elif position_y == 0:
            commentaire_y = "son manque de"
        else:
            commentaire_y = position_y
        print(f"*Il va observer {commentaire_x} carpes et {commentaire_y} roseaux de son étang.*")

        #position de la deuxieme salle de la sequence
        position_x = etage.FloorBlueprint[etage.liste_sequence[1]]["position_x"]
        if position_x < 0:
            commentaire_x = f"moins de {abs(position_x)}"
        elif position_x == 0:
            commentaire_x = "son manque de"
        else:
            commentaire_x = position_x
        position_y = etage.FloorBlueprint[etage.liste_sequence[1]]["position_y"]
        if position_y < 0:
            commentaire_y = f"moins de {abs(position_y)}"
        elif position_y == 0:
            commentaire_y = "son manque de"
        else:
            commentaire_y = position_y
        print(f"*Il va regarder travailler {commentaire_x} cuisiniers et {commentaire_y} servantes dans sa cuisine.*")

        #position de la troisieme salle de la sequence
        position_x = etage.FloorBlueprint[etage.liste_sequence[2]]["position_x"]
        if position_x < 0:
            commentaire_x = f"moins de {abs(position_x)}"
        elif position_x == 0:
            commentaire_x = "son manque de"
        else:
            commentaire_x = position_x
        position_y = etage.FloorBlueprint[etage.liste_sequence[2]]["position_y"]
        if position_y < 0:
            commentaire_y = f"moins de {abs(position_y)} "
        elif position_y == 0:
            commentaire_y = "son manque d'"
        else:
            commentaire_y = f"{position_y} "
        print(f"*Il va admirer {commentaire_x} fleurs et {commentaire_y}arbres dans son jardin.*")

        #position de la derniere salle de la sequence
        position_x = etage.FloorBlueprint[etage.liste_sequence[3]]["position_x"]
        if position_x < 0:
            commentaire_x = f"moins de {abs(position_x)}"
        elif position_x == 0:
            commentaire_x = "son manque de"
        else:
            commentaire_x = position_x
        position_y = etage.FloorBlueprint[etage.liste_sequence[3]]["position_y"]
        if position_y < 0:
            commentaire_y = f"moins de {abs(position_y)}"
        elif position_y == 0:
            commentaire_y = "son manque de"
        else:
            commentaire_y = position_y
        print(f"*Il va lire {commentaire_x} livres et {commentaire_y} comptes-rendus dans sa bibliothèque.*")

        print("*Puis il vient saluer son garde, qui le reconnait et lui offre une preuve de sa fidélité.*")
        services.Affichage.EntreePourContinuer()
        print("Vous reposez le parchemin sur le plateau et repartez.")
        services.Affichage.EntreePourContinuer()


@salle_de_type("DDR")
def reveler_ddr(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.ddr()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print("La salle est remplie de jeux d'arcades aux thêmes divers et variés, mais les carcasses de métal et de peinture sont presque toutes inopérables.")
    print("Seule une machine affiche fièrement ses couleurs et son nom en lettres de néon :")
    services.Affichage.EntreePourContinuer()
    print("""Dance Dance Revolution MAXIMUM OUTPUT!!!""")
    services.Affichage.EntreePourContinuer()
    print("Sur l'écran, vous pouvez voir plusieurs images de boites de nuits à l'ambiance endiablée "
              "dans lesquelles sont modélisés des personnages banals aux visages radieux.")
    print("Seul un jeune homme en costume à paillette et pattes d'éléphant se déhanche furieusement sur le dancefloor, un regard vide plaqué sur le visage.")
    services.Affichage.EntreePourContinuer()
    print("Les scores des différents joueurs se mettent alors a défiler, et a la fin, un message indiquant que celui qui bat le score du joueur en tête sera récompensé.")
    services.Affichage.EntreePourContinuer()
    print("L'image de profil du joueur n°1 ressemble trait pour trait a celui de l'homme aux pattes d'éléphants.")
    services.Affichage.EntreePourContinuer()
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
        if services.Player.nombre_de_gold >= 75:
            game_done = etage.DanceDanceRevolutionIntroduction()
            if game_done:
                StopAllMusic()
                print("La machine explose !")
                services.Affichage.EntreePourContinuer()
                print("Vous faites attention aux morceaux de verre brisés et aux étincelles, et regardez derriere l'écran.")
                services.Affichage.EntreePourContinuer()
                print("Vous trouvez un squelette habillé avec un costume a pailette et des pattes d'éléphants.")
                services.Affichage.EntreePourContinuer()
                print("Entre ses doigts squelettiques, il tient un petit coffre de bois noir.")
                services.Affichage.EntreePourContinuer()
                print("Vous arrachez le coffre du sac d'os et vous empressez de l'ouvrir.")
                services.Affichage.EntreePourContinuer()
                salle["terminé par joueur"] = True
                etage.GiveRandomArtefact()
            else:
                print("Vous vous éloignez de la machine et reprenez votre souffle.")
                services.Affichage.EntreePourContinuer()
            PlayMusicDeLetage()
        else:
            print("Vous videz vos poches, mais ne trouvez pas assez d'argent pour jouer.")
            services.Affichage.EntreePourContinuer()
            print("Rapelez vous : L'addiction aux jeux d'argents, c'est une maladie reconnue par l'Association américaine de psychiatrie !")
            services.Affichage.EntreePourContinuer()
            print("Gardez toujours un oeil sur ce qui est véritablement important :")
            services.Affichage.EntreePourContinuer()
            print("L'hydratation.")
            services.Affichage.EntreePourContinuer()
            print("Vous avez bu un verre d'eau ces dernières dix minutes ?")
            services.Affichage.EntreePourContinuer()
            print("Exactement.")
            services.Affichage.EntreePourContinuer()
            print("Allez boire de l'eau.")
            services.Affichage.EntreePourContinuer()
            print(f"Pendant ce temps, {services.Player.nom_du_personnage} sort de la salle pour éviter les tentations.")
            services.Affichage.EntreePourContinuer()
    else:
        print("Vous regardez les images défiler, et continuez votre chemin.")
        services.Affichage.EntreePourContinuer()


@salle_de_type("BROKEN")
def reveler_broken(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.broken()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print("Vous trouvez une... bien étrange machine.")
    services.Affichage.EntreePourContinuer()
    print("D'un côté, une jolie horloge de parquet annotée de nombres et références.")
    print("De l'autre, un morceau de taule plié de manière artistique, qui représente un nombre différent selon le point de vue.")
    print("Et au milieu, une sépraration nette, comme si on avait coupé en deux "
          "les deux machines et qu'on avait recollé ensemble deux bouts de machines différentes.")
    services.Affichage.EntreePourContinuer()
    print("...?")
    services.Affichage.EntreePourContinuer()
    print("Ah non.")
    services.Affichage.EntreePourContinuer()
    print("Pas *collé*.")
    services.Affichage.EntreePourContinuer()
    print("Juste posé l'un contre l'autre.")
    services.Affichage.EntreePourContinuer()
    print("Vous poussez le morceau de taule sur le coté, et rentrez votre main dans la cavité derriere le cadran de l'horloge.")
    print("Vous en ressortez un petit coffre de bois noir !")
    services.Affichage.EntreePourContinuer()
    print("Vous remerciez le manque d'inspiration du développeur, et ouvrez votre coffre gratuit.")
    services.Affichage.EntreePourContinuer()
    etage.GiveRandomArtefact()

    # fait que l'event soit finit et ne peut ps etre relancé
    salle["terminé par joueur"] = True


@salle_de_type("PLAQUE PRESSION")
def reveler_plaque_pression(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.machine()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print("Vous trouvez un méchanisme ancien !")
    services.Affichage.EntreePourContinuer()
    print("C'est...")
    services.Affichage.EntreePourContinuer()
    print("...une plaque de pression.")
    services.Affichage.EntreePourContinuer()
    print("Vous jettez un regard désespéré à votre pied enfoncé de quelques centimètres dans le sol, et croisez les doigts.")
    services.Affichage.EntreePourContinuer()
    print(
        "Aussitot, des arbalètes sournoises, cachées dans les murs, vous criblent de flèches !"
    )
    services.Affichage.EntreePourContinuer()
    if not ("Sabre du Roi de Glace" in services.Player.liste_dartefacts_optionels):
        degat = round(services.Player.points_de_vie_max * 0.33)
        services.Player.points_de_vie -= degat
        print(f"Vous perdez {degat} points de vie.")
        services.Affichage.EntreePourContinuer()
        if services.Player.points_de_vie <= 0:
            if services.Player.possede_une_fee == True and "Fée dans un Bocal" in services.Player.liste_dartefacts_optionels:
                services.Player.liste_dartefacts_optionels.remove("Fée dans un Bocal")
                services.Player.possede_une_fee = False
                print("Vous alliez mourir, mais votre fée sort de son bocal et vous sauve la mise. Ouf !")
                services.Player.points_de_vie = round(0.33 * services.Player.points_de_vie_max)
                services.Affichage.EntreePourContinuer()
            else :
                StopAllMusic()
                PlaySound("death")
                print("Vous échouez a stopper le saignement, et perdez la vie.")
                services.Affichage.EntreePourContinuer()
                services.Player.player_tags.append("KIA")
                CheckForKIA()
    else:
        print("Cepandant, des éclats de glace se forment aux endroits ou les flèches auraient du se planter.")
        services.Affichage.EntreePourContinuer()
    if not "Fantome" in services.Player.player_tags:
        print("Avant que vous n'ayez le temps de comprendre ce qu'il vient de se passer, un gaz violet remplit la salle, vous rendant confus !")
        services.Affichage.EntreePourContinuer()
        print("Enfin, un monstre tombe du plafond.")
        services.Affichage.EntreePourContinuer()
        services.Player.commence_le_combat_confus = True
        livrer_combat()
        services.Player.commence_le_combat_confus = False
        CheckForKIA()
        PlayMusicDeLetage()
        print("Vous entendez un crissement irrégulier, et la plaque de pression se retrouve bloquée dans sa position.")
        print("Vous n'aurez pas a vous soucier de cette salle davantage.")
        services.Affichage.EntreePourContinuer()

    # fait que l'event soit finit et ne peut ps etre relancé
    salle["terminé par joueur"] = True


@salle_de_type("ECLAIR")
def reveler_eclair(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.eclair()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print("Vous entrez dans une salle singulière, dont le sol est tapissé de terre fertile.")
    services.Affichage.EntreePourContinuer()
    print("Des armes de toute formes sont plantées dans la terre, que la rouille rend inutilisable.")
    services.Affichage.EntreePourContinuer()
    print("Au dessus, la vapeur d'eau est condensée en un grondant et tourbillonant nuage noir.")
    services.Affichage.EntreePourContinuer()
    while True:
        try:
            print("Une petite colline vous permet de vous approcher du nuage noir.")
            print("\n1 - Monter sur la colline")
            print("2 - Partir")
            choix = int(input("\nFaites votre choix avec les nombres : "))
            ClearConsole()
            if choix in [1, 2]:
                break
        except ValueError:
            ClearConsole()
    if choix == 1:
        # fait que l'event soit finit et ne peut ps etre relancé
        salle["terminé par joueur"] = True

        #faire liste action evoluable
        liste_action_qui_peut_evoluer = [
            "Attaque Légère",
            "Lance Rapide",
            "Lance Statique",
            "Lance Electrique",
            "Lance de l'Eclair",
            "Lance Foudroyante",
            "Bô Chaud",  #
            "Bô Brulant",  #
            "Bô Enflammé",  #
            "Bô de la Fournaise",
            "Bô Magmatique",
            "Katana Bleu",
            "Katana Froid",
            "Katana Givré",
            "Katana Glacial",
            "Katana Polaire",
            "Corne Argile",  #
            "Corne Lapis",  #
            "Corne Granite",  #
            "Corne Obsidienne",
            "Corne de la Montagne",
            "Poing Léger",  #
            "Poing Renforcé",  #
            "Poing Lourd",  #
            "Poing Maitrisé",  #
            "Poing Fatal",  #
            "Dague Volevie",
            "Dague Siphoneuse",
            "Dague Vampirique",
            "Dague Parasite",
            "Dague Destructrice",
            "Tir Arcanique",
            "Faisceau Rapide",
            "Faisceau Statique",
            "Faisceau Electrique",
            "Faisceau de l'Eclair",
            "Faisceau Foudroyant",
            "Thermosphère Chaude",
            "Thermosphère Brulante",
            "Thermosphère Enflammée",
            "Thermosphère de la Fournaise",
            "Thermosphère Magmatique",
            "Pic Bleu",
            "Pic Froid",
            "Pic Givré",
            "Pic Glacial",
            "Pic Polaire",
            "Création d'Argile",
            "Création de Lapis",
            "Création de Granite",
            "Création Obsidienne",
            "Création de la Montagne",
            "Explosion Légère",
            "Explosion Renforcée",
            "Explosion Lourde",
            "Explosion Maitrisée",
            "Explosion Fatale",
            "Dance Volevie",
            "Dance Siphoneuse",
            "Dance Vampirique",
            "Dance Parasite",
            "Dance Destructrice",
            "Sonata Pitoyable",  # 3% ou 8pv
            "Sonata Miséricordieuse",  # 5% ou 15pv
            "Sonata Empathique",  # 12% ou 20pv
            "Sonata Sincère",  # 17% ou 25pv
            "Sonata Bienveillante",  # 20% ou 33pv
            ]
        liste_action_en_possession = []
        for action in services.Player.techniques_possedes:
            if action in liste_action_qui_peut_evoluer:
                liste_action_en_possession.append(action)
        for action in services.Player.sorts_possedes:
            if action in liste_action_qui_peut_evoluer:
                liste_action_en_possession.append(action)

        #prendre action au pif
        if len(liste_action_en_possession) == 0:
            services.Player.nombre_de_monstres_tues += 20
            uppgrade_impossible = True
        else:
            uppgrade_impossible = False
            nombre_aleatoire = random.randint(0, (len(liste_action_en_possession) - 1))
            nom_action_a_evoluer = liste_action_en_possession[nombre_aleatoire]

        #trouver son evolution
        if nom_action_a_evoluer == "Attaque Légère":
            nom_nouvelle_action = "Attaque Lourde"
            description = "La technique"
            services.Player.techniques_possedes.remove(nom_action_a_evoluer)
            services.Player.techniques_possedes.append(nom_nouvelle_action)
        elif nom_action_a_evoluer == "Tir Arcanique":
            description = "Le sort"
            nom_nouvelle_action = "Missile Arcanique"
            services.Player.sorts_possedes.remove(nom_action_a_evoluer)
            services.Player.sorts_possedes.append(nom_nouvelle_action)
        elif nom_action_a_evoluer in LISTETECHNIQUES:
            position_de_laction = LISTETECHNIQUES.index(nom_action_a_evoluer)
            nom_nouvelle_action = LISTETECHNIQUES[position_de_laction + 1]
            description = "La technique"
            services.Player.techniques_possedes.remove(nom_action_a_evoluer)
            services.Player.techniques_possedes.append(nom_nouvelle_action)
        elif nom_action_a_evoluer in LISTESORTS:
            position_de_laction = LISTESORTS.index(nom_action_a_evoluer)
            nom_nouvelle_action = LISTESORTS[position_de_laction + 1]
            description = "Le sort"
            services.Player.sorts_possedes.remove(nom_action_a_evoluer)
            services.Player.sorts_possedes.append(nom_nouvelle_action)


        print("Alors que vous vous approchez du nuage, la verdure se fait de plus en plus rare, jusqu'à ce que vos pas s'enfoncent dans un sol sec et aride.")
        print("Vous continuez de vous avancer, utilisant les différentes lames pour vous hisser sur le sommet de la colline.")
        services.Affichage.EntreePourContinuer()
        print("Enfin, vous arrivez tout en haut, haletant.")
        services.Affichage.EntreePourContinuer()
        print("Vous sentez alors l'orage gronder, et vos cheveux se hissent sur votre crane !")
        print("Vous levez Zeroual dans un geste de défence, et sentez un éclair surpuissant le traverser une seconde plus tard !")
        services.Affichage.EntreePourContinuer()
        print("L'impact vous projette au sol, et vous dévalez la face de la colline en brisant au passage les fragiles lames de métal !")
        services.Affichage.EntreePourContinuer()
        print("Alors que vous vous relevez, vous voyez le nuage disparaitre, et Zeroual briller d'une manière étrange.")
        services.Affichage.EntreePourContinuer()
        services.Save.SaveTheGameSansAffichage()
        if uppgrade_impossible:
            print("Zeroual a absorbé l'équivalent de 20 nouvelles âmes !")
        else:
            print(f"{description} [{nom_action_a_evoluer}] devient [{nom_nouvelle_action}] !")
        services.Affichage.EntreePourContinuer()
        print("Vous tournez le dos à l'étrange colline et repartez d'ou vous venez.")
        services.Affichage.EntreePourContinuer()
    elif choix == 2:
        print("Vous laissez votre regard se perdre dans le faux ciel peint au plafond...et sortez de la salle.")
        services.Affichage.EntreePourContinuer()  


@salle_de_type("LEVIER")
def reveler_levier(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.machine()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print("Vous trouvez un méchanisme ancien !")
    services.Affichage.EntreePourContinuer()
    print("C'est...")
    services.Affichage.EntreePourContinuer()
    print("...un levier !")
    services.Affichage.EntreePourContinuer()
    print("Littéralement.\nUn simple levier placé au centre de la salle, sur un piedestal de verre.")
    services.Affichage.EntreePourContinuer()
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
        services.Affichage.EntreePourContinuer()
        print("Vous laissez ce levier tranquille, rempli de cette assurance sur vos choix et actions, vous sentant intelligent comme personne !")
        services.Affichage.EntreePourContinuer()
        print("Et si vous aviez tiré le levier ?\nVous auriez pu avoir tant de choses...\nPlus tard, sur votre lit de mort, c'est la dernière pensée qui traversera votre esprit.")
        services.Affichage.EntreePourContinuer()
        print("Ou pas ?\nQui sait.\nPas vous en tout cas, vu que vous n'avez pas tiré le levier.")
        services.Affichage.EntreePourContinuer()
    if choix == 1:
        print("Vous avancez gaiement, sautillant de pas en pas, jusqu'à atteindre le magnifique et tentateur levier au milieu de la salle.")
        services.Affichage.EntreePourContinuer()
        print("Qui sait ce qui se serait passé si vous ne l'aviez pas tiré ?\nVous l'auriez sans doute regretté sur votre lit de mort.")
        services.Affichage.EntreePourContinuer()
        print("Ou pas ?\nQui sait.\nPas vous en tout cas, vu que vous allez tirer le levier !")
        services.Affichage.EntreePourContinuer()
        print("Vous posez fermement vos mains sur le levier, tirez dessus, et...")
        services.Affichage.EntreePourContinuer()
        effet_aleatoire = random.randint(1, 10)
        if effet_aleatoire == 1 :
            print("...rien ne se passe.")
            services.Affichage.EntreePourContinuer()
            print("C'est vraiment nul.")
            services.Affichage.EntreePourContinuer()
        elif effet_aleatoire == 2:
            print("...le sol s'ouvre sous vos pieds !\nCa devait être le mauvais levier !")
            services.Affichage.EntreePourContinuer()
            print("Vous tombez dans le trou béant, glissez sur la pierre fraiche pendant une vingtaine de minute, et atterissez...")
            services.Affichage.EntreePourContinuer()
            print("...au centre de l'arène !")
            services.Player.position_x = 0
            services.Player.position_y = 0
            services.Player.numero_de_la_salle = 1
            etage.UpdatePlayerPosition()
            services.Affichage.EntreePourContinuer()
        elif effet_aleatoire == 3:
            print("...un monstre de niveau superieur apparait !")
            services.Affichage.EntreePourContinuer()
            services.Player.player_tags.append("Monstre De Niveau Superieur")
            livrer_combat()
            services.Player.player_tags.remove("Monstre De Niveau Superieur")
            PlayMusicDeLetage()
        elif effet_aleatoire == 4:
            print(
                "...des arbalètes sournoises, cachées dans les murs, vous criblent de flèches !"
            )
            services.Affichage.EntreePourContinuer()
            if not ("Sabre du Roi de Glace" in services.Player.liste_dartefacts_optionels):
                degat = round(services.Player.points_de_vie_max * 0.33)
                services.Player.points_de_vie -= degat
                print(f"Vous perdez {degat} points de vie.")
                services.Affichage.EntreePourContinuer()
                if services.Player.points_de_vie <= 0:
                    if services.Player.possede_une_fee == True and "Fée dans un Bocal" in services.Player.liste_dartefacts_optionels:
                        services.Player.liste_dartefacts_optionels.remove("Fée dans un Bocal")
                        services.Player.possede_une_fee = False
                        print("Vous alliez mourir, mais votre fée sort de son bocal et vous sauve la mise. Ouf !")
                        services.Player.points_de_vie = round(0.33 * services.Player.points_de_vie_max)
                        services.Affichage.EntreePourContinuer()
                    else:
                        StopAllMusic()
                        PlaySound("death")
                        print("Vous échouez a stopper le saignement, et perdez la vie.")
                        services.Affichage.EntreePourContinuer()
                        services.Player.player_tags.append("KIA")
                        CheckForKIA()
            else:
                print("Cepandant, des éclats de glace se forment aux endroits ou les flèches auraient du se planter.")
                services.Affichage.EntreePourContinuer()
        elif effet_aleatoire == 5:
            print("...un petit coffre tombe du plafond et rebondit sur le sol !")
            services.Affichage.EntreePourContinuer()
            print("Enfin, sur votre tête, puis sur le sol.")
            services.Affichage.EntreePourContinuer()
            nom_de_litem = GetRandomItemFromList(LISTEITEM)
            services.Player.items_possedes[nom_de_litem] += 1
            print(f"A l'interieur, vous trouvez l'objet {nom_de_litem}")
            services.Affichage.EntreePourContinuer()
        elif effet_aleatoire == 6:
            print("...rien ne se passe.")
            services.Affichage.EntreePourContinuer()
            print("C'est vraiment nul.")
            services.Affichage.EntreePourContinuer()
            print("Au moment ou vous tournez le dos au méchanisme, vous voyez une figure fantomatique s'approcher de vous !")
            services.Affichage.EntreePourContinuer()
            print("La chose porte un casque de chantier jaune, un pantalon bleu a bretelle, et un visage pâle et fatigué.")
            services.Affichage.EntreePourContinuer()
            print("*Ouai, ouai, je sais.*")
            services.Affichage.EntreePourContinuer()
            print("L'ingénieur se rapproche de vous et vous tend quelque chose.")
            print("*C'était sensé faire tomber des araignées du plafond, mais, héhé, elles sont toutes mortes. Prend ca comme compensation.*")
            services.Affichage.EntreePourContinuer()
            print("Vous obtenez un Redcoin !")
            services.Affichage.EntreePourContinuer()
            print("Aussitot, un souffle de vent vous pousse en dehors de la salle.")
            print("*Fiche moi le camp pronto, j'ai un truc à réparer.*")
            services.Affichage.EntreePourContinuer()
        elif effet_aleatoire == 7:
            print("...une petite boite noire se materialise *dans* le piedestal !")
            print("Vous brisez le verre pour récuperer la boite, et l'ouvrez.")
            services.Affichage.EntreePourContinuer()
            etage.GiveRandomArtefact()
        elif effet_aleatoire == 8:
            print("...un monstre apparait !")
            services.Affichage.EntreePourContinuer()
            livrer_combat()
            PlayMusicDeLetage()
        elif effet_aleatoire == 9:
            print("...un orbe bleu apparait !")
            print("Il flotte jusqu'à vous, et rentre dans votre poitrine.")
            services.Affichage.EntreePourContinuer()
            print("Vous gagnez 7 points de vie/mana max !")
            services.Player.points_de_vie_max += 7
            services.Player.points_de_mana_max += 7
            services.Affichage.EntreePourContinuer()
        elif effet_aleatoire == 10:
            print("...vous entendez le son caractéristique d'une mèche d'explosif qui s'allume !")
            print("Vous sortez de la salle en courant, et bientot cette dernière disparait dans l'explosion d'une ccentaine de paquets de tnt !")
            print("Pris dans l'explosion, vous êtes projetés de plusieurs mètres en avant dans un mur, laissant sur ce dernier une indentation en forme de vous !")
            if not ("Sabre du Roi de Glace" in services.Player.liste_dartefacts_optionels):
                degat = round(services.Player.points_de_vie_max * 0.66)
                services.Player.points_de_vie -= degat
                print(f"Vous perdez {degat} points de vie.")
                services.Affichage.EntreePourContinuer()
                if services.Player.points_de_vie <= 0:
                    if services.Player.possede_une_fee == True and "Fée dans un Bocal" in services.Player.liste_dartefacts_optionels:
                        services.Player.liste_dartefacts_optionels.remove("Fée dans un Bocal")
                        services.Player.possede_une_fee = False
                        services.Player.points_de_vie = round(0.33 * services.Player.points_de_vie_max)
                        print("Vous alliez mourir, mais votre fée sort de son bocal et vous sauve la mise. Ouf !")
                        services.Affichage.EntreePourContinuer()
                    else:
                        StopAllMusic()
                        PlaySound("death")
                        print("Vous ne vous releverez jamais de cette explosion.")
                        services.Affichage.EntreePourContinuer()
                        services.Player.player_tags.append("KIA")
                        CheckForKIA()
            else:
                print("Cepandant, alors que vous vous relevez, vous vous rendez compte que votre corps tout entier était recouvert d'une épaisse armure de glace qui a absorbé le choc.")
                services.Affichage.EntreePourContinuer()
        if not "Fantome" in services.Player.player_tags:
            print("Au final, est ce que ca valait le coup de tirer le levier ?")
            services.Affichage.EntreePourContinuer()
            print("Seul vous peut en décider.")
            services.Affichage.EntreePourContinuer()
        # fait que l'event soit finit et ne peut ps etre relancé
        salle["terminé par joueur"] = True
