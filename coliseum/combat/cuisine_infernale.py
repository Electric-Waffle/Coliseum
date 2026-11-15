"""Mini-jeu de la Cuisine Infernale (combat contre Ahmed)."""

import random

from coliseum.console import ClearConsole


class CuisineInfernaleMixin:

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
                ClearConsole()
                if choix in range(1, len(liste_action) + 1):
                    break
            except ValueError:
                ClearConsole()
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
                    ClearConsole()
                    if choix in range(1, len(liste_ingredients) + 1):
                        break
                except ValueError:
                    ClearConsole()
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
                    ClearConsole()
                    if choix in range (1, len(liste_ingredients) + 1):
                        break
                except ValueError:
                    ClearConsole()
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
                        ClearConsole()
                        if choix in range(1, len(liste_ingredients_en_cuisson) + 1):
                            break
                    except ValueError:
                        ClearConsole()
                
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
