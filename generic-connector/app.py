from flask import Flask, request, jsonify
from flask_cors import CORS

from utils.psql_connector import PostgresConnector
from utils.mysql_connector import MySQLConnector
from utils.mongo_connector import MongoConnector

app = Flask(__name__)
CORS(app)

connectors = {}

@app.route('/about', methods=['GET'])
def about():
    return {'app_version': "0.0.0"}, 200

@app.route('/connect', methods=['POST'])
def connect():
    try:
        data = request.get_json()
        db_type = data['type'].lower()
        username = data['username']
        password = data['password']
        database = data['database']
        connection_key = f"{db_type}_{database}"
        host = data.get('host', 'localhost')
        port = int(data.get('port'))

        if db_type == 'postgres':
            connector = PostgresConnector()
        elif db_type == 'mysql':
            connector = MySQLConnector()
        elif db_type == 'mongo':
            connector = MongoConnector()
        else:
            return jsonify({"error": "Unsupported database type"}), 400

        connector.connect(username, password, database, host, port)
        connectors[connection_key] = connector
        return jsonify({"message": f"{db_type} connected successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/execute', methods=['POST'])
def execute():
    try:
        data = request.get_json()
        db_type = data['type'].lower()
        database = data['database']
        query = data['query']
        connection_key = f"{db_type}_{database}"

        connector = connectors.get(connection_key)

        print(f"Executing query on {connection_key}: {query}")
        
        if not connector:
            return jsonify({"error": f"No active connection for {connection_key}"}), 400

        result = connector.execute_and_return_result(query)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
