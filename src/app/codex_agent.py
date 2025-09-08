import os
from dotenv import load_dotenv
from openai import OpenAI

# 🔁 Charge les variables d’environnement depuis le fichier .env
load_dotenv()

# 🔑 Initialise le client OpenAI avec la clé API (stockée dans .env)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 📂 Fonction utilitaire : lister tous les fichiers Python dans un dossier (et ses sous-dossiers)
#def lister_fichiers_python(dossier):
#    """Liste tous les fichiers .py dans un dossier et ses sous-dossiers"""
#    fichiers = []
#    for racine, _, fichiers_locaux in os.walk(dossier):
#        for nom in fichiers_locaux:
#            if nom.endswith(".py"):
#                chemin_absolu = os.path.join(racine, nom)
#                fichiers.append(chemin_absolu)
#    return fichiers

# 📖 Fonction utilitaire : lire le contenu d’un fichier texte (ex : fichier Python)
def lire_fichier(chemin):
    with open(chemin, "r", encoding="utf-8") as f:
        return f.read()

# 💾 Fonction utilitaire : écrire du contenu texte dans un fichier (remplace le contenu existant)
def ecrire_fichier(chemin, contenu):
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)

# 🤖 Fonction principale : utilise GPT-4 pour modifier un fichier selon un prompt
def modifier_code(chemin, prompt):
    # 1. Lire le contenu du fichier à modifier
    code = lire_fichier(chemin)

    # 2. Préparer le message à envoyer au modèle (rôle system + prompt utilisateur)
    messages = [
        {
            "role": "system",
            "content": "Tu es un expert Python qui améliore le code."
        },
        {
            "role": "user",
            "content": f"Voici le code :\n\n{code}\n\nModifie-le selon : {prompt}"
        }
    ]

    # 3. Appel à l’API OpenAI pour générer une version modifiée du fichier
    response = client.chat.completions.create(
        model="gpt-4",         # Utilise le modèle GPT-4
        messages=messages,     # Dialogue à transmettre
        temperature=0.3        # Moins de créativité, plus de rigueur
    )

    # 4. Extraire le code généré depuis la réponse
    nouveau_code = response.choices[0].message.content

    # 5. Écraser le fichier avec le nouveau code généré
    ecrire_fichier(chemin, nouveau_code)

    # 6. Afficher un message de confirmation
    print("✅ Fichier mis à jour.")

# 🧪 Exemple d’utilisation : modifie le fichier main.py en ajoutant des logs
modifier_code("main.py", "Ajoute des logs pour chaque fonction.")
# (Assurez-vous que main.py existe dans le même répertoire que ce script)