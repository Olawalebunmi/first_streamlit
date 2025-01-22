import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.figure_factory as ff
import warnings

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Datahub Newbies Survey",
    page_icon=":bar_chart:",
    layout="wide"
)

# Title and header setup
# Streamlit Page Configuration
st.set_page_config(page_title="Datahub Newbies Survey", page_icon=":bar_chart:", layout="wide")

# Adjust header font size using CSS
st.markdown("""
    <style>
        .css-18e3th9 {
            font-size: 32px !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)
st.markdown(
    '<style>div.block-container{padding-top:1rem;}</style>',
    unsafe_allow_html=True
)

# Load dataset
try:
    datahub = pd.read_csv("newbies_numeric.csv")
except FileNotFoundError:
    st.error("The file 'newbies_numeric.csv' was not found. Please upload the file.")
    st.stop()

# Sidebar filters
st.sidebar.header("Choose your Filter:")

# Filter for Tools
tools = st.sidebar.multiselect(
    "Pick your Tools:",
    options=datahub["tools"].unique() if "tools" in datahub.columns else [],
    default=[]
)

# Filter for Education
education = st.sidebar.multiselect(
    "Choose your Education Level:",
    options=datahub["education"].unique() if "education" in datahub.columns else [],
    default=[]
)

# Filter for Satisfaction
satisfaction = st.sidebar.multiselect(
    "Choose Satisfaction Level:",
    options=datahub["satisfaction"].unique() if "satisfaction" in datahub.columns else [],
    default=[]
)

# Filter for Industry
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

# Display last updated time
col1, col2, col3 = st.columns((0.3, 0.7, 0.7))
with col1:
    box_date = datetime.datetime.now().strftime("%d %B %Y")
    st.write(f"Last updated by:\n{box_date}")

# Bar chart for Industry and Tools
with col2:
    try:
        fig1 = px.bar(
            datahub,
            x="industry",
            y="tools",
            title="Industry and Tools used by Analysts",
            hover_data=["industry"],
            template="seaborn",
            height=400,
            text_auto=True
        )
        st.plotly_chart(fig1, use_container_width=True)
    except KeyError as e:
        st.error(f"Missing required columns for chart: {e}")

# Grouped data: Tools and Industry
st.markdown("### Tools and Industry")
_, view1, dwn1 = st.columns([0.15, 0.7, 0.15])
with view1:
    expander = st.expander("View grouped data")
    try:
        grouped_data = datahub.groupby("tools")["industry"].count()
        expander.write(grouped_data)
    except KeyError as e:
        st.error(f"Missing required columns for grouping: {e}")

with dwn1:
    try:
        csv_data = grouped_data.to_csv().encode("utf-8")
        st.download_button(
            label="Download Data",
            data=csv_data,
            file_name="Tools_and_Industry.csv",
            mime="text/csv",
            help="Click here to download the data as a CSV file"
        )
    except NameError:
        st.error("Data not available for download.")

# Pie chart for Experience levels
col4, col5 = st.columns((0.7, 0.7))
with col4:
    st.subheader("Proportion of Experience Levels")
    try:
        experience_counts = datahub["experience"].value_counts().reset_index()
        experience_counts.columns = ["experience", "count"]
        fig3 = px.pie(
            experience_counts,
            values="count",
            names="experience",
            hole=0.5
        )
        st.plotly_chart(fig3, use_container_width=True)
    except KeyError as e:
        st.error(f"Missing required column for pie chart: {e}")

# Treemap: Experience Distribution Across Industries
st.subheader("Experience Distribution Across Industries")
try:
    experience_counts = (
        datahub.groupby(["motivation", "satisfaction", "industry", "experience"])
        .size()
        .reset_index(name="count")
    )
    fig4 = px.treemap(
        experience_counts,
        path=["motivation", "satisfaction", "industry", "experience"],
        values="count",
        template="seaborn",
        color="experience",
        color_continuous_scale="Viridis",
        height=650
    )
    st.plotly_chart(fig4, use_container_width=True)
except KeyError as e:
    st.error(f"Missing required columns for treemap: {e}")

# Pie charts for Motivation and Satisfaction
chart1, chart2 = st.columns((2, 2))
with chart1:
    st.subheader("Motivation by Industry")
    try:
        fig5 = px.pie(
            experience_counts,
            values="count",
            names="motivation",
            template="plotly_dark"
        )
        st.plotly_chart(fig5, use_container_width=True)
    except KeyError as e:
        st.error(f"Missing required column for motivation pie chart: {e}")

with chart2:
    st.subheader("Satisfaction by Industry")
    try:
        fig6 = px.pie(
            experience_counts,
            values="count",
            names="satisfaction",
            template="plotly_dark"
        )
        st.plotly_chart(fig6, use_container_width=True)
    except KeyError as e:
        st.error(f"Missing required column for satisfaction pie chart: {e}")

# Scatter plot for Motivation vs Satisfaction
st.subheader("Relationship Between Motivation and Satisfaction")
try:
    scatter_fig = px.scatter(
        datahub,
        x="satisfaction_numeric",
        y="motivation_numeric",
        title="Motivation vs Satisfaction",
        labels={"satisfaction_numeric": "Satisfaction", "motivation_numeric": "Motivation"},
    )
    st.plotly_chart(scatter_fig, use_container_width=True)
except KeyError as e:
    st.error(f"Missing required columns for scatter plot: {e}")

# Data view and download
st.subheader("View and Download Data")
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
