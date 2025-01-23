import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

st.write("Hello there")
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
        datahub,
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
        datahub,
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
st.title("Data Analyst Dashboard")
st.markdown("### Industry and Tools vs Tools and Experience")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Proportion of Experience Levels
try:
    experience_counts = datahub["experience"].value_counts().reset_index()
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
        datahub.groupby(["motivation", "satisfaction", "industry", "experience"])
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
st.markdown("### Proportion of Experience Levels and Experience Distribution")
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
st.markdown("### Motivation and Satisfaction by Industry")
col5, col6 = st.columns(2)
with col5:
    st.plotly_chart(fig5, use_container_width=True)
with col6:
    st.plotly_chart(fig6, use_container_width=True)

# Data view and download
st.markdown("### View and Download Data")
with st.expander("View Data"):
    try:
        st.write(filtered_data)
    except Exception as e:
        st.error(f"Error displaying data: {e}")

    try:
        csv = filtered_data.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Filtered Dataset",
            data=csv,
            file_name="filtered_data.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"Error preparing data for download: {e}")

# Scatter Plot: Motivation vs Satisfaction
st.markdown("### Scatter Plot: Motivation vs Satisfaction")
try:
    scatter_fig = px.scatter(
        datahub,
        x="satisfaction_numeric",
        y="motivation_numeric",
        title="Relationship Between Motivation and Satisfaction",
        labels={"satisfaction_numeric": "Satisfaction", "motivation_numeric": "Motivation"}
    )
    st.plotly_chart(scatter_fig, use_container_width=True)
except KeyError as e:
    st.error(f"Missing columns for scatter plot: {e}")

# Data view and download
st.markdown("### View and Download Data")
with st.expander("View Data"):
    try:
        st.write(datahub.style.background_gradient(cmap="Blues"))
    except Exception as e:
        st.error(f"Error displaying data: {e}")

    try:
        csv = datahub.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Full Dataset",
            data=csv,
            file_name="newbies_data.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"Error preparing data for download: {e}")

