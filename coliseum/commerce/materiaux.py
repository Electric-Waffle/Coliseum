"""Matériaux : fusion et comptage."""

from pygame import mixer
import random
import time

from coliseum import services
from coliseum.audio import PlaySFX
from coliseum.donnees.village import DICTIONNAIREMATERIAUFUSION


def AugmenteMateriauDansDictionnaire(retour = False):
    liste_de_materiau_dedoublable = []
    for materiau in services.Player.liste_de_materiaux :
        if services.Player.liste_de_materiaux[materiau] >= 1:
            liste_de_materiau_dedoublable.append(materiau)
    
    if len(liste_de_materiau_dedoublable) >= 1 :
        materiau_choisi = liste_de_materiau_dedoublable[random.randint(0, (len(liste_de_materiau_dedoublable) - 1))]
        services.Player.liste_de_materiaux[materiau_choisi] += round(services.Player.liste_de_materiaux[materiau_choisi] *(0.33 * random.randint(1, 6)))

    if retour :
        return materiau_choisi


def FuseMaterials(materiau_a, materiau_b):
    mixer.music.set_volume(0.1)
    print("Des bruits d'engrenages en mouvements et de vapeur sous pression se font entendre.")
    print("Puis, tout s'arrete, la porte de la deuxieme cabine s'ouvre, et...")
    services.Sove.ModifieDechetsDansSove("Enleve", materiau_a, 1)
    services.Sove.ModifieDechetsDansSove("Enleve", materiau_b, 1)
    for materiau in DICTIONNAIREMATERIAUFUSION:
        recette_fusion = DICTIONNAIREMATERIAUFUSION[materiau]
        if materiau_a in recette_fusion and materiau_b in recette_fusion:
            services.Sove.ModifieDechetsDansSove("Ajout", materiau, 1)
            PlaySFX("fusion_y")
            time.sleep(5)
            print(f"...il y a quelque chose à l'interieur !")
            services.Affichage.EntreePourContinuer()
            print(f"Vous obtenez [{materiau}] !")
            services.Affichage.EntreePourContinuer()
            mixer.music.set_volume(1)
            return None
    PlaySFX("fusion_n")
    time.sleep(5)
    print(f"...il n'y a rien d'utilisable a l'interieur.")
    services.Affichage.EntreePourContinuer()
    mixer.music.set_volume(1)
