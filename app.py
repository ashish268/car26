import streamlit as st
import pickle
import pandas as pd
import os

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Car Price Predictor", layout="wide")

# ================= LOGIN =================
VALID_USERS = {
    "admin": "12345"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in VALID_USERS and VALID_USERS[username] == password:
            st.session_state.logged_in = True
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid credentials ❌")


if not st.session_state.logged_in:
    login()
    st.stop()

# ================= LOAD MODEL =================
model_path = r"C:\Users\mishti\car_model.pkl"   # ✅ FIXED PATH

if not os.path.exists(model_path):
    st.error("❌ car_model.pkl not found at given path")
    st.stop()

try:
    model = pickle.load(open(model_path, "rb"))
except Exception as e:
    st.error("❌ Error loading model")
    st.write(e)
    st.stop()

# ================= UI =================
st.title("🚗 Used Car Price Predictor")

col1, col2 = st.columns(2)

with col1:
    year = st.slider("Year", 1995, 2023, 2018)
    kms = st.number_input("Kilometers Driven", 0, 300000, 50000)
    fuel = st.selectbox("Fuel", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
    owner = st.selectbox("Owner", ["First", "Second", "Third", "Fourth & Above"])

with col2:
    mileage = st.number_input("Mileage", 5.0, 40.0, 18.0)
    engine = st.number_input("Engine (CC)", 500, 5000, 1200)
    power = st.number_input("Power (bhp)", 20.0, 500.0, 90.0)
    seats = st.selectbox("Seats", [2, 4, 5, 6, 7, 8])
    new_price = st.number_input("New Price (Lakhs)", 1.0, 100.0, 8.0)

# ================= INPUT =================
input_dict = {
    "Year": year,
    "Kilometers_Driven": kms,
    "Fuel_Type": fuel,
    "Transmission": transmission,
    "Owner_Type": owner,
    "Mileage": mileage,
    "Engine": engine,
    "Power": power,
    "Seats": seats,
    "New_Price": new_price
}

input_df = pd.DataFrame([input_dict])

# ================= PREPROCESS =================
input_df = pd.get_dummies(input_df)

expected_columns = [
    'Year', 'Kilometers_Driven', 'Mileage', 'Engine', 'Power',
    'Seats', 'New_Price',
    'Fuel_Type_CNG', 'Fuel_Type_Diesel', 'Fuel_Type_Electric',
    'Fuel_Type_LPG', 'Fuel_Type_Petrol',
    'Transmission_Manual',
    'Owner_Type_Second', 'Owner_Type_Third', 'Owner_Type_Fourth & Above'
]

for col in expected_columns:
    if col not in input_df.columns:
        input_df[col] = 0

input_df = input_df[expected_columns]

# ================= PREDICTION =================
if st.button("🚀 Predict Price"):
    try:
        prediction = model.predict(input_df)[0]
        prediction = max(prediction, 0)
        st.success(f"💰 Estimated Price: ₹ {round(prediction, 2)} Lakhs")
    except Exception as e:
        st.error("❌ Prediction failed")
        st.write(e)

