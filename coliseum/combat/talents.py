"""Effets des talents du joueur."""

import random


class TalentsMixin:

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

    def AppliqueLimitationSaignee(self, degat_saignee):
        if degat_saignee > 50:
            degat_saignee = 50
        return degat_saignee
