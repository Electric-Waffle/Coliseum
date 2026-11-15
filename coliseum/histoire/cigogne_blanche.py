"""Écriture du livre de la Cigogne Blanche."""

from coliseum import services
from coliseum.chemins import DOSSIER_RACINE
from coliseum.donnees.bibliotheque import DICTIONNAIREDESCRIPTIONCIGOGNEBLANCHE


def DecodeurPourLesAccents(chaine):
    chaine = chaine.replace('é',"e")
    chaine = chaine.replace('é',"e")
    chaine = chaine.replace('ê',"e")
    chaine = chaine.replace('ê',"e")
    chaine = chaine.replace('à',"a")
    chaine = chaine.replace('â',"a")
    chaine = chaine.replace('ï',"i")
    return chaine


def EcrireDansLivreCigogneBlanche():
    dir_path = DOSSIER_RACINE
    chemin_du_fichier = dir_path + "\Livre_De_La_Cigogne_Blanche.txt"
    with open(chemin_du_fichier, "w") as fichier:
        fichier.write(f"                           -=Livre de la Cigogne Blanche=-\n\n*Le dernier espoir, que la Volontee donne a celles et ceux qui se battent encore,\nse nomme connaissance.*\n")
        fichier.write("\n================================================================================")
        fichier.write("\n================================================================================\n")

        for theme in DICTIONNAIREDESCRIPTIONCIGOGNEBLANCHE:

            liste_de_entree_dans_le_theme = services.Sove.ModifieCigogneBlancheDansSove(theme, "Donne")

            if len(liste_de_entree_dans_le_theme) == 0:
                continue
            else:
                fichier.write(f"\n                                 -={theme}=-\n\n")

                for entree in liste_de_entree_dans_le_theme:
                    description_de_lentree = DICTIONNAIREDESCRIPTIONCIGOGNEBLANCHE[theme][entree]

                    description_de_lentree = DecodeurPourLesAccents(description_de_lentree)
                    entree = DecodeurPourLesAccents(entree)

                    fichier.write(f"\n\n{entree} : {description_de_lentree}\n\n")
                    

            fichier.write("\n--------------------------------------------------------------------------------")
            fichier.write("\n--------------------------------------------------------------------------------\n")
