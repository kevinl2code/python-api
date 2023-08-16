import os
from functools import lru_cache
import psycopg2
import psycopg2.extras
from dotenv import dotenv_values

config = dotenv_values(".env")
host = config["PG_DB_HOST"]
name = config["PG_DB_NAME"]
user = config["PG_DB_USER"]
password = config["PG_DB_PASSWORD"]

print(f'host {host}')


class PostgresClient:
    # Down the road if I want to have different environments
    # def __init__(self, host, port, database, user, password):
    def __init__(self):
        self.host = host
        self.port = 5432
        # self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                # database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            print("Connected to PostgreSQL database")
        except psycopg2.Error as e:
            print("Error: Unable to connect to PostgreSQL database")
            print(e)

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Disconnected from PostgreSQL database")

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query + ' RETURNING id', params)
            else:
                self.cursor.execute(query + ' RETURNING id')
            self.connection.commit()
            print("Query executed successfully")
            return self.cursor.fetchone()[0]

        except psycopg2.Error as e:
            print("Error executing query:")
            print(e)

    def fetch_data(self, query, params=None):
        # with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except psycopg2.Error as e:
            print("Error fetching data:")
            print(e)
            return None


@lru_cache
def get_postgres_client():
    return PostgresClient()

# Example usage
# if __name__ == "__main__":
#     db_client = PostgreSQLClient(
#         host="your_host",
#         port="your_port",
#         database="your_database",
#         user="your_user",
#         password="your_password"
#     )

#     db_client.connect()

#     create_table_query = """
#         CREATE TABLE IF NOT EXISTS test_table (
#             id SERIAL PRIMARY KEY,
#             name VARCHAR(100),
#             age INT
#         )
#     """

#     db_client.execute_query(create_table_query)

#     insert_data_query = """
#         INSERT INTO test_table (name, age) VALUES (%s, %s)
#     """

#     data_to_insert = ("John Doe", 30)
#     db_client.execute_query(insert_data_query, data_to_insert)

#     select_data_query = "SELECT * FROM test_table"
#     rows = db_client.fetch_data(select_data_query)

#     if rows:
#         for row in rows:
#             print(row)

#     db_client.disconnect()
