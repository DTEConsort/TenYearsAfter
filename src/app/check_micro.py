import sounddevice as sd

print("🔍 Liste des périphériques audio détectés :\n")
for i, device in enumerate(sd.query_devices()):
    print(f"{i}: {device['name']} - {device['max_input_channels']} canaux d'entrée")