import requests
import json
import pandas as pd
from io import StringIO
import streamlit as st
import plotly.express as px

response_token = requests.post("https://beta.tagapi.net/auth/login",
                        params = {'login':'apiuser-tl', 'password':'rxQQpyBq67m5wCvx6QFtkfwdGCWfNYkK'})
result_token = json.loads(response_token.text)
token = result_token["token"]

response_all_tags = requests.get("https://beta.tagapi.net/tags/listdate/read/2019-01-01/2020-10-01",
                        params = {'token':token})
result_all_tags = json.loads(response_all_tags.text)

tag_id = st.selectbox('Tag ID', result_all_tags)


response_fetch = requests.get("https://beta.tagapi.net/simpletag/" + tag_id,
                        params = {'token':token})

response_all_tags = requests.get("https://beta.tagapi.net/tags/listdate/read/2019-01-01/2020-10-01",
                        params = {'token':token})


response_csv = requests.get("https://beta.tagapi.net/tag/csv/" + tag_id,
                        params = {'token':token})
result_csv = json.loads(response_csv.text)


try:
    text_csv = StringIO(result_csv["content"])
    temperature_data = pd.read_csv(text_csv, sep=";")
    df = temperature_data.rename(columns={'Time (UTC)':'index'}).set_index('index')
    fig = px.line(temperature_data, x='Time (UTC)', y="Temperature (°C)")
    st.write(fig)
    st.write('Temperature Data', temperature_data)
except:
   st.write(result_csv['context'])
