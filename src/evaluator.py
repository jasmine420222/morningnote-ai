# evaluator.py
# Purpose: Create CSV templates for model comparison and fact-checking.
#
# These templates are filled in manually after reviewing both model outputs.
# The evaluation covers: clarity, groundedness, risk awareness, and usefulness.

import pandas as pd
import os


def create_model_comparison_template(output_dir: str = "outputs") -> str:
    """
    Create a blank model comparison CSV template and save it to outputs/.

    The template has rows for each evaluation dimension and columns for
    Model A score, Model B score, and notes.

    Parameters
    ----------
    output_dir : str
        Directory to save the CSV file (default: "outputs").

    Returns
    -------
    str
        Path to the saved CSV file.

    Example
    -------
    >>> path = create_model_comparison_template()
    >>> print(f"Saved to: {path}")
    """
    # TODO: Implement this function in Phase 7
    # Hint: Create a DataFrame with these dimensions as rows:
    # clarity, financial_relevance, groundedness, conciseness,
    # risk_awareness, usefulness
    raise NotImplementedError("create_model_comparison_template() is not yet implemented.")


def create_fact_check_template(output_dir: str = "outputs") -> str:
    """
    Create a blank fact-check CSV template and save it to outputs/.

    The template has columns for: model, claim, supported (Yes/Partial/No),
    evidence, and notes.

    Parameters
    ----------
    output_dir : str
        Directory to save the CSV file (default: "outputs").

    Returns
    -------
    str
        Path to the saved CSV file.

    Example
    -------
    >>> path = create_fact_check_template()
    >>> print(f"Saved to: {path}")
    """
    # TODO: Implement this function in Phase 7
    raise NotImplementedError("create_fact_check_template() is not yet implemented.")
