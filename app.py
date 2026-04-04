import streamlit as st
import pickle
import pandas as pd
import os

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Car Price Predictor", layout="wide", page_icon="🚗")

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    .main { background-color: #f0f2f6; }
    .stButton>button {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 12px 40px;
        border-radius: 25px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
        cursor: pointer;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #764ba2, #667eea);
        transform: scale(1.02);
    }
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        font-size: 32px;
        font-weight: bold;
        margin-top: 20px;
        box-shadow: 0 8px 32px rgba(102,126,234,0.4);
    }
    .title-text {
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 16px;
        margin-bottom: 30px;
    }
    .section-header {
        color: #667eea;
        font-size: 18px;
        font-weight: 700;
        border-left: 4px solid #667eea;
        padding-left: 10px;
        margin: 20px 0 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ================= LOGIN =================
VALID_USERS = {"admin": "12345"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("## 🔐 Login to Car Price Predictor")
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
for path in ["car_model.pkl", "./car_model.pkl", "models/car_model.pkl"]:
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                model = pickle.load(f)
            break
        except Exception as e:
            st.error(f"❌ Error loading model: {e}")
            st.stop()

if model is None:
    st.error("❌ car_model.pkl NOT FOUND")
    st.write("📁 Files:", os.listdir())
    st.stop()

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🚗 Car Gallery")
    st.markdown("### 🏎️ Featured Cars")

    st.image(
        "https://imgd.aeplcdn.com/664x374/n/cw/ec/141115/creta-exterior-right-front-three-quarter.jpeg",
        caption="🔵 Hyundai Creta — Popular SUV"
    )
    st.image(
        "https://imgd.aeplcdn.com/664x374/n/cw/ec/204996/thar-2025-exterior-right-front-three-quarter.jpeg?isig=0&q=80",
        caption="🟡 Mahindra Thar — Off-Road Beast"
    )

    st.markdown("---")
    st.markdown("### 🏷️ Sponsored Ads")
    st.markdown("📢 **Mahindra Thar** – Book Now! [CarWale](https://www.carwale.com)")
    st.markdown("📢 **Hyundai Creta** – Best Seller! [CarWale](https://www.carwale.com)")

    st.markdown("---")
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ================= MAIN UI =================
st.markdown('<p class="title-text">🚗 Used Car Price Predictor</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Get an instant estimated price for any used car in India</p>', unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="section-header">🏷️ Car Details</p>', unsafe_allow_html=True)

    brand = st.selectbox("Brand", [
        "Maruti", "Hyundai", "Honda", "Toyota", "Ford", "Volkswagen",
        "BMW", "Mercedes-Benz", "Audi", "Tata", "Mahindra", "Renault",
        "Nissan", "Chevrolet", "Skoda", "Jeep", "Jaguar", "Volvo",
        "Land", "Mini", "Mitsubishi", "Fiat", "Datsun", "Porsche",
        "Smart", "Bentley", "ISUZU"
    ])

    year = st.slider("Year of Manufacture", 1996, 2019, 2015)

    fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])

    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

with col2:
    st.markdown('<p class="section-header">📍 Other Details</p>', unsafe_allow_html=True)

    location = st.selectbox("Location", [
        "Mumbai", "Pune", "Chennai", "Hyderabad", "Jaipur",
        "Kochi", "Coimbatore", "Kolkata", "Delhi", "Bangalore", "Ahmedabad"
    ])

    owner = st.selectbox("Owner Type", ["First", "Second"])

    kms = st.number_input("Kilometers Driven", min_value=0, max_value=300000, value=50000, step=1000)

    mileage = st.number_input("Mileage (kmpl)", min_value=5.0, max_value=40.0, value=18.0, step=0.5)

    seats = st.selectbox("Seats", [2, 4, 5])

# ================= PREDICTION =================
st.markdown("<br>", unsafe_allow_html=True)
_, col_btn, _ = st.columns([1, 1, 1])
with col_btn:
    predict_btn = st.button("🚀 Predict Price")

if predict_btn:
    input_df = pd.DataFrame([{
        "Location": location,
        "Year": year,
        "Kilometers_Driven": kms,
        "Fuel_Type": fuel,
        "Transmission": transmission,
        "Owner_Type": owner,
        "Mileage": float(mileage),
        "Seats": float(seats),
        "Brand": brand
    }])

    try:
        prediction = model.predict(input_df)[0]
        prediction = max(prediction, 0)

        st.markdown(f"""
        <div class="result-box">
            💰 Estimated Price: ₹ {prediction:.2f} Lakhs
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("📋 View Input Summary"):
            st.dataframe(input_df.T.rename(columns={0: "Value"}), use_container_width=True)

    except Exception as e:
        st.error("❌ Prediction failed")
        st.exception(e)
 
