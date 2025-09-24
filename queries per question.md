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
