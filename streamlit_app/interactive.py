import streamlit as st
import pandas as pd

# Example Data - Replace this with your actual data or query results
data = {
    'modality': ['SMS', 'EMAIL', 'IVR', 'SMS', 'EMAIL', 'IVR'],
    'campaign': ['Campaign 1', 'Campaign 1', 'Campaign 1', 'Campaign 2', 'Campaign 2', 'Campaign 2'],
    'outreach': [100, 150, 200, 120, 160, 180],
    'responses': [50, 70, 100, 60, 90, 110]
}

df = pd.DataFrame(data)

# Create two columns
col1, col2 = st.columns([1, 3])  # Adjust the ratio to control the width

# Place the filter dropdown in the first column
with col1:
    modality = st.selectbox("Select Modality", options=['All', 'SMS', 'EMAIL', 'IVR'])

# Filter data based on user selection
if modality != 'All':
    df = df[df['modality'] == modality]

# Display the chart in the second column
with col2:
    st.subheader(f"Outreach by Campaign for {modality}")
    st.bar_chart(df.groupby('campaign')['outreach'].sum())

# You can also place the response chart below or create another row with columns
col3, col4 = st.columns([1, 3])

# Place another filter or widget in the first column of the new row if needed
with col3:
    st.write("")  # Placeholder for alignment

# Place the response chart in the second column of the new row
with col4:
    st.subheader(f"Responses by Campaign for {modality}")
    st.bar_chart(df.groupby('campaign')['responses'].sum())
