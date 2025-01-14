import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px

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
col1, col2 = st.columns([0.3, 0.7])
with col1:
    box_date = datetime.datetime.now().strftime("%d %B %Y")
    st.write(f"Last updated: **{box_date}**")

# Role and Field Chart
with col2:
    try:
        fig = px.bar(
            datahub,
            x="Current Role",
            y="Field",
            labels={"Field": "Field"},
            title="Role and Field of Analysts",
            hover_data=["Field"],
            template="plotly_white",
            height=500,
        )
        st.plotly_chart(fig, use_container_width=True)
    except KeyError as e:
        st.error(f"Missing required columns for chart: {e}")

# View and download grouped data
st.markdown("### Roles and Fields")
_, view1, dwn1 = st.columns([0.15, 0.7, 0.15])

with view1:
    expander = st.expander("View grouped data")
    try:
        grouped_data = datahub.groupby("Role")["Field"].sum()
        expander.write(grouped_data)
    except KeyError as e:
        st.error(f"Missing required columns for grouping: {e}")

with dwn1:
    try:
        csv_data = grouped_data.to_csv().encode("utf-8")
        st.download_button(
            "Download Data",
            data=csv_data,
            file_name="Role_and_Field.csv",
            mime="text/csv",
        )
    except NameError:
        st.error("Data not available for download.")

# Total Fields Over Time
st.markdown("### Fields Over Time")
try:
    datahub["Month_Year"] = datahub["date"].dt.strftime("%b'%y")
    result = datahub.groupby("Month_Year")["Field"].sum().reset_index()

    fig1 = px.line(
        result,
        x="Month_Year",
        y="Field",
        title="Total Fields Over Time",
        template="plotly_white",
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Expander for viewing data
    expander2 = st.expander("View Fields Over Time Data")
    expander2.write(result)

    # Download button for data
    st.download_button(
        "Download Time Data",
        data=result.to_csv().encode("utf-8"),
        file_name="Fields_Over_Time.csv",
        mime="text/csv",
    )
except KeyError as e:
    st.error(f"Missing required columns for time analysis: {e}")
except Exception as e:
    st.error(f"An error occurred while processing time data: {e}")

# Divider
st.divider()

# Placeholder for additional charts
st.markdown("### Additional Analysis (Placeholder)")
