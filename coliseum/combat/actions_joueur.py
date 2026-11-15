"""Tour du joueur : menu d'actions, techniques, sorts, objets, défense, fuite."""

import random

from coliseum.console import ClearConsole


class ActionsJoueurMixin:

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
                    ClearConsole()
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
                    ClearConsole()
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
                    ClearConsole()
                    # affiche la fin du menu (l'input)
                    liste_de_numero_daction_possible = self.GetListOfActionPossible(
                        nombre_associe_a_laction_pour_lutilisateur
                    )
                    if valeur_action not in liste_de_numero_daction_possible:
                        valeur_action = None  # valeur invalide
                except ValueError:
                    ClearConsole()
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
                if caracteristique_du_techniques[2] >= 15:
                    pourcentage_de_critique = random.randint(10, 15)
                elif caracteristique_du_techniques[2] <= 5:
                    pourcentage_de_critique = random.randint(0, 5)
                else:
                    pourcentage_de_critique = random.randint(5, 10)
                pourcentage_de_critique += self.modele.CHANCECOUPCRITIQUE
                # application des modificateurs sur les degats de coup critique
                degat_critique = caracteristique_du_techniques[3]
                degat_critique += self.modele.degat_de_coup_critique
                degat_critique += round(self.modele.accumulation_degat_technique_critique)
                degat_critique += round(
                    (self.modele.DEGATBONUSATTAQUECRITIQUE / 100) * degat_critique
                )
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
                                if self.modele.stigma_monstre_positif == "Coeur Inferno":
                                    nombre_aleatoire = 0
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
                                if self.modele.stigma_monstre_positif == "Coeur Inferno":
                                    nombre_aleatoire = 0
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
                    degat_critique += self.modele.degat_de_coup_critique
                    degat_critique += round(self.modele.accumulation_degat_technique_critique)
                    degat_critique += round(
                        (self.modele.DEGATBONUSATTAQUECRITIQUE / 100) * degat_critique
                    )
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
                if caracteristique_du_sort[2] >= 15:
                    pourcentage_de_critique = random.randint(10, 15)
                elif caracteristique_du_sort[2] <= 5:
                    pourcentage_de_critique = random.randint(0, 5)
                else:
                    pourcentage_de_critique = random.randint(5, 10)
                pourcentage_de_critique += self.modele.CHANCESORTCRITIQUE
                # application des modificateurs sur les degats de coup critique
                degat_critique = caracteristique_du_sort[3]
                degat_critique += self.modele.degat_de_sort_critique
                degat_critique += round(self.modele.accumulation_degat_sort_critique)
                degat_critique += round(
                    (self.modele.DEGATBONUSSORTCRITIQUE / 100) * degat_critique
                )
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
                                if self.modele.stigma_monstre_positif == "Coeur Inferno":
                                    nombre_aleatoire = 0
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
                                if self.modele.stigma_monstre_positif == "Coeur Inferno":
                                    nombre_aleatoire = 0
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
                                if self.modele.stigma_monstre_positif == "Coeur Inferno":
                                    nombre_aleatoire = 0
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
            self.Sove.RajouteEntreeAuLivreCigogneBlancheSiOnAPas("Les Items", nom_de_litem)
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

    def SeDefendre(self):
        if self.modele.stigma_monstre_bonus == "Flammes du Désir":
            self.EffetStigmaFlammeDesir()
        else :
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
        if self.modele.stigma_monstre_bonus == "Flammes du Désir":
            self.EffetStigmaFlammeDesir()
        else:
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
