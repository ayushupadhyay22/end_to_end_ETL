#def load_to_postgres(df, config):
#    db_url = get_db_url(config)
#    table_name = config['postgres']['table']
#    logging.info(f"Loading data to {table_name} in PostgreSQL")
#    engine = create_engine(db_url)
#    df.to_sql(table_name, engine, if_exists='replace', index=False)
#    logging.info("Table created successfully")
from sqlalchemy import create_engine
import logging

def get_db_url(config):
    """
    Constructs the database URL for SQLAlchemy.
    """
    pg = config['postgres']
    #return f"postgresql+psycopg2://{pg['user']}:{pg['password']}@{pg['host']}:{pg['port']}/{pg['dbname']}"
    return f"postgresql+psycopg2://{pg['user']}@{pg['host']}:{pg['port']}/{pg['dbname']}"

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import logging

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import logging

def load_to_postgres(df, config):
    """
    Loads a Pandas DataFrame into a PostgreSQL table using psycopg2.
    Assumes no password is needed for PostgreSQL connection.
    """
    pg = config['postgres']
    dbname = pg['dbname']
    user = pg['user']
    host = pg['host']
    port = pg['port']
    table = pg['table']

    logging.info(f"Inserting DataFrame into PostgreSQL table: {table}")

    try:
        # Establish connection (no password)
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            host=host,
            port=port
        )
        cursor = conn.cursor()

        # Dynamically build CREATE TABLE statement with all TEXT columns
        create_cols = ', '.join([f'"{col}" TEXT' for col in df.columns])
        create_query = f'CREATE TABLE IF NOT EXISTS "{table}" ({create_cols});'
        cursor.execute(create_query)

                # Build column string separately
        columns = ', '.join([f'"{col}"' for col in df.columns])

        # Safe insert query
        insert_query = f'INSERT INTO "{table}" ({columns}) VALUES %s'


        # Convert DataFrame to list of tuples
        data_tuples = [tuple(map(str, row)) for row in df.to_numpy()]

        # Use psycopg2.extras.execute_values for efficient bulk insert
        execute_values(cursor, insert_query, data_tuples)

        # Commit and close
        conn.commit()
        cursor.close()
        conn.close()

        logging.info(f"Successfully inserted {len(df)} rows into {table}")

    except Exception as e:
        logging.exception("Failed to load data to PostgreSQL via psycopg2")
        raise
