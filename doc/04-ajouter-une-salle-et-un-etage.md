# Ajouter une salle, un étage, un étage alternatif

Ces trois ajouts ne demandent pas le même effort :

- une **salle** est une fonction à écrire et une ligne à ajouter : le système est prévu pour ;
- un **étage** n'est pas une donnée : son numéro est testé à environ 130 endroits
  répartis dans 14 fichiers. Cette fiche liste ceux qui comptent ;
- un **étage alternatif** est un étage existant dont seul le *nom* change, et
  ce nom est testé à une trentaine d'endroits.

Sauf mention contraire, les fichiers sont dans `coliseum/exploration/`.

## 1. Comment fonctionne une carte

Le donjon et le village utilisent le même objet, `services.FloorMaker`
(classe `Floor`, `etage.py`), et la même structure : `FloorBlueprint`.

```python
FloorBlueprint = {
    1: {"position_x": 0, "position_y": 0, "marqué sur la carte": False,
        "terminé par joueur": False, "type": "ENTREE"},
    2: {"position_x": 2, "position_y": 0, ..., "type": "MONSTRE"},
    ...
}
```

| Clé | Rôle |
|---|---|
| numéro (clé du dictionnaire) | identifiant de la salle ; la salle 1 est toujours l'entrée |
| `position_x`, `position_y` | case sur la grille ; multipliées par 25 pour le dessin |
| `type` | ce qui s'y passe : c'est la clé du registre des salles |
| `marqué sur la carte` | l'icône de la salle a déjà été dessinée |
| `terminé par joueur` | la salle est vidée : l'observer affiche « La salle est sans interêt. » |

La seule différence entre donjon et village est la façon dont ce dictionnaire
est rempli :

| | Donjon | Village |
|---|---|---|
| Qui remplit `FloorBlueprint` | `Floor.SetupFloorLayout()` : aléatoire | `histoire.village.PrepareTheVillage()` : écrit en dur |
| Positions | `MakeFloorBlueprint()` | fixées à la main |
| Types | `InitiateRoleToAttribute()` + `AttributingRoleToRoom()` | fixés à la main |
| Numéro d'étage | 0 à 11 | -1 |

### Parcours d'une observation

```
FloorMaker.ShowFloor()                          etage.py
 ├─ PrintFloorBlueprint()                       dessine les cases, et l'icône des salles « marquées »
 │   └─ salles.icones.dessiner_l_icone(type, x, y)
 └─ WalkInFloor()                               boucle de déplacement
     ├─ WalkLeft / WalkRight / WalkUp / WalkDown
     │   └─ CheckPlayerPosition()               la case existe-t-elle ? met à jour Player.numero_de_la_salle
     └─ choix 5 : RevealRoom()
         ├─ salle = FloorBlueprint[Player.numero_de_la_salle]
         ├─ si salle["terminé par joueur"] : message et rien d'autre
         ├─ sinon salles.registre.reveler_la_salle(self, salle)
         │   └─ la fonction décorée @salle_de_type(salle["type"])
         └─ inscription de la salle au livre de la Cigogne Blanche
```

`RevealRoom()` est appelée sous le filet de sécurité local : une erreur dans
une salle est journalisée, le joueur est dédommagé, la partie continue.

## 2. Ajouter une salle

### a. Écrire la fonction

Dans le fichier de `salles/` qui correspond à son thème :

| Fichier | Thème |
|---|---|
| `salles/base.py` | monstres, trésors, pièges, clé, salle secrète |
| `salles/rencontres.py` | gardiens, bête, boss caché, rituel, obélisque |
| `salles/enigmes.py` | séquences, leviers, plaques, puits, mini-jeux |
| `salles/machines.py` | arbre, bols, jacuzzi, chargeur, affixeurs, distributeur |
| `salles/attractions.py` | atelier, loterie, braziers, pêche |
| `salles/village.py` | commerçants, quartiers, chemins, habitants |

Un nouveau fichier doit être ajouté à l'import de `salles/__init__.py`, sinon
ses salles n'existent pas.

```python
@salle_de_type("FONTAINE")
def reveler_fontaine(etage, salle):
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()
        services.Draw.machine()
        etage.UseMonocleDeVerite()
        salle["marqué sur la carte"] = True

    print("Une fontaine coule au centre de la pièce.")
    services.Affichage.EntreePourContinuer()
    services.Player.points_de_vie = services.Player.points_de_vie_max
    salle["terminé par joueur"] = True
```

La fonction reçoit :

- `etage` : le `Floor` en cours. Il donne accès à la carte (`etage.FloorBlueprint`)
  et aux mini-jeux (`etage.DoPeche`, `etage.DanceDanceRevolution`,
  `etage.ReposDansJacuzzi`, `etage.GiveRandomArtefact`...) ;
- `salle` : le dictionnaire de la salle. Le modifier modifie la carte.

Une même fonction peut servir à plusieurs types : `@salle_de_type("FAUX SPOT", "SPOT")`.
Inscrire deux fois le même type lève une erreur au lancement.

### b. La faire apparaître

**Dans le donjon**, deux modifications dans `etage.py` :

1. dans `InitiateRoleToAttribute()`, déclarer combien il y en a par étage.
   La méthode commence par un `if / else` (combat contre le Gardien, ou cas
   normal). Déclarer le compteur **après** ce bloc, comme le font
   `nombre_de_puit` ou `nombre_de_coeur` : il existe ainsi dans les deux cas.

```python
        self.nombre_de_fontaine = 0
        if services.Player.numero_de_letage in [3, 6]:
            self.nombre_de_fontaine = 1
```

2. dans `AttributingRoleToRoom()`, ajouter une branche à la chaîne :

```python
        elif self.nombre_de_fontaine != 0:
            caracteristique_de_la_salle["type"] = "FONTAINE"
            self.nombre_de_fontaine -= 1
```

Cette chaîne est une file de priorité : chaque salle libre reçoit le premier
type dont le compteur n'est pas à zéro. Quand tous les compteurs sont vides,
les salles restantes reçoivent au hasard MONSTRE, GOLD, ITEM ou PIEGE. Si la
somme des compteurs dépasse le nombre de salles de l'étage, les types placés
en fin de chaîne ne sont pas attribués : placer une salle indispensable assez
haut dans la chaîne.

**Dans le village**, ajouter une entrée au dictionnaire écrit en dur dans
`PrepareTheVillage()` (`coliseum/histoire/village.py`), avec ses coordonnées.
Une case n'est accessible que si elle touche une case existante : le
déplacement refuse toute position absente du dictionnaire.

### c. Icône sur la carte

Dans `salles/icones.py`, ajouter une ligne à `ICONE_PAR_TYPE_DE_SALLE` :

```python
    "FONTAINE": "machine",
```

La valeur est le nom d'une méthode de `DrawInTurtle` (`coliseum/interface/dessin.py`).
Pour une icône nouvelle, y écrire une méthode de dessin. Une salle absente de
la table n'a pas d'icône, ce qui est le cas de toutes les salles du village.

### d. Livre de la Cigogne Blanche

À la fin de `RevealRoom()`, le dictionnaire `liste_salle_et_equivalent` associe
un type à un nom lisible. Si le type y figure, ce nom est inscrit dans la
sauvegarde permanente. Pour qu'une nouvelle salle entre dans le livre :

1. ajouter `"FONTAINE": "Fontaine de Jouvence"` à `liste_salle_et_equivalent` ;
2. ajouter `"Fontaine de Jouvence": "sa description"` à
   `DICTIONNAIREDESCRIPTIONCIGOGNEBLANCHE["Les Salles"]` (`coliseum/donnees/bibliotheque.py`).

Faire le 1 sans le 2 provoque une `KeyError` quand le joueur fait écrire le livre.

### Boîte à outils d'une salle

| Besoin | Appel |
|---|---|
| Afficher puis attendre Entrée | `print(...)` puis `services.Affichage.EntreePourContinuer()` |
| Effacer l'écran | `ClearConsole()` |
| Lancer un combat, erreurs gérées | `livrer_combat()` (retourne `True` s'il s'est déroulé sans erreur) |
| Combat spécial | poser l'état avant : `services.Player.player_tags.append("Monstre Dopé")`, `Player.affronte_une_mimique = True`, `Player.affronte_obelisque = True`... et le retirer après |
| Afficher la mort si le joueur a été tué | `CheckForKIA()` après le combat |
| Relancer la musique de l'étage | `PlayMusicDeLetage()` |
| Jouer un son, une ambiance | `PlaySound("nom")`, `PermanentPlaySFX("nom")` |
| Donner de l'or (bonus appliqués) | `services.Player.AddGoldToPlayer(montant)` |
| Donner un objet | `services.Player.items_possedes["Remède"] += 1` |
| Donner un artefact | `etage.GiveRandomArtefact()` |
| Ouvrir un commerçant | méthodes de `services.Trader` (`DoTrading`, `DoAncien`, `DoChamane`...) |
| Lire ou écrire le permanent | `services.Sove.ModifieTagsDansSove("Checke", "Mon Tag")`, `"Ajout"`, `"Enleve"` |
| Sauvegarder sans message | `services.Save.SaveTheGameSansAffichage()` |
| Savoir si on est au village | `services.Player.numero_de_letage == -1` |
| Déplacer le curseur de la carte | `ColiseumGoto(x, y)` |

Convention suivie par les salles existantes : dessiner l'icône et passer
`marqué sur la carte` à `True` à la première visite ; passer
`terminé par joueur` à `True` quand il n'y a plus rien à y faire. Une salle
réutilisable (commerçant, machine) ne se termine jamais.

## 3. Ajouter un étage

Le Coliseum va de l'étage 0 à l'étage 11. Un étage n'est décrit nulle part en
un seul endroit : son numéro est comparé directement dans le code. Pour les
retrouver tous :

```bash
grep -rn "numero_de_letage ==\|numero_de_letage in" coliseum
```

Voici, dans l'ordre où le jeu les rencontre, les endroits à compléter pour un
étage numéro `N`.

### Passage à l'étage

| Quoi | Où | Détail |
|---|---|---|
| Fin de la run | `GoDown()`, `progression.py` | la run s'arrête quand `numero_de_letage == 12` : déplacer cette borne |
| Nom de l'étage | `DefinitNomEtage()`, `progression.py` | ajouter `elif numero == N: nom_de_letage = "..."` |
| Remise à zéro | `RemiseAZeroDesVariablesPourProchainEtage()`, `progression.py` | nombre d'ennemis de l'arène : `5 + N * 2`, sauf exceptions (0, 10, 11) |
| Texte d'arrivée | `Affiche.AffichageDescriptionEtage()`, `coliseum/interface/affichage.py` | une branche par numéro |
| Musique | `audio.PlayMusicDeLetage()` | joue `etage_N.mp3` : le fichier doit exister dans `ColiseumDependencies/` |

### Carte de l'étage

| Quoi | Où | Détail |
|---|---|---|
| Nombre de salles | `Floor.SetupFloorLayout()` | `16 + N * 5`, sauf exceptions |
| Contenu | `Floor.InitiateRoleToAttribute()` | la plupart des compteurs dépendent de l'étage par une liste (`in [2, 4, 6, 8, 10]`) : y ajouter `N` là où c'est voulu |
| Salle secrète | `RevealRoom()`, liste `liste_du_nom_de_la_salle_secrete_en_fonction_de_letage` | indexée par numéro d'étage : sans entrée pour `N`, `IndexError` |
| Contenu de la salle secrète | `Observe.SeeSomething()`, `observation.py` | à vérifier : je n'ai pas lu cette méthode en détail |

### Combats

| Quoi | Où | Détail |
|---|---|---|
| Monstres de l'arène | `_nom_du_monstre_de_l_etage()`, `coliseum/combat/preparation.py` | ajouter `N` à une tranche d'étages, ou créer une tranche avec sa liste dans `combat/modele.py` |
| Boss | `liste_de_boss`, `coliseum/combat/modele.py` | l'indice est le numéro de l'étage |
| Choix de l'adversaire | `liste_de_monstre_totaux_pour_dernier_choix`, `modele.py` | une entrée par étage |
| Texte avant le boss | `Affiche.AfficheIntroCombatBoss()`, `affichage.py` | une branche par numéro |
| Musiques | `ColiseumDependencies/` | `battle_theme_N.mp3`, `boss_N.mp3` |
| Fiches | `coliseum/combat/bestiaire/` | voir la fiche 02 |

### Autour

| Quoi | Où | Détail |
|---|---|---|
| Marchand | `coliseum/commerce/marchand.py` | les prix suivent l'étage automatiquement ; 11 tests sur le numéro d'étage règlent le reste, à relire |
| Livre | `DICTIONNAIREDESCRIPTIONCIGOGNEBLANCHE["Les Etages"]` | une entrée au nom de l'étage, sinon `KeyError` à l'écriture du livre |
| Menu | `coliseum/interface/menu_coliseum.py`, `coliseum/application.py` | quelques étages ont un menu particulier (0, 10) |

Rien n'est à faire pour la sauvegarde : numéro et nom d'étage sont déjà
enregistrés.

## 4. Ajouter un étage alternatif

### Le mécanisme

Un étage alternatif n'a pas de numéro à lui. C'est l'étage `N` avec un autre
**nom**, et tout le reste du jeu le reconnaît à ce nom.

```
étage N-1 : une salle écrit   services.Player.etage_alternatif = True
                              (aujourd'hui : reveler_puit aux étages 1, 4 et 6,
                               et reveler_boss pour les Limbes)
        │
        ▼
GoDown() -> DefinitNomEtage()                    progression.py
        numero == N et etage_alternatif  ->  nom_de_letage = "Nom Alternatif"
        puis etage_alternatif = False            le drapeau est consommé
        │
        ▼
à partir d'ici, seul Player.nom_de_letage dit qu'on est dans la variante
```

Étages alternatifs existants : Jungle Cruelle (2), Le Lumisade (5), Douves du
Pénitent (7), Limbes Flétrissants (10).

### Les endroits à modifier

| Quoi | Où | Détail |
|---|---|---|
| Déclencheur | une salle de l'étage `N-1` | y écrire `services.Player.etage_alternatif = True` ; pour une salle nouvelle, voir section 2 |
| Nom | `DefinitNomEtage()`, `progression.py` | `if services.Player.etage_alternatif: nom_de_letage = "Nom Alternatif"` sous la branche de l'étage `N` |
| Musique de l'étage | `audio.PlayMusicDeLetage()` | ajouter le nom à la liste : le jeu joue alors `etage_N_alt.mp3` |
| Combats | `Model.__init__`, `coliseum/combat/modele.py` | ajouter le nom à la liste qui fixe `self.etage_alternatif = True` |
| Boss | `liste_de_boss_alternatif`, `modele.py` | indice = numéro de l'étage **moins 1** |
| Musiques de combat | `ColiseumDependencies/` | `battle_theme_N_alt.mp3`, `boss_N_alt.mp3` |
| Texte d'arrivée | `Affiche.AffichageDescriptionEtage()` | test sur le nom, dans la branche de l'étage `N` |
| Texte avant le boss | `Affiche.AfficheIntroCombatBoss()` | idem |
| Salles qui changent | les fonctions de `salles/` concernées | tester `services.Player.nom_de_letage == "Nom Alternatif"` |
| Nom de salle dans le livre | fin de `RevealRoom()` | la salle COEUR a un nom par étage et par variante |
| Livre | `DICTIONNAIREDESCRIPTIONCIGOGNEBLANCHE["Les Etages"]` | une entrée au nom alternatif |
| Fiche du boss | `coliseum/combat/bestiaire/boss.py` | voir la fiche 02 |

Pour retrouver tous les tests sur un nom d'étage :

```bash
grep -rn "nom_de_letage ==\|nom_de_letage in" coliseum
```

Deux points d'attention :

- le nom est écrit en toutes lettres à chaque endroit. Une faute de frappe ne
  provoque aucune erreur : l'étage se comporte simplement comme sa version normale ;
- la carte d'un étage alternatif est générée comme celle de l'étage normal
  (`InitiateRoleToAttribute()` ne regarde que le numéro). Pour une carte
  différente, y ajouter un test sur le nom.

## 5. Modèle de salle

```python
@salle_de_type("MON_TYPE")                 # le ou les types gérés par cette fonction
def reveler_mon_type(etage, salle):
    # --- première visite : dessiner l'icône (donjon uniquement)
    if not salle["marqué sur la carte"]:
        services.Player.checkForStigmaPlusAhti()   # stigma qui soigne en observant une salle
        services.Draw.machine()                    # méthode de dessin de l'icône
        etage.UseMonocleDeVerite()                 # artefact qui donne de l'or à chaque découverte
        salle["marqué sur la carte"] = True

    # --- variante selon le lieu, si besoin
    if services.Player.nom_de_letage == "Jungle Cruelle":
        print("Texte de la variante alternative.")
    else:
        print("Texte normal.")
    services.Affichage.EntreePourContinuer()

    # --- choix du joueur : boucle jusqu'à une réponse valide
    while True:
        try:
            print("1 - Partir")
            print("2 - Agir")
            choix = int(input("\nFaites votre choix avec les nombres : "))
            ClearConsole()
            if choix in [1, 2]:
                break
        except ValueError:                         # le joueur a tapé autre chose qu'un nombre
            ClearConsole()

    if choix == 2:
        # --- effet : combat, gain, commerçant, déclencheur d'étage alternatif...
        if livrer_combat():
            services.Player.AddGoldToPlayer(50)
        CheckForKIA()
        PlayMusicDeLetage()
        # services.Player.etage_alternatif = True  # le prochain étage sera sa variante

        # --- la salle est vidée : elle ne pourra plus être observée
        salle["terminé par joueur"] = True
```

Imports habituels en tête du fichier de salles :

```python
from coliseum import services
from coliseum.audio import PlayMusicDeLetage, PlaySound
from coliseum.combat.lancement import livrer_combat
from coliseum.console import ClearConsole
from coliseum.histoire.village import CheckForKIA
from coliseum.exploration.salles.registre import salle_de_type
```

## 6. Listes de contrôle

**Salle**

- [ ] fonction `@salle_de_type`, dans un fichier importé par `salles/__init__.py`
- [ ] donjon : compteur dans `InitiateRoleToAttribute()` (après le `if / else`), branche dans `AttributingRoleToRoom()`
- [ ] village : entrée dans le dictionnaire de `PrepareTheVillage()`, case adjacente à une case existante
- [ ] icône dans `ICONE_PAR_TYPE_DE_SALLE`
- [ ] livre : `liste_salle_et_equivalent` **et** `DICTIONNAIREDESCRIPTIONCIGOGNEBLANCHE["Les Salles"]`

**Étage**

- [ ] `GoDown()`, `DefinitNomEtage()`, `RemiseAZeroDesVariablesPourProchainEtage()`
- [ ] `AffichageDescriptionEtage()`, `AfficheIntroCombatBoss()`
- [ ] `SetupFloorLayout()`, `InitiateRoleToAttribute()`, nom de la salle secrète
- [ ] monstres de l'arène, `liste_de_boss`, fiches du bestiaire
- [ ] `etage_N.mp3`, `battle_theme_N.mp3`, `boss_N.mp3`
- [ ] `DICTIONNAIREDESCRIPTIONCIGOGNEBLANCHE["Les Etages"]`

**Étage alternatif**

- [ ] déclencheur à l'étage précédent
- [ ] nom dans `DefinitNomEtage()`, `PlayMusicDeLetage()`, `Model.__init__`
- [ ] `liste_de_boss_alternatif` et fiche du boss
- [ ] textes d'arrivée et d'avant-boss
- [ ] `etage_N_alt.mp3`, `battle_theme_N_alt.mp3`, `boss_N_alt.mp3`
- [ ] `DICTIONNAIREDESCRIPTIONCIGOGNEBLANCHE["Les Etages"]`
