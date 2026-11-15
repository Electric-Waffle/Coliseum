"""Terminal « console du système » : le comportement d'origine du jeu.

Sert pour jouer dans un vrai terminal (`python Coliseum.py --console`) et pour
les tests automatiques, qui lisent ce que le jeu écrit sur la sortie standard.
`print` et `input` ne sont pas redéfinis ici : ils utilisent déjà la console.
"""

import os
import time


class TerminalSysteme:

    def effacer(self):
        os.system("cls" if os.name == "nt" else "clear")

    def attendre(self, secondes):
        time.sleep(secondes)

    def montrer_image(self, chemin_vers_limage):
        # Import tardif : tkinter n'est chargé que si une image est vraiment montrée.
        import tkinter as tk

        fenetre = tk.Tk()
        image = tk.PhotoImage(file=chemin_vers_limage)
        canevas = tk.Canvas(fenetre, width=image.width(), height=image.height())
        canevas.pack()
        canevas.create_image(0, 0, anchor=tk.NW, image=image)
        fenetre.mainloop()

    def fermer(self):
        pass
