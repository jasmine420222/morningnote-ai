# model_runner.py
# Purpose: Send a prompt to an LLM API and return the generated text.
#
# IMPORTANT: API keys must come from environment variables.
# They must NEVER be hard-coded in this file.

import os


def run_openai_model(prompt: str, model_name: str = "gpt-4o-mini") -> str:
    """
    Send a prompt to an OpenAI model and return the response text.

    Parameters
    ----------
    prompt : str
        The full prompt string to send to the model.
    model_name : str
        The OpenAI model to use (default: "gpt-4o-mini").

    Returns
    -------
    str
        The generated morning note text from the model.

    Raises
    ------
    ValueError
        If the OPENAI_API_KEY environment variable is not set.

    Example
    -------
    >>> note = run_openai_model(prompt, model_name="gpt-4o-mini")
    >>> print(note[:200])
    """
    # TODO: Implement this function in Phase 6
    # Hint:
    #   api_key = os.getenv("OPENAI_API_KEY")
    #   if not api_key: raise ValueError("OPENAI_API_KEY not set")
    #   from openai import OpenAI
    #   client = OpenAI(api_key=api_key)
    #   response = client.chat.completions.create(...)
    raise NotImplementedError("run_openai_model() is not yet implemented.")


def run_anthropic_model(prompt: str, model_name: str = "claude-haiku-4-5-20251001") -> str:
    """
    Send a prompt to an Anthropic Claude model and return the response text.

    Parameters
    ----------
    prompt : str
        The full prompt string to send to the model.
    model_name : str
        The Anthropic model to use (default: "claude-haiku-4-5-20251001").

    Returns
    -------
    str
        The generated morning note text from the model.

    Raises
    ------
    ValueError
        If the ANTHROPIC_API_KEY environment variable is not set.

    Example
    -------
    >>> note = run_anthropic_model(prompt)
    >>> print(note[:200])
    """
    # TODO: Implement this function in Phase 6
    # Hint:
    #   api_key = os.getenv("ANTHROPIC_API_KEY")
    #   if not api_key: raise ValueError("ANTHROPIC_API_KEY not set")
    #   import anthropic
    #   client = anthropic.Anthropic(api_key=api_key)
    #   message = client.messages.create(...)
    raise NotImplementedError("run_anthropic_model() is not yet implemented.")
