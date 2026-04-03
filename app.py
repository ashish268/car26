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
model = None
possible_paths = [
    "car_model.pkl",
    "./car_model.pkl",
    "models/car_model.pkl",
    "./models/car_model.pkl"
]

for path in possible_paths:
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                model = pickle.load(f)
            break
        except Exception as e:
            st.error(f"❌ Error loading model from {path}: {e}")
            st.stop()

if model is None:
    st.error("❌ car_model.pkl NOT FOUND")
    st.write("📁 Files in app folder:", os.listdir())
    st.stop()

# ================= UI =================
st.title("🚗 Used Car Price Predictor")

col1, col2 = st.columns(2)

with col1:
    brand = st.selectbox("Brand", [
        "Maruti", "Hyundai", "Honda", "Toyota", "Ford", "Volkswagen",
        "BMW", "Mercedes-Benz", "Audi", "Tata", "Mahindra", "Renault",
        "Nissan", "Chevrolet", "Skoda", "Jeep", "Jaguar", "Volvo",
        "Land", "Mini", "Mitsubishi", "Fiat", "Force", "Isuzu",
        "Lamborghini", "Ferrari", "Bentley", "Other"
    ])
    location = st.selectbox("Location", [
        "Mumbai", "Pune", "Chennai", "Hyderabad", "Jaipur",
        "Kochi", "Coimbatore", "Kolkata", "Delhi", "Bangalore", "Ahmedabad"
    ])
    year = st.slider("Year", 1995, 2023, 2018)
    kms = st.number_input("Kilometers Driven", 0, 300000, 50000)
    fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

with col2:
    owner = st.selectbox("Owner Type", ["First", "Second", "Third", "Fourth & Above"])
    mileage = st.number_input("Mileage (kmpl)", 5.0, 40.0, 18.0)
    engine = st.number_input("Engine (CC)", 500, 5000, 1200)
    power = st.number_input("Power (bhp)", 20.0, 500.0, 90.0)
    seats = st.selectbox("Seats", [2, 4, 5, 6, 7, 8])

# ================= INPUT =================
# Must match EXACTLY the columns the pipeline was trained on:
# ['Location', 'Year', 'Kilometers_Driven', 'Fuel_Type', 'Transmission',
#  'Owner_Type', 'Mileage', 'Engine', 'Power', 'Seats', 'Brand']

input_df = pd.DataFrame([{
    "Location": location,
    "Year": year,
    "Kilometers_Driven": kms,
    "Fuel_Type": fuel,
    "Transmission": transmission,
    "Owner_Type": owner,
    "Mileage": float(mileage),
    "Engine": float(engine),
    "Power": float(power),
    "Seats": float(seats),
    "Brand": brand
}])

# ================= PREDICTION =================
if st.button("🚀 Predict Price"):
    try:
        # Pipeline handles all preprocessing internally — no manual encoding needed
        prediction = model.predict(input_df)[0]
        prediction = max(prediction, 0)
        st.success(f"💰 Estimated Price: ₹ {round(prediction, 2)} Lakhs")
    except Exception as e:
        st.error("❌ Prediction failed")
        st.exception(e)
