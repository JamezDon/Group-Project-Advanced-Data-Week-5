import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Displays current plant data.")

plant_data = pd.read_json("plants.json")


names = plant_data["name"].unique()

selected_plant = st.sidebar.selectbox("Select a plant", names)

filtered_data = plant_data[plant_data["name"] == selected_plant]
st.table(filtered_data)

avg_temp = filtered_data["temperature"].mean()
avg_soil_moisture = filtered_data["soil_moisture"].mean()
st.metric("Average temperature", avg_temp)
st.metric("Average soil moisture", avg_soil_moisture)

botanist = filtered_data["botanist"].to_dict()
botanist_name = botanist[0]["name"]
botanist_email = botanist[0]["email"]
botanist_phone = botanist[0]["phone"]

st.subheader("Assigned botanist")
st.text(f"Name: {botanist_name}")
st.text(f"Phone: {botanist_phone}")
st.text(f"Email: {botanist_email}")
