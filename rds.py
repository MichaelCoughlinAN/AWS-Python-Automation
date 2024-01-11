import boto3
import psycopg2

# Function to connect to PostgreSQL database
def connect_to_postgres(host, dbname, user, password):
    conn_string = f"host={host} dbname={dbname} user={user} password={password}"
    conn = psycopg2.connect(conn_string)
    return conn

# Function to execute a query in PostgreSQL
def execute_postgres_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Example usage
if __name__ == "__main__":
    # PostgreSQL example usage
    postgres_conn = connect_to_postgres('your-db-host', 'your-db-name', 'your-db-user', 'your-db-password')
    
    # Example query - adjust as needed
    query_result = execute_postgres_query(postgres_conn, 'SELECT * FROM your_table;')
    for row in query_result:
        print(row)

    # Remember to close the connection
    postgres_conn.close()
