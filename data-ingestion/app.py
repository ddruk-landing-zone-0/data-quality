from flask import Flask, request, jsonify
from schemas import SCHEMAS
from utils.sample_generator import generate_samples
from utils.connector_client import connect_to_db, insert_to_db, create_table_if_not_exists


app = Flask(__name__)


@app.route('/about', methods=['GET'])
def about():
    return {'app_version': "0.0.0"}, 200

@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.get_json()
    db_type = data.get("type", "").lower()

    if db_type not in SCHEMAS:
        return jsonify({"error": f"Unsupported db type: {db_type}"}), 400

    try:
        # Connect
        connect_response = connect_to_db(db_type)

        # Create schema/table if not exists
        schema_response = create_table_if_not_exists(db_type)

        # Generate & insert data
        schema = SCHEMAS[db_type]
        samples = generate_samples(schema.get("fields", list(schema["columns"].keys())), n=10)
        insert_response = insert_to_db(db_type, samples)

        return jsonify({
            "connect_response": connect_response,
            "schema_response": schema_response,
            "insert_response": insert_response,
            "inserted_samples": samples
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
