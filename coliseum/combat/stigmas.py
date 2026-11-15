"""Effets des stigmas du joueur et du monstre."""

import random

from coliseum.console import ClearConsole


class StigmasMixin:

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

    def EffetStigmaBergentruckung(self):
        element = "un coup de boule monstrueux."
        degat = round(self.modele.monstre_points_de_vie_max * 0.1)
        self.SiZeroRameneAUn(degat)
        self.modele.monstre_points_de_vie -= degat
        phrase = (
            f"Il va s'écraser à l'autre bout de la salle et perd {degat} points de vie !"
        )
        self.vue.AfficherAttaquePremierTour(element, phrase)

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
                ClearConsole()
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
                    ClearConsole()
                else:
                    self.modele.InCombat = False
                    self.modele.type_de_derniere_action_utilisee = "Fuir"
                ClearConsole()
            except ValueError:
                ClearConsole()
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

    def EffetStigmaOdeurPutride(self):
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 15:
            self.modele.est_maudit_par_endurance = True
            self.modele.est_maudit_par_endurance_nombre_tour += 3
            self.vue.AfficheOdeurPutride()

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

    def EffetStigmaBerserker(self):
        pourcentage_perdu = 100 - round((self.modele.points_de_vie_max * 100) / self.modele.points_de_vie_max)
        self.modele.DEGATBONUSMONSTREBERSERKER = pourcentage_perdu
        if pourcentage_perdu >= 50 :
            self.vue.AfficheStigmaBerserker(pourcentage_perdu)

    def EffetStigmaFlammeDesir(self):
        degat_flammes = round(self.modele.points_de_vie_max * 0.05)
        if self.modele.points_de_vie <= degat_flammes :
            degat_flammes = self.modele.points_de_vie - 1
        self.EnleveVieAuJoueur(degat_flammes)
        commentaire = f"Vous tentez de rester sur place pour passer votre tour ou vous défendre... mais les flammes du désir qui courent sur le sol vous brulent !\nVous perdez {degat_flammes} points de vie !"
        self.vue.AfficheStigmaFlammeDesir(commentaire)

    def EffetStigmaEtoile(self):
        commentaire = "Quand l'Etoile Du Matin lance un sort, c'est le mana qui se plie à sa volontée."
        self.vue.AfficheStigmaEtoile(commentaire)

    def EffetStigmaConcoctions(self):
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 25 :
            nombre_aleatoire = random.randint(0, 2)
            if nombre_aleatoire == 0 :
                self.modele.monstre_points_de_force += 2
                commentaire = "L'ennemi devient plus fort !"
            elif nombre_aleatoire == 1 :
                self.modele.monstre_points_de_intelligence += 2
                commentaire = "L'ennemi devient plus intelligent !"
            else :
                self.modele.monstre_points_de_resistance += 2
                commentaire = "L'ennemi devient plus résistant !"
            self.vue.AfficheStigmaConcoctions(commentaire)

    def EffetStigmaApathie(self):
        nombre_aleatoire = random.randint(0, 100)
        if nombre_aleatoire <= 10 :

            self.modele.est_maudit_par_le_gold = True
            self.modele.est_maudit_par_les_items = True
            self.modele.est_maudit_par_endurance = True

            # plus vie/mana
            self.modele.est_maudit_par_la_vie = True
            self.modele.est_maudit_par_le_mana = True

            # interdit sorts technique
            self.modele.est_maudit_par_les_sorts = True
            self.modele.est_maudit_par_les_techniques = True

            self.modele.est_maudit_par_endurance_nombre_tour += 2
            self.modele.est_maudit_par_les_items_nombre_tour += 2
            self.modele.est_maudit_par_le_gold_nombre_tour += 3
            self.modele.est_maudit_par_la_vie_nombre_tour += 3
            self.modele.est_maudit_par_le_mana_nombre_tour += 3
            self.modele.est_maudit_par_les_sorts_nombre_tour += 1
            self.modele.est_maudit_par_les_techniques_nombre_tour += 1

            self.vue.AfficheStigmaApathie()

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

    def EffetStigmaDernierChoix(self):
        while True:
            try:
                choix = self.vue.GetStigmaDernierChoixChoice()
                if choix in [1, 2]:
                    self.modele.dernier_choix_effectue = True
                    ClearConsole()
                    break
                ClearConsole()
            except ValueError:
                ClearConsole()
        if choix == 1:
            if random.randint(0, 1) == 0:
                liste_dennemis = self.modele.liste_de_monstre_totaux_pour_dernier_choix[self.modele.numero_de_letage - 1]
                commentaire = "La foule est en délire !\nParmis les spectateurs, une étrange forme éclate de rire, et fait disparaitre l'ennemi avec un claquement de doigts.\nQui sera son remplaçant ?"
                numero = 1
                for nom in liste_dennemis:
                    commentaire += f"\n{numero} - {nom}" 
                    numero += 1   
                while True:
                    try:
                        choix = self.vue.GetStigmaDernierChoixEnnemyChoice(commentaire)
                        if choix in range(1, (len(liste_dennemis) + 1)):
                            ClearConsole()
                            ancien_monstre = self.modele.monstre_nom
                            self.modele.monstre_nom = liste_dennemis[choix - 1]
                            self.SetAttributesFromName()
                            self.vue.AfficheNouveauMonstre(
                                ancien_monstre, self.modele.monstre_nom
                            )
                            break
                        ClearConsole()
                    except ValueError:
                        ClearConsole()
            else:
                liste_commentaires = [
                    "La foule ne réagit pas.\nPeut être l'avez elle vu venir, le plot-twist...",
                    "Les spectateurs se regardent, interloqués.\nVous l'entendez murmurer : *C'est quoi , un plot twist ?*",
                    "Vous recevez une boite de thon sur le coin de la figure, alors que les spectres vous hue, en scandant *On en a marre des plot twist ! C'est un outil d'écriture pour les fénéants ! Surtout quand ya pas de foreshadowing avant !*",
                    "La foule vous regarde, inexpressive.\nLe public est dur, aujourd'hui.",
                    "*Renifler ? On est des spectres, andouille ! On a pas de nez !*\nSi les remarques de vos spectateurs vous amusent un peu, celles qui vous traitent de *spectrophobie* vous font carrément flipper.\nYa moyen de se faire cancel quand on est au fond d'un donjon ???",
                    "Un lourd silence suit votre tirade.\nUn des spectateurs applaudit très fort, seul touché par votre humour.\nCela ne rend pas la scène moins génante.\nOuch.",
                    "*On s'en fout de tes blagues !*\nOuch.",
                    "*Bouh ! Montre nous tes pieds !*\nL'ennemi et vous vous retournez vers le spectatueur, qui s'arrête un instant avant de lacher un *Bah quoi ?* aussi sonore que désopilant.\nAu grand dam de la liberté d'expression, deux figures fantomatiques escortent le spectre en dehors des gradins.",
                    "*Et sinon , pour quand le prochain épisode de Skyrim ?*\nVous vous étonnez de la présence d'un de vos viewers dans les gradins, et choisissez de répondre a son innocente question par un silence lourd en signification.",
                    "Un spectre n'as pas compris.\nIl vous demande alors d'expliquer votre blague.\nSi votre mentor était là, il vous dirait : *On apelle ça un bide.* avant de lacher un taquin *git good* dont lui seul a le secret.",
                    "Ca n'a pas marché.\nNe cherchez pas de raisons.\nL'humour, ya des jours avec et des jours sans.",
                    "La foule est en délire !\nParmis les spectateurs, une étrange forme éclate de rire, et fait disparaitre l'ennemi avec un claquement de doigts.\nEnfin, elle claque des doigts, mais rien ne se passe.\nElle regarde, intelroqué, sa main, puis hausse les épaules.",
                    "Si seulement...Mais non.\nPas de changements pour vous.",
                    "Changer l'ennemi, c'est du 50/50.\nEt là, vous êtes dans le mauvais 50.\nCelui ou il se passe rien.",
                    "Et c'est un non ! Bien essayé, mais c'est malheureusement insuffisant !",
                    "La prochaine fois, peut être.\nMais pas *cette* prochaine fois.",
                    "On auraitcru que ca marche cette fois ci.. sauf que ca a pas marché.",
                    "La prochaine fois, peut être.\nMais pas... Ah , je l'ai déja faite, celle ci.",
                    "C'est quand la derniere fois que vous avez bu de l'eau ?\nParce que j'aimerai dire *Comptez la dessus et buvez de l'eau !*, mais si vous en avaez bu récemment ca n'as pas de sens...",
                    "Un petit jeu ?\nJe vous demande, parceque celui ci, vous l'avez perdu.\nEt par celui ci, j'entend *changer l'ennemi*.\nAllez je commence :\nQu'est-ce qui a 3 E et ne contient pourtant qu'une seule lettre ?\n\nVous chercherez la répone sur le net.",
                    "Prenez un peu de temps, écoutez la musique.\nC'est sympa non ?\nC'est moi qui l'aie choisie !\n\nSinon, pour le changement d'ennemi, ca a pas marché, et tout le monde vous déteste.\nWomp Womp.",
                    "Une étrange figure dans les gradin vous lance un *bof*, et vous comprenez que vous ne changerez pas l'ennemi de sitôt.",
                    "Une étrange figure dans les gradins tend le bras, poing fermé sauf pour un pouce tendu a l'horizontale... et qui pointe maintenant vers le sol.\nDommage.",
                    "...c'est vraiment avec ce genre d'humour que vous avez conquis les plateformes de streaming ???\nC'est qui vos viewers ?\nDes enfants ?",
                    "Une lumière rouge illumine la pièce pendant un quart de seconde, et un bruit de buzzer se fait entendre.\nUn spectre, les mains posées sur un pupitre, regarde l'arène, et une voix se fait entendre :\n*Alors Pedro ? Quelle est votre réponse ?*\nLe Spectre répond alors : *Euh..Euh... C'est... c'est vraiment Nul ! Réponse A ! Et elle est Finale !*\nLa même voix se fait entendre : *Eh bien Pedro... c'est... c'est une bonne réponse ! A vous les 10 essences dorées !*\nVous arretez d'écouter les gradins se moquer de vous, et retournez au combat.\n\nUne larme perle au coin de vos yeux...\n",
                    "Vous terminez de parlez et finissez par zozoter le dernier mot.\nNon seulement vous avez l'aire d'un couillon, mais en plus on se moque de vous.\nPas facile, les cheveux sur la langue...",
                    "Vous pensez a énoncer les mots que vous avez soigneusements choisi, avant de vous raviser : la blague est vraiment trop pourrie.",
                    "Craignos.\nMême moi j'aurais jamais dit ca devant un public.\nJ'ai aucune envie de décrire, ni d'imaginer la scène.\nOn va juste dire que ca a échoué.\nRetour au combat.",
                    "Ca vous plait, toute ces répliques différentes ?\nMoi aussi !\n Dans la pluspart, je vous insulte cordialement, et ca c'est un vrai plaisir !\nJ'espère juste que c'est pas la premiere fois que vous échoué, sinon cette réplique vous paraitra bizarre.\nPardon ?\nOui, bien sûr.\nVous avez échoué a changer l'ennemi.\nChop Chop, retour au combat !",
                ]
                self.vue.StigmaDernierChoixEchec(liste_commentaires[random.randint(0, (len(liste_commentaires)-1))])

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
                ClearConsole()
                if choix in [1, 2, 3, 4]:
                    # 4: comparer la réponse donnée a la réponse voulue
                    if choix == question_pose["Reponse a la question"]:
                        return True
                    else:
                        return False
            except ValueError:
                ClearConsole()

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

        # stigma joueur positif
        if self.modele.stigma_joueur_positif == "Bénie par les Fées":
            self.EffetStigmaBeniParLesFees()
        elif self.modele.stigma_joueur_positif == "Second Souffle":
            self.EffetStigmaSecondSouffle()
        elif self.modele.stigma_joueur_positif == "Recharge Rapide":
            self.EffetStigmaRechargeRapide()
        elif self.modele.stigma_joueur_positif == "Transhumanisme":
            self.EffetStigmaTranshumanisme()
        elif self.modele.stigma_joueur_negatif == "Pause Repas":
            self.EffetStigmaPauseRepas()
        elif self.modele.stigma_joueur_negatif == "Miss Hyde":
            self.EffetStigmaMissHyde()
        elif self.modele.stigma_joueur_negatif == "Fatigue Chronique":
            self.EffetStigmaFatigueChronique()
        elif self.modele.stigma_joueur_negatif == "Flemme":
            self.EffetStigmaFlemme()
        elif self.modele.stigma_joueur_negatif == "Ange Déchue":
            self.EffetStigmaAngeDechue()

        # stigma joueur bonus
        if self.modele.stigma_joueur_bonus == "Sanjiva":
            self.EffetStigmaSanjiva()
        elif self.modele.stigma_joueur_bonus == "Musculeux":
            self.EffetStigmaMusculeux()

        # stigma monstre positif
        if self.modele.stigma_monstre_positif == "Toucher de Midas" and random.randint(0,100) <= 5:
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
        elif self.modele.stigma_monstre_positif == "Odeur Putride":
            self.EffetStigmaOdeurPutride()
        elif self.modele.stigma_monstre_positif == "Plus d'un Tour":
            self.EffetStigmaPlusDUnTour()

        # stigma monstre negatif
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

        # stigma montre bonus
        if self.modele.stigma_monstre_bonus == "Berserker":
            self.EffetStigmaBerserker()
        elif self.modele.stigma_monstre_bonus == "Concoctions":
            self.EffetStigmaConcoctions()
        elif self.modele.stigma_monstre_bonus == "Apathie":
            self.EffetStigmaApathie()

        # effet artefact joueur ou tag mostre
        if "Mage" in self.modele.liste_dartefacts_optionels:
            self.AppliqueMage()
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

    def EffetStigmaSecondSouffle(self):
        if self.modele.points_de_endurance < self.modele.points_de_endurance_max * 0.5 :
            self.modele.points_de_endurance += 3
            self.vue.AfficheStigmaSecondSouffle("Votre entrainement vous permet de calmer votre respiration a travers l'essouflement et vous regagnez des points d'endurance.")
        if self.modele.points_de_endurance > self.modele.points_de_endurance_max :
            self.modele.points_de_endurance = self.modele.points_de_endurance_max

    def EffetStigmaRechargeRapide(self):
        if self.modele.points_de_mana < self.modele.points_de_mana_max * 0.5 :
            self.RecouvrementDeMana(3)
            self.vue.AfficheStigmaRechargeRapide("Vous invoquez dans votre esprit le gout que la dinde avait lors d'un de ces somptueux banquets a Venise... et reprenez des points de mana .")

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
        if (random.randint(0,100) <= 8 and not self.TousItemsVides()):

            #  item aléatoire
            item_a_manger = random.choice(self.ListeItemsPossedes())

            #  disparition de l'item
            self.modele.items[item_a_manger] -= 1

            # récupération des pm
            self.RecouvrementDeMana(int(round(self.modele.points_de_mana_max * 0.15)))

            #  affichage de l'action
            self.vue.AfficheStigmaPauseRepas(f"Vous avez faim. Vous farfouillez dans votre sac et sortez l\'item [{item_a_manger}] que vous vous empressez d'avaler.\nPas d'effets, mais vous reprenez quelques pm !")

    def EffetStigmaCircuitsLogiques(self):
        if self.modele.points_de_vie < round(self.modele.points_de_vie_max * 0.05):
            self.modele.InCombat = False
            self.modele.type_de_derniere_action_utilisee = "Fuir"
            self.vue.AfficheCircuitsLogiques()
