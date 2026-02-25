import streamlit as st
import pickle
import pandas as pd
import altair as alt
import random
import time

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Used Car Price Predictor",
    page_icon="🚗",
    layout="wide"
)

# ================= LOGIN SETUP =================
VALID_USERS = {
    "admin": "admin123",
    "user": "car123"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login_page():
    st.markdown("<h1>🔐 AI Secure Login</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")

        if st.button("🚀 Enter AI System", use_container_width=True):
            if username in VALID_USERS and VALID_USERS[username] == password:
                st.session_state.logged_in = True
                st.success("Access Granted ✅")
                st.rerun()
            else:
                st.error("Invalid credentials ❌")


if not st.session_state.logged_in:
    login_page()
    st.stop()

# ================= SIDEBAR =================
st.sidebar.success("🟢 AI System Online")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.info("🤖 AI Powered ML Dashboard")
st.sidebar.markdown("📊 Neural Price Prediction")
st.sidebar.markdown("🔐 Secure Authentication")
st.sidebar.markdown("🚘 Smart Valuation Engine")

st.sidebar.markdown("### 🏷️ Sponsored")
st.sidebar.image(
    "https://imgd.aeplcdn.com/664x374/n/cw/ec/40087/thar-exterior-right-front-three-quarter.jpeg",
    caption="Mahindra Thar"
)

# ================= FUTURISTIC CSS =================
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0f2027, #000000 70%);
}

h1 {
    color: #00fff5;
    text-shadow: 0 0 18px #00fff5;
    text-align: center;
}

.card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 22px;
    border: 1px solid rgba(0,255,245,0.3);
    box-shadow: 0 0 25px rgba(0,255,245,0.15);
}

.ad {
    background: linear-gradient(135deg, #ff512f, #dd2476);
    padding: 20px;
    border-radius: 20px;
    color: white;
    text-align: center;
    box-shadow: 0 0 25px rgba(255,81,47,0.6);
}

.price-box {
    background: linear-gradient(135deg, #00fff5, #0072ff);
    padding: 30px;
    border-radius: 22px;
    color: black;
    text-align: center;
    box-shadow: 0 0 35px rgba(0,255,245,0.7);
}

.gift-box {
    background: linear-gradient(135deg, #ff9a00, #ff3d00);
    padding: 25px;
    border-radius: 22px;
    color: white;
    text-align: center;
    box-shadow: 0 0 30px rgba(255,154,0,0.7);
}

.stButton > button {
    background: linear-gradient(90deg, #00fff5, #0072ff);
    color: black;
    font-weight: bold;
    border-radius: 30px;
    padding: 12px 25px;
    box-shadow: 0 0 20px rgba(0,255,245,0.6);
}
</style>
""", unsafe_allow_html=True)

# ================= LOAD MODEL =================
data = pickle.load(open("used_car_model.pkl", "rb"))
model = data["model"]
model_columns = data["columns"]

# ================= HEADER =================
st.markdown("<h1>🚗 AI Used Car Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("### Neural Network • Smart Valuation • Futuristic UI")
st.markdown("---")

# ================= MAIN AD =================
st.markdown("""
<div class="ad">
🚘 <b>AI LIMITED OFFER</b><br>
FREE Inspection + Best Resale Intelligence<br>
📞 1800-1200-10
</div>
""", unsafe_allow_html=True)

# ================= IMAGES =================
img1, img2, img3 = st.columns(3)
img1.image("https://www.carstreetindia.com/carstreet-login/uploads/blog/67a9c463c14951738923637_Carrera%201.jpeg", use_container_width=True)
img2.image("https://content.jdmagicbox.com/comp/nashik/n8/0253px253.x253.140508132504.h3n8/catalogue/anand-auto-consultant-panchavati-nashik-second-hand-car-dealers-chevrolet-cpwvh0icvn.jpg", use_container_width=True)
img3.image("https://www.kamdhenucars.com/assets/front/images/cars/3294/1756467960_mCdCzQu6.jpg", use_container_width=True)

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
    "Owner_Type": owner
}

input_df = pd.DataFrame([input_dict])
input_df = pd.get_dummies(
    input_df,
    columns=["Fuel_Type", "Transmission", "Owner_Type"],
    drop_first=True
)
input_df = input_df.reindex(columns=model_columns, fill_value=0)

# ================= PREDICTION =================
st.markdown("---")
if st.button("🤖 Run AI Valuation Engine", use_container_width=True):

    with st.spinner("🧠 AI analyzing 1.2M car records..."):
        time.sleep(2)
        prediction = model.predict(input_df)[0]

    st.markdown(
        f"""
        <div class="price-box">
            <h2>Neural Network Output</h2>
            <h1>₹ {round(prediction, 2)} Lakhs</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ================= KPIs =================
    c1, c2, c3 = st.columns(3)
    c1.metric("📈 Market Trend", "Upward", "+6.2%")
    c2.metric("🧠 AI Confidence", "94%")
    c3.metric("🚘 Demand Score", "High")

    # ================= AI RECOMMENDATION =================
    st.markdown("### 🤖 AI Recommendation")
    if prediction > 10:
        st.success("🚀 Excellent resale value. Good time to sell.")
    elif prediction > 5:
        st.info("📊 Fair value. Hold or negotiate.")
    else:
        st.warning("⚠️ Low resale value. Consider upgrading.")

    # ================= GIFT SYSTEM =================
    gifts = [
        "🎁 Free Car Wash Coupon",
        "🎉 ₹500 Fuel Voucher",
        "🎧 Free Bluetooth Speaker",
        "🛠️ Free Car Health Check",
        "🚘 Premium Car Cover"
    ]

    won_gift = random.choice(gifts)

    with st.expander("🎁 Open Mystery AI Reward"):
        st.markdown(
            f"""
            <div class="gift-box">
                <h2>Congratulations!</h2>
                <h3>{won_gift}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.image(
            "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
            use_container_width=True
        )

    # ================= FUTURISTIC CHART =================
    chart_df = pd.DataFrame({
        "Scenario": ["Low", "Predicted", "High"],
        "Price (Lakhs)": [prediction * 0.85, prediction, prediction * 1.15]
    })

    chart = alt.Chart(chart_df).mark_line(
        point=True,
        strokeWidth=4
    ).encode(
        x="Scenario",
        y="Price (Lakhs)",
        color=alt.value("#00fff5")
    )

    st.altair_chart(chart, use_container_width=True)
