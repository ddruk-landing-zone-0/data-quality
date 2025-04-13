from pymongo import MongoClient
from utils.base_connector import BaseConnector
from pymongo import InsertOne, UpdateOne, DeleteOne
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
            elif operation == "update":
                filter_criteria = query.get("filter", {})
                update_data = query.get("update", {})
                result = self.db[collection_name].update_many(filter_criteria, {"$set": update_data})
                return {"matched_count": result.matched_count, "modified_count": result.modified_count}
            elif operation == "delete":
                filter_criteria = query.get("filter", {})
                result = self.db[collection_name].delete_many(filter_criteria)
                return {"deleted_count": result.deleted_count}
            elif operation == "count":
                filter_criteria = query.get("filter", {})
                count = self.db[collection_name].count_documents(filter_criteria)
                return {"count": count}
            elif operation == "aggregate":
                pipeline = query.get("pipeline", [])
                if not isinstance(pipeline, list):
                    raise ValueError("Pipeline must be a list")
                ans = list(self.db[collection_name].aggregate(pipeline))
                # Convert ObjectId to string for JSON serialization
                for doc in ans:
                    doc["_id"] = str(doc["_id"])
                return ans
            elif operation == "distinct":
                field = query.get("field")
                filter_criteria = query.get("filter", {})
                if not field:
                    raise ValueError("Missing field for distinct operation")
                distinct_values = self.db[collection_name].distinct(field, filter_criteria)
                return {"distinct_values": distinct_values}
            elif operation == "drop":
                result = self.db[collection_name].drop()
                return {"result": "Collection dropped"}
            elif operation == "create_index":
                index_field = query.get("index_field")
                if not index_field:
                    raise ValueError("Missing index field for create_index operation")
                result = self.db[collection_name].create_index(index_field)
                return {"result": f"Index created: {result}"}
            elif operation == "list_indexes":
                indexes = list(self.db[collection_name].list_indexes())
                # Convert ObjectId to string for JSON serialization
                for index in indexes:
                    index["_id"] = str(index["_id"])
                return indexes
            elif operation == "drop_index":
                index_name = query.get("index_name")
                if not index_name:
                    raise ValueError("Missing index name for drop_index operation")
                result = self.db[collection_name].drop_index(index_name)
                return {"result": f"Index dropped: {result}"}
            elif operation == "bulk_write":
                operations = query.get("operations", [])
                if not isinstance(operations, list):
                    raise ValueError("Operations must be a list")
                bulk_operations = []
                for op in operations:
                    op_type = op.get("type")
                    if op_type == "insert":
                        bulk_operations.append(
                            InsertOne(op.get("document"))
                        )
                    elif op_type == "update":
                        bulk_operations.append(
                            UpdateOne(op.get("filter"), {"$set": op.get("update")})
                        )
                    elif op_type == "delete":
                        bulk_operations.append(
                            DeleteOne(op.get("filter"))
                        )
                result = self.db[collection_name].bulk_write(bulk_operations)
                return {
                    "inserted_count": result.inserted_count,
                    "matched_count": result.matched_count,
                    "modified_count": result.modified_count,
                    "deleted_count": result.deleted_count
                }
            elif operation == "list_collections":
                collections = self.db.list_collection_names()
                return {"collections": collections}
            elif operation == "list_databases":
                databases = self.client.list_database_names()
                return {"databases": databases}
            elif operation == "drop_database":
                db_name = query.get("db_name")
                if not db_name:
                    raise ValueError("Missing database name for drop_database operation")
                self.client.drop_database(db_name)
                return {"result": f"Database {db_name} dropped"}
            elif operation == "create_collection":
                collection_name = query.get("collection_name")
                if not collection_name:
                    raise ValueError("Missing collection name for create_collection operation")
                self.db.create_collection(collection_name)
                return {"result": f"Collection {collection_name} created"}
            else:
                raise ValueError(f"Unsupported MongoDB operation")
        except Exception as e:
            raise ValueError(f"Invalid MongoDB query format {e}") from e
