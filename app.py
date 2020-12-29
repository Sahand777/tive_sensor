
import requests
import json
import pandas as pd
from io import StringIO
import plotly.express as px
import streamlit as st




account_id = st.text_input('Account ID')
userkey = {"TiveApiKey": "eaabf233f89146789a71a69857ede984","x-tive-account-id": account_id}

response_shipment = requests.get("https://api2.prod1.tive.co/api/v2/shipment/status", params = {"States" : ["Active"]}, headers = userkey)
result_shipment = json.loads(response_shipment.text)
list_of_shipment = []
for i in range(len(result_shipment['result'])):
    list_of_shipment.append(result_shipment['result'][i]['id'])

response_device = requests.get("https://api2.prod1.tive.co/api/v2/device", headers = userkey)
result_device = json.loads(response_device.text)
list_of_tracker = []
for i in range(len(result_device['result'])):
    list_of_tracker.append(result_device['result'][i]['name'])
tracker = st.selectbox('Tracker Name', list_of_tracker)
query_trackerdata = {
"listOfTrackers" : tracker,
"sensors" : [
    "Location", 
    "Temperature",
    "Humidity",
    "Pressure",
    "Light",
    "Motion", 
    "Battery",
    "Acceleration"
    ],
"startTime" : "11%2F25%2F2020",
"endTime" : "12%2F11%2F2020",
"dataFormat" : "CSV"
}
shipment_id = st.selectbox("Shipment ID", list_of_shipment)
response_csv = requests.get("https://api2.prod1.tive.co/api/v2/shipment/" + shipment_id +"/trackerdata",
                        params = query_trackerdata, headers = userkey)

result_csv = json.loads(response_csv.text)
try:
    df = pd.read_csv(StringIO(result_csv["result"]), sep=",")
    st.write(df)
    df_columns = ['Temperature', 'Humidity', 'Pressure', 'Light', 'Motion', 'Acceleration']
    data_type = st.selectbox('Type of Data for plot', df_columns)
    if data_type == 'Acceleration':
        fig = px.line(df, x = 'Time', y = ['Acceleration', 'AccelerationX', 'AccelerationY', 'AccelerationZ'])
    else:
        fig = px.line(df, x = 'Time', y = data_type)
    st.write(fig)
    fig_map = px.line_mapbox(df, lat="Lat", lon="Lng",  zoom=3, height=300)
    fig_map.update_layout(mapbox_style="open-street-map", mapbox_zoom = 10, mapbox_center_lat = df.dropna().reset_index().loc[0, 'Lat'],
        margin={"r":0,"t":0,"l":0,"b":0})
    st.write(fig_map)
except:
    st.write("Please check the Inputs!")



