"""Altérations d'état (feu, poison, gel...) : application à chaque tour et affichage."""



class AlterationsMixin:

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

    def RaisonDePasserSonTour(self):
        if self.modele.stigma_monstre_bonus == "Flammes du Désir":
            self.EffetStigmaFlammeDesir()
            self.modele.en_plein_iaido = False
            self.modele.en_plein_iaido_nombre_tour = 0
            self.modele.abomination_touche = False
            self.modele.passe_son_tour = False
        else :
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
            if self.modele.stigma_monstre_positif == "Pyrocien" and not self.modele.monstre_en_etat_de_choc and (self.modele.monstre_points_de_mana + round(degat * 0.5)) <= self.modele.monstre_points_de_mana_max :
                mana_recup = round(degat * 0.5)
                self.modele.monstre_points_de_mana += mana_recup
                commentaire += f"L'ennemi stimule ses veines de mana grâce au feu, et il récupère des points de mana."
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
        if self.modele.stigma_monstre_bonus == "Aura Corrosive":
            self.modele.est_maudit_par_la_vie = True
            self.modele.est_maudit_par_la_vie_nombre_tour = 2
            self.modele.est_maudit_par_le_mana = True
            self.modele.est_maudit_par_le_mana_nombre_tour = 2
            commentaire += "\nVous n'arrivez pas a supporter l'Aura Corrosive de l'ennemi ! Vous êtes blessé et déconcentré continuellement !"
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
        if self.modele.stigma_monstre_positif == "Coeur Inferno":
            self.modele.est_en_feu = True
            self.modele.est_en_feu_nombre_tour = 2
            self.modele.est_en_feu_degat = 5
            commentaire += "\nLes flammes qui incinèrent l'Arène vous font l'effet d'une fournaise ! Vous brûlez continuellement !"
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
            self.modele.est_paralyse_nombre_tour += nombre_tour + 1
