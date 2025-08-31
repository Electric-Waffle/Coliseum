import subprocess
import os
import time


# C'EST ICI LE MODE DEBUG !
mode_debug = 1
# C'EST ICI LE MODE DEBUG !



chemin_vers_le_main_py = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ColiseumDependencies", "main.py")
subprocess.call(["python", chemin_vers_le_main_py])
if mode_debug == 1 :
    input("\n\nUne terrible erreur est survenue... Le jeu va se fermer...\nMais pour etre sûr de comprendre ce qui s'est passé... Voici un barrage.\nAppuyez sur entree pour continuer :")
    input("\nEt encore :")
    input("\nEt encore :")
    input("\nEt encore :")
    print("Cette fois ci, faut juste attendre 10 secondes. Comme ca si vous avez spam la touche entree, vous pouvez quand meme voir l'erreur !")
    time.sleep(10)
    input("\nLa prochaine fois, si vous voulez juste que l'écran crashe, vous pouvez modifier le mode debug dans le code Coliseum.py.\nVous faitez en sorte que la variable soit égale à 0, et bam !")