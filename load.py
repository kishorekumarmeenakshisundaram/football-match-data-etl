import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


def create_postrgres_engine():
    load_dotenv()

    db_url= URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=int(os.getenv("POSTGRES_PORT")),
        database=os.getenv("POSTGRES_DB")
    )
    return create_engine(db_url)

def load_to_postgres(df):
    engine = create_postrgres_engine()

    df.to_sql(
        "world_cup_matches",
        engine,
        if_exists="replace",
        index=False
    )

    print(f"{len(df)} matches loaded successfully.")

    