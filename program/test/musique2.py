import math
import struct
import wave

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
    'REST': 0  # Silence
}

# Notes de la musique de Zelda avec les durées correspondantes
notes_zelda = [
    ('E4', 0.5),  # Première mesure
    ('G4', 0.5),
    ('A4', 0.5),
    ('REST', 0.5),
    ('A4', 0.5),
    ('G4', 0.5),
    ('E4', 0.5),
    ('REST', 0.5),
    ('E4', 0.5),
    ('G4', 0.5),
    ('A4', 0.5),
    ('REST', 0.5),
    ('A4', 0.5),
    ('G4', 0.5),
    ('E4', 0.5),
    ('REST', 0.5),
    ('E4', 0.5),
    ('G4', 0.5),
    ('A4', 0.5),
    ('REST', 0.5),
    ('A4', 0.5),
    ('G4', 0.5),
    ('E4', 0.5),
    ('REST', 0.5),
    ('E4', 0.5),
    ('G4', 0.5),
    ('A4', 0.5),
    ('REST', 0.5),
    ('A4', 0.5),
    ('G4', 0.5),
    ('E4', 0.5),
    ('REST', 0.5),
]

# Fonction pour générer des échantillons pour une note spécifique
def generer_note(frequence, duree_seconde, amplitude=0.5, frequence_echantillonnage=44100):
    nombre_echantillons = int(duree_seconde * frequence_echantillonnage)
    echantillons = []
    for i in range(nombre_echantillons):
        valeur = amplitude * math.sin(2 * math.pi * frequence * i / frequence_echantillonnage)
        echantillons.append(valeur)
    return echantillons

# Fonction pour générer la mélodie complète
def generer_melodie(notes, temps_note, frequence_echantillonnage=44100):
    melodie = []
    for note, duree in notes:
        if note == 'REST':
            echantillons_note = [0] * int(temps_note * frequence_echantillonnage)
        else:
            frequence = NOTES[note]
            echantillons_note = generer_note(frequence, temps_note, frequence_echantillonnage=frequence_echantillonnage)
        melodie.extend(echantillons_note)
    return melodie

# Générer la mélodie complète de Zelda
melodie = generer_melodie(notes_zelda, temps_note=0.5)

# Écriture dans un fichier WAV
nom_fichier = "zelda.wav"
with wave.open(nom_fichier, 'wb') as fichier_wav:
    fichier_wav.setnchannels(1)  # Mono
    fichier_wav.setsampwidth(2)  # 16-bit
    fichier_wav.setframerate(44100)  # Fréquence d'échantillonnage
    fichier_wav.writeframes(b''.join(struct.pack('<h', int(sample * 32767)) for sample in melodie))

print(f"Fichier WAV '{nom_fichier}' créé avec succès.")
