import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_cursor(db_name, environment):
    postgres_connection = psycopg2.connect(
        database=db_name,
        user=os.environ[f'ANALYSIS_DB_{environment.upper()}_USER'],
        password=os.environ[f'ANALYSIS_DB_{environment.upper()}_PASSWORD'],
        host=os.environ[f'ANALYSIS_DB_{environment.upper()}_HOST'],
        port='5432'
    )
    postgres_connection.autocommit = True

    # Creating a cursor object using the cursor() method
    return postgres_connection.cursor(cursor_factory=RealDictCursor)
