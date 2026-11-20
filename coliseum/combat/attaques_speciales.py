"""Attaques propres à certains monstres et boss (une méthode par attaque)."""

from collections import deque
import os
import random
import time

from coliseum.chemins import DOSSIER_RESSOURCES
from coliseum.console import ClearConsole, attendre

# nom de l'action dans la fiche du monstre -> nom de la méthode qui la joue.
# POURQUOI des noms de méthode et pas les méthodes elles-mêmes : la table est
# construite avant la classe ; `getattr(self, nom)` retrouve la méthode au
# moment du combat (voir UseMonsterAttack et UseMonsterMagic).
SORTS_SPECIAUX_DE_MONSTRE = {
    "Tout Feu Tout Flamme": "ToutFeuToutFlamme",
    "Volepièce": "Volepiece",
    "Bandit Manchot": "BanditManchot",
    "Cat-astrophe": "Cat_astrophe",
    "Son Lent": "SonLent",
    "Vole-Ame": "Vole_Ame",
    "Rituel": "Rituel",
    "Tempêtes du Nord": "TempeteDuNord",
    "Tempêtes du Sud": "TempeteDuSud",
    "Tempêtes de l'Est": "TempeteDeEst",
    "Tempêtes de l'Ouest": "TempeteDeOuest",
    "Vacarme Rapide": "VacarmeRapide",
    "Vacarme Lent": "VacarmeLent",
    "Vide": "Vide",
    "Eveil de Runes": "EveilDeRunes",
    "Lamentations": "Lamentations",
    "Invoquation Canope": "InvoquationCanope",
    "Magie Noire": "MagieNoire",
    "Magie Ténébreuse": "MagieTenebreuse",
    "Tournicota": "Tournicota",
    "Tournicotons": "Tournicotons",
    "Tournicotez": "Tournicotez",
    "Tome de Salomon": "TomeDeSalomon",
    "Sort Ultime": "SortUltime",
    "Ultime Ultime": "UltimeUltime",
    "Ultima": "Ultima",
    "Dragon Ascendant": "DragonAscendant",
    "Magie Abyssale": "MagieAbyssale",
    "Jugement": "Jugement",
    "Systeme de Support": "SystemeSupport",
    "Protocole Supernova": "ProtocoleSupernova",
    "Flash Bang": "FlashBang",
    "Laser Anti-Personnel": "LaserAntipersonnel",
    "Symphonie": "Symphonie",
}

# Attaques spéciales qui n'avaient AUCUN jet de touche et infligent des dégâts
# ou des malédictions au joueur : elles reçoivent maintenant le jet d'esquive
# commun (voir LaSpecialeEstEsquivee dans actions_monstre.py).
# Laissées de côté volontairement : Laser Anti-Personnel et Protocole Supernova
# (décrits comme inévitables), Roulette (plusieurs issues mêlées), Ultima,
# Aspiration, et celles qui ont déjà leur propre jet.
SPECIALES_AVEC_JET_D_ESQUIVE = (
    "Laser",
    "Eveil de Runes",
    "Tournicotons",
    "Dragon Ascendant",
    "Vacarme Rapide",
    "Rituel",
    "Lamentations",
)

TECHNIQUES_SPECIALES_DE_MONSTRE = {
    "Durcissement Argilite": "DurcissementArgilite",
    "Envol": "Envol",
    "Hurlement": "Hurlement",
    "Attire-Gold": "AttireGold",
    "Coup Anti-Magie": "CoupAntiMagie",
    "Attire-Magie": "AttireMagie",
    "Aspiration": "Aspiration",
    "Laser": "Laser",
    "Roulette": "Roulette",
    "Jet d'Argent": "JetDargent",
    "Gemme Bleue": "GemmeBleue",
    "Durcissement Calcaire": "DurcissementCalcaire",
    "Combo Misérable": "ComboMiserable",
    "Crystal Elémentaire": "CrystalElementaireDore",
    "Panacée Universelle": "PanaceeUniverselle",
    "Sables du Temps": "SablesDuTemps",
}


class AttaquesSpecialesMixin:

    def ToutFeuToutFlamme(self):
        chance_enflammer = 25
        chance_enflammer += round((self.modele.CHANCEBONUSJOUEURENFEU/100) * chance_enflammer)
        chance_denvoyer_une_flamelette = 80
        nombre_de_flamelette = 0
        nombre_de_tour_enflamme = 0
        commentaire = "L'ennemi lance le Tout Feu Tout flamme ! Des petites flamelettes sortent de son corps et s'approchent de vous !"
        self.vue.AfficheDebutComboFeu(commentaire)
        # determine le nombre de coup infligés
        nombre_aleatoire = 0
        while nombre_aleatoire < chance_denvoyer_une_flamelette:
            nombre_de_flamelette += 1
            commentaire = f"L'ennemi envoie {nombre_de_flamelette} flamelette..."
            #ca enflamme ?
            nombre_aleatoire = random.randint(0,100)
            if nombre_aleatoire < chance_enflammer :
                commentaire_resultat = "\n...qui vous enflamme pour 1 tour !"
                nombre_de_tour_enflamme += 1
            else : 
                commentaire_resultat = "\n...que vous arrivez a esquiver !"
            #affichage
            self.vue.AfficheComboFeu(commentaire, commentaire_resultat)
            #intialisation autre nombre aleatoire sauf si nombre coup > 10
            nombre_aleatoire = random.randint(0,100)
            if nombre_de_flamelette > 9:
                nombre_aleatoire = 100
        if nombre_de_tour_enflamme != 0:
            self.AppliqueEffetElementaireSurJoueur("feu", (nombre_de_tour_enflamme + 1), 5)
            commentaire = (
                "L'assaut des flamelettes s'arrete enfin."
                f"\nAu final, vous resterez enflammé pendant {nombre_de_tour_enflamme} tours !"
            )
        else:
            commentaire = (
                "L'assaut des flamelettes s'arrete enfin."
                "\nEt vous les avez tous esquivés !"
            )
            if "Tiare de Suie" in self.modele.liste_dartefacts_optionels:
                    commentaire += "\nL'artefact [Tiare de Suie] bénit votre échappée !"
                    self.modele.beni_par_feu_sacre = True
                    self.modele.beni_par_feu_sacre_nombre_tour += 2
        self.vue.AfficheFinComboFeu(commentaire)

    def Volepiece(self):
        commentaire = "L'ennemi utilise le sort Volepièce !\nVos golds se mettent a sortir de votre poche et a léviter vers L'ennemi..."
        if self.modele.nombre_de_gold > 0:
            chance_de_reussite = 70
            nombre_aleatoire = random.randint(0, 100)
            if nombre_aleatoire < chance_de_reussite:
                nombre_gold_perdu = round(self.modele.nombre_de_gold * 0.1)
                self.modele.nombre_de_gold -= nombre_gold_perdu
                commentaire_reussite = f"...et vous perdez {nombre_gold_perdu} golds !"
            else:
                self.modele.nombre_de_gold -= 1
                degat = 5
                self.modele.monstre_points_de_vie -= degat
                commentaire_reussite = ("...mais vous ne vous laissez pas faire et frappez"
                                        " de toutes vos forces un des golds flottant en direction"
                                        " de l'ennemi .\nCelui ci est propulsé en arrière par la pièce et"
                                        f" le sort se brise.\nHomerun ! Vous lui infligez {degat} points de dégâts "
                                        "et récuperez tous vos golds !...sauf celui que vous avez envoyé bien evidemment.")
            self.EquilibrageGold()
        else:
            commentaire_reussite = ("...ou pas. L'ennemi incrédule regarde votre poche s'ouvrir"
                                    " et révéler un vide financier aussi troublant que pitoyable (et je pèse mes mots)."
                                    "\nAlors que vous rougissez de honte, l'ennemi vous envoie un"
                                    " regard empli de compassion et fait léviter 50 de ses propres golds vers "
                                    "votre poche encore ouverte !\n \n \nNe parlons plus *jamais* de cet incident.\n")
            self.modele.nombre_de_gold = 50
        self.vue.AfficheVolepiece(commentaire, commentaire_reussite)

    def BanditManchot(self):
        commentaire = ("L'ennemi fait apparaitre une machine a sous, le Bandit Manchot,"
                       " en plein milieu de la salle !\nTrois grosses roues se mettent a"
                       " tourner avant de s'arreter progressivement...")
        self.vue.AfficheBanditManchot(commentaire)
        liste_symbole = []
        numero_symbole = 0
        while numero_symbole != 3:
            numero_symbole += 1
            nombre_aleatoire = random.randint(1, 8)
            if nombre_aleatoire == 1:
                commentaire = f"La roue numéro {numero_symbole} s'arrête sur le symbole [Citron] !"
                liste_symbole.append("Citron")
            elif nombre_aleatoire == 2:
                commentaire = f"La roue numéro {numero_symbole} s'arrête sur le symbole [Charbon] !"
                liste_symbole.append("Charbon")
            elif nombre_aleatoire == 3:
                commentaire = f"La roue numéro {numero_symbole} s'arrête sur le symbole [Cloche] !"
                liste_symbole.append("Cloche")
            elif nombre_aleatoire == 4:
                commentaire = f"La roue numéro {numero_symbole} s'arrête sur le symbole [Quatre] !"
                liste_symbole.append("Quatre")
            elif nombre_aleatoire == 5:
                commentaire = f"La roue numéro {numero_symbole} s'arrête sur le symbole [Ananas] !"
                liste_symbole.append("Ananas")
            elif nombre_aleatoire == 6:
                commentaire = f"La roue numéro {numero_symbole} s'arrête sur le symbole [Diamant] !"
                liste_symbole.append("Diamant")
            elif nombre_aleatoire == 7:
                commentaire = f"La roue numéro {numero_symbole} s'arrête sur le symbole [Fer a Cheval] !"
                liste_symbole.append("Fer à Cheval")
            elif nombre_aleatoire == 8:
                commentaire = f"La roue numéro {numero_symbole} s'arrête sur le symbole [Sept] !"
                liste_symbole.append("Sept")
            self.vue.AfficheRouletteBanditManchot(commentaire)
        if liste_symbole[0] == liste_symbole[1] == liste_symbole[2]: 
            gain = 777
            gain += round(gain * (self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Noyau d'Aurelionite"] / 100 ))
            self.Player.nombre_de_gold += gain
            commentaire = f"\nJACKPOT !\nTout les symboles sont les mêmes !\nVous gagnez {gain} golds !"
            self.vue.AfficheBanditManchot(commentaire)
        else:
            commentaire = "\nVoici les résultats :"
            for symbol in liste_symbole:
                if symbol == "Citron":
                    self.AppliqueEffetElementaireSurJoueur("glace", 2)
                    commentaire += "\n -Vous gelez pendant 2 tours."
                elif symbol == "Charbon":
                    self.AppliqueEffetElementaireSurJoueur("feu", 2, 5)
                    commentaire += "\n -Vous brulez pendant 2 tours."
                elif symbol == "Cloche":
                    nombre_tour = 1
                    self.AppliqueEffetElementaireSurJoueur("foudre", nombre_tour)
                    if self.modele.est_paralyse:
                        commentaire += "\n -Vous êtes paralysé pendant 1 tour."
                    else:
                        commentaire += "\n -Vous deviez être paralysé pendant 1 tour... mais vous y résistez."
                elif symbol == "Quatre":
                    self.AppliqueEffetElementaireSurJoueur("glace", 2)
                    self.AppliqueEffetElementaireSurJoueur("feu", 2, 5)
                    nombre_tour = 2
                    self.AppliqueEffetElementaireSurJoueur("foudre", nombre_tour)
                    if self.modele.est_paralyse:
                        commentaire += "\n -Vous gelez, brulez, êtes paralysé, pendant 2 tours."
                    else:
                        commentaire += "\n -Vous gelez et brulez pendant 1 tour, mais résistez a la paralysie."
                elif symbol == "Ananas":
                    self.modele.monstre_est_gele = True
                    self.modele.monstre_est_gele_nombre_tour += 1
                    commentaire += "\n -L'ennemi est gelé pendant 1 tour."
                elif symbol == "Diamant":
                    self.modele.monstre_est_en_feu = True
                    self.modele.monstre_est_en_feu_nombre_tour += 1
                    self.modele.monstre_est_en_feu_degat = 5
                    commentaire += "\n -L'ennemi est brulé pendant 1 tour."
                elif symbol == "Fer à Cheval":
                    self.modele.monstre_est_paralyse = True
                    self.modele.monstre_est_paralyse_nombre_tour += 1
                    commentaire += "\n -L'ennemi est paralysé pendant 1 tour."
                elif symbol == "Sept":
                    self.modele.monstre_est_gele = True
                    self.modele.monstre_est_gele_nombre_tour += 1
                    self.modele.monstre_est_en_feu = True
                    self.modele.monstre_est_en_feu_nombre_tour += 1
                    self.modele.monstre_est_en_feu_degat = 5
                    self.modele.monstre_est_paralyse = True
                    self.modele.monstre_est_paralyse_nombre_tour += 1
                    commentaire += "\n -L'ennemi est gelé, brulé, paralysé, pendant 1 tour."
            # affinage des dalterations d'état (si nombre de tour = 1, l'ennemi ne le subit pas car nombre de tour = 0 a la fin du tour.)
            # (besoin de rajouter 1 aux nombres de tours)
            self.vue.AfficheBanditManchot(commentaire)

    def SonLent(self):
        commentaire = "L'ennemi joue un son lent et discordant.\nVotre âme est en completement chamboulée.\nOn dirait presque...\n...de la k-pop ?"
        mana_perdu = round(self.modele.points_de_mana_max * 0.2)
        self.modele.points_de_mana -= mana_perdu
        self.EquilibragePointsDeVieEtManaEtEndurance()
        commentaire_2 = f"Vous perdez {mana_perdu} points de mana !"
        self.vue.SonLent(commentaire, commentaire_2)

    def Cat_astrophe(self):
        commentaire = ("L'ennemi revet une tunique noire et invoque le dieu félin de la malchance : Cat-Astrophe !"
                       "\nEn faisant un pas en arrière, vous trébuchez sur une peau de banane...")
        self.vue.AfficheCatastrophe(commentaire)
        nombre_aleatoire = 0
        while nombre_aleatoire < 85:
            nombre_aleatoire = random.randint(0, 20)
            commentaire = self.modele.liste_de_commentaire_pour_catastrophe[nombre_aleatoire]
            self.vue.AfficheCatastrophe(commentaire)
            nombre_aleatoire = random.randint(0, 100)
        commentaire = ("...et l'ennemi profite que vous soyez distrait par cette machine de goldberg grandeur nature pour vous drainer le sang au niveau de la jambe."
                       "\nQuand vous vous en rendez compte, vous échangez un regard confus avec la chose a vos pied pendant quelques secondes."
                       "\nL'ennemi vous lache, retourne a sa position sans vous lacher du regard, et se remet en posture de combat en essayant de cacher son embarras. ")
        commentaire_2 = ("...eeeet vous recevez un coktail de fléchette bleue et rouge dans le dos par la machine de goldberg.\nCat-Astrophe, amusé, repart dans sa dimension.")
        self.AppliqueEffetElementaireSurJoueur("feu", 3, 5)
        self.AppliqueEffetElementaireSurJoueur("glace", 3)
        drain = round(self.modele.points_de_vie_max *0.05)
        drain = self.EnleveVieAuJoueur(drain)
        self.modele.monstre_points_de_vie += drain
        self.EquilibragePointsDeVieEtManaEtEndurance()
        self.CheckePuisAppliqueTransmutation(drain)
        commentaire_3 = (f"Au final, vous vous faites drainer {drain} points de vie. De plus, vous êtes gelé et brulé pendant 2 tours.")
        self.vue.AfficheFinCatastrophe(commentaire, commentaire_2, commentaire_3)
        if self.modele.commentaire_transmutation_degat != "":
            self.vue.AfficheTransmutationDegat(self.modele.commentaire_transmutation_degat)

    def Vole_Ame(self):
        commentaire = "L'ennemi utilise le sort Vole-Ame !\nUne sorte de parasite sort de son front et rentre dans le votre.\nVous entendez une voix résonner dans votre esprit."
        self.vue.AfficheDebutVoleAme(commentaire)
        action_taken = False
        cout = round(self.modele.points_de_vie_max*0.3)
        while action_taken == False:
            try:
                commentaire = ("Eh toi là. Wesh maggle, résiste pas c'est pour ton bien. Sisi jte jure.\n"
                               "On fait un deal gros: tu m'donne ta vie, ou tu m'donne ton mana, sinon jte bousille le corps.\n"
                               "C'est la dèche couzin, m'en veux pas trop. Ou pas. Tu fait c'que tu veux pélo.\n"
                               f"\n1 - Résister quand même (coute {cout} de vie)(la véritée t'a pas interêt mec)\n2 - Donner son mana (-1 point de mana max)"
                               "\n3 - Donner sa vie (-1 point de vie max)")
                commentaire_2 = "Bon alors, tu fais quoi ? Et grouille toi (choisir avec les nombres) "
                choix = self.vue.GetChoiceVoleAme(commentaire, commentaire_2)
                if choix == 1:
                    cout = self.EnleveVieAuJoueur(cout)
                    self.CheckePuisAppliqueTransmutation(cout)
                    commentaire = "Vasy je savais t'était un rat !\n\nLe parasite sort de votre esprit et vous ressentez une grosse douleur un peu partout dans votre corps."
                    action_taken = True
                elif choix == 2:
                    self.modele.points_de_mana_max -= 1
                    commentaire = "Tu régale le S !\n\nLe parasite sort de votre esprit et avec lui, une partie de votre âme"
                    action_taken = True
                elif choix == 3:
                    self.modele.points_de_vie_max -= 1
                    commentaire = "Et au plaisir, narvalo !\n\nLe parasite sort de votre esprit et avec lui, une partie de votre vitalitée."
                    action_taken = True
                ClearConsole()
            except ValueError:
                ClearConsole()
        self.vue.AfficheFinVoleAme(commentaire)
        if self.modele.commentaire_transmutation_degat != "":
            self.vue.AfficheTransmutationDegat(self.modele.commentaire_transmutation_degat)

    def Rituel(self):
        commentaire = ("L'ennemi invoque des bougies tout autour de lui.\nLa salle s'assombrit et des"
                       " lignes de feu se dessinent entre les bougies dans un patterne ésotérique.\nVous"
                       " y reconnaissez la forme d'un papillon, d'un scarabé, et d'un ver de farine.")
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire < 60:
            commentaire_2 = ("Alors que les bougies se mettent a tourner, vous pouvez voir les formes tracées par les ligne de feu"
                             " se mouvoir comme dans un kinéographe. Les 3 insectes sortent alors du cercle et viennent se poser devant vous."
                             "\n \nPuis les bougies s'arretent de tourner brusquemment, et les insectes prennent une forme déformée, gore, comme si ils avaient été écrasés."
                             "\nAu même moment, toutes vos blessures se rouvrent, votre vision se brouille, et des cris d'insectes remplissent votre esprit.")
            degat = round(self.modele.points_de_vie_max * 0.15)
            nombre_tour = 2
            degat = self.EnleveVieAuJoueur(degat)
            self.CheckePuisAppliqueTransmutation(degat)
            self.modele.est_maudit_par_la_vie = True
            self.modele.est_maudit_par_la_vie_nombre_tour += nombre_tour
            self.modele.est_maudit_par_le_mana = True
            self.modele.est_maudit_par_le_mana_nombre_tour += nombre_tour
            self.modele.est_maudit_par_les_items = True
            self.modele.est_maudit_par_les_items_nombre_tour += nombre_tour
            commentaire_degat = (f"Vous perdez {degat} points de vie. Vous êtes bléssé, déconcentré, et confus, pendant 2 tours ! ")
        else:
            commentaire_2 = ("Alors que les bougies se mettent a tourner, vous foncez sur l'ennemi et"
                             " lui envoyez un dropkick bien placé. Les bougies disparaissent et la salle"
                             " retrouve sa lumière !\nLes lignes de brulure au sol sont les seuls restes du rituel.")
            commentaire_degat = ("?\nVous pouvez jurer reconnaitre une tête de mort dans les traces carbonisées...")
        self.vue.AfficheRituel(commentaire, commentaire_2, commentaire_degat)
        if self.modele.commentaire_transmutation_degat != "":
            self.vue.AfficheTransmutationDegat(self.modele.commentaire_transmutation_degat)

    def TempeteDuNord(self):
        commentaire = "L'ennemi fait souffler une tempête venant du Nord ! Le froid est insupportable !"
        commentaire_effet = "Vous gelez pendant 4 tours !"
        self.AppliqueEffetElementaireSurJoueur("glace", 4)
        self.vue.AfficheTempeteOuVacarme(commentaire, commentaire_effet)
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire < 50:
            commentaire_effet = "Le vent rentre dans votre système respiratoire et vous empeche de faire rentrer de l'air !\nVous devenez muet pendant 1 tour !"
            self.modele.est_maudit_par_les_sorts = True
            self.modele.est_maudit_par_les_sorts_nombre_tour += 2
            self.vue.AfficheTempeteOuVacarmeAvecEffet(commentaire_effet)

    def TempeteDuSud(self):
        nombre_tour = 5
        
        commentaire = "L'ennemi fait souffler une tempête venant du Sud ! La chaleur est intenable !"
        commentaire_effet = f"Vous brulez pendant {nombre_tour - 1} tours !"
        self.AppliqueEffetElementaireSurJoueur("feu", nombre_tour, 5)
        self.vue.AfficheTempeteOuVacarme(commentaire, commentaire_effet)
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire < 50:
            commentaire_effet = "Le vent fort vous fait perdre votre équilibre !\nVous devenez instable pendant 1 tour !"
            self.modele.est_maudit_par_les_techniques = True
            self.modele.est_maudit_par_les_techniques_nombre_tour += 2
            self.vue.AfficheTempeteOuVacarmeAvecEffet(commentaire_effet)

    def TempeteDeEst(self):
        commentaire = "L'ennemi fait souffler une tempête venant de l'Est ! L'électricitée statique produite par les particules en friction rentre dans votre corps !"
        nombre_tour = 3
        self.AppliqueEffetElementaireSurJoueur("foudre", nombre_tour)
        if self.modele.est_paralyse:
            commentaire_effet = "Vous devenez paralysé pendant 2 tours !"
        else:
            commentaire_effet = "Mais vous résistez a la paralysie !"
        self.vue.AfficheTempeteOuVacarme(commentaire, commentaire_effet)
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire < 50:
            commentaire_effet = "L'afflux soudain du moyen voltage touche vos neurones !\nVous devenez confus pendant 3 tours !"
            self.modele.est_maudit_par_les_items = True
            self.modele.est_maudit_par_les_items_nombre_tour += 4
            self.vue.AfficheTempeteOuVacarmeAvecEffet(commentaire_effet)

    def TempeteDeOuest(self):
        commentaire = "L'ennemi fait souffler une tempête venant de l'Ouest ! La magie qui l'impregne attire votre énergie vitale vers l'ennemi !"
        saignee = round(self.modele.points_de_vie_max*0.1)
        saignee = self.EnleveVieAuJoueur(saignee)
        self.CheckePuisAppliqueTransmutation(saignee)
        self.modele.monstre_points_de_vie_max += saignee
        self.EquilibragePointsDeVieEtManaEtEndurance()
        commentaire_effet = f"Vous vous faites drainer {saignee} points de vie !"
        self.vue.AfficheTempeteOuVacarme(commentaire, commentaire_effet)
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire < 50:
            commentaire_effet = "Le vent apporte avec lui une maladie exotique !\nVous êtes atteint du Mal Jaune pendant 3 tours !"
            self.modele.est_maudit_par_le_gold = True
            self.modele.est_maudit_par_le_gold_nombre_tour += 4
            self.vue.AfficheTempeteOuVacarmeAvecEffet(commentaire_effet)
        if self.modele.commentaire_transmutation_degat != "":
            self.vue.AfficheTransmutationDegat(self.modele.commentaire_transmutation_degat)

    def VacarmeRapide(self):
        commentaire = "L'ennemi produit un vacarme chaotique qui vous fait saigner des oreilles ! Le son est trop rapide pour être mélodieux !"
        degat = 15 + self.modele.monstre_level
        degat = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat)
        degat = self.EnleveVieAuJoueur(degat)
        commentaire_effet = f"Vous perdez {degat} points de vie ."
        self.vue.AfficheTempeteOuVacarme(commentaire, commentaire_effet)
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire < 50:
            commentaire_effet = "La fréquence du son rentre en résonnance avec vos organes internes et leur cause des dégâts mineurs !\nVous devenez blessé pendant 3 tours !"
            self.modele.est_maudit_par_la_vie = True
            self.modele.est_maudit_par_la_vie_nombre_tour += 4
            self.vue.AfficheTempeteOuVacarmeAvecEffet(commentaire_effet)

    def VacarmeLent(self):
        commentaire = "L'ennemi produit un vacarme strident qui reste trop longtemps sur les même notes ! C'est pire que le crissement d'une craie sur un tableau !"
        degat = round(self.modele.points_de_mana_max * 0.2)
        self.modele.points_de_mana -= degat
        self.EquilibragePointsDeVieEtManaEtEndurance()
        commentaire_effet = f"Le son bouleverse jusqu'à votre âme, et vous fait perdre {degat} points de mana !"
        self.vue.AfficheTempeteOuVacarme(commentaire, commentaire_effet)
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire < 50:
            commentaire_effet = "Entendre ce son vous laissera des séquelles psychologiques pendant un bon bout de temps.\nVous devenez déconcentré pendant 3 tours !"
            self.modele.est_maudit_par_le_mana = True
            self.modele.est_maudit_par_le_mana_nombre_tour += 4
            self.vue.AfficheTempeteOuVacarmeAvecEffet(commentaire_effet)

    def Vide(self):
        commentaire = "L'ennemi... s'ouvre en deux. C'est la meilleure explication que je puisse donner.\nA l'interieur, vous pouvez voir un abysse sans fond..."
        self.vue.AfficheVide(commentaire)
        commentaire = ("...                                                                                                    (O) (O)"
                       "\nTerrifiant.")
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire < 50 :
            commentaire = ("...et une paire de deux yeux paniqués peuvent aussi vous voir.\nVous vous sentez terriblement mal, "
                           "comme si l'origine de toute folie venait de vous prêter attention."
                           "\nVous devenez confus, déconcentré, et déstabilisé pendant 1 tour.")
            self.modele.est_maudit_par_les_techniques = True
            self.modele.est_maudit_par_les_techniques_nombre_tour += 2
            self.modele.est_maudit_par_les_sorts = True
            self.modele.est_maudit_par_les_sorts_nombre_tour += 2
            self.modele.est_maudit_par_les_items = True
            self.modele.est_maudit_par_les_items_nombre_tour += 2
        self.vue.AfficheVide(commentaire)

    def EveilDeRunes(self):
        commentaire = ("L'ennemi lance un set de runes qui retombent mollement sur le sol.\nSeule une rune est retournée .")
        self.vue.AfficheEveilDeRunes(commentaire)
        nombre_aleatoire = random.randint(1,4)
        if nombre_aleatoire ==  1:
            commentaire = ("-=[EMET: LA VERITEE]=-\nDes images incompréhensibles vous rentrent dans l'esprit, vous rendant confus et déconcentré pendant 2 tours !")
            self.modele.est_maudit_par_les_items = True
            self.modele.est_maudit_par_les_items_nombre_tour += 3
            self.modele.est_maudit_par_le_mana = True
            self.modele.est_maudit_par_le_mana_nombre_tour += 3
        elif nombre_aleatoire ==  2:
            degat = 8 + self.modele.monstre_level
            degat = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat)
            degat = self.EnleveVieAuJoueur(degat)
            commentaire = (f"-=[MET: LA MORT]=-\nUne douleur atroce vous tord les boyaux, et vous commencez a cracher du sang.\nVous perdez {degat} points de vie !")
        elif nombre_aleatoire ==  3:
            nombre_tour = 4
            
            commentaire = (f"-=[SH: LE FEU]=-\nVous vous enflammez instantanément pendant {nombre_tour - 1} tours !")
            self.AppliqueEffetElementaireSurJoueur("feu", nombre_tour, 5)
        elif nombre_aleatoire ==  4:
            commentaire = ("-=[HKHEYM : LA VIE]=-\nL'ennemi et vous reprenez tous deux quelques points de vie !")
            pourcentage = 10
            soin_joueur = round(self.modele.points_de_vie_max * (pourcentage/100))
            soin_monstre = round(self.modele.monstre_points_de_vie_max * (pourcentage/100))
            self.modele.points_de_vie += soin_joueur
            self.modele.monstre_points_de_vie += soin_monstre
            self.EquilibragePointsDeVieEtManaEtEndurance()
        self.vue.AfficheEveilDeRunes(commentaire)

    def Lamentations(self):
        commentaire = "L'ennemi lance le sort Lamentations !\nUne puissante vague d'émotions basées sur les experiences négatives du lanceur vous assaille !"
        commentaire_2 = ("Vous vous laissez à moitié emporter par le désespoir, et êtes obligés de vous lacérer la jambe pour revenir a la réalitée.\nMais les"
                         " images de guerre et de compagnons perdus, elles, restent.\nVous allez devoir apprendre a vivre avec.")
        degat = round(self.modele.points_de_vie_max * 0.1)
        degat = self.EnleveVieAuJoueur(degat)
        self.CheckePuisAppliqueTransmutation(degat)
        commentaire_3 = (f"Pour l'instant, vous perdez {degat} points de vie et devenez déconcentré pendant 4 tours ! ")
        self.modele.est_maudit_par_le_mana = True
        self.modele.est_maudit_par_le_mana_nombre_tour += 5
        self.vue.AfficheLamentations(commentaire, commentaire_2, commentaire_3)
        if self.modele.commentaire_transmutation_degat != "":
            self.vue.AfficheTransmutationDegat(self.modele.commentaire_transmutation_degat)

    def InvoquationCanope(self):
        chance_de_toucher = 90
        chance_de_toucher -= self.modele.CHANCEBONUSESQUIVE
        nombre_aleatoire = random.randint(1, 4)
        commentaire_description = "L'ennemi invoque des vases canopes qui se mettent a tourner autour de lui."
        if nombre_aleatoire == 1:
            commentaire_vase = ("Le vase canope a tête humaine s'approche de vous et une voix résonne dans votre tête :"
                                "\n -=[QUE TON FOIE SOIT DOULOUREUX, PAR ISIS !]=- ")
            nombre_aleatoire = random.randint(1,100)
            if nombre_aleatoire > chance_de_toucher :
                commentaire_effet = self.ConstructionCommentaireVaseCanopeEchec()                
            else:
                degat = 11 + self.modele.monstre_level
                degat = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat)
                degat = self.EnleveVieAuJoueur(degat)
                commentaire_effet = ("Vous ressentez une immense douleur au foie, qui vous fait perdre le controle de votre corps."
                               f"\nVous perdez {degat} points de vie et devenez blessé pendant 2 tours!")
                self.modele.est_maudit_par_la_vie = True
                self.modele.est_maudit_par_la_vie_nombre_tour += 3
        elif nombre_aleatoire == 2:
            commentaire_vase = ("Le vase canope a tête de babouin s'approche de vous et une voix résonne dans votre tête :"
                                "\n -=[QUE TES POUMONS S'ENFLAMMENT, PAR NEPHTYS !]=- ")
            nombre_aleatoire = random.randint(1,100)
            if nombre_aleatoire > chance_de_toucher :
                commentaire_effet = self.ConstructionCommentaireVaseCanopeEchec()
            else:
                nombre_tour = 4
                
                commentaire_effet = ("Apparement les anciennes déesses connaisent pas le sens figuré, parce que vous vous embrasez sur place !"
                        f"\nVous brulez pendant {nombre_tour - 1} tours!")
                self.AppliqueEffetElementaireSurJoueur("feu", nombre_tour, 5)
        elif nombre_aleatoire == 3:
            commentaire_vase = ("Le vase canope a tête de faucon s'approche de vous et une voix résonne dans votre tête :"
                                "\n -=[QUE TES TRIPES SE TORDENT, PAR SELKET !]=- ")
            nombre_aleatoire = random.randint(1,100)
            if nombre_aleatoire > chance_de_toucher :
                commentaire_effet = self.ConstructionCommentaireVaseCanopeEchec()
            else:

                commentaire_effet = ("Vous sentez une douleur lancinante dans vos intestins. la douleur est telle que vous avez du mal a vous concentrer."
                        "\nVous devenez confus et déconcentré pendant 3 tours!")
                self.modele.est_maudit_par_les_items = True
                self.modele.est_maudit_par_les_items_nombre_tour += 4
                self.modele.est_maudit_par_le_mana = True
                self.modele.est_maudit_par_le_mana_nombre_tour += 4
        elif nombre_aleatoire == 4:
            commentaire_vase = ("Le vase canope a tête de chacal s'approche de vous et une voix résonne dans votre tête :"
                                "\n -=[QUE TON ESTOMAC SE DECHIRE, PAR NEITH !]=- ")
            nombre_aleatoire = random.randint(1,100)
            if nombre_aleatoire > chance_de_toucher :
                commentaire_effet = self.ConstructionCommentaireVaseCanopeEchec()                
            else:
                degat = 8 + self.modele.monstre_level
                degat = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat)
                degat = self.EnleveVieAuJoueur(degat)
                commentaire_effet = ("Vous sentez une brulure étrange, puis une douleur horrible vous déchirer l'abdomen."
                                    f"\nVous perdez {degat} points de vie et devenez instable pendant 2 tours!")
                self.modele.est_maudit_par_les_techniques = True
                self.modele.est_maudit_par_les_techniques_nombre_tour += 3
        self.vue.AfficheInvoquationCanope(commentaire_description, commentaire_vase, commentaire_effet)

    def ConstructionCommentaireVaseCanopeEchec(self):
        commentaire = "Sauf que lancer des anciennes malédictions egyptiennes c'est rigolo mais c'est compliqué, et les vases s'écrasent sur le sol.\n"
        commentaire += "Des lettres de sang apparaissent sur le corps de l'ennemi :\n*Maudit soit celui qui use de ma puissance ; il recevra le feu, l’eau et la peste.*"
        degat = round(self.modele.monstre_points_de_vie_max*0.05)
        self.modele.monstre_points_de_vie -= degat
        commentaire += f"\n \nL'ennemi perd {degat} points de vie, se retrouve gelé et brulé pendant 2 tours !"
        self.modele.monstre_est_gele = True
        self.modele.monstre_est_gele_nombre_tour += 3
        self.modele.monstre_est_en_feu = True
        self.modele.monstre_est_en_feu_degat = 5
        self.modele.monstre_est_en_feu_nombre_tour += 3
        return commentaire

    def MagieNoire(self):
        commentaire = ("L'ennemi invoque la puissance de figures noires, cachées, oubliées, interdites,"
                       " qui dansent de sombres rituels entre la lumière des flammes et les ombres de coeurs corrompus.")
        chance_de_toucher = 85
        chance_de_toucher -= self.modele.CHANCEBONUSESQUIVE
        nombre_aleatoire = random.randint(0, 100)
        self.vue.AfficheDebutMagieNoire(commentaire)
        if nombre_aleatoire < chance_de_toucher :
            commentaire = ("Vous sentez votre esprit partir dans les pénombres emplies de souillures, cachées dans les recoins"
                           " de la noosphere...\n...et quelque chose tenter de prendre votre place.")
            degat = 12 + self.modele.monstre_level
            degat = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat)
            degat = self.EnleveVieAuJoueur(degat)
            commentaire_effet = ("Vous reprenez vos esprits quelques"
                                 " secondes plus tard, les mains sur la poignée de votre propre arme"
                                 ", plantée dans votre propre bras.\nVous perdez "
                                 f"{degat} points de vie et devenez déconcentré pendant 4 tours !")
            self.modele.est_maudit_par_le_mana = True
            self.modele.est_maudit_par_le_mana_nombre_tour += 5
        else:
            commentaire = ("Mais vous résistez a l'envahisseur terrifiant...")
            if self.modele.points_de_mana in [0, 1]:
                commentaire_effet = ("...au prix de quelques points de vie.")
                self.EnleveVieAuJoueur(2)
            else:
                commentaire_effet = ("...au prix de quelques points de mana.")
                self.modele.points_de_mana -= 2
        self.vue.AfficheMagieNoire(commentaire, commentaire_effet)

    def MagieTenebreuse(self):
        commentaire = ("L'ennemi invoque la puissance de fantômes anciens, emprisonnés, marqués par les ténébres,"
                       " qui hurlent dans le vide des chants de folie à la frontière entre le plan astral et l'abysse éternel.")
        chance_de_toucher = 85
        chance_de_toucher -= self.modele.CHANCEBONUSESQUIVE
        nombre_aleatoire = random.randint(0, 100)
        self.vue.AfficheDebutMagieNoire(commentaire)
        if nombre_aleatoire < chance_de_toucher :
            commentaire = ("Vous sentez votre esprit partir dans les cages de concepts métaphysiques, pendues au dessus des royaumes frissonnants de la mort,"
                           " creusées dans les os et la chair des hurleurs dogmatiques ...\n...et quelque chose tenter de prendre votre place.")
            commentaire_effet = ("Votre esprit est tordu par les mains pales "
                                 "de créations lovecraftiennes et "
                                 "tentaculaires.\nVous devenez instable et déconcentré pendant 2 tours !")
            self.modele.est_maudit_par_les_sorts = True
            self.modele.est_maudit_par_les_sorts_nombre_tour += 3
            self.modele.est_maudit_par_les_techniques = True
            self.modele.est_maudit_par_les_techniques_nombre_tour += 3
        else:
            commentaire = ("Mais vous résistez a l'envahisseur astral...")
            if self.modele.points_de_mana in [0, 1, 2, 3, 4]:
                commentaire_effet = ("...au prix de quelques points de vie.")
                self.EnleveVieAuJoueur(5)
            else:
                commentaire_effet = ("...au prix de quelques points de mana.")
                self.modele.points_de_mana -= 5
        self.vue.AfficheMagieNoire(commentaire, commentaire_effet)

    def MagieAbyssale(self):
        commentaire = ("L'ennemi invoque la puissance d'entitées inconcevables, en plein sommeil, bercées par les clapotis du sang"
                       " sur la neige et les flammes de brasiers sépulcraux. Leurs berceaux de pus et de logique se balancant au grès d'un vent fantôme.")
        chance_de_toucher = 55
        chance_de_toucher -= self.modele.CHANCEBONUSESQUIVE
        nombre_aleatoire = random.randint(0, 100)
        self.vue.AfficheDebutMagieNoire(commentaire)
        if nombre_aleatoire < chance_de_toucher :
            commentaire = ("Vous sentez votre esprit fondre, se reformer en un vaisseau pouvant accueillir la conscience de ces créateurs"
                           " venant de temps immémoriels. L'horizon se transforme en un enchainement de lignes oranges, bleues, jaunes, définissant avec"
                           " grande précision votre monde et les évènements qui s'y produisent...\n...et c'est si be-[ERREUR: CONNECTION AVEC HOTE EN DANGER]")
            mana_perdu = round(self.modele.points_de_mana_max * 0.3)
            self.modele.points_de_mana -= mana_perdu
            self.EquilibragePointsDeVieEtManaEtEndurance()
            commentaire_effet = ("[NETTOYAGE DU CACHE EN COURS...]\n[NETTOYAGE TERMINE]\n \n"
                                 "[RECONNECTION EN COURS..]\n \n \n \nVous ouvrez les yeux et regardez l'ennemi surpris.\n"
                                 f"Attendez...Tour [{self.modele.nombre_de_tours}] ? Ca n'est pas possible... vous etiez"
                                 f" au Tour [{self.modele.nombre_de_tours-1}] a l'instant, entrain de vous demander ce que vous alliez faire ! "
                                 "\nL'experience déconcertante vous rend instable et déconcentré pendant 2 tours.\nDe plus,"
                                 f"vous perdez {mana_perdu} points de mana !")
            self.modele.est_maudit_par_les_sorts = True
            self.modele.est_maudit_par_les_sorts_nombre_tour += 3
            self.modele.est_maudit_par_les_techniques = True
            self.modele.est_maudit_par_les_techniques_nombre_tour += 3
        else:
            commentaire = ("Mais vous résistez a l'envahisseur innomable...")
            if 0 <= self.modele.points_de_mana <= 9:
                commentaire_effet = ("...au prix de quelques points de vie.")
                self.EnleveVieAuJoueur(10)
            else:
                commentaire_effet = ("...au prix de quelques points de mana.")
                self.modele.points_de_mana -= 10
        self.vue.AfficheMagieNoire(commentaire, commentaire_effet)

    def SortUltime(self):
        commentaire = "L'ennemi lance le [Sort Ultime] !"
        commentaire += ("\nLes runes inscrites sur son armure dorée s'activent et rassemblent"
                       " une quantité ultime de mana au creux de la main de l'ennemi, lorsque"
                       " soudainement...")
        chance_de_toucher = 85
        chance_de_toucher -= self.modele.CHANCEBONUSESQUIVE
        nombre_aleatoire = random.randint(0, 100)
        self.vue.AfficheSortUltime(commentaire)
        if nombre_aleatoire < chance_de_toucher :
            commentaire_effet = ("...une gigantesque boule de feu bleue sort de sa paume et vient s'écraser sur vous !")
            vie_perdue = 20 + self.modele.monstre_level
            vie_perdue = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(vie_perdue)
            vie_perdue = self.EnleveVieAuJoueur(vie_perdue)
            self.CheckePuisAppliqueTransmutation(vie_perdue)
            mana_perdu = round(self.modele.points_de_mana_max*0.2)
            self.modele.points_de_mana -= mana_perdu
            self.EquilibragePointsDeVieEtManaEtEndurance()
            commentaire_effet += (f"\nVous perdez {vie_perdue} points de vie a cause de l'impact,"
                                 f" et vous perdez {mana_perdu} point de mana car votre âme "
                                 "souffre de la chaleur de ce feu mysterieux !")
        else:
            mana_gagne = round(self.modele.points_de_mana_max*0.2)
            self.RecouvrementDeMana(mana_gagne)
            self.EquilibragePointsDeVieEtManaEtEndurance()
            commentaire_effet = ("...l'ennemi sert le poing.\nLe mana accumulé n'a alors plus de sortie possible et se répend dans la salle.\nVous voyez"
                                 " l'ennemi regarder avec confusion la paume de sa main, puis se plaindre de la"
                                 " trahison d'une personne que vous ne voyez pas.\nCepandant, le mana dans la salle vous permet de recharger un peu vos propres réserves.")
            commentaire_effet += f"\nVous regagnez {mana_gagne} points de mana !"
            if "Tiare de Suie" in self.modele.liste_dartefacts_optionels:
                    commentaire_effet += "\nL'artefact [Tiare de Suie] bénit votre échappée !"
                    self.modele.beni_par_feu_sacre = True
                    self.modele.beni_par_feu_sacre_nombre_tour += 2
        self.vue.AfficheSortUltime(commentaire_effet)
        if self.modele.commentaire_transmutation_degat != "":
            self.vue.AfficheTransmutationDegat(self.modele.commentaire_transmutation_degat)

    def Tournicotons(self):
        liste_de_direction = []
        liste_de_direction_possibles = ["Haut", "Droite", "Bas", "Gauche"]
        commentaire = ("Tournicotons ! Tournicotons !\nL'ennemi tourne sur"
                       " lui même et fait apparaitre des vagues de feu qui semblent"
                       " se déplacer selon les mouvements de ses doigts et fait s'évaporer une partie de vos sorts de protections.\nVous voyez"
                       " les vagues faire des mouvements précis, mais sans aller vers vous...")
        self.vue.AfficheTournicotons(commentaire)
        for numero_de_la_direction in range(0, 6):
            nombre_aleatoire = random.randint(1, 4)
            direction_a_afficher = liste_de_direction_possibles[nombre_aleatoire - 1]
            liste_de_direction.append(direction_a_afficher)
            if direction_a_afficher in ["Haut", "Bas"]:
                petit_mot = "en"
            else :
                petit_mot = "à"
            direction_a_afficher = f"...puis {petit_mot} {liste_de_direction[numero_de_la_direction]}..."
            if numero_de_la_direction == 0:
                direction_a_afficher = f"Les vagues semblent bouger {petit_mot} {liste_de_direction[numero_de_la_direction]}..."
            self.vue.AfficheDirectionTournicotons(direction_a_afficher)
        ClearConsole()
        commentaire = "...et tout à coup, les vagues de feu se jettent sur vous !"
        self.vue.AfficheTournicotons(commentaire)
        for numero_de_la_direction_a_prendre in range(0, 6):
            while True:
                try:
                    commentaire = (f"Comment voulez vous tenter d'esquiver la vague [{numero_de_la_direction_a_prendre + 1}] ?"
                                   "\n1 - En sautant\n2 - En faisant une roulade sur la droite\n3 - En se baissant"
                                   "\n4 - En prenant appui sur un morceau de ruine pour se propulser vers la gauche")
                    numero_de_laction = self.vue.GetTournicotonsChoix(commentaire)
                    if numero_de_laction in [1, 2, 3, 4]:
                        direction_prise = liste_de_direction_possibles[numero_de_laction - 1]
                        ClearConsole()
                        break
                    ClearConsole()
                except ValueError:
                    ClearConsole()
            if direction_prise == liste_de_direction[numero_de_la_direction_a_prendre]:
                commentaire = f"Vous esquivez de justesse la vague de feu numéro [{numero_de_la_direction_a_prendre + 1}] !"
            else :
                degat = 5 + self.modele.monstre_level
                degat = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat)
                degat = self.EnleveVieAuJoueur(degat)
                commentaire = ("Des piliers de flammes sortent de toutes les directions, sauf une seule."
                               "\nMalheureusement, ce n'est pas la direction que vous avez prise."
                               f"\nLa violence du choc vous inflige {degat} points de dégâts !")
            self.vue.AfficheTournicotons(commentaire)
        commentaire = "Les vagues de flammes s'éteignent progressivement, jusqu'à disparaitre complètement dans le sol."
        self.vue.AfficheTournicotons(commentaire)

    def DragonAscendant(self):
        liste_de_direction = []
        liste_de_direction_possibles = ["Gauche", "Bas", "Droite", "Haut"]
        commentaire = ("L'ennemi invoque un dragon asiatique fait de flammes et de braises qui semble"
                       " se déplacer selon les mouvements d'une baguette de sureau et fait s'évaporer vos sorts de protection.\nVous voyez l'étrange"
                       " créature faire des mouvements amples dans toute la pièce, sans vous preter attention...")
        self.vue.AfficheDragonAscendant(commentaire)
        nombre_aleatoire = 1
        nombre_de_vague = 10
        for numero_de_la_direction in range(0, nombre_de_vague):
            nombre_aleatoire = random.randint(1, 4)
            liste_de_direction.append(liste_de_direction_possibles[nombre_aleatoire - 1])
            direction_a_afficher = liste_de_direction[numero_de_la_direction]
            if direction_a_afficher in ["Haut", "Bas"]:
                petit_mot = "en"
            else :
                petit_mot = "à"
            direction_a_afficher = f"...puis {petit_mot} {liste_de_direction[numero_de_la_direction]}..."
            if numero_de_la_direction == 0:
                direction_a_afficher = f"Le dragon vole tranquillement {petit_mot} {liste_de_direction[numero_de_la_direction]}..."
            if nombre_aleatoire == 0:
                direction_a_afficher = "...puis vous le perdez de vue derrière un pilier..."
            nombre_aleatoire = random.randint(0, 10)
            self.vue.AfficheDirectionDragonAscendant(direction_a_afficher)
        ClearConsole()
        commentaire = "...et soudainement, l'horrible brasier vivant se jette sur vous !"
        self.vue.AfficheDragonAscendant(commentaire)
        for numero_de_la_direction_a_prendre in range(0, nombre_de_vague):
            while True:
                try:
                    commentaire = (f"Comment voulez vous tenter d'esquiver l'attaque [{numero_de_la_direction_a_prendre + 1}] du dragon ?"
                                   "\n1 - En se jettant a plat ventre pour glisser sur une flaque de sang\n2 - En se cachant dans un cratère d'explosion a gauche\n3 - En sprintant sur la droite"
                                   "\n4 - En prenant appui sur un mur derrière vous pour vous élancer dans les airs")
                    numero_de_laction = self.vue.GetDragonAscendantChoix(commentaire)
                    if numero_de_laction in [1, 2, 3, 4]:
                        direction_prise = liste_de_direction_possibles[numero_de_laction - 1]
                        ClearConsole()
                        break
                    ClearConsole()
                except ValueError:
                    ClearConsole()
            if direction_prise == liste_de_direction[numero_de_la_direction_a_prendre]:
                commentaire = f"Vous esquivez de justesse la ruée numéro [{numero_de_la_direction_a_prendre + 1}] du dragon !"
            else :
                degat = 10 + self.modele.monstre_level
                degat = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat)
                degat = self.EnleveVieAuJoueur(degat)
                commentaire = ("Des orbes de flammes bloquent 2 directions, pendant que le dragon fonce sur la troisième."
                               "\nMalheureusement, vous n'avez pas esquivé dans la bonne direction."
                               f"\nLa violence du choc et la chaleur de l'invoquation vous inflige {degat} points de dégâts !")
            self.vue.AfficheDragonAscendant(commentaire)
        commentaire = "Le dragon de flamme finit par se volatiliser dans un nuage de fumée que vous n'aviez pas vu auparavant."
        self.vue.AfficheDragonAscendant(commentaire)

    def Tournicota(self):
        commentaire = "Tournicota ! Tournicota !\nL'ennemi tourne sur lui même et fait apparaitre une boule de lumière, qu'il frappe de toute ses forces !"
        self.vue.AfficheDebutTournicota(commentaire)
        attaque_en_cours = True
        nombre_de_renvois = 0
        while attaque_en_cours:
            while True:
                try:
                    #chance de renvoyer l'orbe
                    pourcentage_de_reussite = 100
                    pourcentage_de_reussite -= (
                        nombre_de_renvois * 3
                    )
                    #chance de fuir
                    pourcentage_de_reussite_de_fuite = 75
                    pourcentage_de_reussite_de_fuite -= (
                        nombre_de_renvois * 3
                    )
                    pourcentage_de_reussite_de_fuite += (
                        self.modele.CHANCEBONUSESQUIVE
                    )
                    commentaire = ("L'Orbe s'approche de vous ! Que voulez vous faire ?"
                                   f"\n1 - Tenter de renvoyer l'orbe [{pourcentage_de_reussite}% de réussite]"
                                   f"\n2 - Tenter d'esquiver l'orbe [{pourcentage_de_reussite_de_fuite}% de réussite]")
                    choix = self.vue.GetChoixTournicota(commentaire)
                    if choix in [1, 2]:
                        ClearConsole()
                        break
                    ClearConsole()
                except ValueError:
                    ClearConsole()
            if choix == 1 :
                # renvoi orbe
                nombre_aleatoire = random.randint(0, 100)
                commentaire = "Vous tentez de renvoyer l'orbe..."
                # reussite du renvoi ?
                if nombre_aleatoire < pourcentage_de_reussite:
                    #oui
                    commentaire_reussite = ("...et réussissez !\nVous donnez un coup formidable dans"
                                            " l'orbe de lumière et celui-ci repart vers l'ennemi avec"
                                            " plus de vitesse.\nCa sera plus dur la prochaine fois")
                    nombre_de_renvois += 1
                    nombre_aleatoire = random.randint(0, 100)
                    pourcentage_de_reussite_monstre = 30
                    pourcentage_de_reussite_monstre += (
                        nombre_de_renvois * 3
                    )
                    #monstre renvoie ?
                    if nombre_aleatoire < pourcentage_de_reussite_monstre:
                        #non
                        degat = 15 + self.modele.monstre_level
                        degat += round(
                            (self.modele.DEGATBONUSATTAQUE / 100) * degat
                        )                
                        degat -= round(
                            (self.modele.BONUSREDUCTIONDEGAT / 100) * degat
                        )
                        self.modele.monstre_points_de_vie -= degat
                        commentaire_effet = ("L'ennemi voit arriver l'orbe et tente de le renvoyer, mais se le prend en plein torse a la place !"
                                             f"\nIl perd {degat} points de vie !")
                        attaque_en_cours = False
                    else:
                        #oui
                        commentaire_effet = "L'ennemi voit arriver l'orbe et le renvoie difficilement vers vous d'un revers de la main."
                        nombre_de_renvois += 1
                        self.vue.AfficheTournicota(commentaire, commentaire_reussite, commentaire_effet)
                else:
                    #non
                    commentaire_reussite = "...et échouez .\nVous ne mettez pas assez de force dans votre coup et l'orbe de lumière vient s'écraser sur votre corps."
                    degat = 15 + self.modele.monstre_level
                    degat = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat)
                    degat = self.EnleveVieAuJoueur(degat)
                    self.CheckePuisAppliqueTransmutation(degat)
                    commentaire_effet = f"Vous devenez confus et déconcentré pendant 2 tours et perdez {degat} points de vie !"
                    self.modele.est_maudit_par_les_items = True
                    self.modele.est_maudit_par_les_items_nombre_tour += 3
                    self.modele.est_maudit_par_le_mana = True
                    self.modele.est_maudit_par_le_mana_nombre_tour += 3
                    attaque_en_cours = False
            else:
                #esquive orbe
                commentaire = "Vous tentez d'esquiver l'orbe..."
                nombre_aleatoire = random.randint(0, 100)
                #senfui ?
                if nombre_aleatoire < pourcentage_de_reussite_de_fuite:
                    #oui
                    commentaire_reussite = "...et réussissez à échapper à la boule de lumière !"
                    commentaire_effet = ("Mais l'ennemi n'est pas content de vous voir gacher comme ça ses efforts"
                                         " pour mettre en place une attaque intéractive, et il fait disparaitre "
                                         "quelques golds de votre poche !")
                    self.modele.nombre_de_gold -= 5
                    self.EquilibrageGold()
                    attaque_en_cours = False
                else:
                    #non
                    commentaire_reussite = "...mais c'était trop tard.\nL'orbe de lumière vient s'écraser sur un bout de votre pied qui était resté là."
                    degat = 5 + self.modele.monstre_level
                    degat = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat)
                    degat = self.EnleveVieAuJoueur(degat)
                    self.CheckePuisAppliqueTransmutation(degat)
                    commentaire_effet = f"Vous devenez confus et déconcentré pendant 2 tours et perdez {degat} points de vie !"
                    self.modele.est_maudit_par_les_items = True
                    self.modele.est_maudit_par_les_items_nombre_tour += 3
                    self.modele.est_maudit_par_le_mana = True
                    self.modele.est_maudit_par_le_mana_nombre_tour += 3
                    attaque_en_cours = False
        self.vue.AfficheTournicota(commentaire, commentaire_reussite, commentaire_effet)
        if self.modele.commentaire_transmutation_degat != "":
            self.vue.AfficheTransmutationDegat(self.modele.commentaire_transmutation_degat)

    def Tournicotez(self):
        commentaire = ("Tournicotez ! Tournicotez ! L'ennemi tourne sur lui même et fait apparaitre des lettres dans les airs !")
        self.vue.AfficheTournicotez(commentaire)
        while True :
            try:
                commentaire = ("UN QUIZZ ! QUIZZ QUIZZ QUIZZ !\nJAI DEMANDE-MANDE A"
                               " ALFRED DE ME PREPARRER QUELQUES QUESTIONS MAIS IL A"
                               " TENTE DE ME TUER-UER !\nCETAIT VRAIMENT MECHANT-CHANT"
                               " DE SA PART ALORS TU N'AURA PAS DE QUIZZ !"
                               " MAIS TU VA CHOISIR-SIR !\nJE TE FAIT QUOI ? QUOI QUOI QUOI QUOI ?\n"
                               "DIS MOI LE NUMERO-MERO DE CE QUE TU PREFERE-FERE !"
                               "\n1 - JE VAIS TE FAIRE MAAAAAAL !"
                               "\n2 - JE VAIS TE FAIRE PEEEEUUUR !"
                               "\n3 - JE VAIS TE VOOOOLER !"
                               "\n4 - JE VAIS TE PRENDRE UN BOOOOUT DE TON AME !")
                choix = self.vue.GetChoixTournicotez(commentaire)
                ClearConsole()
                if choix in [1, 2, 3, 4]:
                    break
            except ValueError:
                ClearConsole()
        if choix == 1:
            saignee = round(self.modele.points_de_vie_max * 0.2)
            saignee = self.EnleveVieAuJoueur(saignee)
            self.modele.monstre_points_de_vie += saignee
            self.EquilibragePointsDeVieEtManaEtEndurance()
            commentaire = ("Votre sang sort par vos narines, et forme une boule qui est aussitôt absorbée par l'ennemi."
                           f"\nVous vous faites drainer {saignee} points de vie !")
        elif choix == 2:
            mana_perdu = round(self.modele.points_de_mana_max * 0.25)
            self.modele.points_de_mana -= mana_perdu
            self.EquilibragePointsDeVieEtManaEtEndurance()
            commentaire = ("Votre esprit se relache au dela de ce qui est possible, et vous perdez le controle sur votre réserve de mana."
                           f"\nVous perdez {mana_perdu} points de mana !")
        elif choix == 3:
            gold_perdu = round(self.modele.nombre_de_gold * 0.1)
            if self.modele.nombre_de_gold > 0 :
                self.modele.nombre_de_gold -= gold_perdu
                commentaire = ("Vous entendez une petite musique entrainante venant de votre poche."
                            "\nAlors que vous regardez, incrédule, des petites mains et des petits pieds pousser sur vos pièces,"
                            " ces dernières sautent de votre poche et marchent d'un pas synchronisé vers un trou de souris dans le mur."
                            "\nVous les entendez siffloter le générique de votre dessin animé préféré !"
                            f"\nVous perdez {gold_perdu} golds !")
            else :
                commentaire = ("Vous entendez une petite musique entrainante venant de votre poche."
                            "\nAlors que vous regardez, incrédule, des petites mains et des petits pieds pousser sur vos boutons de manchette,,"
                            " ces derniers sautent de votre poche et marchent d'un pas synchronisé vers un trou de souris dans le mur."
                            "\nVous les entendez siffloter le générique de votre dessin animé préféré !"
                            f"\nVous perdez vos boutons de manchette !\n \n...en même temps vous n'aviez rien d'autre à perdre."
                            "\nDans un acte d'une rare gentillesse, l'ennemi vous rend vos boutons de manchette.")
        elif choix == 4:
            pourcentage_perdu = 1
            commentaire = ("Vous voyez deux compteurs apparaitre dans les airs, en dessous des mots Attaque et Sort,"
                           f"\net affichant respectivement {self.modele.taux_de_coup_critique} et {self.modele.taux_de_sort_critique}."
                           f"\nTout à coup, les nombres diminuent de {pourcentage_perdu} ."
                           f"\nVous perdez {pourcentage_perdu}% de chance de faire un sort ou un coup critique !")
            self.modele.taux_de_coup_critique -= pourcentage_perdu
            if self.modele.taux_de_coup_critique < 0:
                self.modele.taux_de_coup_critique = 0
            self.modele.taux_de_sort_critique -= pourcentage_perdu
            if self.modele.taux_de_sort_critique < 0:
                self.modele.taux_de_sort_critique = 0
        self.vue.AfficheTournicotez(commentaire)

    def TomeDeSalomon(self):
        commentaire = "L'ennemi ouvre une réplique de l'Ars Goetia !\nUne partie de votre force se retrouve scellée..."
        self.vue.AfficheTomeDeSalomon(commentaire)
        nombre_aleatoire = random.randint(1, 6)
        if nombre_aleatoire <= 6:
            mana_perdu = round(self.modele.points_de_mana_max*0.2)
            self.modele.points_de_mana -= mana_perdu
            self.EquilibragePointsDeVieEtManaEtEndurance()
            commentaire = f"Votre mana est scellé ! Vous perdez {mana_perdu} points de mana !"
        if nombre_aleatoire <= 5:
            self.modele.est_maudit_par_les_items = True
            self.modele.est_maudit_par_les_items_nombre_tour += 3
            commentaire += "\nVos items sont scellés ! Vous devenez confus pendant 2 tours !"
        if nombre_aleatoire <= 4:
            self.modele.est_maudit_par_le_mana = True
            self.modele.est_maudit_par_le_mana_nombre_tour += 3
            commentaire += "\nVotre esprit est scellé ! Vous devenez déconcentré pendant 2 tours !"
        if nombre_aleatoire <= 3:
            self.modele.est_maudit_par_les_sorts = True
            self.modele.est_maudit_par_les_sorts_nombre_tour += 3
            commentaire += "\nVotre âme est scellée ! Vous devenez muet pendant 2 tours !"
        if nombre_aleatoire <= 2:
            self.modele.est_maudit_par_la_vie = True
            self.modele.est_maudit_par_la_vie_nombre_tour += 3
            commentaire += "\nVotre vitalité est scellée ! Vous devenez blessé pendant 2 tours !"
        if nombre_aleatoire <= 1:
            self.modele.est_maudit_par_les_techniques = True
            self.modele.est_maudit_par_les_techniques_nombre_tour += 3
            commentaire += "\nVos sens sont scellés ! Vous devenez instable pendant 2 tours !"
        self.vue.AfficheTomeDeSalomon(commentaire)

    def DoPianisteResultatDerniereAttaque(self, notes_restante, reussite):
        ClearConsole()
        if not reussite:
            return False
        else:
            if notes_restante > 0:
                self.modele.points_de_vie -= notes_restante * 15
                self.vue.AfficheSonTechnique("SOUL")
                print(f"Les {notes_restante} notes restantes dans les airs vous tombent dessus et vous transpercent de toute part !\nVous perdez {notes_restante * 15} points de vie !")
                dummies = input("Appuyez sur Entrée pour continuer")
                ClearConsole()

            if self.modele.points_de_vie <= 0 :
                
                if self.modele.possede_une_fee == True :
                    self.modele.possede_une_fee = False
                    self.modele.points_de_vie = round(0.66 * self.modele.points_de_vie_max)
                    print(f"Votre Fée sort de son bocal et vous sauve la vie en soignant {round(0.66 * self.modele.points_de_vie_max)} points de vie !")
                    dummies = input("Appuyez sur Entrée pour continuer")
                    ClearConsole()
                    
                elif "Voile de Ino" in self.modele.liste_dartefacts_optionels:
                    self.modele.liste_dartefacts_optionels.remove("Voile de Ino")
                    self.modele.points_de_vie = round(0.66 * self.modele.points_de_vie_max)
                    print(f"Votre Voile se plaque sur votre visage et vous sauve la vie en soignant {round(0.66 * self.modele.points_de_vie_max)} points de vie !")
                    dummies = input("Appuyez sur Entrée pour continuer")
                    ClearConsole()

                else:
                    print("Vous mourrez.")
                    dummies = input("Appuyez sur Entrée pour continuer")
                    ClearConsole()
                    return False
                
            print("Il n'y a plus de notes dans les airs.\nVous êtes en vie !\nFinissez le boss !")
            dummies = input("Appuyez sur Entrée pour continuer")
            ClearConsole()
            return True

    def DoPianisteDerniereAttaque(self):
        
        directions_possibles = ["Haut", "Bas", "Gauche", "Droite"]
        directions = [random.choice(directions_possibles) for _ in range(20)]

        mapping = {
            "Haut": 8,
            "Bas": 2,
            "Gauche": 4,
            "Droite": 6
        }
        
        attaque_terminee_sans_mourir = True
        start_time = time.time()
        
        # File FIFO des 3 derniers coups affichés
        buffer = deque(maxlen=3)
        
        total_iterations = len(directions) + 3  # 3 tours de plus pour vider le décalage
        remaining_directions = total_iterations
        
        for i in range(total_iterations):
            affichage = ""

            # Vérif du temps
            if time.time() - start_time > 66:
                return remaining_directions, attaque_terminee_sans_mourir
                   
            # Vérif des PV
            if self.modele.points_de_vie <= 0:
                if self.modele.possede_une_fee == True :
                    self.modele.possede_une_fee = False
                    self.modele.points_de_vie = round(0.66 * self.modele.points_de_vie_max)
                    affichage += f"Votre Fée sort de son bocal et vous sauve la vie en soignant {round(0.66 * self.modele.points_de_vie_max)} points de vie !"
                    
                elif "Voile de Ino" in self.modele.liste_dartefacts_optionels:
                    self.modele.liste_dartefacts_optionels.remove("Voile de Ino")
                    self.modele.points_de_vie = round(0.66 * self.modele.points_de_vie_max)
                    affichage += f"Votre Voile se plaque sur votre visage et vous sauve la vie en soignant {round(0.66 * self.modele.points_de_vie_max)} points de vie !"

                else:
                    attaque_terminee_sans_mourir = False
                    return remaining_directions, attaque_terminee_sans_mourir
            
            
            if i < len(directions):
                # Phase d'affichage de la direction
                direction = directions[i]
                if direction == "Haut":
                    affichage += "\nLe Pianiste lève les Bras en Haut !"
                elif direction == "Bas":
                    affichage += "\nLe Pianiste baisse les Bras vers le Bas !"
                elif direction == "Gauche":
                    affichage += "\nLe Pianiste déplace ses doigts vers la Gauche !"
                elif direction == "Droite":
                    affichage += "\nLe Pianiste déplace ses doigts vers la Droite !"
                buffer.append(direction)
            else:
                # Phase finale : pas de nouvelle direction, juste le buffer
                affichage += "\n..."
            
            if len(buffer) < 3:
                # Pas encore assez d'historique → juste ENTER
                print(affichage)
                input("Appuyez sur Entrée pour continuer")
                ClearConsole()
            else:
                # On demande la direction d'il y a 3 coups
                ancienne_direction = buffer[0]
                affichage += "\nOù irez-vous ?\n"
                for dir_name, num in mapping.items():
                    affichage += f"{num} = {dir_name}  "
                
                while True:
                    try:
                        print(affichage)
                        choix = int(input("\nFaites votre choix avec les nombres : "))
                        ClearConsole()
                        if choix in mapping.values():
                            break
                    except ValueError:
                        ClearConsole()
                
                if choix == mapping[ancienne_direction]:
                    print("Vous esquivez la vague de notes !")
                else:
                    print(f"Les notes vous transpercent et infligent 15 points de dégâts !!\n"
                        f"Il aurait fallu aller vers le/la [{ancienne_direction}] !")
                    self.modele.points_de_vie -= 15
                    self.vue.AfficheSonTechnique("ICEt")
            
            remaining_directions = total_iterations - (i + 1)
        
        ClearConsole()
        print("Vous attendez, alerte, que Le Pianiste finisse son morceau...")
        attendre(66 - (time.time() - start_time))
        ClearConsole()
        return remaining_directions, attaque_terminee_sans_mourir

    def UltimeUltime(self):
        commentaire_description = ("L'ennemi se met à hurler et la salle entière se met a trembler !"
                       "\nUne aura dorée se met à l'entourer,"
                       "\nson armure prend une couleur de nacre,"
                       "\npuis il tend les bras,"
                       "\net...")
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire < 50:
            commentaire_reussite = ("..envoie un rayon d'aura qui vous traverse et inflige des dommages à l'essence même de votre être !"
                           "\nVous devenez muet pendant 3 tours !"
                           "\nVous devenez instable pendant 3 tours !")
            self.modele.est_maudit_par_les_sorts = True
            self.modele.est_maudit_par_les_sorts_nombre_tour += 4
            self.modele.est_maudit_par_les_techniques = True
            self.modele.est_maudit_par_les_techniques_nombre_tour += 4
        else:
            commentaire_reussite = ("...se met a tousser.\nVoire s'étouffer.\nL'armure reprend sa couleur,"
                           " l'aura se dissipe, et l'ennemi se met a crier d'une voix cassée ridicule sur une personne qui n'est pas la.")
        self.vue.AfficheUltimeUltime(commentaire_description, commentaire_reussite)

    def Ultima(self):
        commentaire = ("L'ennemi inspire un grand coup, puis vous regarde d'un air déterminé."
                       "\n-Je suis le Roi de tout un peuple."
                       "\n-De mes responsabilitées, je me ramène au serment fait à mes sujets, et j'en invoque sa puissance."
                       "\n \nSon expression devient glaciale. L'ennemi tend une main ouverte au dessus de votre tête."
                       "\n \n-Par décret royal, j'ordonne a ton existence...")
        self.vue.AfficheUltima(commentaire)
        commentaire = "...de cesser."
        self.vue.AfficheUltima(commentaire)
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire < 25:
            self.modele.points_de_vie = round(self.modele.points_de_vie_max * 0.05)
            liste_commentaire = [
                "Et votre existance cesse.",
                "Et votre dxistence cesse.",
                "Et votre posstance cesse.",
                "Et zdtre existaapo cesse.",
                "Et votre existance cythe.",
                "NN votre epoLtance cesse.",
                "Et vztre existNKZe cesse.",
                "Et vRRre exEetance ceOZI.",
                "lq votre exLKNDZce cesse.",
                "Et voyjz ,xistznce ceNDe.",
                "Et v8888 existazde cesse.",
                "Et votre existLo4e ce86m.",
                "Et vzdre exLMlance cesse.",
                "Et 15263 jxiszdzce cesse.",
                "Et aaaae exiszddce c515e.",
                "HE LPHEL PHELPHELP HELPH.",
                "Et vAlfd existazde cesse.",
                "Et Alfre dVousRega rdese.",
                "Et vozde eaddaddce cespe.",
                "az zd re exi555nce cesse.",
                "Et votre existance ceiie.",
                "ge votre exizdzacz c555e.",
                "Et degre existance cesse.",
                "E5 votre existazdg cevbe.",
                "Et votre izfzgance ceaae.",
                "zd vrrre gezfeance ckkke.",
                "Et vagee exntjtyre ckyge.",
                "Ea votre ex;yhnnce ceuyr.",
                "Et v485e xiithtree cgeht.",
                "zc votre exzhtance czgre.",
                "Et vozge ex8735uze cesse.",
                "zg votre pxistance cfzee.",
                "Et votre exgzqzvce cesse.",
                "Et vgzee existance cesse.",
                "Ee voaff ex     ce cesse.",
                "Et votre existance cesad.",
                "at   tre exis   e  cesse.",
                "Et vefre existance cesse.",
                "Ev voô^a exegzezce crece."
            ]
            nombre_aleatoire = 0
            nombre_de_affichage = 0
            commentaire = liste_commentaire[0]
            self.vue.AfficheDebutUltimaError(commentaire)
            while nombre_de_affichage != 100:
                commentaire = liste_commentaire[nombre_aleatoire]
                self.vue.AfficheUltimaError(commentaire)
                nombre_aleatoire = random.randint(1, (len(liste_commentaire) - 1))
                nombre_de_affichage += 1
            dir_path = DOSSIER_RESSOURCES
            chemin_du_fichier = dir_path + "\\error.txt"
            with open(chemin_du_fichier, "w") as fichier:
                fichier.write("Caracteristique|Valeur")
                fichier.write("\nerror|error")
            commentaire = ("[ERREUR : VIE DU PERSONNAGE N'EXISTE PAS]"
                           "\n[CREATION D'UNE NOUVELLE VARIABLE VIE DU PERSONNAGE]"
                           "\n[VIE DU PERSONNAGE INITIALISEE A 5% DE SA VIE MAXIMUM]")
            self.vue.AfficheUltima(commentaire)
            commentaire = ("L'ennemi vous regarde sans comprendre puis se met a maudire la faiblesse de traditions\ninutiles et du soutien inexistant de son peuple.\nSans savoir...")
            os.remove(chemin_du_fichier)
            self.vue.AfficheUltima(commentaire)
        else:
            commentaire = ("Mais rien ne se passe.\nL'ennemi se met a maudire la faiblesse de traditions inutiles et du soutient inexistant de son peuple.")
            self.vue.AfficheUltima(commentaire)

    def SystemeSupport(self):
        soin = 50
        commentaire = "L'ennemi utilise le programme [Système de Support]."
        nombre_aleatoire = random.randint(1, 100)
        if nombre_aleatoire < 50 :
            soin += random.randint(1, 25)
        commentaire_soin = (f"Des méchanismes s'activent en lui, et il reprend {soin} points de vie !")
        self.modele.monstre_points_de_vie += soin
        self.EquilibragePointsDeVieEtManaEtEndurance()
        self.vue.AfficheSystemeSupport(commentaire, commentaire_soin)

    def FlashBang(self):
        commentaire = "L'ennemi utilise le programme [FlashBang]."

        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 25:
            commentaire_degat = ("Mais le programme plante !")
            if "Tiare de Suie" in self.modele.liste_dartefacts_optionels:
                    commentaire_degat += "\nL'artefact [Tiare de Suie] bénit votre échappée !"
                    self.modele.beni_par_feu_sacre = True
                    self.modele.beni_par_feu_sacre_nombre_tour += 2
        else:
            commentaire_degat = ("Il fait sortir une ampoule qu'il allume et éteint a plusieurs reprise.\nPuis tire dans les airs sans prévenir.\n\nL'influx soudain de sons et lumière vous rend déconcentré pendant 3 tours !")
            self.modele.est_maudit_par_le_mana = True
            self.modele.est_maudit_par_le_mana_nombre_tour += 3
        self.vue.AfficheFlashBang(commentaire, commentaire_degat)

    def ProtocoleSupernova(self):
        degat_a_ennemi = round(self.modele.monstre_points_de_vie_max * 0.1)
        if self.modele.monstre_points_de_vie - degat_a_ennemi < 1:
            degat_a_ennemi = self.modele.monstre_points_de_vie - 1
        degat_a_joueur = round(self.modele.points_de_vie_max * 0.1)
        if self.modele.points_de_vie - degat_a_joueur < 1:
            degat_a_joueur = self.modele.monstre_points_de_vie - 1
        commentaire = "L'ennemi utilise le programme [Protocole Supernova]."

        commentaire_degat = (f"Il vibre, fume, puis tire un projectile ultra-rapide inesquivable qui passe a travers vos éventuelles protections !"
                            f"\nIl perd {degat_a_ennemi} points de vie, et vous inflige {degat_a_joueur} points de dégâts !")
        self.modele.monstre_points_de_vie -= degat_a_ennemi
        self.EnleveVieAuJoueur(degat_a_joueur)
        self.vue.AfficheProtocoleSupernova(commentaire, commentaire_degat)

    def LaserAntipersonnel(self):
        degat_a_joueur = round(self.modele.points_de_vie_max * 0.05)
        commentaire = "L'ennemi utilise le programme [Laser Anti-Personnel]."

        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 25:
            commentaire_degat = ("Mais le programme plante !")
            if "Tiare de Suie" in self.modele.liste_dartefacts_optionels:
                    commentaire_degat += "\nL'artefact [Tiare de Suie] bénit votre échappée !"
                    self.modele.beni_par_feu_sacre = True
                    self.modele.beni_par_feu_sacre_nombre_tour += 2
        else:
            commentaire_degat = (f"Il charge puis tire un laser qui passe a travers vos éventuelles protections !\nVous perdez {degat_a_joueur} points de vie !")
            self.EnleveVieAuJoueur(degat_a_joueur)
        self.vue.AfficheLaserAntipersonnel(commentaire, commentaire_degat)

    def Symphonie(self):
        degat_a_joueur = round(self.modele.points_de_vie_max * 0.2)
        commentaire = "L'ennemi lance une Symphonie !"

        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 50:
            commentaire_degat = ("Mais rien ne se passe.")
            if "Tiare de Suie" in self.modele.liste_dartefacts_optionels:
                    commentaire_degat += "\nL'artefact [Tiare de Suie] bénit votre échappée !"
                    self.modele.beni_par_feu_sacre = True
                    self.modele.beni_par_feu_sacre_nombre_tour += 2
        else:
            commentaire_degat = (f"Des notes magiques sortent du piano et fusent a travers l'air, vous transpercant de toute part.")
            commentaire_degat += (f"\nVous devenez gelé, enflammé et confu pendant 4 tours !")
            commentaire_degat += (f"\nDe plus, vous perdez {degat_a_joueur} points de vie !")
            self.modele.est_gele = True
            self.modele.est_gele_nombre_tour += 5
            self.modele.est_en_feu = True
            self.modele.est_en_feu_nombre_tour += 5
            self.modele.est_maudit_par_les_items = True
            self.modele.est_maudit_par_les_items_nombre_tour += 5
            self.EnleveVieAuJoueur(degat_a_joueur)
        self.vue.AfficheSymphonie(commentaire, commentaire_degat)

    def Jugement(self):
        # Les dégâts dépendent du nombre d'âmes (monstres tués), mais saturent :
        #     part des PV max = 25 % x âmes / (âmes + 20)
        # 20 âmes : 12,5 % | 30 : 15 % | 60 : 18,8 % | 100 : 20,8 % | 250 : 23,1 %.
        # Les premières âmes comptent beaucoup, les suivantes de moins en moins :
        # la part tend vers 25 % sans jamais l'atteindre. L'ancien calcul
        # (dégâts = nombre d'âmes) n'avait aucune limite.
        ames = max(0, self.modele.nombre_de_monstres_tues)
        degat = max(1, round(0.25 * self.modele.points_de_vie_max * ames / (ames + 20)))
        commentaire = "Le prince des sables invoque une balance et pose sur l'un de ses plateaux : une plume.\nPuis il tend la main vers vous..."
        nombre_aleatoire = random.randint(1, 100)
        if nombre_aleatoire < 50 :
            degat = self.EnleveVieAuJoueur(degat)
            commentaire_degat = ("...et recupere une boule blanche qui sort rapidement de votre torse."
                                 "\nIl le pose sur la balance, et pour chaque millimetres que le plateau descend, vous sentez une grande douleur."
                                 f"\nVous perdez {degat} points de vie !")
        else:
            commentaire_degat = "...mais vous courrez vers la balance et la tranchez d'un coup sec avant que quoi que ce soit ne se passe."
        self.vue.AfficheJugement(commentaire, commentaire_degat)

    def DurcissementArgilite(self):
        gain_de_points_de_defence = 6
        commentaire = "L'ennemi rassemble l'argile en dessous des dalles pour se faire une carapace solide !"
        commentaire_effet = f"Il gagne {gain_de_points_de_defence} points de défence pendant 3 tours !"
        self.vue.AfficheDurcissementArgilite(commentaire, commentaire_effet)
        self.modele.monstre_gain_de_defence = True
        self.modele.monstre_gain_de_defence_nombre = gain_de_points_de_defence
        self.modele.monstre_gain_de_defence_nombre_tour += 4

    def DurcissementCalcaire(self):
        gain_de_points_de_defence = 18
        commentaire = "L'ennemi rassemble le calcaire contenu dans les murs de la salle se faire une carapace solide !"
        commentaire_effet = f"Il gagne {gain_de_points_de_defence} points de défence pendant 3 tours !"
        self.vue.AfficheDurcissementCalcaire(commentaire, commentaire_effet)
        self.modele.monstre_gain_de_defence = True
        self.modele.monstre_gain_de_defence_nombre = gain_de_points_de_defence
        self.modele.monstre_gain_de_defence_nombre_tour += 4

    def PanaceeUniverselle(self):
        commentaire = "L'ennemi avale un fruit étrange à peau rouge, de la taille/forme d'une orange, mais avec une chair jauneâtre ."
        commentaire_effet = "Une aura bleue l'entoure, et..."
        if self.modele.monstre_est_en_feu:
            self.modele.monstre_est_en_feu = False
            self.modele.monstre_est_en_feu_nombre_tour = 0
            self.modele.monstre_est_en_feu_degat = 0
            commentaire_effet += "\n     ...il s'arrête immédiatement de bruler !"
        if self.modele.monstre_est_gele:
            self.modele.monstre_est_gele = False
            self.modele.monstre_est_gele_nombre_tour = 0
            commentaire_effet += "\n     ...il dégèle instantanément !"
        if self.modele.monstre_est_en_feu:
            self.modele.monstre_est_vulnerable = False
            self.modele.monstre_est_vulnerable_nombre_tour = 0
            self.modele.monstre_niveau_de_vulnerabilite = 0
            commentaire_effet += "\n     ...il n'est plus vulnérable !"
        if self.modele.monstre_est_en_feu:
            self.modele.monstre_est_empoisonne = False
            self.modele.monstre_est_empoisonne_nombre_tour = 0
            self.modele.monstre_est_empoisonne_degat = 0
            commentaire_effet += "\n     ...il est soigné de son poison !"
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire < 55:
            gain_de_vie = round(self.modele.monstre_points_de_vie_max*0.2)
            self.modele.monstre_points_de_vie += gain_de_vie
            self.EquilibragePointsDeVieEtManaEtEndurance()
            commentaire_effet += f"\n     ...il reprend {gain_de_vie} points de vie !"
        if commentaire_effet == "Une aura bleue l'entoure, et...":
            commentaire_effet = "Mais rien ne se passe !"
        self.vue.AffichePanaceeUniverselle(commentaire, commentaire_effet)

    def Envol(self):
        commentaire = "L'ennemi s'élance dans les airs.\nIl sera beaucoup plus difficile a toucher maintenant !"
        commentaire_effet = f"Vous perdez 30% de chance de reussir une attaque ou un sort pendant 3 tours !"
        self.vue.AfficheEnvol(commentaire, commentaire_effet)
        self.modele.monstre_est_envol = True
        self.modele.monstre_est_envol_nombre_tour = 4

    def Hurlement(self):
        commentaire = "L'ennemi lance un hurlement à glacer le sang !"
        nombre_aleatoire = random.randint(1, 3)
        if nombre_aleatoire == 1:
            commentaire_effet = "La peur vous fait trembler comme une feuille.\nVous devenez instable pendant 4 tours !"
            self.modele.est_maudit_par_les_techniques = True
            self.modele.est_maudit_par_les_techniques_nombre_tour += 5
        elif nombre_aleatoire == 2:
            commentaire_effet = "La peur vous envahit l'esprit.\nVous devenez déconcentré pendant 4 tours !"
            self.modele.est_maudit_par_le_mana = True
            self.modele.est_maudit_par_le_mana_nombre_tour += 5
        else :
            commentaire_effet = "Mais vous arrivez à résister à la peur qui tente désespérément de s'accrocher a vous !"
        self.vue.AfficheHurlement(commentaire, commentaire_effet)

    def AttireGold(self):
        commentaire = ("L'ennemi utilise la technique Attire-Gold !\nIl fait de grands gestes faisant penser"
                       " a un spectacle de geisha et utilise l'aura et les flux d'énergie magique généré par ces techniques ancestrales pour..."
                       "\n \n \nEuh...\n \n \nNon enfaite il sort juste un gros aimant de sa poche, sur lequel est collé l'étiquette *GOLD*.")
        if self.modele.nombre_de_gold > 0:
            chance_de_reussite = 50
            nombre_aleatoire = random.randint(0, 100)
            if nombre_aleatoire < chance_de_reussite:
                nombre_gold_perdu = round(self.modele.nombre_de_gold * 0.20)
                self.modele.nombre_de_gold -= nombre_gold_perdu
                commentaire_reussite = f"{nombre_gold_perdu} golds traversent votre poche pour venir se coller à l'aimant.\n \nCharmant."
            else:
                commentaire_reussite = ("Vous sentez vos golds commencer à bouger et sortez calmement un plus gros aimant pour les maintenir en place.\n \nPourquoi pas.")
            self.EquilibrageGold()
        else:
            commentaire_reussite = ("Vous regardez l'ennemi avec le sourire satisfait et le haussement de sourcil rapide de celui qui à tout"
                                    " dépensé et n'a plus d'argent à se faire voler.\nVous vous sentez fier, même si vous ne le devriez pas.\n \nEn rétaliation, il "
                                    "vous envoie une enclume sur le coin de la tête.\nVous vous sentez confus maintenant.\nPendant 10 tours.\n \nEt puis quoi encore !")
            self.modele.est_maudit_par_les_items = True
            self.modele.est_maudit_par_les_items_nombre_tour += 11
        self.vue.AfficheAttireGold(commentaire, commentaire_reussite)

    def CoupAntiMagie(self):
        commentaire = ("L'ennemi vous envoie une pierre dessus.\n"
        "Des runes anciennes gravées a l'interieur se mettent a scintiller"
        " et désactivent vos sorts de protection !"
        "\nPuis il tente de vous poignarder...")
        
        nombre_aleatoire = random.randint(0, 100)
        chance_de_toucher = 80
        chance_de_toucher -= self.modele.CHANCEBONUSESQUIVE
        if nombre_aleatoire < chance_de_toucher:
            self.modele.utilise_brume_sang = False
            self.modele.brume_sang_nombre_tours = 0
            self.modele.utilise_mirroir_eau = False
            self.modele.mirroir_eau_nombre_tours = 0
            degat = 20 + self.modele.monstre_level
            degat = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat)
            degat = self.EnleveVieAuJoueur(degat)
            commentaire_effet = f"..et vous taillade profondément le côté !\nVous perdez {degat} points de vie et devenez blessé pendant 3 tours !"
            self.modele.est_maudit_par_la_vie = True
            self.modele.est_maudit_par_la_vie_nombre_tour = 4
        else:
            commentaire_effet = "Mais vous renvoyez la pierre en direction de l'ennemi,\nqui fait un bond en arrière pour esquiver, et abandonne alors son attaque."
        self.vue.AfficheCoupAntiMagie(commentaire, commentaire_effet)

    def AttireMagie(self):
        commentaire = ("L'ennemi utilise la technique Attire-Magie !\nIl se met a effectuer une dance esotérique"
                       " concentrant les énergies de l'univers et de la destinée sur le bout de ses doigts pour..."
                       "\n \n \nEuh...\n \n \nNon enfaite il sort juste un gros aimant de sa poche.\nL'étiquette *GOLD* est recouverte du mot *MANA* écrit au feutre noir.")
        if self.modele.points_de_mana > 0:
            chance_de_reussite = 60
            nombre_aleatoire = random.randint(0, 100)
            if nombre_aleatoire < chance_de_reussite:
                nombre_mana_perdu = round(self.modele.points_de_mana_max * 0.20)
                self.modele.points_de_mana -= nombre_mana_perdu
                commentaire_reussite = f"{nombre_mana_perdu} boules unitaires de mana traversent votre torse pour venir se coller à l'aimant.\n \nCharmant."
            else:
                commentaire_reussite = ("Vous sentez votre mana s'agiter dans votre réserve et sortez calmement un plus gros aimant pour le maintenir en place.\n \nPourquoi pas.")
            self.EquilibragePointsDeVieEtManaEtEndurance()
        else:
            commentaire_reussite = ("Vous regardez l'ennemi avec le sourire satisfait et le haussement de sourcil rapide de celui qui à tout"
                                    " dépensé dans des sorts ratés et n'a plus de mana a se faire voler.\nVous vous sentez fier, même si vous ne le devriez pas.\n \nEn rétaliation, il "
                                    "vous envoie une enclume sur le coin de la tête.\nVous vous sentez confus maintenant.\nPendant 10 tours.\n \nEt puis quoi encore !")
            self.modele.est_maudit_par_les_items = True
            self.modele.est_maudit_par_les_items_nombre_tour += 11
        self.vue.AfficheAttireMana(commentaire, commentaire_reussite)

    def Aspiration(self):
        #prend gold, mana + vie, manamax + viemax, taux critique sort+ attaque, force + intelligence, defence
        commentaire = "L'ennemi active un mécanisme implanté dans son corps et commence à aspirer votre essence..."
        self.vue.AfficheAspiration(commentaire)
        nombre_aleatoire = random.randint(1, 16)
        if nombre_aleatoire <= 16:
            gold_perdu = round(self.modele.nombre_de_gold*0.05) + 1
            if self.modele.nombre_de_gold == 0:
                gold_perdu = 0
            self.modele.nombre_de_gold -= gold_perdu
            commentaire = f"{gold_perdu} gold sont aspirés par la bouche béante !"
            self.EquilibrageGold()
            self.vue.AfficheAspiration(commentaire)
        if nombre_aleatoire <= 11:
            points_vie_mana_perdu = round(self.modele.points_de_mana_max*0.05) + 5
            self.modele.points_de_mana -= points_vie_mana_perdu
            points_vie_mana_perdu = self.EnleveVieAuJoueur(points_vie_mana_perdu)
            commentaire = f"{points_vie_mana_perdu} points de vie et de mana sont aspirés par la bouche béante !"
            self.EquilibragePointsDeVieEtManaEtEndurance()
            self.vue.AfficheAspiration(commentaire)
        if nombre_aleatoire <= 6:
            points_vie_mana_max_perdu = 1
            if self.modele.points_de_mana_max == 0:
                points_vie_mana_max_perdu = 0
            self.modele.points_de_vie_max -= points_vie_mana_max_perdu
            self.modele.points_de_mana_max -= points_vie_mana_max_perdu
            commentaire = f"{points_vie_mana_max_perdu} points de vie max et de mana max sont aspirés par la bouche béante !"
            self.vue.AfficheAspiration(commentaire)
        if nombre_aleatoire <= 4:
            chance_coup_sort_critique_perdu = 2
            if ((self.modele.taux_de_coup_critique == 0)
                or (self.modele.taux_de_sort_critique == 0) ):
                chance_coup_sort_critique_perdu = 0
            self.modele.taux_de_coup_critique -= chance_coup_sort_critique_perdu
            self.modele.taux_de_sort_critique -= chance_coup_sort_critique_perdu
            commentaire = f"{chance_coup_sort_critique_perdu}% de chance de faire un coup ou un sort critique sont aspirés par la bouche béante !"
            self.vue.AfficheAspiration(commentaire)
        if nombre_aleatoire <= 2:
            points_force_intelligence_perdu = 1
            if ((self.modele.points_de_force == 0)
                or (self.modele.points_de_intelligence == 0) ):
                points_force_intelligence_perdu = 0
            self.modele.points_de_force -= points_force_intelligence_perdu
            self.modele.points_de_intelligence -= points_force_intelligence_perdu
            commentaire = f"{points_force_intelligence_perdu} points de force et de intelligence sont aspirés par la bouche béante !"
            self.vue.AfficheAspiration(commentaire)
        if nombre_aleatoire <= 1:
            points_defence_perdu = 1
            if self.modele.points_de_defence == 0:
                points_defence_perdu = 0
            self.modele.points_de_defence -= points_defence_perdu
            commentaire = f"{points_defence_perdu} points de défence est aspiré par la bouche béante !"
            self.vue.AfficheAspiration(commentaire)
        degat = 32 - nombre_aleatoire*2
        if self.modele.monstre_est_gele:
            degat += round(degat*0.5)
        self.modele.monstre_points_de_vie -= degat
        commentaire = f"Le mécanisme surchauffe et s'arrête, occasionnant {degat} points de dégâts a l'ennemi !"
        self.vue.AfficheAspiration(commentaire)

    def Laser(self):
        commentaire = "L'ennemi rassemble les rayons de lumière environnant et les amplifie avant de les lacher sur vous sous forme de laser !"
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire < 60:
            degat = 20 + self.modele.monstre_level
            degat = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat)
            degat = self.EnleveVieAuJoueur(degat)
            self.CheckePuisAppliqueTransmutation(degat)
            mana_perdu = round(self.modele.points_de_mana_max*0.2)
            self.modele.points_de_mana -= mana_perdu
            self.EquilibragePointsDeVieEtManaEtEndurance()
            nombre_tour = 4
            
            commentaire_effet = ("Ce dernier carbonise la peau de votre thorax et fait bruler le mana dans votre réserve."
                                 f"\nVous perdez {degat} points de vie, {mana_perdu} points de mana, "
                                 f"et vous vous mettez a bruler pendant {nombre_tour - 1} tours !")
            self.AppliqueEffetElementaireSurJoueur("feu", 4, 5)
        else:
            commentaire_effet = ("Mais une erreur de calcul dans le traitement des rayons de lumière fait que le laser"
                           " s'éclate en ensemble chaotique de plus petits lasers qui laissent sur les murs de profonds sillages carbonisés.")
            if "Tiare de Suie" in self.modele.liste_dartefacts_optionels:
                    commentaire_effet += "\nL'artefact [Tiare de Suie] bénit votre échappée !"
                    self.modele.beni_par_feu_sacre = True
                    self.modele.beni_par_feu_sacre_nombre_tour += 2
        self.vue.AfficheLaser(commentaire, commentaire_effet)
        if self.modele.commentaire_transmutation_degat != "":
            self.vue.AfficheTransmutationDegat(self.modele.commentaire_transmutation_degat)

    def Roulette(self):
        # mise ou pas = critique ou pas. si rouge, foule d'effet sur joueur. si vert, foule d'effet sur ennemi.
        # definition de la mise
        commentaire = ("L'ennemi fait apparaitre une roulette géante en plein milieu de la salle !"
                       "\nElle est composée d'une alternance de cases rouges et vertes, et d'une bille prête à traverser"
                       " le plateau tournant a une vitesse incroyable.")
        commentaire_mise = ("Vous pouvez miser des golds sur la case ou s'arretera la bille pour activer des effets supplémentaires."
                            "\n1 - Miser 0 gold : vous inflige des dégâts quel que soit le résultat"
                            "\n2 - Miser 5 golds : redonne de la vie au gagnant"
                            "\n3 - Miser 10 golds : temps et dégât de brulure/gel x 200%"
                            "\n4 - Miser 15 golds : -15 golds au perdant, +45 golds au gagnant (mise comprise)")
        self.vue.AfficheDebutRoulette(commentaire)
        # definition de la couleur de la case
        while True:
            try:
                choix_mise = self.vue.GetRouletteChoix(commentaire_mise)
                ClearConsole()
                if choix_mise in [1, 2, 3, 4]:
                    if ((choix_mise == 2 and self.modele.nombre_de_gold < 5) or
                        (choix_mise == 3 and self.modele.nombre_de_gold < 10) or
                        (choix_mise == 4 and self.modele.nombre_de_gold < 15)):
                        self.vue.AfficheMiseImpossibleRoulette()
                    else:
                        break
            except ValueError:
                ClearConsole()
        nombre_de_tour = 1
        couleur_case = "Rouge"
        nombre_de_tour_final = random.randint(35, 42)
        while nombre_de_tour != nombre_de_tour_final:
            if couleur_case == "Rouge":
                couleur_case = "Verte"
            else:
                couleur_case = "Rouge"
            commentaire = f"La bille tombe enfin sur la roulette et se pose sur la case {couleur_case}..."
            temps = 0.008 * nombre_de_tour
            self.vue.AfficheResultatRoulette(commentaire, temps)
            nombre_de_tour += 1
        commentaire = f"La bille tombe enfin sur la roulette et se pose sur la case {couleur_case}!"
        self.vue.AfficheDebutRoulette(commentaire)
        # application des effets
        if couleur_case == "Rouge":
            nombre_tour = 4
            degat_feu = 5
            degat = 0
            if choix_mise == 1:
                degat = 15 + self.modele.monstre_level
                degat = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat)
                degat = self.EnleveVieAuJoueur(degat)
                commentaire_mise = f"Et a cause de votre mise, vous perdez {degat} points de vie !"
            elif choix_mise == 2:
                self.modele.nombre_de_gold -= 5
                vie_reprise = round(self.modele.monstre_points_de_vie_max*0.2)
                self.modele.monstre_points_de_vie += vie_reprise
                self.EquilibragePointsDeVieEtManaEtEndurance()
                commentaire_mise = f"Et a cause de votre mise, l'ennemi regagne {vie_reprise} points de vie !"
            elif choix_mise == 3:
                self.modele.nombre_de_gold -= 10
                nombre_tour += nombre_tour
                degat_feu += degat_feu
                commentaire_mise = "Et à cause de votre mise, les effets élémentaires sont bien plus potents !"
            else:
                self.modele.nombre_de_gold -= 30
                commentaire_mise = f"Et a cause de votre mise, vous perdez 15 golds supplémentaires !"
            commentaire_effet = (f"Vous gelez et vous enflammez pendant {nombre_tour} tours."
                                 f"\nVous devenez déconcentré et blessé pendant {nombre_tour} tours."
                                 "\nC'est le jeu ma pauvre lucette !")
            self.AppliqueEffetElementaireSurJoueur("glace", nombre_tour)
            
            self.AppliqueEffetElementaireSurJoueur("feu", nombre_tour, degat_feu)
            self.modele.est_maudit_par_le_mana = True
            self.modele.est_maudit_par_le_mana_nombre_tour += nombre_tour
            self.modele.est_maudit_par_la_vie = True
            self.modele.est_maudit_par_la_vie_nombre_tour += nombre_tour
        else:
            nombre_tour = 4
            degat_feu = 3
            degat = 0
            if choix_mise == 1:
                degat = 15 + self.modele.monstre_level
                degat = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat)
                degat = self.EnleveVieAuJoueur(degat)
                commentaire_mise = f"Et à cause de votre mise, vous perdez {degat} points de vie !"
            elif choix_mise == 2:
                self.modele.nombre_de_gold -= 5
                vie_reprise = round(self.modele.points_de_vie_max*0.2)
                self.modele.points_de_vie += vie_reprise
                self.EquilibragePointsDeVieEtManaEtEndurance()
                commentaire_mise = f"Et grâce à votre mise, vous regagnez {vie_reprise} points de vie !"
            elif choix_mise == 3:
                self.modele.nombre_de_gold -= 10
                nombre_tour += nombre_tour
                degat_feu += degat_feu
                commentaire_mise = "Et grâce à votre mise, les effets élémentaires sont bien plus potents !"
            else:
                self.modele.nombre_de_gold += 45
                commentaire_mise = f"JACKPOT !\nVotre mise vous est rendue et vous gagnez 30 golds supplémentaires !"
            commentaire_effet = (f"L'ennemi gele et s'enflamme pendant {nombre_tour} tours !"
                                 "\nC'est le jeu baby !")
            self.modele.monstre_est_gele = True
            self.modele.monstre_est_gele_nombre_tour += nombre_tour
            self.modele.monstre_est_en_feu = True
            self.modele.monstre_est_en_feu_nombre_tour += nombre_tour
            self.modele.monstre_est_en_feu_degat = degat_feu
        self.vue.AfficheFinRoulette(commentaire_effet, commentaire_mise)

    def JetDargent(self):
        commentaire = ("L'ennemi vous lance un gold qui traverse le mur du son, et vos éventuels sorts de protection !")
        chance_de_reussite = 70
        chance_de_reussite -= self.modele.CHANCEBONUSESQUIVE
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire < chance_de_reussite:
            degat = 20 + self.modele.monstre_level
            degat = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat)
            degat = self.EnleveVieAuJoueur(degat)
            commentaire_reussite = ("La pièce vous brise les côtes et vous envoie vous écraser a travers un mur comme un boulet de canon"
                                    " avant même que vous ne compreniez ce qui se passe !"
                                    f"\nVous perdez {degat} points de vie et devenez blessé pendant 10 tours !")
            self.modele.est_maudit_par_la_vie = True
            self.modele.est_maudit_par_la_vie_nombre_tour += 11
        else:
            commentaire_reussite = ("Vous amenez votre lame devant vous et lui faites faire une rotation à 90°."
                                    "\nLa pièce frappe de plein fouet votre lame et se fait devier vers le plafond."
                                    "\n \nVous la récuperez à sa descente et gagnez 1 gold !")
            if "Tiare de Suie" in self.modele.liste_dartefacts_optionels:
                    commentaire_reussite += "\nL'artefact [Tiare de Suie] bénit votre échappée !"
                    self.modele.beni_par_feu_sacre = True
                    self.modele.beni_par_feu_sacre_nombre_tour += 2
            self.modele.nombre_de_gold += 1
        self.vue.AfficheAttireMana(commentaire, commentaire_reussite)

    def GemmeBleue(self):
        commentaire = ("L'ennemi fait briller la gemme bleue d'une magnifique tiare !")
        chance_de_reussite = 60
        chance_de_reussite -= self.modele.CHANCEBONUSESQUIVE
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire < chance_de_reussite:
            pourcentage_aleatoire = random.randint(1,3)
            mana_perdu = round(self.modele.points_de_mana_max*(pourcentage_aleatoire/10))
            self.modele.points_de_mana -= mana_perdu
            self.EquilibragePointsDeVieEtManaEtEndurance()
            commentaire_reussite = ("Votre regard est mysterieusement attiré par la lumière étrange qui baigne maintenant la salle."
                                    "\nEn son sein, vous pouvez apercevoir un royaume au bord du déclin,"
                                    " et une femme somptueusement habillée regarder l'horizon d'un air mélancolique."
                                    "\nPuis elle tourne la tête et vous regarde."
                                    f"\n \nVous revenez à vous mais sentez que {mana_perdu} points de mana ont disparu de votre réserve !")
        else:
            commentaire_reussite = ("Vous fermez les yeux devant la lumière magique, et ne les rouvrez que lorsque la salle redevient normale.")
            if "Tiare de Suie" in self.modele.liste_dartefacts_optionels:
                    commentaire_reussite += "\nL'artefact [Tiare de Suie] bénit votre échappée !"
                    self.modele.beni_par_feu_sacre = True
                    self.modele.beni_par_feu_sacre_nombre_tour += 2
        self.vue.AfficheGemmeBleue(commentaire, commentaire_reussite)

    def ComboMiserable(self):
        chance_de_maudir = 25
        chance_denvoyer_un_coup = 80
        nombre_de_coup = 0
        nombre_de_tour_maudit = 0
        degats_finaux = 0
        commentaire = "L'ennemi commence un combo misérable ! Une aura noire entoure sa lame et il s'approche de vous !"
        self.vue.AfficheDebutComboMiserable(commentaire)
        # determine le nombre de coup infligés
        nombre_aleatoire = 0
        while nombre_aleatoire < chance_denvoyer_un_coup:
            nombre_de_coup += 1
            commentaire = f"L'ennemi envoie {nombre_de_coup} coup..."
            #ca enflamme ?
            nombre_aleatoire = random.randint(0,100)
            if nombre_aleatoire < chance_de_maudir :
                commentaire_resultat = "\n...qui vous rend muet pour 1 tour et vous inflige des dégats !"
                degat_a_ajouter = 5 + self.modele.monstre_level
                degat_a_ajouter = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat_a_ajouter)
                degats_finaux += degat_a_ajouter
                nombre_de_tour_maudit += 1
            else : 
                commentaire_resultat = "\n...que vous arrivez a esquiver !"
            #affichage
            self.vue.AfficheComboMiserable(commentaire, commentaire_resultat)
            #intialisation autre nombre aleatoire sauf si nombre coup > 10
            nombre_aleatoire = random.randint(0,100)
            if nombre_de_coup > 9:
                nombre_aleatoire = 100
        if nombre_de_tour_maudit != 0:
            self.modele.est_maudit_par_les_sorts = True
            self.modele.est_maudit_par_les_sorts_nombre_tour = nombre_de_tour_maudit + 1
            degats_finaux = self.EnleveVieAuJoueur(degats_finaux)
            commentaire = (
                "L'assaut s'arrête enfin."
                f"\nAu final, vous perdez {degats_finaux} points de vie et resterez muet pendant {nombre_de_tour_maudit} tours !"
            )
        else:
            commentaire = (
                "L'assaut s'arrête enfin."
                "\nEt vous avez tout esquivé !"
            )
        self.vue.AfficheFinComboMiserable(commentaire)

    def CrystalElementaireDore(self):
        commentaire = "L'ennemi sort un crystal élémentaire doré et vous regarde à travers."
        element_aleatoire = random.randint(1, 4)
        if element_aleatoire == 1:
            commentaire_item = "Le crystal prend une teinte rouge avant de se briser. Vous vous retrouvez enflammé pendant 4 tours !"
            nombre_tour = 5
            
            self.AppliqueEffetElementaireSurJoueur("feu", nombre_tour, 5)

        elif element_aleatoire == 2:
            commentaire_item = "Le crystal prend une teinte bleue avant de se briser. Vous vous retrouvez gelé pendant 3 tours !"
            self.AppliqueEffetElementaireSurJoueur("glace", 4)
        elif element_aleatoire == 3:
            nombre_tour = 5
            self.AppliqueEffetElementaireSurJoueur("foudre", nombre_tour)
            if self.modele.est_paralyse:
                commentaire_item = "Le crystal prend une teinte blanche avant de se briser. Vous vous retrouvez paralysé pendant 4 tour !"
            else:
                commentaire_item = "Le crystal prend une teinte blanche avant de se briser. Vous sentez la paralysie arriver, mais y résistez !"
        elif element_aleatoire == 4:
            saignee = round(self.modele.points_de_vie_max * 0.25)
            saignee = self.EnleveVieAuJoueur(saignee)
            self.modele.monstre_points_de_vie += saignee
            self.EquilibragePointsDeVieEtManaEtEndurance()
            commentaire_item = f"Le crystal prend une teinte violette avant de se briser. Vous vous faites drainer {saignee} points de vie !"
        self.vue.AfficheCrystalElementaireDore(commentaire, commentaire_item)

    def SablesDuTemps(self):
        commentaire = "L'ennemi laisse s'écouler un sable fin sur le sol... mais il disparait dans les airs."
        if self.modele.monstre_points_de_vie < self.modele.vie_du_monstre_pour_sables_du_temps_a_utiliser:
            commentaire_effet = ("Aussitôt, le temps semble se renverser pour l'ennemi."
                           "\nSes anciennes blessures se referment, ses altérations d'état sont soignées, et tout le sang"
                           "versé ces deux derniers tours retourne dans le corps de son propriétaire comme si il n'était jamais sorti.")
            self.modele.monstre_points_de_vie = self.modele.vie_du_monstre_pour_sables_du_temps_a_utiliser
            if self.modele.monstre_est_en_feu:
                self.modele.monstre_est_en_feu = False
                self.modele.monstre_est_en_feu_nombre_tour = 0
                self.modele.monstre_est_en_feu_degat = 0
            if self.modele.monstre_est_gele:
                self.modele.monstre_est_gele = False
                self.modele.monstre_est_gele_nombre_tour = 0
            if self.modele.monstre_est_vulnerable:
                self.modele.monstre_est_vulnerable = False
                self.modele.monstre_est_vulnerable_nombre_tour = 0
                self.modele.monstre_niveau_de_vulnerabilite = 0
            if self.modele.monstre_est_empoisonne:
                self.modele.monstre_est_empoisonne = False
                self.modele.monstre_est_empoisonne_nombre_tour = 0
                self.modele.monstre_est_empoisonne_degat = 0
        else:
            commentaire_effet = ("Les rouages du temps semblent s'arrêter un instant, puis reprennent leur course infinie.")
        self.vue.AfficheSablesDuTemps(commentaire, commentaire_effet)
