import paho.mqtt.client as mqtt
import json
import requests
from datetime import datetime

def get_list_sensor():
    list_sensor = []
    res = requests.get("http://main-test-api-1:80/api/sensor/getAll")
    data = res.json()
    for sensor in data['result']:
        list_sensor.append(str(sensor['sensor_id']))
    return list_sensor


    
    

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("tgr2023/horix/#")
    
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    data = json.loads(msg.payload)
    topic = msg.topic.split("/")[-1]
    if (topic in list_sensor):
        record = {
            "sensor_id": topic,
            "water_height": data['water_height'],
        }
        res = requests.post("http://main-test-api-1:80/api/predictWater/create", json=record)
        print(res.text)

        
    
if __name__ == '__main__':
    client = mqtt.Client()
    client.username_pw_set("TGR_GROUP18", "QL445T")

    client.on_connect = on_connect
    client.on_message = on_message
    list_sensor = get_list_sensor()
    client.connect(host = "192.168.1.2",port= 1883)

    client.loop_forever()