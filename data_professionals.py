import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import numpy as np
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


# Dashboard Title
st.markdown("<center><h1>Data Analyst Survey Dashboard</h1></center>", unsafe_allow_html=True)
st.write("filter")
# Date of last update
col1, col2, col3 = st.columns([0.3, 0.7, 0.7])
with col1:
    box_date = datetime.datetime.now().strftime("%d %B %Y")
    st.write(f"Last updated: **{box_date}**")


# Display filtered data in the sidebar
st.sidebar.subheader("Filtered Data")
st.sidebar.dataframe("filtered_data")

# Filter data based on selection
if selected_tools:
    filtered_data = datahub[datahub['tools'].isin(selected_tools)]
else:
    filtered_data = datahub


# Display filtered data as a table
st.write("Filtered Data:")
st.write(filtered_data)

