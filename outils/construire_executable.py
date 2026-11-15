"""Fabrique la version distribuable du jeu : un dossier contenant Coliseum.exe.

    python outils/construire_executable.py

Prérequis, sur la machine qui construit seulement : `pip install pyinstaller`.
Le joueur, lui, n'a rien à installer : ni Python, ni pygame.

Résultat :

    dist/Coliseum/
        Coliseum.exe              double-clic pour jouer
        ColiseumDependencies/     musiques, bruitages, images, sauvegardes
        (fichiers de PyInstaller : Python et pygame embarqués)

Pour distribuer le jeu, on zippe le dossier `dist/Coliseum` entier.

POURQUOI un dossier et pas un seul fichier .exe (`--onefile`) :
1. un .exe unique se décompresse dans un dossier temporaire à chaque
   lancement ; avec plus de 700 Mo de musiques, le démarrage serait très long ;
2. ce dossier temporaire est effacé à la fermeture : les sauvegardes écrites
   dedans seraient perdues. Ici les sauvegardes vivent à côté de l'exe, dans
   ColiseumDependencies, et le jeu les retrouve grâce à coliseum/chemins.py.

POURQUOI `--windowed` : le jeu a sa propre fenêtre (coliseum/terminal/fenetre.py).
Sans cette option, Windows ouvrirait en plus une console noire vide.
"""

import os
import shutil
import subprocess
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
NOM = "Coliseum"
DOSSIER_DE_SORTIE = os.path.join(RACINE, "dist")
DOSSIER_DE_TRAVAIL = os.path.join(RACINE, "build")
RESSOURCES = "ColiseumDependencies"

# Présents dans le dossier de ressources mais inutiles au joueur.
A_NE_PAS_COPIER = ("__pycache__", "pygame_bonne_version", "*.py", "*.pyc")
# Les sauvegardes livrées doivent être vierges, pas celles du développeur.
SAUVEGARDES = ("save.txt", "s0ve.txt")


def construire_l_executable():
    commande = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm", "--clean",
        "--onedir", "--windowed",
        "--name", NOM,
        "--distpath", DOSSIER_DE_SORTIE,
        "--workpath", DOSSIER_DE_TRAVAIL,
        "--specpath", DOSSIER_DE_TRAVAIL,
        os.path.join(RACINE, "Coliseum.py"),
    ]
    subprocess.check_call(commande, cwd=RACINE)


def copier_les_ressources():
    destination = os.path.join(DOSSIER_DE_SORTIE, NOM, RESSOURCES)
    if os.path.isdir(destination):
        shutil.rmtree(destination)
    shutil.copytree(
        os.path.join(RACINE, RESSOURCES), destination,
        ignore=shutil.ignore_patterns(*(A_NE_PAS_COPIER + SAUVEGARDES)),
    )
    for nom in SAUVEGARDES:
        _ecrire_la_sauvegarde_vierge(nom, os.path.join(destination, nom))


def _ecrire_la_sauvegarde_vierge(nom, destination):
    """Écrit la version du dépôt git, c'est à dire une sauvegarde de départ.

    `git show HEAD:chemin` lit un fichier tel qu'il est dans le dernier commit,
    sans toucher au fichier de travail : la partie du développeur reste intacte.
    """
    resultat = subprocess.run(
        ["git", "show", f"HEAD:{RESSOURCES}/{nom}"],
        cwd=RACINE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if resultat.returncode != 0:
        raise SystemExit(f"Impossible de lire {nom} dans le dépôt git : {resultat.stderr.decode(errors='replace')}")
    with open(destination, "wb") as fichier:
        fichier.write(resultat.stdout)


if __name__ == "__main__":
    construire_l_executable()
    copier_les_ressources()
    print(f"\nJeu prêt à distribuer : {os.path.join(DOSSIER_DE_SORTIE, NOM)}")
