import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import folium_static


st.markdown("""# :oncoming_taxi: NYC TaxiFare - At your service ! :taxi:
""")

st.sidebar.markdown("""# Enter your infos :smiley: """)

date = st.sidebar.date_input("Enter a date")
time = st.sidebar.time_input("Enter time of the ride")
passenger_count = st.sidebar.slider("How many passengers?", 1,8,1)
pickup_address = st.sidebar.text_input("Enter pickup adress")
dropoff_address = st.sidebar.text_input("Enter dropoff adress")


def geocode(address):
        url = "https://nominatim.openstreetmap.org/search?"
        response = requests.get(url, params={
            'q': address,
            'format': 'json'
        })
        if response.status_code == 200:
            return [response.json()[0]['lat'], response.json()[0]['lon']]
        else:
            return [0, 0]


NY_coordinates = [40.7128, -74.0060]

if pickup_address:
    pickup_coordinates = geocode(pickup_address)
if dropoff_address:
    dropoff_coordinates = geocode(dropoff_address)

map = folium.Map(location=NY_coordinates,tiles="stamentoner")

if pickup_address:
    if dropoff_address:
        folium.Marker(pickup_coordinates,title="Pick-up address").add_to(map)
        folium.Marker(dropoff_coordinates,title="Pick-up address").add_to(map)
        folium.PolyLine([(float(pickup_coordinates[0]),float(pickup_coordinates[1])),(float(dropoff_coordinates[0]),float(dropoff_coordinates[1]))],
                color='red',
                weight=10,
                opacity=0.8).add_to(map)

folium_static(map,height=500,width=800)


url = "https://taxifarecoco-4ufqwrfzhq-ew.a.run.app/predict"


if pickup_address:
    if dropoff_address:
        user_request = {
                "pickup_datetime" : date,
                "pickup_longitude" : pickup_coordinates[1],
                "pickup_latitude" : pickup_coordinates[0],
                "dropoff_longitude" : dropoff_coordinates[1],
                "dropoff_latitude" : dropoff_coordinates[0],
                "passenger_count" : passenger_count}


        url_geo = requests.get(url, params=user_request).json()

        amount = url_geo["fare_amount"]


        st.sidebar.markdown(f"""
                            # Estimated price for you ride is :
                            # :heavy_dollar_sign: """ +str(round(amount,2)))
