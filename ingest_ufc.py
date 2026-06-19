"""Ingest UFC all-time statistical leaders from statleaders.ufc.com into the RAG knowledge base."""
import httpx

BASE = "http://localhost:8000/api/v1/documents/ingest/text"

FACTS = [
    {
        "source": "statleaders.ufc.com",
        "topic": "UFC All-Time Leaders — Total Fights and Wins",
        "content": (
            "UFC all-time leaders in total fights and wins (data as of June 7, 2026): "
            "Most total fights: 1st Jim Miller (47 fights), 2nd Andrei Arlovski (42 fights), "
            "3rd Donald Cerrone (38 fights), 4th tied Clay Guida / Charles Oliveira / Neil Magny (37 fights each). "
            "Most wins in UFC history: 1st Jim Miller (28 wins), 2nd Charles Oliveira (25 wins), "
            "3rd Neil Magny (24 wins), 4th tied Andrei Arlovski / Donald Cerrone / Max Holloway (23 wins each). "
            "Jim Miller holds both the record for most UFC fights (47) and most UFC wins (28). "
            "Charles Oliveira ranks 2nd in wins (25) and is tied 4th in total fights (37). "
            "Max Holloway has 23 UFC wins despite competing primarily as a featherweight."
        ),
    },
    {
        "source": "statleaders.ufc.com",
        "topic": "UFC All-Time Leaders — Fight Finishes, KO/TKO, and Submissions",
        "content": (
            "UFC all-time leaders in fight finishes, knockouts, and submissions (data as of June 7, 2026): "
            "Most fight finishes: 1st Charles Oliveira (21 finishes), 2nd Jim Miller (20 finishes), "
            "3rd tied Donald Cerrone / Derrick Lewis (16 finishes each). "
            "Most KO/TKO wins: 1st Derrick Lewis (16 KO/TKO), 2nd Matt Brown (13 KO/TKO), "
            "3rd multiple fighters tied at 11 KO/TKO wins. "
            "Most submission wins: 1st Charles Oliveira (17 submissions), 2nd Jim Miller (14 submissions), "
            "3rd tied Demian Maia / Gerald Meerschaert (11 submissions each). "
            "Most decision wins: 1st tied Brad Tavares / Neil Magny (14 decision wins each). "
            "Charles Oliveira leads in both total finishes (21) and submission wins (17), making him the most prolific finisher in UFC history. "
            "Derrick Lewis is the all-time UFC KO/TKO leader with 16 knockout victories."
        ),
    },
    {
        "source": "statleaders.ufc.com",
        "topic": "UFC All-Time Leaders — Win Streaks and Title Fight Victories",
        "content": (
            "UFC all-time leaders in win streaks and title fight victories (data as of June 7, 2026): "
            "Longest win streaks in UFC history: "
            "1st tied Anderson Silva and Islam Makhachev — both with 16-fight win streaks. "
            "3rd Kamaru Usman with a 15-fight win streak. "
            "Anderson Silva's 16-fight win streak was built across his legendary middleweight title reign (2006–2012). "
            "Islam Makhachev matched Silva's record with his 16-fight win streak in the lightweight division. "
            "Most title fight victories: 1st Jon Jones (16 title fight wins), 2nd Georges St-Pierre (13 title fight wins), "
            "3rd Demetrious Johnson (12 title fight wins). "
            "Jon Jones holds the all-time UFC record for most title fight victories with 16, across both light heavyweight and heavyweight divisions. "
            "Georges St-Pierre won 13 title fights across his welterweight and middleweight reigns. "
            "Demetrious Johnson won 12 title fights during his record-setting flyweight championship reign."
        ),
    },
    {
        "source": "statleaders.ufc.com",
        "topic": "UFC All-Time Leaders — Fight Night Bonuses",
        "content": (
            "UFC all-time leaders in Fight Night bonuses (Performance of the Night, Fight of the Night) as of June 7, 2026: "
            "1st Charles Oliveira: 21 bonuses — the most in UFC history. "
            "2nd Donald Cerrone: 18 bonuses. "
            "3rd Justin Gaethje: 17 bonuses. "
            "Charles Oliveira's 21 bonuses reflect his reputation as one of the most exciting finishers in the sport. "
            "Donald Cerrone earned 18 bonuses across his long UFC career, consistent with his fan-friendly fighting style. "
            "Justin Gaethje earned 17 bonuses, driven by his high-output, aggressive striking style. "
            "Fight Night bonuses include Performance of the Night (given to the best finish) and Fight of the Night (given to both fighters in the best overall fight)."
        ),
    },
    {
        "source": "statleaders.ufc.com",
        "topic": "UFC All-Time Leaders — Total Fight Time",
        "content": (
            "UFC all-time leaders in total fight time and average fight duration (data as of June 7, 2026): "
            "Most total time spent fighting in the UFC: "
            "1st Max Holloway: 8 hours 52 minutes 43 seconds. "
            "2nd Rafael Dos Anjos: 8 hours 43 minutes 19 seconds. "
            "3rd Frankie Edgar: 7 hours 57 minutes 10 seconds. "
            "Shortest average fight duration (most finishing ability): "
            "1st Terrance McKinney: 2 minutes 16 seconds average. "
            "2nd Tom Aspinall: 2 minutes 18 seconds average. "
            "3rd Drew McFedries: 2 minutes 20 seconds average. "
            "Longest average fight duration (most championship-style longevity): "
            "1st Valentina Shevchenko: 19 minutes 4 seconds average. "
            "2nd Joanna Jedrzejczyk: 18 minutes 37 seconds average. "
            "3rd Demetrious Johnson: 18 minutes 34 seconds average. "
            "Max Holloway has spent the most total time in the octagon of any UFC fighter. "
            "Valentina Shevchenko's average fight time of over 19 minutes reflects her dominant championship-level performances."
        ),
    },
    {
        "source": "statleaders.ufc.com",
        "topic": "UFC All-Time Leaders — Significant Strikes",
        "content": (
            "UFC all-time leaders in significant strikes landed and strike accuracy (data as of June 7, 2026): "
            "Most significant strikes landed in UFC history: "
            "1st Max Holloway: 3,681 significant strikes landed. "
            "2nd Sean Strickland: 2,430 significant strikes landed. "
            "3rd Angela Hill: 2,364 significant strikes landed. "
            "Best significant strike accuracy (minimum 5 fights): "
            "1st Alistair Overeem: 74.3% strike accuracy. "
            "2nd Shara Magomedov: 63.0% strike accuracy. "
            "3rd Ciryl Gane: 61.7% strike accuracy. "
            "Max Holloway holds the all-time UFC record for significant strikes landed with 3,681, more than 1,200 ahead of second place. "
            "This record is built on his extremely high output across 23 UFC wins. "
            "Alistair Overeem's 74.3% significant strike accuracy is the highest in UFC history among qualified fighters. "
            "Angela Hill is the all-time leader in significant strikes among women's UFC fighters with 2,364."
        ),
    },
    {
        "source": "statleaders.ufc.com",
        "topic": "UFC All-Time Leaders — Knockdowns",
        "content": (
            "UFC all-time leaders in knockdowns scored (data as of June 7, 2026): "
            "Most knockdowns scored in UFC history: "
            "1st Donald Cerrone: 20 knockdowns. "
            "2nd tied Anderson Silva / Jeremy Stephens: 18 knockdowns each. "
            "Donald Cerrone holds the UFC all-time record for most knockdowns scored with 20, reflecting his well-rounded striking across 38 UFC fights. "
            "Anderson Silva scored 18 knockdowns, largely during his 16-fight win streak as UFC Middleweight Champion. "
            "Jeremy Stephens scored 18 knockdowns in the featherweight and lightweight divisions. "
            "A knockdown is recorded when a fighter drops to the canvas as a result of legal strikes."
        ),
    },
    {
        "source": "statleaders.ufc.com",
        "topic": "UFC All-Time Leaders — Takedowns and Grappling",
        "content": (
            "UFC all-time leaders in takedowns and grappling control (data as of June 7, 2026): "
            "Most takedowns landed in UFC history: "
            "1st Merab Dvalishvili: 119 takedowns landed. "
            "2nd Georges St-Pierre: 90 takedowns landed. "
            "3rd Gleison Tibau: 84 takedowns landed. "
            "Best takedown accuracy (minimum 5 fights, 20 attempts): "
            "1st Nordine Taleb: 76.2% takedown accuracy. "
            "2nd Taila Santos: 75.0% takedown accuracy. "
            "3rd Robbie Lawler: 73.9% takedown accuracy. "
            "Best takedown defense (minimum 5 fights, 20 opponent attempts): "
            "1st Julio Arce: 96.2% takedown defense. "
            "2nd Ilia Topuria: 95.2% takedown defense. "
            "3rd Jon Jones: 95.0% takedown defense. "
            "Merab Dvalishvili leads all UFC fighters with 119 takedowns landed — more than 29 ahead of second place Georges St-Pierre (90). "
            "Ilia Topuria has the 2nd-best takedown defense in UFC history at 95.2%, underlining his elite wrestling defense."
        ),
    },
    {
        "source": "statleaders.ufc.com",
        "topic": "UFC All-Time Leaders — Control Time",
        "content": (
            "UFC all-time leaders in control time and control time percentage (data as of June 7, 2026): "
            "Most total control time in UFC history: "
            "1st Georges St-Pierre: 2 hours 42 minutes 4 seconds of control time. "
            "2nd Clay Guida: 2 hours 36 minutes 28 seconds of control time. "
            "3rd Demian Maia: 2 hours 35 minutes 20 seconds of control time. "
            "Best control time percentage (minimum 5 fights): "
            "1st Bartosz Fabinski: 79.1% control time percentage. "
            "2nd Gregor Gillespie: 71.9% control time percentage. "
            "3rd Pat Sabatini: 71.0% control time percentage. "
            "Georges St-Pierre leads all UFC fighters with over 2 hours and 42 minutes of total ground control, reflecting his dominant wrestling-based game plan across his welterweight and middleweight career. "
            "Demian Maia is 3rd in total control time, consistent with his world-class Brazilian jiu-jitsu and ground-control style."
        ),
    },
    {
        "source": "statleaders.ufc.com",
        "topic": "UFC All-Time Leaders — Submission Attempts",
        "content": (
            "UFC all-time leaders in submission attempts (data as of June 7, 2026): "
            "Most submission attempts in UFC history: "
            "1st Jim Miller: 52 submission attempts. "
            "2nd Charles Oliveira: 51 submission attempts. "
            "3rd Chris Lytle: 31 submission attempts. "
            "Most submission attempts per 15 minutes (rate leaders): "
            "1st Paul Sass: 7.38 attempts per 15 minutes. "
            "2nd John Albert: 6.14 attempts per 15 minutes. "
            "3rd TJ Waldburger: 4.79 attempts per 15 minutes. "
            "Jim Miller leads UFC history with 52 submission attempts across his record 47 UFC fights. "
            "Charles Oliveira is second with 51 submission attempts — and has the highest conversion rate, having finished 17 of them. "
            "Paul Sass holds the most active submission-hunting rate in UFC history at 7.38 attempts per 15 minutes of fight time."
        ),
    },
]


def main():
    print("Ingesting UFC all-time statistical leaders from statleaders.ufc.com...\n")
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
    print('  • "Who has the most wins in UFC history?"')
    print('  • "Who is the all-time UFC KO/TKO leader?"')
    print('  • "Who has the longest win streak in the UFC?"')
    print('  • "How many title fight wins does Jon Jones have?"')
    print('  • "Who has the most significant strikes landed in UFC history?"')
    print('  • "Who leads the UFC in takedowns?"')
    print('  • "Which fighter has the most submission wins in the UFC?"')
    print('  • "Who has spent the most total time fighting in the UFC?"')


if __name__ == "__main__":
    main()
