"""Musiques et bruitages hors combat.

Deux canaux pygame suffisent : un pour la musique de fond, un pour les effets
sonores. Lancer un nouveau son sur un canal coupe celui qui y jouait.

ATTENTION : `CHANNELMUSIQUEDEBASE` et `CHANNELSFX` sont remplacés à chaque
nouveau son. Depuis un autre module, il faut donc toujours passer par
`audio.CHANNELMUSIQUEDEBASE` (lu au moment de l'appel) et jamais par
`from coliseum.audio import CHANNELMUSIQUEDEBASE`, qui garderait l'ancien canal.
"""

import os
import time

from pygame import mixer

from coliseum import services
from coliseum.chemins import DOSSIER_RESSOURCES

CHANNELMUSIQUEDEBASE = None
CHANNELSFX = None


def initialiser():
    """Ouvre la sortie audio et réserve les deux canaux avec un son muet.

    Appelée une fois au lancement : réserver les canaux tout de suite permet aux
    autres fonctions de les couper sans vérifier s'ils existent.
    """
    global CHANNELMUSIQUEDEBASE, CHANNELSFX
    mixer.init()
    mixer.set_num_channels(16)
    son_muet = mixer.Sound(os.path.join(DOSSIER_RESSOURCES, "nothing.mp3"))
    CHANNELMUSIQUEDEBASE = son_muet.play()
    CHANNELSFX = son_muet.play()


def couper_la_musique_de_fond():
    # Volume à zéro avant l'arrêt : couper net un son en cours fait un « clac ».
    CHANNELMUSIQUEDEBASE.set_volume(0)
    time.sleep(0.01)
    CHANNELMUSIQUEDEBASE.stop()


def PlaySound(musique):
    PlayMusic(musique, "sound")


def PlayMusic(musique, type_of_music="music"):
    global CHANNELMUSIQUEDEBASE
    dir_path = services.Player.chemin_musique
    musique = dir_path + f"\\{musique}.mp3"
    CHANNELMUSIQUEDEBASE.set_volume(0)
    time.sleep(0.01)
    CHANNELMUSIQUEDEBASE.stop()
    lancement_de_musique = mixer.Sound(musique)
    if type_of_music == "music":
        CHANNELMUSIQUEDEBASE = lancement_de_musique.play(loops=-1)
    else:
        CHANNELMUSIQUEDEBASE = lancement_de_musique.play()


def PlaySFX(musique, type_of_sfx="noloop"):
    global CHANNELSFX
    dir_path = services.Player.chemin_musique
    musique = dir_path + f"\\{musique}.mp3"
    CHANNELSFX.set_volume(0)
    time.sleep(0.01)
    CHANNELSFX.stop()
    lancement_de_musique = mixer.Sound(musique)
    if type_of_sfx == "noloop":
        CHANNELSFX = lancement_de_musique.play()
    else:
        CHANNELSFX = lancement_de_musique.play(loops=-1)


def PermanentPlaySFX(musique):
    PlaySFX(musique,"loop")


def PlayWavSound(musique):
    dir_path = services.Player.chemin_musique
    musique = dir_path + f"\\sfx\\{musique}.wav"
    mixer.music.load(musique)
    mixer.music.play()


def StopAllMusic():
    global CHANNELMUSIQUEDEBASE
    global CHANNELSFX

    CHANNELMUSIQUEDEBASE.set_volume(0)
    time.sleep(0.01)
    CHANNELMUSIQUEDEBASE.stop()
    CHANNELSFX.set_volume(0)
    time.sleep(0.01)
    CHANNELSFX.stop()


def PlayMusicDeLetage():
    nom_de_la_musique = str(services.Player.numero_de_letage)
    if services.Player.nom_de_letage in ["Jungle Cruelle", "Limbes Flétrissants", "Douves du Pénitent", "Le Lumisade"]:
        nom_de_la_musique += "_alt"
    if services.Player.numero_de_letage == -1 and services.Sove.ModifieTagsDansSove("Checke", "Village Nuit"):
        nom_de_la_musique += "_alt"
    if services.Player.nom_de_letage == "Dédale Frontière" or services.Player.mode_jukebox :
        PlayMusic(services.Player.musique_etage_10)
    else:
        PlayMusic(f"etage_{nom_de_la_musique}")
