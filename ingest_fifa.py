"""Ingest FIFA World Cup stats (last 10 tournaments, 1990-2022) into the RAG knowledge base."""
import httpx

BASE = "http://localhost:8000/api/v1/documents/ingest/text"

FACTS = [
    {
        "source": "wikipedia.org/wiki/FIFA_World_Cup_records_and_statistics",
        "topic": "FIFA World Cup — Last 10 Tournaments Overview (1990–2022)",
        "content": (
            "Summary of the last 10 FIFA World Cups (1990–2022): "
            "1990 Italy: Winner West Germany, Runner-up Argentina, Host Italy. "
            "1994 USA: Winner Brazil, Runner-up Italy, Host United States. "
            "1998 France: Winner France, Runner-up Brazil, Host France. "
            "2002 South Korea/Japan: Winner Brazil, Runner-up Germany, co-hosted by South Korea and Japan. "
            "2006 Germany: Winner Italy, Runner-up France, Host Germany. "
            "2010 South Africa: Winner Spain, Runner-up Netherlands, Host South Africa — first World Cup held in Africa. "
            "2014 Brazil: Winner Germany, Runner-up Argentina, Host Brazil. "
            "2018 Russia: Winner France, Runner-up Croatia, Host Russia. "
            "2022 Qatar: Winner Argentina, Runner-up France, Host Qatar — first World Cup in the Middle East. "
            "All 10 tournaments used 24 teams (1990, 1994) or 32 teams (1998–2022). "
            "The 2026 World Cup (USA/Mexico/Canada) will expand to 48 teams."
        ),
    },
    {
        "source": "wikipedia.org/wiki/1990_FIFA_World_Cup",
        "topic": "1990 FIFA World Cup — Italy",
        "content": (
            "The 1990 FIFA World Cup was held in Italy from June 8 to July 8, 1990. "
            "24 teams participated, playing 52 matches. "
            "West Germany won the tournament, defeating Argentina 1-0 in the final in Rome. "
            "The winning goal was scored by Andreas Brehme from the penalty spot in the 85th minute. "
            "Argentina finished as runners-up and Italy finished third. "
            "Golden Boot (top scorer): Salvatore Schillaci (Italy) with 6 goals. "
            "Golden Ball (best player): Salvatore Schillaci (Italy). "
            "Golden Glove (best goalkeeper): Sergio Goycochea (Argentina). "
            "Total goals scored: 115 goals in 52 matches (2.21 goals per game — the lowest average in World Cup history at the time). "
            "Total attendance: 2,516,215 across all matches. "
            "The 1990 World Cup is remembered for its defensive, low-scoring matches. "
            "It was West Germany's third World Cup title (after 1954 and 1974). "
            "Franz Beckenbauer became the first man to win the World Cup as both a player (1974) and a coach (1990). "
            "Cameroon reached the quarterfinals, the best result by an African team at the time. "
            "Roger Milla of Cameroon, aged 38, became the oldest scorer in World Cup history at that point."
        ),
    },
    {
        "source": "wikipedia.org/wiki/1994_FIFA_World_Cup",
        "topic": "1994 FIFA World Cup — United States",
        "content": (
            "The 1994 FIFA World Cup was held in the United States from June 17 to July 17, 1994. "
            "24 teams participated, playing 52 matches. "
            "Brazil won the tournament, defeating Italy on penalty kicks (3-2) after a 0-0 draw in the final at the Rose Bowl, Pasadena. "
            "It was the first World Cup final decided by penalty shootout. "
            "Roberto Baggio missed Italy's final penalty, sealing Brazil's victory. "
            "Italy finished as runners-up and Sweden finished third. "
            "Golden Boot (top scorer): Hristo Stoichkov (Bulgaria) and Oleg Salenko (Russia) with 6 goals each. "
            "Oleg Salenko set a single-match record by scoring 5 goals against Cameroon. "
            "Golden Ball (best player): Romário (Brazil). "
            "Total goals scored: 141 goals in 52 matches (2.71 goals per game). "
            "Total attendance: 3,587,538 — the highest total attendance in World Cup history. "
            "It was Brazil's fourth World Cup title (1958, 1962, 1970, 1994). "
            "Bulgaria reached the semifinals — their best-ever World Cup finish. "
            "Hristo Stoichkov was the star of the tournament for Bulgaria. "
            "Romania and Saudi Arabia also had notable performances, both advancing from the group stage."
        ),
    },
    {
        "source": "wikipedia.org/wiki/1998_FIFA_World_Cup",
        "topic": "1998 FIFA World Cup — France",
        "content": (
            "The 1998 FIFA World Cup was held in France from June 10 to July 12, 1998. "
            "32 teams participated for the first time, playing 64 matches. "
            "France won the tournament, defeating Brazil 3-0 in the final at Stade de France, Saint-Denis. "
            "Zinedine Zidane scored two headers and Emmanuel Petit added a third. "
            "Brazil finished as runners-up and Croatia finished third in their first-ever World Cup appearance. "
            "Golden Boot (top scorer): Davor Šuker (Croatia) with 6 goals. "
            "Golden Ball (best player): Ronaldo (Brazil). "
            "Ronaldo suffered a mysterious illness or seizure the night before the final, yet still played. "
            "Total goals scored: 171 goals in 64 matches (2.67 goals per game). "
            "Total attendance: 2,785,100. "
            "It was France's first World Cup title. "
            "The tournament expanded from 24 to 32 teams. "
            "Argentina's Gabriel Batistuta scored hat-tricks and was a top performer. "
            "Dennis Bergkamp's last-minute goal for Netherlands vs Argentina in the quarterfinals is considered one of the greatest goals in World Cup history."
        ),
    },
    {
        "source": "wikipedia.org/wiki/2002_FIFA_World_Cup",
        "topic": "2002 FIFA World Cup — South Korea and Japan",
        "content": (
            "The 2002 FIFA World Cup was co-hosted by South Korea and Japan from May 31 to June 30, 2002. "
            "32 teams participated, playing 64 matches. "
            "Brazil won the tournament, defeating Germany 2-0 in the final in Yokohama, Japan. "
            "Ronaldo scored both goals in the final. "
            "Germany finished as runners-up and Turkey finished third. "
            "Golden Boot (top scorer): Ronaldo (Brazil) with 8 goals — the most goals scored by any player in a single World Cup tournament (tied record). "
            "Golden Ball (best player): Oliver Kahn (Germany, goalkeeper — the only goalkeeper to win this award). "
            "Total goals scored: 161 goals in 64 matches (2.52 goals per game). "
            "Total attendance: 2,705,197. "
            "It was Brazil's fifth and most recent World Cup title. "
            "It was the first World Cup held in Asia and the first co-hosted tournament. "
            "South Korea reached the semifinals — the best result by an Asian team in World Cup history. "
            "Hakan Şükür (Turkey) scored after just 11 seconds vs South Korea — the fastest goal in World Cup history. "
            "Senegal reached the quarterfinals on their debut, beating defending champion France in the group stage."
        ),
    },
    {
        "source": "wikipedia.org/wiki/2006_FIFA_World_Cup",
        "topic": "2006 FIFA World Cup — Germany",
        "content": (
            "The 2006 FIFA World Cup was held in Germany from June 9 to July 9, 2006. "
            "32 teams participated, playing 64 matches. "
            "Italy won the tournament, defeating France on penalty kicks (5-3) after a 1-1 draw in the final in Berlin. "
            "Zinedine Zidane was sent off in extra time for headbutting Marco Materazzi in his final career match. "
            "France finished as runners-up and Germany finished third (as host). "
            "Golden Boot (top scorer): Miroslav Klose (Germany) with 5 goals. "
            "Golden Ball (best player): Zinedine Zidane (France) — awarded despite his red card. "
            "Golden Glove (best goalkeeper): Gianluigi Buffon (Italy). "
            "Total goals scored: 147 goals in 64 matches (2.30 goals per game). "
            "Total attendance: 3,353,655. "
            "It was Italy's fourth World Cup title (1934, 1938, 1982, 2006). "
            "The tournament was nicknamed 'The Summer Fairy Tale' in Germany for its festive atmosphere. "
            "The referee Horacio Elizondo sent off Zidane in his 200th and final professional match. "
            "Miroslav Klose became Germany's all-time World Cup top scorer at the tournament."
        ),
    },
    {
        "source": "wikipedia.org/wiki/2010_FIFA_World_Cup",
        "topic": "2010 FIFA World Cup — South Africa",
        "content": (
            "The 2010 FIFA World Cup was held in South Africa from June 11 to July 11, 2010. "
            "32 teams participated, playing 64 matches. "
            "Spain won the tournament, defeating Netherlands 1-0 after extra time in the final in Johannesburg. "
            "Andrés Iniesta scored the winning goal in the 116th minute of extra time. "
            "Netherlands finished as runners-up and Germany finished third. "
            "Golden Boot (top scorer): Four players tied with 5 goals each — David Villa (Spain), Wesley Sneijder (Netherlands), Diego Forlán (Uruguay), Thomas Müller (Germany). Villa won on assists tiebreaker. "
            "Golden Ball (best player): Diego Forlán (Uruguay). "
            "Golden Glove (best goalkeeper): Iker Casillas (Spain). "
            "Best Young Player: Thomas Müller (Germany). "
            "Total goals scored: 145 goals in 64 matches (2.27 goals per game). "
            "Total attendance: 3,178,856. "
            "It was Spain's first World Cup title and the first won by a European team outside of Europe. "
            "It was the first World Cup held in Africa. "
            "The vuvuzela horn became iconic at this tournament. "
            "USA, Ghana, and South Korea also had notable runs. "
            "Defending champion Italy was eliminated in the group stage."
        ),
    },
    {
        "source": "wikipedia.org/wiki/2014_FIFA_World_Cup",
        "topic": "2014 FIFA World Cup — Brazil",
        "content": (
            "The 2014 FIFA World Cup was held in Brazil from June 12 to July 13, 2014. "
            "32 teams participated, playing 64 matches. "
            "Germany won the tournament, defeating Argentina 1-0 after extra time in the final at Maracanã, Rio de Janeiro. "
            "Mario Götze scored the winning goal in the 113th minute. "
            "Argentina finished as runners-up and Netherlands finished third. "
            "Golden Boot (top scorer): James Rodríguez (Colombia) with 6 goals. "
            "Golden Ball (best player): Lionel Messi (Argentina). "
            "Golden Glove (best goalkeeper): Manuel Neuer (Germany). "
            "Best Young Player: Paul Pogba (France). "
            "Total goals scored: 171 goals in 64 matches (2.67 goals per game). "
            "Total attendance: 3,386,810. "
            "It was Germany's fourth World Cup title (1954, 1974, 1990, 2014). "
            "The semifinal 'Mineirazo' or 'Sete a Um': Germany defeated host Brazil 7-1 — the biggest semifinal defeat in World Cup history. "
            "Germany scored five goals in 18 minutes (24th–29th minute) in that semifinal. "
            "Miroslav Klose scored his 16th World Cup goal in the Brazil match, becoming the all-time leading scorer in World Cup history, surpassing Ronaldo's record of 15. "
            "Colombia's James Rodríguez scored a stunning volley against Uruguay, voted best goal of the tournament. "
            "Neymar was injured (fractured vertebra) in the quarterfinals, missing the rest of the tournament for Brazil."
        ),
    },
    {
        "source": "wikipedia.org/wiki/2018_FIFA_World_Cup",
        "topic": "2018 FIFA World Cup — Russia",
        "content": (
            "The 2018 FIFA World Cup was held in Russia from June 14 to July 15, 2018. "
            "32 teams participated, playing 64 matches. "
            "France won the tournament, defeating Croatia 4-2 in the final in Moscow. "
            "The final featured two own goals, a penalty, and a long-range strike by Pogba. "
            "Croatia finished as runners-up (their best-ever finish) and Belgium finished third. "
            "Golden Boot (top scorer): Harry Kane (England) with 6 goals, including three from penalties. "
            "Golden Ball (best player): Luka Modrić (Croatia). "
            "Golden Glove (best goalkeeper): Thibaut Courtois (Belgium). "
            "Best Young Player: Kylian Mbappé (France). "
            "Total goals scored: 169 goals in 64 matches (2.64 goals per game). "
            "Total attendance: 3,031,768. "
            "It was France's second World Cup title (1998 and 2018). "
            "Kylian Mbappé, aged 19, became the second teenager to score in a World Cup final (after Pelé in 1958). "
            "VAR (Video Assistant Referee) was used for the first time in a World Cup. "
            "Belgium's 3-2 comeback win over Japan from 0-2 down is one of the greatest upsets. "
            "Germany, the defending champion, was eliminated in the group stage — only the second time a defending champion failed to advance (after France in 2002). "
            "England reached the semifinals for the first time since 1990. "
            "Luka Modrić became the first player from outside Brazil, Germany, Argentina, or France to win the Golden Ball since 2002."
        ),
    },
    {
        "source": "wikipedia.org/wiki/2022_FIFA_World_Cup",
        "topic": "2022 FIFA World Cup — Qatar",
        "content": (
            "The 2022 FIFA World Cup was held in Qatar from November 20 to December 18, 2022. "
            "32 teams participated, playing 64 matches. "
            "Argentina won the tournament, defeating France 3-3 (4-2 on penalties) in the final at Lusail Stadium, Lusail. "
            "The final is widely considered the greatest World Cup final in history. "
            "France finished as runners-up and Croatia finished third. Morocco finished fourth — the best-ever result by an African or Arab nation. "
            "Golden Boot (top scorer): Kylian Mbappé (France) with 8 goals — equaling Ronaldo's single-tournament record set in 2002. Mbappé scored a hat-trick in the final. "
            "Golden Ball (best player): Lionel Messi (Argentina) — Messi's second Golden Ball (also won in 2014). "
            "Golden Glove (best goalkeeper): Emiliano Martínez (Argentina). "
            "Best Young Player: Enzo Fernández (Argentina). "
            "Total goals scored: 172 goals in 64 matches (2.69 goals per game — highest ever for a 32-team tournament). "
            "Total attendance: 3,404,252. "
            "It was Argentina's third World Cup title (1978, 1986, 2022) and Lionel Messi's first. "
            "It was the first World Cup held in the Middle East and the first played in northern hemisphere winter. "
            "The tournament was held in a compact host country requiring little travel between venues. "
            "Morocco beat Spain and Portugal to become the first African team to reach the semifinals. "
            "Lionel Messi scored 7 goals and 3 assists, totaling 10 direct goal contributions — the most in a single World Cup. "
            "Lautaro Martínez scored the winning penalty in the final shootout. "
            "Saudi Arabia beat Argentina 2-1 in the group stage in one of the biggest upsets in World Cup history. "
            "Japan also beat Germany and Spain in the group stage, advancing past both European giants."
        ),
    },
    {
        "source": "wikipedia.org/wiki/FIFA_World_Cup_records_and_statistics",
        "topic": "FIFA World Cup — All-Time Individual Scoring Records",
        "content": (
            "All-time FIFA World Cup individual scoring records: "
            "Most goals in World Cup history: Miroslav Klose (Germany) with 16 goals across 4 tournaments (2002: 5, 2006: 5, 2010: 4, 2014: 2). He surpassed Ronaldo's record of 15 in 2014. "
            "Most goals in a single tournament: Ronaldo (Brazil) in 2002 with 8 goals and Kylian Mbappé (France) in 2022 with 8 goals — both share the record. "
            "Most goals in a single match: Oleg Salenko (Russia) scored 5 goals vs Cameroon in 1994 — the most goals by one player in a single World Cup match. "
            "Fastest goal: Hakan Şükür (Turkey) scored after 11 seconds vs South Korea in the 2002 third-place match — the fastest goal in World Cup history. "
            "Other top all-time scorers: Ronaldo (Brazil) 15 goals, Gerd Müller (West Germany) 14 goals, Just Fontaine (France) 13 goals — all scored in one tournament in 1958, Pelé (Brazil) 12 goals. "
            "Most World Cup appearances (matches played): Lothar Matthäus (Germany) with 25 matches. "
            "Most World Cups played: Antonio Carbajal (Mexico, 1950–1966) and Lothar Matthäus (Germany, 1982–1998) — each appeared in 5 World Cups. "
            "Most assists in a single tournament: Lionel Messi (Argentina) with 3 assists in 2022 (also scored 7 goals for 10 direct contributions). "
            "Only goalkeeper to win Golden Ball: Oliver Kahn (Germany), 2002."
        ),
    },
    {
        "source": "wikipedia.org/wiki/FIFA_World_Cup_records_and_statistics",
        "topic": "FIFA World Cup — All-Time Team Records and Country Titles",
        "content": (
            "All-time FIFA World Cup team records and titles by country: "
            "Most World Cup titles: Brazil 5 (1958, 1962, 1970, 1994, 2002). "
            "Germany 4 titles (1954, 1974, 1990, 2014). "
            "Italy 4 titles (1934, 1938, 1982, 2006). "
            "Argentina 3 titles (1978, 1986, 2022). "
            "France 2 titles (1998, 2018). "
            "Uruguay 2 titles (1930, 1950). England 1 title (1966). Spain 1 title (2010). "
            "Brazil is the only country to have qualified for every World Cup (all 22 tournaments through 2022). "
            "Germany has the most runner-up finishes with 4 (1966, 1982, 1986, 2002). "
            "Brazil has scored the most total goals in World Cup history (229 through 2022). "
            "Biggest victory: Hungary 10-1 El Salvador (1982 group stage). "
            "Most goals in a single match: Austria 7-5 Switzerland (1954) — 12 total goals, the highest-scoring World Cup match ever. "
            "Germany's 7-1 win over Brazil in the 2014 semifinal (the Mineirazo) is the largest margin of victory in a World Cup semifinal. "
            "Spain won the 2010 World Cup without conceding more than 1 goal in any knockout match. "
            "France in 2018 became only the third team to win the World Cup with players from that nation born abroad (diversity of squad). "
            "The Netherlands have been runners-up 3 times (1974, 1978, 2010) without winning the title. "
            "Host nations have won the World Cup 6 times: Uruguay 1930, Italy 1934, England 1966, West Germany 1974, Argentina 1978, France 1998."
        ),
    },
    {
        "source": "wikipedia.org/wiki/FIFA_World_Cup_records_and_statistics",
        "topic": "FIFA World Cup — Notable Records and Milestones",
        "content": (
            "Notable FIFA World Cup records and milestones: "
            "Highest attendance tournament: 1994 USA with 3,587,538 total spectators across 52 matches. "
            "Highest single-match attendance: 199,854 at Maracanã, Rio de Janeiro — Brazil vs Uruguay, 1950 (unofficial final). "
            "First World Cup final decided by penalties: 1994 (Brazil vs Italy). "
            "Youngest scorer: Pelé (Brazil) at 17 years and 239 days vs Wales in 1958 quarterfinal. "
            "Oldest scorer: Roger Milla (Cameroon) at 42 years and 39 days vs Russia in 1994. "
            "Most red cards in a tournament: 2006 Germany (28 yellow cards and 4 red cards in 64 matches). "
            "Longest unbeaten run: Brazil went 13 matches unbeaten from 1958 to 1966. "
            "First World Cup in Africa: 2010 South Africa. First in Asia: 2002 South Korea/Japan. First in Middle East: 2022 Qatar. "
            "First World Cup to use VAR (Video Assistant Referee): 2018 Russia. "
            "Kylian Mbappé (France, 2018) and Pelé (Brazil, 1958) are the only teenagers to score in a World Cup final. "
            "Zinedine Zidane is the only player to score in two World Cup finals (1998 and 2006). "
            "Ronaldo (Brazil) scored in the 1998 and 2002 finals, and Kylian Mbappé (France) scored in the 2018 and 2022 finals. "
            "The 2026 FIFA World Cup will be hosted by the United States, Canada, and Mexico, featuring 48 teams for the first time."
        ),
    },
]


def main():
    print("Ingesting FIFA World Cup stats (last 10 tournaments, 1990–2022)...\n")
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
    print('  • "Who won the 2022 FIFA World Cup?"')
    print('  • "Who is the all-time top scorer in World Cup history?"')
    print('  • "Which country has won the most World Cups?"')
    print('  • "What happened in the 2014 semifinal between Germany and Brazil?"')
    print('  • "Who won the Golden Boot in 2018?"')
    print('  • "What is the fastest goal ever scored in a World Cup?"')
    print('  • "How many goals did Kylian Mbappé score in the 2022 World Cup final?"')
    print('  • "Which was the first World Cup held in Africa?"')


if __name__ == "__main__":
    main()
