import threading
import time
import os


# Fonction pour le chronomètre
def chronometre():
    temps = 0
    while not stop_event.is_set():
        print("Appuyez sur Entrée pour arrêter le chronomètre..."
              f"\nTemps écoulé: {temps} secondes", end="\r")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')  # Effacer la ligne du chronomètre
        temps += 1


# Créer un thread pour le chronomètre
stop_event = threading.Event()
chronometre_thread = threading.Thread(target=chronometre)
chronometre_thread.start()
input("")
stop_event.set()  # Arrêter le chronomètre
chronometre_thread.join()  # Attendre que le thread se termine

