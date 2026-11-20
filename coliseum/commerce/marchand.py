"""Marchand du Coliseum et commerçants du village."""

import random

from coliseum import services
from coliseum import audio
from coliseum.audio import PermanentPlaySFX, PlayMusicDeLetage, PlaySound, StopAllMusic
from coliseum.commerce.materiaux import FuseMaterials
from coliseum.console import ClearConsole, attendre
from coliseum.donnees.actions import (
    LISTEACTIONRANG1,
    LISTEACTIONRANG2,
    LISTEACTIONRANG3,
    LISTEACTIONRANG4,
)
from coliseum.donnees.artefacts import LISTEEFFETSARTEFACT
from coliseum.donnees.village import (
    ANNUAIREPRIXVILLAGE,
    LISTERECETTES,
    LISTERUMEURS,
    MATERIAUXRANG1,
    MATERIAUXRANG2,
    MATERIAUXRANG3,
    MATERIAUXRANG4,
    MATERIAUXRANG5,
    MATERIAUXRANG6,
    MATERIAUXRANG7,
)
from coliseum.histoire.cigogne_blanche import EcrireDansLivreCigogneBlanche
from coliseum.joueur.benedictions import (
    RecupereBenedictionEnCours,
    RecupereMaledictionEnCours,
    RegardeSiBenedictionDisponible,
)


class TraderUsage:

    def __init__(self):
        self.modificateur = 1
        if services.Player.stigma_negatif == "Mauvaise Réputation":
            self.modificateur = 1.5
        self.modificateur += (services.Player.numero_de_letage / 10) - 0.1
        self.modificateur_badge_terni = 1
        if "Badge Terni" in services.Player.liste_dartefacts_optionels and services.Player.nombre_dennemis_a_letage == 0:
            self.modificateur_badge_terni -= 0.3
        if "Médaillon de Platine" in services.Player.liste_dartefacts_optionels:
            self.modificateur_badge_terni -= 0.3
        self.annuaire_des_prix = {
            "Feuille Jindagee": round(round(15 * self.modificateur)) * self.modificateur_badge_terni,
            "Fruit Jindagee": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,
            "Feuille Aatma": round(round(20 * self.modificateur)) * self.modificateur_badge_terni,
            "Fruit Aatma": round(round(50 * self.modificateur)) * self.modificateur_badge_terni,
            "Crystal Elémentaire": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,
            "Ambroisie": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,
            "Hydromel": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,
            "Orbe de Furie": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,
            "Orbe de Folie": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,
            "Remède": round(round(20 * self.modificateur)) * self.modificateur_badge_terni,
            "Remède Superieur": round(round(50 * self.modificateur)) * self.modificateur_badge_terni,
            "Remède Divin": round(round(100 * self.modificateur)) * self.modificateur_badge_terni,
            "Pillule": round(round(30 * self.modificateur)) * self.modificateur_badge_terni,
            "Pillule Superieure": round(round(60 * self.modificateur)) * self.modificateur_badge_terni,
            "Pillule Divine": round(round(110 * self.modificateur)) * self.modificateur_badge_terni,
            "Fléchette Rouge": round(round(20 * self.modificateur)) * self.modificateur_badge_terni,
            "Flèche Rouge": round(round(55 * self.modificateur)) * self.modificateur_badge_terni,
            "Fléchette Bleue": round(round(20 * self.modificateur)) * self.modificateur_badge_terni,
            "Flèche Bleue": round(round(55 * self.modificateur)) * self.modificateur_badge_terni,
            "Poudre Explosive": round(round(30 * self.modificateur)) * self.modificateur_badge_terni,
            "Roche Explosive": round(round(50 * self.modificateur)) * self.modificateur_badge_terni,
            "Bombe Explosive": round(round(70 * self.modificateur)) * self.modificateur_badge_terni,
            "Fiole de Poison": round(round(50 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Gourde de Poison": round(round(110 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Sève d'Absolution": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Larme d'Absolution": round(round(70 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Soluté d'Absolution": round(round(100 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Sève d'Exorcisme": round(round(20 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Larme d'Exorcisme": round(round(45 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Soluté d'Exorcisme": round(round(70 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Mutagène Bleu": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Grand Mutagène Bleu": round(round(80 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Mutagène Rouge": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Grand Mutagène Rouge": round(round(80 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Mutagène Vert": round(round(40 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Grand Mutagène Vert": round(round(80 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Mutagène Doré": round(round(90 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Grand Mutagène Doré": round(round(150 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Mutagène Hérétique": round(round(100 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Mutagène Fanatique": round(round(100 * self.modificateur)) * self.modificateur_badge_terni,  # [debutTour]
            "Red Coin": 0,
            "Tirage": 0,
            "Machette Rouillée": 150,
            "Vieille Pelle": 200,
            "Gemme de Vie": round(round(300 * self.modificateur)) * self.modificateur_badge_terni,
            "Gemme d'Esprit": round(round(300 * self.modificateur)) * self.modificateur_badge_terni,
            "Fée dans un Bocal": 0,
            "Méga Tirage": 777,
        }
        self.liste_item_etage_1 = [
            "Feuille Jindagee",
            "Feuille Aatma",
            "Crystal Elémentaire",
            "Pillule",
            "Poudre Explosive",
            "Tirage",
            "Red Coin",
            "Fée dans un Bocal",
        ]
        self.liste_item_etage_2 = [
            "Feuille Jindagee",
            "Feuille Aatma",
            "Crystal Elémentaire",
            "Remède",
            "Poudre Explosive",
            "Machette Rouillée",
            "Tirage",
            "Red Coin",
            "Fée dans un Bocal",
        ]
        self.liste_item_etage_3 = [
            "Feuille Jindagee",
            "Feuille Aatma",
            "Crystal Elémentaire",
            "Pillule",
            "Poudre Explosive",
            "Vieille Pelle",
            "Tirage",
            "Méga Tirage",
            "Red Coin",
            "Gemme de Vie",
            "Fée dans un Bocal",
        ]
        self.liste_item_etage_4 = [
            "Feuille Jindagee",
            "Feuille Aatma",
            "Crystal Elémentaire",
            "Pillule",
            "Poudre Explosive",
            "Tirage",
            "Méga Tirage",
            "Red Coin",
            "Gemme de Vie",
            "Fée dans un Bocal",
        ]
        self.liste_item_etage_5_6 = [
            "Feuille Jindagee",
            "Feuille Aatma",
            "Crystal Elémentaire",
            "Pillule",
            "Poudre Explosive",
            "Tirage",
            "Méga Tirage",
            "Red Coin",
            "Gemme d'Esprit",
            "Fée dans un Bocal",
        ]
        self.liste_item_etage_7_8 = [
            "Feuille Jindagee",
            "Feuille Aatma",
            "Crystal Elémentaire",
            "Pillule",
            "Poudre Explosive",
            "Tirage",
            "Méga Tirage",
            "Red Coin",
            "Gemme de Vie",
            "Gemme d'Esprit",
            "Fée dans un Bocal",
        ]
        self.liste_item_etage_9_10 = [
            "Feuille Jindagee",
            "Fruit Jindagee",
            "Feuille Aatma",
            "Fruit Aatma",
            "Crystal Elémentaire",
            "Ambroisie",
            "Hydromel",
            "Orbe de Furie",
            "Orbe de Folie",
            "Remède",
            "Remède Superieur",
            "Remède Divin",
            "Pillule",
            "Pillule Superieure",
            "Pillule Divine",
            "Fléchette Rouge",
            "Flèche Rouge",
            "Fléchette Bleue",
            "Flèche Bleue",
            "Poudre Explosive",
            "Roche Explosive",
            "Bombe Explosive",
            "Fiole de Poison",
            "Gourde de Poison",
            "Sève d'Absolution",
            "Larme d'Absolution",
            "Soluté d'Absolution",
            "Sève d'Exorcisme",
            "Larme d'Exorcisme",
            "Soluté d'Exorcisme",
            "Mutagène Bleu",
            "Grand Mutagène Bleu",
            "Mutagène Rouge",
            "Grand Mutagène Rouge",
            "Mutagène Vert",
            "Grand Mutagène Vert",
            "Mutagène Doré",
            "Grand Mutagène Doré",
            "Mutagène Hérétique",
            "Mutagène Fanatique",
            "Tirage",
            "Méga Tirage",
            "Red Coin",
            "Fée dans un Bocal",
        ]
        self.liste_dartefact_optionels = ["Machette Rouillée", "Vieille Pelle"]
        self.liste_item_actuelle = []

    def SetItemList(self):
        if services.Player.numero_de_letage == 1:
            self.liste_item_actuelle = self.liste_item_etage_1
        elif services.Player.numero_de_letage == 2:
            self.liste_item_actuelle = self.liste_item_etage_2
        elif services.Player.numero_de_letage == 3:
            self.liste_item_actuelle = self.liste_item_etage_3
        elif services.Player.numero_de_letage == 4:
            self.liste_item_actuelle = self.liste_item_etage_4
        elif services.Player.numero_de_letage in [5, 6]:
            self.liste_item_actuelle = self.liste_item_etage_5_6
        elif services.Player.numero_de_letage in [7, 8]:
            self.liste_item_actuelle = self.liste_item_etage_7_8
        else:
            self.liste_item_actuelle = self.liste_item_etage_9_10

    def ShowItems(self):
        print("1 - Retour")
        numero_a_afficher = 2
        for item in self.liste_item_actuelle:
            print(f"{numero_a_afficher} - {item} : {self.PriceOfItem(item)}")
            numero_a_afficher += 1

    def PriceOfItem(self, item):
        return self.annuaire_des_prix[item]

    def SetRedCoinPrice(self):
        if services.Player.redcoin_bought:
            self.annuaire_des_prix["Red Coin"] = 9999999
        else:
            self.annuaire_des_prix["Red Coin"] = round(round(services.Player.numero_de_letage * 100) * self.modificateur_badge_terni)
        self.annuaire_des_prix["Tirage"] = round(round(
            (services.Player.numero_de_letage * 50)
            + (services.Player.number_of_tirage * (services.Player.numero_de_letage * 15)) * self.modificateur_badge_terni)
        )
        self.annuaire_des_prix["Fée dans un Bocal"] = round(round(
            ((services.Player.numero_de_letage * 50) + 25) * self.modificateur) * self.modificateur_badge_terni
        )

    def UseMegaTirage(self):
        # double tirage des recompenses
        element_tirage = []
        for _ in range(0, 2):
            nombre_aleatoire = random.randint(1, 13)
            if nombre_aleatoire == 1:
                element_tirage.append("Feu")
            if nombre_aleatoire == 3:
                element_tirage.append("Foudre")
            if nombre_aleatoire == 5:
                element_tirage.append("Glace")
            if nombre_aleatoire == 7:
                element_tirage.append("Terre")
            if nombre_aleatoire == 9:
                element_tirage.append("Physique")
            if nombre_aleatoire == 11:
                element_tirage.append("Sang")
            else:
                element_tirage.append("Vide")
        # choix du joueur
        while True:
            try:
                if services.Player.affronte_un_boss:
                    print(
                        f"A l'endroit ou se tenait l'ennemi, il y a maintenant une petite boite en métal bleu ornée d'un grand *POW*.\nVous y plongez la main à l'interieur."
                    )
                else:
                    print(
                        f"Le marchand vous laisse plonger la main dans une boite en carton bleue ornée d'un grand *POW*."
                    )
                print(
                    "A l'interieur, vous pouvez toucher le contour de deux masses étranges, rugueuse."
                    f"\nEn les palpant, vous ressentez une connection avec l'élément [{element_tirage[0]}] et l'élement [{element_tirage[1]}]."
                    f"\n1 - Retirer le [{element_tirage[0]}]"
                    f"\n2 - Retirer le [{element_tirage[1]}]"
                )
                choix = int(input("Choisissez avec les nombres : "))
                ClearConsole()
                if choix in [1, 2]:
                    break
            except ValueError:
                ClearConsole()
        if element_tirage[choix - 1] == "Feu":
            type_du_tirage = "le sort"
            nom_du_tirage = "Explosion de Feu Sacré"
        elif element_tirage[choix - 1] == "Foudre":
            nom_du_tirage = "Combo Electrique"
            type_du_tirage = "la technique"
        elif element_tirage[choix - 1] == "Glace":
            nom_du_tirage = "Mirroir d'Eau"
            type_du_tirage = "le sort"
        elif element_tirage[choix - 1] == "Terre":
            nom_du_tirage = "Position du Massif"
            type_du_tirage = "la technique"
        elif element_tirage[choix - 1] == "Physique":
            nom_du_tirage = "Poussée d'Adrénaline"
            type_du_tirage = "la technique"
        elif element_tirage[choix - 1] == "Sang":
            nom_du_tirage = "Brume de Sang"
            type_du_tirage = "le sort"
        if (
            (element_tirage[choix - 1] != "Vide")
            and (nom_du_tirage not in services.Player.sorts_possedes)
            and (nom_du_tirage not in services.Player.techniques_possedes)
        ):
            commentaire = f"Vous obtenez {type_du_tirage} {nom_du_tirage} !"
            if type_du_tirage == "le sort":
                services.Player.sorts_possedes.append(nom_du_tirage)
                if "Syra" in services.Player.liste_dartefacts_optionels:
                    commentaire += ("Grace au verre de Syra que vous avez bu, vous gagnez aussi 10 pv max !")
                    services.Player.points_de_vie += 10
                    services.Player.points_de_vie_max += 10
                    services.Affichage.EntreePourContinuer()
            elif type_du_tirage == "la technique":
                services.Player.techniques_possedes.append(nom_du_tirage)
                if "Syra" in services.Player.liste_dartefacts_optionels:
                    commentaire += ("\nGrace au verre de Syra que vous avez bu, vous gagnez aussi 10 pm max !")
                    services.Player.points_de_mana += 10
                    services.Player.points_de_mana_max += 10
                    services.Affichage.EntreePourContinuer()
        else:
            commentaire = "Vous sortez la masse, et elle disparait dans les airs.\nMauvaise Pioche !"
        services.Affichage.AfficheMegaTirage(commentaire)

    def UseTirage(self):
        # sort ou technique ?
        if random.randint(0, 1) == 0 :
            type_tirage = "le sort"
        else:
            type_tirage = "la technique"
        # element ?
        element_tirage = []
        for _ in range(0, 2):
            if type_tirage == "le sort":
                nombre_aleatoire = random.randint(1, 7)
            else:
                nombre_aleatoire = random.randint(1, 6)
            if nombre_aleatoire == 1:
                element_tirage.append("Feu")
            if nombre_aleatoire == 2:
                element_tirage.append("Foudre")
            if nombre_aleatoire == 3:
                element_tirage.append("Glace")
            if nombre_aleatoire == 4:
                element_tirage.append("Terre")
            if nombre_aleatoire == 5:
                element_tirage.append("Physique")
            if nombre_aleatoire == 6:
                element_tirage.append("Sang")
            if nombre_aleatoire == 7:
                element_tirage.append("Divin")
        # choix du joueur
        while True:
            try:
                if services.Player.affronte_un_boss:
                    print(
                        f"A l'endroit ou se tenait l'ennemi, il y a maintenant une petite boite en métal jaune ornée d'un grand *?*.\nVous y plongez la main à l'interieur."
                    )
                else:
                    print(
                        f"Le marchand vous laisse plonger la main dans une boite en carton jaune ornée d'un grand *?*."
                    )
                print(
                    "A l'interieur, vous pouvez toucher le contour de deux masses étranges, rugueuse."
                    f"\nEn les palpant, vous ressentez une connection avec l'élément [{element_tirage[0]}] et l'élement [{element_tirage[1]}]."
                    f"\n1 - Retirer le [{element_tirage[0]}]"
                    f"\n2 - Retirer le [{element_tirage[1]}]"
                )
                choix = int(input("Choisissez avec les nombres : "))
                ClearConsole()
                if choix in [1, 2]:
                    break
            except ValueError:
                ClearConsole()
        # construction de la récompense
        # nom commun
        if type_tirage == "le sort":
            if element_tirage[choix - 1] == "Feu":
                nom_du_tirage = "Thermosphère"
            elif element_tirage[choix - 1] == "Foudre":
                nom_du_tirage = "Faisceau"
            elif element_tirage[choix - 1] == "Glace":
                nom_du_tirage = "Pic"
            elif element_tirage[choix - 1] == "Terre":
                nom_du_tirage = "Création"
            elif element_tirage[choix - 1] == "Physique":
                nom_du_tirage = "Explosion"
            elif element_tirage[choix - 1] == "Sang":
                nom_du_tirage = "Dance"
            elif element_tirage[choix - 1] == "Divin":
                nom_du_tirage = "Sonata"
        elif type_tirage == "la technique":
            if element_tirage[choix - 1] == "Feu":
                nom_du_tirage = "Bô"
            elif element_tirage[choix - 1] == "Foudre":
                nom_du_tirage = "Lance"
            elif element_tirage[choix - 1] == "Glace":
                nom_du_tirage = "Katana"
            elif element_tirage[choix - 1] == "Terre":
                nom_du_tirage = "Corne"
            elif element_tirage[choix - 1] == "Physique":
                nom_du_tirage = "Poing"
            elif element_tirage[choix - 1] == "Sang":
                nom_du_tirage = "Dague"
        # bon ou mauvais tirage (seulement etage 7,8)
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 70:
            sort_attaque_forte_pour_etage_7_8 = False
        else:
            sort_attaque_forte_pour_etage_7_8 = True
        # Adjectif
        if services.Player.numero_de_letage in [1, 2]:
            if element_tirage[choix - 1] == "Feu":
                nom_du_tirage += " Chaud"
            elif element_tirage[choix - 1] == "Foudre":
                nom_du_tirage += " Rapide"
            elif element_tirage[choix - 1] == "Glace":
                nom_du_tirage += " Bleu"
            elif element_tirage[choix - 1] == "Terre":
                nom_du_tirage += " Argile"
            elif element_tirage[choix - 1] == "Physique":
                nom_du_tirage += " Léger"
            elif element_tirage[choix - 1] == "Sang":
                nom_du_tirage += " Volevie"
            elif element_tirage[choix - 1] == "Divin":
                nom_du_tirage += " Pitoyable"
        elif services.Player.numero_de_letage in [3, 4]:
            if element_tirage[choix - 1] == "Feu":
                nom_du_tirage += " Brulant"
            elif element_tirage[choix - 1] == "Foudre":
                nom_du_tirage += " Statique"
            elif element_tirage[choix - 1] == "Glace":
                nom_du_tirage += " Froid"
            elif element_tirage[choix - 1] == "Terre":
                nom_du_tirage += " Lapis"
            elif element_tirage[choix - 1] == "Physique":
                nom_du_tirage += " Renforcé"
            elif element_tirage[choix - 1] == "Sang":
                nom_du_tirage += " Siphoneuse"
            elif element_tirage[choix - 1] == "Divin":
                nom_du_tirage += " Miséricordieuse"
        elif services.Player.numero_de_letage in [5, 6]:
            if element_tirage[choix - 1] == "Feu":
                nom_du_tirage += " Enflammé"
            elif element_tirage[choix - 1] == "Foudre":
                nom_du_tirage += " Electrique"
            elif element_tirage[choix - 1] == "Glace":
                nom_du_tirage += " Givré"
            elif element_tirage[choix - 1] == "Terre":
                nom_du_tirage += " Granite"
            elif element_tirage[choix - 1] == "Physique":
                nom_du_tirage += " Lourd"
            elif element_tirage[choix - 1] == "Sang":
                nom_du_tirage += " Vampirique"
            elif element_tirage[choix - 1] == "Divin":
                nom_du_tirage += " Empathique"
        elif services.Player.numero_de_letage in [7, 8]:
            if element_tirage[choix - 1] == "Feu":
                if sort_attaque_forte_pour_etage_7_8:
                    nom_du_tirage += " de la Fournaise"
                else:
                    nom_du_tirage += " Magmatique"
            elif element_tirage[choix - 1] == "Foudre":
                if sort_attaque_forte_pour_etage_7_8:
                    nom_du_tirage += " de l'Eclair"
                else:
                    nom_du_tirage += " Foudroyante"
            elif element_tirage[choix - 1] == "Glace":
                if sort_attaque_forte_pour_etage_7_8:
                    nom_du_tirage += " GLacial"
                else:
                    nom_du_tirage += " Polaire"
            elif element_tirage[choix - 1] == "Terre":
                if sort_attaque_forte_pour_etage_7_8:
                    nom_du_tirage += " Obsidienne"
                else:
                    nom_du_tirage += " de la Montagne"
            elif element_tirage[choix - 1] == "Physique":
                if sort_attaque_forte_pour_etage_7_8:
                    nom_du_tirage += "Maitrisé"
                else:
                    nom_du_tirage += "Fatal"
            elif element_tirage[choix - 1] == "Sang":
                if sort_attaque_forte_pour_etage_7_8:
                    nom_du_tirage += " Parasite"
                else:
                    nom_du_tirage += " Destructrice"
            elif element_tirage[choix - 1] == "Divin":
                if sort_attaque_forte_pour_etage_7_8:
                    nom_du_tirage += " Sincère"
                else:
                    nom_du_tirage += " Bienveillante"
        elif services.Player.numero_de_letage in [9, 10]:
            if element_tirage[choix - 1] == "Feu":
                nom_du_tirage += " Solaire"
            elif element_tirage[choix - 1] == "Foudre":
                nom_du_tirage += "de la Mort Blanche"
            elif element_tirage[choix - 1] == "Glace":
                nom_du_tirage += " Zéro"
            elif element_tirage[choix - 1] == "Terre":
                nom_du_tirage += " Continentale"
            elif element_tirage[choix - 1] == "Physique":
                nom_du_tirage += " de la Comète"
            elif element_tirage[choix - 1] == "Sang":
                nom_du_tirage += " Créatrice"
            elif element_tirage[choix - 1] == "Divin":
                nom_du_tirage += " Absolutrice"
        # Accord au féminin, si besoin
        if nom_du_tirage == "Faisceau Foudroyante":
            nom_du_tirage = "Faisceau Foudroyant"
        elif nom_du_tirage == "Thermosphère Chaud":
            nom_du_tirage = "Thermosphère Chaude"
        elif nom_du_tirage == "Thermosphère Brulant":
            nom_du_tirage = "Thermosphère Brulante"
        elif nom_du_tirage == "Thermosphère Enflammé":
            nom_du_tirage = "Thermosphère Enflammée"
        elif nom_du_tirage == "Création Argile":
            nom_du_tirage = "Création d'Argile"
        elif nom_du_tirage == "Création Lapis":
            nom_du_tirage = "Création de Lapis"
        elif nom_du_tirage == "Création Granite":
            nom_du_tirage = "Création de Granite"
        elif nom_du_tirage == "Explosion Léger":
            nom_du_tirage = "Explosion Légère"
        elif nom_du_tirage == "Explosion Renforcé":
            nom_du_tirage = "Explosion Renforcée"
        elif nom_du_tirage == "Explosion Lourd":
            nom_du_tirage = "Explosion Lourde"
        elif nom_du_tirage == "Explosion Maitrisé":
            nom_du_tirage = "Explosion Maitrisée"
        elif nom_du_tirage == "Explosion Fatal":
            nom_du_tirage = "Explosion Fatale"
        # affichage de la récompense
        if (nom_du_tirage in services.Player.sorts_possedes) or (
            nom_du_tirage in services.Player.techniques_possedes
        ):
            print(
                "Vous retirez un bout de papier !"
                "\nIl y est écrit : Des fois on gagne, des fois on perd. L'important, c'est de participer !"
            )
            services.Affichage.EntreePourContinuer()
        else:
            print(f"Vous retirez {type_tirage} {nom_du_tirage} !")
            services.Affichage.EntreePourContinuer()
            # application de la recompense
            if type_tirage == "le sort":
                services.Player.sorts_possedes.append(nom_du_tirage)
                if "Syra" in services.Player.liste_dartefacts_optionels:
                    print("Grace au verre de Syra que vous avez bu, vous gagnez aussi 10 pv max !")
                    services.Player.points_de_vie += 10
                    services.Player.points_de_vie_max += 10
                    services.Affichage.EntreePourContinuer()
            else:
                services.Player.techniques_possedes.append(nom_du_tirage)
                if "Syra" in services.Player.liste_dartefacts_optionels:
                    print("Grace au verre de Syra que vous avez bu, vous gagnez aussi 10 pm max !")
                    services.Player.points_de_mana += 10
                    services.Player.points_de_mana_max += 10
                    services.Affichage.EntreePourContinuer()
        services.Save.SaveTheGameSansAffichage()
            

    def DoTrading(self):
        # marchand
        services.Affichage.AfficheRentrerChezMarchand()
        self.MiseAJourDesPrix()
        services.Trader.SetItemList()
        self.argent_depense_cumul = 0
        while True:
            while True:
                try:
                    ClearConsole()
                    services.Trader.SetRedCoinPrice()
                    print("     -=[ Marchand ]=-")
                    print(f"   Vous avez {services.Player.nombre_de_gold} golds. ")
                    services.Trader.ShowItems()
                    choix = int(
                        input("\nChoisissez l'item a acheter avec les nombres : ")
                    )
                    ClearConsole()
                    if choix in range(1, (len(services.Trader.liste_item_actuelle) + 2)):
                        break
                except ValueError:
                    ClearConsole()
            if choix in range(2, (len(services.Trader.liste_item_actuelle) + 2)):
                nom_de_litem = services.Trader.liste_item_actuelle[choix - 2]
                if services.Player.nombre_de_gold >= services.Trader.PriceOfItem(nom_de_litem):
                    services.Player.nombre_de_gold -= services.Trader.PriceOfItem(nom_de_litem)
                    self.argent_depense_cumul += services.Trader.PriceOfItem(nom_de_litem)
                    print(f"Vous avez acheté [{nom_de_litem}] !")
                    services.Affichage.EntreePourContinuer()
                    if nom_de_litem == "Red Coin":
                        services.Player.redcoin_bought = True
                        services.Player.nombre_de_red_coin += 1
                    elif nom_de_litem == "Tirage":
                        services.Player.number_of_tirage += 1
                        services.Trader.UseTirage()
                    elif nom_de_litem == "Méga Tirage":
                        services.Trader.UseMegaTirage()
                    elif nom_de_litem == "Gemme de Vie":
                        if services.Player.gemme_de_vie:
                            print("Mais vous en aviez déjà une...\nTant pis.")
                            services.Affichage.EntreePourContinuer()
                        else:
                            services.Player.gemme_de_vie = True
                    elif nom_de_litem == "Gemme d'Esprit":
                        if services.Player.gemme_de_mana:
                            print("Mais vous en aviez déjà une...\nTant pis.")
                            services.Affichage.EntreePourContinuer()
                        else:
                            services.Player.gemme_de_mana = True
                    elif nom_de_litem == "Fée dans un Bocal":
                        if services.Player.possede_une_fee:
                            print(
                                "Alors que vous rangiez votre bocal dans votre sacoche,"
                                " vous voyez les deux fées unir leur pouvoir a travers"
                                " les bocaux pour briser leur cage de verre et s'enfuir."
                                "\nUne bonne lecon d'apprise : Jamais plus de deux fées sur soi !"
                            )
                            services.Affichage.EntreePourContinuer()
                            services.Player.possede_une_fee = False
                        else:
                            services.Player.possede_une_fee = True
                    elif nom_de_litem in services.Trader.liste_dartefact_optionels:
                        services.Player.liste_dartefacts_optionels.append(nom_de_litem)
                    else:
                        services.Player.items_possedes[nom_de_litem] += 1
                else:
                    services.Affichage.AffichePasAssezDargent()
            elif choix == 1:
                services.Affichage.AffichePartirMarchand(self.argent_depense_cumul)
                break
            ClearConsole()

    def MiseAJourDesPrix(self):
        self.__init__()

    def DoArtefactTrading(self):
        liste_des_artefacts_impossibles_a_acheter = [
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
            "Ecaille de la Bête",
            "Hors Stock"
            ]
        while True:
            while True:
                dict_de_tout_les_artefacts = dict(LISTEEFFETSARTEFACT)
                liste_des_artefacts_possede = services.Sove.ModifieArtefactDansSove("Donne",None)
                liste_de_artefacts_possibles = []
                for key in dict_de_tout_les_artefacts:
                    if key not in liste_des_artefacts_possede and key not in liste_des_artefacts_impossibles_a_acheter:
                        liste_de_artefacts_possibles.append(key)
                liste_de_artefacts_a_proposer = services.Sove.ModifieArtefactProposeDansSove("Donne",None)
                try:
                    print("     -=Maitre Des Artefacts=-")
                    print("   -Tout coûte 4 Essences Dorée !-\n")
                    print(f"        [Dans Sacoche : {  services.Sove.ModifieDechetsDansSove('Nombre','Essence Dorée',None) }]\n\n")
                    numero = 1
                    for artefact in liste_de_artefacts_a_proposer:
                        print(f"{numero} - Acheter l'artefact [{artefact}]")
                        print(f"{dict_de_tout_les_artefacts[artefact]['Commentaire']}")
                        for caracteristique in dict_de_tout_les_artefacts[artefact]:
                            if caracteristique != "Commentaire":
                                print(f"       # {caracteristique} + {dict_de_tout_les_artefacts[artefact][caracteristique]} ")
                        print("\n")
                        numero += 1
                    print(f"{numero} - Liste d'artefacts déjà débloqués\n")
                    numero += 1
                    print(f"{numero} - Partir\n")
                    choix = int(input("Faites votre choix avec les nombres : "))
                    ClearConsole()
                    if choix in range(1, numero + 1):
                        break
                except ValueError:
                    ClearConsole()
            if choix == numero :
                break
            elif choix == (numero - 1) :
                while True:
                    try:
                        print("     -=Maitre Des Artefacts=-\n\n")
                        for artefact in liste_des_artefacts_possede:
                            print(f"[{artefact}]")
                            print(f"{dict_de_tout_les_artefacts[artefact]['Commentaire']}")
                            for caracteristique in dict_de_tout_les_artefacts[artefact]:
                                if caracteristique != "Commentaire":
                                    print(f"       # {caracteristique} + {dict_de_tout_les_artefacts[artefact][caracteristique]} ")
                            print("\n")
                        print("1 - Retour")
                        choix = int(input("Faites votre choix avec les nombres : "))
                        ClearConsole()
                        if choix == 1:
                            break
                    except ValueError:
                        ClearConsole()
            else:
                if not  services.Sove.ModifieDechetsDansSove("Limite", "Essence Dorée", 3):
                    print("Vous n'avez pas assez d'essence dorée !")
                    services.Affichage.EntreePourContinuer()

                else:
                    artefact_choisi = liste_de_artefacts_a_proposer[choix - 1]

                    if artefact_choisi == "Hors Stock":
                        print("Hey ! Ce n'est pas a vendre !")
                        services.Affichage.EntreePourContinuer()
                    else:
                        services.Sove.ModifieDechetsDansSove("Enleve", "Essence Dorée", 3)
                        services.Sove.ModifieArtefactDansSove("Ajout", artefact_choisi)
                        services.Sove.ModifieArtefactProposeDansSove("Enleve", artefact_choisi)
                        liste_de_artefacts_possibles.remove(artefact_choisi)

                        if len(liste_de_artefacts_possibles) == 0:
                            artefact_choisi_aleatoirement = "Hors Stock"
                        else:
                            artefact_choisi_aleatoirement = random.choice(liste_de_artefacts_possibles)
                        services.Sove.ModifieArtefactProposeDansSove("Ajout", artefact_choisi_aleatoirement)
                        print(f"Le Maitre vous donne un bon de commande, et promet de rendre l'artefact [{artefact_choisi}] au Coliseum !")
                        services.Affichage.EntreePourContinuer()




        

    def DoKeyTrading(self):
        if not  services.Sove.ModifieTagsDansSove("Checke", "Mage Hollistique") :
            while True:
                while True:
                    try:
                        print("La salle est vide, sauf pour un morceau de papier sur la table.\n\n")
                        print("1 - Lire le papier")
                        print("2 - Repartir")
                        choix = int(input("\nFaites votre choix avec les nombres : "))
                        ClearConsole()
                        if choix in [1, 2]:
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 2 :
                    break
                elif choix == 1:
                    print("*Bonjour. Bonsoir ? Qu'importe. Ou peut etre que ca importe ? Bref.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Mon nom est Lina, je suis mage hollistique, a la croisée des fils du destins, trimbalée de droite a gauche pour être toujours la bonne personne, au bon moment, au bon endroit.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Toute les choses de l'univers sont connectées, même si ce qui relie cause a effet n'est pas évident a voir de premier abord. Mais je crois que..*")
                    services.Affichage.EntreePourContinuer()
                    print("*Je crois que l'univers n'a plus rien en stock pour moi.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Tout ce que j'ai fait a toujours été la bonne chose a faire pour faire avancer mon histoire. Mais depuis que je suis arrivée la, plus rien ne bouge.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Je ne veux plus de cette existance. Ou peut etre que ne plus vouloir de cette existance fait parti du plan de l'univers, et que ma perte est la bonne chose a faire, au bon moment, au bon endroit ? Je ne sais pas, et je ne peux pas savoir.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Ca ne marche pas comme ca.*")
                    services.Affichage.EntreePourContinuer()
                    print("*A celui qui me cherche, a celui qui a besoin de moi, ne cherche pas plus loin, car je suis parti dans les Champs pour vivre comme un fantome, et espérer oublier les années qui passent.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Ne sois pas triste : car je te laisse en cadeau ce symbole. Ce n'est pas un symbole particulier, j'ai juste dessiné n'importe quoi. Mais maintenant que tu l'a vu, tu fait partie de l'équation.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Que tu le veuille ou non, tout ce que tu fera t'amènera vers la suite de ton aventure. Il suffit juste que tu te laisse aller, et que tu fasse ce que tu veuille.*")
                    services.Affichage.EntreePourContinuer()
                    print("*De toute facon, faire ce que tu veut est la bonne chose a faire. Et tu fera ca au bon moment, au bon endroit, pour la bonne personne.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Je te laisse la suite.*")
                    services.Affichage.EntreePourContinuer()
                    print("*-Mes amitiés, Lina*")
                    services.Affichage.EntreePourContinuer()
                    if not  services.Sove.ModifieTagsDansSove("Checke", "Symbole Vu"):
                        print("Vous regardez le symbole .")
                        services.Affichage.EntreePourContinuer()
                        print("C'est un S en perspective.")
                        services.Affichage.EntreePourContinuer()
                        print("Vous vous mettez a penser aux dernieres lignes du message : il n'y a pas de guide précis sur ce que vous devez faire, car ce que vous allez faire est la bonne chose a faire ?")
                        services.Affichage.EntreePourContinuer()
                        print("Eh bien !\nQue c'est bizarre, une mage hollistique !")
                        services.Affichage.EntreePourContinuer()
                        services.Sove.ModifieTagsDansSove("Ajout", "Symbole Vu")
        if  services.Sove.ModifieTagsDansSove("Checke", "Mage Hollistique") and not  services.Sove.ModifieTagsDansSove("Checke", "Mage Hollistique Dans Tour"):
            services.Sove.ModifieTagsDansSove("Ajout", "Mage Hollistique Dans Tour")
            print("*Hey ! C'est toi !*")
            services.Affichage.EntreePourContinuer()
            print("Vous retrouvez un visage familier derriere le comptoir : c'est la Mage que vous avez amené au quatrieme étage !")
            services.Affichage.EntreePourContinuer()
            print("*Après que ce piano se soit écrasé sur moi, j'ai atteri ici. Et tu devinera jamais quoi ?*")
            services.Affichage.EntreePourContinuer()
            print("*Le batiment est a mon nom ! Incroyable non ?*")
            services.Affichage.EntreePourContinuer()
            print("*C'est comme si ma grande mission dans la vie , c'était d'arriver là.*")
            services.Affichage.EntreePourContinuer()
            print("*Comme si, toute cette aventure était une suite d'actions aléatoires cruciales qui, par le coup du sort, étaient pile poil ce que je devais faire.*")
            services.Affichage.EntreePourContinuer()
            print("*Au bon endroit, au bon moment, hein ?*")
            services.Affichage.EntreePourContinuer()
            print("*J'ai lu le papier. Je crois que je peux t'aider.*")
            services.Affichage.EntreePourContinuer()
            print("*Quand nous avons récupéré les clés dans le coliseum, tu sais ces petites boules noires ? J'ai eu l'impression de comprendre un truc:*")
            print("*Elles ont la même énergie que les âmes ici. Je pense que ces deux choses sont liées. Je pense que...*")
            services.Affichage.EntreePourContinuer()
            print("*Il n'y a plus de clé apres le troisième étage parce que les gens ici ont arrêté de croire que l'on pouvait aller plus loin que le troisième étage.*")
            services.Affichage.EntreePourContinuer()
            print("*Mais si ! Ca fait sens ! Regarde, tout le monde parle du Coliseum comme d'une batisse magique, avec leur cercle de la vie et tout le tsoin tsoin.*")
            services.Affichage.EntreePourContinuer()
            print("*Comme quoi tout était influencé par les désirs des gens.*")
            services.Affichage.EntreePourContinuer()
            print("*Et si les clés étaient une cumulation du désir des gens de sortir ? D'avancer ? De descendre encore plus profondément dans le labyrinthe ?* ")
            services.Affichage.EntreePourContinuer()
            print("*Rapelle toi : tout est lié de manière imperceptible ! Ce qui relie cause a effet n'est pas si évident !*")
            services.Affichage.EntreePourContinuer()
            print("*Bref. Si ma théorie est juste, alors contente toi d'apporter des matériaux correspondants aux différents étages, et je m'occuperais de raviver le lien entre étage et génération d'une clé pour en sortir.*")
            services.Affichage.EntreePourContinuer()
            print("*Ta compris ? Non ? T'inquiète pas, ca va être facile a comprendre dans quelques instants.*")
            services.Affichage.EntreePourContinuer()
        if  services.Sove.ModifieTagsDansSove("Checke", "Mage Hollistique Dans Tour"):
            while True:
                while True:
                    try:
                        liste_de_trades = [
                            "Clé"
                        ]
                        print(f"     -=Mage Hollistique=-")
                        print("Au bon endroit, au bon moment, toujours !\n\n")
                        numero = 1
                        for trade in liste_de_trades:
                            level_actuel_de_uppgrade =  services.Sove.ModifieLivraisonDansSove("Nombre", trade)
                            characteristique_de_luppgrade = ANNUAIREPRIXVILLAGE[trade]
                            if len(characteristique_de_luppgrade) == level_actuel_de_uppgrade:
                                prix_de_luppgrade = "Impossible"
                                print(f"{numero} - {trade} niv. MAX")
                            else:
                                prix_de_luppgrade = characteristique_de_luppgrade[level_actuel_de_uppgrade]
                                level_atteint = level_actuel_de_uppgrade + 1
                                if len(characteristique_de_luppgrade) == level_atteint:
                                    level_atteint = "MAX"
                                print(f"{numero} - {trade} niv. {level_actuel_de_uppgrade} ==) {trade} niv. {level_actuel_de_uppgrade + 1}")
                                print("    Materiaux nécéssaires:")
                                for materiau in prix_de_luppgrade:
                                    if materiau != "Emblème de la Fin":
                                        nombre_materiau_dans_sac = services.Sove.ModifieDechetsDansSove("Nombre",materiau)
                                    else :
                                        nombre_materiau_dans_sac = "Non Possédé" 
                                        if services.Sove.ModifieLivraisonDansSove("Nombre", materiau) >= 1 :
                                            nombre_materiau_dans_sac = "Possédé" 
                                    print(f"      - {prix_de_luppgrade[materiau]} {materiau} [{nombre_materiau_dans_sac}]")
                            print("\n")

                            numero += 1
                        print(f"\n{numero} - Retour\n")
                        choix = int(input("Faites votre choix avec les nombres : "))
                        ClearConsole()

                        if choix in range(1, numero + 1):
                            break

                    except ValueError:
                        ClearConsole()
                
                if choix == numero:
                    break

                else:
                    # trouver le prix en materiau de luppgrade
                    objet_choisi = liste_de_trades[choix - 1]
                    level_actuel_de_uppgrade =  services.Sove.ModifieLivraisonDansSove("Nombre", objet_choisi)
                    if len(characteristique_de_luppgrade) == level_actuel_de_uppgrade:
                        print("Impossible d'augmenter le niveau de cet objet.")
                        services.Affichage.EntreePourContinuer()
                    else:
                        characteristique_de_luppgrade = ANNUAIREPRIXVILLAGE[objet_choisi]
                        prix_de_luppgrade = characteristique_de_luppgrade[level_actuel_de_uppgrade]

                        achat_possible = self.CheckIfEnoughMaterials(prix_de_luppgrade)

                        if not achat_possible:
                            print("Vous n'avez pas assez de materiaux !")
                            services.Affichage.EntreePourContinuer()

                        else:
                            self.BuyUppgrade(prix_de_luppgrade)

                            print(f"*Je prend ca, je fais ceci, et... Ta da ! Il devrait y avoir une clé a l'étage {level_actuel_de_uppgrade + 4} maintenant !*")
                            print("*Comment je le sais ? Bah, je le sais pas encore. Mais si tu m'a donné tout ca c'est forcément pour une raison ! Tiens, prend donc un bon de livraison au cas ou.*")
                            services.Affichage.EntreePourContinuer()

                            services.Sove.ModifieLivraisonDansSove("Ajout", objet_choisi)


    def DoBankTrading(self):
        while True:
            while True:
                try:
                    print("     -=Banque et Echanges=-\n\n")
                    print("1 - Echanger 2 materiaux contre 1 de même rang")
                    print("2 - Améliorer son équipement")
                    print("3 - Quitter la Banque\n")
                    choix = int(input("Faites votre choix avec les nombres : "))
                    ClearConsole()
                    if choix in range(1, 4):
                        break
                except ValueError: 
                    ClearConsole()

            if choix == 3:
                break

            elif choix == 2 and not "Carte VIP" in  services.Sove.ModifieTagsDansSove("Donne", None):
                print("Le Banquier vous regarde avec un air amusé, puis tape une pancarte affiché a coté de lui d'un doigt provocateur.")
                services.Affichage.EntreePourContinuer()
                print("*Le service OBJETS de la Banque n'est accordé qu'aux détenteurs de la Carte VIP*")
                services.Affichage.EntreePourContinuer()

            elif choix == 2:
                while True:
                    while True:
                        try:
                            liste_de_trades = [
                                "Médaillon de Leprechaun",
                                "Noyau d'Aurelionite",
                            ]
                            print(f"     -=Banque=-\n\n")
                            numero = 1
                            for trade in liste_de_trades:
                                level_actuel_de_uppgrade =  services.Sove.ModifieLivraisonDansSove("Nombre", trade)
                                characteristique_de_luppgrade = ANNUAIREPRIXVILLAGE[trade]
                                if len(characteristique_de_luppgrade) == level_actuel_de_uppgrade:
                                    prix_de_luppgrade = "Impossible"
                                    print(f"{numero} - {trade} niv. MAX")
                                else:
                                    prix_de_luppgrade = characteristique_de_luppgrade[level_actuel_de_uppgrade]
                                    level_atteint = level_actuel_de_uppgrade + 1
                                    if len(characteristique_de_luppgrade) == level_atteint:
                                        level_atteint = "MAX"
                                    print(f"{numero} - {trade} niv. {level_actuel_de_uppgrade} ==) {trade} niv. {level_actuel_de_uppgrade + 1}")
                                    print("    Materiaux nécéssaires:")
                                    for materiau in prix_de_luppgrade:
                                        if materiau != "Emblème de la Fin":
                                            nombre_materiau_dans_sac = services.Sove.ModifieDechetsDansSove("Nombre",materiau)
                                        else :
                                            nombre_materiau_dans_sac = "Non Possédé" 
                                            if services.Sove.ModifieLivraisonDansSove("Nombre", materiau) >= 1 :
                                                nombre_materiau_dans_sac = "Possédé" 
                                        print(f"      - {prix_de_luppgrade[materiau]} {materiau} [{nombre_materiau_dans_sac}]")
                                print("\n")

                                numero += 1
                            
                            print(f"{numero} - Poser des questions sur les objets proposés\n")
                            numero += 1
                            print(f"{numero} - Retour\n")
                            choix = int(input("Faites votre choix avec les nombres : "))
                            ClearConsole()

                            if choix in range(1, numero + 1):
                                break

                        except ValueError:
                            ClearConsole()
                    
                    if choix == numero:
                        break

                    elif choix == (numero - 1):
                        print("*Bien Sur, estimée clientelle !*")
                        services.Affichage.EntreePourContinuer()
                        print("*Ces objets sont de véritables artefacts, si l'on peut qualifier d'artefact ce que nous créons !*")
                        services.Affichage.EntreePourContinuer()
                        print("*Saviez vous par exemple que le Noyau d'Aurelionite n'en est pas un ? En effet, les aurelionites, ces golems dorés, n'ont pas de coeur ou de noyau a proprement parler !*")
                        services.Affichage.EntreePourContinuer()
                        print("*Ce nom leur a été donné parce que son inventeur, avant de partir dans les champs, s'est inspiré de cette propriété que les aurelionites a se mouvoir dans l'or pour creer un petit bijou qui...*")
                        services.Affichage.EntreePourContinuer()
                        print("Le vendeur vous regarde alors que vous êtes en plein baillement.")
                        services.Affichage.EntreePourContinuer()
                        print("*...*")
                        services.Affichage.EntreePourContinuer()
                        print("*...*")
                        services.Affichage.EntreePourContinuer()
                        print("*...*")
                        services.Affichage.EntreePourContinuer()
                        print("*..eurk. Ca manque de manière ici.*")
                        services.Affichage.EntreePourContinuer()
                        print("Vous lancez un regard percant au vendeur.")
                        services.Affichage.EntreePourContinuer()
                        print("*Le Médaillon augmente les chances qu'un monstre lache des materiaux de 5% par niveau.*")
                        print("*Le Noyau augmente les gains de golds de toute sources de 10% par niveau.*")
                        services.Affichage.EntreePourContinuer()
                        print("Le vendeur se rassoie et vous regarde de manière hautaine, un mélange apparent de dégout et d'arrogance plaqué sur son visage.")
                        services.Affichage.EntreePourContinuer() 

                    else:
                        # trouver le prix en materiau de luppgrade
                        objet_choisi = liste_de_trades[choix - 1]
                        level_actuel_de_uppgrade =  services.Sove.ModifieLivraisonDansSove("Nombre", objet_choisi)
                        characteristique_de_luppgrade = ANNUAIREPRIXVILLAGE[objet_choisi]
                        if len(characteristique_de_luppgrade) == level_actuel_de_uppgrade:
                            print("Impossible d'augmenter le niveau de cet objet.")
                            services.Affichage.EntreePourContinuer()
                        else:
                            prix_de_luppgrade = characteristique_de_luppgrade[level_actuel_de_uppgrade]

                            achat_possible = self.CheckIfEnoughMaterials(prix_de_luppgrade)

                            if not achat_possible:
                                print("Vous n'avez pas assez de materiaux !")
                                services.Affichage.EntreePourContinuer()

                            else:
                                self.BuyUppgrade(prix_de_luppgrade)

                                print(f"Le Banquier prend vos materiaux et vous donne un bon de commande sur lequel est écrit : [{objet_choisi} de niveau {level_actuel_de_uppgrade + 1}].")
                                print("Il vous assure que le prochain aventurier pourra retrouver tout les objets que vous avez commandé chez le marchand de n'importe quel étage, et vous remercie de votre achat !")
                                services.Affichage.EntreePourContinuer()

                                services.Sove.ModifieLivraisonDansSove("Ajout", objet_choisi)

            elif choix == 1:
                while True:
                    while True:
                        try:
                            liste_dechet_echangeables = []
                            print("     -=Echange deux [objet]=-\n\n")
                            numero = 1
                            for dechet in services.Player.liste_de_materiaux:
                                nombre =  services.Sove.ModifieDechetsDansSove("Nombre", dechet, None)
                                if nombre >= 2 :
                                    liste_dechet_echangeables.append(dechet)
                                    print(f"{numero} - {dechet} ({nombre} dans la sacoche)")
                                    numero += 1
                            print(f"{numero} - Retour\n")
                            choix = int(input("Faites votre choix avec les nombres : "))
                            ClearConsole()
                            if choix in range(1, numero + 1):
                                break
                        except ValueError:
                            ClearConsole()
                    if choix == numero:
                        break
                    else:
                        dechet_choisi = liste_dechet_echangeables[choix - 1]
                        liste_dobjets_proposes_a_lechange = []
                        if dechet_choisi in MATERIAUXRANG1:
                            liste_dobjets_proposes_a_lechange = MATERIAUXRANG1
                        elif dechet_choisi in MATERIAUXRANG2:
                            liste_dobjets_proposes_a_lechange = MATERIAUXRANG2
                        elif dechet_choisi in MATERIAUXRANG3:
                            liste_dobjets_proposes_a_lechange = MATERIAUXRANG3
                        elif dechet_choisi in MATERIAUXRANG4:
                            liste_dobjets_proposes_a_lechange = MATERIAUXRANG4
                        elif dechet_choisi in MATERIAUXRANG5:
                            liste_dobjets_proposes_a_lechange = MATERIAUXRANG5
                        elif dechet_choisi in MATERIAUXRANG6:
                            liste_dobjets_proposes_a_lechange = MATERIAUXRANG6
                        if dechet_choisi in MATERIAUXRANG7: #impossible
                            print("Le Banquier vous regarde avec un air pincé, puis hoche la tête de gauche a droite.")
                            services.Affichage.EntreePourContinuer()
                        else:
                            while True:
                                while True:
                                    try:
                                        print(f"     -=Echange deux [{dechet_choisi}] contre un [objet]=-\n\n")
                                        numero = 1
                                        for objet in liste_dobjets_proposes_a_lechange:
                                            print(f"{numero} - {objet}")
                                            numero += 1
                                        print(f"{numero} - Retour\n")
                                        choix = int(input("Faites votre choix avec les nombres : "))
                                        ClearConsole()
                                        if choix in range(1, numero + 1):
                                            break
                                    except ValueError:
                                        ClearConsole()
                                    
                                if choix == numero:
                                    break
                                else:
                                    dechet_qui_va_etre_echange = liste_dobjets_proposes_a_lechange[choix - 1]

                                    while True:
                                        try:
                                            print(f"     -=Echange deux [{dechet_choisi}] contre un [{dechet_qui_va_etre_echange}]=-\n\n")
                                            print(f"Voulez vous échanger 2 [{dechet_choisi}] contre 1 [{dechet_qui_va_etre_echange}] ?\n")
                                            print("1 - Oui")
                                            print("2 - Non\n")
                                            choix = int(input("Faites votre choix avec les nombres : "))
                                            ClearConsole()
                                            if choix in [1, 2]:
                                                break
                                        except ValueError:
                                            ClearConsole()
                                        
                                    if choix == 2:
                                        pass

                                    else:
                                        services.Sove.ModifieDechetsDansSove("Enleve", dechet_choisi, 2)
                                        services.Sove.ModifieDechetsDansSove("Ajout", dechet_qui_va_etre_echange, 1)
                                        print("C'est fait !")
                                        services.Affichage.EntreePourContinuer()


                                if not  services.Sove.ModifieDechetsDansSove("Limite", dechet_choisi, 2):
                                    break


                            






    def DoVillageTrading(self, trader):
        liste_de_uppgrade_armurier = [
            "Chapeau",
            "Boucles d'Oreille",
            "Collier",
            "Cotte de Maille",
            "Bracelet",
            "Gants",
            "Anneau",
            "Bottes"
        ]
        liste_de_uppgrade_sorciere = [
            "Fiole de Sève",
            "Fiole de Rosée",
            "Tisane d'Ecorce",
            "Tisane de Racine",
            "Charge de Feu",
            "Charge de Glace",
            "Charge de Foudre",
            "Charge de Terre",
            "Charge de Chair",
            "Charge de Sang",
        ]
        liste_de_uppgrade_herboriste = [
            "Ration Jindagee",
            "Ration Jindagee Raffinée",
            "Ration Aatma",
            "Ration Aatma Rafinée",
            "Ration Cristalline",
            "Ration d'Hydromel",
            "Ration Ambroisie",
            "Ration Explosive",
            "Ration Explosive Raffinée",
            "Pack de Fléchettes",
            "Pack de Flèches",
            "Pack Premier Tour",
        ]
        if trader =="ARMURIER":
            liste_de_trades = liste_de_uppgrade_armurier
        if trader =="SORCIERE":
            liste_de_trades = liste_de_uppgrade_sorciere
        if trader =="HERBORISTE":
            liste_de_trades = liste_de_uppgrade_herboriste
        while True:
            while True:
                try:
                    print(f"     -={trader}=-\n\n")
                    print("1 - Partir")
                    print("2 - Poser des questions sur l'équipement")
                    print("3 - Améliorer son équipement\n")
                    choix = int(input("Faites votre choix avec les nombres : "))
                    ClearConsole()
                    if choix in range (1, 4):
                        break
                except ValueError:
                        ClearConsole()
            
            if choix == 1 :
                break

            elif choix == 2:
                if trader =="ARMURIER":
                    print("*Hum ? C'que ça fait ?*")
                    services.Affichage.EntreePourContinuer()
                    print("L'Armurier réfléchit quelques temps, et releve la tête.")
                    services.Affichage.EntreePourContinuer()
                    print("*Bah, ca protege, nan ?*")
                    services.Affichage.EntreePourContinuer()
                    print("Vous lancez un regard blazé à l'Armurier, avant de voir une petite femme sortir de sous le comptoir.")
                    services.Affichage.EntreePourContinuer()
                    print("*Bonjour, estimé voyageur ! Vous vous demandez ce que font nos articles, et j'ai la réponse !*")
                    services.Affichage.EntreePourContinuer()
                    print("*Il ne faut surtout pas demander a ce gros tas de muscle, tout ce qu'il sait faire, c'est taper sur l'enclume et taper sur les nerfs !*")
                    services.Affichage.EntreePourContinuer()
                    print("Sur ces mots, la marchande donne un gros coup de pied sur le genou de l'Armurier.\nCe qui n'a pas l'air de lui faire grand effet.")
                    services.Affichage.EntreePourContinuer()
                    print("*Je disais donc, voici en gros les effets que nos articles auront sur le prochain aventurier que vous allez sponsoriser :*")
                    services.Affichage.EntreePourContinuer()
                    print("  - Le Chapeau")
                    print("*Tissé avec la plus grande délicatesse, il augmente l'intelligence de 3 points par niveaux.*")
                    services.Affichage.EntreePourContinuer()
                    print("  - Les Boucles d'Oreilles")
                    print("*Il y a un très subtil patterne dans les mailles du bijou qui orne ces boucles, et ce patterne augmente le taux de sort critique de 2% par niveaux.*")
                    services.Affichage.EntreePourContinuer()
                    print("  - Le Collier")
                    print("*Un chef d'oeuvre ! Des techniques aiguisées pendant des siècles qui augmentent le taux de techniques critiques de 2% par niveaux !*")
                    services.Affichage.EntreePourContinuer()
                    print("  - La Cotte de Maille")
                    print("*J'ai étudié moi même une cotte de maille enchantée venant des Tout-Premiers, et cette réplique donne 4 points de défence supplémentaires par niveaux.*")
                    services.Affichage.EntreePourContinuer()
                    print("  - Le Bracelet")
                    print("*Un objet d'or fin qui mobilise le mana et le transforme en force, 3 points supplémentaires par niveaux.*")
                    services.Affichage.EntreePourContinuer()
                    print("  - Les Gants")
                    print("*Ils sont renforcés au niveau des phalanges avec un alliage de cette roche qui compose les golem.*\n*Ca met plus de poid lors des attaques, et augmente les dégats critiques des techniques de 3 points par niveaux !*")
                    services.Affichage.EntreePourContinuer()
                    print("  - L'Anneau")
                    print("*C'est le même principe que le bracelet, mais son action est concentrée au niveau des veines de mana, afin de rajouter 3 points de dégât par niveau lors des sorts critiques.*")
                    services.Affichage.EntreePourContinuer()
                    print("  - Les Bottes")
                    print("*Rembourrées, renforcées, le produit phare de notre boutique !*\n*Elles augmentent le taux d'esquive de 1% par niveau.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Quoi ?*\n*C'est pas beaucoup ?*\n*Et pourtant ca veut dire qu'au niveau maximum, ca annule 15% des attaques et sorts qui viennent sur vous !*")
                    services.Affichage.EntreePourContinuer()
                    print("*Et c'est sans compter la précision de ces actions ou les pourcentages d'esquive que les aventuriers peuvent accumuler dans le Coliseum...*")
                    services.Affichage.EntreePourContinuer()
                    print("*Alors, vous en pensez quoi ?*\n*Ca vaut le coup hein ?*")
                    services.Affichage.EntreePourContinuer()
                    print("*Pour tout ce qui est paiement, je vous laisse voir avec mon frère.*\n*Moi je retourne a mes prototypes !*")
                    services.Affichage.EntreePourContinuer()
                    print("Vous faites un signe de main a la marchande qui retourne alors sous le comptoir, et l'armurier se remet a frapper l'enclume.")
                    services.Affichage.EntreePourContinuer()
                if trader =="SORCIERE":
                    print("*Mes produits ?*")
                    services.Affichage.EntreePourContinuer()
                    print("*Eh bien..ils sont...bon ?*")
                    services.Affichage.EntreePourContinuer()
                    print("Vous lancez un regard intrigué a la sorcière")
                    services.Affichage.EntreePourContinuer()
                    print("*...bon écoutez, je vais vous décrire chacune de mes potions.*")
                    services.Affichage.EntreePourContinuer()
                    print("La Sorcière sort un gros livre poussiéreux, et l'ouvre a une page gribouillée.")
                    print("Vous pouvez lire sur la couverture : [100 RECETTES DE POTIONS ET SOLUTES ALCHIMIQUES QUI PEUVENT TOMBER A L'EPREUVE DU SABBAT, EDITION 1053 APRES JC]")
                    services.Affichage.EntreePourContinuer()
                    print("*Alors..euh..ah oui !*\n*La Fiole de Sève.*")
                    print("*C'est pas vraiment de la sève, mais c'est comme ca qu'on l'appelle, et ca augmente les points de mana maximum de 4 par niveau !*\n*Enfin, seulement si on la boit.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Ensuite, la Fiole de Rosée.*")
                    print("*Ca je sais, je sais, c'est...comme la fiole de sève..mais...ca augmente la force !*\n*Ah non, les points de vie maximum.*\n*4 points par niveaux.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Ensuite, les tisanes.*\n*Ca je connait par coeur !*\n*Genre, la Tisane d'Ecorce.*")
                    print("*Eh bah, quand on la boit, ca change le corps.*\n*Et genre, quand il regagne des points de mana, en mangeant des fruits aatma ou avec un talent, il reprend plus de points de mana !*\n*2 points par niveaux.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Par exemple, si je prend une pillule et que je dois récuperer 20 points de mana, eh bah si j'ai bu une tisane d'écorce de niveau 3 avant, bah je reprend 26 points de mana a la place de 20.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Et ya l'autre tisane aussi, la tisane de...de... de Racine !*")
                    services.Affichage.EntreePourContinuer()
                    print("*Même chose, mais ca redonne 2 points de vie supplémentaires par niveau, pour toute les sources !*")
                    services.Affichage.EntreePourContinuer()
                    print("*Ensuite...ya...attend quoi ?*")
                    services.Affichage.EntreePourContinuer()
                    print("La sorcière ré-ouvre son livre et regarde une page.")
                    services.Affichage.EntreePourContinuer()
                    print("*Aie, je me suis trompée !*\n*C'est la tisane d'Ecorce qui améliore le regain de vie, et la tisane de Racine qui améliore le regain de mana !*")
                    print("*Je me trompe toujours entre ces deux là !*")
                    services.Affichage.EntreePourContinuer()
                    print("*Enfin bref.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Après on a la potion de transmutation qui...attend non celle la je la fait pas.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Celle la non plus..*")
                    services.Affichage.EntreePourContinuer()
                    print("*Celle la non plus...je crois...*")
                    services.Affichage.EntreePourContinuer()
                    print("Vous arrêtez la sorcière et lui montrez les orbes de poussière de différentes couleur sur son comptoir.")
                    services.Affichage.EntreePourContinuer()
                    print("*Ah oui !*\n*Les charges élémentaires !*")
                    services.Affichage.EntreePourContinuer()
                    print("*En gros, ca ajoute 10% de dégâts bonus aux sorts et attaques de l'élément associé a la charge, pour chaque niveau.*")
                    print("*Genre avec une charge de sang de niveau 5, on fait 25% de dégats en plus quand on utilise une technique ou un sort de sang.*")
                    services.Affichage.EntreePourContinuer()
                    print("*Et...c'est tout.*")
                    services.Affichage.EntreePourContinuer()
                    print("La Sorcière range son livre de révision sous son comptoir.")
                    services.Affichage.EntreePourContinuer()
                    print("*Demandez moi si vous avez besoin de quoi que ce soit d'autre !*")
                    services.Affichage.EntreePourContinuer()
                if trader =="HERBORISTE":
                    print("*...*")
                    services.Affichage.EntreePourContinuer()
                    print("Un Homme a l'allure mystérieuse, dont le visage est caché par un foulard, vous regarde attentivement.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous avez l'impression que votre question est tombée dans l'oreille d'un sourd...")
                    services.Affichage.EntreePourContinuer()
                    print("...mais vous vous rendez compte qu'elle est tombée dans l'oreille d'un muet, lorsque l'Herboriste vous parle en ASL.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous essayez de décrypter les signes effectués par le vendeur, lorsque celui ci s'arrête et soupire.")
                    services.Affichage.EntreePourContinuer()
                    print("Il vous prend alors la tête avec ses deux bras étonnamment musclés, et la tourne lentement vers une pancarte a votre droite...")
                    print("...sur laquelle est écrit en grosses lettres la description de chaque services qu'il propose.")
                    services.Affichage.EntreePourContinuer()
                    print("Ration Jindagee : 2 Feuilles Jindagee par niveaux seront données a votre aventurier.")
                    print("Ration Jindagee Raffinée : 1 Fruit Jindagee par niveaux seront données a votre aventurier.")
                    services.Affichage.EntreePourContinuer()
                    print("Ration Aatma : 2 Feuilles Aatma par niveaux seront données a votre aventurier.")
                    print("Ration Aatma Raffinée : 1 Fruit Aatma par niveaux seront données a votre aventurier.")
                    services.Affichage.EntreePourContinuer()
                    print("Ration Cristalline : 2 Crystaux Elementaires par niveaux seront données a votre aventurier.")
                    services.Affichage.EntreePourContinuer()
                    print("Ration d'Hydromel : 2 fioles d'Hydromel par niveaux seront données a votre aventurier.")
                    print("Ration d'Ambroisie : 2 fioles d'Ambroisie par niveaux seront données a votre aventurier.")
                    services.Affichage.EntreePourContinuer()
                    print("Ration Explosive : 2 unitées de Poudre Explosive par niveaux seront données a votre aventurier.")
                    print("Ration Explosive Raffinée : 1 Roche Explosive par niveaux seront données a votre aventurier.")
                    services.Affichage.EntreePourContinuer()
                    print("Ration de Fléchettes : 2 fléchettes bleues et 2 fléchettes rouges par niveaux seront données a votre aventurier.")
                    print("Ration de Flèches : 1 flèches bleues et 1 flèches rouges par niveaux seront données a votre aventurier.")
                    services.Affichage.EntreePourContinuer()
                    print("Pack Premier Tour : un booster pack de produits a utiliser au premier tour sera donné a votre aventurier.")
                    print("Il comprend 1 fiole de poison, 1 sève d'exorcisme, 1 sève d'absolution, 1 Mutagène Rouge, 1 Mutagène Bleu et 1 Mutagène Vert par niveau.")
                    services.Affichage.EntreePourContinuer()
                    print("L'herboriste vous lache la tête et retourne a ses occupations, alors que vous regardez le sol quelques instants pour cacher votre embarras.")
                    services.Affichage.EntreePourContinuer()
            else:
                while True:
                    while True:
                        try:
                            print(f"     -={trader}=-\n\n")
                            numero = 1
                            for trade in liste_de_trades:
                                level_actuel_de_uppgrade =  services.Sove.ModifieLivraisonDansSove("Nombre", trade)
                                characteristique_de_luppgrade = ANNUAIREPRIXVILLAGE[trade]
                                if len(characteristique_de_luppgrade) == level_actuel_de_uppgrade:
                                    prix_de_luppgrade = "Impossible"
                                    print(f"{numero} - {trade} niv. MAX")
                                else:
                                    prix_de_luppgrade = characteristique_de_luppgrade[level_actuel_de_uppgrade]
                                    level_atteint = level_actuel_de_uppgrade + 1
                                    if len(characteristique_de_luppgrade) == level_atteint:
                                        level_atteint = "MAX"
                                    print(f"{numero} - {trade} niv. {level_actuel_de_uppgrade} ==) {trade} niv. {level_actuel_de_uppgrade + 1}")
                                    print("    Materiaux nécéssaires:")
                                    for materiau in prix_de_luppgrade:
                                        if materiau != "Emblème de la Fin":
                                            nombre_materiau_dans_sac = services.Sove.ModifieDechetsDansSove("Nombre",materiau)
                                        else :
                                            nombre_materiau_dans_sac = "Non Possédé" 
                                            if services.Sove.ModifieLivraisonDansSove("Nombre", materiau) >= 1 :
                                                nombre_materiau_dans_sac = "Possédé" 
                                        print(f"      - {prix_de_luppgrade[materiau]} {materiau} [{nombre_materiau_dans_sac}]")
                                print("\n")

                                numero += 1
                            print(f"{numero} - Revenir au Menu Principal")
                            choix = int(input("\nFaites votre choix avec les nombres : "))
                            ClearConsole()

                            if choix in range(1, numero + 1):
                                break

                        except ValueError:
                            ClearConsole()
                    
                    if choix == numero:
                        break

                    else:
                        # trouver le prix en materiau de luppgrade
                        objet_choisi = liste_de_trades[choix - 1]
                        level_actuel_de_uppgrade =  services.Sove.ModifieLivraisonDansSove("Nombre", objet_choisi)
                        characteristique_de_luppgrade = ANNUAIREPRIXVILLAGE[objet_choisi]
                        if len(characteristique_de_luppgrade) == level_actuel_de_uppgrade:
                            print("Impossible d'augmenter le niveau de cet objet.")
                            services.Affichage.EntreePourContinuer()
                        else:
                            prix_de_luppgrade = characteristique_de_luppgrade[level_actuel_de_uppgrade]

                            achat_possible = self.CheckIfEnoughMaterials(prix_de_luppgrade)

                            if not achat_possible:
                                print("Vous n'avez pas assez de materiaux !")
                                services.Affichage.EntreePourContinuer()

                            else:
                                self.BuyUppgrade(prix_de_luppgrade)

                                print(f"Le propriétaire de l'étal prend vos materiaux et vous donne un bon de commande sur lequel est écrit : [{objet_choisi} de niveau {level_actuel_de_uppgrade + 1}].")
                                print("Il vous assure que le prochain aventurier pourra retrouver tout les objets que vous avez commandé chez le marchand de n'importe quel étage, et vous remercie de votre achat !")
                                services.Affichage.EntreePourContinuer()

                                services.Sove.ModifieLivraisonDansSove("Ajout", objet_choisi)


    def CheckIfEnoughMaterials(self, prix_en_dictionnaire):
        for materiau in prix_en_dictionnaire:

            if materiau != "Emblème de la Fin":
                prix_en_materiau = prix_en_dictionnaire[materiau]
                possible =  services.Sove.ModifieDechetsDansSove("Limite", materiau, prix_en_materiau)

            else: 
                possible = (services.Sove.ModifieLivraisonDansSove("Nombre", materiau) >= 1)

            if possible == False:
                return False
        
        return True
    
    def BuyUppgrade(self, prix_en_dictionnaire):
        for materiau in prix_en_dictionnaire:
            prix_en_materiau = prix_en_dictionnaire[materiau]
            if materiau != "Emblème de la Fin":
                services.Sove.ModifieDechetsDansSove("Enleve", materiau, prix_en_materiau)

    def DoMapTrader(self):
        while True:
            while True:
                try:
                    print("     -=Chuchoteur=-\n\n")
                    print("1 - Hum... Bonjour ?")
                    print("2 - Qui êtes vous ?")
                    print("3 - Qu'est ce que vous avez écrit par terre ?")
                    print("4 - Améliorer votre carte")
                    print("5 - Repartir\n")
                    choix = int(input("Faites votre choix avec les nombres : "))
                    ClearConsole()
                    if choix in range(1, 6):
                        break
                except ValueError: 
                    ClearConsole()

            if choix == 1:
                print("L'Homme s'arrête d'écrire, marmonne quelque chose dans sa barbe, et se relève.")
                services.Affichage.EntreePourContinuer()
                print("Il vous regarde droit dans les yeux.")
                services.Affichage.EntreePourContinuer()
                print("Comme si il voyait quelque chose de terrible.")
                services.Affichage.EntreePourContinuer()
                print("Comme si il voyait... la chose derrière le masque.")
                services.Affichage.EntreePourContinuer()
                StopAllMusic()
                attendre(5)
                services.FloorMaker.StopAllVillageChannels()
                services.FloorMaker.InitialisationOfTownVariations()
                PlayMusicDeLetage()
                print("*Bonjour !*")
                services.Affichage.EntreePourContinuer()
                print("L'homme se rassoit, et continue de dessiner des symboles au sol.")
                services.Affichage.EntreePourContinuer()

            elif choix == 2:
                print("L'homme continue s'arrête d'écrire sur le sol, puis pointe du doigt un mot écrit en grandes lettres sur un pavé a proximité :")
                services.Affichage.EntreePourContinuer()
                print("*Le Chuchoteur, Mathématicien Probabiliste*")
                services.Affichage.EntreePourContinuer()
                print("Le Chuchoteur remarque votre regard interrogateur et soupire.")
                services.Affichage.EntreePourContinuer()
                print("*Je suis un mathématicien probabiliste. C'est a dire que je me base sur les faits, que j'essaye de trouver une tendance parmis ces faits, et que j'en tire des conclusions.*")
                services.Affichage.EntreePourContinuer()
                print("Le Chuchoteur vous regarde intensément, puis soupire de manière (très) audible.")
                services.Affichage.EntreePourContinuer()
                print("*Des choses étrangent se passent dans le Coliseum. Je dirait même plus : aléatoires. Moi j'essaye de comprendre comment ca marche afin de trouver la dispositions des étages ou l'ordre des monstres qui apparaissent.*")
                services.Affichage.EntreePourContinuer()
                print("*Tu as du remarquer la carte fournie au premier étage, pas vrai ? C'est une de mes inventions.*")
                services.Affichage.EntreePourContinuer()
                print("*Entre les fibres de papier, j'ai codé un algorithme magique complexe qui scanne ce que voit le porteur et en tire des conclusions sur la structure d'un étage, et l'endroit ou le porteur se trouve.*")
                services.Affichage.EntreePourContinuer()
                print("*Vu que c'est a chaque fois le même algorithme, on peut produire ces cartes en masse et les distribuer gratuitement a tout les nouveaux voyageurs !*")
                services.Affichage.EntreePourContinuer()
                print("*J'ai vendu ma création au Directeur de la Banque afin qu'il s'occupe de la production, et moi j'ai eu cette maison en échange.*")
                services.Affichage.EntreePourContinuer()
                print("*Mais la, je m'ennuie.*")
                services.Affichage.EntreePourContinuer()
                print("*Tout le monde se satisfait de pouvoir faire quelques étages avec ma carte, et ducoup, plus personne ne me donne de données. Et je ne peux pas améliorer mon algorithme sans ces données !*")
                services.Affichage.EntreePourContinuer()
                print("*Si seulement quelqu'un pouvait aller observer toute les salles des étages afin que je puisse améliorer les cartes pour qu'elles marchent sur les étages plus profond...*")
                services.Affichage.EntreePourContinuer()
                if not  services.Sove.ModifieTagsDansSove("Checke","Chuchoteur"):
                    print("Vous pensez au problème du chuchoteur, et une idée germe dans votre esprit !")
                    services.Affichage.EntreePourContinuer()
                    print("A partir de maintenant, a chaque fois que vous observez toute les salles d'un étage et que vous le finissez, vous vous rapellerez de la disposition de l'étage afin d'en parler au Chuchoteur !")
                    services.Affichage.EntreePourContinuer()
                    print("Le nombre d'étages connus est référé sous le nom de *Carte Mentale*. Plus vous en avez, plus vous pourrez améliorer la carte !")
                    services.Affichage.EntreePourContinuer()
                    services.Sove.ModifieTagsDansSove("Ajout","Chuchoteur")

            elif choix == 3:
                print("*La Réponse Mathématique Unique a la Vie et a l'Univers. Vous voulez savoir ce que c'est ?*")
                services.Affichage.EntreePourContinuer()
                print("Le Chuchoteur se rapproche de votre oreille, et vous chuchote quelque chose :")
                services.Affichage.EntreePourContinuer()
                print("*Une énorme perte de temps.*")
                services.Affichage.EntreePourContinuer()
                print("Vous jettez un regard blazé au Chuchoteur.")
                services.Affichage.EntreePourContinuer()
                print("*Bah quoi ?*\n*Comment voulez vous résumer le spectrum entier des évenements et lois qui régissent notre Univers ?*\n*Avec un nombre ?*\n*Quelle signification il aurait ce nombre ??*")
                services.Affichage.EntreePourContinuer()
                print("*Et puis ca serait quoi ?*\n*42 ?*")
                services.Affichage.EntreePourContinuer()
                print("*Non. Moi je dis qu'il faut se résoudre a la triste véritée .*")
                services.Affichage.EntreePourContinuer()

            elif choix == 5:
                break

            elif choix == 4:
                while True:
                    while True:
                        try:
                            liste_de_trades = [
                                "Carte",
                            ]
                            print(f"     -=Chuchoteur=-")
                            print(f"  Cartes Mentale : [{ services.Sove.ModifieDechetsDansSove('Nombre', 'Carte Mentale', None)}]\n\n")
                            numero = 1
                            for trade in liste_de_trades:
                                level_actuel_de_uppgrade =  services.Sove.ModifieLivraisonDansSove("Nombre", trade)
                                characteristique_de_luppgrade = ANNUAIREPRIXVILLAGE[trade]
                                if len(characteristique_de_luppgrade) == level_actuel_de_uppgrade:
                                    prix_de_luppgrade = "Impossible"
                                    print(f"{numero} - {trade} niv. MAX")
                                else:
                                    prix_de_luppgrade = characteristique_de_luppgrade[level_actuel_de_uppgrade]
                                    level_atteint = level_actuel_de_uppgrade + 1
                                    if len(characteristique_de_luppgrade) == level_atteint:
                                        level_atteint = "MAX"
                                    print(f"{numero} - {trade} niv. {level_actuel_de_uppgrade} ==) {trade} niv. {level_actuel_de_uppgrade + 1}")
                                    print("    Materiaux nécéssaires:")
                                    for materiau in prix_de_luppgrade:
                                        if materiau != "Emblème de la Fin":
                                            nombre_materiau_dans_sac = services.Sove.ModifieDechetsDansSove("Nombre",materiau)
                                        else :
                                            nombre_materiau_dans_sac = "Non Possédé" 
                                            if services.Sove.ModifieLivraisonDansSove("Nombre", materiau) >= 1 :
                                                nombre_materiau_dans_sac = "Possédé" 
                                        print(f"      - {prix_de_luppgrade[materiau]} {materiau} [{nombre_materiau_dans_sac}]")
                                print("\n")

                                numero += 1
                            print(f"\n{numero} - Retour\n")
                            choix = int(input("Faites votre choix avec les nombres : "))
                            ClearConsole()

                            if choix in range(1, numero + 1):
                                break

                        except ValueError:
                            ClearConsole()
                    
                    if choix == numero:
                        break

                    else:
                        # trouver le prix en materiau de luppgrade
                        objet_choisi = liste_de_trades[choix - 1]
                        level_actuel_de_uppgrade =  services.Sove.ModifieLivraisonDansSove("Nombre", objet_choisi)
                        characteristique_de_luppgrade = ANNUAIREPRIXVILLAGE[objet_choisi]
                        if len(characteristique_de_luppgrade) == level_actuel_de_uppgrade:
                            print("Impossible d'augmenter le niveau de cet objet.")
                            services.Affichage.EntreePourContinuer()
                        else:
                            prix_de_luppgrade = characteristique_de_luppgrade[level_actuel_de_uppgrade]

                            achat_possible = self.CheckIfEnoughMaterials(prix_de_luppgrade)

                            if not achat_possible:
                                print("Vous n'avez pas assez de materiaux !")
                                services.Affichage.EntreePourContinuer()

                            else:
                                self.BuyUppgrade(prix_de_luppgrade)

                                print(f"Vous murmurez vos souvenirs d'étages complets, et le Chuchoteur les dessine a la hate.")
                                print("Il regarde ensuite ses dessins avec un regard fou, faisant une croix sur certains nombres et reliant certaines salles entre elles.")
                                print("Puis, il sort un prototype de carte, sur laquelle sont écrit des millions de symboles différents, et chuchote quelques mots qui viennent se perdre dans les fibres de papier.")
                                print(f"*Ca y est ! J'ai trouvé !*\n*Les Cartes des prochains voyageurs devraient maintenant pouvoir afficher la structure de l'étage {level_actuel_de_uppgrade + 4} !*")
                                print("*Prend donc ce bon de livraison, au cas ou .*")
                                services.Affichage.EntreePourContinuer()

                                services.Sove.ModifieLivraisonDansSove("Ajout", objet_choisi)

    def DoFabricator(self):
        while True:
            while True:
                try:
                    print("     -=Fabricateur=-\n")
                    print("   Premier Materiau Inséré")
                    print("           Aucun\n")
                    print("   Deuxieme Materiau Inséré")
                    print("           Aucun\n\n")
                    numero = 1
                    liste_materiau = []
                    liste_materiau_temp =  services.Sove.ModifieDechetsDansSove("Donne", None, None)
                    for materiau in liste_materiau_temp:
                        if liste_materiau_temp[materiau] > 0:
                            liste_materiau.append(materiau)
                    if "Carte Mentale" in liste_materiau:
                        liste_materiau.remove("Carte Mentale")
                    for materiau in liste_materiau:
                        print(f"{numero} - Insérer [{materiau}] ({liste_materiau_temp[materiau]} dans sacoche)")
                        numero += 1
                    print(f"{numero} - Partir\n")
                    choix = int(input("Faites votre choix avec les nombres : "))
                    ClearConsole()
                    if choix in range(1, numero + 1):
                        break
                except ValueError:
                    ClearConsole()
            if choix == numero:
                break
            else:
                premier_materiau = liste_materiau[choix - 1]
                liste_materiau.pop(choix - 1)
                while True:
                    while True:
                        try:
                            print("     -=Fabricateur=-\n")
                            print("   Premier Materiau Inséré")
                            print(f"     {premier_materiau}\n")
                            print("   Deuxieme Materiau Inséré")
                            print("           Aucun\n\n")
                            numero = 1
                            for materiau in liste_materiau:
                                print(f"{numero} - Insérer [{materiau}] ({liste_materiau_temp[materiau]} dans sacoche)")
                                numero += 1
                            print(f"{numero} - Revenir en arrière\n")
                            choix = int(input("Faites votre choix avec les nombres : "))
                            ClearConsole()
                            if choix in range(1, numero + 1):
                                break
                        except ValueError:
                            ClearConsole()
                    if choix == numero:
                        break
                    else:
                        deuxieme_materiau = liste_materiau[choix - 1]

                        while True:
                            try:
                                print("     -=Fabricateur=-\n")
                                print("   Premier Materiau Inséré")
                                print(f"     {premier_materiau}\n")
                                print("   Deuxieme Materiau Inséré")
                                print(f"     {deuxieme_materiau}\n\n")
                                print(f"Voulez vous combiner [{premier_materiau}] avec [{deuxieme_materiau}] ?")
                                print("(Qu'il y aie un résultat ou pas, vous perdrez ces materiaux.)\n")
                                print("1 - Oui")
                                print("2 - Non\n")
                                choix = int(input("Faites votre choix avec les nombres : "))
                                ClearConsole()
                                if choix in [1, 2]:
                                    break
                            except ValueError:
                                ClearConsole()
                        if choix == 1:
                            print("Vous mettez vos materiaux dans la machine et la porte de la cabine se referme.")
                            services.Affichage.EntreePourContinuer()
                            FuseMaterials(premier_materiau, deuxieme_materiau)
                            break

                            






                    

    def DoColiseum(self):
        if not  services.Sove.ModifieTagsDansSove("Checke", "Passe de Combat") and  services.Sove.ModifieTagsDansSove("Checke", "Village Nuit"):
            print("Vous vous faites arrêter à l'entrée par un Punk de très grande taille.")
            print("*Pas de Passe, pas de combats. Dégage, moustique .*")
            services.Affichage.EntreePourContinuer()
        elif  services.Sove.ModifieTagsDansSove("Checke", "Passe de Combat") and  services.Sove.ModifieTagsDansSove("Checke", "Village Nuit"):
            print("Vous vous faites arreter à l'entrée par un Punk de très grande taille.")
            print("*Pas de Passe, pas de-*")
            services.Affichage.EntreePourContinuer()
            print("*Oh. My bad. Rentrez donc.*")
            services.Affichage.EntreePourContinuer()
        else:
            while True:
                while True:
                    liste_de_actions_deja_possedee =  services.Sove.ModifieActionsConnuesDansSove("Donne", None)
                    nombre_dactions_connues = len(liste_de_actions_deja_possedee)
                    if nombre_dactions_connues == 0:
                        if not  services.Sove.ModifieTagsDansSove("Checke", "Uppgrade Colisée") and not  services.Sove.ModifieTagsDansSove("Checke", "Carte de Membre (Basique)"):
                            services.Sove.ModifieTagsDansSove("Ajout", "Uppgrade Colisée")
                            niveau_de_colisee = 0
                            print("*Bienvenue au colisée , Pigeon !*")
                            services.Affichage.EntreePourContinuer()
                            print("*Ici, tu va pouvoir regarder des combats en temps réel ! Chique !*")
                            services.Affichage.EntreePourContinuer()
                            print("*Mais le batiment a un nouveau patron maintenant, et il s'apelle OSEILLE !*")
                            services.Affichage.EntreePourContinuer()
                            print("*Alors tu paye pour avoir ta carte de membre, tu paye pour voir tes combats, et une fois que t'en a assez vu, tu doit payer pour avoir une meilleure carte de membre, et ainsi de suite.*")
                            services.Affichage.EntreePourContinuer()
                            print("*Ta compris ?*\n*Non ?*\n*Pas mon problème !*")
                            services.Affichage.EntreePourContinuer()
                        niveau_de_colisee = 0
                    if  services.Sove.ModifieTagsDansSove("Checke", "Carte de Membre (Basique)") :
                        niveau_de_colisee = 1
                        liste_daction_que_lon_peut_avoir_a_ce_niveau = list(LISTEACTIONRANG1)
                    if  services.Sove.ModifieTagsDansSove("Checke", "Carte de Membre (Avancée)") :
                        niveau_de_colisee = 2
                        liste_daction_que_lon_peut_avoir_a_ce_niveau = list(LISTEACTIONRANG2)
                    if  services.Sove.ModifieTagsDansSove("Checke", "Carte de Membre (Exclusive)") :
                        niveau_de_colisee = 3
                        liste_daction_que_lon_peut_avoir_a_ce_niveau = list(LISTEACTIONRANG3)
                    if  services.Sove.ModifieTagsDansSove("Checke", "Carte de Membre (VVIP)") :
                        niveau_de_colisee = 4
                        liste_daction_que_lon_peut_avoir_a_ce_niveau = list(LISTEACTIONRANG4)
                    
                    for action in liste_de_actions_deja_possedee:
                        if action in liste_daction_que_lon_peut_avoir_a_ce_niveau:
                            liste_daction_que_lon_peut_avoir_a_ce_niveau.remove(action)


                    try:
                        print("     -=Colisée=-")
                        print(f"  Essences Astrales : { services.Sove.ModifieDechetsDansSove('Nombre', 'Essence Astrale', None)} \n")
                        if  services.Sove.ModifieTagsDansSove("Checke", "Uppgrade Colisée"):
                            print("1 - Améliorer son rang")
                        elif  services.Sove.ModifieTagsDansSove("Checke", "Maximum Colisée"):
                            print("1 - Assister a un combat (Plus de combats !)")
                        else:
                            print(f"1 - Assister à un combat [{niveau_de_colisee * 5} essences astrales]")
                        print("2 - Partir\n")
                        choix = int(input("Faites votre choix avec les nombres : "))
                        ClearConsole()
                        if choix in [1, 2]:
                            break
                    except ValueError:
                        ClearConsole()
                if choix == 2:
                    break
                elif choix == 1 and niveau_de_colisee > 2 and  services.Sove.ModifieTagsDansSove("Checke", "Village Jour"):
                        print("Hey, je devrais pas te le dire mais...")
                        services.Affichage.EntreePourContinuer()
                        print("On garde une liste des combats que les gens regardent.")
                        services.Affichage.EntreePourContinuer()
                        print("Si on voit que les gens regardent toujours les mêmes types de combats, on sait alors que ca va pas dans leur vie et qu'ils risquent de partir dans les Champs pour toujours.")
                        services.Affichage.EntreePourContinuer()
                        print("Ducoup, on fait en sorte d'interdire l'accès aux colisée pour les gens une fois qu'ils ont vu tout les types de combats d'une catégorie.")
                        services.Affichage.EntreePourContinuer()
                        print("Pourquoi je te dis ca ?")
                        services.Affichage.EntreePourContinuer()
                        print("Parce que là, t'a vu tout ce qu'y avait a voir.")
                        services.Affichage.EntreePourContinuer()
                        print("Donc si tu veux voir d'autres combats, de plus haut niveau je veux dire...")
                        print("Reviens la nuit.")
                        services.Affichage.EntreePourContinuer()
                elif choix == 1 and  services.Sove.ModifieTagsDansSove("Checke", "Uppgrade Colisée"):
                    if niveau_de_colisee >= 2 and  services.Sove.ModifieTagsDansSove("Checke", "Village Jour"):
                        print("Hey, je devrais pas te le dire mais...")
                        services.Affichage.EntreePourContinuer()
                        print("On garde une liste des combats que les gens regardent.")
                        services.Affichage.EntreePourContinuer()
                        print("Si on voit que les gens regardent toujours les mêmes types de combats, on sait alors que ca va pas dans leur vie et qu'ils risquent de partir dans les Champs pour toujours.")
                        services.Affichage.EntreePourContinuer()
                        print("Ducoup, on fait en sorte d'interdire l'accès aux colisée pour les gens une fois qu'ils ont vu tout les types de combats d'une catégorie.")
                        services.Affichage.EntreePourContinuer()
                        print("Pourquoi je te dis ca ?")
                        services.Affichage.EntreePourContinuer()
                        print("Parce que là, t'a vu tout ce qu'y avait a voir.")
                        services.Affichage.EntreePourContinuer()
                        print("Donc si tu veux voir d'autres combats, de plus haut niveau je veux dire...")
                        print("Reviens la nuit.")
                        services.Affichage.EntreePourContinuer()
                        if not  services.Sove.ModifieTagsDansSove("Checke", "Passe de Combat"):
                            services.Sove.ModifieTagsDansSove("Ajout", "Passe de Combat")
                            print("Avec ce passe de préférence, sinon ils te laisseront pas rentrer.")
                            print("Le punk vous tend un bout de carton aux reliures dorées.")
                            services.Affichage.EntreePourContinuer()
                            print("Vous obtenez le Passe de Combat !")
                            services.Affichage.EntreePourContinuer()
                    else:
                        print("*Les matchs de plus haute qualité, c'est pas pour les trucs dans ton genre.*\n*Va falloir cracher la monnaie si tu veut entrer dans la cour des grands, Bousin !*")
                        services.Affichage.EntreePourContinuer()
                        if niveau_de_colisee == 0:
                            print("*Pour une carte de membre basique, faut pas faire trop cher sinon les moucherons dans ton genre pourraient pas piffer leur thune.*")
                            print("*Disons... 10 essences astrales. Ouai, c'est suffisant !*")
                            services.Affichage.EntreePourContinuer()
                            prix = {"Essence Astrale" : 10}
                        elif niveau_de_colisee == 1:
                            print("*Pour une carte de membre avancée, on rentre dans les choux direct, sans prévenir !*")
                            print("*Alors tu te bouge et tu m'donne genre 15 essences astrales et 15 essences dorées !*")
                            services.Affichage.EntreePourContinuer()
                            prix = {"Essence Astrale" : 15, "Essence Dorée" : 15,}
                        elif niveau_de_colisee == 2:
                            print("*Pour une carte de membre exclusive, va falloir avoir plus de thunes. Mais c'est pas un problème si t'es là !*")
                            print("*J'vais réquisitionner 15 essences carmines pour l'interêt collectif, ta vu.*")
                            services.Affichage.EntreePourContinuer()
                            prix = {"Essence Carmine" : 15}
                        elif niveau_de_colisee == 3:
                            print("*T'es plus un péqueneau maintenant, t'es une vraie star ! Mais va falloir prouver que t'étais un combattant de ouf si tu veux monter de niveau.*")
                            print("*La carte VVIP elle coute 10 essences. Essences de quoi ? Bah toute les essences mon reuf !*")
                            print("*Vitalitée, Magie, Fortitude, Sagesse, Résistance, Dorée, Astrale, Carmine !*")
                            services.Affichage.EntreePourContinuer()
                            prix = {"Essence de Vitalitée" : 10, "Essence de Magie" : 10, "Essence de Fortitude" : 10, "Essence de Sagesse" : 10, "Essence de Résistance" : 10, "Essence Dorée" : 10, "Essence Astrale" : 10, "Essence Carmine" : 10, }
                        while True:
                            try:
                                print("*Tu paye ?*")
                                print("\n1 - Oui")
                                print("2 - Non\n")
                                choix = int(input("Faites votre choix avec les nombres : "))
                                ClearConsole()
                                if choix in [1, 2]:
                                    break
                            except ValueError:
                                ClearConsole()
                        if choix == 2:
                            print("*Ben tu dégage !*")
                            services.Affichage.EntreePourContinuer()
                        
                        elif choix == 1:

                            achat_possible = self.CheckIfEnoughMaterials(prix)

                            if not achat_possible:
                                print("*T'a pas assez, troufion !!*")
                                services.Affichage.EntreePourContinuer()

                            else:
                                print("*Donne moi ta came, et prend ton truc.*")
                                self.BuyUppgrade(prix)
                                print("Le punk prend vos matériaux avant de vous lancer une carte a la figure.")
                                services.Affichage.EntreePourContinuer()
                                services.Sove.ModifieTagsDansSove("Enleve", "Uppgrade Colisée")
                                if niveau_de_colisee == 0:
                                    print("Vous obtenez la Carte de Membre (Basique) !")
                                    services.Sove.ModifieTagsDansSove("Ajout", "Carte de Membre (Basique)")
                                elif niveau_de_colisee == 1:
                                    print("Vous obtenez la Carte de Membre (Avancée) !")
                                    services.Sove.ModifieTagsDansSove("Ajout", "Carte de Membre (Avancée)")
                                elif niveau_de_colisee == 2:
                                    print("Vous obtenez la Carte de Membre (Exclusive) !")
                                    services.Sove.ModifieTagsDansSove("Ajout", "Carte de Membre (Exclusive)")
                                elif niveau_de_colisee == 3:
                                    print("Vous obtenez la Carte de Membre (VVIP) !")
                                    services.Sove.ModifieTagsDansSove("Ajout", "Carte de Membre (VVIP)")
                                services.Affichage.EntreePourContinuer()


                elif choix == 1 and  services.Sove.ModifieTagsDansSove("Checke", "Maximum Colisée"):
                    print("*Désolé Golmon, ya pas de lunettes pour t'aider a lire sur la pancarte que t'a déjà vu tout ce que y'avait a voir ici.*")
                    services.Affichage.EntreePourContinuer()

                elif choix == 1:
                    if  services.Sove.ModifieDechetsDansSove("Limite", "Essence Astrale", (niveau_de_colisee * 5)):
                        liste_de_description_monstre = [
                            "un Gluant visqueux et suintant",
                            "un Feu Follet dansant gaiement",
                            "un Golem de Terre, concentré sur sa cible",
                            "une Ombre Tangible, preque invisible",
                            "un Clone de Verre et ses mouvements irréguliers",
                            "un Métroïde indescriptible a la forme alien",
                            "un Trienun et son fidèle Bandit Manchot",
                            "un Phénix Juvénile complètement équipé",
                            "un Rochemikaze prêt a exploser",
                            "un Loup de Glace grognant a l'approche de sa victime",
                            "un Voleur Félin silencieux, ténébreux, mysterieux",
                            "un Siffloteur volant gracieusement dans le ciel tel un serpent ailé",
                            "un Lapin du Désastre et ses yeux couleur de sang",
                            "un Cerf Voleur silencieux, ténébreux, mystérieux",
                            "un Aspiratrésor Blindé lançant son BIOS",
                            "un Gluant de Crystal aux courbes régulières et grand sourire",
                            "un Sixenun et sa fidèle Roulette",
                            "un Siffloteur de Jade volant gracieusement dans le ciel tel un serpent ailé",
                            "une Aurelionite éblouissant les gradins par son placage or",
                            "un Sacatrésor et son sourire malicieux",
                            "le Clone d'Obsidienne et ses protocoles",
                            "le Chevalier Pourpre en plein monologue",
                            "le Roi Amonrê, prométhée moderne",
                            "l'Apprentie, génie de la magie",
                            "le Bouffon, drapé d'une aura de folie",
                            "le Prince des Voleurs, encore débutant dans cet exercice",
                            "le Roi Déchu et son infame paranoïa",
                            "le grand, le musculeux, le Maitre Mage",
                            ]
                        description_monstre = random.choice(liste_de_description_monstre)

                        if description_monstre in [
                            "le Clone d'Obsidienne et ses protocoles",
                            "le Chevalier Pourpre en plein monologue",
                            "le Roi Amonrê, prométhée moderne",
                            "l'Apprentie, génie de la magie",
                            "le Bouffon, drapé d'une aura de folie",
                            "le Prince des Voleurs, encore débutant dans cet exercice",
                            "le Roi Déchu et son infame paranoïa",
                            "le grand, le musculeux, le Maitre Mage",
                        ]:
                            description_foule = "silencieuse"
                        else:
                            description_foule = "bruyante"
                        
                        liste_de_description_combat = [
                            "un jeune homme blond habillé de vert et coiffé d'un long chapeau pointu",
                            "une jeune femme dotée d'une armure futuriste orange et rouge",
                            "un être étrange sans bras ni jambe, et dont les membres sont pourtant accroché a son torse",
                            "un trentenaire doté d'un long manteau et d'une sorte de petit tournevis lumineux, et accompagné d'une jeune femme,",
                            "une femme avec des long cheveux blond et habillée avec une robe rose",
                            "une femme à l'aura divine, aux cheveux verts surmontés d'une couronne de lauriers dorés",
                            "un adolescent portant un Glock, tout de noir vetu, avec des gants rouges et un masque de carnaval blanc recouvrant seulement ses yeux",
                            "un enfant aux cheveux en piques, portant de grosses chaussures et une gigantesque clé jaune-argent",
                            "une petite boule rose toute joyeuse",
                            "un gros rat jaune avec une queue en forme d'éclair",
                            "un hérisson humanoïde bleu avec de grosses chaussures rouges et blanches",
                            "un jeune homme aux cheveux en pique, doté d'une gigantesque et brutale épée a deux main",
                            "un homme doté d'un épais manteau noir et d'une baguette magique, arborant une cicatrice sur le front",
                            "un vieillard a la longue barbe blanche, dotée d'un sceptre de bois noueux et d'un manteau blanc très épais",
                            "une femme blonde avec une paire de lunettes d'aviateurs sur la tête, a l'interieur d'un tank",
                            "une femme blonde dans un tracksuit jaune, armée d'un long katana",
                            "une trentenaire brune aux cheveux bouclés armée d'un fusil a impulsion, dotée d'un débardeur blanc taché de sang vert",
                            "un homme noir baraqué au crane chauve, bougeant ses pectoraux en rythme",
                            "un homme noir a la coiffure impeccable, lunettes de soleil, et dents... pointues ?",
                            "une trentenaire noire aux cheveux bouclés et regard puissant, arméee d'un katana parfaitement entretenu",
                            "un homme noir habillé avec des vêtements de shériff sur lequel sont brodé le nom *King Schultz*, et armé d'un révolver"
                        ]
                        description_combattant = random.choice(liste_de_description_combat)
                        action_a_apprendre = random.choice(liste_daction_que_lon_peut_avoir_a_ce_niveau)
                        liste_daction_que_lon_peut_avoir_a_ce_niveau.remove(action_a_apprendre)
                        print("Vous payez votre du et prenez place dans les gradins.")
                        services.Affichage.EntreePourContinuer()
                        print(f"Une foule {description_foule} attend avec impatience l'arrivée d'un combattant.")
                        services.Affichage.EntreePourContinuer()
                        print("Soudainement , vous entendez un bruit de pas sur le sable de l'Arène, et cette derniere change d'apparence !")
                        services.Affichage.EntreePourContinuer()
                        print(f"Vous apercevez {description_combattant}, s'avancant fièrement dans l'arène !")
                        services.Affichage.EntreePourContinuer()
                        print(f"De l'autre coté, vous distinguez la silhouette de son ennemi : {description_monstre} !")
                        services.Affichage.EntreePourContinuer()
                        print("Les sorts pleuvent, les techniques s'enchainent, les items sont tantot utilisés, tantot jetés !")
                        services.Affichage.EntreePourContinuer()
                        print("Et alors que le combat touche a sa fin, vous regardez avec intensité le Zeroual dans l'arène.")
                        services.Affichage.EntreePourContinuer()
                        print(f"Vous voyez l'action [{action_a_apprendre}] se faire de manière parfaite, et un déclic s'opère en vous !")
                        services.Affichage.EntreePourContinuer()
                        print("En analysant l'action en tant que spectateur, en se souvenant d'avoir fait l'action en tant que combattant...")
                        print("...vous comprenez finalement comment elle fonctionne, et son image est gravée a jamais dans votre esprit.")
                        services.Affichage.EntreePourContinuer()
                        print(f"Vous apprenez [{action_a_apprendre}] de manière permanente !")
                        print("Elle sera directement disponible lors de votre prochaine partie !")
                        services.Affichage.EntreePourContinuer()
                        print("Le combat se finit, la foule se disperse, et vous sortez du Colisée encore chamboulé par votre découverte.")
                        services.Affichage.EntreePourContinuer()
                        services.Sove.ModifieActionsConnuesDansSove("Ajout", action_a_apprendre)
                        services.Sove.ModifieDechetsDansSove("Enleve", "Essence Astrale", (niveau_de_colisee * 5))
                        if len(liste_daction_que_lon_peut_avoir_a_ce_niveau) == 0 and niveau_de_colisee != 4:
                            services.Sove.ModifieTagsDansSove("Ajout", "Uppgrade Colisée")
                            print("Le Punk vous arrête a la sortie.")
                            services.Affichage.EntreePourContinuer()
                            print("*Ca y est pigeon, ta vu tout ce qu'il y avait a voir a ce niveau.*")
                            services.Affichage.EntreePourContinuer()
                            print("*La prochaine fois, faudra augmenter ta carte !*")
                            services.Affichage.EntreePourContinuer()
                        elif len(liste_daction_que_lon_peut_avoir_a_ce_niveau) == 0 and niveau_de_colisee == 4:
                            services.Sove.ModifieTagsDansSove("Ajout", "Maximum Colisée")
                            print("Le Punk vous arrête a la sortie.")
                            services.Affichage.EntreePourContinuer()
                            print("*Ca y est. Tu as vu tout ce qu'il y avait a voir.*")
                            services.Affichage.EntreePourContinuer()
                            print("*Pleure pas, on ne te jette pas du Colisée pour l'éternitée non plus !*")
                            services.Affichage.EntreePourContinuer()
                            print("*Si tu revient d'ici une centaine d'année, on te laissera voir les match depuis de tout début. Et on te fera même une petite ristourne !*")
                            services.Affichage.EntreePourContinuer()
                            print("*Maintenant, file !")
                            services.Affichage.EntreePourContinuer()
                    else:
                        print("*Tu tente quoi la ? Un braquage ? J'vais t'braquer moi tu va voir !*")
                        services.Affichage.EntreePourContinuer()

    def DoChamane(self):
        benediction_actuelle = RecupereBenedictionEnCours()
        malediction_actuelle = RecupereMaledictionEnCours()
        while True:
            while True:
                print("     -=La Chamane=-\n\n")
                print("1 - Parler")
                print("2 - Malédictions")
                print("3 - Bénédictions")
                print("4 - Partir\n")
                choix = int(input("Faites votre choix avec les nombres : "))
                ClearConsole()
                if choix in range(1, 5):
                    break
            if choix == 4:
                break
            if choix == 1 :
                print("*Bonsoir, avatar.*")
                services.Affichage.EntreePourContinuer()
                print("*Aime tu te promener dans la Crypte ?*")
                services.Affichage.EntreePourContinuer()
                print("*Premiers arrivés ici, nous pensions que le salut résidait dans la prière, envers une déitée sans nom et sans visage qui répondrait a notre désespoir...*")
                services.Affichage.EntreePourContinuer()
                print("*...et tu te trouve actuellement dans son sanctuaire.*")
                services.Affichage.EntreePourContinuer()
                print("Vous regardez nerveusement autour de vous, et décernez les contours de milions de visages en peine dans la roche.")
                services.Affichage.EntreePourContinuer()
                print("*Calme donc ton esprit, ce ne sont que de simples ombres d'une époque bien lointaine.*")
                services.Affichage.EntreePourContinuer()
                print("*De petites vaguelette a la surface d'un étang infiniment grand, dans lequel nous avons laché une pierre il y a bien des millénaires..*")
                services.Affichage.EntreePourContinuer()
                print("*..ressens-tu la surface de l'eau s'élever et redescendre, avatar ?*")
                services.Affichage.EntreePourContinuer()
                print("Vous sentez une frisson parcourir votre dos, comme une main qui suit les courbes de la chair.")
                services.Affichage.EntreePourContinuer()
                print("*Te voila devant moi ce soir, vétu seulement de la volontée de celles et ceux qui empruntent ton nom.*")
                services.Affichage.EntreePourContinuer()
                print("*Mais si tu tente de satisfaire les esprits de tes predecesseurs emmurés ici en traversant le coliseum orné de leur terreurs...*")
                services.Affichage.EntreePourContinuer()
                print("*...tu pourra alors te draper dans leur lumière.*\n*Devenir ce dieu sans visage qui parcourt leur tombeau avec le poids de leurs prières sur tes épaules.*")
                services.Affichage.EntreePourContinuer()
                print("*Abat le Maitre Mage armé de malédictions, et tu pourras bénéficier de mes bénédictions.*")
                services.Affichage.EntreePourContinuer()
                print("*Le choix viendra d'en haut, mais les mots t'apartiennent, avatar.*")
                services.Affichage.EntreePourContinuer()
            elif choix == 2:
                while True:
                    while True:
                        try:
                            
                            benediction_actuelle = RecupereBenedictionEnCours()
                            malediction_actuelle = RecupereMaledictionEnCours()
                            print("     -=La Chamane=-")
                            print(f" Malédiction Activée : [{malediction_actuelle}] \n\n")
                            print("1 - Activer la Malédiction [Apyre]")
                            print("     # Les sorts et techniques de feu ne fonctionnent plus\n")
                            print("2 - Activer la Malédiction [Infrigérable]")
                            print("     # Les sorts et techniques de glace ne fonctionnent plus\n")
                            print("3 - Activer la Malédiction [Isolant]")
                            print("     # Les sorts et techniques de foudre ne fonctionnent plus\n")
                            print("4 - Activer la Malédiction [Arénacé]")
                            print("     # Les sorts et techniques de terre ne fonctionnent plus\n")
                            print("5 - Activer la Malédiction [Anoxique]")
                            print("     # Les sorts et techniques physiques ne fonctionnent plus\n")
                            print("6 - Activer la Malédiction [Exsangue]")
                            print("     # Les sorts et techniques de sang ne fonctionnent plus\n")
                            print("7 - Activer la Malédiction [Impotent]")
                            print("     # Les ennemis sont invincibles pendant les 3 premiers tours\n")
                            print("8 - Activer la Malédiction [Chronophage]")
                            print("     # Affecte le personnage avec le *Tachyon Instable*")
                            print("     # Le tachyon charge avec les actions et se décharge avec l'inaction.")
                            print("     # Si la charge arrive a 100% , c'est la mort.\n")
                            print("9 - Activer la Malédiction [Sparifique]")
                            print("     # Ne gagne plus d'artefact, sauf en tuant les boss.\n")
                            print("10 - Activer la Malédiction [Ascétique]")
                            print("     # Diminue les gains de gold de 50%, regagne 10% de vie a chaque début de combat.\n")
                            print("11 - Activer la Malédiction [Pur]")
                            print("     # Ne peut pas acheter de talents.\n")
                            print("12 - Activer la Malédiction [Ordinaire]")
                            print("     # Ne peut plus enchanter de sorts ou techniques.\n")
                            print("13 - Désactiver la Malédiction actuelle\n")
                            print("14 - Revenir au menu principal\n")
                            choix = int(input("Faites votre choix avec les nombres : "))
                            ClearConsole()
                            if choix in range(1, 15):
                                break
                        except ValueError:
                            ClearConsole()
                    if choix == 14:
                        break
                    elif choix == 13:
                        if malediction_actuelle != "Aucun":
                             services.Sove.ModifieTagsDansSove("Enleve", malediction_actuelle)
                    else:
                        liste_malediction = RecupereMaledictionEnCours("liste")
                        malediction_choisie = liste_malediction[choix - 1]
                        if malediction_actuelle != "Aucun":
                             services.Sove.ModifieTagsDansSove("Enleve", malediction_actuelle)
                        services.Sove.ModifieTagsDansSove("Ajout", malediction_choisie)
            elif choix == 3:
                while True:
                    while True:
                        try:
                            
                            benediction_actuelle = RecupereBenedictionEnCours()
                            malediction_actuelle = RecupereMaledictionEnCours()
                            print("     -=La Chamane=-")
                            print(f" Bénédiction Activée : [{benediction_actuelle}] \n\n")

                            if  services.Sove.ModifieTagsDansSove("Checke", "Debloque Incandescent"):
                                print("1 - Activer la Bénédiction [Incandescent]")
                                print("     # Les sorts et techniques de feu font 75% de dégat supplémentaire.\n")
                            else:
                                print("1 - Activer la Bénédiction [ACCES NON AUTORISE]\n")

                            if  services.Sove.ModifieTagsDansSove("Checke", "Debloque Glaciaire"):
                                print("2 - Activer la Bénédiction [Glaciaire]")
                                print("     # Les sorts et techniques de glace font 75% de dégat supplémentaire.\n")
                            else:
                                print("2 - Activer la Bénédiction [ACCES NON AUTORISE]\n")

                            if  services.Sove.ModifieTagsDansSove("Checke", "Debloque Conducteur"):
                                print("3 - Activer la Bénédiction [Conducteur]")
                                print("     # Les sorts et techniques de foudre font 75% de dégat supplémentaire.\n")
                            else:
                                print("3 - Activer la Bénédiction [ACCES NON AUTORISE]\n")

                            if  services.Sove.ModifieTagsDansSove("Checke", "Debloque Rocailleux"):
                                print("4 - Activer la Bénédiction [Rocailleux]")
                                print("     # Les sorts et techniques de terre font 75% de dégat supplémentaire.\n")
                            else:
                                print("4 - Activer la Bénédiction [ACCES NON AUTORISE]\n")
                                
                            if  services.Sove.ModifieTagsDansSove("Checke", "Debloque Musclé"):
                                print("5 - Activer la Bénédiction [Musclé]")
                                print("     # Les sorts et techniques physique font 75% de dégat supplémentaire.\n")
                            else:
                                print("5 - Activer la Bénédiction [ACCES NON AUTORISE]\n")

                            if  services.Sove.ModifieTagsDansSove("Checke", "Debloque Sain"):
                                print("6 - Activer la Bénédiction [Sain]")
                                print("     # Les sorts et techniques de sang font 75% de dégat supplémentaire.\n")
                            else:
                                print("6 - Activer la Bénédiction [ACCES NON AUTORISE]\n")

                            if  services.Sove.ModifieTagsDansSove("Checke", "Debloque Omnipotent"):
                                print("7 - Activer la Bénédiction [Omnipotent]")
                                print("     # Gagne 1 point de vie/mana max par monstre tué.\n")
                            else:
                                print("7 - Activer la Bénédiction [ACCES NON AUTORISE]\n")

                            if  services.Sove.ModifieTagsDansSove("Checke", "Debloque Accumulateur de Tachyon"):
                                print("8 - Activer la Bénédiction [Accumulateur de Tachyon]")
                                print("     # Donne l'artefact *Accumulateur de Tachyon* au personnage.")
                                print("     # Le tachyon se charge au fur et a mesure du temps et des actions.")
                                print("     # Si une action est effectuée sans assez de ressource (endurance/mana),")
                                print("     # 50% de charge seront utilisés a la place, rendant l'action gratuite.")
                                print("     # Si la charge dépasse 110%, elle est utilisée pour bénir le personnage pendant 5 tours.\n")
                            else:
                                print("8 - Activer la Bénédiction [ACCES NON AUTORISE]\n")

                            if  services.Sove.ModifieTagsDansSove("Checke", "Debloque Polyvalent"):
                                print("9 - Activer la Bénédiction [Polyvalent]")
                                print("     # Donne 1 artefact supplémentaire gratuit a chaque début d'étage.\n")
                            else:
                                print("9 - Activer la Bénédiction [ACCES NON AUTORISE]\n")

                            if  services.Sove.ModifieTagsDansSove("Checke", "Debloque Materiel"):
                                print("10 - Activer la Bénédiction [Materiel]")
                                print("     # Les gains de gold augmentent de 100%.\n")
                            else:
                                print("10 - Activer la Bénédiction [ACCES NON AUTORISE]\n")

                            if  services.Sove.ModifieTagsDansSove("Checke", "Debloque Augmenté"):
                                print("11 - Activer la Bénédiction [Augmenté]")
                                print("     # Le personnage commence avec toute les affinités élémentaires déja acquises.\n")
                            else:
                                print("11 - Activer la Bénédiction [ACCES NON AUTORISE]\n")

                            if  services.Sove.ModifieTagsDansSove("Checke", "Debloque Extraordinaire"):
                                print("12 - Activer la Bénédiction [Extraordinaire]")
                                print("     # Une action (sort ou technique) sera enchanté gratuitement a chaque début d'étage.\n")
                            else:
                                print("12 - Activer la Bénédiction [ACCES NON AUTORISE]\n")

                            print("13 - Désactiver la Bénédiction actuelle\n")
                            print("14 - Revenir au menu principal\n")
                            choix = int(input("Faites votre choix avec les nombres : "))
                            ClearConsole()
                            if choix in range(1, 15):
                                break
                        except ValueError:
                            ClearConsole()
                    if choix == 14:
                        break
                    elif choix == 13:
                        if malediction_actuelle != "Aucun":
                             services.Sove.ModifieTagsDansSove("Enleve", benediction_actuelle)
                    else:
                        liste_benediction = RecupereBenedictionEnCours("liste")
                        benediction_choisie = liste_benediction[choix - 1]
                        if RegardeSiBenedictionDisponible(benediction_choisie):
                            if benediction_actuelle != "Aucun":
                                services.Sove.ModifieTagsDansSove("Enleve", benediction_actuelle)
                            services.Sove.ModifieTagsDansSove("Ajout", benediction_choisie)
                        else:
                            print("ACCES NON AUTORISE")
                            print("TERMINEZ UNE PARTIE AVEC LA MALEDICTION CORRESPONDANTE")
                            services.Affichage.EntreePourContinuer()

                        
                    
    def DoAncien(self):
        while True:
            while True:
                try:
                    print("     -=L'Ancien=-")
                    print(f"  Essences Carmine : { services.Sove.ModifieDechetsDansSove('Nombre', 'Essence Carmine', None)} \n\n")
                    print("1 - Parler")
                    print("2 - Ecouter le vieil homme parler (1 Essence Carmine)")
                    print("3 - Faire le point sur les indices")
                    print("4 - Améliorer son équipement")
                    print("5 - Partir\n")
                    choix = int(input("Faites votre choix avec les nombres : "))
                    ClearConsole()
                    if choix in range(1, 6):
                        break
                except ValueError:
                    ClearConsole()
                    
            if choix == 1:
                print("Vous posez une question a l'homme, mais il ne vous répond pas.")
                services.Affichage.EntreePourContinuer()
                print("Ses yeux perdus dans la lumière de la lune, ses cheveux soyeux, vous avez l'impression de regarder une peinture...")
                services.Affichage.EntreePourContinuer()
                print("Soudainement, il tourne la tête vers vous...")
                services.Affichage.EntreePourContinuer()
                if not  services.Sove.ModifieTagsDansSove("Checke", "Livre de la Cigogne Blanche"):
                    services.Sove.ModifieTagsDansSove("Ajout", "Livre de la Cigogne Blanche")
                    print("IL pose ses mains sur votre crane, et vous sentez le mod ne t oue   r    n")
                    services.Affichage.EntreePourContinuer()
                    print("ieee            er          [SSS]")
                    services.Affichage.EntreePourContinuer()
                    print("[SSSS]      [ss]     [SSSYSSS]")
                    services.Affichage.EntreePourContinuer()
                    print("[SSSSSSYSTEME OVERRIDEEE]")
                    services.Affichage.EntreePourContinuer()
                    print("[TELEEECHARGEEMous regardez l'ENT EN CcafaitmalcafaitmalcafaitmalOURS]")
                    services.Affichage.EntreePourContinuer()
                    print("[TELECHARGaaaaaaaaEMENT TERMINE]")
                    EcrireDansLivreCigogneBlanche()
                    services.Affichage.EntreePourContinuer()
                    print("L'homme enlève ses doigts de votre crane.")
                    services.Affichage.EntreePourContinuer()
                    print("Le monde arrête de tourner.")
                    services.Affichage.EntreePourContinuer()
                    print("*..l disait donc vrai...*")
                    services.Affichage.EntreePourContinuer()
                    print("Vous regardez l'homme en deux crachotements.")
                    services.Affichage.EntreePourContinuer()
                    print("...voici un cadeau.\ntu ne le verra pas, mais ce n'est pas ...grave.")
                    services.Affichage.EntreePourContinuer()
                    print("car c'est un cadeau pour toi, pas pour toi.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous avez l'impression que quelque chose a lu vos pensées.")
                    services.Affichage.EntreePourContinuer()
                    print("...viens..quand tu aura vu des choses...")
                    services.Affichage.EntreePourContinuer()
                    print(".je le mettrais a jour...")
                    services.Affichage.EntreePourContinuer()
                    print("...le...")
                    services.Affichage.EntreePourContinuer()
                    print("l'Ancien se retourne, et continue de regarder la lune.")
                    services.Affichage.EntreePourContinuer()
                    print("...le livre de la cigogne blanche.\nle dernier espoir pour que quelqu'un arrête le cauchemard.")
                    services.Affichage.EntreePourContinuer()
                    print("...")
                    services.Affichage.EntreePourContinuer()
                    print("...oh.")
                    services.Affichage.EntreePourContinuer()
                    print("...je vois.")
                    services.Affichage.EntreePourContinuer()
                    print("l'Ancien esquisse un sourire.")
                    services.Affichage.EntreePourContinuer()
                    print("la cigogne est blanche...")
                    services.Affichage.EntreePourContinuer()
                    print("...blanche comme la lune.")
                    services.Affichage.EntreePourContinuer()
                else:
                    print("Il pose aa aal")
                    services.Affichage.EntreePourContinuer()
                    print("[SSSYSTEMM Osa main sur votre craneVERRIDE]")
                    services.Affichage.EntreePourContinuer()
                    print("[SYSTEM : Le livre de la cigogne blanche a été mis a jour avec vos connaissances !]")
                    services.Affichage.EntreePourContinuer()
                    print("L'homme retire sa main de votre tête, et le monde s'arrête de tourner.")
                    services.Affichage.EntreePourContinuer()
                    EcrireDansLivreCigogneBlanche()
                print("...")
                services.Affichage.EntreePourContinuer()
                print("..le fabricateur...")
                services.Affichage.EntreePourContinuer()
                print("...apporte moi le sang des dieux, et j'essayerais de me rappeler ce qui peut être fusionné...")
                services.Affichage.EntreePourContinuer()
                print("...")
                services.Affichage.EntreePourContinuer()
                print("L'Ancien se replonge dans un silence lourd de conséquence.")
                services.Affichage.EntreePourContinuer()
                

            elif choix == 2 and  services.Sove.ModifieDechetsDansSove("Limite", "Essence Carmine", 1):
                liste_de_recettes_entendues = services.Sove.ModifieRecettesDansSove("Donne", None)
                liste_de_recettes_possibles = []
                for number in range(0, 17):
                    liste_de_recettes_possibles.append(number)
                for numero_de_rumeur in liste_de_recettes_possibles:
                    if numero_de_rumeur in liste_de_recettes_entendues:
                        liste_de_recettes_possibles.remove(numero_de_rumeur)

                liste_de_histoires = [
                    "de contrées sauvages, de dragons ayant volé une citée d'or et de nains, et d'une longue traversée de ces contrées par un groupe hétéroclite d'aventuriers.",
                    "d'une grande caverne enfermant des monstres amicaux, et de l'enfant qui a conquit la caverne et le coeur des habitants par sa bontée et sa gentillesse. ",
                    "d'un royaume en ruine, de peuples éparpillés aux quatre coins de sa carte, et des blessures dans le paysage laissées par une gigantesque bête de malice attendant son heure dans un chateau de pierre et d'obsidienne.",
                    "de sons familiers, d'une femme aveugle attirée dans une maison hantée, et de la perception dont elle a fait preuve pour s'en sortir.",
                    "d'un homme chamboulé, amnésique, dans un chateau de poussière et de monstres, armé seulement d'une lanterne à amadou pour affronter les ténèbres de son histoire.",
                    "de vallées oubliées, nichées sur le toit du monde, redécouvertes par une archéologue intrépide qui survit a toute ses rencontre grace a sa détermination, son cran, et ses méthodes de survivaliste.",
                    "d'un homme aigris, témoin d'une époque que sa fille de coeur ne connaitra jamais, alors qu'il navigue sur les terres de son passé entre le danger des hommes, et le dangers de champignons parasitaires.",
                    "d'un groupe hétéroclite de personnes tombées sur une planète hostile, chassés par des êtres qui manipulent la réalité, alors qu'il regardent le soir les vestiges de leur humanité tomber de leur vaisseau spatial comme autant de gouttes dans une pluie de chair et de sang.",
                    "d'un enfant, écrasé par la peine, la honte, et le regret, se réfugiant dans un monde imaginaire ou son enfance prend vie, sans pour autant réussir a échapper a la culpabilité qui lui tord les veines et la haine envers lui même qui touche son coeur comme le couteau qui carresse son abdomen tout les soirs.",
                    "d'une jeune rock-star, modifiée pour la récolte de dechets, et qui se sert de sa vision du monde calée sur le rhytme de la musique qui fait battre son coeur pour déjouer les plans d'une méga corporation avec l'aide d'un groupe de hackeur.",
                    "d'une feuille solitaire qui revient encore et toujours a la vie alors qu'elle tombe de son arbre mort, voyageant a travers l'espace et le temps accompagné toujours par quelqu'un, et vouant son existance a la protection de la terre contre tout les dangers.",
                ]
                histoire = random.choice(liste_de_histoires)
                print(f"Vous donnez une essence carmine a l'ancien, et celui ci commence a raconter une de ses nombreuses histoires...")
                print(f"Quelque chose a propos {histoire}.")
                services.Affichage.EntreePourContinuer()

                if len(liste_de_recettes_possibles) == 0:
                    print("Mais il n'y a plus rien d'utile dans ce qu'il dit.")
                    services.Affichage.EntreePourContinuer()
                
                else:
                    services.Sove.ModifieDechetsDansSove("Enleve","Essence Carmine",1)
                    numero_de_recette_entendue = random.choice(liste_de_recettes_possibles)
                    recette = LISTERECETTES[numero_de_recette_entendue]
                    print("Alors que vous écoutez attentivement les divagations de l'homme, quelque chose vous interpelle dans les mots utilisés !")
                    services.Affichage.EntreePourContinuer()
                    print("Vous imprimez dans votre esprit les mots suivants :")
                    services.Sove.ModifieRecettesDansSove("Ajout", numero_de_recette_entendue)
                    print(recette)
                    services.Affichage.EntreePourContinuer()



            elif choix == 2:
                print("Vous cherchez quelque chose d'autre a donner a l'Ancien, mais il met sa main sur votre sacoche.\nIl ne vous ouvrira les portes de son esprit seulement contre des essences carmines.")
                services.Affichage.EntreePourContinuer()

            elif choix == 3:
                print("Vous faites le point sur les indices entendus :\n")
                liste_de_recettes_entendues = services.Sove.ModifieRecettesDansSove("Donne", None)

                for numero_de_la_recette in liste_de_recettes_entendues:
                    print(LISTERECETTES[numero_de_la_recette])
                    print("")
                    
                print("\n")
                services.Affichage.EntreePourContinuer()

            elif choix == 5:
                break

            elif choix == 4:
                while True:
                    while True:
                        try:
                            liste_de_trades = [
                                "Sacoche",
                                "Emblème de la Fin",
                            ]
                            print(f"     -=L'Ancien=-\n\n")
                            numero = 1
                            for trade in liste_de_trades:
                                level_actuel_de_uppgrade =  services.Sove.ModifieLivraisonDansSove("Nombre", trade)
                                characteristique_de_luppgrade = ANNUAIREPRIXVILLAGE[trade]
                                if len(characteristique_de_luppgrade) == level_actuel_de_uppgrade:
                                    prix_de_luppgrade = "Impossible"
                                    print(f"{numero} - {trade} niv. MAX")
                                else:
                                    prix_de_luppgrade = characteristique_de_luppgrade[level_actuel_de_uppgrade]
                                    level_atteint = level_actuel_de_uppgrade + 1
                                    if len(characteristique_de_luppgrade) == level_atteint:
                                        level_atteint = "MAX"
                                    print(f"{numero} - {trade} niv. {level_actuel_de_uppgrade} ==) {trade} niv. {level_actuel_de_uppgrade + 1}")
                                    print("    Materiaux nécéssaires:")
                                    for materiau in prix_de_luppgrade:
                                        if materiau != "Emblème de la Fin":
                                            nombre_materiau_dans_sac = services.Sove.ModifieDechetsDansSove("Nombre",materiau)
                                        else :
                                            nombre_materiau_dans_sac = "Non Possédé" 
                                            if services.Sove.ModifieLivraisonDansSove("Nombre", materiau) >= 1 :
                                                nombre_materiau_dans_sac = "Possédé" 
                                        print(f"      - {prix_de_luppgrade[materiau]} {materiau} [{nombre_materiau_dans_sac}]")
                                print("\n")

                                numero += 1
                            print(f"\n{numero} - Retour\n")
                            choix = int(input("Faites votre choix avec les nombres : "))
                            ClearConsole()

                            if choix in range(1, numero + 1):
                                break

                        except ValueError:
                            ClearConsole()
                    
                    if choix == numero:
                        break

                    else:
                        # trouver le prix en materiau de luppgrade
                        objet_choisi = liste_de_trades[choix - 1]
                        level_actuel_de_uppgrade =  services.Sove.ModifieLivraisonDansSove("Nombre", objet_choisi)
                        characteristique_de_luppgrade = ANNUAIREPRIXVILLAGE[objet_choisi]
                        if len(characteristique_de_luppgrade) == level_actuel_de_uppgrade:
                            print("Impossible d'augmenter le niveau de cet objet.")
                            services.Affichage.EntreePourContinuer()
                        else:
                            prix_de_luppgrade = characteristique_de_luppgrade[level_actuel_de_uppgrade]

                            achat_possible = self.CheckIfEnoughMaterials(prix_de_luppgrade)

                            if not achat_possible:
                                print("Vous n'avez pas assez de materiaux !")
                                services.Affichage.EntreePourContinuer()

                            else:
                                self.BuyUppgrade(prix_de_luppgrade)

                                print(f"L'ancien vous regarde, et vous voyez une larme perler dans ses yeux.")
                                print("Il se retourne alors, prend quelque chose derriere lui, et vous le tend.")
                                services.Affichage.EntreePourContinuer()
                                if objet_choisi == "Sacoche":
                                    print("Vous obtenez la Sacoche !")
                                    print("Cet objet plein de souvenirs interfere avec tout ce que vous tenez comme acquis dans ce monde.")
                                    print("Vous pouvez maintenant obtenir des essences carmines a votre mort, pour chaque paquets de 5 redcoins !")
                                else:
                                    print("Vous obtenez l'Emblème de la Fin !")
                                    print("Ce blason infiniment précieux vous octroie la même autoritée que les tout premiers aventuriers, et vous permet d'ameliorer votre équipement a un tout autre niveau !")
                                services.Affichage.EntreePourContinuer()
                                services.Sove.ModifieLivraisonDansSove("Ajout", objet_choisi)


    def DoHotel(self):
        while True:
            while True:
                liste_des_tags =  services.Sove.ModifieTagsDansSove("Donne", None)
                try:
                    print("     -=Saloon=-")
                    print(f"  Essences Dorée : { services.Sove.ModifieDechetsDansSove('Nombre', 'Essence Dorée', None)}")
                    if not "Clé de la Chambre" in liste_des_tags:
                        print(f"  Essences Astrales : { services.Sove.ModifieDechetsDansSove('Nombre', 'Essence Astrale', None)}")
                    print("\n")
                    if "Clé de la Chambre" in liste_des_tags:
                        print("1 - Dormir")
                    else:
                        print("1 - Acheter une chambre (50 essences dorées + 50 essences astrales)")
                    print("2 - Prendre a boire (1 essence dorée)")
                    print("3 - Faire le point sur les rumeurs")
                    print("4 - Partir\n")
                    choix = int(input("Faites votre choix avec les nombres : "))
                    ClearConsole()
                    if choix in range(1, 5):
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1 and not "Clé de la Chambre" in liste_des_tags:
                if  services.Sove.ModifieDechetsDansSove("Limite","Essence Dorée",50) and  services.Sove.ModifieDechetsDansSove("Limite","Essence Astrale",50):
                    print("Vous tendez les materiaux a la réceptioniste, et elle vous donne une clé en échange.")
                    services.Affichage.EntreePourContinuer()
                    print("Vous obtenez la Clé de la Chambre !\nVous pouvez maintenant aller dormir dans une des chambres de l'hotel !")
                    services.Sove.ModifieDechetsDansSove("Enleve","Essence Dorée",50)
                    services.Sove.ModifieDechetsDansSove("Enleve","Essence Astrale",50)
                    services.Sove.ModifieTagsDansSove("Ajout", "Clé de la Chambre")
                    services.Affichage.EntreePourContinuer()
                else:
                    print("Vous n'avez pas assez de matériaux !")
                    services.Affichage.EntreePourContinuer()
                    
            elif choix == 1:
                print("Vous montez dans votre chambre et tombez lourdement sur le lit !")
                print("C'est moelleux...si doux... et vous etes tellement.. tellement.....")
                services.Affichage.EntreePourContinuer()
                StopAllMusic()
                print("...fatigué......")
                attendre(2)
                ClearConsole()
                if "Village Jour" in liste_des_tags:
                    PlaySound("nighty")
                    attendre(5.5)
                    print("Quand vous vous réveillez, vos yeux sont accueilli par la douce lueur d'une lune fixée dans le ciel.")
                    services.Affichage.EntreePourContinuer()
                    services.Sove.ModifieTagsDansSove("Ajout","Village Nuit")
                    services.Sove.ModifieTagsDansSove("Enleve","Village Jour")
                elif "Village Nuit" in liste_des_tags:
                    PlaySound("daythy")
                    attendre(3.9)
                    print("Quand vous vous réveillez, vos oreilles sont accueilli par le bruit de la rue bondée en dessous.")
                    services.Affichage.EntreePourContinuer()
                    services.Sove.ModifieTagsDansSove("Ajout","Village Jour")
                    services.Sove.ModifieTagsDansSove("Enleve","Village Nuit")
                StopAllMusic()
                services.FloorMaker.StopAllVillageChannels()
                services.FloorMaker.InitialisationOfTownVariations()
                PlayMusicDeLetage()
                audio.CHANNELMUSIQUEDEBASE.set_volume(0.5)
                PermanentPlaySFX("noise")

            elif choix == 2 and  services.Sove.ModifieDechetsDansSove("Limite", "Essence Dorée", 1):
                liste_de_rumeurs_entendues = services.Sove.ModifieRumeursDansSove("Donne", None)
                liste_de_rumeurs_possibles = []
                if "Village Jour" in liste_des_tags:
                    for number in range(0, 26):
                        liste_de_rumeurs_possibles.append(number)
                elif "Village Nuit" in liste_des_tags:
                    for number in range(26, 51):
                        liste_de_rumeurs_possibles.append(number)
                liste_de_rumeurs_possibles = [
                    numero for numero in liste_de_rumeurs_possibles
                    if numero not in liste_de_rumeurs_entendues
                ]

                liste_de_boissons = ["Diabolo Pêche", "Diabolo Kiwi", "Diabolo Citron", "Diabolo Fraise", "Jus de Cactus", "Jus de Fruit", "Smoothie au Brocoli", "Jus de Tomate", "Tabasco Extra-Fort", "Mayonnaise", "l'Air Pur qui Habite les Montagnes", "Cette Odeur de Vienoisserie devant les Boulangeries le Matin", "Lave en Fusion (sans sucre)", "Glaçons", "Plutonium Enrichi", "Pétillant a la Grenadine", "Thé Vert", "Thé Verre", "Troie", "Filaments", "Fromage Rapé", "Particules Elementaires (sans alcool)", "Menthe de Sirop", "Café (sans cafféine) (sans gluten) (sans sucre) (sans alcool) (sans eau) (sans grains de café) (sans café) (sans verre)", "Lait d'Amandes", "Chloroforme", "Sel", "Poivre", "Poussière et Autres Saletées Récupérées Sur Le Comptoir", "Terre", "Rien Du Tout (vous vouliez juste faire plaisir a la barman.. barwoman ?)", "verre de verre de verre de verre de verre de verre de verre de verre de verre de verre de verre de verre d'eau"]
                boisson = random.choice(liste_de_boissons)
                print(f"Vous commandez un verre de {boisson} a la barman (barwoman ?), et le sirotez en tendant l'oreille...")
                services.Affichage.EntreePourContinuer()

                if len(liste_de_rumeurs_possibles) == 0:
                    print("...mais tout ce que vous entendez, vous l'aviez déja entendu auparavant.")
                    services.Affichage.EntreePourContinuer()
                
                else:
                    services.Sove.ModifieDechetsDansSove("Enleve","Essence Dorée",1)
                    numero_de_rumeur_entendue = random.choice(liste_de_rumeurs_possibles)
                    rumeur = LISTERUMEURS[numero_de_rumeur_entendue]
                    print("...et entendez quelque chose d'intéressant alors que vous finissez votre verre !")
                    services.Affichage.EntreePourContinuer()
                    services.Sove.ModifieRumeursDansSove("Ajout", numero_de_rumeur_entendue)
                    print(rumeur)
                    services.Affichage.EntreePourContinuer()



            elif choix == 2:
                print("Vous trainez dans le saloon, mais la réceptioniste vous demande de sortir, si vous ne comptez pas prendre une consommation !")
                services.Affichage.EntreePourContinuer()

            elif choix == 3:
                print("Vous faites le point sur les rumeurs entendues :\n")
                liste_de_rumeurs_entendues = services.Sove.ModifieRumeursDansSove("Donne", None)

                for numero_de_la_rumeur in liste_de_rumeurs_entendues:
                    print(LISTERUMEURS[numero_de_la_rumeur])
                    print("")
                    
                print("\n")
                services.Affichage.EntreePourContinuer()

            elif choix == 4:
                break
