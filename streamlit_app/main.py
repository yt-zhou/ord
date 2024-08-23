import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Helper function to fetch data
def fetch_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return []

# Visualization 1: Messages sent per campaign
st.title("SMS Logs Analytics Dashboard")
messages_sent_data = fetch_data("http://localhost:5000/smslogs/messages-sent")
if messages_sent_data:
    df_messages_sent = pd.DataFrame(messages_sent_data)
    st.subheader("Messages Sent Per Campaign")
    st.bar_chart(df_messages_sent.set_index('campaignId')['message_count'])

# Visualization 2: Responses per campaign
responses_data = fetch_data("http://localhost:5000/smslogs/responses")
if responses_data:
    df_responses = pd.DataFrame(responses_data)
    st.subheader("Responses Per Campaign")
    st.bar_chart(df_responses.set_index('campaignId')['response_count'])

# Visualization 3: Members opted in per campaign
opted_in_data = fetch_data("http://localhost:5000/members/opted-in")
if opted_in_data:
    df_opted_in = pd.DataFrame(opted_in_data)
    st.subheader("Members Opted In Per Campaign")
    st.bar_chart(df_opted_in.set_index('_id')['opted_in_count'])


# Visualization 5: Campaigns Created Per Year Per Client
campaigns_yearly_data = fetch_data("http://localhost:5000/campaigns/yearly")
if campaigns_yearly_data:
    df_campaigns_yearly = pd.DataFrame(campaigns_yearly_data)
    
    # Print the raw data
    st.write("Campaigns Yearly Data (Raw):", df_campaigns_yearly)
    
    # Normalize the '_id' field to extract 'clientName' and 'year'
    if '_id' in df_campaigns_yearly.columns:
        df_id_normalized = pd.json_normalize(df_campaigns_yearly['_id'])
        df_campaigns_yearly = pd.concat([df_id_normalized, df_campaigns_yearly['count']], axis=1)
        
        # Print the normalized data
        st.write("Normalized Campaigns Yearly Data:", df_campaigns_yearly)
        
        # Check if there are any missing values
        st.write("Checking for missing values:")
        st.write(df_campaigns_yearly.isnull().sum())
        
    # Process and visualize the data
    if not df_campaigns_yearly.empty and 'year' in df_campaigns_yearly.columns and 'clientName' in df_campaigns_yearly.columns:
        df_campaigns_yearly_pivot = df_campaigns_yearly.pivot_table(index='year', columns='clientName', values='count')
        st.subheader("Campaigns Created Per Year Per Client")
        st.line_chart(df_campaigns_yearly_pivot)
    else:
        st.warning("No data available to display the visualization.")
else:
    st.error("No data returned from the API.")


st.sidebar.title("Analytics Dashboard")
st.sidebar.markdown("This dashboard visualizes data from SMS logs, members, and campaigns.")
