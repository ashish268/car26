import streamlit as st
import pickle
import pandas as pd
import altair as alt
import random

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Used Car Price Predictor",
    page_icon="🚗",
    layout="wide"
)

# ================= USER STORAGE =================
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": "admin123",
        "user": "car123"
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"

# ================= AUTH PAGES =================
def login_page():
    st.markdown("<h1 style='text-align:center;'>🔐 Login</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🚗 Used Car Price Predictor")
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")

        if st.button("🚀 Login", use_container_width=True):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.success("Login successful ✅")
                st.rerun()
            else:
                st.error("Invalid credentials ❌")

        st.markdown("---")
        if st.button("📝 New User? Sign Up"):
            st.session_state.auth_page = "signup"
            st.rerun()


def signup_page():
    st.markdown("<h1 style='text-align:center;'>📝 Sign Up</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        new_user = st.text_input("👤 Create Username")
        new_pass = st.text_input("🔑 Create Password", type="password")
        confirm_pass = st.text_input("🔁 Confirm Password", type="password")

        if st.button("✅ Create Account", use_container_width=True):
            if new_user in st.session_state.users:
                st.error("Username already exists ❌")
            elif new_user == "" or new_pass == "":
                st.warning("Fields cannot be empty ⚠️")
            elif new_pass != confirm_pass:
                st.error("Passwords do not match ❌")
            else:
                st.session_state.users[new_user] = new_pass
                st.success("Account created successfully 🎉")
                st.session_state.auth_page = "login"
                st.rerun()

        st.markdown("---")
        if st.button("🔙 Back to Login"):
            st.session_state.auth_page = "login"
            st.rerun()


# ================= AUTH ROUTING =================
if not st.session_state.logged_in:
    if st.session_state.auth_page == "login":
        login_page()
    else:
        signup_page()
    st.stop()

# ================= SIDEBAR =================
st.sidebar.success(f"Logged in as {st.session_state.current_user}")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.auth_page = "login"
    st.rerun()

st.sidebar.info("AI Powered ML Application")
st.sidebar.markdown("📊 Real-time Price Prediction")
st.sidebar.markdown("🔐 Secure Login & Signup")
st.sidebar.markdown("🚗 Used Car Valuation")

# ================= CSS =================
st.markdown("""
<style>
body {
    background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
}
h1 {
    color: #00ffd5;
    text-align: center;
}
.card {
    background: linear-gradient(145deg, #141e30, #243b55);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 0 25px rgba(0,255,213,0.25);
    margin-bottom: 20px;
}
.ad {
    background: linear-gradient(135deg, #ff512f, #dd2476);
    padding: 18px;
    border-radius: 18px;
    color: white;
    text-align: center;
    font-size: 18px;
    margin: 15px 0;
}
.gift-box, .price-box {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    padding: 20px;
    border-radius: 20px;
    color: white;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ================= LOAD MODEL =================
data = pickle.load(open("used_car_model.pkl", "rb"))
model = data["model"]
model_columns = data["columns"]

# ================= HEADER =================
st.markdown("<h1>🚗 AI Used Car Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("### Smart • Commercial • Futuristic ML App")
st.markdown("---")

# ================= MAIN AD =================
st.markdown("""
<div class="ad">
🚘 <b>LIMITED TIME OFFER!</b><br>
FREE Car Inspection + Best Resale Value
</div>
""", unsafe_allow_html=True)

# ================= INPUTS =================
left, right = st.columns(2)

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    year = st.slider("📅 Year", 1995, 2025, 2018)
    kms = st.slider("🛣️ Kilometers Driven", 0, 200000, 50000)
    seats = st.selectbox("💺 Seats", [2, 4, 5, 6, 7])
    owner = st.selectbox("👤 Owner Type", ["First", "Second", "Third", "Fourth & Above"])
    fuel = st.selectbox("⛽ Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
    transmission = st.selectbox("⚙️ Transmission", ["Manual", "Automatic"])
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    mileage = st.slider("📊 Mileage (km/l)", 5.0, 35.0, 18.0)
    engine = st.slider("🔩 Engine (CC)", 500, 4000, 1200)
    power = st.slider("⚡ Power (bhp)", 40.0, 400.0, 90.0)
    new_price = st.slider("💰 New Price (Lakhs ₹)", 2.0, 50.0, 8.0)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= PREPARE INPUT =================
input_df = pd.DataFrame([{
    "Year": year,
    "Kilometers_Driven": kms,
    "Mileage": mileage,
    "Engine": engine,
    "Power": power,
    "Seats": seats,
    "New_Price": new_price,
    "Fuel_Type": fuel,
    "Transmission": transmission,
    "Owner_Type": owner
}])

input_df = pd.get_dummies(
    input_df,
    columns=["Fuel_Type", "Transmission", "Owner_Type"],
    drop_first=True
)
input_df = input_df.reindex(columns=model_columns, fill_value=0)

# ================= PREDICTION =================
if st.button("🚀 PREDICT PRICE", use_container_width=True):
    prediction = model.predict(input_df)[0]

    st.markdown(f"""
    <div class="price-box">
        <h2>💎 Estimated Car Value</h2>
        <h1>₹ {round(prediction, 2)} Lakhs</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="gift-box">
        <h3>🎁 Bonus Gift</h3>
        <p>{random.choice([
            "Free Car Wash",
            "₹500 Fuel Voucher",
            "Car Health Check",
            "Premium Car Cover"
        ])}</p>
    </div>
    """, unsafe_allow_html=True)
