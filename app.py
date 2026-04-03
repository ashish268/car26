import streamlit as st
import joblib
import pandas as pd
import numpy as np

# ================= LOGIN SETUP =================
VALID_USERS = {
    "admin": "12345"
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
data = joblib.load("car_model.pkl")
model = data["model"]
columns = data["columns"]

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
power = 90

# ================= PREPARE INPUT =================
input_dict = {
    "Year": year,
    "Kilometers_Driven": kms,
    "Mileage": mileage,
    "Engine": engine,
    "Power": power,
    "Seats": seats,
    "New_Price": new_price,
    "Fuel_Type": fuel,
    "Transmission": transmission,
    "Owner_Type": owner,
    "Brand": brand
}

input_df = pd.DataFrame([input_dict])

# ✅ FIX: Ensure all columns exist (IMPORTANT)
for col in columns:
    if col not in input_df.columns:
        input_df[col] = np.nan

# Keep same order
input_df = input_df[columns]

# ================= PREDICTION =================
st.markdown("---")

if st.button("🚀 PREDICT PRICE", use_container_width=True):
    try:
        prediction = model.predict(input_df)[0]
        prediction = max(prediction, 0)

        st.success(f"💰 Estimated Car Price: ₹ {round(prediction, 2)} Lakhs")

    except Exception as e:
        st.error("❌ Prediction failed. Check input format.")
        st.write(e)

