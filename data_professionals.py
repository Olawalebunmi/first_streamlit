import streamlit as st

#create a bold header
st.markdown("**#Data Analysis Report**", unsafe_allow_html=True)

st.markdown("**##Overview**" , unsafe_allow_html=True)

st.write("""
         In this report, we analyze the data analyst survey to identify current roles, years of experience in data related fields, tools mostly used, challenges and otherrelevent variables which will be discussed.
         Sixty-nine (69) respondents filled the form, and their responses will be use for the analysis.
         An exploratory data analysis will be conducted, along with relevant visualizations to gain deep insights into the raw data.
         The analysis will include findings on:
         - Current role with the highest number of respondents.
         - Current role and years spent in each field.
         - The number of current roles in each field.
         - Satisfaction level of people by their job roles.
         - Tools mostly use by professionals for analysis.
         - Industries that offer more job opportunities. 
         """)

