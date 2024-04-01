import os
import pandas as pd
import psycopg2

df = pd.read_csv("data/processed/idh_index.csv")


def upload_to_db_efficiently(df, table_name="public.idh"):

    with psycopg2.connect(
        host="localhost",
        port=5432,
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        connect_timeout=5
    ) as conn:
        with conn.cursor() as cursor:
            # Truncate the existing table (i.e. remove all existing rows)
            cursor.execute(f"TRUNCATE {table_name}")
            conn.commit()

            # Now insert the brand-new data
            # Initialize a string buffer
            sio = StringIO()
            # Write the Pandas DataFrame as a CSV file to the buffer
            sio.write(df.to_csv(index=None, header=None))
            # Be sure to reset the position to the start of the stream
            sio.seek(0)
            cursor.copy_from(
                file=sio,
                table=table_name,
                sep=",",
                null="",
                size=8192,
                columns=df.columns
            )
            conn.commit()
            print("DataFrame uploaded to TimescaleDB")