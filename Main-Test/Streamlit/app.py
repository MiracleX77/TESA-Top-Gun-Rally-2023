from datetime import datetime, timedelta
import os 
import pymongo
import math
import pandas as pd
import streamlit as st
import plotly.express as px
import time
import pydeck as pdk
from PIL import Image
from streamlit_tailwind import st_tw
import altair as alt


backGround = """
<style>
    /* Targeting the root container of Streamlit */
    .stApp {
        background: linear-gradient(to right, #61045F, #1A2980); /* Blue gradient */
    }
</style>
"""

# Inject the custom CSS
st.markdown(backGround, unsafe_allow_html=True)


# ---- MAINPAGE ----
value = st_tw(
    text="""
            <div class="bg-gray-900 p-4 h-48 rounded-xl flex items-center justify-center">
                <span class="text-center font-mono text-3xl text-white italic">WELCOME TO HORIX DASHBOARD</span>
            </div>
        """,
    height=192  # 4 x specified height in tailwind
)

button = st_tw(
    text="""
        <div class="p-4 md:p-8 bg-gray-900 shadow-lg rounded-lg">
            <h1 class="text-xl md:text-2xl font-bold text-gray-200 text-center">INTRODUCTION</h1>
            <p class="mt-2 text-gray-200">
                This website is dedicated to exploring the innovative application of 
                ESP32 technology for precise water level monitoring. Our primary objective 
                is to develop reliable flood prediction models for Ubon ratchathani . 
                By leveraging advanced sensor data and analytics, we aim to provide accurate 
                and timely forecasts to mitigate the impact of flooding and ensure the safety and
                  preparedness of the northeastern region community.
            </p>
        </div>
        """,
    height=200,
    key="button1"
)

button5 = st_tw(
    text="""
    
        <div class="flex justify-center">
            <button class="bg-gray-900 hover:bg-pink-700 text-white font-mono py-2 px-4 w-full rounded">
                Water Data Today
            </button>
        </div>  
        """,
    height=40,  # Adjust height as needed
    key="button5"
)






def init_connection():
    username = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
    password = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')
    mongo  = pymongo.MongoClient(f"mongodb://{username}:{password}@main-test-mongo-1:27017/")
    return mongo


client = init_connection()

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.


def get_data():
    db = client.TGR
    items = db.water.find()
    items = list(items)  # make hashable for st.cache_data
    return items

def get_sensor_data():
    db = client.TGR
    items = db.sensor.find()
    items = list(items)  # make hashable for st.cache_data
    return items

def get_predict_data():
    db = client.TGR
    items = db.predict_water.find()
    items = list(items)  # make hashable for st.cache_data
    return items


# custom sidebar
# CSS to inject contained in a multiline string


# time for refrest
refresh_interval = 2

# create a title use styles


items = get_data()
items_sensor = get_sensor_data()
items_predict = get_predict_data()

items_frame = pd.DataFrame(items)
items_frame = items_frame.drop(columns=["_id"])

items_frame_sensor = pd.DataFrame(items_sensor)
items_frame_sensor = items_frame_sensor.drop(columns=["_id"])

items_frame_predict = pd.DataFrame(items_predict)
items_frame_predict = items_frame_predict.drop(columns=["_id"])


merged_frame = pd.merge(items_frame, items_frame_sensor[['sensor_id', 'name', 'lat', 'long']], on='sensor_id')
final_frame = merged_frame[['sensor_id', 'name', 'water_height', 'create_on', 'status', 'lat', 'long']]
final_frame = final_frame.rename(columns={'name': 'sensor_name'})
final_frame = final_frame.drop(columns=['create_on'])
    
merged_frame1 = pd.merge(items_frame_predict, items_frame_sensor[['sensor_id', 'name', 'lat', 'long']], on='sensor_id')
final_frame_predict = merged_frame1[['sensor_id', 'name', 'water_height', 'create_on', 'status', 'lat', 'long']]
final_frame_predict = final_frame_predict.rename(columns={'name': 'sensor_name'})
final_frame_predict = final_frame_predict.drop(columns=['create_on'])

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #1f2937;
    }
</style>
""", unsafe_allow_html=True)

last_data = final_frame.tail(2)

last_data_status = last_data.iloc[1]["status"]
# กำหนดสถานะและรหัสสี
if last_data_status == "DANGER":
    status_color = "#dc3545"  # สีแดง
    last_data_status = "DANGER"
    text_color = "#FFFFFF"    # สีขาว
elif last_data_status == "WARNING":
    status_color = "#ffc107"  # สีเหลือง
    last_data_status = "WARNING"
    text_color = "#000000"    # สีดำสำหรับความเข้ากันได้ดีกับสีเหลือง
else:
    status_color = "#198754"
    last_data_status = "NORMAL"
    text_color = "#FFFFFF"    # สีขาว

image = Image.open('./image/Thammasat_University_icon.png')
st.sidebar.image(image, caption='',width=200) 
st.sidebar.header("Filter Data:")


col1, col2, col3= st.columns(3)
col1.metric("sensor name", last_data.iloc[1]["sensor_name"])
col2.metric("Today", f"{last_data.iloc[1]['water_height']} m ", f"{last_data.iloc[1]['water_height']-last_data.iloc[0]['water_height']} m ","inverse")
col3.markdown(f"""
    <div style='background-color: {status_color}; color: {text_color}; 
    padding: 1px; border-radius: 10px; text-align: center; font-size: 0.7em; font-family: 'Roboto', sans-serif;'>
        <h1 style='margin: 0;'>{last_data_status}</h1>
    </div>
    """, unsafe_allow_html=True)

current_date = datetime.now().date()
def calculate_dates_per_sensor(df, current_date):
    df['date'] = None  # สร้างคอลัมน์ใหม่สำหรับวันที่
    for sensor_id in df['sensor_id'].unique():
        sensor_rows = df[df['sensor_id'] == sensor_id]
        last_date = current_date - timedelta(days=len(sensor_rows) - 1)
        date_range = [last_date + timedelta(days=x) for x in range(len(sensor_rows))]
        df.loc[df['sensor_id'] == sensor_id, 'date'] = date_range
    return df
final_frame_with_dates = calculate_dates_per_sensor(final_frame, current_date)

# Existing filters
sensor_name = st.sidebar.selectbox(
    "Select Sensor ID:", options=['All'] + list(final_frame["sensor_name"].unique()), index=0)
status = st.sidebar.selectbox(
    "Select Status:", options=['All'] + list(final_frame["status"].unique()), index=0)
start_date = st.sidebar.date_input('Start date', datetime(2022, 1, 1))
end_date = st.sidebar.date_input('End date', datetime.now().date())

# New selectbox for choosing the graph type
# st.sidebar.header("Select Water Data:")
graph_type = st.sidebar.selectbox(
    "Select Water Data:", ['WATER LEVEL PER WEEK', 'WATER LEVEL PREDICT', 'UBON RATCHATHANI MAP'])


# Filter the data based on the sidebar selections
# Start with a condition that includes all data
filter_condition = (final_frame["date"] >= start_date) & (final_frame["date"] <= end_date)

if sensor_name != 'All':
    filter_condition = filter_condition & (final_frame["sensor_name"] == sensor_name)
if status != 'All':
    filter_condition = filter_condition & (final_frame["status"] == status)

# Apply the filter to the DataFrame
filtered_data = final_frame.loc[filter_condition]
button = st_tw(
    text="""
        <div class="flex justify-center">
            <button class="bg-gray-900 hover:animate-pulse text-white font-mono py-2 w-full rounded bg-gray-900">
                Filter Data Selected
            </button>
        </div>
        """,
    height=40,
    key="button2"   # Adjust height as needed
)

st.dataframe(filtered_data)

# show filtered data


# Display the selected graph type
if graph_type == 'WATER LEVEL PER WEEK':
    st.markdown("""---""")

    button = st_tw(
        text="""
             <div class="flex justify-center">
            <button class="hover:animate-pulse text-white font-mono py-2 w-full rounded bg-gray-900 ">
                WATER LEVEL PER WEEK
            </button>
        </div>
            """,
        height=50,
        key="button3"   # Adjust height as needed
    )

    # Use filtered_data instead of items_frame
    water_height_filtered = filtered_data['water_height']
    create_on_filtered = filtered_data['date']
    status_filtered = filtered_data['status']

    chart_data_front = pd.DataFrame({
        # to second
        "DATE": create_on_filtered.values,
        "WATER LEVEL": water_height_filtered.values,
        "STATUS": status_filtered.values
    })
    row = chart_data_front.shape
    
    if(row[0] > 8):
        chart_data_front_1 = chart_data_front.iloc[-7:]
        
        col1, col2, col3 = st.columns(3)
        col4,col5,col6,col7 = st.columns(4)
        for i in range(7):
            value = chart_data_front_1.iloc[i, 1]
            if(i == 0):
                b_value = chart_data_front.iloc[-8, 1]
            else:
                b_value = chart_data_front_1.iloc[i-1, 1]
            col = eval(f"col{i+1}")  
            col.metric(str(chart_data_front_1.iloc[i, 0]),value, f"{str(value-b_value)} m")
        line_chart = alt.Chart(chart_data_front_1).mark_line(
        color="#1e40af"  # สีของเส้น
        ).encode(
            x='DATE:T',  # กำหนดชนิดข้อมูลเป็นเวลา
            y=alt.Y('WATER LEVEL:Q', scale=alt.Scale(domain=[
                80,
                180
            ]))  # กำหนดชนิดข้อมูลเป็นตัวเลขและสเกลของแกน Y
        )

        # สร้างกราฟพื้นที่สำหรับเติมสีใต้เส้น
        area_chart = alt.Chart(chart_data_front_1).mark_area(
            color="#1e40af",  # สีของพื้นที่
            opacity=0.3  # ความโปร่งแสงของสี
        ).encode(
            x='DATE:T',
            y='WATER LEVEL:Q'
        )

        # รวมกราฟเส้นและกราฟพื้นที่
        final_chart = area_chart + line_chart

        # แสดงกราฟใน Streamlit
        st.altair_chart(final_chart, use_container_width=True)
    else:
        chart_data_front_1 = chart_data_front.iloc[-row[0]:]
        line_chart = alt.Chart(chart_data_front_1).mark_line(
        color="#1e40af"  # สีของเส้น
        ).encode(
            x='DATE:T',  # กำหนดชนิดข้อมูลเป็นเวลา
            y=alt.Y('WATER LEVEL:Q', scale=alt.Scale(domain=[
                80,
                180
            ]))  # กำหนดชนิดข้อมูลเป็นตัวเลขและสเกลของแกน Y
        )

        # สร้างกราฟพื้นที่สำหรับเติมสีใต้เส้น
        area_chart = alt.Chart(chart_data_front_1).mark_area(
            color="#1e40af",  # สีของพื้นที่
            opacity=0.3  # ความโปร่งแสงของสี
        ).encode(
            x='DATE:T',
            y='WATER LEVEL:Q'
        )

        # รวมกราฟเส้นและกราฟพื้นที่
        final_chart = area_chart + line_chart

        # แสดงกราฟใน Streamlit
        st.altair_chart(final_chart, use_container_width=True)

    # Display a WATER FRONT AND BACK PER MONTH
    st.markdown("""---""")


elif graph_type == 'WATER LEVEL PREDICT':
    st.markdown("""---""")
    
    button = st_tw(
        text="""
             <div class="flex justify-center">
            <button class="hover:animate-pulse text-white font-mono py-2 w-full rounded bg-gray-900 ">
                WATER LEVEL PREDICT
            </button>
        </div>
            """,
        height=50,
        key="button3"   # Adjust height as needed
    )
    def calculate_dates_per_sensor1(df, current_date):
        df['date'] = None  # สร้างคอลัมน์ใหม่สำหรับวันที่
        for sensor_id in df['sensor_id'].unique():
            sensor_rows = df[df['sensor_id'] == sensor_id]
            start_date = current_date + timedelta(days=1)
        # Generate the date range starting from the current date
            date_range = [start_date + timedelta(days=x) for x in range(len(sensor_rows))]
            df.loc[df['sensor_id'] == sensor_id, 'date'] = date_range
        return df
    final_frame_with_dates1 = calculate_dates_per_sensor1(final_frame_predict, current_date)
    

    water_height_filtered1 = final_frame_with_dates1['water_height']
    create_on_filtered1 = final_frame_with_dates1['date']
    status_filtered1 = final_frame_with_dates1['status']

    chart_data_front1 = pd.DataFrame({
        # to second
        "DATE": create_on_filtered1.values,
        "WATER LEVEL": water_height_filtered1.values,
        "STATUS": status_filtered1.values
    })
    row1 = chart_data_front1.shape
    
    if(row1[0] >= 5):
        chart_data_front_11 = chart_data_front1.iloc[-5:]
        
        coll1, coll2= st.columns(2)
        coll3,coll4,coll5= st.columns(3)
        chart_data_front_11.iloc[4,0]
        for i in range(5):
            value = chart_data_front_11.iloc[i, 1]
            if(i == 0):
                b_value = last_data.iloc[1]['water_height']
            else:
                b_value = chart_data_front_11.iloc[i-1, 1]
            col = eval(f"coll{i+1}")  
            col.metric("Time", value, f"{str(value-b_value)} m")

            
        line_chart1 = alt.Chart(chart_data_front_11).mark_line(
        color="#1e40af"  # สีของเส้น
        ).encode(
            x='DATE:T',  # กำหนดชนิดข้อมูลเป็นเวลา
            y=alt.Y('WATER LEVEL:Q', scale=alt.Scale(domain=[
                80,
                180
            ]))  # กำหนดชนิดข้อมูลเป็นตัวเลขและสเกลของแกน Y
        )

        # สร้างกราฟพื้นที่สำหรับเติมสีใต้เส้น
        area_chart1 = alt.Chart(chart_data_front_11).mark_area(
            color="#1e40af",  # สีของพื้นที่
            opacity=0.3  # ความโปร่งแสงของสี
        ).encode(
            x='DATE:T',
            y='WATER LEVEL:Q'
        )

        # รวมกราฟเส้นและกราฟพื้นที่
        final_chart1 = area_chart1 + line_chart1

        # แสดงกราฟใน Streamlit
        st.altair_chart(final_chart1, use_container_width=True)
    else:
        chart_data_front_11 = chart_data_front1.iloc[-row1[0]:]
        line_chart1 = alt.Chart(chart_data_front_11).mark_line(
        color="#1e40af"  # สีของเส้น
        ).encode(
            x='DATE:T',  # กำหนดชนิดข้อมูลเป็นเวลา
            y=alt.Y('WATER LEVEL:Q', scale=alt.Scale(domain=[
                80,
                180
            ]))  # กำหนดชนิดข้อมูลเป็นตัวเลขและสเกลของแกน Y
        )

        # สร้างกราฟพื้นที่สำหรับเติมสีใต้เส้น
        area_chart1 = alt.Chart(chart_data_front_11).mark_area(
            color="#1e40af",  # สีของพื้นที่
            opacity=0.3  # ความโปร่งแสงของสี
        ).encode(
            x='DATE:T',
            y='WATER LEVEL:Q'
        )

        # รวมกราฟเส้นและกราฟพื้นที่
        final_chart1 = area_chart1 + line_chart1

        # แสดงกราฟใน Streamlit
        st.altair_chart(final_chart1, use_container_width=True)

    # Display a WATER FRONT AND BACK PER MONTH
    st.markdown("""---""")


elif graph_type == "UBON RATCHATHANI MAP":
    st.markdown("""---""")
    button = st_tw(
        text="""
        <div class="flex justify-center">
            <button class="bg-gray-900 hover:animate-pulse text-white font-mono py-2 w-full rounded bg-gray-900">
                UBON RATCHATHANI MAP
            </button>
        </div>
        """,
        height=40,
        key="button8"   # Adjust height as needed
    )
    latitude = 15.2287  # Update with the latitude for Ubon Ratchathani
    longitude = 104.8564  # Update with the longitude for Ubon Ratchathani

    st.pydeck_chart(pdk.Deck(

        map_style='mapbox://styles/mapbox/streets-v11',  # Choose a map style
        initial_view_state=pdk.ViewState(
            latitude=latitude,
            longitude=longitude,
            zoom=13,
            pitch=50,
        ),
        # No layers added, only the map will be displayed
    ))

    st.markdown("""---""")


time.sleep(refresh_interval)
# refresh every 1 second
st.rerun()