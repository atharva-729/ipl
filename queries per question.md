q1. top run scorers per season

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

q2. highest strike rate batsmen per season 

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