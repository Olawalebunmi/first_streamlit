import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import matplotlib.pyplot as plt

import plotly.graph_objects as go


# Page configuration
st.set_page_config(page_title="Data Analyst Dashboard", layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Reading in data
try:
    datahub = pd.read_csv("newbies.csv", encoding="utf-8")
except FileNotFoundError:
    st.error("The file 'newbies.csv' was not found. Please ensure it is in the correct directory.")
    st.stop()  # Stop execution if the file is missing
except Exception as e:
    st.error(f"An error occurred while reading the CSV file: {e}")
    st.stop()

st.header("Data Analyst Survey")
html_title = """
<style>
    .title-test {
    font-weight:bold;
    padding: Spx;
    border-radius:6px
    }
    </style>
    <center><h1 class="title-test">Data Analyst Survey Dashboard</h1></center>"""
st.markdown(html_title, unsafe_allow_html=True)

# Sidebar multiselect for filtering (with distinct options)
st.sidebar.header("Filter Options")
distinct_tools = datahub['tools'].unique()  # Get unique values from the 'Tool' column
selected_tools = st.sidebar.multiselect(
    "Select Tools to Display", 
    options=distinct_tools,  # Populate with unique tool names
    default=distinct_tools  # Default selection (all tools)
)

# Filter data based on selection
if selected_tools:
    filtered_data = datahub[datahub['tools'].isin(selected_tools)]
else:
    filtered_data = datahub

# Display filtered data as a table
st.write("Filtered Data:")
st.write(filtered_data)

# Plot a bar chart with the filtered data
fig, ax = plt.subplots()
usage_sums = filtered_data.groupby('Tool')['Usage'].sum()  # Aggregate usage by Tool
ax.bar(usage_sums.index, usage_sums.values, color='skyblue')
ax.set_xlabel("tools")
ax.set_ylabel("Usage (%)")
ax.set_title("Tool Usage by Professionals")
ax.spines[['top', 'right']].set_visible(False)  # Remove top and right spines

# Add data labels
for i, v in enumerate(usage_sums.values):
    ax.text(i, v + 2, str(v), ha='center')

# Display the chart
st.pyplot(fig)