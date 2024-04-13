import random


class Model:

    def __init__(self, Player):

        BuildABear = False  # debug mode
        if BuildABear:
            # caractéristiques
            self.points_de_vie = int(input("Combien de points de vie ?"))
            self.points_de_vie_max = int(input("Combien de points" " de vie max ?"))
            self.points_de_mana = int(input("Combien de points de mana ?"))
            self.points_de_mana_max = int(input("Combien de points " "de mana max ?"))
            self.points_de_defence = int(input("Combien de points" " de defence ?"))
            self.points_de_force = int(input("Combien de points de force ?"))
            self.points_de_intelligence = int(
                input("Combien de points d'intelligence ?")
            )
            self.taux_de_coup_critique = int(input("Pourcentage de coup" "critique ?"))
            self.degat_de_coup_critique = int(input("Degat de coup" " critique ?"))
            self.taux_de_sort_critique = int(input("Pourcentage de sort " "critique ?"))
            self.degat_de_sort_critique = int(input("Degat de sort" " critique ?"))
            self.taux_de_esquive = int(input("Pourcentage d'esquive ?"))
            self.nombre_de_gold = int(input("Combien de golds ?"))

        else:
            self.points_de_vie = Player.points_de_vie
            self.points_de_vie_max = Player.points_de_vie_max
            self.points_de_mana = Player.points_de_mana
            self.points_de_endurance_max = Player.points_dendurance
            self.points_de_endurance = self.points_de_endurance_max
            self.points_de_mana_max = Player.points_de_mana_max
            self.points_de_defence = Player.points_de_defence
            self.points_de_force = Player.points_de_force
            self.points_de_intelligence = Player.points_dintelligence
            self.taux_de_coup_critique = Player.taux_coup_critique
            self.degat_de_coup_critique = Player.degat_coup_critique
            self.taux_de_sort_critique = Player.taux_sort_critique
            self.degat_de_sort_critique = Player.degat_sort_critique
            self.taux_de_esquive = Player.taux_desquive
            self.nombre_de_gold = Player.nombre_de_gold
            self.quete_en_cours = Player.quete
            self.liste_dartefact_optionels = Player.liste_dartefacts_optionels
            self.nombre_de_red_coin = Player.nombre_de_red_coin
            self.numero_de_letage = Player.numero_de_letage
            self.est_une_mimique = Player.affronte_une_mimique
            self.monstre_EstUnBoss = Player.affronte_un_boss
            self.stigma_joueur_positif = Player.stigma_positif
            self.stigma_joueur_negatif = Player.stigma_negatif
            self.stigma_joueur_bonus = Player.stigma_bonus
            self.nombre_de_monstres_tues = Player.nombre_de_monstres_tues  # nombres de monstres tues, pour les ames
            self.possede_une_fee = Player.possede_une_fee  # reprend toute sa vie a la mort, une fois
            self.possede_une_gemme_vie = Player.gemme_de_vie  # rend 20% de vie a la fin d'un combat
            self.possede_une_gemme_magie = Player.gemme_de_mana  # rend 20% de mana a la fin d'un combat
            self.monstre_de_lobelisque = Player.affronte_obelisque

        # alteration de letat ou influence d'artefacts
        self.sacrifice_actif = False
        self.se_defend = False
        self.nombre_de_tours = 1
        self.commentaire_transmutation_degat = ""
        self.gain_mana_mutagene = 0
        self.perd_mana_mutagene = 0
        self.gain_vie_mutagene = 0
        self.perd_vie_mutagene = 0
        self.utilise_orbe_de_furie_nombre_tour = 0
        self.utilise_orbe_de_folie_nombre_tour = 0
        self.beni_par_feu_sacre = False
        self.beni_par_feu_sacre_nombre_tour = 0
        self.utilise_mirroir_eau = False
        self.mirroir_eau_nombre_tours = 0
        self.utilise_brume_sang = False
        self.brume_sang_nombre_tours = 0
        self.rafale_nombre_tours = 0
        self.limite_degat = 0
        self.utilise_le_massif = False
        self.utilise_le_bluff = False
        self.gain_de_defence = 0
        self.utilise_posture_de_la_montagne = False
        self.posture_de_la_montagne_tour = 0
        self.stigma_consumme_tour = random.randint(1, 4)
        self.a_utilise_sang_ce_tour = False
        self.a_utilise_feu_ce_tour = False
        self.a_utilise_foudre_ce_tour = False
        self.a_utilise_glace_ce_tour = False
        self.a_utilise_terre_ce_tour = False
        self.a_utilise_physique_ce_tour = False
        self.musculeux_touche = False
        self.abomination_touche = False
        self.aveugle_touche = False
        self.dernier_choix_effectue = (
            False  # Regarde si le stigma dernier choix a deja prit effet
        )
        self.passe_son_tour = False  # Passe son tour ou non
        self.flemme = False  # savoir si le joueur a la flemme
        self.en_plein_iaido = False  # savoir si le joueur est en plein iaido
        self.en_plein_iaido_nombre_tour = 0
        self.est_maudit_par_la_vie = False  # attaques coutent de la vie
        self.est_maudit_par_la_vie_nombre_tour = 0
        self.est_maudit_par_le_gold = False  # sorts et attaques coutent gold
        self.est_maudit_par_le_gold_nombre_tour = 0
        self.est_maudit_par_le_mana = False  # sorts coutent plus de mana
        self.est_maudit_par_le_mana_nombre_tour = 0
        self.est_gele = False  # gele, prend 2x + de degats
        self.est_gele_nombre_tour = 0
        self.est_en_feu = False  # en feu, dégats sur le temps
        self.est_en_feu_nombre_tour = 0
        self.est_en_feu_degat = 0
        self.est_paralyse = False  # paralysé, passe son tour
        self.est_paralyse_nombre_tour = 0
        self.est_maudit_par_les_techniques = False  # plus d'utilisation de techniques
        self.est_maudit_par_les_techniques_nombre_tour = 0
        self.est_maudit_par_les_sorts = False  # plus d'utilisation de sorts
        self.est_maudit_par_les_sorts_nombre_tour = 0
        self.est_maudit_par_les_items = False  # plus d'utilisation d'item
        self.est_maudit_par_les_items_nombre_tour = 0
        self.est_enpoisonne = False  # empoisonné, gros dégats sur peu de temps
        self.est_enpoisonne_nombre_tour = 0
        self.est_enpoisonne_degat = 0
        self.level_de_poison = 0
        self.utilise_pousse_adrenaline = False
        self.pousse_adrenaline_tour = 0
        self.utilise_ambroisie = False  # utilise l'ambroisie
        self.utilise_ambroisie_nombre_tour = 0
        self.utilise_hydromel = False  # utilise l'hydromel
        self.utilise_hydromel_nombre_tour = 0
        self.utilise_feuille_jindagee = False  # utilise feuille jindagee
        self.utilise_feuille_jindagee_nombre_tour = 0
        self.utilise_fruit_jindagee = False  # utilise fruit jindagee
        self.utilise_fruit_jindagee_nombre_tour = 0
        self.utilise_feuille_aatma = False  # utilise feuille aatma
        self.utilise_feuille_aatma_nombre_tour = 0
        self.utilise_fruit_aatma = False  # utilise fruit aatma
        self.utilise_fruit_aatma_nombre_tour = 0
        self.utilise_orbe_de_folie = False  # utilise orbe folie
        self.utilise_orbe_de_furie = False  # utilise orbe furie
        self.mutagene_bleu_utilise = False
        self.grand_mutagene_bleu_utilise = False
        self.mutagene_rouge_utilise = False
        self.grand_mutagene_rouge_utilise = False
        self.mutagene_vert_utilise = False
        self.grand_mutagene_vert_utilise = False
        self.mutagene_dore_utilise = False
        self.grand_mutagene_dore_utilise = False
        self.mutagene_heretique_utilise = False
        self.mutagene_fanatique_utilise = False
        self.utilise_rafale = False

        # influence de l'arbre de talent
        # FEU  (DMG OVER TIME)
        self.affinite_au_feu = False  # augmente les degats des attaques de feu DONE
        if "Affinitée de Feu" in Player.talents_possedes:
            self.affinite_au_feu = True
        self.surchauffe = False  # augmente les degat du feu DONE
        if "Surchauffe" in Player.talents_possedes:
            self.surchauffe = True
        self.aura_de_feu = False  # augmente la duree du feu DONE
        if "Aura de Feu" in Player.talents_possedes:
            self.aura_de_feu = True
        self.rafale = False  # double sort de feu mais x2.1 mana /sort a rajouter () DONE
        if "Rafale" in Player.talents_possedes:
            self.rafale = True
        self.pyrophile = False  # joueur en feu regagne mana DONE
        if "Pyrophile" in Player.talents_possedes:
            self.pyrophile = True
        self.pyrosorcier = False  # cible en feu donne mana DONE
        if "Pyrosorcier" in Player.talents_possedes:
            self.pyrosorcier = True
        self.pyromage = False  # cible en feu donne vie (50% degats du feu) DONE
        if "Pyromage" in Player.talents_possedes:
            self.pyromage = True

        # FOUDRE (PASS ENEMY TURN)
        self.affinite_electrique = False  # augmente les degats des attaques de foudre DONE
        if "Affinitée de Foudre" in Player.talents_possedes:
            self.affinite_electrique = True
        self.anti_neurotransmitteurs = False  # ennemi prend degats quand paralysé DONE
        if "Anti-Neurotransmitteurs" in Player.talents_possedes:
            self.anti_neurotransmitteurs = True
        self.anti_neurotransmitteurs_degat = 5  # points de degat also done
        self.energiseur = False  # sorts electrique coute moins de mana DONE
        if "Energiseur" in Player.talents_possedes:
            self.energiseur = True
        self.facture = False  # ennemi tué quand paralysé lachent x5 gold DONE
        if "Facture" in Player.talents_possedes:
            self.facture = True
        self.rapide = False  # 50% commence le combat avec ennemi paralyse [x] DONE
        if "Rapide" in Player.talents_possedes:
            self.rapide = True
        self.electro = False  # si rapide procs, ennemi perd 10% de sa vie DONE
        if "Electro" in Player.talents_possedes:
            self.electro = True
        self.luciole = False  # ennemi paralyse s'enflamme pendant 2 tours DONE
        if "Luciole" in Player.talents_possedes:
            self.luciole = True
        self.luciole_etat = False  # en feu electrique ou pas also done
        self.luciole_degat = 10  # points de vie also done
        self.luciole_tour = 0  #nombre tour feu electrique also done

        # GLACE  (FREEZE THE ENNEMY, TAKES 2x DMG)
        self.affinite_de_glace = False  # augmente les degats des attaques de glace DONE
        if "Affinitée de Glace" in Player.talents_possedes:
            self.affinite_de_glace = True
        self.ere_glaciaire = False  # augmente la duree du gel DONE
        if "Ere Glaciaire" in Player.talents_possedes:
            self.ere_glaciaire = True
        self.eclats_de_glace = False  # ennemi degele prend degat DONE
        if "Eclats de Glace" in Player.talents_possedes:
            self.eclats_de_glace = True
        self.grand_froid_degat_supplement = 0
        self.eclats_de_glace_degat = 10  #points de vie
        self.grand_froid = False  # 50% chance ennemi gele 4t au debut combat, eclat de glace fait plus de degats [x] DONE
        if "Grand Froid" in Player.talents_possedes:
            self.grand_froid = True
        if self.grand_froid:
            self.eclats_de_glace_degat += 5  # eclat de glace fait plus de degat
        self.choc_thermique = False  # degat feu x2 sur ennemi gele DONE
        if "Choc Thermique" in Player.talents_possedes:
            self.choc_thermique = True
        self.coeur_de_glace = False  # chance de se faire passer son tour /2 DONE
        if "Coeur de Glace" in Player.talents_possedes:
            self.coeur_de_glace = True
        self.cycle_glaciaire = False  # regagne vie quand ennemi degele DONE
        if "Cycle Glaciaire" in Player.talents_possedes:
            self.cycle_glaciaire = True

        # TERRE  (LOW CHANCE OF HEAVY DMG : LAPIDATION)
        self.affinite_de_terre = False  # augmente les degats des attaques de terre DONE
        if "Affinitée de Terre" in Player.talents_possedes:
            self.affinite_de_terre = True
        self.patience = False  # regagne vie quand passe son tour DONE
        if "Patience" in Player.talents_possedes:
            self.patience = True
        self.rigueur = (
            False  # posture de la montagne, defence up +3 pdt 5t /technique a rajouter DONE
        )
        if "Rigueur" in Player.talents_possedes:
            self.rigueur = (
                True  # posture de la montagne, defence up +3 pdt 5t /technique a rajouter DONE
            )
        self.fracturation = False  # 10% de paralysie si lapidation proc DONE
        if "Fracturation" in Player.talents_possedes:
            self.fracturation = True
        self.poussiere_de_diamant = (
            False  # cout mana des sorts de terre = % de vie restant DONE
        )
        if "Poussière de Diamants" in Player.talents_possedes:
            self.poussiere_de_diamant = (
                True  # cout mana des sorts de terre = % de vie restant DONE
            )
        self.richesse_souterraine = False  # gold laché x2.5 DONE
        if "Richesses Souterraines" in Player.talents_possedes:
            self.richesse_souterraine = True
        self.eboulis = False  # 15% de re-lapider un ennemi lapidé DONE
        if "Eboulis" in Player.talents_possedes:
            self.eboulis = True

        # PHYSIQUE (LOW DMG, SUPPORT OTHER ELEMENTS)
        self.affinite_de_effort = False  # augmente les degats des attaques physique DONE
        if "Affinitée Physique" in Player.talents_possedes:
            self.affinite_de_effort = True
        self.peau_de_fer = False  # feu s'éteint 50% + rapidement DONE
        if "Peau de Fer" in Player.talents_possedes:
            self.peau_de_fer = True
        self.bluff = (
            False  # reflete degat pdt 1 tour. si ennemi n'attaque pas, paralysie 1 tour DONE
        )
        if "Bluff" in Player.talents_possedes:
            self.bluff = (
                True  # reflete degat pdt 1 tour. si ennemi n'attaque pas, paralysie 1 tour DONE
            )
        self.connaissance = False  # les sorts coutent moins cher en mana DONE
        if "Connaissance" in Player.talents_possedes:
            self.connaissance = True
        self.carte_du_gout = False  # objets rendent plus de mana/hp DONE
        if "Carte du Gout" in Player.talents_possedes:
            self.carte_du_gout = True
        self.reflex = False  # 75% commencer un combat avec une attaque legere [x] DONE
        if "Réflex" in Player.talents_possedes:
            self.reflex = True
        self.oeuil_magique = (
            False  # chance de rater un sort/2 , 5% rajouter effet elementaire au pif a chaque attaque DONE
        )
        if "Oeuil Magique" in Player.talents_possedes:
            self.oeuil_magique = (
                True  # chance de rater un sort/2 , 5% rajouter effet elementaire au pif a chaque attaque DONE
            )

        # SANG (GETS HEALTH BACK)
        self.affinite_du_sang = False  # augmente les degats des attaques de sang DONE
        if "Affinitée de Sang" in Player.talents_possedes:
            self.affinite_du_sang = True
        self.nectar = False  # attaques et sorts rendent plus de pv DONE
        if "Nectar" in Player.talents_possedes:
            self.nectar = True
        self.anemie = False  # 10% de geler un ennemi a qui on prend de la vie DONE
        if "Anémie" in Player.talents_possedes:
            self.anemie = True
        self.baron_rouge = False  # 25% chance de voler du mana en plus de pv DONE
        if "Baron Rouge" in Player.talents_possedes:
            self.baron_rouge = True
        self.suroxygenation = (
            False  # premiere attaque du combat fait 200% de degats en plus DONE
        )
        if "Suroxygénation" in Player.talents_possedes:
            self.suroxygenation = (
                True  # premiere attaque du combat fait 200% de degats en plus DONE
            )
        self.conditions_limites = (
            False  # hp entre 0 et 5% de hp max = vole 25% de la vie du monstre sauf boss DONE
        )
        if "Conditions Limites" in Player.talents_possedes:
            self.conditions_limites = (
                True  # hp entre 0 et 5% de hp max = vole 25% de la vie du monstre sauf boss DONE
            )
        self.anticoagulants = (
            False  # atttaques et sorts de sang font 25% dgt en plus si vole vie DONE
        )
        if "Anticoagulants" in Player.talents_possedes:
            self.anticoagulants = (
                True  # atttaques et sorts de sang font 25% dgt en plus si vole vie DONE
            )

        # AME (KILLS = DMG)
        self.pira = (
            False  # bô de feu 5 kill = attk +1  10kill =brule +5% /technique a rajouter DONE
        )
        if "Pira" in Player.talents_possedes:
            self.pira = (
                True  # bô de feu 5 kill = attk +1  10kill =brule +5% /technique a rajouter DONE
            )
        self.elektron = False  # lance de foudre 5 kill = attk +1  10kill =paralysie +2% /technique a rajouter DONE
        if "Elektron" in Player.talents_possedes:
            self.elektron = True
        self.tsumeta_sa = False  # katana de glace 5 kill = attk +1  10kill =gele +3% /technique a rajouter DONE
        if "Tsumeta-Sa" in Player.talents_possedes:
            self.tsumeta_sa = True
        self.mathair = False  # corne de terre 5 kill = attk +1  10kill =lapide +3% /technique a rajouter DONE
        if "Mathair" in Player.talents_possedes:
            self.mathair = True
        self.fos = False  # gant physique 3 kill = attk +1   /technique a rajouter DONE
        if "Fos" in Player.talents_possedes:
            self.fos = True
        self.haddee = False  # dague de sang 5 kill = attk +1  10kill =volevie +3% /technique a rajouter DONE
        if "Haddee" in Player.talents_possedes:
            self.haddee = True

        # FUSION (WHEN ATTRIBUTES COALESCE)
        self.oeuil_de_feu = False  # Sorts de feu ne ratent plus DONE
        if "Oculus Ignis" in Player.talents_possedes:
            self.oeuil_de_feu = True
        self.oeuil_de_foudre = False  # Sorts de foudre ne ratent plus DONE
        if "Oculus de Caelo" in Player.talents_possedes:
            self.oeuil_de_foudre = True
        self.oeuil_de_glace = False  # Sorts de glace ne ratent plus DONE
        if "Oculus Glacies" in Player.talents_possedes:
            self.oeuil_de_glace = True 
        self.oeuil_de_physique = False  # Sorts physiques ne ratent plus DONE
        if "Corporalis Oculus" in Player.talents_possedes:
            self.oeuil_de_physique = True
        self.oeuil_de_sang = False  # Sorts de sang ne ratent plus DONE
        if "Sanguis Oculus" in Player.talents_possedes:
            self.oeuil_de_sang = True
        self.oeuil_de_terre = False  # Sorts de terre ne ratent plus DONE
        if "Oculus Terrae" in Player.talents_possedes:
            self.oeuil_de_terre = True
        self.avalanche = False  # Gele 3t et inflige de gros degats. cout en mana massif /sort a rajouter DONE
        if "Avalanche" in Player.talents_possedes:
            self.avalanche = True
        self.metamorphose = False  # invincible pendant les 2 premiers tours du combat DONE
        if "Metamorphosis" in Player.talents_possedes:
            self.metamorphose = True
        self.bougie_magique = (
            False  # ennemi qui se dé-enflamme a 15% chance de se re-enflammer 1 t DONE
        )
        if "Bougie Magique" in Player.talents_possedes:
            self.bougie_magique = (
                True  # ennemi qui se dé-enflamme a 15% chance de se re-enflammer 1 t DONE
            )
        self.ultra_instinct = (
            False  # commence le combat par une attaque physique aléatoire DONE
        )
        if "Ultra-Instinct" in Player.talents_possedes:
            self.ultra_instinct = (
                True  # commence le combat par une attaque physique aléatoire DONE
            )
        self.rejuvenation = (
            False  # 2% de chance de repdrendre 20% de vie max a chaque tour DONE
        )
        if "Réjuvénation" in Player.talents_possedes:
            self.rejuvenation = (
                True  # 2% de chance de repdrendre 20% de vie max a chaque tour DONE
            )
        self.benediction_du_mana = False  # reprend mana au debut de chaque tours DONE
        self.malediction_du_mana = (
            False  # degat des sorts x1.25, prend 3% de vie a chaque lancer de sort DONE
        )
        if "Elémento-Réceptif" in Player.talents_possedes:
            self.benediction_du_mana = True  # reprend mana au debut de chaque tours DONE
            self.malediction_du_mana = (
                True  # degat des sorts x1.25, prend 3% de vie a chaque lancer de sort DONE
            )
        self.maitre_du_mana = False  # 3% de mana max recup a chaque tour DONE
        if "Maitre du Mana" in Player.talents_possedes:
            self.maitre_du_mana = True
        self.pandemonium = False  # ennemi paralysé, enflammé, gelé, lapidé, drainé de sa vie au debut de chaquescombats DONE
        if "Grand Pandémonium Elémentaire" in Player.talents_possedes:
            self.pandemonium = True
        self.liberation_de_feu = (
            False  # enflamme l'ennemi pendant 5 tours /sort a rajouter DONE
        )
        if "Libération de Feu" in Player.talents_possedes:
            self.liberation_de_feu = (
                True  # enflamme l'ennemi pendant 5 tours /sort a rajouter DONE
            )
        self.liberation_de_foudre = (
            False  # paralyse l'ennemi pendant 2 tours /sort a rajouter DONE
        )
        if "Libération de Foudre" in Player.talents_possedes:
            self.liberation_de_foudre = (
                True  # paralyse l'ennemi pendant 2 tours /sort a rajouter DONE
            )
        self.liberation_de_glace = (
            False  # gele l'ennemi pendant 5 tours /sort a rajouter DONE
        )
        if "Libération de Glace" in Player.talents_possedes:
            self.liberation_de_glace = (
                True  # gele l'ennemi pendant 5 tours /sort a rajouter DONE
            )
        self.liberation_de_physique = (
            False  # fait entre 7 et 77 points de degats /technique a rajouter DONE
        )
        if "Libération Physique" in Player.talents_possedes:
            self.liberation_de_physique = (
                True  # fait entre 7 et 77 points de degats /technique a rajouter DONE
            )
        self.liberation_de_sang = (
            False  # draine 20% de sa vie max sur 5 tours /sort a rajouter DONE
        )
        if "Libération de Sang" in Player.talents_possedes:
            self.liberation_de_sang = (
                True  # draine 20% de sa vie max sur 5 tours /sort a rajouter DONE
            )
        self.liberation_de_terre = False  # effectue de gros degats /sort a rajouter DONE
        if "Libération de Terre" in Player.talents_possedes:
            self.liberation_de_terre = True
        # ATTAQUE

        # intialisation
        self.techniques = []
        techniques_supplementaires = []
        self.sorts = []
        sorts_supplementaires = []
        self.items = {}

        #OLD (je supprime pas... au cas ou.)
        self.mirroir_eau = True  # renvoie degats
        self.brume_de_sang = True  # transforme degat en vie
        self.explosion_de_feu = True  # gros dégats et en feu
        self.carrousel = True  # tout les elements dans sa tronche
        self.combo_electrique = True  # suite d'attaques pouvant paralyser
        self.position_du_massif = True  # attaque ennemie ne fait pas plus de 5% vie max
        self.pousse_adrenaline = True  # degat x2 pendant 2 tours, puis paralysie
        self.iaido = True  # 2 tours de preparation, un coup donnant d'immense degats. 10% de kill sauf boss

        #
        #  glossaire de techniques
        self.techniques_de_ame = [
            "Pira",
            "Elektron",
            "Tsumeta-Sa",
            "Mathaïr",
            "Fos",
            "Haddee",
        ]
        self.techniques_de_foudre = [
            "Lance Rapide",
            "Lance Statique",
            "Lance Electrique",
            "Lance de l'Eclair",
            "Lance Foudroyante", 
            "Lance de la Mort Blanche",
        ]

        self.techniques_de_feu = [
            "Bô Chaud", #
            "Bô Brulant", #
            "Bô Enflammé", #
            "Bô de la Fournaise",
            "Bô Magmatique",
            "Bô Solaire",
        ]

        self.techniques_de_glace = [
            "Katana Bleu",
            "Katana Froid",
            "Katana Givré",
            "Katana Glacial",
            "Katana Polaire",
            "Katana Zéro",
        ]

        self.techniques_de_terre = [
            "Corne Argile", #
            "Corne Lapis", #
            "Corne Granite", #
            "Corne Obsidienne",
            "Corne de la Montagne",
            "Corne Continentale",
        ]

        self.techniques_de_physique = [
            "Attaque Légère",
            "Poing Léger", #
            "Poing Renforcé", #
            "Poing Lourd", #
            "Poing Maitrisé", #
            "Poing Fatal", #
            "Poing de la Comète",
        ]

        self.techniques_de_sang = [
            "Dague Volevie",
            "Dague Siphoneuse",
            "Dague Vampirique",
            "Dague Parasite",
            "Dague Destructrice",
            "Dague Créatrice",
        ]
        self.annuaire_de_cout_des_techniques = {
            "Griffes du Démon": 66,
            "Attaque Légère": 5,
            "Pira": 25,
            "Elektron": 25,
            "Tsumeta-Sa": 25,
            "Mathaïr": 25,
            "Fos": 25,
            "Haddee": 25,
            "Lance Rapide": 8,
            "Lance Statique": 12,
            "Lance Electrique": 15,
            "Lance de l'Eclair": 17,
            "Lance Foudroyante": 20, 
            "Lance de la Mort Blanche": 25,
            "Bô Chaud": 8, #
            "Bô Brulant": 12, #
            "Bô Enflammé": 15, #
            "Bô de la Fournaise": 17,
            "Bô Magmatique": 20,
            "Bô Solaire": 25,
            "Katana Bleu": 8,
            "Katana Froid": 12,
            "Katana Givré": 15,
            "Katana Glacial": 17,
            "Katana Polaire": 20,
            "Katana Zéro": 25,
            "Corne Argile": 8, #
            "Corne Lapis": 12, #
            "Corne Granite": 15, #
            "Corne Obsidienne": 17,
            "Corne de la Montagne": 20,
            "Corne Continentale": 25,
            "Poing Léger": 8, #
            "Poing Renforcé": 12, #
            "Poing Lourd": 15, #
            "Poing Maitrisé": 17, #
            "Poing Fatal": 20, #
            "Poing de la Comète": 25,
            "Dague Volevie": 8,
            "Dague Siphoneuse": 12,
            "Dague Vampirique": 15,
            "Dague Parasite": 17,
            "Dague Destructrice": 20,
            "Dague Créatrice": 25,
            "Posture de la Montagne": 15,
            "Libération Physique": 25,
            "Bluff": 15,
            "Combo Electrique": 18,
            "Position du Massif": 10,
            "Poussée d'Adrénaline": 30,
            "Iaido": 30,
        }
        # %touche, degat, %crit, degat crit, %element, description, message si rate, si touche, si touche crit, nombre tours, effet element
        self.annuaire_de_caracteristique_des_techniques = {
            "Attaque Légère": [95, 7, 30, 4, 0, "Vous frappez l'ennemi avec peu de force, mais beaucoup de précision...", 
                               "...ce qui ne vous empeche pas de rater quand meme.", "..et le faites grimacer de douleur !", 
                               "et le faites reculer de plusieurs pas en arrière !!", 0, 0],
            "Lance Rapide": [80, 10, 20, 6, 8, 
                             "Vous concentrez de l'énergie dans votre lance et...", 
                             "...donnez un coup dans le vide.", 
                             "...touchez l'ennemi !", 
                             "...embrochez l'ennemi !!", 1, 0],
            "Lance Statique": [78, 18, 20, 8, 10, 
                               "Vous chargez quelques volts dans votre lance et...", 
                               "...la lachez sous le coup du choc statique.", 
                               "...frappez l'ennemi !", 
                               "...embrochez l'ennemi !!", 1, 0],
            "Lance Electrique": [76, 27, 18, 8, 8, 
                                 "Vous chargez votre lance en électricitée et...", 
                                 "...trébuchez sur un caillou.", 
                                 "...transpercez l'ennemi !", 
                                 "...embrochez l'ennemi a haute vitesse !!", 2, 0],
            "Lance de l'Eclair": [74, 36, 16, 11, 10, 
                                  "Vous impregnez votre lance avec un haut voltage et...", 
                                  "...vos muscles contractés vous empêchent d'attaquer.", 
                                  "...donnez un grand coup transversal sur l'ennemi !", 
                                  "...embrochez l'ennemi sans qu'il n'aie le temps de réagir !", 2, 0],
            "Lance Foudroyante": [72, 45, 15, 11, 8, 
                                  "Vous rassemblez les ions de l'air au bout de votre lance et touchez l'ennemi...", 
                                  "...sans effet.", 
                                  "...ce qui invoque la foudre sur sa position !", 
                                  "...ce qui invoque une avalanche de foudre sur sa position !!", 3, 0],
            "Lance de la Mort Blanche": [70, 52, 15, 13, 10,
                                         "Vous chargez des millions de zettavolts dans la pointe de votre lance avant de l'envoyer...",
                                         "...et manquez de peu le torse du monstre .",
                                         "...et brisez la jambe du monstre !",
                                         "...et embrochez violemment le corps du monstre !!",
                                         3,
                                         0],
            "Bô Chaud": [80, 10, 20, 5, 15, 
                         "Vous balancez votre bô enflammé vers l'ennemi...", 
                         "...mais votre élan est brisé alors que vous trébuchez.", 
                         "...et votre coup frappe l'ennemi avec une puissance ardente !", 
                         "...et votre coup brûlant traverse l'ennemi avec une force dévastatrice !!", 3, 7],
            "Bô Brulant": [78, 18, 20, 8, 15, 
                           "Vous plongez dans le combat avec votre bô enflammé...", 
                           "...mais votre bô glisse de vos mains et tombe au sol.", 
                           "...et votre coup atteint l'ennemi, le faisant reculer avec une chaleur intense !", 
                           "...et votre attaque brule l'ennemi dans un tourbillon de braises !!", 4, 7],
            "Bô Enflammé": [76, 27, 20, 8, 17, 
                            "Vous sentez la chaleur émanant de votre bô enflammé alors que vous vous préparez à attaquer...", 
                            "...mais votre coup manque l'ennemi de justesse.", 
                            "...et votre bô frappe l'ennemi, laissant derrière lui une traînée de flammes !", 
                            "...et votre attaque enflamme l'ennemi, le laissant brûler dans une douleur intense !!", 4, 6],
            "Bô de la Fournaise": [74, 36, 20, 10, 17, 
                                   "Vous brandissez votre bô enflammé, illuminant l'arène...", 
                                   "...mais votre bô se coince dans un obstacle, retardant votre attaque.", 
                                   "...et votre coup de bô enflammé percute l'ennemi, le laissant brûlant de douleur !", 
                                   "...et votre attaque engloutit l'ennemi dans un torrent de flammes infernales !!", 4, 6],
            "Bô Magmatique": [72, 45, 20, 10, 19, 
                              "Les volutes de magma s'échappent de votre bô alors que vous vous préparez à l'attaquer...", 
                              "...mais votre coup est esquivé par l'ennemi agile.", 
                              "...et votre bô enflammé frappe l'ennemi avec une force titanesque, le faisant vaciller sous l'impact !", 
                              "...et votre attaque engloutit l'ennemi dans un enfer liquide de magma en fusion !!", 4, 5],
            "Bô Solaire": [70, 52, 20, 12, 19, 
                           "Vous levez votre bô vers le ciel, invoquant les flammes du soleil pour l'envelopper...", 
                           "...mais votre attaque est repoussée par une énergie opposée.", 
                           "...et votre bô enflammé réduit l'ennemi en cendres dans une explosion solaire !", 
                           "...et votre attaque solaire consume l'ennemi dans une déferlante de flammes solaires, ne laissant derrière elle que des cendres !!", 5, 5],
            "Katana Bleu": [80, 10, 20, 9, 15, 
                            "Vous maniez votre katana avec une agilité impressionnante, canalisant l'énergie du vent glacé à travers sa lame acérée...", 
                            "...mais votre coup est paré par l'ennemi avec une précision redoutable, l'énergie bleutée du vent se dissipant dans l'air.", 
                            "...et votre katana pénètre la défense de l'ennemi avec une efficacité foudroyante, irradiant une aura glaciale au moment de l'impact !", 
                            "...et votre coup critique tranche l'ennemi avec une vitesse surprenante, libérant une explosion de givre qui enveloppe le champ de bataille !!", 3, 0],
            "Katana Froid": [78, 18, 20, 9, 15, 
                             "Vous sentez le froid glacial émanant de votre katana alors que vous l'apprêtez à l'attaque...", 
                             "...mais votre coup manque l'ennemi de justesse, se perdant dans le vent.", 
                             "...et votre katana transperce l'ennemi avec une froideur saisissante, laissant derrière lui une brume glaciale !", 
                             "...et votre coup critique gèle l'ennemi dans un bloc de glace, le laissant impuissant !!", 3, 0],
            "Katana Givré": [76, 27, 20, 9, 17, 
                             "Vous plongez dans la mêlée avec votre katana givré, prêt à défier le froid de l'adversité...", 
                             "...mais votre attaque est déviée par l'ennemi, glissant alors hors de portée.", 
                             "...et votre katana tranche l'ennemi avec une efficacité glaciale, lui infligeant des dommages profonds !", 
                             "...et votre attaque engloutit l'ennemi dans un torrent de glace, l'emportant contre les murs de l'arène !!", 3, 0],
            "Katana Glacial": [74, 36, 20, 9, 17, 
                               "Vous canalisez le pouvoir de la glace dans votre katana, le couvrant de cristaux gelés...", 
                               "...mais votre attaque est repoussée par l'ennemi, la glace se brisant sur son armure.",
                               "...et votre katana découpe l'ennemi avec une précision glaciale, le laissant frissonner sous l'impact !", 
                               "...et votre coup critique gèle instantanément l'ennemi dans une sculpture de glace, le figeant dans sa douleur !!", 4, 0],
            "Katana Polaire": [72, 45, 20, 9, 19, 
                               "Vous invoquez le pouvoir polaire dans votre katana, le recouvrant d'une lueur bleue arctique...", 
                               "...mais votre coup est esquivé par l'ennemi agile, glissant entre ses doigts gelés.", 
                               "...et il transperce l'ennemi avec une force polaire, le laissant frissonner sous l'effet du froid !", 
                               "...et le coup critique congèle l'ennemi dans un blizzard infini, le laissant pris au piège dans un vortex de glace !!", 4, 0],
            "Katana Zéro": [70, 52, 20, 9, 19, 
                            "Vous érigez un mur de glace devant vous avant de faire jaillir votre katana dans un éclair de lumière, invoquant le gel absolu pour consumer vos ennemis...", 
                            "...mais votre attaque est bloquée par l'ennemi avec une résistance glaciale, l'énergie glacée du zéro absolu se dissipant dans l'air.", 
                            "...et votre katana tranche l'ennemi avec une puissance dévastatrice, brisant sa défense, tandis que le froid absolu envahit son corps !", 
                            "...et votre coup critique engloutit l'ennemi dans une tempête de neige aveuglante, le laissant désorienté et impuissant, "
                            "alors que le gel absolu s'abat avec une fureur dévastatrice !!", 4, 0],
            "Corne Argile": [80, 10, 10, 13, 10, 
                             "Vous brandissez votre corne d'argile avec une force imposante, invoquant la terre pour écraser vos ennemis...",
                              "...mais votre attaque est repoussée par l'ennemi, l'énergie terrestre se dissipant dans l'air.",
                              "...et votre corne écrase l'ennemi avec une puissance tellurique, secouant le sol sous son impact !",
                              "...et votre coup critique fracasse l'ennemi dans un tremblement de terre dévastateur, ébranlant les fondations du colisée !!",
                              0, 65],
            "Corne Lapis": [78, 18, 10, 15, 10, 
                            "Vous invoquez la force des gemmes précieuses dans votre corne de lapis, illuminant le champ de bataille de leur éclat...",
                                        "...mais votre attaque est parée par l'ennemi, l'énergie cristalline se dissipant dans l'air.",
                                        "...et votre corne perce l'ennemi avec une précision brillante, étincelant de lumière au moment de l'impact !",
                                        "...et votre coup critique étourdit l'ennemi avec une explosion de lumière éblouissante, le laissant vulnérable à vos attaques suivantes !!",
                                        0, 75],
            "Corne Granite": [76, 27, 10, 17, 12, 
                              "Vous chargez votre corne de granite avec une résolution inébranlable, prêt à broyer vos ennemis sous son poids...",
                                        "...mais votre attaque est esquivée par l'ennemi, l'énergie rocheuse se dissipant dans l'air.",
                                        "...et votre corne écrase l'ennemi avec une force minérale, créant des fissures dans son armure !",
                                        "...et votre coup critique pulvérise l'ennemi dans une explosion de roche, projetant des éclats mortels dans toutes les directions !!",
                                        0, 85],
            "Corne Obsidienne": [74, 36, 10, 19, 12, 
                                 "Vous maniez votre corne d'obsidienne avec une férocité implacable, invoquant les ténèbres pour dévorer vos ennemis...",
                                        "...mais votre attaque est contrée par l'ennemi, l'énergie ténébreuse se dissipant dans l'air.",
                                        "...et votre corne transperce l'ennemi avec une brutalité sombre, obscurcissant leur vision au moment de l'impact !",
                                        "...et votre coup critique déchire l'ennemi dans une explosion de ténèbres, plongeant le champ de bataille dans un abîme de désespoir !!",
                                        0, 95],
            "Corne de la Montagne": [74, 45, 10, 19, 14, 
                                     "Vous brandissez votre corne de la montagne avec une force titanesque, évoquant la puissance des sommets pour anéantir vos ennemis...",
                                        "...mais votre attaque est déviée par l'ennemi, l'énergie majestueuse de la montagne se dissipant dans l'air.",
                                        "...et votre corne broie l'ennemi avec une puissance monumentale, faisant trembler le sol sous son poids !",
                                        "...et votre coup critique écrase l'ennemi dans un cataclysme montagneux, déclenchant une avalanche de destruction !!",
                                        0, 100],
            "Corne Continentale": [70, 52, 10, 23, 16, 
                                   "Vous invoquez la force ancestrale de la terre dans votre corne continentale, prêt à écraser toute opposition sous le poids des siècles...",
                                        "...mais votre attaque est esquivée par l'ennemi, l'énergie immuable du continent se dissipant dans l'air.",
                                        "...et votre corne écrase l'ennemi avec une force implacable, marquant le champ de bataille de votre empreinte !",
                                        "...et votre coup critique brise l'ennemi dans un cataclysme sismique, fissurant le sol et engloutissant tout sur son passage !!",
                                        0, 110],
            "Poing Léger": [80, 10, 50, 7, 0, 
                            "Vous lancez votre poing avec une agilité impressionnante, frappant l'ennemi avec la vitesse d'un éclair...",
                              "...mais votre coup est esquivé par l'ennemi, votre poing glissant dans le vide.",
                              "...et votre poing frappe l'ennemi avec une précision fulgurante, déclenchant une onde de choc !",
                              "...et votre coup critique pulvérise l'ennemi dans un tourbillon de coups rapides !!",
                              0, 0],
            "Poing Renforcé": [78, 18, 50, 7, 0, 
                               "Vous chargez votre poing avec une force surhumaine, prêt à briser toute résistance sur votre chemin...",
                                        "...mais votre attaque est parée par l'ennemi, votre poing rebondissant sur leur défense renforcée.",
                                        "...et votre poing frappe l'ennemi avec une puissance dévastatrice, créant des fissures dans leur armure !",
                                        "...et votre coup critique déchaîne une tempête de coups dévastateurs, réduisant l'ennemi en miettes !!",
                                        0, 0],
            "Poing Lourd": [76, 27, 50, 7, 0, 
                            "Vous abattez votre poing avec une force brutale, déterminé à anéantir tout sur votre passage...",
                                        "...mais votre attaque est esquivée de justesse par l'ennemi, votre poing fracassant le sol.",
                                        "...et votre poing écrase l'ennemi avec une puissance titanesque, créant un cratère à l'impact !",
                                        "...et votre coup critique frappe l'ennemi comme un coup de massue, les projetant loin avec une force irrésistible !!",
                                        0, 0],
            "Poing Maitrisé": [74, 36, 50, 8, 0, 
                               "Vous canalisez votre énergie dans votre poing avec une précision impeccable, prêt à frapper là où ça fait mal...",
                                        "...mais votre coup est paré par l'ennemi avec une habileté remarquable, votre poing stoppé dans son élan.",
                                        "...et votre poing percute l'ennemi avec une précision chirurgicale, ciblant leurs points faibles !",
                                        "...et votre coup critique atteint une harmonie parfaite de puissance et de précision, infligeant des dégâts massifs avec une grâce mortelle !!",
                                        0, 0],
            "Poing Fatal": [72, 45, 50, 8, 0, 
                            "Vous déchaînez votre poing avec une rage incontrôlable, prêt à réduire vos ennemis en poussière...",
                                        "...mais votre attaque est déviée par l'ennemi avec une résolution implacable, votre poing s'écrasant dans le vide.",
                                        "...et votre poing frappe l'ennemi avec une force destructrice, pulvérisant tout sur son passage !",
                                        "...et votre coup critique anéantit l'ennemi dans une explosion de puissance brute, laissant un désert de destruction dans son sillage !!",
                                        0, 0],
            "Poing de la Comète": [70, 52, 50, 10, 0, 
                                   "Vous lancez votre poing comme une comète enflammée, déterminé à réduire vos ennemis en cendres...",
                                        "...mais votre attaque est contrée par l'ennemi avec une adresse remarquable, votre poing frôlant leur défense.",
                                        "...et votre poing frappe l'ennemi avec une vélocité incandescente, créant une traînée de feu dans son sillage !",
                                        "...et votre coup critique s'abat sur l'ennemi comme un cataclysme céleste, dévastant tout sur son passage !!",
                                        0, 0],
            "Dague Volevie": [80, 8, 15, 10, 30, "Vous maniez votre dague avec une grâce aérienne, prêt à voler la vie de vos ennemis...",
                              "...mais votre attaque est esquivée par l'ennemi avec une agilité surprenante, votre lame passant à travers l'air.",
                              "...et votre dague tranche l'ennemi avec une fluidité mortelle, aspirant leur énergie vitale !",
                              "...et votre coup critique déchire l'ennemi dans une frénésie de coups rapides, drainant leur force vitale et les laissant exsangues !",
                              0, 5],
            "Dague Siphoneuse": [78, 15, 15, 10, 25, "Vous imprégnez votre dague d'une soif insatiable, prête à siphonner la force de vos ennemis...",
                                        "...mais votre attaque est parée par l'ennemi avec une résistance farouche, votre lame déviée de sa trajectoire.",
                                        "...et votre dague absorbe la force de l'ennemi avec voracité, vous revitalisant à chaque coup !",
                                        "...et votre coup critique aspire l'essence même de l'ennemi, les laissant affaiblis et épuisés !",
                                        0, 5],
            "Dague Vampirique": [76, 24, 15, 10, 25, "Vous imprégnez votre dague d'une soif de sang vorace, prête à sucer la vie de vos ennemis...",
                                        "...mais votre attaque est esquivée par l'ennemi avec une adresse déconcertante, votre lame tranchant l'air.",
                                        "...et votre dague transperce l'ennemi avec une férocité vampirique, aspirant leur sang !",
                                        "...et votre coup critique déchire l'ennemi dans un festin de sang, vous régénérant avec chaque goutte versée !",
                                        0, 4],
            "Dague Parasite": [74, 33, 15, 11, 20, "Vous infectez votre dague d'une malice rampante, prête à parasiter les forces de vos ennemis...",
                                        "...mais votre attaque est contrée par l'ennemi avec une vigilance impitoyable, votre lame repoussée par leur volonté.",
                                        "...et votre dague infeste l'ennemi de venin insidieux, affaiblissant leur résistance !",
                                        "...et votre coup critique propage la corruption à travers l'ennemi, les réduisant à un état de décrépitude totale !",
                                        0, 4],
            "Dague Destructrice": [72, 42, 15, 11, 20, "Vous brandissez votre dague avec une férocité destructrice, prêt à anéantir toute opposition sur votre chemin...",
                                        "...mais votre attaque est parée par l'ennemi avec une détermination impitoyable, votre lame détournée de son objectif.",
                                        "...et votre dague déchire l'ennemi avec une force explosive, laissant derriere elle un sillage de sang aussitot absorbé !",
                                        "...et votre coup critique détruit les défenses de l'ennemi, laissant sa vitalité se faire absorber par le métal vorace !",
                                        0, 3],
            "Dague Créatrice": [70, 49, 15, 12, 15, "Vous maniez votre dague avec une habileté créative, prête à façonner le destin de vos ennemis...",
                                        "...mais votre attaque est esquivée par l'ennemi avec une ruse éclairée, votre lame glissant à côté de sa cible.",
                                        "...et votre dague sculpte l'ennemi avec une précision artistique, infligeant de grandes blessures !",
                                        "...et votre coup critique forge une destinée inéluctable pour l'ennemi, les condamnant à chuter pour votre réussite !",
                                        0, 3],
        }

        # glossaire des techniques supplementaires
        if self.rigueur:
            techniques_supplementaires.append("Posture de la Montagne")
        if self.pira:
            techniques_supplementaires.append("Pira")
        if self.elektron:
            techniques_supplementaires.append("Elektron")
        if self.tsumeta_sa:
            techniques_supplementaires.append("Tsumeta-Sa")
        if self.mathair:
            techniques_supplementaires.append("Mathaïr")
        if self.fos:
            techniques_supplementaires.append("Fos")
        if self.haddee:
            techniques_supplementaires.append("Haddee")
        if self.liberation_de_physique:
            techniques_supplementaires.append("Libération Physique")
        if self.bluff:
            techniques_supplementaires.append("Bluff")
        if self.combo_electrique:
            techniques_supplementaires.append("Combo Electrique")
        if self.position_du_massif:
            techniques_supplementaires.append("Position du Massif")
        if self.pousse_adrenaline:
            techniques_supplementaires.append("Poussée d'Adrénaline")
        if self.iaido:
            techniques_supplementaires.append("Iaido")

        # ajout des techniques a la liste techniques
        if BuildABear:
            for attaque in self.techniques_de_foudre:
                self.techniques.append(attaque)
            for attaque in self.techniques_de_feu:
                self.techniques.append(attaque)
            for attaque in self.techniques_de_glace:
                self.techniques.append(attaque)
            for attaque in self.techniques_de_terre:
                self.techniques.append(attaque)
            for attaque in self.techniques_de_physique:
                self.techniques.append(attaque)
            for attaque in self.techniques_de_sang:
                self.techniques.append(attaque)
            if len(techniques_supplementaires) > 0:
                for attaque in techniques_supplementaires:
                    self.techniques.append(attaque)
        else:
            for technique in Player.techniques_possedes:
                self.techniques.append(technique)

        # glossaire de sorts
        self.sorts_de_foudre = [
            "Faisceau Rapide",
            "Faisceau Statique",
            "Faisceau Electrique",
            "Faisceau de l'Eclair",
            "Faisceau Foudroyant",
            "Faisceau de la Mort Blanche",
        ]

        self.sorts_de_feu = [
            "Thermosphère Chaude",
            "Thermosphère Brulante",
            "Thermosphère Enflammée",
            "Thermosphère de la Fournaise",
            "Thermosphère Magmatique",
            "Thermosphère Solaire",
        ]

        self.sorts_de_glace = [
            "Pic Bleu",
            "Pic Froid",
            "Pic Givré",
            "Pic Glacial",
            "Pic Polaire",
            "Pic Zéro",
        ]

        self.sorts_de_terre = [
            "Création d'Argile",
            "Création de Lapis",
            "Création de Granite",
            "Création Obsidienne",
            "Création de la Montagne",
            "Création Continentale",
        ]

        self.sorts_de_physique = [
            "Explosion Légère",
            "Explosion Renforcée",
            "Explosion Lourde",
            "Explosion Maitrisée",
            "Explosion Fatale",
            "Explosion de la Comète",
        ]

        self.sorts_de_sang = [
            "Dance Volevie",
            "Dance Siphoneuse",
            "Dance Vampirique",
            "Dance Parasite",
            "Dance Destructrice",
            "Dance Créatrice",
        ]

        self.sorts_de_soin = [
            "Sonata Pitoyable", #3% ou 8pv
            "Sonata Miséricordieuse", #5% ou 15pv
            "Sonata Empathique", #12% ou 20pv
            "Sonata Sincère", #17% ou 25pv
            "Sonata Bienveillante", #20% ou 33pv
            "Sonata Absolutrice", #25% ou 40pv
        ]
        self.annuaire_de_pourcentage_de_soin_des_sorts = {
            "Sonata Pitoyable": 3 + (self.points_de_intelligence // 2),
            "Sonata Miséricordieuse": 5 + (self.points_de_intelligence // 2),
            "Sonata Empathique": 12 + (self.points_de_intelligence // 2),
            "Sonata Sincère": 17 + (self.points_de_intelligence // 2),
            "Sonata Bienveillante": 20 + (self.points_de_intelligence // 2),
            "Sonata Absolutrice": 25 + (self.points_de_intelligence // 2)
        }
        self.annuaire_de_soin_minimum_des_sorts = {
            "Sonata Pitoyable": 15 + (self.points_de_intelligence),
            "Sonata Miséricordieuse": 27 + (self.points_de_intelligence),
            "Sonata Empathique": 40 + (self.points_de_intelligence),
            "Sonata Sincère": 53 + (self.points_de_intelligence // 2),
            "Sonata Bienveillante": 66 + (self.points_de_intelligence // 2),
            "Sonata Absolutrice": 78 + (self.points_de_intelligence // 2)
        }
        self.annuaire_de_description_des_sorts_de_soin = {
            "Sonata Pitoyable": "Un bruit pathétique vous enveloppe et apaise la douleur de vos blessures.",
            "Sonata Miséricordieuse": "Un son a peine apréciable se plaque contre votre peau et referme vos blessures.",
            "Sonata Empathique": "Une musique potable soulage votre âme et vos blessures.",
            "Sonata Sincère": "Un chant cristallin inspire votre esprit et revigore votre corps.",
            "Sonata Bienveillante": "Une chorale glorieuse vous fait oublier les problèmes de votre situation et cicatrise vos blessures.",
            "Sonata Absolutrice": "Une mélodie féerique ramène votre être tout entier a un état optimal."
        }
        # %touche, degat, %crit, degat crit, %element, description, message si rate, si touche, si touche crit, nombre tours, effet element
        self.annuaire_de_caracteristique_des_sorts = {
            "Tir Arcanique": [95, 10, 30, 4, 0, 
                              "Vous faites un signe de pistolet avec vos doigts...", 
                              "...mais cela n'impressionne pas l'ennemi.", 
                              "...et faites sortir une boule de mana qui vient s'écraser sur l'ennemi !", 
                              "...en faites sortir une dizaine de petites boules de mana qui viennent projeter l'ennemi en arrière !!", 0, 0],
            "Faisceau Rapide": [90, 14, 20, 2, 8, "Vous lancez un faisceau d'énergie avec une rapidité fulgurante, illuminant le champ de bataille...",
                              "...mais votre sort est dissipé par l'ennemi, l'énergie se dissipant dans l'air.",
                              "...et votre faisceau frappe l'ennemi avec une précision éclair, infligeant des dégâts rapides !",
                              "...et votre faisceau déchire l'ennemi avec une force explosive, le projetant dans les ténèbres !!",
                              1, 0],
            "Faisceau Statique": [88, 22, 20, 4, 10, "Vous chargez votre faisceau d'énergie statique, créant des étincelles d'électricité dans l'air...",
                                        "...mais votre sort est dissipé par l'ennemi, l'énergie statique se dispersant sans effet.",
                                        "...et votre faisceau électrise l'ennemi, créant des arcs d'électricité qui parcourent leur corps !",
                                        "...et votre faisceau critique surcharge l'ennemi, le consumant dans un tourbillon d'éclairs et de foudre !!",
                                        1, 0],
            "Faisceau Electrique": [86, 31, 18, 4, 12, "Vous concentrez une grande quantité d'électricité dans votre faisceau, créant une aura électrique autour de vous...",
                                        "...mais votre sort est contrecarré par l'ennemi, l'énergie électrique se dispersant dans l'air.",
                                        "...et votre faisceau électrocute l'ennemi, les faisant trembler sous la décharge !",
                                        "...et votre faisceau critique électrocute l'ennemi dans une explosion d'électricité, les réduisant en cendres !!",
                                        2, 0],
            "Faisceau de l'Eclair": [84, 40, 16, 7, 14, "Vous invoquez la puissance de la foudre dans votre faisceau, illuminant le ciel avec des éclairs dévastateurs...",
                                        "...mais votre sort est esquivé par l'ennemi avec une agilité surnaturelle, l'éclair s'écrasant dans le sol.",
                                        "...et votre faisceau frappe l'ennemi avec la force de la foudre, les électrocutant sur place !",
                                        "...et votre faisceau critique déchaîne un orage de destruction, frappant l'ennemi avec une force insurmontable !!",
                                        2, 0],
            "Faisceau Foudroyant": [82, 49, 15, 7, 10, "Vous libérez un faisceau d'énergie foudroyante, déchirant le ciel avec un éclair dévastateur...",
                                        "...mais votre sort est paré par l'ennemi, l'énergie foudroyante se dispersant sans effet.",
                                        "...et votre faisceau invoque la foudre sur l'ennemi, les électrocutant avec une intensité terrifiante !",
                                        "...et votre faisceau critique déclenche un cataclysme électrique, dévorant l'ennemi dans un déluge de foudre et de tonnerre !!",
                                        3, 0],
            "Faisceau de la Mort Blanche": [80, 56, 15, 11, 12, "Vous canalisez la puissance de l'éclair dans votre faisceau, illuminant le champ de bataille avec une lueur mortelle...",
                                        "...mais votre sort est dissipé par l'ennemi, l'énergie blanche se dispersant dans l'air.",
                                        "...et votre faisceau éclate sur l'ennemi avec une force surhumaine, les laissant carbonisés et fumants !",
                                        "...et votre faisceau critique déclenche un ouragan de destruction, annihilant tout sur son passage !!",
                                        3, 0],
            "Thermosphère Chaude": [90, 14, 20, 1, 18, "Vous invoquez une vague de chaleur intense, faisant monter la température ambiante dans la thermosphère...",
                              "...mais votre sort est dispersé par l'ennemi, la chaleur se dissipant sans effet.",
                              "...et la thermosphère brûle l'ennemi avec une intensité incandescente, leur infligeant des dégâts ardents !",
                              "...et votre thermosphère déclenche une explosion de chaleur dévastatrice, incinérant l'ennemi dans une fournaise ardente !!",
                              3, 7],
            "Thermosphère Brulante": [88, 22, 20, 4, 18, "Vous créez un tourbillon de flammes autour de l'ennemi, l'enveloppant dans une tempête de feu...",
                                        "...mais votre sort est contré par l'ennemi, les flammes se dissipant dans l'air.",
                                        "...et la thermosphère enflamme l'ennemi avec une furie incandescente, les laissant calcinés et brûlés !",
                                        "...et votre thermosphère critique déclenche une conflagration cataclysmique, réduisant l'ennemi en cendres et en fumée !!",
                                        4, 7],
            "Thermosphère Enflammée": [86, 31, 20, 4, 20, "Vous libérez une explosion de flammes dans la thermosphère, créant une inferno dévastatrice...",
                                        "...mais votre sort est esquivé par l'ennemi, les flammes s'écrasant dans le sol.",
                                        "...et la thermosphère enflamme l'ennemi avec une fureur incendiaire, les consumant dans les flammes !",
                                        "...et votre thermosphère critique déclenche une apocalypse de feu, carbonisant tout sur son passage !!",
                                        4, 6],
            "Thermosphère de la Fournaise": [84, 40, 20, 6, 20, "Vous invoquez le pouvoir de la fournaise dans la thermosphère, créant une incandescence infernale...",
                                        "...mais votre sort est dissipé par l'ennemi, l'incendie se dispersant sans effet.",
                                        "...et la thermosphère engloutit l'ennemi dans un brasier en fusion, les laissant réduits en cendres !",
                                        "...et votre thermosphère critique déclenche un holocauste flamboyant, consumant tout dans un feu purificateur !!",
                                        4, 6],
            "Thermosphère Magmatique": [82, 49, 20, 6, 22, "Vous invoquez la puissance du magma dans la thermosphère, créant des rivières de lave en fusion...",
                                        "...mais votre sort est paré par l'ennemi, la lave se solidifiant avant de pouvoir les toucher.",
                                        "...et la thermosphère baigne l'ennemi dans la lave en fusion, les réduisant à l'état de cendres brûlantes !",
                                        "...et votre thermosphère critique déclenche une éruption cataclysmique, ensevelissant tout dans un océan de feu et de destruction !!",
                                        4, 5],
            "Thermosphère Solaire": [80, 56, 20, 8, 22, "Vous canalisez l'énergie solaire dans la thermosphère, créant une explosion de lumière et de chaleur...",
                                        "...mais votre sort est dissipé par l'ennemi, l'énergie solaire se dissipant dans l'air.",
                                        "...et la thermosphère embrase l'ennemi avec une intensité solaire, les consumant dans les flammes de l'astre roi !",
                                        "...et votre thermosphère critique déclenche une supernova dévastatrice, réduisant tout à néant dans un éclat aveuglant !!",
                                        5, 5],
            "Pic Bleu": [90, 14, 20, 5, 18, "Vous invoquez un pic de glace d'un bleu éclatant, pointant menaçant vers l'ennemi...",
                     "...mais votre sort est esquivé par l'ennemi, le pic de glace se fondant dans l'air.",
                     "...et le pic de glace transperce l'ennemi avec une précision glaciale, leur infligeant des dégâts cinglants !",
                     "...et votre pic de glace critique déchire l'ennemi avec une froideur implacable, les laissant gelés jusqu'à l'âme !!",
                     3, 0],
            "Pic Froid": [88, 22, 20, 5, 18, "Vous créez un pic de glace empreint d'une froideur intense, pointant menaçant vers l'ennemi...",
                                "...mais votre sort est dissipé par l'ennemi, le pic de glace se fondant dans l'air.",
                                "...et le pic de glace gèle l'ennemi avec une fureur glaciale, les laissant engourdis et gelés !",
                                "...et votre pic de glace critique déclenche une tempête de glace dévastatrice, gelant tout sur son passage !!",
                                3, 0],
            "Pic Givré": [86, 31, 20, 5, 20, "Vous invoquez un pic de glace enveloppé d'une aura de froid glacial, pointant menaçant vers l'ennemi...",
                                "...mais votre sort est paré par l'ennemi, le pic de glace se brisant avant de les toucher.",
                                "...et le pic de glace congèle l'ennemi avec une intensité glaciale, les laissant frigorifiés et glacés !",
                                "...et votre pic de glace critique déclenche une tempête blizzard dévastatrice, congelant l'ennemi dans un maelström de glace et de neige !!",
                                3, 0],
            "Pic Glacial": [84, 40, 20, 5, 20, "Vous canalisez le pouvoir de l'hiver dans un pic de glace immense et imposant, pointant menaçant vers l'ennemi...",
                                "...mais votre sort est dissipé par l'ennemi, le pic de glace se brisant avant de les toucher.",
                                "...et le pic de glace glace l'ennemi jusqu'au cœur avec une cruauté glaçante, les laissant pris dans les griffes du froid !",
                                "...et votre pic de glace critique déclenche une tempête de verglas dévastatrice, gelant tout dans un monde de glace éternelle !!",
                                4, 0],
            "Pic Polaire": [82, 49, 20, 5, 22, "Vous invoquez un pic de glace chargé du froid polaire, pointant menaçant vers l'ennemi...",
                                "...mais votre sort est dissipé par l'ennemi, le pic de glace se brisant avant de les toucher.",
                                "...et le pic de glace enveloppe l'ennemi dans une nuit éternelle de froid glacial, les laissant gelés jusqu'à l'âme !",
                                "...et votre pic de glace critique déclenche une apocalypse glaciaire, gelant tout dans un désert de glace sans fin !!",
                                4, 0],
            "Pic Zéro": [80, 56, 20, 5, 22, "Vous libérez un pic de glace d'un froid absolu, pointant menaçant vers l'ennemi...",
                                "...mais votre sort est dissipé par l'ennemi, le pic de glace se brisant avant de les toucher.",
                                "...et le pic de glace congèle l'ennemi dans un hiver éternel, les laissant prisonniers du gel !",
                                "...et votre pic de glace critique déclenche un cataclysme glacial, gelant tout dans un néant de froid absolu !!",
                                4, 0],
            "Création d'Argile": [90, 14, 10, 10, 12, "Vous façonnez de l'argile à partir de l'éther, créant une masse informe de matière molle...",
                          "...mais votre sort est dissipé par l'ennemi, l'argile se dispersant sans effet.",
                          "...et votre création d'argile prend forme, enveloppant l'ennemi dans une prison de boue glaise !",
                          "...et votre création d'argile critique façonne une golem de boue, écrasant l'ennemi sous son poids écrasant !!",
                          0, 60],
            "Création de Lapis": [88, 22, 10, 12, 12, "Vous invoquez des fragments de lapis-lazuli, créant une aura de gemmes étincelantes...",
                                    "...mais votre sort est contrecarré par l'ennemi, les gemmes se dispersant dans l'air.",
                                    "...et votre création de lapis engloutit l'ennemi dans un tourbillon de pierres précieuses, les ensorcelant dans un éclat éblouissant !",
                                    "...et votre création de lapis critique forge un golem de gemmes, pulvérisant l'ennemi avec un torrent de puissance cristalline !!",
                                    0, 65],
            "Création de Granite": [86, 31, 10, 14, 14, "Vous créez des montagnes de granit à partir de l'éther, érigeant des murailles de pierre impénétrable...",
                                        "...mais votre sort est esquivé par l'ennemi, les montagnes de granit s'effondrant avant de les toucher.",
                                        "...et votre création de granite écrase l'ennemi sous un déluge de roches massives, les broyant sous leur poids écrasant !",
                                        "...et votre création de granite critique élève un titan de pierre, écrasant l'ennemi dans une avalanche de destruction !!",
                                        0, 70],
            "Création Obsidienne": [84, 40, 10, 16, 14, "Vous invoquez des flots d'obsidienne en fusion, créant un océan de lave en fusion...",
                                        "...mais votre sort est dissipé par l'ennemi, la lave se solidifiant avant de les toucher.",
                                        "...et votre création d'obsidienne engloutit l'ennemi dans un brasier en fusion, les laissant calcinés et brûlés !",
                                        "...et votre création d'obsidienne critique forge un golem de lave, consumant l'ennemi dans un enfer de feu liquide !!",
                                        0, 80],
            "Création de la Montagne": [82, 49, 10, 16, 16, "Vous invoquez le pouvoir des montagnes, élevant des sommets majestueux à partir de l'éther...",
                                            "...mais votre sort est dissipé par l'ennemi, les montagnes s'effondrant avant de les toucher.",
                                            "...et votre création de montagne écrase l'ennemi sous une masse de roche dévastatrice, les écrasant sous leur poids écrasant !",
                                            "...et votre création de montagne critique engendre un titan des cimes, piétinant l'ennemi dans une éruption de destruction !!",
                                            0, 90],
            "Création Continentale": [80, 56, 10, 20, 18, "Vous invoquez la puissance des continents, façonnant des terres immenses à partir de l'éther...",
                                            "...mais votre sort est dissipé par l'ennemi, les terres s'effondrant avant de les toucher.",
                                            "...et votre création continentale écrase l'ennemi sous un raz-de-marée de terre dévastatrice, les ensevelissant sous des continents en mouvement !",
                                            "...et votre création continentale critique forge un titan des terres, écrasant l'ennemi dans une apocalypse géante de destruction !!",
                                            0, 100],
            "Explosion Légère": [90, 14, 50, 4, 0, "Vous canalisez une petite quantité d'énergie, créant une explosion de faible intensité...",
                                 "...mais votre sort est dissipé par l'ennemi, l'explosion se dissipant avant d'atteindre sa cible.",
                                 "...et votre explosion touche l'ennemi, le projetant en arrière dans une déflagration contrôlée !",
                                 "...et votre explosion critique engendre une détonation dévastatrice, balayant l'ennemi dans une onde de choc explosive !!",
                                 0, 0],
            "Explosion Renforcée": [88, 22, 50, 4, 0, "Vous accumulez une puissance explosive plus grande, créant une détonation de force accrue...",
                                        "...mais votre sort est détourné par l'ennemi, l'explosion étant absorbée avant de l'atteindre.",
                                        "...et votre explosion frappe l'ennemi avec une force accrue, les envoyant voler dans une explosion puissante !",
                                        "...et votre explosion critique déclenche un feu d'artifice d'explosions, pulvérisant l'ennemi dans un torrent d'énergie destructrice !!",
                                        0, 0],
            "Explosion Lourde": [86, 31, 50, 4, 0, "Vous libérez une vague d'énergie explosive, créant une déflagration massive...",
                                    "...mais votre sort est contrecarré par l'ennemi, l'explosion se dispersant sans causer de dégâts.",
                                    "...et votre explosion frappe l'ennemi de plein fouet, les propulsant à travers la pièce dans une explosion écrasante !",
                                    "...et votre explosion critique déclenche une détonation titanesque, ravageant l'ennemi dans un cataclysme explosif !!",
                                    0, 0],
            "Explosion Maitrisée": [84, 40, 50, 5, 0, "Vous contrôlez l'énergie explosive avec précision, créant une explosion focalisée et dirigée...",
                                        "...mais votre sort est esquivé par l'ennemi, l'explosion passant à côté d'eux sans les toucher.",
                                        "...et votre explosion frappe l'ennemi avec une précision mortelle, les projetant dans une explosion contrôlée !",
                                        "...et votre explosion critique génère une déflagration surpuissante, annihilant l'ennemi dans une explosion ciblée !!",
                                        0, 0],
            "Explosion Fatale": [82, 49, 50, 5, 0, "Vous libérez une explosion d'une puissance destructrice, consumant tout sur son passage...",
                                    "...mais votre sort est dissipé par l'ennemi, l'explosion s'évaporant avant d'atteindre sa cible.",
                                    "...et votre explosion dévastatrice frappe l'ennemi de plein fouet, les réduisant en cendres dans une déflagration massive !",
                                    "...et votre explosion critique déchaîne une détonation apocalyptique, pulvérisant l'ennemi dans une explosion infernale !!",
                                    0, 0],
            "Explosion de la Comète": [80, 56, 50, 7, 0, "Vous invoquez une explosion colossale, déclenchant une détonation cosmique...",
                                            "...mais votre sort est détourné par l'ennemi, l'explosion s'effaçant avant de les toucher.",
                                            "...et votre explosion cosmique consume l'ennemi dans une supernova dévastatrice, les élevant dans une explosion interstellaire !",
                                            "...et votre explosion cosmique critique crée une explosion galactique, éradiquant l'ennemi dans une conflagration cosmique !!",
                                            0, 0],
            "Dance Volevie": [90, 14, 15, 5, 32, "Vous dansez avec agilité, tournoyant autour de votre ennemi avec grâce...",
                       "...mais votre danse est interrompue par l'ennemi, votre mouvement étant bloqué avant de pouvoir infliger des dégâts.",
                       "...et votre danse enveloppe l'ennemi dans un tourbillon de mouvements rapides, les frappant à plusieurs reprises !",
                       "...et votre danse critique crée une tempête de lames tournoyantes, taillant l'ennemi dans une danse mortelle !!",
                       0, 5],
            "Dance Siphoneuse": [88, 19, 15, 7, 27, "Vous dansez avec une fluidité hypnotique, drainant l'énergie vitale de votre ennemi avec chaque mouvement...",
                                    "...mais votre danse est perturbée par l'ennemi, l'effet de drain étant dissipé avant de pouvoir se manifester.",
                                    "...et votre danse aspire l'énergie vitale de l'ennemi, vous guérissant tandis que vous les affaiblissez !",
                                    "...et votre danse critique engendre une frénésie de draine, vidant l'ennemi de leur vitalité dans une danse vampirique !!",
                                    0, 5],
            "Dance Vampirique": [86, 28, 15, 7, 27, "Vous dansez avec une grâce sinistre, réclamant le sang de vos ennemis pour renforcer votre propre pouvoir...",
                                    "...mais votre danse est repoussée par l'ennemi, leur volonté brisant votre lien avant que vous puissiez vous nourrir.",
                                    "...et votre danse se nourrit du sang de l'ennemi, vous régénérant tandis que vous les affaiblissez !",
                                    "...et votre danse critique déclenche un festin sanguinaire, dévorant l'ennemi dans une danse de mort vampirique !!",
                                    0, 4],
            "Dance Parasite": [84, 37, 15, 8, 22, "Vous dansez avec une démarche insidieuse, implantant des parasites dans le corps de votre ennemi avec chaque mouvement...",
                                    "...mais votre danse est contrée par l'ennemi, leur corps rejetant les parasites avant qu'ils ne puissent causer de dommages.",
                                    "...et votre danse infeste l'ennemi de parasites, les affaiblissant tandis que vous en tirez profit !",
                                    "...et votre danse critique crée une marée de parasites, dévorant l'ennemi de l'intérieur dans une danse parasitaire !!",
                                    0, 4],
            "Dance Destructrice": [82, 46, 15, 8, 22, "Vous dansez avec une férocité sauvage, déchirant l'ennemi avec chaque mouvement brutal...",
                                        "...mais votre danse est contrecarrée par l'ennemi, leur résistance réduisant l'impact de vos attaques.",
                                        "...et votre danse déchaîne une tempête de destruction, frappant l'ennemi avec une force brute !",
                                        "...et votre danse critique libère une explosion de puissance destructrice, déchirant l'ennemi dans une danse chaotique de mort !!",
                                        0, 3],
            "Dance Créatrice": [80, 53, 15, 9, 17, "Vous dansez avec une grâce envoûtante, tissant des illusions et des mirages autour de l'ennemi...",
                                    "...mais votre danse est dissipée par l'ennemi, leur volonté brisant les illusions avant qu'elles ne puissent prendre forme.",
                                    "...et votre danse crée des images hypnotiques, distrayant l'ennemi tandis que vous drainez sa vitalité !",
                                    "...et votre danse critique engendre un spectacle de création magique, piégeant l'ennemi dans un monde de mirages drainant sa vitalité !!",
                                    0, 2],
        }
        self.annuaire_de_cout_des_sorts = {
            "Tir Arcanique": 5,
            "Faisceau Rapide": 8,
            "Faisceau Statique": 15,
            "Faisceau Electrique": 20,
            "Faisceau de l'Eclair": 25,
            "Faisceau Foudroyant": 30,
            "Faisceau de la Mort Blanche": 40,
            "Thermosphère Chaude": 8,
            "Thermosphère Brulante": 15,
            "Thermosphère Enflammée": 20,
            "Thermosphère de la Fournaise": 25,
            "Thermosphère Magmatique": 30,
            "Thermosphère Solaire": 40,
            "Pic Bleu": 8,
            "Pic Froid": 15,
            "Pic Givré": 20,
            "Pic Glacial": 25,
            "Pic Polaire": 30,
            "Pic Zéro": 40,
            "Création d'Argile": 8,
            "Création de Lapis": 15,
            "Création de Granite": 20,
            "Création Obsidienne": 25,
            "Création de la Montagne": 30,
            "Création Continentale": 40,
            "Explosion Légère": 8,
            "Explosion Renforcée": 15,
            "Explosion Lourde": 20,
            "Explosion Maitrisée": 25,
            "Explosion Fatale": 30,
            "Explosion de la Comète": 30,
            "Dance Volevie": 8,
            "Dance Siphoneuse": 15,
            "Dance Vampirique": 20,
            "Dance Parasite": 25,
            "Dance Destructrice": 30,
            "Dance Créatrice": 40,
            "Rafale": 15,
            "Avalanche": 30,
            "Libération Enflammée": 30,
            "Libération Fulgurante": 30,
            "Libération Glaciale": 30,
            "Libération Sanglante": 30,
            "Libération Holomélanocrate": 30,
            "Mirroir d'Eau": 35,
            "Brume de Sang": 35,
            "Explosion de Feu Sacré": 30,
            "Carrousel": 40,
            "Sonata Pitoyable": 8, 
            "Sonata Miséricordieuse": 15,
            "Sonata Empathique": 20,
            "Sonata Sincère": 25,
            "Sonata Bienveillante": 30,
            "Sonata Absolutrice": 40
        }
        # glossaire des sorts supplementaires
        if self.rafale:
            sorts_supplementaires.append("Rafale")
        if self.avalanche:
            sorts_supplementaires.append("Avalanche")
        if self.liberation_de_feu:
            sorts_supplementaires.append("Libération Enflammée")
        if self.liberation_de_foudre:
            sorts_supplementaires.append("Libération Fulgurante")
        if self.liberation_de_glace:
            sorts_supplementaires.append("Libération Glaciale")
        if self.liberation_de_sang:
            sorts_supplementaires.append("Libération Sanglante")
        if self.liberation_de_terre:
            sorts_supplementaires.append("Libération Holomélanocrate")

        if self.mirroir_eau:
            sorts_supplementaires.append("Mirroir d'Eau")
        if self.brume_de_sang:
            sorts_supplementaires.append("Brume de Sang")
        if self.explosion_de_feu:
            sorts_supplementaires.append("Explosion de Feu Sacré")
        if self.carrousel:
            sorts_supplementaires.append("Carrousel")

        # ajout des sorts a la liste sorts
        if BuildABear:
            for attaque in self.sorts_de_foudre:
                self.sorts.append(attaque)
            for attaque in self.sorts_de_feu:
                self.sorts.append(attaque)
            for attaque in self.sorts_de_glace:
                self.sorts.append(attaque)
            for attaque in self.sorts_de_terre:
                self.sorts.append(attaque)
            for attaque in self.sorts_de_physique:
                self.sorts.append(attaque)
            for attaque in self.sorts_de_sang:
                self.sorts.append(attaque)
            for attaque in self.sorts_de_soin:
                self.sorts.append(attaque)
            if len(sorts_supplementaires) > 0:
                for attaque in sorts_supplementaires:
                    self.sorts.append(attaque)
        else:
            for sort in Player.sorts_possedes:
                self.sorts.append(sort)
        

        # Dictionnaire des items utilisables
        # feuille/fruit jindagee = +3%/+6% pvmax chaques tours 5 tours
        # feuille/fruit aatma = +3%/+6% manamax chaques tours 5 tours
        # crystal elementaire = effet elementaire elatoire 2t chez lennemi
        # Ambroisie = attk +15% pendant 5 tours
        # Hydromel = sorts +15% pendant 5 tours
        # Orbe de furie = prochaine attaque  +300% dgt
        # Orbe de folie = prochain sort +300% dgt
        # remede 0/superieur/divin = rend 10%/20%/30% pvmax
        # pillule 0/superieur/divin = rend 10%/20%/30% pvmax
        # Flechette Rouge = enflamme l'ennemi 2 tours
        # Flechette Bleue = gele l'ennemi 2 tours
        # Fleche Rouge = enflamme l'ennemi 5 tours
        # Fleche Bleue = gele l'ennemi 5 tours
        # Poudre/Roche/Bombe Explosive = inflige 5% pvmax ennemi + vulnerable 5%/10%/15% elements
        # Fiole/gourde de poison = inflige 25% pvmax ennemi sur 10/5 tours [debutTour]
        # seve/larme/soluté d'absolution = inflige 7%/11%/15% pvmax boss [debutTour]
        # seve/larme/solute d'exorcisme = inflige 10%/15%/20% pvmax ennemi [debutTour]
        # Grand/0 mutagene Bleu = +10%/+15% manamax -10%/-5% pvmax [debutTour]
        # Grand/0 mutagene Rouge = +10%/+15% pvmax -10%/-5% manamax [debutTour]
        # Grand/0 mutagene Vert = +10%/+15% chance critique [debutTour]
        # Grand/0 mutagene Doré = +10%/+15% mana/pvmax et chance critique [debutTour]
        # mutagene fanatique = +50% manamax 0% chacne critique [debutTour]
        # mutagene hérétique = +50% pvmax 0% chacne critique [debutTour]
        # BuildABear
        self.items = Player.items_possedes
        self.items_autorises_que_au_premier_tour = [
            "Fiole de Poison",
            "Gourde de Poison",
            "Sève d'Absolution",
            "Larme d'Absolution",
            "Soluté d'Absolution",
            "Larme d'Exorcisme",
            "Sève d'Exorcisme",
            "Soluté d'Exorcisme",
            "Mutagène Bleu",
            "Grand Mutagène Bleu",
            "Mutagène Rouge",
            "Grand Mutagène Rouge",
            "Mutagène Vert",
            "Grand Mutagène Vert",
            "Mutagène Doré",
            "Grand Mutagène Doré",
            "Mutagène Hérétique",
            "Mutagène Fanatique",
        ]

        # Liste de stigmas

        

        # Placeholdeur pour les caractéristiques du monstre
        self.commentaire_de_resurection_de_monstre = "Aucun"
        self.type_daction_du_monstre = "None"
        self.vie_du_monstre_pour_sables_du_temps_actuel = 0
        self.vie_du_monstre_pour_sables_du_temps_tour_avant = 0
        self.vie_du_monstre_pour_sables_du_temps_a_utiliser = 0
        self.monstre_level = 0
        self.monstre_gain_de_defence = False
        self.monstre_gain_de_defence_nombre = 0
        self.monstre_gain_de_defence_nombre_tour = 0
        self.monstre_a_utilise_feu_ce_tour = False
        self.monstre_a_utilise_foudre_ce_tour = False
        self.monstre_a_utilise_glace_ce_tour = False
        self.monstre_a_utilise_physique_ce_tour = False
        self.monstre_a_utilise_sang_ce_tour = False
        self.monstre_a_utilise_terre_ce_tour = False
        self.monstre_a_utilise_blesse_ce_tour = False
        self.monstre_a_utilise_deconcentre_ce_tour = False
        self.monstre_a_utilise_gold_ce_tour = False
        self.monstre_a_utilise_instable_ce_tour = False
        self.monstre_a_utilise_muet_ce_tour = False
        self.monstre_a_utilise_confus_ce_tour = False
        self.monstre_nom = "Bob"
        self.monstre_passe_son_tour = False
        self.monstre_en_etat_de_choc = False
        self.monstre_en_etat_de_choc_nombre_tour = False
        self.monstre_points_de_vie = 20
        self.monstre_points_de_vie_max = 20
        self.monstre_points_de_mana = 20
        self.monstre_points_de_mana_max = 20
        self.monstre_points_de_resistance = 2
        self.monstre_nombre_de_vies_supplementaire = 1
        self.monstre_points_de_force = 1
        self.monstre_points_de_intelligence = 1
        self.monstre_est_envol = False  # Envol, -30% chance de toucher
        self.monstre_est_envol_nombre_tour = 0
        self.monstre_est_gele = False  # Gele, prend 2x + de degats
        self.monstre_est_gele_nombre_tour = 0
        self.monstre_est_en_feu = False  # en feu, perd des pv par tour
        self.monstre_est_en_feu_nombre_tour = 0
        self.monstre_est_en_feu_degat = 0
        self.monstre_est_paralyse = False  # paralysie, passe son tour
        self.monstre_est_paralyse_nombre_tour = 0
        self.monstre_est_vulnerable = False  # vulnerable, suceptible elements
        self.monstre_est_vulnerable_nombre_tour = 0
        self.monstre_niveau_de_vulnerabilite = 0
        self.monstre_est_empoisonne = False  # poison, gros degat peu de tours
        self.monstre_est_empoisonne_nombre_tour = 0
        self.monstre_est_empoisonne_degat = 0
        self.monstre_est_regeneration = False  # regen, reprend vie par tour
        self.monstre_est_regeneration_nombre_tour = 0
        self.monstre_est_regeneration_soin = 0
        self.monstre_liste_actions = []
        self.monstre_recompense = {"Attaque": 1, "Defence": 1}

        # Placeholdeur pour les stigmas du monstre
        self.stigma_monstre_positif = "None"
        self.stigma_monstre_negatif = "None"
        self.stigma_monstre_bonus = "None"

        # Valeur supplementaires
        self.liste_des_items = []
        self.InCombat = True
        self.derniere_action_utilisee = None
        self.type_de_derniere_action_utilisee = None
    

        # Dictionnaires pour Monstres
        self.liste_de_monstres_etage_1_2 = [
            "Gluant",
            "Feu Follet",
            "Golem de Terre",
            "Ombre Tangible",
            "Clone de Verre",
        ]
        self.liste_de_monstres_etage_3_4 = [
            "Métroïde",
            "Trienun",
            "Phénix Juvénile",
            "Rochemikaze",
            "Loup de Glace",
        ]
        self.liste_de_monstres_etage_5_6 = [
            "Voleur Félin",
            "Siffloteur",
            "Lapin du Désastre",
            "Cerf Voleur",
            "Aspiratrésor Blindé",
        ]
        self.liste_de_monstres_etage_7_8 = [
            "Gluant de Crystal",
            "Sixenun",
            "Siffloteur de Jade",
            "Aurelionite",
            "Sacatrésor",
        ]
        self.liste_de_monstres_etage_9_10 = [
            "Gluant",
            "Feu Follet",
            "Golem de Terre",
            "Ombre Tangible",
            "Clone de Verre",
            "Métroïde",
            "Trienun",
            "Phénix Juvénile",
            "Rochemikaze",
            "Loup de Glace",
            "Voleur Félin",
            "Siffloteur",
            "Lapin du Désastre",
            "Cerf Voleur",
            "Aspiratrésor Blindé",
            "Gluant de Crystal",
            "Sixenun",
            "Siffloteur de Jade",
            "Chinasous",
            "Sacatrésor",
        ]
        self.liste_de_monstre_totaux_pour_dernier_choix = [
            self.liste_de_monstres_etage_1_2,
            self.liste_de_monstres_etage_1_2,
            self.liste_de_monstres_etage_3_4,
            self.liste_de_monstres_etage_3_4,
            self.liste_de_monstres_etage_5_6,
            self.liste_de_monstres_etage_5_6,
            self.liste_de_monstres_etage_7_8,
            self.liste_de_monstres_etage_7_8,
            self.liste_de_monstres_etage_9_10,
            self.liste_de_monstres_etage_9_10,
        ]
        self.liste_de_boss = [
            "Clone d'Obsidienne",
            "Chevalier Pourpre",
            "Roi Amonrê",
            "Apprenti",
            "Bouffon",
            "Prince des Voleurs",
            "Roi Déchu",
            "Maitre Mage",
            "Amalgame",
            "Coliseum",
        ]
        dir_path = Player.chemin_musique
        musique = dir_path + "\\"
        self.CHEMINABSOLUMUSIQUE = musique
        self.alfred_liste_questions = [
            {
                "Question": ("La mort provoque l'arrêt des fonctions vitales du corps."
                             "\nMais l'âme, elle, peux entendre la voix des choses qui peuplent l'au dela, et se préparent a l'accueillir."
                             "\nQu'est-ce-qui accompagne l'arrivée de l'âme dans l'au dela, et est annoncé après la mort ?"),
                "Reponse 1": "1 - Un concert de trompettes",
                "Reponse 2": "2 - Un risque de pluie",
                "Reponse 3": "3 - Une lumière pourpre",
                "Reponse 4": "4 - Un train doré",
                "Reponse a la question": 2,
            },
            {
                "Question": ("Le Sixenun est un monstre qui a la capacité étonnante de faire apparaitre une roulette,"
                             "\nappliquant selon le résultat du tirage, des effets qui passent a travers toutes sortes de protection."
                             "Le Trienun, un parent éloigné un peu plus faible, peux aussi faire apparaitre un jeu d'argent"
                             "\ncommunémment trouvé dans les casino. Lequel ?"),
                "Reponse 1": "1 - Une Grille de Keno",
                "Reponse 2": "2 - Le Pachinko",
                "Reponse 3": "3 - La Table de BlackJack",
                "Reponse 4": "4 - Le Bandit Manchot",
                "Reponse a la question": 4,
            },
            {
                "Question": ("Quel frère du Roi, aussi connu sous le nom de Roi des Sables,"
                             "\na mysterieusement disparu avant la fin de la construction du Coliseum ?"),
                "Reponse 1": "1 - Le Roi Amonrè",
                "Reponse 2": "2 - Le Roi Amonré",
                "Reponse 3": "3 - Le Roi Amonrê",
                "Reponse 4": "4 - Le Roi Amonre",
                "Reponse a la question": 3,
            },
            {
                "Question": ("Quel adjectif qualifie un sort de soin de niveau 2 ?"),
                "Reponse 1": "1 - Absolutrice",
                "Reponse 2": "2 - Pitoyable",
                "Reponse 3": "3 - Miséricordieuse",
                "Reponse 4": "4 - Empathique",
                "Reponse a la question": 3,
            },
            {
                "Question": ("A quel objet attribue-t-on les techniques de glace ?"),#5
                "Reponse 1": "1 - Katana",
                "Reponse 2": "2 - Lance",
                "Reponse 3": "3 - Dague",
                "Reponse 4": "4 - Hache",
                "Reponse a la question": 1,
            },
            {
                "Question": ("Combien de points de vie tu perd si tu répond mal a"
                             "ma question ?"),
                "Reponse 1": "1 - La moitié de ce qu'il te reste",
                "Reponse 2": "2 - La moitié de ce que tu peux avoir",
                "Reponse 3": "3 - Le quart de ce qu'il te reste",
                "Reponse 4": "4 - Le quart de ce que tu peux avoir",
                "Reponse a la question": 1,
            },
            {
                "Question": ("Qui a construit le Coliseum ?"),
                "Reponse 1": "1 - Le Roi Déchu",
                "Reponse 2": "2 - Le Maitre Mage",
                "Reponse 3": "3 - Rigor Mortex",
                "Reponse 4": "4 - La Reine Oubliée",
                "Reponse a la question": 2,
            },
            {
                "Question": ("Combien d'ailes possède le griffon du Royaume, l'emblème du Coliseum ?"),
                "Reponse 1": "1 - Deux",
                "Reponse 2": "2 - Trois",
                "Reponse 3": "3 - Quatre",
                "Reponse 4": "4 - Cinq",
                "Reponse a la question": 4,
            },
            {
                "Question": ("Dans le couloir de fin, on peux voir dans le mur des moments forts de l'aventure"
                             ", gravés dand la roche.\nUn moment en particulier est emmuré, mais on peut "
                             "apercevoir un certain mot, et un nombre lui étant associé.\nQuelle est la"
                             "relation entre le mot et le nombre ?"),
                "Reponse 1": "1 - Chaque chiffres du nombre correspondent a la position de la lettre au dessus, dans l'alphabet",
                "Reponse 2": "2 - Le nombre représente la position de chaque lettres du mot dans l'alphabet, additionnés entre eux",
                "Reponse 3": "3 - Chaque chiffres du nombre correspondent au chiffre par lequel on pourrait remplacer la lettre, genre 5 pour E.",
                "Reponse 4": "4 - Quel mot ? Quel nombre ? De quoi tu parle ?",
                "Reponse a la question": 1,
            },
            {
                "Question": ("Quel code permet de gagner le talent *Affinité de Feu* ?"), #10
                "Reponse 1": "1 - 4862",
                "Reponse 2": "2 - 8324",
                "Reponse 3": "3 - 1257",
                "Reponse 4": "4 - 2684",
                "Reponse a la question": 3,
            },
            {
                "Question": ("Quel membre de la cour du Roi est devenu le clone d'Obsidienne Magique ?"),
                "Reponse 1": "1 - Le Ministre de la Justice",
                "Reponse 2": "2 - La Reine Oubliée",
                "Reponse 3": "3 - Le Messager Royal",
                "Reponse 4": "4 - L'entieretée de la Garde Royale",
                "Reponse a la question": 4,
            },
            {
                "Question": ("Si je te brise les côtes la maintenant tout de suite,\nQuelles sont les chances que tu esquive ?"),
                "Reponse 1": f"1 - {self.taux_de_esquive}",
                "Reponse 2": f"2 - {self.taux_de_esquive * 2}",
                "Reponse 3": f"3 - {self.taux_de_esquive - 1}",
                "Reponse 4": f"4 - {self.taux_de_esquive + 1}",
                "Reponse a la question": 1,
            },
            {
                "Question": ("Qu'est ce que j'ai dans ma poche ?"),
                "Reponse 1": "1 - Rien du tout",
                "Reponse 2": "2 - Un anneau",
                "Reponse 3": "3 - De quoi prélever les ressources dont j'ai besoin",
                "Reponse 4": "4 - Une fiole d'anesthésiant",
                "Reponse a la question": 2,
            },
            {
                "Question": ("Que fait le Bouffon quand il dit *Tournicotons* ?"),
                "Reponse 1": "1 - Il reprend de la vie",
                "Reponse 2": "2 - Il invoque des vagues de flammes répondant a ses instructions",
                "Reponse 3": "3 - Il pose des questions, comme moi",
                "Reponse 4": "4 - Il lance une partie de tennis avec un orbe de lumière",
                "Reponse a la question": 2,
            },
            {
                "Question": ("Que dit le Bouffon avant de reprendre de la vie ?"),#15
                "Reponse 1": "1 - *Tournicota ! Tournicota !*",
                "Reponse 2": "2 - *Tournicotez ! Tournicotez !*",
                "Reponse 3": "3 - *Tournicoti ! Tournicoti !*",
                "Reponse 4": "4 - *Tournicotons ! Tournicotons !*",
                "Reponse a la question": 3,
            },
            {
                "Question": ("Quelle sont les chances que le livre de la cigogne montre un sort enregistré par quelqu'un d'autre ?"),
                "Reponse 1": "1 - 10%",
                "Reponse 2": "2 - 1%",
                "Reponse 3": "3 - 5%",
                "Reponse 4": "4 - 3%",
                "Reponse a la question": 4,
            },
            {
                "Question": ("Les personnages, tout comme les monstres,"
                             " ont des stigmas liés a leur experience et/ou leur condition."
                             "\nQue fait le stigma Sanjiva ?"),
                "Reponse 1": "1 - Il empêche d'être blessé ou déconcentré",
                "Reponse 2": "2 - Il redonne des points de vie en cas d'urgence",
                "Reponse 3": "3 - Il permet de ressusciter une fois sans fée",
                "Reponse 4": "4 - Il donne une regénération constante des points de vie",
                "Reponse a la question": 2,
            },
            {
                "Question": ("Qui est l'intru ?"),
                "Reponse 1": "1 - Fiole de poison",
                "Reponse 2": "2 - Poudre explosive",
                "Reponse 3": "3 - Feuille Jindagee",
                "Reponse 4": "4 - Crystal Elementaire*",
                "Reponse a la question": 1,
            },
            {
                "Question": ("Qui est l'intru ?"),
                "Reponse 1": "1 - Poing de la Comète",
                "Reponse 2": "2 - Dague Volevie",
                "Reponse 3": "3 - Corne Obsidienne",
                "Reponse 4": "4 - Faisceau Electrique",
                "Reponse a la question": 4,
            },
            {
                "Question": ("Qui est l'intru ?"), #20
                "Reponse 1": "1 - Sixenun",
                "Reponse 2": "2 - Siffloteur",
                "Reponse 3": "3 - Sacatrésor",
                "Reponse 4": "4 - Aurelionite",
                "Reponse a la question": 2,
            },
        ]
        # SORTS MONSTRE
        #SORTS GENERAUX
        self.sorts_de_feu_de_monstre = [
            "Flamme",
            "Vents du Sud",
            "Flamme Avancée",
            "Thermosphère Brulante",
            "Thermosphère de la Fournaise",
            "Thermosphère Magmatique",
            "Thermosphère Solaire"
        ]
        self.sorts_de_foudre_de_monstre = [
            "Claquement de Foudre",
            "Vents de l'Est",
            "Coup de Foudre",
            "Faisceau Statique",
            "Faisceau de l'Eclair",
            "Faisceau Foudroyant",
            "Rituel Canope",
            "Faisceau de la Mort Blanche"
        ]
        self.sorts_de_glace_de_monstre = [
            "Froideur d'Outretombe",
            "Cercueil de Neige",
            "Vents du Nord",
            "Gel",
            "Giga Gel",
            "Oméga Gelure",
            "Pic Froid",
            "Pic Glacial",
            "Pic Polaire",
            "Pic Zéro"
        ]
        self.sorts_de_terre_de_monstre = [
            "Oméga Lapidation",
            "Création de Lapis",
            "Création Obsidienne",
            "Création de la Montagne",
            "Création Continentale"
        ]
        self.sorts_de_sang_de_monstre = [
            "Vents de l'Ouest",
            "Oméga Saignée",
            "Mache",
            "Dance Siphoneuse",
            "Dance Parasite",
            "Houken",
            "Dance Destructrice",
            "Dance Créatrice"
        ]
        self.sorts_de_physique_de_monstre = [
            "Poing de Mana",
            "Tir Arcanique",
            "Explosion",
            "Point Vital",
            "Son Rapide",
            "Bombe Arcanique",
            "Jugement",
            "Explosion Renforcée",
            "Explosion Maitrisée",
            "Missile Arcanique",
            "Explosion Fatale",
            "Explosion de la Comète"
        ]
        #SORTS SPECIAUX
        self.sorts_de_soin_de_monstre = [
            "Soin",
            "Feu Regénérateur",
            "Réglages d'Usine",
            "Regénération Basaltique",
            "Carotte Magique",
            "Soin Avancé",
            "Engloutis",
            "Sonata Pitoyable",
            "Rejuvenation",
            "Sonata Miséricordieuse",
            "Sonata Sincère",
            "Tournicoti",
            "Sonata Bienveillante",
            "Sonata Absolutrice"
        ]
        self.sorts_de_blessure_de_monstre = [ # technique coute vie
            ""
        ]
        self.sorts_de_deconcentration_de_monstre = [ # sorts coute plus de mana
            "Possession du mana",
            "Oeuil Maudit"
        ]
        self.sorts_de_gold_de_monstre = [ #action coute gold
            "Ruée vers l'or",
        ]
        self.sorts_de_instable_de_monstre = [ #pas de technique
            ""
        ]
        self.sorts_de_muet_de_monstre = [ # pas de sorts
            ""
        ]
        self.sorts_de_confusion_de_monstre = [ # pas d'item
            "Confusion"
        ]
        #SORTS SUPPLEMENTAIRES
        self.sorts_supplementaire_de_monstre = [ 
            # sorts spéciaux ayant besoin de leur propre implémentation
            "Tout Feu Tout Flamme",
            "Volepièce",
            "Bandit Manchot",
            "Cat-astrophe",
            "Son Lent",
            "Vole-Ame",
            "Rituel",
            "Tempêtes du Nord",
            "Tempêtes du Sud",
            "Tempêtes de l'Est",
            "Tempêtes de l'Ouest",
            "Vacarme Rapide",
            "Vacarme Lent",
            "Vide",
            "Eveil de Runes",
            "Lamentations",
            "Invoquation Canope",
            "Magie Noire",
            "Magie Ténébreuse",
            "Tournicota",
            "Tournicotons",
            "Tournicotez",
            "Tome de Salomon",
            "Sort Ultime",
            "Ultime Ultime",
            "Ultima",
            "Dragon Ascendant",
            "Magie Abyssale",
        ]
        self.ANNUAIRECOUTSORTMONSTRE = {
            "Flamme": 5,
            "Vents du Sud": 5,
            "Flamme Avancée": 5,
            "Thermosphère Brulante": 5,
            "Thermosphère de la Fournaise": 5,
            "Thermosphère Magmatique": 5,
            "Thermosphère Solaire": 5,
            "Claquement de Foudre": 5,
            "Vents de l'Est": 5,
            "Coup de Foudre": 5,
            "Faisceau Statique": 5,
            "Faisceau de l'Eclair": 5,
            "Faisceau Foudroyant": 5,
            "Rituel Canope": 5,
            "Faisceau de la Mort Blanche": 5,
            "Froideur d'Outretombe": 5,
            "Cercueil de Neige": 5,
            "Vents du Nord": 5,
            "Gel": 5,
            "Giga Gel": 5,
            "Oméga Gelure": 5,
            "Pic Froid": 5,
            "Pic Glacial": 5,
            "Pic Polaire": 5,
            "Pic Zéro": 5,
            "Oméga Lapidation": 5,
            "Création de Lapis": 5,
            "Création Obsidienne": 5,
            "Création de la Montagne": 5,
            "Création Continentale"
            "Vents de l'Ouest": 5,
            "Oméga Saignée": 5,
            "Mache": 5,
            "Dance Siphoneuse": 5,
            "Dance Parasite": 5,
            "Houken": 5,
            "Dance Destructrice": 5,
            "Dance Créatrice": 5,
            "Poing de Mana": 5,
            "Tir Arcanique": 5,
            "Explosion": 5,
            "Point Vital": 5,
            "Son Rapide": 5,
            "Bombe Arcanique": 5,
            "Jugement": 5,
            "Explosion Renforcée": 5,
            "Explosion Maitrisée": 5,
            "Missile Arcanique": 5,
            "Explosion Fatale": 5,
            "Explosion de la Comète": 5,
            "Soin": 5,
            "Feu Regénérateur": 5,
            "Réglages d'Usine": 5,
            "Regénération Basaltique": 5,
            "Carotte Magique": 5,
            "Soin Avancé": 5,
            "Engloutis": 5,
            "Sonata Pitoyable": 5,
            "Rejuvenation": 5,
            "Sonata Miséricordieuse": 5,
            "Sonata Sincère": 5,
            "Tournicoti": 5,
            "Sonata Bienveillante": 5,
            "Sonata Absolutrice": 5,
            "Possession du mana": 5,
            "Oeuil Maudit": 5,
            "Ruée vers l'or": 5,
            "Confusion": 5,
            "Tout Feu Tout Flamme": 5,
            "Volepièce": 5,
            "Bandit Manchot": 5,
            "Cat-astrophe": 5,
            "Son Lent": 5,
            "Vole-Ame": 5,
            "Rituel": 5,
            "Tempêtes du Nord": 5,
            "Tempêtes du Sud": 5,
            "Tempêtes de l'Est": 5,
            "Tempêtes de l'Ouest": 5,
            "Vacarme Rapide": 5,
            "Vacarme Lent": 5,
            "Vide": 5,
            "Eveil de Runes": 5,
            "Lamentations": 5,
            "Invoquation Canope": 5,
            "Magie Noire": 5,
            "Magie Ténébreuse": 5,
            "Tournicota": 5,
            "Tournicotons": 5,
            "Tournicotez": 5,
            "Tome de Salomon": 5,
            "Sort Ultime": 5,
            "Ultime Ultime": 5,
            "Ultima": 5,
            "Dragon Ascendant": 5,
            "Magie Abyssale": 5,
        }
        self.annuaire_de_caracteristique_des_sorts_generaux_de_monstre = {
            # %touche, degat, %crit, degat crit, %element, description, message si rate, si touche, si touche crit, nombre tours, effet element
            "Flamme": [95, 4, 20, 5, 50, "L'ennemi fait apparaitre une flamme sur votre position....", 
                       "...mais vous l'esquivez .", 
                       "...et elle vous brule !", 
                       "...et elle vous carbonise !!", 3, 5],
            "Vents du Sud": [90, 5, 25, 5, 50, "L'ennemi invoque les vents brulants du Sud...", 
                             "...mais vous résistez aux temperatures extrêmes .", 
                             "...et vous commencez a bruler !",
                             "...et vos membres s'embrasent sur place !!", 4, 5],
            "Thermosphère Brulante": [88, 10, 20, 4, 18, "L'ennemi crée un tourbillon de flammes autour de vous, vous enveloppant dans une tempête de feu...",
                                      "...mais vous contrez son sort, les flammes se dissipant dans l'air.",
                                      "...et la thermosphère vous enflamme avec une furie incandescente, vous laissant calciné et brûlé !",
                                      "...et sa thermosphère critique déclenche une conflagration cataclysmique, vous réduisant en cendres et en fumée !!",
                                      4, 7],
            "Thermosphère de la Fournaise": [84, 15, 20, 6, 20, "L'ennemi invoque le pouvoir de la fournaise dans la thermosphère, créant une incandescence infernale...",
                                                    "...mais son sort est dissipé par votre résistance, l'incendie se dispersant sans effet.",
                                                    "...et la thermosphère vous engloutit dans un brasier en fusion, vous laissant réduit en cendres !",
                                                    "...et sa thermosphère critique déclenche un holocauste flamboyant, vous consumant dans un feu purificateur !!",
                                                    4, 6],
            "Thermosphère Magmatique": [82, 20, 20, 6, 22, "L'ennemi invoque la puissance du magma dans la thermosphère, créant des rivières de lave en fusion...",
                                                    "...mais son sort est paré par votre résistance, la lave se solidifiant avant de pouvoir vous toucher.",
                                                    "...et la thermosphère vous baigne dans la lave en fusion, vous réduisant à l'état de cendres brûlantes !",
                                                    "...et sa thermosphère critique déclenche une éruption cataclysmique, vous ensevelissant dans un océan de feu et de destruction !!",
                                                    4, 5],
            "Thermosphère Solaire": [80, 25, 20, 8, 22, "L'ennemi canalise l'énergie solaire dans la thermosphère, créant une explosion de lumière et de chaleur...",
                                                    "...mais son sort est dissipé par votre résistance, l'énergie solaire se dissipant dans l'air.",
                                                    "...et la thermosphère vous embrase avec une intensité solaire, vous consumant dans les flammes de l'astre roi !",
                                                    "...et sa thermosphère critique déclenche une supernova dévastatrice, vous réduisant tout à néant dans un éclat aveuglant !!",
                                                    5, 5],
            "Vents de l'Est": [85, 8, 30, 5, 10, "L'ennemi invoque les vents violents et pleins de sables de l'Est...", 
                             "...mais vous résistez aux frottements du sable .", 
                             "...et l'électricité statique due au frottement du sable vous perce de toute part !",
                             "...et l'électricité statique due au frottement du sable vous fait hurler de douleur !!", 0, 0],
            "Faisceau Statique": [88, 10, 20, 4, 10, "L'ennemi charge son faisceau d'énergie statique, créant des étincelles d'électricité dans l'air...",
                                        "...mais vous parez son sort, l'énergie statique se dispersant sans effet.",
                                        "...et le faisceau vous électrise, créant des arcs d'électricité qui parcourent votre corps !",
                                        "...et le faisceau critique vous surcharge, vous consumant dans un tourbillon d'éclairs et de foudre !!",
                                        2, 0],
            "Faisceau de l'Eclair": [84, 15, 16, 7, 14, "L'ennemi invoque la puissance de la foudre dans son faisceau, illuminant le ciel avec des éclairs dévastateurs...",
                                                    "...mais vous parez son sort avec une agilité surnaturelle, l'éclair s'écrasant dans le sol.",
                                                    "...et le faisceau vous frappe avec la force de la foudre, vous électrocutant sur place !",
                                                    "...et le faisceau critique déchaîne un orage de destruction, vous frappant avec une force insurmontable !!",
                                                    2, 0],
            "Faisceau Foudroyant": [82, 20, 15, 7, 10, "L'ennemi libère un faisceau d'énergie foudroyante, déchirant le ciel avec un éclair dévastateur...",
                                                    "...mais vous parez son sort, l'énergie foudroyante se dispersant sans effet.",
                                                    "...et le faisceau invoque la foudre sur vous, vous électrocutant avec une intensité terrifiante !",
                                                    "...et le faisceau critique déclenche un cataclysme électrique, vous dévorant dans un déluge de foudre et de tonnerre !!",
                                                    3, 0],
            "Faisceau de la Mort Blanche": [80, 25, 15, 10, 12, "L'ennemi canalise la puissance de l'éclair dans son faisceau, illuminant le champ de bataille avec une lueur mortelle...",
                                                    "...mais vous parez son sort, l'énergie blanche se dispersant dans l'air.",
                                                    "...et le faisceau éclate sur vous avec une force surhumaine, vous laissant carbonisé et fumant !",
                                                    "...et le faisceau critique déclenche un ouragan de destruction, vous annihilant sur son passage !!",
                                                    3, 0],
            "Vents du Nord": [85, 9, 30, 5, 10, "L'ennemi invoque les vents glaciaux du Nord...", 
                             "...mais vous résistez aux températures givrantes .", 
                             "...et vous commencez a geler sur place !",
                             "...et vous vous mettez a ressentir de la chaleur et une torpeur mortelle !!", 3, 0],
            "Pic Froid": [88, 10, 20, 5, 18, "L'ennemi crée un pic de glace empreint d'une froideur intense, pointant menaçant vers vous...",
                                "...mais son sort est dissipé par vous, le pic de glace se fondant dans l'air.",
                                "...et le pic de glace vous gèle avec une fureur glaciale, vous laissant engourdi et gelé !",
                                "...et le pic de glace critique déclenche une tempête de glace dévastatrice, gelant tout sur son passage !!",
                                3, 0],
            "Pic Glacial": [84, 15, 20, 5, 20, "L'ennemi canalise le pouvoir de l'hiver dans un pic de glace immense et imposant, pointant menaçant vers vous...",
                                "...mais son sort est dissipé par vous, le pic de glace se brisant avant de vous toucher.",
                                "...et le pic de glace vous glace jusqu'au cœur avec une cruauté glaçante, vous laissant pris dans les griffes du froid !",
                                "...et le pic de glace critique déclenche une tempête de verglas dévastatrice, gelant tout dans un monde de glace éternelle !!",
                                4, 0],
            "Pic Polaire": [82, 20, 20, 5, 22, "L'ennemi invoque un pic de glace chargé du froid polaire, pointant menaçant vers vous...",
                                "...mais son sort est dissipé par vous, le pic de glace se brisant avant de vous toucher.",
                                "...et le pic de glace vous enveloppe dans une nuit éternelle de froid glacial, vous laissant gelé jusqu'à l'âme !",
                                "...et le pic de glace critique déclenche une apocalypse glaciaire, gelant tout dans un désert de glace sans fin !!",
                                4, 0],
            "Pic Zéro": [80, 25, 20, 5, 22, "L'ennemi libère un pic de glace d'un froid absolu, pointant menaçant vers vous...",
                                "...mais son sort est dissipé par vous, le pic de glace se brisant avant de vous toucher.",
                                "...et le pic de glace vous congèle dans un hiver éternel, vous laissant prisonnier du gel !",
                                "...et le pic de glace critique déclenche un cataclysme glacial, gelant tout dans un néant de froid absolu !!",
                                4, 0],
            "Création de Lapis": [88, 10, 10, 8, 12, "L'ennemi invoque des fragments de lapis-lazuli, créant une aura de gemmes étincelantes...",
                                    "...mais vous contrecarrez son sort, les gemmes se dispersant dans l'air.",
                                    "...et sa création de lapis vous engloutit dans un tourbillon de pierres précieuses, vous ensorcelant dans un éclat éblouissant !",
                                    "...et sa création de lapis critique forge un golem de gemmes, pulvérisant vous avec un torrent de puissance cristalline !!",
                                    0, 65],
            "Création Obsidienne": [84, 15, 10, 10, 14, "L'ennemi invoque des flots d'obsidienne en fusion, créant un océan de lave en fusion...",
                                        "...mais vous dissipez son sort, la lave se solidifiant avant de vous toucher.",
                                        "...et sa création d'obsidienne vous engloutit dans un brasier en fusion, vous laissant calciné et brûlé !",
                                        "...et sa création d'obsidienne critique forge un golem de lave, vous consumant dans un enfer de feu liquide !!",
                                        0, 80],
            "Création de la Montagne": [82, 20, 10, 10, 16, "L'ennemi invoque le pouvoir des montagnes, élevant des sommets majestueux à partir de l'éther...",
                                            "...mais vous dissipez son sort, les montagnes s'effondrant avant de vous toucher.",
                                            "...et sa création de montagne vous écrase sous une masse de roche dévastatrice, vous écrasant sous leur poids écrasant !",
                                            "...et sa création de montagne critique engendre un titan des cimes, vous piétinant dans une éruption de destruction !!",
                                            0, 90],
            "Création Continentale": [80, 25, 10, 10, 18, "L'ennemi invoque la puissance des continents, façonnant des terres immenses à partir de l'éther...",
                                            "...mais vous dissipez son sort, les terres s'effondrant avant de vous toucher.",
                                            "...et sa création continentale vous écrase sous un raz-de-marée de terre dévastatrice, vous ensevelissant sous des continents en mouvement !",
                                            "...et sa création continentale critique forge un titan des terres, vous écrasant dans une apocalypse géante de destruction !!",
                                            0, 100],
            "Vents de l'Ouest": [85, 10, 30, 5, 10, "L'ennemi invoque les vents magiques de l'Ouest...", 
                             "...mais vous résistez a ses effets .", 
                             "...et il vous lacère la peau !",
                             "...et il vous crible de blessures saignant abondemment !!", 0, 8],
            "Dance Siphoneuse": [88, 10, 15, 7, 27, "L'ennemi danse avec une fluidité hypnotique, drainant votre énergie vitale avec chaque mouvement...",
                                "...mais vous contrez sa danse, l'effet de drain étant dissipé avant de pouvoir se manifester.",
                                "...et sa danse aspire votre énergie vitale, le renforçant tandis qu'il vous affaiblit !",
                                "...et sa danse critique engendre une frénésie de draine, vous vidant de votre vitalité dans une danse vampirique !!",
                                0, 5],
            "Dance Parasite": [84, 15, 35, 8, 22, "L'ennemi danse avec une démarche insidieuse, implantant des parasites dans votre corps avec chaque mouvement...",
                                    "...mais vous parez sa danse, votre corps rejetant les parasites avant qu'ils ne puissent causer de dommages.",
                                    "...et sa danse vous infeste de parasites, vous affaiblissant tandis qu'il en tire profit !",
                                    "...et sa danse critique crée une marée de parasites, vous dévorant de l'intérieur dans une danse parasitaire !!",
                                    0, 4],
            "Dance Destructrice": [82, 20, 15, 8, 22, "L'ennemi danse avec une férocité sauvage, déchirant votre corps avec chaque mouvement brutal...",
                                        "...mais vous esquivez sa danse, votre résistance réduisant l'impact de ses attaques.",
                                        "...et sa danse déchaîne une tempête de destruction, vous frappant avec une force brute !",
                                        "...et sa danse critique libère une explosion de puissance destructrice, vous déchirant dans une danse chaotique de mort !!",
                                        0, 3],
            "Dance Créatrice": [80, 25, 15, 9, 17, "L'ennemi danse avec une grâce envoûtante, tissant des illusions et des mirages autour de vous...",
                                    "...mais vous dissipez sa danse, votre volontée brisant les illusions avant qu'elles ne puissent prendre forme.",
                                    "...et sa danse crée des images hypnotiques, vous drainant votre vitalitée !",
                                    "...et sa danse critique engendre un spectacle de créations magiques, vous piégeant dans un monde de mirages drainant votre vitalité !!",
                                    0, 2],
            "Explosion Renforcée": [88, 10, 50, 4, 0, "L'ennemi accumule une puissance explosive plus grande, créant une détonation de force accrue...",
                                    "...mais vous dissipez son sort, l'explosion étant absorbée avant de vous atteindre.",
                                    "...et son explosion vous frappe avec une force accrue, vous envoyant voler dans une explosion puissante !",
                                    "...et son explosion critique déclenche un feu d'artifice d'explosions, vous pulvérisant dans un torrent d'énergie destructrice !!",
                                    0, 0],
            "Explosion Maitrisée": [84, 15, 50, 5, 0, "L'ennemi contrôle l'énergie explosive avec précision, créant une explosion focalisée et dirigée...",
                                        "...mais vous parez son sort avec une agilité surnaturelle, l'explosion passant à côté de vous sans vous toucher.",
                                        "...et son explosion vous frappe avec une précision mortelle, vous projetant dans une explosion contrôlée !",
                                        "...et son explosion critique génère une déflagration surpuissante, vous annihilant dans une explosion ciblée !!",
                                        0, 0],
            "Explosion Fatale": [82, 20, 50, 5, 0, "L'ennemi libère une explosion d'une puissance destructrice, consumant tout sur son passage...",
                                    "...mais vous dissipez son sort, l'explosion s'évaporant avant de vous atteindre.",
                                    "...et son explosion dévastatrice vous frappe de plein fouet, vous réduisant en cendres dans une déflagration massive !",
                                    "...et son explosion critique déchaîne une détonation apocalyptique, vous anéantissant dans une explosion infernale !!",
                                    0, 0],
            "Explosion de la Comète": [80, 25, 50, 7, 0, "L'ennemi invoque une explosion colossale, déclenchant une détonation cosmique...",
                                            "...mais vous détournez son sort, l'explosion s'effaçant avant de vous toucher.",
                                            "...et son explosion cosmique consume tout dans une supernova dévastatrice, vous élevant dans une explosion interstellaire !",
                                            "...et son explosion cosmique critique crée une explosion galactique, vous éradiquant dans une conflagration cosmique !!",
                                            0, 0],
            "Missile Arcanique": [90, 12, 30, 3, 0, "L'ennemi invoque des projectiles arcaniques tourbillonnants, les lançant dans votre direction...",
                                "...mais les projectiles arcaniques se dispersent dans l'air sans vous toucher.",
                                "...et les projectiles arcaniques vous frappent avec une force magique, vous infligeant des dégâts !",
                                "...et les projectiles arcaniques vous ciblent avec précision, vous laissant vulnérable à leur magie mortelle !!",
                                0, 0],
            "Flamme Avancée": [80, 10, 27, 3, 15, "L'ennemi canalise le feu ardent, créant une vague de flammes dévastatrices qui vous engloutissent...",
                                            "...mais les flammes sont dissipées par votre résistance au feu, vous protégeant des dégâts.",
                                            "...et les flammes vous brûlent avec une intensité infernale, vous laissant marqué par leur chaleur !",
                                            "...et les flammes vous engloutissent dans un brasier de destruction, vous réduisant en cendres dans un spectacle apocalyptique !!",
                                            4, 5],
            "Claquement de Foudre": [95, 6, 10, 4, 10, "L'ennemi invoque un éclair en claquant des doigts, le dirigeant droit vers vous avec un geste rapide...",
                                                "...mais votre agilité vous permet d'éviter l'éclair, le laissant frapper le sol sans vous toucher.",
                                                "...et l'éclair vous frappe avec une décharge électrique, vous infligeant des dégâts d'électricité !",
                                                "...et l'éclair vous cible avec précision, vous laissant secoué par sa puissance électrique !!",
                                                2, 0],
            "Coup de Foudre": [80, 16, 20, 5, 15, "L'ennemi invoque une version supérieure du claquement de foudre, déclenchant une tempête électrique sur vous...",
                                                "...mais votre résistance à la foudre vous protège des dégâts de l'orage, vous laissant indemne.",
                                                "...et l'orage électrique vous frappe avec une force titanesque, vous électrocutant avec sa puissance dévastatrice !",
                                                "...et l'orage vous cible avec précision, vous laissant paralysé par la foudre qui vous consume !!",
                                                2, 0],
            "Rituel Canope": [85, 10, 20, 4, 8, "L'ennemi invoque le dieu égyptien Horus, maître de la foudre, à travers un rituel mystique, lançant un sort pour potentiellement vous paralyser...",
                                            "...mais votre volonté forte vous protège de l'effet paralysant du rituel, vous permettant de résister à sa magie.",
                                            "...et le rituel invoque des éclairs célestes pour vous punir, vous infligeant des dégâts d'électricité !",
                                            "...et le rituel critique invoque la colère divine, vous paralysant dans une tourmente d'éclairs et de tonnerre !!",
                                            3, 0],
            "Froideur d'Outretombe": [90, 5, 40, 5, 15, "L'ennemi canalise un froid glacial de l'outretombe, enveloppant tout dans un gel éternel...",
                                    "...mais vous esquivez habilement l'attaque, vous échappant au piège de la glace.",
                                    "...et vous êtes gelé jusqu'aux os, vous laissant engourdi et vulnérable !",
                                    "...et une force sinistre vous enserre dans un étau de gel mortel !!",
                                    3, 0],
            "Cercueil de Neige": [90, 9, 50, 8, 17, "L'ennemi invoque un cercueil de neige glaciale, l'enveloppant dans une tempête de poudreuse...",
                                    "...mais vous évitez de justesse l'emprisonnement, vous frayant un chemin à travers la tempête de neige.",
                                    "...et il vous engloutit, vous piégeant dans un monde de froid et d'obscurité !",
                                    "...et une avalanche dévastatrice vous submerge sous un flot de neige et de glace !!",
                                    4, 0],
            "Gel": [85, 8, 20, 10, 10, "L'ennemi vous enveloppe dans un gel paralysant, figeant vos mouvements dans un étau de glace...",
                                    "...mais vous brisez l'emprise glaciale, vous libérant de l'emprisonnement de la glace.",
                                    "...et le gel vous pétrifie, vous laissant vulnérable et impuissant face à l'ennemi !",
                                    "...et vous êtes immobilisé dans un bloc de gel implacable !!",
                                    3, 0],
            "Giga Gel": [85, 13, 25, 8, 20, "L'ennemi libère une vague de gel dévastatrice, transformant tout en son passage en une toundra gelée...",
                                    "...mais vous parvenez à esquiver la vague de gel, vous échappant des griffes du froid.",
                                    "...et le giga gel vous engloutit, vous piégeant dans une tempête glaciale de désespoir !",
                                    "...et un étau de glace implacable vous figeant !!",
                                    4, 0],
            "Oméga Gelure": [90, 17, 35, 6, 25, "L'ennemi invoque l'essence même du froid, créant une glaciation totale dans son sillage...",
                                    "...mais vous parvenez à échapper à la glaciation, vous préservant de la tempête glaciale.",
                                    "...et l'oméga gelure vous engloutit dans une tourmente glaciale, vous enveloppant dans un hiver éternel !",
                                    "...et vous condamnant à un sommeil éternel sous un manteau de neige !!",
                                    5, 0],
            "Oméga Lapidation": [85, 17, 35, 6, 15, "L'ennemi invoque une pluie de pierres, transformant le champ de bataille en un chaos de roche...",
                                    "...mais vous parvenez à éviter les projectiles, vous préservant des assauts de la nature.",
                                    "...et vous êtes assailli sous une cascade de pierres, vous laissant meurtri et blessé !",
                                    "...et une tempête de roche vous brise sous le poids de la lapidation !!",
                                    100, 0],
            "Oméga Saignée": [90, 18, 35, 6, 15, "L'ennemi ouvre des plaies béantes dans le tissu de la réalité, provoquant un appel d'air et de force...",
                                    "...mais vous parvenez à résister à l'assaut, vous protégeant des attaques sanglantes.",
                                    "...qui vous fait saigner à blanc, vous vidant de votre force et de votre vitalité !",
                                    "...qui vous condamne à subir un drain de vie inarrêtable !!",
                                    8, 0],
            "Mache": [90, 10, 10, 10, 0, "L'ennemi vous engloutit entièrement, vous mâchant avant de vous recracher...",
                        "...mais vous parvenez à vous libérer de ses mâchoires, échappant de justesse à une fin dévorante.",
                        "...et vous êtes soumis à la mastication implacable de l'ennemi, vous laissant meurtri et blessé !",
                        "...et une force vorace vous dévore dans un festin macabre !!",
                        0, 0],
            "Houken": [88, 15, 15, 5, 0, "L'ennemi libère un coup tranchant de houken, fendant l'air dans un éclair dévastateur...",
                                "...mais vous esquivez habilement le coup, évitant de justesse d'être coupé en deux.",
                                "...et le houken vous balaie d'un coup puissant, vous laissant marqué par son passage !",
                                "...et une lame d'acier vous coupe en deux dans un éclat de lumière divine !!",
                                0, 0],
            "Poing de Mana": [95, 6, 25, 4, 0, "L'ennemi canalise le pouvoir du mana dans son poing, déclenchant un coup explosif...",
                                    "...mais vous parvenez à contrer l'attaque, dissipant l'énergie du poing de mana.",
                                    "...et le poing de mana vous frappe avec une force magique, vous laissant secoué et désorienté !",
                                    "...et une explosion d'énergie vous consume dans un tourbillon de mana !!",
                                    0, 0],
            "Tir Arcanique": [95, 5, 30, 2, 0, "L'ennemi tire une flèche chargée d'arcane, déchirant l'air avec une précision mortelle...",
                                    "...mais vous déviez habilement la flèche, évitant de justesse d'être transpercé.",
                                    "...et la flèche d'arcane vous frappe avec une force mystique, vous laissant affaibli et vulnérable !",
                                    "...et une salve de flèches d'arcane vous transperce dans un éclair de magie !!",
                                    0, 0],
            "Explosion": [95, 8, 30, 5, 0, "L'ennemi déclenche une explosion dévastatrice, consumant tout sur son passage...",
                                "...mais vous parvenez à vous éloigner de l'explosion, évitant de justesse d'être englouti par les flammes.",
                                "...et l'explosion vous frappe avec une force cataclysmique, vous laissant brûlé et meurtri !",
                                "...et une détonation massive vous déchire dans un éclair de destruction !!",
                                0, 0],
            "Point Vital": [50, 20, 10, 10, 0, "L'ennemi cible directement votre point vital, visant à frapper là où ça fait mal...",
                        "...mais vous parvenez à protéger votre point faible, évitant de subir des dommages critiques.",
                        "...et l'attaque atteint votre point vital, vous laissant vulnérable et affaibli !",
                        "...et une frappe précise déchire votre point vital dans un éclair de douleur !!",
                        0, 0],
            "Son Rapide": [80, 10, 30, 8, 0, "L'ennemi libère un son rapide, déchiquetant l'air avec une rapidité effarante...",
                                    "...mais vous parvenez à résister au son rapide, protégeant vos tympans de l'assaut sonore.",
                                    "...et le son rapide vous assaille avec une force assourdissante, vous laissant désorienté et étourdi !",
                                    "...et une vague sonore déchire vos sens dans un tourbillon de cacophonie !!",
                                    0, 0],
            "Bombe Arcanique": [90, 6, 30, 5, 0, "L'ennemi lance une bombe chargée d'arcane, détonant dans un éclair de magie dévastateur...",
                                        "...mais vous parvenez à esquiver la bombe arcanique, évitant de justesse d'être consumé par sa puissance.",
                                        "...et la bombe arcanique vous frappe avec une force mystique, vous laissant brûlé et meurtri !",
                                        "...et une explosion magique vous engloutit dans un tourbillon de pouvoir arcanique !!",
                                        0, 0]
        }
        self.annuaire_de_caracteristique_des_sorts_speciaux_de_monstre = {
            # taux de reussite/soin minimum, tours d'effet/%soin, description, message si touche
            "Soin": [7, 8, "L'ennemi lance un sort de soin !", 
                     "Le mana l'enveloppe et il reprend des points de vie !"],
            "Feu Regénérateur": [8, 10, "L'ennemi invoque un feu régénérateur pour restaurer ses points de vie.", 
                                "Le feu répare ses os brisés et guérit ses blessures."],
            "Réglages d'Usine": [22, 11, "L'ennemi tente de réinitialiser ses points de vie avec des réglages d'usine.", 
                                "Une énergie mystérieuse enveloppe l'ennemi, le restaurant à son état optimal."],
            "Regénération Basaltique": [20, 10, "L'ennemi utilise les roches environnantes pour se régénérer.", 
                                        "Les minéraux du basalte fusionnent avec le corps de l'ennemi, guérissant ses blessures."],
            "Carotte Magique": [40, 15, "L'ennemi mange une carotte magique pour restaurer ses points de vie.", 
                                "Les enzymes de la carotte se répandent dans le corps de l'ennemi, le soignant et le revitalisant."],
            "Soin Avancé": [45, 21, "L'ennemi enveloppe son corps de mana pour soigner ses blessures.", 
                            "Les blessures de l'ennemi cicatrisent à l'aide du mana invoqué."],
            "Engloutis": [10 * self.numero_de_letage, 10, "L'ennemi engloutit un objet pour récupérer des points de vie.", 
                  "L'objet est absorbé par l'ennemi qui reprend des forces."],
            "Rejuvenation": [40, 20, "L'ennemi invoque un sort de réjuvenation pour se régénérer.", 
                            "Une lueur énergétique entoure l'ennemi, le revitalisant et réparant ses blessures."],
            "Tournicoti": [45, 21, "Tournicoti ! Tournicoti !\nL'ennemi tourne sur lui même et ses vêtements deviennent verts .", "Il reprend des points de vie !"],
            "Sonata Pitoyable": [18, 9, "L'ennemi utilise le sort Sonata Pitoyable !", "Un bruit pathétique enveloppe l'ennemi et apaise la douleur de ses blessures."],
            "Sonata Miséricordieuse": [30, 12, "L'ennemi utilise le sort Sonata Miséricordieuse !", 
                                       "Un son a peine apréciable se plaque contre sa peau et referme ses blessures."],
            "Sonata Sincère": [40, 15, "L'ennemi utilise le sort Sonata Sincère !", 
                               "Un chant cristallin inspire son esprit et revigore son corps."],
            "Sonata Bienveillante": [65, 15, "L'ennemi utilise le sort Sonata Bienveillante !", 
                                     "Une chorale glorieuse lui fait oublier les problèmes de sa situation et cicatrise ses blessures."],
            "Sonata Absolutrice": [85, 15, "L'ennemi utilise le sort Sonata Absolutrice !", 
                                   "Une mélodie féerique ramène son être tout entier a un état optimal."],

            "Oeuil Maudit": [30, 3, "L'ennemi se met a vous lancer un regard malveillant, empli de haine...", 
                                   "...mais vous le fixez sans broncher, jusqu'a ce qu'il détourne de lui même le regard.", 
                                   "...et des murmures malveillants se mettent a résonner dans votre esprit, semant le doute dans vos pensées."],
            "Possession du mana": [35, 4, "L'ennemi tente de s'approprier le flux de mana environnant...",
                                   "...mais il échappe a son controle",
                                   "...et il y arrive, le retournant contre vous."],
            "Ruée vers l'or": [50, 4, "L'ennemi vous stimule avec des effets sonores et lumineux, l'incitant à dépenser des pièces...", 
                               "...mais vous n'êtes pas très réceptif a ce genre de choses.", 
                               "...et fait naitre en vous les symptomes du Mal Jaune !"],
            "Confusion": [65, 3, "L'ennemi vous jette un sort de confusion...", 
                          "...mais il échoue.", 
                          "...et vos pensées deviennent aussi brouillées qu'un bruit de fond."],
        }

        # TECHNIQUES MONSTRE
        #TECHNIQUES GENERAlES
        self.techniques_de_feu_de_monstre = [
            "Poing de Feu",
            "Souffle de Feu",
            "Jet de Magma",
            "Ultralaser",
            "Lame de Feu",
            "Fleche Rouge",
            "Laser Ultime"
        ]
        self.techniques_de_foudre_de_monstre = [
            "Accrochage",
            "Pendule Etrange",
            
        ]
        self.techniques_de_glace_de_monstre = [
            "Morsure de Givre",
            "Lame de Gel",
            "Fleche Bleue"
        ]
        self.techniques_de_terre_de_monstre = [
            "Eboulis",
            "Tomberoche",
            "Coup de pierre"
        ]
        self.techniques_de_sang_de_monstre = [
            "Drain",
            "Lame Pourpre",
            "Ascension Runique",
            "Corruption",
        ]
        self.techniques_de_physique_de_monstre = [
            "Coup de Boule",
            "Frappe Lourde",
            "Attaque Légère",
            "Impact",
            "Coup de Griffe",
            "Morsure",
            "Gros Coup de Boule",
            "Avale",
            "Attaque Lourde",
            "Lame Courageuse",
            "Attaque Titanesque",
            "Lame Ultime",
            "Lame Vaillante"
        ]
        #TECHNIQUES SPECIALES
        self.techniques_de_soin_de_monstre = [
            "Lèche-Blessure",
            "Constructions du Zénith",
            "Gemme Rouge",
            "Medecine de Guerre",
            "Remede Divin",
            "Bouclier Ultime"
        ]
        self.techniques_de_blessure_de_monstre = [ # technique coute vie
            "Poing Eclat",
            "Coup du Foie"
        ]
        self.techniques_de_deconcentration_de_monstre = [ # sorts coute plus de mana
            ""
        ]
        self.techniques_de_gold_de_monstre = [ #action coute gold
            "Lame Dorée"
        ]
        self.techniques_de_instable_de_monstre = [ #pas de technique
            ""
        ]
        self.techniques_de_muet_de_monstre = [ # pas de sorts
            "Etranglement",
            "Brulevent"
        ]
        self.techniques_de_confusion_de_monstre = [ # pas d'item
            "Roulé-Boulet"
        ]
        #TECHNIQUES SUPPLEMENTAIRES
        self.techniques_supplementaire_de_monstre = [ 
            # sorts spéciaux ayant besoin de leur propre implémentation
            "Durcissement Argilite",
            "Envol",
            "Hurlement",
            "Attire-Gold",
            "Coup Anti-Magie",
            "Attire-Magie",
            "Aspiration",
            "Laser",
            "Roulette",
            "Jet d'Argent",
            "Gemme Bleue",
            "Durcissement Calcaire",
            "Combo Misérable",
            "Crystal Elémentaire",
            "Panacée Universelle",
            "Sables du Temps",
        ]
        #ANNUAIRE DE CARACTERISTIQUES ATTAQUES GENERALES ET SPECIALES
        self.annuaire_de_caracteristique_des_techniques_generales_de_monstre = {
            # %touche, degat, %crit, degat crit, %element, description, message si rate, si touche, si touche crit, nombre tours, effet element
            "Poing de Feu": [90, 5, 25, 5, 25, "L'ennemi lance un poing enflammé vers vous, laissant derrière lui une traînée de flammes...",
                       "...mais son poing s'écrase dans le vide, les flammes se dissipant dans l'air.",
                       "...et son poing enflammé vous frappe, provoquant une brûlure vive !",
                       "...et son poing enflammé s'abat violemment, engendrant une explosion de flammes dévastatrice !!",
                       4, 5],
            "Souffle de Feu": [85, 15, 30, 5, 30, "L'ennemi aspire profondément, puis libère un souffle brûlant sur vous...",
                                    "...mais son souffle de feu vous manque de peu, les flammes léchant l'air sans toucher.",
                                    "...et son souffle de feu vous englobe , les flammes laissant des marques de brûlure !",
                                    "...et son souffle de feu se transforme en une tempête infernale, vous engloutissant dans un brasier enragé !!",
                                    3, 8],
            "Jet de Magma": [88, 10, 30, 5, 25, "L'ennemi lance un jet de magma en fusion sur vous, la lave jaillissant avec force...",
                                    "...mais son jet de magma dévie de sa trajectoire, s'écrasant loin de sa cible.",
                                    "...et son jet de magma vous frappe de plein fouet, la lave brûlante faisant fondre tout sur son passage !",
                                    "...et son jet de magma se transforme en une cascade de lave en fusion, vous engloutissant dans un torrent de destruction !!",
                                    3, 12],
            "Ultralaser": [80, 17, 25, 5, 25, "L'ennemi charge une énergie intense dans ses yeux, puis libère un rayon laser destructeur sur sa cible...",
                                "...mais son ultralaser vous manque de justesse, le rayon brûlant fendant l'air sans toucher.",
                                "...et son ultralaser vous frappe de plein fouet, laissant derrière un sillon de destruction !",
                                "...et son ultralaser se transforme en un rayon dévastateur, vous pulvérisant dans une explosion cataclysmique !!",
                                5, 5],
            "Lame de Feu": [85, 10, 40, 3, 20, "L'ennemi matérialise une lame de feu dans sa main, puis la lance avec force sur sa cible...",
                                "...mais sa lame de feu vous rate de peu, disparaissant dans un éclat de flammes.",
                                "...et sa lame de feu vous transperce, laissant une brûlure béante !",
                                "...et sa lame de feu se transforme en un raz-de-marée de flammes, vous déchirant dans une explosion de chaleur intense !!",
                                4, 5],
            "Fleche Rouge": [100, 3, 20, 15, 100, "L'ennemi tire une flèche enflammée sur sa cible, la pointe rougeoyante filant à toute vitesse...",
                                    "...mais elle manque sa cible de justesse, se perdant dans l'horizon.",
                                    "...et elle trouve sa cible , vous causant une brûlure vive !",
                                    "...et elle se transforme en une pluie de projectiles ardents, vous criblant dans une déferlante de flammes !!",
                                    4, 5],
            "Laser Ultime": [75, 15, 20, 7, 10, "L'ennemi concentre toute son énergie dans un rayon laser colossal, puis le déchaîne sur sa cible...",
                                    "...mais son laser ultime vous rate de peu, l'énergie dévastatrice s'éparpillant dans l'air.",
                                    "...et son laser ultime vous frappe avec une force inouïe, laissant derrière un cratère fumant !",
                                    "...et son laser ultime se transforme en une décharge d'énergie cosmique, vous pulvérisant dans une explosion apocalyptique !!",
                                    8, 5],
            "Accrochage": [80, 10, 30, 7, 10, "L'ennemi se jette sur vous, s'accrochant fermement à votre tête et déclenchant des décharges électriques...",
                       "...mais vous le prenez a deux mains et le décrochez, son attaque électrique s'évaporant dans l'air.",
                       "...vous laissant tremblant de spasmes !",
                       "...et s'accrochant fermement, il décharge une énergie électrique dévastatrice, vous paralysant dans une torpeur électrique !!",
                       2, 0],
            "Pendule Etrange": [85, 17, 30, 5, 15, "L'ennemi active une étrange pendule, manipulant le temps autour de sa cible...",
                            "...mais son pendule étrange ne produit aucun effet, le temps continuant de s'écouler normalement.",
                            "...et son pendule étrange vous enveloppe dans un voile temporel, faisant revivre a vos muscles les signaux électriques des dernieres heures en un instant !",
                            "...et activant pleinement son pendule, il crée une boucle temporelle dévastatrice, "
                            "faisant revivre a vos muscles les signaux électriques des dernieres heures en un instant, une centaine de fois !!",
                            2, 0],
            "Morsure de Givre": [90, 16, 35, 8, 20, "L'ennemi plonge ses crocs glacés dans votre chair, drainant votre chaleur vitale...",
                      "...mais il manque son coup, son souffle glacé se dissipant dans l'air.",
                      "...et il vous touche, glaçant vos membres !",
                      "...et frappant avec force, il vous transperce de ses crocs glacés, vous laissant frissonnant !!",
                      4, 0],
            "Lame de Gel": [85, 10, 25, 5, 20, "L'ennemi charge avec sa lame de gel, prêt à vous geler et à drainer votre vitalité...",
                            "...mais il rate son coup, sa lame de gel s'émoussant sur le sol.",
                            "...et il vous touche, glaçant votre chair et drainant votre force vitale !",
                            "...et frappant avec force, il vous transperce de sa lame gelée, drainant votre vie et vous laissant engourdis et affaiblis !!",
                            4, 0],
            "Fleche Bleue": [100, 3, 10, 15, 100, "L'ennemi décoche une flèche glaciale vers vous, prête à vous geler et à drainer votre vie...",
                                "...mais sa flèche manque sa cible de justesse, fondant en gouttes d'eau glacée.",
                                "...et il vous touche, figeant votre sang et drainant votre vitalité !",
                                "...et avec une précision mortelle, il vous transperce de sa flèche de glace, drainant votre vie et vous laissant frigorifiés et affaiblis !!",
                                5, 0],
            "Coup de pierre": [85, 13, 20, 7, 25, "L'ennemi assène un coup de poing solide sur vous, imprégné de l'énergie de la terre pour vous briser...",
                      "...mais son coup de poing rate sa cible, s'écrasant sur le sol dans un fracas de pierre.",
                      "...et il vous touche, vous secouant violemment et vous brisant !",
                      "...et avec une force titanesque, il vous frappe avec un coup de pierre, vous laissant brisés et affaiblis !!",
                      85, 0],
            "Eboulis": [90, 8, 25, 3, 15, "L'ennemi déclenche un éboulement de roches sur vous, prêt à vous submerger et vous briser...",
                        "...mais son éboulis manque sa cible, les roches se brisant sur le sol.",
                        "...et il vous touche, vous ensevelissant sous les décombres et vous broyant !",
                        "...et avec un rugissement puissant, il vous ensevelit sous un torrent de pierres, vous laissant écrasés et affaiblis !!",
                        90, 0],
            "Tomberoche": [90, 18, 35, 7, 20, "L'ennemi lève une énorme roche au-dessus de votre tête, prêt à l'abattre sur vous pour vous écraser...",
                            "...mais sa tomberoche rate sa cible de peu, s'écrasant à côté dans un bruit sourd.",
                            "...et il vous touche, écrasant votre corps sous le poids de la roche et vous brisant !",
                            "...et avec un coup dévastateur, il vous écrase sous la tomberoche, vous laissant écrasés et affaiblis !!",
                            110, 0],
            "Drain": [80, 15, 20, 4, 20, "L'ennemi utilise un sort de drain, aspirant votre énergie vitale pour se renforcer...",
                        "...mais son sort de drain ne vous atteint pas, se dissipant dans l'air.",
                        "...et il vous touche, aspirant votre force vitale pour se renforcer !",
                        "...et avec une habileté malveillante, il vous draine de votre vie, se renforçant alors que vous vous affaiblissez !!",
                        5, 0],
            "Lame Pourpre": [85, 15, 20, 5, 20, "L'ennemi dégaine une lame sombre imprégnée de puissance vitale, prêt à vous trancher et à drainer votre vie...",
                      "...mais sa lame pourpre rate sa cible de justesse, glissant dans l'air sans vous toucher.",
                      "...et il vous touche, vous tranchant avec sa lame maudite et drainant votre vie !",
                      "...et avec une précision mortelle, il vous frappe de sa lame pourpre, vous drainant de votre vie et se renforçant !!",
                      8, 0],
            "Ascension Runique": [85, 17, 25, 3, 23, "L'ennemi invoque des runes sanguines pour une ascension sinistre, drainant votre énergie vitale pour se renforcer...",
                        "...mais son invocation échoue, les runes s'évaporant dans l'air sans effet.",
                        "...et il vous touche, drainant votre énergie vitale alors qu'il s'élève en puissance !",
                        "...et avec un rituel démoniaque, il vous aspire de votre vitalité, se renforçant tandis que vous vous affaiblissez !!",
                        7, 0],

            "Coup de Boule": [95, 5, 25, 3, 10, "L'ennemi s'approche de vous et envoie un gros coup de boule !", 
                              "Mais vous esquivez le coup !", 
                              "Et vous vous le prenez en pleine tronche !", 
                              "Et il vous envoie valser !", 0, 0],
            "Frappe Lourde": [65, 10, 15, 8, 0, "L'ennemi lève son arme lourde et s'apprête à vous frapper avec une force dévastatrice...",
                      "...mais son attaque puissante manque sa cible, vous laissant indemne.",
                      "...et il vous touche de plein fouet avec sa frappe lourde, vous infligeant des dégâts massifs !",
                      "...et avec un coup dévastateur, il vous frappe violemment, vous causant d'énormes dégâts !!",
                      0, 0],
            "Attaque Légère": [95, 5, 25, 2, 0, "L'ennemi effectue une attaque rapide et légère...",
                                    "...mais elle n'atteint pas sa cible, vous laissant indemne.",
                                    "...et il vous touche avec son attaque légère, vous infligeant des dégâts mineurs.",
                                    "...et avec une attaque précise, il vous touche légèrement, vous causant quelques dégâts !",
                                    0, 0],
            "Impact": [85, 10, 34, 4, 0, "L'ennemi charge vers vous, prêt à vous asséner un coup puissant...",
                        "...mais son attaque brutale manque sa cible, vous laissant intact.",
                        "...et il vous frappe de plein fouet avec son impact violent, vous infligeant des dégâts considérables !",
                        "...et avec une force surhumaine, il vous frappe avec son impact, vous causant d'énormes dégâts !!",
                        0, 0],
            "Coup de Griffe": [90, 12, 25, 4, 0, "L'ennemi vous attaque avec ses griffes acérées, cherchant à vous lacérer...",
                                    "...mais son coup de griffe rate sa cible, vous laissant indemne.",
                                    "...et il vous griffe violemment, vous infligeant des dégâts tranchants.",
                                    "...et avec un mouvement rapide, il vous frappe de ses griffes, vous causant des dégâts !",
                                    0, 0],
            "Morsure": [83, 8, 20, 4, 0, "L'ennemi tente de vous mordre avec ses crocs aiguisés, cherchant à vous infliger des blessures profondes...",
                            "...mais sa morsure manque sa cible, vous laissant hors de danger.",
                            "...et il vous mord avec ferveur, vous infligeant des dégâts perforants.",
                            "...et avec une morsure vicieuse, il vous attaque, vous causant des dégâts !",
                            0, 0],
            "Gros Coup de Boule": [83, 15, 20, 5, 0, "L'ennemi se prépare à vous asséner un coup de boule brutal...",
                                        "...mais son coup de tête échoue, vous laissant indemne.",
                                        "...et il vous frappe d'un coup de tête massif, vous infligeant des dégâts considérables.",
                                        "...et avec un impact dévastateur, il vous assène un coup de boule, vous causant d'énormes dégâts !!",
                                        0, 0],
            "Avale": [86, 13, 25, 3, 0, "L'ennemi ouvre grand sa gueule, prêt à vous engloutir...",
                        "...mais vous esquivez au dernier moment, et il ne croque que le sol.",
                        "...et il vous avale d'un coup, vous infligeant des dégâts internes.",
                        "...et avec un appétit vorace, il vous engloutit, vous causant des dégâts !",
                        0, 0],
            "Attaque Lourde": [80, 7, 10, 4, 0, "L'ennemi prépare une attaque puissante, cherchant à vous submerger sous la force de son assaut...",
                                    "...mais son attaque lourde manque sa cible, vous laissant indemne.",
                                    "...et il vous touche avec son attaque massive, vous infligeant des dégâts importants.",
                                    "...et avec un coup colossal, il vous frappe violemment, vous causant d'énormes dégâts !!",
                                    0, 0],
            "Lame Courageuse": [90, 14, 20, 3, 0, "L'ennemi brandit son épée avec courage, prêt à vous affronter...",
                          "...mais son coup courageux manque sa cible, vous laissant indemne.",
                          "...et il vous frappe avec bravoure, vous infligeant des dégâts significatifs.",
                          "...et avec une attaque héroïque, il vous touche avec force, vous causant des dégâts !",
                          0, 0],
            "Attaque Titanesque": [90, 17, 10, 5, 0, "L'ennemi rassemble sa force pour une attaque titanesque, cherchant à vous anéantir...",
                                        "...mais son attaque gigantesque rate sa cible, vous laissant indemne.",
                                        "...et il vous frappe avec une puissance colossale, vous infligeant des dégâts monumentaux.",
                                        "...et avec une attaque d'une intensité dévastatrice, il vous frappe avec une force titanesque, vous causant des dégâts énormes !!",
                                        0, 0],
            "Lame Ultime": [80, 20, 20, 6, 0, "L'ennemi déchaîne son attaque ultime, faisant briller son arme d'une lueur éclatante...",
                                    "...mais son coup ultime manque sa cible, vous laissant indemne.",
                                    "...et il vous touche avec son attaque suprême, vous infligeant des dégâts incommensurables.",
                                    "...et avec une frappe transcendante, il vous attaque avec une force ultime, vous causant des dégâts cataclysmiques !!",
                                    0, 0],
            "Lame Vaillante": [85, 22, 30, 8, 0, "L'ennemi attaque vaillamment avec son épée, cherchant à vous vaincre avec courage...",
                                    "...mais son coup vaillant manque sa cible, vous laissant indemne.",
                                    "...et il vous frappe avec courage, vous infligeant des dégâts vaillants.",
                                    "...et avec une attaque intrépide, il vous touche avec vaillance, vous causant des dégâts !",
                                    0, 0],
            "Corruption": [85, 15, 25, 7, 0, "L'ennemi vous regarde avec un regard sinistre, invoquant des forces sombres pour corrompre votre essence...",
                         "...mais son attaque de corruption échoue, ne parvenant pas à altérer votre force vitale.",
                         "...et il réussit à corrompre votre être, drainant lentement votre vitalité avec des ténèbres maléfiques.",
                         "...et avec une puissance sinistre, il vous corrompt profondément, drainant votre vie avec une force maléfique !!",
                         0, 0],
        }
        self.annuaire_de_caracteristique_des_techniques_speciales_de_monstre = {
            # degats/soin minimum, taux de reussite, tours d'effet/pourcentage de soin, description, message si rate, message si touche
            "Lèche-Blessure": [30, 75, 8, "L'ennemi lèche ses blessures...",
                              "...mais rien ne se passe.",
                              "...et elles commencent a se refermer !"],
            "Constructions du Zénith": [30, 85, 10, "L'ennemi tente de reconfigurer les parties de son corps...",
                                                "...mais il échoue.",
                                                "...et les organes les plus touchés sont alors protégés et soignés en priorité !"],
            "Gemme Rouge": [40, 80, 10, "L'ennemi utilise une gemme rouge pour se soigner...",
                                        "...mais rien ne se passe.",
                                        "...et elle se met a émettre une lumière apaisante, le soignant !"],
            "Medecine de Guerre": [35, 75, 10, "L'ennemi s'administre une médecine de guerre pour récupérer de ses blessures...",
                                                "...sans succès.",
                                                "...et il parvient a se rétablir juste assez pour terminer le combat !"],
            "Remede Divin": [50, 100, 13, "L'ennemi avale un remède divin pour restaurer sa santé...",
                                        "...en oubliant qu'il ne le digère pas.",
                                        "...et reprend beaucoup de vie !"],
            "Bouclier Ultime": [100, 60, 15, "L'ennemi érige un bouclier ultime pour se protéger et récupérer de ses blessures...",
                                            "...et tombe en avant sous le poids de l'objet.",
                                            "...et il enveloppe l'ennemi, le protégeant et le soignant."],

            "Poing Eclat": [7, 85, 4, "Le monstre vous assène un puissant coup de poing qui explose en une pluie d'éclats acérés...",
                            "...mais les éclats se dispersent dans l'air sans vous toucher .",
                            "...et vous êtes criblé de blessures alors que les éclats s'enfoncent profondément dans votre chair !"],
            "Coup du Foie": [17, 75, 4, "Le monstre vous frappe violemment au niveau du foie...",
                                        "...mais l'attaque rate son objectif de peu .",
                                        "...et vous sentez une douleur lancinante alors que le coup vous blesse et vous handicape !"],
            "Lame Dorée": [15, 85, 5, "Le monstre vous attaque avec une lame dorée étincelante...",
                            "...mais son attaque manque sa cible, vous laissant indemne.",
                            "...et vous sentez une étrange sensation de malaise alors que la lame vous infecte d'une maladie sournoise !"],
            "Etranglement": [5, 70, 3, "L'ennemi s'enroule autour de votre cou...", 
                             "...mais vous arrivez a vous débarrasser de son étreinte.", 
                             "...et vous étrangle sans ménagement."],
            "Brulevent": [7, 70, 2, "Le monstre libère un souffle ardent qui consume tout l'oxygène de la salle...",
                          "...mais vous parvenez à éviter de justesse le souffle brûlant.",
                          "...et vous vous retrouvez soudainement incapable de parler alors que la chaleur envahit votre gorge !"],
            "Roulé-Boulet": [20, 75, 5, "Le monstre se met en boule et vous percute avec une force dévastatrice, vous envoyant valser à travers la pièce...",
                             "...mais vous parvenez à encaisser le coup sans trop de dommages, vous permettant de rester sur vos gardes.",
                            "...et vous vous retrouvez étourdi et désorienté, votre esprit confus par le choc violent !"],

        }
        self.liste_de_commentaire_pour_catastrophe = [
            "...ce qui fait trembler la salle... ",
            "...ce qui fait se dévisser un écrou... ",
            "...ce qui fait rouler un balle... ",
            "...ce qui fragilise un pavé... ",
            "...ce qui fait bouger un insecte... ",
            "...ce qui fait tomber un lustre... ",
            "...ce qui fait pression sur un morceau de bois... ",
            "...ce qui fait une étincelle... ",
            "...ce qui fait tourner une roue... ",
            "...ce qui fait rebondir une bille... ",
            "...ce qui fait peur a l'autruche... ",
            "...ce qui fait rigoler Alfred... ",
            "...ce qui fait dire une phrase au cactus... ",
            "...ce qui fait voler un avion en papier... ",
            "...ce qui remplis une gourde avec une goutte d'eau... ",
            "...ce qui fait contrepoid sur la balance... ",
            "...ce qui fait décoller une amende pour stationnement interdite sur le mur de la salle... ",
            "...ce qui fait se poser une mouche sur le mix de fléchette bleue et rouge enclenchée dans l'arbalette cachéee dans le mur et prête a etre déclenchée a la fin de cette attaque... ",
            "...ce qui draine le developpeur de son imagination pour inventer d'autres phrases a mettre dans ce running gag... ",
            "...ce qui alerte l'attention du gouvernement sur le problème des gens qui appellent un pain au chocolat une chocolatine ... ",
            "...ce qui fait de cette phrase la 21ème et dernière a être écrite dans la liste de commentaire possible a recevoir... ",
        ]


        # Constantes Bonus
        self.CHANCEDETOUCHERBONUS = 0
        self.DEGATBONUSSORTS = 0
        self.DEGATBONUSATTAQUE = 0
        self.DEGATBONUSSORTCRITIQUE = 0
        self.DEGATBONUSATTAQUECRITIQUE = 0
        self.DEGATBONUSATTAQUEFEU = 0
        self.DEGATBONUSSORTFEU = 0
        self.DEGATBONUSFEU = 0
        self.DEGATBONUSATTAQUEFOUDRE = 0
        self.DEGATBONUSSORTFOUDRE = 0
        self.DEGATPARALYSIE = 0
        self.DEGATFEUELECTRIQUE = 0
        self.DEGATBONUSATTAQUEGLACE = 0
        self.DEGATBONUSSORTGLACE = 0
        self.DEGATGELURE = 0
        self.DEGATBONUSATTAQUETERRE = 0
        self.DEGATBONUSSORTTERRE = 0
        self.DEGATLAPIDATION = 0
        self.DEGATBONUSATTAQUEPHYSIQUE = 0
        self.DEGATBONUSSORTPHYSIQUE = 0
        self.DEGATBONUSATTAQUESANG = 0
        self.DEGATBONUSSORTSANG = 0
        self.DEGATTECHNIQUEBONUSDUMONSTRE = 0 #===
        self.DEGATSORTBONUSDUMONSTRE = 0 #===
        self.DEGATSAIGNEE = 0
        self.SOINSSAIGNEE = 0
        self.PIRADEGAT = 0
        self.PIRABRULE = 0
        self.PIRABRULETOUR = 0
        self.ELEKTRONDEGAT = 0
        self.ELEKTRONPARALYSE = 0
        self.ELEKTRONPARALYSETOUR = 0
        self.TSUMETASADEGAT = 0
        self.TSUMETASAGELE = 0
        self.TSUMETASAGELETOUR = 0
        self.MATHAIRDEGAT = 0
        self.MATHAIRLAPIDE = 0
        self.FOSDEGAT = 0
        self.HADDEEDEGAT = 0
        self.HADDEEDRAIN = 0
        self.CHANCESORTCRITIQUEDUMONSTRE = 0 #===
        self.CHANCECOUPCRITIQUEDUMONSTRE = 0 #===
        self.CHANCECOUPCRITIQUE = 0
        self.CHANCESORTCRITIQUE = 0
        self.CHANCEBONUSESQUIVE = 0
        self.CHANCEBONUSDEFAIREBRULER = 0
        self.CHANCEBONUSDEFAIREPARALYSER = 0
        self.CHANCEBONUSDEFAIREGELER = 0
        self.CHANCEBONUSDEFAIRELAPIDER = 0
        self.CHANCEBONUSDEFAIRESAIGNER = 0
        self.CHANCERATERATTAQUE = 0
        self.CHANCERATERSORT = 0
        self.TOURBONUSENNEMIENFEU = 0
        self.TOURBONUSENNEMIENGLACE = 0
        self.TOURBONUSENNEMIENPARALYSIE = 0
        self.TOURBONUSJOUEURENFEU = 0 #===
        self.TOURBONUSJOUEURENGLACE = 0 #===
        self.TOURBONUSJOUEURENPARALYSIE = 0 #===
        self.DEGATBONUSITEM = 0
        self.SUPPORTBONUSITEM = 0
        self.CHANCEBONUSJOUEURPARALYSE = 0 #===
        self.CHANCEBONUSJOUEURENFEU = 0 #===
        self.CHANCEBONUSJOUEURENGLACE = 0 #===
        self.CHANCEBONUSJOUEURENSANG = 0 #===
        self.CHANCEBONUSJOUEURLAPIDE = 0 #===
        self.BONUSREDUCTIONDEGAT = 0
        self.BONUSREDUCTIONDEGATSURJOUEUR = 0 #====
        self.BONUSREDUCTIONMANASORTTOUT = 0
        self.BONUSREDUCTIONMANASORTTERRE = 0
        self.BONUSREDUCTIONMANASORTFOUDRE = 0
        self.BONUSREDUCTIONMANASORTFEU = 0
        self.BONUSCOUTMALEDICTIONMANA = 0
        self.BONUSCOUTMALEDICTIONVIEOUGOLD = 0

        # a la fin on a stocké dans le modèle :

        # - une liste d'attaque  :   self.techniques
        # - une liste de sorts :     self.sorts
        # - un dictionnaire
        #   avec nom d'objet et     self.items
        #   quantité :
        # - une floppée de          les caractéristiques
        #   marqueurs Booléens      les altérations d'état et influence d'objet
        #   concernant :            les influences de l'arbre de talent
        #                           les talents issus de fusions
        #                           les stigmas du joueur (non booleens)
        #                           le tour en cours et la derniere attaque
        #
        # -une flopee de            celles utilisees pour calculer
        #    "constantes" :         les bonus/malus des attaques/sorts
        #
        #
        # -un dictionnaire des couts des attaques
        #
        #
        # A faire :
        #
        #
        #
        #Faire secret des quetes                                  | MAINTENANT
        #Faire livres de bibliotheque finale et secret des livres |
        #
        #
        #                           S'assurer que tout les stigmas soient                          |
        #                                                   implementés                            |
        #                                        (6/6*) (15/15+) (15/15-)                          |
        #                                        (0/8*) (0/29+) (0/29-)                            | 
        #mettre trucs secret dans observation pour relier a indices (wip)                          |
        #faire dessin indice (wip)                                                                 | POUR LA PROCHAINE UPDATE
        #relier dessin indice a recup (wip)                                                        |
        #faire dessin redcoin (wip)                                                                |
        #relier dessin a recup  (wip)                                                              |
        #faire les observations (wip)                                                              |
        #faire les intro/intro rez des boss secrets (wip)                                          |
        #faire les systemes de données transverssées a travers les runs (genre bibliotheque) (wip) |
        #faire message de mort des ennemis (wip)                                                   |
        #faire Vaati personnage d'entretien (wip)                                                  |
        #
        #
        #                           cleanup                                                                               |
        #                           Documention méthodes                                                                  | DERNIERE LIGNE DROITE (plus tard)


