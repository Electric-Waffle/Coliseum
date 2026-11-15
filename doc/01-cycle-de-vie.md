# Cycle de vie de l'application

Cette fiche répond à trois questions : où sont les données, dans quel ordre le
jeu s'exécute, et par quelles fonctions on passe pour faire telle action.

Tous les chemins sont relatifs à la racine du projet.

## 1. Où se trouvent les choses

### Sur le disque

| Emplacement | Contenu |
|---|---|
| `Coliseum.py` | Point d'entrée. Lance le jeu sous le filet de sécurité global. |
| `coliseum/` | Tout le code. |
| `ColiseumDependencies/*.mp3` | Musiques. |
| `ColiseumDependencies/sfx/*.wav` | Bruitages de combat. |
| `ColiseumDependencies/__py.property__/` | Images des pages secrètes. |
| `ColiseumDependencies/save.txt` | Sauvegarde de la run en cours. Réinitialisée à la fin de la run. |
| `ColiseumDependencies/s0ve.txt` | Sauvegarde permanente : tout ce qui reste débloqué d'une run à l'autre. |
| `ColiseumDependencies/s1ve.txt` | Si ce fichier existe, il remplace `s0ve.txt` (mode Ascension). |
| `ColiseumDependenciesErrorLog.txt` | Journal des erreurs. |

Aucun module ne calcule ces chemins lui-même : ils viennent tous de
`coliseum/chemins.py` (`DOSSIER_RACINE`, `DOSSIER_RESSOURCES`, `JOURNAL_DES_ERREURS`).

### Dans le code

| Dossier | Rôle |
|---|---|
| `application.py` | Boucle principale et tables d'actions des menus. |
| `services.py` | Annuaire des neuf objets uniques (voir plus bas). |
| `erreurs.py` | Les deux filets de sécurité. |
| `audio.py`, `console.py`, `chemins.py`, `outils.py` | Socle technique. |
| `donnees/` | Constantes : personnages, techniques, sorts, objets, artefacts, prix du village, textes. |
| `joueur/` | Le joueur, ses talents, ses bénédictions, ses bonus. |
| `interface/` | Menus, textes hors combat, dessin de la carte. |
| `exploration/` | Carte d'étage, passage d'un étage à l'autre, et `salles/`. |
| `commerce/` | Marchand du Coliseum et commerçants du village. |
| `sauvegarde/` | Lecture et écriture de `save.txt` et `s0ve.txt`. |
| `histoire/` | Étage 0, arrivée au village, fins du jeu. |
| `combat/` | Tout le combat, dont `bestiaire/`. |

### En mémoire : les objets uniques

`coliseum/services.py` crée neuf objets au lancement. On y accède partout par
`services.Nom`.

| Objet | Classe | Fichier | Ce qu'il porte |
|---|---|---|---|
| `services.Player` | `PlayerCaracteristics` | `joueur/caracteristiques.py` | Toute la run : caractéristiques, inventaire, étage, tags. |
| `services.FloorMaker` | `Floor` | `exploration/etage.py` | La carte de l'étage (`FloorBlueprint`) et les mini-jeux. |
| `services.Trader` | `TraderUsage` | `commerce/marchand.py` | Marchand et commerçants. |
| `services.Affichage` | `Affiche` | `interface/affichage.py` | Textes et écrans hors combat. |
| `services.Draw` | `DrawInTurtle` | `interface/dessin.py` | Dessin de la carte (turtle). |
| `services.Save` | `SaveManagement` | `sauvegarde/partie.py` | `save.txt`. |
| `services.Sove` | `SoveManagement` | `sauvegarde/permanente.py` | `s0ve.txt`, par thème. |
| `services.Observation` | `Observe` | `exploration/observation.py` | Lieux spéciaux, et lecture/écriture brute de `s0ve.txt`. |
| `services.Ending` | `EndingAndGift` | `histoire/fin.py` | Fins du jeu. |

Deux états transversaux sont à connaître, tous deux dans `services.Player` :

- `player_tags` : liste de marqueurs temporaires ("Fantome", "Jeu Fini", "KIA",
  "Combattant le Gardien", "Monstre Dopé"...). Beaucoup de décisions du jeu se
  prennent en testant la présence d'un tag.
- `numero_de_letage` et `nom_de_letage` : `-1` est le village, `0` à `11` le
  Coliseum. Le **nom** distingue un étage de sa version alternative.

## 2. Du lancement à la boucle principale

```
python Coliseum.py
 └─ erreurs.executer_avec_rapport_de_crash(lancer)
     └─ application.lancer_le_jeu()
         1. audio.initialiser()                    ouvre le son, réserve 2 canaux
         2. services.initialiser()                 crée les neuf objets uniques
         3. sauvegarde.partie.SetupGameMode()      lit s0ve.txt -> Player.mode_de_jeu
         4. interface.secrets.AffichageSecretPage3()
         5. sauvegarde.partie.GetNomEtageEtDebugValues()   lit save.txt (nom d'étage, debug)
         6. interface.menu_demarrage.MenuDeDemarrage()     nouvelle partie / continuer / tutoriel
         7. boucle infinie : _jouer_une_action()
```

`Player.mode_de_jeu` vaut "Descente", "Véritable Descente", "Ascension" ou
"Erreur" (pas de sauvegarde permanente : le jeu s'arrête).

### Menu de démarrage

- **Nouvelle partie** : `ChoseCharacter()` -> `Player.UseCharacterForInitCaracteristics()`
  -> `Save.FromPlayerToDict()` -> `Save.FromDictToSaveFile()` -> `Affichage.AffichageDescriptionEtage()`
  -> `FloorMaker.SetupFloorLayout()` (génère la carte du premier étage).
- **Continuer** : `Save.LoadTheGame()` = `FromSaveFileToDict()` + `FromDictToPlayer()`.

### Une itération de la boucle

`application._jouer_une_action()` :

1. `Draw.__init__()` relit dans la sauvegarde permanente si la carte peut être dessinée.
2. `interface.menu_coliseum.GetChoix()` affiche le menu et retourne un numéro.
3. Le numéro est cherché dans `ACTIONS_DU_VILLAGE` (étage `-1`) ou
   `ACTIONS_DU_COLISEUM`, et la fonction trouvée est appelée.
4. Au Coliseum, si le joueur porte le tag "Fantome" ou "Jeu Fini",
   `histoire.village.PrepareTheVillage()` l'envoie au village.

Le jeu ne sort de cette boucle que par `sys.exit()` (menu de sauvegarde, game over) ou par un crash.

## 3. Par où passe chaque action

### Menu du Coliseum (`ACTIONS_DU_COLISEUM`)

| Choix | Fonction | Suite |
|---|---|---|
| 1 Affronter un monstre | `_combattre_dans_l_arene` | `combat.lancement.DoFight()` (jukebox à l'étage 10) |
| 2 Boss / descendre | `_affronter_le_boss_ou_descendre` | `exploration.progression.DoBossOrGoDown()` (étage 0 : `histoire.boss_zero.DoBossZero()`) |
| 3 Marchand | `_voir_le_marchand` | `Trader.DoTrading()` |
| 4 Explorer l'étage | `FloorMaker.ShowFloor()` | voir « Explorer » |
| 5 Fiche de personnage | `_ouvrir_la_fiche_de_personnage` | `Player.ShowPlayerCaracteristicsAndItems()` |
| 6 Red Coin | `_depenser_les_redcoins` | `joueur.talents.DoRedcoin()` |
| 7 Sauvegarder | `_sauvegarder` | `Save.SaveTheGame()` |
| 8 Debug | `_ouvrir_le_menu_de_debug` | `interface.menu_debug.ShowDebugMenu()` |

### Menu du village (`ACTIONS_DU_VILLAGE`)

| Choix | Fonction |
|---|---|
| 1 Se promener | `FloorMaker.ShowFloor()` : le même système de carte que le donjon |
| 2 Sauvegarder | `Save.SaveTheGame()` |
| 3 Parler aux villageois | `Affichage.ParleAuPnj()` ou `ParleAuPnjNuit()` |

### Explorer (donjon et village)

```
FloorMaker.ShowFloor()
 ├─ PrintFloorBlueprint()        dessine la carte (si la livraison « Carte » le permet)
 └─ WalkInFloor()                boucle : 4/6/8/2 se déplacer, 5 observer, 0 fiche
     ├─ WalkLeft/Right/Up/Down() + CheckPlayerPosition()
     └─ RevealRoom()
         └─ exploration.salles.reveler_la_salle(etage, salle)
             └─ la fonction @salle_de_type correspondant à salle["type"]
```

Le donjon et le village ne diffèrent que par le contenu de `FloorBlueprint` :
généré aléatoirement pour un étage (`SetupFloorLayout`), écrit en dur pour le
village (`PrepareTheVillage`). Voir la fiche 04.

### Combattre

```
combat.lancement.livrer_combat()                filet local : une erreur ne tue pas la partie
 └─ combattre()
     ├─ controleur.Control(Player, Trader, FloorMaker, Sove)
     │    ├─ vue.Vue(Player)
     │    └─ modele.Model(Player)               copie l'état du joueur dans le modèle
     └─ Control.Battle()
         ├─ _preparer_le_combat()               monstre, musique, premiers tours
         ├─ boucle : tour du joueur, tour du monstre, FinTour()
         ├─ CheckForGameOver()
         └─ MontreFuiteOuRecompense()           recopie le modèle dans le joueur
```

Pendant le combat, rien n'est écrit dans `services.Player` : tout vit dans le
modèle. C'est `MontreFuiteOuRecompense` (`combat/fin_de_combat.py`) qui
recopie vie, mana, or, objets et récompenses dans le joueur. Le détail du tour
est dans la fiche 02.

### Changer d'étage

```
exploration.progression.DoBossOrGoDown()
 ├─ boss pas encore battu  -> combat.lancement.DoBossFight()
 └─ boss battu             -> GoDown()
                               ├─ Player.numero_de_letage += 1
                               ├─ DefinitNomEtage()                         nom normal ou alternatif
                               ├─ RemiseAZeroDesVariablesPourProchainEtage()
                               └─ Affichage.AffichageDescriptionEtage()
                              puis audio.PlayMusicDeLetage() et FloorMaker.SetupFloorLayout()
```

`GoDown()` retourne `False` quand la run est finie (étage 12, ou étage 9 sans
la « Marque du Sacrifice ») : `application` ajoute alors le tag "Jeu Fini" et
appelle `Ending.DoEnding()`.

### Mourir, finir, aller au village

- Mort en combat : `CheckForGameOver` pose des tags sur le joueur ; au retour,
  `histoire.village.CheckForKIA()` affiche la mort si le tag "KIA" est présent.
- Tag "Fantome" ou "Jeu Fini" : `PrepareTheVillage()` remet la run à zéro,
  installe la carte du village et passe `numero_de_letage` à `-1`.

### Sauvegarder et charger

| Action | Chemin |
|---|---|
| Sauver la run | `Save.FromPlayerToDict()` puis `Save.FromDictToSaveFile("\\save.txt")` |
| Sauver sans message | `Save.SaveTheGameSansAffichage()` (appelée après chaque génération d'étage) |
| Charger la run | `Save.FromSaveFileToDict()` puis `Save.FromDictToPlayer()` |
| Lire le permanent | `Observation.GetPermanentThingsFromS0ve()` retourne un dictionnaire |
| Écrire le permanent | `Observation.SetPermanentThingsToS0ve(dictionnaire)` |
| Permanent, par thème | `Sove.ModifieTagsDansSove`, `ModifieArtefactDansSove`, `ModifieRumeursDansSove`, `ModifieRecettesDansSove`, `ModifieLivraisonDansSove`, `ModifieDechetsDansSove`, `ModifieCigogneBlancheDansSove`... |

Les méthodes `Sove.Modifie...DansSove(type_de_action, ...)` prennent une action
en premier argument : "Ajout", "Enleve", "Checke" (retourne un booléen),
"Donne" (retourne la valeur). Exemple : `Sove.ModifieTagsDansSove("Checke", "Village Jour")`.

**Ajouter une donnée à sauvegarder dans la run** demande trois modifications
dans `sauvegarde/partie.py` et `joueur/caracteristiques.py` :

1. une valeur par défaut dans `PlayerCaracteristics.__init__` ;
2. une ligne dans `FromPlayerToDict` (joueur -> dictionnaire) ;
3. une ligne dans `FromDictToPlayer` (dictionnaire -> joueur).

Attention : `FromDictToPlayer` lit chaque clé sans valeur par défaut. Une
sauvegarde écrite avant l'ajout de la clé plante au chargement (`KeyError`).

## 4. Les erreurs

Deux filets, tous deux dans `coliseum/erreurs.py` :

| Filet | Où | Effet |
|---|---|---|
| Local : `WriteErrorInErrorLog(erreur)` | dans un `except Exception` autour d'un combat, d'une salle, d'une génération d'étage | journal + soin et or de dédommagement, la partie continue |
| Global : `executer_avec_rapport_de_crash(lancer)` | une seule fois, dans `Coliseum.py` | rapport à l'écran + journal, attente d'Entrée, code de sortie 1 |

`sys.exit()` lève `SystemExit`, qui n'hérite pas de `Exception` : quitter le
jeu traverse les deux filets sans les déclencher. Il ne faut donc jamais écrire
`except:` nu ni `except BaseException:` dans le jeu.

## 5. Le son

| Besoin | Fonction (`coliseum/audio.py`) |
|---|---|
| Musique en boucle | `PlayMusic("nom")` joue `ColiseumDependencies/nom.mp3` |
| Son joué une fois | `PlaySound("nom")` |
| Bruitage sur le second canal | `PlaySFX("nom")`, `PermanentPlaySFX("nom")` en boucle |
| Musique de l'étage | `PlayMusicDeLetage()` joue `etage_<numéro>.mp3`, ou `etage_<numéro>_alt.mp3` |
| Tout couper | `StopAllMusic()` |

Le combat a ses propres canaux, gérés par `combat/vue.py` (`PlayMusic`,
`AfficheSonSort`, `AfficheSonTechnique`).
