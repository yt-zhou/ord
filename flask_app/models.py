# models.py

import mysql.connector
from pymongo import MongoClient
import ssl

# MySQL connection
def get_mysql_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="", #insert user here
        password="", #insert password here
        database="HcTai"
    )
    return conn

# Local MongoDB connection
def get_local_mongo_connection():

    client = MongoClient('localhost:27017',
                         tls=True,
                         tlsAllowInvalidCertificates=True,
                         username = '', #insert user here
                         password = '', #insert password here
                         authSource = 'HcTai')
    
    
    db = client['HcTai']  

    print("Connected to MongoDB with SSL...")

    return db


# Master MongoDB connection
def get_master_mongo_connection():

    client = MongoClient('localhost:27017',
                         tls=True,
                         tlsAllowInvalidCertificates=True,
                         username = '', #insert user here
                         password = '', #insert password here
                         authSource = 'HcTaiMaster')
    
    
    db = client['HcTaiMaster']  

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
        db = get_mongo_connection()
        # Just list the collections to see if the connection works
        collections = db.list_collection_names()
        if collections:
            print("MongoDB connection is successful. Collections:", collections)
        else:
            print("MongoDB connection failed.")
    except Exception as err:
        print(f"MongoDB error: {err}")

