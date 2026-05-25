# MorningNote AI — Project Writeup

*Course: Generative AI for Finance*
*Due: May 27, 2026*

---

## 1. Project Summary

MorningNote AI is a prototype AI tool that generates personalized financial morning notes
for equity watchlists. Instead of manually searching for tickers and reading scattered
headlines, a user selects a sector of interest and the system automatically builds a watchlist,
fetches real market data, and generates a structured morning briefing using two different LLMs.

---

## 2. Motivation and Problem

[TO BE WRITTEN: 1-2 paragraphs explaining why this problem matters and who it is for]

---

## 3. Design Decisions

### Why sector-based selection instead of manual ticker entry?

[TO BE WRITTEN]

### Why yfinance for market data?

[TO BE WRITTEN]

### Why a saved CSV for news instead of a live news API?

[TO BE WRITTEN]

### Why compare two models?

[TO BE WRITTEN]

---

## 4. System Architecture

[TO BE WRITTEN: Describe the pipeline from sector selection to saved outputs]

---

## 5. Data Sources

| Source | What it provides | How we use it |
|--------|-----------------|---------------|
| yfinance | Real-time stock prices | Market data section of prompt |
| data/sample_news.csv | Real news headlines | News section of prompt |

---

## 6. Prompt Design

[TO BE WRITTEN: Explain how the prompt is structured and why anti-hallucination
instructions were included]

---

## 7. Model Comparison Results

[TO BE WRITTEN after running the notebook: Summarize findings from model_comparison.csv]

### Quantitative Comparison

[Insert model_comparison.csv table here]

### Qualitative Observations

[TO BE WRITTEN]

---

## 8. Fact-Check Results

[TO BE WRITTEN after running the notebook: Summarize findings from fact_check_table.csv]

---

## 9. Baseline vs AI Comparison

[TO BE WRITTEN: Compare the raw baseline note with the AI-generated notes.
Does AI add value? Where?]

---

## 10. Failure Case

[TO BE WRITTEN: Describe at least one case where a model output was weak,
unsupported, overconfident, or misleading]

---

## 11. Limitations

1. The sector-to-ticker mapping is manually curated.
2. The tool does not connect to the user's real portfolio.
3. The news CSV may not capture every important market event.
4. LLMs may overstate causality between price movements and news.
5. This prototype covers only 4 sectors and 5 companies each.
6. Human review is still needed for investment-facing content.

---

## 12. What We Would Improve with More Time

[TO BE WRITTEN]

---

## 13. Conclusion

[TO BE WRITTEN]

---

*This is not investment advice.*
