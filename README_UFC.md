# UFC Dataset — RAG Knowledge Base

This dataset populates the RAG knowledge base with **UFC all-time statistical leaders** sourced directly from [statleaders.ufc.com](https://statleaders.ufc.com/) (data as of June 7, 2026). Once ingested, you can ask natural-language questions and Claude will answer using only the ingested material.

## What the script ingests

Running `python ingest_ufc.py` loads **10 text chunks** into the FAISS vector index, covering every major statistical category tracked by UFC:

| # | Topic |
|---|---|
| 1 | Total fights and wins leaders — Jim Miller (47 fights, 28 wins), Oliveira, Cerrone |
| 2 | Fight finishes, KO/TKO, and submission leaders — Lewis (16 KOs), Oliveira (17 subs) |
| 3 | Win streaks and title fight victories — Jones (16 title wins), Silva & Makhachev (16-fight streaks) |
| 4 | Fight Night bonuses — Oliveira (21), Cerrone (18), Gaethje (17) |
| 5 | Total fight time — Holloway (8h 52m), Dos Anjos, Edgar; fastest/slowest averages |
| 6 | Significant strikes landed — Holloway (3,681), Strickland (2,430); accuracy leaders |
| 7 | Knockdowns — Cerrone (20), Silva & Stephens (18 each) |
| 8 | Takedowns and grappling — Dvalishvili (119 TDs), GSP (90); accuracy and defense leaders |
| 9 | Control time — GSP (2h 42m), Guida, Maia; control percentage leaders |
| 10 | Submission attempts — Miller (52), Oliveira (51); attempts-per-15-min rate leaders |

## How it works

Each chunk is embedded locally using `all-MiniLM-L6-v2` and stored in a FAISS index. When you submit a query, the API retrieves the most semantically similar chunks and passes them as context to Claude, which generates a grounded answer — it will not invent statistics beyond what was ingested.

## Quick start

Make sure the server is running, then ingest:

```bash
# Start the server (if not already running)
uvicorn app.main:app --reload

# Load the UFC dataset
python ingest_ufc.py
```

## Sample queries

Try these in the Swagger UI at `http://localhost:8000/docs` or via `curl`:

```bash
curl -X POST http://localhost:8000/api/v1/query/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Who has the most wins in UFC history?", "include_sources": true}'
```

### Wins and Fight Totals
- "Who has the most wins in UFC history?"
- "Who has fought the most times in the UFC?"
- "How many UFC fights has Jim Miller had?"
- "Who has the most UFC wins among active fighters?"
- "How many wins does Charles Oliveira have in the UFC?"
- "Who has the most decision wins in the UFC?"

### Finishes — KO/TKO and Submissions
- "Who is the all-time UFC KO/TKO leader?"
- "How many knockouts does Derrick Lewis have in the UFC?"
- "Who has the most submission wins in UFC history?"
- "Who has the most total fight finishes in the UFC?"
- "How many submissions does Charles Oliveira have?"
- "Who has the most submission attempts in UFC history?"
- "Who attempts the most submissions per 15 minutes?"

### Win Streaks and Title Fights
- "Who has the longest win streak in the UFC?"
- "How many fights did Anderson Silva win in a row?"
- "Did Islam Makhachev match Anderson Silva's win streak?"
- "Who has the most title fight victories in UFC history?"
- "How many title fight wins does Jon Jones have?"
- "How many title fights did Georges St-Pierre win?"
- "What is Kamaru Usman's UFC win streak?"

### Striking
- "Who has the most significant strikes landed in UFC history?"
- "How many significant strikes has Max Holloway landed?"
- "Who has the best strike accuracy in the UFC?"
- "Who has scored the most knockdowns in UFC history?"
- "How many knockdowns does Donald Cerrone have?"
- "Which female fighter has the most significant strikes in UFC history?"

### Grappling and Takedowns
- "Who has landed the most takedowns in the UFC?"
- "How many takedowns does Merab Dvalishvili have?"
- "Who has the best takedown accuracy in UFC history?"
- "Who has the best takedown defense in the UFC?"
- "What is Ilia Topuria's takedown defense percentage?"
- "Who has the most control time in the UFC?"
- "How much control time does Georges St-Pierre have?"
- "Who has the highest control time percentage?"

### Fight Time
- "Who has spent the most time fighting in the UFC?"
- "How long has Max Holloway spent in the octagon?"
- "Which fighter has the shortest average fight time?"
- "Which fighter has the longest average fight duration?"
- "What is Valentina Shevchenko's average fight time?"

### Bonuses
- "Who has the most Fight Night bonuses in UFC history?"
- "How many performance bonuses does Charles Oliveira have?"
- "Who has the second-most bonuses in UFC history?"

## Data coverage

| Attribute | Detail |
|---|---|
| Source | statleaders.ufc.com (official UFC stats) |
| Data as of | June 7, 2026 |
| Categories | Fights, wins, finishes, KO/TKO, submissions, decisions, win streaks, title fights, bonuses, fight time, striking, knockdowns, takedowns, control time, submission attempts |
| Qualifications | Rate stats (accuracy, control %) require minimum 5 fights and/or 20 attempts |
| Coverage | All-time UFC leaders across all weight classes and eras |
