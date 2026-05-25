# evaluator.py
# Purpose: Generate evaluation templates for human scoring of model outputs.
#
# Think of this file as the "exam paper maker":
#   - It creates two blank CSV files in the outputs/ folder
#   - Your team fills them in manually after reading both model outputs
#   - No AI does the scoring — it's all human judgment
#
# Why manual? Because the rubric requires you to show you actually read
# and understood the AI outputs, not just that you generated them.

import os
import pandas as pd


# ── Table 1: Model Comparison ────────────────────────────────────────────────

def create_model_comparison_template(
    model_a_name: str = "GPT-4o-mini",
    model_b_name: str = "Claude Haiku",
    output_dir: str = "outputs",
) -> pd.DataFrame:
    """
    Create a blank model comparison table and save it as a CSV.

    In plain English:
        Makes a table with 6 rows (one per evaluation dimension).
        You fill in scores from 1-5 for each model after reading their outputs.
        The table is saved to outputs/model_comparison.csv.

    Scoring scale:
        1 = poor  |  2 = weak  |  3 = acceptable  |  4 = good  |  5 = excellent

    Parameters
    ----------
    model_a_name : str
        Display name for Model A (default: "GPT-4o-mini").
    model_b_name : str
        Display name for Model B (default: "Claude Haiku").
    output_dir : str
        Folder to save the CSV in (default: "outputs").

    Returns
    -------
    pd.DataFrame
        The blank comparison table (also saved to disk).

    Example
    -------
    >>> df = create_model_comparison_template()
    >>> print(df)
    """
    # These are the 6 dimensions the rubric asks us to evaluate
    # Each dimension is one row in the table
    dimensions = [
        {
            "dimension": "clarity",
            "description": "Is the note easy to read and well-structured?",
            model_a_name: "",   # You fill this in (1-5)
            model_b_name: "",   # You fill this in (1-5)
            "notes": "",        # Any observations about the difference
        },
        {
            "dimension": "financial_relevance",
            "description": "Does the note focus on what matters for this sector?",
            model_a_name: "",
            model_b_name: "",
            "notes": "",
        },
        {
            "dimension": "groundedness",
            "description": "Does the note stick to the provided data, or does it make things up?",
            model_a_name: "",
            model_b_name: "",
            "notes": "",
        },
        {
            "dimension": "conciseness",
            "description": "Is the note appropriately brief, without unnecessary padding?",
            model_a_name: "",
            model_b_name: "",
            "notes": "",
        },
        {
            "dimension": "risk_awareness",
            "description": "Does the note flag risks and use cautious language where needed?",
            model_a_name: "",
            model_b_name: "",
            "notes": "",
        },
        {
            "dimension": "usefulness",
            "description": "Would this note actually help someone start their trading day?",
            model_a_name: "",
            model_b_name: "",
            "notes": "",
        },
    ]

    df = pd.DataFrame(dimensions)

    # Make sure the outputs/ folder exists before saving
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, "model_comparison.csv")
    df.to_csv(filepath, index=False)

    print(f"[evaluator] Model comparison template saved to {filepath}")
    print(f"  → Open the file and fill in scores (1-5) for '{model_a_name}' and '{model_b_name}'")

    return df


# ── Table 2: Fact-Check ──────────────────────────────────────────────────────

def create_fact_check_template(
    output_dir: str = "outputs",
) -> pd.DataFrame:
    """
    Create a blank fact-check table and save it as a CSV.

    In plain English:
        Makes a table where each row is one specific claim from a model output.
        You read the AI's morning note, pick 3-5 sentences that make factual claims,
        then check whether each claim is supported by the source data
        (the market data table or the news CSV).

    Supported options:
        Yes     — the claim is directly supported by the source data
        Partial — the claim is roughly correct but overstated or imprecise
        No      — the claim is not supported (hallucination or wrong causality)

    Parameters
    ----------
    output_dir : str
        Folder to save the CSV in (default: "outputs").

    Returns
    -------
    pd.DataFrame
        The blank fact-check table (also saved to disk).

    Example
    -------
    >>> df = create_fact_check_template()
    >>> print(df)
    """
    # We pre-fill example rows so you know exactly what to write
    # Replace these with real claims from your actual model outputs
    example_rows = [
        {
            "model": "Model A (GPT-4o-mini)",
            "claim": "Example: NVDA rose 1.73% on the day",
            "supported": "",        # Fill in: Yes / Partial / No
            "evidence": "",         # Where in the data you checked (e.g., "yfinance market data")
            "notes": "",            # Any extra observations
        },
        {
            "model": "Model A (GPT-4o-mini)",
            "claim": "Example: The rise was caused by strong AI chip demand",
            "supported": "",
            "evidence": "",
            "notes": "",
        },
        {
            "model": "Model B (Claude Haiku)",
            "claim": "Example: Evidence is limited for the reason behind AMD's move",
            "supported": "",
            "evidence": "",
            "notes": "",
        },
        {
            "model": "Model B (Claude Haiku)",
            "claim": "Example: [Add a real claim from your model output here]",
            "supported": "",
            "evidence": "",
            "notes": "",
        },
    ]

    df = pd.DataFrame(example_rows)

    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, "fact_check_table.csv")
    df.to_csv(filepath, index=False)

    print(f"[evaluator] Fact-check template saved to {filepath}")
    print("  → Replace the example claims with real sentences from your model outputs.")
    print("  → Fill in 'supported' (Yes/Partial/No) and 'evidence' for each claim.")

    return df


# ── Helper: print a summary of both tables ──────────────────────────────────

def print_evaluation_instructions() -> None:
    """
    Print a quick reminder of how to fill in the evaluation tables.

    Call this in the notebook after generating the two model outputs,
    so you and your partner know exactly what to do next.
    """
    print("""
=== Evaluation Instructions ===

Step 1 — Read both model outputs in outputs/
    - outputs/model_a_morning_note.md
    - outputs/model_b_morning_note.md

Step 2 — Fill in outputs/model_comparison.csv
    Score each dimension 1-5 for both models.
    1=poor, 2=weak, 3=acceptable, 4=good, 5=excellent

Step 3 — Fill in outputs/fact_check_table.csv
    Pick 3-5 specific factual claims from each model output.
    Check each claim against the market data and news CSV.
    Label each: Yes / Partial / No

Step 4 — Identify one failure case
    Find one example where a model made an unsupported causal claim
    (e.g., "stock rose BECAUSE of...") when the data only shows
    the event and the price move happened at the same time.
    Write this up in docs/writeup.md Section 10.
""")
