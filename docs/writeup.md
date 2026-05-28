# MorningNote AI — Project Writeup

*Course: Generative AI for Finance*
*Due: May 27, 2026*

---

## 1. Project Summary

MorningNote AI is a prototype AI tool that generates personalized financial morning notes
for equity watchlists. Instead of manually searching for tickers and reading scattered
headlines, a user selects a sector of interest and the system automatically builds a watchlist,
fetches real market data, and generates a structured morning briefing using two different LLMs.

We then compare the two models' output on a six-dimension rubric and fact-check selected claims
against the source data, so the project is as much an evaluation of *whether* generative AI helps
in this workflow as it is a working demo.

---

## 2. Motivation and Problem

Financial news is noisy and fragmented. A retail investor, finance student, or junior analyst
who follows a particular theme — say AI semiconductors or big tech — typically has to open many
tabs every morning: one for prices, several for headlines, another for the earnings calendar, and
then mentally stitch it all into a view of "what matters today." This is repetitive, easy to do
inconsistently, and time-consuming before the market even opens.

The user problem we target is: *"I know what sector I care about, but I don't want to manually
search every ticker, read all the news, and organize everything into a clear morning note."* Our
goal is **not** a trading or recommendation system. It is to test whether a grounded LLM workflow
can turn raw market data and real headlines into a structured, useful, and honestly-hedged
briefing — and to show, through evaluation, where that AI adds value and where it still needs
human review.

---

## 3. Design Decisions

### Why sector-based selection instead of manual ticker entry?

Our original proposal had the user type in tickers every day. Based on teaching-team feedback we
redesigned the entry point around *interests* rather than *symbols*: the user picks a sector
(e.g. "AI & Semiconductors") and the system maps it to a curated five-name watchlist. This is
closer to how people actually think about the market ("I follow chips"), removes daily friction,
and still leaves room for a custom or mixed watchlist for power users. The sector→ticker map is a
**product rule**, not synthetic data — the prices and news behind it remain real.

### Why yfinance for market data?

`yfinance` gives free, reproducible access to real prices, previous closes, percent changes, and
volume with no API key. We considered WRDS/Compustat/CRSP, which are higher quality, but for a
user-facing morning briefing the core need is recent price action, not academic-grade panels.
yfinance is simpler to run and to grade. Crucially, our loader **raises a clear error rather than
inventing fake prices** if data is missing — grounding integrity over convenience.

### Why a saved CSV for news instead of a live news API?

We use a dual strategy: NewsAPI when a key is present, with an automatic fallback to a curated
`data/sample_news.csv` of ~360 real headlines. The saved CSV makes the project **reproducible
during grading** (it does not depend on a live key or rate limits) while still using real news.
All evaluation in this writeup was run against the curated CSV so the results are reproducible.

### Why compare two models?

Comparing one model to itself tells you little. Running the **same prompt** through two different
model families (OpenAI vs Anthropic) lets us ask a more useful question: do model choices
materially change the quality of a financial briefing, and in which dimensions? It also forces an
explicit evaluation rubric instead of an informal "looks good to me."

---

## 4. System Architecture

The pipeline is a linear, inspectable flow; each stage is one small module in `src/`:

```
sector_mapping.py    user's sector/custom choice  →  ticker watchlist
        ↓
market_data.py       yfinance  →  prices, % change, volume
                               →  broad market snapshot (indices, commodities, FX, rates)
                               →  earnings calendar
        ↓
news_loader.py       NewsAPI (live)  →  fallback to data/sample_news.csv  →  headlines for tickers
        ↓
prompt_builder.py    assemble all of the above into one grounded prompt (prompts/morningnote_prompt.txt)
        ↓
model_runner.py      run_openai_model() and run_anthropic_model() on the SAME prompt
        ↓
outputs/             model_a_morning_note.md, model_b_morning_note.md, baseline_note.md
        ↓
evaluator.py         model_comparison.csv, fact_check_table.csv  (filled by a human reviewer)
```

The same flow is exposed two ways: the `morningnote_demo.ipynb` notebook (step-by-step) and a
Streamlit app (`app.py`) with sector / custom / mixed watchlist modes. API keys are read from a
`.env` file via environment variables and are never hard-coded.

---

## 5. Data Sources

| Source | What it provides | How we use it |
|--------|-----------------|---------------|
| yfinance | Real stock prices, % change, volume; index/commodity/FX/rate snapshot; earnings dates | Market-data, snapshot, and earnings sections of the prompt |
| data/sample_news.csv | ~360 real news headlines (date, ticker, headline, source, url) | News section of the prompt; the reproducible fallback when no live key is set |
| NewsAPI (optional) | Live headlines when `NEWSAPI_KEY` is set | Primary news source; results refresh the CSV |

---

## 6. Prompt Design

The prompt (`prompts/morningnote_prompt.txt`) injects the sector, ticker list, market snapshot,
per-stock data, earnings calendar, and recent headlines, then asks for a fixed eight-section
note: **TL;DR, Broad Market Context, Sector Overview, Stock Snapshot, Earnings Watch, Key Themes,
Risk Radar, What to Watch, and Confidence & Limitations**.

The instructions are deliberately anti-hallucination:

- Use **only** the provided data; do not invent facts.
- Do not make unsupported causal claims; prefer "the move coincided with…" over "was caused by…".
- If a move has no clear driver in the news, **say the evidence is limited**.
- No buy/sell recommendations; this is not investment advice.

The fixed section structure also acts as a guardrail: it keeps both models on-task and makes the
two outputs directly comparable section-by-section.

**Fair-comparison note.** Because the experiment hinges on a fair comparison, both models receive
the identical prompt **and** the same generation settings: `temperature=0.3` for both, with an
output budget large enough for the full eight sections (we initially capped Anthropic at 1024
tokens, which truncated Claude's note mid-way; we raised it to 2048 and aligned temperature so the
only intended difference is the model itself).

---

## 7. Model Comparison Results

We compared **Model A — OpenAI `gpt-4o-mini`** against **Model B — Anthropic
`claude-haiku-4-5-20251001`** on the same "AI & Semiconductors" watchlist (NVDA, GOOGL, MSFT, AMD,
AVGO), same prompt, same data. A human reviewer scored each note 1–5 on six dimensions.

### Quantitative Comparison

| Dimension | Model A (GPT-4o-mini) | Model B (Claude Haiku) |
|---|:---:|:---:|
| Clarity | 5 | 4 |
| Financial relevance | 4 | 5 |
| Groundedness | 4 | 5 |
| Conciseness | 5 | 3 |
| Risk awareness | 3 | 5 |
| Usefulness | 4 | 5 |
| **Total** | **25** | **27** |

### Qualitative Observations

The two models have clearly different "personalities" on the identical prompt:

- **GPT-4o-mini is the better quick read.** It is concise (~3.1k characters), scannable, and
  faster to digest — it wins clarity and conciseness, and is the better fit when speed is the
  priority.
- **Claude Haiku is more thorough.** It is roughly twice as long (~6.7k characters), cites
  specific named headlines (e.g. BofA's "ignore the noise" on NVDA, the Vera-CPU story on AMD),
  includes trading volume and price levels, and — most distinctively — separates fact from
  inference with explicit **High / Medium / Low confidence tiers** and a closing disclaimer. This
  drives its wins on financial relevance, groundedness, risk awareness, and usefulness.

The most interesting result is the **gap between the mechanical score and the holistic judgment**.
The six-dimension totals are nearly tied (25 vs 27). On reflection the reviewer preferred Claude
overall because, for this use case, information richness and traceable grounding outweighed
brevity — even though Claude scored *lower* on conciseness. In other words, the rubric and the
"which would I actually use" verdict can diverge, and the extra dimension that tipped the decision
was the *value weighting*, not any single score. GPT remains the better choice when the priority
is a fast morning scan.

---

## 8. Fact-Check Results

We extracted six concrete claims (two from GPT, four from Claude) and checked each against the two
source datasets — the yfinance market data and the news CSV. Full table:
`outputs/fact_check_table.csv`.

| Model | Claim | Supported? |
|---|---|:---:|
| GPT | AMD made a $10B Taiwan AI-infrastructure investment | **Yes** |
| GPT | NVDA gaining "amid discussions about its potential in China" | **Partial** |
| Claude | NVDA traded on 186.5M shares of volume | **Yes** |
| Claude | NVIDIA's "Vera" CPUs may have weighed on AMD today | **Partial** |
| Claude | Bill Ackman's $2.1B investment relates to MSFT | **Partial** |
| Claude | Paul Tudor Jones made an $8B bet on small-cap chaos | **Yes** |

**Key finding.** Both models are **factually accurate on the hard numbers** — prices, percent
changes, trading volume, and dollar amounts all matched the source data exactly (the three "Yes" claims). Every "Partial" is the same failure mode: a real headline and a real price move both exist, but the model **links them as cause-and-effect (or as a specific association) when the data only shows co-occurrence**. To both models' credit, these inferences are hedged ("may have weighed", "(limited evidence)"), which is why we scored them Partial rather than No — but the pattern is exactly the causality risk the prompt warns against.

Note: model outputs were generated at a different time than the baseline snapshot; intraday price movements account for small discrepancies between the two.
---

## 9. Baseline vs AI Comparison

The non-AI baseline (`outputs/baseline_note.md`) simply dumps the raw inputs: the sector, the
tickers, the price table, the earnings calendar, and the list of headlines. It is complete and
100% faithful to the data, but it is **just data** — the reader still has to do all the synthesis.

The AI notes add value precisely in that synthesis layer: they group the five names into
leaders/laggards, connect headlines to themes, surface a risk radar, and frame everything in
cautious language with a confidence statement. For a human skimming before the open, that
organization is a real improvement over raw headlines. The trade-off is that the AI introduces the
causal-attribution risk documented in §8, which the baseline — by saying nothing — cannot. The
honest conclusion: **AI improves readability and structure, but the baseline is "safer" precisely
because it never interprets.** That is the case for keeping a human in the loop.

---

## 10. Failure Case

The clearest failure case comes from the higher-rated model, Claude. In its MSFT snapshot it wrote
that **"Bill Ackman's $2.1B investment"** was relevant to Microsoft. The underlying headline reads:
*"Billionaire Bill Ackman Pours $2,092,970,000 Into One Asset, Dumps Uber and Two Mag 7 Stocks."*

Two things are notable:

1. The **dollar figure is correct** — $2.1B is an accurate rounding of $2,092,970,000. The model
   handled the number well.
2. But the asset is explicitly **unnamed** ("One Asset"), and the headline even mentions *dumping*
   two "Mag 7" stocks. By placing this item under MSFT, the model implies an association — Ackman
   buying *into* Microsoft — that the source does not support and arguably contradicts.

This is a subtle and instructive failure: not a fabricated number, but an **unsupported
association** presented with quiet confidence inside an otherwise well-grounded note. It is more
dangerous than an obvious error because it reads as authoritative. The same pattern appears in the
NVDA/China and Vera-CPU/AMD claims (§8). It is the central reason the project insists on human
review for any investment-facing content, and why a model that is *more* detailed (and scores
higher overall) can also create *more* surface area for this kind of mistake.

---

## 11. Limitations

1. The sector-to-ticker mapping is manually curated.
2. The tool does not connect to the user's real portfolio.
3. The news CSV may not capture every important market event.
4. LLMs may overstate causality between price movements and news (see §8 and §10).
5. This prototype covers 10 sectors with 5 companies each.
6. The evaluation is based on a single watchlist on a single day, scored by one reviewer — the
   numbers are illustrative, not statistically robust.
7. Human review is still needed for investment-facing content.

---

## 12. What We Would Improve with More Time

- Run the comparison across multiple sectors and several days, with more than one reviewer, to
  make the scores statistically meaningful.
- Add a lightweight automated fact-check pass that flags causal language unsupported by the data,
  turning §8 from manual into semi-automated.
- Pull in SEC filings, earnings transcripts, and macro data for richer grounding.
- Let the model cite the specific headline/row behind each claim, so every statement is traceable.
- Use WRDS/Compustat/CRSP to build sector watchlists dynamically by market cap or fundamentals
  rather than from a hand-curated map.

---

## 13. Conclusion

A grounded, structured prompt running over real market data and real headlines does produce a
genuinely useful morning briefing — more readable and better organized than a raw data dump, and
factually reliable on the hard numbers. The two models trade off along a clear axis: GPT-4o-mini
is the concise quick-read, Claude Haiku is the thorough, risk-aware, better-grounded note, and on
balance we preferred Claude for this use case. But the evaluation also exposed a consistent
weakness — turning correlation into causation/association — that the better model is, if anything,
more prone to because it says more. The practical takeaway is that generative AI is a strong
*drafting and synthesis* tool for this workflow, but the final judgment, especially on causal and
attributive claims, still belongs to a human.

---

*This is not investment advice.*
