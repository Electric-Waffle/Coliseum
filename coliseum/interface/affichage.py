"""Textes et écrans du jeu hors combat : introductions, descriptions d'étage, dialogues des villageois."""

import ast
import os
import random
import sys
import time

from coliseum import services
from coliseum.audio import PlayMusic, PlayMusicDeLetage, PlaySound, StopAllMusic
from coliseum.chemins import DOSSIER_RESSOURCES
from coliseum.console import ClearConsole
from coliseum.donnees.items import LISTEITEM, LISTEITEMDEFENCE
from coliseum.exploration.plan_etage import RegardeSiEtageCompletementObserve
from coliseum.joueur.bonus import (
    DonneSouvenirsDeTechniqueEtSorts,
    EnchantementAleatoire,
    PasseDeLivraisonABonus,
)
from coliseum.outils import GetRandomItemFromList


class Affiche:

    def __init__(self):
        pass

    def EntreePourContinuer(self):
        input("(Appuyez sur entrée pour continuer)")
        ClearConsole()

    def ParleAuPnjNuit(self):
        print("Vous vous approchez d'une personne et l'interpelez.")
        self.EntreePourContinuer()
        while True:
            while True:
                try:
                    print("*Bonsoir.*\n\n")
                    print("1 - Le Colysée...")
                    print("2 - Le village est bien calme.")
                    print("3 - Qu'est ce que je peux faire, la nuit ?")
                    print("4 - Ca commence a devenir sacrément cher, les améliorations !")
                    print("5 - Le dernier étage...")
                    print("6 - C'est quoi, un Tout-Premier ?\n")
                    print("7 - Au revoir\n")
                    choix = int(input("Faites votre choix avec les nombres : "))
                    ClearConsole()
                    if choix in range(1,8):
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print("Toi aussi tu veux voir les combats qui se déroulent la nuit, hein ?")
                services.Affichage.EntreePourContinuer()
                print("Eh bien, désolé de devoir calmer ta joie, mais ca n'est pas aussi simple.")
                services.Affichage.EntreePourContinuer()
                print("Depuis que ce gang de..de punk..a prit controle de la batisse, il faut respecter leurs règles.\nTout est devenu compliqué.")
                services.Affichage.EntreePourContinuer()
                print("Lorsque tu regarde les combats , tu te rendra vite compte qu'ils sont différents, a une chose près : leur talent.")
                services.Affichage.EntreePourContinuer()
                print("Les techniques utilisées sont variées, certe, mais elles sont du même niveau.\nLe gang fait ca pour que tu aie l'impression qu'il y a toujours quelque chose de neuf qui se passe, j'imagine.")
                services.Affichage.EntreePourContinuer()
                print("Et quand tu a vu toute les techniques d'un même niveau ?\nTu te retrouve bloqué a l'exterieur, a devoir payer quelques rares materiaux pour augmenter ton *grade*, afin de voir des matchs d'une plus grande intensité.")
                services.Affichage.EntreePourContinuer()
                print("En clair, tu ne peut pas voir les matchs du troisieme grade si tu n'a pas vu tout les matchs du premier et deuxieme grade.\nTu vois ou je veux en venir ?")
                services.Affichage.EntreePourContinuer()
                print("Si tu veux regarder les matchs du colysée la nuit, il faut que tu regarde tout les matchs disponible la journée.\nTu pourra alors augmenter ton grade afin de voir les matchs de haut niveaux qui se déroulent maintenant.")
                services.Affichage.EntreePourContinuer()
                print("C'est cher, oui, mais si tu a réussi a arriver ici, c'est que tu dois etre assez riche en materiau pour te le permettre !\nOu peut etre fait tu partie de ces sans-abris qui jonchent les rues piétonnes et les bancs du quartier commercial, ayant vendu toute tes ressources pour arriver a voir la Nuit ?")
                services.Affichage.EntreePourContinuer()
            elif choix == 2:
                print("Effectivement.\nLe prix d'une nuit dans un hotel ou une maison est si cher, il agit comme une barrière naturelle qui empeche tout le monde de venir ici.")
                services.Affichage.EntreePourContinuer()
                print("Mais ne pense pas un seul instant être dans le monde des riche : certains donnent tout ce qu'ils ont pour pouvoir voir ce ciel étoilé.\nIl y a même un business qui emmene certaines personnes passer quelques années ici, puis les ramènent de force dans le Jour !")
                services.Affichage.EntreePourContinuer()
                print("Faire l'experience du calme et de la tranquilité avant d'être abruptement ramené devant le soleil implacable, ca en brise certains.")
                services.Affichage.EntreePourContinuer()
            elif choix == 3:
                print("Eh bien, il y a d'abord le Colysée au Nord, qui propose des combats bien plus avancés ou se produisent des aventuriers extremement puissants.")
                services.Affichage.EntreePourContinuer()
                print("Au Sud, tu peut entrer dans la Banque qui y possède une succursale, pour échanger des materiaux ou augmenter ton matos.\nSi tu a de la chance, tu pourra peut etre même voir la Shamane dans le Temple a l'extreme Sud.\nOn dit que c'est une Tout-Première, alors ne te la met pas a dos !")
                services.Affichage.EntreePourContinuer()
                print("A l'Ouest, il n'y a rien d'interressant.\nQuoique...le Fabricateur n'est pas présent dans cette version des Champs du Crépuscule.\nC'est quelque chose , non ?")
                services.Affichage.EntreePourContinuer()
                print("A l'est, l'Hotel est la seule batisse ouverte.\nTu peux aller y passer la nuit, ou commander un verre et écouter les gens parler.")
                services.Affichage.EntreePourContinuer()
                print("Mon petit doigt me dit que les rumeurs la nuit doivent être bien plus excitantes que celles prononcées la journée...")
                services.Affichage.EntreePourContinuer()
            elif choix == 4 :
                print("Les améliorations ?")
                services.Affichage.EntreePourContinuer()
                print("Les améliorations...")
                services.Affichage.EntreePourContinuer()
                print("Les améliorations !")
                services.Affichage.EntreePourContinuer()
                print("Tu fais partie de ces gens qui fondent leurs espoirs sur les aventuriers qui arrivent ?")
                services.Affichage.EntreePourContinuer()
                print("Je trouve ca un peu bête, surtout qu'au final, tu perd tes ressources si ils ne dépassent pas le 3eme étage.\nMoi par exemple, j'ai fondé ma fortune sur le business des prêts en materiaux.")
                services.Affichage.EntreePourContinuer()
                print("Ca , ca a de l'avenir !")
                services.Affichage.EntreePourContinuer()
                print("Maintenant que j'y pense, qu dernier gala de charité du Directeur de la Banque, il y avait un objet proposé qui pourrait être interressant pour les gens comme vous...")
                services.Affichage.EntreePourContinuer()
                print("C'était une amulette, et une espece de pièce en or massif...qui permettait d'augmenter la chance de récuperer des materiaux sur les monstres ?\nPersonne ne l'a acheté, donc ca devrait toujours etre en vente au service objet de la banque.")
                services.Affichage.EntreePourContinuer()
                print("Hum? On vous refuse l'entrée ?")
                services.Affichage.EntreePourContinuer()
                print("C'est normal, il faut un espece de pass vip pour en bénéficier.\nSuffit de faire une faveur au Directeur, et le tour est joué !")
                services.Affichage.EntreePourContinuer()
                print("Je crois qu'il passe ses journée dans le jardin de son manoir, dans le quartier résidentiel, le jour.")
                services.Affichage.EntreePourContinuer()
                print("Le pauvre bougre profiterait bien d'un animal de companie, ou même d'une bête.\nPeut importe son apparence, il arriverait meme a dresser une immondicitée abobinable sur lesquels les dieux eux mêmes auraient experimentés !")
                services.Affichage.EntreePourContinuer()
                print("...")
                services.Affichage.EntreePourContinuer()
                print("...je sais pas pourquoi j'ai dit ca...")
                services.Affichage.EntreePourContinuer()
            elif choix == 5:
                print("Personne n'a battu le Coliseum, donc je ne pourrait pas te dire si il existe !\nPar contre il existe une théorie surprenante sur son existance.")
                services.Affichage.EntreePourContinuer()
                print("Dans le Coliseum, on ne peut voir que 8 boss, sans compter les variations du Chevalier Pourpre et du Roi Déchu.")
                services.Affichage.EntreePourContinuer()
                print("Sachant que les boss et les étages eux même changent entre les assauts, un aventurier devrait pouvoir tomber sur n'importe quel boss a chaque fois qu'il entre dans ce donjon maudit.")
                services.Affichage.EntreePourContinuer()
                print("Donc si il n'y a que 8 boss dans le roulement des boss possibles, il devrait n'y avoir que 7 étages, n'est ce pas ?")
                services.Affichage.EntreePourContinuer()
                print("Mais d'après le Cartographe, l'algorithme qu'il a créé pour fabriquer ses cartes est théoriquement valable pour 11 étages !")
                services.Affichage.EntreePourContinuer()
                print("Alors, 8 ou 11 ?")
                services.Affichage.EntreePourContinuer()
                print("Je vous laisserait a vos réflexions sur ce petit bout de trivia connu seulement par des gens exceptionnels :")
                services.Affichage.EntreePourContinuer()
                print("Les fresques que l'on trouve assez rarement montrent assez souvent une batisse divine qui correspond assez bien au panthéon divin, la divine maison abritant toute les divinités que l'humanitée a un jour priée.\nLes écrits parlent de centaines de milions d'étages contenus dans la petite ile flottante.")
                services.Affichage.EntreePourContinuer()
                print("Et devinez ce que le cartographe a trouvé dans son algorithme ?")
                services.Affichage.EntreePourContinuer()
                print("Des milions de petites variables, inutilisées dans le modèle actuel du Coliseum.")
                services.Affichage.EntreePourContinuer()
                print("Alors laissez moi vous poser la question :")
                services.Affichage.EntreePourContinuer()
                print("Qu'est ce véritablement que le dernier étage ?")
                services.Affichage.EntreePourContinuer()
                print("Si cette réflexion vous interesse, alors trouvez un moyen d'explorer la batisse de fond en comble.")
                services.Affichage.EntreePourContinuer()
            elif choix == 6:
                print("C'est simplement le nom que l'on donne aux tout-premiers aventurier arrivés aux Champs du Crépuscule.")
                services.Affichage.EntreePourContinuer()
                print("Bien sur, au début, ils n'étaient pas des aventuriers mais simplement le peuple qui avait été enfermé ici par le Roi Déchu.")
                services.Affichage.EntreePourContinuer()
                print("Mais ca n'a plus beaucoup d'importance ici, pas vrai ?")
                services.Affichage.EntreePourContinuer()
                print("Après avoir vécu autant de temps ici, ils sont devenus, fous, aigris, ou plein d'une sagesse insondable qui n'est accessibles qu'à celles et ceux qui seraient assez compétent pour recevoir et décrypter cette sagesse.")
                services.Affichage.EntreePourContinuer()
                print("Et pour ceux qui ne sont pas ici ?")
                services.Affichage.EntreePourContinuer()
                print("Tu les trouvera dans les champs alentours, aussi vivants que des zombies, a chercher une mort de l'égo qui ne viendra jamais.")
                services.Affichage.EntreePourContinuer()
                print("Pour l'instant, j'en connais deux : la chamane du temple au Sud, et...")
                services.Affichage.EntreePourContinuer()
                print("...")
                services.Affichage.EntreePourContinuer()
                print("Non.\nCa ne me reviens pas.")
                services.Affichage.EntreePourContinuer()
            elif choix == 7:
                print("Bonne soirée !")
                self.EntreePourContinuer()
                break


    def ParleAuPnj(self):
        print("Vous vous approchez d'une personne et l'interpelez.")
        self.EntreePourContinuer()
        while True:
            while True:
                try:
                    print("*Hey ! Qu'est ce que je peux faire pour toi l'ami ?*\n\n")
                    print("1 - On est ou ?")
                    print("2 - Comment je suis arrivé là ?")
                    print("3 - Qu'est ce que je peux faire ?")
                    print("4 - Un type bizarre a créé la nuit ?")
                    print("5 - Le quatrième étage...")
                    print("6 - Au revoir\n")
                    choix = int(input("Faites votre choix avec les nombres : "))
                    ClearConsole()
                    if choix in range(1,7):
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                print("Ici ? C'est les champs du crépuscule.\nPlus précisément, tu es au centre du village, sur la stèle du renouveau.")
                self.EntreePourContinuer()
                print("C'est l'endroit ou presque toute les personnes qui ont péri dans le Coliseum se retrouvent.")
                self.EntreePourContinuer()
                print("Enfaite, on lui a donné ce nom car un mage a trouvé que cet endroit était similaire a un autre, illustré dans ses bouquins de magie.\nQuelque chose a propos d'un domaine ou habitait les dieux du Nirvana, ou qui s'en rapproche.\nEt puis le Village, c'est parce que personne n'a trouvé de meilleur nom !")
                self.EntreePourContinuer()
                print("Et puis la stèle du renouveau, c'est parce que..eh bien..c'est la que nous revenons a la vie ?\nMétaphoriquement parlant, bien sur.")
                self.EntreePourContinuer()
                print("Mais j'y pense, si tu me pose cette question, c'est que tu dois être nouveau !\nSurtout ne panique pas, et demande moi autre chose si tu veut !")
                self.EntreePourContinuer()
            elif choix == 2:
                print("Tu ne t'ai jamais demandé pourquoi personne n'était jamais revenu du Coliseum ?\nJe veux dire, tu as terminé le premier étage et battu le clone d'obsidienne, son boss.\nSon boss qui était présent quand tu es arrivé.\nCa voudrait dire quoi ?\nQue personne n'a jamais battu le premier étage ? Que le clone d'obsidienne a été le bourreau de toute les personnes qui sont entrée, sauf toi et toi seulement ?")
                self.EntreePourContinuer()
                print("La véritée est tout autre.")
                self.EntreePourContinuer()
                print("Pareil a un organisme vivant, le Coliseum assimile tout ce qui rentre a l'interieur.\nEnsuite, après la mort des corps étrangers, il se passe un triage.")
                self.EntreePourContinuer()
                print("Si tu n'es pas assez fort, tu te fait digerer. Ton énergie vitale et ton mana servira au bon fonctionnement de la structure.")
                print("Si tu a dépassé un certain point, alors tu es digéré jusqu'à un certain point. Tes compétences, charactéristiques, et meme ton corps n'existe plus, mais ton ame survie et est amenée ici.")
                print("Et si tu es assez fort, alors tu deviens un des acteurs principaux du Coliseum : Un boss.")
                self.EntreePourContinuer()
                print("Seulement, pour que le système marche, il faut que les acteurs soient, d'une certaine manière, immortels. Si ils mourraient au bout d'une seule représentation, ca serait pas rentable.")
                self.EntreePourContinuer()
                print("Ainsi donc, la même énergie qui est absorbée du corps des challengers...")
                print("...sert a invoquer des monstres, garder l'intégritée de l'étage, et ranimer les boss !")
                self.EntreePourContinuer()
                print("La seule chose qu'on a toujours pas réussi a comprendre, c'est pourquoi on nous laisse quand meme sous forme d'âme, si on ne peut plus contribuer a l'entropie du système...")
                self.EntreePourContinuer()
            elif choix == 3:
                print("Eh bien, un peu tout ce que tu veux !")
                self.EntreePourContinuer()
                print("Tu es une ame maintenant, tu as tout le temps du monde.")
                print("Mais en gros, voila les activités principales du Village :")
                self.EntreePourContinuer()
                print("A l'Ouest, c'est la déchetterie. C'est un des endroits les plus importants.")
                self.EntreePourContinuer()
                print("Tout ce que tu possédait sur toi, matériaux, artefacts, golds; ne peuvent pas étre completement absorbé par le Coliseum.")
                print("Et c'est la que tu peut retrouver ton équipement sous forme de materiau.")
                print("Va donc y faire un tour, parce que tout ici se paye en materiau. On ne peut rien changer a l'endroit lui meme, étant des ames immaterielles.\nCepandant, pour une raison obscure, on peut utiliser les materiaux pour faire maison et autre, même si on en a plus vraiment besoin.")
                self.EntreePourContinuer()
                print("Ya aussi un fabricateur la bas, afin de combiner les materiaux entre eux, mais si on met pas les bons materiaux ils sont détruit.\nPersonne ne se souvient des recettes possibles, donc c'est devenu plutot inutile.")
                self.EntreePourContinuer()
                print("Au Nord, c'est le Coliseum.")
                self.EntreePourContinuer()
                print("Tu sais, quand tu te bat, tu peut voir des figures fantomatiques dans les gradins ?\nBah c'est nous.\nD'une certaine manière, on peut accéder au coliseum par la réplique de colisée au Nord, et ainsi assister aux combats.")
                print("Seul problème, un groupe en a prit le controle, et maintenant on doit payer avec des materiaux si on veut assister aux matchs.\nC'est litteralement notre seule source de divertissement, alors on paye et puis c'est tout.")
                self.EntreePourContinuer()
                print("Au Sud, c'est la partie commerciale.")
                self.EntreePourContinuer()
                print("Tu pourrais penser, au vu du nom, que c'est un endroit ou tu peut acheter des choses pour toi, mais enfaite c'est tout le contraire.")
                self.EntreePourContinuer()
                print("Tu peut payer des materiaux pour acheter ou construire des choses qui se retrouveront a l'étage 1 pour les futurs challengers.\nD'une certaine manière, tu les sponsorise !")
                self.EntreePourContinuer()
                print("Comment ils font ca ?\nCertains parlent d'une grande figure habillée avec des habits de majordome, mais on sait pas vraiment.\nPourquoi ils font ca ?\nL'ennui peut etre, qu'en sais-je.")
                self.EntreePourContinuer()
                print("A l'Est, c'est le quartier résidentiel.")
                self.EntreePourContinuer()
                print("Tu peut y trouver des maisons style bidonville dans lesquelles seul les plus riches peuvent être, quelques gens importants, et même un hotel.")
                print("Pourquoi des fantomes qui n'ont plus besoin de dormir voudraient payer des materiaux pour dormir dans une chambre d'hotel ?\nEh bien c'est là que ca devient interessant.")
                self.EntreePourContinuer()
                print("Je te la fait courte : Si tu dors dans un lit, dans une maison, tu te fait téléporter dans le même endroit, mais la nuit.")
                self.EntreePourContinuer()
                print("Apparemment, c'est un type bizarre qui a fait ca pour encourager les gens a continuer de vivre normalement : boire manger dormir, même si ca a pas de sens pour un fantome.")
                print("Et la nuit, les marchandises se font plus rares et précieuses, tandis que les combats se font plus intenses !")
                self.EntreePourContinuer()
                print("Enfin, si d'ici quelques millions d'années la folie finit par te prendre, dans cet endroit sans substance ou le soleil ne se couche jamais...")
                self.EntreePourContinuer()
                print("Tu peut toujours aller errer dans les champs en bordure de ville, en esperant un jour perdre la boule .")
                self.EntreePourContinuer()
                print("C'est ce qui se rapproche le plus de la mort, après tout.")
                self.EntreePourContinuer()
            elif choix == 4 :
                print("Je connais pas trop les détails, va donc écouter un peu les rumeurs des gens au saloon : ils s'y connaissent mieux que moi !")
                print("Après c'est pas grand chose pour toi, la nuit. \nMais a force de voir toujours les memes personnes, les memes endroits, la meme chaleur, et le meme soleil pendant des centaines d'années...")
                self.EntreePourContinuer()
                print("Voir la nuit, c'est un changement très apprécié. Bien plus que ca : c'est de l'espoir.")
                self.EntreePourContinuer()
            elif choix == 5:
                print("Il n'y avait pas de clé au quatrième étage ?")
                self.EntreePourContinuer()
                print("Hum...")
                self.EntreePourContinuer()
                print("C'est vrai que ca fait tellement longtemps que quelqu'un n'est pas venu du quatrième étage... j'ai presque oublié qu'il existe !")
                print("En tout cas, si il y a bien une personne qui peut t'aider pour ce truc bizarre, c'est bien la folle du quartier résidentiel ! Elle vit dans la tour tordue avec pleins de cristaux a l'interieur !")
                print("Et meme si elle n'y est pas, elle devrait avoir laissé un truc interconnecté à elle, pour pouvoir la retrouver !\nElle parlait tout le temps de trucs hol.. hillos..hollistique ?\nUn sacré phénomène !")
                self.EntreePourContinuer()
                print("Après, ca devrait pas avoir beaucoup d'interet pour toi...\nTu veut sponsoriser quelqu'un ?")
                self.EntreePourContinuer()
            elif choix == 6:
                print("A plus !")
                self.EntreePourContinuer()
                break

    def ParlerAvecLeDirecteur(self):
        liste_de_tags =  services.Sove.ModifieTagsDansSove("Donne",None)
        liste_des_artefacts_debloque = services.Sove.ModifieArtefactDansSove("Donne",None)
        if not "Carte VIP" in liste_de_tags and "Ecaille de la Bête" in liste_des_artefacts_debloque:
            print("Alors que vous vous approchez du jardin du banquier, vous apercevez la Bete que vous avez libéré entrain de s'approcher doucement du Directeur.")
            services.Affichage.EntreePourContinuer()
            print("Vous commencez a courir dans sa direction, afin de le prévenir de l'arrivée imminente de la chose, mais c'est trop tard : La Bete se jette sur le pauvre homme...")
            services.Affichage.EntreePourContinuer()
            print("...et lèche son visage, alors que l'homme rigole.")
            services.Affichage.EntreePourContinuer()
            print("La Bête vous regarde, tourne la tête, et s'approche de vous en trotinant.")
            services.Affichage.EntreePourContinuer()
            print("*Hey l'ami !*")
            services.Affichage.EntreePourContinuer()
            print("L'Homme s'approche de vous et vous tend la main.")
            services.Affichage.EntreePourContinuer()
            print("*J'ai vu via le Coliseum que c'est toi qui a récupéré la carte afin de libérer mon ami, et que tu a meme battu le boss pour qu'il puisse s'échapper !*")
            services.Affichage.EntreePourContinuer()
            print("Vous serrez la main fantomatique du directeur, alors que la Bete se frotte a vos jambes.")
            services.Affichage.EntreePourContinuer()
            print("*Tu vois, tout ce temps, je m'étais fait a ma fortune, mais je n'avais personne avec qui partager la richesse d'une simple accolade.*")
            print("*Alors quand Neil est arrivé ici, et que tout le monde le fuyait...*")
            services.Affichage.EntreePourContinuer()
            print("*...je lui ai donné sa chance.*")
            services.Affichage.EntreePourContinuer()
            print("*Et maintenant regarde ! Il est aussi inofensif qu'une bébé chiot, et j'ai enfin une raison de me balader dans mon grand jardin !*")
            services.Affichage.EntreePourContinuer()
            print("*Je voulais te remercier d'une manière ou d'une autre d'avoir libéré Neil, alors voici : une carte VIP que tu peut utiliser dans ma banque pour acheter nos items exclusifs !*")
            services.Affichage.EntreePourContinuer()
            print("Le Directeur vous tend une carte dorée.\nVous obtenez la Carte VIP ! Vous pouvez maintenant acheter et upgrader les objets exclusifs de la Banque !")
            services.Sove.ModifieTagsDansSove("Ajout","Carte VIP")
            services.Affichage.EntreePourContinuer()
            print("*Comme pour les autres marchand, l'aventurier que tu sponsorisera avec ces items devrait pouvoir les trouver directement au premier étage du Coliseum.*")
            services.Affichage.EntreePourContinuer()
            print("*Passe nous rendre visite quand tu le souhaite !*")
            services.Affichage.EntreePourContinuer()
        elif "Carte VIP" in liste_de_tags:
            while True:
                while True:
                    try:
                        print("Neil et le Directeur jouent gaiement dans le jardin de la demeure.\n\n")
                        print("1 - Parler au Directeur")
                        print("2 - Caresser Neil")
                        print("3 - Jouer avec eux")
                        print("4 - Dire au revoir\n")
                        choix = int(input("\nFaites votre choix avec les nombres : "))
                        ClearConsole()
                        if choix in range(1, 5):
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 4 :
                    print("Vous saluez les deux personnages et sortez du Jardin.")
                    services.Affichage.EntreePourContinuer()
                    break
                elif choix == 1:
                    print("*L'un des avantages d'être aussi riche ici, c'est qu'on peut litteralement tout construire avec sa richesse.*")
                    print("*Chaque materiau a son utilité !*")
                    services.Affichage.EntreePourContinuer()
                    print("*Par exemple, tu vois quand je suis arrivé ? Les essences dorées ne servaient pas a grand chose.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Ce n'était qu'une ressource supplementaire qui venait encombrer la décharge, vu que chaque aventuriers mourraient avec au minimum 100 golds.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Eh bien moi, ces essences, j'ai passé un bon nombre d'année a les toucher, a les casser, a les modifier.*")
                    print("*A force, j'ai trouvé un moyen d'en faire une sorte de colle qui peut faire tenir les materiaux ensembles ! Voila pourquoi toute les maisons brillent ! Leurs joints sont litérallement fait d'or !*")
                    services.Affichage.EntreePourContinuer()
                    print("*Et d'après mon experience, je suis sûr qu'on pourrait faire marcher le fabricateur et combiner cette colle avec un éclat de cloche pour en faire une petite cloche...*")
                    services.Affichage.EntreePourContinuer()
                    print("*Pourquoi je ne le fais pas ? Ca ne m'interesse pas de sponsoriser. Je suis très bien comme je suis actuellement !*")
                    services.Affichage.EntreePourContinuer()
                elif choix == 2:
                    print("Vous approchez une main hésitante de la carapace chitineuse de Neil, et elle se met a vibrer.")
                    services.Affichage.EntreePourContinuer()
                    print("Votre main s'enfonce alors dans une texture semblable a un nuage de coton, et Neil ferme ses yeux.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous vous laissez prendre au jeu, et ne retirez votre main qu'après quelques minutes aussi étranges que raffraichissantes.")
                    services.Affichage.EntreePourContinuer()
                    print("Neil semble avoir apprécié l'experience !")
                    services.Affichage.EntreePourContinuer()
                    liste_de_tags =  services.Sove.ModifieTagsDansSove("Donne",None)
                    if not "Neil" in liste_de_tags:
                        print("Neil vous regarde dans les yeux avec insistance !")
                        services.Affichage.EntreePourContinuer()
                        print("Vous plongez votre regard dans le sien et voyez des formes étranges,")
                        services.Affichage.EntreePourContinuer()
                        print("Des couleurs incroyables, des mots incompréhensibles,")
                        services.Affichage.EntreePourContinuer()
                        print("Des notions ésot-[SYSTEME INTRUSION EN COURS]")
                        services.Affichage.EntreePourContinuer()
                        print("[TENTATIVE DE REJET D'INTRUSION ECHOUEE]")
                        services.Affichage.EntreePourContinuer()
                        print("[REECRITURE URE URE CODDDDDDEEE]")
                        services.Affichage.EntreePourContinuer()
                        print("[MESSAGE ADMINTILISATEURINCONNU ERREUR MESSAGE]")
                        print("Vous avez débloqué [Neil] en tant que personnage jouable !")
                        services.Sove.ModifieTagsDansSove("Ajout","Neil")
                        print("[FIN MESSAGE ADMINTILISATEURINCONNU ERREUR FIN MESSAGE]")
                        services.Affichage.EntreePourContinuer()
                        print("[SYSTEME : AUCUNE INTRUSION DETECTEE]")
                        services.Affichage.EntreePourContinuer()
                        print("Neil vous lance un sourire mystérieux, et retourne jouer avec son nouvel ami.")
                        services.Affichage.EntreePourContinuer()

                elif choix == 3:
                    print("Vous prenez un frisbee et le jettez dans les airs.")
                    services.Affichage.EntreePourContinuer()
                    print("Le Directeur et Neil se battent pour essayer de l'avoir en premier...")
                    services.Affichage.EntreePourContinuer()
                    numero_aleatoire = random.randint(0,100)
                    if numero_aleatoire < 50:
                        print("...et c'est le Directeur qui le prend dans ses mains !")
                    else:
                        print("...et c'est Neil qui l'attrape dans sa bouche !")
                    services.Affichage.EntreePourContinuer()
                    print("Vous riez aux éclats !")
                    services.Affichage.EntreePourContinuer()
        else:
            print("Vous vous approchez du jardin d'une grande demeure")
            services.Affichage.EntreePourContinuer()
            while True:
                while True:
                    try:
                        print("Un homme est assis devant une partie d'échec.\n\n")
                        print("1 - Parler a l'homme")
                        print("2 - Jouer contre l'homme")
                        print("3 - Repartir")
                        choix = int(input("\nFaites votre choix avec les nombres : "))
                        ClearConsole()
                        if choix in range(1, 4):
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 3 :
                    print("Vous saluez l'homme et sortez du Jardin.")
                    services.Affichage.EntreePourContinuer()
                    break
                elif choix == 1:
                    print("*J'imagine que les gens de cette génération ne connaissent pas les règles d'usage ?*")
                    services.Affichage.EntreePourContinuer()
                    print("*Je suis le Directeur. Je possède la Banque dans le quartier commercial.*")
                    services.Affichage.EntreePourContinuer()
                    print("Le Directeur lève les yeux de sa partie et vous regarde.")
                    services.Affichage.EntreePourContinuer()
                    print("*Ce n'est pas suffisant ? Je suis un homme riche, et seul. L'un de ces deux faits est vrai par choix, et l'autre, par obligation.*")
                    services.Affichage.EntreePourContinuer()
                    print("Le Directeur redirige son regard sur sa partie.")
                    services.Affichage.EntreePourContinuer()
                    print("*Et maintenant , ayez l'obligation de sortir de chez moi.*")
                    services.Affichage.EntreePourContinuer()
                elif choix == 2:
                    print("*Je n'ai pas besoin de compagnie, encore moins de la votre.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Si vous voulez faire quelque chose, trouvez moi plutot un animal de companie, car je préfère leur présence a la votre.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Même une bête ferait l'affaire !*")
                    services.Affichage.EntreePourContinuer()


    def ShowDeath(self, game_is_over=False):
        if not game_is_over and services.Player.numero_de_letage < 5:
            StopAllMusic()
            print("[AVENTURE TERMINE]")
            services.Affichage.EntreePourContinuer()
            print("[CALCUL DE LA CONTRIBUTION DU PERSONNAGE EN COURS...]")
            services.Affichage.AfficheAvecUnTempsDattente(3)
            print("[CALCUL TERMINE]")
            services.Affichage.EntreePourContinuer()
            print("[CONTRIBUTION DU PERSONNAGE INSUFFISANTE]")
            services.Affichage.EntreePourContinuer()
            print("[REALISATION DU DESIR REFUSEE]")
            services.Affichage.EntreePourContinuer()
            print("[MORT VALIDEE]")
            services.Affichage.EntreePourContinuer()
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
        if services.Player.numero_de_letage >= 4 and not game_is_over:
            services.Player.player_tags.append("Fantome")
        else:
            sys.exit()

    def AfficheGacha(self, recompense):
        PlaySound("gacha")
        print("Le mutagène se révèle...")
        services.Affichage.AfficheAvecUnTempsDattente(1.7)
        print("Le mutagène se révèle être...")
        services.Affichage.AfficheAvecUnTempsDattente(1.7)
        print("Le mutagène se révèle être un...")
        services.Affichage.AfficheAvecUnTempsDattente(1.5)
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
        if services.Player.stigma_positif == "Débrouillarde":
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
                services.Player.items_possedes[nom_de_litem] += 1
            else:
                print("...mais aucune idée ne vous vient a l'esprit.")
            self.EntreePourContinuer()
        if services.Player.stigma_positif == "Cueilleuse":
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
                services.Player.items_possedes[nom_de_litem] += 1
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
        if not services.Player.boss_battu:
            print("A part le boss.")
        if not services.Player.red_coin_recu_par_extermination and services.Player.boss_battu:
            print(
                "Un spectateur fantomatique amusé par votre désir d'extermination vous envoie un cadeau depuis les gradins, avant de disparaitre."
            )
            self.EntreePourContinuer()
            print("Vous gagnez un Red Coin !")
            services.Player.nombre_de_red_coin += 1
            services.Player.red_coin_recu_par_extermination = True
        self.EntreePourContinuer()

    def AfficheIntroCombatBoss(self):
        if services.Player.nom_de_letage == "Limbes Flétrissants":
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
            if ("Regard de la Bête" in services.Player.liste_dartefacts_optionels and (not "Âme de la Bête" in services.Player.liste_dartefacts_optionels) 
            and (not "Âme de la Bête" in services.Player.liste_dartefacts_optionels)) : 
                print("La grille s'ouvre.\nLe Maitre des lieux... s'effondre ?")
                self.EntreePourContinuer()
                print("Vous pouvez voir le boss, haletant, devant le cadavre de la bête que vous avez libéré de sa capsule, un peu plus tôt.")
                self.EntreePourContinuer()
                print("Vous vous approchez de la chose par terre, et Zeroual s'empresse d'absorber son âme.")
                self.EntreePourContinuer()
                print("Vous obtenez l'artefact [Âme de la Bête] !")
                print("Un reste de quelque chose que vous ne pouvez pas décrire.\nVous gagnez 5 points de force !")
                self.EntreePourContinuer()
                services.FloorMaker.GiveRandomArtefact("Âme de la Bête","Don")
                services.Player.points_de_force += 5
                services.Player.nombre_de_monstres_tues += 1
                print("Le boss finit de reprendre son souffle, et commence son speech, malgrès ses blessures.")
                self.EntreePourContinuer()
                services.Player.player_tags.append("Boss Blessé")
            else:
                print("La grille s'ouvre.\nLe Maitre des lieux s'approche.")
                self.EntreePourContinuer()
        if (services.Player.numero_de_letage != 8) and (services.Player.nom_de_letage not in ["Jungle Cruelle"]):
            PlayMusic("boss_introV2")
        liste_commentaire = []
        if services.Player.numero_de_letage == 1:
            commentaire = "Une boule d'obsidienne flotte jusqu'à votre niveau, et une voix artificielle remplit l'arène."
            liste_commentaire.append(commentaire)
            commentaire = (
                "*SENTIENCE RECONNUE. INITIATION DU PROTOCOLE D'EXPLIQUATION ENCLENCHE*"
                "\n*POUR LES CRIMES SUIVANT CONTRE VOTRE ROI MALGRES SES ANNEES DE BONS ET LOYAUX SERVICES, VOUS VOILA CONDAMNE A LA PEINE DE MORT :*"
                "\n*TENTATIVE DE TRAHISON, TENTATIVE DE REGICIDE, TENTATIVE DE REBELLION, TENTATIVE DE REVOLUTION,*"
                "\n*AVOIR CRACHE SUR UN TABLEAU DU ROI, AVOIR EXPRIME DE LA DISSATISFACTION ENVERS LE ROI ACTUEL,*"
                "\n*AVOIR UN COMPORTEMENT SUSPECT PROCHE DE LA RESIDENCE DU ROI, AVOIR UN COMPORTEMENT SUSPECT PROCHE DE LA CAPITALE DU ROI,*"
                "\n*AVOIR UN COMPORTEMENT SUSPECT DANS LE ROYAUME DIRIGE PAR LE ROI, ET ENCORE 2324 AUTRES INFRACTIONS NON CITEE.*"
            )
            liste_commentaire.append(commentaire)
            commentaire = (
                "*QUESTIONS SOUVENT POSEES :*"
                "\n* - MAIS JE N'AI JAMAIS FAIT CELA !*"
                "\n* - CELA DOIT ETRE UNE ERREUR !*"
                "\n* - COMMENT PEUT ON SORTIR D'ICI ?*"
                "\n*UNE SEULE REPONSE : UN ROI JUSTE NE PUNIT PAS LES INNOCENTS.*"
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
        elif services.Player.numero_de_letage == 0:
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
        elif services.Player.numero_de_letage == 9:
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
        elif services.Player.numero_de_letage == 2:
            if services.Player.nom_de_letage == "Jungle Cruelle":
                StopAllMusic()
                commentaire = ("L'armure vide se rapproche de vous, et se met en position de combat.")
                liste_commentaire.append(commentaire)
                commentaire = ("Vous jettez un coup d'oeil au tentacule accroché a l'ennemi,"
                               " et vous rendez compte qu'elle n'est pas seulement accrochée, mais fusionnée avec l'armure et son précédent occupant...")
                liste_commentaire.append(commentaire)
                if "Lame Spectrale" in services.Player.liste_dartefacts_optionels:
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
                    commentaire = ("        ...Coquille...")
                    liste_commentaire.append(commentaire)
                    commentaire = ("                 ...vide.")
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
                    f"\n*Toi par exemple, tu a du sang de monstre sur les mains.*\n*Je dirais que tu a massacré...{services.Player.nombre_de_monstres_tues} monstres.*"
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
        elif services.Player.numero_de_letage == 3:
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
                "\n*Le roi, dans sa folie, s'est emparé des cadavres de ses soi-disants ennemis qu'il a cousut entre eux. Puis, il a mit l'âme de son frère a l'interieur.*"
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
        elif services.Player.numero_de_letage == 4:
            commentaire = (
                "Vous entendez le son d'un livre qui se ferme fort, et l'apparence de l'arène change brusquement. "
                "\nVous observez alors un bureau finement décoré et rempli d'étagères sur lesquelles sont négligement placés des livres de magie et de sortillèges."
                "\nAu milieu, une adolescente d'une quinzaine d'année vous regarde fixement, coincée entre deux piles de livre plus haute qu'elle."
            )
            liste_commentaire.append(commentaire)
            commentaire = "*C'est l'heure pas vrai ?*\n*Bon, ben me fout pas la honte hein !*\n*Ya un endroit qu'il faut pas taper, c'est là.*"
            liste_commentaire.append(commentaire)
            commentaire = (
                "L'ennemie tapote son torse, ou repose une amulette a l'aspect ancien."
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
        elif services.Player.numero_de_letage == 5:
            if services.Player.nom_de_letage == "Le Lumisade":
                StopAllMusic()
                services.Affichage.IntroBoss("Un battement de cil plus tard, vous vous retrouvez à l'entrée de l'hotel.")
                services.Affichage.IntroBoss("L'arène devant vous étant vide, vous vous tournez vers la salle de bal, depuis laquelle vous entendez une musique familière, la même qu'à votre arrivée à cet étage.")
                services.Affichage.IntroBoss("Vous tendez une main hésitante sur la poignée de la porte...")
                services.Affichage.IntroBoss("...les marques de brulures sont désormais omniprésentes.")
                services.Affichage.IntroBoss("Un feu invisible, qui grignotte silencieusement le bois et le tissu.")
                services.Affichage.IntroBoss("L'hotel brule.")
                PlayMusic("boss_5_alt_intro")
                commentaire = "*Cela fait toujours bizarre.*"
                liste_commentaire.append(commentaire)
                commentaire = "La salle de bal est splendide, équipée de somptueuses tables de banquet."
                liste_commentaire.append(commentaire)
                commentaire = "*De se rapeller.*\n*Ou peut-être n'ai-je jamais oublié ?*"
                liste_commentaire.append(commentaire)
                commentaire = "Le parquet ne crisse pas sous vos pas, les fenêtres sont ornées de cadres en chêne..."
                liste_commentaire.append(commentaire)
                commentaire = "*Un peu comme une pause, finalement.*\n*Je n'ai plus besoin de faire semblant, pendant juste un instant.*"
                liste_commentaire.append(commentaire)
                commentaire = "Un doux feu crépite dans les différentes cheminées occupant des espaces décorés ..."
                liste_commentaire.append(commentaire)
                commentaire = "*Certains disent qu'on peut se perdre dans son role.*\n*Cet étage là, c'est un peu comme une fenetre sur ce que j'étais, avant.*"
                liste_commentaire.append(commentaire)
                commentaire = "Un magnifique piano blanc comme la neige throne au milieu de la salle, éclairé par un lustre de jade."
                liste_commentaire.append(commentaire)
                commentaire = "*Un magnifique panorama.*\n*Une tendre embrassade venue du passé.*\n*Un peu d'ordre dans la tempête chaotique qu'est ma vie.*"
                liste_commentaire.append(commentaire)
                commentaire = "Le boss de l'étage est assis là, répétant la même musique , encore et encore."
                liste_commentaire.append(commentaire)
                commentaire = "*Tu sais, si j'avais pu jouer cette petite mélodie...*"
                liste_commentaire.append(commentaire)
                commentaire = "*Impressionner le Roi...*"
                liste_commentaire.append(commentaire)
                commentaire = "*Ou juste écouté mon père...*"
                liste_commentaire.append(commentaire)
                commentaire = "*...alors peut être que j'aurais pu rester ici.*"
                liste_commentaire.append(commentaire)
                commentaire = "*Pas de fautes, pas d'embarras, pas de problèmes.*"
                liste_commentaire.append(commentaire)
                commentaire = "*J'ai mal appellé le diable, et il s'est tant amusé de mes bouffoneries qu'il m'a pris sous son aile.*"
                liste_commentaire.append(commentaire)
                commentaire = "*Et cette singulière erreur est devenu le point tournant de ma vie.*\n*Une bien trop amère leçon qui m'aura tout coûté.*"
                liste_commentaire.append(commentaire)
                commentaire = "*Mais je ne suis pas dupe.*"
                liste_commentaire.append(commentaire)
                commentaire = "Vous sentez de la colère dans les notes."
                liste_commentaire.append(commentaire)
                commentaire = "*Il serait bien présomptueux de débarquer dans cette étrange batisse de chair et d'âme, et de s'attendre a ce que tout le monde soit un villain dans l'histoire.*"
                liste_commentaire.append(commentaire)
                commentaire = "*Certains sont des victimes, d'autres se réfugient dans la folie, d'autres encore sont aveuglés par la loyauté, et les derniers ont en eux le Mal dans toute son horreur.*\n*Mais tout vient d'un seul sentiment, Terriblement humain :*"
                liste_commentaire.append(commentaire)
                commentaire = "*Le désir de vivre.*\n*De survivre.*\n*Tel un cafard vivant dans les cachots de la honte,*"
                liste_commentaire.append(commentaire)
                commentaire = "*les palais de la force,*"
                liste_commentaire.append(commentaire)
                commentaire = "*l'étreinte du désespoir,*"
                liste_commentaire.append(commentaire)
                commentaire = "*mais vivant toujours.*"
                liste_commentaire.append(commentaire)
                commentaire = "La musique se fait plus lente, mélancolique."
                liste_commentaire.append(commentaire)
                commentaire = "*Dans quoi un tel insecte peut se réconforter à part le passé ?*"
                liste_commentaire.append(commentaire)
                commentaire = "*A part un nom d'ici, j'avais tout pour moi.*\n*Un Chateau de luxe et de satin dans lequel travailler, Une famille pour m'épauler, Un hobbie pour m'aporter fierté...*"
                liste_commentaire.append(commentaire)
                commentaire = "*...et même quand tout cela s'est effondré, dans ces abysses de rancoeur et de folie, j'ai quand meme trouvé la force d'avancer, et le véritable amour !*"
                liste_commentaire.append(commentaire)
                commentaire = "*Je me rapelle, on se tenait l'un à coté de l'autre, les mains sur le meme piano...*"
                liste_commentaire.append(commentaire)

            else :
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
        elif services.Player.numero_de_letage == 6:
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
                "*Pas de réponse ?*"
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
        elif services.Player.numero_de_letage == 7:
            if services.Player.nom_de_letage == "Douves du Pénitent":
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
                commentaire = "*J'ai jeté un chevalier qui ne voulait que mon bien dans un affreux paysage. Découpé mon frère pour creer un garde capable de me défendre de mes propres démons.*"
                liste_commentaire.append(commentaire)
                commentaire = "*Fusionné mes ministres avec la fabrique du temps, pour me protéger d'invisibles et tout-puissants ennemis. Contaminé de ma folie le plus involontairement drole des Hommes du nord.*"
                liste_commentaire.append(commentaire)
                commentaire = "*J'ai brûlé sa chair et sa maison. Immolé son coeur. Tout ca pour une simple fausse note.*"
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
                commentaire = "Un halo cramoisi enveloppe la tête nue du Roi, et celui ci se met à dégager une puissante aura corrosive."
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
                commentaire = "*Ce pion a tué mon apprentie. Je m'occuperais personnellement de son cas. Débrouillez vous avec ca.*"
                liste_commentaire.append(commentaire)
                commentaire = "Une armure d'or et de rubis magiques apparait sur le Roi Déchu. Une épée apparait a ses pieds."
                liste_commentaire.append(commentaire)
                commentaire = "*HAHAHA!*\n*A nous deux maintenant ASSASSIN !* "
                liste_commentaire.append(commentaire)
        elif services.Player.numero_de_letage == 8:
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
            commentaire = "*...d'un faux génie, un trésor d'efforts sans résultats, une apprentie loyale brisée par ses propres démons...*"
            liste_commentaire.append(commentaire)
            commentaire = "*...d'un homme du nord portant un masque de faux sourires, porté par son désir de survivre...*"
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
                "le Maitre Mage prend une grande inspiration."
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
        elif services.Player.numero_de_letage == 9:
            commentaire = "" "\n" "\n"
        elif services.Player.nom_de_letage == "Dédale Frontière" :
            commentaire = "" "\n" "\n"
        elif services.Player.nom_de_letage == "Limbes Flétrissants" :
            if services.Player.numero_boss_alt == 1:
                commentaire = "" "\n" "\n"
            elif services.Player.numero_boss_alt == 2:
                commentaire = "" "\n" "\n"
            elif services.Player.numero_boss_alt == 3:
                commentaire = "" "\n" "\n"
            elif services.Player.numero_boss_alt == 4:
                commentaire = "" "\n" "\n"
            elif services.Player.numero_boss_alt == 5:
                commentaire = "" "\n" "\n"
            elif services.Player.numero_boss_alt == 6:
                commentaire = "" "\n" "\n"
            elif services.Player.numero_boss_alt == 7:
                commentaire = "" "\n" "\n"
            elif services.Player.numero_boss_alt == 8:
                commentaire = "" "\n" "\n"
            elif services.Player.numero_boss_alt == 9:
                commentaire = "" "\n" "\n"
            elif services.Player.numero_boss_alt == 10:
                commentaire = "" "\n" "\n"
        for commentaire in liste_commentaire:
            services.Affichage.IntroBoss(commentaire)

        if services.Player.nom_de_letage == "Le Lumisade":
            StopAllMusic()
            PlayMusic("boss_5_alt_fight_intro", "intro")
            print("C'était ma jolie oie des neiges, libérée le temps d'un soupir de son affreux canard...")
            services.Affichage.AfficheAvecUnTempsDattente(3.3)
            print("Un rayon de soleil aussi fort que l'amour parental, perçant a travers les glaces...")
            services.Affichage.AfficheAvecUnTempsDattente(3.3)
            print("J'ai fait tout pour garder le bon cap, être une bonne personne, profitant des rares éclaircies..")
            services.Affichage.AfficheAvecUnTempsDattente(3.3)
            print("Des joies, de mon futur, mon bohneur, mon destin radieux...")
            services.Affichage.AfficheAvecUnTempsDattente(2.75)
            print("..qui m'a été ARRACHE !")
            services.Affichage.AfficheAvecUnTempsDattente(1)
            print("L'hotel s'embrase dans un éclair de feu !")
            services.Affichage.AfficheAvecUnTempsDattente(0.5)
            print("MERDE !")
            time.sleep(0.25)
            print("MERDE !")
            time.sleep(0.25)
            print("MERDE !")
            time.sleep(0.25)
            print("MERDE !")
            time.sleep(0.25)
            print("MERDE !")
            services.Affichage.AfficheAvecUnTempsDattente(0.25)
            print("QUELLE SITUATION DE MERDE !!!")
            services.Affichage.AfficheAvecUnTempsDattente(1)
            print("ROI DE MERDE !!!")
            time.sleep(0.5)
            print("PIERRE DE MERDE !!!")
            time.sleep(0.5)
            print("COLISEE DE MERDE !!!")
            time.sleep(0.5)
            print("DESTIN DE MERDE !!!")
            services.Affichage.AfficheAvecUnTempsDattente(0.75)
            print("J'AI FAIT QUOI POUR MERITER CETTE TORTURE ??? HEIN ???")
            services.Affichage.AfficheAvecUnTempsDattente(1.75)
            print("OH PERE, VOS DERNIERES VOLONTEES AURONT ETE MA PLUS GRANDE MALEDICTION...")
            services.Affichage.AfficheAvecUnTempsDattente(2.75)
            print("Le Boss se retourne.")
            services.Affichage.AfficheAvecUnTempsDattente(1)
            print("DANSONS MARIONETTE !")
            services.Affichage.AfficheAvecUnTempsDattente(1)


    def AfficheDescente(self):
        if services.Player.nom_de_letage == "Limbes Flétrissants" and services.Player.numero_boss_alt != 11:
            print("L'ennemi battu, vous entendez quelque chose s'ouvrir.")
            self.EntreePourContinuer()
            print("C'est la porte de la ferme en ruine.")
            self.EntreePourContinuer()
            print("A l'interieur, vous ne voyez pas grand chose d'interressant.")
            print("Le bois vermoulu crisse et plie sous vos pas, et seul le son du vent a travers les planches semble vous accompagner.")
            self.EntreePourContinuer()
            print("Dans un coin proche de l'entrée, vous trouvez un vieil escalier de bois, descendant dans l'obscurité.")
            self.EntreePourContinuer()
        elif services.Player.nom_de_letage == "Limbes Flétrissants" and services.Player.numero_boss_alt == 11:
            StopAllMusic()
            print("Vous vous approchez de la maison en ruine.")
            self.EntreePourContinuer()
            print("La porte s'ouvre lentement.")
            self.EntreePourContinuer()
            print("Derrière, vous trouvez une commode en ruine surmontée d'un coffret de bois d'olivier.")
            if services.Player.death_divinity :
                print("A l'interieur, il y a plusieurs boites de bois noir !")
                services.FloorMaker.GiveRandomArtefact()
                services.FloorMaker.GiveRandomArtefact()
                services.FloorMaker.GiveRandomArtefact()
                print("Après avoir récupéré les artefacts, vous regardez autour de vous pour trouver une sortie.")
                self.EntreePourContinuer()
                print("Au niveau de la cuisine, vous voyez une faille, ou une fracture a hauteur de tête.")
                self.EntreePourContinuer()
                print("Comme si quelqu'un ou quelque chose était passé par là, mais avait rebroussé chemin après n'avoir rien trouvé.")
                self.EntreePourContinuer()
                print("Vous entrez dans la faille, et vous retrouvez dans un escalier de pierre.")
                services.Player.numero_de_letage = 10
                services.Player.etage_alternatif = False

            else:
                self.EntreePourContinuer()
                print("A l'interieur, vous trouvez une photo jaunie par le temps, sur laquelle une centaine de figures différentes, toutes drapées de chitons, se tiennent par les épaules et sourient.")
                self.EntreePourContinuer()
                print("Derriere, il est écrit : *Dans la vie comme dans la mort, je ne fait qu'envier votre sort.*")
                self.EntreePourContinuer()
                print("...")
                self.EntreePourContinuer()
                donnees_de_s0ve = services.Observation.GetPermanentThingsFromS0ve()
                donnees_de_s0ve["77454135415415"] = "Divinité de la Mort"
                services.Observation.SetPermanentThingsToS0ve(donnees_de_s0ve)
                dir_path = DOSSIER_RESSOURCES
                chemin_du_fichier_save = dir_path + "\\save.txt"
                os.remove(chemin_du_fichier_save)
                PlaySound("questdone")
                print("Vous obtenez la Divinité de la Mort !")
                print("\nC'est une photo du dernier panthéon des dieux, il y a bien longtemps.\nElle est imprégnée de la culpabilité du Dieu de la Mort, seul survivant de la Guerre de l'Interdit.")
                print("\n - Vous pouvez désormais utiliser les méchanismes anciens a leurs plein potentiel !")
                self.EntreePourContinuer()
                print(" - Terah gagne le Deuxieme Stigma Positif [Réceptacle de la Mort] !")
                self.EntreePourContinuer()
                print(" - Vous pouvez désormais utiliser l'élément de la Mort ! Vous pouvez retrouver la liste des talents Ames dans le fichi[ERREUR : FICHIER INTROUVABLE] ")
                print("[FICHIER NOM:122367325 ADDRESSE IPV4:(XXX) INTROUVABLE]")
                self.EntreePourContinuer()
                print(" - La porte aux redcoins s'ouvre désormais pour tout les personnages jouables ! Finissez le boss rush a nouveau pour gagner 5 artefacts et sortez directement a l'étage 11 !")
                self.EntreePourContinuer()
                print(" - Les musiques des Limbes s'offrent a vous dans l'observatorium : entrez le code 2831805 ! ")
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
                print("Terah sentit la pierre de désir fracturer l'espace pour venir jusqu'à lui.")
                self.EntreePourContinuer()
                print("Il vit une ombre affreuse venir de la cuisine.")
                self.EntreePourContinuer()
                print("Terah ignora la voix tordue de la chose en face, ferma les yeux, et compta jusqu'à quatre.")
                time.sleep(2.5)
                ClearConsole()
                print("[B0NJ0uR PeTITT5 FL5URR !!§§:;/ 1L EST T3MPsss D- ]")
                time.sleep(1.5)
                sys.exit()
        elif "Passe La Porte Redcoin" not in services.Player.player_tags :
            print(
                "Vous pressez votre main contre la grille autrefois fermée."
                "\nAlors que la clé incrustée s'efface de votre main, la grille s'ouvre lentement."
            )
            self.EntreePourContinuer()
        if "Draupnir" in services.Player.liste_dartefacts_optionels and "Passe La Porte Redcoin" not in services.Player.player_tags :
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
            gain_gold = services.Player.nombre_de_gold
            services.Player.AddGoldToPlayer(gain_gold)
            print(f"Après une petite heure a tout ramasser, vous vous retrouvez avec {gain_gold} golds supplémentaires !")
            self.EntreePourContinuer()
        if "Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure" in services.Player.liste_dartefacts_optionels:
            print("Alors que vous avancez, vous trébuchez sur votre propre pied et tombez sur le sol.")
            self.EntreePourContinuer()
            print("Votre Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure tombe de votre inventaire et se brise en plusieurs centaines de morceaux !")
            self.EntreePourContinuer()
            services.Player.liste_dartefacts_optionels.remove("Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure")
            print("Vous faites le deuil de votre Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure et continuez d'avancer, une larme perlant à l'oeuil et les meilleurs souvenirs passés avec votre Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure passant en boucle dans votre mémoire...")
            self.EntreePourContinuer()
        for artefact in services.Player.liste_dartefacts_optionels:
            if artefact in ["Element [Ame] Surchargé", "Element [Foudre] Surchargé", "Element [Feu] Surchargé", "Element [Terre] Surchargé", "Element [Glace] Surchargé", "Element [Sang] Surchargé", "Element [Corps] Surchargé"]:
                services.Player.liste_dartefacts_optionels.remove(artefact)
                print("Vous sentez l'appel de la nature et vous soulagez sur place.")
                print(f"Vous perdez l'effet [{artefact}] de la boisson que vous aviez bu !")
                self.EntreePourContinuer()
        if "Assurance Distributeur" in services.Player.liste_dartefacts_optionels:
            print(f"L'artefact [Assurance Distributeur] part en fumée, protégeant ainsi les artefacts achetés au distributeur !")
            services.Player.liste_dartefacts_optionels.remove("Assurance Distributeur")
            self.EntreePourContinuer()
        else:
            for artefact in services.Player.liste_dartefacts_optionels:
                if artefact in ["Epée de Damocles", "Morceau d'Ether Fragile", "Eau Bénite", "Bandeau Catharsis", "Charbon Primordial", "Saphir de Gel", "Fossile Figé", "Fiole des Eclairs"]:
                    services.Player.liste_dartefacts_optionels.remove(artefact)
                    print(f"L'artefact [{artefact}] disparait de votre inventaire !\nLes artefacts achetés au distributeurs ne tiennent vraiment pas dans la durée...")
                    self.EntreePourContinuer()
        if "Canigou" in services.Player.liste_dartefacts_optionels:
            services.Player.liste_dartefacts_optionels.remove("Canigou")
            print("Alors que vous avancez, Canigou fait des petits gémissements de douleur.")
            self.EntreePourContinuer()
            print("Vous saviez qu'un chien modifié ne survivrait pas longtemps en dehors d'un habitat spécifiquement désigné pour lui.")
            print("Vous regardez Canigou avec des larmes dans vos yeux, le caressez une dernière fois, et le laissez repartir dans la niche d'ou il vient.")
            self.EntreePourContinuer()
            print("Adieu, petit chien. On se reverra dans une autre partie.")
            self.EntreePourContinuer()
        if ("Regard de la Bête" in services.Player.liste_dartefacts_optionels and (not "Âme de la Bête" in services.Player.liste_dartefacts_optionels) 
            and (not "Âme de la Bête" in services.Player.liste_dartefacts_optionels)) :
            print("Un peu plus bas dans les escaliers, vous trouvez des morceaux de fer.")
            self.EntreePourContinuer()
            print("Vous aviez vu des marques de griffe au niveau de la grille, mais ne pensiez pas que la bête que vous aviez libéré puisse descendre sans la Clé Incrustée...")
            self.EntreePourContinuer()
            print("...?")
            self.EntreePourContinuer()
            print("Quelque chose brille entre les morceaux de grille éparpillés au sol.")
            self.EntreePourContinuer()
            print("Vous obtenez l'artefact [Ecaille de la Bête] !")
            print("Le dernier témoin de l'existence d'une bête féroce dans le Coliseum, laissée derriere a la poursuite de la liberté.\nVous gagnez 10 points de défence !")
            services.FloorMaker.GiveRandomArtefact("Ecaille de la Bête","Don")
            services.Player.points_de_defence += 10
            self.EntreePourContinuer()
            donnees_de_s0ve = services.Observation.GetPermanentThingsFromS0ve() 
            liste_dartefact_debloque = ast.literal_eval(donnees_de_s0ve["Artefact Debloques"])
            if not "Ecaille de la Bête" in liste_dartefact_debloque :
                PlaySound("questdone")
                print("L'artefact [Ecaille de la Bête] est désormais disponible dans la livre de la Cigogne Bleue !")
                self.EntreePourContinuer()
                liste_dartefact_debloque.append("Ecaille de la Bête")
                donnees_de_s0ve["Artefact Debloques"] = liste_dartefact_debloque
                services.Observation.SetPermanentThingsToS0ve(donnees_de_s0ve)
        if  services.Sove.ModifieTagsDansSove("Checke", "Chuchoteur"):
            if RegardeSiEtageCompletementObserve(services.FloorMaker.FloorBlueprint):
                print("Vous avez terminé l'étage, et avez observé toute les salles observables !")
                print("Vous mémorisez la structure de l'étage dans un coin de votre esprit.")
                print("Vous gagnez une Carte Mentale !")
                services.Sove.ModifieDechetsDansSove("Ajout", "Carte Mentale", 1)



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

    def AffichePartirMarchand(self, argent_depense):
        print("Vous faites un signe au marchand et repassez la porte de tissu.")
        self.EntreePourContinuer()
        if argent_depense >= services.Player.numero_de_letage * 150 or argent_depense >= 1000:
            print("Ce dernier vous arrête dans vos pas, et vous donne un jeton singulier.")
            self.EntreePourContinuer()
            print("Il vous explique que ce ce cadeau récompense celle et ceux qui déboursent plus d'un certain nombre de gold, en une fois.")
            self.EntreePourContinuer()
            print("Quand vous lui demander quoi faire de ce jeton, il vous fait un sourire malicieux, et designe le symbole triangulaire qui orne sa porte.")
            self.EntreePourContinuer()
            print("Vous gagnez un Jeton !")
            self.EntreePourContinuer()
            services.Player.jetons += 1
        nombre_aleatoire = random.randint(0, 100)
        if services.Player.numero_de_letage == 1 and  services.Sove.ModifieTagsDansSove("Checke","Livraison En Attente"):
            services.Sove.ModifieTagsDansSove("Enleve","Livraison En Attente")
            services.Sove.ModifieTagsDansSove("Ajout","Livraison Terminée")
            print("Le marchand vous arrête, vous observe quelques instants, et vous tend une petite boite de carton noir enrobée dans un tissu rouge élégant.")
            services.Affichage.EntreePourContinuer()
            print("Vous ouvrez la boite et trouvez :")
            PasseDeLivraisonABonus()
            services.Affichage.EntreePourContinuer()
            print("Au fond de la boite, il y a un simple morceau de papier sur lequel est écrit :")
            print("*Quelqu'un pense a vous.*")
            services.Affichage.EntreePourContinuer()
            services.Save.SaveTheGameSansAffichage()
        elif nombre_aleatoire <= 10:
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
        StopAllMusic()
        if services.Player.numero_de_letage == 0:
            commentaire = (
                "Vous ouvrez les yeux en bas d'un escalier monumental dont les marches semblent s'effondrer sur elle même."
                "\nEn vous retournant, vous découvrez un espace sali par le sang et la poussière, jonchés de constructions humaines faites d'os et de terre."
                "\nLa grille est grande ouverte, et une masse argentée semble flotter au milieu de l'arène."
                "\nVous voici a l'étage zéro du Coliseum , la cage mélancolique d'une âme brisée."
            )
            services.Player.boss_battu = True
        elif services.Player.numero_de_letage == 1:
            commentaire = (
                "Vous descendez les marches de l'escalier en spirale, et sentez une odeur acre de moisissure monter a vos narines."
                "\nDes murs crasseux, des gradins en ruine, et un sol de gravier et d'os mélangés vous attendent a la fin."
                "\nVous voici au premier étage du Coliseum , une ruine mal entretenue."
            )
            if services.Player.benediction == "Augmenté":
                if not "Affinitée de Foudre" in services.Player.talents_possedes:
                    services.Player.talents_possedes.append("Affinitée de Foudre")
                if not "Affinitée de Glace" in services.Player.talents_possedes:
                    services.Player.talents_possedes.append("Affinitée de Glace")
                if not "Affinitée de Terre" in services.Player.talents_possedes:
                    services.Player.talents_possedes.append("Affinitée de Terre")
                if not "Affinitée de Feu" in services.Player.talents_possedes:
                    services.Player.talents_possedes.append("Affinitée de Feu")
                if not "Affinitée de Sang" in services.Player.talents_possedes:
                    services.Player.talents_possedes.append("Affinitée de Sang")
                if not "Affinitée Physique" in services.Player.talents_possedes:
                    services.Player.talents_possedes.append("Affinitée Physique")
                if not "Elémento-Réceptif" in services.Player.talents_possedes:
                    services.Player.talents_possedes.append("Elémento-Réceptif")
                
        elif services.Player.numero_de_letage == 2:
            if services.Player.nom_de_letage == "Jungle Cruelle" :
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
        elif services.Player.numero_de_letage == 3:
            commentaire = (
                "Vous laissez derrière vous l'humiditée excessive, et entendez un bruissement sourd."
                "\nUn sol jaune granuleux dans lequel on s'enfonce, un étage sans mur, un soleil artificiel et "
                "\nun vent impossible battant le sable dans vos yeux vous attendent en bas."
                "\nVous voici au troisième étage du Coliseum , un océan de sable."
            )
        elif services.Player.numero_de_letage == 4:
            commentaire = (
                "Vous laissez derrière vous la sécheresse, et revenez a un environement plus comfortable."
                "\nDes murs infiniment haut sur lesquels reposent des étagères remplies d'un nombre impossible de livres, "
                "\ndes plateaux volants remplis de bouquins, allant d'un bout a l'autre de l'arene, et un sol couvert de moquette douce au toucher vous attendent en bas."
                "\nVous voici au quatrième étage du Coliseum , une tour dédiée a l'étude de la magie."
            )
        elif services.Player.numero_de_letage == 5:
            if services.Player.nom_de_letage == "Carnaval de Rouille" :
                commentaire = (
                    "Vous laissez derrière vous les livres, et entendez une musique entêtante."
                    "\nDes clowns peints sur le mur, des manequins souriants simulant une foule désoeuvrée,"
                    "\ndes fausses attractions fabriquées a la hâte avec quelques bouts de carton ,"
                    "\net de vieilles enceintes crachant une musique joyeuse en boucle vous attendent en bas."
                    "\nVous voici au cinquième étage du Coliseum , une misérable fête foraine."
                )
            else:
                commentaire = (
                    "Vous laissez derrière vous les livres, et ressentez la morsure du froid."
                    "\nLe hall d'entrée d'un somptueux hotel, une délicieuse musique qui se répand depuis la salle du bal,"
                    "\net des fenetres  donnant vue sur de magnifiques décord enneigés cerclés par des cathédrales montagnes de pierres vous attendent en bas."
                    "\nTout est exquis, si on ne prete pas attention au manque de gens et aux taches de brulé sur les murs."
                    "\nVous voici au cinquième étage du Coliseum , le grand et luxueux hôtel du Nord : Le Lumisade."
                )
        elif services.Player.numero_de_letage == 6:
            commentaire = (
                "Vous laissez derrière vous la folie, et ressentez une présence particulière."
                "\nUn bidonville vide de monde, dans lequel sont parsemés horloges montres et alarmes brisées, "
                "\ndes vieilles banderoles trouées accrochées au plafond, et une gigantesque tour d'horloge au milieu de l'arène vous attendent en bas."
                "\nVous entendez le tic particulier d'un mécanisme, mais l'aiguille des secondes est coincée sur 13h42."
                "\nVous voici au sixième étage du Coliseum , une fracture entre temps et société de quartiers pauvres."
            )
        elif services.Player.numero_de_letage == 7:
            if services.Player.nom_de_letage == "Douves du Pénitent":
                commentaire = (
                    "Vous laissez derrière vous le royaume du prince des voleurs, et entendez le sons de quelques clapotis."
                    "\nDes murs de pierre nus, trainés dans la boue, des grilles protégeants quelques culs de sacs des rares personnes a s'aventurer ici, "
                    "\net une peu profonde mais omniprésente couche d'eau tapissant le sol d'un étage qui ressemble plus a une prison innondée qu'à un lieu de vie."
                    "\nVous voici au septieme étage du Coliseum , la bulle de confort d'un esprit torturé par ses propres décisions, pleurant a jamais un pardon qui ne peut être accordé."
                )
            else:
                commentaire = (
                    "Vous laissez derrière vous le royaume du prince des voleurs, et sentez la température augmenter."
                    "\nDes flammes inextinguibles, des cris sans réponses venant de nulle part, des cadavres accrochés a différents instruments de torture, "
                    "\net le mot *Traitre* écrit a l'aide de différents type **d'encre** sur tout les murs de l'arène, telle est la vision qui vous attend en bas."
                    "\nVous voici au septieme étage du Coliseum , le bac à sable d'un esprit fou, torturé, paranoïaque."
                )
        elif services.Player.numero_de_letage == 8:
            commentaire = (
                "Vous laissez derrière vous les esprits torturés, et vous concentrez sur votre but."
                "\nDes murs propres, neufs, ornés de torches. Un sol de marbre, dépassant les gradins, montant au plafond.\nEt une place au dessus de la sortie,"
                " sur laquelle se trouve un vieil homme à la barbe blanche, soignée.\nVoila ce que vous trouvez en bas."
                "\nVous voici au huitième étage du Coliseum , une arène digne de ce nom pour un affrontement avec son créateur."
            )
        elif services.Player.numero_de_letage == 9 and not ("Marque du Sacrifice" in services.Player.liste_dartefacts_optionels):
            print(
                "Derrière, vous voyez un long couloir.\nUne vieille porte rouillée a votre gauche vous intrigue,"
                " mais pas plus que ca."
            )
            services.Affichage.EntreePourContinuer()
            print(
                "Sur le chemin menant a la fin du couloir, vous voyez un petit trou dans les murs."
                "\nA l'interieur, vous apercevez le mot coliseum reposant sur une sorte d'épée,\navec un genre de scintillement au dessus du i."
                "\nEn dessous, le mot O B S E R V A T O R I U M est gravé au couteau, et un nombre en dessous de chaques lettre."
                "\nCa fait un nombre sacrément long !"
            )
            services.Affichage.EntreePourContinuer()
            commentaire = (
                "Mais vos pensées sont interrompues par le chant des oiseaux que vous entendez a quelques metres."
                "\nVous courrez en direction de la sortie, et retrouvez l'herbe verte, les batiments au loin, et le grillage"
                " caractéristique entourant le Coliseum.\nVous êtes sorti vivant !"
            )
        elif services.Player.numero_de_letage == 9:
            print("Vous arrivez au couloir de la sortie, mais vos yeux sont fixé sur l'étrange porte rouillée a votre gauche.")
            services.Affichage.EntreePourContinuer()
            print("La marque sur votre épaule chauffe un peu, et la porte s'ouvre en grand.")
            services.Affichage.EntreePourContinuer()
            print("Vous descendez les escaliers derrière la porte.")
            services.Affichage.EntreePourContinuer()
            commentaire = (
                "Vous laissez derrière vous la sortie et les promesses de vie facile à la poursuite de la véritée."
                "\nUn étage étrange, ou la fabrique de la réalitée semble venir mourir a vos pied."
                "\nVous pouvez retrouver un élément de chaque étages sur le sol froid de l'arène, et quand ce n'est pas leur couleur, c'est leur proportion qui varie."
                "\nCertaines banderolles sont encastrés dans le mur, des carrés de sables sortent ca et la de nulle part, "
                "\net vous êtes a peu pres sur que la géométrie des lieux est non euclidienne vu que vous pouvez traverser la salle en un pas si vous passez au bon endroit."
                "\nVous voici au neuvième étage du Coliseum , une poubelle ou viennent reposer les concepts oubliés."
            )
        elif services.Player.numero_de_letage == 10:
            if services.Player.nom_de_letage == "Limbes Flétrissants" and services.Player.numero_boss_alt == 1:
                commentaire = (
                    "Vous passez la porte, qui se referme derriere vous."
                    "\nDevant vous s'étend un vide noir pourpre qui semble ne jamais finir, et en vous retournant vous ne voyez plus la porte."
                    "\nA la place, vous voyez une batisse de bois décrépite, comme une ferme, entourés par des champs labourés stériles, le tout sur une ile qui semble flotter dans le vide."
                    "\nUne entité vous attend devant la porte de la ferme, la même qui vous a attiré ici vous en êtes sûr."
                    "\nVous voici Là ou les Fleurs viennent Fâner, quelque part dans le Coliseum."
                )
            elif services.Player.nom_de_letage == "Limbes Flétrissants" and services.Player.numero_boss_alt != 1:
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
        elif services.Player.numero_de_letage == 11:
            commentaire = (
                "Vous laissez enfin les marches de l'étage interminable et avancez vers la fin de votre voyage."
                "\nUne salle blanche vous attend en bas. Tout est blanc, et vous n'arrivez pas a définir les limites de la salle. Il n'y a que le nécessaire."
                "\nVous voici au onzième étage du Coliseum , la pénultième vision."
            )
        elif services.Player.numero_de_letage == 12:
            commentaire = (
                "Derrière, vous retrouvez le chant des oiseaux, l'herbe verte, et le grillage"
                " caractéristique entourant le Coliseum.\nVous êtes sorti vivant, riche, et puissant !"
            )
        print(commentaire)
        services.Affichage.EntreePourContinuer()
        services.Sove.RajouteEntreeAuLivreCigogneBlancheSiOnAPas("Les Etages", services.Player.nom_de_letage)
        if services.Player.numero_de_letage == 1 and services.Player.mode_de_jeu != "Ascension":
            DonneSouvenirsDeTechniqueEtSorts()
        if services.Player.benediction == "Polyvalent"and services.Player.mode_de_jeu != "Ascension":
            print("D'anciennes prières arrivent jusqu'à vous, et font apparaitre une petite boite de bois noir, que vous vous empressez d'ouvrir !")
            services.Affichage.EntreePourContinuer()
            services.FloorMaker.GiveRandomArtefact()
        if services.Player.benediction == "Extraordinaire"and services.Player.mode_de_jeu != "Ascension":
            print("D'anciennes prières arrivent jusqu'à vous, et enchantent une de vos actions !")
            services.Affichage.EntreePourContinuer()
            EnchantementAleatoire()
        if services.Player.numero_de_letage == 4 and "Mage" in services.Player.liste_dartefacts_optionels:
            print("*Je... je sens quelque chose.*")
            services.Affichage.EntreePourContinuer()
            print("Vous stoppez votre descente au moment ou vos pieds touchent le sol de l'étage, et vous tournez vers la Mage qui vous accompagne.")
            services.Affichage.EntreePourContinuer()
            print("*C'est la que nos chemins se séparent.*")
            services.Affichage.EntreePourContinuer()
            print("Vous lui lancez un regard sévère, inquisiteur.")
            services.Affichage.EntreePourContinuer()
            print("*Quand je fais quelque chose, je le fais en suivant mon instinct. Et c'est toujours la bonne chose a faire.*")
            services.Affichage.EntreePourContinuer()
            print("*Et la, j'ai très envie de toucher ce bouton.*")
            services.Affichage.EntreePourContinuer()
            print("Vous regardez le bouton en question, que vous n'aviez jamais vu auparavant, ainsi que la pancarte *LIVRAISON* juste au dessus")
            services.Affichage.EntreePourContinuer()
            print("*Je ne sais pas ce qui va se passer, mais sache une chose : si on doit se retrouver, on se retrouvera. Et maintenant...*")
            services.Affichage.EntreePourContinuer()
            print("La mage s'approche du bouton, et l'enfonce.")
            services.Affichage.EntreePourContinuer()
            print("Plusieurs secondes s'écoulent...")
            services.Affichage.EntreePourContinuer()
            print("Le bruit des plateaux volants remplit la salle...")
            services.Affichage.EntreePourContinuer()
            print("...")
            services.Affichage.EntreePourContinuer()
            print("*Oh. Fausse alerte alors ! Je m'attendais a quelque chose d'au-")
            time.sleep(3)
            ClearConsole()
            print("Un piano a queue tombe sur la Mage.")
            PlaySound("death")
            services.Affichage.EntreePourContinuer()
            print("Vous n'osez pas regarder la scène, alors qu'un des plateau vous donne un bout de papier sur lequel il est écrit :")
            services.Affichage.EntreePourContinuer()
            print("*LIVRAISON TERMINEE. BONNE JOURNEE !*")
            services.Affichage.EntreePourContinuer()
            print("Vous détournez le regard, et avancez au centre de l'arène.")
            services.Affichage.EntreePourContinuer()
            services.Player.liste_dartefacts_optionels.remove("Mage")
            services.Sove.ModifieTagsDansSove("Ajout", "Mage Hollistique")
