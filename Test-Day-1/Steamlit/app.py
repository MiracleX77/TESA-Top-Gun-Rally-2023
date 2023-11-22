import requests
import streamlit as st
import pandas as pd
import time

# ตั้งค่า URL ของ API
# api_device_url = "http://api:80/api/device/getDevicesByUserId/65562bdf5e187e59da1e8349"
device_1 = "655631c654cc6ac08fa21fab"
device_2 = "655632a79a0c48b0dfe9b982"
api_get_mc_url = "http://api:80/api/moisture/getAllMoistureByListDeviceId"

# ฟังก์ชันสำหรับการดึงข้อมูลจาก API
def get_device_data():
    response = requests.get(api_device_url)
    return response.json()  # สมมติว่า API ส่งกลับข้อมูลในรูปแบบ JSON

# หน้าหลักของ Streamlit
def main():
    st.title("Dashboard Title")
    
    
    # ดึงข้อมูลอุปกรณ์
    # device_data = get_device_data()
    list_device_id = [device_1, device_2]

    data_1 = pd.DataFrame(columns=["mc"])
    data_2 = pd.DataFrame(columns=["mc"])

    chart_1 = st.empty()
    chart_2 = st.empty()

    text_1 = st.empty()  # สำหรับแสดงข้อความของ mc สำหรับ device 1
    text_2 = st.empty()  # สำหรับแสดงข้อความของ mc สำหรับ device 2


    while True:
        response = requests.post(api_get_mc_url, json={"list_device_id": list_device_id})
        mc_data = response.json()["result"]
        
        new_data_1 = {
            "time": pd.to_datetime("now"),
            "mc": mc_data[0]['moisture'],
        }
        new_data_2 = {
            "time": pd.to_datetime("now"),
            "mc": mc_data[1]['moisture'],
        }
        new_data_df_1 = pd.DataFrame([new_data_1])
        data_1 = pd.concat([data_1, new_data_df_1], ignore_index=True).tail(50)  # ให้แสดงเพียง 50 รายการล่าสุด
        chart_1.line_chart(data_1.set_index("time"))
        text_1.markdown(f"Current Moisture (Device 1): `{mc_data[0]['moisture']}`")  # แสดงข้อความ
        new_data_df_2 = pd.DataFrame([new_data_2])
        data_2 = pd.concat([data_2, new_data_df_2], ignore_index=True).tail(50)  # ให้แสดงเพียง 50 รายการล่าสุด
        chart_2.line_chart(data_2.set_index("time"))
        text_2.markdown(f"Current Moisture (Device 2): `{mc_data[1]['moisture']}`")  # แสดงข้อความ


        time.sleep(0.5)  # หน่วงเวลา 1 วินาที

if __name__ == "__main__":
    main()
