import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Set page configuration - this must be the first Streamlit command
st.set_page_config(layout="wide", page_title="Reporting Dashboard")

# Custom CSS for styling based on the provided design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Mulish:wght@300;600&display=swap');

    /* Set background */
    .reportview-container, .main {
        background-color: #f8f9fa;
        padding: 20px;
        font-family: 'Mulish', sans-serif;
    }

    /* Dashboard header */
    .dashboard-header {
        display: flex;
        align-items: center;
        background-color: #ffffff;
        padding: 20px;
        margin-bottom: 20px;
        border-bottom: 1px solid #ddd;
        position: relative;
        width: 100%;
    }
    .logo {
        width: 50px;
        height: auto;
        margin-right: 20px;
    }
    .title {
        font-size: 36px;
        text-align: left;
        color: #212529;
        font-weight: bold;
        margin: 0;
        font-family: 'Mulish SemiBold', sans-serif;
    }

    /* Stat cards */
    .stat-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-family: 'Mulish Light', sans-serif;
        position: relative;
        margin: 0 10px;
    }
    .stat-title {
        font-size: 14px;
        color: #666;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .stat-value {
        font-size: 36px;
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
    }

    /* Chart container */
    .chart-container {
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        border: 1px solid #ddd;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .chart-title {
        font-size: 20px;
        font-weight: 600;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Dashboard header with logo and title
st.markdown('''
    <div class="dashboard-header">
        <img src="/home/parallels/ord/streamlit_app/logo.png" class="logo">  <!-- Replace with your logo's path -->
        <h1 class="title">Reporting Dashboard</h1>
    </div>
''', unsafe_allow_html=True)

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
    st.markdown('''
    <div class="stat-card">
        <div class="stat-title">Total Messages Sent</div>
        <div class="stat-value">{} </div>
    </div>
    '''.format(total_messages), unsafe_allow_html=True)

with col2:
    st.markdown('''
    <div class="stat-card">
        <div class="stat-title">Active Campaigns</div>
        <div class="stat-value">{} </div>
    </div>
    '''.format(len(campaign_data)), unsafe_allow_html=True)

with col3:
    st.markdown('''
    <div class="stat-card">
        <div class="stat-title">Replied Targets</div>
        <div class="stat-value">{} </div>
    </div>
    '''.format(replied_targets), unsafe_allow_html=True)

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
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="chart-title">Enrollment Per Campaign</h2>', unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(combined_df["Campaign Name"], combined_df["Member Count"], color='#1f77b4')
        ax.set_xlabel("Member Count")
        ax.set_ylabel("Campaign Name")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#d1d1d1')
        ax.spines['bottom'].set_color('#d1d1d1')
        ax.tick_params(colors='#343a40', which='both')
        ax.set_facecolor('#f8f9fa')
        fig.patch.set_facecolor('#f8f9fa')

        # Add value labels on the bars
        for bar in bars:
            ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
                    f'{bar.get_width():,.0f}', va='center', ha='left', color='#343a40')

        # If campaign names are long, rotate them
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="chart-title">Reply Rate Analysis</h2>', unsafe_allow_html=True)

        labels = ['Replied', 'Did Not Reply']
        sizes = [replied_targets, total_unique_targets - replied_targets]
        colors = ['#4CAF50', '#FF6F61']

        fig1, ax1 = plt.subplots(figsize=(8, 6))
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(fig1)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.warning("No data available to display the chart.")
