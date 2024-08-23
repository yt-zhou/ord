import mysql.connector
from dotenv import load_dotenv
from pymongo import MongoClient
import ssl
import os

# Load environment variables from .env file
load_dotenv()

# MySQL connection
def get_mysql_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DB')
    )
    return conn

# Local MongoDB connection
def get_local_mongo_connection():
    client = MongoClient('localhost:27017',
                         tls=True,
                         tlsAllowInvalidCertificates=True,
                         username=os.getenv('MONGO_LOCAL_USER'),
                         password=os.getenv('MONGO_LOCAL_PASSWORD'),
                         authSource=os.getenv('MONGO_LOCAL_DB'))
    db = client[os.getenv('MONGO_LOCAL_DB')]  
    print("Connected to MongoDB with SSL...")
    return db

# Master MongoDB connection
def get_master_mongo_connection():
    client = MongoClient('localhost:27017',
                         tls=True,
                         tlsAllowInvalidCertificates=True,
                         username=os.getenv('MONGO_MASTER_USER'),
                         password=os.getenv('MONGO_MASTER_PASSWORD'),
                         authSource=os.getenv('MONGO_MASTER_DB'))
    db = client[os.getenv('MONGO_MASTER_DB')]  
    print("Connected to Master MongoDB with SSL...")
    return db

# Test MySQL connection
def test_mysql_connection():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        conn.close()
        if result:
            print("MySQL connection is successful.")
        else:
            print("MySQL connection failed.")
    except mysql.connector.Error as err:
        print(f"MySQL error: {err}")

# Test MongoDB connection
def test_mongo_connection():
    try:
        db = get_local_mongo_connection()  # Changed to get_local_mongo_connection
        collections = db.list_collection_names()
        if collections:
            print("MongoDB connection is successful. Collections:", collections)
        else:
            print("MongoDB connection failed.")
    except Exception as err:
        print(f"MongoDB error: {err}")

if __name__ == "__main__":
    test_mysql_connection()
    test_mongo_connection()