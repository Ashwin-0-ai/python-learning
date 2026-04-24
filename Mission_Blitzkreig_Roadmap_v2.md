# Mission Blitzkreig — Revised Roadmap v2

**Goal:** Land a Data Analytics / AI Marketing role in Germany.
**Timeline:** 6 months total. Month 1 complete, Month 2 in progress.
**Last updated:** April 2026

---

## Guiding principles for this version

1. **Depth over breadth.** Fewer projects, each one production-quality.
2. **Build for the recruiter's filter.** Every month adds one keyword that appears in German job postings: dbt, Snowflake, Power BI, Docker, Azure, RAG.
3. **Stop living in notebooks after Month 2.** Proper Python packages, tests, CI. Notebooks for exploration only.
4. **AI-augmented workflow is mandatory.** Every task: AI drafts, you audit and refactor. Document the audit in commits.
5. **German language runs in parallel.** 30 min/day from Month 2 onward. Target B1 by Month 6.
6. **README is 80% of the portfolio signal.** Most recruiters never read the code.

---

## MONTH 1 — Python & Data Foundations ✅ COMPLETE

Kept exactly as done. No changes.

- Days 1–10: Python basics (variables, loops, functions, error handling, file I/O)
- Days 11–19: Pandas, data cleaning, merging, time-series, Plotly, KPI calculations (CTR, CPM, ROI, CVR)
- Days 20–21: Code quality pass, GitHub README, Month 1 wrap

**Portfolio Project 1:** Irish OOH Advertising Campaign Analysis (notebooks, Plotly dashboards, Excel exports)

---

## MONTH 2 — SQL + Cloud Data Warehouse + Analytics Engineering

**Theme:** Move from SQLite as a learning toy to the stack recruiters actually filter for.

### Week 5 — SQL Fundamentals ✅ IN PROGRESS

Keep your current plan as-is.

- Day 22 ✅ SQL setup, first queries
- Day 23 ✅ WHERE, ORDER BY, LIMIT
- Day 24 ✅ Aggregates (COUNT, SUM, AVG, MIN, MAX)
- Day 25 📍 GROUP BY, HAVING *(currently here)*
- Day 26 JOINs (INNER, LEFT, RIGHT, FULL)
- Day 27 Subqueries, nested queries, IN/NOT IN/EXISTS
- Day 28 Week-5 review — rebuild Project 1 queries in SQL

### Week 6 — Advanced SQL (the part interviews actually test)

- Day 29 CTEs (WITH clause), readability patterns
- Day 30 Window functions part 1 — ROW_NUMBER, RANK, DENSE_RANK
- Day 31 Window functions part 2 — LAG, LEAD, running totals, moving averages
- Day 32 Query optimization — indexes, EXPLAIN plans, when joins get slow
- Day 33 Date/time functions, string functions, CASE WHEN patterns
- Day 34 SQL interview-style problems (StrataScratch / DataLemur free tier)
- Day 35 Week-6 review — solve 10 mixed problems end-to-end

### Week 7 — Cloud Data Warehouse + Data Modeling

- Day 36 Snowflake free trial OR BigQuery sandbox — sign up, load OOH dataset
- Day 37 Snowflake/BigQuery architecture — warehouses, storage, partitioning
- Day 38 Data modeling — fact vs. dimension tables, star schema
- Day 39 Slowly Changing Dimensions (SCD Type 1 and 2)
- Day 40 Redesign OOH dataset as a star schema in the cloud DWH
- Day 41 Load, query, measure cost/performance
- Day 42 Week-7 review — document the schema with a diagram

### Week 8 — dbt Core (analytics engineering)

- Day 43 Install dbt Core, connect to Snowflake/BigQuery
- Day 44 Staging models, sources, refs
- Day 45 Marts layer, dimensional models
- Day 46 dbt tests (generic + singular), documentation
- Day 47 dbt macros and Jinja basics
- Day 48 Lineage graphs, `dbt docs generate`
- Day 49 Month 2 wrap — push the full dbt project to GitHub

**Portfolio Project 2:** OOH Campaign Analytics — dbt project on Snowflake/BigQuery, star schema, tests, docs, lineage graph in README. Push `.sql` and `dbt_project.yml`, not notebooks.

---

## MONTH 3 — Power BI + Statistics + A/B Testing

**Theme:** Become the person who can both crunch and communicate. This is the month that turns you from "Python scripter" into "analyst."

### Week 9 — Power BI fundamentals

- Days 50–51 Power BI Desktop install, data load, basic visuals
- Days 52–53 Data modeling in Power BI, relationships, star schema connection to dbt output
- Days 54–55 DAX basics — measures vs. columns, CALCULATE, filter context
- Day 56 Build v1 of OOH executive dashboard

### Week 10 — Advanced Power BI

- Day 57 Time intelligence DAX (YTD, MTD, prior period)
- Day 58 Advanced measures — iterators, variables, RANKX
- Day 59 Row-level security, parameters, bookmarks
- Day 60 Dashboard design principles (IBCS basics — German companies love this)
- Day 61 Publish to Power BI Service, scheduled refresh
- Day 62 Polish the OOH exec dashboard
- Day 63 Week-10 review — screenshot + write-up for portfolio

### Week 11 — Statistics you'll actually use

- Day 64 Distributions, central tendency, variance
- Day 65 Sampling, confidence intervals
- Day 66 Hypothesis testing — t-test, chi-square
- Day 67 p-values, effect size, multiple testing
- Day 68 Correlation vs. causation, confounders
- Day 69 `scipy.stats` hands-on
- Day 70 Week-11 review — write one-page "stats for marketing" cheat sheet

### Week 12 — A/B Testing end-to-end

- Day 71 Experiment design — hypothesis, metrics, guardrails
- Day 72 Sample size and power calculation
- Day 73 Simulate an A/B test on marketing data
- Day 74 Analyze results, segment analysis
- Day 75 Common mistakes — peeking, Simpson's paradox, novelty effects
- Day 76 Write 2-page A/B test case study as a business memo
- Day 77 Month 3 wrap

**Portfolio Project 3:** Power BI dashboard (published to Power BI Service) + A/B test case study as a 2-page PDF memo.

---

## MONTH 4 — Python Engineering + Cloud + Docker

**Theme:** Stop being a notebook kid. Become someone who ships software.

### Week 13 — Python as an engineer writes it

- Day 78 Project structure — `src/`, `tests/`, `pyproject.toml`, virtual envs with uv or poetry
- Day 79 Type hints, `mypy`, docstrings
- Day 80 `ruff` for linting and formatting
- Day 81 `pytest` basics — fixtures, parametrize, assertions
- Day 82 Test the utility functions from Project 1
- Day 83 Refactor Project 1 into a proper installable package
- Day 84 Week-13 review

### Week 14 — Docker + CI

- Day 85 Docker concepts, install, first container
- Day 86 Dockerfile for a Python app, multi-stage builds
- Day 87 docker-compose for multi-service setups
- Day 88 GitHub Actions — run tests on push
- Day 89 GitHub Actions — lint + type-check on PR
- Day 90 Containerize Project 1, push image to GHCR
- Day 91 Week-14 review

### Week 15 — Azure fundamentals

- Day 92 Azure free account, portal tour
- Day 93 Microsoft Learn AZ-900 fundamentals — modules 1–3
- Day 94 AZ-900 modules 4–6
- Day 95 Azure Blob Storage — upload/download with Python SDK
- Day 96 Azure SQL Database — provision, connect
- Day 97 Azure Data Factory overview — one simple copy pipeline
- Day 98 Week-15 review

### Week 16 — End-to-end ETL pipeline

- Day 99 Pull from a public marketing API (e.g., ad platform sandbox)
- Day 100 Land raw data in Azure Blob
- Day 101 Transform with Python in a container
- Day 102 Load to Azure SQL or Snowflake
- Day 103 dbt transforms on top
- Day 104 Power BI dashboard reads from the final layer
- Day 105 Month 4 wrap — diagram the whole pipeline in the README

**Portfolio Project 4:** Containerized ETL pipeline with CI — API → Blob → Python → SQL/Snowflake → dbt → Power BI. This is the project that gets you past the ATS filter.

---

## MONTH 5 — LLMs, RAG & AI Marketing (the differentiator)

**Theme:** The "AI" in "AI Marketing" stops being aspirational. This month puts you in a different candidate pool.

### Week 17 — LLM API basics

- Day 106 Claude API + OpenAI API — first calls
- Day 107 Prompt engineering — zero-shot, few-shot, chain-of-thought
- Day 108 Structured outputs (JSON mode, tool use)
- Day 109 Function calling basics
- Day 110 Build LLM-powered text classifier for marketing copy
- Day 111 Cost tracking, rate limits, error handling
- Day 112 Week-17 review

### Week 18 — Embeddings + vector databases

- Day 113 What embeddings are, intuition and math lite
- Day 114 `sentence-transformers` hands-on
- Day 115 Chroma (local, free) — store and query embeddings
- Day 116 Qdrant alternative, trade-offs
- Day 117 Semantic search over a marketing document corpus
- Day 118 Evaluate retrieval quality (recall@k)
- Day 119 Week-18 review

### Week 19 — Build a RAG system end-to-end

- Day 120 Architecture — ingest, chunk, embed, retrieve, generate
- Day 121 Chunking strategies — fixed, semantic, recursive
- Day 122 Build ingestion pipeline for marketing PDFs
- Day 123 Build retrieval + generation loop with LangChain or LlamaIndex
- Day 124 Citations, source grounding, hallucination reduction
- Day 125 Evaluation — RAGAS or custom eval set
- Day 126 Week-19 review

### Week 20 — AI agents + deployment

- Day 127 Agent concepts — tools, planning, reflection
- Day 128 Pick one framework — LangGraph, Claude Agents SDK, or OpenAI Agents
- Day 129 Build agent that queries your Snowflake warehouse via SQL tool
- Day 130 Add a second tool — RAG retrieval over marketing docs
- Day 131 Streamlit or Gradio UI
- Day 132 Containerize, deploy locally, write demo video script
- Day 133 Month 5 wrap

**Portfolio Project 5:** "Marketing Copilot" — RAG over a marketing knowledge base + an agent that can pull campaign performance from your data warehouse and draft campaign briefs. Streamlit UI, Docker container, demo video. **This project alone gets interviews.**

---

## MONTH 6 — Applied ML + Polish + Job Hunt

**Theme:** Close remaining gaps, ship portfolio, start applying.

### Week 21 — Applied ML for marketing

- Day 134 scikit-learn basics — train/test split, fit/predict
- Day 135 Customer segmentation with k-means
- Day 136 Churn prediction — logistic regression
- Day 137 Churn prediction — random forest, feature importance
- Day 138 Model evaluation — precision, recall, ROC-AUC, confusion matrix
- Day 139 Marketing mix modeling intro (conceptual, one notebook)
- Day 140 Week-21 review

### Week 22 — MLOps lite

- Day 141 MLflow — experiment tracking
- Day 142 MLflow — model registry, versioning
- Day 143 FastAPI — serve a model as an API
- Day 144 Containerize the API, add tests
- Day 145 Connect Power BI to the API for live predictions
- Day 146 Week-22 review
- Day 147 Polish Project 6 README

### Week 23 — Portfolio + CV + LinkedIn polish

- Day 148 Rewrite all 6 project READMEs with the same template (problem, stack, architecture diagram, results, how to run)
- Day 149 GitHub profile README, pinned repos strategy
- Day 150 German CV (Lebenslauf) — tabular, photo, DOB, signed
- Day 151 English CV tailored for 3 target role types
- Day 152 LinkedIn profile overhaul — headline, about, skills, projects
- Day 153 Write 3 LinkedIn posts about projects (start building presence)
- Day 154 Week-23 review

### Week 24 — Interview prep + start applying

- Day 155 SQL live coding practice — StrataScratch / DataLemur
- Day 156 Power BI / DAX interview questions
- Day 157 Case study practice — "how would you measure the success of campaign X?"
- Day 158 System design lite — "design a data pipeline for a marketing team"
- Day 159 Behavioral — STAR answers for top 10 questions, one project elevator pitch
- Day 160 Apply to 10 roles this day (don't wait to be "ready")
- Day 161 Apply to 10 more, then keep a weekly applications cadence

**Portfolio Project 6:** Churn prediction model deployed as FastAPI + Docker, called from Power BI. Glues everything together.

---

## Parallel tracks (run from Month 2 onward)

**German language.** 30 min/day. Duolingo + one real class per week (italki, Lingoda, or a VHS class). Target: A2 by end of Month 3, B1 by end of Month 6. Takes the Mittelstand from "no" to "maybe."

**AI-augmented workflow (mandatory).** Every task: draft with Cursor/Claude Code, audit, refactor, test. Document the audit in commit messages. Example commit: *"Refactor ingestion — AI used deprecated pandas.append, replaced with pd.concat; added test for empty input edge case."* Interview gold.

**Daily commit cadence.** Keep your existing habit. Each day's work lands on its branch.

**Weekly review (every Sunday, 30 min).** What shipped? What slipped? Adjust the week ahead. Keep a running `LEARNINGS.md` in the repo.

---

## What you have at the end (portfolio snapshot for recruiters)

1. **OOH Campaign Analysis** — Python + Pandas + Plotly (Month 1)
2. **OOH Analytics Engineering** — SQL + Snowflake/BigQuery + dbt, star schema, tests, docs (Month 2)
3. **OOH Executive Dashboard + A/B Test Case Study** — Power BI + statistics memo (Month 3)
4. **End-to-End ETL Pipeline** — Docker + Azure + GitHub Actions + dbt + Power BI (Month 4)
5. **Marketing Copilot** — RAG + agent + Streamlit + Docker (Month 5) ← **the differentiator**
6. **Churn Prediction API** — scikit-learn + MLflow + FastAPI + Docker + Power BI (Month 6)

Six projects, each one keyword-dense, each one with a clean README, each one proving a different slice of the stack German employers filter for.

---

## GitHub branch strategy (simpler than the v1 plan)

Stop creating a branch per month — it over-engineers the workflow for a solo learner.

Instead:
- `main` — working, stable code at all times
- One branch per project: `project-2-dbt-ooh`, `project-5-marketing-copilot`, etc.
- Merge into `main` when the project is shippable, with a tag: `v2.0-project-2-complete`

This looks more like how real teams work and is what a recruiter wants to see.

---

## Risks and kill switches

If you fall behind: **cut ML first (Month 6 Week 21).** RAG and dbt matter more for your target roles.

If you get ahead: **deepen Project 5 (Marketing Copilot)** — add evaluation dashboards, multi-agent orchestration, or fine-tune a small model. This is the project that compounds.

If a project stalls for more than 3 days: **ship what you have, document the limitation, move on.** A shipped project with known gaps beats an unshipped perfect one.

---

## First action after reading this

Finish Day 25 (GROUP BY / HAVING) today as planned. Tomorrow, Day 26 (JOINs). From Day 29 onward, switch to the new plan — that's where the expansion starts (CTEs, window functions, then dbt).

Also: sign up for a free Snowflake trial or BigQuery sandbox account this week, so you're ready when Week 7 starts.

---

## Hybrid Plan v3 (2 Hours/Day) — Printable Weekly Checklist

Use this section as your execution tracker.

- Print this section and tick each box daily.
- Weekly structure:
	- Mon-Fri: 90 min build + 30 min German.
	- Sat: interview drills + networking + German speaking.
	- Sun: weekly review + planning + buffer.
- KPI target from Month 4 onward: 5 quality applications/week.

### Week 1

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat (drills + outreach + German speaking)
- [ ] Sun (review + planning)
- Focus: SQL fundamentals reset (WHERE, GROUP BY, JOINs, subqueries)

### Week 2

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: CTEs, window functions, SQL timed drills

### Week 3

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: warehouse setup, schema draft, KPI query layer

### Week 4

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: dbt setup, staging + marts + tests + docs

### Week 5

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: Project A hardening (tests, naming, quality checks)

### Week 6

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: Project A README + final QA + publish prep

### Week 7

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: publish Project A, start Power BI foundation

### Week 8

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: Power BI model + DAX basics + dashboard v1

### Week 9

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: dashboard storytelling and business flow

### Week 10

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: advanced DAX + Project B memo + README

### Week 11

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: stats + A/B testing basics for interviews

### Week 12

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: CV v1 + LinkedIn update + target company list

### Week 13

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: Project C scope + real doc ingestion pipeline

### Week 14

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: retrieval + generation + citation controls

### Week 15

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: Project C interface + evaluation + demo prep

### Week 16

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: publish Project C + begin active applications

### Week 17

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: interview bank + SQL/case drill cycle

### Week 18

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: mock interviews + STAR story refinement

### Week 19

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: GitHub polish + LinkedIn project content

### Week 20

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: targeted applications + company-specific prep

### Week 21

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: SQL and DAX weakness elimination

### Week 22

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: full mock loop + communication fixes

### Week 23

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: project deep dives + behavioral depth

### Week 24

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: Month 6 checkpoint (interviewable)

### Week 25

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: Project D ETL architecture + extraction

### Week 26

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: ETL transforms + tests + Docker

### Week 27

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: CI + data quality + reliability

### Week 28

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: Project D publish + interview narrative

### Week 29

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: advanced interview drills + gap closure

### Week 30

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: optional FastAPI mini add-on

### Week 31

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: external mock + feedback implementation

### Week 32

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: company-specific prep sheets + interview tuning

### Week 33

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: active pipeline conversion sprint

### Week 34

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: final technical refresh + follow-up cadence

### Week 35

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: assignment quality and final-round readiness

### Week 36

- [ ] Mon
- [ ] Tue
- [ ] Wed
- [ ] Thu
- [ ] Fri
- [ ] Sat
- [ ] Sun
- Focus: offer conversion + next 90-day plan

---

## Weekly KPI Card (Print 36 copies)

Week #: ________

- [ ] Hours completed (target 14): ________
- [ ] Build output shipped (1 minimum): __________________________
- [ ] SQL/DAX/case drills completed: ________
- [ ] Applications sent (target from Month 4: 5): ________
- [ ] Networking messages sent (target 5): ________
- [ ] German speaking sessions (target 2): ________
- [ ] Biggest blocker identified
- [ ] Next week's top 3 priorities defined

## Kill-Switch Checks (Sunday)

- [ ] If behind 2 weeks: run recovery week (no new scope)
- [ ] If response rate is low 3 weeks: tighten role targeting and CV messaging
- [ ] If overloaded: cut optional FastAPI work first
- [ ] Protect quality of Projects A, B, C before anything else
