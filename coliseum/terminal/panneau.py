"""Panneau de récap : une image de fond et des cadres de caractéristiques.

    ┌─────────────────────────────────────────────┐
    │ ┌ Vie ─ 32/40 ┐    Nom      ┌ Force ──── 4 ┐ │
    │ ┌ Mana ─ 8/15 ┐  sous-titre ┌ Défense ── 2 ┐ │
    │ ┌ Golds ── 12 ┐             ┌ Esquive  8 % ┐ │
    │               image de fond                  │
    │ ┌ Objets : Remède x5 · Fléchette Bleue x2 ─┐ │
    │ ┌ Artefacts : Bocle de Philoctète ─────────┐ │
    └─────────────────────────────────────────────┘

Le panneau reçoit un `Recap` (coliseum/interface/recapitulatif.py) et le
dessine. Il ne sait rien du jeu : le même panneau sert au joueur et au monstre.

FLUX : `montrer(recap)` est appelé plusieurs fois par seconde par la fenêtre.
Si le récap est égal au précédent, rien ne se passe. Sinon tout le panneau
est effacé et redessiné : avec une trentaine de formes, c'est instantané et
bien plus simple que de retrouver quelle forme modifier.
"""

import tkinter as tk
import tkinter.font

TEXTE_SANS_IMAGE = "-- No Data Found --"
COULEUR_FOND = "#0c0c0c"
COULEUR_DU_CADRE = "#161616"
COULEUR_DU_BORD = "#5a5a5a"
COULEUR_ETIQUETTE = "#9a9a9a"
COULEUR_VALEUR = "#ffffff"
COULEUR_JAUGE_VIDE = "#333333"
SEPARATEUR = "  ·  "
LIGNES_MAX_PAR_BLOC = 2
# Le zoom d'une image tkinter est une fraction de deux entiers ; plus le
# dénominateur autorisé est grand, plus la taille obtenue est précise.
DENOMINATEUR_MAX_DU_ZOOM = 8


class PanneauDeRecap:

    def __init__(self, parent, famille_de_police, taille_de_police):
        self._recap = None
        self._image_source = None       # (chemin, image d'origine)
        self._image_ajustee = None      # ((chemin, largeur, hauteur), image à la taille du panneau)
        self._police = tkinter.font.Font(family=famille_de_police, size=taille_de_police)
        self._police_grasse = tkinter.font.Font(family=famille_de_police, size=taille_de_police, weight="bold")
        self._police_du_titre = tkinter.font.Font(family=famille_de_police, size=taille_de_police + 3, weight="bold")
        self._ligne = self._police.metrics("linespace")
        self._marge = max(4, self._ligne // 2)

        # Taille demandée minimale : c'est la fenêtre qui fixe la place.
        self.widget = tk.Canvas(parent, width=1, height=1, background=COULEUR_FOND, highlightthickness=0)
        # `<Configure>` : le canevas vient de changer de taille.
        self.widget.bind("<Configure>", lambda evenement: self._dessiner())

    def montrer(self, recap):
        """Affiche `recap` (ou l'écran vide si None). Ne redessine que s'il a changé."""
        if recap == self._recap:
            return
        self._recap = recap
        self._dessiner()

    # ------------------------------------------------------------------ dessin

    def _dessiner(self):
        canevas = self.widget
        largeur, hauteur = canevas.winfo_width(), canevas.winfo_height()
        canevas.delete("all")
        if largeur < 50 or hauteur < 50:
            return
        recap = self._recap
        image = self._image_couvrante(recap.image, largeur, hauteur) if recap is not None else None
        if image is not None:
            canevas.create_image(largeur // 2, hauteur // 2, image=image)
        if recap is None:
            self._ecrire_l_absence_d_image(largeur // 2, hauteur // 2)
            return

        haut_du_bas = self._dessiner_le_bas(recap.bas, largeur, hauteur)
        largeur_de_colonne = min(int(largeur * 0.30), self._police.measure("0") * 28)
        self._dessiner_une_colonne(recap.gauche, self._marge, largeur_de_colonne, haut_du_bas)
        self._dessiner_une_colonne(recap.droite, largeur - self._marge - largeur_de_colonne,
                                   largeur_de_colonne, haut_du_bas)
        bas_du_titre = self._dessiner_le_titre(recap, largeur, largeur_de_colonne)
        if image is None:
            self._ecrire_l_absence_d_image(largeur // 2, (bas_du_titre + haut_du_bas) // 2)

    def _ecrire_l_absence_d_image(self, x, y):
        self.widget.create_text(x, y, text=TEXTE_SANS_IMAGE, font=self._police, fill=COULEUR_ETIQUETTE)

    def _dessiner_le_titre(self, recap, largeur, largeur_de_colonne):
        """Nom et sous-titre, centrés en haut entre les deux colonnes. Retourne le bas du titre."""
        place = largeur - 2 * (largeur_de_colonne + 2 * self._marge)
        if place < self._police.measure("0") * 6:
            return self._marge
        canevas = self.widget
        textes = canevas.create_text(
            largeur // 2, self._marge * 2, anchor="n", justify="center", width=place - 2 * self._marge,
            text=recap.titre, font=self._police_du_titre, fill=COULEUR_VALEUR,
        )
        bas = canevas.bbox(textes)[3]
        if recap.sous_titre:
            sous_titre = canevas.create_text(
                largeur // 2, bas, anchor="n", text=recap.sous_titre,
                font=self._police, fill=COULEUR_ETIQUETTE,
            )
            bas = canevas.bbox(sous_titre)[3]
            canevas.addtag_withtag("titre", sous_titre)
        canevas.addtag_withtag("titre", textes)
        gauche, haut, droite, bas = canevas.bbox("titre")
        fond = self._rectangle(gauche - self._marge, haut - self._marge, droite + self._marge, bas + self._marge)
        # Le fond a été créé après les textes : on le glisse dessous.
        canevas.tag_lower(fond, "titre")
        return bas + self._marge

    def _dessiner_une_colonne(self, cadres, x, largeur, y_max):
        y = self._marge
        for cadre in cadres:
            hauteur = self._ligne + self._marge + (self._marge if cadre.jauge is not None else 0)
            # Un cadre qui déborderait sur le bas du panneau n'est pas dessiné.
            if y + hauteur > y_max - self._marge:
                return
            self._dessiner_un_cadre(cadre, x, y, largeur, hauteur)
            y += hauteur + self._marge // 2

    def _dessiner_un_cadre(self, cadre, x, y, largeur, hauteur):
        canevas = self.widget
        interieur = self._marge
        self._rectangle(x, y, x + largeur, y + hauteur)
        y_du_texte = y + self._marge // 2
        canevas.create_text(x + interieur, y_du_texte, anchor="nw", text=cadre.etiquette,
                            font=self._police, fill=COULEUR_ETIQUETTE)
        canevas.create_text(x + largeur - interieur, y_du_texte, anchor="ne", text=cadre.valeur,
                            font=self._police_grasse, fill=COULEUR_VALEUR)
        if cadre.jauge is not None:
            haut = y + hauteur - self._marge
            bas = y + hauteur - self._marge // 2
            gauche, droite = x + interieur, x + largeur - interieur
            canevas.create_rectangle(gauche, haut, droite, bas, fill=COULEUR_JAUGE_VIDE, width=0)
            if cadre.jauge > 0:
                canevas.create_rectangle(gauche, haut, gauche + (droite - gauche) * cadre.jauge, bas,
                                         fill=cadre.couleur, width=0)

    def _dessiner_le_bas(self, blocs, largeur, hauteur):
        """Dessine les blocs du bas, collés au bord inférieur. Retourne le haut de la zone occupée."""
        largeur_du_texte = largeur - 4 * self._marge
        lignes_des_blocs = [
            self._composer_les_lignes(bloc, largeur_du_texte) for bloc in blocs if bloc.elements
        ]
        ecart = self._marge // 2
        hauteur_totale = sum(len(lignes) * self._ligne + self._marge + ecart for lignes in lignes_des_blocs)
        y = hauteur - self._marge - hauteur_totale + ecart
        haut_de_la_zone = y
        for lignes in lignes_des_blocs:
            hauteur_du_bloc = len(lignes) * self._ligne + self._marge
            self._rectangle(self._marge, y, largeur - self._marge, y + hauteur_du_bloc)
            self.widget.create_text(2 * self._marge, y + self._marge // 2, anchor="nw",
                                    text="\n".join(lignes), font=self._police, fill=COULEUR_VALEUR)
            y += hauteur_du_bloc + ecart
        return haut_de_la_zone

    def _composer_les_lignes(self, bloc, largeur):
        """Répartit « Titre : a · b · c » sur LIGNES_MAX_PAR_BLOC lignes au plus.

        Ce qui ne rentre pas est remplacé par « +N » : le récap reste court,
        la fiche complète se consulte toujours depuis la console.
        """
        mesurer = self._police.measure
        lignes = []
        ligne = f"{bloc.titre} : "
        ligne_vide = True
        for rang, element in enumerate(bloc.elements):
            candidate = ligne + ("" if ligne_vide else SEPARATEUR) + element
            if mesurer(candidate) <= largeur or ligne_vide:
                ligne, ligne_vide = candidate, False
                continue
            if len(lignes) + 1 == LIGNES_MAX_PAR_BLOC:
                return lignes + [self._terminer_par_le_reste(ligne, len(bloc.elements) - rang, largeur)]
            lignes.append(ligne)
            ligne, ligne_vide = "  " + element, False
        return lignes + [ligne]

    def _terminer_par_le_reste(self, ligne, nombre_restant, largeur):
        suffixe = f"{SEPARATEUR}+{nombre_restant}"
        morceaux = ligne.split(SEPARATEUR)
        # Tant que « ligne + suffixe » dépasse, on retire le dernier élément
        # de la ligne et on le compte dans le reste.
        while len(morceaux) > 1 and self._police.measure(SEPARATEUR.join(morceaux) + suffixe) > largeur:
            morceaux.pop()
            nombre_restant += 1
            suffixe = f"{SEPARATEUR}+{nombre_restant}"
        return SEPARATEUR.join(morceaux) + suffixe

    def _rectangle(self, gauche, haut, droite, bas):
        return self.widget.create_rectangle(gauche, haut, droite, bas,
                                            fill=COULEUR_DU_CADRE, outline=COULEUR_DU_BORD)

    # ------------------------------------------------------------------- image

    def _image_couvrante(self, chemin, largeur, hauteur):
        """Retourne l'image agrandie ou réduite pour couvrir tout le panneau, ou None.

        Une image absente ou illisible donne None : le panneau affiche alors
        le texte « -- No Data Found -- », sans faire planter le jeu.
        """
        if not chemin:
            return None
        cle = (chemin, largeur, hauteur)
        if self._image_ajustee is not None and self._image_ajustee[0] == cle:
            return self._image_ajustee[1]
        source = self._charger(chemin)
        if source is None:
            return None
        # ATTENTION : tkinter n'affiche une image que tant qu'un objet Python
        # la référence. La garder dans `self` l'empêche d'être libérée.
        self._image_ajustee = (cle, self._ajuster(source, largeur, hauteur))
        return self._image_ajustee[1]

    def _charger(self, chemin):
        if self._image_source is not None and self._image_source[0] == chemin:
            return self._image_source[1]
        try:
            image = tk.PhotoImage(master=self.widget, file=chemin)
        except tk.TclError:
            image = None
        self._image_source = (chemin, image)
        return image

    def _ajuster(self, source, largeur, hauteur):
        """Fabrique une image qui couvre largeur x hauteur, centrée, sans la déformer.

        CONCEPT : sans bibliothèque d'images, tkinter ne sait qu'agrandir une
        image par un entier (`zoom`) et la réduire par un entier (`subsample`).
        Combiner les deux donne un rapport `numerateur / denominateur` : pour
        agrandir de 1,5 fois, on agrandit 3 fois et on réduit 2 fois. On
        choisit la plus petite fraction qui couvre le panneau, puis on ne
        copie que la partie centrale de l'image, celle qui sera visible.
        """
        largeur_source, hauteur_source = source.width(), source.height()
        rapport_voulu = max(largeur / largeur_source, hauteur / hauteur_source)
        numerateur, denominateur = _plus_petite_fraction_au_dessus(rapport_voulu)
        largeur_utile = min(largeur_source, -(-largeur * denominateur // numerateur))
        hauteur_utile = min(hauteur_source, -(-hauteur * denominateur // numerateur))
        gauche = (largeur_source - largeur_utile) // 2
        haut = (hauteur_source - hauteur_utile) // 2
        ajustee = tk.PhotoImage(master=self.widget)
        ajustee.tk.call(
            ajustee, "copy", source,
            "-from", gauche, haut, gauche + largeur_utile, haut + hauteur_utile,
            "-zoom", numerateur, numerateur,
            "-subsample", denominateur, denominateur,
        )
        return ajustee


def _plus_petite_fraction_au_dessus(rapport):
    """Retourne (numérateur, dénominateur) de la plus petite fraction >= rapport."""
    meilleure = None
    for denominateur in range(1, DENOMINATEUR_MAX_DU_ZOOM + 1):
        numerateur = max(1, -int(-rapport * denominateur // 1))
        if meilleure is None or numerateur * meilleure[1] < meilleure[0] * denominateur:
            meilleure = (numerateur, denominateur)
    return meilleure
