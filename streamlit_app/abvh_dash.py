import streamlit as st
import requests
import pandas as pd

# Helper function to fetch data from Flask API
def fetch_campaign_data():
    url = "http://localhost:5000/campaigns/abvh"  # Adjust the URL as needed
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch campaign data")
        return []

# Streamlit function to display the data
def display_campaign_data():
    st.title("Campaigns for ABVH - Node o20")

    # Fetch the campaign data
    campaign_data = fetch_campaign_data()

    # If there is data, display it in a table
    if campaign_data:
        # Convert to DataFrame for better display
        df = pd.DataFrame(campaign_data)
        st.dataframe(df)

        # Optional: Display specific columns with formatting
        selected_columns = df[['clientName', 'campaignName', 'smsSource', 'opClientId', 'opCampaignId', 'firstCampaignCate', 'createdAt', 'active', 'suspended']]
        st.subheader("Selected Campaign Data")
        st.dataframe(selected_columns)
    else:
        st.warning("No data available for the specified query.")

# Run the display function
display_campaign_data()
