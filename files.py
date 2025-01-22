import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import warnings
import plotly.figure_factory as ff

warnings.filterwarnings('ignore')
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

# Title
st.title(":bar_chart: Data Analyst Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}<\style>', unsafe_allow_html=True)

# Load data
datahub = pd.read_csv("newbies_numeric.csv")

# Last updated info
col1, col2, col3 = st.columns((0.3, 0.7, 0.7))
with col1:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by: \n {box_date}")

# Sidebar filters
st.sidebar.header("Choose your Filter: ")
tools = st.sidebar.multiselect("Pick your Tools", datahub["tools"].unique())
education = st.sidebar.multiselect("Choose your Education Level", datahub["education"].unique())
satisfaction = st.sidebar.selectbox("Choose Satisfaction Level", datahub["satisfaction"].unique())
industry = st.sidebar.selectbox("Choose your Industry", datahub["industry"].unique())

# Apply filters to the data
filtered_data = datahub
if tools:
    filtered_data = filtered_data[filtered_data["tools"].isin(tools)]
if education:
    filtered_data = filtered_data[filtered_data["education"].isin(education)]
if satisfaction:
    filtered_data = filtered_data[filtered_data["satisfaction"] == satisfaction]
if industry:
    filtered_data = filtered_data[filtered_data["industry"] == industry]

# Bar chart - Industry vs Tools
with col2:
    try:
        fig1 = px.bar(
            filtered_data,
            x="industry",
            y="tools",
            labels={"industry": "Industry", "tools": "Tools"},
            title="Industry and Tools used by Analysts",
            template="seaborn",
            height=400,
            text_auto=True
        )
        fig1.update_layout(title="Industry and Tools used by Analysts", barmode='group', showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    except KeyError as e:
        st.error(f"Missing required columns for chart: {e}")

# Bar chart - Tools vs Experience
with col3:
    try:
        fig2 = px.bar(
            filtered_data,
            x="experience",
            y="tools",
            labels={"experience": "Experience", "tools": "Tools"},
            title="Tools used and Years of Experience",
            template="seaborn",
            height=500,
            text_auto=True
        )
        fig2.update_layout(title="Tools used and Years of Experience", barmode='group', showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    except KeyError as e:
        st.error(f"Missing required columns for chart: {e}")

# Pie chart - Proportion of Experience Levels
col4, col5 = st.columns((0.7, 0.7))
with col4:
    st.subheader("Proportion of Experience Levels")
    experience_counts = filtered_data["experience"].value_counts().reset_index()
    experience_counts.columns = ["experience", "count"]
    fig3 = px.pie(
        experience_counts,
        values="count",
        names="experience",
        hole=0.5,
        title="Experience Distribution"
    )
    fig3.update_traces(text=experience_counts["experience"], textposition="outside")
    st.plotly_chart(fig3, use_container_width=True)

# Treemap - Experience Distribution Across Industries
st.subheader("Experience Distribution Across Industries")
experience_counts = filtered_data.groupby(["motivation", "satisfaction", "industry", "experience"]).size().reset_index(name="count")
try:
    fig4 = px.treemap(
        experience_counts,
        path=["motivation", "satisfaction", "industry", "experience"],
        values="count",
        template="seaborn",
        color="experience",
        color_continous_scale="Viridis",
        height=650
    )
    st.plotly_chart(fig4, use_container_width=True)
except KeyError as e:
    st.error(f"Missing required columns for chart: {e}")

# Motivation and Satisfaction Pie charts
chart1, chart2 = st.columns(2)
with chart1:
    st.subheader("Motivation by Industry")
    fig = px.pie(experience_counts, values="count", names="motivation", template="plotly_dark")
    fig.update_traces(text=experience_counts['motivation'], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)
with chart2:
    st.subheader("Satisfaction by Industry")
    fig = px.pie(experience_counts, values="count", names="satisfaction", template="plotly_dark")
    fig.update_traces(text=experience_counts['satisfaction'], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

# Scatter plot - Motivation vs Satisfaction
st.subheader(":point_right: Motivation vs Satisfaction Relationship")
data1 = px.scatter(filtered_data, x="satisfaction_numeric", y="motivation_numeric")
data1.update_layout(title="Relationship between Motivation and Satisfaction",
                    titlefont=dict(size=20),
                    xaxis=dict(title="Satisfaction", titlefont=dict(size=19)),
                    yaxis=dict(title="Motivation", titlefont=dict(size=19)))
st.plotly_chart(data1, use_container_width=True)

# Data Download button
csv = filtered_data.to_csv(index=False).encode('utf-8')
st.download_button('Download Data', data=csv, file_name="Filtered_Data.csv", mime="text/csv")
