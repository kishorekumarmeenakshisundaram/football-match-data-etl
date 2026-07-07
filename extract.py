import requests
from datetime import datetime
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")

def extract_matches():
    url = "https://api.football-data.org/v4/matches"

    headers = {
        "X-Auth-Token": API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Save raw JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        with open(f"raw_matches_{timestamp}.json", "w") as f:
            json.dump(data, f, indent=4)

        print("Data extracted successfully")
        print(f"Total matches returned: {len(data.get('matches', []))}")

        return data
    
    else:
        print("Failed:", response.status_code)