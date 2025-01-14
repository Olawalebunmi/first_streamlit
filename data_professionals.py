import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go


# Reading in data
df = pd.read_csv("newbies.csv", encoding ="utf-8")
st.set_page_config("layout = wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image = Image.open('Data Analyst.png')

col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image(image, width=100)

html_title = """
<style>
    .title-test {
    font-weight:bold;
    padding: Spx;
    border-radius:6px
    }
    </style>
    <center><h1 class="title-test">Data Analyst Survey Dashboard</h1></center>"""
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

#To view the data in the chart
_, view1, dwn1, view2, dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander = st.expander("Roles and Fields")
    data = datahub[["Role", "Field"]].groupby(by="Role")["Field"].sum()
    expander.write(data)

#downloading the data in form of csv
with dwn1:
    st.download_button("Get Data", data = data.to_csv().encode("utf-8"),
                       file_name="Role and Field.csv", mime="text/csv")

#Creating another chart
datahub["Month_Year"] = datahub["date"].dt.strftime("%b'%y")
result = datahub.groupby(by=datahub["date"])["Field"].sum().reset_index()

#with col5:
    #fig1 = px.line(result, x= "Month_Year", y = "Field", title = "Total Fields Over Time",
                   #template ="gridoff")
    #st.plotly_chart(fig1,use_container_width=True)

#with view2:
#expander = st.expander("Fields over Time or Monthly Sales")
    #data = result
    #expander.write(data)

#downloading the data in form of csv
#with dwn2:
    #st.download_button("Get Data", data = data.to_csv().encode("utf-8"),
                       #file_name="Total Field Over Time.csv", mime="text/csv")
    


#To add a straight line beloe chart
st.divider()

#fig3 = go.Figure()
#fig3.add_trace(go.Bar(x = result1)) = 

