import mysql.connector
from utils.base_connector import BaseConnector

class MySQLConnector(BaseConnector):
    def __init__(self):
        self.conn = None

    def connect(self, username, password, database, host, port):
        self.conn = mysql.connector.connect(
            user=username,
            password=password,
            database=database,
            host=host,
            port=port
        )

    def execute_and_return_result(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        if cursor.description:
            return cursor.fetchall()
        return []
