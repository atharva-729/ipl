\copy (
    SELECT
        m.season,
        d.batsman AS player,
        d.batting_team AS team,
        SUM(d.runs_batsman) AS runs,
        sum(case when d.extras_type in ('noballs', 'wides') then 0 else 1 end) AS balls,
        ROUND(((SUM(d.runs_batsman) * 100.0) /
              NULLIF(COUNT(*) FILTER (WHERE d.extras_type NOT IN ('wides','noballs')), 0))::numeric, 2) AS strike_rate,
        SUM(CASE WHEN d.runs_batsman = 4 THEN 1 ELSE 0 END) AS fours,
        SUM(CASE WHEN d.runs_batsman = 6 THEN 1 ELSE 0 END) AS sixes,
        ROUND(((SUM(CASE WHEN d.runs_batsman IN (4,6) THEN 1 ELSE 0 END)::float /
               NULLIF(COUNT(*) FILTER (WHERE d.extras_type NOT IN ('wides','noballs')), 0)) * 100)::numeric, 2) AS boundary_pct,
        SUM(CASE WHEN d.runs_total = 0 THEN 1 ELSE 0 END) AS dot_balls,
        ROUND(((SUM(CASE WHEN d.runs_total = 0 THEN 1 ELSE 0 END)::float /
               NULLIF(COUNT(*), 0)) * 100)::numeric, 2) AS dot_pct,
        COUNT(DISTINCT d.player_out) AS dismissals,
        ROUND((SUM(d.runs_batsman)::float / NULLIF(COUNT(DISTINCT d.player_out), 0))::numeric, 2) AS batting_avg
    FROM matches m
    JOIN deliveries d ON m.match_id = d.match_id
    WHERE d.over BETWEEN 1 AND 6
    GROUP BY m.season, d.batsman, d.batting_team
) TO 'C:/Users/91821/Desktop/ipl/batting_powerplay.csv' CSV HEADER;
