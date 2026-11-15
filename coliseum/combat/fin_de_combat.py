"""Surveillance des points de vie, résurrections, game over, fuite et récompenses."""

import random
from coliseum.console import attendre


class FinDeCombatMixin:

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
            if self.Player.malediction == "Impotent" and self.modele.nombre_de_tours <= 3:
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
                                                "Spectre", "Aurore", "Le Pianiste"] and self.modele.monstre_nombre_de_vies_supplementaire == 0:
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
                            self.SetAttributesFromName()
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
                            if self.modele.est_une_mimique :
                                nombre_aleatoire = 0
                            limite = 25 + self.Player.dictionnaire_duppgrade_qui_necessitent_plus_de_code_pour_fonctionner["Médaillon de Leprechaun"]
                            if nombre_aleatoire <= limite:
                                materiau = self.modele.monstre_recompense[
                                    cle
                                ]
                                self.Player.liste_de_materiaux[materiau] += 1
                                commentaire = (
                                    f"L'ennemi lache le materiau [{self.modele.monstre_recompense[cle]}] !"
                                )
                                if self.modele.stigma_joueur_bonus == 'Démanteleur' and random.randint(0,100)<25 :
                                    self.Player.liste_de_materiaux[materiau] += 1
                                    commentaire += (
                                        f"\nVous démantelez son cadavre d'une main experte et récupérez un deuxieme materiau !"
                                    )
                            else : 
                                continue
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
                    if ("Marque du Tyrant" in self.modele.liste_dartefacts_optionels) and (self.modele.points_de_vie_max == self.modele.points_de_vie):
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
                        self.modele.liste_dartefacts_optionels.append("Carte de Sécurité")
                        self.vue.AffichageMonstreDopeRecompense(commentaire1, commentaire2)
                    if self.modele.est_une_mimique:
                        commentaire1 = ("Le corps de la mimique git a terre...\nVous en profitez pour fouiller a l'interieur du coffre doré.")
                        commentaire2 = ("Vous en sortez un (autre) petit coffre de bois noir, que vous vous empressez d'ouvrir !")
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
                        if self.modele.monstre_EstUnBoss :
                            self.Sove.RajouteEntreeAuLivreCigogneBlancheSiOnAPas("Les Boss", self.modele.monstre_nom)
                        else :
                            self.Sove.RajouteEntreeAuLivreCigogneBlancheSiOnAPas("Les Ennemis", self.modele.monstre_nom)
            if self.modele.possede_une_fee == False :
                self.vue.AffichePlusDeFee()
                self.Player.possede_une_fee = False
                
        self.StopCombatSounds()

    def StopCombatSounds(self):
        self.vue.CHANNELSONSORT.set_volume(0)
        self.vue.CHANNELSONTECHNIQUE.set_volume(0)
        self.vue.CHANNELMUSIQUECOMBAT.set_volume(0)
        attendre(0.01)
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
