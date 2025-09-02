import subprocess
import os
import time


# C'EST ICI LE MODE DEBUG !
mode_debug = 1
# C'EST ICI LE MODE DEBUG !



chemin_vers_le_main_py = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ColiseumDependencies", "main.py")
subprocess.call(["python", chemin_vers_le_main_py])
if mode_debug == 1 :
    input("\n\nLe jeu va se fermer...\nLe vouliez vous ainsi ?\nPour évoter les problemes fantomes, ce message apparait quand le programme plante ou quand l'utilisateur décide d'arreter de jouer.\nAppuyez sur entree pour continuer :")
    input("\nAinsi donc, si vous vouliez quitter, vour pouvez juste cliquer sur la croix rouge.\nApuuyez sur entree pour continuer :")
    input("\nMais si le jeu s'est arrété a cause d'un bug... vous feriez mieux de prendre connaissance du message d'erreur ci dessus.\nAppuyez sur entree pour continuer : ")
    input("\nCe barrage de demande est fait pour éviter les joueurs qui spamment la touche entree et ne voyent pas le message d'erreur.\nAppuyez sur entree pour continuer : ")
    print("Cette fois ci, faut juste attendre 10 secondes. Comme ca si vous avez spam la touche entree, vous pouvez quand meme voir l'erreur !")
    time.sleep(10)
    input("\nLa prochaine fois, si vous ne voulez pas voir ces messages, vous pouvez modifier le mode debug dans le code Coliseum.py.\nVous faitez en sorte que la variable soit égale à 0, et bam !\nAppuyez sur entree pour fermer la fenetre : ")