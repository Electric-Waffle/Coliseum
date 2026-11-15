# Ajouter un monstre

Un monstre, c'est quatre choses, dans cet ordre :

1. une **fiche** dans le bestiaire (ses caractéristiques) ;
2. un endroit où son **nom apparaît** (liste de monstres d'un étage, liste de boss...) ;
3. ses **actions** : réutiliser des actions existantes, ou en déclarer de nouvelles ;
4. éventuellement un **comportement** particulier : stigmas, tags, phases.

Tous les fichiers cités sont dans `coliseum/combat/`.

## 1. Le parcours d'un monstre pendant un combat

Comprendre ce parcours dit où brancher chaque chose.

```
Control.Battle()                                    controleur.py
 └─ _preparer_le_combat()
     ├─ MonsterMaker()                              preparation.py
     │   ├─ SetNameFromLevelAndBoss()               choisit modele.monstre_nom
     │   └─ SetAttributesFromName()
     │       ├─ fiche_du_monstre(nom, combat)       bestiaire/fiche.py : appelle TA fonction @monstre
     │       ├─ fiche.appliquer(modele)             recopie la fiche dans le modèle, puis appelle `finition`
     │       └─ ajoute le bonus de vie de l'étage   sauf bonus_de_vie_de_l_etage=False
     ├─ PatternDesignConstantUpdater()              bonus passifs des stigmas et talents
     ├─ AfficheMonstreNiveauEtMusique()             choisit et lance la musique
     ├─ PremierTourJoueur()
     └─ PremierTourMonstre()                        effets de début de combat (stigmas, tag "Terreur")

 à chaque tour :
 ├─ PatternDesignConstantUpdater()
 ├─ _jouer_le_tour_du_joueur()
 ├─ _jouer_le_tour_du_monstre()                     controleur.py
 │   ├─ GetMonsterChoice()                          actions_monstre.py : tire UNE action au hasard
 │   │                                              dans fiche.actions, toutes équiprobables
 │   ├─ "Technique" -> UseMonsterAttack(nom)
 │   └─ "Sort"      -> UseMonsterMagic(nom)         vérifie d'abord le mana (RegardeSiMonstreAAssezDeMana)
 ├─ CheckHp()                                       fin_de_combat.py : mort, vies supplémentaires, phases
 └─ FinTour()
     ├─ AppliqueEtMetAJourAlterationEtat()          alterations.py : feu, poison, gel...
     └─ ApplicationStigmaPourFinDuTour()            stigmas.py : stigmas et tags de fin de tour

 fin : MontreFuiteOuRecompense()                    fin_de_combat.py : distribue fiche.recompense
```

Le monstre n'a pas d'intelligence : il tire une action au hasard parmi celles
de sa fiche. Pour qu'une action sorte plus souvent, il n'existe pas de poids ;
le « comportement » se règle par le choix des actions, les stigmas, les tags
et les phases.

## 2. Écrire la fiche

Dans le fichier du bestiaire qui correspond à sa famille :

| Fichier | Famille |
|---|---|
| `bestiaire/monstres_des_etages.py` | monstres ordinaires |
| `bestiaire/boss.py` | boss de fin d'étage, normaux et alternatifs |
| `bestiaire/boss_rush.py` | boss des Limbes Flétrissants et leurs phases |
| `bestiaire/speciaux.py` | mimiques, boss d'histoire, gardien, obélisque |

Un nouveau fichier de fiches doit être ajouté à l'import de `bestiaire/__init__.py`,
sinon ses monstres n'existent pas.

```python
@monstre("Rat Géant")
def rat_geant(combat):
    return FicheMonstre(
        stigma_positif="Gluantesque",
        stigma_negatif="Gluantin",
        force=3,
        intelligence=0,
        resistance=1,
        vies_supplementaires=0,
        vie_max=40,
        mana_max=10,
        actions={
            "Coup de Boule": "Technique",
            "Soin": "Sort",
        },
        recompense={"Vie max": 2, "Gold": 20 + combat.bonus_gold},
    )
```

Deux monstres ne peuvent pas porter le même nom : le décorateur lève une
erreur au lancement du jeu.

## 3. Faire apparaître le monstre

Les listes sont dans `modele.py` (`Model.__init__`). Le choix est fait par
`PreparationMixin._nom_du_monstre_a_affronter()` dans `preparation.py`.

| Pour qu'il apparaisse comme... | Modifier |
|---|---|
| monstre ordinaire d'un étage | `liste_de_monstres_etage_1_2`, `_3_4`, `_5_6`, `_7_8`, `_9_10_11`. Le tirage s'adapte à la longueur de la liste. |
| boss d'un étage | `liste_de_boss` : l'indice est le numéro de l'étage (indice 0 = étage 0). |
| boss d'un étage alternatif | `liste_de_boss_alternatif` : l'indice est le numéro de l'étage **moins 1**. |
| boss des Limbes | `liste_de_boss_rush` : l'indice est `Player.numero_boss_alt - 1`. |
| boss de fin d'histoire d'un personnage | `BOSS_D_HISTOIRE_PAR_PERSONNAGE` dans `preparation.py` |
| phase suivante d'un boss | voir « Phases » plus bas |

`liste_de_monstre_totaux_pour_dernier_choix` (aussi dans `modele.py`) sert au
stigma « Monsieur Loyal », qui laisse le joueur choisir son adversaire. Elle
est construite à partir des listes par étage : un monstre ajouté à l'une
d'elles y figure automatiquement.

### Musique

`AfficheMonstreNiveauEtMusique()` (`preparation.py`) choisit le fichier d'après
l'étage, pas d'après le monstre :

| Cas | Fichier joué |
|---|---|
| monstre ordinaire | `battle_theme_<étage>.mp3` |
| boss | `boss_<étage>.mp3` |
| étage alternatif | même nom suivi de `_alt` |
| boss des Limbes | `alt_<numero_boss_alt>_phase_1.mp3` |
| mimique | `mimique_<étage / 2>.mp3` |
| boss d'histoire | `story_end.mp3` |

Un monstre n'a donc pas de musique à lui, sauf à ajouter un cas dans cette méthode.

## 4. Configurer ses actions

`actions` associe un nom d'action à son type : `"Technique"` ou `"Sort"`.
Une action déjà connue du jeu fonctionne immédiatement. Pour une action
nouvelle, tout se déclare dans `modele.py`, et selon sa famille :

### a. Attaque ou sort à dégâts (cas le plus courant)

Ajouter une entrée à
`annuaire_de_caracteristique_des_techniques_generales_de_monstre` (ou
`..._sorts_generaux_de_monstre`). Onze valeurs, dans cet ordre :

```python
"Morsure": [
    90,    # [0] % de chances de toucher
    6,     # [1] dégâts de base
    20,    # [2] % de chances de coup critique
    4,     # [3] dégâts ajoutés en cas de critique
    25,    # [4] % de chances d'appliquer l'effet élémentaire
    "L'ennemi se jette sur vous, gueule ouverte...",   # [5] description
    "...mais vous l'évitez.",                          # [6] message si raté
    "...et ses crocs vous entaillent le bras !",       # [7] message si touché
    "...et ses crocs se referment sur votre gorge !!", # [8] message si critique
    3,     # [9] nombre de tours de l'effet élémentaire
    5,     # [10] puissance de l'effet : son sens dépend de l'élément (tableau ci-dessous)
],
```

L'élément n'est pas dans l'entrée : il vient de la liste où le nom figure.
Ajouter le nom à **une** de ces listes pour lui donner un élément :

| Liste (`techniques_de_..._de_monstre` ou `sorts_de_..._de_monstre`) | Effet quand [4] réussit | Sens de [9] et [10] |
|---|---|---|
| `feu` | brûlure | [9] tours, [10] dégâts par tour |
| `foudre` | paralysie | [9] tours |
| `glace` | gel | [9] tours |
| `sang` | drain : le monstre se soigne d'autant | [10] % de la vie max du joueur |
| `terre` | lapidation : dégâts en plus | [10] % des dégâts de l'attaque |
| `physique` | aucun effet, seulement le type de dégâts | inutilisés |

C'est `CheckMonsterTypeOfAction()` (`actions_monstre.py`) qui lit ces listes
au début de l'action.

À vérifier : dans `UseMonsterAttack`, la branche de la lapidation teste
`self.modele.a_utilise_terre_ce_tour` (le drapeau du **joueur**) et non
`monstre_a_utilise_terre_ce_tour`. Telle quelle, une technique de terre d'un
monstre ne lapide que si le joueur a lui-même utilisé la terre ce tour-ci.
Le code d'origine était ainsi ; je ne l'ai pas modifié.

### b. Soin

Ajouter le nom à `techniques_de_soin_de_monstre` (ou `sorts_de_soin_de_monstre`),
et une entrée à `annuaire_de_caracteristique_des_techniques_speciales_de_monstre` :

```python
# technique : soin minimum, % de réussite, % de la vie max rendue, description, message si raté, message si réussi
"Lèche-Blessure": [30, 75, 8, "L'ennemi lèche ses blessures...", "...mais rien ne se passe.", "...et elles se referment !"],
```

Pour un sort, c'est `annuaire_de_caracteristique_des_sorts_speciaux_de_monstre`,
avec quatre valeurs : soin minimum, % de la vie max rendue, description, message.

### c. Malédiction (altération sans dégâts)

Ajouter le nom à l'une de ces listes, et une entrée au même annuaire « spécial »
que pour le soin (dégâts, % de réussite, nombre de tours, description, raté, réussi) :

| Liste | Effet sur le joueur |
|---|---|
| `techniques_de_blessure_de_monstre` | les techniques coûtent de la vie |
| `techniques_de_deconcentration_de_monstre` | les sorts coûtent plus de mana |
| `techniques_de_gold_de_monstre` | chaque action coûte de l'or |
| `techniques_de_instable_de_monstre` | plus de techniques |
| `techniques_de_muet_de_monstre` | plus de sorts |
| `techniques_de_confusion_de_monstre` | plus d'objets |

Les mêmes listes existent en `sorts_de_..._de_monstre`.

### d. Tout sort a un coût

Tout sort, quelle que soit sa famille, doit avoir une entrée dans
`ANNUAIRECOUTSORTMONSTRE` (`modele.py`) :

```python
"Morsure Spectrale": 8,
```

Sans cette entrée, `RegardeSiMonstreAAssezDeMana()` plante avec `KeyError`.
Si le monstre n'a pas assez de mana, il perd son tour (`MetMonstreEnEtatDeChoc`).

### e. Attaque spéciale (logique libre)

Quand les trois familles ne suffisent pas, on écrit une méthode. Deux étapes,
toutes deux dans `attaques_speciales.py` :

1. écrire la méthode dans `AttaquesSpecialesMixin` ;
2. l'inscrire dans `TECHNIQUES_SPECIALES_DE_MONSTRE` ou
   `SORTS_SPECIAUX_DE_MONSTRE`, en haut du fichier : `"Nom de l'action": "NomDeLaMethode"`.

```python
    def Envol(self):
        commentaire = "L'ennemi s'élance dans les airs.\nIl sera beaucoup plus difficile a toucher maintenant !"
        commentaire_effet = "Vous perdez 30% de chance de reussir une attaque ou un sort pendant 3 tours !"
        self.vue.AfficheEnvol(commentaire, commentaire_effet)
        self.modele.monstre_est_envol = True
        self.modele.monstre_est_envol_nombre_tour = 4
```

L'affichage passe par la vue : ajouter une méthode `AfficheXxx` dans `vue.py`,
ou réutiliser `self.vue.AffichageUneLignePuisUnEntreePourContinuer(texte)`.

Ordre de recherche dans `UseMonsterAttack` / `UseMonsterMagic` : annuaire
général, puis soin, puis malédiction, puis table des attaques spéciales. Un
nom présent dans l'annuaire général ne sera donc jamais traité comme spécial.

#### Boîte à outils d'une attaque spéciale

| Besoin | Appel |
|---|---|
| Infliger des dégâts au joueur (tient compte de la défense et de la métamorphose) | `degat = self.EnleveVieAuJoueur(degat)` |
| Appliquer les bonus de dégâts du monstre et la réduction du joueur | `degat = self.AppliqueDegatsBonusDuMonstreContreLeJoueur(degat)` |
| Laisser bluff, montagne, miroir d'eau et brume de sang réagir aux dégâts | `self.CheckePuisAppliqueTransmutation(degat)`, à appeler **après** `EnleveVieAuJoueur` : elle annule ou renvoie les dégâts déjà infligés |
| Brûler, geler, paralyser le joueur | `self.AppliqueEffetElementaireSurJoueur("feu", tours, degats)` ("glace", "foudre"...) |
| Maudire le joueur | `self.modele.est_maudit_par_les_sorts = True` et `..._nombre_tour = n` (aussi `par_la_vie`, `par_le_mana`, `par_le_gold`, `par_les_techniques`, `par_les_items`) |
| Soigner le monstre | `self.modele.monstre_points_de_vie += n` puis `self.EquilibragePointsDeVieEtManaEtEndurance()` |
| Poser un état sur le monstre | `self.modele.monstre_est_envol`, `monstre_est_regeneration`, `monstre_est_vulnerable`... avec leur `..._nombre_tour` |
| Vérifier si le monstre s'est tué lui-même | `self.CheckOnlyMonsterHp()` |
| Voler de l'or ou du mana | `self.modele.nombre_de_gold`, `self.modele.points_de_mana` |
| Demander un choix au joueur | une méthode `GetXxxChoix` dans `vue.py` |

## 5. Configurer son comportement

### Stigmas

Les trois champs `stigma_positif`, `stigma_negatif`, `stigma_bonus` sont de
simples chaînes. Elles n'ont d'effet que là où le code les teste. Reprendre
un stigma existant suffit ; en créer un se fait comme pour un stigma de
joueur (fiche 03), en testant `self.modele.stigma_monstre_positif`
(ou `_negatif`, `_bonus`) aux mêmes endroits :

| Moment | Méthode |
|---|---|
| bonus ou malus permanent | `PatternDesignConstantUpdater()` dans `preparation.py` |
| début de combat | `PremierTourMonstre()` dans `preparation.py` |
| fin de chaque tour | `ApplicationStigmaPourFinDuTour()` dans `stigmas.py` |
| au moment de payer un sort | `RegardeSiMonstreAAssezDeMana()` dans `actions_monstre.py` |

### Tags

`tags` est une liste de marqueurs testés par `"Nom" in self.modele.monstre_tags`.
Tags existants : "Terreur", "Fausse Terreur", "Super Etoile", "Domovoï",
"Kikimora", "Cuisine Infernale" (avec "Entrée", "Plat", "Dessert"), "En Fuite",
et les "Voluntad ..." du gardien. Ils sont déclenchés à la fin de
`ApplicationStigmaPourFinDuTour()` et, pour "Terreur", dans `PremierTourMonstre()`.

Un tag sert quand l'effet doit pouvoir se cumuler ou changer en cours de
combat ; un stigma, quand il y en a un seul et qu'il est fixe.

### Vies supplémentaires et phases

`vies_supplementaires=n` : quand le monstre tombe à zéro, `CheckHp()`
(`fin_de_combat.py`) lui rend la moitié de sa vie, lui fait passer un tour,
et décrémente le compteur.

Un boss à **phases** est une suite de fiches. Quand la dernière vie
supplémentaire est consommée, `CheckHp()` change `modele.monstre_nom` et
rappelle `SetAttributesFromName()`, qui applique la fiche de la phase suivante.
Cette partie n'est pas encore une table. Pour ajouter une phase il faut, dans
`CheckHp()` :

1. ajouter le nom du boss à la liste `["Maitre Mage", "Apprentie", ...]` ;
2. ajouter une branche `elif self.modele.monstre_nom == "Mon Boss":` qui
   affiche la transition et écrit `self.modele.monstre_nom = "Mon Boss (Phase 2)"` ;
3. écrire la fiche `@monstre("Mon Boss (Phase 2)")`.

### Récompenses

`recompense` est distribuée par `MontreFuiteOuRecompense()`. Clés reconnues :

| Clé | Effet |
|---|---|
| "Attaque", "Defence", "Intelligence" | points de caractéristique |
| "Vie", "Mana" | soin immédiat |
| "Vie max", "Mana max", "Endurance" | maximum augmenté |
| "Taux coup critique", "Degat coup critique", "Taux sort critique", "Degat sort critique", "Taux esquive" | bonus de combat |
| "Gold" | or (ajouter `combat.bonus_gold` pour suivre l'étage) |
| "Red coin" | red coins |
| "Tirage", "Méga Tirage" | tirages chez le marchand |
| "Materiau" | nom d'un matériau, lâché par le monstre |

Une clé inconnue est ignorée sans erreur.

### Livre de la Cigogne Blanche

À la victoire, `MontreFuiteOuRecompense()` inscrit le nom du monstre dans la
sauvegarde permanente, thème "Les Boss" ou "Les Ennemis". Quand le joueur fait
écrire le livre, `histoire.cigogne_blanche.EcrireDansLivreCigogneBlanche()` va
chercher la description de chaque nom dans
`DICTIONNAIREDESCRIPTIONCIGOGNEBLANCHE` (`coliseum/donnees/bibliotheque.py`).
Un nom sans description y provoque une `KeyError` : ajouter une entrée
`"Mon Monstre": "sa description"` dans le bon thème.

## 6. Modèle de fiche, tous champs expliqués

```python
def _finir_mon_monstre(modele):
    """Appelée après l'application de la fiche. À réserver à ce qu'un champ ne sait pas dire.

    Reçoit le modèle du combat : on peut y lire l'étage, modifier la liste
    d'actions, renommer le monstre, donner au joueur un sort de circonstance.
    """
    if modele.numero_de_letage >= 6:
        modele.monstre_liste_actions["Morsure"] = "Technique"
    modele.sorts.append("Faire fuir le Domovoï")


@monstre("Mon Monstre")          # nom affiché, et clé utilisée par les listes d'apparition
def mon_monstre(combat):
    # `combat` donne ce qui dépend du combat en cours :
    #   combat.numero_etage      étage (déjà augmenté si le monstre est « dopé »)
    #   combat.bonus_gold        or supplémentaire lié à l'étage
    #   combat.bonus_vie         vie supplémentaire liée à l'étage
    #   combat.vies_du_gardien   vies restantes du gardien de l'étage 0
    return FicheMonstre(
        # --- stigmas : chaînes testées par le code du combat. None = valeur par défaut du modèle.
        stigma_positif="Gluantesque",
        stigma_negatif="Gluantin",
        stigma_bonus=None,

        # --- caractéristiques
        force=3,                   # +10 % de dégâts de technique par point
        intelligence=0,            # +10 % de dégâts de sort par point
        resistance=1,              # réduit les dégâts qu'il reçoit
        vie_max=40,                # la vie de départ ; l'étage y ajoute combat.bonus_vie
        mana_max=10,               # réserve pour ses sorts
        vies_supplementaires=0,    # nombre de résurrections (voir « phases »)

        # --- actions : une est tirée au hasard à chaque tour
        actions={
            "Coup de Boule": "Technique",
            "Soin": "Sort",
        },

        # --- gains du joueur en cas de victoire
        recompense={"Vie max": 2, "Gold": 20 + combat.bonus_gold, "Materiau": "Coeur Gravitaire"},

        # --- facultatif
        tags=["Terreur"],                         # marqueurs de mécaniques spéciales
        etat_initial={"est_maudit_par_les_items": True,          # autres attributs du modèle
                      "est_maudit_par_les_items_nombre_tour": 999},  # à fixer au début du combat
        bonus_de_vie_de_l_etage=False,            # False : la vie ne grandit pas avec l'étage
        finition=_finir_mon_monstre,              # fonction(modele) appelée en dernier
    )
```

Ordre d'application, dans `FicheMonstre.appliquer()` : champs nommés, puis
`etat_initial`, puis `finition`. Le bonus de vie de l'étage est ajouté ensuite
par `SetAttributesFromName()`, qui remplit alors la vie et le mana à leur maximum.

## 7. Liste de contrôle

- [ ] fiche `@monstre` écrite, dans un fichier importé par `bestiaire/__init__.py`
- [ ] nom ajouté à une liste d'apparition de `modele.py`
- [ ] chaque action de `actions` existe : annuaire général, ou soin, ou malédiction, ou table des attaques spéciales
- [ ] chaque sort a son coût dans `ANNUAIRECOUTSORTMONSTRE`
- [ ] les clés de `recompense` sont dans la liste reconnue
- [ ] pour un boss à phases : branche dans `CheckHp()` et fiche de chaque phase
- [ ] les fichiers de musique de l'étage existent
- [ ] description ajoutée dans `DICTIONNAIREDESCRIPTIONCIGOGNEBLANCHE` ("Les Ennemis" ou "Les Boss")
