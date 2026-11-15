"""Menu de démarrage : nouvelle partie, choix du personnage, chargement, tutoriel."""

from coliseum import services
from coliseum.audio import PlayMusic
from coliseum.console import ClearConsole
from coliseum.donnees.personnages import DICTIONNAIREDEPERSONNAGEAAFFICHER, LISTEDEPERSONNAGE
from coliseum.erreurs import WriteErrorInErrorLog
from coliseum.interface.secrets import ShowObservatorium, ShowRecup


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
    print(f"                              /      2 - Continuer : [{services.Player.nom_de_letage}] ")
    print("                             /       3 - Tutoriel       \ ")
    print("                            /                            \ ")
    print("                           /                              \ ")
    return int(
        input(
            "Choisissez une action avec le numéro correspondant, et appuyez sur Entrée pour continuer : "
        )
    )


def ChoseCharacter():
    ClearConsole()
    # recommence jusqu'à ce que le choix soit fait
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
                    if DICTIONNAIREDEPERSONNAGEAAFFICHER[choix] == "Neil" and (not services.Sove.ModifieTagsDansSove("Checke","Neil")):
                        pass
                    else:
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
                    services.Player.UseCharacterForInitCaracteristics(
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


def GetChoixPersonnageChoice():
    print("     -={ Personnages }=-")
    print("\n1 - Retour")
    for numero in DICTIONNAIREDEPERSONNAGEAAFFICHER:
        if DICTIONNAIREDEPERSONNAGEAAFFICHER[numero] == "Neil" and (not services.Sove.ModifieTagsDansSove("Checke","Neil")):
            pass
        else:
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
    services.Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("              { Partie 2 : Histoire }")
    print(
        "\nLe coliseum est une batisse ancienne, commandée par un roi fou a son magicien pour enfermer"
    )
    print(
        "les gens de son peuple qu'il croyait dangereux. Au fur et a mesure des années, de plus en plus"
    )
    print(
        "d'innocents se sont retrouvé dans les arènes sordides, a combattre des créations monstrueuses de chair et de sang."
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
    services.Affichage.EntreePourContinuer()
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
        "Chaques monstres tués vous rapporte une amélioration de certaines de vos caractéristiques, et un peu de golds."
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
    services.Affichage.EntreePourContinuer()
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
    services.Affichage.EntreePourContinuer()
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
    services.Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("            { Partie 5a : Le Coeur du Jeu }")
    print(
        "\nLe Coliseum s'explore en trois temps : "
        "\nLe temps de repos, ou menu d'étage, qui permet de choisir l'action a faire"
        "\nLe temps d'observation, afin d'observer toute les salles de l'étage pour trouver objets, artefacts, et salles particulières."
        "\nLe temps de combat, pour devenir plus fort ou battre le boss.\n"
    )
    services.Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("            { Partie 5b : Le Déroulement des Combats }")
    print("\nEn temps de combat, tout se déroule au tour par tour.\n")
    print("En premier lieu s'effectuent les actions de début de combat.\n\t[Certains effets de certaines actions, Artefacts, ou encore taaAAaal8lents se font avant le début du combat, au tour 0.]\n")
    print("Ensuite, vous choisissez un type d'action parmis celles disponibles.\n\t[Allez vous jeter un sort ? Effectuer une technique ? Utiliser un Item ?]\n")
    print("Juste après, vous choisissez une action dans le menu affiché.\n\t[Si vous avez choisit de lancer un sort, il faut maintenant dire quel sort en particulier.]\n")
    print("Votre action est effectuée, puis celle de l'ennemi a la suite.\n\t[En tant que combat au tour par tour classique, vous ne pouvez rien faire pendant que l'ennemi fait son action. Tout ou presque est déterminé par un mélange de nombres d'aléatoire et de comparaison de statistisques.]\n\t[Vous faire touhcer ou non, pour combien de points, tout cela est en dehors de votre controle immédiat , et ne dépend plus que d'une notion simple : Avez vous suffisamment préparé votre personnage ? Avec les bonnes caractéristiques ? Les bons items ? Les bons effets ? Tout est question de stratégie.]\n\t[Rares sont les attaques qui vous demandent expressément de faire quelque chose pour influer son résultat !]\n")
    print("Enfin, Les différents effets d'altérations d'états s'appliquent.\n\t[Etes vous entrain de bruler ? De reprendre des poitns de vie ? L'ennemi est il affecté par une quelquonque malédiction ? Les altération d'état, effectifs une fois par tour, se font a la fin du tour de l'ennemi, sauf si il est mort. Stratégisez au mieux le moment de votre victoire pour profiter le plus possible des altérations d'état qui vous sont bénéfiques !]\n")
    services.Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("            { Partie 5c : Nota Bene des Combats }")
    print("\nOn recommence ce cycle (Type Action Joueur > Action Joueur > Quelqu'un est mort/fuie ? > Sinon Action Ennemi > Alteration Etat > Quelqu'un est mort/fuie ?) jusqu'à ce qu'un des deux participant meure ou fuie.\n\t[La fuite est un faux ami. Non seulement vous perdez les objets utilisés pendant le conbat, vous ne gagnez pas de caractéristiques, mais en plus l'ennemi disparait pour de bon !]\n\t[D'un autre coté, cela vous permet de rester en vie.]\n\t[Mais d'un autre coté, la fuite n'est pas garantie, et il arrive parfois que celle ci soit interdite.]")
    print(
        "\nGardez a l'esprit que vos points de vie (PV) représentent la vitalité qu'il vous reste,"
        "\net que si ils tombent a zéro, c'est terminé.\n\nCepandant, les points de mana (PM) servent juste "
        "à lancer des sorts, et peuvent descendre a zéro sans réelles conséquences.\n\t[Gardez à l'esprit que les sorts font en général plus de dégat que les techniques, mais qu'il est plus difficile de récupérer des points de mana, surtout en début de jeu.]"
        "\n\nDe la meme maniere, pas de conséquence si vous n'avez plus de points d'endurance (PE), qui servent a utiliser des techniques et remontent naturellement.\n\t[Par *naturellement*, on entend *Entre chaque combats*. Si vous voulez faire remonter vos points d'endurance en plein combat, il faut faire une action qui n'en utilise pas : Sort, Item, Defense, ou encore Passer son Tour. Moins l'action demande de l'effort, plus elle est risquée, mais plus elle permet de reprendre des points d'endurances.]\n\t[Gardez bien cela a l'esprit : vous ne pouvez pas enchainer les techniques à l'infini ! Vous devez vous reposer de temps a autre !]"
    )
    print("\n\n")
    services.Affichage.EntreePourContinuer()
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
    services.Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("        { Partie 6b : Foire aux Questions }")
    print("\n*Ya un type bizarre qui execute les rochemikazes, de temps a autre. C'est qui ?*")
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
        " - C'est aussi exact ! Le fun du Coliseum vient du fait que vous êtes lachés dans un environnement étranger, sans guide,"
    )
    print(
        "et avec le moins d'expliquations possibles !"
        "\nAlors prenez un papier, un crayon, et notez au fur et a mesure les informations que vous découvrirez !"
    )
    print("\n\n")
    services.Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("            { Partie 7 : Message de l'Auteur }")
    print(
        "\nCe jeu est un rpg roguelight tour par tour textuel.\nSi vous n'avez rien compris a cette phrase, ce n'est pas grave.\nL'important, c'est ce mot : T E X T U E L"
    )
    print(
        "\nCe jeu ne possède pas (ou très très peu) de graphisme.\nLes lieux que vous allez découvrir, les combats que vous allez mener, les dialogues que vous allez vouloir passer, tout cela ne peut pas être montré : c'est donc écrit. Décrit.\nAu fil de longues lignes au langage fleuri et d'impressionnants paragraphes, vous allez pouvoir vivre cette aventure avec pour compagnons des musiques spécialements choisies, un carnet de note fouillu, et votre imagination débordante."
    )
    print("\nVous comprenez donc que si vous n'aimez pas lire, apprendre, ou imaginer a partir d'une ambiance, ce jeu n'est pas fait pour vous.\nJ'irais meme jusqu'a dire que vous allez passer a coté des clins d'oeils humoristiques, des incroyables secrets derrière lesquels se cachent la plupart du contenu, et du style d'écriture qui fait le charme de cet univers.\nJe ne peux imaginer aimer ce jeu tout en passant a coté de ces expériences.")
    print("\nJoueurs et Joueuses habitués des graphismes soignés, abhorrant la lecture des pavés de texte, passant a toute hate les descriptions qui construisent et mettent en place les mondes fantastiques dans lesquels ils évoluent,\nContinuez a vos risques et périls.")
    print("\n\n")
    services.Affichage.EntreePourContinuer()
    print("                    { Tutoriel }")
    print("            { Dernière Partie : Bonne chance ! }")
    print(
        "\nMaintenant, vous savez tout ce qu'il y a a savoir pour débuter une partie."
    )
    print(
        "Alors qu'attendez vous ? Ne soyez pas timide ! Il y a une montagne de chose a faire et a découvrir !"
    )
    print("Lancez donc une partie sans attendre, et dans l'échec apprenez a réussir !")
    print("\n\n")
    services.Affichage.EntreePourContinuer()
    PlayMusic("start")


def MenuDeDemarrage():
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
                    if services.Player.mode_de_jeu == "Véritable Descente":
                        services.Player.nom_de_letage = "Sanctuaire du Sacrifice"
                        services.Player.numero_de_letage = 0
                        services.Player.nombre_dennemis_a_letage = 0
                    else:
                        services.Player.nom_de_letage = "Ruines Abandonnées"
                    services.Save.FromPlayerToDict()
                    services.Save.FromDictToSaveFile("\\save.txt")
                    services.Save.FromSaveFileToDict()
                    services.Save.FromDictToPlayer()
                    services.Affichage.AffichageDescriptionEtage()
                    services.FloorMaker.SetupFloorLayout()
                    # personnage choisi
                    in_menu_principal = False
                    if  services.Sove.ModifieTagsDansSove("Checke","Livraison Terminée"):
                        services.Sove.ModifieTagsDansSove("Enleve","Livraison Terminée")
                        services.Sove.ModifieTagsDansSove("Ajout","Livraison En Attente")
                except Exception as error:
                    WriteErrorInErrorLog(error)

        # continuer une partie sauvegardee
        elif choix == 2:
            personnage_a_ete_choisi = services.Save.LoadTheGame()
            if personnage_a_ete_choisi:
                # sauvegarde chargée dans la classe Joueur
                in_menu_principal = False
                services.Affichage.AfficheChargement()
                if services.Player.mode_de_jeu == "Ascension" and (services.Player.numero_de_letage == 0):
                    services.Player.mode_de_jeu = "Descente"  

        # tutorial
        elif choix == 3:
            ShowTutorial()

        # Observatoire de musique
        elif choix == 1521951822120151892113:
            ShowObservatorium()

        # Recupérateur de secrets
        elif choix == 24:
            PlayMusic("gravestone")
            ShowRecup() 
            PlayMusic("start")
