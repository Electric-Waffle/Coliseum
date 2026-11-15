"""Salles ordinaires du donjon : monstres, trésors, pièges, clé et salle secrète."""


from coliseum import services
from coliseum.audio import PlayMusicDeLetage, PlaySound, StopAllMusic
from coliseum.console import ClearConsole
from coliseum.donnees.items import LISTEITEM
from coliseum.histoire.village import CheckForKIA
from coliseum.interface.dessin import ColiseumGoto
from coliseum.outils import GetRandomItemFromList
from coliseum.combat.lancement import livrer_combat
from coliseum.exploration.salles.registre import salle_de_type


@salle_de_type("ENTREE")
def reveler_entree(etage, salle):
    if services.Player.numero_de_letage == -1:
        print("Vous retournez sur la Stèle du Renouveau, au centre du village.")
    else:
        print("Vous retournez dans l'Arène au centre de l'étage.")
    ColiseumGoto(0, -12.5)
    services.Affichage.EntreePourContinuer()


@salle_de_type("MONSTRE")
def reveler_monstre(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.monstre()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    # lance le combat
    print("Vous entendez un bruit derrière vous, et découvrez un monstre !")
    services.Affichage.EntreePourContinuer()
    livrer_combat()
    CheckForKIA()
    PlayMusicDeLetage()

    # fait que l'event soit finit et ne peut ps etre relancé
    salle["terminé par joueur"] = True


@salle_de_type("MONSTRE_SUPERIEUR")
def reveler_monstre_superieur(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.monstre()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    # lance le combat
    print("Vous entendez un bruit derrière vous, et découvrez un monstre...?")
    services.Affichage.EntreePourContinuer()
    print("Ce dernier est recouvert d'aiguilles en tout genre, et possède un regard vraiment féroce.")
    services.Affichage.EntreePourContinuer()
    print("C'est un monstre dopé de niveau superieur !")
    services.Affichage.EntreePourContinuer()
    services.Player.player_tags.append("Monstre Dopé")
    livrer_combat()
    services.Player.player_tags.remove("Monstre Dopé")
    PlayMusicDeLetage()

    # fait que l'event soit finit et ne peut ps etre relancé
    salle["terminé par joueur"] = True


@salle_de_type("GOLD")
def reveler_gold(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.gold()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True
    print("Vous trouvez un sac de gold caché sous une table.")
    gain_gold = 50 * services.Player.numero_de_letage
    gain_gold = services.Player.AddGoldToPlayer(gain_gold, True)
    print(f"Vous gagnez {gain_gold} golds !")
    services.Affichage.EntreePourContinuer()
    # fait que l'event soit finit et ne peut ps etre relancé
    salle["terminé par joueur"] = True


@salle_de_type("RIEN")
def reveler_rien(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print("Rien que des autels en ruine et des casiers à documents remplis de poussière.")
    services.Affichage.EntreePourContinuer()

    # fait que l'event soit finit et ne peut ps etre relancé
    salle["terminé par joueur"] = True


@salle_de_type("ITEM")
def reveler_item(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.item()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print("Vous trouvez une vieille caisse de provision.")
    print(
        "La plupart des objets sont irrécupérables, a peine des amas de rouille et de pourriture."
    )
    print(
        "Seul un sac de plastique vert fermé hermétiquement attire votre attention."
    )
    services.Affichage.EntreePourContinuer()
    nom_de_litem = GetRandomItemFromList(LISTEITEM)
    print(f"A l'interieur se trouve l'objet : {nom_de_litem} !")
    services.Affichage.EntreePourContinuer()
    services.Player.items_possedes[nom_de_litem] += 1
    # fait que l'event soit finit et ne peut ps etre relancé
    salle["terminé par joueur"] = True


@salle_de_type("KEY")
def reveler_key(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.key()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print(
        "Vous trouvez une salle vide, sauf pour une étrange substance flottant dans les airs."
    )
    print(
        "Alors que vous approchez votre main de la substance, cette dernière fonce d'un coup sur votre paume ouverte et y imprime un tatouage particulier."
    )
    services.Affichage.EntreePourContinuer()
    print("Vous obtenez la Clé Incrustée !")
    services.Affichage.EntreePourContinuer()
    services.Player.possede_la_cle = True

    if services.Player.nom_de_letage == "Limbes Flétrissants" :
        services.Ending.PrintEtEntreePourContinuer("..?")
        services.Ending.PrintEtEntreePourContinuer("Vous entendez une voix résonner autour de vous :")
        if services.Player.numero_boss_alt == 1:
            services.Ending.PrintEtEntreePourContinuer("*Bienvenue enfant maudit.*")
            services.Ending.PrintEtEntreePourContinuer("*Je ne peux pas vraiment te parler librement, alors je vais être brève.*\n*Laisse moi te parler du contexte et de ta situation.*")
            services.Ending.PrintEtEntreePourContinuer("*Premièrement, j'espère que tu maitrise le combat, car ce que tu va vivre va tester tes compétences dans tout les domaines du combat.*")
            services.Ending.PrintEtEntreePourContinuer("*Tu te trouve dans un endroit oublié, là ou on enferme ce que l'on ne peut pas controller, pour affronter 10 terribles existances.* ")
            services.Ending.PrintEtEntreePourContinuer("*Dernièrement,*")
            services.Ending.PrintEtEntreePourContinuer("*Celui que tu vas affronter ici se nomme Cauchemard.*\n*C'est le résidu de ce qui s'est introduit dans l'esprit du roi pour le rendre fou.*")
            services.Ending.PrintEtEntreePourContinuer("*Prend ton mal en patience et attend.*\n*Cette chose est intuable tant que l'on ne chante pas les mélodies qui appaisent l'esprit jeune.*")
            services.Ending.PrintEtEntreePourContinuer("*Et crois moi, celui qui l'a jeté dans ce cachot de poussière s'est assuré que ces mélodies soient chantées a un moment ou un autre.*")
            services.Ending.PrintEtEntreePourContinuer("*IL ne peut pas se permettre de voir Cauchemard s'échapper, encore.*")
            services.Ending.PrintEtEntreePourContinuer("*Fais attention a son influence, il peut altérer ton état d'un claquement de doigts, et ce pendant longtemps.*")
              #  voix dit que c'est elle qui a appelé, parle de Cauchemard
        elif services.Player.numero_boss_alt == 2:
            services.Ending.PrintEtEntreePourContinuer("*Bien. Tu as conquis un des nombreux obstacles qui t'attendent.*")
            services.Ending.PrintEtEntreePourContinuer("*Premièrement, laisse moi te parler un peu de moi.*")
            services.Ending.PrintEtEntreePourContinuer("*Je suis une ombre, un souffle, une présence.*")
            services.Ending.PrintEtEntreePourContinuer("*Je suis ton futur, tout comme tu es mon passé.*")
            services.Ending.PrintEtEntreePourContinuer("*Je suis le réceptacle de la Mort, après qu'elle ait été laissée tombée par le Dieu de la Mort il y a bien longtemps de cela, dans une guerre sanglante.*")
            services.Ending.PrintEtEntreePourContinuer("*Dernièrement,*")
            services.Ending.PrintEtEntreePourContinuer("*Celui que tu vas affronter est un enfant royal, venu des sables chauds.*\n*Mais aux yeux de celui qui l'a mutilé, C'etait un matériau.*")
            services.Ending.PrintEtEntreePourContinuer("*Une partie de lui vit avec son père, le reste a été condamné a une existance terrible, vivre sans être vivant.*")
            services.Ending.PrintEtEntreePourContinuer("*Cepandant, a force de perseverance, il s'est réparé avec l'aide de la science et de la magie.*")
            services.Ending.PrintEtEntreePourContinuer("*C'est maintenant un adversaire redoutable, aidé par 2 gardiens de chair et d'âme.*")
            services.Ending.PrintEtEntreePourContinuer("*Fais bien attention a ta liste de sorts, de nouvelles actions pourraient t'aider à le vaincre.*")
            pass  #  voix dit comment arrivé là, parle de astonre
        elif services.Player.numero_boss_alt == 3:
            services.Ending.PrintEtEntreePourContinuer("*Hey, encore là ? C'est bien.*")
            services.Ending.PrintEtEntreePourContinuer("*Premièrement, je pense que je peux t'en dire un peu plus sur l'endroit ou tu te trouve.*")
            services.Ending.PrintEtEntreePourContinuer("*Le Coliseum à produit de nombreux guerriers et guerrières au fur et a mesure des années, mais aucuns n'arrivent a la cheville de ceux qui ont un lien avec sa création.*")
            services.Ending.PrintEtEntreePourContinuer("*Ces âmes là sont puissantes. Très puissantes. Trop puissantes.*")
            services.Ending.PrintEtEntreePourContinuer("*En clair, la Pierre de Désir les a rangés dans un coin inacessible, destiné a être oublié par le temps dans un coin du grand livre de l'Histoire.*")
            services.Ending.PrintEtEntreePourContinuer("*Destinés a pourrir dans le plus pur des or.*")
            services.Ending.PrintEtEntreePourContinuer("*Dernièrement,*")
            services.Ending.PrintEtEntreePourContinuer("*Il n'y a ici que des épitomes de puissance, pas seulement des guerriers et monarques.*")
            services.Ending.PrintEtEntreePourContinuer("*Tu affrontera ainsi Ahmed, le cuisinier du Roi Fou.*")
            services.Ending.PrintEtEntreePourContinuer("*Il doit y avoir quelque part un livre de recette pour t'expliquer comment fonctionne la cuisine via Mots de Pouvoir.*")
            services.Ending.PrintEtEntreePourContinuer("*Pourquoi lire un livre de recette ?*")
            services.Ending.PrintEtEntreePourContinuer("*Car ce combat te demandera de jongler entre combat normal et cuisine.*")
            services.Ending.PrintEtEntreePourContinuer("*Assure toi de suivre ses demandes de plats à la lettre, ou tu pourrais bien perdre ta vie.*")
            services.Ending.PrintEtEntreePourContinuer("*Car Ahmed est un maitre de la magie de visualisation, et après des années a servir dans la plus grande anxiétée un capricieux petit tyrant, il se peut que les règles avec lesquelles tu devras jouer pendant ce combat soient... tordues.*")
            pass  #  voix dit que font les autres ici, parle de Ahmed
        elif services.Player.numero_boss_alt == 4:
            services.Ending.PrintEtEntreePourContinuer("*Tu te débrouille bien, enfant maudit. Je suis fier de toi.*")
            services.Ending.PrintEtEntreePourContinuer("*Premièrement, parlons de ce que je fait ici.*")
            services.Ending.PrintEtEntreePourContinuer("*J'ai été attirée ici par la présence d'âmes puissantes, en attente de passer a la Vie d'Après.*")
            services.Ending.PrintEtEntreePourContinuer("*Et je suis tombée prisonnière de cet endroit, appelant avec ferveur quelqu'un comme toi.*")
            services.Ending.PrintEtEntreePourContinuer("*Exactement comme toi.*")
            services.Ending.PrintEtEntreePourContinuer("*Tu dois donc te demander ce qui se passe en dehors si la Grande Faucheuse est coincée ici ?*")
            services.Ending.PrintEtEntreePourContinuer("*Et bien... rien du tout.*\n*Et c'est bien ca le problème.*")
            services.Ending.PrintEtEntreePourContinuer("*Pour résumer assez rapidement, dis toi que je ne suis pas la pour briser le lien qui relie les corps et les esprit.*")
            services.Ending.PrintEtEntreePourContinuer("*Donc toutes les personnes décédées depuis un bon millénaire sont encore là, coincées dans leurs corps, incapable de bouger ou de s'exprimer, mais ressentant tout.*")
            services.Ending.PrintEtEntreePourContinuer("*L'enfer n'est rien à coté d'un millénaire déprivé de sensations et de mouvements.*")
            services.Ending.PrintEtEntreePourContinuer("*Dernièrement,*")
            services.Ending.PrintEtEntreePourContinuer("*L'adversaire que tu vas affronter ici est... délicat.*")
            services.Ending.PrintEtEntreePourContinuer("*Quand je suis arrivée là, c'était un monstre terrible a l'apparence trompeuse, maitrisant une armée incroyable.*")
            services.Ending.PrintEtEntreePourContinuer("*Mais aujourd'hui, je ne suis pas sûre.*")
            services.Ending.PrintEtEntreePourContinuer("*Fais juste attention a sa technique ancestrale, que seul lui peut reproduire malgrès les efforts constants de sa race.*")
            services.Ending.PrintEtEntreePourContinuer("*Lorsqu'il...*")
            services.Ending.PrintEtEntreePourContinuer("*...se remue comme un flanc.*")
            services.Ending.PrintEtEntreePourContinuer("*De plus, c'était a l'époque un berserker, doté d'une capacité inouie a maitriser sa rage.*")
            services.Ending.PrintEtEntreePourContinuer("*En clair, plus le temps passe, plus sa rage augmente, et plus il fait de dégâts.*")
            services.Ending.PrintEtEntreePourContinuer("*Note bien : je n'ai pas parlé de tours, mais bien de temps passé, secondes minutes et companie.*\n*Je sais que le temps passe différemment pour toi, mais dans ce combat vous êtes au même niveau.*")
            pass  #  voix dit enfermé par pierre, parle de roi gluant
        elif services.Player.numero_boss_alt == 5:
            services.Ending.PrintEtEntreePourContinuer("*Bon, je vois que tu es qualifié, il est maintenant temps de parler de mon plan.*")
            services.Ending.PrintEtEntreePourContinuer("*Premièrement, pour rentrer ici, il faut 50 redcoins.*\n*Mais sais tu ce que sont les redcoins ?*")
            services.Ending.PrintEtEntreePourContinuer("*C'est une accumulation de l'énergie des anciens dieux sous forme liquide.*\n*A donner aux mortels pour leur courage, ou a avaler en cas de pépin pour retrouver toute sa force divine.*")
            services.Ending.PrintEtEntreePourContinuer("*C'est une extention du pouvoir divin, une sorte de batterie rechargeable pour les Dieux.*")
            services.Ending.PrintEtEntreePourContinuer("*Et au vu de leur disparition, il n'en existe PAS, cinquantes en circulation.*")
            services.Ending.PrintEtEntreePourContinuer("*C'est pour ca que cette porte existe, car dans le système créé par la Pierre de Désir, il faut une condition pour tout, afin d'avoir un système équilibré et juste.*")
            services.Ending.PrintEtEntreePourContinuer("*En clair, on satisfait les conditions du système en te permettant de passer la porte, mais on empeche tout le monde de la passer en mettant des conditions impossibles a remplir.*")
            services.Ending.PrintEtEntreePourContinuer("*On obtient alors une porte infranchissable derriere laquelle enfermer ceux que l'on ne peut pas controller, entièrement.*")
            services.Ending.PrintEtEntreePourContinuer("*Sauf que tu as franchit cette porte.*")
            services.Ending.PrintEtEntreePourContinuer("*Parlons en au prochain étage.*")
            services.Ending.PrintEtEntreePourContinuer("*Dernièrement,*")
            services.Ending.PrintEtEntreePourContinuer("*Tu va affronter une personne bien singulière, en aucun cas lié au Coliseum.*")
            services.Ending.PrintEtEntreePourContinuer("*Sa présence est due a un problème impossible :*")
            services.Ending.PrintEtEntreePourContinuer("*Quelqu'un est rentré dans ce monde, en venant d'ailleurs.*")
            services.Ending.PrintEtEntreePourContinuer("*Je ne parle pas de Jean, mais d'un certain Pyrobarbare en quete d'aventure.*")
            services.Ending.PrintEtEntreePourContinuer("*Et comme le système est juste et equilibré, il faut une existence pour contrer sa présence.*")
            services.Ending.PrintEtEntreePourContinuer("*Voici comment est née Obo la Cryobarbare.*")
            services.Ending.PrintEtEntreePourContinuer("*C'est une création artificielle, je n'ai donc pas beaucoup d'informations sur elle.*")
            services.Ending.PrintEtEntreePourContinuer("*Je sais juste que la Pierre du Désir a eue beaucoup de mal a la mettre ici-bas, non pas a cause de sa force...*")
            services.Ending.PrintEtEntreePourContinuer("*...mais parce qu'elle est vraiment, mais alors VRAIMENT, énervante a combattre.*")
            pass  #  voix dit redcoin dupe, parle de Obo
        elif services.Player.numero_boss_alt == 6:
            services.Ending.PrintEtEntreePourContinuer("*Toujours là ?*\n*Toujours motivé ?*")
            services.Ending.PrintEtEntreePourContinuer("*Continuons.*")
            services.Ending.PrintEtEntreePourContinuer("*J'ai vu la manière dont tu as passé la porte.*")
            services.Ending.PrintEtEntreePourContinuer("*Tu t'es avancé , et il y avait déja quelques redcoins enfoncés dedans.*")
            services.Ending.PrintEtEntreePourContinuer("*Et parmis ces redcoins, il y en avait des identiques.*")
            services.Ending.PrintEtEntreePourContinuer("*Comment la porte que personne n'a jamais approché pouvait contenir des redcoins avec la même énergie ?*")
            services.Ending.PrintEtEntreePourContinuer("*Tu as, d'une certiane manière, dupliqué des redcoins.*")
            services.Ending.PrintEtEntreePourContinuer("*Je dirais même plus :*")
            services.Ending.PrintEtEntreePourContinuer("*Tu les as posé, avant.*")
            services.Ending.PrintEtEntreePourContinuer("*Il y a quelque chose en toi qui te pousse dans une direction inconnue, mais qui pourtant est toujours la bonne.*")
            services.Ending.PrintEtEntreePourContinuer("*Je me suis battue contre la Pierre de Désir, et ma divinité me permet de comprendre certaines choses qui sont...compliquées.*\n*C'est pour cette raison que je suis au courant pour le système ainsi que son administrateur.*")
            services.Ending.PrintEtEntreePourContinuer("*Mais il y a quelqu'un qui fait des choses incroyables, et qui utilise le sytème a son avantage pour tenter de battre celui qui l'a construit.*")
            services.Ending.PrintEtEntreePourContinuer("*Et ce quelqu'un...*")
            services.Ending.PrintEtEntreePourContinuer("*...peut garder certaines choses entre chaque tentatives ratées.*")
            services.Ending.PrintEtEntreePourContinuer("*C'est littéralement impossible, inconcevable, se dire qu'après une remise a zéro complète du Coliseum, certaines choses restent.*")
            services.Ending.PrintEtEntreePourContinuer("*Mais c'est la seule explication possible.*")
            services.Ending.PrintEtEntreePourContinuer("*En quoi ca m'aide ? Parlons en tout a l'heure.*")
            services.Ending.PrintEtEntreePourContinuer("*Dernièrement,*")
            services.Ending.PrintEtEntreePourContinuer("*J'ai déja utilisé tout mon temps de parole ici.*")
            services.Ending.PrintEtEntreePourContinuer("*Cette personne est un camarade mort avant la création du Coliseum, et je ne sais pas ce qu'il fait ici.*")
            services.Ending.PrintEtEntreePourContinuer("*Un camarade a qui ?*")
            services.Ending.PrintEtEntreePourContinuer("*Au Chevalier que l'on ne veut pas rencontrer.*")
            pass  #  voix dit objectif avec divinité, parle de Mercenaire
        elif services.Player.numero_boss_alt == 7:
            services.Ending.PrintEtEntreePourContinuer("*...*")
            services.Ending.PrintEtEntreePourContinuer("*...*")
            services.Ending.PrintEtEntreePourContinuer("*...*")
            services.Ending.PrintEtEntreePourContinuer("*bon.*")
            services.Ending.PrintEtEntreePourContinuer("*Parlons d'autres choses.*")
            services.Ending.PrintEtEntreePourContinuer("*Premièrement, j'espère que tu es familier avec l'histoire de la Guerre de l'Interdit*")
            services.Ending.PrintEtEntreePourContinuer("*Si tu ne l'es pas, un petit récapitulatif :*")
            services.Ending.PrintEtEntreePourContinuer("*Les Dieux fabriquent des machines qui utilisent leur divinité, pour voir jusqu'ou ils peuvent aller.*")
            services.Ending.PrintEtEntreePourContinuer("*Ils construisent une machine pour travers les dimensions, arrivent dans un monde et rentrent en guerre avec lui.*")
            services.Ending.PrintEtEntreePourContinuer("*Grosse bataille, ils recrutent un héros humain et 4 héros de quatres races différentes pour garder la porte vers ce nouveau monde, jusqu'à trouver un moyen de l'arreter ou de gagner la guerre.*")
            services.Ending.PrintEtEntreePourContinuer("*Re-Grosse bataille, ils envoient la machine et leurs gardiens dans une autre dimension, mais voila : le frere jaloux du leader s'accroche au groupe pendant son transfert.*")
            services.Ending.PrintEtEntreePourContinuer("*Et...on en sait pas plus.*")
            services.Ending.PrintEtEntreePourContinuer("*Par contre, ca fait sortir toutes les troupes de l'autre monde, Re-Re-Grosse bataille, et tout les dieux meurent, mais ils referment la porte.*")
            services.Ending.PrintEtEntreePourContinuer("*Cet endroit la, c'est un peu la soeur de la ou se trouve la machine.*")
            services.Ending.PrintEtEntreePourContinuer("*Il a juste prit cette apparence parce que c'est le domaine de la Mort, et il reflete toujours l'endroit ou y il a eu le plus de massacres.*")
            services.Ending.PrintEtEntreePourContinuer("*Si tu veut, on se trouve dans l'ancienne maison du Dieu de la Mort.*")
            services.Ending.PrintEtEntreePourContinuer("*Sacré endroit pour emprisonner le réceptacle de la Divinité de la Mort, hein ?*")
            services.Ending.PrintEtEntreePourContinuer("*Dernièrement,*")
            services.Ending.PrintEtEntreePourContinuer("*Le héros des humains, gardien de la porte interdite, est mort.*")
            services.Ending.PrintEtEntreePourContinuer("*Mais sa volontée a persistée.*")
            services.Ending.PrintEtEntreePourContinuer("*L'essence même de son sens du devoir, cristalisé dans un être plutot faible, mais qui n'abandonne jamais.*")
            services.Ending.PrintEtEntreePourContinuer("*Fais attention, a chaque fois qu'il revient a la vie, tu subira un effet élémentaire très fort !*")
            pass  #  voix dit histoire de l'endroit avec portail et tt, parle de Volontée Immortelle
        elif services.Player.numero_boss_alt == 8:
            services.Ending.PrintEtEntreePourContinuer("*Oui, revenons en au plan maintenant.*")
            services.Ending.PrintEtEntreePourContinuer("*Lorsque j'ai été capturé, on m'a enlevé ma divinité de la Mort, et on l'a placée quelque part ici.*")
            services.Ending.PrintEtEntreePourContinuer("*A la fin des Limbes.*")
            services.Ending.PrintEtEntreePourContinuer("*C'est plutot malin de la part de la Pierre de Désir, mettre un pouvoir absolu derriere une congrégation de 10 être extremement puissants, derriere une porte impossible a ouvrir.*")
            services.Ending.PrintEtEntreePourContinuer("*En plus, vu que l'on est dans un endroit qui représente une dimension dont laquelle rien ne devait sortir, même si quelqu'un récupère la divinité, il restera coincé ici a jamais.*")
            services.Ending.PrintEtEntreePourContinuer("*Ou jusqu'à ce que la Pierre de Désir vienne jeter un coup d'oeil et récupère le pauvre individu pour en faire un autre de ses boss.*")
            services.Ending.PrintEtEntreePourContinuer("*Sauf que tu n'es pas un individu normal.*")
            services.Ending.PrintEtEntreePourContinuer("*Tu peut prendre des objets appartenant aux dieux et faire comme si tu les avait toujours possédés.*")
            services.Ending.PrintEtEntreePourContinuer("*Et une fois que tu recommence la descente du Coliseum...*")
            services.Ending.PrintEtEntreePourContinuer("*...notre monde sera affecté de telle sorte que tu aura eu, d'aussi loin qu'on puisse se souvenir, la divinité en ta possession.*")
            services.Ending.PrintEtEntreePourContinuer("*On peut faire sortir la Mort de cette cage pour que les gens puissent recommencer a mourir proprement !*")
            services.Ending.PrintEtEntreePourContinuer("*Et vu que lorsque tu commence ton aventure, tu descend les marches du Coliseum...*")
            services.Ending.PrintEtEntreePourContinuer("*...alors tant que tu ne la commence pas, tu est en dehors du Coliseum !*")
            services.Ending.PrintEtEntreePourContinuer("*Tu ne comprend pas ?*\n*La mort reprend son cours tant que tu ne lance pas le système , car la mort ne sera plus piégée dans le Coliseum, mais en dehors !*")
            services.Ending.PrintEtEntreePourContinuer("*Je te dirait plus au prochain étage.*")
            services.Ending.PrintEtEntreePourContinuer("*Dernièrement,*")
            services.Ending.PrintEtEntreePourContinuer("*La combattante a cet étage s'appelle Eris.*")
            services.Ending.PrintEtEntreePourContinuer("*C'est la forme corporelle de la Déesse du chaos.*")
            services.Ending.PrintEtEntreePourContinuer("*Mais vu que la Déesse du Chaos est déjà morte il y a longtemps, je ne comprend pas ce que son corps divin fait là...*")
            services.Ending.PrintEtEntreePourContinuer("*...*")
            services.Ending.PrintEtEntreePourContinuer("*...*")
            services.Ending.PrintEtEntreePourContinuer("*Je comprend pas.*")
            services.Ending.PrintEtEntreePourContinuer("*Si elle est morte pendant la Guerre de l'Interdit, alors il ne devrait plus y avoir aucune trace d'elle, sauf pour sa divinité qui aurait rejoint un réceptacle adapté.*")
            services.Ending.PrintEtEntreePourContinuer("*Ca voudrait dire que...*")
            services.Ending.PrintEtEntreePourContinuer("*...*")
            services.Ending.PrintEtEntreePourContinuer("*Non.*")
            services.Ending.PrintEtEntreePourContinuer("*On arrête là.*")
            pass  #  voix dit Eris ? bizarre !, parle de Eris
        elif services.Player.numero_boss_alt == 9:
            services.Ending.PrintEtEntreePourContinuer("*...*")
            services.Ending.PrintEtEntreePourContinuer("*Voila ta tache.*")
            services.Ending.PrintEtEntreePourContinuer("*Bat les deux derniers combattants, récupère la divinité de la Mort, puis remet a zéro cette... ligne temporelle ?*\n*Ce monde ?*\n*Je ne sais pas.*")
            services.Ending.PrintEtEntreePourContinuer("*J'imagine que tu voudrais quand même une récompense pour cette quête ?*")
            services.Ending.PrintEtEntreePourContinuer("*Sache que posséder la divinité de la Mort sur toi te permettrait deux choses.*")
            services.Ending.PrintEtEntreePourContinuer("*Déja, tu vois les méchanismes anciens ?*")
            services.Ending.PrintEtEntreePourContinuer("*Ce sont en fait des méchanismes divin, créés par les Dieux pour tester les limites de leur pouvoir.*\n*En ayant la même aura que les dieux, tu possèdera la capacité de les utiliser a leurs plein potentiel.*")
            services.Ending.PrintEtEntreePourContinuer("*Un exemple parmis tant d'autres, tu as déja remarqué le double fond dans les coffres a artefacts ?*\n*Non ?*")
            services.Ending.PrintEtEntreePourContinuer("*C'est normal. Tu n'es pas un dieu. Car les dieux savent que les meilleurs artefacts sont dans le double fond de la boite a artefact.")
            services.Ending.PrintEtEntreePourContinuer("*Enfin, tu pourras aussi utiliser l'élément Ame.*\n*J'imagine que tu a déja vu le sigil des éléments, non ?*")
            services.Ending.PrintEtEntreePourContinuer("*Ca ne t'a jamais fait bizarre de pouvoir utiliser des talents pour tout les éléments, sauf pour l'élément Ame ?*")
            services.Ending.PrintEtEntreePourContinuer("*Et puis, en vrai, vu que toi, Terah, tu est le réceptacle de cette Divinité, je suis sur que tu pourrais débloquer un joli stigma si tu le possédait.*")
            services.Ending.PrintEtEntreePourContinuer("*...*")
            services.Ending.PrintEtEntreePourContinuer("*Ca ne suffit pas ?*")
            services.Ending.PrintEtEntreePourContinuer("*Alors je te le demande formellement.*")
            services.Ending.PrintEtEntreePourContinuer("*S'il te plait, Oh entité supérieure qui guide les pas des gens tombés dans le piège du Coliseum...*")
            services.Ending.PrintEtEntreePourContinuer("*Ramène la mort parmis ce monde.*")
            services.Ending.PrintEtEntreePourContinuer("*...*")
            services.Ending.PrintEtEntreePourContinuer("*S'il te plait.*")
            services.Ending.PrintEtEntreePourContinuer("*...*")
            services.Ending.PrintEtEntreePourContinuer("*Dernièrement,*")
            services.Ending.PrintEtEntreePourContinuer("*Tu a ici un amalgame de la souffrance des âmes retenues prisonnières dans le Coliseum.*")
            services.Ending.PrintEtEntreePourContinuer("*C'est la que la Pierre de Désir vient jeter les souffrances psychiques et émotionnelles de celles et ceux qui sont piégés.*")
            services.Ending.PrintEtEntreePourContinuer("*C'est un véritable spectre en quête de libertée.*")
            services.Ending.PrintEtEntreePourContinuer("*Il possède toutes les techniques et sorts que l'on peut gagner dans le Coliseum.*")
            services.Ending.PrintEtEntreePourContinuer("*Bonne chance.*")
            pass  #  voix dit histoire de l'endroit, pour elle, parle de Spectre
        elif services.Player.numero_boss_alt == 10:
            services.Ending.PrintEtEntreePourContinuer("...")
            services.Ending.PrintEtEntreePourContinuer("...")
            services.Ending.PrintEtEntreePourContinuer("...")
            services.Ending.PrintEtEntreePourContinuer("Je n'ai pas le choix.")
            pass  #  voix dit rien, parle pas
        services.Ending.PrintEtEntreePourContinuer("*C'est tout pour maintenant.*\n*Que la divinité de la mort emplisse ton coeur de sa puissance, enfant maudit.*")
        services.Ending.PrintEtEntreePourContinuer("Vous sentez l'énergie du vide tout autour s'infiltrer par vos pores, et gagnez 10 points de vie max ainsi que 10 points de mana max !")
        services.Player.points_de_mana_max += 5
        services.Player.points_de_mana += 5
        services.Player.points_de_vie_max += 10
        services.Player.points_de_vie += 10
    # fait que l'event soit finit et ne peut ps etre relancé
    salle["terminé par joueur"] = True


@salle_de_type("LEY")
def reveler_ley(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.ley()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print(
        "Alors que vous fouillez la pièce, vous ressentez une immense puissance dans le sol."
    )
    print(
        "Vous avez trouvé un ley !\nC'est un chemin que l'énergie de la nature parcourt."
    )
    services.Affichage.EntreePourContinuer()
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
        services.Affichage.EntreePourContinuer()
        print(
            "Au bout de plusieurs heures de sport intensif, votre corps gagne en puissance alors que votre vitalité est au max."
        )
        services.Affichage.EntreePourContinuer()
        print("Vous gagnez 4 points de vie max !")
        print("Vous reprenez tout vos points de vie !")
        print("Vous gagnez 1 point d'endurance ! ")
        services.Player.points_de_vie_max += 4
        services.Player.points_de_vie = services.Player.points_de_vie_max
        services.Player.points_dendurance += 1
        services.Affichage.EntreePourContinuer()
    else:
        print(
            "Vous faites la position du lotus au dessus du ley, et meditez."
        )
        print(
            "Votre esprit se fait remplir de sons, couleurs, et souvenirs que vous n'aviez jamais experiencé auparavant."
        )
        services.Affichage.EntreePourContinuer()
        print(
            "Au bout de lusieurs heures, vous arrivez a dompter la mémoire de la Terre, et votre réservoir de mana s'en trouve aggrandit."
        )
        services.Affichage.EntreePourContinuer()
        print("Vous gagnez 5 points de mana max !")
        print("Vous reprenez tout vos points de mana !")
        services.Player.points_de_mana_max += 5
        services.Player.points_de_mana = services.Player.points_de_mana_max
        services.Affichage.EntreePourContinuer()
    print("Le ley s'assèche, et disparait.")
    print("L'énergie a du trouver un autre endroit pour passer.")
    services.Affichage.EntreePourContinuer()

    # fait que l'event soit finit et ne peut ps etre relancé
    salle["terminé par joueur"] = True


@salle_de_type("MIMIQUE")
def reveler_mimique(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.mimique()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print("Vous trouvez un magnifique coffre doré !")
    print(
        "Ses reliures de cuivres, ses gravures de bois noble, ses contours en or fin vous attirent"
        " et remplissent votre coeur de cupidité !"
    )
    services.Affichage.EntreePourContinuer()
    print(
        "Seul bémol : une respiration sourde, saccadée, provenant d'une sorte d'idole de chair grandeur nature.\nAh oui, et le coffre est a moitié enfoncé dans le torse de la créature."
    )
    services.Affichage.EntreePourContinuer()
    while True:
        try:
            print("Que faire ?")
            print("\n1 - Approcher le coffre")
            print("2 - Inspecter les alentours")
            print("3 - Partir")
            choix = int(
                input("\nChoisissez votre action avec les nombres : ")
            )
            ClearConsole()
            if choix in [1, 2, 3]:
                break
        except ValueError:
            ClearConsole()
    if choix == 1:
        # lance le combat
        print(
            "L'idole se lève et vous attaque !"
        )
        services.Affichage.EntreePourContinuer()
        services.Player.affronte_une_mimique = True
        livrer_combat()
        services.Player.affronte_une_mimique = False
        PlayMusicDeLetage()

        # fait que l'event soit finit et ne peut ps etre relancé
        salle["terminé par joueur"] = True
    if choix == 2:
        if services.Player.numero_de_letage == 2 :
            print("Vous observez la clairière dans laquelle se trouve l'idole.\nIl y a de nombreuses iconographies de personnages divins, religieux, ou juste mythiques.")
            services.Affichage.EntreePourContinuer()
            print("Vous trouvez aussi des relicats de feux grandioses, et de cierges humbles, posés a même le sol noir et spongieux...")
            services.Affichage.EntreePourContinuer()
            print("...un frisson vous parcourt le dos.")
            services.Affichage.EntreePourContinuer()
            print("Vous vous retournez vers une chapelle décrépite que vous n'aviez pas vu avant. Le bois rongé par les âges crépites sous vos pieds, comme si il prenait feu, et au centre se trouve un livre étrange couvert d'une...")
            print("...")
            services.Affichage.EntreePourContinuer()
            print("Vous y lisez ceci :")
            services.Affichage.EntreePourContinuer()
            print("*Nous, êtres de vie.*")
            print("*Nous, êtres de chair.*")
            print("*Nous, êtres de volontés.*")
            services.Affichage.EntreePourContinuer()
            print("*Vidons nos calices de leur vie à tes pieds.*")
            print("*Adorons ton image des chairs puissantes qui rodent la nuit.*")
            print("*Remplissons ton être de notre volonté immolée.*")
            services.Affichage.EntreePourContinuer()
            print("*Si le monde prend pitié de notre souffrance , si il juge que nos prières sont assez dévouées, si il appose son sceau karmique sur nos existances,*")
            print("*Alors, dieu artificiel, tu verra le jour.*")
            print("*Et tu offrira la mort a ce qui en veut a notre vie, notre chair, notre volontée.*")
            services.Affichage.EntreePourContinuer()
            print("*Simule la divinité de ce qui a habité ces murs, et offre nous ta bénédiction.*")
            print("*Aide nous : Comment faire pour ne pas mourir ?*")
            services.Affichage.EntreePourContinuer()
            print("La dernière phrase de la page est écrite avec une encre rouge : *Pour ne pas mourir, il faut tuer*")
            services.Affichage.EntreePourContinuer()
            print("Le reste du livre opppose une resistance a l'ouverture, comme si les pages étaient collées entre elles.")
            print("Vous laissez la chapelle fantomatique derrière vous et retournez au centre de la clairière.")
            services.Affichage.EntreePourContinuer()
        elif services.Player.numero_de_letage == 4 :
            print("")
        elif services.Player.numero_de_letage == 6 :
            print("")
        elif services.Player.numero_de_letage == 8 :
            print("")
        elif services.Player.numero_de_letage == 10 :
            print("")
    else:
        print("Vous reculez prudemment.")
        services.Affichage.EntreePourContinuer()


@salle_de_type("PIEGE")
def reveler_piege(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.piege()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print(
        "Vous fouillez la salle...et déclenchez un piège en déplacant un meuble."
    )
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
                services.Player.points_de_vie = round(0.33 * services.Player.points_de_vie_max)
                print("Vous alliez mourir, mais votre fée sort de son bocal et vous sauve la mise. Ouf !")
                services.Affichage.EntreePourContinuer()
            else:
                StopAllMusic()
                PlaySound("death")
                print("Vous échouez a stopper le saignement, et perdez la vie.")
                services.Affichage.EntreePourContinuer()
                services.Player.player_tags.append("KIA")
                CheckForKIA()
        else:
            print(
                "Le piège se ré-enclenche.\nEvitez de fouiller cette salle dans le futur !"
            )
            services.Affichage.EntreePourContinuer()
    else:
        print("Cepandant, des éclats de glace se forment aux endroits ou les flèches auraient du se planter.")
        print("De plus, avant que les arbalettes ne puissent battre en retraite dans les murs de la salle, un froid glacial les éclate par gélifraction.")
        services.Affichage.EntreePourContinuer()
        print("Vous n'aurez plus a vous soucier de cette salle désormais !")
        services.Affichage.EntreePourContinuer()
        # fait que l'event soit finit et ne peut ps etre relancé
        salle["terminé par joueur"] = True


@salle_de_type("SECRET")
def reveler_secret(etage, salle):
    # dessine la salle, si ce n'est pas fait
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.secret()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    services.Observation.SeeSomething()
