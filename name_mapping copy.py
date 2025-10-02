import pandas as pd
from rapidfuzz import process, fuzz

# Load data
auctions = pd.read_csv("auction_data.csv")
deliveries = pd.read_csv("deliveries.csv")

# Unique player names from deliveries
players_deliveries = pd.unique(
    deliveries[['batsman','bowler','player_out']].values.ravel('K')
)
players_deliveries = pd.Series(players_deliveries).dropna().unique()

# Function to map auction name -> closest match in deliveries
def match_name(name, choices, scorer=fuzz.token_sort_ratio, threshold=50):
    match, score, _ = process.extractOne(name, choices, scorer=scorer)
    return match if score >= threshold else None

# Apply matching
auctions["delivery_name"] = auctions["name"].apply(
    lambda x: match_name(x, players_deliveries)
)

# Check how many didn’t match
unmatched = auctions[auctions["delivery_name"].isna()]

# Save mapping for manual review
auctions[["name","delivery_name"]].to_csv("name_mapping_2.csv", index=False)
