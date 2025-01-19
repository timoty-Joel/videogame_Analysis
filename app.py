import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned dataset
@st.cache
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

df = load_data('/mnt/data/Cleaned_Video_Games.csv')

# Dashboard title
st.title('Video Games Data Visualization')
