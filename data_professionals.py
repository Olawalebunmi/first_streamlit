import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import warnings

warnings.filterwarnings("ignore")

# Page configuration
st.set_page_config(
    page_title="Datahub Newbies Survey",
    page_icon=":bar_chart:",
    layout="wide"
)




# Sidebar filters
st.sidebar.header("Choose your Filter:")

# Adjust header font size using CSS
st.markdown("""
    <style>
        .css-18e3th9 {
            font-size: 32px !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Load dataset
try:
    datahub = pd.read_csv("newbies_numeric.csv")
except FileNotFoundError:
    st.error("The file 'newbies_numeric.csv' was not found. Please upload the file.")
    st.stop()


# Title and layout
st.title("Data Analyst Dashboard")
st.markdown("---")  # Horizontal line for separation

# KPI section with small compact columns
kpi_cols = st.columns(3, gap="small")  # Use small gap for compact display


# KPI calculations
num_respondents = datahub['id'].nunique()

num_industry= datahub['industry'].nunique()

num_tools=datahub["tools"].nunique()


col1, col2, col3 = st.columns(3)

# KPI Display
with kpi_cols[0]:
    st.metric("Number of Respondents", num_respondents)

with kpi_cols[1]:
    st.metric("Number of Industry", num_industry)

with kpi_cols[2]:
    st.metric("Number of Tools", num_tools)



# Sidebar filters & widget
# Sidebar filters
tools = st.sidebar.multiselect(
    "Pick your Tools:",
    options=datahub["tools"].unique() if "tools" in datahub.columns else [],
    default=[]
)

education = st.sidebar.multiselect(
    "Choose your Education Level:",
    options=datahub["education"].unique() if "education" in datahub.columns else [],
    default=[]
)

satisfaction = st.sidebar.multiselect(
    "Choose Satisfaction Level:",
    options=datahub["satisfaction"].unique() if "satisfaction" in datahub.columns else [],
    default=[]
)

industry = st.sidebar.multiselect(
    "Choose your Industry:",
    options=datahub["industry"].unique() if "industry" in datahub.columns else [],
    default=[]
)

# Apply filters
filtered_data = datahub.copy()
if tools:
    filtered_data = filtered_data[filtered_data["tools"].isin(tools)]
if education:
    filtered_data = filtered_data[filtered_data["education"].isin(education)]
if satisfaction:
    filtered_data = filtered_data[filtered_data["satisfaction"].isin(satisfaction)]
if industry:
    filtered_data = filtered_data[filtered_data["industry"].isin(industry)]

# Display last updated time near the sidebar
st.sidebar.markdown("#### Last Updated:")
st.sidebar.write(datetime.datetime.now().strftime("%d %B %Y"))

# Chart 1: Industry and Tools
try:
    fig1 = px.bar(
        filtered_data,  # Use filtered data
        x="industry",
        y="tools",
        title="Industry and Tools used by Analysts",
        hover_data=["industry"],
        template="seaborn",
        text_auto=True
    )
except KeyError as e:
    fig1 = None
    st.error(f"Missing columns for 'Industry and Tools' chart: {e}")

# Chart 2: Tools and Experience
try:
    fig2 = px.bar(
        filtered_data,  # Use filtered data
        x="experience",
        y="tools",
        title="Tools used and Years of Experience",
        hover_data=["experience"],
        template="seaborn",
        text_auto=True
    )
except KeyError as e:
    fig2 = None
    st.error(f"Missing columns for 'Tools and Experience' chart: {e}")

# Display Chart Pair 1
#st.title("Data Analyst Dashboard")
#st.title("### Data Analyst Dashboard")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)

# Data view and download
#st.markdown("##View and Download Data")
# source data for tools and experience

#_view1, dwn1, view2, dwn2 = ([0.15,0.20,0.20,0.20])

#with view1:
    #expander = st.expander("Tools and Industry")
    #data = datahub[["tools", "industry"]].groupby(by="tools")["industry"].sum()
    #expander.write(datahub)


# Filter Data
filtered_data = datahub.copy()

if tools:
    filtered_data = filtered_data[filtered_data["tools"].isin(tools)]

if industry:
    filtered_data = filtered_data[filtered_data["experience"].isin(industry)]

# Display Filtered Table
st.title("Filtered Table: Tools and Experience")
if filtered_data.empty:
    st.warning("No data available for the selected filters.")
else:
    st.write(filtered_data)

# Chart 3: Proportion of Experience Levels
try:
    experience_counts = filtered_data["experience"].value_counts().reset_index()  # Use filtered data
    experience_counts.columns = ["experience", "count"]
    fig3 = px.pie(
        experience_counts,
        values="count",
        names="experience",
        title="Proportion of Experience Levels",
        hole=0.5
    )
except KeyError as e:
    fig3 = None
    st.error(f"Missing column for 'Experience Levels' pie chart: {e}")

# Chart 4: Experience Distribution Across Industries
try:
    experience_dist = (
        filtered_data.groupby(["motivation", "satisfaction", "industry", "experience"])  # Use filtered data
        .size()
        .reset_index(name="count")
    )
    fig4 = px.treemap(
        experience_dist,
        path=["motivation", "satisfaction", "industry", "experience"],
        values="count",
        title="Experience Distribution Across Industries",
        template="seaborn",
        color="experience",
        color_continuous_scale="Viridis"
    )
except KeyError as e:
    fig4 = None
    st.error(f"Missing columns for 'Experience Distribution' treemap: {e}")

# Display Chart Pair 2
#st.markdown("### Proportion of Experience Levels and Experience Distribution")
col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(fig3, use_container_width=True)
with col4:
    st.plotly_chart(fig4, use_container_width=True)

# Chart 5: Motivation by Industry
try:
    fig5 = px.pie(
        experience_dist,
        values="count",
        names="motivation",
        title="Motivation by Industry",
        template="plotly_dark"
    )
except KeyError as e:
    fig5 = None
    st.error(f"Missing column for 'Motivation by Industry' pie chart: {e}")

# Chart 6: Satisfaction by Industry
try:
    fig6 = px.pie(
        experience_dist,
        values="count",
        names="satisfaction",
        title="Satisfaction by Industry",
        template="plotly_dark"
    )
except KeyError as e:
    fig6 = None
    st.error(f"Missing column for 'Satisfaction by Industry' pie chart: {e}")

# Display Chart Pair 3
#st.markdown("### Motivation and Satisfaction by Industry")
col5, col6 = st.columns(2)
with col5:
    st.plotly_chart(fig5, use_container_width=True)
with col6:
    st.plotly_chart(fig6, use_container_width=True)

# Data view and download
#st.markdown("##View and Download Data")
with st.expander("View Data"):
    try:
        st.write(filtered_data)  # Use filtered data
    except Exception as e:
        st.error(f"Error displaying data: {e}")

    try:
        csv = filtered_data.to_csv(index=False).encode("utf-8")  # Use filtered data
        st.download_button(
            label="Download Filtered Dataset",
            data=csv,
            file_name="filtered_data.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"Error preparing data for download: {e}")

# Scatter Plot: Motivation vs Satisfaction
#st.markdown("### Scatter Plot: Motivation vs Satisfaction")
try:
    scatter_fig = px.scatter(
        filtered_data,  # Use filtered data
        x="satisfaction_numeric",
        y="motivation_numeric",
        title="Relationship Between Motivation and Satisfaction",
        labels={"satisfaction_numeric": "Satisfaction", "motivation_numeric": "Motivation"}
    )
    st.plotly_chart(scatter_fig, use_container_width=True)
except KeyError as e:
    st.error(f"Missing columns for scatter plot: {e}")
