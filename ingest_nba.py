"""Ingest 2026 NBA Playoff facts from basketball-reference.com into the RAG knowledge base."""
import httpx

BASE = "http://localhost:8000/api/v1/documents/ingest/text"

FACTS = [
    {
        "source": "basketball-reference.com",
        "topic": "2026 NBA Playoff Leaders",
        "content": (
            "2026 NBA Playoff statistical leaders: "
            "Points leader: Victor Wembanyama (San Antonio Spurs) with 505 total points. "
            "Rebounds leader: Victor Wembanyama (San Antonio Spurs) with 225 total rebounds. "
            "Assists leader: Stephon Castle (San Antonio Spurs) with 137 total assists. "
            "Win Shares leader: OG Anunoby (New York Knicks) with 3.7 win shares."
        ),
    },
    {
        "source": "nba.com",
        "topic": "2026 NBA Finals MVP — Jalen Brunson",
        "content": (
            "Jalen Brunson of the New York Knicks won the 2026 NBA Finals MVP award. "
            "Brunson scored 45 points in Game 5 to clinch the championship, including 15 points in the 4th quarter. "
            "His 4th-quarter performance matched Michael Jordan (Game 6, 1998) for the most points in a Finals-clinching win since play-by-play data was first tracked in 1997. "
            "Brunson averaged 9.9 4th-quarter points throughout the 2026 postseason — best by a champion since Dirk Nowitzki in 2011. "
            "With the Finals MVP, Brunson joined an elite group of players with an NCAA title, Naismith Player of the Year award, NBA championship, and Finals MVP: Bill Walton, Kareem Abdul-Jabbar, and Michael Jordan. "
            "Brunson was the clear winner of the 2026 NBA Finals MVP. "
            "The Finals MVP for the 2026 NBA Championship was Jalen Brunson."
        ),
    },
    {
        "source": "nba.com",
        "topic": "2026 NBA Finals — Knicks win championship",
        "content": (
            "The New York Knicks won the 2026 NBA Championship, defeating the San Antonio Spurs in the Finals. "
            "The Knicks won the series 4-1, clinching the title in Game 5 on Saturday June 13, 2026. "
            "The Knicks championship parade was held on June 18, 2026 in New York City. "
            "It was the Knicks' first championship in 53 years, since 1973. "
            "Jalen Brunson won the 2026 NBA Finals MVP award. "
            "Game-by-game scores: "
            "Game 1 (June 3): Knicks 105, Spurs 95 (Knicks win, in San Antonio). "
            "Game 2 (June 5): Knicks 105, Spurs 104 (Knicks win, in San Antonio). "
            "Game 3 (June 8): Spurs 115, Knicks 111 (Spurs win, in New York). "
            "Game 4 (June 10): Knicks 107, Spurs 106 (Knicks win, in New York — OG Anunoby tip-in in greatest comeback in Finals history). "
            "Game 5 (June 13): Knicks 112, Spurs 108 (Knicks win, clinch championship — Brunson 45 pts). "
            "The Knicks-Spurs Finals was the most-watched NBA Finals in 28 years, averaging 20.6M viewers per game."
        ),
    },
    {
        "source": "basketball-reference.com",
        "topic": "2026 Western Conference Finals — Spurs vs Thunder",
        "content": (
            "The San Antonio Spurs defeated the Oklahoma City Thunder 4-3 in the 2026 Western Conference Finals. "
            "Game-by-game scores: "
            "Game 1 (May 18): Spurs 122, Thunder 115 (in Oklahoma City — Spurs win). "
            "Game 2 (May 20): Thunder 122, Spurs 113 (in Oklahoma City — Thunder win). "
            "Game 3 (May 22): Thunder 123, Spurs 108 (in San Antonio — Thunder win). "
            "Game 4 (May 24): Spurs 103, Thunder 82 (in San Antonio — Spurs win). "
            "Game 5 (May 26): Thunder 127, Spurs 114 (in Oklahoma City — Thunder win). "
            "Game 6 (May 28): Spurs 118, Thunder 91 (in San Antonio — Spurs win). "
            "Game 7 (May 30): Spurs 111, Thunder 103 (in Oklahoma City — Spurs win). "
            "Victor Wembanyama was named Western Conference Finals MVP. "
            "Shai Gilgeous-Alexander scored 35 points in Game 7 for Oklahoma City but it was not enough."
        ),
    },
    {
        "source": "basketball-reference.com",
        "topic": "2026 Eastern Conference Finals — Knicks vs Cavaliers",
        "content": (
            "The New York Knicks swept the Cleveland Cavaliers 4-0 in the 2026 Eastern Conference Finals. "
            "Game-by-game scores: "
            "Game 1 (May 19): Cavaliers 104, Knicks 115 (in New York — Knicks win). "
            "Game 2 (May 21): Cavaliers 93, Knicks 109 (in New York — Knicks win). "
            "Game 3 (May 23): Knicks 121, Cavaliers 108 (in Cleveland — Knicks win). "
            "Game 4 (May 25): Knicks 130, Cavaliers 93 (in Cleveland — Knicks win, sweep)."
        ),
    },
    {
        "source": "basketball-reference.com",
        "topic": "2026 Eastern Conference Semifinals",
        "content": (
            "Eastern Conference Semifinals results in the 2026 NBA Playoffs: "
            "New York Knicks defeated Philadelphia 76ers 4-0 (sweep). Scores: "
            "Game 1: 76ers 98, Knicks 137. Game 2: 76ers 102, Knicks 108. "
            "Game 3: Knicks 108, 76ers 94. Game 4: Knicks 144, 76ers 114. "
            "Cleveland Cavaliers defeated Detroit Pistons 4-3. Scores: "
            "Game 1: Cavaliers 101, Pistons 111. Game 2: Cavaliers 97, Pistons 107. "
            "Game 3: Pistons 109, Cavaliers 116. Game 4: Pistons 103, Cavaliers 112. "
            "Game 5: Cavaliers 117, Pistons 113. Game 6: Pistons 115, Cavaliers 94. "
            "Game 7: Cavaliers 125, Pistons 94."
        ),
    },
    {
        "source": "basketball-reference.com",
        "topic": "2026 Western Conference Semifinals",
        "content": (
            "Western Conference Semifinals results in the 2026 NBA Playoffs: "
            "Oklahoma City Thunder defeated Los Angeles Lakers 4-0 (sweep). Scores: "
            "Game 1: Lakers 90, Thunder 108. Game 2: Lakers 107, Thunder 125. "
            "Game 3: Thunder 131, Lakers 108. Game 4: Thunder 115, Lakers 110. "
            "San Antonio Spurs defeated Minnesota Timberwolves 4-2. Scores: "
            "Game 1: Timberwolves 104, Spurs 102. Game 2: Timberwolves 95, Spurs 133. "
            "Game 3: Spurs 115, Timberwolves 108. Game 4: Spurs 109, Timberwolves 114. "
            "Game 5: Timberwolves 97, Spurs 126. Game 6: Spurs 139, Timberwolves 109."
        ),
    },
    {
        "source": "basketball-reference.com",
        "topic": "2026 Eastern Conference First Round",
        "content": (
            "Eastern Conference First Round results in the 2026 NBA Playoffs: "
            "New York Knicks defeated Atlanta Hawks 4-2. Scores: "
            "Game 1: Hawks 102, Knicks 113. Game 2: Hawks 107, Knicks 106 (Hawks win). "
            "Game 3: Knicks 108, Hawks 109 (Hawks win). Game 4: Knicks 114, Hawks 98. "
            "Game 5: Hawks 97, Knicks 126. Game 6: Knicks 140, Hawks 89. "
            "The Knicks trailed the series 1-2 before winning three straight. "
            "Philadelphia 76ers upset Boston Celtics 4-3. Scores: "
            "Game 1: 76ers 91, Celtics 123. Game 2: 76ers 111, Celtics 97. "
            "Game 3: Celtics 108, 76ers 100. Game 4: Celtics 128, 76ers 96. "
            "Game 5: 76ers 113, Celtics 97. Game 6: Celtics 93, 76ers 106. "
            "Game 7: 76ers 109, Celtics 100. "
            "Cleveland Cavaliers defeated Toronto Raptors 4-3. Scores: "
            "Game 1: Raptors 113, Cavaliers 126. Game 2: Raptors 105, Cavaliers 115. "
            "Game 3: Cavaliers 104, Raptors 126. Game 4: Cavaliers 89, Raptors 93. "
            "Game 5: Raptors 120, Cavaliers 125. Game 6: Cavaliers 110, Raptors 112. "
            "Game 7: Raptors 102, Cavaliers 114. "
            "Detroit Pistons defeated Orlando Magic 4-3. Scores: "
            "Game 1: Magic 112, Pistons 101. Game 2: Magic 83, Pistons 98. "
            "Game 3: Pistons 105, Magic 113. Game 4: Pistons 88, Magic 94. "
            "Game 5: Magic 109, Pistons 116. Game 6: Pistons 93, Magic 79. "
            "Game 7: Magic 94, Pistons 116."
        ),
    },
    {
        "source": "basketball-reference.com",
        "topic": "2026 Western Conference First Round",
        "content": (
            "Western Conference First Round results in the 2026 NBA Playoffs: "
            "Oklahoma City Thunder defeated Phoenix Suns 4-0 (sweep). Scores: "
            "Game 1: Suns 84, Thunder 119. Game 2: Suns 107, Thunder 120. "
            "Game 3: Thunder 121, Suns 109. Game 4: Thunder 131, Suns 122. "
            "San Antonio Spurs defeated Portland Trail Blazers 4-1. Scores: "
            "Game 1: Blazers 98, Spurs 111. Game 2: Blazers 106, Spurs 103 (Blazers win). "
            "Game 3: Spurs 120, Blazers 108. Game 4: Spurs 114, Blazers 93. "
            "Game 5: Blazers 95, Spurs 114. "
            "Los Angeles Lakers defeated Houston Rockets 4-2. Scores: "
            "Game 1: Rockets 98, Lakers 107. Game 2: Rockets 94, Lakers 101. "
            "Game 3: Lakers 112, Rockets 108. Game 4: Lakers 96, Rockets 115 (Rockets win). "
            "Game 5: Rockets 99, Lakers 93 (Rockets win). Game 6: Lakers 98, Rockets 78. "
            "Minnesota Timberwolves defeated Denver Nuggets 4-2. Scores: "
            "Game 1: Timberwolves 105, Nuggets 116 (Nuggets win). "
            "Game 2: Timberwolves 119, Nuggets 114. "
            "Game 3: Nuggets 96, Timberwolves 113. Game 4: Nuggets 96, Timberwolves 112. "
            "Game 5: Timberwolves 113, Nuggets 125 (Nuggets win). "
            "Game 6: Nuggets 98, Timberwolves 110."
        ),
    },
    {
        "source": "basketball-reference.com",
        "topic": "2026 NBA Playoffs team offensive stats per game",
        "content": (
            "2026 NBA Playoffs per-game offensive stats by team: "
            "New York Knicks (18 games): 117.1 PPG, 44.9 RPG, 25.8 APG, 8.6 SPG, 4.3 BPG, FG% .497, 3P% .395. "
            "Oklahoma City Thunder (15 games): 115.5 PPG, 41.7 RPG, 25.9 APG, 10.2 SPG, 4.6 BPG, FG% .470, 3P% .365. "
            "San Antonio Spurs (22 games): 113.4 PPG, 46.6 RPG, 24.6 APG, 8.5 SPG, 7.0 BPG, FG% .461, 3P% .361. "
            "Cleveland Cavaliers (18 games): 107.9 PPG, 40.9 RPG, 21.7 APG, 7.9 SPG, 5.1 BPG, FG% .456, 3P% .328. "
            "Detroit Pistons (14 games): 104.9 PPG, 43.9 RPG, 22.4 APG, 8.7 SPG, 7.3 BPG, FG% .448, 3P% .359. "
            "Minnesota Timberwolves (12 games): 108.3 PPG, 45.5 RPG, 23.3 APG, FG% .437, 3P% .337. "
            "Philadelphia 76ers (11 games): 103.1 PPG, FG% .447, 3P% .338. "
            "Los Angeles Lakers (10 games): 102.2 PPG, FG% .472, 3P% .385. "
            "The league average was 108.1 PPG, FG% .453, 3P% .348."
        ),
    },
    {
        "source": "basketball-reference.com",
        "topic": "2026 NBA Playoffs team defensive stats and advanced metrics",
        "content": (
            "2026 NBA Playoffs advanced team stats: "
            "New York Knicks: Offensive Rating 121.5, Defensive Rating 105.4, Net Rating +16.1, Pace 95.8. Best net rating of any team. "
            "San Antonio Spurs: Offensive Rating 115.1, Defensive Rating 106.9, Net Rating +8.2, Pace 97.6. "
            "Oklahoma City Thunder: Offensive Rating 119.3, Defensive Rating 112.0, Net Rating +7.3, Pace 95.5. "
            "Detroit Pistons: Offensive Rating 110.7, Defensive Rating 109.0, Net Rating +1.7. "
            "Boston Celtics: Offensive Rating 113.7, Defensive Rating 110.7, Net Rating +3.0. "
            "Cleveland Cavaliers: Offensive Rating 111.5, Defensive Rating 114.7, Net Rating -3.2. "
            "The Knicks had the highest offensive rating (121.5) and best net rating (+16.1) of all 16 playoff teams. "
            "The Spurs allowed opponents 105.4 points per 100 possessions (opponents offensive rating), one of the best defenses in the playoffs. "
            "Knicks defensive rating: 105.4 (best in playoffs). "
            "Spurs played the most games (22) of any team in the 2026 playoffs."
        ),
    },
]


def main():
    print("Ingesting 2026 NBA Playoff facts from basketball-reference.com...\n")
    total_chunks = 0
    for i, fact in enumerate(FACTS, 1):
        resp = httpx.post(BASE, json={
            "content": fact["content"],
            "source": fact["source"],
            "metadata": {"topic": fact["topic"]},
        }, timeout=30)
        if resp.status_code == 201:
            data = resp.json()
            total_chunks += data["chunk_count"]
            print(f"[{i}/{len(FACTS)}] ✓  {fact['topic']} → {data['chunk_count']} chunk(s)")
        else:
            print(f"[{i}/{len(FACTS)}] ✗  {fact['topic']} — {resp.status_code}: {resp.text}")

    print(f"\nDone! {total_chunks} total chunks ingested.")
    print("\nTry these queries in the Swagger UI at http://localhost:8000/docs:")
    print('  • "Who won the 2026 NBA Championship?"')
    print('  • "Who was the playoff scoring leader?"')
    print('  • "What were the scores in the Western Conference Finals Game 7?"')
    print('  • "How did the Knicks do in the first round?"')
    print('  • "What is the Knicks offensive rating in the playoffs?"')
    print('  • "Who did the Thunder beat in the first round and by what scores?"')


if __name__ == "__main__":
    main()
