from flask import Flask, jsonify
from bson import ObjectId
from .models import get_mysql_connection, get_local_mongo_connection, get_master_mongo_connection

app = Flask(__name__)

# MySQL route
@app.route('/mysql')
def get_mysql_data():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM SmsLog")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

# Local MongoDB route
@app.route('/mongo-local')
def get_local_mongo_data():
    db = get_local_mongo_connection()
    collection = db['campaigns']  # Replace 'your_collection_name' with your MongoDB collection name
    documents = list(collection.find())
    documents = [convert_objectid_to_str(doc) for doc in documents]
    return jsonify(documents)

# Master MongoDB route
@app.route('/mongo-master')
def get_master_mongo_data():
    db = get_master_mongo_connection()
    collection = db['masterCampaignMaps']  # Replace 'your_collection_name' with your MongoDB collection name
    documents = list(collection.find())
    print(documents)
    documents = [convert_objectid_to_str(doc) for doc in documents]
    return jsonify(documents)

def convert_objectid_to_str(document):
    if isinstance(document, dict):
        for key, value in document.items():
            if isinstance(value, ObjectId):
                document[key] = str(value)
            elif isinstance(value, dict):
                convert_objectid_to_str(value)
            elif isinstance(value, list):
                document[key] = [convert_objectid_to_str(item) if isinstance(item, (ObjectId, dict)) else item for item in value]
    elif isinstance(document, list):
        document = [convert_objectid_to_str(item) if isinstance(item, (ObjectId, dict)) else item for item in document]
    return document


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
