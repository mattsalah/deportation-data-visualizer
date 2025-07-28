"""
Streamlit app for visualizing ICE arrest data.

Dataset source: https://deportationdata.org/data/ice.html

"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Set up paths
here = Path(__file__).resolve().parent

@st.cache_data
def load_data():
    data_path = here / 'data' / 'arrests.xlsx'
    if data_path.exists():
        df = pd.read_excel(data_path, skiprows=6)
        return df
    else:
        st.error("Data file not found.")
        return pd.DataFrame()

# Load the data
df = load_data()

# Main app logic
st.title("Dashboard")

if df.empty:
    st.warning("No data available.")
else:
       
    # Filters
    st.sidebar.header("Filters")

    # "Apprehension State"
    if 'Apprehension State' in df.columns:
        options = df['Apprehension State'].dropna().unique()
        selected = st.sidebar.multiselect("Select Apprehension State", sorted(options), default=options)
        df = df[df['Apprehension State'].isin(selected)]

    # "Apprehension Criminality"
    if 'Apprehension Criminality' in df.columns:
        options = df['Apprehension Criminality'].dropna().unique()
        selected = st.sidebar.multiselect("Select Apprehension Criminality", sorted(options), default=options)
        df = df[df['Apprehension Criminality'].isin(selected)]

    # "Citizenship Country"
    if 'Citizenship Country' in df.columns:
        options = df['Citizenship Country'].dropna().unique()
        selected = st.sidebar.multiselect("Select Citizenship Country", sorted(options), default=options)
        df = df[df['Citizenship Country'].isin(selected)]

    # "Gender"
    if 'Gender' in df.columns:
        options = df['Gender'].dropna().unique()
        selected = st.sidebar.multiselect("Select Gender", sorted(options), default=options)
        df = df[df['Gender'].isin(selected)]

    # Ensure the date column is datetime
    if 'Apprehension Date' in df.columns:
        df['Apprehension Date'] = pd.to_datetime(df['Apprehension Date'], errors='coerce')
        df_grouped = df.groupby('Apprehension Date').size().reset_index(name='count')
        df_grouped = df_grouped.sort_values('Apprehension Date')
        df_grouped['15_day_avg'] = df_grouped['count'].rolling(window=15, min_periods=1).mean()

        st.subheader("Arrests Over Time")
        
        st.write("Total: ", df_grouped['count'].sum())

        # Show raw data
        if st.checkbox("15 Day Rolling Average"):
            st.line_chart(df_grouped.set_index('Apprehension Date')[['15_day_avg']])
        else:
            st.line_chart(df_grouped.set_index('Apprehension Date')[['count']])
        
    else:
        st.error("Column 'Apprehension Date' not found in the dataset.")
        
    st.subheader("Data Overview")
    st.write("This table shows the first 100 rows of the dataset.")
    st.dataframe(df.head(100))

