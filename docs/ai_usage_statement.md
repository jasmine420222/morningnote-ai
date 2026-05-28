# AI Usage Statement

*MorningNote AI — Generative AI for Finance Final Project*

---

## Tools Used

We used the following AI tools during this project:

1. **ChatGPT** — to help brainstorm the project scope, refine the PRD, design the
   evaluation framework, and clarify course requirements.

2. **Claude** — to help generate the initial project structure, draft Python modules,
   and debug code. We manually reviewed all generated code, tested the notebook on real
   tickers, verified that API keys were not hard-coded, and confirmed that outputs were
   based on real market data and news.

3. **OpenAI gpt-4o-mini** (Model A) — used as one of the two LLMs generating morning notes
   as part of the project's core functionality.

4. **Anthropic claude-haiku-4-5-20251001** (Model B) — used as the second LLM for model
   comparison.

---

## What AI Helped With

- Drafting the initial function signatures and docstrings in `src/`
- Suggesting the prompt structure for anti-hallucination instructions
- Formatting the evaluation tables in `outputs/`
- Explaining Python library usage (yfinance, pandas, Streamlit)

---

## How We Checked AI Outputs

- We manually reviewed all generated Python code before running it.
- We tested the notebook on real tickers and verified market data came from yfinance.
- We verified that no API keys were hard-coded in any file.
- We manually fact-checked claims in both model outputs against the source data
  (see `outputs/fact_check_table.csv`).
- We did not treat any AI-generated financial analysis as source truth.

---

## Which Parts Were Manually Produced

- Selection of sector-to-ticker mappings based on our own judgment
- Collection of real news headlines for `data/sample_news.csv`
- Human scoring of the model comparison table (`outputs/model_comparison.csv`)
- Identification of the failure case discussed in the writeup
- Final writeup conclusions and oral defense preparation

---

## Important Note

We do not treat AI-generated analysis as source truth. All financial claims in our
evaluation were checked against the input data where possible. The tool explicitly
instructs the LLMs to use cautious language and flag limited evidence.

---

## Paid Services and Cost

The project calls two paid LLM APIs as its core functionality:

| Provider | Model | Role | Approximate cost |
|----------|-------|------|------------------|
| OpenAI | `gpt-4o-mini` | Model A (morning note) | well under $1 total |
| Anthropic | `claude-haiku-4-5-20251001` | Model B (morning note) | well under $1 total |

Both are low-cost models and each note is a single short request. Across all of our
development and evaluation runs the combined spend was a fraction of a dollar — far below
the $50-per-team threshold that would require instructor approval. Market data (yfinance)
and the news fallback (`data/sample_news.csv`) are free; NewsAPI offers a free tier.
