import streamlit as st
import pickle
import pandas as pd

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
try:
    with open("car_model.pkl", "rb") as f:
        data = pickle.load(f)

    # Handle dict or direct model
    if isinstance(data, dict):
        model = data.get("model", None)
        model_columns = data.get("columns", None)
    else:
        model = data
        model_columns = None

    if model is None:
        st.error("❌ Model not found inside pkl file")
        st.stop()

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

# ================= HANDLE OLD MODEL =================
if model_columns is not None:
    input_df = pd.get_dummies(input_df)

    # Add missing columns
    for col in model_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    # Ensure correct order
    input_df = input_df[model_columns]

# ================= PREDICTION =================
if st.button("🚀 Predict Price"):
    try:
        prediction = model.predict(input_df)[0]
        prediction = max(prediction, 0)

        st.success(f"💰 Estimated Price: ₹ {round(prediction, 2)} Lakhs")

    except Exception as e:
        st.error("❌ Prediction failed")
        st.write("Error:", e)

