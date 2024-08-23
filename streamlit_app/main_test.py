import streamlit as st
import requests
import pandas as pd

st.title("Data Visualization")

# MySQL Data
st.subheader("Data from MySQL")
mysql_data = requests.get("http://localhost:5000/mysql").json()
mysql_df = pd.DataFrame(mysql_data)
#st.write(mysql_df)

# Local MongoDB Data
st.subheader("Data from Local MongoDB")
mongo_local_data = requests.get("http://localhost:5000/mongo-local").json()
mongo_local_df = pd.DataFrame(mongo_local_data)
#st.write(mongo_local_df)

# Master MongoDB Data
st.subheader("Data from Master MongoDB")
mongo_master_data = requests.get("http://localhost:5000/mongo-master").json()
mongo_master_df = pd.DataFrame(mongo_master_data)
#st.write(mongo_master_df)

# Visualization Example (Bar chart)
if not mysql_df.empty:
    st.subheader("Bar Chart Example (MySQL Data)")
    st.bar_chart(mysql_df['target'].value_counts())  # Replace 'some_column' with an appropriate column name
