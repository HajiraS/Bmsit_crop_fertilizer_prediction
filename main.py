import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load the datasets
fertilizer_df = pd.read_csv("Fertilizer Prediction.csv")
crop_df = pd.read_csv("Crop_recommendation.csv")

# Clean column names to avoid errors
fertilizer_df.columns = fertilizer_df.columns.str.strip().str.lower()
crop_df.columns = crop_df.columns.str.strip().str.lower()

# Streamlit App Title
st.title("🌾 Smart Crop & Fertilizer Recommendation System")

# Sidebar for user inputs
st.sidebar.header("Enter Environmental Parameters")

# User input fields
temperature = st.sidebar.number_input("🌡️ Temperature (°C)", min_value=0, max_value=50, value=25)
humidity = st.sidebar.number_input("💧 Humidity (%)", min_value=0, max_value=100, value=60)
rainfall = st.sidebar.number_input("🌦️ Rainfall (mm)", min_value=0, max_value=300, value=100)
nitrogen = st.sidebar.number_input("🧪 Nitrogen (N)", min_value=0, max_value=100, value=50)
phosphorous = st.sidebar.number_input("🧪 Phosphorous (P)", min_value=0, max_value=100, value=50)
potassium = st.sidebar.number_input("🧪 Potassium (K)", min_value=0, max_value=100, value=50)
ph = st.sidebar.number_input("⚖️ Soil pH", min_value=0.0, max_value=14.0, value=6.5)
moisture = st.sidebar.number_input("💦 Moisture (%)", min_value=0, max_value=100, value=50)
soil_type = st.sidebar.selectbox("🌱 Select Soil Type", fertilizer_df["soil type"].unique())

# Crop Recommendation Based on N, P, K, Temperature, Humidity, and pH
def recommend_crop(n, p, k, temp, hum, ph):
    filtered_crop = crop_df[
        (crop_df["n"] == n) &
        (crop_df["p"] == p) &
        (crop_df["k"] == k) &
        (crop_df["temperature"] <= temp + 5) & (crop_df["temperature"] >= temp - 5) &
        (crop_df["humidity"] <= hum + 10) & (crop_df["humidity"] >= hum - 10) &
        (crop_df["ph"] <= ph + 0.5) & (crop_df["ph"] >= ph - 0.5)
    ]
    if not filtered_crop.empty:
        return filtered_crop.iloc[0]["label"]
    else:
        return "No exact match found, adjust parameters."

# Fertilizer Recommendation Based on N, P, K, Moisture, Humidity, Temperature, and Soil Type
def recommend_fertilizer(n, p, k, moisture, hum, temp, soil):
    filtered_fertilizer = fertilizer_df[
        (fertilizer_df["n"] == n) &
        (fertilizer_df["p"] == p) &
        (fertilizer_df["k"] == k) &
        (fertilizer_df["moisture"] <= moisture + 10) & (fertilizer_df["moisture"] >= moisture - 10) &
        (fertilizer_df["humidity"] <= hum + 10) & (fertilizer_df["humidity"] >= hum - 10) &
        (fertilizer_df["temperature"] <= temp + 5) & (fertilizer_df["temperature"] >= temp - 5) &
        (fertilizer_df["soil type"] == soil)
    ]
    if not filtered_fertilizer.empty:
        return filtered_fertilizer.iloc[0]["fertilizer name"]
    else:
        return "No suitable fertilizer found."

# Prediction Button
if st.sidebar.button("🔍 Predict"):
    recommended_crop = recommend_crop(nitrogen, phosphorous, potassium, temperature, humidity, ph)
    recommended_fertilizer = recommend_fertilizer(nitrogen, phosphorous, potassium, moisture, humidity, temperature, soil_type)

    # Display Recommendations
    st.subheader("✅ Recommended Crop")
    st.success(f"🌱 {recommended_crop}")

    st.subheader("💡 Recommended Fertilizer")
    st.info(f"🧪 {recommended_fertilizer}")

    # Visualization: Modern Scatter Plot using Plotly
    st.subheader("📊 Environmental Factor Analysis")
    data = pd.DataFrame({
        "Factors": ["Nitrogen", "Phosphorous", "Potassium", "Temperature", "Humidity", "pH", "Moisture"],
        "Values": [nitrogen, phosphorous, potassium, temperature, humidity, ph, moisture]
    })
    fig = px.scatter(data, x="Factors", y="Values", size="Values", color="Factors",
                     title="Environmental Factors for Crop & Fertilizer Selection", template="plotly_dark")
    st.plotly_chart(fig)
