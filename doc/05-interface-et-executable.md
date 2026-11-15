# Interface du jeu et exécutable

## 1. Deux écrans possibles

```bash
python Coliseum.py             # fenêtre du jeu : texte, saisie et carte
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
┌──────────────────────────────────────┬──────────────────┐
│ texte du jeu                         │ carte de l'étage │
├──────────────────────────────────────┤ (dessin turtle)  │
│ > saisie du joueur                   │                  │
└──────────────────────────────────────┴──────────────────┘
```

Le jeu garde la main dans le fil principal. La fenêtre ne « vit » (se
redessine, reçoit le clavier) que pendant que le jeu attend :

| Le jeu fait | La fenêtre fait |
|---|---|
| `input()` | `lire_une_ligne()` fait tourner la boucle d'événements jusqu'à la touche Entrée |
| `attendre(n)` | `attendre()` fait tourner la boucle d'événements pendant `n` secondes |
| `print()` | `ecrire()` ajoute le texte ; il apparaît à la prochaine attente |

Trois comportements à connaître :

- **Saisie en avance.** Une ligne validée pendant une pause est gardée et
  servie au `input()` suivant, comme dans une console.
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
`coliseum/interface/dessin.py` n'ont pas été modifiés. La carte reste vide
tant que le jeu ne la dessine pas (il faut la livraison « Carte »).

### Ajouter un troisième écran

Écrire une classe avec les méthodes `effacer`, `attendre`, `montrer_image`,
`fermer`, qui remplace `sys.stdout` et `sys.stdin` à sa création, puis la
passer à `console.utiliser(...)` dans `Coliseum.py`.

## 4. L'exécutable

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
