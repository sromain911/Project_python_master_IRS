import numpy as np
import sounddevice as sd
import time

# Définition des constantes pour les notes de la gamme (fréquences en Hz)
NOTES = {
    'C4': 261.63,
    'D4': 293.66,
    'E4': 329.63,
    'F4': 349.23,
    'G4': 392.00,
    'A4': 440.00,
    'B4': 493.88,
    'C5': 523.25,
}

# Notes pour une mélodie simple de boîte à musique
melodie = [
    'E4', 'D4', 'C4', 'D4', 'E4', 'E4', 'E4',  # Exemple de mélodie
    'D4', 'D4', 'D4', 'E4', 'G4', 'G4',  # Exemple de mélodie
    'E4', 'D4', 'C4', 'D4', 'E4', 'E4', 'E4', 'D4', 'D4', 'E4', 'D4', 'C4'
]

# Durée de chaque note en secondes
duree_note = 0.5
temps_pause = 0.1  # Temps de pause entre les notes

# Fonction pour générer un échantillon audio pour une note donnée
def generer_echantillon(note, duree, frequence_echantillonnage=44100):
    t = np.linspace(0, duree, int(duree * frequence_echantillonnage), endpoint=False)
    frequence = NOTES.get(note, 0)
    if frequence == 0:
        return np.zeros_like(t)
    else:
        return 0.5 * np.sin(2 * np.pi * frequence * t)

# Fonction pour jouer une note
def jouer_note(note):
    echantillon = generer_echantillon(note, duree_note)
    sd.play(echantillon, samplerate=44100)
    time.sleep(duree_note + temps_pause)

# Jouer la mélodie complète
for note in melodie:
    jouer_note(note)

# Attente que la mélodie se termine
time.sleep(1)

# Arrêt de la lecture audio
sd.stop()
