# Interface du jeu et exécutable

## 1. Deux écrans possibles

```bash
python Coliseum.py             # fenêtre du jeu : récaps, carte, texte et saisie
python Coliseum.py --console   # terminal, comme à l'origine
```

Le jeu ne sait pas lequel est actif. Il parle à son écran de cinq façons, et
`coliseum/console.py` transmet au terminal choisi au lancement :

| Le jeu écrit | Ce qui se passe |
|---|---|
| `print(...)` | écrit dans `sys.stdout`, que la fenêtre remplace par son propre flux |
| `input(...)` | lit dans `sys.stdin`, remplacé de la même façon |
| `ClearConsole()` | `terminal.effacer()` |
| `attendre(secondes)` | `terminal.attendre(secondes)` |
| `montrer_image(chemin)` | `terminal.montrer_image(chemin)` |

| Terminal | Fichier | Usage |
|---|---|---|
| `TerminalFenetre` | `coliseum/terminal/fenetre.py` | par défaut, et dans l'exécutable |
| `TerminalSysteme` | `coliseum/terminal/systeme.py` | option `--console`, et tests automatiques |

## 2. Règles à respecter dans le code du jeu

- **Jamais `time.sleep`**, toujours `attendre` (`from coliseum.console import attendre`).
  Pendant un `time.sleep`, la fenêtre ne se redessine pas et Windows finit par
  l'afficher « ne répond pas ». La seule exception est `coliseum/audio.py`,
  dont les pauses durent un centième de seconde.
- **Jamais `os.system("cls")`**, toujours `ClearConsole()`.
- **Jamais de nouvelle fenêtre tkinter** (`tk.Tk()`) : passer par
  `montrer_image`, ou ajouter une méthode aux deux terminaux.
- `print` et `input` s'utilisent normalement.
- Les fonctions globales de turtle (`goto`, `forward`, `circle`, `clear`...)
  s'utilisent normalement : elles dessinent dans la carte de la fenêtre.
  `setup(...)` et `title(...)` y sont sans effet.

## 3. Comment la fenêtre fonctionne

```
┌────────────────────────────┬────────────────────────────┐
│ récap du joueur            │ carte de l'étage           │
│ (image + caractéristiques) │ ou, en combat,             │
│                            │ récap du monstre           │
├────────────────────────────┴────────────────────────────┤
│ texte du jeu                                            │
│ > saisie du joueur                                      │
└─────────────────────────────────────────────────────────┘
```

Le haut occupe 40 % de la hauteur et la console 60 % ; les deux zones du
haut, chacune la moitié de la largeur. Pour déplacer la séparation, changer
`POIDS_DU_HAUT` et `POIDS_DE_LA_CONSOLE` en tête de
`coliseum/terminal/fenetre.py` (2 et 3 = 40 % / 60 % ; 1 et 1 = moitié-moitié).
La carte, carrée, prend toute la hauteur du haut.

Le jeu garde la main dans le fil principal. La fenêtre ne « vit » (se
redessine, reçoit le clavier) que pendant que le jeu attend :

| Le jeu fait | La fenêtre fait |
|---|---|
| `input()` | `lire_une_ligne()` fait tourner la boucle d'événements jusqu'à la touche Entrée |
| `attendre(n)` | `attendre()` fait tourner la boucle d'événements pendant `n` secondes |
| `print()` | `ecrire()` ajoute le texte ; il apparaît à la prochaine attente |

Trois comportements à connaître :

- **Pas de saisie en avance.** Une touche Entrée frappée pendant une pause,
  ou pendant que le jeu calcule, est ignorée : seule une ligne validée pendant
  que le jeu attend une réponse compte. Marteler Entrée ne fait donc pas
  défiler les dialogues suivants. (En mode `--console`, c'est le terminal de
  Windows qui garde les frappes : ce comportement n'y existe pas.)
- **Fermeture.** Cliquer sur la croix ne détruit pas la fenêtre sur le coup :
  la demande est notée, et la prochaine attente du jeu lève `SystemExit`,
  exactement comme un `sys.exit()`. Le filet de sécurité ne se déclenche pas.
- **Fils secondaires.** Pêche, jacuzzi et pierre de sang affichent du texte
  depuis un second fil pendant que le fil principal attend la saisie. tkinter
  n'acceptant qu'un seul fil, ces écritures passent par une file d'attente
  vidée trente fois par seconde par le fil principal.

### La carte

turtle dessine normalement dans une fenêtre à lui. `TerminalFenetre` crée son
propre canevas, puis installe un écran et un crayon turtle dessus **avant** le
premier dessin du jeu :

```python
turtle.Turtle._screen = ecran
turtle.Turtle._pen = turtle.RawTurtle(ecran)
```

Les fonctions globales de turtle utilisent ces deux objets s'ils existent, et
n'ouvrent donc jamais de seconde fenêtre. Les dessins de
`coliseum/interface/dessin.py` n'ont pas été modifiés. Tant que le joueur
n'a pas la carte (livraison « Carte » couvrant l'étage, et carte remise par le
marchand de l'étage 1), `-- No Data Found --` s'affiche à sa place : voir
`carte_possedee()` dans `recapitulatif.py`, qui reprend la condition de
`ColiseumGoto`. Pendant un
combat, la carte n'est pas effacée : le récap du monstre est posé devant
elle, et elle réapparaît telle quelle à la fin du combat.

### Ajouter un troisième écran

Écrire une classe avec les méthodes `effacer`, `attendre`, `montrer_image`,
`fermer`, qui remplace `sys.stdout` et `sys.stdin` à sa création, puis la
passer à `console.utiliser(...)` dans `Coliseum.py`.

## 4. Les récaps du joueur et du monstre

Un récap est une image qui couvre toute sa zone, avec des cadres par-dessus :
caractéristiques à gauche et à droite, nom en haut, listes plus longues
(stigmas, objets, artefacts, altérations d'état) en bas. Il ne remplace pas la
fiche de personnage ni l'utilisation des objets, qui restent dans la console.

### Qui fait quoi

| Fichier | Rôle | Connaît |
|---|---|---|
| `coliseum/interface/recapitulatif.py` | lit l'état du jeu, fabrique un `Recap` | le jeu, pas tkinter |
| `coliseum/terminal/panneau.py` | dessine un `Recap` | tkinter, pas le jeu |
| `coliseum/terminal/fenetre.py` | interroge le premier, donne le résultat au second | les deux |

Un `Recap` contient : `titre`, `sous_titre`, `image` (chemin complet ou
`None`), `gauche` et `droite` (des `Cadre` : étiquette, valeur, jauge
facultative), `bas` (des `Bloc` : titre et liste de courts textes).

### Le suivi en temps réel

```
toutes les 150 ms, et juste avant chaque saisie :
fenetre._mettre_a_jour_les_recaps()
 ├─ recap_du_joueur()   → Recap, ou None si aucun personnage n'est choisi
 ├─ recap_du_monstre()  → Recap, ou None hors combat
 ├─ panneau.montrer(recap)      ne redessine que si le Recap a changé
 └─ monstre présent ? son récap passe devant la carte ; sinon la carte revient
```

Le jeu ne prévient jamais l'écran : c'est l'écran qui relit l'état. Aucune
attaque, salle ou objet n'a donc à s'occuper du récap, y compris ceux qui
seront ajoutés plus tard.

| Moment | D'où viennent les valeurs du joueur |
|---|---|
| hors combat | `services.Player` |
| pendant un combat | le modèle du combat (`control.modele`), que le combat modifie |
| récompenses de fin de combat | `services.Player` à nouveau |

Le combat s'annonce lui-même, dans `Control` (`combat/controleur.py`) :
`suivre_le_combat(self)` dès que le monstre est créé, `oublier_le_combat()`
dans un `finally` avant les récompenses. Tout combat passant par `Battle()`
est donc suivi, sans rien faire de plus.

Une erreur dans le calcul d'un récap n'arrête pas le jeu : elle est écrite une
fois dans le journal des erreurs, et le récap concerné se vide.

### Les images

| Pour | Où donner le chemin |
|---|---|
| un monstre | `image=...` dans sa `FicheMonstre` (fiche 02) |
| un personnage | `IMAGES_DES_PERSONNAGES` dans `donnees/personnages.py` (fiche 03) |

```python
image=r"images\monstres\rat_geant.png"     # = ColiseumDependencies\images\monstres\rat_geant.png
```

- Le chemin part de `ColiseumDependencies`. Ce dossier est copié tel quel à
  côté de l'exécutable : les images suivent sans autre réglage.
- **PNG ou GIF uniquement.** tkinter ne lit pas le JPEG sans bibliothèque
  supplémentaire.
- L'image est agrandie ou réduite pour couvrir toute la zone, centrée, sans
  être déformée : ce qui dépasse est coupé. La zone est environ 1,65 fois plus
  large que haute ; une image de 960 × 580 pixels, sujet au centre, convient.
  Les bords gauche, droit et bas sont recouverts par les cadres.
- La mise à l'échelle de tkinter est rudimentaire (pas de lissage) : une image
  proche de la taille d'affichage rend mieux qu'une très grande image réduite.
- Pas de chemin, ou fichier introuvable ou illisible : `-- No Data Found --`
  s'affiche à la place de l'image, les cadres restent.

### Changer ce qui est affiché

Tout se passe dans `recapitulatif.py` : `_recap_hors_combat` et
`_recap_en_combat` pour le joueur, `recap_du_monstre` pour le monstre. Ajouter
une ligne `_cadre("Âmes", joueur.nombre_de_monstres_tues)` à `gauche` suffit à
faire apparaître un cadre. Un cadre qui ne tient plus dans la hauteur n'est
pas dessiné ; une liste du bas trop longue est coupée à deux lignes et se
termine par `+N`.

Les altérations d'état sont reprises de
`ConstruirePhraseAlterationEtatPourVue()` (`combat/alterations.py`), la méthode
qui les liste déjà pour la console : une altération ajoutée là apparaît dans
le récap sans autre modification.

## 5. L'exécutable

### Ce qu'il faut savoir d'abord

Un programme qui utilise `print` et `input` **peut** être transformé en
exécutable : PyInstaller produit par défaut un exécutable qui ouvre une
console. Ce n'était donc pas la console qui bloquait. La fenêtre apporte autre
chose : une seule fenêtre au lieu de deux (console + carte turtle), un
affichage identique sur toutes les machines, et un exécutable sans console
noire.

### Fabriquer

```bash
py -3.12 -m pip install pygame==2.5.2 pyinstaller
```

```bash
py -3.12 outils/construire_executable.py
```

Le résultat est le dossier `dist/Coliseum/`. Pour distribuer le jeu, zipper ce
dossier entier ; le joueur le dézippe et double-clique sur `Coliseum.exe`. Il
n'a besoin ni de Python ni de pygame.

| Dans `dist/Coliseum/` | Rôle |
|---|---|
| `Coliseum.exe` | le jeu |
| `_internal/` | Python, pygame et tkinter embarqués par PyInstaller |
| `ColiseumDependencies/` | musiques, bruitages, images, et sauvegardes **vierges** |

### Icône

Poser un fichier `icone.ico` dans `ColiseumDependencies`, puis reconstruire.
Il sert à la fois à `Coliseum.exe` (option `--icon` de PyInstaller, ajoutée
par le script si le fichier existe) et à la fenêtre du jeu (`_poser_l_icone`
dans `fenetre.py`). Il faut un vrai fichier `.ico`, idéalement avec les
tailles 16, 32, 48 et 256 pixels ; un `.png` renommé ne fonctionne pas.

### Points d'attention

- **Python du Microsoft Store.** PyInstaller ne fonctionne pas avec lui
  (erreur `WinError 1920`). Utiliser un Python installé depuis python.org.
  C'est pour cela que la commande utilise `py -3.12` et non `python`.
- **Un dossier, pas un fichier unique.** L'option `--onefile` décompresserait
  700 Mo de musiques à chaque lancement, dans un dossier temporaire effacé à
  la fermeture : les sauvegardes seraient perdues.
- **Sauvegardes.** Dans l'exécutable, `coliseum/chemins.py` place la racine du
  jeu à côté de `Coliseum.exe` (`sys.frozen`). `save.txt` et `s0ve.txt` sont
  donc lus et écrits dans `dist/Coliseum/ColiseumDependencies/`. Le script y
  copie la version du dépôt git (`git show HEAD:...`), pas vos sauvegardes
  personnelles.
- **Dossier protégé.** Le jeu écrit à côté de son exécutable. Installé dans
  `C:\Program Files`, il n'aurait pas le droit d'y écrire : le laisser dans un
  dossier de l'utilisateur.
- **Antivirus.** Un exécutable PyInstaller non signé peut être signalé par
  Windows SmartScreen ou un antivirus au premier lancement.
- **Crash sans console.** Si le jeu plante avant que sa fenêtre existe, il n'y
  a nulle part où écrire : `coliseum/erreurs.py` affiche alors le rapport dans
  une boîte de dialogue, en plus du journal.
