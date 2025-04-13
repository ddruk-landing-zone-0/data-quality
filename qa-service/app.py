from flask import Flask, request, jsonify
import os
from constraints import CONSTRAINTS
from utils.connector_client import connect_to_db, perform_checks
from utils.db_logger import connect_to_qa_db, create_qa_table_if_not_exists, store_log_check_result

app = Flask(__name__)

qa_db_creds = {
    "host": os.getenv("QA_POSTGRES_HOST", "my-qa-postgres-container-0"),
    "port": os.getenv("QA_POSTGRES_PORT", "5432"),
    "username": os.getenv("QA_POSTGRES_USER", "admin"),
    "password": os.getenv("QA_POSTGRES_PASSWORD", "admin"),
    "database": os.getenv("QA_POSTGRES_DATABASE", "qa_db"),
    "table": "qa_logs"
}
 
@app.route("/about")
def about():
    return {'app_version': "0.0.0"}, 200

@app.route("/perform-check", methods=["POST"])
def perform_check():
    data = request.get_json()
    db_type = data.get("type", "").lower()
    database = data.get("database", "")

    if db_type not in CONSTRAINTS:
        return jsonify({"error": f"Unsupported db type: {db_type}"}), 400
    if database not in CONSTRAINTS[db_type]:
        return jsonify({"error": f"Unsupported database: {database}"}), 400
    
    try:
        # Connect to target database
        print(f"[1/6] Connecting to {db_type} database: {database}")
        connect_response = connect_to_db(db_type,database)

        # Perform checks
        print(f"[2/6] Performing checks on {db_type} database: {database}")
        check_response = perform_checks(db_type, database)

        # Connect to the qa database
        print(f"[3/6] Connecting to QA database")
        qa_db_response = connect_to_qa_db(qa_db_creds)

        # Create the table if it doesn't exist
        print(f"[4/6] Creating table if not exists in QA database")
        create_table_response = create_qa_table_if_not_exists(
            db_type = "postgres",
            database = qa_db_creds["database"],
            table = qa_db_creds["table"]
        )

        # Check if the table creation was successful
        if create_table_response.get("error"):
            return jsonify({"error": "Failed to create table in QA DB"}), 500
        
        # Store the log check result
        print(f"[5/6] Storing log check result in QA database")
        store_response = store_log_check_result(
            db_type = "postgres",
            database = qa_db_creds["database"],
            table = qa_db_creds["table"],
            results = check_response
        )

        # Check if the log storing was successful
        if store_response.get("error"):
            return jsonify({"error": "Failed to store log check result"}), 500
        
        # Return the results
        print(f"[6/6] Check results: {check_response}")
        return jsonify({
            "connect_response": connect_response,
            "check_response": check_response,
            "qa_db_response": qa_db_response,
            "create_table_response": create_table_response,
            "store_response": store_response
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)

