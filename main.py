from extract import extract_matches
from transform import transform_matches
from load import load_to_postgres


def main():
    print("Extracting data...")
    data = extract_matches()

    print("Transforming data...")
    df = transform_matches(data)

    print(df.head())

    print("Loading to PostgresSQL...")
    load_to_postgres(df)

    print("Pipeline completed successfully.")

if __name__=="__main__":
    main()
