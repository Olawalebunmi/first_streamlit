import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')

st.write("Hello")

st.set_page_config(page_title="Datahub Newbies Survey", page_icon=":bar_chart:", layout="wide")

st.title (":bar_chart: Data Analyst Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}<\style>', unsafe_allow_html=True)

datahub = "newbies.csv"

col1, col2, col3 = st.columns((0.3, 0.7, 0.7))
with col1:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by: \n {box_date}")

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
            help = "Click here to download the data as a csv file"
        )
    except NameError:
        st.error("Data not available for download.")

# Tools and Experience
with col3:
    try:
        fig2 = px.bar(
            datahub,
            x="experience",
            y="tools",
            labels={"experience": "experience"},
            title="Tools used and Years of Experience",
            hover_data=["experience"],
            template="seaborn",
            height=500,
             text_auto=True
        )
        st.plotly_chart(fig2, use_container_width=True)
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
            help = "Click here to download the data as a csv file"
        )
    except NameError:
        st.error("Data not available for download.")
# Divider
#st.divider()

col4, col5 = st.columns((0.7, 0.7))
with col4: 
    st.subheader("Proportion of Experience Levels")
# Group data by Experience and count entries
experience_counts = datahub["experience"].value_counts().reset_index()
experience_counts.columns = ["experience", "count"]

#create a pie chart
fig3 = px.pie(
    experience_counts, 
    values = "count", 
    names = "experience", 
    hole = 0.5
)
 # Update trace for better label placement
fig3.update_traces(text = datahub["experience"], textposition = "outside")

# Display the pie chart in Streamlit
st_plotly_chart(fig3,use_container_width=True)

cl4, cl5 = st.columns(2)
with cl4:
    with st.expander("Category_ViewData"):
         # Display data with background gradient
        st.write(datahub.style.background_gradient(cmap="Blues"))
        # Convert data to CSV for download
        csv = datahub.to_csv(index = False).encode('utf-8')
        st.download_button(
            label = "Download Data", data = csv, file_name="Category by Experience.csv", mime = "text/csv",
                           help = "Click here to download the data as csv file")

# Create a treemap
st.subheader("Experience Distribution Across Industries")
# Count occurrences of each combination of industry and experience
experience_counts = datahub.groupby(["motivation", "satisfaction","industry", "experience"]).size().reset_index(name="count"),
fig4 = px.treemap(
    experience_counts, 
    path = ["motivation", "satisfaction", "industry", "experience"],
    values = "count",
    template ="seaborn",
    color="experience",
    color_continous_scale="Viridis",
    height = 650
)
st.plotly_chart(fig4, use_container_width=True)

chart1, chart2 = st.columns((2))
with chart1:
    st.subheader("Motiivation of industry")
    fig = px.pie(experience_counts, values = "count", names = "motivation", template = "plotly_dark")
    fig.update_traces(text = experience_counts['Segment'], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

with chart2:
    st.subheader("Satisfaction of industry")
    fig = px.pie(experience_counts, values = "count", names = "Satisfaction", template = "plotly_dark")
    fig.update_traces(text = experience_counts['Satisfaction'], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

import plotly.figure_factory as ff
st.subheader(":point_right: Motivation level by Industry Summary")
with st.expander("Summary Table"):
    datahub_sample = datahub[0:5][["motivation", "satisfaction", "industry", "experience", "job_ease"]]
    fig = ff.create_table(datahub_sample, coloorscale = "cividis")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Satisfaction level by Industry Table")
    experience_counts["Satisfaction"] = experience_counts["Satisfaction"]
    industry = pd.pivot_table(data=experience_counts, values= "satisfaction", index = ["Motivation"], columns= "satisfaction")
    st.write(industry.style.background_gradient(cmap="Blues"))

# Create scatter plot
data1 = px.scatter(datahub, x = "satisfaction_numeric", y = "motivation_nnumeric")
data1['layout'].update(title="Relationship between Motivation and Satisfaction using scatter plot",
                       titlefont = dict(size=20),xaxis=dict(title="Satisfaction", titlefont=dict(size=19)),
                       yaxis=dict(title="Motivation", titlefont=dict(size=19)))
st.plotly_chart(data1,use_container_width=True)

with st.expander("View Data"):
    st.write(experience_counts.iloc[:50,1:20,2].style.background_graddient(cmap="Oranges"))

#Download original dataset
csv = datahub.to_csv(index = False).encoode('utf-8')
st.download_button('Download Data', data = csv, file_name = "Data.csv", mime = "text/csv")
