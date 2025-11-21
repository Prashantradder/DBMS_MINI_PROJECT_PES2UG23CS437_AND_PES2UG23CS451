#working
import pandas as pd
from db_config import get_engine

def fetch_all(query):
    """
    Executes a SQL SELECT query and returns the result as a DataFrame.
    """
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df


def call_procedure(proc_name, params=[]):
    """
    Calls a stored procedure with given parameters and returns
    a list of DataFrames for each result set.
    """
    engine = get_engine()
    conn = engine.raw_connection()  # NO 'with' here
    cursor = conn.cursor()

    try:
        cursor.callproc(proc_name, params)

        results = []
        for res in cursor.stored_results():
            cols = [c[0] for c in res.description] if res.description else []
            rows = res.fetchall()
            results.append(pd.DataFrame(rows, columns=cols))

        conn.commit()
        return results
    except Exception as e:
        print(f"Error executing procedure: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
