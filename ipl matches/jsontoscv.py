import os
import json
import pandas as pd

# Folder with CricSheet JSONs
json_folder = "C:\\Users\\91821\\Desktop\\;)\\things that matter\\ipl\\ipl matches" 
matches_data = []
deliveries_data = []

match_id = 1000

for file in os.listdir(json_folder):
    if file.endswith(".json"):
        with open(os.path.join(json_folder, file), "r", encoding="utf-8") as f:
            data = json.load(f)

            info = data["info"]

            # --- Match metadata ---
            match_id += 1
            season = info["season"]
            date = info["dates"][0]
            venue = info.get("venue")
            team1, team2 = info["teams"][0], info["teams"][1]
            toss_winner = info["toss"]["winner"]
            toss_decision = info["toss"]["decision"]
            winner = info.get("outcome", {}).get("winner")
            result = info.get("outcome", {}).get("result")
            margin = str(info.get("outcome", {}).get("by"))

            matches_data.append([
                match_id, season, date, venue, team1, team2,
                toss_winner, toss_decision, winner, result, margin
            ])

            # --- Deliveries ---
            for inning_no, inning in enumerate(data["innings"], start=1):
                batting_team = inning["team"]
                inning_runs = 0
                inning_wickets = 0
                for over in inning["overs"]:
                    over_no = over["over"]
                    deliveryno = 1
                    for delivery in over["deliveries"]:
                        inning_runs += delivery["runs"]["total"]
                        inning_wickets += 1 if "wickets" in delivery else 0
                        deliveries_data.append([
                            match_id,
                            inning_no,
                            over_no,
                            deliveryno,
                            batting_team,
                            delivery["batter"],
                            delivery["bowler"],
                            delivery["runs"]["batter"],
                            delivery["runs"]["extras"],
                            delivery["runs"]["total"],
                            inning_runs,
                            list(delivery.get("extras", {}).keys())[0] if "extras" in delivery else None,
                            delivery["wickets"][0]["kind"] if "wickets" in delivery else None,
                            delivery["wickets"][0]["player_out"] if "wickets" in delivery else None,
                            inning_wickets
                        ]
                        )
                        deliveryno += 1

                        

# Convert to DataFrames
matches_df = pd.DataFrame(matches_data, columns=[
    "match_id", "season", "date", "venue", "team1", "team2",
    "toss_winner", "toss_decision", "winner", "result", "margin"
])

deliveries_df = pd.DataFrame(deliveries_data, columns=[
    "match_id", "inning", "over", "ball", "batting_team",
    "batsman", "bowler", "runs_batsman", "runs_extras", "runs_total", "inning_runs",
    "extras_type", "wicket_kind", "player_out", "inning_wickets"
])

# Save to CSV
matches_df.to_csv("C:\\Users\\91821\\Desktop\\;)\\things that matter\\ipl\\ipl matches\\matches.csv", index=False)
deliveries_df.to_csv("C:\\Users\\91821\\Desktop\\;)\\things that matter\\ipl\\ipl matches\\deliveries.csv", index=False)

print("Matches CSV:", matches_df.shape)
print("Deliveries CSV:", deliveries_df.shape)
