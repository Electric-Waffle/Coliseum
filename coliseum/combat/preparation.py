"""Mise en place du combat : choix du monstre, musique, premiers tours, bonus des talents."""

import random

from coliseum.combat.bestiaire import ContexteDeCombat, fiche_du_monstre
from coliseum.combat.reductions import ESQUIVE_UTILE_MAX, reduction_en_pourcentage
from coliseum.console import ClearConsole

# Cape Victorieuse et Contrat de Travail agrandissent le bonus de dégâts (le
# « pool ») d'un pourcentage ; ce pourcentage ne dépasse jamais 100 %, c'est à
# dire que le bonus au maximum double.
PLAFOND_AMELIORATION_DEGATS_TOTAUX = 100
# Bonus de dégâts des attaques normales des monstres, par étage au dessus du premier.
BONUS_DEGATS_MONSTRE_PAR_ETAGE = 6

# Le boss de fin d'histoire dépend du personnage joué.
BOSS_D_HISTOIRE_PAR_PERSONNAGE = {
    "Elma": "Yvan",
    "Saumel": "El Baron",
    "Vesperum": "Armée des Anges",
    "Peralta": "Doug Trudy",
    "Voyageur": "Thémis",
}


class PreparationMixin:

    def SetBenedictionDuMana(self):
        """Ne prend rien, ne retourne rien.

        Défini les variables benediction du mana
        et malediction du mana grace a un input
        de l'utilisateur
        """
        if self.modele.benediction_du_mana and self.modele.malediction_du_mana:
            action_taken = False
            while not action_taken:
                try:
                    choix_du_joueur_pour_le_talent_benediction_du_mana = (
                        self.vue.GetChoiceMana()
                    )
                    # demande au user si il veut etre beni ou maudit par le mana
                    if choix_du_joueur_pour_le_talent_benediction_du_mana == 1:
                        self.modele.malediction_du_mana = False
                        action_taken = True
                    elif choix_du_joueur_pour_le_talent_benediction_du_mana == 2:
                        self.modele.benediction_du_mana = False
                        action_taken = True
                    ClearConsole()
                except ValueError:
                    ClearConsole()

    def PatternDesignConstantUpdater(self):
        #sert a tester plusieurs types de dégats sans avoir a changer les dégats de chaques attaques et sorts
        bonus_equilibrage_technique = self.modele.debug_bonus_equilibrage_technique
        bonus_equilibrage_technique_critique = self.modele.debug_bonus_equilibrage_technique_critique
        bonus_equilibrage_technique_feu = self.modele.debug_bonus_equilibrage_technique_feu
        bonus_equilibrage_technique_terre = self.modele.debug_bonus_equilibrage_technique_terre
        bonus_equilibrage_technique_foudre = self.modele.debug_bonus_equilibrage_technique_foudre
        bonus_equilibrage_technique_glace = self.modele.debug_bonus_equilibrage_technique_glace
        bonus_equilibrage_technique_physique = self.modele.debug_bonus_equilibrage_technique_physique
        bonus_equilibrage_technique_sang = self.modele.debug_bonus_equilibrage_technique_sang
        bonus_equilibrage_sort = self.modele.debug_bonus_equilibrage_sort
        bonus_equilibrage_sort_critique = self.modele.debug_bonus_equilibrage_sort_critique
        bonus_equilibrage_sort_feu = self.modele.debug_bonus_equilibrage_sort_feu
        bonus_equilibrage_sort_terre = self.modele.debug_bonus_equilibrage_sort_terre
        bonus_equilibrage_sort_foudre = self.modele.debug_bonus_equilibrage_sort_foudre
        bonus_equilibrage_sort_glace = self.modele.debug_bonus_equilibrage_sort_glace
        bonus_equilibrage_sort_physique = self.modele.debug_bonus_equilibrage_sort_physique
        bonus_equilibrage_sort_sang = self.modele.debug_bonus_equilibrage_sort_sang
        bonus_equilibrage_sang_regain_sante = self.modele.debug_bonus_sang_regain_sante
        

        
        # degat des sorts   BASIQUE
        bonus_odin = 0
        nombre_aleatoire_pour_odin = random.randint(0, 100)
        if (self.modele.stigma_joueur_bonus == "Faveurs d'Odin") and (nombre_aleatoire_pour_odin <= 8):
            bonus_odin = 500
        bonus_malediction_mana = 0
        bonus_hyde = 0
        if self.modele.miss_hyde_transformation :
            bonus_hyde = 50
        if self.modele.malediction_du_mana:
            bonus_malediction_mana = 25
        bonus_adrenaline = 0
        if self.modele.utilise_pousse_adrenaline:
            bonus_adrenaline = 50
        bonus_talent = 0
        if self.modele.suroxygenation and (self.modele.nombre_de_tours == 1):
            bonus_talent = 200
        bonus_hydromel = 0
        if self.modele.utilise_hydromel:
            bonus_hydromel = 50
        bonus_orbe_de_folie = 0
        if self.modele.utilise_orbe_de_folie:
            bonus_orbe_de_folie = 300
        bonus_monstre_gele = 0
        if self.modele.monstre_est_gele:
            bonus_monstre_gele = 100
        bonus_stigma = 0
        if self.modele.stigma_joueur_positif == "Diligent":
            bonus_stigma = 50
        elif self.modele.stigma_joueur_positif == "Forces Obscures":
            bonus_stigma = 25
        elif (self.modele.stigma_joueur_positif == "Chaos Emotionel") and (
            self.modele.points_de_vie < (self.modele.points_de_vie_max * 0.10)
        ):
            bonus_stigma += 300
        if self.modele.stigma_monstre_negatif == "Astralien":
            bonus_stigma += 15
        bonus_artefact = 0
        if "Morceau d'Ether Fragile" in self.modele.liste_dartefacts_optionels:
            bonus_artefact += 25
        malus_stigma = 0
        if self.modele.stigma_joueur_negatif == "Serment d'Hyppocrate":
            malus_stigma = 25
        if self.modele.stigma_monstre_positif == "Lignée Royale":
            malus_stigma += 50
        self.modele.DEGATBONUSSORTS = (
            (self.modele.numero_de_letage * 2)
            + (self.modele.points_de_intelligence * 10)
            + (self.modele.points_de_mana_max // 10)
            + bonus_malediction_mana
            + bonus_adrenaline
            + bonus_hydromel
            + bonus_orbe_de_folie
            + bonus_monstre_gele
            + bonus_stigma
            + bonus_talent
            + bonus_odin
            + bonus_hyde
            + bonus_equilibrage_sort
            + bonus_artefact
            + self.modele.accumulation_degat_sort
        )
        # ATTENTION : la résistance du monstre n'est plus retirée ici. Elle
        # l'était en plus de la réduction appliquée au sort (BONUSREDUCTIONDEGAT),
        # donc les sorts la subissaient deux fois et les techniques une seule.
        self.modele.DEGATBONUSSORTS -= malus_stigma
        if self.modele.stigma_monstre_positif == "Esotericisme":
            self.modele.DEGATBONUSSORTS = -100

        amelioration_degats_totaux = 0
        if "Cape Victorieuse" in self.modele.liste_dartefacts_optionels:
            amelioration_degats_totaux += (self.modele.nombre_de_monstres_tues * 0.5)
        if "Contrat de Travail" in self.modele.liste_dartefacts_optionels:
            amelioration_degats_totaux += round(self.modele.nombre_de_gold // 50)
        amelioration_degats_totaux = min(amelioration_degats_totaux, PLAFOND_AMELIORATION_DEGATS_TOTAUX)
        self.modele.DEGATBONUSSORTS += ((amelioration_degats_totaux / 100)* self.modele.DEGATBONUSSORTS)

        bonus_esquive = round(self.modele.taux_de_esquive / 2)
        self.modele.CHANCEDETOUCHERBONUS = bonus_esquive

        # degat des attaques
        bonus_odin = 0
        nombre_aleatoire_pour_odin = random.randint(0, 100)
        if (self.modele.stigma_joueur_bonus == "Faveurs d'Odin") and (nombre_aleatoire_pour_odin <= 8):
            bonus_odin = 500
        bonus_hyde = 0
        if self.modele.miss_hyde_transformation :
            bonus_hyde = 50
        bonus_adrenaline = 0
        if self.modele.utilise_pousse_adrenaline:
            bonus_adrenaline = 50
        bonus_talent = 0
        if self.modele.suroxygenation and (self.modele.nombre_de_tours == 1):
            bonus_talent = 200
        bonus_ambroisie = 0
        if self.modele.utilise_ambroisie:
            bonus_ambroisie = 50
        bonus_orbe_de_furie = 0
        if self.modele.utilise_orbe_de_furie:
            bonus_orbe_de_furie = 300
        bonus_monstre_gele = 0
        if self.modele.monstre_est_gele:
            bonus_monstre_gele = 100
        bonus_stigma = 0
        if self.modele.stigma_joueur_positif == "Solide":
            bonus_stigma = 50
        elif self.modele.stigma_joueur_positif == "Forces Obscures":
            bonus_stigma = 25
        elif (self.modele.stigma_joueur_positif == "Chaos Emotionel") and (
            self.modele.points_de_vie < (self.modele.points_de_vie_max * 0.10)
        ):
            bonus_stigma = 300
        if self.modele.stigma_monstre_negatif == "Fragile":
            bonus_stigma += 10
        bonus_artefact = 0
        if "Epée de Damocles" in self.modele.liste_dartefacts_optionels:
            bonus_artefact += 25
        malus_stigma = 0
        if self.modele.stigma_joueur_negatif == "Serment d'Hyppocrate":
            malus_stigma = 25
        elif self.modele.stigma_joueur_negatif == "Manchot":
            malus_stigma = 50
        if self.modele.stigma_monstre_negatif == "Gluantesque":
            malus_stigma += 10
        self.modele.DEGATBONUSATTAQUE = (
            (self.modele.numero_de_letage * 2) #4
            + (self.modele.points_de_force * 10) #400
            + (self.modele.points_de_vie_max // 10) #41
            + bonus_adrenaline
            + bonus_ambroisie
            + bonus_orbe_de_furie
            + bonus_monstre_gele
            + bonus_stigma
            + bonus_talent
            + bonus_odin
            + bonus_hyde
            + bonus_equilibrage_technique
            + bonus_artefact
            + self.modele.accumulation_degat_technique
        )
        self.modele.DEGATBONUSATTAQUE -= malus_stigma

        amelioration_degats_totaux = 0
        if "Cape Victorieuse" in self.modele.liste_dartefacts_optionels:
            amelioration_degats_totaux += (self.modele.nombre_de_monstres_tues * 0.5)
        if "Contrat de Travail" in self.modele.liste_dartefacts_optionels:
            amelioration_degats_totaux += round(self.modele.nombre_de_gold // 50)
        amelioration_degats_totaux = min(amelioration_degats_totaux, PLAFOND_AMELIORATION_DEGATS_TOTAUX)
        self.modele.DEGATBONUSATTAQUE += ((amelioration_degats_totaux / 100)* self.modele.DEGATBONUSATTAQUE)

        # degat des sorts crit
        bonus_stigma = 0
        if self.modele.stigma_monstre_positif == "Flocon de Neige":
            bonus_stigma = 50
        malus_stigma = 0
        if self.modele.stigma_joueur_negatif == "Famine":
            malus_stigma = 50
        self.modele.DEGATBONUSSORTCRITIQUE = (
            bonus_stigma + bonus_equilibrage_sort_critique
        )
        self.modele.DEGATBONUSSORTCRITIQUE -= malus_stigma
        if "Chaine de Main" in self.modele.liste_dartefacts_optionels:
            self.modele.DEGATBONUSSORTCRITIQUE += 100
            

        # degat des attaques crit
        bonus_stigma = 0
        if self.modele.stigma_joueur_positif == "Flocon de Neige":
            bonus_stigma = 50
        malus_stigma = 0
        if self.modele.stigma_joueur_negatif == "Famine":
            malus_stigma = 50
        self.modele.DEGATBONUSATTAQUECRITIQUE = (
            bonus_stigma + bonus_equilibrage_technique_critique
        )
        self.modele.DEGATBONUSATTAQUECRITIQUE -= malus_stigma


        # degat des attk de feu    ELEMENTAIRE
        bonus_talent = 0
        if self.modele.affinite_au_feu:
            bonus_talent += 25
        bonus_stigma = 0
        if self.modele.stigma_monstre_negatif == "Cryolien":
            bonus_stigma += 20
        bonus_gel = 0
        if self.modele.monstre_est_gele and self.modele.choc_thermique:
            bonus_gel = 200
        bonus_benediction_chamane = 0
        if self.Player.benediction == "Incandescent":
            bonus_benediction_chamane = 75
        bonus_uppgrade = self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Charge de Feu"]
        self.modele.DEGATBONUSATTAQUEFEU = bonus_talent + bonus_stigma + bonus_gel + bonus_uppgrade + bonus_benediction_chamane + bonus_equilibrage_technique_feu

        # degat des sorts de feu
        bonus_talent = 0
        if self.modele.affinite_au_feu:
            bonus_talent += 25
        bonus_stigma = 0
        if self.modele.stigma_monstre_negatif == "Cryolien":
            bonus_stigma += 20
        bonus_gel = 0
        if self.modele.monstre_est_gele and self.modele.choc_thermique:
            bonus_gel = 200
        bonus_benediction_chamane = 0
        if self.Player.benediction == "Incandescent":
            bonus_benediction_chamane = 75
        bonus_uppgrade = self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Charge de Feu"]
        self.modele.DEGATBONUSSORTFEU = bonus_talent + bonus_stigma + bonus_gel + bonus_uppgrade + bonus_benediction_chamane + bonus_equilibrage_sort_feu

        # degat du feu
        bonus_talent = 0
        if self.modele.surchauffe:
            bonus_talent += 20
        bonus_stigma = 0
        if self.modele.stigma_joueur_bonus == "Ange de Feu":
            bonus_stigma += 300
        if self.modele.stigma_monstre_negatif == "Cryolien":
            bonus_stigma += 20
        self.modele.DEGATBONUSFEU = bonus_talent + bonus_stigma

        # degat des attk de foudre
        bonus_talent = 0
        if self.modele.affinite_electrique:
            bonus_talent += 25
        bonus_stigma = 0
        if self.modele.stigma_monstre_negatif == "Surcharge Facile":
            bonus_stigma += 25
        malus_stigma = 0
        if self.modele.stigma_monstre_positif == "Electrodynamisme":
            malus_stigma += 20
        bonus_benediction_chamane = 0
        if self.Player.benediction == "Conducteur":
            bonus_benediction_chamane = 75
        bonus_uppgrade = self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Charge de Foudre"]
        self.modele.DEGATBONUSATTAQUEFOUDRE = bonus_talent + bonus_stigma + bonus_uppgrade + bonus_benediction_chamane + bonus_equilibrage_technique_foudre
        self.modele.DEGATBONUSATTAQUEFOUDRE -= malus_stigma

        # degat des sorts de foudre
        bonus_talent = 0
        if self.modele.affinite_electrique:
            bonus_talent += 25
        bonus_stigma = 0
        if self.modele.stigma_monstre_negatif == "Surcharge Facile":
            bonus_stigma += 25
        malus_stigma = 0
        if self.modele.stigma_monstre_positif == "Electrodynamisme":
            malus_stigma += 20
        bonus_benediction_chamane = 0
        if self.Player.benediction == "Conducteur":
            bonus_benediction_chamane = 75
        bonus_uppgrade = self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Charge de Foudre"]
        self.modele.DEGATBONUSSORTFOUDRE = bonus_talent + bonus_stigma + bonus_uppgrade + bonus_benediction_chamane + bonus_equilibrage_sort_foudre
        self.modele.DEGATBONUSSORTFOUDRE -= malus_stigma

        # degat de la paralysie (par neurotransmitteur)
        self.modele.DEGATPARALYSIE = 2  # %de vie du monstre

        # degat du feu electrique (par luciole)
        self.modele.DEGATFEUELECTRIQUE = 4  # %de vie du monstre

        # degat des attk de glace
        bonus_talent = 0
        if self.modele.affinite_de_glace:
            bonus_talent += 25
        bonus_stigma = 0
        if self.modele.stigma_monstre_negatif == "Pyrolien":
            bonus_stigma += 15
        elif self.modele.stigma_monstre_negatif == "Cryophobia":
            bonus_stigma += 15
        bonus_benediction_chamane = 0
        if self.Player.benediction == "Glaciaire":
            bonus_benediction_chamane = 75
        bonus_uppgrade = self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Charge de Glace"]
        self.modele.DEGATBONUSATTAQUEGLACE = bonus_talent + bonus_stigma + bonus_uppgrade + bonus_benediction_chamane + bonus_equilibrage_technique_glace

        # degat des sorts de glace
        bonus_talent = 0
        if self.modele.affinite_de_glace:
            bonus_talent += 25
        bonus_stigma = 0
        if self.modele.stigma_monstre_negatif == "Pyrolien":
            bonus_stigma += 25
        elif self.modele.stigma_monstre_negatif == "Cryophobia":
            bonus_stigma += 45
        bonus_benediction_chamane = 0
        if self.Player.benediction == "Glaciaire":
            bonus_benediction_chamane = 75
        bonus_uppgrade = self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Charge de Glace"]
        self.modele.DEGATBONUSSORTGLACE = bonus_talent + bonus_stigma + bonus_uppgrade + bonus_benediction_chamane + bonus_equilibrage_sort_glace

        # degat de la gelure (quand on en sort)
        self.modele.DEGATGELURE = 5  # %de vie du monstre

        # degat des attk de terre
        bonus_talent = 0
        if self.modele.affinite_de_terre:
            bonus_talent += 25
        malus_stigma = 0
        if self.modele.stigma_monstre_negatif == "Géodynamisme":
            malus_stigma += 25
        bonus_benediction_chamane = 0
        if self.Player.benediction == "Rocailleux":
            bonus_benediction_chamane = 75
        bonus_uppgrade = self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Charge de Terre"]
        self.modele.DEGATBONUSATTAQUETERRE = bonus_talent + bonus_uppgrade + bonus_benediction_chamane + bonus_equilibrage_technique_terre
        self.modele.DEGATBONUSATTAQUETERRE -= malus_stigma

        # degat des sorts de terre
        bonus_talent = 0
        if self.modele.affinite_de_terre:
            bonus_talent += 25
        malus_stigma = 0
        if self.modele.stigma_monstre_negatif == "Géodynamisme":
            malus_stigma += 25
        bonus_benediction_chamane = 0
        if self.Player.benediction == "Rocailleux":
            bonus_benediction_chamane = 75
        bonus_uppgrade = self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Charge de Terre"]
        self.modele.DEGATBONUSSORTTERRE = bonus_talent + bonus_uppgrade + bonus_benediction_chamane + bonus_equilibrage_sort_terre
        self.modele.DEGATBONUSSORTTERRE -= malus_stigma

        # degat de la lapidation
        bonus_artefact = 0
        if "Haricot Magique" in self.modele.liste_dartefacts_optionels:
            bonus_artefact = 25
        self.modele.DEGATLAPIDATION = bonus_artefact  # %de degat supp

        # degat des attk physique
        bonus_talent = 0
        if self.modele.affinite_de_effort:
            bonus_talent += 25
        bonus_stigma = 0
        if self.modele.stigma_monstre_negatif == "Anisotrope":
            bonus_stigma += 25
        bonus_benediction_chamane = 0
        if self.Player.benediction == "Musclé":
            bonus_benediction_chamane = 75
        bonus_uppgrade = self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Charge de Chair"]
        self.modele.DEGATBONUSATTAQUEPHYSIQUE = bonus_talent + bonus_stigma + bonus_uppgrade + bonus_benediction_chamane + bonus_equilibrage_technique_physique

        # degat des sorts physiques
        bonus_talent = 0
        if self.modele.affinite_de_effort:
            bonus_talent += 25
        bonus_stigma = 0
        if self.modele.stigma_monstre_negatif == "Anisotrope":
            bonus_stigma += 25
        bonus_benediction_chamane = 0
        if self.Player.benediction == "Musclé":
            bonus_benediction_chamane = 75
        bonus_uppgrade = self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Charge de Chair"]
        self.modele.DEGATBONUSSORTPHYSIQUE = bonus_talent + bonus_stigma + bonus_uppgrade + bonus_benediction_chamane + bonus_equilibrage_sort_physique

        # degat des attk de sang
        bonus_talent = 0
        if self.modele.affinite_du_sang:
            bonus_talent += 25
        bonus_stigma = 0
        if self.modele.stigma_monstre_negatif == "Faible Hematopoïèse":
            bonus_stigma += 25
        bonus_benediction_chamane = 0
        if self.Player.benediction == "Sain":
            bonus_benediction_chamane = 75
        bonus_uppgrade = self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Charge de Sang"]
        self.modele.DEGATBONUSATTAQUESANG = bonus_talent + bonus_stigma + bonus_uppgrade + bonus_benediction_chamane + bonus_equilibrage_technique_sang

        # degat des sorts de sang
        bonus_talent = 0
        if self.modele.affinite_du_sang:
            bonus_talent += 25
        bonus_stigma = 0
        if self.modele.stigma_monstre_negatif == "Faible Hematopoïèse":
            bonus_stigma += 25
        bonus_benediction_chamane = 0
        if self.Player.benediction == "Sain":
            bonus_benediction_chamane = 75
        bonus_uppgrade = self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Charge de Sang"]
        self.modele.DEGATBONUSSORTSANG = bonus_talent + bonus_stigma + bonus_uppgrade + bonus_benediction_chamane + bonus_equilibrage_sort_sang

        # degat de la saignée
        bonus_talent = 0
        self.modele.DEGATSAIGNEE = bonus_talent

        # soin de la saignée
        bonus_talent = 0
        if self.modele.nectar:
            bonus_talent += 30
        self.modele.SOINSSAIGNEE = bonus_talent + bonus_equilibrage_sang_regain_sante
        if self.modele.stigma_monstre_negatif == "Sang Doré":
            self.modele.SOINSSAIGNEE += self.modele.SOINSSAIGNEE

        # attk âme
        self.modele.PIRADEGAT = self.modele.nombre_de_monstres_tues // 2
        self.modele.PIRABRULE = 5 * (self.modele.nombre_de_monstres_tues // 5)
        self.modele.PIRABRULETOUR = self.modele.nombre_de_monstres_tues // 10

        self.modele.ELEKTRONDEGAT = self.modele.nombre_de_monstres_tues // 2
        self.modele.ELEKTRONPARALYSE = 5 * (self.modele.nombre_de_monstres_tues // 10)
        self.modele.ELEKTRONPARALYSETOUR = self.modele.nombre_de_monstres_tues // 13

        self.modele.TSUMETASADEGAT = self.modele.nombre_de_monstres_tues // 2
        self.modele.TSUMETASAGELE = 5 * (self.modele.nombre_de_monstres_tues // 5)
        self.modele.TSUMETASAGELETOUR = self.modele.nombre_de_monstres_tues // 10

        self.modele.MATHAIRDEGAT = self.modele.nombre_de_monstres_tues // 2
        self.modele.MATHAIRLAPIDE = 10 * (self.modele.nombre_de_monstres_tues // 10)

        self.modele.FOSDEGAT = self.modele.nombre_de_monstres_tues

        self.modele.HADDEEDEGAT = self.modele.nombre_de_monstres_tues // 2
        self.modele.HADDEEDRAIN = 8 * (self.modele.nombre_de_monstres_tues // 10)


        # pourcentage de coup critique  POURCENTAGES
        bonus_benediction = 0
        if self.modele.beni_par_feu_sacre:
            bonus_benediction += 777
        bonus_mutation = 0
        if self.modele.mutagene_vert_utilise:
            bonus_mutation = 10
        elif self.modele.grand_mutagene_vert_utilise:
            bonus_mutation = 15
        elif self.modele.mutagene_dore_utilise:
            bonus_mutation = 10
        elif self.modele.grand_mutagene_dore_utilise:
            bonus_mutation = 20
        elif (
            self.modele.mutagene_fanatique_utilise
            or self.modele.mutagene_heretique_utilise
        ):
            bonus_mutation = -1000
        self.modele.CHANCECOUPCRITIQUE = (
            self.modele.taux_de_coup_critique
            + self.modele.taux_de_esquive // 3
            + bonus_mutation
            + bonus_benediction
        )

        # pourcentage de sort critique
        bonus_benediction = 0
        if self.modele.beni_par_feu_sacre:
            bonus_benediction += 777
        bonus_mutation = 0
        if self.modele.mutagene_vert_utilise:
            bonus_mutation = 10
        elif self.modele.grand_mutagene_vert_utilise:
            bonus_mutation = 15
        elif self.modele.mutagene_dore_utilise:
            bonus_mutation = 10
        elif self.modele.grand_mutagene_dore_utilise:
            bonus_mutation = 20
        elif (
            self.modele.mutagene_fanatique_utilise
            or self.modele.mutagene_heretique_utilise
        ):
            bonus_mutation = -1000
        self.modele.CHANCESORTCRITIQUE = (
            self.modele.taux_de_sort_critique
            + self.modele.taux_de_esquive // 3
            + bonus_mutation
            + bonus_benediction
        )
        # pourcentage d'esquive 
        bonus_caracteristique = self.modele.taux_de_esquive
        bonus_artefact = 0
        if "Bandeau Catharsis" in self.modele.liste_dartefacts_optionels:
            bonus_artefact += 5
        # POURQUOI un plafond : l'esquive protège déjà des coups, augmente la
        # chance de toucher (moitié) et de critique (tiers). Au dessus de 50,
        # un monstre à 85 % de touche tomberait sous 35 % : trop proche de
        # l'intouchable. Les deux autres bonus gardent la valeur non plafonnée.
        self.modele.CHANCEBONUSESQUIVE = min(ESQUIVE_UTILE_MAX, bonus_caracteristique + bonus_artefact)

        # pourcentage d'enflammer
        bonus_vulnerable = 0
        bonus_vulnerable = self.modele.monstre_niveau_de_vulnerabilite * 5
        bonus_charge = 0
        if "Element [Feu] Surchargé" in self.modele.liste_dartefacts_optionels:
            bonus_charge += 10
        malus_stigma = 0
        if self.modele.stigma_monstre_positif == "Roche Ténébreuse":
            malus_stigma = 100
        self.modele.CHANCEBONUSDEFAIREBRULER = bonus_vulnerable + bonus_charge + round(self.modele.accumulation_chance_brulure)
        self.modele.CHANCEBONUSDEFAIREBRULER -= malus_stigma
        # pourcentage de paralyser
        bonus_vulnerable = 0
        bonus_vulnerable = self.modele.monstre_niveau_de_vulnerabilite * 5
        bonus_charge = 0
        if "Element [Foudre] Surchargé" in self.modele.liste_dartefacts_optionels:
            bonus_charge += 10
        bonus_artefact = 0
        if "Fiole d'Eclair" in self.modele.liste_dartefacts_optionels:
            bonus_artefact += 5
        self.modele.CHANCEBONUSDEFAIREPARALYSER = bonus_vulnerable + bonus_charge + bonus_artefact + round(self.modele.accumulation_chance_paralysie)
        
        # pourcentage de geler
        bonus_vulnerable = 0
        bonus_vulnerable = self.modele.monstre_niveau_de_vulnerabilite * 5
        bonus_charge = 0
        if "Element [Glace] Surchargé" in self.modele.liste_dartefacts_optionels:
            bonus_charge += 15
        malus_stigma = 0
        if self.modele.stigma_monstre_bonus == "Nordique":
            malus_stigma = 100
        bonus_stigma = 0
        if self.modele.stigma_monstre_negatif == "Conductivité Thermique":
            bonus_stigma = 25
        self.modele.CHANCEBONUSDEFAIREGELER = 0 + bonus_vulnerable + bonus_charge + round(self.modele.accumulation_chance_gelure) + bonus_stigma
        self.modele.CHANCEBONUSDEFAIREGELER -= malus_stigma
        # pourcentage de lapider
        bonus_vulnerable = 0
        bonus_vulnerable = self.modele.monstre_niveau_de_vulnerabilite * 5
        bonus_charge = 0
        if "Element [Terre] Surchargé" in self.modele.liste_dartefacts_optionels:
            bonus_charge += 15
        bonus_artefact = 0
        if "Fossile Figé" in self.modele.liste_dartefacts_optionels:
            bonus_artefact += 7
        malus_stigma = 0
        if self.modele.stigma_monstre_positif == "Armure de Plates":
            malus_stigma = 100
        self.modele.CHANCEBONUSDEFAIRELAPIDER = 0 + bonus_vulnerable + bonus_charge + bonus_artefact + round(self.modele.accumulation_chance_lapider)
        self.modele.CHANCEBONUSDEFAIRELAPIDER -= malus_stigma

        # pourcentage de saignee
        bonus_vulnerable = 0
        bonus_vulnerable = self.modele.monstre_niveau_de_vulnerabilite * 5
        bonus_charge = 0
        if "Element [Sang] Surchargé" in self.modele.liste_dartefacts_optionels:
            bonus_charge += 15
        malus_stigma = 0
        if self.modele.stigma_monstre_bonus == "Corps d'Acier":
            malus_stigma = 100
        self.modele.CHANCEBONUSDEFAIRESAIGNER = 0 + bonus_vulnerable + bonus_charge + round(self.modele.accumulation_chance_drainer)
        self.modele.CHANCEBONUSDEFAIRESAIGNER -= malus_stigma

        # pourcentage de louper une attaque
        malus_envol = 0
        if self.modele.monstre_est_envol:
            malus_envol = 30
        self.modele.CHANCERATERATTAQUE = malus_envol

        # pourcentage de louper un sort 
        malus_envol = 0
        if self.modele.monstre_est_envol:
            malus_envol = 30
        self.modele.CHANCERATERSORT = malus_envol

        # tours benef pour le feu    TOURS DALTERATION ETAT
        bonus_talent = 0
        if self.modele.aura_de_feu:
            bonus_talent += 3
        bonus_artefact = 0
        if "Charbon Primordial" in self.modele.liste_dartefacts_optionels:
            bonus_artefact += 1
        malus_stigma = 0
        self.modele.TOURBONUSENNEMIENFEU = bonus_talent + bonus_artefact
        # tours benef pour la glace
        bonus_talent = 0
        if self.modele.ere_glaciaire:
            bonus_talent += 3
        bonus_artefact = 0
        if "Miette de Pain Congelée" in self.modele.liste_dartefacts_optionels:
            bonus_artefact = 2
        if "Saphir de Gel" in self.modele.liste_dartefacts_optionels:
            bonus_artefact += 1
        malus_stigma = 0
        if self.modele.stigma_monstre_bonus == "Nordique":
            malus_stigma = 100
        self.modele.TOURBONUSENNEMIENGLACE = bonus_talent + bonus_artefact
        self.modele.TOURBONUSENNEMIENGLACE -= malus_stigma
        # tours benef pour la paralysie
        bonus_talent = 0
        malus_stigma = 0
        self.modele.TOURBONUSENNEMIENPARALYSIE = bonus_talent
        self.modele.TOURBONUSENNEMIENPARALYSIE -= malus_stigma
        # tours quon se prend pour le feu
        malus_talent = 0
        bonus_talent = 0
        if self.modele.peau_de_fer:
            bonus_talent = 50
        self.modele.TOURBONUSJOUEURENFEU = malus_talent
        self.modele.TOURBONUSJOUEURENFEU -= bonus_talent
        # tours quon se prend pour la glace (pas de modificateurs pour l'instant)
        self.modele.TOURBONUSJOUEURENGLACE = 0
        # tours quon se prend pour la paralysie (pas de modificateurs pour l'instant)
        self.modele.TOURBONUSJOUEURENPARALYSIE = 0

        # degat supplementaire d'item (pas de modificateurs pour l'instant)    ITEMS
        self.modele.DEGATBONUSITEM = 0
        # soin supplementaire d'item
        bonus_stigma = 0
        if self.modele.stigma_joueur_positif == "Pharmacodynamisme":
            bonus_stigma = 100
        bonus_talent = 0
        if self.modele.carte_du_gout:
            bonus_talent = 50
        self.modele.SUPPORTBONUSITEM = bonus_stigma + bonus_talent

        # pourcentage de se faire paralyser    ENVERS LE JOUEUR
        bonus_talent = 0
        if self.modele.coeur_de_glace:
            bonus_talent = -50
        bonus_stigma = 0
        if self.modele.stigma_joueur_positif == "Endurci":
            bonus_stigma = -100
        self.modele.CHANCEBONUSJOUEURPARALYSE = bonus_talent + bonus_stigma
        # pourcentage de degat bonus de technique contre le joueur
        bonus_gel = 0
        if self.modele.est_gele:
            bonus_gel = 50
        bonus_artefact = 0
        if "Bandeau Catharsis" in self.modele.liste_dartefacts_optionels:
            bonus_artefact += 10
        bonus_hyde = 0
        if self.modele.miss_hyde_transformation :
            bonus_hyde = 50
        bonus_stigma = 0
        if self.modele.stigma_joueur_negatif == "Attache Physique":
            bonus_stigma = 25
        bonus_force = self.modele.monstre_points_de_force * 10
        self.modele.DEGATTECHNIQUEBONUSDUMONSTRE = bonus_gel + bonus_stigma + bonus_force + bonus_artefact + bonus_hyde + self.modele.DEGATBONUSMONSTREBERSERKER
        # pourcentage de degat bonus de sort contre le joueur
        bonus_gel = 0
        if self.modele.est_gele:
            bonus_gel = 50
        bonus_hyde = 0
        if self.modele.miss_hyde_transformation :
            bonus_hyde = 50
        bonus_artefact = 0
        if "Bandeau Catharsis" in self.modele.liste_dartefacts_optionels:
            bonus_artefact += 15
        bonus_stigma = 0
        if self.modele.stigma_joueur_negatif == "Attache Physique":
            bonus_stigma = 25
        bonus_force = self.modele.monstre_points_de_intelligence * 10
        self.modele.DEGATSORTBONUSDUMONSTRE = bonus_gel + bonus_stigma + bonus_force + bonus_artefact + bonus_hyde + self.modele.DEGATBONUSMONSTREBERSERKER
        # bonus de dégâts des attaques NORMALES des monstres, selon l'étage.
        # Additif : il s'ajoute aux autres bonus du monstre (sa force...), comme
        # les bonus du joueur. Les attaques spéciales ne le reçoivent pas : leur
        # base grandit déjà d'un point par étage (« base + niveau du monstre »).
        self.modele.DEGATBONUSETAGEDUMONSTRE = BONUS_DEGATS_MONSTRE_PAR_ETAGE * max(0, self.modele.numero_de_letage - 1)
        # pourcentage de se faire enflammer (pas de modificateurs pour l'instant)
        self.modele.CHANCEBONUSJOUEURENFEU = 0
        # pourcentage de se faire geler (pas de modificateurs pour l'instant)
        self.modele.CHANCEBONUSJOUEURENGLACE = 0
        # pourcentage de se faire saigner (pas de modificateurs pour l'instant)
        self.modele.CHANCEBONUSJOUEURENSANG = 0
        # pourcentage de se faire lapider (pas de modificateurs pour l'instant)
        self.modele.CHANCEBONUSJOUEURLAPIDE = 0
        # reduction des degats de base contre les monstres
        # (formules dans coliseum/combat/reductions.py)
        self.modele.BONUSREDUCTIONDEGAT = reduction_en_pourcentage(
            self.modele.monstre_points_de_resistance + self.modele.monstre_gain_de_defence_nombre
        )

        # reduction des degats de base contre les joueurs
        # Miss Hyde retirait 50 % de réduction ; à 2 % par point, cela fait 25 points.
        malus_hyde = 0
        if self.modele.miss_hyde_transformation :
            malus_hyde = 25
        self.modele.DEFENCEEFFICACE = max(0, self.modele.points_de_defence + self.modele.gain_de_defence - malus_hyde)
        # gardé pour l'affichage : part de réduction en pourcentage seulement
        self.modele.BONUSREDUCTIONDEGATSURJOUEUR = reduction_en_pourcentage(self.modele.DEFENCEEFFICACE)

        # reduction du cout en mana des sorts generaux
        bonus_talent = 0
        if self.modele.connaissance:
            bonus_talent = 20
        self.modele.BONUSREDUCTIONMANASORTTOUT = bonus_talent

        # reduction du cout en mana des sorts de terre
        bonus_talent = 0
        if self.modele.poussiere_de_diamant:
            bonus_talent = round(
                (self.modele.points_de_vie * 100) / (self.modele.points_de_vie_max)
            )
            bonus_talent = 100 - bonus_talent  # Pour avoir l'inverse de la vie possédée, aka le reste de vie.
            if bonus_talent > 50:
                bonus_talent = 50
        self.modele.BONUSREDUCTIONMANASORTTERRE = bonus_talent

        # reduction du cout en mana des sorts de foudre
        bonus_talent = 0
        if self.modele.energiseur:
            bonus_talent = 30
        self.modele.BONUSREDUCTIONMANASORTFOUDRE = bonus_talent

        # reduction du cout en mana des sorts de feu
        bonus_talent = 0
        if self.modele.utilise_rafale:
            bonus_talent = -200
        self.modele.BONUSREDUCTIONMANASORTFEU = bonus_talent
        # cout mana malediction
        malus_alteration_etat = 0
        if self.modele.est_maudit_par_le_mana:
            malus_alteration_etat = 75
            if "Morceau de Plomb" in self.modele.liste_dartefacts_optionels:
                malus_alteration_etat = 40
        self.modele.BONUSCOUTMALEDICTIONMANA = malus_alteration_etat
        # cout vie malediction
        malus_alteration_etat = 0
        if self.modele.est_maudit_par_la_vie or self.modele.est_maudit_par_le_gold:
            malus_alteration_etat = 10
            if "Chaperon Rouge" in self.modele.liste_dartefacts_optionels:
                malus_alteration_etat = 6.5
        self.modele.BONUSCOUTMALEDICTIONVIEOUGOLD = malus_alteration_etat
        #chance du monstre de faire un sort critique :
        malus_stigma = 0
        if self.modele.stigma_monstre_negatif == "Divinement Renié":
            malus_stigma = 100
        self.modele.CHANCESORTCRITIQUEDUMONSTRE = malus_stigma
        #chance du monstre de faire un coup critique :
        self.modele.CHANCESORTCRITIQUEDUMONSTRE = 0

    def SetNameFromLevelAndBoss(self):
        self.modele.monstre_level = self.modele.numero_de_letage
        nom = self._nom_du_monstre_a_affronter()
        if nom is not None:
            self.modele.monstre_nom = nom

    def _nom_du_monstre_a_affronter(self):
        """Nom du monstre de ce combat, ou None pour garder celui du modèle."""
        if self.modele.monstre_EstUnBoss:
            nom = self._nom_du_boss()
        elif self.modele.boss_histoire:
            nom = BOSS_D_HISTOIRE_PAR_PERSONNAGE.get(self.modele.nom_du_personnage)
        else:
            nom = self._nom_du_monstre_de_l_etage()
        # ATTENTION : la mimique est décidée en dernier, après le tirage au sort
        # du monstre de l'étage. Ce tirage inutile est conservé volontairement :
        # le supprimer décalerait tous les tirages aléatoires suivants.
        if self.modele.est_une_mimique:
            nom = "Mimique"
        return nom

    def _nom_du_boss(self):
        if self.modele.etage_alternatif:
            return self.modele.liste_de_boss_alternatif[self.modele.numero_de_letage - 1]
        if self.Player.nom_de_letage == "Limbes Flétrissants":
            return self.modele.liste_de_boss_rush[self.Player.numero_boss_alt - 1]
        return self.modele.liste_de_boss[self.modele.numero_de_letage]

    def _nom_du_monstre_de_l_etage(self):
        etage = self.modele.numero_de_letage
        if etage == 0:
            return "Drone de Sécurité YucaTech Inc."
        monstres_par_etages = (
            ((1, 2), self.modele.liste_de_monstres_etage_1_2),
            ((3, 4), self.modele.liste_de_monstres_etage_3_4),
            ((5, 6), self.modele.liste_de_monstres_etage_5_6),
            ((7, 8), self.modele.liste_de_monstres_etage_7_8),
            ((9, 10, 11), self.modele.liste_de_monstres_etage_9_10_11),
        )
        for etages, monstres in monstres_par_etages:
            if etage in etages:
                return monstres[random.randint(0, len(monstres) - 1)]
        # Un monstre « dopé » des derniers étages dépasse l'étage 11 : aucun
        # monstre n'est prévu, le modèle garde son nom par défaut.
        return None

    def MonsterMaker(self):
        self.SetNameFromLevelAndBoss()
        self.SetAttributesFromName()

    def SetAttributesFromName(self):
        combat = ContexteDeCombat(self.modele, self.Player)
        fiche = fiche_du_monstre(self.modele.monstre_nom, combat)
        fiche.appliquer(self.modele)
        if fiche.bonus_de_vie_de_l_etage:
            self.modele.monstre_points_de_vie_max += combat.bonus_vie
        self.modele.monstre_points_de_vie = self.modele.monstre_points_de_vie_max
        self.modele.monstre_points_de_mana = self.modele.monstre_points_de_mana_max
        if not self.modele.monstre_EstUnBoss and self.Player.battu_le_sacrifie:
            liste_de_gardien = ["Voluntad Káak", "Voluntad Hielo", "Voluntad Le Rayo", "Voluntad Le Luumo", "Voluntad U Kiikel", "Voluntad U Wíinkilal", "Voluntad Tin Tuukul"]
            nombre_aleatoire = random.randint(0, 100)
            if nombre_aleatoire < 50:
                gardien_aleatoire = random.randint(0, 6)
                self.modele.monstre_tags.append(liste_de_gardien[gardien_aleatoire])
                liste_de_gardien.pop(gardien_aleatoire)
            if nombre_aleatoire < 50 and self.modele.numero_de_letage > 4 :
                gardien_aleatoire = random.randint(0, 5)
                self.modele.monstre_tags.append(liste_de_gardien[gardien_aleatoire])

    def AfficheMonstreNiveauEtMusique(self):
        numero_musique = self.modele.numero_de_letage
        if "Monstre De Niveau Superieur" in self.modele.player_tags:
            numero_musique -= 1
        if "Monstre Dopé" in self.modele.player_tags:
            numero_musique -= 2

        if (numero_musique == 10 and self.Player.nom_de_letage != "Limbes Flétrissants") or self.Player.mode_jukebox :
            nom_de_la_musique = self.Player.musique_combat_10
        elif self.modele.est_une_mimique:
            numero_etage_pour_mimique = str(int( self.modele.numero_de_letage / 2))
            nom_de_la_musique = "mimique_" + numero_etage_pour_mimique
            if self.modele.numero_de_letage not in [2,4,6,8,10]:
                nom_de_la_musique = "mimique_1"
        elif self.modele.boss_histoire:
            nom_de_la_musique = "story_end"
        elif not self.modele.monstre_EstUnBoss:
            nom_de_la_musique =  f"battle_theme_{numero_musique}"
        elif self.Player.nom_de_letage == "Limbes Flétrissants":
            if self.modele.monstre_nom == "Roi Gluant":
                nom_de_la_musique = "battle_theme_1"
            else:
                nom_de_la_musique = f"alt_{self.Player.numero_boss_alt}_phase_1"
        else:
            nom_de_la_musique = f"boss_{numero_musique}"
        if self.modele.etage_alternatif and not self.modele.est_une_mimique and not self.Player.mode_jukebox:
            nom_de_la_musique += "_alt"
        musique = self.modele.CHEMINABSOLUMUSIQUE + nom_de_la_musique
        self.vue.AfficheMonstreLevelMusique(
            self.modele.monstre_nom, self.modele.monstre_level, musique
        )

    def PremierTourJoueur(self):
        if self.modele.pandemonium:
            self.EffetPandemoniumPiegeElementaire()
        else:
            if self.modele.rapide:
                self.EffetRapidePiegeElectrique()
            if self.modele.grand_froid:
                self.EffetGrandFroidPiegeGlace()
            if self.modele.reflex:
                self.EffetReflexPiegePhysique()
        if self.modele.stigma_joueur_positif == "Monsieur Loyal":
            if (
                not self.modele.dernier_choix_effectue
                and not self.modele.monstre_EstUnBoss
                and not self.modele.est_une_mimique
            ):
                self.EffetStigmaDernierChoix()
        if self.modele.stigma_joueur_positif == "Bénie par les Fées":
            self.EffetStigmaBeniParLesFees()
        if self.modele.stigma_joueur_negatif == "Fatigue Chronique":
            self.EffetStigmaFatigueChronique()
        if self.modele.stigma_joueur_negatif == "Flemme":
            self.EffetStigmaFlemme()
        elif self.modele.stigma_joueur_negatif == "Ange Déchue":
            self.EffetStigmaAngeDechue()
        if self.modele.stigma_joueur_bonus == "Bergentruckung":
            self.EffetStigmaBergentruckung()
        limite_vie = round(self.modele.points_de_vie_max * 0.05)
        if self.modele.conditions_limites and (self.modele.points_de_vie <= limite_vie):
            self.AppliqueTalentConditionsLimites()
        if self.modele.ultra_instinct:
            self.AppliqueTalentUltraInstinct()
        if self.modele.commence_le_combat_confus:
            self.modele.est_maudit_par_les_items = True
            self.modele.est_maudit_par_les_items_nombre_tour += 5
        if "Char Leclerc 3ème Génération à Dispositif GALIX, Canon Principal 120mm et Armement Secondaire à Mitrailleuse 12,7 mm Coaxiale et Mitrailleuse de 7,62 mm en Superstructure" in self.modele.liste_dartefacts_optionels:
            self.AppliqueTank()
        if "Mage" in self.modele.liste_dartefacts_optionels:
            self.AppliqueMage()
        if "Boss Blessé" in self.modele.player_tags:
            degat = round(self.modele.monstre_points_de_vie_max * 0.15)
            self.modele.monstre_points_de_vie -= degat
        if "Totem de la Force" in self.modele.liste_dartefacts_optionels:
            self.modele.utilise_fruit_jindagee = True
            self.modele.utilise_fruit_jindagee_nombre_tour += 3
        if "Totem de la Sagesse" in self.modele.liste_dartefacts_optionels:
            self.modele.utilise_fruit_aatma = True
            self.modele.utilise_fruit_aatma_nombre_tour += 3
        if "Totem du Courage" in self.modele.liste_dartefacts_optionels:
            nombre_aleatoire = random.randint(1, 5)
            if nombre_aleatoire == 1:
                self.modele.accumulation_chance_brulure += 4
            elif nombre_aleatoire == 2:
                self.modele.accumulation_chance_gelure += 5
            elif nombre_aleatoire == 3:
                self.modele.accumulation_chance_paralysie += 2.5
            elif nombre_aleatoire == 4:
                self.modele.accumulation_chance_lapider += 4
            elif nombre_aleatoire == 5:
                self.modele.accumulation_chance_drainer += 4
        if "Monstre Dopé" in self.Player.player_tags:
            self.modele.monstre_est_gele = True
            self.modele.monstre_est_gele_nombre_tour += 5
            self.modele.monstre_points_de_vie -= round(self.modele.monstre_points_de_vie_max * 0.1)
            self.vue.AfficheDopage()
        if self.Player.malediction == "Ascétique":
            self.modele.points_de_vie += round(self.modele.points_de_vie_max * 0.2)
            self.EquilibragePointsDeVieEtManaEtEndurance()

    def EffetRapidePiegeElectrique(self):
        element = "un piège électrique."
        random_number = random.randint(0, 100)
        if random_number < 51:
            self.modele.monstre_est_paralyse = True
            self.modele.monstre_est_paralyse_nombre_tour = 1
            phrase = "Il rentre dedans sans s'en rendre compte, et devient paralysé pendant 1 tour !"
            if self.modele.electro:
                degat = round(self.modele.monstre_points_de_vie_max * 0.1)
                self.modele.monstre_points_de_vie -= degat
                phrase += f"\nDe plus, le piège lui inflige {degat} points de dégâts !"
        else:
            self.modele.monstre_est_paralyse = False
            phrase = "Il passe a côté sans s'en rendre compte, et le piège se dissipe dans l'ether."
        self.vue.AfficherAttaquePremierTour(element, phrase)

    def EffetGrandFroidPiegeGlace(self):
        element = "un piège de glace."
        random_number = random.randint(0, 100)
        if random_number < 51:
            self.modele.monstre_est_gele = True
            self.modele.monstre_est_gele_nombre_tour = 4
            phrase = "Il rentre dedans sans s'en rendre compte, et devient gelé pendant 4 tour !"
        else:
            self.modele.monstre_est_gele = False
            phrase = "Il passe a côté sans s'en rendre compte, et le piège se dissipe dans l'ether."
        self.vue.AfficherAttaquePremierTour(element, phrase)

    def EffetReflexPiegePhysique(self):
        element = "une attaque légère ultrarapide."
        random_number = random.randint(0, 100)
        if random_number < 76:
            degat = round(self.modele.monstre_points_de_vie_max * 0.05)
            self.modele.monstre_points_de_vie -= degat
            phrase = f"Elle touche un point faible et l'ennemi s'écroule sur le sol, perdant {degat} point de vie !"
        else:
            phrase = "Elle passe a quelques centimètres de lui sans faire de dégâts."
        self.vue.AfficherAttaquePremierTour(element, phrase)

    def EffetPandemoniumPiegeElementaire(self):
        element = "un déluge de sorts envoyés a haute vitesse."
        degat = round(self.modele.monstre_points_de_vie_max * 0.07)
        self.modele.monstre_points_de_vie -= degat
        saignee = round(self.modele.monstre_points_de_vie_max * 0.04)
        saignee = self.AppliqueLimitationSaignee(saignee)
        self.modele.monstre_points_de_vie -= saignee
        self.modele.points_de_vie += saignee
        self.EquilibragePointsDeVieEtManaEtEndurance()
        phrase = (
            f"Il se retrouve paralysé pendant 2 tours,"
            f" s'embrase et gèle simultanément pendant 5 tours,"
            f" se retrouve drainé de {saignee} point de vie,"
            f" avant de perdre {degat} points de vie sous une avalanche de rochers !"
        )
        if self.modele.electro:
            degat = round(self.modele.monstre_points_de_vie_max * 0.1)
            self.modele.monstre_points_de_vie -= degat
            phrase += f"\nDe plus, l'électricité lui inflige {degat} points de dégâts !"
        self.modele.monstre_est_en_feu = True
        self.modele.monstre_est_en_feu_degat = 5
        self.modele.monstre_est_en_feu_nombre_tour += 5
        self.modele.monstre_est_gele = True
        self.modele.monstre_est_gele_nombre_tour = 5
        self.modele.monstre_est_paralyse = True
        self.modele.monstre_est_paralyse_nombre_tour = 2
        self.modele.monstre_passe_son_tour = True
        self.vue.AfficherAttaquePremierTour(element, phrase)

    def PremierTourMonstre(self):
        if self.modele.stigma_monstre_positif == "Toucher de Midas":
            self.EffetStigmaToucherDeMidas()
        elif self.modele.stigma_monstre_positif == "Siphon de Mana":
            self.EffetStigmaSiphonDeMana()
        elif self.modele.stigma_monstre_positif == "Faveurs Explosives":
            self.EffetStigmaFaveursExplosives()
        elif self.modele.stigma_monstre_positif == "Benediction Divine":
            self.EffetStigmaBenedictionDivine()
        elif self.modele.stigma_monstre_positif == "Bomberman":
            self.EffetStigmaBomberman()
        elif self.modele.stigma_monstre_positif == "Plus d'un Tour":
            self.EffetStigmaPlusDUnTour()
        if self.modele.stigma_monstre_negatif == "Megalovania":
            self.EffetStigmaMegalovania()
        elif self.modele.stigma_monstre_negatif == "Homoncule":
            self.EffetStigmaHomoncule()
        elif self.modele.stigma_monstre_negatif == "Patchwork":
            self.EffetStigmaPatchwork()
        elif self.modele.stigma_monstre_negatif == "Arlequin":
            self.EffetStigmaArlequin()
        if self.modele.stigma_monstre_bonus == "Mal Jaune":
            self.EffetStigmaMalJaune()
        if "Terreur" in self.modele.monstre_tags:
            self.EffetTagTerreur()

    def SetupTimeSands(self):
        self.modele.vie_du_monstre_pour_sables_du_temps_actuel = self.modele.monstre_points_de_vie
        self.modele.vie_du_monstre_pour_sables_du_temps_tour_avant = self.modele.monstre_points_de_vie
        self.modele.vie_du_monstre_pour_sables_du_temps_a_utiliser = self.modele.monstre_points_de_vie
