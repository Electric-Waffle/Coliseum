"""Tour du monstre : choix de l'action, techniques et sorts génériques."""

import random

from coliseum.combat.attaques_speciales import (
    SORTS_SPECIAUX_DE_MONSTRE,
    SPECIALES_AVEC_JET_D_ESQUIVE,
    TECHNIQUES_SPECIALES_DE_MONSTRE,
)
from coliseum.combat.reductions import degats_apres_la_defence_du_joueur


class ActionsMonstreMixin:

    def GetMonsterChoice(self):
        # .items transforme le dictionnaire en une liste de plusieurs tuples
        # chaque tuples correspond a une paire clé/valeur
        # random.choice choisit un tuple aléatoire dans cette liste de tuples
        # la clé est affectée a la premiere variable (nom_action)
        # la valeur est affectée a la deuxieme variable (type_action)
        items_list = list(self.modele.monstre_liste_actions.items())
        nom_action, type_action = random.choice(items_list)
        return nom_action, type_action

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

    def AppliqueDegatsBonusDuMonstreContreLeJoueur(self, degat, attaque_normale=False, avec_reduction_plate=True):
        """Dégâts d'un coup de monstre : bonus du monstre, puis défense du joueur.

        1. POOL : bonus de force (ou d'intelligence), gel du joueur, stigmas...
           Ces pourcentages s'ADDITIONNENT entre eux, puis la somme s'applique
           une seule fois à la base. Pour une attaque normale, le bonus d'étage
           (+6 par étage au dessus du premier) entre dans la même somme.
        2. DÉFENSE : réduction en pourcentage, puis réduction plate, avec un
           plancher (voir reductions.py).

        - attaque_normale : True pour les attaques des tables générales (pas
          pour les attaques spéciales, dont la base grandit déjà avec l'étage).
        - avec_reduction_plate : False pour les dégâts sur la durée (brûlure).
        """
        if self.modele.type_daction_du_monstre == "Sort":
            pool = self.modele.DEGATSORTBONUSDUMONSTRE
        else:
            pool = self.modele.DEGATTECHNIQUEBONUSDUMONSTRE
        if attaque_normale:
            pool += self.modele.DEGATBONUSETAGEDUMONSTRE
        degat += round((pool / 100) * degat)
        return degats_apres_la_defence_du_joueur(degat, self.modele.DEFENCEEFFICACE, avec_reduction_plate)

    def LaSpecialeEstEsquivee(self, action):
        """Jet d'esquive pour les attaques spéciales qui n'en avaient pas.

        POURQUOI une liste : quelques attaques sont décrites comme inévitables
        (Laser Anti-Personnel, Protocole Supernova) ou ont leur propre jet
        (Coup Anti-Magie, Magie Noire, Jugement...). Seules celles de cette
        liste reçoivent le jet commun.

        Chance d'être touché = 100 - esquive, avec l'esquive plafonnée à 50
        (voir ESQUIVE_UTILE_MAX) : sans esquive, rien ne change ; au mieux
        l'attaque touche une fois sur deux, jamais moins.
        """
        if action not in SPECIALES_AVEC_JET_D_ESQUIVE:
            return False
        chance_d_etre_touche = 100 - self.modele.CHANCEBONUSESQUIVE
        return random.randint(1, 100) > chance_d_etre_touche

    def GereEsquiveDeLaSpeciale(self, action):
        commentaire = f"L'ennemi lance [{action}]...\n...mais vous parvenez à l'esquiver !"
        if "Tiare de Suie" in self.modele.liste_dartefacts_optionels:
            commentaire += "\nL'artefact [Tiare de Suie] bénit votre échappée !"
            self.modele.beni_par_feu_sacre = True
            self.modele.beni_par_feu_sacre_nombre_tour += 2
        self.vue.AfficheEsquiveDeLaSpeciale(commentaire)

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
                degat_de_base = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat_de_base, attaque_normale=True)
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
                                    degat_du_feu = self.CalculeCoupDeGraceDeLaBrulureSurJoueur()
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
                elif action in SORTS_SPECIAUX_DE_MONSTRE:
                    if self.LaSpecialeEstEsquivee(action):
                        self.GereEsquiveDeLaSpeciale(action)
                    else:
                        lancer_l_attaque_speciale = getattr(self, SORTS_SPECIAUX_DE_MONSTRE[action])
                        lancer_l_attaque_speciale()
            #affiche si les degats ont été changés par bluff, montagne, brume de sang ou mirroir d'eau
            if self.modele.commentaire_transmutation_degat != "":
                self.vue.AfficheTransmutationDegat(self.modele.commentaire_transmutation_degat)
        else:
            self.MetMonstreEnEtatDeChoc(action)

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
            degat_de_base = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat_de_base, attaque_normale=True)
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
                                degat_du_feu = self.CalculeCoupDeGraceDeLaBrulureSurJoueur()
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
                    degat = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat, attaque_normale=True)
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
            elif action in TECHNIQUES_SPECIALES_DE_MONSTRE:
                if self.LaSpecialeEstEsquivee(action):
                    self.GereEsquiveDeLaSpeciale(action)
                else:
                    lancer_l_attaque_speciale = getattr(self, TECHNIQUES_SPECIALES_DE_MONSTRE[action])
                    lancer_l_attaque_speciale()
        #affiche si les degats ont été changés par bluff, montagne, brume de sang ou mirroir d'eau
        if self.modele.commentaire_transmutation_degat != "":
            self.vue.AfficheTransmutationDegat(self.modele.commentaire_transmutation_degat)

    def RegardeSiMonstreAAssezDeMana(self, action):
        if self.modele.stigma_monstre_bonus == "Etoile":
            self.EffetStigmaEtoile()
            action_possible = True
        else :
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
