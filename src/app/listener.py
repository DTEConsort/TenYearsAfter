# src/app/listener.py

# src/app/listener.py

# 🎙️ Bibliothèques pour la capture audio
import sounddevice as sd                    # Permet d'accéder au micro (et haut-parleurs)
import scipy.io.wavfile                     # Pour écrire des fichiers audio WAV
import io                                   # Pour créer un fichier en mémoire (buffer)

# 🔐 Pour utiliser l’API OpenAI
from openai import OpenAI                   # Client OpenAI
from dotenv import load_dotenv              # Pour lire les variables dans le fichier .env
import os                                   # Pour accéder aux variables d’environnement

# 📥 On charge les variables du fichier .env (clé API, etc.)
load_dotenv()

def enregistrer_audio_en_memoire(duree, frequence=44100, index_micro=2):
    """
    🎙️ Enregistre l’audio depuis un micro pendant `duree` secondes.
    👉 Le son est stocké dans un fichier temporaire en mémoire (sans l’enregistrer sur disque).
    """

    print(f"🎙️ Enregistrement pendant {duree} secondes...")

    # ⏺️ Capture le son depuis le micro choisi
    audio = sd.rec(
        int(duree * frequence),     # Nombre d’échantillons = durée * fréquence d’échantillonnage
        samplerate=frequence,       # Qualité audio (44100 Hz = qualité CD)
        channels=2,                 # En stéréo (2 canaux)
        dtype='int16',              # Format audio
        device=index_micro          # Numéro du micro à utiliser (à adapter selon ton setup)
    )

    # 🕐 Attendre la fin de l’enregistrement
    sd.wait()

    # 💾 On crée un "faux fichier" audio en mémoire
    buffer_audio = io.BytesIO()
    scipy.io.wavfile.write(buffer_audio, frequence, audio)
    buffer_audio.seek(0)  # Revenir au début du buffer

    return buffer_audio

def transcrire_audio_depuis_buffer(audio_buffer):
    """
    🤖 Envoie le fichier audio (en mémoire) à l’API OpenAI (modèle Whisper) pour transcription.
    📤 Retourne le texte transcrit à partir de ta voix.
    """

    print("📤 Envoi à OpenAI pour transcription...")

    # 🔑 Initialiser le client OpenAI (la clé est chargée depuis .env)
    client = OpenAI()

    # 📡 Envoi du buffer audio à l'API de transcription (Whisper)
    response = client.audio.transcriptions.create(
        model="whisper-1",                                      # Modèle utilisé
        file=("audio.wav", audio_buffer, "audio/wav")           # Fichier audio simulé
    )

    return response.text  # 📝 Texte obtenu

def run():
    """
    ⚙️ Fonction principale du script :
    1. Enregistre ta voix pendant quelques secondes
    2. Transcrit automatiquement ce que tu as dit
    3. Affiche le texte en console
    """

    # 🎙️ Enregistre la voix pendant 10 secondes
    buffer_audio = enregistrer_audio_en_memoire(duree=10, index_micro=2)

    # 🧠 Transcrit ce qui a été dit
    texte = transcrire_audio_depuis_buffer(buffer_audio)

    # 🖨️ Affiche la transcription dans la console
    print("\n📝 Transcription obtenue :")
    print(texte)

if __name__ == "__main__":
    run()