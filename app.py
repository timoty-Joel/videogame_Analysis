import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned dataset
#@st.cache
def load_data(file_path):
    data = pd.read_csv(file_path)
    data['Year_of_Release'] = pd.to_datetime(data['Year_of_Release'], errors='coerce')
    data = data.dropna(subset=['Year_of_Release']).copy()
    data['Year_of_Release'] = data['Year_of_Release'].dt.year
    return data

df = load_data('data/Cleaned_VideoGames.csv')

# Dashboard title
st.title('Video Games Data Visualization')
st.markdown('Explore video game sales trends, top platforms, genres, and other metrics.')

# Sidebar Filter
st.sidebar.header('Filters')

# Convert Year_of_Release to datetime if not already
#df['Year_of_Release'] = pd.to_datetime(df['Year_of_Release'], errors='coerce')
#df['Year_of_Release'] = df['Year_of_Release'].dt.year.astype(int)

if not df['Year_of_Release'].empty:
    min_year, max_year = df['Year_of_Release'].min(), df['Year_of_Release'].max()
else:
    min_year, max_year = 2000, 2020 

selected_year = st.sidebar.slider(
    "Select the Year Range", 
    min_value = int(min_year),
    max_value = int(max_year),
    value = (int(min_year), int(max_year)),
    step = 1
)

# Apply the filter
genres = df['Genre'].unique()
selected_genre = st.sidebar.multiselect("Select the Genre", genres)

platform = df['Platform'].unique()
selected_platform = st.sidebar.multiselect("Select the Platform", platform)

filtered_df = df[
    (df['Platform'].isin(selected_platform)) & 
    (df['Genre'].isin(selected_genre)) & 
    (df['Year_of_Release'].between(selected_year[0], selected_year[1]))
]

total_sales = filtered_df['Total_Global_Sales'].sum()
top_game = filtered_df.loc[filtered_df['Total_Global_Sales'].idxmax(), 'Name'] if not filtered_df.empty else "N/A"

# Main Dashboard
st.header("Overview Metrics")
st.metric("Top Game ", f"{total_sales:.2f}")
st.metric("Top Game by Sales", top_game)

# Visualization
st.subheader("Total Sales by Platform")
if not filtered_df.empty:
    platform_sales = filtered_df.groupby('Platform')['Total_Global_Sales'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize = (8, 4))
    platform_sales.plot(kind='bar', ax=ax, color = 'skyblue')
    ax.set_ylabel('Sales')
    ax.set_xlabel('Platform')
    ax.set_title('Total Sales by Platform')
    st.pyplot(fig)
else:
    st.warning("No Data Available to be Performed")