import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px


import plotly.graph_objects as go


# Reading in data
datahub = "newbies.csv"
st.set_page_config("layout = wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
#image = Image.open "Data Analyst.png"

col2 = st.columns([0.9])


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

#creating filter
# Create for tools
st.sidebar.header("Choose your Filter: ")
tools = st.sidebar.multiselect("Pick your Tools", datahub["tools"].unique())

#create for education
st.sidebar.header("choose your filter: ")
education = st.sidebar.multiselect("Choose your Education Level", datahub["education"].unique())

#create for satisfaction
satisfaction = ("Choose Satisfaction Level", datahub["satisfaction"].unique())

#create for sindustry
industry = ("Choose your Industry", datahub["industry"].unique())

# Industry andTools
with col2:
    try:
        fig1= px.bar(
            datahub,
            x="Industry",
            y="Tools",
            labels={"industry": "industry"},
            title="Industry and Tools used by Analysts",
            hover_data=["industry"],
            template="seaborn",
            height=400,
             text_auto=True
        )
        st.plotly_chart(fig1, use_container_width=True)
    except KeyError as e:
        st.error(f"Missing required columns for chart: {e}")



with col2:
    st.markdown(html_title, unsafe_allow_html=True)

col3, col4, col5 = st.columns([0.1, 0.45, 0.45])

with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by: \n {box_date}")

with col4:
    fig = px.bar(datahub, x = "Current Role", y = "Field", labels = {"Field" : "Field"},
                 title = "Role and Field of Analyst", hover_data = ["Field"],
                 template= "gridoff",height=500)
    st.plotly_chart(fig,use_container_width=True)
    


import matplotlib.pyplot as plt


# Page configuration
st.set_page_config(page_title="Data Analyst Dashboard", layout="wide")

# Reading in data
try:
    datahub = pd.read_csv("newbies.csv", encoding="utf-8")
    #datahub["date"] = pd.to_datetime(datahub["date"])  # Ensure 'date' is in datetime format
except FileNotFoundError:
    st.error("The file 'newbies.csv' was not found. Please ensure it is in the correct directory.")
    st.stop()  # Stop execution if the file is missing
except Exception as e:
    st.error(f"An error occurred while reading the CSV file: {e}")
    st.stop()

# Customizing page style
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Displaying an Image
try:
    image = Image.open('Data Analyst.png')
    st.image(image, width=100)
except FileNotFoundError:
    st.warning("Image file 'Data Analyst.png' not found. Skipping image display.")

# Dashboard Title
st.markdown("<center><h1>Data Analyst Survey Dashboard</h1></center>", unsafe_allow_html=True)

# Date of last update
col1, col2, col3 = st.columns([0.3, 0.7, 0.7])
with col1:
    box_date = datetime.datetime.now().strftime("%d %B %Y")
    st.write(f"Last updated: **{box_date}**")

# Role and Field Chart
with col2:
    try:
        fig = px.bar(
            datahub,
            x="industry",
            y="tools",
            labels={"industry": "industry"},
            title="Industry and Tools of Analysts",
            hover_data=["industry"],
            template="plotly_white",
            height=500,
        )
        st.plotly_chart(fig, use_container_width=True)
    except KeyError as e:
        st.error(f"Missing required columns for chart: {e}")

# View and download grouped data
st.markdown("### Tools and Industry")
_, view1, dwn1 = st.columns([0.15, 0.7, 0.15])

with view1:
    expander = st.expander("View grouped data")
    try:
        grouped_data = datahub.groupby("tools")["industry"].sum()
        expander.write(grouped_data)
    except KeyError as e:
        st.error(f"Missing required columns for grouping: {e}")

with dwn1:
    try:
        csv_data = grouped_data.to_csv().encode("utf-8")
        st.download_button(
            "Download Data",
            data=csv_data,
            file_name="Tools_and_Industry.csv",
            mime="text/csv",
        )
    except NameError:
        st.error("Data not available for download.")

# Tools and Experience
with col3:
    try:
        fig = px.bar(
            datahub,
            x="experience",
            y="tools",
            labels={"experience": "experience"},
            title="Tools used and Years of Experience",
            hover_data=["experience"],
            template="plotly_white",
            height=500,
        )
        st.plotly_chart(fig, use_container_width=True)
    except KeyError as e:
        st.error(f"Missing required columns for chart: {e}")

# View and download grouped data
st.markdown("### Tools and Experience")
_, view2, dwn2 = st.columns([0.15, 0.7, 0.15])

with view2:
    expander = st.expander("View grouped data")
    try:
        grouped_data = datahub.groupby("tools")["experience"].sum()
        expander.write(grouped_data)
    except KeyError as e:
        st.error(f"Missing required columns for grouping: {e}")

with dwn2:
    try:
        csv_data = grouped_data.to_csv().encode("utf-8")
        st.download_button(
            "Download Data",
            data=csv_data,
            file_name="Tools_and_Experience.csv",
            mime="text/csv",
        )
    except NameError:
        st.error("Data not available for download.")
# Divider
st.divider()


