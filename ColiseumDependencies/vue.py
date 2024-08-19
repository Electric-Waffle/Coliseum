import os
import sys
from pygame import mixer
import time


def clear_console():
    # Vérifier le système d'exploitation pour déterminer la commande appropriée
    os.system('cls' if os.name == 'nt' else 'clear')


class Vue:
    def __init__(self, Player):
        self.Player = Player
        mixer.init()
        DIRPATH = Player.chemin_musique
        self.CHEMINMUSIQUE = DIRPATH + "\\sfx\\"

    def AfficheSonSort(self, son):
        musique = self.CHEMINMUSIQUE + son + ".wav"
        self.SONSORT = mixer.Sound(musique)
        self.SONSORT.set_volume(0.5)
        self.SONSORT.play()

    def AfficheSonTechnique(self, son):
        musique = self.CHEMINMUSIQUE + son + ".wav"
        self.SONTECHNIQUE = mixer.Sound(musique)
        self.SONTECHNIQUE.set_volume(0.5)
        self.SONTECHNIQUE.play()

    def PlayMusic(self, musique):
        mixer.init()
        mixer.music.load(f"{musique}.mp3")
        mixer.music.play(-1)

    def PlaySound(self, musique):
        musique = self.CHEMINMUSIQUE + musique + ".mp3"
        mixer.init()
        mixer.music.load(musique)
        mixer.music.play()

    def PlayIntro(self, musique):
        mixer.init()
        mixer.music.load(f"{musique}.mp3")
        mixer.music.play()

    def PrintInfo(self, hp, damage): #old
        print(f"Vous avez fait {damage} points de dégats !")
        print(f"Il reste {hp} points de vie a l'ennemi.")

    def AffichageUneLignePuisUnEntreePourContinuer(self, commentaire):
        print(commentaire)
        self.EntreePourContinuer()

    def GetChoiceMana(self):
        print("Vous sentez vos nombreuses affinités se débattre à "
              "l'interieur de votre âme. Que souhaitez vous faire ?")
        print("1-Apaiser son esprit, calmer les élements.")
        print("2-Se servir de cette instabilitée dans vos sorts.")
        return int(input("(Faites votre choix :) "))

    def GetMenuChoice(
            self, nombre_tour, alteration_technique, alteration_sort,
            alteration_item, alteration_fuite, derniere_action_utilise,
            points_de_vie_monstre, points_de_mana_monstre,
            points_de_vie,
            points_de_vie_max, mana, manamax,
            endurance, endurance_max,
            nom_monstre, alteration_etat_monstre,
            alteration_etat_joueur, affiche_gold
            ):
        clear_console()
        print(f"          _-{{ Tour {nombre_tour} }}-_     ")
        print(f"     _-{{ Status - {nom_monstre} }}-_")
        print(f"          {points_de_vie_monstre} PV | {points_de_mana_monstre} PM")
        print(alteration_etat_monstre)
        print("")
        print(f"     _-{{ Status - {self.Player.nom_du_personnage} }}-_")
        print(f"  {points_de_vie}/{points_de_vie_max} PV | {endurance}/{endurance_max} PE | {mana}/{manamax} PM{affiche_gold}")
        print(alteration_etat_joueur)
        print("")
        print("     _-{ Choix du Joueur }-_")
        print("")
        print(f"1 Techniques {alteration_technique}")
        print(f"2 Sorts {alteration_sort}")
        print(f"3 Items {alteration_item}")
        print(f"4 Fuir {alteration_fuite}")
        print("5 Se défendre")
        print("6 Passer son tour")
        print(f"7 Derniere action : {derniere_action_utilise}")
        print("")
        return int(input("Choisissez une action avec les nombres : "))

    def ShowDebutMenuAction(self, nombre_tour, titre_menu):
        print("   _-{ Tour", nombre_tour, "}-_    ")
        print("   _-{", titre_menu, "}-_")
        print("")
        print("1 Retour")

    def ShowMenuAction(self, nombre, action, cout):
        print(f"{nombre} {action} [{cout}]")

    def ShowMenuActionItem(self, nombre, nom_item, quantite_item):
        print(f"{nombre} {nom_item} : {quantite_item}")

    def GetMenuActionChoice(self):
        print("")
        return int(input("Choisissez une action avec les nombres : "))

    def AfficheMonstreLevelMusique(self, nom, niveau, musique):
        self.PlayMusic(musique)
        print(f"L'ennemi [{nom}] de niveau {niveau} apparait !")
        self.EntreePourContinuer()

    def AfficherAttaquePremierTour(self, element, phrase_indiquant_la_reussite_ou_non):
        print(f"Avant même que l'ennemi n'aie le temps de bouger, vous placez {element}")
        print(phrase_indiquant_la_reussite_ou_non)
        self.EntreePourContinuer()

    def EntreePourContinuer(self):
        input("(Appuyez sur entrée pour continuer)")
        clear_console()

    def AfficheToucherDeMidas(self, degat, commentaire):
        print(f"Les golds dans vos poches se mettent a bruler. Vous perdez {degat} pv.")
        print(commentaire)
        self.EntreePourContinuer()

    def AfficheSiphonDeMana(self, mana_siphone):
        print("Vous sentez la présence de l'ennemi s'alourdir et se tordre.")
        print(f"{mana_siphone} points de mana se retrouvent aspirés hors "
              "de votre corps par ce puit de densité.")
        self.EntreePourContinuer()

    def GetFaveursExplosives(self, degat):
        print("L'ennemi se met a briller de manière étrange.")
        print("Il se prépare a exploser !")
        print(f"Si vous restez dans la salle, vous prendrez {degat} points de dégat. Que souhaitez-vous faire ?")
        print("1-Rester dans la salle, continuer le combat.")
        print("2-Fuir.") 
        return int(input("(Faites votre choix :)"))

    def AfficheFaveursExplosives(self, commentaire):
        print("Malgrès la force de l'explosion, vous arrivez à vous relever.")
        print(commentaire)
        self.EntreePourContinuer()

    def AfficheBenedictionDivine(self, vie_reprise):
        print("De par la bénédiction qu'a recu l'ennemi a sa naissance,")
        print(f"Il reprend {vie_reprise} points de vie.")
        self.EntreePourContinuer()

    def AfficheBomberman(self, vie_perdue):
        print("L'ennemi envoie une bombe furtive a l'endroit ou"
              " vous vous trouvez !")
        print("Elle explose avant que vous ne puissiez esquiver"
              f" et vous perdez {vie_perdue} points de vie.")
        self.EntreePourContinuer()

    def AffichePlusDUnTour(self, type_delement, description_element):
        print("L'ennemi tend son bras et une boule lumineuse sort de"
              " sa manche avant de vous rentrer dedans.")
        print(f"L'élément {type_delement} réagit violemment dans votre corps !")
        print(description_element)
        self.EntreePourContinuer()

    def AfficheMegalovania(self, vie_perdue):
        print("L'ennemi bouge, tourne, se pavane devant vous.")
        print("A tel point qu'il ne voit pas une colonne de "
              "pierre et rentre violemment dedans.")
        print(f"Il perd {vie_perdue} points de vie !")
        self.EntreePourContinuer()

    def AfficheHomoncule(self, vie_perdue):
        print("La vie artificielle qui se tient devant vous perd en "
              "vitalité au fur et a mesure que le combat s'éternise.")
        print(f"L'ennemi perd {vie_perdue} points de vie.")
        self.EntreePourContinuer()

    def AffichePatchwork(self, vie_perdue):
        print("L'ennemi perd des bouts de son corps sans sourciller.")
        print("On dirait qu'il ne ressent plus la douleur...")
        print(f"Mais cela ne l'empeche pas de perdre {vie_perdue} points de vie.")
        self.EntreePourContinuer()

    def AfficheArlequin(self, type_delement, description_element):
        print("L'ennemi tend son bras et une boule lumineuse sort de"
              " sa manche... avant de venir s'écraser sur son torse.")
        print("FAIR PLAY ! FAIR PLAY ! MUAHAHAHAH !")
        print(f"L'élément {type_delement} semble réagir violemment dans son corps !")
        print(description_element)
        self.EntreePourContinuer()

    def AfficheMalJaune(self):
        print("L'ennemi conjure une sphère de lumière qui s'élève dans les airs.")
        print("La salle se retrouve baignée dans une teinte dorée.")
        print("Vous commencez à avoir la tête qui tourne et seul le"
              " tintement des gold dans votre poche semble pouvoir vous calmer.")
        print("Vous êtes touché par le Mal Jaune ! Vos actions coutent des pièces !")
        self.EntreePourContinuer()

    def AfficheBeniParLesFees(self, sante_recupere):
        print("De par la bénédiction que vous avez recu a la naissance,")
        print(f"Vous reprenez {sante_recupere} points de vie !")
        self.EntreePourContinuer()

    def AfficheAngeDechue(self, limite):
        print()
        print(f"Parce que vos points de vie sont inferieurs a {limite},"
              "Votre enveloppe charnelle vous lache. "
              "Vous n'avez le temps de faire qu'une seule action avant de "
              "définitivement fermer vos yeux sur le monde.")
        self.EntreePourContinuer()

    def AfficheRaisonDePasserTour(self, personnage, commentaire):
        print(f"{personnage} tour...")
        print(commentaire)
        self.EntreePourContinuer()

    def AfficheFeuEtPoison(self, personnage, commentaire):
        print(personnage)
        print(commentaire)
        self.EntreePourContinuer()

    def AfficheAatmaEtJindagee(self, commentaire, soin, type_de_soin):
        print(commentaire)
        print(f"Vous regagnez {soin} points de {type_de_soin} !")
        self.EntreePourContinuer()

    def AfficheRegenerationMonstre(self, soin):
        print(f"L'ennemi récupere {soin} points de vie.")
        self.EntreePourContinuer()

    def ShowGameOverScreen(self, musique1, musique2):
        mixer.init()
        mixer.music.load(f"{musique1}.mp3")
        mixer.music.play()
        print("Votre vision se brouille, et bientôt le monde entier se résume a une tache floue dans l'horizon.")
        print("Vous refermez vos yeux pour la toute dernière fois.")
        self.EntreePourContinuer()
        print("[AVENTURE TERMINE]")
        self.EntreePourContinuer()
        print("[CALCUL DE LA CONTRIBUTION DU PERSONNAGE EN COURS...]")
        time.sleep(3)
        clear_console()
        print("[CALCUL TERMINE]")
        self.EntreePourContinuer()
        print("[CONTRIBUTION DU PERSONNAGE INSUFFISANTE]")
        self.EntreePourContinuer()
        print("[REALISATION DU DESIR REFUSEE]")
        self.EntreePourContinuer()
        print("[MORT VALIDEE]")
        self.EntreePourContinuer()
        self.PlayMusic(musique2)
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

    def AfficheResultatFuite(self, commentaire):
        print("Vous tentez de prendre la fuite...")
        print(commentaire)
        self.EntreePourContinuer()

    def AfficheFuite(self, musique, commentaire):
        mixer.init()
        mixer.music.load(f"{musique}.mp3")
        mixer.music.play()
        print(commentaire)
        self.EntreePourContinuer()

    def AfficheWinObelisque(self, musique):
        mixer.init()
        mixer.music.load(f"{musique}.mp3")
        mixer.music.play()
        print("Vous avez remporté le combat !")
        self.EntreePourContinuer()
        print("Mais alors que vous vous approchez de l'ennemi pour absorber sa puissance,"
              " vous le voyez se dissoudre et ne laisser rien derriere lui.")
        self.EntreePourContinuer()
        mixer.quit()

    def AfficheTitreRecompense(self, musique, nom):
        self.PlayMusic(musique)
        print("Vous avez remporté le combat !")
        print(f"Vous absorbez la puissance de l'ennemi [{nom}].")

    def AfficheRecompense(self, commentaire):
        print(commentaire)

    def AfficheNouveauMonstre(self, ancien_nom, nouveau_nom):
        print(f"L'ennemi [{ancien_nom}] profite de votre pitié pour s'enfuir.")
        print(f"Il se fait remmplacer par l'ennemi [{nouveau_nom}] !")
        self.EntreePourContinuer()

    def GetStigmaDernierChoixChoice(self):
        print("Vous lancez un regard froid a l'ennemi. Vous êtes désormais le seul garant de son futur.")
        print("Vous pouvez :")
        print("1 - Laisser l'ennemi partir et se faire remplacer par un autre de même niveau")
        print("2 - Garder l'ennemi actuel")
        return int(input("Choisissez une action avec les nombres : "))

    def AfficheSanjiva(self):
        print("Le destin de votre âme est entremêlé avec les fils de la Mort.")
        print("Sanjiva, l'enfer des 1000 reincarnations, vous accueille à bras ouverts.")
        print("Vos points de vie sont remis à un nombre acceptable.")
        self.EntreePourContinuer()

    def AfficheAddict(self):
        print("L'ennemi montre des signes de manque.")
        print("Cela fait un bon bout de temps que le combat a commencé et qu'il n'a pas eu sa dose de meurtre journalière.")
        print("Vous le voyez passer par tout les états du sevrage...")
        print("...Sueurs froides, Hallucinations, Assèchement de la bouche...")
        print("...Arrêt Cardiaque.")
        print("La vie quitte doucement le corps de l'ennemi.")
        self.EntreePourContinuer()

    def IntroAlfred(self, musique):
        self.PlayMusic(musique)
        print("L'ennemi disparait dans un nuage de poussière. En plein "
              "milieu, un homme (?) dans une tenue de maitre hotelier"
              " vous regarde d'un air amusé.")
        print("Sa peau blanchâtre semble avoir la consistance de la craie,"
              " et ses cheveux"
              " noirs de jais bien entretenus trahissent un style de vie"
              " plus que confortable.")
        print("- Bien le bonjour, pantin. Vous étiez entrain de vous battre"
              " avec l'un de"
              " mes fournisseurs, et je n'ai pas pu m'empecher de venir vous"
              " voir de plus près.")
        self.EntreePourContinuer()
        print("- Je me prénomme Alfred, mais il y a de grandes chances que"
              " vous le saviez déja, pas vrai ?")
        print("*Alfred décoche un sourire emplit de malice à un angle de la"
              " pièce."
              " Vous croyez apercevoir d'innombrables dents sous ses lèvres"
              " blanches.*")
        self.EntreePourContinuer()
        print("- Arrêtons ici la fausse politesse. Je viens de sauver la peau"
              " du pantin au prix de la vie de mon ami. Vous me devez quelque"
              " chose.")
        print("- Vous me devez...un jeu. Répondez juste à ma question ou je "
              "me sert en ressources directement sur vous.")
        self.EntreePourContinuer()
        print("- Prêt ? Voyons voir...")
        self.EntreePourContinuer()

    def AlfredChoice(self, question, reponse1, reponse2, reponse3, reponse4):
        print(question)
        print(reponse1)
        print(reponse2)
        print(reponse3)
        print(reponse4)
        return int(input("Choisissez une réponse avec les nombres : "))

    def FinAlfred(self, commentaire, commentaire2, commentaire3):
        print("- Hum... Si je me souviens bien...")
        self.EntreePourContinuer()
        print(commentaire)
        print(commentaire2)
        self.EntreePourContinuer()
        print(commentaire3)
        self.EntreePourContinuer()
        print("- Sur ce, bonne journée et à la prochaine fois !")
        print("*Alfred disparait dans un nuage de poussière. Le même que celui"
              " dans lequel il est apparu mais qui se propage... a l'envers ?*")
        self.EntreePourContinuer()

    def AfficheConsumme(self, nombre_tour):
        print("Tel un papillon de nuit, la vie de l'ennemi est liée a un cycle"
              " de naissance et de mort invisible et introuvable au niveau humain.")
        print(f"Et au tour {nombre_tour}, le cycle recommence.")
        print("L'ennemi stoppe tout mouvements sans prévenir, et "
              "la lueur de vie dans ses yeux s'éteint tout aussi brusquement.")
        self.EntreePourContinuer()

    def AfficheCircuitsLogiques(self):
        print("L'ennemi reconnait que la situation est critique.")
        print("Ses circuits logiques s'activent et mettent un place un protocole de fuite.")
        print("Des fils sortent du dos de l'ennemi tels de long tentacules de cuivre.")
        print("Ils s'accrochent a votre tête et envoient une impulsion dans une zone ciblée de votre cerveau.")
        self.EntreePourContinuer()
        print("Sans savoir pourquoi, vous vous mettez a fuir le combat !")
        self.EntreePourContinuer()

    def AfficheFinAlterationEtat(self, commentaire):
        print("_/[ Mise a Jour des Alterations d'Etat ]\\_")
        print(commentaire)
        print("")
        self.EntreePourContinuer()

    def AfficheSortOuAttaque(self, description, commentaire_a_afficher, commentaire_degat):
        print(description)
        print(commentaire_a_afficher)
        print(commentaire_degat)
        self.EntreePourContinuer()

    def AfficheActionImpossible(self, raison_si_action_pas_possible):
        self.AffichageUneLignePuisUnEntreePourContinuer(raison_si_action_pas_possible)
    
    def AfficheResurrection(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheMontagne(self, commentaire):
        self.AfficheSonSort("DIRTm")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
    
    def AfficheGriffe(self, commentaire):
        self.AfficheSonSort("DARK")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheQuete(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AffichageSacrifice(self, commentaire1, commentaire2, commentaire3, commentaire4):
        mixer.quit()
        print(commentaire1)
        self.EntreePourContinuer()
        print(commentaire2)
        self.EntreePourContinuer()
        print(commentaire3)
        self.EntreePourContinuer()
        print(commentaire4)
        self.EntreePourContinuer()

    def AfficheLiberationPhysique(self, commentaire, commentaire_malus):
        self.AfficheSonSort("PHYSm")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_malus)

    def AfficheDebutComboElectrique(self, commentaire):
        self.AfficheSonSort("ELECt")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheComboElectrique(self, commentaire, paralysie):
        print(commentaire)
        print(paralysie)
        self.EntreePourContinuer()

    def AfficheFinComboElectrique(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheMassif(self, commentaire):
        self.AfficheSonSort("DIRTm")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheBluff(self, commentaire):
        self.AfficheSonSort("PHYSt")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheDebutIaido(self):
        print("Vous rangez votre lame dans son fourreau et sacrifiez vos 3 prochains tours pour effectuer une coupe parfaite.")
        self.EntreePourContinuer()

    def AfficheIaido(self, commentaire):
        self.AfficheSonSort("ULTIMEt")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheAdrenaline(self, commentaire):
        self.AfficheSonSort("PHYSt")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheRafale(self, commentaire):
        self.AfficheSonSort("FIREm")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheAvalanche(self, commentaire):
        self.AfficheSonSort("ICEm")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheLiberationFeu(self, commentaire, commentaire_2):
        self.AfficheSonSort("FIREm")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_2)

    def AfficheLiberationFoudre(self, commentaire, commentaire_2):
        self.AfficheSonSort("ELECm")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_2)

    def AfficheLiberationGlace(self, commentaire, commentaire_2):
        self.AfficheSonSort("ICEm")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_2)

    def AfficheLiberationSang(self, commentaire, commentaire_2):
        self.AfficheSonSort("BLOODm")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_2)

    def AfficheLiberationTerre(self, commentaire, commentaire_2):
        self.AfficheSonSort("DIRTm")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_2)

    def AfficheMirroirEau(self, commentaire):
        self.AfficheSonSort("ICEm")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheBrumeSang(self, commentaire):
        self.AfficheSonSort("BLOODm")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheFeuSacre(self, commentaire):
        self.AfficheSonSort("FIREm")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheDebutCarrousel(self, commentaire):
        self.AfficheSonSort("ULTIMEm")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheCarrousel(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
    
    def AfficheFinCarrousel(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheBenedictionMana(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheMaledictionMana(self, degat_malediction_du_mana):
        print(f"Les éléments se débattent dans votre âme et vous infligent {degat_malediction_du_mana} points de vie.")
        self.EntreePourContinuer()

    def AfficheUtilisationItem(self, commentaire, commentaire_item):
        print(commentaire)
        print(commentaire_item)
        self.EntreePourContinuer()

    def AfficheSortDeSoin(self, commentaire_sort, commentaire_description_du_sort, commentaire_soin):
        self.AfficheSonSort("HEAL")
        print(commentaire_sort)
        print(commentaire_description_du_sort)
        print(commentaire_soin)
        self.EntreePourContinuer()

    def AfficheTransmutationDegat(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheDebutComboFeu(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheComboFeu(self, commentaire, paralysie):
        print(commentaire)
        print(paralysie)
        self.EntreePourContinuer()

    def AfficheFinComboFeu(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheVolepiece(self, commentaire, commentaire_reussite):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_reussite)

    def AfficheBanditManchot(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
    
    def AfficheRouletteBanditManchot(self, commentaire):
        print(commentaire)
        time.sleep(1)

    def AfficheCatastrophe(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheFinCatastrophe(self, commentaire, commentaire_2, commentaire_3):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_2)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_3)

    def SonLent(self, commentaire, commentaire_2):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_2)

    def AfficheDebutVoleAme(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheFinVoleAme(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def GetChoiceVoleAme(self, commentaire, commentaire_2):
        print(commentaire)
        return int(input(commentaire_2))
    
    def AfficheRituel(self, commentaire, commentaire_2, commentaire_degat):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_2)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_degat)

    def AfficheTempeteOuVacarme(self, commentaire, commentaire_effet):
        print(commentaire)
        print(commentaire_effet)
        self.EntreePourContinuer()

    def AfficheTempeteOuVacarmeAvecEffet(self, commentaire_effet):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_effet)

    def AfficheVide(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheEveilDeRunes(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheLamentations(self, commentaire, commentaire_2, commentaire_3):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_2)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_3)

    def AfficheInvoquationCanope(self, commentaire_description, commentaire_vase, commentaire_effet):
        print(commentaire_description)
        print(commentaire_vase)
        self.EntreePourContinuer()
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_effet)

    def AfficheDebutMagieNoire(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheMagieNoire(self, commentaire, commentaire_effet):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_effet)

    def AfficheSortUltime(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheTournicotons(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def GetTournicotonsChoix(self, commentaire):
        print(commentaire)
        return int(input("Choisissez une réponse avec les nombres : "))
    
    def AfficheDirectionTournicotons(self, direction_a_afficher):
        print(direction_a_afficher)
        time.sleep(0.5)
        clear_console()

    def AfficheDragonAscendant(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def GetDragonAscendantChoix(self, commentaire):
        print(commentaire)
        return int(input("Choisissez une réponse avec les nombres : "))
    
    def AfficheDirectionDragonAscendant(self, direction_a_afficher):
        print(direction_a_afficher)
        time.sleep(0.8)
        clear_console()

    def AfficheDebutTournicota(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheTournicota(self, commentaire, commentaire_reussite, commentaire_effet):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_reussite)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_effet)

    def GetChoixTournicota(self, commentaire):
        print(commentaire)
        return int(input("Choisissez une réponse avec les nombres : "))
    
    def AfficheTournicotez(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
    
    def GetChoixTournicotez(self, commentaire):
        print(commentaire)
        return int(input("ALORS-LORS ? DONNE-ONNE MOI LE NUMEROS DE CE QUE JE VAIS TE FAIRE ! : "))
    
    def AfficheTomeDeSalomon(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheUltimeUltime(self, commentaire_description, commentaire_reussite):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_description)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_reussite)

    def AfficheUltima(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheDebutUltimaError(self, commentaire):
        print(commentaire)
        time.sleep(2)
        clear_console()
    
    def AfficheUltimaError(self, commentaire):
        print(commentaire)
        clear_console()

    def AfficheDurcissementArgilite(self, commentaire, commentaire_effet):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_effet)

    def AfficheDurcissementCalcaire(self, commentaire, commentaire_effet):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_effet)

    def AffichePanaceeUniverselle(self, commentaire, commentaire_effet):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_effet)

    def AfficheEnvol(self, commentaire, commentaire_effet):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_effet)

    def AfficheHurlement(self, commentaire, commentaire_effet):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_effet)

    def AfficheAttireGold(self, commentaire, commentaire_reussite):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_reussite)

    def AfficheCoupAntiMagie(self, commentaire, commentaire_effet):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_effet)

    def AfficheAttireMana(self, commentaire, commentaire_reussite):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_reussite)

    def AfficheAspiration(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheLaser(self, commentaire, commentaire_effet):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_effet)

    def AfficheDebutRoulette(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def GetRouletteChoix(self, commentaire_mise):
        print(commentaire_mise)
        return int(input("Choisissez une réponse avec les nombres : "))
    
    def AfficheMiseImpossibleRoulette(self):
        print("Vous n'avez pas assez d'argent !")
        self.EntreePourContinuer()

    def AfficheResultatRoulette(self, commentaire, temps):
        print(commentaire)
        time.sleep(temps)
        clear_console()

    def AfficheFinRoulette(self, commentaire_effet, commentaire_mise):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_effet)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_mise)

    def AfficheGemmeBleue(self, commentaire, commentaire_reussite):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_reussite)

    def AfficheDebutComboMiserable(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheComboMiserable(self, commentaire, malediction):
        print(commentaire)
        print(malediction)
        self.EntreePourContinuer()

    def AfficheFinComboMiserable(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheCrystalElementaireDore(self, commentaire, commentaire_item):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_item)

    def AfficheSablesDuTemps(self, commentaire, commentaire_effet):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_effet)

    def AfficheTalentPyrophile(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheTalentPyrosorcier(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheTalentPyromage(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheAntiNeurotransmetteur(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheLuciole(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheTalentEclatDeGlace(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheTalentCycleGlaciaire(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheTalentConditionLimite(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheTalentMetamorphose(self):
        print("Mais vous êtes en état de métamorphose, et les dégâts affichés ne comptent plus.")
        self.EntreePourContinuer()

    def AfficheTalentUltraInstinct(self, commentaire, commentaire_resultat):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_resultat)

    def AfficheTalentMaitreDuMana(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheTalentRejuvenation(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def GetStigmaDernierChoixEnnemyChoice(self, commentaire):
        print(commentaire)
        return int(input("Choisissez une réponse avec les nombres : "))
    
    def AfficheResurrectionApprenti(self, musique):
        mixer.quit()
        print(" *Je...Je...vais mourir ?* ")
        print(" *non...* ")
        dummies = input("Appuyez sur entree pour continuer")
        clear_console()
        print(" *Je...Je...vais mourir ?* ")
        print(" *NON...* ")
        dummies = input("Appuyez sur entree pour conTUNIER")
        clear_console()
        print(" *Je...Je...vais mourir ?* ")
        print(" *NON ! NON ! NON ! NON ! NON ! NON !* ")
        dummies = input("Appuyez sur entree pour )àç_è_ç%%")
        clear_console()
        print(" *Je...Je...vais mourir ?* ")
        print(" *NONNONNONNONNONNONNONNONNONNONNONNONNONNONNONNONNONNONNONNONNONNONNONNONNONNONNONNONNONNON* ")
        dummies = input("Appuyez sur entree%%%%%%§/%M/%/%M/.8765")
        clear_console()
        print(" *Je...Je...vais mourir ?* ")
        print(" *NOOOOOOOOOOOOOOOOOONNNNNNNNNNNNNNNNNNNNNNNNNN22223334E4444487898767890¨%§/.§%§§§§§§§§§§§§§§§§* ")
        dummies = input("¨%¨£%¨%§§%¨%§/../°09entree°0987654323456¨%%%%§§§§§§§§§§§§")
        clear_console()
        time.sleep(2)
        clear_console()
        print("L'apprenti brise son amulette !")
        time.sleep(3)
        clear_console()
        print("L'apprenti ouvre une fAAille dimensionnelle !")
        time.sleep(5)
        clear_console()
        print("Vouuuuuuujjjjjj VOUs faites ASPIRER dnades !")
        time.sleep(3)
        clear_console()
        print("*JEEEEEE NEEEEE VAIIIIIISSS PAAAAAAAAASSSSS MOOOOOOOOUUUUURRRRRIIIIIRRRRRR !!!!!!§§§§§§§!§!§§!!§!*")
        time.sleep(3)
        clear_console()
        self.PlayMusic(musique + "boss_4_phase_2")
        print(" (l'apprenti fait des signes magiques dans les airs et commence a grandir, augmenter de taille."
              " Sa peau devient noir. Sa puissSSSaNNce eSSSSttt décucucucucucucuplée. Son apprence est ppppproche d'un oni, démon japonais......;;;;;////)")
        time.sleep(9)
        clear_console()
        print(" (L'apprentiOIBENOUQEFJQNOHULe MINARAI recouvre des points de vie !")
        time.sleep(3)
        clear_console()
        print(" *JJJJjjjjjjjeeeee n''''''aaaaiiii   paaaaassaspapassss ffaittitittt tooooooottotouutuuttuttt ccccaaaaaa poppouuuuuuurrrr rrrrriieenenenennnnn !!!*")
        time.sleep(5)
        clear_console()
        print(" *ETTTTT TOIIIII ????????*")
        time.sleep(4)
        clear_console()
        print("*TTTTTUUUUUUU*")
        time.sleep(4)
        clear_console()
        print("*VVVVVAAAAAA*")
        time.sleep(4)
        clear_console()
        print("*MMMMOURRRIRR*")
        time.sleep(4)
        clear_console()
        self.EntreePourContinuer()

    def AfficheResurrectionArmeeAnge(self, musique):
        mixer.quit()
        print("L'Arméee des Anges commenca a devenir plus épars.'")
        self.EntreePourContinuer()
        print("La victoire semblait être a portée.")
        self.EntreePourContinuer()
        print("Vesperum avait assez fait de degat pour rentrer en contact avec des anges plus hauts placés.")
        self.EntreePourContinuer()
        print("Et pourtant...")
        self.EntreePourContinuer()
        print("Il ne pu que regarder, muet, alors que l'armée des démons rejoignit l'armée des Anges")
        self.EntreePourContinuer()
        print("Ce que signifiait sa présence, la réponse que les êtres divins ont apportés quand a sa puissance...")
        self.EntreePourContinuer()
        print("C'était une véritable Armée de la Fin.")
        time.sleep(3)
        self.PlayMusic(musique + "story_end")
        clear_console()

    def AfficheResurrectionArchange(self, musique):
        mixer.quit()
        print("L'Armée de la Fin commenca a devenir plus épars.")
        self.EntreePourContinuer()
        print("Et a ce moment...")
        self.EntreePourContinuer()
        print("...le combat s'arrêta.")
        self.EntreePourContinuer()
        print("Les combattants des deux cotés s'agenouillèrent.")
        self.EntreePourContinuer()
        print("Un Archange descendit des cieux.")
        self.EntreePourContinuer()
        print("*Emilien. Arrête donc ta quête. Tu ne peux retrouver Sainte Elisa. IL en a besoin.*")
        self.EntreePourContinuer()
        print("Vesperum se releva et lanca a l'archange un regard de défi.")
        self.EntreePourContinuer()
        print("*Si IL n'est pas assez concerné pour venir me proposer un autre deal..*")
        self.EntreePourContinuer()
        print("*...ca doit être parceque je n'ai pas encore tué un archange !*")
        time.sleep(3)
        self.PlayMusic(musique + "story_end")
        clear_console()

    def AfficheResurrectionMaitreMage(self, musique):
        mixer.quit()
        print("Le Maitre Mage pose un genou a terre, et commence a haleter.")
        self.EntreePourContinuer()
        print("*C'est que je suis plus tout jeune moi !*\n*Tu sais depuis combien de centaines d'années je poireaute ici ??*")
        self.EntreePourContinuer()
        print("Vous vous demandez depuis combien de centaines d'années il poireaute ici.")
        self.EntreePourContinuer()
        print("*...pas bavard. Je vois. C'est parce que tu es décu du combat ?*")
        self.EntreePourContinuer()
        print("*Ne t'inquiète pas. C'est pas...*")
        time.sleep(3)
        self.PlayMusic(musique + "boss_8_phase_2")
        clear_console()
        print("Des ailes de mana sortent du dos du Maitre Mage.")
        time.sleep(3)
        clear_console()
        print("*...encORE...*")
        time.sleep(2)
        clear_console()
        print("Le mana environnant se met a trembler, et la foule hurle son engouement...")
        time.sleep(3)
        clear_console()
        print("*...FINI !*")
        time.sleep(2)
        clear_console()
        print("Vous assistez a la métamorphose du Maitre Mage en Ministre du Mana, grand commandant des forces de la nature !")
        self.EntreePourContinuer()

    def AfficheResurrectionColiseum(self, musique):
        mixer.quit()
        print("")
        self.EntreePourContinuer()
        self.PlayMusic(musique + "boss_10_phase_2")

    def AfficheResurrectionCauchemard(self, musique):
        mixer.quit()
        print("intro de la phase 2")
        self.PlayIntro(musique + "alt_1_phase_2_intro")
        self.EntreePourContinuer()
        print("Phase 2")
        self.EntreePourContinuer()
        self.PlayMusic(musique + "alt_1_phase_2")

    def AfficheResurrectionAhmedEntree(self, musique):
        mixer.quit()
        self.EntreePourContinuer()
        print("Phase 2")
        self.EntreePourContinuer()
        self.PlayMusic(musique + "alt_3_phase_2")

    def AfficheResurrectionAhmedPlat(self, musique):
        mixer.quit()
        self.EntreePourContinuer()
        print("Phase 3")
        self.EntreePourContinuer()
        self.PlayMusic(musique + "alt_3_phase_3")

    def AfficheResurrectionGluancelot(self, musique):
        mixer.quit()
        print("intro de la phase 1")
        self.PlayIntro(musique + "alt_4_phase_1_intro")
        self.EntreePourContinuer()
        print("Phase 1")
        self.EntreePourContinuer()
        self.PlayMusic(musique + "alt_4_phase_1")

    def AfficheResurrectionVolonteeImmortelle(self, musique):
        mixer.quit()
        self.EntreePourContinuer()
        print("Phase 2")
        self.EntreePourContinuer()
        self.PlayMusic(musique + "alt_7_phase_2")

    def AfficheResurrectionVolonteePersistante(self, musique):
        mixer.quit()
        self.EntreePourContinuer()
        print("Phase 3")
        self.EntreePourContinuer()
        self.PlayMusic(musique + "alt_7_phase_3")

    def AfficheResurrectionVolonteeInstable(self, musique):
        mixer.quit()
        print("intro de la phase 4")
        self.PlayIntro(musique + "alt_7_phase_4_intro")
        self.EntreePourContinuer()
        print("Phase 4")
        self.EntreePourContinuer()
        self.PlayMusic(musique + "alt_7_phase_4")

    def AfficheResurrectionSpectre(self, musique):
        mixer.quit()
        self.EntreePourContinuer()
        print("Phase 2")
        self.EntreePourContinuer()
        self.PlayMusic(musique + "alt_9_phase_2")

    def AfficheResurrectionAurore(self, musique):
        mixer.quit()
        print("intro de la phase 2")
        self.PlayIntro(musique + "alt_10_phase_2_intro")
        self.EntreePourContinuer()
        print("Phase 2")
        self.EntreePourContinuer()
        self.PlayMusic(musique + "alt_10_phase_2")

    def AfficheJugement(self, commentaire, commentaire_degat):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_degat)

    def AfficheSeDefendre(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheSermentHeimdall(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheOuroboros(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheMonstreEtatDeChoc(self, action):
        self.AffichageUneLignePuisUnEntreePourContinuer(f"L'ennemi tente d'utiliser le sort [{action}],"
                                                        " mais il n'a pas assez de mana ."
                                                        "\nSon réservoir de mana implose !"
                                                        "\nIl est en état de choc !")
        
    def AfficheEffetTerreur(self, liste_deffets):
        self.AffichageUneLignePuisUnEntreePourContinuer("L'ennemi lance un cri sinistre qui réveille en vous vos plus sombres terreurs !")
        print(liste_deffets[0])
        self.AffichageUneLignePuisUnEntreePourContinuer(liste_deffets[1])

    def AfficheEffetFausseTerreur(self, liste_deffets):
        self.AffichageUneLignePuisUnEntreePourContinuer("L'ennemi lance un cri terrifiant, mais vous y résistez !")
        self.AffichageUneLignePuisUnEntreePourContinuer(liste_deffets[0])

    def AfficheEffetDomovoi(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheEffetKikimora(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheActionDomovoi(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheActionKikimora(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
    
    def AfficheEffetSuperEtoile(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheCuisineInfernaleCreationCommande(self, commande, temps):
        print("Vous recevez une commande pour un des clients fantomatiques !")
        self.AffichageUneLignePuisUnEntreePourContinuer(f"Vous devez réaliser le plat [{commande}] pour le tour [{temps}] !")
        
    def AfficheCuisineInfernaleReussi(self, commande):
        self.AffichageUneLignePuisUnEntreePourContinuer("L'ennemi se rapproche de vous d'un ton menacant...")
        self.AffichageUneLignePuisUnEntreePourContinuer(f"...puis récupère le plat [{commande}] que vous avez préparé avant de partir le servir pendant 2 tours !")

    def AfficheCuisineInfernaleEchoue(self, commande, degats):
        self.AffichageUneLignePuisUnEntreePourContinuer("L'ennemi se rapproche de vous d'un ton menacant...")
        print(f"...avant de vous mettre un gigantesque upercut dans la machoire, furieux de ne pas trouver le plat [{commande}] !")
        self.AffichageUneLignePuisUnEntreePourContinuer(f"Vous perdez {degats} points de vie !\nEssayez de préparer votre plat dans le temps imparti la prochaine fois !")

    def AfficheDebutActionCuisineInfernale(self):
        print("       -{ Cuisiner [Action] }-\n")

    def AfficheActionCuisineInfernale(self, numero, action, cout):
        print(f" {numero} - [{action}] {cout}")

    def AfficheFinActionCuisineInfernale(self):
        choix = int(input("\nChoisissez avec les nombres (vous ne pouvez pas revenir en arrière) : "))
        return choix
    
    def AfficheCommentaireActionCuisineInfernale(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheDebutIngredientCuisineInfernale(self):
        print("       -{ Cuisiner [Ingredients] }-\n")

    def AfficheIngredientCuisineInfernale(self, numero, ingredient, quantite):
        print(f" {numero} - [{ingredient}] | {quantite} en stock |")

    def AfficheFinIngredientCuisineInfernale(self):
        choix = int(input("\nChoisissez avec les nombres (vous ne pouvez pas revenir en arrière) : "))
        return choix
    
    def AfficheCommentaireIngredientCuisineInfernale(self, ingredient):
        self.AffichageUneLignePuisUnEntreePourContinuer(f"...et l'utilisez avec l'ingredient [{ingredient}].")

    def AfficheDebutCuissonCuisineInfernale(self, ingredient):
        self.AffichageUneLignePuisUnEntreePourContinuer(f"...et rajoutez dedans l'ingredient [{ingredient}].")

    def AfficheMelangeCuisineInfernale(self, ingredient_un, ingredient_deux):
        self.AffichageUneLignePuisUnEntreePourContinuer(f"...et mélangez ensemble [{ingredient_un}] et [{ingredient_deux}].")

    def AfficheCuisineInfernalePlatCuisine(self, plat_cuisine):
        self.AffichageUneLignePuisUnEntreePourContinuer(f"Vous obtenez le plat [{plat_cuisine}] !")

    def AffichePerteTempsCuisineInfernale(self, commentaire):
        print("Vous perdez votre temps !")
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheDebutArretCuissonCuisineInfernale(self):
        print("       -{ Cuisiner [Arrêt de la Cuisson] }-\n")

    def AfficheArretCuissonCuisineInfernale(self, numero, ingredient, cuisson):
        print(f" {numero} - [{ingredient}] | Cuisson : {cuisson} |")

    def AfficheChoixArretCuissonCuisineInfernale(self):
        choix = int(input("\nChoisissez avec les nombres (vous ne pouvez pas revenir en arrière) : "))
        return choix
    
    def AfficheIngredientArretCuissonCuisineInfernale(self, ingredient):
        self.AffichageUneLignePuisUnEntreePourContinuer(f"...et arrêtez la cuisson de l'ingrédient [{ingredient}].")

    def AfficheCuisinePasAssezDeCuisineInfernale(self, raison):
        self.AffichageUneLignePuisUnEntreePourContinuer(f"Cepandant, vous n'avez pas assez de {raison}, et échouez a produire le plat.")

    def AfficheCommentaireIngredientCuisineAromatisationInfernale(self, ingredient):
        print(f"...et l'utilisez... sur l'ingrédient... [{ingredient}].")
        self.AffichageUneLignePuisUnEntreePourContinuer("Que Dieu aie pitié de vous comme vous n'avez pas eu pitié de cet ingrédient.")

    def AfficheSystemeSupport(self, commentaire, commentaire_soin):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_soin)

    def AfficheProtocoleSupernova(self, commentaire, commentaire_degat):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_degat)

    def AfficheLaserAntipersonnel(self, commentaire, commentaire_degat):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_degat)

    def AfficheFlashBang(self, commentaire, commentaire_degat):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire_degat)

    def AfficheGardienDeAme(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheGardienDeCorps(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheTank(self, degat):
        self.AffichageUneLignePuisUnEntreePourContinuer(f"Vous pointez du doigt l'ennemi en face de vous, et votre Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure tire un obus dévastateur qui lui inflige {degat} points de dégâts !")
        self.AffichageUneLignePuisUnEntreePourContinuer("Votre Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure se met alors en veille jusqu'au prochain combat.")

    def AfficheCanigou(self, commentaire):
        self.AffichageUneLignePuisUnEntreePourContinuer(commentaire)

    def AfficheEppeeDamocles(self):
        self.AffichageUneLignePuisUnEntreePourContinuer("Votre épée de Damocles finit par vous tomber sur la tête, se brisant a son contact !\nVous perdez l'artefact, ainsi que beaucoup de points de vie !")

    def AfficheMorceauEtherFragile(self):
        self.AffichageUneLignePuisUnEntreePourContinuer("Votre Morceau d'Ether Fragile finit par se briser, et vous perdez tout vos points de mana !")

    def AfficheEffetEauBenite(self):
        self.AffichageUneLignePuisUnEntreePourContinuer("Votre fiole d'eau bénite réagit avec votre mana !\nVous voila béni pendant un tour !")