import psycopg2
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_to_postgres(host, dbname, user, password):
    """
    Establish a connection to a PostgreSQL database.

    :param host: Database host address.
    :param dbname: Name of the database.
    :param user: Username for the database.
    :param password: Password for the database.
    :return: Connection object.
    """
    try:
        conn_string = f"host={host} dbname={dbname} user={user} password={password}"
        connection = psycopg2.connect(conn_string)
        return connection
    except psycopg2.DatabaseError as e:
        logger.error(f"Database connection failed: {e}")
        raise

def execute_postgres_query(connection, query):
    """
    Execute a query on a PostgreSQL database.

    :param connection: Database connection object.
    :param query: SQL query string.
    :return: Query result.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    except psycopg2.DatabaseError as e:
        logger.error(f"Query execution failed: {e}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        postgres_conn = connect_to_postgres('your-db-host', 'your-db-name', 'your-db-user', 'your-db-password')
        
        query_result = execute_postgres_query(postgres_conn, 'SELECT * FROM your_table;')
        for row in query_result:
            print(row)

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        if postgres_conn:
            postgres_conn.close()
