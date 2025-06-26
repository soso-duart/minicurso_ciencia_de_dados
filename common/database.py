import duckdb
import logging


logger = logging.getLogger("my_app")

def execute_query(query, database='database.duckdb'):
    logger.info(f"Executing query on database: {database}")
    conn = duckdb.connect(database)
    logger.debug(f"Executing query: {query} on database: {database}")
    try:
        return conn.execute(query).df()
    finally:
        conn.close()
        logger.info("Query executed successfully")
