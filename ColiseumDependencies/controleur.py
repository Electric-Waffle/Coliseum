import modele
import vue
import os
import random
import time
from collections import deque


def clear_console():
    # Vérifie le système d'exploitation pour déterminer la commande appropriée
    os.system("cls" if os.name == "nt" else "clear")


class Control:

    def __init__(self, Player, Trader, Floormaker, Sove):
        """Ne prend rien, ne retourne rien.

        Initialise la vue, et l'ensemble du modèle
         (sauf la variable benediction_du_mana)
        """
        self.Player = Player
        self.Floormaker = Floormaker
        self.tirage = Trader
        self.Sove = Sove
        self.vue = vue.Vue(Player)
        self.modele = modele.Model(Player)
        self.sound_of_action = "ITEM"
        clear_console()

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
                    clear_console()
                except ValueError:
                    clear_console()

    def CheckHp(self, type_de_laction="None"):
        """Peux prendre le type d'action du monstre, retourne True ou False si il reste de la vie ou pas

        Verifie si les points de vie du joueur puis du monstre sont superieurs a zéro, 
        applique les effets et introductions liés a une résurrection
        """
        if self.modele.points_de_vie < 1:
            if "Voile de Ino" in self.modele.liste_dartefacts_optionels:
                self.modele.liste_dartefacts_optionels.remove("Voile de Ino")
                vie_recupere = round(0.66 * self.modele.points_de_vie_max)
                self.modele.points_de_vie = vie_recupere
                self.modele.beni_par_feu_sacre = True
                self.modele.beni_par_feu_sacre_nombre_tour += 3
                commentaire = (
                    "Alors que vous alliez mourir, le voile d'Ino que vous portiez se plaque alors contre votre peau avant de disparaitre."
                    f"\nVous vous mettez alors a briller et regagnez {vie_recupere} points de vie !"
                    "\nDe plus, vous vous sentez béni par la déesse elle-même !\nVos deux prochaines attaques seront des coups critiques !"
                )
                if "Oeuil de Phénix" in self.modele.liste_dartefacts_optionels:
                    commentaire += "\nDe plus, votre Oeuil de Phénix s'accroche a votre poitrine et vous injecte une grosse dose de mana !"
                    self.modele.points_de_mana = self.modele.points_de_mana_max
                self.vue.AfficheResurrection(commentaire)
                return True
            if self.modele.possede_une_fee:
                if (self.modele.stigma_joueur_negatif == "Maudit"):
                    commentaire = (
                        "Alors que vous alliez mourir, votre fée sort de son flacon. "
                        "\nCepandant, au lieu de vous aider, elle est repoussée par "
                        "votre aura démoniaque maudite, et s'enfuie."
                    )
                    self.vue.AfficheResurrection(commentaire)
                    return False
                else:
                    self.modele.possede_une_fee = False
                    vie_recupere = round(0.66 * self.modele.points_de_vie_max)
                    self.modele.points_de_vie = vie_recupere
                    commentaire = (
                        "Alors que vous alliez mourir, votre fée sort de son flacon "
                        "et tourne rapidement autour de vous avant de disparaitre."
                        "\nLa poussiere laissée derriere par ses mouvements"
                        f" s'infiltre dans vos plaies, et vous regagnez {vie_recupere} points de vie !"
                    )
                    if "Oeuil de Phénix" in self.modele.liste_dartefacts_optionels:
                        commentaire += "\nDe plus, votre Oeuil de Phénix s'accroche a votre poitrine et vous injecte une grosse dose de mana !"
                        self.modele.points_de_mana = self.modele.points_de_mana_max
                    self.vue.AfficheResurrection(commentaire)
                    return True
            else:
                nombre_aleatoire = random.randint(0, 100)
                if (self.modele.stigma_joueur_bonus == "Logique au dessus des Cieux") and (type_de_laction == "Sort"):
                    if nombre_aleatoire <= 10:
                        commentaire = "Vous sentez la vie vous quitter.\nMais vous refusez de mourir a cause d'un sort.\n \n \nAlors,\nvous ne mourrez pas."
                        self.modele.points_de_vie = round(self.modele.points_de_vie_max * 0.1)
                        self.vue.AfficheResurrection(commentaire)
                        return True
                elif (self.modele.stigma_joueur_bonus == "Emotion au dessus des Cieux") and (type_de_laction == "Technique"):
                    if nombre_aleatoire <= 10:
                        commentaire = "Vous sentez la vie vous quitter.\nMais vous refusez de mourir a cause d'une technique.\n \n \nAlors,\nvous ne mourrez pas."
                        self.modele.points_de_vie = round(self.modele.points_de_vie_max * 0.1)
                        self.vue.AfficheResurrection(commentaire)
                        return True
                if "Echarde de Pinocchio" in self.modele.liste_dartefacts_optionels:
                    if nombre_aleatoire in [1, 2, 3, 4, 5]:
                        commentaire = "Vous sentez la vie vous quitter.\nOu pas.\n \nVotre mort durant ce combat n'etait qu'un simple mensonge. \nEn fait, vous n'avez même jamais perdu de vie !"
                        self.modele.points_de_vie = self.modele.points_de_vie_max
                        self.vue.AfficheResurrection(commentaire)
                        return True
                return False
        elif self.modele.monstre_points_de_vie < 1:
            if self.Player.malediction == "Impotent" and self.modele.nombre_de_tours <= 5:
                self.EffetImpotent()
            else:
                if self.modele.monstre_nombre_de_vies_supplementaire > 0:
                    self.EnleveAlterationEtat()
                    self.modele.monstre_passe_son_tour = True
                    self.modele.commentaire_de_resurection_de_monstre = "...fatigué par sa resurection."
                    self.modele.monstre_nombre_de_vies_supplementaire -= 1
                    vie_recupere = round(0.5 * self.modele.monstre_points_de_vie_max)
                    commentaire = (
                        "Alors que l'ennemi allait mourir, il "
                        "prend une pose particuliere et hurle."
                        "\nDe par sa détermination, il reprend"
                        f" {vie_recupere} points de vie, mais son"
                        " teint perd en couleur et vivacité.\nD'après"
                        " son état, il devrait etre capable de refaire"
                        f" ceci {self.modele.monstre_nombre_de_vies_supplementaire} fois."
                    )
                    if self.modele.stigma_monstre_positif == "Cendres du Renouveau":
                        vie_recupere = self.modele.monstre_points_de_vie_max
                        self.modele.monstre_passe_son_tour = False
                        self.modele.commentaire_de_resurection_de_monstre = "Aucun"
                        commentaire = (
                            "Soudainement, L'ennemi s'embrase et disparait dans un nuage de cendre. "
                            "\nLe nuage se met alors a tourner, tourner, tourner, puis se regroupe en une "
                            "forme particulière, comme une statue noire de jais."
                            f"\nLa statue se met alors a prendre des couleurs, et bientot vous"
                            " retrouvez votre ennemi en pleine forme, avec tout ses points de vie.\nD'après"
                            " son état, il devrait etre capable de refaire"
                            f" ceci {self.modele.monstre_nombre_de_vies_supplementaire} fois."
                        )
                    elif self.modele.monstre_nom == "Ah Kin" and self.modele.monstre_nombre_de_vies_supplementaire in [9, 6, 3]:
                        self.modele.monstre_tags.append("En Fuite")
                    elif self.modele.monstre_nom == "Armée des Anges":
                        musique = self.modele.CHEMINABSOLUMUSIQUE 
                        self.modele.monstre_passe_son_tour = False
                        if self.modele.monstre_nombre_de_vies_supplementaire == 0 :
                            self.vue.AfficheResurrectionArmeeAnge(musique)
                            self.modele.monstre_nom = "Armée de la Fin"
                            self.SetAttributesFromName()
                        else:
                            vie_recupere = self.modele.monstre_points_de_vie_max
                            self.modele.commentaire_de_resurection_de_monstre = "Aucun"
                            commentaire = (
                                "Le son d'un cor retenti. Les renforts de l'armée s'approchent."
                                "\nD'après votre instinct, il ne devrait y avoir plus que"
                                f" {self.modele.monstre_nombre_de_vies_supplementaire} autres vagues."
                            )
                    elif self.modele.monstre_nom == "Armée de la Fin":
                        musique = self.modele.CHEMINABSOLUMUSIQUE 
                        self.modele.monstre_passe_son_tour = False
                        if self.modele.monstre_nombre_de_vies_supplementaire == 0 :
                            self.vue.AfficheResurrectionArchange(musique)
                            self.modele.monstre_nom = "Archange Michael"
                            self.SetAttributesFromName()
                        else:
                            vie_recupere = self.modele.monstre_points_de_vie_max
                            self.modele.commentaire_de_resurection_de_monstre = "Aucun"
                            commentaire = (
                                "Le son d'un cor retenti. Les renforts de l'armée s'approchent."
                                "\nD'après votre instinct, il ne devrait y avoir plus que"
                                f" {self.modele.monstre_nombre_de_vies_supplementaire} autres vagues."
                            )
                    if self.modele.monstre_nom in ["Maitre Mage", "Apprentie", "Coliseum", "Cauchemard",
                                                "Ahmed (Entrée)", "Ahmed (Plat de résistance)", "Roi Gluant",
                                                "Volontée Immortelle", "Volontée Persistante", "Volontée Instable",
                                                "Spectre", "Aurore"] and self.modele.monstre_nombre_de_vies_supplementaire == 0:
                        chemin_musique = self.modele.CHEMINABSOLUMUSIQUE 
                        if self.modele.monstre_nom == "Maitre Mage":
                            self.modele.commentaire_de_resurection_de_monstre = "...un peu sonné par sa transformation."
                            self.vue.AfficheResurrectionMaitreMage(chemin_musique)
                            self.modele.monstre_nom = "Ministre du Mana"
                        elif self.modele.monstre_nom == "Apprentie":
                            self.modele.commentaire_de_resurection_de_monstre = "...pour s'adapter à son nouvel hôte."
                            self.vue.AfficheResurrectionApprenti(chemin_musique)
                            self.modele.monstre_nom = "Minaraï"
                        elif self.modele.monstre_nom == "Le Pianiste":
                            self.modele.commentaire_de_resurection_de_monstre = "...et tombe, inerte, à terre."
                            self.vue.AfficheResurrectionPianiste(chemin_musique)
                            self.modele.monstre_nom = "Noa"
                            notes_restante, reussite = self.DoPianisteDerniereAttaque()
                            return self.DoPianisteResultatDerniereAttaque(notes_restante, reussite)
                        elif self.modele.monstre_nom == "Coliseum":
                            self.modele.commentaire_de_resurection_de_monstre = "...afin de se libérer de son ancienne forme."
                            self.vue.AfficheResurrectionColiseum(chemin_musique)
                            self.modele.monstre_nom = "Pierre de Désir"
                        elif self.modele.monstre_nom == "Cauchemard" :
                            self.modele.monstre_tags.remove("Super Etoile")
                            self.modele.monstre_tags.remove("Terreur")
                            self.modele.monstre_tags.append("Fausse Terreur")
                            self.modele.commentaire_de_resurection_de_monstre = "...affaibli par le chant positif."
                            self.vue.AfficheResurrectionCauchemard(chemin_musique)
                            self.modele.monstre_nom = "Cauchemard (Affaibli)" #zzzzzz
                        elif self.modele.monstre_nom == "Ahmed (Entrée)" :
                            self.modele.commentaire_de_resurection_de_monstre = "...pour reprendre ses esprits après le rush."
                            self.vue.AfficheResurrectionAhmedEntree(chemin_musique)
                            self.modele.monstre_nom = "Ahmed (Plat de résistance)" #zzzzzz
                        elif self.modele.monstre_nom == "Ahmed (Plat de résistance)" :
                            self.modele.commentaire_de_resurection_de_monstre = "...pour reprendre ses esprits après le rush."
                            self.vue.AfficheResurrectionAhmedPlat(chemin_musique)
                            self.modele.monstre_nom = "Ahmed (Dessert)" #zzzzzz
                        elif self.modele.monstre_nom == "Roi Gluant" :
                            self.modele.commentaire_de_resurection_de_monstre = "...pour fermer les yeux de son défunt souverain."
                            self.vue.AfficheResurrectionGluancelot(chemin_musique)
                            self.modele.monstre_nom = "Gluantcelot" #zzzzzz
                        elif self.modele.monstre_nom == "Volontée Immortelle" :
                            self.modele.commentaire_de_resurection_de_monstre = "...pour souffler un coup."
                            self.vue.AfficheResurrectionVolonteeImmortelle(chemin_musique)
                            self.modele.monstre_nom = "Volontée Persistante" #zzzzzz
                        elif self.modele.monstre_nom == "Volontée Persistante" :
                            self.modele.commentaire_de_resurection_de_monstre = "...pour reprendre ses esprits."
                            self.vue.AfficheResurrectionVolonteePersistante(chemin_musique)
                            self.modele.monstre_nom = "Volontée Instable" #zzzzzz
                        elif self.modele.monstre_nom == "Volontée Instable" :
                            self.modele.commentaire_de_resurection_de_monstre = "...pour se reconcentrer sur son adversaire."
                            self.vue.AfficheResurrectionVolonteeInstable(chemin_musique)
                            self.modele.monstre_nom = "Volontée Indomptable" #zzzzzz
                        elif self.modele.monstre_nom == "Spectre" :
                            self.modele.commentaire_de_resurection_de_monstre = "...pour se disputer avec les autres âmes en peine."
                            self.vue.AfficheResurrectionSpectre(chemin_musique)
                            self.modele.monstre_nom = "Spectre (Agonie)" #zzzzzz
                        elif self.modele.monstre_nom == "Aurore" :
                            self.modele.commentaire_de_resurection_de_monstre = "...pour se masser l'endroit ou se situe sa marque du sacrifice."
                            self.vue.AfficheResurrectionAurore(chemin_musique)
                            self.modele.monstre_nom = "Divine Faucheuse" #zzzzzz
                        self.SetAttributesFromName()
                    else:
                        if self.modele.monstre_nom in ["Volontée Immortelle", "Volontée Persistante", "Volontée Instable"]:
                            vie_recupere = self.modele.monstre_points_de_vie_max
                        self.modele.monstre_points_de_vie = vie_recupere
                        self.vue.AfficheResurrection(commentaire)
                else:
                    return False
        return True
    
    def EnleveAlterationEtat(self):
        self.modele.monstre_en_etat_de_choc = False
        self.modele.monstre_en_etat_de_choc_nombre_tour = 0
        self.modele.monstre_est_envol = False  # Envol, -30% chance de toucher
        self.modele.monstre_est_envol_nombre_tour = 0
        self.modele.monstre_est_maudit = False  # Maudit, -2 pm par tours.
        self.modele.monstre_est_maudit_nombre_tour = 0
        self.modele.monstre_est_gele = False  # Gele, prend 2x + de degats
        self.modele.monstre_est_gele_nombre_tour = 0
        self.modele.monstre_est_en_feu = False  # en feu, perd des pv par tour
        self.modele.monstre_est_en_feu_nombre_tour = 0
        self.modele.monstre_est_en_feu_degat = 0
        self.modele.monstre_est_paralyse = False  # paralysie, passe son tour
        self.modele.monstre_est_paralyse_nombre_tour = 0
        self.modele.monstre_est_vulnerable = False  # vulnerable, suceptible elements
        self.modele.monstre_est_vulnerable_nombre_tour = 0
        self.modele.monstre_niveau_de_vulnerabilite = 0
        self.modele.monstre_est_empoisonne = False  # poison, gros degat peu de tours
        self.modele.monstre_est_empoisonne_nombre_tour = 0
        self.modele.monstre_est_empoisonne_degat = 0
        self.modele.monstre_est_regeneration = False  # regen, reprend vie par tour
        self.modele.monstre_est_regeneration_nombre_tour = 0
        self.modele.monstre_est_regeneration_soin = 0

    def FailFleeing(self):
        """Ne prend rien, retourne True ou False si l'échec de fuite est vrai ou pas

        calcule la réussite ou non de l'échec de la fuite
        """
        if (
                self.modele.stigma_joueur_negatif == "Pas d'Echappatoire" or 
                self.modele.monstre_EstUnBoss or
                self.modele.monstre_de_lobelisque or
                self.modele.boss_histoire
            ):
            commentaire = "...et vous vous ravisez.\nPas d'échappatoire.\n \nC'est tout ou rien."
            self.vue.AfficheResultatFuite(commentaire)
            return True
        else:
            taux_de_reussite_de_la_fuite = self.modele.taux_de_esquive + 40
            nombre_aleatoire = random.randint(0, 100)
            if "Masque d'Oblivion" in self.modele.liste_dartefacts_optionels:
                # fuite garantie
                nombre_aleatoire = 0
            if nombre_aleatoire > taux_de_reussite_de_la_fuite:  # fuite echec
                commentaire = "...mais échouez."
                self.vue.AfficheResultatFuite(commentaire)
                return True
            commentaire = "...et réussissez ! Mais pas avant que L'ennemi ne fasse une dernière action."
            self.vue.AfficheResultatFuite(commentaire)
            return False

    def GetListOfActionPossible(self, nombre):
        """Prend une liste d'action (sort ou technique),
        retourne une liste de nombre allant de 1 au nombre d'actions dans la liste.

        Ajoute la position de l'action de la liste d'action dans une liste.
        """
        listes = []
        numero_de_laction = 1
        while (nombre - 1) != (numero_de_laction):
            listes.append(numero_de_laction)
            numero_de_laction += 1
        listes.append(numero_de_laction)
        return listes

    def GetItemList(self):
        """Ne prend rien, retourne une liste des items utilisables selon le tour et leur nombre."""
        list_of_items = []
        for nom_item in self.modele.items:
            if self.modele.items[nom_item] == 0:  # passe si on a pas un objet
                continue
            if (
                nom_item in self.modele.items_autorises_que_au_premier_tour
                and self.modele.nombre_de_tours != 1
            ):  # passe si on est pas au tour 1
                continue
            list_of_items.append(nom_item)
        return list_of_items

    def GetUserChoice(self, derniere_action_utilise, type_de_derniere_action_utilise):
        choix_de_utilisateur_fait = False
        valeur_menu = None
        valeur_action = None
        self.modele.liste_des_items = self.GetItemList()
        if derniere_action_utilise is None:
            derniere_action_utilise = "[Aucune]"
        if derniere_action_utilise in self.modele.items_autorises_que_au_premier_tour:
            derniere_action_utilise += " [Impossible]"
        elif derniere_action_utilise in self.modele.items:
            derniere_action_utilise += f" [{self.modele.items[derniere_action_utilise]} dans la sacoche]"
        (alteration_technique, alteration_sort, alteration_item, alteration_fuite) = (
            self.DefinitionAlterationDesActionsPourAffichage()
        )
        alteration_etat_monstre, alteration_etat_joueur = (
            self.ConstruirePhraseAlterationEtatPourVue()
        )
        affiche_gold = ""
        if self.modele.est_maudit_par_le_gold:
            affiche_gold = f"\n     {self.modele.nombre_de_gold} golds"
        if self.modele.monstre_en_etat_de_choc:
            monstre_points_de_mana_a_afficher = "ERROR"
        else:
            monstre_points_de_mana_a_afficher = self.modele.monstre_points_de_mana
        while not choix_de_utilisateur_fait:
            while valeur_menu is None:  # valeur du menu (technique sort item)
                try:
                    valeur_menu = self.vue.GetMenuChoice(
                        self.modele.nombre_de_tours,
                        alteration_technique,
                        alteration_sort,
                        alteration_item,
                        alteration_fuite,
                        derniere_action_utilise,
                        self.modele.monstre_points_de_vie,
                        monstre_points_de_mana_a_afficher,
                        self.modele.points_de_vie,
                        self.modele.points_de_vie_max,
                        self.modele.points_de_mana,
                        self.modele.points_de_mana_max,
                        self.modele.points_de_endurance,
                        self.modele.points_de_endurance_max,
                        self.modele.monstre_nom,
                        alteration_etat_monstre,
                        alteration_etat_joueur,
                        affiche_gold,
                    )
                    clear_console()
                    if valeur_menu == 1:
                        liste_daction_a_passer_a_vue = self.modele.techniques
                        titre_du_menu = "Techniques"
                    elif valeur_menu == 2:
                        liste_daction_a_passer_a_vue = self.modele.sorts
                        titre_du_menu = "Sorts"
                    elif valeur_menu == 3:
                        liste_daction_a_passer_a_vue = self.modele.items
                        titre_du_menu = "Items"
                    elif valeur_menu == 4:
                        valeur_action = "Fuir"
                    elif valeur_menu == 5:
                        valeur_action = "Se défendre"
                    elif valeur_menu == 6:
                        valeur_action = "Passer son tour"
                    elif valeur_menu == 7:
                        if (
                            derniere_action_utilise == "[Aucune]"
                            or type_de_derniere_action_utilise == "Pas possible"
                        ):  # si pas de derniere action
                            valeur_menu = 6
                            valeur_action = "Passer son tour"
                        else:
                            valeur_menu = type_de_derniere_action_utilise
                            valeur_action = self.modele.derniere_action_utilisee

                    else:
                        valeur_menu = None  # valeur invalide
                except ValueError:
                    clear_console()
            while valeur_action is None:  # valeur de laction
                try:
                    self.vue.ShowDebutMenuAction(
                        self.modele.nombre_de_tours, titre_du_menu
                    )  # affiche le debut du menu (titre)
                    nombre_associe_a_laction_pour_lutilisateur = 2
                    if valeur_menu != 3:
                        for action in liste_daction_a_passer_a_vue:
                            affichage_cout = ""
                            if titre_du_menu == "Sorts":
                                action_sans_affix = self.EnleveurAffix(action)
                                affichage_cout = self.ConstructionAffichageCoutSort(
                                    action_sans_affix
                                )
                            elif titre_du_menu == "Techniques":
                                action_sans_affix = self.EnleveurAffix(action)
                                affichage_cout = (
                                    self.ConstructionAffichageCoutTechnique(action_sans_affix)
                                )
                            elif titre_du_menu == "Items":
                                affichage_cout = self.ConstructionAffichageCoutItems(
                                    action
                                )
                            self.vue.ShowMenuAction(
                                nombre_associe_a_laction_pour_lutilisateur,
                                action,
                                affichage_cout,
                            )  # affiche les actions du menu, sauf item
                            nombre_associe_a_laction_pour_lutilisateur += 1
                    else:
                        for nom_item in self.modele.items:
                            if (
                                self.modele.items[nom_item] == 0
                            ):  # passe laffichage si on a pas un objet
                                continue
                            if (
                                nom_item
                                in self.modele.items_autorises_que_au_premier_tour
                                and self.modele.nombre_de_tours != 1
                            ):
                                continue
                            self.vue.ShowMenuActionItem(
                                nombre_associe_a_laction_pour_lutilisateur,
                                nom_item,
                                self.modele.items[nom_item],
                            )  # Un affichage seulement pour les items
                            nombre_associe_a_laction_pour_lutilisateur += 1
                    valeur_action = (
                        self.vue.GetMenuActionChoice()
                    )  
                    clear_console()
                    # affiche la fin du menu (l'input)
                    liste_de_numero_daction_possible = self.GetListOfActionPossible(
                        nombre_associe_a_laction_pour_lutilisateur
                    )
                    if valeur_action not in liste_de_numero_daction_possible:
                        valeur_action = None  # valeur invalide
                except ValueError:
                    clear_console()
            if (
                valeur_action == 1
            ):  # si le user a fait retour, retour au menu precedent on recommence tout
                valeur_action = None
                valeur_menu = None
            else:
                choix_de_utilisateur_fait = True  # choix a ete fait
        return valeur_menu, valeur_action

    def TranslateUserChoice(self, numero_du_type_de_laction, numero_de_laction):
        # type de l'action, sauf pour la derniere action faite
        if numero_du_type_de_laction == 1:
            type_de_laction = "Techniques"
        elif numero_du_type_de_laction == 2:
            type_de_laction = "Sorts"
        elif numero_du_type_de_laction == 3:
            type_de_laction = "Items"
        elif numero_du_type_de_laction == 4:
            type_de_laction = "Fuir"
            nom_de_laction = "Fuir"
        elif numero_du_type_de_laction == 5:
            type_de_laction = "Se défendre"
            nom_de_laction = "Se défendre"
        elif numero_du_type_de_laction == 6:
            type_de_laction = "Passer son tour"
            nom_de_laction = "Passer son tour"
        else:  # Si cest la derniere attaque faite, il ny a pas de numero, mais deja les noms en caracteres
            return numero_du_type_de_laction, numero_de_laction

        # nom de laction
        if type_de_laction == "Techniques":
            nom_de_laction = self.modele.techniques[(numero_de_laction - 2)]
        elif type_de_laction == "Sorts":
            nom_de_laction = self.modele.sorts[(numero_de_laction - 2)]
        elif type_de_laction == "Items":
            liste_of_items = self.GetItemList()
            nom_de_laction = liste_of_items[(numero_de_laction - 2)]
        self.modele.type_de_derniere_action_utilisee = type_de_laction
        self.modele.derniere_action_utilisee = nom_de_laction
        return type_de_laction, nom_de_laction

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
        if self.modele.stigma_monstre_negatif == "Lignée Royale":
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
        self.modele.DEGATBONUSSORTS -= (
            self.modele.monstre_points_de_resistance * 3
        ) + malus_stigma
        if self.modele.stigma_monstre_positif == "Esotericisme":
            self.modele.DEGATBONUSSORTS = -100

        amelioration_degats_totaux = 0
        if ["Cape Victorieuse"] in self.modele.liste_dartefacts_optionels:
            amelioration_degats_totaux += (self.modele.nombre_de_monstres_tues * 0.5)
        if ["Contrat de Travail"] in self.modele.liste_dartefacts_optionels:
            amelioration_degats_totaux += round(self.modele.nombre_de_gold // 50)
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
        if ["Cape Victorieuse"] in self.modele.liste_dartefacts_optionels:
            amelioration_degats_totaux += (self.modele.nombre_de_monstres_tues * 0.5)
        if ["Contrat de Travail"] in self.modele.liste_dartefacts_optionels:
            amelioration_degats_totaux += round(self.modele.nombre_de_gold // 50)
        self.modele.DEGATBONUSATTAQUE += ((amelioration_degats_totaux / 100)* self.modele.DEGATBONUSATTAQUE)

        # degat des sorts crit
        bonus_stigma = 0
        if self.modele.stigma_monstre_positif == "Flocon de Neige":
            bonus_stigma = 50
        malus_stigma = 0
        if self.modele.stigma_joueur_negatif == "Famine":
            malus_stigma = 50
        self.modele.DEGATBONUSSORTCRITIQUE = (
            self.modele.degat_de_sort_critique + bonus_stigma + bonus_equilibrage_sort_critique
        )
        self.modele.DEGATBONUSSORTCRITIQUE -= malus_stigma
        if "Chaine de Main" in self.modele.liste_dartefacts_optionels:
            self.modele.DEGATBONUSSORTCRITIQUE += self.modele.DEGATBONUSSORTCRITIQUE
            

        # degat des attaques crit
        bonus_stigma = 0
        if self.modele.stigma_joueur_positif == "Flocon de Neige":
            bonus_stigma = 50
        malus_stigma = 0
        if self.modele.stigma_joueur_negatif == "Famine":
            malus_stigma = 50
        self.modele.DEGATBONUSATTAQUECRITIQUE = (
            self.modele.degat_de_coup_critique + bonus_stigma + bonus_equilibrage_technique_critique
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
        self.modele.CHANCEBONUSESQUIVE = bonus_caracteristique + bonus_artefact

        # pourcentage d'enflammer
        bonus_vulnerable = 0
        bonus_vulnerable = self.modele.monstre_niveau_de_vulnerabilite * 5
        bonus_charge = 0
        if "Element [Feu] Surchargé" in self.modele.liste_dartefacts_optionels:
            bonus_charge += 10
        malus_stigma = 0
        if self.modele.stigma_monstre_positif == "Roche Ténébreuse":
            malus_stigma = 100
        self.modele.CHANCEBONUSDEFAIREBRULER += bonus_vulnerable + bonus_charge + round(self.modele.accumulation_chance_brulure)
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
        self.modele.CHANCEBONUSDEFAIREGELER = 0 + bonus_vulnerable + bonus_charge + round(self.modele.accumulation_chance_gelure)
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
        if self.modele.stigma_joueur_positif == ["Endurci"]:
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
        if self.modele.stigma_joueur_negatif == ["Attache Physique"]:
            bonus_stigma = 25
        bonus_force = self.modele.monstre_points_de_force * 10
        self.modele.DEGATTECHNIQUEBONUSDUMONSTRE = bonus_gel + bonus_stigma + bonus_force + bonus_artefact + bonus_hyde
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
        if self.modele.stigma_joueur_negatif == ["Attache Physique"]:
            bonus_stigma = 25
        bonus_force = self.modele.monstre_points_de_intelligence * 10
        self.modele.DEGATSORTBONUSDUMONSTRE = bonus_gel + bonus_stigma + bonus_force + bonus_artefact + bonus_hyde
        # pourcentage de se faire enflammer (pas de modificateurs pour l'instant)
        self.modele.CHANCEBONUSJOUEURENFEU = 0
        # pourcentage de se faire geler (pas de modificateurs pour l'instant)
        self.modele.CHANCEBONUSJOUEURENGLACE = 0
        # pourcentage de se faire saigner (pas de modificateurs pour l'instant)
        self.modele.CHANCEBONUSJOUEURENSANG = 0
        # pourcentage de se faire lapider (pas de modificateurs pour l'instant)
        self.modele.CHANCEBONUSJOUEURLAPIDE = 0
        # reduction des degats de base contre les monstres
        bonus_defence = 0
        bonus_defence = (
            self.modele.monstre_points_de_resistance + self.modele.monstre_gain_de_defence_nombre
        ) * 3
        self.modele.BONUSREDUCTIONDEGAT = bonus_defence

        # reduction des degats de base contre les joueurs
        bonus_defence = 0
        bonus_defence = (
            self.modele.points_de_defence + self.modele.gain_de_defence
        ) * 3
        malus_hyde = 0
        if self.modele.miss_hyde_transformation :
            malus_hyde = 50
        self.modele.BONUSREDUCTIONDEGATSURJOUEUR = bonus_defence - malus_hyde

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
        if self.modele.monstre_EstUnBoss:
            if self.modele.etage_alternatif:
                self.modele.monstre_nom = self.modele.liste_de_boss_alternatif[
                    (self.modele.numero_de_letage - 1)
                ]
            elif self.Player.nom_de_letage == "Limbes Flétrissants":
                self.modele.monstre_nom = self.modele.liste_de_boss_rush[
                    (self.Player.numero_boss_alt - 1)
                ]
            else:
                self.modele.monstre_nom = self.modele.liste_de_boss[
                    (self.modele.numero_de_letage)
                ]
        elif self.modele.boss_histoire:
            if self.modele.nom_du_personnage == "Elma":
                self.modele.monstre_nom = "Yvan"
            elif self.modele.nom_du_personnage == "Saumel":
                self.modele.monstre_nom = "El Baron"
            elif self.modele.nom_du_personnage == "Vesperum":
                self.modele.monstre_nom = "Armée des Anges"
            elif self.modele.nom_du_personnage == "Peralta":
                self.modele.monstre_nom = "Doug Trudy"
            elif self.modele.nom_du_personnage == "Voyageur":
                self.modele.monstre_nom = "Thémis"
        else:
            if self.modele.numero_de_letage == 0:
                self.modele.monstre_nom = "Drone de Sécurité YucaTech Inc."
            elif self.modele.numero_de_letage in [1, 2]:
                self.modele.monstre_nom = self.modele.liste_de_monstres_etage_1_2[
                    (random.randint(0, 4))
                ]
            elif self.modele.numero_de_letage in [3, 4]:
                self.modele.monstre_nom = self.modele.liste_de_monstres_etage_3_4[
                    (random.randint(0, 4))
                ]
            elif self.modele.numero_de_letage in [5, 6]:
                self.modele.monstre_nom = self.modele.liste_de_monstres_etage_5_6[
                    (random.randint(0, 4))
                ]
            elif self.modele.numero_de_letage in [7, 8]:
                self.modele.monstre_nom = self.modele.liste_de_monstres_etage_7_8[
                    (random.randint(0, 4))
                ]
            elif self.modele.numero_de_letage in [9, 10, 11]:
                self.modele.monstre_nom = self.modele.liste_de_monstres_etage_9_10_11[
                    (random.randint(0, 19))
                ]
            # elif self.modele.numero_de_letage == 0:
                # self.modele.monstre_nom = "Gluant"
        if self.modele.est_une_mimique:
            self.modele.monstre_nom = "Mimique"

    def MonsterMaker(self):
        self.SetNameFromLevelAndBoss()
        self.SetAttributesFromName()

    def SetAttributesFromName(self):
        # viemax vie resistance force intelligence viesbonus stigma +/-/*

        # Monstres
        gold_bonus_par_etage = round(125 * (self.modele.numero_de_letage / 10))
        vie_bonus_par_etage = round(500 * (self.modele.numero_de_letage / 10))
        if self.modele.monstre_nom == "Pierre":
            self.modele.stigma_monstre_positif = "Plus d'un Tour"
            self.modele.stigma_monstre_negatif = "Gluantin"
            self.modele.monstre_points_de_force = 2
            self.modele.monstre_points_de_intelligence = 10
            self.modele.monstre_points_de_resistance = 3
            self.modele.monstre_nombre_de_vies_supplementaire = 99
            self.modele.monstre_points_de_vie_max = 100
            self.modele.monstre_points_de_mana_max = 50
            self.modele.monstre_liste_actions = {
                "Sables du Temps": "Technique",
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2}
        elif self.modele.monstre_nom == "???":  # récompense de Alfred
            self.modele.monstre_recompense = {"Taux esquive": 2, "Attaque": 1, "Defence": 1, "Intelligence": 1, "Gold": 100 + gold_bonus_par_etage}
        elif self.modele.monstre_nom == "Gluant":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = "Gluantin"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage, "Materiau": "Coeur Gravitaire"}

###################################################################################################################################
        elif self.modele.monstre_nom == "AstonRe":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = "Gluantin"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}
            self.modele.monstre_tags = ["Kikimora", "Domovoï"]
            self.modele.sorts.append("Faire fuir le Domovoï")
            self.modele.sorts.append("Faire fuir la Kikimora")
        elif self.modele.monstre_nom == "Cauchemard":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = "Gluantin"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 1
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_tags = ["Terreur", "Super Etoile"]
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}
        elif self.modele.monstre_nom == "Cauchemard (Affaibli)":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = "Gluantin"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}
        elif self.modele.monstre_nom == "Ahmed (Plat de résistance)":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = ""
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 1
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}
            self.modele.monstre_tags = ("Cuisine Infernale", "Plat")
            self.modele.liste_cuisson = {}
            self.modele.monstre_commande = {}
        elif self.modele.monstre_nom == "Ahmed (Dessert)":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = ""
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}
            self.modele.monstre_tags = ("Cuisine Infernale", "Dessert")
            self.modele.liste_cuisson = {}
            self.modele.monstre_commande = {}
        elif self.modele.monstre_nom == "Gluantcelot":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = "Gluantin"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 1
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}
        elif self.modele.monstre_nom == "Volontée Persistante":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = "Gluantin"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 4
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}
        elif self.modele.monstre_nom == "Volontée Instable":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = "Gluantin"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 4
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}
        elif self.modele.monstre_nom == "Volontée Indomptable":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = "Gluantin"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 1
            self.modele.monstre_points_de_vie_max = 3000
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}
        elif self.modele.monstre_nom == "Spectre (Agonie)":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = "Gluantin"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}
        elif self.modele.monstre_nom == "Divine Faucheuse":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = "Gluantin"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 4
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}        
        elif self.modele.monstre_nom == "Ahmed (Entrée)":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = ""
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 1
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}
            self.modele.monstre_tags = ("Cuisine Infernale", "Entrée")
            self.modele.techniques.append("Cuisiner")
        elif self.modele.monstre_nom == "Roi Gluant":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = "Gluantin"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 1
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}
        elif self.modele.monstre_nom == "Obo la Cryobarbare":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = "Gluantin"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 2
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}
        elif self.modele.monstre_nom == "Mercenaire":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = "Gluantin"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}
        elif self.modele.monstre_nom == "Volontée Immortelle":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = "Gluantin"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 4
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}
        elif self.modele.monstre_nom == "Eris (?)":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = "Gluantin"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 2
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}
        elif self.modele.monstre_nom == "Spectre":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = "Gluantin"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 1
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}
        elif self.modele.monstre_nom == "Aurore":
            self.modele.stigma_monstre_positif = "Gluantesque"
            self.modele.stigma_monstre_negatif = "Gluantin"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 1
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Coup de Boule": "Technique",
                "Etranglement": "Technique", # rend muet
                "Soin": "Sort",
                "Flamme": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 2, "Gold": 15 + gold_bonus_par_etage}
###################################################################################################################################

        elif self.modele.monstre_nom == "Feu Follet":
            self.modele.stigma_monstre_positif = "Siphon de Mana"
            self.modele.stigma_monstre_negatif = "Pyrolien"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 2
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Tout Feu Tout Flamme": "Sort", # combo electrique, pour le feu [x]
                "Feu Regénérateur": "Sort", # soin
                "Poing de Feu": "Technique", # brule
                "Brulevent": "Technique" # rend muet
            }
            self.modele.monstre_recompense = {"Mana max": 2, "Gold": 10 + gold_bonus_par_etage, "Materiau": "Ectoplasme Chaud"}
        elif self.modele.monstre_nom == "Golem de Terre":
            self.modele.stigma_monstre_positif = "Géodynamisme"
            self.modele.stigma_monstre_negatif = "Corps Massif"
            self.modele.monstre_points_de_force = 2
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 2
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 15
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Frappe Lourde": "Technique",  # gros degat, peu chance toucher
                "Poing Eclat": "Technique",  # rend blesse
                "Durcissement Argilite": "Technique",  # plus de defence  [x]
                "Eboulis": "Technique",  # peux lapider
                "Poing de Mana": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 1, "Degat coup critique": 1, "Gold": 20 + gold_bonus_par_etage, "Materiau": "Poussière Animée"}
        elif self.modele.monstre_nom == "Ombre Tangible":
            self.modele.stigma_monstre_positif = "Malédiction"
            self.modele.stigma_monstre_negatif = "Astralien"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 2
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Froideur d'Outretombe": "Sort", # gele
                "Claquement de Foudre": "Sort", # paralyse
                "Confusion": "Sort", # confond
                "Poing de Mana": "Sort"
            }
            self.modele.monstre_recompense = {"Mana max": 1, "Degat sort critique": 1, "Gold": 15 + gold_bonus_par_etage, "Materiau": "Ether Non-Newtonien"}
        elif self.modele.monstre_nom == "Clone de Verre":
            self.modele.stigma_monstre_positif = "Brisures"
            self.modele.stigma_monstre_negatif = "Fragile"
            self.modele.monstre_points_de_force = 2
            self.modele.monstre_points_de_intelligence = 2
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 1
            self.modele.monstre_points_de_vie_max = 10
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Attaque Légère": "Technique",
                "Durcissement Argilite": "Technique", # augmente def
                "Tir Arcanique": "Sort"
            }
            self.modele.monstre_recompense = {"Vie max": 1, "Vie": 15, "Mana max": 1, "Mana": 15, "Gold": 15 + gold_bonus_par_etage, "Materiau": "Eclat de Verre"}
        elif self.modele.monstre_nom == "Métroïde":
            self.modele.stigma_monstre_positif = "Xénoanatomie"
            self.modele.stigma_monstre_negatif = "Cryophobia"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 10
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 100
            self.modele.monstre_points_de_mana_max = 40
            self.modele.monstre_liste_actions = {
                "Accrochage": "Technique", # paralyse et degat
                "Drain": "Technique", # draine vie
                "Impact": "Technique", # degat
            }
            self.modele.monstre_recompense = {"Taux sort critique": 1, "Mana max": 3, "Gold": 35 + gold_bonus_par_etage, "Materiau": "Fluide Alien"}
        elif self.modele.monstre_nom == "Trienun":
            self.modele.stigma_monstre_positif = "Fièvre du Jeu"
            self.modele.stigma_monstre_negatif = "Addict"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 135
            self.modele.monstre_points_de_mana_max = 40
            self.modele.monstre_liste_actions = {
                "Réglages d'Usine": "Sort", #soin
                "Volepièce": "Sort", # prend golds [x]
                "Bandit Manchot": "Sort", # lance 3 symbole. feu, glace ou paralysie ou les trois, pour lui ou joueur  [x]
                "Ruée vers l'or": "Sort" # donne mal jaune
            }
            self.modele.monstre_recompense = {"Taux sort critique": 1,"Taux coup critique": 1, "Gold": 50 + gold_bonus_par_etage, "Materiau": "Morceau de Cloche"}
        elif self.modele.monstre_nom == "Phénix Juvénile":
            self.modele.stigma_monstre_positif = "Cendres du Renouveau"
            self.modele.stigma_monstre_negatif = "Faible Hematopoïèse"
            self.modele.monstre_points_de_force = 4
            self.modele.monstre_points_de_intelligence = 3
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 1
            self.modele.monstre_points_de_vie_max = 100
            self.modele.monstre_points_de_mana_max = 40
            self.modele.monstre_liste_actions = {
                "Souffle de Feu": "Technique",
                "Envol": "Technique", #reduit les chances de toucher de 30%  [x]
                "Coup du Foie": "Technique", # rend bléssé
                "Possession du mana": "Sort", # sorts coutent plus cher
                "Feu Regénérateur": "Sort",
                "Vents du Sud": "Sort",
            }
            self.modele.monstre_recompense = {"Taux esquive": 1, "Taux coup critique": 1, "Vie max": 3, "Gold": 35 + gold_bonus_par_etage, "Materiau": "Ecaille de Phénix"}
        elif self.modele.monstre_nom == "Rochemikaze":
            self.modele.stigma_monstre_positif = "Faveurs Explosives"
            self.modele.stigma_monstre_negatif = "Surveillé"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 5
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 110
            self.modele.monstre_points_de_mana_max = 40
            self.modele.monstre_liste_actions = {
                "Roulé-Boulet": "Technique", # confond
                "Jet de Magma": "Technique", # enflamme
                "Tomberoche": "Technique", # lapide
                "Regénération Basaltique": "Sort", # peut rendre bcp pv
                "Explosion": "Sort",
            }
            self.modele.monstre_recompense = {"Attaque": 1, "Vie": 20, "Gold": 35 + gold_bonus_par_etage, "Materiau": "Roche Glycérine"}
        elif self.modele.monstre_nom == "Loup de Glace":
            self.modele.stigma_monstre_positif = "Instincts de Bête"
            self.modele.stigma_monstre_negatif = "Cryolien"
            self.modele.monstre_points_de_force = 6
            self.modele.monstre_points_de_intelligence = 6
            self.modele.monstre_points_de_resistance = 4
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 125
            self.modele.monstre_points_de_mana_max = 40
            self.modele.monstre_liste_actions = {
                "Morsure de Givre": "Technique", #peux geler
                "Coup de Griffe": "Technique", #peu degat, gros degat crit
                "Hurlement": "Technique", #pas de technique, pas de sorts  [x]
                "Cercueil de Neige": "Sort", # gele
            }
            self.modele.monstre_recompense = {"Degat coup critique": 2, "Vie max": 2, "Gold": 35 + gold_bonus_par_etage, "Materiau": "Poil Gelé"}
        elif self.modele.monstre_nom == "Voleur Félin":
            self.modele.stigma_monstre_positif = "Auromancie"
            self.modele.stigma_monstre_negatif = "Copycat"
            self.modele.monstre_points_de_force = 8
            self.modele.monstre_points_de_intelligence = 12
            self.modele.monstre_points_de_resistance = 10
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 75
            self.modele.monstre_points_de_mana_max = 50
            self.modele.monstre_liste_actions = {
                "Attire-Gold": "Technique", #prend du gold [x]
                "Lèche-Blessure": "Technique", # soin
                "Cat-astrophe": "Sort", #gele,enflamme,draine en mm temps [x]
                "Point Vital": "Sort", # gros degat critiques
            }
            self.modele.monstre_recompense = {"Mana max": 4, "Gold": 45 + gold_bonus_par_etage, "Degat sort critique": 2, "Materiau": "Moustache de Chat"}
        elif self.modele.monstre_nom == "Siffloteur":
            self.modele.stigma_monstre_positif = "Extinction de Voix"
            self.modele.stigma_monstre_negatif = "Sang Doré"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 15
            self.modele.monstre_points_de_resistance = 12
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 80
            self.modele.monstre_points_de_mana_max = 50
            self.modele.monstre_liste_actions = {
                "Vents du Nord": "Sort", #gele
                "Vents du Sud": "Sort", #brule
                "Vents de l'Est": "Sort", #paralyse
                "Vents de l'Ouest": "Sort", #draine
                "Son Rapide": "Sort", #Fais perdre bcp pv
                "Son Lent": "Sort" #fais perdre bcp mana [x]
            }
            self.modele.monstre_recompense = {"Mana max": 4, "Gold": 45 + gold_bonus_par_etage, "Materiau": "Fragment Osseux"}
        elif self.modele.monstre_nom == "Lapin du Désastre":
            self.modele.stigma_monstre_positif = "Fertilité"
            self.modele.stigma_monstre_negatif = "Violence"
            self.modele.monstre_points_de_force = 14
            self.modele.monstre_points_de_intelligence = 12
            self.modele.monstre_points_de_resistance = 9
            self.modele.monstre_nombre_de_vies_supplementaire = 1
            self.modele.monstre_points_de_vie_max = 50
            self.modele.monstre_points_de_mana_max = 50
            self.modele.monstre_liste_actions = {
                "Morsure": "Technique", #gros degats
                "Gel": "Sort", # gele
                "Giga Gel": "Sort", # peut geler sur longtemps
                "Oeuil Maudit": "Sort", #augmente cout mana
                "Carotte Magique": "Sort", #soin
            }
            self.modele.monstre_recompense = {"Vie max": 4, "Gold": 45 + gold_bonus_par_etage, "Materiau": "Iris du Malheur"}
        elif self.modele.monstre_nom == "Cerf Voleur":
            self.modele.stigma_monstre_positif = "Rituel Vaudoo"
            self.modele.stigma_monstre_negatif = "Hématophobe"
            self.modele.monstre_points_de_force = 15
            self.modele.monstre_points_de_intelligence = 15
            self.modele.monstre_points_de_resistance = 14
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 75
            self.modele.monstre_points_de_mana_max = 50
            self.modele.monstre_liste_actions = {
                "Coup Anti-Magie": "Technique", #attaaque meme si protection [x]
                "Attire-Magie": "Technique", #perd pm [x]
                "Coup de pierre": "Technique", # lapide
                "Vole-Ame": "Sort", # perd viemax [x]
                "Coup de Foudre": "Sort", # paralyse
            }
            self.modele.monstre_recompense = {"Mana max": 4, "Gold": 45 + gold_bonus_par_etage, "Taux sort critique": 1, "Materiau": "Velour de Cervidé"}
        elif self.modele.monstre_nom == "Aspiratrésor Blindé":
            self.modele.stigma_monstre_positif = "Circuits Logique"
            self.modele.stigma_monstre_negatif = "Surcharge Processeur"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 15
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 25
            self.modele.monstre_points_de_mana_max = 50
            self.modele.monstre_liste_actions = {
                "Aspiration": "Technique" # prend gold, mana + vie, manamax + viemax, taux critique sort+ attaque, force + intelligence, defence [x]
            }
            self.modele.monstre_recompense = {"Gold": 60 + gold_bonus_par_etage, "Intelligence": 1, "Defence": 1, "Taux sort critique": 1, "Taux coup critique":1, "Materiau": "Composants Electroniques"}
        elif self.modele.monstre_nom == "Gluant de Crystal":
            self.modele.stigma_monstre_positif = "Esotéricisme"
            self.modele.stigma_monstre_negatif = "Anisotropie"
            self.modele.monstre_points_de_force = 20
            self.modele.monstre_points_de_intelligence = 20
            self.modele.monstre_points_de_resistance = 10
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 150
            self.modele.monstre_points_de_mana_max = 60
            self.modele.monstre_liste_actions = {
                "Gros Coup de Boule": "Technique",
                "Corruption": "Technique", #drain
                "Laser": "Technique",  # laser brule vie + mana [x]
                "Soin Avancé": "Sort", #soin
                "Flamme Avancée": "Sort", #brule
                "Rituel": "Sort", #perd vie, malediction vie + mana + item 2 tours [x]
            }
            self.modele.monstre_recompense = {"Mana max": 3, "Vie max": 3, "Materiau": "Eclat de Crystal"}
        elif self.modele.monstre_nom == "Sixenun":
            self.modele.stigma_monstre_positif = "Carrousel Chanceux"
            self.modele.stigma_monstre_negatif = "Consummé"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 15
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 110
            self.modele.monstre_points_de_mana_max = 60
            self.modele.monstre_liste_actions = {
                "Roulette": "Technique", #lance roulette. mise ou pas = critique ou pas. si rouge, foule d'effet sur joueur. si vert, foule d'effet sur ennemi. [x]
                "Jet d'Argent": "Technique", #jette piece passe a travers sorts, 75% gros degats , 25% attrape gold. [x]
            }
            self.modele.monstre_recompense = {"Mana": 100, "Vie": 100, "Attaque": 1, "Gold": 60 + gold_bonus_par_etage, "Materiau": "Pilules de Roulette"}
        elif self.modele.monstre_nom == "Siffloteur de Jade":
            self.modele.stigma_monstre_positif = "Bouclier Acoustique"
            self.modele.stigma_monstre_negatif = "Mégalovania"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 25
            self.modele.monstre_points_de_resistance = 12
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 115
            self.modele.monstre_points_de_mana_max = 60
            self.modele.monstre_liste_actions = {
                "Tempêtes du Nord": "Sort", #gele + 50% plus de sorts [x]
                "Tempêtes du Sud": "Sort", #brule + 50% plus de techniques [x]
                "Tempêtes de l'Est": "Sort", #paralyse + 50% confus (plus item) [x]
                "Tempêtes de l'Ouest": "Sort", #draine + 50% mal jaune (action coute gold) [x]
                "Vacarme Rapide": "Sort", #Fais perdre bcp pv + 50% blesse [x]
                "Vacarme Lent": "Sort" #fais perdre bcp mana + 50% instable (plus de mana par sorts) [x]
            }
            self.modele.monstre_recompense = {"Degat sort critique": 2, "Degat coup critique": 2, "Gold": 30 + gold_bonus_par_etage, "Materiau": "Fragment de Jade"}
        elif self.modele.monstre_nom == "Aurelionite":
            self.modele.stigma_monstre_positif = "Toucher de Midas"
            self.modele.stigma_monstre_negatif = "Aveuglé"
            self.modele.monstre_points_de_force = 35
            self.modele.monstre_points_de_intelligence = 35
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 2
            self.modele.monstre_points_de_vie_max = 175
            self.modele.monstre_points_de_mana_max = 60
            self.modele.monstre_liste_actions = {
                "Lame Dorée": "Technique", #peut donner mal jaune
                "Ultralaser": "Technique", #peut bruler
                "Constructions du Zénith": "Technique", #soin
                "Oméga Gelure": "Sort", #gele
                "Oméga Lapidation": "Sort", #degat +lapide
                "Oméga Saignée": "Sort", # drain vie
            }
            self.modele.monstre_recompense = {"Defence": 2, "Gold": 100 + gold_bonus_par_etage, "Materiau": "Poussière Dorée Animée"}
        elif self.modele.monstre_nom == "Sacatrésor":
            self.modele.stigma_monstre_positif = "Manipulation"
            self.modele.stigma_monstre_negatif = "Inflammable"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 20
            self.modele.monstre_points_de_mana_max = 60
            self.modele.monstre_liste_actions = {
                "Gemme Rouge": "Technique", #soin
                "Gemme Bleue": "Technique", #vol mana [x]
            }
            self.modele.monstre_recompense = {"Taux esquive": 1, "Vie max": 2, "Mana max": 2, "Taux sort critique": 1, "Taux coup critique":1, "Gold": 150 + gold_bonus_par_etage, "Materiau": "Gemme Bleue"}
        elif self.modele.monstre_nom == "Mimique":
            self.modele.stigma_monstre_positif = "Abomination"
            self.modele.stigma_monstre_negatif = "Homoncule"
            self.modele.monstre_points_de_force = round(2.5 * self.modele.numero_de_letage)
            self.modele.monstre_points_de_intelligence = round(2.5 * self.modele.numero_de_letage)
            self.modele.monstre_points_de_resistance = round(2.5 * self.modele.numero_de_letage)
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = round((60 * self.modele.numero_de_letage) + 100)
            self.modele.monstre_points_de_mana_max = 100
            self.modele.monstre_liste_actions = {
                "Avale": "Technique", #bcp degat
                "Vide": "Sort", # plus technique plus sorts plus item [x]
                "Engloutis": "Sort", #soin
                "Mache": "Sort", #drain saignee
            }
            liste_action_supplementaire = {}
            if self.modele.numero_de_letage == 2:
                liste_action_supplementaire = {
                    "Coup de Boule": "Technique",
                    "Etranglement": "Technique", # rend muet
                    "Soin": "Sort",
                    "Flamme": "Sort",
                    "Tout Feu Tout Flamme": "Sort", # combo electrique, pour le feu [x]
                    "Feu Regénérateur": "Sort", # soin
                    "Poing de Feu": "Technique", # brule
                    "Brulevent": "Technique", # rend muet
                    "Frappe Lourde": "Technique",  # gros degat, peu chance toucher
                    "Poing Eclat": "Technique",  # rend blesse
                    "Durcissement Argilite": "Technique",  # plus de defence  [x]
                    "Eboulis": "Technique",  # peux lapider
                    "Poing de Mana": "Sort",
                    "Froideur d'Outretombe": "Sort", # gele
                    "Claquement de Foudre": "Sort", # paralyse
                    "Confusion": "Sort", # confond
                    "Poing de Mana": "Sort",
                    "Attaque Légère": "Technique",
                    "Durcissement Argilite": "Technique", # augmente def
                    "Tir Arcanique": "Sort"
                }
            elif self.modele.numero_de_letage == 4:
                liste_action_supplementaire = {
                    "Accrochage": "Technique", # paralyse et degat
                    "Drain": "Technique", # draine vie
                    "Impact": "Technique", # degat
                    "Réglages d'Usine": "Sort", #soin
                    "Volepièce": "Sort", # prend golds [x]
                    "Bandit Manchot": "Sort", # lance 3 symbole. feu, glace ou paralysie ou les trois, pour lui ou joueur  [x]
                    "Ruée vers l'or": "Sort", # donne mal jaune
                    "Souffle de Feu": "Technique",
                    "Envol": "Technique", #reduit les chances de toucher de 30%  [x]
                    "Coup du Foie": "Technique", # rend bléssé
                    "Possession du mana": "Sort", # sorts coutent plus cher
                    "Roulé-Boulet": "Technique", # confond
                    "Jet de Magma": "Technique", # enflamme
                    "Tomberoche": "Technique", # lapide
                    "Regénération Basaltique": "Sort", # peut rendre bcp pv
                    "Explosion": "Sort",
                    "Morsure de Givre": "Technique", #peux geler
                    "Coup de Griffe": "Technique", #peu degat, gros degat crit
                    "Hurlement": "Technique", #pas de technique, pas de sorts  [x]
                    "Cercueil de Neige": "Sort", # gele
                }
            elif self.modele.numero_de_letage == 6:
                liste_action_supplementaire = {
                    "Attire-Gold": "Technique", #prend du gold [x]
                    "Lèche-Blessure": "Technique", # soin
                    "Cat-astrophe": "Sort", #gele,enflamme,draine en mm temps [x]
                    "Point Vital": "Sort", # gros degat critiques
                    "Vents du Nord": "Sort", #gele
                    "Vents du Sud": "Sort", #brule
                    "Vents de l'Est": "Sort", #paralyse
                    "Vents de l'Ouest": "Sort", #draine
                    "Son Rapide": "Sort", #Fais perdre bcp pv
                    "Son Lent": "Sort", #fais perdre bcp mana [x]
                    "Morsure": "Technique", #gros degats
                    "Gel": "Sort", # gele
                    "Giga Gel": "Sort", # peut geler sur longtemps
                    "Oeuil Maudit": "Sort", #augmente cout mana
                    "Carotte Magique": "Sort", #soin
                    "Coup Anti-Magie": "Technique", #attaaque meme si protection [x]
                    "Attire-Magie": "Technique", #perd pm [x]
                    "Coup de pierre": "Technique", # lapide
                    "Vole-Ame": "Sort", # perd viemax [x]
                    "Coup de Foudre": "Sort", # paralyse
                    "Aspiration": "Technique" # prend gold, mana + vie, manamax + viemax, taux critique sort+ attaque, force + intelligence, defence [x]
                }
            elif self.modele.numero_de_letage in [8, 10]:
                liste_action_supplementaire = {
                    "Gros Coup de Boule": "Technique",
                    "Corruption": "Technique", #drain
                    "Laser": "Technique",  # laser brule vie + mana [x]
                    "Soin Avancé": "Sort", #soin
                    "Flamme Avancée": "Sort", #brule
                    "Rituel": "Sort", #perd vie, malediction vie + mana + item 2 tours [x]
                    "Roulette": "Technique", #lance roulette. mise ou pas = critique ou pas. si rouge, foule d'effet sur joueur. si vert, foule d'effet sur ennemi. [x]
                    "Jet d'Argent": "Technique", #jette piece passe a travers sorts, 75% gros degats , 25% attrape gold. [x]
                    "Tempêtes du Nord": "Sort", #gele + 50% plus de sorts [x]
                    "Tempêtes du Sud": "Sort", #brule + 50% plus de techniques [x]
                    "Tempêtes de l'Est": "Sort", #paralyse + 50% confus (plus item) [x]
                    "Tempêtes de l'Ouest": "Sort", #draine + 50% mal jaune (action coute gold) [x]
                    "Vacarme Rapide": "Sort", #Fais perdre bcp pv + 50% blesse [x]
                    "Vacarme Lent": "Sort", #fais perdre bcp mana + 50% instable (plus de mana par sorts) [x]
                    "Lame Dorée": "Technique", #peut donner mal jaune
                    "Ultralaser": "Technique", #peut bruler
                    "Constructions du Zénith": "Technique", #soin
                    "Oméga Gelure": "Sort", #gele
                    "Oméga Lapidation": "Sort", #degat +lapide
                    "Oméga Saignée": "Sort", # drain vie
                    "Gemme Rouge": "Technique", #soin
                    "Gemme Bleue": "Technique", #vol mana [x]
                }
            for action in liste_action_supplementaire:
                self.modele.monstre_liste_actions[action] = liste_action_supplementaire[action]

            self.modele.monstre_recompense = {"Taux esquive": 1, "Mana max": 5, 
                                              "Vie max": 5, "Degat sort critique": 3, 
                                              "Degat coup critique": 3, "Gold": 25 + gold_bonus_par_etage, "Materiau": "Fragment Insatiable"}

        # Boss
        elif self.modele.monstre_nom == "Clone d'Obsidienne":
            self.modele.stigma_monstre_positif = "Roche Ténébreuse"
            self.modele.stigma_monstre_negatif = "Flocon de Neige"
            self.modele.stigma_monstre_bonus = "Hyallo-Réflection"
            self.modele.monstre_points_de_force = 3
            self.modele.monstre_points_de_intelligence = 3
            self.modele.monstre_points_de_resistance = 2
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 165
            self.modele.monstre_points_de_mana_max = 35
            self.modele.monstre_liste_actions = {
                "Attaque Lourde": "Technique",
                "Durcissement Calcaire": "Technique", # augmente def
                "Bombe Arcanique": "Sort",
                "Sonata Pitoyable": "Sort", #soin
                "Eveil de Runes": "Sort", # differents effet selon la rune invoquée [x]
                "Coup de Boule": "Technique",
                "Froideur d'Outretombe": "Sort", # gele
            }
            self.modele.monstre_recompense = {"Red coin": 1, "Tirage": 1, "Gold": 50 + gold_bonus_par_etage, "Mana max": 10, "Endurance": 10}
        elif self.modele.monstre_nom == "Chevalier Pourpre":
            self.modele.stigma_monstre_positif = "Armure de Plates"
            self.modele.stigma_monstre_negatif = "Trauma de Guerre"
            self.modele.stigma_monstre_bonus = "Corps d'Acier"
            self.modele.monstre_points_de_force = 6
            self.modele.monstre_points_de_intelligence = 3
            self.modele.monstre_points_de_resistance = 8
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 220
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Lame de Feu": "Technique", #brule
                "Lame de Gel": "Technique", #gele
                "Lame Pourpre": "Technique", #draine
                "Lame Courageuse": "Technique", #gros degats
                "Medecine de Guerre": "Technique", #soin
                "Lamentations": "Sort", #blesse et maudit plus mana [x]
            }
            self.modele.monstre_recompense = {"Red coin": 1, "Tirage": 1, "Gold": 100 + gold_bonus_par_etage, "Vie max": 10, "Endurance": 10}
        elif self.modele.monstre_nom == "Coquille Vide":
            self.modele.stigma_monstre_positif = "Armure de Plates"
            self.modele.stigma_monstre_negatif = "Trauma de Guerre"
            self.modele.stigma_monstre_bonus = "Corps d'Acier"
            self.modele.monstre_points_de_force = 6
            self.modele.monstre_points_de_intelligence = 3
            self.modele.monstre_points_de_resistance = 8
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 300
            self.modele.monstre_points_de_mana_max = 15
            self.modele.monstre_liste_actions = {
                "Coup Anti-Magie": "Technique", #attaaque meme si protection [x]
                "Lame de Feu": "Technique", #brule
                "Lame de Gel": "Technique", #gele
                "Lame Pourpre": "Technique", #draine
                "Lame Courageuse": "Technique", #gros degats
                "Medecine de Guerre": "Technique", #soin
                "Lamentations": "Sort", #blesse et maudit plus mana [x]
            }
            self.modele.monstre_recompense = {"Red coin": 1, "Tirage": 1, "Gold": 100 + gold_bonus_par_etage, "Vie max": 10, "Endurance": 10}
        elif self.modele.monstre_nom == "Roi Amonrê":
            self.modele.stigma_monstre_positif = "Bénédiction Divine"
            self.modele.stigma_monstre_negatif = "Patchwork"
            self.modele.stigma_monstre_bonus = "Apotre de Râ"
            self.modele.monstre_points_de_force = 2
            self.modele.monstre_points_de_intelligence = 10
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 1
            self.modele.monstre_points_de_vie_max = 320
            self.modele.monstre_points_de_mana_max = 45
            self.modele.monstre_liste_actions = {
                "Invoquation Canope": "Sort", #invoque vase canope, peut echouer [x]
                "Rejuvenation": "Sort", #gros soin
                "Jugement": "Sort", #degat = monstre tue [x]
                "Combo Misérable": "Technique" #combo electrique , mais maudit [x]
            }
            self.modele.monstre_recompense = {"Red coin": 1, "Tirage": 1, "Gold": 150 + gold_bonus_par_etage, "Taux sort critique": 10, "Endurance": 10 }
        elif self.modele.monstre_nom == "Apprentie":
            self.modele.stigma_monstre_positif = "Sort Chanceux"
            self.modele.stigma_monstre_negatif = "Anxiété Sociale"
            self.modele.stigma_monstre_bonus = "Mal Jaune"
            self.modele.monstre_points_de_force = 3
            self.modele.monstre_points_de_intelligence = 12
            self.modele.monstre_points_de_resistance = 5
            self.modele.monstre_nombre_de_vies_supplementaire = 1
            self.modele.monstre_points_de_vie_max = 200
            self.modele.monstre_points_de_mana_max = 45
            self.modele.monstre_liste_actions = {
                "Faisceau Statique": "Sort",  #paralyse
                "Thermosphère Brulante": "Sort", #brule
                "Pic Froid": "Sort", #gele
                "Création de Lapis": "Sort", #lapide
                "Explosion Renforcée": "Sort", #gros dégats
                "Dance Siphoneuse": "Sort", #saigne
                "Sonata Miséricordieuse": "Sort", #soigne
                "Magie Noire": "Sort" #blesse et hausse cout mana [x]
            }
            self.modele.monstre_recompense = {"Red coin": 1, "Méga Tirage": 1, "Gold": 200 + gold_bonus_par_etage, }
        elif self.modele.monstre_nom == "Minaraï":
            self.modele.stigma_monstre_positif = "Sort Chanceux"
            self.modele.stigma_monstre_negatif = "Anxiété Sociale"
            self.modele.stigma_monstre_bonus = "Mal Jaune"
            self.modele.monstre_points_de_force = 10
            self.modele.monstre_points_de_intelligence = 20
            self.modele.monstre_points_de_resistance = 12
            self.modele.monstre_nombre_de_vies_supplementaire = 1
            self.modele.monstre_points_de_vie_max = 300
            self.modele.monstre_points_de_mana_max = 75
            self.modele.monstre_liste_actions = {
                "Faisceau de l'Eclair": "Sort",  #paralyse
                "Thermosphère de la Fournaise": "Sort", #brule
                "Pic Glacial": "Sort", #gele
                "Création Obsidienne": "Sort", #lapide
                "Explosion Maitrisée": "Sort", #gros dégats
                "Dance Parasite": "Sort", #saigne
                "Sonata Sincère": "Sort", #soigne
                "Magie Ténébreuse": "Sort" #empeche sort et technique [x]
            }
            self.modele.monstre_recompense = {"Red coin": 1, "Méga Tirage": 1, "Gold": 200 + gold_bonus_par_etage, "Taux sort critique": 5, "Intelligence": 5, "Endurance": 10}
        elif self.modele.monstre_nom == "Bouffon":
            self.modele.stigma_monstre_positif = "Plus d'un Tour"
            self.modele.stigma_monstre_negatif = "Arlequin"
            self.modele.stigma_monstre_bonus = "Nordique"
            self.modele.monstre_points_de_force = 10
            self.modele.monstre_points_de_intelligence = 10
            self.modele.monstre_points_de_resistance = 15
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 750
            self.modele.monstre_points_de_mana_max = 50
            self.modele.monstre_liste_actions = {
                "Tournicoti": "Sort", #reprend vie
                "Tournicota": "Sort", #envoie boule a renvoyer ou esquiver [x]
                "Tournicotons": "Sort", #vague a esquiver [x]
                "Tournicotez": "Sort", #queston a repondre [x]
            }
            self.modele.monstre_recompense = {"Red coin": 1, "Tirage": 1, "Gold": 250 + gold_bonus_par_etage, "Taux sort critique": 5, "Vie max": 15, "Mana max": 15, "Endurance": 10}
        elif self.modele.monstre_nom == "Le Pianiste":
            self.modele.stigma_monstre_positif = "Coeur Immolé"
            self.modele.stigma_monstre_negatif = "Inconsolable Rage"
            self.modele.stigma_monstre_bonus = "Nordique"
            self.modele.monstre_points_de_force = 5
            self.modele.monstre_points_de_intelligence = 15
            self.modele.monstre_points_de_resistance = 12
            self.modele.monstre_nombre_de_vies_supplementaire = 1
            self.modele.monstre_points_de_vie_max = 750
            self.modele.monstre_points_de_mana_max = 100
            self.modele.monstre_liste_actions = {
                "Do": "Sort", # reprend vie
                "Ré": "Sort", # met le feu
                "Mi": "Sort", # met la glace
                "Fa": "Sort", # met la foudre 
                "Sol": "Sort", # met le sang
                "La": "Sort", # met le dégat
                "Si": "Sort", # rend confus
                "Symphonie": "Sort", # met feu glace sang degat
                "Déchiquetage": "Technique", # Blesse énormément
            }
            self.modele.monstre_recompense = {"Red coin": 1, "Tirage": 1, "Gold": 250 + gold_bonus_par_etage, "Taux sort critique": 5, "Vie max": 15, "Mana max": 15, "Endurance": 10}
        elif self.modele.monstre_nom == "Noa":
            self.modele.stigma_monstre_positif = "Coeur Immolé"
            self.modele.stigma_monstre_negatif = "Inconsolable Rage"
            self.modele.stigma_monstre_bonus = "Nordique"
            self.modele.monstre_points_de_force = 0
            self.modele.monstre_points_de_intelligence = 0
            self.modele.monstre_points_de_resistance = 0
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 1
            self.modele.monstre_points_de_mana_max = 1
            self.modele.monstre_liste_actions = {
                "Rien": "Technique", 
            }
            self.modele.monstre_recompense = {"Red coin": 1, "Tirage": 1, "Gold": 250 + gold_bonus_par_etage, "Taux sort critique": 5, "Vie max": 15, "Mana max": 15, "Endurance": 10}
        elif self.modele.monstre_nom == "Prince des Voleurs":
            self.modele.stigma_monstre_positif = "Bomberman"
            self.modele.stigma_monstre_negatif = "Hautain"
            self.modele.stigma_monstre_bonus = "Intemporel"
            self.modele.monstre_points_de_force = 18
            self.modele.monstre_points_de_intelligence = 18
            self.modele.monstre_points_de_resistance = 20
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 1100
            self.modele.monstre_points_de_mana_max = 30
            self.modele.monstre_liste_actions = {
                "Attaque Titanesque": "Technique", #utilise orbe furie et attaque
                "Remede Divin": "Technique", #soin
                "Fleche Rouge": "Technique", #brule
                "Fleche Bleue": "Technique", #gele
                "Crystal Elémentaire": "Technique",  # inflige lourd brule ou gele [x]
                "Pendule Etrange": "Technique", #paralysie
                "Panacée Universelle": "Technique", #soigne toute les altérations d'état [x]
                "Missile Arcanique": "Sort", #utilise orbe folie et sort
                "Tome de Salomon": "Sort", #draine mp [x]
                "Houken": "Sort", #draine vie
                
            }
            self.modele.monstre_recompense = {"Red coin": 1, "Tirage": 1, "Gold": 300 + gold_bonus_par_etage, "Degat coup critique": 10, "Degat sort critique": 10, "Endurance": 10}
        elif self.modele.monstre_nom == "Roi Déchu":
            self.modele.stigma_monstre_positif = "Lignée Royale"
            self.modele.stigma_monstre_negatif = "Divinement Renié"
            self.modele.stigma_monstre_bonus = "Paranoïa"
            self.modele.monstre_points_de_force = 5
            self.modele.monstre_points_de_intelligence = 5
            self.modele.monstre_points_de_resistance = 25
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 432
            self.modele.monstre_points_de_mana_max = 15
            self.modele.monstre_liste_actions = {
                "Lame Ultime": "Technique", #gros degats
                "Bouclier Ultime": "Technique", #reprend beaucoup de vie
                "Laser Ultime": "Technique", #moyen degat et feu
                "Sort Ultime": "Sort", #gros degat, perd mana [x]
                "Ultime Ultime": "Sort", # impossible d'utiliser sorts et techniques [x]
                "Ultima": "Sort", #ramene la vie du joueur a 10% [x]
            }
            self.modele.monstre_recompense = {"Red coin": 1, "Tirage": 1, "Gold": 350 + gold_bonus_par_etage, "Defence": 5, "Attaque": 5, "Endurance": 10}
        elif self.modele.monstre_nom == "Maitre Mage":
            self.modele.stigma_monstre_positif = "Hardi"
            self.modele.stigma_monstre_negatif = "Aucun"
            self.modele.stigma_monstre_bonus = "Ministre de la Magie"
            self.modele.monstre_points_de_force = 15
            self.modele.monstre_points_de_intelligence = 25
            self.modele.monstre_points_de_resistance = 14
            self.modele.monstre_nombre_de_vies_supplementaire = 1
            self.modele.monstre_points_de_vie_max = 600
            self.modele.monstre_points_de_mana_max = 70
            self.modele.monstre_liste_actions = {
                "Ascension Runique": "Technique", #seulement la rune du drain de vie
                "Lame Vaillante": "Technique", #grosse attaque
                "Sables du Temps": "Technique", #paralysie 3 tour, monstre perd 5% vie [x]
                "Faisceau Foudroyant": "Sort", #paralyse
                "Thermosphère Magmatique": "Sort", #brule
                "Pic Polaire": "Sort", #gele
                "Création de la Montagne": "Sort", #lapide
                "Explosion Fatale": "Sort", #gros degats
                "Dance Destructrice": "Sort", #drain
                "Sonata Bienveillante": "Sort" #soigne
            }
            self.modele.monstre_recompense = {
                "Red coin": 1, "Tirage": 1,
                "Gold": 400 + gold_bonus_par_etage}
        elif self.modele.monstre_nom == "Ministre du Mana":
            self.modele.stigma_monstre_positif = "Hardi"
            self.modele.stigma_monstre_negatif = "Fatigue"
            self.modele.stigma_monstre_bonus = "Ministre de la Magie"
            self.modele.monstre_points_de_force = 30
            self.modele.monstre_points_de_intelligence = 38
            self.modele.monstre_points_de_resistance = 24
            self.modele.monstre_nombre_de_vies_supplementaire = 1
            self.modele.monstre_points_de_vie_max = 488
            self.modele.monstre_points_de_mana_max = 100
            self.modele.monstre_liste_actions = {
                "Dragon Ascendant": "Sort", #attaque par vague a esquiver [x]
                "Rituel Canope": "Sort", #seulement le canope de la paralysie 
                "Magie Abyssale": "Sort", #scelle sort et technique, draine 10% pm [x]
                "Faisceau de la Mort Blanche": "Sort", #paralyse
                "Thermosphère Solaire": "Sort", #brule
                "Pic Zéro": "Sort", #gele
                "Création Continentale": "Sort", #lapide
                "Explosion de la Comète": "Sort", #gros degats
                "Dance Créatrice": "Sort", #drain
                "Sonata Absolutrice": "Sort" #soin
            }
            self.modele.monstre_recompense = {"Red coin": 1, "Méga Tirage": 1, "Vie max": 20, 
                                       "Mana max": 20, "Gold": 400 + gold_bonus_par_etage, "Endurance": 10}
        elif self.modele.monstre_nom == "Ah Kin":
            self.modele.stigma_monstre_positif = "Aucun"
            self.modele.stigma_monstre_negatif = "Aucun"
            self.modele.stigma_monstre_bonus = "Aucun"
            self.modele.monstre_points_de_force = 30
            self.modele.monstre_points_de_intelligence = 38
            self.modele.monstre_points_de_resistance = 24
            self.modele.monstre_nombre_de_vies_supplementaire = self.Player.vies_du_gardien
            self.modele.monstre_points_de_vie_max = 800
            self.modele.monstre_points_de_mana_max = 50
            self.modele.monstre_liste_actions = {
                "Attaque Lourde": "Technique",
                "Lame Courageuse": "Technique", #gros degats
                "Crystal Elémentaire": "Technique",  # inflige lourd brule ou gele [x]
                "Remede Divin": "Technique", #soin
                "Combo Misérable": "Technique", #combo electrique , mais maudit [x]
            }
            self.modele.monstre_recompense = {}
            if self.modele.monstre_nombre_de_vies_supplementaire == 9:
                self.modele.monstre_tags.append("Voluntad Káak")
                self.modele.monstre_tags.append("Voluntad Hielo")
                self.modele.monstre_tags.append("Voluntad Le Rayo")
            elif self.modele.monstre_nombre_de_vies_supplementaire == 6:
                self.modele.monstre_tags.append("Voluntad Le Luumo")
                self.modele.monstre_tags.append("Voluntad U Kiikel")
                self.modele.monstre_tags.append("Voluntad U Wíinkilal")
            elif self.modele.monstre_nombre_de_vies_supplementaire == 3:
                self.modele.monstre_tags.append("Voluntad Káak") #feu
                self.modele.monstre_tags.append("Voluntad Hielo") #glace
                self.modele.monstre_tags.append("Voluntad Le Rayo") #foudre
                self.modele.monstre_tags.append("Voluntad Le Luumo") #terre
                self.modele.monstre_tags.append("Voluntad U Kiikel") #sang
                self.modele.monstre_tags.append("Voluntad U Wíinkilal") #physique | Voluntad Tin Tuukul pour ame
        elif self.modele.monstre_nom == "Drone de Sécurité YucaTech Inc.":
            self.modele.stigma_monstre_positif = "Aucun"
            self.modele.stigma_monstre_negatif = "Aucun"
            self.modele.stigma_monstre_bonus = "Aucun"
            self.modele.monstre_points_de_force = 30
            self.modele.monstre_points_de_intelligence = 38
            self.modele.monstre_points_de_resistance = 24
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 200
            self.modele.monstre_points_de_mana_max = 50
            self.modele.monstre_liste_actions = {
                "Laser Anti-Personnel": "Sort", # 5% de vie
                "Systeme de Support": "Sort", # soigne 50 pv
                "Protocole Supernova": "Sort",  # perd 10% de vie, inflige 10% de vie
                "Flash Bang": "Sort", # déconcentre
            }
            self.modele.est_maudit_par_les_items = True
            self.modele.est_maudit_par_les_items_nombre_tour = 999
            self.modele.monstre_recompense = {"Vie" : 75, "Mana": 25}
        elif self.modele.monstre_nom == "Yvan":
            self.modele.stigma_monstre_positif = "Aucun"
            self.modele.stigma_monstre_negatif = "Aucun"
            self.modele.stigma_monstre_bonus = "Aucun"
            self.modele.monstre_points_de_force = 30
            self.modele.monstre_points_de_intelligence = 38
            self.modele.monstre_points_de_resistance = 24
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 800
            self.modele.monstre_points_de_mana_max = 1
            self.modele.monstre_liste_actions = {
                "Attaque Lourde": "Technique",
                "Lame Courageuse": "Technique", #gros degats
                "Crystal Elémentaire": "Technique",  # inflige lourd brule ou gele [x]
                "Remede Divin": "Technique", #soin
                "Combo Misérable": "Technique", #combo electrique , mais maudit [x]
            }
            self.modele.monstre_recompense = {"Red coin": 1, "Méga Tirage": 1, "Vie max": 20, 
                                       "Mana max": 20, "Gold": 400 + gold_bonus_par_etage, "Endurance": 10}
        elif self.modele.monstre_nom == "Armée des Anges":
            self.modele.stigma_monstre_positif = "Aucun"
            self.modele.stigma_monstre_negatif = "Aucun"
            self.modele.stigma_monstre_bonus = "Aucun"
            self.modele.monstre_points_de_force = 30
            self.modele.monstre_points_de_intelligence = 38
            self.modele.monstre_points_de_resistance = 24
            self.modele.monstre_nombre_de_vies_supplementaire = 5
            self.modele.monstre_points_de_vie_max = 150
            self.modele.monstre_points_de_mana_max = 20
            self.modele.monstre_liste_actions = {
                "Attaque Lourde": "Technique",
                "Lame Courageuse": "Technique", #gros degats
                "Crystal Elémentaire": "Technique",  # inflige lourd brule ou gele [x]
                "Remede Divin": "Technique", #soin
                "Combo Misérable": "Technique", #combo electrique , mais maudit [x]
                "Houken": "Sort", #draine vie
                "Sonata Sincère": "Sort", #soigne

            }
            self.modele.monstre_recompense = {"Red coin": 1, "Méga Tirage": 1, "Vie max": 20, 
                                       "Mana max": 20, "Gold": 400 + gold_bonus_par_etage, "Endurance": 10}
        elif self.modele.monstre_nom == "Armée de la Fin":
            self.modele.stigma_monstre_positif = "Aucun"
            self.modele.stigma_monstre_negatif = "Aucun"
            self.modele.stigma_monstre_bonus = "Aucun"
            self.modele.monstre_points_de_force = 30
            self.modele.monstre_points_de_intelligence = 38
            self.modele.monstre_points_de_resistance = 24
            self.modele.monstre_nombre_de_vies_supplementaire = 3
            self.modele.monstre_points_de_vie_max = 250
            self.modele.monstre_points_de_mana_max = 1
            self.modele.monstre_liste_actions = {
                "Attaque Lourde": "Technique",
                "Lame Courageuse": "Technique", #gros degats
                "Crystal Elémentaire": "Technique",  # inflige lourd brule ou gele [x]
                "Remede Divin": "Technique", #soin
                "Combo Misérable": "Technique", #combo electrique , mais maudit [x]
                "Houken": "Sort", #draine vie
                "Sonata Sincère": "Sort", #soigne
                "Magie Abyssale": "Sort", #scelle sort et technique, draine 10% pm [x]
                "Eveil de Runes": "Sort", # differents effet selon la rune invoquée [x]
            }
            self.modele.monstre_recompense = {"Red coin": 1, "Méga Tirage": 1, "Vie max": 20, 
                                       "Mana max": 20, "Gold": 400 + gold_bonus_par_etage, "Endurance": 10}
        elif self.modele.monstre_nom == "Archange Michael":
            self.modele.stigma_monstre_positif = "Aucun"
            self.modele.stigma_monstre_negatif = "Aucun"
            self.modele.stigma_monstre_bonus = "Aucun"
            self.modele.monstre_points_de_force = 30
            self.modele.monstre_points_de_intelligence = 38
            self.modele.monstre_points_de_resistance = 24
            self.modele.monstre_nombre_de_vies_supplementaire = 0
            self.modele.monstre_points_de_vie_max = 600
            self.modele.monstre_points_de_mana_max = 1
            self.modele.monstre_liste_actions = {
                "Attaque Lourde": "Technique",
                "Lame Courageuse": "Technique", #gros degats
                "Crystal Elémentaire": "Technique",  # inflige lourd brule ou gele [x]
                "Remede Divin": "Technique", #soin
                "Combo Misérable": "Technique", #combo electrique , mais maudit [x]
                "Houken": "Sort", #draine vie
                "Sonata Sincère": "Sort", #soigne
                "Faisceau de la Mort Blanche": "Sort", #paralyse
                "Magie Abyssale": "Sort", #scelle sort et technique, draine 10% pm [x]
                "Eveil de Runes": "Sort", # differents effet selon la rune invoquée [x]
                "Dance Créatrice": "Sort", #drain
            }
            self.modele.monstre_recompense = {"Red coin": 1, "Méga Tirage": 1, "Vie max": 20, 
                                       "Mana max": 20, "Gold": 400 + gold_bonus_par_etage, "Endurance": 10}
        elif self.modele.monstre_nom == "Amalgame":
            self.modele.stigma_monstre_positif = "Bomberman"
            self.modele.stigma_monstre_negatif = "Inflammable"
            self.modele.stigma_monstre_bonus = "Hyallo-Réflection"
            self.modele.monstre_points_de_force = 30
            self.modele.monstre_points_de_intelligence = 30
            self.modele.monstre_points_de_resistance = 15
            self.modele.monstre_nombre_de_vies_supplementaire = 8
            self.modele.monstre_points_de_vie_max = 1
            self.modele.monstre_points_de_mana_max = 50
            self.modele.monstre_liste_actions = {
                "Attaque Lourde": "Technique",
                "Durcissement Calcaire": "Technique", # augmente def
                "Bombe Arcanique": "Sort",
                "Sonata": "Sort", #soin
                "Eveil de Runes": "Sort", # differents effet selon la rune invoquée [x]
                "Lame de Feu": "Technique", #brule
                "Lame de Gel": "Technique", #gele
                "Lame Pourpre": "Technique", #draine
                "Lame Courageuse": "Technique", #gros degats
                "Medecine de Guerre": "Technique", #soin
                "Lamentations": "Sort", #blesse et maudit plus mana [x]
                "Invoquation Canope": "Sort", #invoque vase canope, peut echouer [x]
                "Rejuvenation": "Sort", #gros soin
                "Jugement": "Sort", #degat = monstre tue
                "Combo Misérable": "Technique", #combo electrique , mais maudit [x]
                "Faisceau Statique": "Sort",  #paralyse
                "Thermosphère Brulante": "Sort", #brule
                "Pic Froid": "Sort", #gele
                "Création de Lapis": "Sort", #lapide
                "Explosion Renforcée": "Sort", #gros dégats
                "Dance Siphoneuse": "Sort", #saigne
                "Sonata Miséricordieuse": "Sort", #soigne
                "Magie Noire": "Sort", #blesse et hausse cout mana [x]
                "Faisceau de l'Eclair": "Sort",  #paralyse
                "Thermosphère de la Fournaise": "Sort", #brule
                "Pic Glacial": "Sort", #gele
                "Création Obsidienne": "Sort", #lapide
                "Explosion Maitrisée": "Sort", #gros dégats
                "Dance Parasite": "Sort", #saigne
                "Sonata Sincère": "Sort", #soigne
                "Magie Ténébreuse": "Sort", #empeche sort et technique [x]
                "Tournicoti": "Sort", #reprend vie
                "Tournicota": "Sort", #envoie boule a renvoyer ou esquiver [x]
                "Tournicotons": "Sort", #vague a esquiver [x]
                "Tournicotez": "Sort", #queston a repondre [x]
                "Attaque Titanesque": "Technique", #utilise orbe furie et attaque
                "Remede Divin": "Technique", #soin
                "Fleche Rouge": "Technique", #brule
                "Fleche Bleue": "Technique", #gele
                "Crystal Elémentaire": "Technique",  # inflige lourd brule ou gele [x]
                "Pendule Etrange": "Technique", #paralysie
                "Panacée Universelle": "Technique", #soigne toute les altérations d'état [x]
                "Missile Arcanique": "Sort", #utilise orbe folie et sort
                "Tome de Salomon": "Sort", #draine mp [x]
                "Houken": "Sort", #draine vie
                "Lame Ultime": "Technique", #gros degats
                "Bouclier Ultime": "Technique", #reprend beaucoup de vie
                "Laser Ultime": "Technique", #moyen degat et feu
                "Sort Ultime": "Sort", #gros degat, perd mana [x]
                "Ultime Ultime": "Sort", # impossible d'utiliser sorts et techniques [x]
                "Ultima": "Sort", #ramene la vie du joueur a 10% [x]
                "Ascension Runique": "Technique", #seulement la rune du drain de vie
                "Lame Vaillante": "Technique", #grosse attaque
                "Sables du Temps": "Technique", #paralysie 3 tour, monstre perd 5% vie [x]
                "Faisceau Foudroyant": "Sort", #paralyse
                "Thermosphère Magmatique": "Sort", #brule
                "Pic Polaire": "Sort", #gele
                "Création de la Montagne": "Sort", #lapide
                "Explosion Fatale": "Sort", #gros degats
                "Dance Destructrice": "Sort", #drain
                "Sonata Bienveillante": "Sort", #soigne
                "Dragon Ascendant": "Sort", #attaque par vague a esquiver [x]
                "Rituel Canope": "Sort", #seulement le canope de la paralysie 
                "Magie Abyssale": "Sort", #scelle sort et technique, draine 10% pm [x]
                "Faisceau de la Mort Blanche": "Sort", #paralyse
                "Thermosphère Solaire": "Sort", #brule
                "Pic Zéro": "Sort", #gele
                "Création Continentale": "Sort", #lapide
                "Explosion de la Comète": "Sort", #gros degats
                "Dance Créatrice": "Sort", #drain
                "Sonata Absolutrice": "Sort" #soin
            }
            self.modele.monstre_recompense = {"Red coin": 1, "Tirage": 1, "Gold": 500 + gold_bonus_par_etage, 
                                       "Defence": 2, "Attaque": 2, "Intelligence": 2, 
                                       "Taux coup critique": 2, "Degat coup critique": 2, 
                                       "Taux sort critique": 2, "Degat sort critique": 2, "Endurance": 10}
        elif self.modele.monstre_nom == "Coliseum":
            self.modele.stigma_monstre_positif = "Aucun"
            self.modele.stigma_monstre_negatif = "Aucun"
            self.modele.stigma_monstre_bonus = "Aucun"
            self.modele.monstre_points_de_force = 40
            self.modele.monstre_points_de_intelligence = 40
            self.modele.monstre_points_de_resistance = 10
            self.modele.monstre_nombre_de_vies_supplementaire = 1
            self.modele.monstre_points_de_vie_max = 700
            self.modele.monstre_points_de_mana_max = 100
            self.modele.monstre_liste_actions = {
                "Lame Ultime": "Technique", #gros degats
                "Bouclier Ultime": "Technique", #reprend beaucoup de vie
                "Laser Ultime": "Technique", #moyen degat et feu
                "Sort Ultime": "Sort", #gros degat, perd mana [x]
                "Ultime Ultime": "Sort", # impossible d'utiliser sor
            }
            self.modele.monstre_recompense = {"Red coin": 1, "Tirage": 1, "Gold": 99999, 
                                       "Attaque": 99999, "Intelligence": 99999}
        elif self.modele.monstre_nom == "Pierre de Désir":
            self.modele.stigma_monstre_positif = ""
            self.modele.stigma_monstre_negatif = ""
            self.modele.stigma_monstre_bonus = ""
            self.modele.monstre_points_de_force = 50
            self.modele.monstre_points_de_intelligence = 50
            self.modele.monstre_points_de_resistance = 20
            self.modele.monstre_nombre_de_vies_supplementaire = 2
            self.modele.monstre_points_de_vie_max = 1500
            self.modele.monstre_points_de_mana_max = 9999
            self.modele.monstre_liste_actions = {
                "Lame Ultime": "Technique", #gros degats
                "Bouclier Ultime": "Technique", #reprend beaucoup de vie
                "Laser Ultime": "Technique", #moyen degat et feu
                "Sort Ultime": "Sort", #gros degat, perd mana [x]
                "Ultime Ultime": "Sort", # impossible d'utiliser sor
            }
            self.modele.monstre_recompense = {"Red coin": 1, "Tirage": 1, "Gold": 99999, 
                                       "Attaque": 99999, "Intelligence": 99999, "Endurance": 99999}
        #Initilaise des bonus de vie/mana pour tester différentes combinaisons
        bonus_vie = 0
        bonus_mana = 0
        self.modele.monstre_points_de_vie_max += vie_bonus_par_etage + bonus_vie
        self.modele.monstre_points_de_vie = self.modele.monstre_points_de_vie_max
        self.modele.monstre_points_de_mana_max += bonus_mana
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
            nom_de_la_musique = "mimic"
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
        

    def AppliqueTank(self):
        degat = round(self.modele.monstre_points_de_vie_max * 0.15)
        self.modele.monstre_points_de_vie -= degat
        self.vue.AfficheTank(degat)

    def EffetStigmaFlemme(self):
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 7:
            self.modele.passe_son_tour = True
            self.modele.flemme = True

    def EffetStigmaFatigueChronique(self):
        nombre_aleatoire = random.randint(0, 100)

        chance_de_passer_tour = 0
        commentaire = "A cause de "
        if 1 <= self.modele.points_de_vie <= 15:
            commentaire += "votre vie très faible, "
            chance_de_passer_tour += 3
        elif 16 <= self.modele.points_de_vie <= 30:
            chance_de_passer_tour += 2
            commentaire += "votre vie faible, "
        elif 31 <= self.modele.points_de_vie <= 45:
            chance_de_passer_tour += 1
            commentaire += "votre vie moyenne, "
        if 1 <= self.modele.points_de_mana <= 15:
            chance_de_passer_tour += 3
            commentaire += "votre mana très faible, "
        elif 16 <= self.modele.points_de_mana <= 30:
            chance_de_passer_tour += 2
            commentaire += "votre mana faible, "
        elif 31 <= self.modele.points_de_mana <= 45:
            chance_de_passer_tour += 1
            commentaire += "votre mana moyen, "
        if 1 <= self.modele.points_de_endurance <= 15:
            chance_de_passer_tour += 3
            commentaire += "votre endurance très faible, "
        elif 16 <= self.modele.points_de_endurance <= 30:
            chance_de_passer_tour += 2
            commentaire += "votre endurance faible, "
        elif 31 <= self.modele.points_de_endurance <= 45:
            chance_de_passer_tour += 1
            commentaire += "votre endurance moyenne, "
        commentaire += " vous sentez une grande fatigue vous envahir..."
        if chance_de_passer_tour == 9 :
            chance_de_passer_tour = 10
            commentaire = "A cause de votre très faible vie, mana et endurance, vous sentez une grande fatigue vous envahir..."

        if nombre_aleatoire < chance_de_passer_tour:
            self.modele.passe_son_tour = True
            self.modele.fatigue_chronique = True
            self.vue.AfficheStigmaFatigueChronique(commentaire)

    def EffetStigmaAngeDechue(self):
        limite_de_pv = round(self.modele.points_de_vie_max * 0.10)
        if self.modele.points_de_vie < limite_de_pv:
            nombre_aleatoire = random.randint(0, 100)
            if nombre_aleatoire <= 25:
                self.modele.points_de_vie = -50
                self.vue.AfficheAngeDechue(limite_de_pv)

    def EffetStigmaBeniParLesFees(self):
        sante_recupere = round(self.modele.points_de_vie_max * 0.03)
        sante_recupere = self.SiZeroRameneAUn(sante_recupere)
        self.modele.points_de_vie += sante_recupere
        self.EquilibragePointsDeVieEtManaEtEndurance()
        self.vue.AfficheBeniParLesFees(sante_recupere)

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

    def EffetStigmaBergentruckung(self):
        element = "un coup de boule monstrueux."
        degat = round(self.modele.monstre_points_de_vie_max * 0.1)
        self.SiZeroRameneAUn(degat)
        self.modele.monstre_points_de_vie -= degat
        phrase = (
            f"Il va s'écraser à l'autre bout de la salle et perd {degat} points de vie !"
        )
        self.vue.AfficherAttaquePremierTour(element, phrase)

    def ChangeChargeMauvaisTachyon(self, action):
        if action in ["attaque" , "sort"]:
            self.modele.charge_mauvais_tachyon += 10
        elif action == "item" :
            self.modele.charge_mauvais_tachyon += 5
        elif action == "defense":
            self.modele.charge_mauvais_tachyon -= 5
        elif action == "passe tour" :
            self.modele.charge_mauvais_tachyon -= 10
        if self.modele.charge_mauvais_tachyon < 0:
            self.modele.charge_mauvais_tachyon = 0
        elif self.modele.charge_mauvais_tachyon >= 100:
            self.modele.charge_mauvais_tachyon = 0
            self.modele.points_de_vie -= 999
            self.vue.AfficheMauvaisTachyonExplose()

    def ChangeChargeBonTachyon(self, action):
        if action in ["attaque" , "sort"]:
            self.modele.charge_bon_tachyon += 3
        elif action == "tour":
            self.modele.charge_bon_tachyon += 5
        elif action == "item" :
            self.modele.charge_bon_tachyon += 2
        elif action == "defense":
            self.modele.charge_bon_tachyon += 1
        elif action == "passe tour" :
            self.modele.charge_bon_tachyon += 0
        if self.modele.charge_bon_tachyon >= 110:
            self.modele.charge_bon_tachyon = 0
            self.modele.beni_par_feu_sacre = True
            self.modele.beni_par_feu_sacre_nombre_tour += 6
            self.vue.AfficheBonTachyonExplose()

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

    def EffetStigmaToucherDeMidas(self):
        degat = round(self.modele.nombre_de_gold * 0.1)
        commentaire = "Ouch !"
        degat = self.EnleveVieAuJoueur(degat)
        if self.modele.points_de_vie < 0:
            commentaire = (
                "Vous sentez votre vie s'écouler par vos pores,"
                " et n'avez le temps de faire qu'une action avant"
                " qu'elle ne vous quitte définitivement."
            )
        self.vue.AfficheToucherDeMidas(degat, commentaire)

    def EffetStigmaSiphonDeMana(self):
        nombre_aleatoire = random.randint(0, 100)
        mana_siphone = round(self.modele.points_de_mana_max * 0.1)
        if self.modele.points_de_mana >= mana_siphone and nombre_aleatoire < 20:
            self.modele.points_de_mana -= mana_siphone
            self.modele.monstre_points_de_mana += mana_siphone
            self.EquilibragePointsDeVieEtManaEtEndurance()
            self.vue.AfficheSiphonDeMana(mana_siphone)

    def EffetStigmaFaveursExplosives(self):
        degat = round(self.modele.points_de_vie_max * 0.25)
        choix = 3
        while choix not in [1, 2]:
            try:
                choix = self.vue.GetFaveursExplosives(degat)
                clear_console()
                if choix == 1:
                    degat = self.EnleveVieAuJoueur(degat)
                    self.CheckePuisAppliqueTransmutation(degat)
                    commentaire = "Vous décollez les morceaux de rocher de votre peau et faites face a l'ennemi."
                    if self.modele.points_de_vie < 0:
                        commentaire = (
                            "Vous sentez votre vie s'écouler par vos pores,"
                            " et n'avez le temps de faire qu'une action "
                            "avant qu'elle ne vous quitte définitivement."
                        )
                    self.vue.AfficheFaveursExplosives(commentaire)
                    clear_console()
                else:
                    self.modele.InCombat = False
                    self.modele.type_de_derniere_action_utilisee = "Fuir"
                clear_console()
            except ValueError:
                clear_console()
        if self.modele.commentaire_transmutation_degat != "":
            self.vue.AfficheTransmutationDegat(self.modele.commentaire_transmutation_degat)

    def EffetStigmaBenedictionDivine(self):
        vie_reprise = round(self.modele.monstre_points_de_vie_max * 0.03)
        self.modele.monstre_points_de_vie += vie_reprise
        self.EquilibragePointsDeVieEtManaEtEndurance()
        self.vue.AfficheBenedictionDivine(vie_reprise)

    def EffetStigmaBomberman(self):
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 10:
            vie_perdue = round(self.modele.points_de_vie_max * 0.1)
            vie_perdue = self.EnleveVieAuJoueur(vie_perdue)
            self.CheckePuisAppliqueTransmutation(vie_perdue)
            self.EquilibragePointsDeVieEtManaEtEndurance()
            self.vue.AfficheBomberman(vie_perdue)
        if self.modele.commentaire_transmutation_degat != "":
            self.vue.AfficheTransmutationDegat(self.modele.commentaire_transmutation_degat)

    def EffetStigmaPlusDUnTour(self):
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 10:
            element_aleatoire = random.randint(1, 4)
            if element_aleatoire == 1:
                type_delement = "*Feu*"
                self.AppliqueEffetElementaireSurJoueur("feu", 2, 5)
                description_element = "Vous vous enflammez pendant 2 tours !"
            elif element_aleatoire == 2:
                type_delement = "*Glace*"
                self.AppliqueEffetElementaireSurJoueur("glace", 2)
                description_element = "Vous devenez gelé pendant 2 tours !"
            elif element_aleatoire == 3:
                type_delement = "*Foudre*"
                if self.modele.nombre_de_tours == 1:
                    nombre_tour = 1
                else:
                    nombre_tour = 2
                self.AppliqueEffetElementaireSurJoueur("foudre", nombre_tour)
                if self.modele.est_paralyse:
                    self.modele.passe_son_tour = True
                    description_element = "Vous devenez paralysé pendant 1 tour !"
                else:
                    description_element = "Vous résistez à la paralysie !"
            elif element_aleatoire == 4:
                type_delement = "*Sang*"
                saignee = round(self.modele.points_de_vie_max * 0.03)
                self.modele.monstre_points_de_vie += saignee
                self.EquilibragePointsDeVieEtManaEtEndurance()
                saignee = self.EnleveVieAuJoueur(saignee)
                description_element = (
                    f"Vous vous faites drainer {saignee} points de vie !"
                )
                if self.modele.points_de_vie < 0:
                    description_element += (
                        "\nVous sentez votre vie s'écouler par vos pores,"
                        " et n'avez le temps de faire qu'une action "
                        "avant qu'elle ne vous quitte définitivement."
                    )
            self.vue.AffichePlusDUnTour(type_delement, description_element)

    def EffetStigmaMegalovania(self):
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 5:
            vie_perdue = round(self.modele.monstre_points_de_vie_max * 0.1)
            self.modele.monstre_points_de_vie -= vie_perdue
            self.EquilibragePointDeVieMonstrePerduParStigma()
            self.vue.AfficheMegalovania(vie_perdue)

    def EffetStigmaHomoncule(self):
        vie_perdue = round(self.modele.monstre_points_de_vie_max * 0.03)
        self.modele.monstre_points_de_vie -= vie_perdue
        self.EquilibragePointDeVieMonstrePerduParStigma()
        self.vue.AfficheHomoncule(vie_perdue)

    def EquilibragePointDeVieMonstrePerduParStigma(self):
        if self.modele.monstre_points_de_vie < 1 and "Super Etoile" not in self.modele.monstre_tags:
            self.modele.monstre_points_de_vie = 1
            self.vue.AfficheMonstreSurvieStigma()

    def EffetStigmaPatchwork(self):
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 25:
            vie_perdue = round(self.modele.monstre_points_de_vie_max * 0.05)
            self.modele.monstre_points_de_vie -= vie_perdue
            self.EquilibragePointDeVieMonstrePerduParStigma()
            self.vue.AffichePatchwork(vie_perdue)

    def EffetStigmaArlequin(self):
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 10:
            element_aleatoire = random.randint(1, 4)
            if element_aleatoire == 1:
                type_delement = "*Feu*"
                self.modele.monstre_est_en_feu = True
                self.modele.monstre_est_en_feu_nombre_tour += 2
                description_element = "Il s'enflamme pendant 2 tours !"
            elif element_aleatoire == 2:
                type_delement = "*Glace*"
                self.modele.monstre_est_gele = True
                self.modele.monstre_est_gele_nombre_tour += 2
                description_element = "Il devient gelé pendant 2 tours !"
            elif element_aleatoire == 3:
                type_delement = "*Foudre*"
                self.modele.monstre_est_paralyse = True
                self.modele.monstre_est_paralyse_nombre_tour += 1
                description_element = "Il devient paralysé pendant 1 tours !"
            elif element_aleatoire == 4:
                type_delement = "*Sang*"
                saignee = round(self.modele.monstre_points_de_vie_max * 0.03)
                saignee = self.AppliqueLimitationSaignee(saignee)
                self.modele.points_de_vie += saignee
                self.EquilibragePointsDeVieEtManaEtEndurance()
                self.modele.monstre_points_de_vie -= saignee
                self.EquilibragePointDeVieMonstrePerduParStigma()
                description_element = f"Il se fait drainer {saignee} points de vie !"
            self.vue.AfficheArlequin(type_delement, description_element)

    def EffetStigmaMalJaune(self):
        self.modele.est_maudit_par_le_gold = True
        self.modele.est_maudit_par_le_gold_nombre_tour = 999
        self.vue.AfficheMalJaune()

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

    def IsMultipleOf(self, nombre_a_checker, multiple_actuel):
        if nombre_a_checker!=0 and ((nombre_a_checker % multiple_actuel) == 0):
            return True
        return False

    def GetMonsterChoice(self):
        # .items transforme le dictionnaire en une liste de plusieurs tuples
        # chaque tuples correspond a une paire clé/valeur
        # random.choice choisit un tuple aléatoire dans cette liste de tuples
        # la clé est affectée a la premiere variable (nom_action)
        # la valeur est affectée a la deuxieme variable (type_action)
        items_list = list(self.modele.monstre_liste_actions.items())
        nom_action, type_action = random.choice(items_list)
        return nom_action, type_action

    def RaisonDePasserSonTour(self):
        personnage = "Vous passez votre"
        iaido_effectue = False
        # a cause de l'attaque iaido
        if self.modele.en_plein_iaido:
            # iaido arrété car paralysie
            if self.modele.est_paralyse and not self.modele.flemme and not self.modele.fatigue_chronique:
                commentaire = "... et votre concentration pour le iaido est stoppée par la paralysie."
                self.modele.en_plein_iaido = False
                self.modele.en_plein_iaido_nombre_tour = 0
            # iaido arrété car flemme
            elif self.modele.flemme and not self.modele.est_paralyse:
                commentaire = "... et votre concentration pour le iaido est stoppée par votre flemme inhérente."
                self.modele.en_plein_iaido = False
                self.modele.en_plein_iaido_nombre_tour = 0
            # iaido arrété car fatigue
            elif self.modele.fatigue_chronique and not self.modele.est_paralyse:
                commentaire = "... et votre concentration pour le iaido est stoppée par votre fatigue chronique."
                self.modele.en_plein_iaido = False
                self.modele.en_plein_iaido_nombre_tour = 0
            # iaido arrété car paralysie + flemme
            elif self.modele.flemme and self.modele.est_paralyse:
                commentaire = "... et votre concentration pour le iaido est stoppée par un mélange de paralysie et de flemme."
                self.modele.en_plein_iaido = False
                self.modele.en_plein_iaido_nombre_tour = 0
            elif self.modele.fatigue_chronique and self.modele.est_paralyse:
                commentaire = "... et votre concentration pour le iaido est stoppée par un mélange de paralysie et de fatigue."
                self.modele.en_plein_iaido = False
                self.modele.en_plein_iaido_nombre_tour = 0
            elif (
                self.modele.stigma_monstre_positif == "Abomination"
                and self.modele.abomination_touche
            ):
                commentaire = "... et votre concentration pour le iaido est stoppée par l'horrible vision de l'abomination devant vous."
                self.modele.en_plein_iaido = False
                self.modele.en_plein_iaido_nombre_tour = 0
                self.modele.abomination_touche = False
            # iaido continue
            else:
                if self.modele.en_plein_iaido_nombre_tour == 2:
                    commentaire = (
                        "...et vous concentrez votre pouvoir dans votre lame..."
                    )
                elif self.modele.en_plein_iaido_nombre_tour == 1:
                    commentaire = "...et vous commencez a voir le chemin a parcourir entre les atomes."
                elif self.modele.en_plein_iaido_nombre_tour == 0:
                    self.modele.en_plein_iaido = False
                    iaido_effectue = True
        # a cause de la paralysie
        elif self.modele.est_paralyse:
            commentaire = "...mais vos muscles paralysés se détendent petit à petit."
        # a cause du stigma Abobination
        elif (
            self.modele.stigma_monstre_positif == "Abomination"
            and self.modele.abomination_touche
        ):
            commentaire = "...car la vision d'horreur de ce monstre abominable vous glace le sang."
            self.modele.abomination_touche = False
        # a cause d'un stigma
        else:
            if self.modele.stigma_joueur_negatif == "Trouble Obsessionnel Compulsif":
                commentaire = "...pour aller ramasser les restes d'items et autre déchets par terre."
            elif self.modele.stigma_joueur_negatif == "Fatigue Chronique":
                commentaire = "...terrassé par votre fatigue."
            else:
                commentaire = "...car vous avez tout simplement la flemme."
        if iaido_effectue:
            self.Iaido()
        else:
            self.vue.AfficheRaisonDePasserTour(personnage, commentaire)
        if not self.modele.en_plein_iaido:
            self.modele.passe_son_tour = False

    def RaisonDePasserTourMonstre(self):
        personnage = "L'ennemi passe son"
        # a cause de la resurection
        if self.modele.commentaire_de_resurection_de_monstre != "Aucun":
            commentaire = self.modele.commentaire_de_resurection_de_monstre
        # a cause de la paralysie
        elif self.modele.monstre_est_paralyse:
            commentaire = "...mais ses muscles paralysés se détendent petit à petit."
        # a cause du stigma musculeux
        elif (
            self.modele.stigma_joueur_bonus == "Musculeux"
            and self.modele.musculeux_touche
        ):
            commentaire = (
                "...trop occupé a baver devant votre physique absolument MUSCULEUX."
            )
            self.modele.musculeux_touche = False
        # a cause du stigma aveuglé
        elif (
            self.modele.stigma_monstre_negatif == "Aveuglé"
            and self.modele.aveugle_touche
        ):
            commentaire = (
                "...et l'utilise plutot pour vous prendre 5 gold par télékinésie."
            )
            self.modele.aveugle_touche = False
            self.modele.nombre_de_gold -= 5
            self.EquilibrageGold()
        # a cause du stigma gluantin
        elif self.modele.stigma_monstre_negatif == "Gluantin" and not self.modele.monstre_en_etat_de_choc :
            commentaire = "...et secoue son corps gluant comme un flanc au caramel. Tout simplement hilarant !"
        # a cause du stigma corps massif
        elif self.modele.stigma_monstre_negatif == "Corps Massif" and not self.modele.monstre_en_etat_de_choc:
            commentaire = "...et en profite pour reposer son corps aussi titanesque que difficile a bouger."
        # a cause du stigma copycat
        elif self.modele.stigma_monstre_negatif == "Copycat" and not self.modele.monstre_en_etat_de_choc :
            commentaire = (
                "...et prend une pose similaire a la votre. Par moquerie ou fair-play ?"
            )
        # a cause du stigma hématophobe
        elif self.modele.stigma_monstre_negatif == "Hématophobe" and not self.modele.monstre_en_etat_de_choc:
            commentaire = (
                "...absolument dégouté par la vision du sang que vous lui avez offerte."
            )
        # a cause de letat de choc
        elif self.modele.monstre_en_etat_de_choc:
            degat = 15
            if "Orbe de Disruption" in self.modele.liste_dartefacts_optionels:
                degat += 10
            commentaire = (
                f"...et récupère son mana.\nIl perd {degat} points de vie a cause de son réservoir de mana troué."
            )
            self.modele.monstre_en_etat_de_choc_nombre_tour -= 1
            if self.modele.monstre_en_etat_de_choc_nombre_tour == 0:
                commentaire = (
                    "...et fini enfin de récupérer son mana !"
                )
                self.modele.monstre_points_de_mana = self.modele.monstre_points_de_mana_max
                self.modele.monstre_en_etat_de_choc = False
            else:
                self.modele.monstre_points_de_vie -= degat
            if "Lame Spectrale" in self.modele.liste_dartefacts_optionels:
                mana_recupere = round(self.modele.points_de_mana_max * 0.1)
                self.RecouvrementDeMana(mana_recupere)
                self.EquilibragePointsDeVieEtManaEtEndurance()
                commentaire += (
                f"\nDe plus, votre Lame Spectrale vous rapporte {mana_recupere} points de mana !"
            )
        elif self.modele.monstre_est_service:
            commentaire = (
                f"...pour servir les clients fantomatiques."
            )
        self.vue.AfficheRaisonDePasserTour(personnage, commentaire)
        self.modele.monstre_passe_son_tour = False

    def EquilibrageGold(self):
        if self.modele.nombre_de_gold < 0:
            self.modele.nombre_de_gold = 0

    def AppliqueFeu(self):
        if self.modele.est_en_feu:
            personnage = "Vous brulez !"
            # Trouver un moyen de calculer les degats de feu
            degat = round(
                ((self.modele.est_en_feu_degat) / 100) * self.modele.points_de_vie_max
            )
            degat = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat)
            if degat <= 1:
                degat = 2
            degat = self.EnleveVieAuJoueur(degat)
            commentaire = f"Vous perdez {degat} points de vie."
            if self.modele.points_de_vie < 0:
                commentaire += (
                    "\n Vous sentez votre vitalitée vous"
                    " quitter. Vous n'avez le temps "
                    "d'effectuer qu'une seule action"
                    " avant votre mort définitive."
                )
            self.vue.AfficheFeuEtPoison(personnage, commentaire)
        if self.modele.monstre_est_en_feu:
            personnage = "L'ennemi brule !"
            # Trouver un moyen de calculer les degats de feu
            bonus = round((self.modele.DEGATBONUSFEU / 100) * self.modele.monstre_est_en_feu_degat)
            degat = round(
                ((self.modele.monstre_est_en_feu_degat + bonus) / 100)
                * self.modele.monstre_points_de_vie_max
            )
            degat = self.SiZeroRameneAUn(degat)
            self.modele.monstre_points_de_vie -= degat
            commentaire = f"Il perd {degat} points de vie !"
            if self.modele.choc_thermique:
                self.modele.monstre_points_de_vie -= degat
                commentaire = f"A cause du choc thermique entre sa gelure et sa brulure, il perd {degat * 2} points de vie !"
            if self.modele.stigma_monstre_positif == "Coeur Immolé" and not self.modele.monstre_en_etat_de_choc and (self.modele.monstre_points_de_mana + round(degat * 0.5)) <= self.modele.monstre_points_de_mana_max :
                mana_recup = round(degat * 0.5)
                self.modele.monstre_points_de_mana += mana_recup
                commentaire += f"Le coeur de l'ennemi à déja souffert par le feu, et sa présence lui permet de récupérer des points de mana."
            self.vue.AfficheFeuEtPoison(personnage, commentaire)

    def AppliqueFeuElectrique(self):
        personnage = "L'ennemi souffre du feu électrique !"
        # Trouver un moyen de calculer les degats de feu
        degat = self.modele.luciole_degat
        self.modele.monstre_points_de_vie -= degat
        commentaire = f"Il perd {degat} points de vie !"
        self.vue.AfficheFeuEtPoison(personnage, commentaire)

    def AppliquePoison(self):
        if self.modele.est_enpoisonne:
            personnage = "Le poison se répand dans votre corps. Vos entrailles vous font un mal de chien !"
            # Trouver un moyen de calculer les degats de poison
            degat = round(
                (self.modele.est_enpoisonne_degat / 100) * self.modele.points_de_vie_max
            )
            degat = self.EnleveVieAuJoueur(degat)
            commentaire = f"Vous perdez {degat} points de vie."
            if self.modele.points_de_vie < 0:
                commentaire += (
                    "\n Vous sentez votre vitalitée vous"
                    " quitter. Vous n'avez le temps "
                    "d'effectuer qu'une seule action"
                    " avant votre mort définitive."
                )
            self.vue.AfficheFeuEtPoison(personnage, commentaire)
        if self.modele.monstre_est_empoisonne:
            personnage = "L'ennemi ressent les effet du poison et grimace !"
            # Trouver un moyen de calculer les degats de poison
            degat = round(
                (self.modele.monstre_est_empoisonne_degat / 100)
                * self.modele.monstre_points_de_vie_max
            )
            degat = self.SiZeroRameneAUn(degat)
            self.modele.monstre_points_de_vie -= degat
            commentaire = f"Il perd {degat} points de vie !"
            self.vue.AfficheFeuEtPoison(personnage, commentaire)

    def CheckOnlyMonsterHp(self):
        if self.modele.monstre_points_de_vie < 1:
            if self.modele.monstre_nombre_de_vies_supplementaire > 0:
                self.modele.monstre_nombre_de_vies_supplementaire -= 1
                self.modele.monstre_points_de_vie = (
                    0.5 * self.modele.monstre_points_de_vie_max
                )
                self.modele.monstre_points_de_vie = round(
                    self.modele.monstre_points_de_vie
                )
            else:
                return False
        return True

    def AppliqueEffetJindagee(self):
        commentaire = "Les effets combinés des plantes jindagee soignent votre corps."
        type_de_soin = "vie"
        soin_de_la_feuille = 0
        soin_du_fruit = 0
        if self.modele.utilise_feuille_jindagee:
            soin_de_la_feuille = 5 + round(self.modele.points_de_vie_max * 0.05)
            if soin_de_la_feuille < 8:
                soin_de_la_feuille = 8
        if self.modele.utilise_fruit_jindagee:
            soin_du_fruit = 10 + round(self.modele.points_de_vie_max * 0.1)
            if soin_du_fruit < 13:
                soin_du_fruit = 13
        vie_soignee = soin_de_la_feuille + soin_du_fruit
        vie_soignee = self.AppliqueSupportBonusItem(vie_soignee, "vie")
        self.modele.points_de_vie += vie_soignee
        self.EquilibragePointsDeVieEtManaEtEndurance()
        self.vue.AfficheAatmaEtJindagee(commentaire, vie_soignee, type_de_soin)

    def AppliqueEffetAatma(self):
        commentaire = "Les effets combinés des plantes aatma soignent votre esprit."
        type_de_soin = "mana"
        soin_de_la_feuille = 0
        soin_du_fruit = 0
        if self.modele.utilise_feuille_aatma:
            soin_de_la_feuille = 5 + round(self.modele.points_de_mana_max * 0.05)
            if soin_de_la_feuille < 8:
                soin_de_la_feuille = 8
        if self.modele.utilise_fruit_aatma:
            soin_du_fruit = 10 + round(self.modele.points_de_mana_max * 0.1)
            if soin_du_fruit < 13:
                soin_du_fruit = 13
        mana_soigne = soin_de_la_feuille + soin_du_fruit
        mana_soigne = self.AppliqueSupportBonusItem(mana_soigne, "mana")
        self.RecouvrementDeMana(mana_soigne)
        self.EquilibragePointsDeVieEtManaEtEndurance()
        self.vue.AfficheAatmaEtJindagee(commentaire, mana_soigne, type_de_soin)

    def AppliqueRegenerationMonstre(self):
        # trouver un moyen de calculer le pourcentage de regeneration
        pourcentage_soin = self.modele.monstre_est_regeneration_soin
        soin = round(self.modele.monstre_points_de_vie_max * (pourcentage_soin / 100))
        self.modele.monstre_points_de_vie += soin
        self.EquilibragePointsDeVieEtManaEtEndurance()
        self.vue.AfficheRegenerationMonstre(soin)

    def AppliqueEtMetAJourAlterationEtat(self):
        if self.modele.bon_tachyon:
            self.ChangeChargeBonTachyon("tour")
        commentaire = ""
        # Joueur
        # sous la rafale
        if self.modele.utilise_rafale:
            self.modele.rafale_nombre_tours -= 1
            if self.modele.rafale_nombre_tours <= 0:
                self.modele.utilise_rafale = False
                commentaire += "\nLes vents de la rafale retournent dans leur monde !"
        # sous la posture de la montagne
        if self.modele.utilise_posture_de_la_montagne:
            self.modele.posture_de_la_montagne_tour -= 1
            if self.modele.posture_de_la_montagne_tour <= 0:
                self.modele.utilise_posture_de_la_montagne = False
                self.modele.gain_de_defence = 0
                commentaire += "\nLa posture de la montagne ne fait plus effet !"
        # sous la position du massif
        if self.modele.utilise_le_massif:
            self.modele.utilise_le_massif == False
            self.modele.limite_degat = 0
            commentaire += "\nLa position du massif ne fait plus effet !"
        # sous le bluff
        if self.modele.utilise_le_bluff:
            self.modele.utilise_le_bluff = False
            nombre_tour = 2
            self.AppliqueEffetElementaireSurJoueur("foudre", nombre_tour)
            if self.modele.est_paralyse:
                commentaire += "\nPersonne ne vous a fait de dégat !\nVos muscles tendus et prêt a recevoir un coup deviennent paralysé !"
            else:
                commentaire += "\nPersonne ne vous a fait de dégat !\nVos muscles tendus et prêt a recevoir un coup commmencent a se paralyser... mais vous y résistez !"
        # sous l'adrenaline
        if self.modele.utilise_pousse_adrenaline:
            self.modele.pousse_adrenaline_tour -= 1
            if self.modele.pousse_adrenaline_tour <= 0:
                self.modele.utilise_pousse_adrenaline = False
                commentaire += ("\nL'adrenaline ne fait plus effet !\n De plus, retenir sa"
                                " respiration pendant autant de temps vous fait tourner"
                                " la tete et vous etes trop occupé a reprendre votre "
                                "souffle pour parler !")
                self.modele.est_maudit_par_les_sorts = True
                self.modele.est_maudit_par_les_sorts_nombre_tour += 4
                self.modele.est_maudit_par_les_techniques = True
                self.modele.est_maudit_par_les_techniques_nombre_tour += 4
        # sous le mirroir d'eau
        if self.modele.utilise_mirroir_eau:
            self.modele.mirroir_eau_nombre_tours -= 1
            if self.modele.mirroir_eau_nombre_tours <= 0:
                self.modele.utilise_mirroir_eau = False
                commentaire += "\nLe mirroir d'eau se disperse dans les airs !"
        # sous la brume de sang
        if self.modele.utilise_brume_sang:
            self.modele.brume_sang_nombre_tours -= 1
            if self.modele.brume_sang_nombre_tours == 0:
                self.modele.utilise_brume_sang = False
                commentaire += "\nLa brume de sang se disperse dans les airs !"
        # sous le feu sacre
        if self.modele.beni_par_feu_sacre:
            self.modele.beni_par_feu_sacre_nombre_tour -= 1
            if self.modele.beni_par_feu_sacre_nombre_tour == 0:
                self.modele.beni_par_feu_sacre = False
                commentaire += "\nLa bénédiction du feu sacré s'estompe !"
        # sous la transformoation en miss hyde
        if self.modele.miss_hyde_transformation:
            self.modele.miss_hyde_transformation_nombre_tour -= 1
            if self.modele.miss_hyde_transformation_nombre_tour == 0:
                self.modele.miss_hyde_transformation = False
                commentaire += "\nLa malédiction de Hyde s'estompe !"
        # sous la folie
        if self.modele.utilise_orbe_de_folie:
            self.modele.utilise_orbe_de_folie_nombre_tour -= 1
            if self.modele.utilise_orbe_de_folie_nombre_tour == 0:
                self.modele.utilise_orbe_de_folie = False
                commentaire += "\nLa folie dans votre esprit s'estompe !"
        # sous la furie
        if self.modele.utilise_orbe_de_furie:
            self.modele.utilise_orbe_de_furie_nombre_tour -= 1
            if self.modele.utilise_orbe_de_furie_nombre_tour == 0:
                self.modele.utilise_orbe_de_furie = False
                commentaire += "\nLa furie dans votre esprit s'estompe !"
        # endurance ne remonte pas
        if self.modele.est_maudit_par_endurance:
            self.modele.est_maudit_par_endurance_nombre_tour -= 1
            if self.modele.est_maudit_par_endurance_nombre_tour == 0:
                self.modele.est_maudit_par_endurance = False
                commentaire += "\nVous pouvez regagner de l'endurance !"
        # attaque coute de la vie
        if self.modele.est_maudit_par_la_vie:
            self.modele.est_maudit_par_la_vie_nombre_tour -= 1
            if self.modele.est_maudit_par_la_vie_nombre_tour == 0:
                self.modele.est_maudit_par_la_vie = False
                commentaire += "\nVos attaques ne vous coutent plus de points de vie !"
        # sorts et attaques coutent gold
        if self.modele.est_maudit_par_le_gold:
            self.modele.est_maudit_par_le_gold_nombre_tour -= 1
            if self.modele.est_maudit_par_le_gold_nombre_tour == 0:
                self.modele.est_maudit_par_le_gold = False
                commentaire += "\nVos actions ne vous coutent plus de golds !"
        # sorts coutent plus de mana
        if self.modele.est_maudit_par_le_mana:
            self.modele.est_maudit_par_le_mana_nombre_tour -= 1
            if self.modele.est_maudit_par_le_mana_nombre_tour == 0:
                self.modele.est_maudit_par_le_mana = False
                commentaire += (
                    "\nLe cout de vos sorts en points de mana revient a la normale !"
                )
        # gele, prend 2x + de degats
        if self.modele.est_gele:
            self.modele.est_gele_nombre_tour -= 1
            if self.modele.est_gele_nombre_tour == 0:
                self.modele.est_gele = False
                commentaire += "\nVous n'êtes plus gelé !"
        # domovoi redonne vie
        if self.modele.retour_domovoi == self.modele.nombre_de_tours:
            self.modele.vie_domovoi = 2
            commentaire += "\nLe Domovoï sort de derriere son four et retourne avec son maître !"
        # domovoi redonne vie
        if self.modele.retour_kikimora == self.modele.nombre_de_tours:
            self.modele.vie_kikimora = 2
            commentaire += "\nLa Kikimora sort de derriere son four et retourne avec son maître !"
        # en feu, dégats sur le temps
        if self.modele.est_en_feu:
            self.AppliqueFeu()
            self.modele.est_en_feu_nombre_tour -= 1
            if self.modele.pyrophile:
                self.AppliqueTalentPyrophile()
            if self.modele.est_en_feu_nombre_tour == 0:
                self.modele.est_en_feu = False
                self.modele.est_en_feu_degat = 0
                commentaire += "\nVous n'êtes plus en feu !"
                if "Pin's Extincteur" in self.modele.liste_dartefacts_optionels:
                    commentaire += "\nVotre Pin's se met à vibrer. Vous reprenez 10 pv et 10 pm !"
                    self.modele.points_de_vie += 10
                    self.modele.points_de_mana += 10
                    self.EquilibragePointsDeVieEtManaEtEndurance()
        # paralysé, passe son tour
        if self.modele.est_paralyse:
            self.modele.est_paralyse_nombre_tour -= 1
            self.modele.passe_son_tour = True
            if self.modele.est_paralyse_nombre_tour == 0:
                self.modele.est_paralyse = False
                self.modele.passe_son_tour = False
                commentaire += "\nVous n'êtes plus paralysé !"
        # cuisson cuisine
        if len(self.modele.liste_cuisson) != 0 :
            for ingredient in self.modele.liste_cuisson:
                if self.modele.liste_cuisson[ingredient] == 0:
                    pass
                else:
                    self.modele.liste_cuisson[ingredient] -= 1
        # plus de métamorphose
        if self.modele.metamorphose :
            self.modele.metamorphose_nombre_tour -= 1
            if self.modele.metamorphose_nombre_tour == 0:
                commentaire += "\nLa métamorphose ne fait plus effet !"
                self.modele.metamorphose = False
        # plus d'utilisation de techniques
        if self.modele.est_maudit_par_les_techniques:
            self.modele.est_maudit_par_les_techniques_nombre_tour -= 1
            if self.modele.est_maudit_par_les_techniques_nombre_tour == 0:
                self.modele.est_maudit_par_les_techniques = False
                commentaire += "\nVous pouvez de nouveau utiliser vos techniques !"
        # plus d'utilisation de sorts
        if self.modele.est_maudit_par_les_sorts:
            self.modele.est_maudit_par_les_sorts_nombre_tour -= 1
            if self.modele.est_maudit_par_les_sorts_nombre_tour == 0:
                self.modele.est_maudit_par_les_sorts = False
                commentaire += "\nVous pouvez de nouveau utiliser vos sorts !"
        # plus d'utilisation d'item
        if self.modele.est_maudit_par_les_items:
            self.modele.est_maudit_par_les_items_nombre_tour -= 1
            if "Bague de l'Âne" in self.modele.liste_dartefacts_optionels:
                self.modele.est_maudit_par_les_items_nombre_tour = 0
            if self.modele.est_maudit_par_les_items_nombre_tour == 0:
                self.modele.est_maudit_par_les_items = False
                commentaire += "\nVous pouvez de nouveau utiliser vos item !"
        # empoisonné, gros dégats sur peu de temps
        if self.modele.est_enpoisonne:
            self.AppliquePoison()
            self.modele.est_enpoisonne_nombre_tour -= 1
            if self.modele.est_enpoisonne_nombre_tour == 0:
                self.modele.est_enpoisonne = False
                commentaire += "\nVous n'êtes plus empoisonné !"
        # utilise l'hydromel
        if self.modele.utilise_hydromel:
            self.modele.utilise_hydromel_nombre_tour -= 1
            if self.modele.utilise_hydromel_nombre_tour == 0:
                self.modele.utilise_hydromel = False
                commentaire += "\nL'hydromel ne fait plus effet !"
        # ramasse déchet
        if self.modele.tour_passe_car_ramasse_item != 0:
            self.modele.tour_passe_car_ramasse_item -= 1            
            if self.modele.tour_passe_car_ramasse_item == 0:
                commentaire += "\nVous avez fini de nettoyer le sol !"
        # utilise l'ambroisie
        if self.modele.utilise_ambroisie:
            self.modele.utilise_ambroisie_nombre_tour -= 1
            if self.modele.utilise_ambroisie_nombre_tour == 0:
                self.modele.utilise_ambroisie = False
                commentaire += "\nL'ambroisie ne fait plus effet !"
        # utilise feuille/fruit jindagee
        # Update le nombre de tour
        if self.modele.utilise_feuille_jindagee:
            self.modele.utilise_feuille_jindagee_nombre_tour -= 1
        if self.modele.utilise_fruit_jindagee:
            self.modele.utilise_fruit_jindagee_nombre_tour -= 1
        # Applique l'effet
        if self.modele.utilise_feuille_jindagee or self.modele.utilise_fruit_jindagee:
            self.AppliqueEffetJindagee()
            # Arrete l'effet si le nombre de tour est égal a 0
            if (
                self.modele.utilise_feuille_jindagee
                and self.modele.utilise_feuille_jindagee_nombre_tour == 0
            ):
                self.modele.utilise_feuille_jindagee = False
                commentaire += "\nLes feuilles jindagee ne font plus effet !"
            if (
                self.modele.utilise_fruit_jindagee
                and self.modele.utilise_fruit_jindagee_nombre_tour == 0
            ):
                self.modele.utilise_fruit_jindagee = False
                commentaire += "\nLes fruits jindagee ne font plus effet !"
        # utilise feuille aatma
        # Update le nombre de tour
        if self.modele.utilise_feuille_aatma:
            self.modele.utilise_feuille_aatma_nombre_tour -= 1
        if self.modele.utilise_fruit_aatma:
            self.modele.utilise_fruit_aatma_nombre_tour -= 1
        # Applique l'effet
        if self.modele.utilise_feuille_aatma or self.modele.utilise_fruit_aatma:
            self.AppliqueEffetAatma()
            # Arrete l'effet si le nombre de tour est égal a 0
            if (
                self.modele.utilise_feuille_aatma
                and self.modele.utilise_feuille_aatma_nombre_tour == 0
            ):
                self.modele.utilise_feuille_aatma = False
                commentaire += "\nLes feuilles aatma ne font plus effet !"
            if (
                self.modele.utilise_fruit_aatma
                and self.modele.utilise_fruit_aatma_nombre_tour == 0
            ):
                self.modele.utilise_fruit_aatma = False
                commentaire += "\nLes fruits aatma ne font plus effet !"
        # diminue le tour du iaido de 1
        if self.modele.en_plein_iaido:
            self.modele.en_plein_iaido_nombre_tour -= 1
        # rend des pm
        if self.modele.maitre_du_mana:
            self.AppliqueTalentMaitreDuMana()
        # rend de la vie
        if self.modele.rejuvenation:
            self.AppliqueTalentRejuvenation()
        # arrete de faire passer son tour au joueur
        if self.modele.passe_son_tour and not self.modele.est_paralyse and not self.modele.en_plein_iaido and not self.modele.flemme and not self.modele.fatigue_chronique and self.modele.tour_passe_car_ramasse_item == 0:
            self.modele.passe_son_tour = False
            self.modele.flemme = False
            self.modele.fatigue_chronique = False

        # Monstres
        # en fuite, fuit le combat
        if "En Fuite" in self.modele.monstre_tags:
            self.modele.type_de_derniere_action_utilisee == "Fuir"
            self.modele.InCombat = False
        # gele, monstre prend 2x + de degats
        if self.modele.monstre_est_gele:
            if ("Voluntad Hielo") in self.modele.monstre_tags:
                commentaire += f"\nVoluntad Hielo, l'esprit de glace, absorbe le gel de {self.modele.monstre_nom} !"
                self.modele.monstre_est_gele_nombre_tour = 0
                self.modele.monstre_est_gele = False
            else:
                self.modele.monstre_est_gele_nombre_tour -= 1
                if self.modele.monstre_est_gele_nombre_tour == 0:
                    self.modele.monstre_est_gele = False
                    commentaire += f"\n{self.modele.monstre_nom} n'est plus gelé !"
                    if self.modele.eclats_de_glace:
                        self.AppliqueTalentEclatDeGlace()
                    if self.modele.cycle_glaciaire:
                        self.AppliqueTalentCycleGlaciaire()
        # en feu, monstre perd des pv par tour
        if self.modele.monstre_est_en_feu:
            if ("Voluntad Káak") in self.modele.monstre_tags:
                commentaire += f"\nVoluntad Káak, l'esprit de feu, absorbe les brulures de {self.modele.monstre_nom} !"
                self.modele.monstre_est_en_feu_nombre_tour = 0
                self.modele.monstre_est_en_feu = False
            else:
                if not self.modele.est_en_feu:  # sinon le feu est appliqué deux fois.
                    self.AppliqueFeu()
                self.modele.monstre_est_en_feu_nombre_tour -= 1
                if self.modele.pyrosorcier:
                    self.AppliqueTalentPyrosorcier()
                if self.modele.pyromage:
                    self.AppliqueTalentPyromage()
                if self.modele.monstre_est_en_feu_nombre_tour == 0:
                    self.modele.monstre_est_en_feu = False
                    self.modele.monstre_est_en_feu_degat = 0
                    commentaire += self.AppliqueTalentBougieMagique()
        # en feu electrique, dégats sur le temps
        if self.modele.luciole_etat:
            self.AppliqueFeuElectrique()
            self.modele.luciole_tour -= 1
            if self.modele.luciole_tour == 0:
                self.modele.luciole_etat = False
                commentaire += f"\nLe feu électrique s'éteint !"
        # paralysie, monstre passe son tour
        if self.modele.monstre_est_paralyse:
            if ("Voluntad Le Rayo") in self.modele.monstre_tags:
                commentaire += f"\nVoluntad Le Rayo, l'esprit de foudre, absorbe la paralysie de {self.modele.monstre_nom} !"
                self.modele.monstre_est_paralyse_nombre_tour = 0
                self.modele.monstre_est_paralyse = False
            else:
                self.modele.monstre_passe_son_tour = True
                self.modele.monstre_est_paralyse_nombre_tour -= 1
                if self.modele.monstre_est_paralyse_nombre_tour == 0:
                    self.modele.monstre_est_paralyse = False
                    self.modele.monstre_passe_son_tour = False
                    if self.modele.luciole:
                        self.AppliqueTalentLuciole()
                    commentaire += f"\n{self.modele.monstre_nom} n'est plus paralysé !"
                else:
                    if self.modele.anti_neurotransmitteurs:
                        self.AppliqueTalentAntiNeurotransmetteur()
        # vulnerable, monstre suceptible elements
        if self.modele.monstre_est_vulnerable:
            self.modele.monstre_est_vulnerable_nombre_tour -= 1
            if self.modele.monstre_est_vulnerable_nombre_tour == 0:
                self.modele.monstre_est_vulnerable = False
                commentaire += f"\n{self.modele.monstre_nom} n'est plus vulnérable !"
        # poison, gros degat peu de tours
        if self.modele.monstre_est_empoisonne:
            self.AppliquePoison()
            self.modele.monstre_est_empoisonne_nombre_tour -= 1
            if self.modele.monstre_est_empoisonne_nombre_tour == 0:
                self.modele.monstre_est_empoisonne = False
                commentaire += f"\n{self.modele.monstre_nom} n'est plus empoisonné !"
        # maudit, -2pm par tours.
        if self.modele.monstre_est_maudit:
            self.modele.monstre_points_de_mana -= 2
            if self.modele.monstre_points_de_mana < 0:
                self.modele.monstre_points_de_mana = 0
            self.modele.monstre_est_maudit_nombre_tour -= 1
            if self.modele.monstre_est_maudit_nombre_tour == 0:
                self.modele.monstre_est_maudit = False
                commentaire += f"\n{self.modele.monstre_nom} n'est plus maudit !"
        # envol, 30% chance rater attaque/sorts
        if self.modele.monstre_est_envol:
            self.modele.monstre_est_envol_nombre_tour -= 1
            if self.modele.monstre_est_envol_nombre_tour == 0:
                self.modele.monstre_est_envol = False
                commentaire += f"\n{self.modele.monstre_nom} se pose sur le sol !"
        # arrete le gain de defence du monstre
        if self.modele.monstre_gain_de_defence:
            self.modele.monstre_gain_de_defence_nombre_tour -= 1
            if self.modele.monstre_gain_de_defence_nombre_tour == 0:
                self.modele.monstre_gain_de_defence = False
                self.modele.monstre_gain_de_defence_nombre = 0
                commentaire += f"\nLe durcissement de {self.modele.monstre_nom} n'a plus effet !"
        # regen, reprend vie par tour
        if self.modele.monstre_est_regeneration:
            self.AppliqueRegenerationMonstre()
            self.modele.monstre_est_regeneration_nombre_tour -= 1
            if self.modele.monstre_est_regeneration_nombre_tour == 0:
                self.modele.monstre_est_regeneration = False
                commentaire += f"\n{self.modele.monstre_nom} ne se regénère plus !"
        # applique la benediction du mana
        if self.modele.benediction_du_mana:
            self.AppliqueBenedictionMana()
        # enleve la defence
        self.modele.se_defend = False
        # arrete de faire passer son tour a l'ennemi
        if self.modele.monstre_passe_son_tour and not self.modele.monstre_est_paralyse:
            self.modele.monstre_passe_son_tour = False
        # dé-sacrifie L'ennemi
        if self.modele.sacrifice_actif:
            self.modele.sacrifice_actif = False
            commentaire += f"\nLa marque sacrificielle sur {self.modele.monstre_nom} s'efface !"
        #continue de faire passer son tour a l'ennemi si il est en etat de choc
        if self.modele.monstre_en_etat_de_choc == True:
            self.modele.monstre_passe_son_tour = True
        #continue le service
        if self.modele.monstre_est_service:
            self.modele.monstre_passe_son_tour = True
            self.modele.monstre_est_service_nombre_tour -= 1
            if self.modele.monstre_est_service_nombre_tour == 0:
                commentaire += f"\nL'ennemi finit son service et reprend le combat !"
                self.modele.monstre_est_service = False
                self.modele.monstre_passe_son_tour = False

        if commentaire != "":
            self.vue.AfficheFinAlterationEtat(commentaire)
        # met en place les sables du temps
        if self.modele.nombre_de_tours > 2:
            self.modele.vie_du_monstre_pour_sables_du_temps_a_utiliser = self.modele.vie_du_monstre_pour_sables_du_temps_tour_avant
        if self.modele.nombre_de_tours > 1:
            self.modele.vie_du_monstre_pour_sables_du_temps_tour_avant = self.modele.vie_du_monstre_pour_sables_du_temps_actuel
        self.modele.vie_du_monstre_pour_sables_du_temps_actuel = self.modele.monstre_points_de_vie
        if self.modele.vie_du_monstre_pour_sables_du_temps_actuel < 0:
            self.modele.vie_du_monstre_pour_sables_du_temps_actuel = 5
        if self.modele.vie_du_monstre_pour_sables_du_temps_tour_avant < 0:
            self.modele.vie_du_monstre_pour_sables_du_temps_tour_avant = 5
        if self.modele.vie_du_monstre_pour_sables_du_temps_a_utiliser < 0:
            self.modele.vie_du_monstre_pour_sables_du_temps_a_utiliser = 5
        self.modele.commentaire_de_resurection_de_monstre = "Aucun"
        

    def CheckForGameOver(self):
        if self.modele.points_de_vie <= 0:
            musique1 = self.modele.CHEMINABSOLUMUSIQUE + "death"
            self.vue.ShowGameOverScreen(musique1)
            self.Player.player_tags.append("KIA")

    def MontreFuiteOuRecompense(self):
        #enleve les bonus mutagene
        self.modele.points_de_vie_max -= self.modele.gain_vie_mutagene
        self.modele.points_de_mana_max -= self.modele.gain_mana_mutagene
        self.modele.points_de_vie_max += self.modele.perd_vie_mutagene
        self.modele.points_de_mana_max += self.modele.perd_mana_mutagene
        #met a jour les caracteristiques du joueur
        if "Domovoï" in self.modele.monstre_tags:
            self.modele.sorts.remove("Faire fuir le Domovoï")
        if "Kikimora" in self.modele.monstre_tags:
            self.modele.sorts.remove("Faire fuir la Kikimora")
        self.Player.items_possedes = self.modele.items
        self.Player.points_de_vie = self.modele.points_de_vie
        self.Player.points_de_vie_max = self.modele.points_de_vie_max
        self.Player.points_de_mana = self.modele.points_de_mana
        self.Player.points_de_mana_max = self.modele.points_de_mana_max
        self.Player.points_de_defence = self.modele.points_de_defence
        self.Player.points_de_force = self.modele.points_de_force
        self.Player.points_dintelligence = self.modele.points_de_intelligence
        self.Player.taux_coup_critique = self.modele.taux_de_coup_critique
        self.Player.degat_coup_critique = self.modele.degat_de_coup_critique
        self.Player.taux_sort_critique = self.modele.taux_de_sort_critique
        self.Player.degat_sort_critique = self.modele.degat_de_sort_critique
        self.Player.taux_desquive = self.modele.taux_de_esquive
        self.Player.nombre_de_gold = self.modele.nombre_de_gold
        if self.modele.mauvais_tachyon:
            self.Player.charge_mauvais_tachyon = self.modele.charge_mauvais_tachyon
        if self.modele.bon_tachyon:
            self.Player.charge_bon_tachyon = self.modele.charge_bon_tachyon
        self.Player.quete = self.modele.quete_en_cours
        if "KIA" in self.Player.player_tags:
            pass
        else:
            if self.modele.stigma_joueur_negatif == "Fair Play" and self.modele.points_de_vie <= round(self.modele.points_de_vie_max * 0.15):
                musique = self.modele.CHEMINABSOLUMUSIQUE + "battle_win"
                self.vue.AfficheFairPlay(musique)
                musique1 = self.modele.CHEMINABSOLUMUSIQUE + "death"
                self.vue.ShowGameOverScreen(musique1)
                self.Player.player_tags.append("KIA")
            elif self.modele.type_de_derniere_action_utilisee == "Fuir" or "En Fuite" in self.modele.monstre_tags:
                musique = self.modele.CHEMINABSOLUMUSIQUE + "escape"
                commentaire = "Vous avez fuit le combat !"
                if "En Fuite" in self.modele.monstre_tags:
                    commentaire = "L'ennemi jette une bombe fumigène et s'enfuit dans le nuage fumée !"
                    self.Player.vies_du_gardien = self.modele.monstre_nombre_de_vies_supplementaire
                self.vue.AfficheFuite(musique, commentaire)
            else:
                
                if self.modele.monstre_de_lobelisque:
                    musique = self.modele.CHEMINABSOLUMUSIQUE + "battle_win"
                    self.vue.AfficheWinObelisque(musique)
                elif self.modele.boss_histoire:
                    pass
                else:
                    if self.modele.monstre_nom == "Ah Kin":
                        self.Player.vies_du_gardien = 0
                    commentaire = ""
                    musique = self.modele.CHEMINABSOLUMUSIQUE + "battle_win"
                    self.vue.AfficheTitreRecompense(musique, self.modele.monstre_nom)
                    for cle in self.modele.monstre_recompense:
                        if cle == "Attaque":
                            self.Player.points_de_force += self.modele.monstre_recompense[cle]
                            commentaire = f"Vous gagnez {self.modele.monstre_recompense[cle]} points de force !"
                        elif cle == "Defence":
                            self.Player.points_de_defence += self.modele.monstre_recompense[cle]
                            commentaire = f"Vous gagnez {self.modele.monstre_recompense[cle]} points de défence !"
                        elif cle == "Intelligence":
                            self.Player.points_dintelligence += (
                                self.modele.monstre_recompense[cle]
                            )
                            commentaire = f"Vous gagnez {self.modele.monstre_recompense[cle]} points d'intelligence !"
                        elif cle == "Vie":
                            self.Player.points_de_vie += self.modele.monstre_recompense[cle]
                            commentaire = f"Vous regagnez {self.modele.monstre_recompense[cle]} points de vie !"
                        elif cle == "Vie max":
                            self.Player.points_de_vie_max += self.modele.monstre_recompense[cle]
                            commentaire = f"Vous gagnez {self.modele.monstre_recompense[cle]} points de vie maximum !"
                        elif cle == "Mana":
                            self.Player.points_de_mana += self.modele.monstre_recompense[cle]
                            commentaire = f"Vous regagnez {self.modele.monstre_recompense[cle]} points de mana !"
                        elif cle == "Mana max":
                            self.Player.points_de_mana_max += self.modele.monstre_recompense[
                                cle
                            ]
                            commentaire = f"Vous gagnez {self.modele.monstre_recompense[cle]} points de mana maximum !"
                        elif cle == "Endurance":
                            self.Player.points_dendurance += self.modele.monstre_recompense[
                                cle
                            ]
                            commentaire = f"Vous gagnez {self.modele.monstre_recompense[cle]} points d'endurance maximum !"
                        elif cle == "Taux coup critique":
                            self.Player.taux_coup_critique += self.modele.monstre_recompense[
                                cle
                            ]
                            commentaire = f"Vous gagnez {self.modele.monstre_recompense[cle]}% de chance de faire un coup critique !"
                        elif cle == "Degat coup critique":
                            self.Player.degat_coup_critique += (
                                self.modele.monstre_recompense[cle]
                            )
                            commentaire = f"Vous gagnez {self.modele.monstre_recompense[cle]} points de degats de coup critique !"
                        elif cle == "Taux sort critique":
                            self.Player.taux_sort_critique += self.modele.monstre_recompense[
                                cle
                            ]
                            commentaire = f"Vous gagnez {self.modele.monstre_recompense[cle]}% de chance de faire un sort critique !"
                        elif cle == "Taux esquive":
                            self.Player.taux_desquive += self.modele.monstre_recompense[
                                cle
                            ]
                            commentaire = f"Vous gagnez {self.modele.monstre_recompense[cle]}% de chance d'esquiver !"
                        elif cle == "Degat sort critique":
                            self.Player.degat_sort_critique += (
                                self.modele.monstre_recompense[cle]
                            )
                            commentaire = f"Vous gagnez {self.modele.monstre_recompense[cle]} points de degats de sort critique !"
                        elif cle == "Red coin":
                            self.Player.nombre_de_red_coin += self.modele.monstre_recompense[
                                cle
                            ]
                            commentaire = (
                                f"Vous gagnez {self.modele.monstre_recompense[cle]} Red Coin !"
                            )
                        elif cle == "Tirage":
                            self.tirage.UseTirage()
                            commentaire = "La boite disparait..."
                        elif cle == "Méga Tirage":
                            self.tirage.UseMegaTirage()
                            commentaire = "La boite disparait..."
                        elif cle == "Gold":
                            nombre_de_gold_gagne = self.modele.monstre_recompense[cle]
                            bonus_gold_gagne = round((self.modele.numero_de_letage / 10) * nombre_de_gold_gagne)
                            nombre_de_gold_gagne += bonus_gold_gagne
                            nombre_de_gold_gagne += round(nombre_de_gold_gagne * (self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Noyau d'Aurelionite"] / 100 ))
                            if self.Player.malediction == "Ascétique":
                                nombre_de_gold_gagne -= round(nombre_de_gold_gagne * 0.5)
                            if self.Player.benediction == "Materiel":
                                nombre_de_gold_gagne += nombre_de_gold_gagne
                            if self.modele.stigma_joueur_negatif == "Chrometophobia":
                                nombre_de_gold_gagne -= round(0.25 * nombre_de_gold_gagne)
                            self.Player.nombre_de_gold += nombre_de_gold_gagne
                            commentaire = f"Vous récuperez {nombre_de_gold_gagne} golds sur le cadavre de l'ennemi !"
                            if self.modele.facture and self.modele.monstre_est_paralyse:
                                self.Player.nombre_de_gold += (nombre_de_gold_gagne * 5)
                                commentaire += ("\nLes esprits de foudre qui vous regardent vous battre depuis les tribunes du Coliseum sont enchantés"
                                            " de voir que vous avez abattu de sang froid un ennemi paralysé et sans défence !\n"
                                            f"Ils font pleuvoir des golds sur vous !\n"
                                            f"Vous récuperez {(nombre_de_gold_gagne * 5)} golds  !")
                            if self.modele.richesse_souterraine:
                                self.Player.nombre_de_gold += (nombre_de_gold_gagne * 2)
                                commentaire += ("\nVotre lien avec la terre fait qu'elle remonte des richesse souterraines"
                                            " à la mort de l'ennemi pour vous féliciter de votre victoire.\nVous récuperez"
                                            f" {(nombre_de_gold_gagne * 2)} golds  !")
                            if "Bandeau Teinté" in self.modele.liste_dartefacts_optionels:
                                commentaire += ("\nVous récuperez les golds invoqués par votre bandeau pour contrebalancer les malheurs de votre combat."
                                                f"\nVous récuperez {self.modele.nombre_de_tours} golds !")
                                self.Player.nombre_de_gold += self.modele.nombre_de_tours
                        elif cle == "Materiau":
                            nombre_aleatoire = random.randint(0,100)
                            limite = 100
                            if nombre_aleatoire <= limite:
                                materiau = self.modele.monstre_recompense[
                                    cle
                                ]
                                self.Player.liste_de_materiaux[materiau] += 1
                                commentaire = (
                                    f"L'ennemi lache le materiau [{self.modele.monstre_recompense[cle]}] !"
                                )
                                if self.modele.stigma_joueur_bonus == 'Démanteleur' and random.randint(0,100)<90 :
                                    self.Player.liste_de_materiaux[materiau] += 1
                                    commentaire += (
                                        f"\nVous démentelez son cadavre d'une main experte et récupérez un deuxieme materiau !"
                                    )
                        self.vue.AfficheRecompense(commentaire)
                    if (self.modele.stigma_joueur_positif == "Conception du Mana" and random.randint(0,1) == 0):
                        mana_gagne = 2
                        self.Player.points_de_mana_max += mana_gagne
                        commentaire = f"Votre origine vous permet d'absorber l'essence même du monstre et de gagner {mana_gagne} points de mana maximum !"
                        self.vue.AfficheRecompense(commentaire)
                    if self.modele.possede_une_gemme_vie:
                        vie_regagnee = round(self.modele.points_de_vie_max * 0.25)
                        self.Player.points_de_vie += vie_regagnee
                        commentaire = f"Votre gemme de vie vous fait regagner {vie_regagnee} points de vie !"
                        self.vue.AfficheRecompense(commentaire)
                    if ("Marque du Tyrant" in self.Player.liste_dartefacts_optionels) and (self.modele.points_de_vie_max == self.modele.points_de_vie):
                        self.Player.points_de_vie += 1
                        self.Player.points_de_vie_max += 1
                        commentaire = f"Vous tendez la main vers L'ennemi, et votre Marque du Tyrant vous donne 1 point de vie max supplémentaire !"
                        self.vue.AfficheRecompense(commentaire)
                    if self.modele.possede_une_gemme_magie:
                        mana_regagne = round(self.modele.points_de_mana_max * 0.25)
                        self.Player.points_de_mana += mana_regagne
                        commentaire = f"Votre gemme de mana vous fait regagner {mana_regagne} points de mana !"
                        self.vue.AfficheRecompense(commentaire)
                    if self.modele.stigma_joueur_negatif == "Incontrolable":
                        commentaire = "Vous perdez votre controle sur votre réserve de mana et perdez tout vos points de mana."
                        self.Player.points_de_mana = 0
                        self.vue.AfficheRecompense(commentaire)
                    bonus_charge = 0
                    if "Element [Ame] Surchargé" in self.modele.liste_dartefacts_optionels:
                        bonus_charge += 1
                    self.Player.nombre_de_monstres_tues += 1 + bonus_charge
                    commentaire = f"Le nombre d'âmes que vous avez absorbé passe à {self.Player.nombre_de_monstres_tues}."
                    self.vue.AfficheRecompense(commentaire)
                    if self.Player.points_de_mana > self.Player.points_de_mana_max:
                        self.Player.points_de_mana = self.Player.points_de_mana_max
                    if self.Player.points_de_vie > self.Player.points_de_vie_max:
                        self.Player.points_de_vie = self.Player.points_de_vie_max
                    self.vue.EntreePourContinuer()
                    if self.Player.quete != "None":
                        self.ResultatQuete()
                    #Ajout des sacrifices
                    if self.modele.sacrifice_actif:
                        self.Player.nombre_de_sacrifices += 1
                        commentaire1 = ("Vous regardez l'ennemi gisant sur le sol, et voyez une lueur bleue émaner de son corps.")
                        commentaire2 = ("Cette lueur commence doucement a monter, avant de venir s'écraser a toute vitesse sur votre bras noirci.")
                        commentaire3 = ("Des lettres apparaissent alors au niveau du dos de votre main :"
                                        "\n\n                          SACRIFICE"
                                        f"\n\n                              {self.Player.nombre_de_sacrifices}\n")
                        commentaire4 = ("Les lettres disparaissent, et tout revient a la normale.")
                        self.vue.AffichageSacrifice(commentaire1, commentaire2, commentaire3, commentaire4)
                    # gain de la carte
                    if "Monstre Dopé" in self.modele.player_tags:
                        commentaire1 = ("Alors que vous examinez le cadavre du monstre, vous trouvez une main coupéee, épinglée au monstre par une des seringues.")
                        commentaire1 += ("\nY est accrochée une carte sur laquelle se trouve la photo d'un homme dans la cinquantaine.")
                        commentaire2 = ("Vous obtenez l'artefact [Carte de Sécurité] !")
                        commentaire2 += ("\nUne carte retrouvée sur la cadavre d'un monstre particulièrement coriace, dopé a l'aide d'étranges substances.\nQui sait ce qu'elle peut bien faire ?")
                        self.Player.liste_dartefacts_optionels.append("Carte de Sécurité")
                        self.vue.AffichageMonstreDopeRecompense(commentaire1, commentaire2)
                    if self.modele.est_une_mimique:
                        commentaire1 = ("Le corps de la mimique git a terre...\nVous en profitez pour fouiller a l'interieur du coffre vivant.")
                        commentaire2 = ("Vous en sortez un petit coffre de bois noir, que vous vous empressez d'ouvrir !")
                        self.vue.AfficheMimiqueMorte(commentaire1, commentaire2)
                        self.Floormaker.GiveRandomArtefact()
                    if self.modele.monstre_EstUnBoss and self.Player.malediction == "Sparifique":
                        commentaire = "D'anciennes forces maudites font appraitre une petite boite de bois noir devant vous, que vous vous empressez d'ouvrir !"
                        self.vue.AfficheSparifique(commentaire)
                        self.Floormaker.GiveRandomArtefact("None","Boss")
                    if not self.modele.monstre_EstUnBoss and self.Player.benediction == "Omnipotent":
                        commentaire = "Vous recevez la force d'anciennes prières !"
                        nombre_aleatoire = random.randint(0,100)
                        if nombre_aleatoire <= 50:
                            self.Player.points_de_vie_max += 1
                            commentaire += "\nVous gagnez un point de vie max !"
                        else:
                            self.Player.points_de_mana_max += 1
                            commentaire += "\nVous gagnez un point de mana max !"
                        self.vue.AfficheOmnipotent(commentaire)
                    if self.modele.stigma_joueur_bonus == "Script":
                        self.Sove.RajouteEntreeAuLivreCigogneBlancheSiOnAPas("Les Ennemis", self.modele.monstre_nom)
            if self.modele.possede_une_fee == False and "Fée dans un Bocal" in self.Player.liste_dartefacts_optionels:
                self.Player.liste_dartefacts_optionels.remove("Fée dans un Bocal")
                self.Player.possede_une_fee = False
                
        self.StopCombatSounds()

    def StopCombatSounds(self):
        self.vue.CHANNELSONSORT.set_volume(0)
        self.vue.CHANNELSONTECHNIQUE.set_volume(0)
        self.vue.CHANNELMUSIQUECOMBAT.set_volume(0)
        time.sleep(0.01)
        self.vue.CHANNELSONSORT.stop()
        self.vue.CHANNELSONTECHNIQUE.stop()
        self.vue.CHANNELMUSIQUECOMBAT.stop()

    def ResultatQuete(self):
        # quete interminable
        if self.Player.quete == "Interminable":
            if self.modele.nombre_de_tours >= 50:
                self.Player.quete += " [Complete]"
            else:
                self.Player.quete += " [Echec]"
        # avancement quete magister
        if "Epreuve du Magister" in self.Player.quete:
            if self.Player.quete == "Epreuve du Magister":
                self.Player.quete = "Epreuve du Magister (1/4)"
            elif self.Player.quete == "Epreuve du Magister (1/4)":
                self.Player.quete = "Epreuve du Magister (2/4)"
            elif self.Player.quete == "Epreuve du Magister (2/4)":
                self.Player.quete = "Epreuve du Magister (3/4)"
            elif self.Player.quete == "Epreuve du Magister (3/4)":
                self.Player.quete = "Epreuve du Magister [Complete]"
        # avancement quete mage epeiste
        if "Epreuve des Mages-Epeistes" in self.Player.quete:
            if self.Player.quete == "Epreuve des Mages-Epeistes":
                self.Player.quete = "Epreuve des Mages-Epeistes (1/4)"
            elif self.Player.quete == "Epreuve des Mages-Epeistes (1/4)":
                self.Player.quete = "Epreuve des Mages-Epeistes (2/4)"
            elif self.Player.quete == "Epreuve des Mages-Epeistes (2/4)":
                self.Player.quete = "Epreuve des Mages-Epeistes (3/4)"
            elif self.Player.quete == "Epreuve des Mages-Epeistes (3/4)":
                self.Player.quete = "Epreuve des Mages-Epeistes [Complete]"
        # avancement quete honneur
        if "Force et Honneur" in self.Player.quete:
            if self.Player.quete == "Force et Honneur":
                self.Player.quete = "Force et Honneur (1/8)"
            elif self.Player.quete == "Force et Honneur (1/8)":
                self.Player.quete = "Force et Honneur (2/8)"
            elif self.Player.quete == "Force et Honneur (2/8)":
                self.Player.quete = "Force et Honneur (3/8)"
            elif self.Player.quete == "Force et Honneur (3/8)":
                self.Player.quete = "Force et Honneur (4/8)"
            elif self.Player.quete == "Force et Honneur (4/8)":
                self.Player.quete = "Force et Honneur (5/8)"
            elif self.Player.quete == "Force et Honneur (5/8)":
                self.Player.quete = "Force et Honneur (6/8)"
            elif self.Player.quete == "Force et Honneur (6/8)":
                self.Player.quete = "Force et Honneur (7/8)"
            elif self.Player.quete == "Force et Honneur (7/8)":
                self.Player.quete = "Force et Honneur [Complete]"
        # avancement quete Moqueries Magiques
        if self.Player.quete == "Moqueries Magiques" and self.modele.monstre_EstUnBoss:
            self.Player.quete = "Moqueries Magiques [Complete]"
        # avancement quete Moqueries Techniques
        if self.Player.quete == "Moqueries Techniques" and self.modele.monstre_EstUnBoss:
            self.Player.quete = "Moqueries Techniques [Complete]"
        commentaire = f"Etat de la quête en cours : {self.Player.quete}"
        if "[Echec]" in self.Player.quete:
            commentaire += "\nAbandonnez cette quete et reprenez la pour réessayer !"
        elif "[Complete]" in self.Player.quete:
            self.vue.PlaySound("questdone")
            commentaire += "\nFélicitation !\nVous avez complété la quête !\nAllez récuperer votre récompense !"
        else:
            commentaire += "\nContinuez comme ca !\nVous êtes sur la bonne voie !"
        self.vue.AfficheQuete(commentaire)
            

    def EffetStigmaDernierChoix(self):
        while True:
            try:
                choix = self.vue.GetStigmaDernierChoixChoice()
                if choix == 1:
                    self.modele.dernier_choix_effectue = True
                    break
                elif choix == 2:
                    self.modele.dernier_choix_effectue = True
                    break
                clear_console()
            except ValueError:
                clear_console()
        if choix == 1:
            liste_dennemis = self.modele.liste_de_monstre_totaux_pour_dernier_choix[self.modele.numero_de_letage - 1]
            commentaire = "Vous laissez l'ennemi s'enfuir et regardez les tribunes autour. Quel nom allez vous appeler ?"
            numero = 1
            for nom in liste_dennemis:
                commentaire += f"\n{numero} - {nom}" 
                numero += 1   
            while True:
                try:
                    choix = self.vue.GetStigmaDernierChoixEnnemyChoice(commentaire)
                    if choix in range(1, (len(liste_dennemis) + 1)):
                        ancien_monstre = self.modele.monstre_nom
                        self.modele.monstre_nom = liste_dennemis[choix - 1]
                        self.SetAttributesFromName()
                        self.vue.AfficheNouveauMonstre(
                            ancien_monstre, self.modele.monstre_nom
                        )
                        break
                    clear_console()
                except ValueError:
                    clear_console()

    def EffetStigmaSanjiva(self):
        limite = round(self.modele.points_de_vie_max * 0.05)
        if self.modele.points_de_vie < limite:
            self.modele.points_de_vie = round(self.modele.points_de_vie_max * 0.2)
            self.vue.AfficheSanjiva()

    def EffetStigmaMusculeux(self):
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 8:
            self.modele.monstre_passe_son_tour = True
            self.modele.musculeux_touche = True

    def EffetStigmaAbomination(self):
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 8:
            self.modele.passe_son_tour = True
            self.modele.abomination_touche = True

    def EffetStigmaAveugle(self):
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 10:
            self.modele.monstre_passe_son_tour = True
            self.modele.aveugle_touche = True

    def EffetStigmaGluantin(self):
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 5:
            self.modele.monstre_passe_son_tour = True

    def EffetStigmaCorpsMassif(self):
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 10:
            self.modele.monstre_passe_son_tour = True

    def EffetStigmaAddict(self):
        if self.modele.nombre_de_tours == 10:
            self.modele.monstre_points_de_vie = -100
            self.vue.AfficheAddict()

    def EffetStigmaSurveille(self):
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire < 3:
            reponse = self.QuestionsDeAlfred()
            if reponse:
                # 5a: si bonne réponse, change nom, fini combat, donne recompense
                self.modele.monstre_nom = "???"
                self.SetAttributesFromName()
                self.modele.InCombat = False
                commentaire = "- ...c'est une bonne réponse."
                commentaire2 = "- Bien joué."
                commentaire3 = (
                    "*Alfred claque des doigts et l'âme"
                    " du monstre prend une teinte de nacre.*"
                )
                self.vue.FinAlfred(commentaire, commentaire2, commentaire3)
            else:
                # 5b: si mauvaise reponse, gold/vie/mana -50%, fuite
                self.modele.nombre_de_gold -= round(self.modele.nombre_de_gold * 0.5)
                self.modele.points_de_vie -= round(self.modele.points_de_vie * 0.5)
                self.modele.points_de_mana -= round(self.modele.points_de_mana * 0.5)
                self.EquilibragePointsDeVieEtManaEtEndurance()
                self.modele.type_de_derniere_action_utilisee = "Fuir"
                self.modele.InCombat = False
                commentaire = "- ...c'est une mauvaise réponse."
                commentaire2 = (
                    "*Alfred ouvre la bouche en grand, bien plus"
                    " que ce qui est humainement possible, et vous"
                    " perdez connaissance devant ce qui semble "
                    "être une mer de dents parfaitement"
                    " aiguisées.*"
                )
                commentaire3 = (
                    "*Quand vous reprenez connaissance dans "
                    "une mare de votre propre sang, vous savez"
                    " que quelque chose de mal s'est produit "
                    "dans cette piece.\nL'âme du monstre n'est "
                    "nulle part.\nVous vous sentez S O U I L L E."
                )
                self.vue.FinAlfred(commentaire, commentaire2, commentaire3)
                print("La perspective de revoir Alfred vous terrifie jusqu'au plus profond de votre être.")
                self.vue.EntreePourContinuer()

    def QuestionsDeAlfred(self):
        # 1:afficher intro alfred
        musique = self.modele.CHEMINABSOLUMUSIQUE + "alfredproto"
        self.vue.IntroAlfred(musique)
        # 2:choisir question a donner
        nombre_de_question = len(self.modele.alfred_liste_questions)
        index_aleatoire = random.randint(0, (nombre_de_question - 1))
        question_pose = self.modele.alfred_liste_questions[index_aleatoire]
        # 3:faire un try/except sur un input pour eviter le crash
        while True:
            try:
                question = question_pose["Question"]
                reponse1 = question_pose["Reponse 1"]
                reponse2 = question_pose["Reponse 2"]
                reponse3 = question_pose["Reponse 3"]
                reponse4 = question_pose["Reponse 4"]
                choix = self.vue.AlfredChoice(
                    question, reponse1, reponse2, reponse3, reponse4
                )
                clear_console()
                if choix in [1, 2, 3, 4]:
                    # 4: comparer la réponse donnée a la réponse voulue
                    if choix == question_pose["Reponse a la question"]:
                        return True
                    else:
                        return False
            except ValueError:
                clear_console()

    def EffetStigmaCopycat(self):
        if self.modele.derniere_action_utilisee == "Passer son tour":
            self.modele.monstre_passe_son_tour = True

    def EffetStigmaHematophobe(self):
        if self.modele.a_utilise_sang_ce_tour:
            nombre_aleatoire = random.randint(0, 100)
            if nombre_aleatoire <= 10:
                self.modele.monstre_passe_son_tour = True

    def EffetStigmaConsumme(self):
        cas_particulier = self.modele.stigma_consumme_tour
        if cas_particulier == 1 and self.modele.nombre_de_tours == 2:
            self.modele.monstre_points_de_vie = -100
            self.vue.AfficheConsumme(self.modele.nombre_de_tours)
        elif cas_particulier == 2 and self.modele.nombre_de_tours == 5:
            self.modele.monstre_points_de_vie = -100
            self.vue.AfficheConsumme(self.modele.nombre_de_tours)
        elif cas_particulier == 3 and self.modele.nombre_de_tours == 11:
            self.modele.monstre_points_de_vie = -100
            self.vue.AfficheConsumme(self.modele.nombre_de_tours)
        elif cas_particulier == 4 and self.modele.nombre_de_tours == 17:
            self.modele.monstre_points_de_vie = -100
            self.vue.AfficheConsumme(self.modele.nombre_de_tours)

    def ApplicationStigmaPourFinDuTour(self):
        if self.modele.stigma_joueur_positif == "Bénie par les Fées":
            self.EffetStigmaBeniParLesFees()
        elif self.modele.stigma_joueur_positif == "Dernier Choix":
            if (
                not self.modele.dernier_choix_effectue
                and not self.modele.monstre_EstUnBoss
                and not self.modele.est_une_mimique
            ):
                self.EffetStigmaDernierChoix()
        if self.modele.stigma_joueur_positif == "Second Souffle":
            self.EffetStigmaSecondSouffle()
        if self.modele.stigma_joueur_positif == "Recharge Rapide":
            self.EffetStigmaRechargeRapide()
        if self.modele.stigma_joueur_positif == "Transhumanisme":
            self.EffetStigmaTranshumanisme()
        if self.modele.stigma_joueur_negatif == "Pause Repas":
            self.EffetStigmaPauseRepas()
        if self.modele.stigma_joueur_negatif == "Miss Hyde":
            self.EffetStigmaMissHyde()
        if self.modele.stigma_joueur_negatif == "Fatigue Chronique":
            self.EffetStigmaFatigueChronique()
        if self.modele.stigma_joueur_negatif == "Flemme":
            self.EffetStigmaFlemme()
        elif self.modele.stigma_joueur_negatif == "Ange Déchue":
            self.EffetStigmaAngeDechue()
        if "Mage" in self.modele.liste_dartefacts_optionels:
            self.AppliqueMage()
        if self.modele.stigma_joueur_bonus == "Sanjiva":
            self.EffetStigmaSanjiva()
        elif self.modele.stigma_joueur_bonus == "Musculeux":
            self.EffetStigmaMusculeux()
        if self.modele.stigma_monstre_positif == "Toucher de Midas":
            self.EffetStigmaToucherDeMidas()
        elif self.modele.stigma_monstre_positif == "Abomination":
            self.EffetStigmaAbomination()
        elif self.modele.stigma_monstre_positif == "Siphon de Mana":
            self.EffetStigmaSiphonDeMana()
        elif self.modele.stigma_monstre_positif == "Circuits Logiques":
            self.EffetStigmaCircuitsLogiques()
        elif self.modele.stigma_monstre_positif == "Bénédiction Divine":
            self.EffetStigmaBenedictionDivine()
        elif self.modele.stigma_monstre_positif == "Bomberman":
            self.EffetStigmaBomberman()
        elif self.modele.stigma_monstre_positif == "Plus d'un Tour":
            self.EffetStigmaPlusDUnTour()
        if self.modele.stigma_monstre_negatif == "Mégalovania":
            self.EffetStigmaMegalovania()
        elif self.modele.stigma_monstre_negatif == "Aveuglé":
            self.EffetStigmaAveugle()
        elif self.modele.stigma_monstre_negatif == "Homoncule":
            self.EffetStigmaHomoncule()
        elif self.modele.stigma_monstre_negatif == "Gluantin":
            self.EffetStigmaGluantin()
        elif self.modele.stigma_monstre_negatif == "Corps Massif":
            self.EffetStigmaCorpsMassif()
        elif self.modele.stigma_monstre_negatif == "Addict":
            self.EffetStigmaAddict()
        elif self.modele.stigma_monstre_negatif == "Surveillé":
            self.EffetStigmaSurveille()
        elif self.modele.stigma_monstre_negatif == "Copycat":
            self.EffetStigmaCopycat()
        elif self.modele.stigma_monstre_negatif == "Hématophobe":
            self.EffetStigmaHematophobe()
        elif self.modele.stigma_monstre_negatif == "Consummé":
            self.EffetStigmaConsumme()
        elif self.modele.stigma_monstre_negatif == "Patchwork":
            self.EffetStigmaPatchwork()
        elif self.modele.stigma_monstre_negatif == "Arlequin":
            self.EffetStigmaArlequin()
        if "Terreur" in self.modele.monstre_tags and self.IsMultipleOf(self.modele.nombre_de_tours, 6):
            self.EffetTagTerreur()
        if "Fausse Terreur" in self.modele.monstre_tags and self.IsMultipleOf(self.modele.nombre_de_tours, 6):
            self.EffetTagFausseTerreur()
        if "Domovoï" in self.modele.monstre_tags:
            self.EffetTagDomovoi()
        if "Kikimora" in self.modele.monstre_tags:
            self.EffetTagKikimora()
        if "Super Etoile" in self.modele.monstre_tags:
            self.EffetSuperEtoile()
        if self.Player.malediction == "Impotent" and self.modele.nombre_de_tours <= 5:
            self.EffetImpotent()
        if "Cuisine Infernale" in self.modele.monstre_tags:
            self.EffetCuisineInfernale()
        if "Voluntad tin tuukul" in self.modele.monstre_tags:
            self.EffetGardienDeAme()
        if "Voluntad U Wíinkilal" in self.modele.monstre_tags:
            self.EffetGardienDeCorps()
        if "Canigou" in self.modele.liste_dartefacts_optionels:
            self.EffetCanigou()
        if "Epée de Damocles" in self.modele.liste_dartefacts_optionels:
            self.EffetEppeeDamocles()
        if "Morceau d'Ether Fragile" in self.modele.liste_dartefacts_optionels:
            self.EffetMorceauEtherFragile()
        if "Eau Bénite" in self.modele.liste_dartefacts_optionels:
            self.EffetEauBenite()

    def EffetImpotent(self):
        if self.modele.monstre_points_de_vie != self.modele.monstre_points_de_vie_max:
            self.modele.monstre_points_de_vie = self.modele.monstre_points_de_vie_max
            commentaire = "D'anciennes forces maudites font reprendre à l'ennemi tout ses points de vie."
            self.vue.AfficheEffetImpotent(commentaire)

    def AppliqueMage(self):
        if self.modele.points_de_vie < 10:
            commentaire = "Vos points de vie sont critiques, vous avez du mal a garder les yeux ouverts..."
            commentaire_effet = "...et l'ennemi en profite pour assener un coup magistral dans la tête de la Mage qui vous accompagnait.\nVous prenez pleine conscience de son sort alors qu'une flaque de sang se forme sous sa tête."
            self.Player.liste_dartefacts_optionels.remove("Mage")
            self.modele.liste_dartefacts_optionels.remove("Mage")
            self.vue.AfficheMage(commentaire, commentaire_effet)
        else:
            commentaire = "La Mage qui vous accompagne lance un sort sur l'ennemi ..."
            nombre_aleatoire = random.randint(0, 3)
            if nombre_aleatoire == 1 :
                commentaire_effet = "Il s'embrase pendant 1 tour !"
                self.modele.monstre_est_en_feu = True
                self.modele.monstre_est_en_feu_nombre_tour += 2
                self.modele.monstre_est_en_feu_degat = 3
            elif nombre_aleatoire == 2 :
                commentaire_effet = "Il gèle pendant 1 tour !"
                self.modele.monstre_est_gele = True
                self.modele.monstre_est_gele_nombre_tour += 2
            else:
                commentaire_effet = "...mais rien ne se passe.\n*Oups !*"
            self.vue.AfficheMage(commentaire, commentaire_effet)

    def EffetEppeeDamocles(self):
        numero_aleatoire = random.randint(0, 100)
        if numero_aleatoire in [1, 2, 3]:
            degat = round(self.modele.points_de_vie_max * 0.25)
            self.modele.points_de_vie -= degat
            if self.modele.points_de_vie < 1:
                self.modele.points_de_vie = 1
            self.Player.liste_dartefacts_optionels.remove("Epée de Damocles")
            self.vue.AfficheEppeeDamocles()
    
    def EffetMorceauEtherFragile(self):
        numero_aleatoire = random.randint(0, 100)
        if numero_aleatoire in [1, 2, 3]:
            self.modele.points_de_mana = 0
            self.Player.liste_dartefacts_optionels.remove("Morceau d'Ether Fragile")
            self.vue.AfficheMorceauEtherFragile()

    def EffetEauBenite(self):
        numero_aleatoire = random.randint(0, 100)
        if numero_aleatoire in [1, 2, 3]:
            self.modele.beni_par_feu_sacre = True
            self.modele.beni_par_feu_sacre_nombre_tour += 1
            self.vue.AfficheEffetEauBenite()

    def EffetCanigou(self):
        degat = round(self.modele.monstre_points_de_vie_max * 0.03)
        # print(f"vie monstre av {self.modele.monstre_points_de_vie}")
        self.modele.monstre_points_de_vie -= degat
        # print(f"vie monstre  ap {self.modele.monstre_points_de_vie}")
        self.vue.AfficheCanigou(f"Canigou saute sur l'ennemi et lui arrache une petite partie de son bras .\nIl perd {degat} points de vie !\nCa c'est un bon toutou !")

    def EffetGardienDeCorps(self):
        self.vue.AfficheGardienDeCorps("Voluntad U Wíinkilal, l'esprit de la chair, vous absorbe des points d'endurance !")
        perte_de_endurance = round(self.modele.points_de_endurance_max * 0.1)
        self.modele.points_de_endurance -= perte_de_endurance
        if self.modele.points_de_endurance < 0:
            self.modele.points_de_endurance = 0

    def EffetGardienDeAme(self):
        self.vue.AfficheGardienDeAme("Voluntad Tin Tuukul, l'esprit de l'âme, rend tout ses points de mana a l'ennemi !")
        self.modele.monstre_points_de_mana = self.modele.monstre_points_de_mana_max

    def EffetStigmaSecondSouffle(self):
        if self.modele.points_de_endurance < self.modele.points_de_endurance_max * 0.5 :
            self.modele.points_de_endurance += 3
            self.vue.AfficheStigmaSecondSouffle("Votre entrainement vous permet de calmer votre respiration a travers l'essouflement et vous regagnez des points d'endurance.")
        if self.modele.points_de_endurance > self.modele.points_de_endurance_max :
            self.modele.points_de_endurance = self.modele.points_de_endurance_max    

    def EffetStigmaRechargeRapide(self):
        if self.modele.points_de_mana < self.modele.points_de_mana_max * 0.5 :
            self.RecouvrementDeMana(3)
            self.vue.AfficheStigmaRechargeRapide("Vous invoquez dans votre esprit le gout que la dinde avait lors d'un de ces somptueux banquet a Venise... et reprenez des points de mana .")

    def EffetStigmaTOC(self):
        self.modele.passe_son_tour = True 
        self.modele.tour_passe_car_ramasse_item += 2
        self.PasserSonTour

    def EffetStigmaTranshumanisme(self):
        if self.modele.points_de_vie < self.modele.points_de_vie_max * 0.5 :
            self.modele.points_de_vie += 3
            self.vue.AfficheStigmaTranshumanisme("Vos blessures vous grattent... surement parce qu'elles guérissent déja. Vous reprenez quelques points de vie .")
        if self.modele.points_de_vie > self.modele.points_de_vie_max :
            self.modele.points_de_vie = self.modele.points_de_vie_max    

    def EffetStigmaMissHyde(self):
        if not self.modele.miss_hyde_transformation and random.randint(0,100)<=5 :
            self.modele.miss_hyde_transformation = True
            self.modele.miss_hyde_transformation_nombre_tour = 3
            self.vue.AfficheStigmaTranshumanisme("Vous sentez la colère monter en vous, et la malédiction des Hyde prend le controle !")


    def EffetStigmaPauseRepas(self):
        if (random.randint(0,100) < 5 and not self.TousItemsVides()):

            #  item aléatoire
            item_a_manger = random.choice(self.ListeItemsPossedes())

            #  disparition de l'item
            self.modele.items[item_a_manger] -= 1

            # récupération des pm
            self.RecouvrementDeMana(int(round(self.modele.points_de_mana_max * 0.15)))

            #  affichage de l'action
            self.vue.AfficheStigmaPauseRepas(f"Vous avez faim. Vous farfouillez dans votre sac et sortez l\'item [{item_a_manger}] que vous vous empressez d'avaler.\nPas d'effets, mais vous reprenez quelques pm !")

    def EffetCuisineInfernale(self):
        # creer ou non une commande
        if len(self.modele.monstre_commande) == 0 and "Entrée" in self.modele.monstre_tags and not self.modele.monstre_est_service:
            longueur_de_commande = random.randint(2, 4)
            self.CuisineInfernaleCommande(longueur_de_commande, "Entrée")
        elif len(self.modele.monstre_commande) in range(0, 2) and "Plat" in self.modele.monstre_tags and not self.modele.monstre_est_service:
            longueur_de_commande = random.randint(3, 5)
            self.CuisineInfernaleCommande(longueur_de_commande, "Plat")
        elif len(self.modele.monstre_commande) in range(0,3) and "Dessert" in self.modele.monstre_tags and not self.modele.monstre_est_service:
            longueur_de_commande = random.randint(3, 5)
            self.CuisineInfernaleCommande(longueur_de_commande, "Dessert")

        # checker si la commande est prête
        if len(self.modele.monstre_commande) != 0:
            for commande in self.modele.monstre_commande:
                commande_etat = self.CuisineInfernaleCheck(commande)
                self.CuisineInfernalePriseCommande(commande_etat, commande)

        # enlever toutes les commandes passées du dictionnaire
        for commande_passee in self.modele.monstre_commande_a_enlever:
            if commande_passee in self.modele.monstre_commande:
                self.modele.monstre_commande.pop(commande_passee)
        self.modele.monstre_commande_a_enlever = []

    def CuisineInfernaleCheck(self, commande):
        temps_commande = self.modele.monstre_commande[commande]
        if (temps_commande == self.modele.nombre_de_tours) and (commande in self.modele.liste_ingredient):
            return "Tolérable"
        elif (temps_commande == self.modele.nombre_de_tours) and (commande not in self.modele.liste_ingredient):
            return "Intolérable"
        else:
            return "Pas le moment"

    def CuisineInfernalePriseCommande(self, commande_etat, commande):
        if commande_etat == "Pas le moment":
            pass
        elif commande_etat == "Tolérable":
            self.modele.monstre_commande_a_enlever.append(commande)
            self.modele.liste_ingredient.pop(commande)
            self.vue.AfficheCuisineInfernaleReussi(commande)
            self.modele.monstre_est_service = True
            self.modele.monstre_est_service_nombre_tour += 2
            self.modele.monstre_passe_son_tour = True
        elif commande_etat == "Intolérable":
            self.modele.monstre_commande_a_enlever.append(commande)
            degat = round(self.modele.points_de_vie_max * 0.25)
            if (self.modele.points_de_vie - degat) < 0 :
                degat = self.modele.points_de_vie - 1
            self.EnleveVieAuJoueur(degat)
            self.vue.AfficheCuisineInfernaleEchoue(commande, degat)

    def CuisineInfernaleCuisiner(self):
        #affiche menu action
        numero = 1
        cout = ""
        if "Entrée" in self.modele.monstre_tags:
            liste_action_commentaire = {"Couper" : "Vous empoignez un couteau...",
                             "Eplucher" : "Vous prenez un économe...", 
                             "Laver" : "Vous récuperez du sel pour faire friction, et faites couler de l'eau froide...",
                             "Etaler" : "Vous empoignez un couteau (à beurre)...", 
                             "Griller" : "Vous branchez un grille pain...", 
                             "Emietter" : "Vous mettez des gants...", 
                             "Sculpter" : "Vous empoignez un set de marteau et burin (désinfecté, bien entendu)...",
                             "Mélanger" : "Vous allez chercher deux ingrédients...",}
            liste_action_adjectif = {"Couper" : "Coupé",
                             "Eplucher" : "Epluché",
                             "Laver" : "Lavé", 
                             "Etaler" : "Etalé",
                             "Griller" :  "Grillé", 
                             "Emietter" : "Emietté", 
                             "Sculpter" : "Sculpté",
                             "Mélanger" : "mélangé à",}
            liste_action = ["Couper", "Eplucher", "Laver", "Etaler", "Griller", "Emietter", "Sculpter", "Mélanger"]
        elif "Plat" in self.modele.monstre_tags:
            liste_action_commentaire = {"Désosser" : "Vous empoignez un couteau (à désosser)...",
                                        "Rôtir" : "Vous préchauffez la rotissoire-magique-qui-fait-rôtir-en-un-seul-tour...",
                                        "Frire |10 pv| " : "Vous allumez un feu extrême sous une poêle remplie d'huile, les goutelettes brulantes fuyant a travers l'air....",
                                        "Cuire" : "Vous allumez le feu sous une des poêles...",
                                        "Arreter la cuisson" : "Vous regardez une des poêles...",
                                        "Mélanger" : "Vous allez chercher deux ingrédients...",
                                        "Caraméliser |50% de chance de réussite| " : "Vous croisez les doigts, allumez un feu chaotique sous une des poêles...",
                                        "Ecraser" : "Vous prenez un mortier en roche volcanique, ainsi que son pilon...",
                                        "Aromatiser" : "Vous créez un mélange immonde de toutes les épices sur lesquelles vous pouvez poser votre terrible et sadique petit regard..."}
            liste_action_adjectif = {"Désosser" : "Désossé",
                                        "Rôtir" : "Rôti",
                                        "Frire |10 pv| " : "Frit",
                                        "Cuire" : "None",
                                        "Arreter la cuisson" : "None",
                                        "Mélanger" : "mélangé à",
                                        "Caraméliser |50% de chance de réussite| " : "Caramélisé",
                                        "Ecraser" : "Ecrasé",
                                        "Aromatiser" : "Aromatisé"}
            liste_action = ["Désosser", "Rôtir", "Ecraser", "Aromatiser", "Frire |10 pv| ", "Caraméliser |50% de chance de réussite| ", "Cuire", "Arreter la cuisson", "Mélanger"]
        elif "Dessert" in self.modele.monstre_tags:
            liste_action_commentaire = {"Equeuter" : "Vous empoignez un petit couteau (a équeuter)...",
                                        "Zester" : "Vous prenez un zesteur (comme une fine rape a fromage, mais pour les fruits)...",
                                        "Rincer" : "Vous faites couler de l'eau froide...",
                                        "Concasser" : "Vous récupérez une grosse massue (désinfectée, bien sur)...",
                                        "Compoter" : "Vous allumez la machine-qui-fait-compoter-en-un-tour-alors-que-normalement-ca-dure-une-plombe...",
                                        "Dénoyauter" : "Vous empoignez un dénoyauteur (c'est juste un couteau)...",
                                        "Flamber" : "Vous trouvez une bouteille de vieil alcool au nom sophistiqué....",
                                        "Napper" : "Vous sortez un bol de creme au café du frigo...",
                                        "Mélanger" : "Vous allez chercher deux ingrédients...",
                                        "Fouetter |10 pe| " : "Vous cherchez un fouet, soupirez, puis prenez une fourchette...",
                                        "Geler |10 pm| " : "Vous refroidissez votre main a l'aide de mana..."}
            liste_action_adjectif = {"Equeuter" : "Equeuté",
                                        "Zester" : "Zesté",
                                        "Rincer" : "Rincé",
                                        "Concasser" : "Concassé",
                                        "Compoter" : "Compoté",
                                        "Dénoyauter" : "Dénoyauté",
                                        "Flamber" : "Flambé",
                                        "Napper" : "Nappé",
                                        "Fouetter |10 pe| " : "Fouetté",
                                        "Geler |10 pm| " : "Gelé",
                                        "Mélanger" : "mélangé à",}
            liste_action = ["Equeuter", "Zester", "Rincer", "Concasser", "Compoter", "Dénoyauter", "Flamber", "Napper", "Geler |10 pm| ", "Fouetter |10 pe| ", "Mélanger"]
        while True:
            try:
                self.vue.AfficheDebutActionCuisineInfernale()
                for action in liste_action:
                    self.vue.AfficheActionCuisineInfernale(numero, action, cout)
                    numero += 1
                numero = 1
                choix = self.vue.AfficheFinActionCuisineInfernale()
                clear_console()
                if choix in range(1, len(liste_action) + 1):
                    break
            except ValueError:
                clear_console()
        action_cuisine = liste_action[choix-1]
        
        #traduit l'action en adjectif
        adjectif_daction = liste_action_adjectif[action_cuisine]


        #petit commentaire selon l'action
        self.vue.AfficheCommentaireActionCuisineInfernale(liste_action_commentaire[action_cuisine])
                

        
        if action_cuisine != "Arreter la cuisson":
            #affiche menu ingredient
            numero = 1
            liste_ingredients_entree = ["Mozarella", "Tomate", "Concombre", "Rillette", "Pain", "Féta", "Saucisson"]
            liste_ingredients_plat = ["Porc", "Poulet", "Haricot Vert", "Carotte", "Oignon Jaune", "Patate", "Thon", "Riz", "Pates", "Couscous"]
            liste_ingredients_dessert = ["Fraise", "Citron", "Ananas", "Chocolat", "Oeuf", "Beurre de Cacahuète", "Lait", "Caramel", "Vanille"]

            if "Entrée" in self.modele.monstre_tags:
                liste_ingredients = liste_ingredients_entree
            elif "Plat" in self.modele.monstre_tags:
                liste_ingredients = liste_ingredients_plat
            elif "Dessert" in self.modele.monstre_tags:
                liste_ingredients = liste_ingredients_dessert

            #ajoute les ingredients qui sont pas dans les autres phase et qu'on a créé
            for ingredient in self.modele.liste_ingredient:
                if (ingredient not in liste_ingredients_entree and
                ingredient not in liste_ingredients_plat and
                ingredient not in liste_ingredients_dessert and
                self.modele.liste_ingredient[ingredient] != 0
                ) :
                    liste_ingredients.append(ingredient)

            # enleve les ingredients qu'on a plus de la liste d'ingredients dispo
            for ingredient in liste_ingredients:
                if self.modele.liste_ingredient[ingredient] == 0:
                    liste_ingredients.remove(ingredient)


            while True:
                try:
                    self.vue.AfficheDebutIngredientCuisineInfernale()
                    for ingredient in liste_ingredients:
                        self.vue.AfficheIngredientCuisineInfernale(numero, ingredient, self.modele.liste_ingredient[ingredient])
                        numero += 1
                    numero = 1
                    choix = self.vue.AfficheFinIngredientCuisineInfernale()
                    clear_console()
                    if choix in range(1, len(liste_ingredients) + 1):
                        break
                except ValueError:
                    clear_console()
            ingredient_un_cuisine = liste_ingredients[choix-1]

            
            if action_cuisine == "Aromatiser":
                self.vue.AfficheCommentaireIngredientCuisineAromatisationInfernale(ingredient_un_cuisine)
            elif action_cuisine not in ["Mélanger", "Cuire"]:
                self.vue.AfficheCommentaireIngredientCuisineInfernale(ingredient_un_cuisine)
        


        #     si action melanger:
        #           quantite ingredient 1 dans liste ingredient -= 1
        #           affiche menu ingredient
        #           afficher petite description action + ingredient = nouvel ingredient
        #           on enleve l'ingredient en question de la liste dingredient
        #           on rajoute le nouveau plat a la liste d'ingredient 
        if action_cuisine == "Mélanger":
            self.modele.liste_ingredient[ingredient_un_cuisine] -= 1
            #affiche menu ingredient
            numero = 1

            #ajoute les ingredients qui sont pas dans les autres phase et qu'on a créé
            for ingredient in self.modele.liste_ingredient:
                if (ingredient not in liste_ingredients_entree and
                ingredient not in liste_ingredients_plat and
                ingredient not in liste_ingredients_dessert and
                self.modele.liste_ingredient[ingredient] != 0
                ) :
                    liste_ingredients.append(ingredient)

            # enleve les ingredients qu'on a plus de la liste d'ingredients dispo
            for ingredient in liste_ingredients:
                if self.modele.liste_ingredient[ingredient] == 0:
                    liste_ingredients.remove(ingredient)


            while True:
                try:
                    self.vue.AfficheDebutIngredientCuisineInfernale()
                    for ingredient in liste_ingredients:
                        self.vue.AfficheIngredientCuisineInfernale(numero, ingredient, self.modele.liste_ingredient[ingredient])
                        numero += 1
                    numero = 1
                    choix = self.vue.AfficheFinIngredientCuisineInfernale()
                    clear_console()
                    if choix in range (1, len(liste_ingredients) + 1):
                        break
                except ValueError:
                    clear_console()
            ingredient_deux_cuisine = liste_ingredients[choix-1]

            self.vue.AfficheMelangeCuisineInfernale(ingredient_un_cuisine, ingredient_deux_cuisine)
            
            plat_cuisine = ingredient_un_cuisine + " " + adjectif_daction + " " + ingredient_deux_cuisine
            self.vue.AfficheCuisineInfernalePlatCuisine(plat_cuisine)
            self.modele.liste_ingredient[ingredient_deux_cuisine] -= 1
            if plat_cuisine in self.modele.liste_ingredient:
                self.modele.liste_ingredient[plat_cuisine] += 1
            else:
                self.modele.liste_ingredient[plat_cuisine] = 1


        #     si action cuire:
        #           on ajoute ingredient dans self modele liste cuisson avec temps = 0
        #           [dans fin tour, on augmente le temps de cuisson de tout les ingredients dans la liste de 1]
        elif action_cuisine == "Cuire":
            if ingredient_un_cuisine in self.modele.liste_cuisson:
                self.vue.AffichePerteTempsCuisineInfernale("Pour une raison quelquonque, vous ne pouvez pas mettre en cuisson deux éléments identiques.")
            else:
                self.modele.liste_cuisson[ingredient_un_cuisine] = 4
                self.modele.liste_ingredient[ingredient_un_cuisine] -= 1
                self.vue.AfficheDebutCuissonCuisineInfernale(ingredient_un_cuisine)







        #     si action enlever cuisson:
        #           on enleve ingredient de liste cuisson, et selon si le temps de cuisson est 1,2,3, on rajoute saignant, mi-cuit, bien cuit ou carbonisé
        #           afficher petite description action + ingredient = nouvel ingredient
        #           on enleve l'ingredient en question de la liste dingredient
        #           on rajoute le nouveau plat a la liste d'ingredient
        elif action_cuisine == "Arreter la cuisson":
            if len(self.modele.liste_cuisson) == 0:
                self.vue.AffichePerteTempsCuisineInfernale("Il n'y a pas de plat en cours de cuisson.")
            else:
                liste_ingredients_en_cuisson = []
                for ingredient in self.modele.liste_cuisson:
                    liste_ingredients_en_cuisson.append(ingredient)
                numero = 1
                while True:
                    try:
                        self.vue.AfficheDebutArretCuissonCuisineInfernale()
                        for ingredient in liste_ingredients_en_cuisson:
                            if self.modele.liste_cuisson[ingredient] == 3:
                                cuisson = "Bleu"
                            elif self.modele.liste_cuisson[ingredient] == 2:
                                cuisson = "Mi-Saignant"
                            elif self.modele.liste_cuisson[ingredient] == 1:
                                cuisson = "Bien Cuit"
                            else :
                                cuisson = "Carbonisé"
                            self.vue.AfficheArretCuissonCuisineInfernale(numero, ingredient, cuisson)
                            numero += 1
                        choix = self.vue.AfficheChoixArretCuissonCuisineInfernale()
                        numero = 1
                        clear_console()
                        if choix in range(1, len(liste_ingredients_en_cuisson) + 1):
                            break
                    except ValueError:
                        clear_console()
                
                # traduction de nombre a ingredient en cours de cuisson
                ingredient_a_arreter_de_cuire = liste_ingredients_en_cuisson[choix - 1]

                # commentaire 
                self.vue.AfficheIngredientArretCuissonCuisineInfernale(ingredient_a_arreter_de_cuire)
                
                #construction du plat
                if self.modele.liste_cuisson[ingredient_a_arreter_de_cuire] == 3:
                    cuisson = "Bleu"
                elif self.modele.liste_cuisson[ingredient_a_arreter_de_cuire] == 2:
                    cuisson = "Mi-Saignant"
                elif self.modele.liste_cuisson[ingredient_a_arreter_de_cuire] == 1:
                    cuisson = "Bien Cuit"
                plat_cuisine = ingredient_a_arreter_de_cuire + " " + cuisson
                

                #ajout du plat a la liste
                self.vue.AfficheCuisineInfernalePlatCuisine(plat_cuisine)
                if plat_cuisine in self.modele.liste_ingredient:
                    self.modele.liste_ingredient[plat_cuisine] += 1
                else:
                    self.modele.liste_ingredient[plat_cuisine] = 1

                #on enleve l'ingredient de la liste de cuisson
                self.modele.liste_cuisson.pop(ingredient_a_arreter_de_cuire)



        #     sinon: (action qui demandent pv pm pe)
        # frire (pv) fouetter (pe) geler (pm)
        #           si on peut enlever la monnaie en cours (pv, pm, pe):
        #                   afficher petite description action + ingredient = nouvel ingredient
        #                   on enleve l'ingredient en question de la liste dingredient
        #                   on rajoute le nouveau plat a la liste d'ingredient    
        #           sinon:
        #                   on dit que c'est pas possible, et qu'on a perdu temps  
        elif action_cuisine in ["Frire |10 pv| ", "Fouetter |10 pe| ", "Geler |10 pm| ", "Caraméliser |50% de chance de réussite| "]:
            condition_valide = True
            nombre_aleatoire_pour_caramelisation = random.randint(0, 100)
            if action_cuisine == "Frire |10 pv| " and self.modele.points_de_vie < 11 :
                condition_valide = False
                raison = "points de vie"
            elif action_cuisine == "Frire |10 pv| " and self.modele.points_de_vie >= 11:
                self.modele.points_de_vie -= 10

            if action_cuisine == "Fouetter |10 pe| " and self.modele.points_de_endurance < 11 :
                condition_valide = False
                raison = "points d'endurance"
            elif action_cuisine == "Fouetter |10 pe| " and self.modele.points_de_endurance >= 11 :
                self.modele.points_de_endurance -= 10

            if action_cuisine == "Geler |10 pm| " and self.modele.points_de_mana < 11 :
                condition_valide = False
                raison = "points de mana"
            elif action_cuisine == "Geler |10 pm| " and self.modele.points_de_mana >= 11 :
                self.modele.points_de_mana -= 10
            
            if action_cuisine == "Caraméliser |50% de chance de réussite| " and nombre_aleatoire_pour_caramelisation < 51:
                condition_valide = False
                raison = "chance"

            if condition_valide:
                plat_cuisine = ingredient_un_cuisine + " " + adjectif_daction
                self.vue.AfficheCuisineInfernalePlatCuisine(plat_cuisine)
                self.modele.liste_ingredient[ingredient_un_cuisine] -= 1
                if plat_cuisine in self.modele.liste_ingredient:
                    self.modele.liste_ingredient[plat_cuisine] += 1
                else:
                    self.modele.liste_ingredient[plat_cuisine] = 1
            else:
                self.vue.AfficheCuisinePasAssezDeCuisineInfernale(raison)
            

        #si action est normale :
        #    afficher petite description action + ingredient = nouvel ingredient
        #    on enleve l'ingredient en question de la liste dingredient
        #    on rajoute le nouveau plat a la liste d'ingredient
        else:
            plat_cuisine = ingredient_un_cuisine + " " + adjectif_daction
            self.vue.AfficheCuisineInfernalePlatCuisine(plat_cuisine)
            self.modele.liste_ingredient[ingredient_un_cuisine] -= 1
            if plat_cuisine in self.modele.liste_ingredient:
                self.modele.liste_ingredient[plat_cuisine] += 1
            else:
                self.modele.liste_ingredient[plat_cuisine] = 1
        

     

    def CuisineInfernaleCommande(self, longueur_commande, type_commande):
        if type_commande == "Entrée":
            liste_ingredient = ["Mozarella", "Tomate", "Concombre", "Rillette", "Pain", "Féta", "Saucisson"]
            liste_action = ["Coupé", "Epluché", "Lavé", "Etalé", "Grillé", "Emietté", "Sculpté"]
        elif type_commande == "Plat":
            liste_ingredient = ["Porc", "Poulet", "Haricot Vert", "Carotte", "Oignon Jaune", "Patate", "Thon", "Riz", "Pates", "Couscous"]
            liste_action = ["Désossé", "Rôti", "Carbonisé", "Bleu", "Mi-Saignant", "Bien Cuit", "Caramélisé", "Frit", "Ecrasé", "Aromatisé"]
        elif type_commande == "Dessert":
            liste_ingredient = ["Fraise", "Citron", "Ananas", "Chocolat", "Oeuf", "Beurre de Cacahuète", "Lait", "Caramel", "Vanille"]
            liste_action = ["Equeuté", "Zesté", "Rincé", "Concassé", "Compoté", "Dénoyauté", "Flambé", "Nappé", "Gelé", "Fouetté"]
        liste_type_commande = ["Ingredient", "Adjectif"]
        liste_commande = ["Ingredient"]
        commande_raw = []
        commande = ""

        #  creer liste_commande
        for _ in range(1, longueur_commande + 1):
            action_aleatoire = random.randint(0,1)
            liste_commande.append(liste_type_commande[action_aleatoire])

       # faire une liste d'ingredient et d'action a mettre ensemble
        for action in liste_commande:
            if action == "Ingredient":
                ingredient_aleatoire = random.randint(0, len(liste_ingredient) - 1)
                commande_raw.append(liste_ingredient[ingredient_aleatoire])
            elif action == "Adjectif":
                adjectif_aleatoire = random.randint(0, len(liste_action) - 1)
                commande_raw.append(liste_action[adjectif_aleatoire])

        #ajout de temps si demande cuisson ou caramélisation
        ajout_de_temps_par_cuisson = 0
        if "Carbonisé" in commande_raw:
            ajout_de_temps_par_cuisson = 4
        elif "Bleu" in commande_raw or "Caramélisé" in commande_raw:
            ajout_de_temps_par_cuisson = 1
        elif "Mi-Saignant" in commande_raw:
            ajout_de_temps_par_cuisson = 2
        elif "Bien Cuit" in commande_raw:
            ajout_de_temps_par_cuisson = 3

        #  Checker les adjectif et companie, creer la véritable commande
        commande += commande_raw[0]
        numero_action = 1
        while numero_action < len(commande_raw):
            commande += " "
            #check si avant c'était un ingredient
            if commande_raw[numero_action] in liste_ingredient:
                commande += "mélangé à "
            commande += commande_raw[numero_action]
            numero_action += 1

        # on a la commande, maintenant faut donner un temps pour la completer
        temps = longueur_commande * 2
        temps += 1
        temps += len(self.modele.monstre_commande) * 2
        temps += self.modele.nombre_de_tours
        temps += ajout_de_temps_par_cuisson

        # modificateur de temps, pour pas avoir a cuisiner h24 non plus
        temps += ajout_de_temps_par_cuisson + self.modele.nombre_de_tours + (len(self.modele.monstre_commande) * 2) + (longueur_commande * 2)

        # on rajoute la commande a la liste de commande
        self.modele.monstre_commande[commande] = temps

        # on Affiche qu'on a créé une commande
        self.vue.AfficheCuisineInfernaleCreationCommande(commande, temps)



    def EffetSuperEtoile(self):
        if self.modele.nombre_de_tours > 28:
            self.modele.monstre_points_de_vie = 0
            commentaire = "La marque du sacrifice sur le cou de l'ennemi s'active et il tombe au sol, inanimé."
            self.vue.AfficheEffetSuperEtoile(commentaire)
        elif self.modele.monstre_points_de_vie != self.modele.monstre_points_de_vie_max:
            self.modele.monstre_points_de_vie = self.modele.monstre_points_de_vie_max
            commentaire = "L'ennemi fait apparaitre un sourire tordu avant de reprendre tout ses points de vie."
            self.vue.AfficheEffetSuperEtoile(commentaire)


    def EffetTagDomovoi(self):
        if self.modele.vie_domovoi != 0:
            soin = 50 + round(self.modele.monstre_points_de_vie_max * 0.01)
            self.modele.monstre_points_de_vie += soin
            self.EquilibragePointsDeVieEtManaEtEndurance()
            commentaire = f"Le Domovoï aux cotés de l'ennemi lance un sort de soin !\nL'ennemi reprend {soin} points de vie !"
            self.vue.AfficheEffetDomovoi(commentaire)
        
    def EffetTagKikimora(self):
        if self.modele.vie_kikimora != 0:
            soin = 3
            self.modele.monstre_points_de_mana += soin
            self.EquilibragePointsDeVieEtManaEtEndurance()
            commentaire = f"La Kikimora aux cotés de l'ennemi lance un sort de transfert !\nL'ennemi reprend {soin} points de mana !"
            self.vue.AfficheEffetKikimora(commentaire)


    def EffetTagTerreur(self):
        liste_deffets_possibles = ["Vous subissez l'état [Confusion] pendant 5 tours !",
                                   "Vous subissez l'état [Dyspnée] pendant 5 tours !",
                                   "Vous subissez l'état [Blessure] pendant 5 tours !",
                                   "Vous subissez l'état [Déconcentration] pendant 5 tours !",
                                   "Vous subissez l'état [Instabilitée] pendant 5 tours !",
                                   "Vous subissez l'état [Muet] pendant 5 tours !",]
        effets_a_appliquer = []
        for _ in range(1,3):
            effet_aleatoire = random.randint(0, (len(liste_deffets_possibles) - 1))
            effets_a_appliquer.append(liste_deffets_possibles.pop(effet_aleatoire))
        for effet in effets_a_appliquer:
            if effet == "Vous subissez l'état [Confusion] pendant 5 tours !":
                self.modele.est_maudit_par_les_items = True
                self.modele.est_maudit_par_les_items_nombre_tour += 5
            elif effet == "Vous subissez l'état [Dyspnée] pendant 5 tours !":
                self.modele.est_maudit_par_endurance = True
                self.modele.est_maudit_par_endurance_nombre_tour += 5
            elif effet == "Vous subissez l'état [Blessure] pendant 5 tours !":
                self.modele.est_maudit_par_la_vie = True
                self.modele.est_maudit_par_la_vie_nombre_tour += 5
            elif effet == "Vous subissez l'état [Déconcentration] pendant 5 tours !":
                self.modele.est_maudit_par_le_mana = True
                self.modele.est_maudit_par_le_mana_nombre_tour += 5
            elif effet == "Vous subissez l'état [Instabilitée] pendant 5 tours !":
                self.modele.est_maudit_par_les_techniques = True
                self.modele.est_maudit_par_les_techniques_nombre_tour += 5
            elif effet == "Vous subissez l'état [Muet] pendant 5 tours !":
                self.modele.est_maudit_par_les_sorts = True
                self.modele.est_maudit_par_les_sorts_nombre_tour += 5
        self.vue.AfficheEffetTerreur(effets_a_appliquer)

    def EffetTagFausseTerreur(self):
        liste_deffets_possibles = ["Vous subissez l'état [Confusion] pendant 5 tours !",
                                   "Vous subissez l'état [Dyspnée] pendant 5 tours !",
                                   "Vous subissez l'état [Blessure] pendant 5 tours !",
                                   "Vous subissez l'état [Déconcentration] pendant 5 tours !",
                                   "Vous subissez l'état [Instabilitée] pendant 5 tours !",
                                   "Vous subissez l'état [Muet] pendant 5 tours !",]
        effets_a_appliquer = []
        effet_aleatoire = random.randint(0, (len(liste_deffets_possibles) - 1))
        effets_a_appliquer.append(liste_deffets_possibles.pop(effet_aleatoire))
        for effet in effets_a_appliquer:
            if effet == "Vous subissez l'état [Confusion] pendant 5 tours !":
                self.modele.est_maudit_par_les_items = True
                self.modele.est_maudit_par_les_items_nombre_tour += 5
            elif effet == "Vous subissez l'état [Dyspnée] pendant 5 tours !":
                self.modele.est_maudit_par_endurance = True
                self.modele.est_maudit_par_endurance_nombre_tour += 5
            elif effet == "Vous subissez l'état [Blessure] pendant 5 tours !":
                self.modele.est_maudit_par_la_vie = True
                self.modele.est_maudit_par_la_vie_nombre_tour += 5
            elif effet == "Vous subissez l'état [Déconcentration] pendant 5 tours !":
                self.modele.est_maudit_par_le_mana = True
                self.modele.est_maudit_par_le_mana_nombre_tour += 5
            elif effet == "Vous subissez l'état [Instabilitée] pendant 5 tours !":
                self.modele.est_maudit_par_les_techniques = True
                self.modele.est_maudit_par_les_techniques_nombre_tour += 5
            elif effet == "Vous subissez l'état [Muet] pendant 5 tours !":
                self.modele.est_maudit_par_les_sorts = True
                self.modele.est_maudit_par_les_sorts_nombre_tour += 5
        self.vue.AfficheEffetFausseTerreur(effets_a_appliquer)

    def EffetStigmaCircuitsLogiques(self):
        if self.modele.points_de_vie < round(self.modele.points_de_vie_max * 0.05):
            self.modele.InCombat = False
            self.modele.type_de_derniere_action_utilisee = "Fuir"
            self.vue.AfficheCircuitsLogiques()

    def FinTour(self):
        # applique/affiche les alteration d'état et diminue leur
        # tours d'application de 1.
        self.AppliqueEtMetAJourAlterationEtat()
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

    def ConstruirePhraseAlterationEtatPourVue(self):
        # construction d'une liste d'alteration subies par le joueur
        phrase_joueur = ""
        liste_alteration_joueur = []
        if self.modele.utilise_posture_de_la_montagne:
            liste_alteration_joueur.append("[Montagne]")
        if self.modele.utilise_pousse_adrenaline:
            liste_alteration_joueur.append("[Adrénaline]")
        if self.modele.metamorphose:
            liste_alteration_joueur.append("[Métamorphose]")
        if self.modele.utilise_mirroir_eau:
            liste_alteration_joueur.append("[Réflexion]")
        if self.modele.utilise_brume_sang:
            liste_alteration_joueur.append("[Brouillard]")
        if self.modele.est_en_feu:
            liste_alteration_joueur.append("[Brûlure]")
        if self.modele.est_gele:
            liste_alteration_joueur.append("[Gelure]")
        if self.modele.est_paralyse:
            liste_alteration_joueur.append("[Paralysie]")
        if self.modele.beni_par_feu_sacre:
            liste_alteration_joueur.append("[Béni]")
        if self.modele.miss_hyde_transformation:
            liste_alteration_joueur.append("[Malédiction des Hyde]")
        if self.modele.mauvais_tachyon:
            liste_alteration_joueur.append(f"[Charge Tachyon Instable : {self.modele.charge_mauvais_tachyon}]")
        if self.modele.bon_tachyon:
            liste_alteration_joueur.append(f"[Accumulateur de Tachyon : {self.modele.charge_bon_tachyon}]")
        if self.modele.concentre:
            liste_alteration_joueur.append("[Concentration]")
        if self.modele.est_maudit_par_le_gold:
            liste_alteration_joueur.append("[Mal Jaune]")
        if self.modele.est_maudit_par_la_vie:
            liste_alteration_joueur.append("[Blessure]")
        if self.modele.est_maudit_par_le_mana:
            liste_alteration_joueur.append("[Déconcentration]")
        if self.modele.est_maudit_par_les_techniques:
            liste_alteration_joueur.append("[Instabilitée]")
        if self.modele.est_maudit_par_les_sorts:
            liste_alteration_joueur.append("[Muet]")
        if self.modele.est_maudit_par_les_items:
            liste_alteration_joueur.append("[Confusion]")
        if self.modele.est_maudit_par_endurance:
            liste_alteration_joueur.append("[Dyspnée]")
        if self.modele.est_enpoisonne:
            liste_alteration_joueur.append("[Poison]")
        if self.modele.utilise_ambroisie:
            liste_alteration_joueur.append("[Ambroisie]")
        if self.modele.utilise_hydromel:
            liste_alteration_joueur.append("[Hydromel]")
        if self.modele.utilise_feuille_jindagee or self.modele.utilise_fruit_jindagee:
            liste_alteration_joueur.append("[Jindagee]")
        if self.modele.utilise_feuille_aatma or self.modele.utilise_fruit_aatma:
            liste_alteration_joueur.append("[Aatma]")
        if self.modele.utilise_rafale:
            liste_alteration_joueur.append("[Rafale]")
        if self.modele.utilise_orbe_de_folie:
            liste_alteration_joueur.append("[Folie]")
        if self.modele.utilise_orbe_de_furie:
            liste_alteration_joueur.append("[Furie]")
        if "Element [Glace] Surchargé" in self.modele.liste_dartefacts_optionels:
            liste_alteration_joueur.append("[Element {Glace} Surchargé]")
        if "Element [Foudre] Surchargé" in self.modele.liste_dartefacts_optionels:
            liste_alteration_joueur.append("[Element {Foudre} Surchargé]")
        if "Element [Feu] Surchargé" in self.modele.liste_dartefacts_optionels:
            liste_alteration_joueur.append("[Element {Feu} Surchargé]")
        if "Element [Terre] Surchargé" in self.modele.liste_dartefacts_optionels:
            liste_alteration_joueur.append("[Element {Terre} Surchargé]")
        if "Element [Sang] Surchargé" in self.modele.liste_dartefacts_optionels:
            liste_alteration_joueur.append("[Element {Sang} Surchargé]")
        if "Element [Corps] Surchargé" in self.modele.liste_dartefacts_optionels:
            liste_alteration_joueur.append("[Element {Corps} Surchargé]")
        if "Element [Ame] Surchargé" in self.modele.liste_dartefacts_optionels:
            liste_alteration_joueur.append("[Element {Ame} Surchargé]")
        if "Canigou" in self.modele.liste_dartefacts_optionels:
            liste_alteration_joueur.append("[Canigou]")
        if self.modele.mutagene_bleu_utilise or self.modele.grand_mutagene_bleu_utilise:
            liste_alteration_joueur.append("[Teinte de Saphir]")
        if self.modele.mutagene_vert_utilise or self.modele.grand_mutagene_vert_utilise:
            liste_alteration_joueur.append("[Teinte d'Emeraude]")
        if (
            self.modele.mutagene_rouge_utilise
            or self.modele.grand_mutagene_rouge_utilise
        ):
            liste_alteration_joueur.append("[Teinte de Rubis]")
        if self.modele.mutagene_dore_utilise or self.modele.grand_mutagene_dore_utilise:
            liste_alteration_joueur.append("[Teinte Dorée]")
        if self.modele.mutagene_heretique_utilise:
            liste_alteration_joueur.append("[Teinte Hérétique]")
        if self.modele.mutagene_fanatique_utilise:
            liste_alteration_joueur.append("[Teinte Fanatique]")
        if self.modele.accumulation_degat_technique != 0:
            liste_alteration_joueur.append(f"[Dégâts Techniques +{self.modele.accumulation_degat_technique}%]")
        if self.modele.accumulation_degat_sort != 0:
            liste_alteration_joueur.append(f"[Dégâts Sorts +{self.modele.accumulation_degat_sort}%]")
        if self.modele.accumulation_degat_technique_critique != 0:
            liste_alteration_joueur.append(f"[Dégâts Crit. Techniques +{self.modele.accumulation_degat_technique_critique}]")
        if self.modele.accumulation_degat_sort_critique != 0:
            liste_alteration_joueur.append(f"[Dégâts Crit. Sorts +{self.modele.accumulation_degat_sort_critique}]")
        if self.modele.accumulation_chance_brulure != 0:
            liste_alteration_joueur.append(f"[Chances de Brûler +{self.modele.accumulation_chance_brulure}%]")
        if self.modele.accumulation_chance_gelure != 0:
            liste_alteration_joueur.append(f"[Chances de Geler +{self.modele.accumulation_chance_gelure}%]")
        if self.modele.accumulation_chance_paralysie != 0:
            liste_alteration_joueur.append(f"[Chances de Paralyser +{self.modele.accumulation_chance_paralysie}%]")
        if self.modele.accumulation_chance_lapider != 0:
            liste_alteration_joueur.append(f"[Chances de Lapider +{self.modele.accumulation_chance_lapider}%]")
        if self.modele.accumulation_chance_drainer != 0:
            liste_alteration_joueur.append(f"[Chances de Drainer +{self.modele.accumulation_chance_drainer}%]")
        # construction de la phrase a montrer
        # switch true =) rajoute l'alteration detat + espace
        # switch false =) rajouter alteration detat + retour a la ligne
        if len(liste_alteration_joueur) == 0:
            phrase_joueur = "     | Aucune altération d'état |"
        else:
            phrase_joueur = "  "
            switch = True
            for etat in liste_alteration_joueur:
                if switch:
                    phrase_joueur += "| "
                    phrase_joueur += etat
                    phrase_joueur += " |"
                    switch = False
                else:
                    phrase_joueur = phrase_joueur.rstrip("|")
                    phrase_joueur += etat
                    phrase_joueur += " |\n  "
                    switch = True
            if switch:
                phrase_joueur = phrase_joueur.rstrip("\n ")

        # construction d'une liste d'alteration subies par L'ennemi
        phrase_monstre = ""
        liste_alteration_monstre = []
        if self.modele.monstre_EstUnBoss:
            liste_alteration_monstre.append("[Boss]")
        if self.modele.monstre_est_en_feu:
            liste_alteration_monstre.append("[Brûlure]")
        if self.modele.luciole_etat:
            liste_alteration_monstre.append("[Feu Electrique]")
        if self.modele.vie_domovoi != 0 and "Domovoï" in self.modele.monstre_tags:
            liste_alteration_monstre.append("[Domovoï]")
        if "Voluntad Káak" in self.modele.monstre_tags:
            liste_alteration_monstre.append("[Voluntad Káak]")
        if "Voluntad Hielo" in self.modele.monstre_tags:
            liste_alteration_monstre.append("[Voluntad Hielo]")
        if "Voluntad Le Rayo" in self.modele.monstre_tags:
            liste_alteration_monstre.append("[Voluntad Le Rayo]")
        if "Voluntad Le Luumo" in self.modele.monstre_tags:
            liste_alteration_monstre.append("[Voluntad Le Luumo]")
        if "Voluntad U Kiikel" in self.modele.monstre_tags:
            liste_alteration_monstre.append("[Voluntad U Kiikel]")
        if "Voluntad U Wíinkilal" in self.modele.monstre_tags:
            liste_alteration_monstre.append("[Voluntad U Wíinkilal]")
        if "Voluntad Tin Tuukul" in self.modele.monstre_tags:
            liste_alteration_monstre.append("[Voluntad Tin Tuukul]")
        if self.modele.vie_kikimora != 0 and "Kikimora" in self.modele.monstre_tags:
            liste_alteration_monstre.append("[Kikimora]")
        if len(self.modele.monstre_commande) != 0:
            for commande in self.modele.monstre_commande:
                commentaire_alteration_etat = f"[{commande} : Tour {self.modele.monstre_commande[commande]}]"
                liste_alteration_monstre.append(commentaire_alteration_etat)
        if self.modele.monstre_est_gele:
            liste_alteration_monstre.append("[Gelure]")
        if self.modele.monstre_est_maudit:
            liste_alteration_monstre.append("[Maudit]")
        if self.modele.monstre_est_paralyse:
            liste_alteration_monstre.append("[Paralysie]")
        if self.modele.monstre_est_vulnerable:
            liste_alteration_monstre.append("[Vulnérable]")
        if self.modele.monstre_est_empoisonne:
            liste_alteration_monstre.append("[Poison]")
        if self.modele.monstre_est_regeneration:
            liste_alteration_monstre.append("[Regeneration]")
        if self.modele.monstre_est_service:
            liste_alteration_monstre.append("[En Plein Service]")
        if self.modele.monstre_gain_de_defence:
            liste_alteration_monstre.append("[Durcissement]")
        if self.modele.monstre_est_envol:
            liste_alteration_monstre.append("[Envol]")
        if self.modele.monstre_en_etat_de_choc:
            liste_alteration_monstre.append("[Etat de Choc]")
        # construction de la phrase a montrer
        # switch true =) rajoute l'alteration detat + espace
        # switch false =) rajouter alteration detat + retour a la ligne
        if len(liste_alteration_monstre) == 0:
            phrase_monstre = "     | Aucune altération d'état |"
        else:
            phrase_monstre = "  "
            switch = True
            for etat in liste_alteration_monstre:
                if switch:
                    phrase_monstre += "| "
                    phrase_monstre += etat
                    phrase_monstre += " |"
                    switch = False
                else:
                    phrase_monstre = phrase_monstre.rstrip("|")
                    phrase_monstre += etat
                    phrase_monstre += " |\n  "
                    switch = True
            if switch:
                phrase_monstre = phrase_monstre.rstrip("\n ")
        return phrase_monstre, phrase_joueur

    def DefinitionAlterationDesActionsPourAffichage(self):
        alteration_technique = ""
        if len(self.modele.techniques) == 0:
            alteration_technique = "[Aucun]"
        elif self.modele.est_maudit_par_les_techniques:
            alteration_technique = "[Impossible]"
        elif self.modele.est_maudit_par_le_gold and self.modele.est_maudit_par_la_vie:
            alteration_technique = "[Coûte du gold et de la vie]"
        elif self.modele.est_maudit_par_le_gold:
            alteration_technique = "[Coûte du gold]"
        elif self.modele.est_maudit_par_la_vie:
            alteration_technique = "[Attention, Blessé !]"
        alteration_sort = ""
        if len(self.modele.sorts) == 0:
            alteration_sort = "[Aucun]"
        elif self.modele.est_maudit_par_les_sorts:
            alteration_sort = "[Impossible]"
        elif self.modele.est_maudit_par_le_gold and self.modele.est_maudit_par_le_mana:
            alteration_sort = "[Coûte du gold et plus de mana]"
        elif self.modele.est_maudit_par_le_gold:
            alteration_sort = "[Coûte du gold]"
        elif self.modele.est_maudit_par_le_mana:
            alteration_sort = "[Attention, Déconcentré !]"
        alteration_item = ""
        if len(self.modele.liste_des_items) == 0:
            alteration_item = "[Aucun]"
        elif self.modele.est_maudit_par_les_items:
            alteration_item = "[Impossible]"
        alteration_fuite = ""
        if self.modele.stigma_joueur_negatif == "Pas d'Echappatoire":
            alteration_fuite = "[Impossible]"
        return (
            alteration_technique,
            alteration_sort,
            alteration_item,
            alteration_fuite,
        )

    def ConstructionAffichageCoutSort(self, action):
        affichage_cout = ""
        cout = self.CoutEnManaDuSort(action)
        affichage_cout += f"{cout} PM"
        if self.modele.est_maudit_par_le_gold:
            affichage_cout += f" et {cout * 2} GOLD"
        if self.modele.est_maudit_par_les_sorts:
            affichage_cout = "Impossible"
        return affichage_cout

    def ConstructionAffichageCoutTechnique(self, action):
        cout_endurance = self.modele.annuaire_de_cout_des_techniques[action]
        affichage_cout = f"{cout_endurance} PE"
        cout_pourcentage = self.modele.BONUSCOUTMALEDICTIONVIEOUGOLD
        cout = round(self.modele.points_de_vie_max * (cout_pourcentage / 100))
        if self.modele.est_maudit_par_la_vie and self.modele.est_maudit_par_le_gold:
            affichage_cout += f" {cout} PV et {cout} GOLD"
        elif self.modele.est_maudit_par_la_vie:
            affichage_cout += f" {cout} PV"
        elif self.modele.est_maudit_par_le_gold:
            affichage_cout += f" {cout} GOLD"
        if self.modele.est_maudit_par_les_techniques:
            affichage_cout = "Impossible"
        return affichage_cout

    def ConstructionAffichageCoutItems(self, action):
        affichage_cout = ""
        if self.modele.est_maudit_par_les_items:
            affichage_cout = "Impossible"
        return affichage_cout

    def UseAttack(self, action):
        # [0]=%touche, [1]=degat, [2]=%crit, [3]=degat crit, [4]=%element,
        # [5]=description, [6]=message si rate, [7]=si touche, [8]=si touche crit
        # [9]=nombre tours, [10]=effet element
        action = self.EnleveurAffix(action, True)
        # regarde l'élément de l'action pour les bonus associés
        self.SetTypeOfAction(action)
        # l'action est elle possible ? Applique le cout de l'action
        action_est_possible, raison_si_action_pas_possible = (
            self.CheckSiAttaquePossibleEtAppliqueCoutAttaque(action)
        )
        if action_est_possible:
            if self.modele.mauvais_tachyon:
                self.ChangeChargeMauvaisTachyon("attaque")
            if self.modele.bon_tachyon:
                self.ChangeChargeBonTachyon("attaque")
            if self.Player.quete == "Moqueries Techniques" and self.modele.monstre_EstUnBoss:
                self.Player.quete = "Moqueries Techniques [Echec]"   
            # methode globale pour les attaques
            if action in self.modele.annuaire_de_caracteristique_des_techniques:
                caracteristique_du_techniques = (
                    self.modele.annuaire_de_caracteristique_des_techniques[action]
                )
                # application des modificateurs sur la chance de toucher
                pourcentage_de_touche = caracteristique_du_techniques[0]
                pourcentage_de_touche -= self.modele.CHANCERATERATTAQUE
                pourcentage_de_touche += self.modele.CHANCEDETOUCHERBONUS
                # application des modificateurs sur les degats de base
                degat_de_base = caracteristique_du_techniques[1]
                pourcentage = self.modele.DEGATBONUSATTAQUE
                if self.modele.a_utilise_feu_ce_tour:
                    pourcentage += self.modele.DEGATBONUSATTAQUEFEU
                elif self.modele.a_utilise_foudre_ce_tour:
                    pourcentage += self.modele.DEGATBONUSATTAQUEFOUDRE
                elif self.modele.a_utilise_terre_ce_tour:
                    pourcentage += self.modele.DEGATBONUSATTAQUETERRE
                elif self.modele.a_utilise_physique_ce_tour:
                    pourcentage += self.modele.DEGATBONUSATTAQUEPHYSIQUE
                elif self.modele.a_utilise_sang_ce_tour:
                    pourcentage += self.modele.DEGATBONUSATTAQUESANG
                elif self.modele.a_utilise_glace_ce_tour:
                    pourcentage += self.modele.DEGATBONUSATTAQUEGLACE
                degat_de_base += round(
                    (pourcentage / 100) * degat_de_base
                )
                degat_de_base -= round(
                    (self.modele.BONUSREDUCTIONDEGAT / 100) * degat_de_base
                )
                # application des modificateurs sur les chances de coup critique
                pourcentage_de_critique = caracteristique_du_techniques[2]
                pourcentage_de_critique += self.modele.CHANCECOUPCRITIQUE
                # application des modificateurs sur les degats de coup critique
                degat_critique = caracteristique_du_techniques[3]
                degat_critique += round(
                    (self.modele.DEGATBONUSATTAQUECRITIQUE / 100) * degat_critique
                )
                degat_critique += round(self.modele.accumulation_degat_technique_critique)
                # application des modificateurs sur les chances d'appliquer un element
                pourcentage_de_element = caracteristique_du_techniques[4]
                if self.modele.a_utilise_feu_ce_tour:
                    pourcentage_de_element += self.modele.CHANCEBONUSDEFAIREBRULER
                elif self.modele.a_utilise_foudre_ce_tour:
                    pourcentage_de_element += self.modele.CHANCEBONUSDEFAIREPARALYSER
                elif self.modele.a_utilise_terre_ce_tour:
                    pourcentage_de_element += self.modele.CHANCEBONUSDEFAIRELAPIDER
                elif self.modele.a_utilise_sang_ce_tour:
                    pourcentage_de_element += self.modele.CHANCEBONUSDEFAIRESAIGNER
                elif self.modele.a_utilise_glace_ce_tour:
                    pourcentage_de_element += self.modele.CHANCEBONUSDEFAIREGELER
                description = caracteristique_du_techniques[5]
                nombre_aleatoire = random.randint(0, 100)
                degat = 0
                if nombre_aleatoire < pourcentage_de_touche:
                    commentaire_element = ""
                    commentaire_a_afficher = caracteristique_du_techniques[7]
                    degat += degat_de_base
                    # ca fait un critique ?
                    if nombre_aleatoire < pourcentage_de_critique:
                        commentaire_a_afficher = caracteristique_du_techniques[8]
                        degat += degat_critique
                        if "Pièce Fondue" in self.modele.liste_dartefacts_optionels:
                            commentaire_a_afficher += "\nL'artefact [Pièce Fondue] maudit l'ennemi !"
                            self.modele.monstre_est_maudit = True
                            self.modele.monstre_est_maudit_nombre_tour += 2
                    # ca declenche  un effet elementaire ?
                    if nombre_aleatoire < pourcentage_de_element:
                        # si oui, quel effet ?
                        if self.modele.a_utilise_feu_ce_tour:
                            # deja en feu ?
                            if self.modele.monstre_est_en_feu:
                                nombre_aleatoire = random.randint(1, 100)
                                if nombre_aleatoire <= 90:
                                    # addition des tours
                                    nombre_tour = caracteristique_du_techniques[9]
                                    nombre_tour += self.modele.TOURBONUSENNEMIENFEU
                                    if self.modele.stigma_monstre_negatif == "Inflammable":
                                        nombre_tour += nombre_tour
                                    if self.modele.utilise_rafale:
                                        nombre_tour += nombre_tour
                                    self.modele.monstre_est_en_feu_nombre_tour += (
                                        nombre_tour
                                    )
                                    # ajustement des degats
                                    degat_du_feu = caracteristique_du_techniques[10]
                                    if (
                                        self.modele.monstre_est_en_feu_degat
                                        < degat_du_feu
                                    ):
                                        self.modele.monstre_est_en_feu_degat = (
                                            degat_du_feu
                                        )
                                    commentaire_element = f"\nVous enflammez l'ennemi pour {nombre_tour} tours supplémentaires !"
                                else:
                                    # finition des degats
                                    pourcentage_degat_du_feu = (
                                        self.modele.monstre_est_en_feu_nombre_tour
                                        * (
                                            self.modele.monstre_est_en_feu_degat
                                            + self.modele.DEGATBONUSFEU
                                        )
                                    )
                                    degat_du_feu = round(
                                        pourcentage_degat_du_feu
                                        * self.modele.monstre_points_de_vie_max
                                    )
                                    degat_du_feu = self.SiZeroRameneAUn(degat_du_feu)
                                    self.modele.monstre_points_de_vie -= degat_du_feu
                                    # arret du feu
                                    self.modele.monstre_est_en_feu_nombre_tour = 0
                                    self.modele.monstre_est_en_feu_degat = 0
                                    self.modele.monstre_est_en_feu = False
                                    # paralysie
                                    self.modele.monstre_est_paralyse = True
                                    self.modele.monstre_est_paralyse_nombre_tour = 2
                                    # construction du comentaire_element
                                    commentaire_element = ("\nVous enflammez l'ennemi.\nCepandant, les"
                                                       " deux feux s'éteignent mutuellement en"
                                                       " consommant l'oxygène disponible, et lui "
                                                       "font de gros dégâts.\nDe plus, le choc le "
                                                       "paralyse !")
                            else:
                                # mise a feu du monstre
                                self.modele.monstre_est_en_feu = True
                                nombre_tour = caracteristique_du_techniques[9]
                                nombre_tour += self.modele.TOURBONUSENNEMIENFEU
                                if self.modele.stigma_monstre_negatif == "Inflammable":
                                    nombre_tour += nombre_tour
                                if self.modele.utilise_rafale:
                                    nombre_tour += nombre_tour
                                self.modele.monstre_est_en_feu_nombre_tour += (
                                    nombre_tour
                                )
                                self.modele.monstre_est_en_feu_degat = (
                                    caracteristique_du_techniques[10]
                                )
                                commentaire_element = f"\nVous enflammez l'ennemi pendant {nombre_tour} tours !"
                        if self.modele.a_utilise_foudre_ce_tour:
                            if self.modele.stigma_monstre_positif == "Hardi":
                                commentaire_element = f"\nL'ennemi résiste a la paralysie !"
                            else:
                                self.modele.monstre_est_paralyse = True
                                self.modele.monstre_passe_son_tour = True
                                nombre_tour_para = caracteristique_du_techniques[9] + self.modele.TOURBONUSENNEMIENPARALYSIE
                                self.modele.monstre_est_paralyse_nombre_tour += (
                                    nombre_tour_para
                                )
                                commentaire_element = f"\nVous paralysez l'ennemi pendant {nombre_tour_para} tours !"
                        if self.modele.a_utilise_glace_ce_tour:
                            nombre_tour_gele = caracteristique_du_techniques[9] + self.modele.TOURBONUSENNEMIENGLACE
                            self.modele.monstre_est_gele = True
                            self.modele.monstre_est_gele_nombre_tour += (
                                nombre_tour_gele
                            )
                            commentaire_element = f"\nVous gelez l'ennemi pendant {nombre_tour_gele} tours !"
                            if nombre_tour_gele <= 0 :
                                commentaire_element = "De part son origine nordique, l'ennemi résiste au gel infligé !"
                                self.modele.monstre_est_gele = False
                                self.modele.monstre_est_gele_nombre_tour = 0
                        if self.modele.a_utilise_sang_ce_tour:
                            if ("Voluntad U Kiikel") in self.modele.monstre_tags:
                                commentaire_degat = f"\nVoluntad U Kiikel, l'esprit de sang, absorbe le drain de vie infligé à {self.modele.monstre_nom} !"
                            else:
                                # calcul de la saignee
                                pourcentage_saignee = caracteristique_du_techniques[10]
                                pourcentage_saignee += self.modele.DEGATSAIGNEE
                                degat_saignee = round(
                                    (pourcentage_saignee / 100)
                                    * self.modele.monstre_points_de_vie_max
                                )
                                degat_saignee = self.AppliqueLimitationSaignee(degat_saignee)
                                # application de la saignee
                                self.modele.monstre_points_de_vie -= degat_saignee
                                soin_saignee = degat_saignee
                                soin_saignee += round(
                                    (self.modele.SOINSSAIGNEE / 100) * degat_saignee
                                )
                                self.modele.points_de_vie += soin_saignee
                                self.EquilibragePointsDeVieEtManaEtEndurance()
                                commentaire_element = f"\nVous drainez {degat_saignee} points de vie a l'adversaire, et en récuperez {soin_saignee} !"
                                if self.modele.anemie:
                                    commentaire_element += self.AppliqueTalentAnemie()
                                if self.modele.baron_rouge:
                                    commentaire_element += self.AppliqueTalentBaronRouge()
                                if self.modele.anticoagulants:
                                    degat_saignement = round(degat * 0.2)
                                    self.modele.monstre_points_de_vie -= degat_saignement
                                    commentaire_element += f"\nVous infligez {degat_saignement} points de vie a l'adversaire par saignement !"
                        if self.modele.a_utilise_terre_ce_tour:
                            # calcul de lapidation
                            pourcentage_lapidation = caracteristique_du_techniques[10]
                            pourcentage_lapidation += self.modele.DEGATLAPIDATION
                            degat_lapidation = round(
                                (pourcentage_lapidation / 100) * degat
                            )
                            # application lapidation
                            degat_lapidation = self.SiZeroRameneAUn(degat_lapidation)
                            if ("Voluntad Le Luumo") in self.modele.monstre_tags:
                                commentaire_element += f"\nVoluntad Le Luumo, l'esprit de terre, absorbe la lapidation infligée sur {self.modele.monstre_nom} !"
                            else:
                                self.modele.monstre_points_de_vie -= degat_lapidation
                                # construction du comentaire_element
                                commentaire_element = f"\nVous infligez {degat_lapidation} points de vie supplémentaire par lapidation !"
                                if self.modele.eboulis:
                                    commentaire_element += self.AppliqueTalentEboulis(degat_lapidation)
                                if self.modele.fracturation:
                                    commentaire_element += self.AppliqueTalentFracturation()
                    nombre_aleatoire_basique = random.randint(0, 100)
                    if "Utilise Feu Basique" in self.modele.player_tags:
                        self.modele.player_tags.remove("Utilise Feu Basique")
                        if nombre_aleatoire_basique <= 17:
                            if self.modele.monstre_est_en_feu:
                                nombre_aleatoire = random.randint(1, 100)
                                if nombre_aleatoire <= 90:
                                    # addition des tours
                                    nombre_tour = 4
                                    nombre_tour += self.modele.TOURBONUSENNEMIENFEU
                                    if self.modele.stigma_monstre_negatif == "Inflammable":
                                        nombre_tour += nombre_tour
                                    if self.modele.utilise_rafale:
                                        nombre_tour += nombre_tour
                                    self.modele.monstre_est_en_feu_nombre_tour += (
                                        nombre_tour
                                    )
                                    commentaire_element = f"\nVous enflammez l'ennemi pour {nombre_tour} tours supplémentaires !"
                                    # ajustement des degats
                                    degat_du_feu = 7
                                    if (
                                        self.modele.monstre_est_en_feu_degat
                                        < degat_du_feu
                                    ):
                                        self.modele.monstre_est_en_feu_degat = (
                                            degat_du_feu
                                        )
                                else:
                                    # finition des degats
                                    pourcentage_degat_du_feu = (
                                        self.modele.monstre_est_en_feu_nombre_tour
                                        * (
                                            self.modele.monstre_est_en_feu_degat
                                            + self.modele.DEGATBONUSFEU
                                        )
                                    )
                                    degat_du_feu = round(
                                        pourcentage_degat_du_feu
                                        * self.modele.monstre_points_de_vie_max
                                    )
                                    degat_du_feu = self.SiZeroRameneAUn(degat_du_feu)
                                    self.modele.monstre_points_de_vie -= degat_du_feu
                                    # arret du feu
                                    self.modele.monstre_est_en_feu_nombre_tour = 0
                                    self.modele.monstre_est_en_feu_degat = 0
                                    self.modele.monstre_est_en_feu = False
                                    # paralysie
                                    self.modele.monstre_est_paralyse = True
                                    self.modele.monstre_est_paralyse_nombre_tour = 2
                                    # construction du comentaire_element
                                    commentaire_element = ("\nVous enflammez l'ennemi.\nCepandant, les"
                                                        " deux feux s'éteignent mutuellement en"
                                                        " consommant l'oxygène disponible, et lui "
                                                        "font de gros dégâts.\nDe plus, le choc le "
                                                        "paralyse !")
                            else:
                                # mise a feu du monstre
                                self.modele.monstre_est_en_feu = True
                                nombre_tour = 4
                                nombre_tour += self.modele.TOURBONUSENNEMIENFEU
                                if self.modele.stigma_monstre_negatif == "Inflammable":
                                    nombre_tour += nombre_tour
                                if self.modele.utilise_rafale:
                                    nombre_tour += nombre_tour
                                self.modele.monstre_est_en_feu_nombre_tour += (
                                    nombre_tour
                                )
                                self.modele.monstre_est_en_feu_degat = (
                                    7
                                )

                                commentaire_element = f"\nVous enflammez l'ennemi pendant {nombre_tour} tours !"
                    elif "Utilise Glace Basique" in self.modele.player_tags:
                        self.modele.player_tags.remove("Utilise Glace Basique")
                        if nombre_aleatoire_basique <= 17:
                            self.modele.monstre_est_gele = True
                            nombre_tour_gele = 3 + self.modele.TOURBONUSENNEMIENGLACE
                            self.modele.monstre_est_gele_nombre_tour += (
                                nombre_tour_gele
                            )
                            commentaire_element = f"\nVous gelez l'ennemi pendant {nombre_tour_gele} tours !"
                            if nombre_tour_gele <= 0 :
                                commentaire_element = "De part son origine nordique, l'ennemi résiste au gel infligé !"
                                self.modele.monstre_est_gele = False
                                self.modele.monstre_est_gele_nombre_tour = 0
                    elif "Utilise Terre Basique" in self.modele.player_tags:
                        self.modele.player_tags.remove("Utilise Terre Basique")
                        if nombre_aleatoire_basique <= 12:
                            # calcul de lapidation
                            pourcentage_lapidation = 85
                            pourcentage_lapidation += self.modele.DEGATLAPIDATION
                            degat_lapidation = round(
                                (pourcentage_lapidation / 100) * degat
                            )
                            # application lapidation
                            degat_lapidation= self.SiZeroRameneAUn(degat_lapidation)
                            if ("Voluntad Le Luumo") in self.modele.monstre_tags:
                                commentaire_degat += f"\nVoluntad Le Luumo, l'esprit de terre, absorbe la lapidation infligée sur {self.modele.monstre_nom} !"
                            else:
                                self.modele.monstre_points_de_vie -= degat_lapidation
                                # construction du comentaire_element
                                commentaire_element = f"\nVous infligez {degat_lapidation} points de vie supplémentaire par lapidation !"
                                if self.modele.eboulis:
                                    commentaire_element += self.AppliqueTalentEboulis(degat_lapidation)
                                if self.modele.fracturation:
                                    commentaire_element += self.AppliqueTalentFracturation()
                    elif "Utilise Foudre Basique" in self.modele.player_tags:
                        if nombre_aleatoire_basique <= 7:
                            self.modele.player_tags.remove("Utilise Foudre Basique")
                            if self.modele.stigma_monstre_positif == "Hardi":
                                commentaire_element = f"\nL'ennemi résiste a la paralysie !"
                            else:
                                self.modele.monstre_est_paralyse = True
                                self.modele.monstre_passe_son_tour = True
                                nombre_tour_para = 2 + self.modele.TOURBONUSENNEMIENPARALYSIE
                                self.modele.monstre_est_paralyse_nombre_tour += (
                                    nombre_tour_para
                                )
                                commentaire_element = f"\nVous paralysez l'ennemi pendant {nombre_tour_para} tours !"
                    elif "Utilise Sang Basique" in self.modele.player_tags:
                        self.modele.player_tags.remove("Utilise Sang Basique")
                        if nombre_aleatoire_basique <= 15:
                            if ("Voluntad U Kiikel") in self.modele.monstre_tags:
                                commentaire_degat = f"\nVoluntad U Kiikel, l'esprit de sang, absorbe le drain de vie infligé à {self.modele.monstre_nom} !"
                            else:
                                # calcul de la saignee
                                pourcentage_saignee = 3
                                pourcentage_saignee += self.modele.DEGATSAIGNEE
                                degat_saignee = round(
                                    (pourcentage_saignee / 100)
                                    * self.modele.monstre_points_de_vie_max
                                )
                                degat_saignee = self.AppliqueLimitationSaignee(degat_saignee)
                                # application de la saignee
                                self.modele.monstre_points_de_vie -= degat_saignee
                                soin_saignee = degat_saignee
                                soin_saignee += round(
                                    (self.modele.SOINSSAIGNEE / 100) * degat_saignee
                                )
                                self.modele.points_de_vie += soin_saignee
                                self.EquilibragePointsDeVieEtManaEtEndurance()
                                commentaire_element = f"\nVous drainez {degat_saignee} points de vie a l'adversaire, et en récuperez {soin_saignee} !"
                                if self.modele.anemie:
                                    commentaire_element += self.AppliqueTalentAnemie()
                                if self.modele.baron_rouge:
                                    commentaire_element += self.AppliqueTalentBaronRouge()
                                if self.modele.anticoagulants:
                                    degat_de_saignement = round(degat * 0.2)
                                    self.modele.monstre_points_de_vie -= degat_de_saignement
                                    commentaire_element += f"\nVous infligez {degat_de_saignement} points de vie a l'adversaire par saignement !"
                    degat = self.SiZeroRameneAUn(degat)
                    commentaire_degat = (
                        f"Vous infligez {degat} points de dégât a l'ennemi !"
                    )
                    commentaire_degat += commentaire_element
                    self.modele.monstre_points_de_vie -= degat
                    if self.modele.oeuil_magique:
                        commentaire_degat += self.AppliqueTalentOeuilMagique()
                    self.vue.AfficheSonTechnique(self.sound_of_action)
                else:
                    commentaire_a_afficher = caracteristique_du_techniques[6]
                    commentaire_degat = "Vous n'infligez aucun degat a l'ennemi."
                    commentaire_element = ""
                self.vue.AfficheSortOuAttaque(
                    description, commentaire_a_afficher, commentaire_degat
                )
            else:
                # attaques qui ne rentrent pas dans la méthode globale (fait plus que juste des degat ou un element)
                if action in self.modele.techniques_de_ame:
                    # degats
                    if action == "Pira":
                        degat_de_base = self.modele.PIRADEGAT
                    elif action == "Elektron":
                        degat_de_base = self.modele.ELEKTRONDEGAT
                    elif action == "Tsumeta-Sa":
                        degat_de_base = self.modele.TSUMETASADEGAT
                    elif action == "Mathaïr":
                        degat_de_base = self.modele.MATHAIRDEGAT
                    elif action == "Fos":
                        degat_de_base = self.modele.FOSDEGAT
                    elif action == "Haddee":
                        degat_de_base = self.modele.HADDEEDEGAT
                    degat_de_base += round(
                        (self.modele.DEGATBONUSATTAQUE / 100) * degat_de_base
                    )
                    degat_de_base -= round(
                        (self.modele.BONUSREDUCTIONDEGAT / 100) * degat_de_base
                    )
                    # description
                    if action == "Pira":
                        description = "Vous invoquez Pira, le bô espagnol contenant l'essence même du feu, "
                        commentaire_a_afficher = (
                            "et assenez un coup surpuissant a l'ennemi."
                        )
                    elif action == "Elektron":
                        description = "Vous invoquez Elektron, la lance nordique contenant l'essence même de la foudre, "
                        commentaire_a_afficher = "et percez le torse du monstre."
                    elif action == "Tsumeta-Sa":
                        description = "Vous invoquez Tsumeta-Sa, le katana japonais contenant l'essence même de la glace, "
                        commentaire_a_afficher = "et entaillez profondement L'ennemi."
                    elif action == "Mathaïr":
                        description = "Vous invoquez Mathaïr, la corne irlandaise contenant l'essence même de la terre, "
                        commentaire_a_afficher = "et manipulez l'environnement avec ses vibrations pour encastrer L'ennemi dans un cerceuil de plusieurs tonnes."
                    elif action == "Fos":
                        description = "Vous invoquez Fos, les gants de combat créôles contenant l'essence même de l'effort,"
                        commentaire_a_afficher = (
                            "et assenez un upercut magistral a l'ennemi."
                        )
                    elif action == "Haddee":
                        description = "Vous invoquez Haddee, la dague rituelle hindou contenant l'essence même du sang,"
                        commentaire_a_afficher = " et lacerez la surface du monstre de centaines de petites coupures nettes."
                    # chance de critique
                    pourcentage_de_critique = 25
                    pourcentage_de_critique += self.modele.CHANCECOUPCRITIQUE
                    # degat critique
                    degat_critique = round(degat_de_base * 0.25)
                    degat_critique += round(
                        (self.modele.DEGATBONUSATTAQUECRITIQUE / 100) * degat_critique
                    )
                    degat_critique += round(self.modele.accumulation_degat_technique_critique)
                    # degats sont critiques ?
                    nombre_aleatoire = random.randint(0, 100)
                    if nombre_aleatoire < pourcentage_de_critique:
                        degat_de_base += degat_critique
                        commentaire_a_afficher += "\nCoup critique !"
                        if "Pièce Fondue" in self.modele.liste_dartefacts_optionels:
                            commentaire_a_afficher += "\nL'artefact [Pièce Fondue] maudit l'ennemi !"
                            self.modele.monstre_est_maudit = True
                            self.modele.monstre_est_maudit_nombre_tour += 2
                    # applique degat
                    degat_de_base = self.SiZeroRameneAUn(degat_de_base)
                    self.modele.monstre_points_de_vie -= degat_de_base
                    commentaire_degat = (
                        f"Vous infligez {degat_de_base} points de vie a l'ennemi !"
                    )
                    # applique effet elementaire ?
                    chance_effet_elementaire = 0
                    if action == "Pira":
                        chance_effet_elementaire += self.modele.PIRABRULE
                        chance_effet_elementaire += self.modele.CHANCEBONUSDEFAIREBRULER
                    elif action == "Elektron":
                        chance_effet_elementaire += self.modele.ELEKTRONPARALYSE
                        chance_effet_elementaire += self.modele.CHANCEBONUSDEFAIREPARALYSER
                    elif action == "Tsumeta-Sa":
                        chance_effet_elementaire += self.modele.TSUMETASAGELE
                        chance_effet_elementaire += self.modele.CHANCEBONUSDEFAIREGELER
                    elif action == "Mathaïr":
                        chance_effet_elementaire += self.modele.MATHAIRLAPIDE
                        chance_effet_elementaire += self.modele.CHANCEBONUSDEFAIRELAPIDER
                    elif action == "Haddee":
                        chance_effet_elementaire += self.modele.HADDEEDRAIN
                        chance_effet_elementaire += self.modele.CHANCEBONUSDEFAIRESAIGNER
                    # effet elementaire ?
                    if nombre_aleatoire < chance_effet_elementaire:
                        if action == "Pira":
                            self.modele.monstre_est_en_feu = True
                            self.modele.monstre_est_en_feu_degat = 5
                            nombre_tour = self.modele.PIRABRULETOUR
                            nombre_tour += self.modele.TOURBONUSENNEMIENFEU
                            if self.modele.stigma_monstre_negatif == "Inflammable":
                                nombre_tour += nombre_tour
                            if self.modele.utilise_rafale:
                                nombre_tour += nombre_tour
                            self.modele.monstre_est_en_feu_nombre_tour += (
                                nombre_tour
                            )
                            commentaire_degat += f"\nL'ennemi se met a bruler pendant {nombre_tour} tours !"
                        elif action == "Elektron":
                            self.modele.monstre_est_paralyse = True
                            self.modele.monstre_est_paralyse_nombre_tour += (
                                self.modele.ELEKTRONPARALYSETOUR
                            )
                            commentaire_degat += f"\nLes muscles du monstre sont paralysés pendant {self.modele.ELEKTRONPARALYSETOUR} tours !"
                        elif action == "Tsumeta-Sa":
                            self.modele.monstre_est_gele = True
                            self.modele.monstre_est_gele += (
                                self.modele.TSUMETASAGELETOUR
                            )
                            commentaire_degat += f"\nL'ennemi se retrouve gelé pendant {self.modele.TSUMETASAGELETOUR} tours !"
                        elif action == "Mathaïr":
                            degat_lapidation = round(degat_de_base * 0.5)
                            degat_lapidation = self.SiZeroRameneAUn(degat_lapidation)
                            if ("Voluntad Le Luumo") in self.modele.monstre_tags:
                                commentaire_degat += f"\nVoluntad Le Luumo, l'esprit de terre, absorbe la lapidation infligée sur {self.modele.monstre_nom} !"
                            else:
                                self.modele.monstre_points_de_vie -= degat_lapidation
                                commentaire_degat += f"\nVous infligez {degat_lapidation} points de vie supplementaire par lapidation !"
                                if self.modele.eboulis:
                                    commentaire_degat += self.AppliqueTalentEboulis(degat_lapidation)
                                if self.modele.fracturation:
                                    commentaire_degat += self.AppliqueTalentFracturation()
                        elif action == "Haddee":
                            if ("Voluntad U Kiikel") in self.modele.monstre_tags:
                                commentaire_degat = f"\nVoluntad U Kiikel, l'esprit de sang, absorbe le drain de vie infligé à {self.modele.monstre_nom} !"
                            else:
                                # enleve vie a monstre
                                degat_saignee = round(degat_de_base * 0.5)
                                degat_saignee = self.AppliqueLimitationSaignee(degat_saignee)
                                self.modele.monstre_points_de_vie -= degat_saignee
                                # rajoute vie a joueur
                                soin_saignee = degat_saignee
                                soin_saignee += round(
                                    (self.modele.SOINSSAIGNEE / 100) * degat_saignee
                                )
                                self.modele.points_de_vie += soin_saignee
                                self.EquilibragePointsDeVieEtManaEtEndurance()
                                commentaire_degat += f"\nVous drainez {degat_saignee} points de vie a l'adversaire, et en récuperez {soin_saignee} !"
                                if self.modele.anemie:
                                    commentaire_degat += self.AppliqueTalentAnemie()
                                if self.modele.baron_rouge:
                                    commentaire_degat += self.AppliqueTalentBaronRouge()
                                if self.modele.anticoagulants:
                                    degat_de_base = round(degat_de_base * 0.2)
                                    self.modele.monstre_points_de_vie -= degat_de_base
                                    commentaire_degat += f"\nVous infligez {degat_de_base} points de vie a l'adversaire par saignement !"
                    self.vue.AfficheSortOuAttaque(
                        description, commentaire_a_afficher, commentaire_degat
                    )
                elif action == "Griffes du Démon":
                    commentaire = ("Vous puisez dans l'énergie démonique qui habite votre corps pour lacerer l'ennemi de vos griffes."
                                   "\nVous infligez 25 points de dégâts a l'ennemi, et le marquez comme sacrifice jusqu'a la fin de ce tour !")
                    self.modele.sacrifice_actif = True
                    self.modele.monstre_points_de_vie -= 25
                    self.vue.AfficheGriffe(commentaire)
                elif action == "Posture de la Montagne":
                    commentaire = "Vous utilisez la posture de la montagne."
                    self.modele.gain_de_defence = round(
                        self.modele.points_de_defence * 0.5
                    ) + 10
                    self.modele.utilise_posture_de_la_montagne = True
                    self.modele.posture_de_la_montagne_tour += 5
                    commentaire += f"\nVous gagnez {self.modele.gain_de_defence} points de defence pendant 5 tours !"
                    self.vue.AfficheMontagne(commentaire)
                elif action == "Libération Physique":
                    commentaire = (
                        "Je suis vivant, donc je suis la vie."
                        "\nJe suis la vie, donc je suis l'énergie."
                        "\nJe suis l'énergie, donc je suis le mana."
                        "\nJe suis le mana, donc je suis vivant."
                        "\nVous laissez votre corps se remplir avec le monde qui vous entoure."
                    )
                    soin_vie = round(self.modele.points_de_vie_max * 0.5)
                    soin_mana = round(self.modele.points_de_mana_max * 0.5)
                    self.modele.points_de_vie += soin_vie
                    self.RecouvrementDeMana(soin_mana)
                    commentaire += f"\nVous reprenez {soin_vie} pv, et {soin_mana} pm."
                    commentaire_malus = "Vous êtes désorientés par l'experience, et retrouverez votre stabilité dans 4 tours"
                    self.modele.est_maudit_par_les_techniques = True
                    self.modele.est_maudit_par_les_techniques_nombre_tour = 5
                    self.vue.AfficheLiberationPhysique(commentaire, commentaire_malus)
                elif action == "Combo Electrique":
                    chance_paralyser = 10
                    chance_paralyser += round((self.modele.CHANCEBONUSDEFAIREPARALYSER/100) * chance_paralyser)
                    nombre_de_coup = 0
                    chance_de_toucher = 50
                    chance_de_toucher -= self.modele.CHANCERATERATTAQUE
                    nombre_aleatoire_coup = 0
                    nombre_de_paralysie = 0
                    commentaire = "Vous lancez le Combo Electrique !"
                    self.vue.AfficheDebutComboElectrique(commentaire)
                    # determine le nombre de coup infligés
                    while nombre_aleatoire_coup < chance_de_toucher:
                        nombre_de_coup += 1
                        commentaire = f"Vous infligez {nombre_de_coup} coup..."
                        # determine le nombre de coup qui ont reussi a paralyser
                        nombre_aleatoire_paralysie = random.randint(0, 100)
                        # ca paralyse ?
                        paralyse = "...sans paralyser."
                        if nombre_aleatoire_paralysie < (chance_paralyser - nombre_de_coup):
                            nombre_de_paralysie += 1
                            paralyse = "...et paralysez l'ennemi pour un tour supplementaire !"
                        nombre_aleatoire_coup = random.randint(0, 100)
                        if nombre_de_coup == 10:
                            nombre_aleatoire_coup = 100
                        self.vue.AfficheComboElectrique(commentaire, paralyse)
                    degat = 5
                    degat = (
                        round(((self.modele.DEGATBONUSATTAQUE + self.modele.DEGATBONUSATTAQUEFOUDRE) / 100) * degat)
                    )
                    degat = degat * nombre_de_coup
                    degat = self.SiZeroRameneAUn(degat)
                    self.modele.monstre_points_de_vie -= degat
                    if nombre_de_paralysie != 0:
                        self.modele.monstre_est_paralyse = True
                        self.modele.monstre_est_paralyse_nombre_tour += (
                            nombre_de_paralysie + 1
                        )
                    commentaire = (
                        "Vous perdez votre équilibre et envoyez le dernier coup dans le vide."
                        f"Vous avez infligé {degat} points de vie a l'adversaire, et l'avez paralysé {nombre_de_paralysie} tour !"
                    )
                    self.vue.AfficheFinComboElectrique(commentaire)
                elif action == "Position du Massif":
                    self.modele.limite_degat = round(
                        self.modele.points_de_vie_max * 0.05
                    )
                    self.modele.utilise_le_massif = True
                    commentaire = (
                        "Vous utilisez la position du massif ! La prochaine "
                        f"attaque ne pourra pas vous enlever plus de {self.modele.limite_degat} points de vie !"
                    )
                    self.vue.AfficheMassif(commentaire)
                elif action == "Poussée d'Adrénaline":
                    self.modele.utilise_pousse_adrenaline = True
                    self.modele.pousse_adrenaline_tour = 4
                    commentaire = ("Vous stoppez votre respiration afin de provoquer un afflux d'adrenaline dans votre corps."
                                   "\nVos dégats sont multipliés par 50% pendant 3 tours !")
                    self.vue.AfficheAdrenaline(commentaire)
                elif action == "Bluff":
                    self.modele.utilise_le_bluff = True
                    commentaire = (
                        "Vous utilisez le Bluff ! La prochaine "
                        "attaque sera doublement renvoyée a l'ennemi,"
                        "mais si il ne fait pas de degat, vous serez paralysé !"
                    )
                    self.vue.AfficheBluff(commentaire)
                elif action == "Iaido":
                    self.modele.en_plein_iaido = True
                    self.modele.en_plein_iaido_nombre_tour = 3
                    self.modele.passe_son_tour = True
                    self.vue.AfficheDebutIaido()
                elif action == "Cuisiner":
                    self.CuisineInfernaleCuisiner()
        else:
            # affiche que laction s'est pas passée, et pourquoi
            self.vue.AfficheActionImpossible(raison_si_action_pas_possible)

    def Iaido(self):
        degat_de_base = 25 + round(self.modele.monstre_points_de_vie_max * 0.1)
        pourcentage = (
            self.modele.DEGATBONUSATTAQUE +
            self.modele.DEGATBONUSATTAQUEFEU +
            self.modele.DEGATBONUSATTAQUEGLACE +
            self.modele.DEGATBONUSATTAQUEFOUDRE +
            self.modele.DEGATBONUSATTAQUESANG +
            self.modele.DEGATBONUSATTAQUEPHYSIQUE
        )
        degat = (
            degat_de_base +
            round((pourcentage / 100) * degat_de_base)
        )
        nombre_aleatoire = random.randint(0, 100)
        commentaire = f"Vous assénez un coup invincible a l'ennemi, et lui infligez {degat} points de vie !"
        self.modele.monstre_points_de_vie -= degat
        if (nombre_aleatoire <= 10) and (not self.modele.monstre_EstUnBoss):
            self.modele.monstre_points_de_vie = -100
            commentaire = "Vous tranchez l'ennemi en deux, et sa mort devient une véritée irrévoquable."
        self.vue.AfficheIaido(commentaire)

    def SetTypeOfAction(self, action):
        if (
            action in self.modele.sorts_de_feu
            or action in self.modele.techniques_de_feu
            or action == "Libération Enflammée"
            or action == "Rafale"
            or action == "Explosion de Feu Sacré"
        ):
            self.modele.a_utilise_feu_ce_tour = True
            if "Epreuve du Magister" in self.Player.quete :
                self.Player.quete = "Epreuve du Magister [Echec]"
            if self.modele.type_de_derniere_action_utilisee == "Techniques":
                self.sound_of_action = "FIREt"
            else:
                self.sound_of_action = "FIREm"
        elif (
            action in self.modele.sorts_de_foudre
            or action in self.modele.techniques_de_foudre
            or action == "Libération Fulgurante"
            or action == "Combo Electrique"
        ):
            self.modele.a_utilise_foudre_ce_tour = True
            if "Epreuve du Magister" in self.Player.quete :
                self.Player.quete = "Epreuve du Magister [Echec]"
            if self.modele.type_de_derniere_action_utilisee == "Techniques":
                self.sound_of_action = "ELECt"
            else:
                self.sound_of_action = "ELECm"
        elif (
            action in self.modele.sorts_de_glace
            or action in self.modele.techniques_de_glace
            or action == "Libération Glaciale"
            or action == "Mirroir d'Eau"
            or action == "Avalanche"
        ):
            self.modele.a_utilise_glace_ce_tour = True
            if "Epreuve du Magister" in self.Player.quete :
                self.Player.quete = "Epreuve du Magister [Echec]"
            if self.modele.type_de_derniere_action_utilisee == "Techniques":
                self.sound_of_action = "ICEt"
            else:
                self.sound_of_action = "ICEm"
        elif (
            action in self.modele.sorts_de_physique
            or action in self.modele.techniques_de_physique
            or action == "Poussée d'Adrénaline"
            or action == "Libération Physique"
            or action == "Griffes du Démon"
        ):
            self.modele.a_utilise_physique_ce_tour = True
            if "Epreuve des Mages-Epeistes" in self.Player.quete :
                self.Player.quete = "Epreuve des Mages-Epeistes [Echec]"
            if self.modele.type_de_derniere_action_utilisee == "Techniques":
                self.sound_of_action = "PHYSt"
            else:
                self.sound_of_action = "PHYSm"
        elif (
            action in self.modele.sorts_de_sang
            or action in self.modele.techniques_de_sang
            or action == "Libération Sanglante"
            or action == "Brume de Sang"
            or action == "Bluff"
        ):
            self.modele.a_utilise_sang_ce_tour = True
            if "Epreuve des Mages-Epeistes" in self.Player.quete :
                self.Player.quete = "Epreuve des Mages-Epeistes [Echec]"
            if self.modele.type_de_derniere_action_utilisee == "Techniques":
                self.sound_of_action = "BLOODt"
            else:
                self.sound_of_action = "BLOODm"
        elif (
            action in self.modele.sorts_de_terre
            or action in self.modele.techniques_de_terre
            or action == "Avalanche"
            or action == "Libération Holomélanocrate"
            or action == "Posture de la Montagne"
            or action == "Position du Massif"
        ):
            self.modele.a_utilise_terre_ce_tour = True
            if "Epreuve des Mages-Epeistes" in self.Player.quete :
                self.Player.quete = "Epreuve des Mages-Epeistes [Echec]"
            if self.modele.type_de_derniere_action_utilisee == "Techniques":
                self.sound_of_action = "DIRTt"
            else:
                self.sound_of_action = "DIRTm"
        elif action in self.modele.sorts_de_soin:
            self.sound_of_action = "HEAL"
        elif action in self.modele.techniques_de_ame:
            self.sound_of_action = "SOUL"

    def CheckTypeOfAction(self, action):
        if (
            action in self.modele.sorts_de_feu
            or action in self.modele.techniques_de_feu
            or action == "Libération Enflammée"
            or action == "Rafale"
            or action == "Explosion de Feu Sacré"
        ):
            return "feu"
        elif (
            action in self.modele.sorts_de_foudre
            or action in self.modele.techniques_de_foudre
            or action == "Libération Fulgurante"
            or action == "Combo Electrique"
        ):
            return "foudre"
        elif (
            action in self.modele.sorts_de_glace
            or action in self.modele.techniques_de_glace
            or action == "Libération Glaciale"
            or action == "Mirroir d'Eau"
            or action == "Avalanche"
        ):
            return "glace"
        elif (
            action in self.modele.sorts_de_physique
            or action in self.modele.techniques_de_physique
            or action == "Poussée d'Adrénaline"
            or action == "Libération Physique"
            or action == "Griffes du Démon"
        ):
            return "physique"
        elif (
            action in self.modele.sorts_de_sang
            or action in self.modele.techniques_de_sang
            or action == "Libération Sanglante"
            or action == "Brume de Sang"
            or action == "Bluff"
        ):
            return "sang"
        elif (
            action in self.modele.sorts_de_terre
            or action in self.modele.techniques_de_terre
            or action == "Avalanche"
            or action == "Libération Holomélanocrate"
            or action == "Posture de la Montagne"
            or action == "Position du Massif"
        ):
            return "terre"
        elif action in self.modele.sorts_de_soin:
            return "soin"
        elif action in self.modele.techniques_de_ame:
            return "ame"

    def ResetTypeElementUtiliseCeTour(self):
        self.modele.a_utilise_feu_ce_tour = False
        self.modele.a_utilise_foudre_ce_tour = False
        self.modele.a_utilise_glace_ce_tour = False
        self.modele.a_utilise_physique_ce_tour = False
        self.modele.a_utilise_sang_ce_tour = False
        self.modele.a_utilise_terre_ce_tour = False

    def CoutEnManaDuSort(self, sort):
        cout_mana = self.modele.annuaire_de_cout_des_sorts[sort]
        cout_pourcentage_supplement = self.modele.BONUSCOUTMALEDICTIONMANA
        # calcule l'augmentation de cout
        if self.modele.est_maudit_par_le_mana:
            cout_mana += round(cout_mana * (cout_pourcentage_supplement / 100))
        reduction_mana = self.modele.BONUSREDUCTIONMANASORTTOUT
        cout_mana -= round((reduction_mana / 100)* cout_mana)
        if sort in self.modele.sorts_de_feu:
            reduction_mana += self.modele.BONUSREDUCTIONMANASORTFEU
        elif sort in self.modele.sorts_de_foudre:
            reduction_mana += self.modele.BONUSREDUCTIONMANASORTFOUDRE
        if sort in self.modele.sorts_de_terre:
            reduction_mana += self.modele.BONUSREDUCTIONMANASORTTERRE
        cout_mana -= round((reduction_mana / 100)* cout_mana)
        if self.modele.concentre:
            cout_mana -= round(0.2 * self.modele.annuaire_de_cout_des_sorts[sort])
        if cout_mana < 1 :
            cout_mana = 1
        return cout_mana

    def CheckSiSortPossibleEtAppliqueCoutSort(self, action):
        cout_gold = 0
        affichage_raison_sort_impossible = ""
        try:
            cout_mana = self.CoutEnManaDuSort(action)
        except Exception as error:
            cout_mana = 0


        # checke le stigma du joueur et sa vie. Applique Colerique.
        limite_vie = round(self.modele.points_de_vie_max * 0.10)
        if self.modele.stigma_joueur_negatif == "Colérique" and (self.modele.points_de_vie < limite_vie):
            affichage_raison_sort_impossible = ("Vous pensez au déroulement du combat, et les raisons pour lesquelles vous êtes en si mauvais état."
                                                "\nCela vous met tellement en colère, que vous n'arrivez pas a vous concentrer pour lancer le sort.")
        # checke si le jjoueur a assez de mana. Non = affichage raison.
        if self.modele.points_de_mana < cout_mana:
            affichage_raison_sort_impossible = "Vous condensez le mana pour invoquer le sort...mais pas assez ne se réunit pour terminer l'invoquation."
        # calcule le cout en gold
        if self.modele.est_maudit_par_le_gold:
            cout_gold = cout_mana * 2
        # checke si le jjoueur a assez de gold. Non = affichage raison.
        if self.modele.nombre_de_gold < cout_gold:
            affichage_raison_sort_impossible = "Alors que vous commencez a lancer le sort, 1 gold disparait pour chaque points de mana qui se condensent. Alors que vos économies arrivent a 0, pas assez de mana ne se réunit pour lancer le sort."
            self.modele.nombre_de_gold = 0
        # checke si le jjoueur a assez de vie si maudit par mana. Non = affichage raison.
        degat_malediction_du_mana = round(self.modele.points_de_vie_max*0.03)
        if degat_malediction_du_mana == 0:
            degat_malediction_du_mana = 1
        if self.modele.malediction_du_mana and (self.modele.points_de_vie <= degat_malediction_du_mana):
            affichage_raison_sort_impossible = "Les éléments se battent trop fortement dans votre âme pour pouvoir les utiliser dans votre sort."
        # checke si le joueur peut lancer le sort.
        if self.modele.est_maudit_par_les_sorts:
            affichage_raison_sort_impossible = (
                "Vous tentez de lancer le sort, mais aucun mot ne sort de votre bouche."
            )
        # checke si les maledictions empechent le jouer de lancer le sort.
        element_du_sort = self.CheckTypeOfAction(action)
        if ((element_du_sort == "feu" and self.Player.malediction == "Apyre") or
            (element_du_sort == "glace" and self.Player.malediction == "Infrigérable") or
            (element_du_sort == "foudre" and self.Player.malediction == "Isolant") or
            (element_du_sort == "physique" and self.Player.malediction == "Anoxique") or
            (element_du_sort == "sang" and self.Player.malediction == "Exsangue") or
            (element_du_sort == "terre" and self.Player.malediction == "Arénacé")):
            affichage_raison_sort_impossible = (
                "Vous tentez d'utiliser le sort, mais une force maudite vous en empêche."
            )
        # si affichage_raison_sort_impossible est vide, alors on peut lancer le sort et on applique son cout. sinon, on retourne la raison.
        if affichage_raison_sort_impossible == "":

            nombre_aleatoire_qui_definit_si_le_sort_est_gratuit = 50

            if "Serment d'Heimdall" in self.modele.liste_dartefacts_optionels:
                nombre_aleatoire_qui_definit_si_le_sort_est_gratuit = random.randint(0, 100)

            if nombre_aleatoire_qui_definit_si_le_sort_est_gratuit in range(1, 4):
                #sort gratuit
                commentaire = "Vous sentez que le mana que vous manipulez pour lancer le sort ne vient pas de vous, mais d'un être superieur.\nVous sentez la marque de la promesse chauffer."
                self.vue.AfficheSermentHeimdall(commentaire)
            else:
                if self.modele.malediction_du_mana:
                    degat_malediction_du_mana = self.EnleveVieAuJoueur(degat_malediction_du_mana)
                    self.vue.AfficheMaledictionMana(degat_malediction_du_mana)
                self.modele.points_de_mana -= cout_mana
                self.modele.nombre_de_gold -= cout_gold

            action_est_possible = True
            return action_est_possible, affichage_raison_sort_impossible
        else:
            if self.modele.bon_tachyon and self.modele.charge_bon_tachyon >= 50:
                self.vue.AfficheBonTachyonUtilisation()
                self.modele.charge_bon_tachyon -= 50
                action_est_possible = True
                affichage_raison_sort_impossible = ""
                return action_est_possible, affichage_raison_sort_impossible
            else:
                action_est_possible = False
                return action_est_possible, affichage_raison_sort_impossible

    def CheckSiAttaquePossibleEtAppliqueCoutAttaque(self, action):
        cout_vie = 0
        cout_gold = 0
        cout_endurance = self.modele.annuaire_de_cout_des_techniques[action]
        affichage_raison_technique_impossible = ""
        cout_vie_a_appliquer = False
        # calcule le cout de vie
        if self.modele.est_maudit_par_la_vie:
            pourcentage = self.modele.BONUSCOUTMALEDICTIONVIEOUGOLD
            cout_vie += round(self.modele.points_de_vie_max * (pourcentage/100))
            cout_vie_a_appliquer = True
        # checke si le joueur a assez d'endurance. Non = affichage raison.
        if ((self.modele.points_de_endurance < cout_endurance and not
            ("Couronne Sacrée" in self.modele.liste_dartefacts_optionels))
            or
            (self.modele.points_de_endurance <= 0 and
            ("Couronne Sacrée" in self.modele.liste_dartefacts_optionels))
        ):
            affichage_raison_technique_impossible = "Vous tentez d'utiliser la technique...mais vous vous effondrez, haletant, sur le sol de l'arène."
        # checke si le jjoueur a assez de vie. Non = affichage raison.
        if self.modele.points_de_vie < cout_vie:
            affichage_raison_technique_impossible = "Vous tentez d'utiliser la technique...mais vos blessures sont trop graves et la douleur vous fait abandonner en plein milieu."
        # calcule le cout en gold
        if self.modele.est_maudit_par_le_gold:
            pourcentage = self.modele.BONUSCOUTMALEDICTIONVIEOUGOLD
            cout_gold = round(self.modele.points_de_vie_max * (pourcentage/100))
        # checke si le jjoueur a assez de gold. Non = affichage raison.
        if self.modele.nombre_de_gold < cout_gold:
            affichage_raison_technique_impossible = "Alors que vous utilisez la technique, 1 gold disparait pour chaque secondes qui passent. Quand vos économies arrivent a 0, votre concentration s'arrete brusquement et vous ratez la technique."
            self.modele.nombre_de_gold = 0
        # checke si le joueur peut lancer les technique.
        if self.modele.est_maudit_par_les_techniques:
            affichage_raison_technique_impossible = "Vous tentez d'utiliser la technique, mais le monde se met a tourner et vous vous retrouvez par terre, sans comprendre pourquoi."
        # checke si les maledictions empechent le jouer de lancer l'attaque.
        element_de_la_technique = self.CheckTypeOfAction(action)
        if ((element_de_la_technique == "feu" and self.Player.malediction == "Apyre") or
            (element_de_la_technique == "glace" and self.Player.malediction == "Infrigérable") or
            (element_de_la_technique == "foudre" and self.Player.malediction == "Isolant") or
            (element_de_la_technique == "physique" and self.Player.malediction == "Anoxique") or
            (element_de_la_technique == "sang" and self.Player.malediction == "Exsangue") or
            (element_de_la_technique == "terre" and self.Player.malediction == "Arénacé")
        ):
            affichage_raison_technique_impossible = (
                "Vous tentez d'utiliser le sort, mais une force maudite vous en empêche."
            )
        # si affichage_raison_technique_impossible est vide, alors on peut lancer le technique et on applique son cout. sinon, on retourne la raison.
        if affichage_raison_technique_impossible == "":
            if cout_vie_a_appliquer:
                cout_vie = self.EnleveVieAuJoueur(cout_vie)
            self.modele.nombre_de_gold -= cout_gold
            self.modele.points_de_endurance -= cout_endurance
            action_est_possible = True
            return action_est_possible, affichage_raison_technique_impossible
        else:
            action_est_possible = False
            return action_est_possible, affichage_raison_technique_impossible
        
    def EnleveurAffix(self, action, doit_faire_action_affix=False):
        liste_affix = ["~Rouge~", # +2 vie
                                   "~Carmin~", # +4 vie
                                   "~Violet~", # +2 mana
                                   "~Pourpre~", # +4 mana
                                   "~Jaune~", # +2 endurance
                                   "~Doré~", # +4 endurance
                                   "~Lolipop~", # +1 vie mana endurance
                                   "~Bubblegum~", # +2 vie mana endurance
                                   "~Escargot~", # +1% degat technique
                                   "~Limace~", # +1% degat sorts
                                   "~Citronnier~", # +0.5 degat critique technique
                                   "~Citron~", # +1 degat critique technique
                                   "~Cerisier~", # +0.5 degat critique sort
                                   "~Cerise~", # +1 degat critique sort
                                   "~Mars~", # +0.5% chance de bruler
                                   "~Neptune~", # +0.5% chance de geler
                                   "~Pluton~", # +0.25% chance de paralyser
                                   "~Lune~", # +0.5% chance de lapider
                                   "~Mercure~", # +0.5% chance de drain
                                   "~Ordre~", # peut bruler
                                   "~Aveugle~", # peut geler
                                   "~Limitation~", # peut lapider
                                   "~Transcendance~", # peut paralyser
                                   "~Eveil~", # peut drainer
                                   "~Antithèse~", # 15% chance d'arreter le gel
                                   "~Chaotique~", # 15% chance d'arreter la brulure
                                   "~Tache~", # 15% chance d'arreter la blessure
                                   "~Rature~", # 15% chance d'arreter la deconcentration
                                   "~Brouillon~", # 15% chance d'arreter la confusion
                                   "~Paragraphe~", # 6% chance d'enlever gel + brulure + blessure + deconcentration + confusion
                                   "~Magnum-Opus~", # 6% chance de donner numero_etage * 5 golds
                                   "~Agrume~", # 6% chance d'être béni
                                   "~Raisin~", # 6% chance d'être en folie
                                   "~Durian~", # 6% chance d'être en furie
                                   "~Gingembre~", # 6% chance d'être jindagee 2 tours
                                   "~Mandragore~", # 6% chance d'être aatma 2 tours
                                   "~Nigredo~", # 2% chance reprendre full vie
                                   "~Albédo~", # 2% chance reprendre full mana
                                   "~Citrinitas~", # 2% chance reprendre full endurance
                                   "~Chrysalide~", # 2% chance devenir invincible 2 tours
                                   ]
        action_transformee_en_liste = list(action.split())
        liste_mot = []
        for mot in action_transformee_en_liste:
            if mot in liste_affix:
                if doit_faire_action_affix:
                    self.DoAffixPurpose(mot)
                else:
                    pass
            else:
                liste_mot.append(mot)

        action_sans_affixe = ""
        for mot in liste_mot:
            action_sans_affixe += mot
            if liste_mot[len(liste_mot) - 1] != mot:
                action_sans_affixe += " "

        return action_sans_affixe

    def DoAffixPurpose(self,mot):
        numero_aleatoire = random.randint(0, 100)
        if mot == "~Rouge~":
            self.modele.points_de_vie += 2
            self.EquilibragePointsDeVieEtManaEtEndurance()
        elif mot == "~Carmin~":
            self.modele.points_de_vie += 4
            self.EquilibragePointsDeVieEtManaEtEndurance()
        elif mot == "~Violet~":
            self.modele.points_de_mana += 2
            self.EquilibragePointsDeVieEtManaEtEndurance()
        elif mot == "~Pourpre~":
            self.modele.points_de_mana += 4
            self.EquilibragePointsDeVieEtManaEtEndurance()
        elif mot == "~Jaune~":
            self.modele.points_de_endurance += 2
            self.EquilibragePointsDeVieEtManaEtEndurance()
        elif mot == "~Doré~":
            self.modele.points_de_endurance += 4
            self.EquilibragePointsDeVieEtManaEtEndurance()
        elif mot == "~Lolipop~":
            self.modele.points_de_vie += 1
            self.modele.points_de_mana += 1
            self.modele.points_de_endurance += 1
            self.EquilibragePointsDeVieEtManaEtEndurance()
        elif mot == "~Bubblegum~":
            self.modele.points_de_vie += 2
            self.modele.points_de_mana += 2
            self.modele.points_de_endurance += 2
            self.EquilibragePointsDeVieEtManaEtEndurance()
        elif mot == "~Escargot~":
            self.modele.accumulation_degat_technique += 1
        elif mot == "~Limace~":
            self.modele.accumulation_degat_sort += 1
        elif mot == "~Citronnier~":
            self.modele.accumulation_degat_technique_critique += 0.5
        elif mot == "~Citron~":
            self.modele.accumulation_degat_technique_critique += 1
        elif mot == "~Cerisier~":
            self.modele.accumulation_degat_sort_critique += 0.5
        elif mot == "~Cerise~":
            self.modele.accumulation_degat_sort_critique += 1
        elif mot == "~Mars~":
            self.modele.accumulation_chance_brulure += 0.5
        elif mot == "~Neptune~":
            self.modele.accumulation_chance_gelure += 0.5
        elif mot == "~Pluton~":
            self.modele.accumulation_chance_paralysie += 0.25
        elif mot == "~Lune~":
            self.modele.accumulation_chance_lapider += 0.5
        elif mot == "~Mercure~":
            self.modele.accumulation_chance_drainer += 0.5
        elif mot == "~Antithèse~":
            if numero_aleatoire <= 15 and self.modele.est_gele:
                self.modele.est_gele_nombre_tour = 0
                self.modele.est_gele = False
        elif mot == "~Chaotique~":
            if numero_aleatoire <= 15 and self.modele.est_en_feu:
                self.modele.est_en_feu_nombre_tour = 0
                self.modele.est_en_feu_degat = 0
                self.modele.est_en_feu = False
        elif mot == "~Tache~":
            if numero_aleatoire <= 15 and self.modele.est_maudit_par_la_vie:
                self.modele.est_maudit_par_la_vie_nombre_tour = 0
                self.modele.est_maudit_par_la_vie = False
        elif mot == "~Rature~":
            if numero_aleatoire <= 15 and self.modele.est_maudit_par_le_mana:
                self.modele.est_maudit_par_le_mana_nombre_tour = 0
                self.modele.est_maudit_par_le_mana = False
        elif mot == "~Brouillon~":
            if numero_aleatoire <= 15 and self.modele.est_maudit_par_les_items:
                self.modele.est_maudit_par_les_items_nombre_tour = 0
                self.modele.est_maudit_par_les_items = False
        elif mot == "~Paragraphe~":
            if numero_aleatoire <= 5:
                self.modele.est_maudit_par_les_items_nombre_tour = 0
                self.modele.est_maudit_par_les_items = False
                self.modele.est_maudit_par_le_mana_nombre_tour = 0
                self.modele.est_maudit_par_le_mana = False
                self.modele.est_maudit_par_la_vie_nombre_tour = 0
                self.modele.est_maudit_par_la_vie = False
                self.modele.est_en_feu_nombre_tour = 0
                self.modele.est_en_feu_degat = 0
                self.modele.est_en_feu = False
                self.modele.est_gele_nombre_tour = 0
                self.modele.est_gele = False
        elif mot == "~Magnum-Opus~":
            if numero_aleatoire <= 6:
                self.modele.nombre_de_gold += self.modele.numero_de_letage * 5
        elif mot == "~Agrume~":
            if numero_aleatoire <= 6:
                self.modele.beni_par_feu_sacre = True
                self.modele.beni_par_feu_sacre_nombre_tour += 2        
        elif mot == "~Raisin~":
            if numero_aleatoire <= 6:
                self.modele.utilise_orbe_de_folie = True
                self.modele.utilise_orbe_de_folie_nombre_tour += 2
        elif mot == "~Durian~":
            if numero_aleatoire <= 6:
                self.modele.utilise_orbe_de_furie = True
                self.modele.utilise_orbe_de_furie_nombre_tour += 2
        elif mot == "~Gingembre~":
            if numero_aleatoire <= 6:
                self.modele.utilise_fruit_jindagee = True
                self.modele.utilise_fruit_jindagee_nombre_tour += 2
        elif mot == "~Mandragore~":
            if numero_aleatoire <= 6:
                self.modele.utilise_fruit_aatma = True
                self.modele.utilise_fruit_aatma_nombre_tour += 2
        elif mot == "~Nigredo~":
            if numero_aleatoire <= 2:
                self.modele.points_de_vie == self.modele.points_de_vie_max
        elif mot == "~Albédo~":
            if numero_aleatoire <= 2:
                self.modele.points_de_mana == self.modele.points_de_mana_max
        elif mot == "~Citrinitas~":
            if numero_aleatoire <= 2:
                self.modele.points_de_endurance == self.modele.points_de_endurance_max
        elif mot == "~Chrysalide~":
            if numero_aleatoire <= 2:
                self.modele.metamorphose = True
                self.modele.metamorphose_nombre_tour += 2

        elif mot == "~Ordre~":
            self.modele.player_tags.append("Utilise Feu Basique")
        elif mot == "~Aveugle~":
            self.modele.player_tags.append("Utilise Glace Basique")
        elif mot == "~Limitation~":
            self.modele.player_tags.append("Utilise Terre Basique")
        elif mot == "~Transcendance~":
            self.modele.player_tags.append("Utilise Foudre Basique")
        elif mot == "~Eveil~":
            self.modele.player_tags.append("Utilise Sang Basique")



    def UseMagic(self, action):
        # [0]=%touche, [1]=degat, [2]=%crit, [3]=degat crit, [4]=%element,
        # [5]=description, [6]=message si rate, [7]=si touche, [8]=si touche crit
        # [9]=nombre tours, [10]=effet element
        self.RecupEndurance(4)
        action = self.EnleveurAffix(action, True)
        action_est_possible, raison_si_action_pas_possible = (
                self.CheckSiSortPossibleEtAppliqueCoutSort(action)
            )
        if action_est_possible:
            if self.modele.mauvais_tachyon:
                self.ChangeChargeMauvaisTachyon("sort")
            if self.modele.bon_tachyon:
                self.ChangeChargeBonTachyon("sort")
            if self.Player.quete == "Moqueries Magiques" and self.modele.monstre_EstUnBoss:
                self.Player.quete = "Moqueries Magiques [Echec]"
            if action in self.modele.annuaire_de_caracteristique_des_sorts:
                caracteristique_du_sort = self.modele.annuaire_de_caracteristique_des_sorts[
                    action
                ]
                # regarde l'élément de l'action pour les bonus associés
                self.SetTypeOfAction(action)
                # application des modificateurs sur la chance de toucher
                pourcentage_de_touche = caracteristique_du_sort[0]
                if self.modele.oeuil_magique:
                    chance_de_rater = 100 - pourcentage_de_touche
                    chance_bonus_de_toucher = round(chance_de_rater/2)
                    pourcentage_de_touche += chance_bonus_de_toucher
                pourcentage_de_touche -= self.modele.CHANCERATERSORT
                pourcentage_de_touche += self.modele.CHANCEDETOUCHERBONUS
                if self.modele.a_utilise_feu_ce_tour and self.modele.oeuil_de_feu:
                    pourcentage_de_touche = 100
                elif self.modele.a_utilise_foudre_ce_tour and self.modele.oeuil_de_foudre:
                    pourcentage_de_touche = 100
                elif self.modele.a_utilise_terre_ce_tour and self.modele.oeuil_de_terre:
                    pourcentage_de_touche = 100
                elif self.modele.a_utilise_physique_ce_tour and self.modele.oeuil_de_physique:
                    pourcentage_de_touche = 100
                elif self.modele.a_utilise_sang_ce_tour and self.modele.oeuil_de_sang:
                    pourcentage_de_touche = 100
                elif self.modele.a_utilise_glace_ce_tour and self.modele.oeuil_de_glace:
                    pourcentage_de_touche = 100
                # application des modificateurs sur les degats de base
                degat_de_base = caracteristique_du_sort[1]
                pourcentage = self.modele.DEGATBONUSSORTS
                if self.modele.a_utilise_feu_ce_tour:
                    pourcentage += self.modele.DEGATBONUSSORTFEU
                elif self.modele.a_utilise_foudre_ce_tour:
                    pourcentage += self.modele.DEGATBONUSSORTFOUDRE
                elif self.modele.a_utilise_terre_ce_tour:
                    pourcentage += self.modele.DEGATBONUSSORTTERRE
                elif self.modele.a_utilise_physique_ce_tour:
                    pourcentage += self.modele.DEGATBONUSSORTPHYSIQUE
                elif self.modele.a_utilise_sang_ce_tour:
                    pourcentage += self.modele.DEGATBONUSSORTSANG
                elif self.modele.a_utilise_glace_ce_tour:
                    pourcentage += self.modele.DEGATBONUSSORTGLACE
                degat_de_base += round((pourcentage / 100) * degat_de_base)
                degat_de_base -= round(
                    (self.modele.BONUSREDUCTIONDEGAT / 100) * degat_de_base
                )
                # application des modificateurs sur les chances de coup critique
                pourcentage_de_critique = caracteristique_du_sort[2]
                pourcentage_de_critique += self.modele.CHANCESORTCRITIQUE
                # application des modificateurs sur les degats de coup critique
                degat_critique = caracteristique_du_sort[3]
                degat_critique += round(
                    (self.modele.DEGATBONUSSORTCRITIQUE / 100) * degat_critique
                )
                degat_critique += round(self.modele.accumulation_degat_sort_critique)
                # application des modificateurs sur les chances d'appliquer un element
                pourcentage_de_element = caracteristique_du_sort[4]
                if self.modele.a_utilise_feu_ce_tour:
                    pourcentage_de_element += self.modele.CHANCEBONUSDEFAIREBRULER
                elif self.modele.a_utilise_foudre_ce_tour:
                    pourcentage_de_element += self.modele.CHANCEBONUSDEFAIREPARALYSER
                elif self.modele.a_utilise_terre_ce_tour:
                    pourcentage_de_element += self.modele.CHANCEBONUSDEFAIRELAPIDER
                elif self.modele.a_utilise_sang_ce_tour:
                    pourcentage_de_element += self.modele.CHANCEBONUSDEFAIRESAIGNER
                elif self.modele.a_utilise_glace_ce_tour:
                    pourcentage_de_element += self.modele.CHANCEBONUSDEFAIREGELER
                description = caracteristique_du_sort[5]
                nombre_aleatoire = random.randint(0, 100)
                degat = 0
                # ca touche ?
                if nombre_aleatoire < pourcentage_de_touche:
                    commentaire_element = ""
                    commentaire_a_afficher = caracteristique_du_sort[7]
                    degat += degat_de_base
                    # ca fait un critique ?
                    if nombre_aleatoire < pourcentage_de_critique:
                        commentaire_a_afficher = caracteristique_du_sort[8]
                        degat += degat_critique
                    # ca declenche  un effet elementaire ?
                    if nombre_aleatoire < pourcentage_de_element:
                        # si oui, quel effet ?
                        if self.modele.a_utilise_feu_ce_tour:
                            # deja en feu ?
                            if self.modele.monstre_est_en_feu:
                                nombre_aleatoire = random.randint(1, 100)
                                if nombre_aleatoire <= 90:
                                    # addition des tours
                                    nombre_tour = caracteristique_du_sort[9]
                                    nombre_tour += self.modele.TOURBONUSENNEMIENFEU
                                    if self.modele.stigma_monstre_negatif == "Inflammable":
                                        nombre_tour += nombre_tour
                                    if self.modele.utilise_rafale:
                                        nombre_tour += nombre_tour
                                    self.modele.monstre_est_en_feu_nombre_tour += (
                                        nombre_tour
                                    )
                                    commentaire_element = f"\nVous enflammez l'ennemi pour {nombre_tour} tours supplémentaires !"
                                    # ajustement des degats
                                    degat_du_feu = caracteristique_du_sort[10]
                                    if (
                                        self.modele.monstre_est_en_feu_degat
                                        < degat_du_feu
                                    ):
                                        self.modele.monstre_est_en_feu_degat = (
                                            degat_du_feu
                                        )
                                else:
                                    # finition des degats
                                    pourcentage_degat_du_feu = (
                                        self.modele.monstre_est_en_feu_nombre_tour
                                        * (
                                            self.modele.monstre_est_en_feu_degat
                                            + self.modele.DEGATBONUSFEU
                                        )
                                    )
                                    degat_du_feu = round(
                                        pourcentage_degat_du_feu
                                        * self.modele.monstre_points_de_vie_max
                                    )
                                    degat_du_feu = self.SiZeroRameneAUn(degat_du_feu)
                                    self.modele.monstre_points_de_vie -= degat_du_feu
                                    # arret du feu
                                    self.modele.monstre_est_en_feu_nombre_tour = 0
                                    self.modele.monstre_est_en_feu_degat = 0
                                    self.modele.monstre_est_en_feu = False
                                    # paralysie
                                    self.modele.monstre_est_paralyse = True
                                    self.modele.monstre_est_paralyse_nombre_tour = 2
                                    # construction du comentaire_element
                                    commentaire_element = ("\nVous enflammez l'ennemi.\nCepandant, les"
                                                       " deux feux s'éteignent mutuellement en"
                                                       " consommant l'oxygène disponible, et lui "
                                                       "font de gros dégâts.\nDe plus, le choc le "
                                                       "paralyse !")
                            else:
                                # mise a feu du monstre
                                self.modele.monstre_est_en_feu = True
                                nombre_tour = caracteristique_du_sort[9]
                                nombre_tour += self.modele.TOURBONUSENNEMIENFEU
                                if self.modele.stigma_monstre_negatif == "Inflammable":
                                    nombre_tour += nombre_tour
                                if self.modele.utilise_rafale:
                                    nombre_tour += nombre_tour
                                self.modele.monstre_est_en_feu_nombre_tour += (
                                    nombre_tour
                                )
                                self.modele.monstre_est_en_feu_degat = (
                                    caracteristique_du_sort[10]
                                )

                                commentaire_element = f"\nVous enflammez l'ennemi pendant {nombre_tour} tours !"
                        if self.modele.a_utilise_foudre_ce_tour:
                            if self.modele.stigma_monstre_positif == "Hardi":
                                commentaire_element = f"\nL'ennemi résiste a la paralysie !"
                            else:
                                self.modele.monstre_est_paralyse = True
                                self.modele.monstre_passe_son_tour = True
                                nombre_tour_para = caracteristique_du_sort[9] + self.modele.TOURBONUSENNEMIENPARALYSIE
                                self.modele.monstre_est_paralyse_nombre_tour += (
                                    nombre_tour_para
                                )
                                commentaire_element = f"\nVous paralysez l'ennemi pendant {nombre_tour_para} tours !"
                        if self.modele.a_utilise_glace_ce_tour:
                            self.modele.monstre_est_gele = True
                            nombre_tour_gele = caracteristique_du_sort[9] + self.modele.TOURBONUSENNEMIENGLACE
                            self.modele.monstre_est_gele_nombre_tour += (
                                nombre_tour_gele
                            )
                            commentaire_element = f"\nVous gelez l'ennemi pendant {nombre_tour_gele} tours !"
                            if nombre_tour_gele <= 0 :
                                commentaire_element = "De part son origine nordique, l'ennemi résiste au gel infligé !"
                                self.modele.monstre_est_gele = False
                                self.modele.monstre_est_gele_nombre_tour = 0
                        if self.modele.a_utilise_sang_ce_tour:
                            if ("Voluntad U Kiikel") in self.modele.monstre_tags:
                                commentaire_degat = f"\nVoluntad U Kiikel, l'esprit de sang, absorbe le drain de vie infligé à {self.modele.monstre_nom} !"
                            else:
                                # calcul de la saignee
                                pourcentage_saignee = caracteristique_du_sort[10]
                                pourcentage_saignee += self.modele.DEGATSAIGNEE
                                degat_saignee = round(
                                    (pourcentage_saignee / 100)
                                    * self.modele.monstre_points_de_vie_max
                                )
                                degat_saignee = self.AppliqueLimitationSaignee(degat_saignee)
                                # application de la saignee
                                self.modele.monstre_points_de_vie -= degat_saignee
                                soin_saignee = degat_saignee
                                soin_saignee += round(
                                    (self.modele.SOINSSAIGNEE / 100) * degat_saignee
                                )
                                self.modele.points_de_vie += soin_saignee
                                self.EquilibragePointsDeVieEtManaEtEndurance()
                                commentaire_element = f"\nVous drainez {degat_saignee} points de vie a l'adversaire, et en récuperez {soin_saignee} !"
                                if self.modele.anemie:
                                    commentaire_element += self.AppliqueTalentAnemie()
                                if self.modele.baron_rouge:
                                    commentaire_element += self.AppliqueTalentBaronRouge()
                                if self.modele.anticoagulants:
                                    degat_de_saignement = round(degat * 0.2)
                                    self.modele.monstre_points_de_vie -= degat_de_saignement
                                    commentaire_element += f"\nVous infligez {degat_de_saignement} points de vie a l'adversaire par saignement !"
                        if self.modele.a_utilise_terre_ce_tour:
                            # calcul de lapidation
                            pourcentage_lapidation = caracteristique_du_sort[10]
                            pourcentage_lapidation += self.modele.DEGATLAPIDATION
                            degat_lapidation = round(
                                (pourcentage_lapidation / 100) * degat
                            )
                            # application lapidation
                            degat_lapidation= self.SiZeroRameneAUn(degat_lapidation)
                            if ("Voluntad Le Luumo") in self.modele.monstre_tags:
                                commentaire_degat += f"\nVoluntad Le Luumo, l'esprit de terre, absorbe la lapidation infligée sur {self.modele.monstre_nom} !"
                            else:
                                self.modele.monstre_points_de_vie -= degat_lapidation
                                # construction du comentaire_element
                                commentaire_element = f"\nVous infligez {degat_lapidation} points de vie supplémentaire par lapidation !"
                                if self.modele.eboulis:
                                    commentaire_element += self.AppliqueTalentEboulis(degat_lapidation)
                                if self.modele.fracturation:
                                    commentaire_element += self.AppliqueTalentFracturation()

                    nombre_aleatoire_basique = random.randint(0, 100)
                    if "Utilise Feu Basique" in self.modele.player_tags:
                        self.modele.player_tags.remove("Utilise Feu Basique")
                        if nombre_aleatoire_basique <= 15:
                            if self.modele.monstre_est_en_feu:
                                nombre_aleatoire = random.randint(1, 100)
                                if nombre_aleatoire <= 90:
                                    # addition des tours
                                    nombre_tour = 4
                                    nombre_tour += self.modele.TOURBONUSENNEMIENFEU
                                    if self.modele.stigma_monstre_negatif == "Inflammable":
                                        nombre_tour += nombre_tour
                                    if self.modele.utilise_rafale:
                                        nombre_tour += nombre_tour
                                    self.modele.monstre_est_en_feu_nombre_tour += (
                                        nombre_tour
                                    )
                                    commentaire_element = f"\nVous enflammez l'ennemi pour {nombre_tour} tours supplémentaires !"
                                    # ajustement des degats
                                    degat_du_feu = 7
                                    if (
                                        self.modele.monstre_est_en_feu_degat
                                        < degat_du_feu
                                    ):
                                        self.modele.monstre_est_en_feu_degat = (
                                            degat_du_feu
                                        )
                                else:
                                    # finition des degats
                                    pourcentage_degat_du_feu = (
                                        self.modele.monstre_est_en_feu_nombre_tour
                                        * (
                                            self.modele.monstre_est_en_feu_degat
                                            + self.modele.DEGATBONUSFEU
                                        )
                                    )
                                    degat_du_feu = round(
                                        pourcentage_degat_du_feu
                                        * self.modele.monstre_points_de_vie_max
                                    )
                                    degat_du_feu = self.SiZeroRameneAUn(degat_du_feu)
                                    self.modele.monstre_points_de_vie -= degat_du_feu
                                    # arret du feu
                                    self.modele.monstre_est_en_feu_nombre_tour = 0
                                    self.modele.monstre_est_en_feu_degat = 0
                                    self.modele.monstre_est_en_feu = False
                                    # paralysie
                                    self.modele.monstre_est_paralyse = True
                                    self.modele.monstre_est_paralyse_nombre_tour = 2
                                    # construction du comentaire_element
                                    commentaire_element = ("\nVous enflammez l'ennemi.\nCepandant, les"
                                                        " deux feux s'éteignent mutuellement en"
                                                        " consommant l'oxygène disponible, et lui "
                                                        "font de gros dégâts.\nDe plus, le choc le "
                                                        "paralyse !")
                            else:
                                # mise a feu du monstre
                                self.modele.monstre_est_en_feu = True
                                nombre_tour = 4
                                nombre_tour += self.modele.TOURBONUSENNEMIENFEU
                                if self.modele.stigma_monstre_negatif == "Inflammable":
                                    nombre_tour += nombre_tour
                                if self.modele.utilise_rafale:
                                    nombre_tour += nombre_tour
                                self.modele.monstre_est_en_feu_nombre_tour += (
                                    nombre_tour
                                )
                                self.modele.monstre_est_en_feu_degat = (
                                    7
                                )

                                commentaire_element = f"\nVous enflammez l'ennemi pendant {nombre_tour} tours !"
                    elif "Utilise Glace Basique" in self.modele.player_tags:
                        self.modele.player_tags.remove("Utilise Glace Basique")
                        if nombre_aleatoire_basique <= 17:
                            self.modele.monstre_est_gele = True
                            nombre_tour_gele = 3 + self.modele.TOURBONUSENNEMIENGLACE
                            self.modele.monstre_est_gele_nombre_tour += (
                                nombre_tour_gele
                            )
                            commentaire_element = f"\nVous gelez l'ennemi pendant {nombre_tour_gele} tours !"
                            if nombre_tour_gele <= 0 :
                                commentaire_element = "De part son origine nordique, l'ennemi résiste au gel infligé !"
                                self.modele.monstre_est_gele = False
                                self.modele.monstre_est_gele_nombre_tour = 0
                    elif "Utilise Terre Basique" in self.modele.player_tags:
                        self.modele.player_tags.remove("Utilise Terre Basique")
                        if nombre_aleatoire_basique <= 12:
                            # calcul de lapidation
                            pourcentage_lapidation = 85
                            pourcentage_lapidation += self.modele.DEGATLAPIDATION
                            degat_lapidation = round(
                                (pourcentage_lapidation / 100) * degat
                            )
                            # application lapidation
                            degat_lapidation= self.SiZeroRameneAUn(degat_lapidation)
                            if ("Voluntad Le Luumo") in self.modele.monstre_tags:
                                commentaire_degat += f"\nVoluntad Le Luumo, l'esprit de terre, absorbe la lapidation infligée sur {self.modele.monstre_nom} !"
                            else:
                                self.modele.monstre_points_de_vie -= degat_lapidation
                                # construction du comentaire_element
                                commentaire_element = f"\nVous infligez {degat_lapidation} points de vie supplémentaire par lapidation !"
                                if self.modele.eboulis:
                                    commentaire_element += self.AppliqueTalentEboulis(degat_lapidation)
                                if self.modele.fracturation:
                                    commentaire_element += self.AppliqueTalentFracturation()
                    elif "Utilise Foudre Basique" in self.modele.player_tags:
                        if nombre_aleatoire_basique <= 7:
                            self.modele.player_tags.remove("Utilise Foudre Basique")
                            if self.modele.stigma_monstre_positif == "Hardi":
                                commentaire_element = f"\nL'ennemi résiste a la paralysie !"
                            else:
                                self.modele.monstre_est_paralyse = True
                                self.modele.monstre_passe_son_tour = True
                                nombre_tour_para = 2 + self.modele.TOURBONUSENNEMIENPARALYSIE
                                self.modele.monstre_est_paralyse_nombre_tour += (
                                    nombre_tour_para
                                )
                                commentaire_element = f"\nVous paralysez l'ennemi pendant {nombre_tour_para} tours !"
                    elif "Utilise Sang Basique" in self.modele.player_tags:
                        self.modele.player_tags.remove("Utilise Sang Basique")
                        if nombre_aleatoire_basique <= 15:
                            if ("Voluntad U Kiikel") in self.modele.monstre_tags:
                                commentaire_degat = f"\nVoluntad U Kiikel, l'esprit de sang, absorbe le drain de vie infligé à {self.modele.monstre_nom} !"
                            else:
                                # calcul de la saignee
                                pourcentage_saignee = 3
                                pourcentage_saignee += self.modele.DEGATSAIGNEE
                                degat_saignee = round(
                                    (pourcentage_saignee / 100)
                                    * self.modele.monstre_points_de_vie_max
                                )
                                degat_saignee = self.AppliqueLimitationSaignee(degat_saignee)
                                # application de la saignee
                                self.modele.monstre_points_de_vie -= degat_saignee
                                soin_saignee = degat_saignee
                                soin_saignee += round(
                                    (self.modele.SOINSSAIGNEE / 100) * degat_saignee
                                )
                                self.modele.points_de_vie += soin_saignee
                                self.EquilibragePointsDeVieEtManaEtEndurance()
                                commentaire_element = f"\nVous drainez {degat_saignee} points de vie a l'adversaire, et en récuperez {soin_saignee} !"
                                if self.modele.anemie:
                                    commentaire_element += self.AppliqueTalentAnemie()
                                if self.modele.baron_rouge:
                                    commentaire_element += self.AppliqueTalentBaronRouge()
                                if self.modele.anticoagulants:
                                    degat_de_saignement = round(degat * 0.2)
                                    self.modele.monstre_points_de_vie -= degat_de_saignement
                                    commentaire_element += f"\nVous infligez {degat_de_saignement} points de vie a l'adversaire par saignement !"
                    degat = self.SiZeroRameneAUn(degat)
                    commentaire_degat = (
                        f"Vous infligez {degat} points de dégât a l'ennemi !"
                    )
                    commentaire_degat += commentaire_element
                    self.modele.monstre_points_de_vie -= degat
                    self.vue.AfficheSonSort(self.sound_of_action)
                else:
                    commentaire_a_afficher = caracteristique_du_sort[6]
                    commentaire_degat = "Vous n'infligez aucun degat a l'ennemi."
                    commentaire_element = ""
                self.vue.AfficheSortOuAttaque(
                    description, commentaire_a_afficher, commentaire_degat
                )
            else:
                # attaques qui ne rentrent pas dans la méthode globale (fait plus que juste des degat ou un element)
                if action in self.modele.sorts_de_soin:
                    commentaire_sort = f"Vous utilisez le sort [{action}]."
                    commentaire_description_du_sort = self.modele.annuaire_de_description_des_sorts_de_soin[action]
                    soin = round((self.modele.annuaire_de_pourcentage_de_soin_des_sorts[action] / 100) * self.modele.points_de_vie_max)
                    if soin < self.modele.annuaire_de_soin_minimum_des_sorts[action]:
                        soin = self.modele.annuaire_de_soin_minimum_des_sorts[action]
                    self.modele.points_de_vie += soin
                    self.EquilibragePointsDeVieEtManaEtEndurance()
                    commentaire_soin = f"Vous reprenez {soin} points de vie !"
                    nombre_aleatoire_basique = random.randint(0, 100)
                    if "Utilise Feu Basique" in self.modele.player_tags:
                        self.modele.player_tags.remove("Utilise Feu Basique")
                        if nombre_aleatoire_basique <= 15:
                            if self.modele.monstre_est_en_feu:
                                nombre_aleatoire = random.randint(1, 100)
                                if nombre_aleatoire <= 90:
                                    # addition des tours
                                    nombre_tour = 4
                                    nombre_tour += self.modele.TOURBONUSENNEMIENFEU
                                    if self.modele.stigma_monstre_negatif == "Inflammable":
                                        nombre_tour += nombre_tour
                                    if self.modele.utilise_rafale:
                                        nombre_tour += nombre_tour
                                    self.modele.monstre_est_en_feu_nombre_tour += (
                                        nombre_tour
                                    )
                                    commentaire_soin += f"\nVous enflammez l'ennemi pour {nombre_tour} tours supplémentaires !"
                                    # ajustement des degats
                                    degat_du_feu = 7
                                    if (
                                        self.modele.monstre_est_en_feu_degat
                                        < degat_du_feu
                                    ):
                                        self.modele.monstre_est_en_feu_degat = (
                                            degat_du_feu
                                        )
                                else:
                                    # finition des degats
                                    pourcentage_degat_du_feu = (
                                        self.modele.monstre_est_en_feu_nombre_tour
                                        * (
                                            self.modele.monstre_est_en_feu_degat
                                            + self.modele.DEGATBONUSFEU
                                        )
                                    )
                                    degat_du_feu = round(
                                        pourcentage_degat_du_feu
                                        * self.modele.monstre_points_de_vie_max
                                    )
                                    degat_du_feu = self.SiZeroRameneAUn(degat_du_feu)
                                    self.modele.monstre_points_de_vie -= degat_du_feu
                                    # arret du feu
                                    self.modele.monstre_est_en_feu_nombre_tour = 0
                                    self.modele.monstre_est_en_feu_degat = 0
                                    self.modele.monstre_est_en_feu = False
                                    # paralysie
                                    self.modele.monstre_est_paralyse = True
                                    self.modele.monstre_est_paralyse_nombre_tour = 2
                                    # construction du comentaire_element
                                    commentaire_soin += ("\nVous enflammez l'ennemi.\nCepandant, les"
                                                        " deux feux s'éteignent mutuellement en"
                                                        " consommant l'oxygène disponible, et lui "
                                                        "font de gros dégâts.\nDe plus, le choc le "
                                                        "paralyse !")
                            else:
                                # mise a feu du monstre
                                self.modele.monstre_est_en_feu = True
                                nombre_tour = 4
                                nombre_tour += self.modele.TOURBONUSENNEMIENFEU
                                if self.modele.stigma_monstre_negatif == "Inflammable":
                                    nombre_tour += nombre_tour
                                if self.modele.utilise_rafale:
                                    nombre_tour += nombre_tour
                                self.modele.monstre_est_en_feu_nombre_tour += (
                                    nombre_tour
                                )
                                self.modele.monstre_est_en_feu_degat = (
                                    7
                                )

                                commentaire_soin += f"\nVous enflammez l'ennemi pendant {nombre_tour} tours !"
                    elif "Utilise Glace Basique" in self.modele.player_tags:
                        self.modele.player_tags.remove("Utilise Glace Basique")
                        if nombre_aleatoire_basique <= 17:
                            self.modele.monstre_est_gele = True
                            nombre_tour_gele = 3 + self.modele.TOURBONUSENNEMIENGLACE
                            self.modele.monstre_est_gele_nombre_tour += (
                                nombre_tour_gele
                            )
                            commentaire_soin += f"\nVous gelez l'ennemi pendant {nombre_tour_gele} tours !"
                            if nombre_tour_gele <= 0 :
                                commentaire_soin += "De part son origine nordique, l'ennemi résiste au gel infligé !"
                                self.modele.monstre_est_gele = False
                                self.modele.monstre_est_gele_nombre_tour = 0
                    elif "Utilise Terre Basique" in self.modele.player_tags:
                        self.modele.player_tags.remove("Utilise Terre Basique")
                        if nombre_aleatoire_basique <= 12:
                            # calcul de lapidation
                            pourcentage_lapidation = 85
                            pourcentage_lapidation += self.modele.DEGATLAPIDATION
                            degat_lapidation = round(
                                (pourcentage_lapidation / 100) * 30
                            )
                            # application lapidation
                            degat_lapidation= self.SiZeroRameneAUn(degat_lapidation)
                            if ("Voluntad Le Luumo") in self.modele.monstre_tags:
                                commentaire_soin += f"\nVoluntad Le Luumo, l'esprit de terre, absorbe la lapidation infligée sur {self.modele.monstre_nom} !"
                            else:
                                self.modele.monstre_points_de_vie -= degat_lapidation
                                # construction du comentaire_element
                                commentaire_soin += f"\nVous infligez {degat_lapidation} points de vie supplémentaire par lapidation !"
                                if self.modele.eboulis:
                                    commentaire_element += self.AppliqueTalentEboulis(degat_lapidation)
                                if self.modele.fracturation:
                                    commentaire_element += self.AppliqueTalentFracturation()
                    elif "Utilise Foudre Basique" in self.modele.player_tags:
                        if nombre_aleatoire_basique <= 7:
                            self.modele.player_tags.remove("Utilise Foudre Basique")
                            if self.modele.stigma_monstre_positif == "Hardi":
                                commentaire_soin += f"\nL'ennemi résiste a la paralysie !"
                            else:
                                self.modele.monstre_est_paralyse = True
                                self.modele.monstre_passe_son_tour = True
                                nombre_tour_para = 2 + self.modele.TOURBONUSENNEMIENPARALYSIE
                                self.modele.monstre_est_paralyse_nombre_tour += (
                                    nombre_tour_para
                                )
                                commentaire_soin += f"\nVous paralysez l'ennemi pendant {nombre_tour_para} tours !"
                    elif "Utilise Sang Basique" in self.modele.player_tags:
                        self.modele.player_tags.remove("Utilise Sang Basique")
                        if nombre_aleatoire_basique <= 15:
                            if ("Voluntad U Kiikel") in self.modele.monstre_tags:
                                commentaire_soin += f"\nVoluntad U Kiikel, l'esprit de sang, absorbe le drain de vie infligé à {self.modele.monstre_nom} !"
                            else:
                                # calcul de la saignee
                                pourcentage_saignee = 3
                                pourcentage_saignee += self.modele.DEGATSAIGNEE
                                degat_saignee = round(
                                    (pourcentage_saignee / 100)
                                    * self.modele.monstre_points_de_vie_max
                                )
                                degat_saignee = self.AppliqueLimitationSaignee(degat_saignee)
                                # application de la saignee
                                self.modele.monstre_points_de_vie -= degat_saignee
                                soin_saignee = degat_saignee
                                soin_saignee += round(
                                    (self.modele.SOINSSAIGNEE / 100) * degat_saignee
                                )
                                self.modele.points_de_vie += soin_saignee
                                self.EquilibragePointsDeVieEtManaEtEndurance()
                                commentaire_soin += f"\nVous drainez {degat_saignee} points de vie a l'adversaire, et en récuperez {soin_saignee} !"
                                if self.modele.anemie:
                                    commentaire_soin += self.AppliqueTalentAnemie()
                                if self.modele.baron_rouge:
                                    commentaire_soin += self.AppliqueTalentBaronRouge()
                                if self.modele.anticoagulants:
                                    degat_de_saignement = 20
                                    self.modele.monstre_points_de_vie -= degat_de_saignement
                                    commentaire_soin += f"\nVous infligez {degat_de_saignement} points de vie a l'adversaire par saignement !"
                    self.vue.AfficheSortDeSoin(commentaire_sort, commentaire_description_du_sort, commentaire_soin)
                elif action == "Rafale":
                    commentaire = ("Vous invoquez des vents venus d'autres mondes pour assister votre"
                                   " feu pendant 3 tours.\nVos prochaines actions feront bruler deux"
                                   " fois plus longtemps leur cible.")
                    self.modele.utilise_rafale = True
                    self.modele.rafale_nombre_tours += 4
                    self.vue.AfficheRafale(commentaire)
                elif action == "Avalanche":
                    degat_de_base = round(self.modele.monstre_points_de_vie_max*0.08)
                    pourcentage = (self.modele.DEGATBONUSSORTGLACE +
                                   self.modele.DEGATBONUSSORTTERRE +
                                   self.modele.DEGATBONUSSORTS)
                    degat += round((pourcentage / 100) * degat_de_base )
                    commentaire = ("Vous invoquez une avalanche de rochers et de glace !"
                                   "\nL'ennemi se retrouve gelé pendant 2 tours et"
                                   f" perd {degat} points de vie par lapidation ! ")
                    if self.modele.eboulis:
                                commentaire += self.AppliqueTalentEboulis(degat)
                    if self.modele.fracturation:
                                commentaire += self.AppliqueTalentFracturation()
                    degat = self.SiZeroRameneAUn(degat)
                    if ("Voluntad Le Luumo") in self.modele.monstre_tags:
                                commentaire = ("Vous invoquez une avalanche de rochers et de glace !"
                                   "\nL'ennemi se retrouve gelé pendant 2 tours, mais "
                                   f"Voluntad Le Luumo, l'esprit de terre, absorbe la lapidation infligée sur {self.modele.monstre_nom} !")
                    else:
                        self.modele.monstre_points_de_vie -= degat
                    self.modele.monstre_est_gele = True
                    self.modele.monstre_est_gele_nombre_tour += 3
                    self.vue.AfficheAvalanche(commentaire)
                elif action == "Libération Enflammée":
                    commentaire = ("Vous ne faites qu'un avec le feu."
                          "\nVos mouvements sont synchronisés avec le rythme invisible"
                          " qui fait danser les flammes. Par un enchainement esoterique"
                          " de déplacements, vous enflammez l'ennemi pendant 5 tours.")
                    commentaire_2 = ("A cause du manque soudain d'oxygène dans la salle,"
                                     " vous ne pouvez plus parler pendant 3 tours.")
                    self.modele.monstre_est_en_feu = True
                    self.modele.monstre_est_en_feu_degat = 5
                    self.modele.monstre_est_en_feu_nombre_tour += 6
                    self.modele.est_maudit_par_les_sorts = True
                    self.modele.est_maudit_par_les_sorts_nombre_tour = 4
                    self.vue.AfficheLiberationFeu(commentaire, commentaire_2)
                elif action == "Libération Fulgurante":
                    commentaire = ("Vous ne faites qu'un avec la foudre."
                          "\nVous pouvez voir l'électricité parcourir le corps du monstre."
                          " Vous l'approchez sans qu'il n'aie le temps"
                          " de réagir et appuyez sur certains points d'acuponcture pour rediriger les"
                          " signaux electriques de son cerveau vers ses muscles. Il devient paralysé pendant 4 tours")
                    commentaire_2 = ("Votre soudaine synchronisation avec la foudre a poussé votre corps dans ses derniers retranchements."
                                     "\nVous perdez 3 points de vie max et 3 points de mana max. Vous ne vous sentez pas bien.")
                    self.modele.points_de_vie_max -= 3
                    self.modele.points_de_mana_max -= 3
                    self.EquilibragePointsDeVieEtManaEtEndurance()
                    self.modele.monstre_est_paralyse = True
                    self.modele.monstre_est_paralyse_nombre_tour += 4
                    self.vue.AfficheLiberationFoudre(commentaire, commentaire_2)
                elif action == "Libération Glaciale":
                    commentaire = ("Vous ne faites qu'un avec la glace."
                          "\nLes particules qui composent votre corps s'arretent brusquement de bouger pendant un instant,"
                          " ce qui est assez pour ralentir les particules de la salle a une temperature proche du zéro absolu."
                          "\nL'ennemi ne réchappe pas de cette interaction sans egratinures, et devient gelé pendant 8 tours.")
                    degat = round(self.modele.points_de_vie_max*0.2)
                    degat = self.EnleveVieAuJoueur(degat)
                    commentaire_2 = ("Vous non plus d'ailleurs. Le temps que le sang se remette a bouger dans vos veines,"
                                     f" votre corps subit des dégats graves et perd {degat} points de vie. De plus, le sang gelé a "
                                     "éclaté vos veines a certains endroits. Vous etes blessé pendant 5 tours.")
                    self.modele.monstre_est_gele = True
                    self.modele.monstre_est_gele_nombre_tour += 8
                    self.modele.est_maudit_par_la_vie = True
                    self.modele.est_maudit_par_la_vie_nombre_tour = 6
                    self.vue.AfficheLiberationGlace(commentaire, commentaire_2)
                elif action == "Libération Sanglante":
                    commentaire = ("Vous ne faites qu'un avec le sang."
                          "\nVous pouvez sentir les globules rouges de votre corps interragir avec vos organes."
                          " \nVous plongez la main dans le corps du monstre, naviguez entre les organes sans percer"
                          " la structure interne de l'ennemi, et saisissez le canal qui apporte l'énergie a son systeme nerveux."
                          " \nD'une main experte, vous pratiquez une incision dans le canal et absorbez "
                          "la vitalité du monstre avant de vous faire repousser par ce dernier.")
                    degat = round(self.modele.points_de_vie_max * 0.2)
                    degat = self.SiZeroRameneAUn(degat)
                    commentaire_2 = (f"Vous recuperez {degat} points de mana et de vie. Mais la vitalité du monstre n'est pas"
                                     "entierement compatible avec la votre. Vous attrapez le Mal Jaune et devenez muet pendant 5 tours.")
                    self.modele.points_de_vie += degat
                    self.modele.monstre_points_de_vie -= degat
                    self.EquilibragePointsDeVieEtManaEtEndurance()
                    self.modele.est_maudit_par_le_gold = True
                    self.modele.est_maudit_par_le_gold_nombre_tour += 6
                    self.modele.est_maudit_par_les_sorts = True
                    self.modele.est_maudit_par_les_sorts_nombre_tour += 6
                    self.vue.AfficheLiberationSang(commentaire, commentaire_2)
                elif action == "Libération Holomélanocrate":
                    degat = round(self.modele.points_de_vie_max * 0.15)
                    degat = self.SiZeroRameneAUn(degat)
                    commentaire = ("Vous ne faites qu'un avec la terre."
                          "\nVous pouvez voir les chemins magiques qui parcourent le sol."
                          " Vous puisez dans la puissance d'un leys pour faire sortir des piliers de magma du plus profond des souterrains."
                          "\nCes derniers écrasent l'ennemi et reffroidissent si vite que les cristaux qui s'y forment peuvent penetrer"
                          f" dans les vaisseaux sanguins du monstre. Il perd {degat} points de vie et "
                          "devient plus vulnérable aux effet élémentaires pendant 5 tours !")
                    commentaire_2 = ("L'énergie qui s'est mise a parcourir votre corps a completement destabilisé votre réserve "
                                     "de mana. Celui ci se répend dans les airs et destabilise vos prochains sorts pendant 4 tours.")
                    self.modele.monstre_points_de_vie -= degat
                    self.modele.monstre_est_vulnerable = True
                    self.modele.monstre_est_vulnerable_nombre_tour = 6
                    self.modele.monstre_niveau_de_vulnerabilite = 15
                    self.modele.points_de_mana = 0
                    self.modele.est_maudit_par_le_mana = True
                    self.modele.est_maudit_par_le_mana_nombre_tour += 5
                    self.vue.AfficheLiberationTerre(commentaire, commentaire_2)
                elif action == "Mirroir d'Eau":
                    self.modele.utilise_mirroir_eau = True
                    self.modele.mirroir_eau_nombre_tours = 3
                    commentaire = ("Vous utilisez le mirroir d'eau !\n"
                                   "Un disque d'eau trop fin pour voir a l'oeil nu se forme devant vous et"
                                   " renvoie les degats venant de l'ennemi pendant 2 tours.")
                    self.vue.AfficheMirroirEau(commentaire)
                elif action == "Brume de Sang":
                    self.modele.utilise_brume_sang = True
                    self.modele.brume_sang_nombre_tours = 3
                    commentaire = ("Vous utilisez la brume de sang !\n"
                                   "Un brouillard de guerre de couleur ocre se forme devant vous et"
                                   " convertit les degats venant de l'ennemi en soins pendant 2 tours.")
                    self.vue.AfficheBrumeSang(commentaire)
                elif action == "Explosion de Feu Sacré":
                    degat = round(self.modele.monstre_points_de_vie_max*0.05)
                    vie_recue = round(self.modele.points_de_vie_max*0.12)
                    mana_recu = round(self.modele.points_de_mana_max*0.12)
                    gold_recu = degat
                    commentaire = ("Vous invoquez une explosion de feu sacré dans la salle !"
                                   f"\nL'ennemi perd {degat} points de vie !"
                                   f"\nVous regagnez {vie_recue} points de vie !"
                                   f"\nVous regagnez {mana_recu} points de mana !"
                                   f"\nVous gagnez {gold_recu} golds !"
                                   f"\nVous êtes béni par le feu sacré ! Vos deux prochaines attaques seront critique !")
                    self.modele.monstre_points_de_vie -= degat
                    self.modele.points_de_vie += vie_recue
                    self.RecouvrementDeMana(mana_recu)
                    self.modele.nombre_de_gold += gold_recu
                    self.modele.beni_par_feu_sacre = True
                    self.modele.beni_par_feu_sacre_nombre_tour += 3
                    self.vue.AfficheFeuSacre(commentaire)
                elif action == "Carrousel":
                    commentaire = ("Vous invoquez un carnaval magique de couleurs et de sons ! C'est la fête !")
                    self.vue.AfficheDebutCarrousel(commentaire)
                    nombre_de_evenement = 0
                    while nombre_de_evenement != 5:
                        element_aleatoire = random.randint(1, 4)
                        if element_aleatoire == 1:
                            commentaire = "Un ballon rouge éclate au dessus du monstre ! Il se retrouve enflammé pendant 2 tours !"
                            self.modele.monstre_est_en_feu = True
                            self.modele.monstre_est_en_feu_degat = 5
                            self.modele.monstre_est_en_feu_nombre_tour += 3
                        elif element_aleatoire == 2:
                            commentaire = "Un serpentin bleu s'enroule autour du torse du monstre ! Il se retrouve gelé pendant 2 tours !"
                            self.modele.monstre_est_gele = True
                            self.modele.monstre_est_gele_nombre_tour += 3
                        elif element_aleatoire == 3:
                            commentaire = "Une tarte a la crême atterit sur la tête du monstre ! Il se retrouve paralysé pendant 1 tour !"
                            self.modele.monstre_est_paralyse = True
                            self.modele.monstre_est_paralyse_nombre_tour += 1
                        elif element_aleatoire == 4:
                            commentaire = "La fumée des feux d'artifices encercle L'ennemi! Il se retrouve vulnerable pendant 2 tour !"
                            self.modele.monstre_est_vulnerable = True
                            self.modele.monstre_est_vulnerable_nombre_tour += 3
                            self.modele.monstre_niveau_de_vulnerabilite = 10
                        nombre_de_evenement += 1
                        self.vue.AfficheCarrousel(commentaire)
                    commentaire = "Quel spectacle !"
                    self.vue.AfficheFinCarrousel(commentaire)
                elif action == "Faire fuir le Domovoï":
                    if self.modele.vie_domovoi != 0:
                        self.modele.vie_domovoi -= 1
                        commentaire = "Vous faites refroidir vos main avec un peu de mana et les approchez du domovoï."
                        if self.modele.vie_domovoi == 0:
                            self.modele.retour_domovoi = self.modele.nombre_de_tours + 6
                            commentaire += "\nCelui-ci court se cacher derrière un four en ruine, un peu plus chaud, pendant quelques temps !"
                        else:
                            commentaire += "\nCelui-ci grimace en vous voyant venir et recule de quelques pas."
                    else :
                        commentaire = ("Vous vous dirigez vers la cachette du domovoï, et trébuchez sur une bouse de vache solidifiée."
                                       "\nCela vous laisse le temps de réfléchir, et vous décidez de laisser le domovoï tranquille."
                                       "\nPensez, cela serait honteux d'aller aggresser quelqu'un qui n'est plus sur le champ de bataille !")
                    self.vue.AfficheActionDomovoi(commentaire)
                elif action == "Faire fuir la Kikimora":
                    if self.modele.vie_kikimora != 0:
                        self.modele.vie_kikimora -= 1
                        commentaire = "Vous faites refroidir vos main avec un peu de mana et les approchez de la kikimora."
                        if self.modele.vie_kikimora == 0:
                            self.modele.retour_kikimora = self.modele.nombre_de_tours + 6
                            commentaire += "\nCelle-ci court se cacher derrière un four en ruine, un peu plus chaud, pendant quelques temps !"
                        else:
                            commentaire += "\nCelle-ci grimace en vous voyant venir et recule de quelques pas."
                    else :
                        commentaire = ("Vous vous dirigez vers la cachette de la kikimora, et trébuchez sur une bouse de vache solidifiée."
                                       "\nCela vous laisse le temps de réfléchir, et vous décidez de laisser la kikimora tranquille."
                                       "\nPensez, cela serait honteux d'aller aggresser quelqu'un qui n'est plus sur le champ de bataille !")
                    self.vue.AfficheActionKikimora(commentaire)
            if "Ecaille d'Ouroboros" in self.modele.liste_dartefacts_optionels:
                commentaire = "l'Ecaille d'Ouroboros réagit a votre sort, et vous reprenez 2 points de vie !"
                self.modele.points_de_vie += 2
                self.EquilibragePointsDeVieEtManaEtEndurance()
                self.vue.AfficheOuroboros(commentaire)
        else:
            # affiche que laction s'est pas passée, et pourquoi
            self.vue.AfficheActionImpossible(raison_si_action_pas_possible)

    def AppliqueBenedictionMana(self):
        soin_mana = round(self.modele.points_de_vie_max*0.03)
        self.RecouvrementDeMana(soin_mana)
        commentaire = f"Les élements dans votre âme sont en harmonie, et vous regagnez {soin_mana} points de mana !"
        self.EquilibragePointsDeVieEtManaEtEndurance()
        self.vue.AfficheBenedictionMana(commentaire)

    def UseItem(self, nom_de_litem):
        # checke si on peut utiliser l'item
        self.RecupEndurance(4)
        action_est_possible, raison_si_action_pas_possible = (
                self.CheckSiItemPossible(nom_de_litem)
            )
        if action_est_possible:
            self.Sove.RajouteEntreeAuLivreCigogneBlancheSiOnAPas("Les Items", self.modele.monstre_nom)
            if self.modele.mauvais_tachyon:
                self.ChangeChargeMauvaisTachyon("item")
            if self.modele.bon_tachyon:
                self.ChangeChargeBonTachyon("item")
            if self.modele.stigma_joueur_negatif == "Trouble Obsessionnel Compulsif":
                self.EffetStigmaTOC()
            self.sound_of_action = "ITEM"
            if "Force et Honneur" in self.Player.quete :
                self.Player.quete = "Force et Honneur [Echec]"
            # enleve 1 au nombre d'item
            self.modele.items[nom_de_litem] -= 1
            commentaire = f"Vous utilisez l'item [{nom_de_litem}]"
            # applique l'effet de l'item
            if nom_de_litem in ["Feuille Jindagee", "Fruit Jindagee"]:
                if nom_de_litem == "Feuille Jindagee":
                    self.modele.utilise_feuille_jindagee = True
                    nombre_tour = 3
                    if "Larme d'Yggdrasil" in self.modele.liste_dartefacts_optionels:
                        nombre_tour += 3
                    self.modele.utilise_feuille_jindagee_nombre_tour += nombre_tour
                    soin = 5 + round(self.modele.points_de_vie_max * 0.05)
                    if soin < 8:
                        soin = 8
                    soin += round((self.modele.SUPPORTBONUSITEM / 100) * soin)
                    soin += self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Tisane d'Ecorce"]
                    commentaire_item = f"Vous reprenez {soin} pv pendant {nombre_tour} tours !"
                elif nom_de_litem == "Fruit Jindagee":
                    self.modele.utilise_fruit_jindagee = True
                    nombre_tour = 3
                    if "Larme d'Yggdrasil" in self.modele.liste_dartefacts_optionels:
                        nombre_tour += 3
                    self.modele.utilise_fruit_jindagee_nombre_tour += nombre_tour
                    soin = 10 + round(self.modele.points_de_vie_max * 0.1)
                    if soin < 13:
                        soin = 13
                    soin += round((self.modele.SUPPORTBONUSITEM / 100) * soin)
                    soin += self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Tisane d'Ecorce"]
                    commentaire_item = f"Vous reprenez {soin} pv pendant {nombre_tour} tours !"
            elif nom_de_litem in ["Feuille Aatma", "Fruit Aatma"]:
                if nom_de_litem == "Feuille Aatma":
                    self.modele.utilise_feuille_aatma = True
                    nombre_tour = 3
                    if "Larme d'Yggdrasil" in self.modele.liste_dartefacts_optionels:
                        nombre_tour += 3
                    self.modele.utilise_feuille_aatma_nombre_tour += nombre_tour
                    soin = 5 + round(self.modele.points_de_mana_max * 0.05)
                    if soin < 8:
                        soin = 8
                    soin += round((self.modele.SUPPORTBONUSITEM / 100) * soin)
                    soin += self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Tisane de Racine"]
                    commentaire_item = f"Vous reprenez {soin} pm pendant {nombre_tour} tours !"
                elif nom_de_litem == "Fruit Aatma":
                    self.modele.utilise_fruit_aatma = True
                    nombre_tour = 3
                    if "Larme d'Yggdrasil" in self.modele.liste_dartefacts_optionels:
                        nombre_tour += 3
                    self.modele.utilise_fruit_aatma_nombre_tour += nombre_tour
                    soin = 10 + round(self.modele.points_de_mana_max * 0.1)
                    if soin < 13:
                        soin = 13
                    soin += round((self.modele.SUPPORTBONUSITEM / 100) * soin)
                    soin += self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Tisane de Racine"]
                    commentaire_item = f"Vous reprenez {soin} pm pendant {nombre_tour} tours !"
            elif nom_de_litem in ["Crystal Elémentaire"]:
                element_aleatoire = random.randint(1, 4)
                if element_aleatoire == 1:
                    commentaire_item = "Le crystal prend une teinte rouge avant de se briser. L'ennemi se retrouve enflammé pendant 2 tours !"
                    self.modele.monstre_est_en_feu = True
                    self.modele.monstre_est_en_feu_degat = 5
                    self.modele.monstre_est_en_feu_nombre_tour += 3
                elif element_aleatoire == 2:
                    commentaire_item = "Le crystal prend une teinte bleue avant de se briser. L'ennemi se retrouve gelé pendant 2 tours !"
                    self.modele.monstre_est_gele = True
                    self.modele.monstre_est_gele_nombre_tour += 3
                elif element_aleatoire == 3:
                    commentaire_item = "Le crystal prend une teinte blanche avant de se briser. L'ennemi se retrouve paralysé pendant 2 tour !"
                    self.modele.monstre_est_paralyse = True
                    self.modele.monstre_est_paralyse_nombre_tour += 3
                    self.modele.monstre_passe_son_tour = True
                elif element_aleatoire == 4:
                    commentaire_item = "Le crystal prend une teinte noire avant de se briser. L'ennemi se retrouve vulnerable pendant 2 tour !"
                    self.modele.monstre_est_vulnerable = True
                    self.modele.monstre_est_vulnerable_nombre_tour += 3
                    self.modele.monstre_niveau_de_vulnerabilite = 10
                if ("Gant de Midas" in self.modele.liste_dartefacts_optionels) and self.modele.est_gele:
                    commentaire_item += "De plus, l'artefact [Gant de Midas] réagit au crystal et vous soigne de votre [Gelure] !"
                    self.modele.est_gele = False
                    self.modele.est_gele_nombre_tour = 0
                if ("Gant d'Héphaïstos" in self.modele.liste_dartefacts_optionels) and self.modele.est_en_feu:
                    commentaire_item += "De plus, l'artefact [Gant d'Héphaïstos] réagit au crystal et vous soigne de votre [Brulure] !"
                    self.modele.est_en_feu = False
                    self.modele.est_en_feu_nombre_tour = 0
                    self.modele.est_en_feu_degat = 0
            elif nom_de_litem in ["Ambroisie", "Hydromel"]:
                if nom_de_litem == "Ambroisie":
                    self.modele.utilise_ambroisie = True
                    self.modele.utilise_ambroisie_nombre_tour = 6
                    commentaire_item = "Le liquide couleur ambre coule dans votre gorge et vous sentez vos techniques devenir plus puissantes pendant 5 tours !"
                elif nom_de_litem == "Hydromel":
                    self.modele.utilise_hydromel = True
                    self.modele.utilise_hydromel_nombre_tour = 6
                    commentaire_item = "Le liquide couleur miel nacré coule dans votre gorge et vous sentez vos sorts devenir plus puissants pendant 5 tours !"
            elif nom_de_litem in ["Orbe de Furie", "Orbe de Folie"]:
                if nom_de_litem == "Orbe de Furie":
                    self.modele.utilise_orbe_de_furie = True
                    self.modele.utilise_orbe_de_furie_nombre_tour = 3
                    if "Demi-Masque de l'Ordre" in self.modele.liste_dartefacts_optionels:
                        self.modele.utilise_orbe_de_furie_nombre_tour += 1
                        commentaire_item = ("Vous tenez l'orbe entre vos main et plongez votre regard dans la chose furieuse qui tourne a l'interieur."
                                            "\nElle rentre alors dans votre esprit et augmente de maniere significative les degats de vos deux prochaines attaque !")
                    else:
                        commentaire_item = ("Vous tenez l'orbe entre vos main et plongez votre regard dans la chose furieuse qui tourne a l'interieur."
                                            "\nElle rentre alors dans votre esprit et augmente de maniere significative les degats de votre prochaine attaque !")
                elif nom_de_litem == "Orbe de Folie":
                    self.modele.utilise_orbe_de_folie = True
                    self.modele.utilise_orbe_de_folie_nombre_tour = 3
                    if "Demi-Masque du Chaos" in self.modele.liste_dartefacts_optionels:
                        self.modele.utilise_orbe_de_folie_nombre_tour += 1
                        commentaire_item = ("Vous tenez l'orbe entre vos main et plongez votre regard dans la chose folle qui tourne a l'interieur."
                                            "\nElle rentre alors dans votre esprit et augmente de maniere significative les degats de vos deux prochains sorts !")
                    else:
                        commentaire_item = ("Vous tenez l'orbe entre vos main et plongez votre regard dans la chose folle qui tourne a l'interieur."
                                            "\nElle rentre alors dans votre esprit et augmente de maniere significative les degats de votre prochain sort !")
            elif nom_de_litem in ["Remède", "Remède Superieur", "Remède Divin"]:
                if nom_de_litem == "Remède":
                    soin = round(self.modele.points_de_vie_max*0.1)
                    if soin < 17:
                        soin = 17
                elif nom_de_litem == "Remède Superieur":
                    soin = round(self.modele.points_de_vie_max*0.2)
                    if soin < 27:
                        soin = 27
                elif nom_de_litem == "Remède Divin":
                    soin = round(self.modele.points_de_vie_max*0.3)
                    if soin < 39:
                        soin = 39
                soin = self.AppliqueSupportBonusItem(soin, "vie")
                self.modele.points_de_vie += soin
                commentaire_item = f"Vous appliquez le remède sur vos blessures et regagnez {soin} points de vie !"
                self.EquilibragePointsDeVieEtManaEtEndurance
            elif nom_de_litem in ["Pillule", "Pillule Superieure", "Pillule Divine"]:
                if nom_de_litem == "Pillule":
                    soin = round(self.modele.points_de_mana_max*0.1)
                    if soin < 17:
                        soin = 17
                elif nom_de_litem == "Pillule Superieure":
                    soin = round(self.modele.points_de_mana_max*0.2)
                    if soin < 27:
                        soin = 27
                elif nom_de_litem == "Pillule Divine":
                    soin = round(self.modele.points_de_mana_max*0.3)
                    if soin < 39:
                        soin = 39
                soin = self.AppliqueSupportBonusItem(soin, "mana")
                self.RecouvrementDeMana(soin)
                commentaire_item = f"Vous avalez la pillule et regagnez {soin} points de mana !"
                self.EquilibragePointsDeVieEtManaEtEndurance
            elif nom_de_litem in ["Fléchette Rouge", "Fleche Rouge", "Fléchette Bleue", "Fleche Bleue"]:
                commentaire_item = "Vous lancez l'objet, qui vient se planter dans le torse du monstre."
                if nom_de_litem == "Fléchette Rouge":
                    commentaire_item += "\nL'ennemi s'enflamme pendant 3 tours !"
                    self.modele.monstre_est_en_feu = True
                    self.modele.monstre_est_en_feu_degat = 5
                    self.modele.monstre_est_en_feu_nombre_tour += 4
                elif nom_de_litem == "Fleche Rouge":
                    commentaire_item += "\nL'ennemi s'enflamme pendant 6 tours !"
                    self.modele.monstre_est_en_feu = True
                    self.modele.monstre_est_en_feu_degat = 5
                    self.modele.monstre_est_en_feu_nombre_tour += 7
                elif nom_de_litem == "Fléchette Bleue":
                    commentaire_item += "\nL'ennemi gèle pendant 3 tours !"
                    self.modele.monstre_est_gele = True
                    self.modele.monstre_est_gele_nombre_tour += 4
                elif nom_de_litem == "Fleche Bleue":
                    commentaire_item += "\nL'ennemi gèle pendant 6 tours !"
                    self.modele.monstre_est_gele = True
                    self.modele.monstre_est_gele_nombre_tour += 7
            elif nom_de_litem in ["Poudre Explosive", "Roche Explosive", "Bombe Explosive"]:
                degat = round(self.modele.monstre_points_de_vie_max*0.05)
                self.modele.monstre_est_vulnerable = True
                self.modele.monstre_est_vulnerable_nombre_tour = 6
                if nom_de_litem == "Poudre Explosive":
                    commentaire_item =( "Vous jetez la poudre aux yeux du monstre et frappez"
                                    " son visage de toutes vos force.\nLa poudre explose "
                                    "et le rend légèrement vulnérable pendant 5 tours !")
                    self.modele.monstre_niveau_de_vulnerabilite = 5
                elif nom_de_litem == "Roche Explosive":
                    commentaire_item =( "Vous jetez la roche aux pieds du monstre et protegez"
                                    " votre visage.\nLa roche explose "
                                    "et rend l'ennemi vulnérable pendant 5 tours !")
                    self.modele.monstre_niveau_de_vulnerabilite = 10
                elif nom_de_litem == "Bombe Explosive":
                    commentaire_item =( "Vous jetez la bombe sur L'ennemi et vous"
                                    " mettez a couvert derriere un morceau de débris.\nLa bombe explose "
                                    "et rend l'ennemi très vulnérable pendant 5 tours !")
                    self.modele.monstre_niveau_de_vulnerabilite = 15
                commentaire_item += f"\nDe plus, L'ennemi perd {degat} points de vie !"
            elif nom_de_litem in ["Fiole de Poison", "Gourde de Poison"]:
                self.modele.monstre_est_empoisonne = True
                if nom_de_litem == "Fiole de Poison":
                    self.modele.monstre_est_empoisonne_degat = 2.5
                    self.modele.monstre_est_empoisonne_nombre_tour = 11
                    commentaire_item = "Vous jetez la fiole sur L'ennemi.\nLe poison rentre dans son systeme et il devient empoisonné pendant 10 tours !"
                elif nom_de_litem == "Gourde de Poison":
                    self.modele.monstre_est_empoisonne_degat = 5
                    self.modele.monstre_est_empoisonne_nombre_tour = 6
                    commentaire_item = "Vous jetez la fiole sur L'ennemi.\nLe poison rentre dans son systeme et il devient gravement empoisonné pendant 5 tours !"
            elif nom_de_litem in ["Sève d'Absolution", "Larme d'Absolution", "Soluté d'Absolution"]:
                if not self.modele.monstre_EstUnBoss:
                    commentaire_item = "Vous répandez le contenu de l'objet sur le corps de l'ennemi...mais rien ne se passe."
                elif nom_de_litem == "Sève d'Absolution":
                    degat = round(self.modele.monstre_points_de_vie_max*0.07)
                    commentaire_item = ("Vous envoyez le liquide visqueux en direction du monstre.\nAux endroits ou la sève"
                                        " est en contact avec L'ennemi, de grosses cloques apparaissent."
                                        f"\nVous infligez {degat} points de degats a l'ennemi !")
                elif nom_de_litem == "Larme d'Absolution":
                    degat = round(self.modele.monstre_points_de_vie_max*0.11)
                    commentaire_item = ("Vous envoyez le liquide visqueux en direction du monstre.\nAux endroits ou les larmes"
                                        " entrent en contact avec L'ennemi, de grosse volutes de fumée apparaissent."
                                        f"\nVous infligez {degat} points de degats a l'ennemi !")
                elif nom_de_litem == "Soluté d'Absolution":
                    degat = round(self.modele.monstre_points_de_vie_max*0.15)
                    commentaire_item = ("Vous envoyez le liquide visqueux en direction du monstre.\nAux endroits ou le soluté"
                                        " est en contact avec L'ennemi, une sorte de feu de Saint-Elme brule paisiblement."
                                        f"\nVous réduisez ses points de vie max de {degat} !")
                self.modele.monstre_points_de_vie -= degat
                self.modele.monstre_points_de_vie_max -= degat
            elif nom_de_litem in ["Sève d'Exorcisme", "Larme d'Exorcisme", "Soluté d'Exorcisme"]:
                if self.modele.monstre_EstUnBoss:
                    commentaire_item = "Vous répandez le contenu de l'objet sur le corps de l'ennemi...mais rien ne se passe."
                elif nom_de_litem == "Sève d'Exorcisme":
                    degat = round(self.modele.monstre_points_de_vie_max*0.10)
                    commentaire_item = ("Vous envoyez le liquide visqueux en direction du monstre.\nAux endroits ou la sève"
                                        " est en contact avec L'ennemi, de grosses plaques rouge apparaissent."
                                        f"\nVous infligez {degat} points de degats a l'ennemi !")
                elif nom_de_litem == "Larme d'Exorcisme":
                    degat = round(self.modele.monstre_points_de_vie_max*0.15)
                    commentaire_item = ("Vous envoyez le liquide visqueux en direction du monstre.\nAux endroits ou les larmes"
                                        " entrent en contact avec L'ennemi, la peau prend une teinte magenta/pourpre."
                                        f"\nVous infligez {degat} points de degats a l'ennemi !")
                elif nom_de_litem == "Soluté d'Exorcisme":
                    degat = round(self.modele.monstre_points_de_vie_max*0.20)
                    commentaire_item = ("Vous envoyez le liquide visqueux en direction du monstre.\nAux endroits ou le soluté"
                                        " est en contact avec L'ennemi, la chair semble fondre"
                                        f"\nVous réduisez ses points de vie max de {degat} !")
                self.modele.monstre_points_de_vie -= degat
                self.modele.monstre_points_de_vie_max -= degat
            elif nom_de_litem in ["Mutagène Bleu", "Grand Mutagène Bleu"]:
                if nom_de_litem == "Mutagène Bleu":
                    commentaire_item = ("Vous buvez une sorte de potion gluante bleue."
                                        "\nBientot, vous sentez quelque chose changer en "
                                        "vous.\nVotre coeur bat bien plus lentement, mais "
                                        "vos sens sont en éveil.")
                    self.modele.mutagene_bleu_utilise = True
                    gain_mana = round(self.modele.points_de_mana_max*0.1)
                    perd_vie = round(self.modele.points_de_vie_max*0.1)
                elif nom_de_litem == "Grand Mutagène Bleu":
                    commentaire_item = ("Vous vous injectez un produit bleu ciel."
                                        "\nBientot, vous sentez quelque chose changer en "
                                        "vous.\nVotre coeur bat plus lentement, mais "
                                        "vos sens sont transcendés.")
                    self.modele.grand_mutagene_bleu_utilise = True
                    gain_mana = round(self.modele.points_de_mana_max*0.2)
                    perd_vie = round(self.modele.points_de_vie_max*0.05)
                self.modele.points_de_vie_max -= perd_vie
                self.modele.perd_vie_mutagene = perd_vie
                self.modele.points_de_mana_max += gain_mana
                self.RecouvrementDeMana(gain_mana)
                self.modele.gain_mana_mutagene = gain_mana
                self.EquilibragePointsDeVieEtManaEtEndurance()
                commentaire_item += f"\nVous gagnez {gain_mana} pm max et perdez {perd_vie} pv max pendant toute la durée du combat !"
            elif nom_de_litem in ["Mutagène Rouge", "Grand Mutagène Rouge"]:
                if nom_de_litem == "Mutagène Rouge":
                    commentaire_item = ("Vous buvez une sorte de potion gluante rouge."
                                        "\nBientot, vous sentez quelque chose changer en "
                                        "vous.\nVos sens se ferment au monde qui vous entoure, mais "
                                        "votre coeur bat plus vite.")
                    self.modele.mutagene_rouge_utilise = True
                    perd_mana = round(self.modele.points_de_mana_max*0.1)
                    gain_vie = round(self.modele.points_de_vie_max*0.1)
                elif nom_de_litem == "Grand Mutagène Rouge":
                    commentaire_item = ("Vous vous injectez un produit pourpre."
                                        "\nBientot, vous sentez quelque chose changer en "
                                        "vous.\nVos sens s'émoussent, mais "
                                        "votre coeur bat bien plus vite.")
                    self.modele.grand_mutagene_rouge_utilise = True
                    perd_mana = round(self.modele.points_de_mana_max*0.05)
                    gain_vie = round(self.modele.points_de_vie_max*0.2)
                self.modele.points_de_vie_max += gain_vie
                self.modele.points_de_vie += gain_vie
                self.modele.gain_vie_mutagene = gain_vie
                self.modele.points_de_mana_max -= perd_mana
                self.modele.perd_mana_mutagene = perd_mana
                self.EquilibragePointsDeVieEtManaEtEndurance()
                commentaire_item += f"\nVous perdez {perd_mana} pm max et gagnez {gain_vie} pv max pendant toute la durée du combat !"
            elif nom_de_litem in ["Mutagène Vert", "Grand Mutagène Vert"]:
                if nom_de_litem == "Mutagène Vert":
                    commentaire_item = ("Vous buvez une sorte de potion gluante vert clair."
                                        "\nBientot, vous sentez quelque chose changer en "
                                        "vous.\nVous ressentez bien mieux vos membres et"
                                        " avez un plus grand controle sur eux.")
                    gain_critique = 10
                    self.modele.mutagene_vert_utilise = True
                elif nom_de_litem == "Grand Mutagène Vert":
                    commentaire_item = ("Vous vous injectez un produit vert sapin."
                                        "\nBientot, vous sentez quelque chose changer en "
                                        "vous.\nVous avez un controle total de vos membres.")
                    self.modele.grand_mutagene_vert_utilise = True
                    gain_critique = 15
                commentaire_item += f"\nVous gagnez {gain_critique} pourcent de faire un coup critique pendant toute la durée du combat !"
            elif nom_de_litem in ["Mutagène Doré", "Grand Mutagène Doré"]:
                if nom_de_litem == "Mutagène Doré":
                    commentaire_item = ("Vous buvez une sorte de potion gluante dorée."
                                        "\nBientot, vous sentez quelque chose changer en "
                                        "vous.\nVotre coeur, vos sens et le controle de votre corps s'améliore.")
                    self.modele.mutagene_dore_utilise = True
                    gain_mana = round(self.modele.points_de_mana_max*0.1)
                    gain_vie = round(self.modele.points_de_vie_max*0.1)
                    gain_critique = 10
                elif nom_de_litem == "Grand Mutagène Doré":
                    commentaire_item = ("Vous vous injectez un produit de couleur miel nacré."
                                        "\nBientot, vous sentez quelque chose changer en "
                                        "vous.\nVotre coeur, vos sens et le controle de votre corps est incomparable.")
                    self.modele.grand_mutagene_dore_utilise = True
                    gain_mana = round(self.modele.points_de_mana_max*0.2)
                    self.modele.gain_mana_mutagene = gain_mana
                    gain_vie = round(self.modele.points_de_vie_max*0.2)
                    self.modele.gain_mana_mutagene = gain_vie
                    gain_critique = 20
                self.modele.points_de_vie_max += gain_vie
                self.modele.points_de_vie += gain_vie
                self.modele.points_de_mana_max += gain_mana
                self.RecouvrementDeMana(gain_mana)
                self.EquilibragePointsDeVieEtManaEtEndurance()
                commentaire_item += f"\nVous gagnez {gain_mana} pm max, {gain_critique} pourcent de faire un coup critique et {gain_vie} pv max pendant toute la durée du combat !"
            elif nom_de_litem in ["Mutagène Hérétique", "Mutagène Fanatique"]:
                if nom_de_litem == "Mutagène Hérétique":
                    commentaire_item = ("Vous vous injectez une substance ressemblant à du sang coagulé."
                                        "\nBientot, vous sentez quelque chose changer en "
                                        "vous.\nVotre coeur se met a battre a une vitesse affolante, "
                                        "et vos membres se mettent a trembler de manière incontrolable .")
                    self.modele.mutagene_heretique_utilise = True
                    gain_vie = round(self.modele.points_de_vie_max*0.5)
                    self.modele.points_de_vie_max += gain_vie
                    self.modele.points_de_vie += gain_vie
                    self.modele.gain_vie_mutagene = gain_vie
                    self.EquilibragePointsDeVieEtManaEtEndurance()
                    commentaire_item += f"\nVous gagnez {gain_vie} points de vie max pendant toute la durée du combat, mais ne pouvez plus faire de coups critiques !"
                elif nom_de_litem == "Mutagène Fanatique":
                    commentaire_item = ("Vous vous injectez une substance ressemblant à un oeuf bleu en décomposition."
                                        "\nBientot, vous sentez quelque chose changer en "
                                        "vous.\nVous vous mettez a ressentir l'entiereté de votre environnement"
                                        " a travers quelque chose qui ne peut etre décrit que comme un septieme sens, "
                                        "et vos membres se mettent a trembler de manière incontrolable .")
                    self.modele.mutagene_fanatique_utilise = True
                    gain_mana = round(self.modele.points_de_vie_max*0.5)
                    self.modele.points_de_mana_max += gain_mana
                    self.RecouvrementDeMana(gain_mana)
                    self.modele.gain_mana_mutagene = gain_mana
                    self.EquilibragePointsDeVieEtManaEtEndurance()
                    commentaire_item += f"\nVous gagnez {gain_mana} points de mana max pendant toute la durée du combat, mais ne pouvez plus faire de coups critiques !"
            self.vue.AfficheUtilisationItem(commentaire, commentaire_item, self.sound_of_action)
            self.modele.type_de_derniere_action_utilisee = "Items"
            self.modele.derniere_action_utilisee = nom_de_litem
        else:
            self.vue.AfficheActionImpossible(raison_si_action_pas_possible)

    def CheckSiItemPossible(self, nom_de_litem):
        raison_pour_pas_utiliser_item = ""
        utiliser_item_est_possible = True
        if self.modele.est_maudit_par_les_items == True:
            raison_pour_pas_utiliser_item = (f"Vous sortez [{nom_de_litem}] de votre sacoche, mais vous n'arrivez pas a"
                                             " vous souvenir comment utiliser l'objet avec votre esprit confus, alors vous"
                                             " le reposez dans votre sacoche.")
        if (nom_de_litem in self.modele.items_autorises_que_au_premier_tour) and self.modele.nombre_de_tours != 1:
            raison_pour_pas_utiliser_item = f"Pour une raison qui vous échappe, vous n'arrivez pas a utiliser [{nom_de_litem}] après le premier tour."
        if self.modele.items[nom_de_litem] == 0:
            raison_pour_pas_utiliser_item = f"Vous cherchez [{nom_de_litem}] dans votre sacoche, mais n'en trouvez plus."
        if self.modele.stigma_joueur_negatif == "Agent d'Entretien":
            raison_pour_pas_utiliser_item = ("Vous aurez le temps de jeter l'emballage de l'item quelque part ?"
                                             "\nEn plein combat ?"
                                             "\n \nNon?\n \n"
                                             "Et est-ce-que les poubelles sont magiques et viendront récuperer vos dechets ?"
                                             "\nToujours pas ?"
                                             "\nAlors rangez moi ça tout de suite !"
                                             "\nVous êtes la pour nettoyer le collisée, pas pour le rendre plus sale !")
        if raison_pour_pas_utiliser_item == "":
            return utiliser_item_est_possible, raison_pour_pas_utiliser_item
        else:
            utiliser_item_est_possible = False
            return utiliser_item_est_possible, raison_pour_pas_utiliser_item

    def Battle(self):
        # set si le mana vous beni ou maudit, si trop d'affinités
        self.SetBenedictionDuMana()
        # set les caracteristiques du monstres
        self.MonsterMaker()
        # set les variables pour les sables du temps
        self.SetupTimeSands()
        # set le design pattern constant avec les ajouts grace aux talents, pour le premiertourjoueur
        self.PatternDesignConstantUpdater()
        # affiche L'ennemi et son niveau, lance la musique
        self.AfficheMonstreNiveauEtMusique()
        # effectue les actions de premier tour du joueur
        self.PremierTourJoueur()
        # effectue les actions de premier tour du monstre
        self.PremierTourMonstre()
        # lance la boucle de combat
        while self.modele.InCombat:
            # set le design pattern constant avec les ajouts grace aux talents
            self.PatternDesignConstantUpdater()
            if not self.CheckHp():
                break
            if not self.modele.passe_son_tour:
                # prend le choix de l'utilisateur
                numero_du_type_de_laction, numero_de_laction = self.GetUserChoice(
                    self.modele.derniere_action_utilisee,
                    self.modele.type_de_derniere_action_utilisee,
                )
                clear_console()
                # traduit le choix en chaine de caractere lisible
                type_de_laction, nom_de_laction = self.TranslateUserChoice(
                    numero_du_type_de_laction, numero_de_laction
                )
                # Effectue les differentes actions joueur
                if type_de_laction == "Sorts":
                    self.UseMagic(nom_de_laction)
                elif type_de_laction == "Techniques":
                    self.UseAttack(nom_de_laction)
                elif type_de_laction == "Items":
                    self.UseItem(nom_de_laction)
                elif type_de_laction == "Fuir":
                    self.modele.InCombat = self.FailFleeing()
                elif type_de_laction == "Passer son tour":
                    self.PasserSonTour()
                elif type_de_laction == "Se défendre":
                    self.SeDefendre()
            else:
                # affiche la raison pour laquelle le joueur a passé son tour
                self.RaisonDePasserSonTour()
            # checke si les pv du joueur/monstre sont a zéro
            if not self.CheckHp():
                break
            type_de_laction_du_monstre = "None"
            if not self.modele.monstre_passe_son_tour:
                # genere une commande aleatoire pour L'ennemi
                nom_de_laction_du_monstre, type_de_laction_du_monstre = (
                    self.GetMonsterChoice()
                )
                # Effectue les differentes actions monstre
                self.modele.type_daction_du_monstre = type_de_laction_du_monstre
                if type_de_laction_du_monstre == "Sort":
                    self.UseMonsterMagic(nom_de_laction_du_monstre)
                elif type_de_laction_du_monstre == "Technique":
                    self.UseMonsterAttack(nom_de_laction_du_monstre)
            else:
                # affiche la raison pour laquelle L'ennemi a passé son tour
                self.RaisonDePasserTourMonstre()
            # checke si les pv du joueur/monstre sont a zéro
            if not self.CheckHp(type_de_laction_du_monstre):
                break
            # gere les alterations d'état et compte les tours
            self.FinTour()
        # check/gere le gameover
        self.CheckForGameOver()
        # gere la victoire ou fuite
        self.MontreFuiteOuRecompense()

    def CheckMonsterTypeOfAction(self, action):
        if (
            action in self.modele.sorts_de_feu_de_monstre
            or action in self.modele.techniques_de_feu_de_monstre
        ):
            self.modele.monstre_a_utilise_feu_ce_tour = True
        if (
            action in self.modele.sorts_de_foudre_de_monstre
            or action in self.modele.techniques_de_foudre_de_monstre
        ):
            self.modele.monstre_a_utilise_foudre_ce_tour = True
        if (
            action in self.modele.sorts_de_glace_de_monstre
            or action in self.modele.techniques_de_glace_de_monstre
        ):
            self.modele.monstre_a_utilise_glace_ce_tour = True
        if (
            action in self.modele.sorts_de_physique_de_monstre
            or action in self.modele.techniques_de_physique_de_monstre
        ):
            self.modele.monstre_a_utilise_physique_ce_tour = True
        if (
            action in self.modele.sorts_de_sang_de_monstre
            or action in self.modele.techniques_de_sang_de_monstre
        ):
            self.modele.monstre_a_utilise_sang_ce_tour = True
        if (
            action in self.modele.sorts_de_terre_de_monstre
            or action in self.modele.techniques_de_terre_de_monstre
        ):
            self.modele.monstre_a_utilise_terre_ce_tour = True
        if (
            action in self.modele.techniques_de_blessure_de_monstre
            or action in self.modele.sorts_de_blessure_de_monstre
        ):
            self.modele.monstre_a_utilise_blesse_ce_tour = True
        if (
            action in self.modele.techniques_de_deconcentration_de_monstre
            or action in self.modele.sorts_de_deconcentration_de_monstre
        ):
            self.modele.monstre_a_utilise_deconcentre_ce_tour = True
        if (
            action in self.modele.techniques_de_gold_de_monstre
            or action in self.modele.sorts_de_gold_de_monstre
        ):
            self.modele.monstre_a_utilise_gold_ce_tour = True
        if (
            action in self.modele.techniques_de_instable_de_monstre
            or action in self.modele.sorts_de_instable_de_monstre
        ):
            self.modele.monstre_a_utilise_instable_ce_tour = True
        if (
            action in self.modele.techniques_de_muet_de_monstre
            or action in self.modele.sorts_de_muet_de_monstre
        ):
            self.modele.monstre_a_utilise_muet_ce_tour = True
        if (
            action in self.modele.techniques_de_confusion_de_monstre
            or action in self.modele.sorts_de_confusion_de_monstre
        ):
            self.modele.monstre_a_utilise_confus_ce_tour = True

    def RemiseAZeroMonsterTypeOfAction(self):
        self.modele.monstre_a_utilise_feu_ce_tour = False
        self.modele.monstre_a_utilise_foudre_ce_tour = False
        self.modele.monstre_a_utilise_glace_ce_tour = False
        self.modele.monstre_a_utilise_physique_ce_tour = False
        self.modele.monstre_a_utilise_sang_ce_tour = False
        self.modele.monstre_a_utilise_terre_ce_tour = False
        self.modele.monstre_a_utilise_blesse_ce_tour = False
        self.modele.monstre_a_utilise_deconcentre_ce_tour = False
        self.modele.monstre_a_utilise_gold_ce_tour = False
        self.modele.monstre_a_utilise_instable_ce_tour = False
        self.modele.monstre_a_utilise_muet_ce_tour = False
        self.modele.monstre_a_utilise_confus_ce_tour = False

    def CheckePuisAppliqueTransmutation(self, degat):
        #priorité des actions déterminées par portée. 
        #Impact sur joueur < Attaque par joueur < mirroir devant joueur < brume tout autour de joueur
        if self.modele.utilise_brume_sang:
            #annule les degats
            self.modele.points_de_vie += degat
            #soigne a la hauteur des dégats subis
            self.modele.points_de_vie += degat
            #construit le message de transmutation
            self.modele.commentaire_transmutation_degat += (
                "Mais la brume de sang absorbe les dégâts.\nUne fine pluie"
                " se met a tomber sur vous et est absorbée par"
                f" votre peau.\nVous regagnez {degat} points de vie !"
            )
        elif self.modele.utilise_mirroir_eau:
            degat = self.SiZeroRameneAUn(degat)
            #annule les degats
            self.modele.points_de_vie += degat
            #applique les degat a l'ennemi
            self.modele.monstre_points_de_vie -= degat
            #construit le message de transmutation
            self.modele.commentaire_transmutation_degat += (
                "Mais le mirroir d'eau absorbe les dégâts.\nUne réplique de"
                " l'attaque faite d'eau sort du mirroir et inflige"
                f" {degat} points de dégâts a l'ennemi !"
            )
        elif self.modele.utilise_le_bluff:
            degat = self.SiZeroRameneAUn(degat)
            #annule les degats
            self.modele.points_de_vie += degat
            #applique les degat a l'ennemi
            self.modele.monstre_points_de_vie -= round(degat * 1.5)
            #construit le message de transmutation
            self.modele.commentaire_transmutation_degat += (
                "Mais vous esquivez l'attaque de l'ennemi au tout dernier des moments."
                "\nVos sens en alerte maximale vous font alors voir le monde au "
                "ralenti, et vos muscles ultra tendus prêt a l'action vous permettent de"
                " déchainer sur l'ennemi une rafale de coups titanesques "
                "avant qu'il n'aie le temps de réagir !\n"
                f"Vous lui infligez {degat} points de dégâts !"
            )
        elif self.modele.utilise_le_massif and (degat>round(self.modele.points_de_vie_max*0.05)):
            #annule les degats
            self.modele.points_de_vie += degat
            #remet les degats a la hauteur de 5% de vie max
            degat = round(self.modele.points_de_vie_max*0.05)
            degat = self.EnleveVieAuJoueur(degat)
            #construit le message de transmutation
            self.modele.commentaire_transmutation_degat += (
                "Mais l'impact de l'attaque se répartit dans votre corps,"
                " puis est dispersé dans le sol grace a votre posture"
                " ancrée a la terre et solide comme une chaine de"
                " montagne.\nDes dégâts que l'on vous a infligés,"
                f" vous ne perdez réellement que {degat} points de vie."
            )
        
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
                clear_console()
            except ValueError:
                clear_console()
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

    def AppliqueDegatsBonusDuMonstreContreLeJoueur(self, degat):
        if self.modele.type_daction_du_monstre == "Sort":
            degat += round(
            (self.modele.DEGATSORTBONUSDUMONSTRE / 100) * degat
        )
        else:
            degat += round(
                (self.modele.DEGATTECHNIQUEBONUSDUMONSTRE / 100) * degat
            )
        degat -= round(
            (self.modele.BONUSREDUCTIONDEGATSURJOUEUR / 100) * degat
        )
        return degat
    
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
        clear_console()
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
                        clear_console()
                        break
                    clear_console()
                except ValueError:
                    clear_console()
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
        clear_console()
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
                        clear_console()
                        break
                    clear_console()
                except ValueError:
                    clear_console()
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
                        clear_console()
                        break
                    clear_console()
                except ValueError:
                    clear_console()
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
                clear_console()
                if choix in [1, 2, 3, 4]:
                    break
            except ValueError:
                clear_console()
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

    def TousItemsVides(self):
        for val in self.modele.items.values():
            if val != 0:
                return False  
        return True  

    def ListeItemsVides(self):
        liste_vides = []
        for cle, val in self.modele.items.items():
            if val == 0:
                liste_vides.append(cle) 
        return liste_vides

    def ListeItemsPossedes(self):
        liste_possedes = []
        for cle, val in self.modele.items.items():
            if val > 0:
                liste_possedes.append(cle) 
        return liste_possedes

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
        if not reussite:
            return False
        else:
            if notes_restante > 0:
                self.modele.points_de_vie -= notes_restante * 15
                self.AfficheSonTechnique("SOUL")
                print(f"Les {notes_restante} notes restantes dans les airs vous tombent dessus et vous transpercent de toute part !\nVous perdez {notes_restante * 15} points de vie !")
                dummies = input("Appuyez sur entree pour continuer")

            if self.modele.points_de_vie <= 0 :
                
                if self.modele.possede_une_fee == True :
                    self.modele.possede_une_fee = False
                    self.modele.points_de_vie = round(0.66 * self.modele.points_de_vie_max)
                    print(f"Votre Fée sort de son bocal et vous sauve la vie en soignant {round(0.66 * self.modele.points_de_vie_max)} points de vie !")
                    dummies = input("Appuyez sur entree pour continuer")
                    
                elif "Voile de Ino" in self.modele.liste_dartefacts_optionels:
                    self.modele.liste_dartefacts_optionels.remove("Voile de Ino")
                    self.modele.points_de_vie = round(0.66 * self.modele.points_de_vie_max)
                    print(f"Votre Voile se plaque sur votre visage et vous sauve la vie en soignant {round(0.66 * self.modele.points_de_vie_max)} points de vie !")
                    dummies = input("Appuyez sur entree pour continuer")

                else:
                    print("Vous mourrez.")
                    dummies = input("Appuyez sur entree pour continuer")
                    return False
                
            print("Il n'y a plus de notes dans les airs.\nVous êtes en vie !\nFinissez le boss !")
            dummies = input("Appuyez sur entree pour continuer")
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
                match direction:
                    case "Haut":
                        affichage += "\nLe Pianiste lève les Bras en Haut !"
                    case "Bas":
                        affichage += "\nLe Pianiste baisse les Bras vers le Bas !"
                    case "Gauche":
                        affichage += "\nLe Pianiste déplace ses doigts vers la Gauche !"
                    case "Droite":
                        affichage += "\nLe Pianiste déplace ses doigts vers la Droite !"
                buffer.append(direction)
            else:
                # Phase finale : pas de nouvelle direction, juste le buffer
                affichage += "\n..."
            
            if len(buffer) < 3:
                # Pas encore assez d'historique → juste ENTER
                print(affichage)
                input("Appuyez sur Entrée pour continuer")
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
                        clear_console()
                        if choix in mapping.values():
                            break
                        else:
                            print("Choix invalide. Réessayez.")
                    except ValueError:
                        clear_console()
                
                if choix == mapping[ancienne_direction]:
                    print("Vous esquivez la vague de notes !")
                else:
                    print(f"Les notes vous transpercent et infligent 15 points de dégâts.\n"
                        f"Il aurait fallu aller vers [{ancienne_direction}].")
                    self.modele.points_de_vie -= 15
                    self.AfficheSonTechnique("ICEt")
            
            remaining_directions = total_iterations - (i + 1)
    


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
            dir_path = os.path.dirname(os.path.realpath(__file__))
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

    def UseMonsterMagic(self, action):
        # [0]=%touche, [1]=degat, [2]=%crit, [3]=degat crit, [4]=%element,
        # [5]=description, [6]=message si rate, [7]=si touche, [8]=si touche crit
        # [9]=nombre tours, [10]=effet element,[11]=cout mana
        assez_de_mana = self.RegardeSiMonstreAAssezDeMana(action)
        if assez_de_mana:
            if action in self.modele.annuaire_de_caracteristique_des_sorts_generaux_de_monstre:
                caracteristique_du_sort = self.modele.annuaire_de_caracteristique_des_sorts_generaux_de_monstre[
                    action
                ]
                # regarde l'élément de l'action pour les bonus associés
                self.CheckMonsterTypeOfAction(action)
                # application des modificateurs sur la chance de toucher
                pourcentage_de_touche = caracteristique_du_sort[0]
                pourcentage_de_touche -= self.modele.CHANCEBONUSESQUIVE
                # application des modificateurs sur les degats de base
                degat_de_base = caracteristique_du_sort[1]
                degat_de_base = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat_de_base)
                # application des modificateurs sur les chances de coup critique
                pourcentage_de_critique = caracteristique_du_sort[2]
                pourcentage_de_critique += round((self.modele.CHANCESORTCRITIQUEDUMONSTRE/100)*pourcentage_de_critique)
                # application des modificateurs sur les degats de coup critique
                degat_critique = caracteristique_du_sort[3]
                # application des modificateurs sur les chances d'appliquer un element
                pourcentage_de_element = caracteristique_du_sort[4]
                if self.modele.monstre_a_utilise_feu_ce_tour:
                    pourcentage_de_element += round((self.modele.CHANCEBONUSJOUEURENFEU / 100) * pourcentage_de_element)
                elif self.modele.monstre_a_utilise_foudre_ce_tour:
                    pourcentage_de_element += round((self.modele.CHANCEBONUSJOUEURPARALYSE / 100) * pourcentage_de_element)
                elif self.modele.monstre_a_utilise_terre_ce_tour:
                    pourcentage_de_element += round((self.modele.CHANCEBONUSJOUEURLAPIDE / 100) * pourcentage_de_element)
                elif self.modele.monstre_a_utilise_sang_ce_tour:
                    pourcentage_de_element += round((self.modele.CHANCEBONUSJOUEURENSANG / 100) * pourcentage_de_element)
                elif self.modele.monstre_a_utilise_glace_ce_tour:
                    pourcentage_de_element += round((self.modele.CHANCEBONUSJOUEURENGLACE / 100) * pourcentage_de_element)
                description = caracteristique_du_sort[5]
                nombre_aleatoire = random.randint(0, 100)
                degat = 0
                # ca touche ?
                if nombre_aleatoire < pourcentage_de_touche:
                    commentaire_element = ""
                    commentaire_a_afficher = caracteristique_du_sort[7]
                    degat += degat_de_base
                    # ca fait un critique ?
                    if nombre_aleatoire < pourcentage_de_critique:
                        commentaire_a_afficher = caracteristique_du_sort[8]
                        degat += degat_critique
                    # ca declenche  un effet elementaire ?
                    if nombre_aleatoire < pourcentage_de_element:
                        # si oui, quel effet ?
                        if self.modele.monstre_a_utilise_feu_ce_tour:
                            # deja en feu ?
                            if self.modele.est_en_feu:
                                nombre_aleatoire = random.randint(1, 100)
                                if nombre_aleatoire <= 90:
                                    # addition des tours
                                    nombre_tour = caracteristique_du_sort[9]
                                    
                                    # ajustement des degats
                                    degat_du_feu = caracteristique_du_sort[10]
                                    if (
                                        self.modele.est_en_feu_degat
                                        < degat_du_feu
                                    ):
                                        degat_du_feu = self.modele.est_en_feu_degat
                                    self.AppliqueEffetElementaireSurJoueur("feu", nombre_tour, degat_du_feu)
                                    commentaire_element = f"\nVous vous enflammez pour {nombre_tour} tours supplémentaires !"
                                else:
                                    # finition des degats
                                    pourcentage_degat_du_feu = (
                                        self.modele.est_en_feu_nombre_tour
                                        * (
                                            self.modele.est_en_feu_degat
                                        )
                                    )
                                    degat_du_feu = round(
                                        pourcentage_degat_du_feu
                                        * self.modele.points_de_vie_max
                                    )
                                    degat_du_feu = self.EnleveVieAuJoueur(degat_du_feu)
                                    # arret du feu
                                    self.modele.est_en_feu_nombre_tour = 0
                                    self.modele.est_en_feu_degat = 0
                                    self.modele.est_en_feu = False
                                    # paralysie
                                    nombre_tour = 2
                                    self.AppliqueEffetElementaireSurJoueur("foudre", nombre_tour)
                                    if self.modele.est_paralyse:
                                        # construction du comentaire_element
                                        commentaire_element = ("\nL'attaque vous enflamme.\nCepandant, les"
                                                            " deux feux s'éteignent mutuellement en"
                                                            " consommant l'oxygène disponible, et vous "
                                                            "font de gros dégâts.\nDe plus, le choc vous "
                                                            "paralyse !")
                                    else:
                                        # construction du comentaire_element
                                        commentaire_element = ("\nL'attaque vous enflamme.\nCepandant, les"
                                                            " deux feux s'éteignent mutuellement en"
                                                            " consommant l'oxygène disponible, et vous "
                                                            "font de gros dégâts.")
                            else:
                                # mise a feu du joueur
                                nombre_tour = caracteristique_du_sort[9]
                                self.AppliqueEffetElementaireSurJoueur("feu", nombre_tour, caracteristique_du_sort[10])
                                commentaire_element = f"\nVous vous enflammez pendant {nombre_tour} tours !"
                        elif self.modele.monstre_a_utilise_foudre_ce_tour:
                            nombre_tour_para = caracteristique_du_sort[9]
                            self.AppliqueEffetElementaireSurJoueur("foudre", nombre_tour_para)
                            if self.modele.est_paralyse:
                                commentaire_element = f"\nL'ennemi vous paralyse pendant {nombre_tour_para+self.modele.TOURBONUSJOUEURENPARALYSIE} tours !"
                            else:
                                commentaire_element = f"\nVous résistez a la paralysie déclenchée par l'ennemi !"
                        elif self.modele.monstre_a_utilise_glace_ce_tour:
                            nombre_tour_gele = caracteristique_du_sort[9]
                            self.AppliqueEffetElementaireSurJoueur("glace", nombre_tour_gele)
                            commentaire_element = f"\nL'ennemi vous gèle pendant {nombre_tour_gele + self.modele.TOURBONUSJOUEURENGLACE} tours !"
                        elif self.modele.monstre_a_utilise_sang_ce_tour:
                            # calcul de la saignee
                            pourcentage_saignee = caracteristique_du_sort[10]
                            degat_saignee = round(
                                (pourcentage_saignee / 100)
                                * self.modele.points_de_vie_max
                            )
                            # application de la saignee
                            degat_saignee = self.EnleveVieAuJoueur(degat_saignee)
                            soin_saignee = degat_saignee
                            self.modele.monstre_points_de_vie += soin_saignee
                            self.EquilibragePointsDeVieEtManaEtEndurance()
                            commentaire_element = f"\nL'ennemi vous draine {degat_saignee} points de vie , et en récupere {soin_saignee} !"
                        elif self.modele.monstre_a_utilise_terre_ce_tour:
                            # calcul de lapidation
                            pourcentage_lapidation = caracteristique_du_sort[10]
                            degat_lapidation = round(
                                (pourcentage_lapidation / 100) * degat
                            )
                            # application lapidation
                            degat_lapidation = self.EnleveVieAuJoueur(degat_lapidation)
                            # construction du comentaire_element
                            commentaire_element = f"\nL'ennemi vous inflige {degat_lapidation} points de dégâts supplémentaire par lapidation !"
                    degat = self.EnleveVieAuJoueur(degat)
                    commentaire_degat = (
                        f"L'ennemi vous inflige {degat} points de dégât !"
                    )
                    commentaire_degat += commentaire_element
                    self.CheckePuisAppliqueTransmutation(degat)
                else:
                    commentaire_a_afficher = caracteristique_du_sort[6]
                    commentaire_degat = "L'ennemi ne vous inflige aucun dégât."
                self.vue.AfficheSortOuAttaque(
                    description, commentaire_a_afficher, commentaire_degat
                )
            else:
                # attaques avec d'autres effets que ceux de la méthode globale
                #soin
                if action in self.modele.sorts_de_soin_de_monstre:
                    caracteristique_du_sort = self.modele.annuaire_de_caracteristique_des_sorts_speciaux_de_monstre[action]
                    #intialisation des caracteristiques
                    soin_minimum = caracteristique_du_sort[0]
                    pourcentage_de_soin = caracteristique_du_sort[1]
                    description = caracteristique_du_sort[2]
                    commentaire_a_afficher = caracteristique_du_sort[3]
                    #appliquer soin
                    soin_applique = round(self.modele.monstre_points_de_vie_max * (pourcentage_de_soin / 100))
                    if soin_applique < soin_minimum:
                        soin_applique = soin_minimum
                    self.modele.monstre_points_de_vie += soin_applique
                    self.EquilibragePointsDeVieEtManaEtEndurance
                    #construire message a afficher
                    commentaire_degat = f"L'ennemi récupère {soin_applique} points de vie !"
                    #afficher resultat
                    self.vue.AfficheSortOuAttaque(
                    description, commentaire_a_afficher, commentaire_degat
                    )
                #alteration d'état
                elif ((action in self.modele.sorts_de_blessure_de_monstre) or
                    (action in self.modele.sorts_de_deconcentration_de_monstre) or
                    (action in self.modele.sorts_de_gold_de_monstre) or
                    (action in self.modele.sorts_de_instable_de_monstre) or
                    (action in self.modele.sorts_de_muet_de_monstre) or
                    (action in self.modele.sorts_de_confusion_de_monstre)):
                    caracteristique_du_sort = self.modele.annuaire_de_caracteristique_des_sorts_speciaux_de_monstre[action]
                    #construction message a afficher
                    description = caracteristique_du_sort[2]
                    #intialisation du pourcentage de touche
                    pourcentage_de_touche = caracteristique_du_sort[0]
                    pourcentage_de_touche -= self.modele.CHANCEBONUSESQUIVE
                    #ca touche ?
                    nombre_aleatoire = random.randint(0, 100)
                    if nombre_aleatoire < pourcentage_de_touche:
                        #touche
                        #construction du message
                        commentaire_a_afficher = caracteristique_du_sort[4]
                        #application de l'effet
                        nombre_tour = caracteristique_du_sort[1]
                        if action in self.modele.sorts_de_blessure_de_monstre:
                            self.modele.est_maudit_par_la_vie = True
                            self.modele.est_maudit_par_la_vie_nombre_tour = nombre_tour
                            commentaire_degat = f"Vous voilà Blessé pendant {nombre_tour} tours !"
                        elif action in self.modele.sorts_de_deconcentration_de_monstre:
                            self.modele.est_maudit_par_le_mana = True
                            self.modele.est_maudit_par_le_mana_nombre_tour = nombre_tour
                            commentaire_degat = f"Vous voilà Déconcentré pendant {nombre_tour} tours !"
                        elif action in self.modele.sorts_de_gold_de_monstre:
                            self.modele.est_maudit_par_le_gold = True
                            self.modele.est_maudit_par_le_gold_nombre_tour = nombre_tour
                            commentaire_degat = f"Vous voilà victime du Mal Jaune pendant {nombre_tour} tours !"
                        elif action in self.modele.sorts_de_instable_de_monstre:
                            self.modele.est_maudit_par_les_techniques = True
                            self.modele.est_maudit_par_les_techniques_nombre_tour = nombre_tour
                            commentaire_degat = f"Vous voilà Instable pendant {nombre_tour} tours !"
                        elif action in self.modele.sorts_de_muet_de_monstre:
                            self.modele.est_maudit_par_les_sorts = True
                            self.modele.est_maudit_par_les_sorts_nombre_tour = nombre_tour
                            commentaire_degat = f"Vous voilà Muet pendant {nombre_tour} tours !"
                        elif action in self.modele.sorts_de_confusion_de_monstre:
                            self.modele.est_maudit_par_les_items = True
                            self.modele.est_maudit_par_les_items_nombre_tour = nombre_tour
                            commentaire_degat = f"Vous voilà Confus pendant {nombre_tour} tours !"
                    else:
                        #touche pas
                        commentaire_a_afficher = caracteristique_du_sort[3]
                        commentaire_degat = "C'est pas passé loin !"
                    self.vue.AfficheSortOuAttaque(
                    description, commentaire_a_afficher, commentaire_degat
                    )
                # attaques qui ne rentrent pas dans la méthode globale (fait plus que juste des degat ou un element)
                elif action == "Tout Feu Tout Flamme":
                    self.ToutFeuToutFlamme()
                elif action == "Volepièce":
                    self.Volepiece()
                elif action == "Bandit Manchot":
                    self.BanditManchot()
                elif action == "Cat-astrophe":
                    self.Cat_astrophe()
                elif action == "Son Lent":
                    self.SonLent()
                elif action == "Vole-Ame":
                    self.Vole_Ame()
                elif action == "Rituel":
                    self.Rituel()
                elif action == "Tempêtes du Nord":
                    self.TempeteDuNord()
                elif action == "Tempêtes du Sud":
                    self.TempeteDuSud()
                elif action == "Tempêtes de l'Est":
                    self.TempeteDeEst()
                elif action == "Tempêtes de l'Ouest":
                    self.TempeteDeOuest()
                elif action == "Vacarme Rapide":
                    self.VacarmeRapide()
                elif action == "Vacarme Lent":
                    self.VacarmeLent()
                elif action == "Vide":
                    self.Vide()
                elif action == "Eveil de Runes":
                    self.EveilDeRunes()
                elif action == "Lamentations":
                    self.Lamentations()
                elif action == "Invoquation Canope":
                    self.InvoquationCanope()
                elif action == "Magie Noire":
                    self.MagieNoire()
                elif action == "Magie Ténébreuse":
                    self.MagieTenebreuse()
                elif action == "Tournicota":
                    self.Tournicota()
                elif action == "Tournicotons":
                    self.Tournicotons()
                elif action == "Tournicotez":
                    self.Tournicotez()
                elif action == "Tome de Salomon":
                    self.TomeDeSalomon()
                elif action == "Sort Ultime":
                    self.SortUltime()
                elif action == "Ultime Ultime":
                    self.UltimeUltime()
                elif action == "Ultima":
                    self.Ultima()
                elif action == "Dragon Ascendant":
                    self.DragonAscendant()
                elif action == "Magie Abyssale":
                    self.MagieAbyssale()
                elif action == "Jugement":
                    self.Jugement()
                elif action == "Systeme de Support":
                    self.SystemeSupport()
                elif action == "Protocole Supernova":
                    self.ProtocoleSupernova()
                elif action == "Flash Bang":
                    self.FlashBang()
                elif action == "Laser Anti-Personnel":
                    self.LaserAntipersonnel()
                elif action == "Symphonie":
                    self.Symphonie()
            #affiche si les degats ont été changés par bluff, montagne, brume de sang ou mirroir d'eau
            if self.modele.commentaire_transmutation_degat != "":
                self.vue.AfficheTransmutationDegat(self.modele.commentaire_transmutation_degat)
        else:
            self.MetMonstreEnEtatDeChoc(action)

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
            commentaire_degat += (f"Vous devenez gelé, enflammé et confu pendant 4 tours !")
            commentaire_degat += (f"De plus, vous perdez {degat_a_joueur} points de vie !")
            self.EnleveVieAuJoueur(degat_a_joueur)
        self.vue.AfficheSymphonie(commentaire, commentaire_degat)
    
    def Jugement(self):
        degat = self.modele.nombre_de_monstres_tues
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
        self.modele.utilise_brume_sang = False
        self.modele.brume_sang_nombre_tours = 0
        self.modele.utilise_mirroir_eau = False
        self.modele.mirroir_eau_nombre_tours = 0
        nombre_aleatoire = random.randint(0, 100)
        chance_de_toucher = 80
        chance_de_toucher -= self.modele.CHANCEBONUSESQUIVE
        if nombre_aleatoire < chance_de_toucher:
            degat = 15 + self.modele.monstre_level
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
                clear_console()
                if choix_mise in [1, 2, 3, 4]:
                    if ((choix_mise == 2 and self.modele.nombre_de_gold < 5) or
                        (choix_mise == 3 and self.modele.nombre_de_gold < 10) or
                        (choix_mise == 4 and self.modele.nombre_de_gold < 15)):
                        self.vue.AfficheMiseImpossibleRoulette()
                    else:
                        break
            except ValueError:
                clear_console()
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

    def SetupTimeSands(self):
        self.modele.vie_du_monstre_pour_sables_du_temps_actuel = self.modele.monstre_points_de_vie
        self.modele.vie_du_monstre_pour_sables_du_temps_tour_avant = self.modele.monstre_points_de_vie
        self.modele.vie_du_monstre_pour_sables_du_temps_a_utiliser = self.modele.monstre_points_de_vie

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
            if self.modele.monstre_est_en_feu:
                self.modele.monstre_est_vulnerable = False
                self.modele.monstre_est_vulnerable_nombre_tour = 0
                self.modele.monstre_niveau_de_vulnerabilite = 0
            if self.modele.monstre_est_en_feu:
                self.modele.monstre_est_empoisonne = False
                self.modele.monstre_est_empoisonne_nombre_tour = 0
                self.modele.monstre_est_empoisonne_degat = 0
        else:
            commentaire_effet = ("Les rouages du temps semblent s'arrêter un instant, puis reprennent leur course infinie.")
        self.vue.AfficheSablesDuTemps(commentaire, commentaire_effet)

    def UseMonsterAttack(self, action):
        # [0]=%touche, [1]=degat, [2]=%crit, [3]=degat crit, [4]=%element,
        # [5]=description, [6]=message si rate, [7]=si touche, [8]=si touche crit
        # [9]=nombre tours, [10]=effet element
        # regarde l'élément de l'action pour les bonus associés
        self.CheckMonsterTypeOfAction(action)
        # methode globale pour les attaques
        if action in self.modele.annuaire_de_caracteristique_des_techniques_generales_de_monstre:
            caracteristique_du_techniques = (
                self.modele.annuaire_de_caracteristique_des_techniques_generales_de_monstre[action]
            )
            # application des modificateurs sur la chance de toucher
            pourcentage_de_touche = caracteristique_du_techniques[0]
            pourcentage_de_touche -= self.modele.CHANCEBONUSESQUIVE
            # application des modificateurs sur les degats de base
            degat = 0
            degat_de_base = caracteristique_du_techniques[1]
            degat_de_base = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat_de_base)
            # application des modificateurs sur les chances de coup critique
            pourcentage_de_critique = caracteristique_du_techniques[2]
            pourcentage_de_critique += round((self.modele.CHANCECOUPCRITIQUEDUMONSTRE/100)*pourcentage_de_critique)
            # application des modificateurs sur les degats de coup critique
            degat_critique = caracteristique_du_techniques[3]
            # application des modificateurs sur les chances d'appliquer un element
            pourcentage_de_element = caracteristique_du_techniques[4]
            if self.modele.monstre_a_utilise_feu_ce_tour:
                pourcentage_de_element += round((self.modele.CHANCEBONUSJOUEURENFEU / 100) * pourcentage_de_element)
            elif self.modele.monstre_a_utilise_foudre_ce_tour:
                pourcentage_de_element += round((self.modele.CHANCEBONUSJOUEURPARALYSE / 100) * pourcentage_de_element)
            elif self.modele.monstre_a_utilise_terre_ce_tour:
                pourcentage_de_element += round((self.modele.CHANCEBONUSJOUEURLAPIDE / 100) * pourcentage_de_element)
            elif self.modele.monstre_a_utilise_sang_ce_tour:
                pourcentage_de_element += round((self.modele.CHANCEBONUSJOUEURENSANG / 100) * pourcentage_de_element)
            elif self.modele.monstre_a_utilise_glace_ce_tour:
                pourcentage_de_element += round((self.modele.CHANCEBONUSJOUEURENGLACE / 100) * pourcentage_de_element)
            description = caracteristique_du_techniques[5]
            nombre_aleatoire = random.randint(0, 100)
            if nombre_aleatoire < pourcentage_de_touche:
                commentaire_element = ""
                commentaire_a_afficher = caracteristique_du_techniques[7]
                degat += degat_de_base

                # ca fait un critique ?
                if nombre_aleatoire < pourcentage_de_critique:
                    commentaire_a_afficher = caracteristique_du_techniques[8]
                    degat += degat_critique
                # ca declenche  un effet elementaire ?
                if nombre_aleatoire < pourcentage_de_element:
                    # si oui, quel effet ?
                    if self.modele.monstre_a_utilise_feu_ce_tour:
                        # deja en feu ?
                        if self.modele.est_en_feu:
                            nombre_aleatoire = random.randint(1, 100)
                            if nombre_aleatoire <= 90:
                                # addition des tours
                                nombre_tour = caracteristique_du_techniques[9]
                                
                                # ajustement des degats
                                degat_du_feu = caracteristique_du_techniques[10]
                                if (
                                    self.modele.est_en_feu_degat
                                    < degat_du_feu
                                ):
                                    degat_du_feu = self.modele.est_en_feu_degat
                                self.AppliqueEffetElementaireSurJoueur("feu", nombre_tour, degat_du_feu)
                                commentaire_element = f"\nVous vous enflammez pour {nombre_tour} tours supplémentaires !"
                            else:
                                # finition des degats
                                pourcentage_degat_du_feu = (
                                    self.modele.est_en_feu_nombre_tour
                                    * (
                                        self.modele.est_en_feu_degat
                                    )
                                )
                                degat_du_feu = round(
                                    pourcentage_degat_du_feu
                                    * self.modele.points_de_vie_max
                                )
                                degat_du_feu = self.EnleveVieAuJoueur(degat_du_feu)
                                # arret du feu
                                self.modele.est_en_feu_nombre_tour = 0
                                self.modele.est_en_feu_degat = 0
                                self.modele.est_en_feu = False
                                # paralysie
                                nombre_tour = 2
                                self.AppliqueEffetElementaireSurJoueur("foudre", nombre_tour)
                                if self.modele.est_paralyse:
                                    # construction du comentaire_element
                                    commentaire_element = ("\nL'attaque vous enflamme.\nCepandant, les"
                                                        " deux feux s'éteignent mutuellement en"
                                                        " consommant l'oxygène disponible, et vous "
                                                        "font de gros dégâts.\nDe plus, le choc vous "
                                                        "paralyse !")
                                else:
                                    # construction du comentaire_element
                                    commentaire_element = ("\nL'attaque vous enflamme.\nCepandant, les"
                                                        " deux feux s'éteignent mutuellement en"
                                                        " consommant l'oxygène disponible, et vous "
                                                        "font de gros dégâts.")
                        else:
                            # mise a feu du joueur
                            nombre_tour = caracteristique_du_techniques[9]
                            
                            self.AppliqueEffetElementaireSurJoueur("feu", nombre_tour, caracteristique_du_techniques[10])
                            commentaire_element = f"\nVous vous enflammez pendant {nombre_tour} tours !"
                    elif self.modele.monstre_a_utilise_foudre_ce_tour:
                        nombre_tour_para = caracteristique_du_techniques[9]
                        self.AppliqueEffetElementaireSurJoueur("foudre", nombre_tour_para)
                        if self.modele.est_paralyse:
                            commentaire_element = f"\nL'ennemi vous paralyse pendant {nombre_tour_para + self.modele.TOURBONUSJOUEURENPARALYSIE} tours !"
                        else:
                            commentaire_element = f"\nVous résistez a la paralysie déclenchée par l'ennemi !"
                    elif self.modele.monstre_a_utilise_glace_ce_tour:
                        nombre_tour_gele = caracteristique_du_techniques[9]
                        self.AppliqueEffetElementaireSurJoueur("glace", nombre_tour_gele)
                        commentaire_element = f"\nL'ennemi vous gèle pendant {nombre_tour_gele + self.modele.TOURBONUSJOUEURENGLACE} tours !"
                    elif self.modele.monstre_a_utilise_sang_ce_tour:
                        # calcul de la saignee
                        pourcentage_saignee = caracteristique_du_techniques[10]
                        degat_saignee = round(
                            (pourcentage_saignee / 100)
                            * self.modele.points_de_vie_max
                        )
                        degat_saignee = self.AppliqueLimitationSaignee(degat_saignee)
                        # application de la saignee
                        degat_saignee = self.EnleveVieAuJoueur(degat_saignee)
                        soin_saignee = degat_saignee
                        self.modele.monstre_points_de_vie += soin_saignee
                        self.EquilibragePointsDeVieEtManaEtEndurance()
                        commentaire_element = f"\nL'ennemi vous draine {degat_saignee} points de vie , et en récupere {soin_saignee} !"
                    elif self.modele.a_utilise_terre_ce_tour:
                        # calcul de lapidation
                        pourcentage_lapidation = caracteristique_du_techniques[10]
                        degat_lapidation = round(
                            (pourcentage_lapidation / 100) * degat
                        )
                        # application lapidation
                        degat_lapidation = self.EnleveVieAuJoueur(degat_lapidation)
                        # construction du comentaire_element
                        commentaire_element = f"\nL'ennemi vous inflige {degat_lapidation} points de dégâts supplémentaire par lapidation !"
                degat = self.EnleveVieAuJoueur(degat)
                commentaire_degat = (
                    f"L'ennemi vous inflige {degat} points de dégât !"
                )
                commentaire_degat += commentaire_element
                self.CheckePuisAppliqueTransmutation(degat)
            else:
                commentaire_a_afficher = caracteristique_du_techniques[6]
                commentaire_degat = "L'ennemi ne vous inflige aucun dégât."
                if "Tiare de Suie" in self.modele.liste_dartefacts_optionels:
                    commentaire_a_afficher += "\nL'artefact [Tiare de Suie] bénit votre échappée !"
                    self.modele.beni_par_feu_sacre = True
                    self.modele.beni_par_feu_sacre_nombre_tour += 2
            self.vue.AfficheSortOuAttaque(
                description, commentaire_a_afficher, commentaire_degat
            )
        else:
            #soin
            if action in self.modele.techniques_de_soin_de_monstre:
                caracteristique_du_techniques = self.modele.annuaire_de_caracteristique_des_techniques_speciales_de_monstre[action]
                #intialisation des caracteristiques
                soin_minimum = caracteristique_du_techniques[0]
                taux_de_reussite = caracteristique_du_techniques[1]
                pourcentage_de_soin = caracteristique_du_techniques[2]
                description = caracteristique_du_techniques[3]
                nombre_aleatoire = random.randint(0, 100)
                if nombre_aleatoire <= taux_de_reussite:
                    commentaire_a_afficher = caracteristique_du_techniques[5]
                    #appliquer soin
                    soin_applique = round(self.modele.monstre_points_de_vie_max * (pourcentage_de_soin / 100))
                    if soin_applique < soin_minimum:
                        soin_applique = soin_minimum
                    self.modele.monstre_points_de_vie += soin_applique
                    self.EquilibragePointsDeVieEtManaEtEndurance
                    #construire message a afficher
                    commentaire_degat = f"L'ennemi récupère {soin_applique} points de vie !"
                else :
                    commentaire_a_afficher = caracteristique_du_techniques[4]
                    commentaire_degat = "L'ennemi ne récupère pas de points de vie ."
                #afficher resultat
                self.vue.AfficheSortOuAttaque(
                description, commentaire_a_afficher, commentaire_degat
                )
            #alteration d'état
            elif ((action in self.modele.techniques_de_blessure_de_monstre) or
                  (action in self.modele.techniques_de_deconcentration_de_monstre) or
                  (action in self.modele.techniques_de_gold_de_monstre) or
                  (action in self.modele.techniques_de_instable_de_monstre) or
                  (action in self.modele.techniques_de_muet_de_monstre) or
                  (action in self.modele.techniques_de_confusion_de_monstre)):
                caracteristique_du_techniques = self.modele.annuaire_de_caracteristique_des_techniques_speciales_de_monstre[action]
                #construction message a afficher
                description = caracteristique_du_techniques[3]
                #intialisation du pourcentage de touche
                pourcentage_de_touche = caracteristique_du_techniques[1]
                pourcentage_de_touche -= self.modele.CHANCEBONUSESQUIVE
                #ca touche ?
                nombre_aleatoire = random.randint(0, 100)
                if nombre_aleatoire < pourcentage_de_touche:
                    #touche
                    #construction du message
                    commentaire_a_afficher = caracteristique_du_techniques[5]
                    #appliquation des dégats:
                    degat = caracteristique_du_techniques[0]
                    degat = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat)
                    degat = self.EnleveVieAuJoueur(degat)
                    self.CheckePuisAppliqueTransmutation(degat)
                    commentaire_degat = f"Vous perdez {degat} points de vie !"
                    #application de l'effet
                    nombre_tour = caracteristique_du_techniques[2]
                    if action in self.modele.techniques_de_blessure_de_monstre:
                        self.modele.est_maudit_par_la_vie = True
                        self.modele.est_maudit_par_la_vie_nombre_tour = nombre_tour
                        commentaire_degat += f"\nMais en plus, vous voilà Blessé pendant {nombre_tour} tours !"
                    elif action in self.modele.techniques_de_deconcentration_de_monstre:
                        self.modele.est_maudit_par_le_mana = True
                        self.modele.est_maudit_par_le_mana_nombre_tour = nombre_tour
                        commentaire_degat += f"\nMais en plus, vous voilà Déconcentré pendant {nombre_tour} tours !"
                    elif action in self.modele.techniques_de_gold_de_monstre:
                        self.modele.est_maudit_par_le_gold = True
                        self.modele.est_maudit_par_le_gold_nombre_tour = nombre_tour
                        commentaire_degat += f"\nMais en plus, vous voilà victime du Mal Jaune pendant {nombre_tour} tours !"
                    elif action in self.modele.techniques_de_instable_de_monstre:
                        self.modele.est_maudit_par_les_techniques = True
                        self.modele.est_maudit_par_les_techniques_nombre_tour = nombre_tour
                        commentaire_degat += f"\nMais en plus, vous voilà Instable pendant {nombre_tour} tours !"
                    elif action in self.modele.techniques_de_muet_de_monstre:
                        self.modele.est_maudit_par_les_sorts = True
                        self.modele.est_maudit_par_les_sorts_nombre_tour = nombre_tour
                        commentaire_degat += f"\nMais en plus, vous voilà Muet pendant {nombre_tour} tours !"
                    elif action in self.modele.techniques_de_confusion_de_monstre:
                        self.modele.est_maudit_par_les_items = True
                        self.modele.est_maudit_par_les_items_nombre_tour = nombre_tour
                        commentaire_degat += f"\nMais en plus, vous voilà Confus pendant {nombre_tour} tours !"
                else:
                    #touche pas
                    commentaire_a_afficher = caracteristique_du_techniques[4]
                    commentaire_degat = "C'est pas passé loin !"
                self.vue.AfficheSortOuAttaque(
                description, commentaire_a_afficher, commentaire_degat
                )
            # attaques qui ne rentrent pas dans la méthode globale (fait plus que juste des degat ou un element)
            elif action == "Durcissement Argilite":
                self.DurcissementArgilite()
            elif action == "Envol":
                self.Envol()
            elif action == "Hurlement":
                self.Hurlement()
            elif action == "Attire-Gold":
                self.AttireGold()
            elif action == "Coup Anti-Magie":
                self.CoupAntiMagie()
            elif action == "Attire-Magie":
                self.AttireMagie()
            elif action == "Aspiration":
                self.Aspiration()
            elif action == "Laser":
                self.Laser()
            elif action == "Roulette":
                self.Roulette()
            elif action == "Jet d'Argent":
                self.JetDargent()
            elif action == "Gemme Bleue":
                self.GemmeBleue()
            elif action == "Durcissement Calcaire":
                self.DurcissementCalcaire()
            elif action == "Combo Misérable":
                self.ComboMiserable()
            elif action == "Crystal Elémentaire":
                self.CrystalElementaireDore()
            elif action == "Panacée Universelle":
                self.PanaceeUniverselle()
            elif action == "Sables du Temps":
                self.SablesDuTemps()
        #affiche si les degats ont été changés par bluff, montagne, brume de sang ou mirroir d'eau
        if self.modele.commentaire_transmutation_degat != "":
            self.vue.AfficheTransmutationDegat(self.modele.commentaire_transmutation_degat)

    def AppliqueTalentPyrophile(self):
        mana_regagne = round(self.modele.points_de_mana_max * 0.1)
        self.RecouvrementDeMana(mana_regagne)
        self.EquilibragePointsDeVieEtManaEtEndurance()
        commentaire = f"Le feu vous accueille comme un vieil ami et vous en tirez votre force.\nVous regagnez {mana_regagne} points de mana !"
        self.vue.AfficheTalentPyrophile(commentaire)
    
    def AppliqueTalentPyrosorcier(self):
        mana_regagne = round(self.modele.points_de_mana_max * 0.05)
        self.RecouvrementDeMana(mana_regagne)
        self.EquilibragePointsDeVieEtManaEtEndurance()
        commentaire = f"Vous tirez votre force de tout les feux, même de celui qui ravage votre ennemi.\nVous regagnez {mana_regagne} points de mana !"
        self.vue.AfficheTalentPyrosorcier(commentaire)

    def AppliqueTalentPyromage(self):
        # calcul des degats de feu inflige a l'ennemi
        bonus = round((self.modele.DEGATBONUSFEU / 100) * self.modele.monstre_est_en_feu_degat)
        degat = round(
            ((self.modele.monstre_est_en_feu_degat + bonus) / 100)
            * self.modele.monstre_points_de_vie_max
        )
        # calcul et application du soin
        vie_regagne = round(degat * 0.5)
        self.modele.points_de_vie += vie_regagne
        self.EquilibragePointsDeVieEtManaEtEndurance()
        commentaire = f"Les flammes sont sous votre commandement absolu, et vous ramène la vitalitée de celles et ceux qu'elles consumment.\nVous regagnez {vie_regagne} points de vie !"
        self.vue.AfficheTalentPyromage(commentaire)

    def AppliqueTalentAntiNeurotransmetteur(self):
        degat = self.modele.anti_neurotransmitteurs_degat + self.modele.monstre_level
        degat = self.SiZeroRameneAUn(degat)
        self.modele.monstre_points_de_vie -= degat
        commentaire = f"Les muscles paralysés se contractent au dela de la limite établie par le cerveau.\nL'ennemi perd {degat} points de vie !"
        self.vue.AfficheAntiNeurotransmetteur(commentaire)

    def AppliqueTalentLuciole(self):
        self.modele.luciole_etat = True
        self.modele.luciole_tour += 3
        commentaire = f"L'électricité contenue dans le corps de l'ennemi se prépare à sortir et provoque un feu électrique qui le brule pendant 2 tours !"
        self.vue.AfficheLuciole(commentaire)

    def AppliqueTalentEclatDeGlace(self):
        degat = self.modele.eclats_de_glace_degat + self.modele.monstre_level
        degat = self.SiZeroRameneAUn(degat)
        self.modele.monstre_points_de_vie -= degat
        commentaire = ("Alors que la glace sur l'ennemi commence à fondre, certains éclats"
                        " plus froids que les autres laissent des trous dans son corps."
                        f"\nIl perd {degat} points de vie !")
        self.vue.AfficheTalentEclatDeGlace(commentaire)

    def AppliqueTalentCycleGlaciaire(self):
        vie_reprise = round(self.modele.points_de_vie_max * 0.25)
        self.modele.points_de_vie += vie_reprise
        commentaire = ("\nLes glaces sont sous votre commandement absolu, et retiennent une partie de la vitalitée perdue par l'ennemi en la gelant."
                       "\nElles vous la ramène ensuite sous forme de soin, au dégel de l'ennemi."
                       f"\nVous reprenez {vie_reprise} points de vie !")
        self.EquilibragePointsDeVieEtManaEtEndurance()
        self.vue.AfficheTalentCycleGlaciaire(commentaire)

    def AppliqueTalentFracturation(self):
        commentaire_supplementaire = ""
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 10:
            commentaire_supplementaire = "\nLes roches fracturent les os de l'ennemi, et la douleur paralyse l'ennemi pendant 2 tours !"
            self.modele.monstre_est_paralyse = True
            self.modele.monstre_est_paralyse_nombre_tour += 3
        return commentaire_supplementaire
    
    def AppliqueTalentEboulis(self, degat):
        commentaire_supplementaire = ""
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 15:
            commentaire_supplementaire = ("\nLes roches sont sous votre commandement, et s'acharnent une nouvelle fois"
                                          f" sur l'ennemi !\nVous lui infligez de nouveau {degat} points de dégâts !")
            self.modele.monstre_points_de_vie -= degat
        return commentaire_supplementaire
    
    def AppliqueSupportBonusItem(self, points_de_soin_ou_mana, type_de_soin):
        pourcentage = self.modele.SUPPORTBONUSITEM
        points_de_soin_ou_mana += round((pourcentage / 100) * points_de_soin_ou_mana)
        if type_de_soin == "vie":
            points_de_soin_ou_mana += self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Tisane d'Ecorce"]
        elif type_de_soin == "mana":
            points_de_soin_ou_mana += self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Tisane de Racine"]
        return points_de_soin_ou_mana
    
    def AppliqueTalentOeuilMagique(self):
        commentaire_effet = ""
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 5:
            commentaire_effet = "Votre oeuil magique s'active et inflige un effet élémentaire supplémentaire !\n"
            numero_de_leffet = random.randint(1, 5)
            if numero_de_leffet == 1:
                nombre_tour = 3
                nombre_tour += self.modele.TOURBONUSENNEMIENFEU
                if self.modele.utilise_rafale:
                    nombre_tour += nombre_tour
                if self.modele.stigma_monstre_negatif == "Inflammable":
                    nombre_tour += nombre_tour
                commentaire_effet = f"L'ennemi se met a bruler pendant {nombre_tour + 1} tours !"
                self.modele.monstre_est_en_feu = True
                self.modele.monstre_est_en_feu_degat = 5
                self.modele.monstre_est_en_feu_nombre_tour += nombre_tour
            elif numero_de_leffet == 2:
                nombre_tour = 3
                nombre_tour += self.modele.TOURBONUSENNEMIENGLACE
                commentaire_effet = f"L'ennemi se met a geler pendant {nombre_tour} tours !"
                self.modele.monstre_est_gele = True
                self.modele.monstre_est_gele_nombre_tour += nombre_tour
                if nombre_tour <= 0 :
                    commentaire_effet = "De part son origine nordique, l'ennemi résiste au gel infligé !"
                    self.modele.monstre_est_gele = False
                    self.modele.monstre_est_gele_nombre_tour = 0
            elif numero_de_leffet == 3:
                nombre_tour = 2
                nombre_tour += self.modele.TOURBONUSENNEMIENPARALYSIE
                commentaire_effet = "L'ennemi devient paralysé pendant 1 tour !"
                self.modele.monstre_est_paralyse = True
                self.modele.monstre_est_paralyse_nombre_tour += nombre_tour
                if nombre_tour <= 0 :
                    commentaire_effet = "Mais l'ennemi serre les dents et résiste à la paralysie infligée !"
                    self.modele.monstre_est_paralyse = False
                    self.modele.monstre_est_paralyse_nombre_tour = 0
            elif numero_de_leffet == 4:
                pourcentage_saignee = 3
                pourcentage_saignee += self.modele.DEGATSAIGNEE
                degat_saignee = round(pourcentage_saignee * self.modele.monstre_points_de_vie_max)
                degat_saignee = self.AppliqueLimitationSaignee(degat_saignee)
                self.modele.monstre_points_de_vie -= degat_saignee
                soin_saignee = degat_saignee
                soin_saignee = round((self.modele.SOINSSAIGNEE / 100) * soin_saignee)
                self.modele.points_de_vie += soin_saignee
                self.EquilibragePointsDeVieEtManaEtEndurance()
                commentaire_effet = f"L'ennemi se fait drainer {degat_saignee} points de vie et vous en regagnez {soin_saignee} !"
                if self.modele.anemie:
                    commentaire_effet += self.AppliqueTalentAnemie()
                if self.modele.baron_rouge:
                    commentaire_effet += self.AppliqueTalentBaronRouge()
                if self.modele.anticoagulants:
                    degat_de_saignement = round(degat_saignee * 0.2)
                    self.modele.monstre_points_de_vie -= degat_de_saignement
                    commentaire_effet += f"\nVous infligez {degat_de_saignement} points de vie a l'adversaire par saignement !"
            elif numero_de_leffet == 5:
                pourcentage_lapidation = 8
                pourcentage_lapidation += self.modele.DEGATLAPIDATION
                degat = round(pourcentage_lapidation * self.modele.monstre_points_de_vie_max)
                self.modele.monstre_points_de_vie -= degat
                commentaire_effet = f"L'ennemi se fait lapider et perd {degat} points de vie !"
        return commentaire_effet
    
    def AppliqueTalentAnemie(self):
        commentaire_supplementaire = ""
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 15:
            nombre_tour = 4
            commentaire_supplementaire = ("\nVous prenez bien plus de sang que necessaire, et la température"
                                          f" de l'ennemi diminue.\nIl se met a geler pendant {nombre_tour} tours !")
            self.modele.monstre_est_gele = True
            self.modele.monstre_est_gele_nombre_tour += nombre_tour
        return commentaire_supplementaire
    
    def AppliqueTalentBaronRouge(self):
        commentaire_supplementaire = ""
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 25:
            mana_recupere = round(self.modele.points_de_mana_max * 0.15)
            self.modele.points_de_mana_max += mana_recupere
            self.EquilibragePointsDeVieEtManaEtEndurance()
            commentaire_supplementaire = ("\nVous absorbez le mana contenu dans le sang drainé de l'ennemi."
                                          f"\nIVous récuperez {mana_recupere} points de mana !")
        return commentaire_supplementaire
    
    def AppliqueTalentConditionsLimites(self):
        commentaire = ("Vous tendez une main tremblante vers l'ennemi et faites utilisez toute la"
                       " force qui reste dans votre pitoyable corps pour attirer le sang environnant.")
        if self.modele.monstre_EstUnBoss:
            commentaire += "\nMais rien ne se passe."
        else:
            drain = round(self.modele.monstre_points_de_vie_max * 0.25)
            self.modele.monstre_points_de_vie -= drain
            self.modele.points_de_vie += drain
            self.EquilibragePointsDeVieEtManaEtEndurance()
            commentaire += f"\nLa vitalité de l'ennemi répond a votre appel et vous lui drainez {drain} points de vie !"
        self.vue.AfficheTalentConditionLimite(commentaire)
    
    def AppliqueTalentBougieMagique(self):
        commentaire = "\nL'ennemi n'est plus en feu !"
        if self.modele.bougie_magique:
            nombre_aleatoire = random.randint(0, 100)
            if nombre_aleatoire <= 15:
                commentaire = "\nL'ennemi allait s'éteindre...mais il se rallume pendant 2 tours !"
                self.modele.monstre_est_en_feu = True
                self.modele.monstre_est_en_feu_nombre_tour += 2
                self.modele.monstre_est_en_feu_degat = 5
        return commentaire
    
    def AppliqueTalentUltraInstinct(self):
        commentaire = "Alors même que le combat commence, vous utilisez une des techniques de votre arsenal à une vitesse ahurissante..."
        if ((len(self.modele.techniques) == 1) and ("Iaido" in self.modele)) or (len(self.modele.techniques) == 0):
            commentaire_resultat = "\n...enfin, si vous en aviez une."
            technique_a_effectuer = False
        else:
            limite_de_techniques = len(self.modele.techniques) - 1
            nom_technique = "Iaido"
            while nom_technique == "Iaido":
                numero_de_la_technique = random.randint(0, limite_de_techniques)
                nom_technique = self.modele.techniques[numero_de_la_technique]
            commentaire_resultat = f"...et choisissez [{nom_technique}]."
            technique_a_effectuer = True
        self.vue.AfficheTalentUltraInstinct(commentaire, commentaire_resultat)
        if technique_a_effectuer == True:
            self.UseAttack(nom_technique)

    def AppliqueTalentMaitreDuMana(self):
        mana_regagne = round(self.modele.points_de_mana_max * 0.03)
        if mana_regagne <= 0:
            mana_regagne = 1
        self.RecouvrementDeMana(mana_regagne)
        self.EquilibragePointsDeVieEtManaEtEndurance()
        commentaire = ("Vous commandez au mana perdu de venir"
                       " augmenter votre puissance."
                       f"\nVous regagnez {mana_regagne} points de mana !")
        self.vue.AfficheTalentMaitreDuMana(commentaire)

    def AppliqueTalentRejuvenation(self):
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire in [1, 2]:
            soin = round(self.modele.points_de_vie_max * 0.2)
            self.modele.points_de_vie += soin
            self.EquilibragePointsDeVieEtManaEtEndurance()
            commentaire = ("Votre corps est habitué à se regénérer grâce à de nombreuses"
                           " sources, et déclenche un processus de réjuvenation partielle"
                           f" par pur hasard.\nVous regagnez {soin} points de vie !")
            self.vue.AfficheTalentRejuvenation(commentaire)

    def SiZeroRameneAUn(self, nombre):
        if nombre <= 0:
            nombre = 1
        return nombre

    def AppliqueLimitationSaignee(self, degat_saignee):
        if degat_saignee > 50:
            degat_saignee = 50
        return degat_saignee

    def SeDefendre(self):
        self.RecupEndurance(7)
        if self.modele.mauvais_tachyon:
            self.ChangeChargeMauvaisTachyon("defense")
        if self.modele.bon_tachyon:
            self.ChangeChargeBonTachyon("defense")
        self.modele.se_defend = True
        commentaire = ("Vous ramenez vos bras a votre torse et vous préparez a recevoir un coup.")
        if self.modele.patience:
            soin = round(self.modele.points_de_vie_max * 0.05)
            self.modele.points_de_vie += soin
            self.EquilibragePointsDeVieEtManaEtEndurance()
            commentaire += f"\nLa Terre récompense votre patience. Vous reprenez {soin} points de vie !"
        if self.modele.est_maudit_par_les_items and "Larmes de Vénus" in self.modele.liste_dartefacts_optionels and random.randint(1,10) <= 2:
            commentaire += f"\nVénus libère votre âme des toxines de la Confusion !"
            self.modele.est_maudit_par_les_items = False
            self.modele.est_maudit_par_les_items_nombre_tour = False
        
        self.vue.AfficheSeDefendre(commentaire)

    
    def PasserSonTour(self):
        self.RecupEndurance(14)
        if self.modele.mauvais_tachyon:
            self.ChangeChargeMauvaisTachyon("passe tour")
        if self.modele.bon_tachyon:
            self.ChangeChargeBonTachyon("passe tour")
        personnage = "Vous passez votre"
        commentaire = "...tout simplement."
        if self.modele.patience:
            soin = round(self.modele.points_de_vie_max * 0.1)
            self.modele.points_de_vie += soin
            self.EquilibragePointsDeVieEtManaEtEndurance()
            commentaire = f"...et reprenez {soin} points de vie."
        if "Chapelet de Moine" in self.modele.liste_dartefacts_optionels:
            commentaire += "\nDe plus, votre chapelet se met a briller d'un feu sacré, et vous devenez [Béni] pendant 1 tour !"
            self.modele.beni_par_feu_sacre = True
            self.modele.beni_par_feu_sacre_nombre_tour += 2
        if "Dessin Nostalgique" in self.modele.liste_dartefacts_optionels:
            commentaire += "\nDe plus, le dessin dans votre poche vous calme, et vous gagnez l'effet [Concentration] pendant 2 tours !"
            self.modele.concentre = True
            self.modele.concentre += 2
        if "Basalte Immonde" in self.modele.liste_dartefacts_optionels and (self.modele.points_de_mana == self.modele.points_de_mana_max):
            commentaire += "\nDe plus, votre morceau de basalte allume en vous une colère insatiable, et vous gagnez l'effet [Furie] pendant 1 tour !"
            self.modele.utilise_orbe_de_furie = True
            self.modele.utilise_orbe_de_furie_nombre_tour += 2
        if "Jade Impardonnable" in self.modele.liste_dartefacts_optionels and (self.modele.points_de_mana == self.modele.points_de_mana_max):
            commentaire += "\nDe plus, votre morceau de jade allume en vous une folie née de l'angoisse, et vous gagnez l'effet [Folie] pendant 1 tour !"
            self.modele.utilise_orbe_de_folie = True
            self.modele.utilise_orbe_de_folie_nombre_tour += 2
        self.vue.AfficheRaisonDePasserTour(personnage, commentaire)


    def EnleveVieAuJoueur(self, degat):
        if self.modele.se_defend:
            reduction_de_degat = 0.25
            if "Bocle de Philoctète" in self.modele.liste_dartefacts_optionels:
                reduction_de_degat = 0.4
            degat = round ((1 - reduction_de_degat) * degat)
        degat = self.SiZeroRameneAUn(degat)
        if self.modele.metamorphose:
            self.vue.AfficheTalentMetamorphose()
        else:
            self.modele.points_de_vie -= degat
        return degat
    
    def RegardeSiMonstreAAssezDeMana(self, action):
        cout_en_mana = self.modele.ANNUAIRECOUTSORTMONSTRE[action]
        if self.modele.monstre_points_de_mana >= cout_en_mana:
            if self.modele.stigma_monstre_negatif == "Inconsolable Rage" and self.modele.monstre_points_de_mana >= (cout_en_mana * 2) and random.randint(1,10) <= 2 :
                cout_en_mana += cout_en_mana
            action_possible = True
            self.modele.monstre_points_de_mana -= cout_en_mana
        else:
            action_possible = False
        return action_possible
    
    def MetMonstreEnEtatDeChoc(self, action):
        self.vue.AfficheMonstreEtatDeChoc(action)
        self.modele.monstre_en_etat_de_choc = True
        self.modele.monstre_en_etat_de_choc_nombre_tour = 3
        self.modele.monstre_passe_son_tour = True

    def RecupEndurance(self, endurance_recuperee):
        if not self.modele.est_maudit_par_endurance:
            bonus_charge = 0
            if "Element [Corps] Surchargé" in self.modele.liste_dartefacts_optionels:
                bonus_charge += 4
            gain_endurance = endurance_recuperee + self.modele.numero_de_letage + bonus_charge
            self.modele.points_de_endurance += gain_endurance
            if (self.modele.points_de_endurance > self.modele.points_de_endurance_max) :
                self.modele.points_de_endurance = self.modele.points_de_endurance_max

    def AppliqueEffetElementaireSurJoueur(self, element, nombre_tour, degats = 0):
        if element == "feu":
            nombre_tour += round((self.modele.TOURBONUSJOUEURENFEU / 100) * nombre_tour)
            self.modele.est_en_feu = True
            self.modele.est_en_feu_nombre_tour += nombre_tour
            self.modele.est_en_feu_degat = degats
        elif element == "glace":
            nombre_tour += round((self.modele.TOURBONUSJOUEURENGLACE / 100) * nombre_tour)
            self.modele.est_gele = True
            self.modele.est_gele_nombre_tour += nombre_tour
        elif element == "foudre":
            nombre_tour += round((self.modele.TOURBONUSJOUEURENPARALYSIE / 100) * nombre_tour)
            self.modele.est_paralyse = True
            self.modele.est_paralyse_nombre_tour += nombre_tour

    def RecouvrementDeMana(self, points_de_mana_recouverts):
        self.modele.points_de_mana += points_de_mana_recouverts
        if self.modele.points_de_mana > self.modele.points_de_mana_max :
            self.modele.points_de_mana = self.modele.points_de_mana_max
        if ["Collier de Nephilim"] in self.modele.liste_dartefacts_optionels:
            self.modele.points_de_vie += round(points_de_mana_recouverts // 2)
            if self.modele.points_de_vie > self.modele.points_de_vie_max :
                self.modele.points_de_vie = self.modele.points_de_vie_max