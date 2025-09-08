# Projet TenYearsAfter

Atelier d’apprentissage Python + LangChain + agents.

## Structure du dépôt

- `src/app` — scripts et exemples d'agents.
- `data` — jeux de données d'exemple.
- `docs` — documents et notes associés.

## Utilisation

Pour vérifier l'environnement, exécutez :

```bash
python src/app/main.py
```

La plupart des scripts nécessitent une clé OpenAI stockée dans un fichier `.env` via la variable `OPENAI_API_KEY`.

## Scripts principaux (`src/app`)

- `main.py` – exemple minimal affichant un message et montrant comment configurer le module `logging`.
- `llm_ping.py` – envoie une requête simple à l’API OpenAI pour vérifier la clé.
- `llm_simple_call.py` – pose une question au modèle via l’API Responses.
- `langchain_basic.py` – premier appel à un modèle OpenAI en passant par LangChain.
- `app_memory.py` – conversation interactive avec mémoire tampon.
- `app_summary_memory.py` – même principe mais avec mémoire résumée.
- `agent_calculator.py` – agent LangChain capable de multiplier deux nombres.
- `agent_calculator2.py` – version interactive combinant multiplication et conversion de températures.
- `agent_multi_tools.py` – agent multi-outils (calcul et conversion) dans une boucle de dialogue.
- `agent_faq.py` – assistant FAQ chargé depuis `data/faq.txt` avec index FAISS.
- `rag_simple.py` – recherche augmentée sur les documents du dossier `docs`.
- `pipeline_agile.py` – pipeline complet : user story → critères Gherkin → tests → tâches → message de commit.
- `pipeline_agile_lean.py` – variante allégée du pipeline (refinement, critères, plan de tâches, commit bonus).
- `codex_agent.py` – modifie un fichier Python selon un prompt grâce à l’API OpenAI.
- `listener.py` – enregistre un court extrait audio et le transcrit avec Whisper.
- `check_micro.py` – liste les périphériques audio disponibles.
- `tools/tools_calculator.py` – outil `multiply` exposé pour les agents LangChain.
- `tools/tools_temperature.py` – convertit des degrés Celsius en Fahrenheit.
