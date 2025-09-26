1. top run scorers per season

select season, batsman, runs, rank from
(select m.season, d.batsman, d.batting_team as team, sum(d.runs_batsman) as runs, rank() over(partition by m.season order by sum(d.runs_batsman) desc) as rank
from matches m join deliveries d on d.match_id = m.match_id
group by m.season, d.batsman, d.batting_team) t
where rank = 1
order by season;


select season, batsman, runs, rank from
(select m.season, d.batsman, sum(d.runs_batsman) as runs, rank() over(partition by m.season order by sum(d.runs_batsman) desc) as rank
from matches m join deliveries d on d.match_id = m.match_id
group by m.season, d.batsman) t
where rank <= 5
order by season;

* highest runs scored in a season

select m.season, d.batsman, sum(d.runs_batsman) from matches m join deliveries d on d.match_id = m.match_id
group by m.season, d.batsman
order by sum(d.runs_total)
desc limit 25;

2. highest strike rate batsmen per season 

with batsman_stats as (
select m.season, d.batsman, d.batting_team as team, sum(d.runs_batsman) as runs, 
sum(case when d.extras_type in ('noballs', 'wides') then 0 else 1 end) as balls, 
round((sum(d.runs_batsman) * 100.0) / nullif(sum(case when d.extras_type in ('noballs', 'wides') then 0 else 1 end), 0), 1) as strike_rate
from matches m join deliveries d on d.match_id = m.match_id
group by m.season, d.batsman, d.batting_team
HAVING SUM(CASE WHEN d.extras_type IN ('noballs','wides') THEN 0 ELSE 1 END) > 200
)
select * from (
select *, rank() over(partition by season order by strike_rate desc) as rank from batsman_stats
) t
where rank <= 3
order by season, rank;



* all batsmen strike rate per season ordered high to low

ipl=> select m.season, d.batsman, sum(d.runs_batsman) as runs, sum(case when d.extras_type in ('noballs', 'wides') then 0 else 1 end) as balls, (sum(d.runs_batsman) * 100.0) / nullif(sum(case when d.extras_type in ('noballs', 'wides') then 0 else 1 end), 0) as strike_rate
ipl-> from matches m join deliveries d on d.match_id = m.match_id
group by m.season, d.batsman
HAVING SUM(CASE WHEN d.extras_type IN ('noballs','wides') THEN 0 ELSE 1 END) > 200
order by strike_rate desc;




3. top boundaries

**sixes**
ipl=> select season, batsman, fours from
ipl-> (select m.season, d.batsman, d.batting_team as team, sum(case when d.runs_batsman = 4 then 1 else 0 end) as fours, rank() over(partition by m.season order by sum(case when d.runs_batsman = 4 then 1 else 0 end) desc) as rank
ipl(> from matches m join deliveries d on d.match_id = m.match_id
ipl(> group by m.season, d.batsman, d.batting_team) t
ipl-> where rank = 1
ipl-> order by season desc;

**fours**
ipl=> select season, batsman, fours from
ipl-> (select m.season, d.batsman, d.batting_team as team, sum(case when d.runs_batsman = 4 then 1 else 0 end) as fours, rank() over(partition by m.season order by sum(case when d.runs_batsman = 4 then 1 else 0 end) desc) as rank
ipl(> from matches m join deliveries d on d.match_id = m.match_id
ipl(> group by m.season, d.batsman, d.batting_team) t
ipl-> where rank = 1
ipl-> order by season desc;



4. most runs in death overs

ipl=> select season, batsman, runs_death, rank from
ipl-> ( select m.season, d.batsman, d.batting_team as team, sum(d.runs_batsman) as runs_death, rank() over(partition by m.season order by sum(d.runs_batsman) desc) as rank
ipl(> from matches m join deliveries d on d.match_id = m.match_id
ipl(> where d.over between 16 and 20
ipl(> group by m.season, d.batsman, d.batting_team) t
ipl-> where rank = 1
ipl-> order by season desc;


5. top wickets

ipl=> select season, bowler, team, wickets from
ipl-> (select m.season, d.bowler, case when d.batting_team = m.team1 then m.team2 else m.team1 end as team, sum(case when d.wicket_kind in ('bowled', 'caught', 'caught and bowled', 'lbw', 'stumped') then 1 else 0 end) as wickets, rank() over(partition by m.season order by sum(case when d.wicket_kind in ('bowled', 'caught', 'caught and bowled', 'lbw', 'stumped') then 1 else 0 end) desc) as rank
ipl(> from matches m join deliveries d on d.match_id = m.match_id
ipl(> group by m.season, d.bowler, case when d.batting_team = m.team1 then m.team2 else m.team1 end) t
ipl-> where rank = 1
ipl-> order by season;

6. top wickets in death overs

ipl=> select season, bowler, team, wickets from
ipl-> (select m.season, d.bowler, case when d.batting_team = m.team1 then m.team2 else m.team1 end as team, sum(case when d.wicket_kind in ('bowled', 'caught', 'caught and bowled', 'lbw', 'stumped') then 1 else 0 end) as wickets, rank() over(partition by m.season order by sum(case when d.wicket_kind in ('bowled', 'caught', 'caught and bowled', 'lbw', 'stumped') then 1 else 0 end) desc) as rank
ipl(> from matches m join deliveries d on d.match_id = m.match_id
ipl(> where d.over between 16 and 20
ipl(> group by m.season, d.bowler, case when d.batting_team = m.team1 then m.team2 else m.team1 end) t
ipl-> where rank = 1
ipl-> order by season;


7. top all rounder

**normalising**

WITH batting AS (
    SELECT
        m.season,
        d.batsman AS player,
        SUM(d.runs_batsman) AS runs

    FROM matches m
    JOIN deliveries d ON d.match_id = m.match_id
    GROUP BY m.season, d.batsman
),
bowling AS (
    SELECT
        m.season,
        d.bowler AS player,
sum(case when d.wicket_kind in ('bowled', 'caught', 'caught and bowled', 'lbw', 'stumped') then 1 else 0 end) as wickets
FROM matches m
    JOIN deliveries d ON d.match_id = m.match_id
    GROUP BY m.season, d.bowler
),
combined AS (
    SELECT
        b.season,
        b.player,
        COALESCE(b.runs, 0) AS runs,
        COALESCE(w.wickets, 0) AS wickets
    FROM batting b
    FULL JOIN bowling w
    ON b.player = w.player AND b.season = w.season
),
normalized AS (
    SELECT
        season,
        player,
        runs,
        wickets,
        runs::float / NULLIF(MAX(runs) OVER (PARTITION BY season),0) +
        wickets::float / NULLIF(MAX(wickets) OVER (PARTITION BY season),0) AS allrounder_score
    FROM combined
)
select * from (
SELECT season, player, runs, wickets, allrounder_score,
       RANK() OVER (PARTITION BY season ORDER BY allrounder_score DESC) AS rnk
FROM normalized
ORDER BY season, rnk)
where runs > 0 and wickets > 0 and rnk = 1;


**standardised**

WITH batting AS (
    SELECT
        m.season,
        d.batsman AS player,
        SUM(d.runs_batsman) AS runs
    FROM matches m
    JOIN deliveries d ON d.match_id = m.match_id
    GROUP BY m.season, d.batsman
),
bowling AS (
    SELECT
        m.season,
        d.bowler AS player,
        SUM(CASE WHEN d.wicket_kind IN ('bowled','caught','caught and bowled','lbw','stumped') THEN 1 ELSE 0 END) AS wickets
    FROM matches m
    JOIN deliveries d ON d.match_id = m.match_id
    GROUP BY m.season, d.bowler
),
combined AS (
    SELECT
        b.season,
        b.player,
        COALESCE(b.runs, 0) AS runs,
        COALESCE(w.wickets, 0) AS wickets
    FROM batting b
    FULL JOIN bowling w
    ON b.player = w.player AND b.season = w.season
),
standardized AS (
    SELECT
        season,
        player,
        runs,
        wickets,
        -- z-scores for runs and wickets
        (runs - AVG(runs) OVER (PARTITION BY season)) / 
            NULLIF(STDDEV_POP(runs) OVER (PARTITION BY season),0) AS runs_z,
        (wickets - AVG(wickets) OVER (PARTITION BY season)) / 
            NULLIF(STDDEV_POP(wickets) OVER (PARTITION BY season),0) AS wickets_z
    FROM combined
)
SELECT *
FROM (
    SELECT
        season,
        player,
        runs,
        wickets,
        (runs_z + wickets_z) AS allrounder_score,
        RANK() OVER (PARTITION BY season ORDER BY (runs_z + wickets_z) DESC) AS rnk
    FROM standardized
) t
WHERE runs > 0 AND wickets > 0 AND rnk = 1
ORDER BY season;



10. **Chasing vs Defending:** Which teams are stronger when batting first vs chasing?


ipl=> WITH chasing AS (
ipl(>     SELECT
ipl(>         chasing_team AS team,
ipl(>         COUNT(*) AS times_chased,
ipl(>         COUNT(*) FILTER (WHERE chasing_team = winner) AS chasing_wins
ipl(>     FROM matches
ipl(>     GROUP BY chasing_team
ipl(> ),
ipl-> defending AS (
ipl(>     SELECT
ipl(>         defending_team AS team,
ipl(>         COUNT(*) AS times_defended,
ipl(>         COUNT(*) FILTER (WHERE defending_team = winner) AS defending_wins
ipl(>     FROM matches
ipl(>     GROUP BY defending_team
ipl(> )
ipl-> SELECT
ipl->     c.team,
ipl->     c.times_chased,
ipl->     c.chasing_wins,
ipl->     ROUND(100.0 * c.chasing_wins / NULLIF(c.times_chased, 0), 2) AS chasing_win_pct,
ipl->     d.times_defended,
ipl->     d.defending_wins,
ipl->     ROUND(100.0 * d.defending_wins / NULLIF(d.times_defended, 0), 2) AS defending_win_pct
ipl-> FROM chasing c
ipl-> JOIN defending d ON c.team = d.team
ipl-> ORDER BY chasing_win_pct DESC;




11. **Home Advantage:** Do teams win more at their home grounds? (needs venue matching)


ipl=> CREATE TABLE venue_mapping (
ipl(>     raw_name TEXT,
ipl(>     canonical_name TEXT
ipl(> );
CREATE TABLE
ipl=> INSERT INTO venue_mapping (raw_name, canonical_name) VALUES
ipl-> -- Chennai Super Kings
ipl-> ('MA Chidambaram Stadium', 'MA Chidambaram Stadium'),
ipl-> ('MA Chidambaram Stadium, Chepauk, Chennai', 'MA Chidambaram Stadium'),
ipl-> ('MA Chidambaram Stadium, Chepauk', 'MA Chidambaram Stadium'),
ipl->
ipl-> -- Mumbai Indians
ipl-> ('Wankhede Stadium', 'Wankhede Stadium'),
ipl-> ('Wankhede Stadium, Mumbai', 'Wankhede Stadium'),
ipl-> ('Brabourne Stadium', 'Wankhede Stadium'),
ipl-> ('Brabourne Stadium, Mumbai', 'Wankhede Stadium'),
ipl-> ('Dr DY Patil Sports Academy, Mumbai', 'Wankhede Stadium'),
ipl->
ipl-> -- Kolkata Knight Riders
ipl-> ('Eden Gardens', 'Eden Gardens'),
ipl-> ('Eden Gardens, Kolkata', 'Eden Gardens'),
ipl->
ipl-> -- Royal Challengers Bangalore
ipl-> ('M Chinnaswamy Stadium', 'M Chinnaswamy Stadium'),
ipl-> ('M Chinnaswamy Stadium, Bengaluru', 'M Chinnaswamy Stadium'),
ipl->
ipl-> -- Sunrisers Hyderabad
ipl-> ('Rajiv Gandhi International Stadium', 'Rajiv Gandhi International Stadium'),
ipl-> ('Rajiv Gandhi International Stadium, Uppal', 'Rajiv Gandhi International Stadium'),
ipl-> ('Rajiv Gandhi International Stadium, Uppal, Hyderabad', 'Rajiv Gandhi International Stadium'),
ipl->
ipl-> -- Delhi Capitals
ipl-> ('Arun Jaitley Stadium', 'Arun Jaitley Stadium'),
ipl-> ('Arun Jaitley Stadium, Delhi', 'Arun Jaitley Stadium'),
ipl-> ('Feroz Shah Kotla', 'Arun Jaitley Stadium'),
ipl->
ipl-> -- Punjab Kings (Kings XI Punjab)
ipl-> ('Punjab Cricket Association Stadium, Mohali', 'Punjab Cricket Association IS Bindra Stadium'),
ipl-> ('Punjab Cricket Association IS Bindra Stadium', 'Punjab Cricket Association IS Bindra Stadium'),
ipl-> ('Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh', 'Punjab Cricket Association IS Bindra Stadium'),
ipl-> ('Maharaja Yadavindra Singh International Cricket Stadium, New Chandigarh', 'Maharaja Yadavindra Singh International Cricket Stadium'),
ipl-> ('Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur', 'Maharaja Yadavindra Singh International Cricket Stadium'),
ipl->
ipl-> -- Rajasthan Royals
ipl-> ('Sawai Mansingh Stadium', 'Sawai Mansingh Stadium'),
ipl-> ('Sawai Mansingh Stadium, Jaipur', 'Sawai Mansingh Stadium'),
ipl->
ipl-> -- Gujarat Titans
ipl-> ('Narendra Modi Stadium', 'Narendra Modi Stadium'),
ipl-> ('Narendra Modi Stadium, Ahmedabad', 'Narendra Modi Stadium'),
ipl-> ('Sardar Patel Stadium, Motera', 'Narendra Modi Stadium'),
ipl->
ipl-> -- Lucknow Super Giants
ipl-> ('Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow', 'BRSABV Ekana Cricket Stadium');

ipl=> CREATE TABLE team_home_venues (
ipl(>     team TEXT,
ipl(>     venue TEXT
ipl(> );
CREATE TABLE
ipl=> INSERT INTO team_home_venues (team, venue) VALUES
ipl-> -- Chennai Super Kings
ipl-> ('Chennai Super Kings', 'MA Chidambaram Stadium'),
ipl->
ipl-> -- Mumbai Indians
ipl-> ('Mumbai Indians', 'Wankhede Stadium'),
ipl->
ipl-> -- Kolkata Knight Riders
ipl-> ('Kolkata Knight Riders', 'Eden Gardens'),
ipl->
ipl-> -- Royal Challengers Bangalore
ipl-> ('Royal Challengers Bangalore', 'M Chinnaswamy Stadium'),
ipl-> ('Royal Challengers Bengaluru', 'M Chinnaswamy Stadium'), -- rename variant
ipl->
ipl-> -- Sunrisers Hyderabad
ipl-> ('Sunrisers Hyderabad', 'Rajiv Gandhi International Stadium'),
ipl->
ipl-> -- Delhi Capitals / Daredevils
ipl-> ('Delhi Capitals', 'Arun Jaitley Stadium'),
ipl-> ('Delhi Daredevils', 'Arun Jaitley Stadium'),
ipl->
ipl-> -- Punjab Kings / Kings XI Punjab
ipl-> ('Punjab Kings', 'Punjab Cricket Association IS Bindra Stadium'),
ipl-> ('Kings XI Punjab', 'Punjab Cricket Association IS Bindra Stadium'),
ipl->
ipl-> -- Rajasthan Royals
ipl-> ('Rajasthan Royals', 'Sawai Mansingh Stadium'),
ipl->
ipl-> -- Gujarat Titans
ipl-> ('Gujarat Titans', 'Narendra Modi Stadium'),
ipl->
ipl-> -- Lucknow Super Giants
ipl-> ('Lucknow Super Giants', 'BRSABV Ekana Cricket Stadium');
INSERT 0 13
ipl=> INSERT INTO team_home_venues (team, venue) VALUES
ipl-> ('Punjab Kings', 'Maharaja Yadavindra Singh International Cricket Stadium');
INSERT 0 1
ipl=> WITH cleaned_matches AS (
ipl(>     SELECT m.match_id, m.season,
ipl(>            v.canonical_name AS venue,
ipl(>            m.team1, m.team2, m.winner
ipl(>     FROM matches m
ipl(>     JOIN venue_mapping v
ipl(>       ON m.venue = v.raw_name
ipl(> ),
ipl-> home_games AS (
ipl(>     SELECT cm.*,
ipl(>            th.team AS home_team
ipl(>     FROM cleaned_matches cm
ipl(>     JOIN team_home_venues th
ipl(>       ON cm.venue = th.venue
ipl(>      AND (cm.team1 = th.team OR cm.team2 = th.team)
ipl(> )
ipl-> SELECT
ipl->     home_team,
ipl->     COUNT(*) AS home_games,
ipl->     COUNT(*) FILTER (WHERE winner = home_team) AS home_wins,
ipl->     ROUND(100.0 * COUNT(*) FILTER (WHERE winner = home_team) / COUNT(*), 2) AS home_win_pct
ipl-> FROM home_games
ipl-> GROUP BY home_team
ipl-> ORDER BY home_win_pct DESC;