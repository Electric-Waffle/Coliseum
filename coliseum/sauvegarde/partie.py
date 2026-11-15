"""Sauvegarde de la run en cours (save.txt) et lecture du mode de jeu au lancement."""

import ast
import csv
import os
import sys

from coliseum import services
from coliseum.chemins import DOSSIER_RESSOURCES
from coliseum.console import ClearConsole
from coliseum.donnees.debug import DEBUG_OPTIONS


class SaveManagement:

    def __init__(self):
        self.dictionnaire_de_sauvegarde = {}

    def FromPlayerToDict(self):
        self.dictionnaire_de_sauvegarde["Nom"] = services.Player.nom_du_personnage
        self.dictionnaire_de_sauvegarde["Stigma Positif"] = services.Player.stigma_positif
        self.dictionnaire_de_sauvegarde["Stigma Négatif"] = services.Player.stigma_negatif
        self.dictionnaire_de_sauvegarde["Stigma Bonus"] = services.Player.stigma_bonus
        self.dictionnaire_de_sauvegarde["Techniques"] = services.Player.techniques_possedes
        self.dictionnaire_de_sauvegarde["Sorts"] = services.Player.sorts_possedes
        self.dictionnaire_de_sauvegarde["Items"] = services.Player.items_possedes
        self.dictionnaire_de_sauvegarde["Materiaux Temporaires"] = services.Player.liste_de_materiaux
        self.dictionnaire_de_sauvegarde["Talents"] = services.Player.talents_possedes
        self.dictionnaire_de_sauvegarde["Points de vie max"] = services.Player.points_de_vie_max
        self.dictionnaire_de_sauvegarde["Points de vie"] = services.Player.points_de_vie
        self.dictionnaire_de_sauvegarde["Points de mana max"] = (
            services.Player.points_de_mana_max
        )
        self.dictionnaire_de_sauvegarde["Points de mana"] = services.Player.points_de_mana
        self.dictionnaire_de_sauvegarde["Points d'endurance"] = services.Player.points_dendurance
        self.dictionnaire_de_sauvegarde["Points de force"] = services.Player.points_de_force
        self.dictionnaire_de_sauvegarde["Points d'intelligence"] = (
            services.Player.points_dintelligence
        )
        self.dictionnaire_de_sauvegarde["Points de defence"] = services.Player.points_de_defence
        self.dictionnaire_de_sauvegarde["Chance de coup critique"] = (
            services.Player.taux_coup_critique
        )
        self.dictionnaire_de_sauvegarde["Degat de coup critique"] = (
            services.Player.degat_coup_critique
        )
        self.dictionnaire_de_sauvegarde["Chance de sort critique"] = (
            services.Player.taux_sort_critique
        )
        self.dictionnaire_de_sauvegarde["Degat de sort critique"] = (
            services.Player.degat_sort_critique
        )
        self.dictionnaire_de_sauvegarde["Chance d'esquive"] = services.Player.taux_desquive
        self.dictionnaire_de_sauvegarde["Nombre de gold"] = services.Player.nombre_de_gold
        self.dictionnaire_de_sauvegarde["Nombre de Redcoins"] = (
            services.Player.nombre_de_red_coin
        )
        self.dictionnaire_de_sauvegarde["Nombre de monstres tués"] = (
            services.Player.nombre_de_monstres_tues
        )
        self.dictionnaire_de_sauvegarde["Numéro de l'etage"] = services.Player.numero_de_letage
        self.dictionnaire_de_sauvegarde["Quete en cours"] = services.Player.quete
        self.dictionnaire_de_sauvegarde["Quete complétées"] = services.Player.quete_complete
        self.dictionnaire_de_sauvegarde["Le Boss a ete Battu"] = services.Player.boss_battu
        self.dictionnaire_de_sauvegarde[
            "Commentaire pour l'affichage du Boss dans le menu"
        ] = services.Player.commentaire_boss
        self.dictionnaire_de_sauvegarde["Nombre d'ennemis restant a l'étage"] = (
            services.Player.nombre_dennemis_a_letage
        )
        self.dictionnaire_de_sauvegarde["Le Redcoin d'extermination a ete recu"] = (
            services.Player.red_coin_recu_par_extermination
        )
        self.dictionnaire_de_sauvegarde["Le Redcoin du marchand a ete achete"] = (
            services.Player.redcoin_bought
        )
        self.dictionnaire_de_sauvegarde["Nombre de Tirage acheté"] = (
            services.Player.number_of_tirage
        )
        self.dictionnaire_de_sauvegarde["Possede une gemme de vie"] = (
            services.Player.gemme_de_vie
        )
        self.dictionnaire_de_sauvegarde["Possede une gemme de mana"] = (
            services.Player.gemme_de_mana
        )
        self.dictionnaire_de_sauvegarde["Possede une fée"] = services.Player.possede_une_fee
        self.dictionnaire_de_sauvegarde["Le livre de sort a ete utilise"] = (
            services.Player.library_used
        )
        self.dictionnaire_de_sauvegarde["Actions oubliées"] = (
            services.Player.liste_daction_oubliees
        )
        self.dictionnaire_de_sauvegarde["Le livre de sort final a ete utilise"] = (
            services.Player.final_library_used
        )
        self.dictionnaire_de_sauvegarde["La vieille dame a été soignée"] = (
            services.Player.mercant_healed
        )
        self.dictionnaire_de_sauvegarde["La fontaine a ete utilise"] = (
            services.Player.fountain_used
        )
        self.dictionnaire_de_sauvegarde["Nombre de Gold dans l'étang"] = (
            services.Player.gold_in_well
        )
        self.dictionnaire_de_sauvegarde["Donneur de quetes"] = services.Player.quest_giver
        self.dictionnaire_de_sauvegarde["Possede la clé"] = services.Player.possede_la_cle
        self.dictionnaire_de_sauvegarde["Etage alternatif"] = services.Player.etage_alternatif
        self.dictionnaire_de_sauvegarde["Blueprint de l'étage"] = (
            services.FloorMaker.FloorBlueprint
        )
        self.dictionnaire_de_sauvegarde["Liste d'artefacts optionnels"] = (
            services.Player.liste_dartefacts_optionels
        )
        self.dictionnaire_de_sauvegarde["Dictionnaire d'uppgrades spéciales"] = (
            services.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner
        )
        self.dictionnaire_de_sauvegarde["Nombre de Sacrifices"] = (
            services.Player.nombre_de_sacrifices
        )
        self.dictionnaire_de_sauvegarde["Nom de l'étage"] = (
            services.Player.nom_de_letage
        )
        self.dictionnaire_de_sauvegarde["Musique Etage 10"] = (
            services.Player.musique_etage_10
        )
        self.dictionnaire_de_sauvegarde["Musique Combat 10"] = (
            services.Player.musique_combat_10
        )
        self.dictionnaire_de_sauvegarde["Numéro du boss Alt"] = (
            services.Player.numero_boss_alt
        )
        self.dictionnaire_de_sauvegarde["Nombre de Flammes Bleue"] = (
            services.Player.flammes_bleue
        )
        self.dictionnaire_de_sauvegarde["Nombre de Flammes Verte"] = (
            services.Player.flammes_verte
        )
        self.dictionnaire_de_sauvegarde["Nombre de Flammes Rouge"] = (
            services.Player.flammes_rouge
        )
        self.dictionnaire_de_sauvegarde["Nombre de Flammes Noire"] = (
            services.Player.flammes_noire
        )
        self.dictionnaire_de_sauvegarde["Nombre de Poisson"] = (
            services.Player.poissons
        )
        self.dictionnaire_de_sauvegarde["Nombre de Jetons"] = (
            services.Player.jetons
        )
        self.dictionnaire_de_sauvegarde["Charge Tachyon Instable"] = (
            services.Player.charge_mauvais_tachyon
        )
        self.dictionnaire_de_sauvegarde["Charge Accumulateur de Tachyon"] = (
            services.Player.charge_bon_tachyon
        )

        # debug
        self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_technique"] = (
            services.Player.debug_bonus_equilibrage_technique
        )
        self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_technique_critique"] = (
            services.Player.debug_bonus_equilibrage_technique_critique
        )
        self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_technique_feu"] = (
            services.Player.debug_bonus_equilibrage_technique_feu
        )
        self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_technique_terre"] = (
            services.Player.debug_bonus_equilibrage_technique_terre
        )
        self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_technique_foudre"] = (
            services.Player.debug_bonus_equilibrage_technique_foudre
        )
        self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_technique_glace"] = (
            services.Player.debug_bonus_equilibrage_technique_glace
        )
        self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_technique_physique"] = (
            services.Player.debug_bonus_equilibrage_technique_physique
        )
        self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_technique_sang"] = (
            services.Player.debug_bonus_equilibrage_technique_sang
        )
        self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_sort"] = (
            services.Player.debug_bonus_equilibrage_sort
        )
        self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_sort_critique"] = (
            services.Player.debug_bonus_equilibrage_sort_critique
        )
        self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_sort_feu"] = (
            services.Player.debug_bonus_equilibrage_sort_feu
        )
        self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_sort_terre"] = (
            services.Player.debug_bonus_equilibrage_sort_terre
        )
        self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_sort_foudre"] = (
            services.Player.debug_bonus_equilibrage_sort_foudre
        )
        self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_sort_glace"] = (
            services.Player.debug_bonus_equilibrage_sort_glace
        )
        self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_sort_physique"] = (
            services.Player.debug_bonus_equilibrage_sort_physique
        )
        self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_sort_sang"] = (
            services.Player.debug_bonus_equilibrage_sort_sang
        )
        self.dictionnaire_de_sauvegarde["debug_bonus_sang_regain_sante"] = (
            services.Player.debug_bonus_sang_regain_sante
        )

    def FromDictToPlayer(self):
        services.Player.nom_du_personnage = (self.dictionnaire_de_sauvegarde["Nom"]).strip('"')
        services.Player.stigma_positif = (
            self.dictionnaire_de_sauvegarde["Stigma Positif"]
        ).strip('"')
        services.Player.stigma_negatif = (
            self.dictionnaire_de_sauvegarde["Stigma Négatif"]
        ).strip('"')
        services.Player.musique_etage_10 = (
            self.dictionnaire_de_sauvegarde["Musique Etage 10"]
        ).strip('"')
        services.Player.musique_combat_10 = (
            self.dictionnaire_de_sauvegarde["Musique Combat 10"]
        ).strip('"')
        services.Player.stigma_bonus = (self.dictionnaire_de_sauvegarde["Stigma Bonus"]).strip(
            '"'
        )
        chaine_de_caractere = self.dictionnaire_de_sauvegarde["Techniques"]
        liste_de_technique = ast.literal_eval(chaine_de_caractere)
        services.Player.techniques_possedes = liste_de_technique
        chaine_de_caractere = self.dictionnaire_de_sauvegarde["Sorts"]
        liste_de_sorts = ast.literal_eval(chaine_de_caractere)
        services.Player.sorts_possedes = liste_de_sorts
        chaine_de_caractere = self.dictionnaire_de_sauvegarde["Actions oubliées"]
        liste_dactions = ast.literal_eval(chaine_de_caractere)
        services.Player.liste_daction_oubliees = liste_dactions
        chaine_de_caractere = self.dictionnaire_de_sauvegarde["Items"]
        dictionaire_de_item = ast.literal_eval(chaine_de_caractere)
        services.Player.items_possedes = dictionaire_de_item
        chaine_de_caractere = self.dictionnaire_de_sauvegarde["Materiaux Temporaires"]
        dictionaire_de_materiaux = ast.literal_eval(chaine_de_caractere)
        services.Player.liste_de_materiaux = dictionaire_de_materiaux
        chaine_de_caractere = self.dictionnaire_de_sauvegarde["Dictionnaire d'uppgrades spéciales"]
        dictionaire_de_uppgrade_speciale = ast.literal_eval(chaine_de_caractere)
        services.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner = dictionaire_de_uppgrade_speciale
        chaine_de_caractere = self.dictionnaire_de_sauvegarde["Talents"]
        liste_de_talent = ast.literal_eval(chaine_de_caractere)
        services.Player.talents_possedes = liste_de_talent
        services.Player.flammes_bleue = int(
            self.dictionnaire_de_sauvegarde["Nombre de Flammes Bleue"]
        )
        services.Player.flammes_verte = int(
            self.dictionnaire_de_sauvegarde["Nombre de Flammes Verte"]
        )
        services.Player.flammes_rouge = int(
            self.dictionnaire_de_sauvegarde["Nombre de Flammes Rouge"]
        )
        services.Player.flammes_noire = int(
            self.dictionnaire_de_sauvegarde["Nombre de Flammes Noire"]
        )
        services.Player.poissons = int(
            self.dictionnaire_de_sauvegarde["Nombre de Poisson"]
        )
        services.Player.jetons = int(
            self.dictionnaire_de_sauvegarde["Nombre de Jetons"]
        )
        services.Player.points_de_vie_max = int(
            self.dictionnaire_de_sauvegarde["Points de vie max"]
        )
        services.Player.points_de_vie_max = int(
            self.dictionnaire_de_sauvegarde["Points de vie max"]
        )
        services.Player.numero_boss_alt = int(
            self.dictionnaire_de_sauvegarde["Numéro du boss Alt"]
        )
        services.Player.points_de_vie = int(self.dictionnaire_de_sauvegarde["Points de vie"])
        services.Player.points_de_mana_max = int(
            self.dictionnaire_de_sauvegarde["Points de mana max"]
        )
        services.Player.points_de_mana = int(self.dictionnaire_de_sauvegarde["Points de mana"])
        services.Player.points_dendurance = int(
            self.dictionnaire_de_sauvegarde["Points d'endurance"]
        )
        services.Player.points_de_force = int(self.dictionnaire_de_sauvegarde["Points de force"])
        services.Player.points_dintelligence = int(
            self.dictionnaire_de_sauvegarde["Points d'intelligence"]
        )
        services.Player.points_de_defence = int(
            self.dictionnaire_de_sauvegarde["Points de defence"]
        )
        services.Player.taux_coup_critique = int(
            self.dictionnaire_de_sauvegarde["Chance de coup critique"]
        )
        services.Player.degat_coup_critique = int(
            self.dictionnaire_de_sauvegarde["Degat de coup critique"]
        )
        services.Player.taux_sort_critique = int(
            self.dictionnaire_de_sauvegarde["Chance de sort critique"]
        )
        services.Player.degat_sort_critique = int(
            self.dictionnaire_de_sauvegarde["Degat de sort critique"]
        )
        services.Player.taux_desquive = int(self.dictionnaire_de_sauvegarde["Chance d'esquive"])
        services.Player.nombre_de_gold = int(self.dictionnaire_de_sauvegarde["Nombre de gold"])
        services.Player.nombre_de_red_coin = int(
            self.dictionnaire_de_sauvegarde["Nombre de Redcoins"]
        )
        services.Player.nombre_de_monstres_tues = int(
            self.dictionnaire_de_sauvegarde["Nombre de monstres tués"]
        )
        services.Player.numero_de_letage = int(
            self.dictionnaire_de_sauvegarde["Numéro de l'etage"]
        )
        services.Player.affronte_un_boss = False
        services.Player.affronte_une_mimique = False
        services.Player.gemme_de_vie = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Possede une gemme de vie"]
        )
        services.Player.gemme_de_mana = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Possede une gemme de mana"]
        )
        services.Player.possede_une_fee = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Possede une fée"]
        )
        services.Player.quete = (self.dictionnaire_de_sauvegarde["Quete en cours"]).strip('"')
        services.Player.quete_complete = self.dictionnaire_de_sauvegarde["Quete complétées"]
        chaine_de_caractere = self.dictionnaire_de_sauvegarde["Quete complétées"]
        liste_de_quete_complete = ast.literal_eval(chaine_de_caractere)
        services.Player.quete_complete = liste_de_quete_complete
        services.Player.boss_battu = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Le Boss a ete Battu"]
        )
        services.Player.commentaire_boss = (
            self.dictionnaire_de_sauvegarde[
                "Commentaire pour l'affichage du Boss dans le menu"
            ]
        ).strip('"')
        services.Player.nom_de_letage = (
            self.dictionnaire_de_sauvegarde[
                "Nom de l'étage"
            ]
        ).strip('"')
        services.Player.nombre_dennemis_a_letage = int(
            self.dictionnaire_de_sauvegarde["Nombre d'ennemis restant a l'étage"]
        )
        services.Player.red_coin_recu_par_extermination = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Le Redcoin d'extermination a ete recu"]
        )
        services.Player.redcoin_bought = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Le Redcoin du marchand a ete achete"]
        )
        services.Player.number_of_tirage = int(
            self.dictionnaire_de_sauvegarde["Nombre de Tirage acheté"]
        )
        services.Player.nombre_de_sacrifices = int(
            self.dictionnaire_de_sauvegarde["Nombre de Sacrifices"]
        )
        services.Player.library_used = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Le livre de sort a ete utilise"]
        )
        services.Player.final_library_used = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Le livre de sort final a ete utilise"]
        )
        services.Player.quest_giver = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Donneur de quetes"]
        )
        services.Player.mercant_healed = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["La vieille dame a été soignée"]
        )
        services.Player.fountain_used = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["La fontaine a ete utilise"]
        )
        services.Player.possede_la_cle = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Possede la clé"]
        )
        services.Player.etage_alternatif = ast.literal_eval(
            self.dictionnaire_de_sauvegarde["Etage alternatif"]
        )
        services.Player.gold_in_well = int(
            self.dictionnaire_de_sauvegarde["Nombre de Gold dans l'étang"]
        )
        services.Player.charge_mauvais_tachyon = int(
            self.dictionnaire_de_sauvegarde["Charge Tachyon Instable"]
        )
        services.Player.charge_bon_tachyon = int(
            self.dictionnaire_de_sauvegarde["Charge Accumulateur de Tachyon"]
        )
        chaine_de_caractere = self.dictionnaire_de_sauvegarde["Blueprint de l'étage"]
        dictionaire_de_letage = ast.literal_eval(chaine_de_caractere)
        services.FloorMaker.FloorBlueprint = dictionaire_de_letage
        chaine_de_caractere = self.dictionnaire_de_sauvegarde[
            "Liste d'artefacts optionnels"
        ]
        liste_de_artefacts_option = ast.literal_eval(chaine_de_caractere)
        services.Player.liste_dartefacts_optionels = liste_de_artefacts_option

        # debug
        services.Player.debug_bonus_equilibrage_technique = int(
            self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_technique"]
        )
        services.Player.debug_bonus_equilibrage_technique_critique = int(
            self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_technique_critique"]
        )
        services.Player.debug_bonus_equilibrage_technique_feu = int(
            self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_technique_feu"]
        )
        services.Player.debug_bonus_equilibrage_technique_terre = int(
            self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_technique_terre"]
        )
        services.Player.debug_bonus_equilibrage_technique_foudre = int(
            self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_technique_foudre"]
        )
        services.Player.debug_bonus_equilibrage_technique_glace = int(
            self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_technique_glace"]
        )
        services.Player.debug_bonus_equilibrage_technique_physique = int(
            self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_technique_physique"]
        )
        services.Player.debug_bonus_equilibrage_technique_sang = int(
            self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_technique_sang"]
        )
        services.Player.debug_bonus_equilibrage_sort = int(
            self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_sort"]
        )
        services.Player.debug_bonus_equilibrage_sort_critique = int(
            self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_sort_critique"]
        )
        services.Player.debug_bonus_equilibrage_sort_feu = int(
            self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_sort_feu"]
        )
        services.Player.debug_bonus_equilibrage_sort_terre = int(
            self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_sort_terre"]
        )
        services.Player.debug_bonus_equilibrage_sort_foudre = int(
            self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_sort_foudre"]
        )
        services.Player.debug_bonus_equilibrage_sort_glace = int(
            self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_sort_glace"]
        )
        services.Player.debug_bonus_equilibrage_sort_physique = int(
            self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_sort_physique"]
        )
        services.Player.debug_bonus_equilibrage_sort_sang = int(
            self.dictionnaire_de_sauvegarde["debug_bonus_equilibrage_sort_sang"]
        )
        services.Player.debug_bonus_sang_regain_sante = int(
            self.dictionnaire_de_sauvegarde["debug_bonus_sang_regain_sante"]
        )

    def FromDictToSaveFile(self, nom_du_fichier):
        dir_path = DOSSIER_RESSOURCES
        chemin_du_fichier_save = dir_path + nom_du_fichier
        with open(chemin_du_fichier_save, "w") as fichier:
            fichier.write("Caracteristique|Valeur")
            for caracteristic in self.dictionnaire_de_sauvegarde:
                fichier.write(
                    f"\n{caracteristic}|{self.dictionnaire_de_sauvegarde[caracteristic]}"
                )

    def FromSaveFileToDict(self):
        dir_path = DOSSIER_RESSOURCES
        # fichier de sauvegarde (temporaire)
        chemin_du_fichier_save = dir_path + "\\save.txt"
        with open(chemin_du_fichier_save, "r") as fichier:
            reader = csv.DictReader(fichier, delimiter="|")
            for line in reader:
                self.dictionnaire_de_sauvegarde[line["Caracteristique"]] = line[
                    "Valeur"
                ]
        # autre sauvegarde (permanente)
        if services.Player.mode_de_jeu == "Ascension":
            chemin_du_fichier_save = dir_path + "\\s1ve.txt"
        else:
            chemin_du_fichier_save = dir_path + "\\s0ve.txt"
        with open(chemin_du_fichier_save, "r") as fichier:
            reader = csv.DictReader(fichier, delimiter="|")
            for line in reader:
                if line["Caracteristique"] in ["Invitation Recue"]:
                    self.dictionnaire_de_sauvegarde[line["Caracteristique"]] = line[
                        "Valeur"
                    ]

    def SaveTheGame(self):
        self.FromPlayerToDict()
        self.FromDictToSaveFile("\\save.txt")
        services.Affichage.AfficheSauvegarde()
        while True:
            try:
                print("Voulez vous quitter la partie ?")
                print("\n1 - Oui")
                print("2 - Non")
                choix = int(input("\n"))
                ClearConsole()
                if choix == 1:
                    sys.exit()
                elif choix == 2:
                    break
            except ValueError:
                ClearConsole()

    def SaveTheGameSansAffichage(self):
        if services.Player.mode_de_jeu != "Ascension":
            self.FromPlayerToDict()
            self.FromDictToSaveFile("\\save.txt")

    def LoadTheGame(self):
        self.FromSaveFileToDict()
        self.FromDictToPlayer()
        return True


def GetNomEtageEtDebugValues():
    try:
        dictionnaire = {}
        dir_path = DOSSIER_RESSOURCES
        # fichier de sauvegarde (temporaire)
        chemin_du_fichier_save = dir_path + "\\save.txt"
        with open(chemin_du_fichier_save, "r") as fichier:
            reader = csv.DictReader(fichier, delimiter="|")
            for line in reader:
                dictionnaire[line["Caracteristique"]] = line[
                    "Valeur"
                ]
        services.Player.nom_de_letage = dictionnaire["Nom de l'étage"]

        # debug
        for value_name in DEBUG_OPTIONS:
            setattr(services.Player, DEBUG_OPTIONS[value_name], dictionnaire[DEBUG_OPTIONS[value_name]])

    except KeyError:
        pass
    except FileNotFoundError:
        pass


def SetupGameMode():
    dir_path = DOSSIER_RESSOURCES
    chemin_sove = dir_path + "\\s0ve.txt"
    chemin_sive = dir_path + "\\s1ve.txt"

    dictionnaire_de_choses_permanentes = {}
    # fichier de sauvegarde (permanant)
    if os.path.isfile(chemin_sive):
        chemin_du_fichier_save = dir_path + "\\s1ve.txt"
    else:
        chemin_du_fichier_save = dir_path + "\\s0ve.txt"
    with open(chemin_du_fichier_save, "r") as fichier:
        reader = csv.DictReader(fichier, delimiter="|")
        for line in reader:
            dictionnaire_de_choses_permanentes[line["Caracteristique"]] = line[
                "Valeur"
            ]
    
    if dictionnaire_de_choses_permanentes["486241597531"] == "Jean.rar":
        services.Player.battu_le_sacrifie = True

    if services.Player.battu_le_sacrifie and os.path.isfile(chemin_sove):
        services.Player.mode_de_jeu = "Véritable Descente"
    elif not services.Player.battu_le_sacrifie and os.path.isfile(chemin_sive):
        services.Player.mode_de_jeu = "Ascension"
    elif not services.Player.battu_le_sacrifie and os.path.isfile(chemin_sove):
        services.Player.mode_de_jeu = "Descente"
    else:
        services.Player.mode_de_jeu = "Erreur"
