"""Le joueur : caractéristiques, inventaire, fiche de personnage et utilisation d'objets hors combat."""

from coliseum import services
from coliseum.chemins import DOSSIER_RESSOURCES
from coliseum.console import ClearConsole
from coliseum.donnees.actions import (
    ANNUAIREDESCRIPTIONSORTSSOIN,
    ANNUAIRESORTSSOIN,
    POURCENTAGESORTSOIN,
    SOINMINIMUMSORTSOIN,
)
from coliseum.donnees.personnages import DICTIONNAIREITEMINITIAL, UPPGRADESPOSSIBLES
from coliseum.erreurs import WriteErrorInErrorLog
from coliseum.joueur.benedictions import RecupereBenedictionEnCours, RecupereMaledictionEnCours


class PlayerCaracteristics:

    def __init__(self):
        self.musique_etage_10 = "etage_10"
        self.musique_combat_10 = "battle_theme_10"
        self.mode_de_jeu = "Normal"
        self.gemme_de_vie = False
        self.gemme_de_mana = False
        self.possede_une_fee = False
        self.mode_jukebox = False
        self.nom_du_personnage = ""
        self.stigma_positif = ""
        self.stigma_negatif = ""
        self.stigma_bonus = ""
        self.techniques_possedes = []
        self.sorts_possedes = []
        self.items_possedes = DICTIONNAIREITEMINITIAL
        self.talents_possedes = ""
        self.flammes_noire = 1
        self.flammes_verte = 2
        self.flammes_bleue = 3
        self.flammes_rouge = 5
        self.poissons = 5
        self.jetons = 0
        self.points_de_vie_max = 0
        self.points_de_vie = 0
        self.points_de_mana_max = 0
        self.points_de_mana = 0
        self.points_de_force = 0
        self.points_dendurance = 0
        self.points_dintelligence = 0
        self.points_de_defence = 0
        self.taux_coup_critique = 0
        self.degat_coup_critique = 0
        self.taux_sort_critique = 0
        self.degat_sort_critique = 0
        self.taux_desquive = 0
        self.nombre_de_gold = 0
        self.nombre_de_red_coin = 0
        self.nombre_de_monstres_tues = 0 # == le nombre d'ame
        self.numero_de_letage = 1
        self.affronte_un_boss = False
        self.commence_le_combat_confus = False
        self.affronte_une_mimique = False
        self.quete = "None"
        self.quete_complete = ["None"]
        self.boss_battu = False
        self.commentaire_boss = "Affronter le Boss"
        self.nombre_dennemis_a_letage = 15
        self.red_coin_recu_par_extermination = False
        self.redcoin_bought = False
        self.library_used = False
        self.liste_daction_oubliees = []
        self.final_library_used = False
        self.quest_giver = True
        self.mercant_healed = False
        self.fountain_used = False
        self.number_of_tirage = 0
        self.invitation_received = False
        self.gold_in_well = 50
        self.chemin_musique = DOSSIER_RESSOURCES
        self.position_y = 0
        self.position_x = 0
        self.numero_de_la_salle = 1
        self.possede_la_cle = False
        self.liste_dartefacts_optionels = []
        self.nombre_de_sacrifices = 0
        self.affronte_obelisque = False
        self.affronte_fin_histoire = False
        self.nom_de_letage = "Aucunes Données Utilisables"
        self.etage_alternatif = False
        self.numero_boss_alt = 1
        self.player_tags = ["Jour"]
        self.death_divinity = False
        donnees_de_s0ve = services.Observation.GetPermanentThingsFromS0ve()
        if donnees_de_s0ve["77454135415415"] == "Divinité de la Mort":
            self.death_divinity = True
        self.battu_le_sacrifie = False
        self.vies_du_gardien = 12
        self.liste_de_materiaux =  {
            # monstre
            "Coeur Gravitaire": 0,
            "Ectoplasme Chaud": 0,
            "Poussière Animée": 0,
            "Ether Non-Newtonien": 0,
            "Eclat de Verre": 0,

            "Fluide Alien": 0,
            "Morceau de Cloche": 0,
            "Ecaille de Phénix": 0,
            "Roche Glycérine": 0,
            "Poil Gelé": 0,

            "Moustache de Chat": 0,
            "Fragment Osseux": 0,
            "Iris du Malheur": 0,
            "Velour de Cervidé": 0,
            "Composants Electroniques": 0,

            "Eclat de Crystal": 0,
            "Pilules de Roulette": 0,
            "Fragment de Jade": 0,
            "Poussière Dorée Animée": 0,
            "Gemme Bleue": 0,

            # personnage
            "Essence de Vitalitée": 0,
            "Essence de Magie": 0,
            "Essence de Fortitude": 0,
            "Essence de Sagesse": 0,
            "Essence de Résistance": 0,

            "Essence Dorée": 0,
            "Essence Astrale": 0,
            "Essence Carmine": 0,

            # artefact
            "Fragment Mélioratif": 0,
            "Fragment Sophiste": 0,
            "Fragment de Fatalité": 0,
            "Fragment Insatiable": 0,
        }
        self.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner = {
            "Tisane de Racine" : 0,
            "Tisane d'Ecorce" : 0,
            "Charge de Feu" : 0,
            "Charge de Glace" : 0,
            "Charge de Foudre" : 0,
            "Charge de Terre" : 0,
            "Charge de Chair" : 0,
            "Charge de Sang" : 0,
            "Médaillon de Leprechaun" : 0,
            "Noyau d'Aurelionite" : 0
        }
        self.benediction = RecupereBenedictionEnCours()
        self.malediction = RecupereMaledictionEnCours()
        self.charge_mauvais_tachyon = 0
        self.charge_bon_tachyon = 0
        
        # debug equilibrage
        self.debug_bonus_equilibrage_technique = 50
        self.debug_bonus_equilibrage_technique_critique = 0
        self.debug_bonus_equilibrage_technique_feu = 0
        self.debug_bonus_equilibrage_technique_terre = 0
        self.debug_bonus_equilibrage_technique_foudre = 0
        self.debug_bonus_equilibrage_technique_glace = 0
        self.debug_bonus_equilibrage_technique_physique = 0
        self.debug_bonus_equilibrage_technique_sang = 0
        self.debug_bonus_equilibrage_sort = 50
        self.debug_bonus_equilibrage_sort_critique = 0
        self.debug_bonus_equilibrage_sort_feu = 0
        self.debug_bonus_equilibrage_sort_terre = 0
        self.debug_bonus_equilibrage_sort_foudre = 0
        self.debug_bonus_equilibrage_sort_glace = 0
        self.debug_bonus_equilibrage_sort_physique = 0
        self.debug_bonus_equilibrage_sort_sang = 0
        self.debug_bonus_sang_regain_sante = 0

    def checkForStigmaPlusAhti(self):
        if self.stigma_positif == "Esprit bien rangé, esprit libéré":
            self.points_de_vie += int(self.points_de_vie_max * 0.1)
            print("Observer la salle vous fait du bien. Vous regagnez des points de vie.")
            services.Affichage.EntreePourContinuer()
            if self.points_de_vie > self.points_de_vie_max:
                self.points_de_vie = self.points_de_vie_max

    def AddGoldToPlayer(self, gain_gold, return_le_gain=False):
        gain_gold += round(gain_gold * (services.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Noyau d'Aurelionite"] / 100))
        if services.Player.malediction == "Ascétique":
            gain_gold -= round(gain_gold * 0.5)
        if services.Player.benediction == "Materiel":
            gain_gold += gain_gold
        services.Player.nombre_de_gold += (gain_gold)
        if return_le_gain:
            return gain_gold

    def BringBackListeMateriauxToZero(self):
        self.liste_de_materiaux = {
            # monstre
            "Coeur Gravitaire": 0,
            "Ectoplasme Chaud": 0,
            "Poussière Animée": 0,
            "Ether Non-Newtonien": 0,
            "Eclat de Verre": 0,

            "Fluide Alien": 0,
            "Morceau de Cloche": 0,
            "Ecaille de Phénix": 0,
            "Roche Glycérine": 0,
            "Poil Gelé": 0,

            "Moustache de Chat": 0,
            "Fragment Osseux": 0,
            "Iris du Malheur": 0,
            "Velour de Cervidé": 0,
            "Composants Electroniques": 0,

            "Eclat de Crystal": 0,
            "Pilules de Roulette": 0,
            "Fragment de Jade": 0,
            "Poussière Dorée Animée": 0,
            "Gemme Bleue": 0,

            # personnage
            "Essence de Vitalitée": 0,
            "Essence de Magie": 0,
            "Essence de Fortitude": 0,
            "Essence de Sagesse": 0,
            "Essence de Résistance": 0,

            "Essence Dorée": 0,
            "Essence Astrale": 0,
            "Essence Carmine": 0,

            # artefact
            "Fragment Mélioratif": 0,
            "Fragment Sophiste": 0,
            "Fragment de Fatalité": 0,
            "Fragment Insatiable": 0,
        }


    def UseCharacterForInitCaracteristics(self, caracteristiques):
        self.nom_du_personnage = caracteristiques[0]
        self.stigma_positif = caracteristiques[2]
        self.stigma_negatif = caracteristiques[3]
        self.stigma_bonus = caracteristiques[4]
        self.techniques_possedes = caracteristiques[5]
        self.sorts_possedes = caracteristiques[6]
        liste_item_a_mettre_a_jour = caracteristiques[7]
        for item in liste_item_a_mettre_a_jour:
            self.items_possedes[item] = liste_item_a_mettre_a_jour[item]
        self.talents_possedes = caracteristiques[8]
        self.points_de_vie_max = caracteristiques[9]
        self.points_de_vie = caracteristiques[9]
        self.points_de_mana_max = caracteristiques[10]
        self.points_de_mana = caracteristiques[10]
        self.points_de_force = caracteristiques[11]
        self.points_dintelligence = caracteristiques[12]
        self.points_de_defence = caracteristiques[13]
        self.taux_coup_critique = caracteristiques[14]
        self.degat_coup_critique = caracteristiques[15]
        self.taux_sort_critique = caracteristiques[16]
        self.degat_sort_critique = caracteristiques[17]
        self.taux_desquive = caracteristiques[18]
        self.nombre_de_gold = caracteristiques[19]
        self.liste_dartefacts_optionels = caracteristiques[20]
        self.points_dendurance = 20

    def PutMateriauxInList(self):
        liste_materiaux = []

        for materiaux in services.Player.liste_de_materiaux:
            if services.Player.liste_de_materiaux[materiaux] != 0:
                liste_materiaux.append(f"{materiaux} : {services.Player.liste_de_materiaux[materiaux]}")

        return liste_materiaux

    def ShowcaseCaracteristics(self):
        liste_artefacts = self.PutArtefactInList()
        liste_materiaux = self.PutMateriauxInList()
        print(f"          -={{ {services.Player.nom_du_personnage} }}=-")

        print(
            f"\nPoints de vie : {services.Player.points_de_vie}/{services.Player.points_de_vie_max}"
            f"\nPoints de mana : {services.Player.points_de_mana}/{services.Player.points_de_mana_max}"
            f"\nEndurance maximale : {services.Player.points_dendurance}"
            f"\nPoints de force : {services.Player.points_de_force} | Points d'intelligence : {services.Player.points_dintelligence}"
            f"\nPoints de defence : {services.Player.points_de_defence}"
            f"\nChance de coup critique : {services.Player.taux_coup_critique}% | Degats de coup critique : {services.Player.degat_coup_critique}"
            f"\nChance de sort critique : {services.Player.taux_sort_critique}% | Degats de sort critique : {services.Player.degat_sort_critique}"
            f"\nChance d'esquive : {services.Player.taux_desquive}%"
            f"\nNombre de Golds : {services.Player.nombre_de_gold} | Nombre de Redcoins : {services.Player.nombre_de_red_coin}"
            f"\nNombre d'âmes absorbées : {services.Player.nombre_de_monstres_tues}"
            f"\nQuête en cours : {services.Player.quete}"
            f"\nQuêtes réalisées : {services.Player.quete_complete}"
            f"\nTechniques apprises : {services.Player.techniques_possedes}"
            f"\nSorts appris : {services.Player.sorts_possedes}"
            f"\nTalents possédés : {services.Player.talents_possedes}"
            f"\nArtefacts : {liste_artefacts}"
            f"\nStigmas + : {services.Player.stigma_positif} | Stigmas - : {services.Player.stigma_negatif} | Stigmas * : {services.Player.stigma_bonus}"
        )
        if len(liste_materiaux) != 0:
            print(f"Matériaux : {liste_materiaux}")

        if "Griffes du Démon" in services.Player.techniques_possedes:
            print(f"S4CR1F1CES R1TU3LS P0UR L'1NN0M4BLE : {services.Player.nombre_de_sacrifices}")

        if services.Player.malediction == "Chronophage":
            print(f"Charge du tachyon instable : {services.Player.charge_mauvais_tachyon}")
        if services.Player.benediction == "Accumulateur de Tachyon":
            print(f"Charge de l'extracteur de Tachyon : {services.Player.charge_bon_tachyon}")
        if services.Player.jetons != 0 :
            print(f"Jetons Fidélité : {services.Player.jetons}")
        if services.Sove.ModifieTagsDansSove("Checke", "Symbole Vu") :
            level_de_la_cle =  services.Sove.ModifieLivraisonDansSove("Nombre", "Clé")
            level_de_la_carte =  services.Sove.ModifieLivraisonDansSove("Nombre", "Carte")
            print(f"\nClé jusqu'à l'étage [{level_de_la_cle + 3}]")
            print(f"Carte jusqu'à l'étage [{level_de_la_carte + 3}]")
        print(" \n          -={{ Items }}=-"
              "\n1 - Retour"
        )
        numero_de_laffichage = services.Player.AffichageItem()
        numero_de_laffichage = services.Player.AffichageSortSoin(numero_de_laffichage)
        return numero_de_laffichage, int(
            input("\nChoisissez une action avec les nombres : ")
        )

    def AffichageItem(self):
        self.liste_ditem_a_afficher = []
        for item in services.Player.items_possedes:
            if services.Player.items_possedes[item] == 0:
                continue
            self.liste_ditem_a_afficher.append(item)
        numero_de_laffichage = 2
        for item in self.liste_ditem_a_afficher:
            print(f"{numero_de_laffichage} - {item} : {services.Player.items_possedes[item]}")
            numero_de_laffichage += 1
        return numero_de_laffichage

    def AffichageSortSoin(self, numero_de_laffichage):
        numero_a_afficher = numero_de_laffichage
        for sort in services.Player.sorts_possedes:
            if sort in ANNUAIRESORTSSOIN:
                if numero_a_afficher == numero_de_laffichage:
                    print("\n     -={{ Sorts de Soin }}=-\n")
                print(f"{numero_a_afficher} - {sort} [{ANNUAIRESORTSSOIN[sort]}pm]")
                numero_a_afficher += 1
        return numero_a_afficher

    def PutArtefactInList(self):
        liste_artefact = []
        if services.Player.gemme_de_vie:
            liste_artefact.append("Gemme de Vie")
        if services.Player.gemme_de_mana:
            liste_artefact.append("Gemme d'Esprit")
        if services.Player.possede_une_fee:
            liste_artefact.append("Fée dans un Bocal")
        if services.Player.possede_la_cle:
            liste_artefact.append("Clé Incrustée")
        for artefact in services.Player.liste_dartefacts_optionels:
            liste_artefact.append(artefact)
        if len(liste_artefact) == 0:
            liste_artefact.append("Aucun")
        return liste_artefact
    
    def ShowGarbage(self):

        try:
            print("Vous regardez dans votre sacoche et trouvez :\n")
            liste_de_materiaux =  services.Sove.ModifieDechetsDansSove("Donne", None, None)
            for dechet in liste_de_materiaux:
                nombre =  services.Sove.ModifieDechetsDansSove("Nombre", dechet, None)
                if nombre != 0 :
                    print(f"{dechet} : {nombre}")
            print("")
            
            liste_de_uppgrade_a_afficher = {}
            for uppgrade in UPPGRADESPOSSIBLES:
                level_de_luppgrade =  services.Sove.ModifieLivraisonDansSove("Nombre", uppgrade)
                if level_de_luppgrade != 0:
                    liste_de_uppgrade_a_afficher[uppgrade] = level_de_luppgrade

            if len(liste_de_uppgrade_a_afficher) != 0:
                print("Vous avez aussi des bons de commande sur lesquels sont écrit :\n")
                for uppgrade in liste_de_uppgrade_a_afficher:
                    if uppgrade == "Clé":
                        print(f"{uppgrade} allant jusqu'à l'étage {liste_de_uppgrade_a_afficher[uppgrade] + 3}")
                    elif uppgrade == "Carte":
                        print(f"{uppgrade} allant jusqu'à l'étage {liste_de_uppgrade_a_afficher[uppgrade] + 4}")
                    else:
                        print(f"{uppgrade} de niveau {liste_de_uppgrade_a_afficher[uppgrade]}")
                print("")

            services.Affichage.EntreePourContinuer()

        except Exception as error:
            WriteErrorInErrorLog(error)

        

    def ShowPlayerCaracteristicsAndItems(self):
        ClearConsole()
        dans_le_menu = True
        while dans_le_menu:
            while True:
                try:
                    limite_de_choix, choix = services.Player.ShowcaseCaracteristics()
                    ClearConsole()
                    if choix in range(1, (limite_de_choix)):
                        break
                except ValueError:
                    ClearConsole()
            if choix == 1:
                ClearConsole()
                dans_le_menu = False
            else:
                if choix in range(2, (len(self.liste_ditem_a_afficher) + 2)):
                    item_a_utiliser = self.liste_ditem_a_afficher[choix - 2]
                    services.Player.UseItem(item_a_utiliser)
                else:
                    position_du_sort = choix - ((len(self.liste_ditem_a_afficher) + 1))
                    services.Player.UseHealingMagic(position_du_sort)

    def UseHealingMagic(self, position_du_sort):
        # prendre le sort en question
        liste_de_sorts_de_soin = []
        for sort in services.Player.sorts_possedes:
            if sort in ANNUAIRESORTSSOIN:
                liste_de_sorts_de_soin.append(sort)
        sort_de_soin_a_utiliser = liste_de_sorts_de_soin[(position_du_sort - 1)]
        # voir si on peux utiliser le sort
        cout_du_sort = ANNUAIRESORTSSOIN[sort_de_soin_a_utiliser]
        if services.Player.points_de_mana >= cout_du_sort:
            # utilisation du sort
            services.Player.points_de_mana -= cout_du_sort
            print(
                f"Vous prenez le temps de vous concentrer pour lancer le sort [{sort_de_soin_a_utiliser}], ce qui réduit son cout en mana et augmente son efficacité."
            )
            print(ANNUAIREDESCRIPTIONSORTSSOIN[sort_de_soin_a_utiliser])
            soin = round(
                (
                    (
                        (POURCENTAGESORTSOIN[sort_de_soin_a_utiliser])
                        + (self.points_dintelligence // 4)
                    )
                    / 100
                )
                * self.points_de_vie_max
            )
            if soin < SOINMINIMUMSORTSOIN[sort_de_soin_a_utiliser]:
                soin = SOINMINIMUMSORTSOIN[sort_de_soin_a_utiliser]
            soin += self.points_dintelligence
            self.points_de_vie += soin
            if self.points_de_vie > self.points_de_vie_max:
                self.points_de_vie = self.points_de_vie_max
            print(f"Vous reprenez {soin} points de vie !")
        else:
            # pas assez de mana
            print(
                "Vous condensez le mana pour invoquer le sort...mais pas assez ne se réunit pour terminer l'invoquation."
            )
        services.Affichage.EntreePourContinuer()
        ClearConsole()

    def UseItem(self, item):
        if item in ["Feuille Jindagee", "Fruit Jindagee"]:
            services.Player.items_possedes[item] -= 1
            if item == "Feuille Jindagee":
                soin = 5 + round(services.Player.points_de_vie_max * 0.05)
                if soin < 8:
                    soin = 8
            elif item == "Fruit Jindagee":
                soin = 10 + round(services.Player.points_de_vie_max * 0.1)
                if soin < 13:
                    soin = 13
            bonus_soin = 0
            if self.stigma_positif == "Pharmacodynamisme":
                bonus_soin += 1
            if "Carte du Gout" in services.Player.talents_possedes:
                bonus_soin += 0.5
            soin += round(bonus_soin * soin)
            soin += services.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Tisane d'Ecorce"]
            nombre_tour = 3
            if "Larme d'Yggdrasil" in services.Player.liste_dartefacts_optionels:
                nombre_tour += 3
            soin_final = soin * nombre_tour
            self.points_de_vie += soin_final
            if services.Player.points_de_vie > services.Player.points_de_vie_max:
                services.Player.points_de_vie = services.Player.points_de_vie_max
            print(
                f"Vous utilisez l'item [{item}], et regagnez {soin_final} points de vie en peu de temps !"
            )
        elif item in ["Feuille Aatma", "Fruit Aatma"]:
            services.Player.items_possedes[item] -= 1
            if item == "Feuille Aatma":
                soin = 5 + round(services.Player.points_de_mana_max * 0.05)
                if soin < 8:
                    soin = 8
            elif item == "Fruit Aatma":
                soin = 10 + round(services.Player.points_de_mana_max * 0.1)
                if soin < 13:
                    soin = 13
            bonus_soin = 0
            if self.stigma_positif == "Pharmacodynamisme":
                bonus_soin += 1
            if "Carte du Gout" in services.Player.talents_possedes:
                bonus_soin += 0.5
            soin += round(bonus_soin * soin)
            soin += services.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Tisane de Racine"]
            nombre_tour = 3
            if "Larme d'Yggdrasil" in services.Player.liste_dartefacts_optionels:
                nombre_tour += 3
            soin_final = soin * nombre_tour
            self.points_de_mana += soin_final
            if services.Player.points_de_mana > services.Player.points_de_mana_max:
                services.Player.points_de_mana = services.Player.points_de_mana_max
            print(
                f"Vous utilisez l'item [{item}], et regagnez {soin_final} points de mana en peu de temps !"
            )
        elif item in ["Remède", "Remède Superieur", "Remède Divin"]:
            services.Player.items_possedes[item] -= 1
            if item == "Remède":
                soin = round(services.Player.points_de_vie_max * 0.1)
                if soin < 17:
                    soin = 17
            elif item == "Remède Superieur":
                soin = round(services.Player.points_de_vie_max * 0.2)
                if soin < 27:
                    soin = 27
            elif item == "Remède Divin":
                soin = round(services.Player.points_de_vie_max * 0.3)
                if soin < 39:
                    soin = 39
            soin += services.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Tisane d'Ecorce"]
            bonus_soin = 0
            if self.stigma_positif == "Pharmacodynamisme":
                bonus_soin += 1
            if "Carte du Gout" in services.Player.talents_possedes:
                bonus_soin += 0.5
            soin += round(bonus_soin * soin)
            services.Player.points_de_vie += soin
            if services.Player.points_de_vie > services.Player.points_de_vie_max:
                services.Player.points_de_vie = services.Player.points_de_vie_max
            print(
                f"Vous appliquez le remède sur vos blessures et regagnez {soin} points de vie !"
            )
        elif item in ["Pillule", "Pillule Superieure", "Pillule Divine"]:
            services.Player.items_possedes[item] -= 1
            if item == "Pillule":
                soin = round(services.Player.points_de_mana_max * 0.1)
                if soin < 17:
                    soin = 17
            elif item == "Pillule Superieure":
                soin = round(services.Player.points_de_mana_max * 0.2)
                if soin < 27:
                    soin = 27
            elif item == "Pillule Divine":
                soin = round(services.Player.points_de_mana_max * 0.3)
                if soin < 39:
                    soin = 39
            soin += services.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Tisane de Racine"]
            bonus_soin = 0
            if self.stigma_positif == "Pharmacodynamisme":
                bonus_soin += 1
            if "Carte du Gout" in services.Player.talents_possedes:
                bonus_soin += 0.5
            soin += round(bonus_soin * soin)
            services.Player.points_de_mana += soin
            if services.Player.points_de_mana > services.Player.points_de_mana_max:
                services.Player.points_de_mana = services.Player.points_de_mana_max
            print(f"Vous avalez la pillule et regagnez {soin} points de mana !")
        else:
            print(f"Vous preferez garder l'item [{item}] pour les combats.")
        services.Affichage.EntreePourContinuer()
