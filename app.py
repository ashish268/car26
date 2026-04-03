import streamlit as st
import pickle
import pandas as pd

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


# ================= CONFIG =================
st.set_page_config(page_title="Car Price Predictor", layout="wide")

if not st.session_state.logged_in:
    login()
    st.stop()

# ================= LOAD MODEL =================
try:
    with open("car_model.pkl", "rb") as f:
        model = pickle.load(f)
except:
    st.error("❌ Model not found. Upload car_model.pkl")
    st.stop()

# ================= UI =================
st.title("🚗 Used Car Price Predictor")

col1, col2 = st.columns(2)

with col1:
    year = st.slider("Year", 1995, 2023, 2018)
    kms = st.number_input("Kilometers Driven", 0, 300000, 50000)
    fuel = st.selectbox("Fuel", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
    seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
    owner = st.selectbox("Owner", ["First Owner", "Second Owner", "Third Owner"])

with col2:
    mileage = st.number_input("Mileage (km/l)", 5.0, 40.0, 18.0)
    engine = st.number_input("Engine (CC)", 500, 5000, 1200)
    max_power = st.number_input("Max Power (bhp)", 20.0, 500.0, 90.0)
    seats = st.selectbox("Seats", [2, 4, 5, 6, 7, 8])
    brand = st.text_input("Car Brand (e.g., Maruti, Hyundai)")

# ================= INPUT DATA =================
input_data = pd.DataFrame({
    "Year": [year],
    "Kilometers_Driven": [kms],
    "Fuel_Type": [fuel],
    "Seller_Type": [seller_type],
    "Transmission": [transmission],
    "Owner": [owner],
    "Mileage": [mileage],
    "Engine": [engine],
    "Max_Power": [max_power],
    "Seats": [seats],
    "Brand": [brand]
})

# ================= PREDICTION =================
if st.button("🚀 Predict Price"):
    try:
        prediction = model.predict(input_data)[0]
        prediction = max(prediction, 0)

        st.success(f"💰 Estimated Price: ₹ {round(prediction, 2)} Lakhs")

    except Exception as e:
        st.error("❌ Prediction failed")
        st.write(e)

