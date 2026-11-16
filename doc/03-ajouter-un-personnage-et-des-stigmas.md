# Ajouter un personnage et des stigmas

Un personnage est une **liste de 21 valeurs** dans un dictionnaire. Il n'a pas
de code à lui : ce qui le rend unique, ce sont ses trois stigmas, et un stigma
n'est qu'un nom que le code du jeu teste à certains endroits.

## 1. Le parcours d'un personnage

```
MenuDeDemarrage()                                   interface/menu_demarrage.py
 ├─ InitialiseDictionnaireDePersonnageAAfficher()   numérote les personnages de LISTEDEPERSONNAGE
 └─ « Nouvelle Partie » -> ChoseCharacter()
     ├─ GetChoixPersonnageChoice()                  affiche la liste numérotée
     ├─ GetPersonnageValideChoice(caracteristiques) affiche la fiche et demande confirmation
     └─ Player.UseCharacterForInitCaracteristics(caracteristiques)
                                                    joueur/caracteristiques.py : recopie les 21 valeurs
 puis Save.FromPlayerToDict() + FromDictToSaveFile()   la run est écrite dans save.txt

 à chaque combat :
 modele.Model(Player)                               combat/modele.py : copie les stigmas dans
                                                    stigma_joueur_positif / _negatif / _bonus

 à la fin de la run :
 Ending.DoEnding()                                  histoire/fin.py
 ├─ ShowStory(nom, True)                            texte de fin, une branche par personnage
 ├─ DoLastFight() puis ShowStory(nom, False)        seulement pour les personnages à boss d'histoire
 └─ GiveGift()                                      artefact de récompense, un par personnage
```

Le menu se construit tout seul à partir de `LISTEDEPERSONNAGE` : ajouter une
entrée suffit pour que le personnage soit proposé et jouable.

## 2. Écrire le personnage

Dans `coliseum/donnees/personnages.py`, ajouter une entrée à
`LISTEDEPERSONNAGE`. L'ordre des valeurs est imposé : c'est leur position qui
compte, pas un nom de champ.

| Position | Valeur | Contrainte |
|---|---|---|
| 0 | nom | identique à la clé du dictionnaire |
| 1 | histoire | texte libre, affiché à la sélection |
| 2 | stigma positif | un nom de stigma (voir section 4) |
| 3 | stigma négatif | idem |
| 4 | stigma bonus | idem, ou `"Aucun"` |
| 5 | techniques de départ | noms présents dans `LISTETECHNIQUES` (`donnees/actions.py`) |
| 6 | sorts de départ | noms présents dans `LISTESORTS` |
| 7 | objets de départ | `{nom: quantité}`, noms présents dans `DICTIONNAIREITEMINITIAL` |
| 8 | talents de départ | noms présents dans `ANNUAIREDECHOIXPOURREDCOIN` |
| 9 | vie max | la vie de départ est égale à la vie max |
| 10 | mana max | idem |
| 11 | force | |
| 12 | intelligence | |
| 13 | défense | |
| 14 | % de coup critique | |
| 15 | dégâts de coup critique | |
| 16 | % de sort critique | |
| 17 | dégâts de sort critique | |
| 18 | % d'esquive | |
| 19 | or de départ | |
| 20 | artefacts de départ | liste de noms présents dans `donnees/artefacts.py` |

L'endurance n'est pas dans la fiche : `UseCharacterForInitCaracteristics` la fixe à 20.

Rien ne vérifie ces noms à la création du personnage. Une faute de frappe ne
se révèle qu'en jeu, au moment où le nom est utilisé : tester le personnage
en combat avant de le considérer comme terminé.

## 3. Ce qu'il faut compléter ailleurs

Un personnage ajouté à `LISTEDEPERSONNAGE` peut jouer toute une run. Les
points suivants ne concernent que la fin de la run et le livre.

| Besoin | Où | Sans cela |
|---|---|---|
| Texte de fin | `EndingAndGift.ShowStory()` dans `histoire/fin.py` : ajouter une branche `elif nom == "Mon Personnage":` | aucun texte n'est affiché |
| Combat de fin d'histoire | ajouter le nom à la liste testée dans `DoEnding()` **et** une entrée à `BOSS_D_HISTOIRE_PAR_PERSONNAGE` (`combat/preparation.py`) | pas de combat final |
| Artefact de récompense | entrée `"Mon Personnage": ["Nom de l'artefact", "description"]` dans `ARTEFACTETDESCRIPTION`, dans `GiveGift()` | voir l'avertissement ci-dessous |
| Livre de la Cigogne Blanche | entrée dans `DICTIONNAIREDESCRIPTIONCIGOGNEBLANCHE["Les Personnages"]` (`donnees/bibliotheque.py`) | `KeyError` à l'écriture du livre |
| Personnage caché | condition sur un tag permanent dans `ChoseCharacter()` et `GetChoixPersonnageChoice()`, comme pour "Neil" | le personnage est visible dès le début |
| Image du récap | entrée `"Mon Personnage": r"images\personnages\mon_personnage.png"` dans `IMAGES_DES_PERSONNAGES` (`donnees/personnages.py`, juste sous `LISTEDEPERSONNAGE`) | le récap affiche `-- No Data Found --` à la place de l'image |

L'image est montrée dans le récap du joueur, en haut à gauche de la fenêtre
(fiche 05, section 4). Le chemin part du dossier `ColiseumDependencies` ;
formats PNG et GIF. Elle est rangée dans un dictionnaire à part, et non dans
la liste du personnage, parce que cette liste est lue par position : y ajouter
une valeur aurait obligé à modifier les vingt personnages existants.

**À vérifier.** `GiveGift()` lit `ARTEFACTETDESCRIPTION[nom_du_personnage]`
sans valeur par défaut. Dans le code actuel, Alex, Terrance, Cassandra et Neil
n'y figurent pas : d'après le code, finir une run avec l'un d'eux lève une
`KeyError`. Je n'ai pas joué ce cas. Un nouveau personnage doit y être ajouté.

Le combat de fin d'histoire fait apparaître un monstre : il lui faut une fiche
dans le bestiaire (fiche 02).

## 4. Créer un stigma

### Ce qu'est un stigma

Une chaîne de caractères. `"Solide"` ne fait rien par lui-même : il agit parce
que `PatternDesignConstantUpdater()` contient
`if self.modele.stigma_joueur_positif == "Solide": bonus_stigma = 50`.

Créer un stigma, c'est donc :

1. choisir un nom et le mettre en position 2, 3 ou 4 de la fiche du personnage ;
2. écrire son effet à l'endroit du jeu qui correspond au moment voulu.

Il n'existe pas de liste centrale des stigmas. Une faute de frappe dans le nom
ne provoque aucune erreur : le stigma ne fait simplement rien. Recopier le nom
par copier-coller.

### Où lire le stigma du joueur

| Contexte | Expression |
|---|---|
| En combat | `self.modele.stigma_joueur_positif`, `self.modele.stigma_joueur_negatif`, `self.modele.stigma_joueur_bonus` |
| Hors combat | `services.Player.stigma_positif`, `services.Player.stigma_negatif`, `services.Player.stigma_bonus` |

En combat, toujours passer par le modèle : c'est une copie prise au début du
combat, et c'est elle que toutes les règles lisent.

### Où brancher l'effet, selon le moment

Tous les fichiers de ce tableau sont dans `coliseum/combat/`.

| Moment voulu | Méthode | Fichier |
|---|---|---|
| Bonus ou malus permanent (dégâts, critique, esquive, coût) | `PatternDesignConstantUpdater()` | `preparation.py` |
| Au début du combat | `PremierTourJoueur()` | `preparation.py` |
| À la fin de chaque tour | `ApplicationStigmaPourFinDuTour()` | `stigmas.py` |
| Quand le joueur utilise une technique | `UseAttack()` ou `CheckSiAttaquePossibleEtAppliqueCoutAttaque()` | `actions_joueur.py` |
| Quand le joueur lance un sort | `UseMagic()` ou `CheckSiSortPossibleEtAppliqueCoutSort()` | `actions_joueur.py` |
| Quand le joueur utilise un objet | `UseItem()` | `actions_joueur.py` |
| Quand le joueur ou le monstre tombe à zéro | `CheckHp()` | `fin_de_combat.py` |
| À la distribution des récompenses | `MontreFuiteOuRecompense()` | `fin_de_combat.py` |

Hors combat, on teste le stigma directement là où l'effet doit se produire.
Exemples existants :

| Stigma | Endroit | Effet |
|---|---|---|
| "Mauvaise Réputation" | `TraderUsage.__init__` (`commerce/marchand.py`) | prix du marchand multipliés par 1,5 |
| "Esprit bien rangé, esprit libéré" | `PlayerCaracteristics.checkForStigmaPlusAhti()`, appelée par les salles | soin en observant une salle |
| "Incompatible" | `DoRedcoin()` (`joueur/talents.py`) | modifie ce qui se passe à l'achat d'un talent |
| "Indigérable" | `PrepareTheVillage()` (`histoire/village.py`) | modifie le texte d'arrivée au village |

### `PatternDesignConstantUpdater` : le cas le plus fréquent

Cette méthode est rappelée au début de chaque tour. Elle recalcule depuis zéro
toutes les constantes du combat (`self.modele.DEGATBONUSATTAQUE`,
`CHANCEBONUSESQUIVE`...) à partir des talents, artefacts et stigmas. Un bonus
de stigma s'y écrit dans le bloc de la constante concernée :

```python
        bonus_stigma = 0
        if self.modele.stigma_joueur_positif == "Solide":
            bonus_stigma = 50
        elif self.modele.stigma_joueur_positif == "Mon Stigma":
            bonus_stigma = 30
```

Comme tout est recalculé à chaque tour, un bonus peut dépendre de l'état du
combat (vie restante, numéro du tour, altération en cours).

### Un effet actif : méthode, branchement, affichage

Exemple complet avec « Bénie par les Fées », qui rend 3 % de la vie à chaque tour.

1. La méthode d'effet, dans `StigmasMixin` (`stigmas.py`) :

```python
    def EffetStigmaBeniParLesFees(self):
        sante_recupere = round(self.modele.points_de_vie_max * 0.03)
        sante_recupere = self.SiZeroRameneAUn(sante_recupere)
        self.modele.points_de_vie += sante_recupere
        self.EquilibragePointsDeVieEtManaEtEndurance()
        self.vue.AfficheBeniParLesFees(sante_recupere)
```

2. Le branchement, dans `PremierTourJoueur()` et dans `ApplicationStigmaPourFinDuTour()` :

```python
        if self.modele.stigma_joueur_positif == "Bénie par les Fées":
            self.EffetStigmaBeniParLesFees()
```

3. L'affichage, dans `Vue` (`vue.py`) :

```python
    def AfficheBeniParLesFees(self, sante_recupere):
        print("De par la bénédiction que vous avez recu a la naissance,")
        print(f"Vous reprenez {sante_recupere} points de vie !")
        self.EntreePourContinuer()
```

Par convention, ces méthodes s'appellent `EffetStigma...` et vivent dans
`stigmas.py`.

### Pièges connus

- **Chaîne `elif` de fin de tour.** Dans `ApplicationStigmaPourFinDuTour()`,
  les stigmas positifs et négatifs du joueur sont dans une seule chaîne
  `if / elif`. Si le stigma positif du personnage figure dans cette chaîne,
  son stigma négatif de fin de tour n'est jamais exécuté. Pour un nouveau
  stigma négatif, écrire un `if` séparé plutôt que d'allonger la chaîne.
- **Comparaison à une liste.** `preparation.py` contient
  `self.modele.stigma_joueur_negatif == ["Attache Physique"]` : une chaîne
  n'est jamais égale à une liste, ce test est toujours faux. Écrire
  `== "Nom"` ou `in ["Nom A", "Nom B"]`.
- **Stigma du monstre.** Les monstres utilisent les mêmes noms, lus dans
  `self.modele.stigma_monstre_positif` / `_negatif` / `_bonus`. Un même stigma
  peut servir aux deux camps, mais chaque camp a ses propres tests.

### Boîte à outils d'un effet de stigma

| Besoin | Appel |
|---|---|
| Ne jamais soigner ou blesser de zéro | `valeur = self.SiZeroRameneAUn(valeur)` |
| Ramener vie, mana, endurance dans leurs bornes | `self.EquilibragePointsDeVieEtManaEtEndurance()` |
| Blesser le joueur (défense prise en compte) | `self.EnleveVieAuJoueur(degat)` |
| Rendre du mana | `self.RecouvrementDeMana(points)` |
| Rendre de l'endurance | `self.RecupEndurance(points)` |
| Blesser le monstre | `self.modele.monstre_points_de_vie -= degat` puis `self.CheckOnlyMonsterHp()` si l'effet peut le tuer |
| Faire passer son tour au joueur ou au monstre | `self.modele.passe_son_tour = True`, `self.modele.monstre_passe_son_tour = True` |
| Connaître le tour en cours | `self.modele.nombre_de_tours` |
| Savoir si c'est un boss | `self.modele.monstre_EstUnBoss` |
| Afficher une ligne puis attendre Entrée | `self.vue.AffichageUneLignePuisUnEntreePourContinuer(texte)` |

## 5. Modèle de personnage

```python
    "Mon Personnage": [
        "Mon Personnage",                    # 0  nom : identique à la clé
        (
            "Première ligne de son histoire."
            "\n           Lignes suivantes, alignées sous la première."
        ),                                   # 1  histoire
        "Mon Stigma Positif",                # 2  stigma +  (effet à écrire, section 4)
        "Mon Stigma Négatif",                # 3  stigma -
        "Aucun",                             # 4  stigma bonus, ou "Aucun"
        ["Attaque Légère"],                  # 5  techniques de départ
        ["Explosion Légère"],                # 6  sorts de départ
        {
            "Feuille Jindagee": 3,
            "Remède": 5,
        },                                   # 7  objets de départ
        ["Affinitée Physique"],              # 8  talents de départ
        40,                                  # 9  vie max
        15,                                  # 10 mana max
        2,                                   # 11 force
        2,                                   # 12 intelligence
        2,                                   # 13 défense
        15,                                  # 14 % de coup critique
        5,                                   # 15 dégâts de coup critique
        10,                                  # 16 % de sort critique
        10,                                  # 17 dégâts de sort critique
        8,                                   # 18 % d'esquive
        0,                                   # 19 or de départ
        [],                                  # 20 artefacts de départ
    ],
```

## 6. Modèle de stigma

```python
# --- combat/stigmas.py, dans StigmasMixin
    def EffetStigmaMonStigma(self):
        """Décrire l'effet en une phrase : qui gagne ou perd quoi, et quand."""
        gain = round(self.modele.points_de_mana_max * 0.05)
        gain = self.SiZeroRameneAUn(gain)
        self.modele.points_de_mana += gain
        self.EquilibragePointsDeVieEtManaEtEndurance()
        self.vue.AfficheStigmaMonStigma(gain)

# --- le branchement, à l'endroit choisi dans le tableau « où brancher l'effet »
        if self.modele.stigma_joueur_positif == "Mon Stigma Positif":
            self.EffetStigmaMonStigma()

# --- combat/vue.py, dans Vue
    def AfficheStigmaMonStigma(self, gain):
        print(f"Votre stigma vous rend {gain} points de mana !")
        self.EntreePourContinuer()

# --- hors combat, là où l'effet doit se produire
        if services.Player.stigma_positif == "Mon Stigma Positif":
            ...
```

## 7. Liste de contrôle

- [ ] entrée ajoutée à `LISTEDEPERSONNAGE`, 21 valeurs dans l'ordre
- [ ] techniques, sorts, objets, talents et artefacts de départ existent sous ce nom exact
- [ ] chaque stigma nouveau a au moins un test dans le code, avec le nom copié-collé
- [ ] image dans `IMAGES_DES_PERSONNAGES` (facultatif)
- [ ] branche dans `ShowStory()`
- [ ] entrée dans `ARTEFACTETDESCRIPTION` (`GiveGift()`)
- [ ] entrée dans `DICTIONNAIREDESCRIPTIONCIGOGNEBLANCHE["Les Personnages"]`
- [ ] si combat de fin d'histoire : liste de `DoEnding()`, `BOSS_D_HISTOIRE_PAR_PERSONNAGE`, fiche du boss
