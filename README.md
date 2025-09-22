Questions we try to answer in this project. All answers are in code right now, will polish this readme afterwards.

## **Player-Centric Questions**

1. **Top Run Scorers:** Who were the top 10 batsmen by runs each season?
2. **Strike Rate Kings:** Among players with ≥200 balls faced, who has the best strike rate?
3. **Boundary Specialists:** Which players hit the most 4s/6s per season?
4. **Death Overs Specialist Batters:** Who scored the most runs in overs 16–20 across all seasons?
5. **Top Wicket-Takers:** Which bowlers took the most wickets per season?
6. **Economy in Death Overs:** Who are the most economical bowlers in overs 16–20 (min 10 overs bowled)?
7. **All-Rounder Value:** Which players contributed the most both with bat (runs) and ball (wickets) in a season?

---

## **Team-Centric Questions**

8. **Win % per Season:** Which teams had the highest win % each season?
9. **Consistency:** Which teams maintained win % > 50% across the most seasons?
10. **Chasing vs Defending:** Which teams are stronger when batting first vs chasing?
11. **Home Advantage:** Do teams win more at their home grounds? (needs venue matching)
12. **Dominance Periods:** Which teams dominated specific eras (2008–2012, 2013–2017, etc.)?

---

## **Auction & ROI (Moneyball-style)**

13. **Auction Price vs Performance:** Do expensive batsmen score more runs? Do expensive bowlers take more wickets? (Correlation/Regression)
14. **Cost per Run / Cost per Wicket:** Which players gave the best ROI for their franchise?
15. **Franchise Efficiency:** Which teams spend the most vs least per win?
16. **Mega Auction Effect:** Did mega-auction seasons disrupt dominant teams (compare win % pre vs post auction)?
17. **Undervalued Gems:** Which low-price players overperformed expectations?

---

## **Game Dynamics**

18. **Impact of Toss:** Does winning the toss significantly increase win %?
19. **Batting First vs Chasing Trend:** Has chasing become more advantageous over time?
20. **Run Rate Trends:** How has average run rate evolved from 2008 to 2025?
21. **Powerplay vs Death Overs:** Compare average runs scored in overs 1–6 vs 16–20.
22. **Match Duration:** Are matches getting longer or shorter (by total balls faced)?
23. **Close Games:** How often do matches end with <10 run margin or last-over chases?

---

## **Hardcore Stats & A/B Tests**

24. **Toss A/B Test:** H0: Toss outcome doesn’t affect result. Run chi-square test.
25. **Home Advantage Test:** H0: Home teams don’t win more often. Run chi-square.
26. **Auction ROI Regression:** Regression of `auction_price ~ runs/wickets` → low R² = moneyball argument.
27. **Batting Order Impact:** Compare strike rates of openers vs middle-order vs finishers.
28. **Consistency Metric:** Define a “consistency score” (std dev of runs across matches) → who are most reliable batsmen?
29. **Bowler Pressure Index:** Probability of taking a wicket in death overs vs powerplay.
