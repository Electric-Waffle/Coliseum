"""Effets d'artefacts, de tags de monstre et de bénédictions."""

import random


class EffetsMixin:

    def AppliqueTank(self):
        degat = round(self.modele.monstre_points_de_vie_max * 0.15)
        self.modele.monstre_points_de_vie -= degat
        self.vue.AfficheTank(degat)

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
            self.modele.liste_dartefacts_optionels.remove("Epée de Damocles")
            self.vue.AfficheEppeeDamocles()

    def EffetMorceauEtherFragile(self):
        numero_aleatoire = random.randint(0, 100)
        if numero_aleatoire in [1, 2, 3]:
            self.modele.points_de_mana = 0
            self.Player.liste_dartefacts_optionels.remove("Morceau d'Ether Fragile")
            self.modele.liste_dartefacts_optionels.remove("Morceau d'Ether Fragile")
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
