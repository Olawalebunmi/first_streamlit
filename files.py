import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.figure_factory as ff
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Streamlit Page Configuration
st.set_page_config(page_title="Datahub Newbies Survey", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart: Data Analyst Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Load the dataset
try:
    datahub = pd.read_csv("newbies.csv")
except FileNotFoundError:
    st.error("The file 'newbies.csv' was not found. Please upload the correct file.")
    st.stop()

# Display last update time
col1, col2, col3 = st.columns((0.3, 0.7, 0.7))
with col1:
    box_date = datetime.datetime.now().strftime("%d %B %Y")
    st.write(f"Last updated by: \n{box_date}")

# Sidebar Filters
st.sidebar.header("Choose your Filter:")
tools = st.sidebar.multiselect("Pick your Tools:", datahub["tools"].unique())
education = st.sidebar.multiselect("Choose your Education Level:", datahub["education"].unique())
satisfaction = st.sidebar.multiselect("Choose Satisfaction Level:", datahub["satisfaction"].unique())
industry = st.sidebar.multiselect("Choose your Industry:", datahub["industry"].unique())

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

# Visualization: Industry and Tools
with col2:
    if not filtered_data.empty:
        fig1 = px.bar(
            filtered_data,
            x="industry",
            y="tools",
            title="Industry and Tools used by Analysts",
            hover_data=["industry"],
            template="seaborn",
            height=400,
            text_auto=True
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

# Visualization: Tools and Experience
with col3:
    if not filtered_data.empty:
        fig2 = px.bar(
            filtered_data,
            x="experience",
            y="tools",
            title="Tools used and Years of Experience",
            hover_data=["experience"],
            template="seaborn",
            height=500,
            text_auto=True
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

# Pie Chart: Proportion of Experience Levels
col4, col5 = st.columns((0.7, 0.7))
with col4:
    st.subheader("Proportion of Experience Levels")
    if not filtered_data.empty:
        experience_counts = filtered_data["experience"].value_counts().reset_index()
        experience_counts.columns = ["experience", "count"]
        fig3 = px.pie(
            experience_counts,
            values="count",
            names="experience",
            hole=0.5,
            title="Experience Levels Distribution",
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

# Treemap: Experience Distribution Across Industries
st.subheader("Experience Distribution Across Industries")
if not filtered_data.empty:
    grouped_data = (
        filtered_data.groupby(["motivation", "satisfaction", "industry", "experience"])
        .size()
        .reset_index(name="count")
    )
    fig4 = px.treemap(
        grouped_data,
        path=["motivation", "satisfaction", "industry", "experience"],
        values="count",
        color="experience",
        color_continuous_scale="Viridis",
        height=650,
        title="Treemap of Experience Distribution",
    )
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.warning("No data available for the selected filters.")

# Summary Table: Motivation Level by Industry
st.subheader(":point_right: Motivation Level by Industry Summary")
with st.expander("Summary Table"):
    if not filtered_data.empty:
        datahub_sample = filtered_data[
            ["motivation", "satisfaction", "industry", "experience", "job_ease"]
        ].head(5)
        fig5 = ff.create_table(datahub_sample, colorscale="cividis")
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

# Scatter Plot: Relationship between Motivation and Satisfaction
st.subheader("Relationship between Motivation and Satisfaction")
if not filtered_data.empty:
    if "satisfaction_numeric" in filtered_data.columns and "motivation_numeric" in filtered_data.columns:
        fig6 = px.scatter(
            filtered_data,
            x="satisfaction_numeric",
            y="motivation_numeric",
            title="Motivation vs Satisfaction",
        )
        st.plotly_chart(fig6, use_container_width=True)
    else:
        st.warning("The columns 'satisfaction_numeric' and 'motivation_numeric' are missing.")
else:
    st.warning("No data available for the selected filters.")

# Download Filtered Data
csv = filtered_data.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download Filtered Data",
    data=csv,
    file_name="Filtered_Data.csv",
    mime="text/csv",
    help="Download the filtered data as a CSV file.",
)
