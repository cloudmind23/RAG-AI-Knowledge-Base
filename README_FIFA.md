# FIFA World Cup Dataset — RAG Knowledge Base

This dataset populates the RAG knowledge base with detailed **FIFA World Cup** statistics covering the **last 10 tournaments (1990–2022)** plus all-time records, sourced from Wikipedia's FIFA World Cup records and statistics page. Once ingested, you can ask natural-language questions and Claude will answer using only the ingested material.

## What the script ingests

Running `python ingest_fifa.py` loads **13 text chunks** into the FAISS vector index, covering:

| # | Topic |
|---|---|
| 1 | Overview of all 10 tournaments — winner, host, runner-up at a glance |
| 2 | **1990 Italy** — West Germany wins, Schillaci Golden Boot, Cameroon's historic run |
| 3 | **1994 USA** — Brazil wins on penalties, record attendance (3.58M), Salenko's 5-goal game |
| 4 | **1998 France** — France's first title, expansion to 32 teams, Zidane's two headers |
| 5 | **2002 South Korea/Japan** — Brazil's 5th title, Ronaldo's 8 goals, Şükür's 11-second goal |
| 6 | **2006 Germany** — Italy wins, Zidane headbutt in final, Klose's rise |
| 7 | **2010 South Africa** — Spain wins, Iniesta's extra-time goal, first WC in Africa |
| 8 | **2014 Brazil** — Germany wins, Mineirazo 7-1, Klose breaks all-time scoring record |
| 9 | **2018 Russia** — France wins, VAR debut, Mbappé becomes 2nd teenager to score in final |
| 10 | **2022 Qatar** — Argentina wins "greatest final ever," Mbappé's 8 goals, Morocco's historic run |
| 11 | All-time individual scoring records — Klose (16 goals), Salenko, Şükür, Pelé, Ronaldo |
| 12 | All-time team records — titles by country, biggest wins, host nation victories |
| 13 | Notable milestones — youngest/oldest scorers, attendance records, VAR, 2026 preview |

## How it works

Each chunk is embedded locally using `all-MiniLM-L6-v2` and stored in a FAISS index. When you submit a query, the API retrieves the most semantically similar chunks and passes them as context to Claude, which generates a grounded answer — it will not invent statistics beyond what was ingested.

## Quick start

Make sure the server is running, then ingest:

```bash
# Start the server (if not already running)
uvicorn app.main:app --reload

# Load the FIFA dataset
python ingest_fifa.py
```

## Sample queries

Try these in the Swagger UI at `http://localhost:8000/docs` or via `curl`:

```bash
curl -X POST http://localhost:8000/api/v1/query/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Who won the 2022 FIFA World Cup?", "include_sources": true}'
```

### Tournament Winners
- "Who won the 2022 FIFA World Cup?"
- "Who won the 2018 World Cup and who did they beat in the final?"
- "Which country won the 2010 World Cup and how?"
- "How did Germany win the 2014 World Cup?"
- "Who were the runner-up and third place in the 1998 World Cup?"

### Golden Boot and Golden Ball
- "Who won the Golden Boot in 2022?"
- "Who won the Golden Ball in the 2018 World Cup?"
- "How many goals did Kylian Mbappé score in the 2022 World Cup final?"
- "Who was the top scorer in the 2014 World Cup?"
- "Which goalkeeper won the Golden Ball award?"

### All-Time Records
- "Who is the all-time top scorer in World Cup history?"
- "How many World Cup goals did Miroslav Klose score?"
- "What is the fastest goal ever scored in a World Cup?"
- "Who scored 5 goals in a single World Cup match?"
- "Which country has won the most World Cups?"
- "How many titles does Brazil have in the World Cup?"
- "Who has played in the most World Cup matches?"

### Tournament Facts and History
- "What happened in the 2014 semifinal between Germany and Brazil?"
- "What is the Mineirazo?"
- "Which was the first World Cup held in Africa?"
- "Which was the first World Cup in Asia?"
- "When was VAR first used in a World Cup?"
- "What is the highest-scoring match in World Cup history?"
- "What is the biggest victory margin in a World Cup match?"
- "Who was the youngest player to score in a World Cup final?"

### Country and Team Records
- "Which teams have been World Cup runners-up without winning the title?"
- "How many times has Germany won the World Cup?"
- "Which African team had the best result in a World Cup?"
- "Has a host country ever won the World Cup?"
- "What was Morocco's achievement in the 2022 World Cup?"

### Player Highlights
- "How many goals did Ronaldo score in the 2002 World Cup?"
- "What happened to Zinedine Zidane in the 2006 World Cup final?"
- "What did Pelé achieve in the 1958 World Cup?"
- "Who scored the winning goal for Spain in the 2010 World Cup final?"
- "How many goals did Lionel Messi score in the 2022 World Cup?"

## Data coverage

| Attribute | Detail |
|---|---|
| Tournaments | 10 World Cups: 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022 |
| Source | Wikipedia — FIFA World Cup records and statistics |
| Per-tournament stats | Winner, runner-up, third place, Golden Boot, Golden Ball, goals, matches, attendance, teams |
| All-time records | Top scorers, most appearances, fastest goal, biggest wins, titles by country |
| Individual tournaments | Key match results, scorers, upsets, and historic moments for each edition |
