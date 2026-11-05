# ⚽ World Cup Matches ETL Pipeline

A simple end-to-end ETL pipeline in Python that pulls FIFA World Cup match data from the [football-data.org](https://www.football-data.org/) API, flattens it with pandas, and loads it into a PostgreSQL database.

## Overview

```
football-data.org API  ──►  Extract  ──►  Transform  ──►  Load  ──►  PostgreSQL
      (JSON)            (raw JSON saved)   (pandas DF)            (world_cup_matches)
```

| Stage | File | What it does |
|-------|------|--------------|
| **Extract** | `extract.py` | Calls the `/v4/matches` endpoint with your API token, saves the raw response as a timestamped JSON file (`raw_matches_YYYYMMDD_HHMMSS.json`), and returns the data |
| **Transform** | `transform.py` | Flattens the nested match JSON into a tabular pandas DataFrame |
| **Load** | `load.py` | Connects to PostgreSQL with SQLAlchemy and writes the DataFrame to the `world_cup_matches` table |
| **Orchestrate** | `main.py` | Runs the three steps in order |

## Tech Stack

- **Python 3**
- **requests** – API calls
- **pandas** – data transformation
- **SQLAlchemy + psycopg2** – PostgreSQL connection and loading
- **python-dotenv** – environment variable management
- **PostgreSQL** – data storage

## Data Model

The pipeline produces a `world_cup_matches` table with these columns:

| Column | Description |
|--------|-------------|
| `match_id` | Unique match ID from the API |
| `match_date` | Kickoff time (UTC) |
| `stage` | Tournament stage (e.g. `LAST_16`) |
| `status` | Match status (e.g. `FINISHED`, `TIMED`) |
| `home_team` | Home team name |
| `away_team` | Away team name |
| `home_score` | Full-time home goals (null if not played) |
| `away_score` | Full-time away goals (null if not played) |
| `winner` | `HOME_TEAM`, `AWAY_TEAM`, `DRAW`, or null |
| `last_updated` | Last update timestamp from the API |

## Project Structure

```
.
├── extract.py        # Fetch data from the API and save raw JSON
├── transform.py      # Convert raw JSON into a DataFrame
├── load.py           # Load the DataFrame into PostgreSQL
├── main.py           # Pipeline entry point
├── requirements.txt  # Python dependencies
├── .gitignore
└── .env              # Your secrets (not committed)
```

## Getting Started

### Prerequisites

- Python 3.9+
- A running PostgreSQL instance with an empty database
- A free API token from [football-data.org](https://www.football-data.org/client/register)

### 1. Clone the repository

```bash
git clone https://github.com/kishorekumarmeenakshisundaram/world-cup-etl-pipeline.git
cd world-cup-etl-pipeline
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
FOOTBALL_API_KEY=your_api_token_here

POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=your_db_name
```

### 4. Run the pipeline

```bash
python main.py
```

Expected output:

```
Extracting data...
Data extracted successfully
Total matches returned: 3
Transforming data...
...
Loading to PostgresSQL...
3 matches loaded successfully.
Pipeline completed successfully.
```

### 5. Verify the data

```sql
SELECT home_team, away_team, home_score, away_score, stage, status
FROM world_cup_matches;
```

## Sample Data

Example of a raw API response saved by the extract step:

```json
{
  "id": 537380,
  "utcDate": "2026-07-07T00:00:00Z",
  "status": "FINISHED",
  "stage": "LAST_16",
  "homeTeam": { "name": "United States" },
  "awayTeam": { "name": "Belgium" },
  "score": { "winner": "AWAY_TEAM", "fullTime": { "home": 1, "away": 4 } }
}
```

## Notes

- The load step uses `if_exists="replace"`, so each run **overwrites** the `world_cup_matches` table with the latest API response.
- The API returns matches for its default date window unless `dateFrom` / `dateTo` parameters are passed.
- Raw JSON snapshots are written to the project folder on every run.

## Future Improvements

- [ ] Switch from `replace` to an upsert on `match_id`
