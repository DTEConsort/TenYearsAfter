import os
from dotenv import load_dotenv

# Charge OPENAI_API_KEY depuis .env
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain


def build_pipeline(model_name: str = "gpt-4.1-mini") -> SequentialChain:
    """
    Pipeline Lean (3 étapes) :
      1) Refinement rapide (INVEST synthétique)
      2) Critères d'acceptation (Gherkin)
      3) Plan de tâches concis (tickets actionnables)
    """
    llm = ChatOpenAI(model=model_name)

    # 1) Refinement rapide
    prompt_refine = PromptTemplate.from_template(
        "Agis en Product Owner. Affine la user story de façon synthétique (format INVEST) :\n"
        "- Contexte (2 phrases max)\n- Persona\n- Besoin\n- Valeur\n- Contraintes clés\n"
        "User story :\n{feature}\n"
    )
    chain_refine = LLMChain(
        llm=llm,
        prompt=prompt_refine,
        output_key="refined_story",
        verbose=True,
    )

    # 2) Critères d'acceptation (Gherkin)
    prompt_ac = PromptTemplate.from_template(
        "À partir de la user story affinée ci-dessous, rédige 4 à 7 critères d’acceptation en Gherkin (FR), "
        "couvrant cas nominal + 1-2 cas limites.\n\n"
        "User story affinée :\n{refined_story}\n"
    )
    chain_ac = LLMChain(
        llm=llm,
        prompt=prompt_ac,
        output_key="acceptance_criteria",
        verbose=True,
    )

    # 3) Plan de tâches concis
    prompt_tasks = PromptTemplate.from_template(
        "Tu es Tech Lead. Propose un plan de tâches concis pour livrer la user story :\n"
        "- Regroupe par domaines : backend, frontend, QA, docs/outillage\n"
        "- Pour chaque ticket : Titre, Brève description, Definition of Done (1-3 bullets), Estimation (JH)\n"
        "- Mentionne dépendances majeures si utile\n\n"
        "Contexte (user story affinée) :\n{refined_story}\n\n"
        "Critères Gherkin :\n{acceptance_criteria}\n"
    )
    chain_tasks = LLMChain(
        llm=llm,
        prompt=prompt_tasks,
        output_key="tasks_plan",
        verbose=True,
    )

    # Chaîne séquentielle Lean
    pipeline = SequentialChain(
        chains=[chain_refine, chain_ac, chain_tasks],
        input_variables=["feature"],
        output_variables=["refined_story", "acceptance_criteria", "tasks_plan"],
        verbose=True,
    )
    return pipeline


def main():
    print("🔁 Pipeline Agile LEAN (refinement → Gherkin → tâches)\n")
    feature = input("Décris ta user story brute (ex: 'En tant qu’utilisateur, je veux ...') :\n> ").strip()
    if not feature:
        print("Aucune user story fournie. Fin.")
        return

    pipeline = build_pipeline()
    results = pipeline({"feature": feature})

    print("\n================= SORTIES (LEAN) =================")
    print("\n--- User story affinée ---\n")
    print(results["refined_story"])

    print("\n--- Critères d’acceptation (Gherkin) ---\n")
    print(results["acceptance_criteria"])

    print("\n--- Plan de tâches concis ---\n")
    print(results["tasks_plan"])
    print("==================================================\n")

try:
    llm = ChatOpenAI(model="gpt-4.1-mini")
    from langchain_core.prompts import PromptTemplate
    commit_prompt = PromptTemplate.from_template(
        "Rédige un message de commit (Conventional Commits) en 1 ligne pour la user story suivante.\n"
        "Contexte:\n{refined_story}\n"
    )
    commit_chain = LLMChain(llm=llm, prompt=commit_prompt, verbose=False)

    # ✅ Appel avec invoke (nouvelle méthode)
    result = commit_chain.invoke({"refined_story": results["refined_story"]})
    commit_msg = result.get("text", str(result)).strip()  # Accès sécurisé

    print("--- Message de commit (bonus) ---\n")
    print(commit_msg)
except Exception as e:
    print(f"(Bonus commit ignoré) Raison: {e}")

if __name__ == "__main__":
    main()