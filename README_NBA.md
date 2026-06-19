# NBA Dataset — RAG Knowledge Base

This dataset populates the RAG knowledge base with detailed **2026 NBA Playoff** data sourced from basketball-reference.com and nba.com. Once ingested, you can ask natural-language questions and Claude will answer using only the ingested material.

## What the script ingests

Running `python ingest_nba.py` loads **11 text chunks** into the FAISS vector index, covering:

| # | Topic |
|---|---|
| 1 | 2026 Playoff statistical leaders (points, rebounds, assists, win shares) |
| 2 | NBA Finals MVP — Jalen Brunson (45 points in Game 5, historic 4th-quarter stats) |
| 3 | NBA Finals — Knicks vs Spurs, game-by-game scores, viewership record |
| 4 | Western Conference Finals — Spurs vs Thunder (7 games) |
| 5 | Eastern Conference Finals — Knicks vs Cavaliers (sweep) |
| 6 | Eastern Conference Semifinals — Knicks vs 76ers, Cavaliers vs Pistons |
| 7 | Western Conference Semifinals — Thunder vs Lakers, Spurs vs Timberwolves |
| 8 | Eastern Conference First Round — all four series with game scores |
| 9 | Western Conference First Round — all four series with game scores |
| 10 | Team offensive stats per game for all playoff teams |
| 11 | Team defensive stats and advanced metrics (offensive/defensive/net rating, pace) |

## How it works

Each chunk is embedded locally using `all-MiniLM-L6-v2` and stored in a FAISS index. When you submit a query, the API retrieves the most semantically similar chunks and passes them as context to Claude, which generates a grounded answer — it will not invent statistics beyond what was ingested.

## Quick start

Make sure the server is running, then ingest:

```bash
# Start the server (if not already running)
uvicorn app.main:app --reload

# Load the NBA dataset
python ingest_nba.py
```

## Sample queries

Try these in the Swagger UI at `http://localhost:8000/docs` or via `curl`:

```bash
curl -X POST http://localhost:8000/api/v1/query/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Who won the 2026 NBA Championship?", "include_sources": true}'
```

### Championship and Finals
- "Who won the 2026 NBA Championship?"
- "Who was the 2026 NBA Finals MVP?"
- "What were the scores in every game of the 2026 NBA Finals?"
- "How many points did Jalen Brunson score in Game 5 of the 2026 Finals?"
- "How many viewers watched the 2026 NBA Finals?"
- "What was historic about OG Anunoby's tip-in in Game 4?"

### Conference Playoffs
- "How did the Knicks do in the Eastern Conference Finals?"
- "What happened in Game 7 of the Western Conference Finals?"
- "Who won the Western Conference Finals and in how many games?"
- "Did the Cavaliers win their first-round series against the Raptors?"
- "Who did the Thunder beat in the first round and by what scores?"
- "What was Shai Gilgeous-Alexander's Game 7 score in the WCF?"

### Individual Stats
- "Who led the 2026 playoffs in scoring?"
- "Who had the most rebounds in the 2026 playoffs?"
- "Who was the assists leader in the 2026 NBA Playoffs?"
- "How many win shares did OG Anunoby have?"
- "Who won the Western Conference Finals MVP?"

### Team Stats
- "What was the Knicks' offensive rating in the 2026 playoffs?"
- "Which team had the best net rating in the 2026 playoffs?"
- "How many games did the Spurs play in the 2026 playoffs?"
- "What was the league average PPG in the 2026 playoffs?"
- "Which team had the most blocks per game?"

### Historical Context
- "When was the last time the Knicks won a championship before 2026?"
- "What record did Brunson's 4th-quarter performance match from Michael Jordan?"
- "Which other players have won an NCAA title, Naismith Award, NBA title, and Finals MVP?"

## Data coverage

| Attribute | Detail |
|---|---|
| Season | 2026 NBA Playoffs |
| Sources | basketball-reference.com, nba.com |
| Teams covered | All 16 playoff teams |
| Rounds | First round through NBA Finals |
| Stats | Points, rebounds, assists, steals, blocks, FG%, 3P%, net rating, pace |
