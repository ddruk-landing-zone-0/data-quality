from pymongo import MongoClient
from utils.base_connector import BaseConnector

class MongoConnector(BaseConnector):
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self, username, password, database, host, port):
        uri = f"mongodb://{username}:{password}@{host}:{port}/{database}"
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=3000)
            self.db = self.client[database]
            # Force actual connection to validate
            self.client.admin.command('ping')
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e} ") from e

    def execute_and_return_result(self, query):
        try:
            operation = query.get("operation", "find")
            collection_name = query.get("collection")
            if not collection_name:
                raise ValueError("Missing collection name")

            if operation == "find":
                filter_criteria = query.get("filter", {})
                ans = list(self.db[collection_name].find(filter_criteria))
                # Convert ObjectId to string for JSON serialization
                for doc in ans:
                    doc["_id"] = str(doc["_id"])
                return ans
            elif operation == "insert":
                documents = query.get("documents", [])
                result = self.db[collection_name].insert_many(documents)
                return {"inserted_ids": [str(_id) for _id in result.inserted_ids]}
            else:
                raise ValueError(f"Unsupported MongoDB operation")
        except Exception as e:
            raise ValueError(f"Invalid MongoDB query format {e}") from e
