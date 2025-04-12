import psycopg2
from utils.base_connector import BaseConnector

class PostgresConnector(BaseConnector):
    def __init__(self):
        self.conn = None

    def connect(self, username, password, database, host, port):
        self.conn = psycopg2.connect(
            user=username,
            password=password,
            database=database,
            host=host,
            port=port
        )

    def execute_and_return_result(self, query):
        try:
            with self.conn.cursor() as cur:
                cur.execute(query)
                if cur.description:
                    result = cur.fetchall()
                else:
                    result = []
                self.conn.commit()  # commit if needed
                return result
        except Exception as e:
            print(f"Error executing query: {query}. Error: {e}")
            try:
                self.conn.rollback()
            except Exception as rollback_error:
                print(f"Error during rollback: {rollback_error}")
                raise rollback_error
            raise e


