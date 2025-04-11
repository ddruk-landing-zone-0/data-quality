from flask import Flask, request, jsonify
from schemas import SCHEMAS
from utils.sample_generator import generate_samples
from utils.connector_client import connect_to_db, insert_to_db

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
        # Ensure DB is connected
        connect_response = connect_to_db(db_type)

        # Generate and insert
        schema = SCHEMAS[db_type]
        samples = generate_samples(schema, n=10)
        insert_response = insert_to_db(db_type, samples)

        return jsonify({
            "connect_response": connect_response,
            "insert_response": insert_response,
            "inserted_samples": samples
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
