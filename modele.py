import random
import os


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

        # alteration de letat ou influence d'artefacts
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

        # glossaire de techniques
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
        # %touche, degat, %crit, degat crit, %element, description, message si rate, si touche, si touche crit, nombre tours, effet element
        self.annuaire_de_caracteristique_des_techniques = {
            "Attaque Légère": [95, 7, 30, 4, 0, "Vous frappez l'ennemi avec peu de force, mais beaucoup de précision...", "...ce qui ne vous empeche pas de rater quand meme.", "..et le faites grimacer de douleur !", "et le faites reculer de plusieurs pas en arrière !!", 0, 0],
            "Lance Rapide": [80, 5, 10, 3, 5, "description", "rate", "touche", "touche crit", 0, 0],
            "Lance Statique": [80, 9, 10, 5, 5, "description", "rate", "touche", "touche crit", 0, 0],
            "Lance Electrique": [80, 13, 13, 5, 8, "description", "rate", "touche", "touche crit", 0, 0],
            "Lance de l'Eclair": [80, 17, 13, 8, 8, "description", "rate", "touche", "touche crit", 0, 0],
            "Lance Foudroyante": [80, 22, 16, 8, 10, "description", "rate", "touche", "touche crit", 0, 0],
            "Lance de la Mort Blanche": [80, 30, 16, 10, 13,
                                         "Vous chargez des millions de zettawats dans la pointe de votre lance avant de l'envoyer...",
                                         "...et manquez de peu le torse du monstre .",
                                         "...et brisez la jambe du monstre !",
                                         "...et embrochez violemment le corps du monstre !!",
                                         2,
                                         0],
            "Bô Chaud": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Bô Brulant": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Bô Enflammé": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Bô de la Fournaise": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Bô Magmatique": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Bô Solaire": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Katana Bleu": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Katana Froid": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Katana Givré": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Katana Glacial": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Katana Polaire": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Katana Zéro": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Corne Argile": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Corne Lapis": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Corne Granite": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Corne Obsidienne": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Corne de la Montagne": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Corne Continentale": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Poing Léger": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Poing Renforcé": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Poing Lourd": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Poing Maitrisé": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Poing Fatal": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Poing de la Comète": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Dague Volevie": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Dague Siphoneuse": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Dague Vampirique": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Dague Parasite": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Dague Destructrice": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Dague Créatrice": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
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
            "Sonata Pitoyable": 3,
            "Sonata Miséricordieuse": 5,
            "Sonata Empathique": 12,
            "Sonata Sincère": 17,
            "Sonata Bienveillante": 20,
            "Sonata Absolutrice": 25
        }
        self.annuaire_de_soin_minimum_des_sorts = {
            "Sonata Pitoyable": 8,
            "Sonata Miséricordieuse": 15,
            "Sonata Empathique": 20,
            "Sonata Sincère": 25,
            "Sonata Bienveillante": 33,
            "Sonata Absolutrice": 40
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
            "Tir Arcanique": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Faisceau Rapide": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Faisceau Statique": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Faisceau Electrique": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Faisceau de l'Eclair": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Faisceau Foudroyant": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Faisceau de la Mort Blanche": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Thermosphère Chaude": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Thermosphère Brulante": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Thermosphère Enflammée": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Thermosphère de la Fournaise": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Thermosphère Magmatique": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Thermosphère Solaire": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Pic Bleu": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Pic Froid": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Pic Givré": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Pic Glacial": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Pic Polaire": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Pic Zéro": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Création d'Argile": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Création de Lapis": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Création de Granite": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Création Obsidienne": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Création de la Montagne": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Création Continentale": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Explosion Légère": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Explosion Renforcée": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Explosion Lourde": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Explosion Maitrisée": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Explosion Fatale": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Explosion de la Comète": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Dance Volevie": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Dance Siphoneuse": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Dance Vampirique": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Dance Parasite": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Dance Destructrice": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Dance Créatrice": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
        }
        self.annuaire_de_cout_des_sorts = {
            "Tir Arcanique": 5,
            "Faisceau Rapide": 5,
            "Faisceau Statique": 5,
            "Faisceau Electrique": 5,
            "Faisceau de l'Eclair": 5,
            "Faisceau Foudroyant": 5,
            "Faisceau de la Mort Blanche": 5,
            "Thermosphère Chaude": 5,
            "Thermosphère Brulante": 5,
            "Thermosphère Enflammée": 5,
            "Thermosphère de la Fournaise": 5,
            "Thermosphère Magmatique": 5,
            "Thermosphère Solaire": 5,
            "Pic Bleu": 5,
            "Pic Froid": 5,
            "Pic Givré": 5,
            "Pic Glacial": 5,
            "Pic Polaire": 5,
            "Pic Zéro": 5,
            "Création d'Argile": 5,
            "Création de Lapis": 5,
            "Création de Granite": 5,
            "Création Obsidienne": 5,
            "Création de la Montagne": 5,
            "Création Continentale": 5,
            "Explosion Légère": 5,
            "Explosion Renforcée": 5,
            "Explosion Lourde": 5,
            "Explosion Maitrisée": 5,
            "Explosion Fatale": 5,
            "Explosion de la Comète": 5,
            "Dance Volevie": 5,
            "Dance Siphoneuse": 5,
            "Dance Vampirique": 5,
            "Dance Parasite": 5,
            "Dance Destructrice": 5,
            "Dance Créatrice": 5,
            "Rafale": 5,
            "Avalanche": 5,
            "Libération Enflammée": 5,
            "Libération Fulgurante": 5,
            "Libération Glaciale": 5,
            "Libération Sanglante": 5,
            "Libération Holomélanocrate": 5,
            "Mirroir d'Eau": 5,
            "Brume de Sang": 5,
            "Explosion de Feu Sacré": 5,
            "Carrousel": 5,
            "Sonata Pitoyable": 5, 
            "Sonata Miséricordieuse": 5,
            "Sonata Empathique": 5,
            "Sonata Sincère": 5,
            "Sonata Bienveillante": 5,
            "Sonata Absolutrice": 5
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
        self.monstre_points_de_vie = 20
        self.monstre_points_de_vie_max = 20
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
            "Labyrinthe",
        ]
        dir_path = os.path.dirname(os.path.realpath(__file__))
        musique = dir_path + "\\stuff\\"
        self.CHEMINABSOLUMUSIQUE = musique
        self.alfred_liste_questions = [
            {
                "Question": "pavé question",
                "Reponse 1": "pavé reponse 1",
                "Reponse 2": "pavé reponse 2",
                "Reponse 3": "pavé reponse 3",
                "Reponse 4": "pavé reponse 4",
                "Reponse a la question": 1,
            },
            {
                "Question": "pavé question",
                "Reponse 1": "pavé reponse 1",
                "Reponse 2": "pavé reponse 2",
                "Reponse 3": "pavé reponse 3",
                "Reponse 4": "pavé reponse 4",
                "Reponse a la question": 1,
            },
            {
                "Question": "pavé question",
                "Reponse 1": "pavé reponse 1",
                "Reponse 2": "pavé reponse 2",
                "Reponse 3": "pavé reponse 3",
                "Reponse 4": "pavé reponse 4",
                "Reponse a la question": 1,
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
            "Sonata",
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
        self.annuaire_de_caracteristique_des_sorts_generaux_de_monstre = {
            # %touche, degat, %crit, degat crit, %element, description, message si rate, si touche, si touche crit, nombre tours, effet element
            "Flamme": [95, 3, 20, 5, 50, "L'ennemi fait apparaitre une flamme sur votre position.", "Mais vous l'esquivez !", "Et elle vous brule !", "Et elle vous carbonise !", 3, 5],
            "Vents du Sud": [90, 5, 25, 5, 50, "L'ennemi invoque les vents brulants du Sud !", "Mais vous résistez aux temperatures extrêmes !", "Et vous commencez a bruler !", "Et vos membres s'embrases sur place !", 4, 5],
            "Flamme Avancée": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Thermosphère Brulante": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Thermosphère de la Fournaise": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Thermosphère Magmatique": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Thermosphère Solaire": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Claquement de Foudre": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Vents de l'Est": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Coup de Foudre": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Faisceau Statique": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Faisceau de l'Eclair": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Faisceau Foudroyant": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Rituel Canope": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Faisceau de la Mort Blanche": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Froideur d'Outretombe": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Cercueil de Neige": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Vents du Nord": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Gel": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Giga Gel": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Oméga Gelure": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Pic Froid": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Pic Glacial": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Pic Polaire": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Pic Zéro": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Oméga Lapidation": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Création de Lapis": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Création Obsidienne": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Création de la Montagne": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Création Continentale": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Vents de l'Ouest": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Oméga Saignée": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Mache": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Dance Siphoneuse": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Dance Parasite": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Houken": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Dance Destructrice": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Dance Créatrice": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Poing de Mana": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Tir Arcanique": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Explosion": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Point Vital": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Son Rapide": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Bombe Arcanique": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Jugement": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Explosion Renforcée": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Explosion Maitrisée": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Missile Arcanique": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Explosion Fatale": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Explosion de la Comète": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0]
        }
        self.annuaire_de_caracteristique_des_sorts_speciaux_de_monstre = {
            # taux de reussite/soin minimum, tours d'effet/%soin, description, message si touche
            "Soin": [5, 5, "L'ennemi lance un sort de soin !", "Le mana l'enveloppe et il reprend des points de vie !"],
            "Feu Regénérateur": [0, 0, "description", "touche"],
            "Réglages d'Usine": [0, 0, "description", "touche"],
            "Regénération Basaltique": [0, 0, "description", "touche"],
            "Carotte Magique": [0, 0, "description", "touche"],
            "Soin Avancé": [0, 0, "description", "touche"],
            "Engloutis": [0, 0, "description", "touche"],
            "Sonata": [0, 0, "description", "touche"],
            "Rejuvenation": [0, 0, "description", "touche"],
            "Sonata Miséricordieuse": [0, 0, "description", "touche"],
            "Sonata Sincère": [0, 0, "description", "touche"],
            "Tournicoti": [0, 0, "description", "touche"],
            "Sonata Bienveillante": [0, 0, "description", "touche"],
            "Sonata Absolutrice": [0, 0, "description", "touche"],
            "Possession du mana": [0, 0, "description", "rate", "touche"],
            "Oeuil Maudit": [0, 0, "description", "rate", "touche"],
            "Ruée vers l'or": [0, 0, "description", "rate", "touche"],
            "Confusion": [0, 0, "description", "rate", "touche"],
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
            "Ascension Runique"
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
            "Corruption",
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
            "Poing de Feu": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Souffle de Feu": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Jet de Magma": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Ultralaser": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Lame de Feu": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Fleche Rouge": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Laser Ultime": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Accrochage": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Pendule Etrange": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Morsure de Givre": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Lame de Gel": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Fleche Bleue": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Eboulis": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Tomberoche": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Coup de pierre": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Drain": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Lame Pourpre": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Ascension Runique": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Coup de Boule": [75, 2, 25, 5, 50, "L'ennemi s'approche de vous et envoie un gros coup de boule !", "Mais vous esquivez le coup !", "Et vous vous le prenez en pleine tronche !", "Et il vous envoie valser !", 0, 0],
            "Frappe Lourde": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Attaque Légère": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Impact": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Coup de Griffe": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Morsure": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Gros Coup de Boule": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Avale": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Attaque Lourde": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Lame Courageuse": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Attaque Titanesque": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Lame Ultime": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
            "Lame Vaillante": [0, 0, 0, 0, 0, "description", "rate", "touche", "touche crit", 0, 0],
        }
        self.annuaire_de_caracteristique_des_techniques_speciales_de_monstre = {
            # degats, taux de reussite, tours d'effet, description, message si rate, message si touche
            "Lèche-Blessure": [0, 0, 0, "description", "rate", "touche"],
            "Corruption": [0, 0, 0, "description", "rate", "touche"],
            "Constructions du Zénith": [0, 0, 0, "description", "rate", "touche"],
            "Gemme Rouge": [0, 0, 0, "description", "rate", "touche"],
            "Medecine de Guerre": [0, 0, 0, "description", "rate", "touche"],
            "Remede Divin": [0, 0, 0, "description", "rate", "touche"],
            "Bouclier Ultime": [0, 0, 0, "description", "rate", "touche"],
            "Poing Eclat": [0, 0, 0, "description", "rate", "touche"],
            "Coup du Foie": [0, 0, 0, "description", "rate", "touche"],
            "Lame Dorée": [0, 0, 0, "description", "rate", "touche"],
            "Etranglement": [8, 25, 3, "L'ennemi s'enroule autour de votre cou...", "...mais vous arrivez a vous débarrasser de son étreinte.", "...et vous étrangle sans ménagement.\nVous devenez muet pendant 2 tours !"],
            "Brulevent": [0, 0, 0, "description", "rate", "touche"],
            "Roulé-Boulet": [0, 0, 0, "description", "rate", "touche"],
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
        self.DEGATBONUSDUMONSTRE = 0 #===
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
        self.BONUSCOUTMALEDICTIONVIE = 0

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
        # A faire :
        #
        #
        #                                                                                                                                                 
        #
        #
        #                        
        #
        #                           S'assurer que tout les stigmas soient                                                 |
        #                                                   implementés                                                   |
        #                                        (6/6*) (15/15+) (15/15-)                                                 |
        #                                        (0/8*) (0/29+) (0/29-)                                                   | BOUDDHA (plus tard)
        #                           appliquer talents aux attaques/sorts                                                  |
        #                                               (48/48e) (21/21c)                                                 |
        #
        #                           Definir les caracteristiques + recompenses                                            |
        #                                         des monstres dans SetAttributeFromName                                  |
        #                           faire messages attaques et sorts                                                      | LORE
        #                           Donner questions a Alfred                                                             |
        #                           Definir cout sort                                                                     |
        #                           definir %touche, degat, %crit, degat crit, %element pour chaque attaque et sorts      |
        #
        #
        #                           cleanup                                                                               |
        #                           Documention méthodes                                                                  | FIN (plus tard)
