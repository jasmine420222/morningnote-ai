# PRD: MorningNote AI

## 1. Project Title

**MorningNote AI: An Agentic Financial Briefing Generator for Equity Watchlists**

---

## 2. One-Sentence Summary

MorningNote AI is an agentic AI tool that helps users generate personalized financial morning notes by selecting an industry or investment theme, automatically building a relevant stock watchlist, retrieving real market data and company news, and comparing outputs from different large language models.

---

## 3. Project Motivation

Financial news feeds are noisy. A retail investor, finance student, or junior analyst may care about a specific sector, such as AI semiconductors, big tech, banking, or energy, but they often need to read many headlines and check many tickers manually every morning.

Our original idea was to let users manually enter a few tickers. Based on feedback from the teaching team, we are redesigning the project to make it more user-friendly: instead of forcing users to enter tickers every day, the user can select an industry or investment theme, and the system will automatically create a focused equity watchlist.

The goal is not to build a trading recommendation system. The goal is to test whether generative AI can help turn messy market data and financial news into a structured, useful, and fact-grounded morning briefing.

---

## 4. Target Users

The target users are:

1. **Retail investors** who follow certain sectors but do not want to read many scattered headlines every morning.
2. **Finance students** who want a structured summary of market movements and company news.
3. **Junior analysts** who need a quick starting point before doing deeper research.

---

## 5. User Problem

The user's problem is:

> "I know what sector I care about, but I do not want to manually search for every ticker, read all the news, and organize everything into a clear morning note."

For example, a user may care about AI and semiconductor stocks. Instead of manually entering NVDA, AMD, AVGO, TSM, and ASML every day, the user can simply choose:

```text
Sector: AI & Semiconductors
Style: Large-cap leaders
Number of companies: 5
```

Then MorningNote AI automatically generates the relevant watchlist and produces a structured briefing.

---

## 6. Product Goal

The product goal is to build a working prototype that can:

1. Let the user select a sector or investment theme.
2. Automatically map that selection to a small equity watchlist.
3. Retrieve real stock market data.
4. Load real company news from a saved CSV file.
5. Build a grounded prompt for LLMs.
6. Generate morning notes using two different models.
7. Compare model outputs.
8. Show where the AI is useful and where it may fail.

This project fits the course requirement because it builds a practical generative/agentic AI tool for a finance workflow.

---

## 7. Core Product Workflow

```text
User selects sector/theme
        ↓
System builds ticker watchlist
        ↓
System fetches real market data with yfinance
        ↓
System loads real company news from CSV
        ↓
System builds structured prompt
        ↓
Model A generates morning note
        ↓
Model B generates morning note
        ↓
System saves both outputs
        ↓
Team evaluates model outputs
        ↓
Final writeup explains results, limitations, and insights
```

---

## 8. Core Features

### Feature 1: Sector / Theme Selection

The user can select one of several predefined sectors or themes.

Initial supported sectors:

```python
SECTOR_TICKERS = {
    "AI & Semiconductors": ["NVDA", "AMD", "AVGO", "TSM", "ASML"],
    "Big Tech": ["AAPL", "MSFT", "GOOGL", "AMZN", "META"],
    "Banking": ["JPM", "BAC", "WFC", "C", "GS"],
    "Energy": ["XOM", "CVX", "COP", "SLB", "EOG"]
}
```

Important clarification:

This sector-to-ticker mapping is **not synthetic financial data**. It is a product design rule that decides which real companies to include when a user selects a sector. The actual market data and news used by the model must come from real sources.

### Feature 2: Real Market Data Retrieval

The system will use `yfinance` to retrieve real market data for selected tickers.

For each ticker, the system should retrieve:

```text
ticker
latest price
previous close
daily percent change
trading volume
```

The code should raise a clear error if market data cannot be fetched. It should not silently create fake price data.

### Feature 3: Real News CSV

The system will load real company news from a CSV file:

```text
data/sample_news.csv
```

The CSV should contain real headlines collected from public financial news sources.

Required columns:

```csv
date,ticker,headline,source,url
```

Example format:

```csv
date,ticker,headline,source,url
2026-05-25,NVDA,Nvidia shares rise as investors focus on AI chip demand,Yahoo Finance,https://example.com
2026-05-25,AMD,AMD announces expanded AI accelerator partnership,Reuters,https://example.com
```

The saved CSV improves reproducibility because the project will not depend fully on live news APIs during grading. However, the news must still be real, not invented.

### Feature 4: Prompt Builder

The system will convert market data and news into a structured prompt.

The prompt must include instructions such as:

```text
You are writing a financial morning note.

Use only the provided market data and news.
Do not invent facts.
Do not make unsupported causal claims.
If the data does not prove why a stock moved, use cautious wording such as "the move coincided with..." or "the available news suggests..."
If evidence is limited, say that evidence is limited.
```

The output format should include:

```text
1. Market Overview
2. Sector Summary
3. Company-Specific Notes
4. Key Risks
5. What to Watch Today
6. Confidence and Limitations
```

### Feature 5: Two-Model Generation

The project should compare two different LLMs or two different model settings.

Preferred option:

```text
Model A: OpenAI GPT model, such as gpt-4o-mini
Model B: Anthropic Claude model, such as Claude Sonnet or Claude Haiku
```

Simpler backup option:

```text
Model A: gpt-4o-mini
Model B: another OpenAI model, such as gpt-4.1-mini or gpt-4o
```

Both models must receive the same input prompt, so the comparison is fair.

### Feature 6: Model Output Saving

The system should save model outputs in the `outputs/` folder.

Example files:

```text
outputs/baseline_note.md
outputs/model_a_morning_note.md
outputs/model_b_morning_note.md
outputs/model_comparison.csv
outputs/fact_check_table.csv
```

### Feature 7: Basic Evaluation

The project must include evaluation evidence.

Our evaluation will include three parts:

1. **Model comparison**
2. **Fact-check table**
3. **Failure case**

---

## 9. Baseline Comparison

In addition to comparing two models, the project should create a simple non-AI baseline.

The baseline will simply list:

```text
selected sector
selected tickers
price changes
raw headlines
```

The AI-generated note should improve over this baseline by:

```text
organizing information
summarizing key movements
highlighting risks
making the briefing easier to read
```

This helps show whether the AI component adds value over a simple non-AI workflow.

---

## 10. Model Comparison Evaluation

The project should compare outputs from two models using a simple human scoring table.

Evaluation dimensions:

```text
clarity
financial relevance
groundedness
conciseness
risk awareness
usefulness
```

Example table:

| Dimension | Model A | Model B | Notes |
|---|---:|---:|---|
| Clarity | 4 | 5 | Model B is easier to read |
| Financial relevance | 4 | 4 | Both mention major market moves |
| Groundedness | 3 | 4 | Model A makes one unsupported causal claim |
| Conciseness | 5 | 3 | Model A is shorter |
| Risk awareness | 3 | 5 | Model B gives better risk language |
| Usefulness | 4 | 4 | Both are more useful than raw headlines |

Scoring scale:

```text
1 = poor
2 = weak
3 = acceptable
4 = good
5 = excellent
```

---

## 11. Fact-Check Evaluation

The project should manually extract selected claims from each model output and check whether they are supported by the source data.

Example table:

| Model | Claim | Supported? | Evidence | Notes |
|---|---|---|---|---|
| GPT | NVDA rose 2.1% | Yes | yfinance market data | Correct |
| GPT | AMD fell because of weak AI demand | No | News does not support this | Unsupported causal claim |
| Claude | Evidence is limited for the reason behind AMD's move | Yes | No direct cause in news | Good caution |

Supported status options:

```text
Yes
Partial
No
```

---

## 12. Failure Case

The project should include at least one failure case where an LLM output is weak, unsupported, too vague, too confident, or misleading.

Example failure case:

```text
The model says a stock moved because of a specific news headline, but the input data only shows that the price movement and headline happened around the same time. The model overstates causality.
```

The final writeup should honestly discuss this limitation and explain why human review is still needed for investment-facing content.

---

## 13. Data Strategy

The project uses two types of real data:

1. **Market data** from `yfinance`.
2. **Company news** from a saved CSV of real news headlines.

We considered using WRDS because it provides high-quality academic financial datasets. However, for this prototype, the core need is recent price movements and company news for a user-facing morning briefing. `yfinance` is simpler, easier to reproduce, and sufficient for the main workflow.

WRDS may be discussed as future work. In a future version, WRDS, Compustat, or CRSP could be used to dynamically select sector constituents by market capitalization, firm fundamentals, or trading style.

The project will not use synthetic prices or synthetic news.

---

## 14. API Keys and Environment Variables

The project may use the following API keys:

```text
OPENAI_API_KEY
ANTHROPIC_API_KEY
FINNHUB_API_KEY optional
NEWS_API_KEY optional
```

API keys must not be hard-coded in the code.

Correct approach:

```python
import os

openai_key = os.getenv("OPENAI_API_KEY")
```

The repository should include:

```text
.env.example
```

Example `.env.example`:

```text
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
FINNHUB_API_KEY=
NEWS_API_KEY=
```

The repository should also include `.gitignore` with:

```text
.env
__pycache__/
.ipynb_checkpoints/
.DS_Store
outputs/*.tmp
```

The final submission must not include real secrets or API keys.

---

## 15. Recommended Technical Stack

```text
Language: Python
Notebook: Jupyter Notebook
App demo: Streamlit
Market data: yfinance
News data: saved CSV of real headlines
LLM APIs: OpenAI and/or Anthropic
Data manipulation: pandas
Output format: Markdown / HTML / CSV
```

---

## 16. Expected Repository Structure

```text
morningnote-ai/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── app.py
├── morningnote_demo.ipynb
│
├── data/
│   ├── sample_news.csv
│   └── sector_tickers.csv
│
├── src/
│   ├── sector_mapping.py
│   ├── market_data.py
│   ├── news_loader.py
│   ├── prompt_builder.py
│   ├── model_runner.py
│   └── evaluator.py
│
├── prompts/
│   └── morningnote_prompt.txt
│
├── outputs/
│   ├── baseline_note.md
│   ├── model_a_morning_note.md
│   ├── model_b_morning_note.md
│   ├── model_comparison.csv
│   └── fact_check_table.csv
│
└── docs/
    ├── PRD.md
    ├── writeup.md
    └── ai_usage_statement.md
```

---

## 17. File Responsibilities

### `src/sector_mapping.py`

Purpose:

```text
Map user-selected sectors to ticker lists.
```

Main function:

```python
get_tickers_for_sector(sector_name)
```

Expected behavior:

- Return a list of tickers for a valid sector.
- Raise a clear error if the sector is not supported.
- Keep the mapping simple and easy to inspect.

### `src/market_data.py`

Purpose:

```text
Fetch real stock data from yfinance.
```

Main function:

```python
get_market_data(tickers)
```

Output:

```text
pandas DataFrame with ticker, latest price, previous close, percent change, volume
```

Expected behavior:

- Use yfinance to fetch real data.
- Return clean data.
- Raise a clear error if data is missing.
- Do not generate fake fallback values.

### `src/news_loader.py`

Purpose:

```text
Load real company news from data/sample_news.csv.
```

Main function:

```python
load_news_for_tickers(tickers, csv_path="data/sample_news.csv")
```

Expected behavior:

- Read the CSV file.
- Filter rows where ticker is in the selected ticker list.
- Return a pandas DataFrame.
- Raise a clear error if the file is missing.
- Do not generate fake fallback news.

### `src/prompt_builder.py`

Purpose:

```text
Build grounded LLM prompt from sector, tickers, market data, and news.
```

Main function:

```python
build_morningnote_prompt(sector, tickers, market_df, news_df)
```

Expected behavior:

- Include market data and news in a readable format.
- Include anti-hallucination instructions.
- Ask the model to use cautious language.
- Ask the model to produce a structured morning note.

### `src/model_runner.py`

Purpose:

```text
Run LLM models using environment variables.
```

Main functions:

```python
run_openai_model(prompt, model_name)
run_anthropic_model(prompt, model_name)
```

Expected behavior:

- Read API keys from environment variables.
- Raise clear errors if API keys are missing.
- Return generated text.
- Do not hard-code secrets.

### `src/evaluator.py`

Purpose:

```text
Create model comparison and fact-check tables.
```

Main functions:

```python
create_model_comparison_template()
create_fact_check_template()
```

Expected behavior:

- Create blank or partially filled CSV templates.
- Save evaluation files in `outputs/`.
- Support manual evaluation.

### `app.py`

Purpose:

```text
A simple Streamlit demo.
```

User interface:

```text
select sector
show selected tickers
show market data
show news
generate morning notes
show model comparison
```

Expected behavior:

- Keep the interface simple.
- Prioritize usability and clarity.
- Avoid unnecessary features such as login, database, or portfolio upload.

### `morningnote_demo.ipynb`

Purpose:

```text
Main notebook showing the full project workflow.
```

Notebook sections:

```text
1. Introduction
2. User selects sector
3. Build watchlist
4. Fetch market data
5. Load news
6. Build prompt
7. Generate outputs from two models
8. Show baseline
9. Compare model outputs
10. Fact-check claims
11. Conclusion and limitations
```

---

## 18. Prompt Template

The prompt should look like this:

```text
You are a financial analyst writing a daily morning note for a user who follows the selected sector.

The user is interested in:
{sector}

The selected tickers are:
{tickers}

Market data:
{market_data}

Company news:
{news_data}

Instructions:
- Use only the provided market data and news.
- Do not invent facts.
- Do not make unsupported causal claims.
- If a stock moved but the reason is not clear from the news, say that the evidence is limited.
- Use cautious language such as "the move coincided with" instead of "the move was caused by" unless the source clearly supports causality.
- This is not investment advice.
- Be concise, structured, and useful for a morning briefing.

Write a structured morning note with the following sections:

1. Market Overview
2. Sector Summary
3. Company-Specific Notes
4. Key Risks
5. What to Watch Today
6. Confidence and Limitations
```

---

## 19. Output Requirements

Each model should produce a note with:

```text
clear section headings
ticker-specific discussion
market data references
news references
risk flags
cautious language
no investment recommendation
```

The note should not say:

```text
Buy this stock
Sell this stock
This stock will definitely rise
This stock is guaranteed to outperform
```

Instead, it should say:

```text
This stock may be worth monitoring
The available data suggests
The evidence is limited
The move coincided with
This development may be relevant for investors watching the sector
```

---

## 20. Success Criteria

The project is successful if:

1. A reviewer can run the notebook or app.
2. The system uses real market data and real news headlines.
3. The system generates a readable morning note.
4. The project compares two model outputs.
5. The evaluation identifies at least one strength and one weakness of the AI output.
6. The writeup clearly explains the product design, data choices, model comparison, limitations, and future work.
7. The repository includes README, requirements, prompts, outputs, and AI usage statement.
8. No API keys or secrets are included in the final submission.

---

## 21. Scope Control

### Must-Have Features

```text
sector selection
ticker mapping
yfinance market data
real news CSV
LLM prompt
two-model output
baseline note
model comparison table
fact-check table
writeup
AI usage statement
README
requirements.txt
```

### Nice-to-Have Features

```text
live news API
WRDS integration
SEC filings
portfolio upload
email delivery
advanced dashboard
automatic fact-checking
GitHub Pages site
```

If time is limited, prioritize the notebook, real data, model comparison, and writeup over a polished web interface.

---

## 22. Limitations

Current limitations:

1. The sector-to-ticker mapping is manually curated.
2. The tool does not connect to the user's real portfolio.
3. The news CSV may not capture every important market event.
4. LLMs may overstate causality.
5. The tool is not investment advice.
6. Human review is still needed for investment-facing content.
7. The prototype focuses on a small number of sectors and companies.
8. The model comparison is based on a limited number of examples.

---

## 23. Future Work

Future improvements could include:

```text
connect directly to user portfolio
use WRDS/Compustat/CRSP for dynamic sector selection
add SEC filings
add earnings calendar
add macroeconomic data
automate fact-checking
support email delivery every morning
add user preference memory
support more sectors and trading styles
```

---

## 24. AI Usage Statement Requirement

The final repository must include:

```text
docs/ai_usage_statement.md
```

It should explain:

```text
which AI tools were used
what they helped with
how the team checked the outputs
which parts were manually reviewed
how AI-generated claims were fact-checked
```

Suggested content:

```markdown
# AI Usage Statement

We used ChatGPT to help brainstorm the project scope, refine the PRD, design the evaluation framework, and explain course requirements.

We used Claude Code or Codex to help generate the initial project structure, draft Python modules, and debug code. We manually reviewed the generated code, tested the notebook on real tickers, checked that API keys were not hard-coded, and verified that outputs were based on the provided market data and news.

We used LLM APIs as part of the project to generate financial morning notes. We evaluated the model outputs by comparing two models and manually fact-checking selected claims against the source data.

We do not treat AI-generated analysis as source truth. All financial claims in the evaluation were checked against the input data where possible.
```

---

## 25. Final Deliverables

The final submission should include:

```text
primary notebook or report
audience-facing writeup
README with reproduction instructions
requirements.txt or environment file
supporting code and prompts
sample outputs
evaluation results
AI usage statement
```

Recommended files:

```text
README.md
requirements.txt
.env.example
.gitignore
app.py
morningnote_demo.ipynb
data/sample_news.csv
src/
prompts/morningnote_prompt.txt
outputs/baseline_note.md
outputs/model_a_morning_note.md
outputs/model_b_morning_note.md
outputs/model_comparison.csv
outputs/fact_check_table.csv
docs/PRD.md
docs/writeup.md
docs/ai_usage_statement.md
```

---

## 26. Development Instructions for Codex or Claude Code

When using Codex or Claude Code, the coding assistant should follow these instructions:

```text
You are helping build a student final project for a Generative AI for Finance course.

Project name:
MorningNote AI: An Agentic Financial Briefing Generator for Equity Watchlists

Please follow this PRD exactly. Keep the project simple, beginner-friendly, reproducible, and easy to explain in an oral defense.

Important requirements:
1. The user should select a sector or investment theme instead of manually entering tickers.
2. The system should map the selected sector to a small stock watchlist.
3. The system should fetch real market data using yfinance.
4. The system should load real company news from data/sample_news.csv.
5. The system should not generate fake data if files or APIs fail.
6. The system should build a grounded LLM prompt.
7. The system should generate morning notes using two different models.
8. The system should save both outputs.
9. The system should include simple evaluation tables for model comparison and fact-checking.
10. API keys must come from environment variables and must not be hard-coded.
11. Include README.md, requirements.txt, .env.example, .gitignore, docs/PRD.md, docs/writeup.md, and docs/ai_usage_statement.md.
12. Add comments in the code so beginners can understand it.

Start by creating the project structure and placeholder files. Do not over-engineer the app.
```

---

## 27. Step-by-Step Development Plan

### Phase 1: Create Project Structure

Create folders:

```text
src/
data/
prompts/
outputs/
docs/
```

Create files:

```text
README.md
requirements.txt
.env.example
.gitignore
app.py
morningnote_demo.ipynb
docs/PRD.md
docs/writeup.md
docs/ai_usage_statement.md
```

### Phase 2: Build Sector Mapping

Create:

```text
src/sector_mapping.py
```

Implement:

```python
get_tickers_for_sector(sector_name)
```

### Phase 3: Build Market Data Loader

Create:

```text
src/market_data.py
```

Implement:

```python
get_market_data(tickers)
```

### Phase 4: Build News Loader

Create:

```text
src/news_loader.py
```

Implement:

```python
load_news_for_tickers(tickers, csv_path="data/sample_news.csv")
```

### Phase 5: Build Prompt Builder

Create:

```text
src/prompt_builder.py
```

Implement:

```python
build_morningnote_prompt(sector, tickers, market_df, news_df)
```

### Phase 6: Build Model Runner

Create:

```text
src/model_runner.py
```

Implement:

```python
run_openai_model(prompt, model_name)
run_anthropic_model(prompt, model_name)
```

### Phase 7: Build Evaluator

Create:

```text
src/evaluator.py
```

Implement:

```python
create_model_comparison_template()
create_fact_check_template()
```

### Phase 8: Build Main Notebook

Create:

```text
morningnote_demo.ipynb
```

The notebook should show the complete workflow from sector selection to evaluation.

### Phase 9: Build Streamlit App

Create:

```text
app.py
```

The app should provide a simple interactive demo.

### Phase 10: Complete Writeup and AI Usage Statement

Create:

```text
docs/writeup.md
docs/ai_usage_statement.md
```

---

## 28. Final Defense Talking Points

In the final defense, the team should be able to explain:

1. Why the project starts from user sector interests instead of manual ticker entry.
2. How the ticker watchlist is created.
3. Where the market data comes from.
4. Where the news data comes from.
5. How the prompt reduces hallucination risk.
6. Why two models are compared.
7. Which model worked better and why.
8. One failure case where the model output was weak or unsupported.
9. What the team built that an AI coding tool could not have fully produced by itself.
10. What the team would improve with more time.

Suggested explanation:

```text
Our original proposal used manual ticker entry. Based on feedback from the teaching team, we redesigned the workflow to start from user interests instead. The user selects a sector or theme, and the system automatically builds a relevant watchlist. This makes the tool easier to use and closer to a real financial news workflow.

We also compared two LLMs on the same input. We found that model differences matter: one model may be more concise, while another may be more cautious about unsupported causal claims. However, both models still require human review, especially when financial causality is unclear.
```

---

## 29. Final Submission Checklist

Before submission, check:

```text
[ ] README.md explains how to run the project.
[ ] requirements.txt is included.
[ ] .env.example is included.
[ ] .env is NOT included.
[ ] No API keys are in the code.
[ ] data/sample_news.csv contains real news headlines.
[ ] yfinance market data works or raises clear errors.
[ ] The notebook runs from top to bottom.
[ ] At least two model outputs are saved.
[ ] Baseline note is included.
[ ] Model comparison table is included.
[ ] Fact-check table is included.
[ ] Failure case is discussed.
[ ] docs/writeup.md is complete.
[ ] docs/ai_usage_statement.md is complete.
[ ] outputs/ folder contains sample results.
[ ] All group members are included in the final submission email.
```

---

## 30. Final Project Boundary

This project is **not**:

```text
a trading bot
a stock prediction model
an investment advice system
a full portfolio management platform
a replacement for human financial analysis
```

This project **is**:

```text
a finance-focused AI briefing prototype
a generative AI workflow for summarizing market data and news
a model comparison experiment
a practical tool demo for a real financial information workflow
```
