import pandas as pd

def transform_matches(data):
    rows=[]

    for match in data.get("matches",[]):
        rows.append({
            "match_id": match["id"],
            "match_date":match["utcDate"],
            "stage":match["stage"],
            "status": match["status"],
            "home_team": match["homeTeam"]["name"],
            "away_team": match["awayTeam"]["name"],
            "home_score": match["score"]["fullTime"]["home"],
            "away_score": match["score"]["fullTime"]["away"],
            "winner": match["score"]["winner"],
            "last_updated": match["lastUpdated"]
        })
    df = pd.DataFrame(rows)
    return df
