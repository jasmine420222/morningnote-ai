# MorningNote AI

An agentic AI tool that generates personalized financial morning notes for equity watchlists.

## What It Does

1. User selects a sector or investment theme (e.g., "AI & Semiconductors")
2. System builds a relevant stock watchlist automatically
3. System fetches real market data using `yfinance`
4. System loads real company news from a saved CSV file
5. System builds a grounded prompt and generates morning notes using two LLMs
6. System saves both outputs and evaluation tables for comparison

## Project Structure

```
morningnote-ai/
├── README.md               ← You are here
├── requirements.txt        ← Python packages needed
├── .env.example            ← Template for API keys
├── .gitignore
│
├── app.py                  ← Streamlit interactive demo
├── morningnote_demo.ipynb  ← Main Jupyter notebook (start here)
│
├── data/
│   ├── sample_news.csv     ← Real news headlines (manually collected)
│   └── sector_tickers.csv  ← Sector-to-ticker mapping reference
│
├── src/                    ← Python modules
│   ├── sector_mapping.py   ← Maps sector name → ticker list
│   ├── market_data.py      ← Fetches real data from yfinance
│   ├── news_loader.py      ← Loads news from CSV
│   ├── prompt_builder.py   ← Builds the LLM prompt
│   ├── model_runner.py     ← Calls OpenAI and Anthropic APIs
│   └── evaluator.py        ← Creates comparison/fact-check tables
│
├── prompts/
│   └── morningnote_prompt.txt  ← Reusable prompt template
│
├── outputs/                ← Generated notes and evaluation files
│   ├── baseline_note.md
│   ├── model_a_morning_note.md
│   ├── model_b_morning_note.md
│   ├── model_comparison.csv
│   └── fact_check_table.csv
│
└── docs/
    ├── PRD.md              ← Product Requirements Document
    ├── writeup.md          ← Audience-facing project writeup
    └── ai_usage_statement.md
```

## How to Run

### Step 1: Clone and set up environment

```bash
git clone <your-repo-url>
cd morningnote-ai
pip install -r requirements.txt
```

### Step 2: Set up API keys

```bash
cp .env.example .env
# Open .env and fill in your API keys
```

### Step 3: Run the Jupyter notebook

```bash
jupyter notebook morningnote_demo.ipynb
```

Run all cells from top to bottom. The notebook will walk you through the full workflow.

### Step 4: (Optional) Run the Streamlit app

```bash
streamlit run app.py
```

## Supported Sectors

| Sector | Tickers |
|--------|---------|
| AI & Semiconductors | NVDA, AMD, AVGO, TSM, ASML |
| Big Tech | AAPL, MSFT, GOOGL, AMZN, META |
| Banking | JPM, BAC, WFC, C, GS |
| Energy | XOM, CVX, COP, SLB, EOG |

## Models Used

- **Model A**: OpenAI `gpt-4o-mini`
- **Model B**: Anthropic `claude-haiku-4-5-20251001`

Both models receive the same input prompt for a fair comparison.

## Important Notes

- This tool is **not** investment advice.
- Market data comes from `yfinance` (real data).
- News data comes from `data/sample_news.csv` (real headlines).
- If data sources are unavailable, the system raises a clear error — it does **not** generate fake data.

## Requirements

- Python 3.9+
- See `requirements.txt` for full package list
- OpenAI API key (required)
- Anthropic API key (required for Model B)
