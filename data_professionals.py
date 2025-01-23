import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px

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

st.header("Filters")
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

# Sidebar filters
st.sidebar.header("Choose your Filter: ")

# Sidebar multiselect with proper options
st.sidebar.header("Filter Options")
tools = st.sidebar.multiselect(
    "Pick your Tools",  # Label for the widget
    options=datahub['tools'].tolist(),  # Convert the 'Tools' column to a list
    default=None  # No default selection
)

# Display the selected tools
if tools:
    st.write("You selected:", tools)
else:
    st.write("No tools selected yet!")

# Filter the DataFrame based on selected tools (if necessary)
if tools:
    filtered_data = datahub[datahub['Tools'].isin(tools)]
    st.write("Filtered Data:")
    st.write(filtered_data)
else:
    st.write("Showing all data:")
    st.write(datahub)

col2 = st.columns([0.9])

# Industry and Tools chart
with col2[0]:
    try:
        fig1 = px.bar(
            filtered_data,
            x="Industry",
            y="Tools",
            labels={"Industry": "Industry", "Tools": "Tools"},
            title="Industry and Tools used by Analysts",
            hover_data=["Industry"],
            template="seaborn",
            height=400,
            text_auto=True
        )
        st.plotly_chart(fig1, use_container_width=True)
    except KeyError as e:
        st.error(f"Missing required columns for chart: {e}")

col3, col4, col5 = st.columns([0.1, 0.45, 0.45])

with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by: \n {box_date}")

# Role and Field of Analyst chart
with col4:
    try:
        fig2 = px.bar(
            filtered_data,
            x="Current Role",
            y="Field",
            labels={"Field": "Field", "Current Role": "Current Role"},
            title="Role and Field of Analyst",
            hover_data=["Field"],
            template="plotly",
            height=500
        )
        st.plotly_chart(fig2, use_container_width=True)
    except KeyError as e:
        st.error(f"Missing required columns for chart: {e}")