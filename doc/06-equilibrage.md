# Équilibrage du combat : comment les chiffres sont calculés

Cette fiche décrit les formules de dégâts, de défense et de drop, et dit où
changer chaque valeur. Elle sert aussi de guide pour **écrire la description**
d'un bonus sans le faire passer pour ce qu'il n'est pas.

## 1. Le « pool » de dégâts bonus

Les bonus de dégâts en pourcentage **s'additionnent entre eux**, puis la somme
est appliquée **une seule fois** à la dégât de base.

```
pool (en %)  = 2 x étage + 10 x force + PV max / 10 + stigmas + objets + artefacts...
dégât        = base x (1 + pool / 100)
```

Pour les sorts : intelligence au lieu de force, mana max / 10 au lieu de PV max / 10.
Le code est dans `coliseum/combat/preparation.py` (`DEGATBONUSATTAQUE`,
`DEGATBONUSSORTS`) et l'application dans `UseAttack` et `UseMagic`
(`actions_joueur.py`).

### Exemple : une technique de base 27, étage 5, force 12, 150 PV max

| | Pool | Dégât |
|---|---|---|
| Sans artefact | 10 + 120 + 15 = **145 %** | 27 x 2,45 = **66** |
| Avec l'Épée de Damocles (+25 %) | 145 + 25 = **170 %** | 27 x 2,70 = **73** |

L'Épée ne multiplie pas 66 par 1,25 (ce qui ferait 83) : elle **ajoute 25 points
de bonus à la somme**. Elle vaut donc 2,5 points de force, puisqu'un point de
force donne +10 %.

### Quelle part du total un bonus représente-t-il ?

Un bonus de `X` points rapporte `X / (100 + pool)` du dégât total :

| Pool déjà présent | +25 de bonus | +100 de bonus (gel) | +300 de bonus (orbe) |
|---|---|---|---|
| +50 % | +17 % | +67 % | +200 % |
| +145 % | +10 % | +41 % | +122 % |
| +300 % | +6 % | +25 % | +75 % |
| +600 % | +3,6 % | +14 % | +43 % |

Plus le pool est grand, plus un même bonus pèse peu **dans le total**. Il
reste toujours la même quantité de bonus ajoutée à la somme.

### Écrire la description d'un bonus

Dire **« +25 % de dégâts bonus »**, jamais « augmente les dégâts de 25 % » : la
seconde formule promet un multiplicateur du résultat. Modèle utilisé pour les
artefacts : *« Ajoute +25% de dégâts bonus a vos techniques (ils s'additionnent
a vos autres bonus de dégâts) »*.

### Les trois sortes d'effets

| Sorte | Exemple | Ce qu'il fait |
|---|---|---|
| **Plat** | +8 force, +10 dégâts critiques, +15 PV max | ajoute une valeur à une stat ou à un résultat |
| **Pourcentage additif** | +25 % de dégâts bonus, gel (+100 %) | s'ajoute à la somme du pool |
| **Multiplicateur du pool** | Cape Victorieuse, Contrat de Travail | multiplie la somme du pool (plafonné à +100 %) |

La résistance du monstre et la défense du joueur sont des **réductions** : elles
s'appliquent après le pool (voir plus bas).

### Ordre du calcul d'un coup du joueur

1. pool, puis `base x (1 + pool / 100)` ;
2. réduction par la résistance du monstre (2 % par point, 60 % au plus) ;
3. si critique, la valeur de critique s'ajoute (valeur fixe) ;
4. les statuts (brûlure...) sont calculés à part, en % des PV max du monstre.

## 2. Défense du joueur et résistance des monstres

Fichier : `coliseum/combat/reductions.py`.

**Défense du joueur**, pour un coup de `dégât` avant défense :

```
1. après % : dégât x (1 - min(60 %, 2 % x défense))
2. après plat : - 0,5 x défense
3. plancher : au moins 15 % du dégât d'origine, et jamais moins de 1
```

| Coup avant défense | Défense 2 | 10 | 20 | 40 | 60 |
|---|---|---|---|---|---|
| 5 | 4 | 1 | 1 | 1 | 1 |
| 30 | 28 | 19 | 8 | 4,5 | 4,5 |
| 100 | 95 | 75 | 50 | 20 | 15 |

**Résistance du monstre** : 2 % par point, plafond 60 %, sans partie plate (les
coups du joueur grandissent avec sa force, une réduction plate serait
négligeable).

À savoir :
- les attaques qui retirent un **pourcentage des PV du joueur** (Rituel,
  Lamentations...) ignorent la défense ;
- la brûlure du joueur est un pourcentage des PV max : elle subit la réduction en
  pourcentage mais pas la partie plate (`avec_reduction_plate=False`) ;
- Miss Hyde retire 25 points de défense (50 % de réduction avant le changement).

**Esquive.** L'esquive utile est plafonnée à **50** (`ESQUIVE_UTILE_MAX`) pour la
chance de ne pas être touché. L'esquive donne aussi la moitié de sa valeur en
chance de toucher et un tiers en chance de critique, sans plafond.

## 3. Bonus d'étage des monstres

Les attaques **normales** des monstres reçoivent **+6 de dégâts bonus par étage
au dessus du premier** (`BONUS_DEGATS_MONSTRE_PAR_ETAGE` dans `preparation.py`),
dans la même somme que leur bonus de force. Les attaques spéciales n'en
reçoivent pas : leur base grandit déjà d'un point par étage (« base + niveau du
monstre »).

## 4. Attaques spéciales et esquive

Sept attaques spéciales qui n'avaient aucun jet de touche reçoivent maintenant
le jet commun (`SPECIALES_AVEC_JET_D_ESQUIVE` dans `attaques_speciales.py`) :
Laser, Éveil de Runes, Tournicotons, Dragon Ascendant, Vacarme Rapide, Rituel,
Lamentations.

Chance d'être touché = `100 - esquive` (esquive plafonnée à 50) : sans esquive
rien ne change, au mieux l'attaque touche une fois sur deux. Laissées de côté
volontairement : Laser Anti-Personnel et Protocole Supernova (décrits comme
inévitables), Roulette (plusieurs issues), Ultima, Aspiration, et celles qui
ont déjà leur jet.

**Jugement** : les dégâts dépendent du nombre d'âmes mais saturent.

```
part des PV max du joueur = 25 % x âmes / (âmes + 20)
```

| Âmes | 10 | 20 | 30 | 60 | 100 | 150 | 250 |
|---|---|---|---|---|---|---|---|
| PV max perdus | 8,3 % | 12,5 % | 15 % | 18,8 % | 20,8 % | 22,1 % | 23,1 % |

## 5. Brûlure

La brûlure retire un pourcentage des **PV max** de sa cible à chaque tour. Elle
ignore donc la résistance et la force. Elle est maintenant bornée
(`coliseum/combat/alterations.py`) :

| | Monstre normal | Boss | Joueur |
|---|---|---|---|
| Pourcentage maximal par tour (palier + bonus, ex. Ange de Feu) | 8 % | 3 % | (inchangé) |
| Coup de grâce maximal (brûler une cible déjà en feu, 10 % des cas) | 20 % | 8 % | 15 % |
| Durée maximale restante, tous bonus confondus | 8 tours | 8 tours | (inchangé) |

Le coup de grâce oubliait de diviser par 100 : il infligeait environ vingt fois
les PV max de la cible (mort immédiate, boss comprise). Corrigé.

**Sables du Temps** (Maître Mage) efface maintenant bien la vulnérabilité et le
poison ; il testait la brûlure, déjà effacée à ce moment-là.

## 6. Drop de matériaux : compteur de malchance

Fichier : `coliseum/combat/drop.py`. Un monstre ne lâche que son matériau avec
environ 25,7 % de chance (jusqu'à 50,5 % avec le Médaillon de Leprechaun 5).

Chaque type de monstre a un compteur d'échecs consécutifs, sauvegardé dans
`s0ve.txt` (clé « Compteur de drop », créée au premier enregistrement). Chance
du tirage suivant = `(échecs + 1) x C`, remise à zéro au drop. `C` est calculée
pour garder la **moyenne** d'origine : 8,95 % à 25,7 % (au pire 12 échecs de suite),
30,7 % à 50,5 % (au pire 4). Une mimique lâche toujours son matériau.

## 7. Artefacts à valeur plate qui grandissent avec l'étage

| Artefact | Valeur |
|---|---|
| Écaille d'Ouroboros (par sort) | 1,5 x étage PV, arrondi |
| Orbe de Disruption (monstre à mana brisé) | 6 x étage PV perdus en plus des 15 de base |
| Pin's Extincteur (fin de brûlure) | 2 x étage PV et 1,5 x étage PM |

Les PV du joueur montent d'environ 25 par étage : `valeur x étage` garde un poids
à peu près constant (5 à 8 % des PV).

**Cape Victorieuse** et **Contrat de Travail** agrandissent le pool : de 0,5 % par
monstre tué, et de 1 % par paquet de 50 pièces. La somme de leurs deux bonus est
plafonnée à +100 % (`PLAFOND_AMELIORATION_DEGATS_TOTAUX`), c'est à dire que le
pool au maximum double.

## 8. Mana et améliorations permanentes

- **Mana** : 3 % du mana max (au moins 1) reviennent à la fin de chaque tour
  (`RegenerationDeManaParTour`, `controleur.py`).
- **Améliorations** (`coliseum/joueur/bonus.py`) : Bracelet et Chapeau donnent
  +3 par niveau (au lieu de 4), les Charges élémentaires +10 % de dégâts bonus
  par niveau (au lieu de 5 %).

## 9. Où changer une valeur

| Pour changer | Fichier et constante |
|---|---|
| Pourcentage de défense, plafond, plat, plancher | `combat/reductions.py` |
| Esquive utile maximale | `combat/reductions.py` : `ESQUIVE_UTILE_MAX` |
| Bonus de dégâts par étage des monstres | `combat/preparation.py` : `BONUS_DEGATS_MONSTRE_PAR_ETAGE` |
| Plafond de Cape et Contrat | `combat/preparation.py` : `PLAFOND_AMELIORATION_DEGATS_TOTAUX` |
| Plafonds de la brûlure | `combat/alterations.py` : `PLAFOND_BRULURE_*`, `PLAFOND_COUP_DE_GRACE_*`, `DUREE_MAX_DE_LA_BRULURE` |
| Attaques spéciales esquivables | `combat/attaques_speciales.py` : `SPECIALES_AVEC_JET_D_ESQUIVE` |
| Courbe de Jugement | `combat/attaques_speciales.py` : méthode `Jugement` |
| Chance de drop | `combat/drop.py` |
| Régénération de mana | `combat/controleur.py` : `RegenerationDeManaParTour` |
