import os
from dotenv import load_dotenv

# Charge la clé OPENAI_API_KEY depuis .env
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain


def build_pipeline(model_name: str = "gpt-4.1-mini") -> SequentialChain:
    """
    Construit un pipeline séquentiel (Agile) :
      1) Refinement de la user story
      2) Critères d'acceptation (Gherkin)
      3) Cas de test (unitaires + d'intégration)
      4) Plan de tâches (tickets)
      5) Message de commit (concis)
    """
    llm = ChatOpenAI(model=model_name)

    # ---------- Étape 1 : Refinement user story ----------
    prompt_refine = PromptTemplate.from_template(
        "Tu es Product Owner. Affine la user story ci-dessous en suivant le format INVEST.\n"
        "Conserve le périmètre métier et clarifie les ambiguïtés si nécessaire.\n\n"
        "User story (brute) :\n{feature}\n\n"
        "Rends :\n- Contexte\n- Persona\n- Besoin\n- Valeur\n- Contraintes/Non-Objectifs\n- Hypothèses\n- Risques\n"
    )
    chain_refine = LLMChain(
        llm=llm,
        prompt=prompt_refine,
        output_key="refined_story",
        verbose=True,
    )

    # ---------- Étape 2 : Critères d'acceptation ----------
    prompt_ac = PromptTemplate.from_template(
        "À partir de la user story affinée ci-dessous, rédige des critères d’acceptation en Gherkin (FR), "
        "couvrant les cas nominaux et quelques cas limites.\n\n"
        "User story affinée :\n{refined_story}\n\n"
        "Rends :\n- Critères Gherkin (Given/When/Then) numérotés\n"
    )
    chain_ac = LLMChain(
        llm=llm,
        prompt=prompt_ac,
        output_key="acceptance_criteria",
        verbose=True,
    )

    # ---------- Étape 3 : Cas de test ----------
    prompt_tests = PromptTemplate.from_template(
        "Tu es QA lead. En te basant sur ces critères Gherkin, fournis des cas de test :\n"
        "- Tests unitaires (structure : Nom, Objectif, Préconditions, Étapes, Résultat attendu)\n"
        "- Tests d’intégration (même structure)\n\n"
        "Critères Gherkin :\n{acceptance_criteria}\n\n"
        "Rends une liste claire et actionnable."
    )
    chain_tests = LLMChain(
        llm=llm,
        prompt=prompt_tests,
        output_key="test_cases",
        verbose=True,
    )

    # ---------- Étape 4 : Plan de tâches ----------
    prompt_tasks = PromptTemplate.from_template(
        "Tu es Tech Lead. Propose un plan de tâches (tickets) pour livrer la user story :\n"
        "- Découpage logique (backend, frontend, infra, QA, docs)\n"
        "- Pour chaque ticket : Titre, Description, Definition of Done, Estimation (idéal jours/hommes), Dépendances\n\n"
        "Contexte (user story affinée) :\n{refined_story}\n\n"
        "Critères Gherkin :\n{acceptance_criteria}\n\n"
        "Inclure aussi : risques techniques et points d’attention."
    )
    chain_tasks = LLMChain(
        llm=llm,
        prompt=prompt_tasks,
        output_key="tasks_plan",
        verbose=True,
    )

    # ---------- Étape 5 : Message de commit ----------
    prompt_commit = PromptTemplate.from_template(
        "Rédige un message de commit concis (type Conventional Commits) résumant la livraison initiale de la user story.\n"
        "Inclure les points clés et, si utile, une référence à un ticket (ex: JIRA-123).\n\n"
        "User story affinée :\n{refined_story}\n\n"
        "Plan de tâches :\n{tasks_plan}\n\n"
        "Rends un message sur 1-2 lignes maximum."
    )
    chain_commit = LLMChain(
        llm=llm,
        prompt=prompt_commit,
        output_key="commit_message",
        verbose=True,
    )

    # ---------- Chaîne séquentielle ----------
    pipeline = SequentialChain(
        chains=[chain_refine, chain_ac, chain_tests, chain_tasks, chain_commit],
        input_variables=["feature"],  # entrée initiale
        output_variables=["refined_story", "acceptance_criteria", "test_cases", "tasks_plan", "commit_message"],
        verbose=True,
    )
    return pipeline


def main():
    print("🔁 Pipeline Agile (refinement → Gherkin → tests → tâches → commit)\n")
    feature = input("Décris ta user story brute (ex: 'En tant qu’utilisateur, je veux ...') :\n> ").strip()
    if not feature:
        print("Aucune user story fournie. Fin.")
        return

    pipeline = build_pipeline()
    results = pipeline({"feature": feature})

    print("\n================= SORTIES =================")
    print("\n--- User story affinée ---\n")
    print(results["refined_story"])

    print("\n--- Critères d’acceptation (Gherkin) ---\n")
    print(results["acceptance_criteria"])

    print("\n--- Cas de test (Unitaires + Intégration) ---\n")
    print(results["test_cases"])

    print("\n--- Plan de tâches (tickets) ---\n")
    print(results["tasks_plan"])

    print("\n--- Message de commit ---\n")
    print(results["commit_message"])
    print("===========================================")


if __name__ == "__main__":
    main()