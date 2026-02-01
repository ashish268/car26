import streamlit as st
import pickle
import pandas as pd
import altair as alt
import random

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
        st.markdown("### 🚗 AI Used Car Price Predictor")
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

# ================= SIDEBAR =================
st.sidebar.success("Logged in ✅")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.subheader("🎵 Background Music")

music_choice = st.sidebar.selectbox(
    "Choose Music",
    ["Chill Tech", "Luxury Drive", "Future AI", "No Music"]
)

music_links = {
    "Chill Tech": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
    "Luxury Drive": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
    "Future AI": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3"
}

if music_choice != "No Music":
    st.markdown(f"""
    <audio autoplay loop controls>
      <source src="{music_links[music_choice]}" type="audio/mp3">
    </audio>
    """, unsafe_allow_html=True)

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
    box-shadow: 0 0 20px rgba(255,81,47,0.6);
}
.gift-box {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    padding: 20px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-top: 20px;
}
.price-box {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    color: white;
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

# ================= MAIN ADS =================
st.markdown("""
<div class="ad">
🚘 <b>LIMITED TIME OFFER!</b><br>
Get <b>FREE Car Inspection</b> + <b>Best Resale Value</b><br>
📞 Call Now: 1800-CAR-AI
</div>
""", unsafe_allow_html=True)

# ================= IMAGES =================
img1, img2, img3 = st.columns(3)
img1.image("https://www.carstreetindia.com/carstreet-login/uploads/blog/67a9c463c14951738923637_Carrera%201.jpeg", use_container_width=True)
img2.image("https://content.jdmagicbox.com/comp/nashik/n8/0253px253.x253.140508132504.h3n8/catalogue/anand-auto-consultant-panchavati-nashik-second-hand-car-dealers-chevrolet-cpwvh0icvn.jpg", use_container_width=True)
img3.image("https://www.kamdhenucars.com/assets/front/images/cars/3294/1756467960_mCdCzQu6.jpg", use_container_width=True)

# ================= SIDEBAR ADS =================
st.sidebar.markdown("### 🏷️ Sponsored Ads")
st.sidebar.image(
    "https://imgd.aeplcdn.com/664x374/n/cw/ec/40087/thar-exterior-right-front-three-quarter.jpeg",
    caption="Mahindra Thar – Book Today!"
)
st.sidebar.image(
    "https://imgd.aeplcdn.com/664x374/n/cw/ec/141115/creta-exterior-right-front-three-quarter.jpeg",
    caption="Hyundai Creta – Best Seller"
)

# ================= INPUTS =================
left, center = st.columns(2)

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    year = st.slider("📅 Year", 1995, 2025, 2018)
    kms = st.slider("🛣️ Kilometers Driven", 0, 200000, 50000)
    seats = st.selectbox("💺 Seats", [2, 4, 5, 6, 7])
    owner = st.selectbox("👤 Owner Type", ["First", "Second", "Third", "Fourth & Above"])
    fuel = st.selectbox("⛽ Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
    transmission = st.selectbox("⚙️ Transmission", ["Manual", "Automatic"])
    st.markdown('</div>', unsafe_allow_html=True)

with center:
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
if st.button("🚀 PREDICT PRICE", use_container_width=True):
    prediction = model.predict(input_df)[0]

    st.markdown(
        f"""
        <div class="price-box">
            <h2>💎 Estimated Car Value</h2>
            <h1>₹ {round(prediction, 2)} Lakhs</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 🎁 Gift System
    gifts = [
        "🎁 Free Car Wash Coupon",
        "🎉 ₹500 Fuel Voucher",
        "🎧 Free Bluetooth Car Speaker",
        "🛠️ Free Car Health Check",
        "🚘 Premium Car Cover"
    ]

    won_gift = random.choice(gifts)

    st.markdown(
        f"""
        <div class="gift-box">
            <h2>🎁 Congratulations!</h2>
            <h3>You Won: {won_gift}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image(
        "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
        caption="🎉 Surprise Gift Unlocked!",
        use_container_width=True
    )

    # 📊 Animated Chart
    chart_df = pd.DataFrame({
        "Scenario": ["Low", "Predicted", "High"],
        "Price (Lakhs)": [prediction * 0.85, prediction, prediction * 1.15]
    })

    chart = alt.Chart(chart_df).mark_bar().encode(
        x="Scenario",
        y="Price (Lakhs)",
        color="Scenario"
    )

    st.altair_chart(chart, use_container_width=True)
