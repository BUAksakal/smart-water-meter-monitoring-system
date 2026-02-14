import streamlit as st
import pandas as pd
import requests
import time

# Başlık
st.markdown(
    """
    <h1 style='text-align: center; color: white; background-color: rgba(0, 100, 0, 0.7); padding: 10px;'>Live DataGrid for Water Meters</h1>
    """,
    unsafe_allow_html=True
)

# Arka plan resmini ayarlama
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.baylanwatermeters.com%2Fen%2Fabout_en.php&psig=AOvVaw2RJBnwXP2GUsUhjSV3I6bP&ust=1724834954656000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCLD4vInllIgDFQAAAAAdAAAAABAJ');
        background-size: cover;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Veri çekmek ve göstermek için sürekli bir döngü
while True:
    try:
        # Flask API'den verileri çek
        response = requests.get('http://localhost:8080/data')

        if response.status_code == 200:
            data = response.json()

            # Verileri Pandas DataFrame'e çevir
            if data:
                df = pd.DataFrame(data)
                st.write("Data received from Flask API:")
                st.dataframe(df)
            else:
                st.write("No data received yet.")
        else:
            st.write("Failed to fetch data from API.")
    except Exception as e:
        st.write(f"An error occurred: {e}")

    time.sleep(5)  # 5 saniye bekle ve tekrar veri çek
