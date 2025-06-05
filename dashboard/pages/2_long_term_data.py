import streamlit as st
import pandas as pd

st.title("Displays plant data over time.")

df = pd.read_json("plants.json")

names = df["name"].unique()

st.sidebar.selectbox("Select a plant", names)
