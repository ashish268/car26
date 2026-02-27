import streamlit as st
import pickle
import pandas as pd
import altair as alt
import random
import numpy as np

# ================= LOGIN SETUP =================
VALID_USERS = {
    "admin": "admin123",
    "user": "car123"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login_page():
    st.markdown("<h1 style='text-align:center;'>🔐 Login</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("### 🚗 Used Car Price Predictor")
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")

        if st.button("🚀 Login", use_container_width=True):
            if username in VALID_USERS and VALID_USERS[username] == password:
                st.session_state.logged_in = True
                st.success("Login successful ✅")
                st.rerun()
            else:
                st.error("Invalid credentials ❌")


# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Used Car Price Predictor",
    page_icon="🚗",
    layout="wide"
)

# ================= LOGIN CHECK =================
if not st.session_state.logged_in:
    login_page()
    st.stop()

# ================= LOAD MODEL =================
data = pickle.load(open("used_car_model.pkl", "rb"))
model = data["model"]
model_columns = data["columns"]

# ================= HEADER =================
st.markdown("<h1>🚗 AI Used Car Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("### Smart • Commercial • Futuristic ML App")
st.markdown("---")

# ================= INPUTS =================
left, right = st.columns(2)

with left:
    year = st.slider("📅 Year", 1996, 2019, 2015)
    kms = st.slider("🛣️ Kilometers Driven", 0, 200000, 50000)
    seats = st.selectbox("💺 Seats", [2, 4, 5, 6, 7])
    owner = st.selectbox("👤 Owner Type", ["First", "Second", "Third", "Fourth & Above"])
    fuel = st.selectbox("⛽ Fuel Type", ["Petrol", "Diesel", "Electric", "LPG"])
    transmission = st.selectbox("⚙️ Transmission", ["Manual", "Automatic"])

with right:
    mileage = st.slider("📊 Mileage (km/l)", 5.0, 35.0, 18.0)
    engine = st.slider("🔩 Engine (CC)", 500, 4000, 1200)
    new_price = st.slider("💰 New Price (Lakhs ₹)", 2.0, 50.0, 8.0)

    brand = st.selectbox(
        "🚗 Car Brand",
        [
            "Audi","BMW","Bentley","Chevrolet","Datsun","Fiat","Force","Ford",
            "Hindustan","Honda","Hyundai","ISUZU","Isuzu","Jaguar","Jeep",
            "Lamborghini","Land","Mahindra","Maruti","Mercedes-Benz","Mini",
            "Mitsubishi","Nissan","OpelCorsa","Porsche","Renault","Skoda",
            "Smart","Tata","Toyota","Volkswagen","Volvo"
        ]
    )

# ================= DEFAULT POWER =================
# Power removed from UI, but model still needs it
power = 90  # average bhp (safe default)

# ================= PREPARE INPUT =================
input_dict = {
    "Year": year,
    "Kilometers_Driven": kms,
    "Mileage": mileage,
    "Engine": engine,
    "Power": power,              # still passed to model
    "Seats": seats,
    "New_Price": new_price,
    "Fuel_Type": fuel,
    "Transmission": transmission,
    "Owner_Type": owner
}

input_df = pd.DataFrame([input_dict])
input_df = pd.get_dummies(
    input_df,
    columns=["Fuel_Type", "Transmission", "Owner_Type"],
    drop_first=True
)

# ================= BRAND ONE-HOT =================
brand_col = f"Brand_{brand}"
input_df[brand_col] = 1

# Align with training columns
input_df = input_df.reindex(columns=model_columns, fill_value=0)

# ================= PREDICTION =================
st.markdown("---")
if st.button("🚀 PREDICT PRICE", use_container_width=True):
    prediction = model.predict(input_df)[0]
    prediction = max(prediction, 0)

    st.success(f"💰 Estimated Car Price: ₹ {round(prediction, 2)} Lakhs")
