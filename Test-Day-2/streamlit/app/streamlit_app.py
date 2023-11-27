import pymongo
import math
import pandas as pd
import streamlit as st
import plotly.express as px
#import numpy as np
#import plotly.figure_factory as ff

st.set_page_config(page_title="House Rent Dashboard",
                    page_icon=":bar_chart:",
                    layout="wide")

# Initialize connection.
# Uses st.cache_resource to only run once.

#MONGO_DETAILS = "mongodb://tesarally:contestor@test-day-2-mongodb:27017/"
MONGO_DETAILS = "mongodb://localhost:27017/"
@st.cache_resource
def init_connection():
   return pymongo.MongoClient(MONGO_DETAILS)

client = init_connection()

@st.cache_data(ttl=600)
def get_data():
   db = client.mockupdata
   items = db.waterdata.find()
   items = list(items)  # make hashable for st.cache_data
   return items


def get_metrix(items):
        items_frame = pd.DataFrame(items)
        items_frame = items_frame.reset_index(drop=False).rename({"index": "index"}, axis=1)
        items_frame = items_frame.drop(columns=['_id'])

        last_item = items_frame.iloc[-1]
        b_last_item = items_frame.iloc[-2]
        with st.container():
                st.subheader(f"Location At {last_item["Name"]} || Time : {last_item["Date"]} - {last_item["Month"]} - {last_item["Year"]}",divider=True)

                col1, col2, col3  = st.columns(3)
                col1.metric("WaterFront", f"{last_item["WaterDataFront"]} m", f"{b_last_item["WaterDataFront"]-last_item["WaterDataFront"]} m")
                col2.metric("WaterBack", f"{last_item["WaterDataBack"]} m", f"{b_last_item["WaterDataBack"]-last_item["WaterDataBack"]} m")
                col3.metric("WaterDrainRate", f"{last_item["WaterDrainRate"]} m3/s", f"{b_last_item["WaterDrainRate"]-last_item["WaterDrainRate"]} m3/s")

st.title(":bar_chart: Water Data Dashboard :bar_chart:")
st.markdown("""---""")
items = get_data()
get_metrix(items=items)
st.sidebar.header("Please Filter Here:")
items_frame = pd.DataFrame(items)
year = st.sidebar.selectbox("Select the Year:", options=['All'] + list(items_frame["Year"].unique()), index=0)
month = st.sidebar.selectbox("Select Month", options=['All'] + list(items_frame["Month"].unique()), index=0)
day = st.sidebar.selectbox("Select the Date:", options=['All'] + list(items_frame["Date"].unique()), index=0)
query = ""
if year != 'All':
    query += " Year == @year"
if month != 'All':
    query += " & Month == @month"
if day != 'All':
    query += " & Date == @day"

df_selection = items_frame if query == "" else items_frame.query(query)

df = df_selection
df = df.drop(columns=['_id'])
df

front_water = df_selection.iloc[:, 5:6]
back_water = df_selection.iloc[:, 6:7]
rate = df_selection.iloc[:, -1]
date = df_selection.iloc[:, 2:5]


front = df_selection.iloc[:, 5]
back = df_selection.iloc[:, 6]
rate = df_selection.iloc[:, -1]



# add title
st.markdown("""---""")
st.title(":bar_chart: WATER DRAIN RATE PER DAYS")
chart_data = pd.DataFrame({
    "DAYS": date.iloc[:, 0].values,
    "WATER RATE": rate.values,
})
st.bar_chart(chart_data, x="DAYS", y="WATER RATE", color="#008000")

st.markdown("""---""")
st.title(":bar_chart: WATER DRAIN RATE  PER MONTH")
chart_data = pd.DataFrame({
    "MONTH": date.iloc[:, 1].values,
    "WATER RATE": rate.values,
})
st.bar_chart(chart_data, x="MONTH", y="WATER RATE", color="#008000")

st.markdown("""---""")
st.title(":bar_chart: WATER DRAIN RATE  PER YEARS")
chart_data = pd.DataFrame({
    "YEARS": date.iloc[:, 2].values,
    "WATER RATE": rate.values,
})
st.bar_chart(chart_data, x="YEARS", y="WATER RATE", color="#008000")

# create st.metric for water front and back per years and month and days
st.markdown("""---""")