import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(layout="wide", page_title="Reporting Dashboard")

# Dashboard header with logo and title
st.image("/home/parallels/ord/streamlit_app/logo.png", width=60)  # Replace with your logo path
st.title("Reporting Dashboard")

# Helper function to fetch data from Flask API
def fetch_data(api_url, params=None):
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return {}

# Fetch campaign data from Flask API
campaign_data = fetch_data("http://localhost:5000/campaigns/aetva")

# Fetch member count data for all campaigns from Flask API
member_count_data = fetch_data("http://localhost:5000/members/aetva-campaigns")

# Fetch total messages sent
total_messages = fetch_data(
    "http://localhost:5000/campaigns/total-messages", 
    params={'campaign_ids[]': [c['_id'] for c in campaign_data]}
).get('total_messages', 0)

# Fetch reply rate data
reply_rate_data = fetch_data(
    "http://localhost:5000/campaigns/reply-rate", 
    params={'campaign_ids[]': [c['_id'] for c in campaign_data]}
)
total_unique_targets = reply_rate_data.get('total_unique_targets', 0)
replied_targets = reply_rate_data.get('replied_targets', 0)

# Display the stat cards using columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Messages Sent", value=f"{total_messages:,}")

with col2:
    st.metric(label="Active Campaigns", value=f"{len(campaign_data)}")

with col3:
    st.metric(label="Replied Targets", value=f"{replied_targets:,}")

# Combine data into a single DataFrame for visualization
if campaign_data and member_count_data:
    campaign_df = pd.DataFrame(campaign_data)
    member_count_df = pd.DataFrame(member_count_data)
    
    # Merge data on campaignId
    combined_df = pd.merge(member_count_df, campaign_df, left_on="campaignId", right_on="_id")
    combined_df = combined_df.rename(columns={"name": "Campaign Name", "memberCount": "Member Count"})

    # Charts container
    col4, col5 = st.columns(2)

    with col4:
        st.subheader("Enrollment Per Campaign")

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(combined_df["Campaign Name"], combined_df["Member Count"], color='#1f77b4')
        ax.set_xlabel("Member Count")
        ax.set_ylabel("Campaign Name")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#d1d1d1')
        ax.spines['bottom'].set_color('#d1d1d1')
        ax.tick_params(colors='#d1d1d1', which='both')
        ax.set_facecolor('#1e1e1e')
        fig.patch.set_facecolor('#1e1e1e')

        # Add value labels on the bars
        for bar in bars:
            ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
                    f'{bar.get_width():,.0f}', va='center', ha='left', color='#d1d1d1')

        # Rotate x-axis labels if they are too long
        plt.xticks(rotation=45, ha='right', color='#d1d1d1')
        plt.yticks(color='#d1d1d1')
        st.pyplot(fig)

    with col5:
        st.subheader("Reply Rate Analysis")

        labels = ['Replied', 'Did Not Reply']
        sizes = [replied_targets, total_unique_targets - replied_targets]
        colors = ['#1f77b4', '#4f9bd2']

        fig1, ax1 = plt.subplots(figsize=(8, 6))
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, textprops={'color': '#d1d1d1'})
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        fig1.patch.set_facecolor('#1e1e1e')

        st.pyplot(fig1)

else:
    st.warning("No data available to display the chart.")
