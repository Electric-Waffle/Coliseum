"""Chef d'orchestre d'un combat.

Le combat suit un MVC où le contrôleur porte toute la logique :
- `modele.Model` : l'état du combat (joueur, monstre, altérations, tables d'actions) ;
- `vue.Vue`      : tout ce qui s'affiche et tout ce qui se joue comme son ;
- `Control`      : les règles, réparties par thème dans les modules voisins.

FLUX d'un combat (`Control.Battle`) :
1. préparation : fiche du monstre (bestiaire), musique, effets de premier tour ;
2. à chaque tour : action du joueur, action du monstre, puis fin de tour
   (altérations d'état, stigmas, remise à zéro des compteurs) ;
3. après chaque action, `CheckHp` regarde si quelqu'un est tombé à zéro ;
4. sortie de boucle : game over éventuel, puis fuite ou récompenses.

PATTERN : classes mixin. `Control` hérite de dix petites classes qui ne
contiennent que des méthodes ; Python les assemble en une seule classe.
POURQUOI : l'ancien contrôleur faisait 11 000 lignes d'un bloc. Toutes ses
méthodes se partagent `self.modele` et `self.vue` et s'appellent entre elles :
les découper en objets indépendants aurait demandé de réécrire chaque appel.
Les mixins rangent le code par thème sans changer un seul appel. C'est une
étape, pas une destination : une mixin ne cache rien aux autres, toutes
voient tout `self`. Extraire de vrais objets (par exemple un gestionnaire
d'altérations qui ne connaît que le modèle) reste le pas suivant.

Où ajouter quoi :
- un monstre             -> combat/bestiaire/
- une attaque de monstre -> une méthode dans attaques_speciales.py + sa ligne
                            dans la table du même fichier
- un stigma, un talent   -> stigmas.py, talents.py
"""

from coliseum.combat import modele, vue
from coliseum.combat.actions_joueur import ActionsJoueurMixin
from coliseum.combat.actions_monstre import ActionsMonstreMixin
from coliseum.combat.alterations import AlterationsMixin
from coliseum.combat.attaques_speciales import AttaquesSpecialesMixin
from coliseum.combat.cuisine_infernale import CuisineInfernaleMixin
from coliseum.combat.effets import EffetsMixin
from coliseum.combat.fin_de_combat import FinDeCombatMixin
from coliseum.combat.preparation import PreparationMixin
from coliseum.combat.stigmas import StigmasMixin
from coliseum.combat.talents import TalentsMixin
from coliseum.console import ClearConsole
from coliseum.interface import recapitulatif


class Control(
    PreparationMixin,
    ActionsJoueurMixin,
    ActionsMonstreMixin,
    AttaquesSpecialesMixin,
    AlterationsMixin,
    StigmasMixin,
    TalentsMixin,
    EffetsMixin,
    CuisineInfernaleMixin,
    FinDeCombatMixin,
):

    def __init__(self, Player, Trader, Floormaker, Sove):
        """Crée la vue et le modèle du combat à partir de l'état actuel du joueur."""
        self.Player = Player
        self.Floormaker = Floormaker
        self.tirage = Trader
        self.Sove = Sove
        self.vue = vue.Vue(Player)
        self.modele = modele.Model(Player)
        self.sound_of_action = "ITEM"
        ClearConsole()

    def EquilibragePointsDeVieEtManaEtEndurance(self):
        if self.modele.points_de_vie > self.modele.points_de_vie_max:
            self.modele.points_de_vie = self.modele.points_de_vie_max
        if self.modele.points_de_mana > self.modele.points_de_mana_max:
            self.modele.points_de_mana = self.modele.points_de_mana_max
        elif self.modele.points_de_mana < 0:
            self.modele.points_de_mana = 0
        if self.modele.monstre_points_de_vie > self.modele.monstre_points_de_vie_max:
            self.modele.monstre_points_de_vie = self.modele.monstre_points_de_vie_max
        elif self.modele.monstre_points_de_mana > self.modele.monstre_points_de_mana_max:
            self.modele.monstre_points_de_mana = self.modele.monstre_points_de_mana_max
        if self.modele.points_de_endurance > self.modele.points_de_endurance_max:
            self.modele.points_de_endurance = self.modele.points_de_endurance_max
        if self.modele.points_de_endurance < 0 and not "Couronne Sacrée" in self.modele.liste_dartefacts_optionels:
            self.modele.points_de_endurance = 0

    def IsMultipleOf(self, nombre_a_checker, multiple_actuel):
        if nombre_a_checker!=0 and ((nombre_a_checker % multiple_actuel) == 0):
            return True
        return False

    def EquilibrageGold(self):
        if self.modele.nombre_de_gold < 0:
            self.modele.nombre_de_gold = 0

    def FinTour(self):
        # applique/affiche les alteration d'état et diminue leur
        # tours d'application de 1.
        self.AppliqueEtMetAJourAlterationEtat()
        # le mana revient un peu chaque tour
        self.RegenerationDeManaParTour()
        # applique les stigmas
        self.ApplicationStigmaPourFinDuTour()
        # remet a 0 les variable a_utilise_element_ce_tour
        self.ResetTypeElementUtiliseCeTour()
        self.RemiseAZeroMonsterTypeOfAction()
        # équilibre les pv et mana
        self.EquilibragePointsDeVieEtManaEtEndurance()
        self.EquilibragePointDeVieMonstrePerduParStigma()
        # clean les tags
        self.cleanTags()
        # augmente le nombre de tour
        self.modele.nombre_de_tours += 1

    def RegenerationDeManaParTour(self):
        """Rend 3 % du mana max (au moins 1) à la fin de chaque tour.

        POURQUOI : le mana ne revenait par aucun moyen automatique. Avec 10 à
        25 points au départ et des sorts à 5-40, on lançait 1 à 5 sorts par
        combat, et les objets de mana devenaient obligatoires.
        """
        if self.modele.points_de_mana_max > 0 and self.modele.points_de_vie > 0:
            self.RecouvrementDeMana(max(1, round(0.03 * self.modele.points_de_mana_max)))

    def cleanTags(self):
        for tag in [
            "Utilise Feu Basique",
            "Utilise Glace Basique",
            "Utilise Terre Basique",
            "Utilise Foudre Basique",
            "Utilise Sang Basique"
        ]:
            try:
                self.modele.player_tags.remove(tag)
            except ValueError:
                pass  # Le tag n'est pas dans la liste, on ignore

    def Battle(self):
        """Déroule un combat complet, de l'apparition du monstre aux récompenses."""
        # CONCEPT : `try / finally`. Que le combat se termine normalement ou
        # par une erreur, le récap du monstre est retiré de l'écran.
        try:
            self._preparer_le_combat()
            while self.modele.InCombat:
                # Les talents peuvent changer les caractéristiques des actions d'un
                # tour à l'autre : les tables d'actions sont recalculées à chaque tour.
                self.PatternDesignConstantUpdater()
                if not self.CheckHp():
                    break
                self._jouer_le_tour_du_joueur()
                if not self.CheckHp():
                    break
                type_de_laction_du_monstre = self._jouer_le_tour_du_monstre()
                if not self.CheckHp(type_de_laction_du_monstre):
                    break
                self.FinTour()
            self.CheckForGameOver()
        finally:
            # ATTENTION : à faire AVANT les récompenses. `MontreFuiteOuRecompense`
            # recopie le modèle dans le joueur puis ajoute les gains au joueur :
            # à partir de là, c'est le joueur que le récap doit relire.
            recapitulatif.oublier_le_combat()
        self.MontreFuiteOuRecompense()

    def _preparer_le_combat(self):
        # Demande au joueur si le mana le bénit ou le maudit (talents d'affinité).
        self.SetBenedictionDuMana()
        self.MonsterMaker()
        # Le monstre existe : son récap remplace la carte dans la fenêtre.
        recapitulatif.suivre_le_combat(self)
        self.SetupTimeSands()
        self.PatternDesignConstantUpdater()
        self.AfficheMonstreNiveauEtMusique()
        self.PremierTourJoueur()
        self.PremierTourMonstre()

    def _jouer_le_tour_du_joueur(self):
        if self.modele.passe_son_tour:
            self.RaisonDePasserSonTour()
            return
        numero_du_type_de_laction, numero_de_laction = self.GetUserChoice(
            self.modele.derniere_action_utilisee,
            self.modele.type_de_derniere_action_utilisee,
        )
        ClearConsole()
        type_de_laction, nom_de_laction = self.TranslateUserChoice(
            numero_du_type_de_laction, numero_de_laction
        )
        # PATTERN : table de dispatch. Le type d'action choisi dans le menu
        # désigne la méthode à appeler ; un type inconnu ne fait rien.
        actions_avec_cible = {
            "Sorts": self.UseMagic,
            "Techniques": self.UseAttack,
            "Items": self.UseItem,
        }
        actions_sans_cible = {
            "Fuir": self._tenter_de_fuir,
            "Passer son tour": self.PasserSonTour,
            "Se défendre": self.SeDefendre,
        }
        if type_de_laction in actions_avec_cible:
            actions_avec_cible[type_de_laction](nom_de_laction)
        elif type_de_laction in actions_sans_cible:
            actions_sans_cible[type_de_laction]()

    def _tenter_de_fuir(self):
        # FailFleeing retourne True quand la fuite échoue : le combat continue.
        self.modele.InCombat = self.FailFleeing()

    def _jouer_le_tour_du_monstre(self):
        """Fait agir le monstre et retourne le type de son action ("Sort", "Technique" ou "None")."""
        if self.modele.monstre_passe_son_tour:
            self.RaisonDePasserTourMonstre()
            return "None"
        nom_de_laction, type_de_laction = self.GetMonsterChoice()
        self.modele.type_daction_du_monstre = type_de_laction
        if type_de_laction == "Sort":
            self.UseMonsterMagic(nom_de_laction)
        elif type_de_laction == "Technique":
            self.UseMonsterAttack(nom_de_laction)
        return type_de_laction

    def SiZeroRameneAUn(self, nombre):
        if nombre <= 0:
            nombre = 1
        return nombre

    def EnleveVieAuJoueur(self, degat):
        if self.modele.se_defend:
            reduction_de_degat = 0.25
            if "Bocle de Philoctète" in self.modele.liste_dartefacts_optionels:
                reduction_de_degat = 0.4
            degat = round((1 - reduction_de_degat) * degat)
        degat = self.SiZeroRameneAUn(degat)
        if self.modele.metamorphose:
            self.vue.AfficheTalentMetamorphose()
        else:
            self.modele.points_de_vie -= degat
        return degat
    
    def RecupEndurance(self, endurance_recuperee):
        if not self.modele.est_maudit_par_endurance:
            bonus_charge = 0
            if "Element [Corps] Surchargé" in self.modele.liste_dartefacts_optionels:
                bonus_charge += 4
            gain_endurance = endurance_recuperee + self.modele.numero_de_letage + bonus_charge
            self.modele.points_de_endurance += gain_endurance
            if (self.modele.points_de_endurance > self.modele.points_de_endurance_max) :
                self.modele.points_de_endurance = self.modele.points_de_endurance_max

    def RecouvrementDeMana(self, points_de_mana_recouverts):
        self.modele.points_de_mana += points_de_mana_recouverts
        if self.modele.points_de_mana > self.modele.points_de_mana_max :
            self.modele.points_de_mana = self.modele.points_de_mana_max
        if "Collier de Nephilim" in self.modele.liste_dartefacts_optionels:
            self.modele.points_de_vie += round(points_de_mana_recouverts // 2)
            if self.modele.points_de_vie > self.modele.points_de_vie_max :
                self.modele.points_de_vie = self.modele.points_de_vie_max