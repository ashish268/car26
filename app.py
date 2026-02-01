import streamlit as st
import pickle
import pandas as pd
import altair as alt

# ================= Page Config =================
st.set_page_config(
    page_title="AI Used Car Price Predictor",
    page_icon="🚗",
    layout="wide"
)

# ================= Background Music =================
st.markdown("""
<audio autoplay loop>
  <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mp3">
</audio>
""", unsafe_allow_html=True)

# ================= CSS Styling =================
st.markdown("""
<style>
body {
    background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
}
h1 { color: #00ffd5; text-align: center; }
h2, h3 { color: #ffcc00; }
.card {
    background: linear-gradient(145deg, #141e30, #243b55);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 0 25px rgba(0,255,213,0.25);
    margin-bottom: 20px;
}
.ad {
    background: linear-gradient(135deg, #ff512f, #dd2476);
    padding: 15px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}
.price-box {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    color: white;
    box-shadow: 0 0 30px rgba(0,198,255,0.7);
}
.footer {
    text-align: center;
    color: #ddd;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ================= Load Model =================
data = pickle.load(open("used_car_model.pkl", "rb"))
model = data["model"]
model_columns = data["columns"]

# ================= Header =================
st.markdown("<h1>🚗 AI Used Car Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("### 🎶 Smart • Animated • Futuristic ML Experience")
st.markdown("---")

# ================= Car Image Gallery =================
img1, img2, img3 = st.columns(3)
img1.image("https://www.carstreetindia.com/carstreet-login/uploads/blog/67a9c463c14951738923637_Carrera%201.jpeg", use_container_width=True)
img2.image("https://content.jdmagicbox.com/comp/nashik/n8/0253px253.x253.140508132504.h3n8/catalogue/anand-auto-consultant-panchavati-nashik-second-hand-car-dealers-chevrolet-cpwvh0icvn.jpg", use_container_width=True)
img3.image("https://www.kamdhenucars.com/assets/front/images/cars/3294/1756467960_mCdCzQu6.jpg", use_container_width=True)

st.markdown("---")

# ================= Layout =================
left, center, right = st.columns([1.2, 1.5, 1])

# ================= Inputs =================
with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔧 Car Details")

    year = st.slider("📅 Year", 1995, 2025, 2018)
    kms = st.slider("🛣️ Kilometers Driven", 0, 200000, 50000)
    seats = st.selectbox("💺 Seats", [2, 4, 5, 6, 7])
    owner = st.selectbox("👤 Owner Type", ["First", "Second", "Third", "Fourth & Above"])
    fuel = st.selectbox("⛽ Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
    transmission = st.selectbox("⚙️ Transmission", ["Manual", "Automatic"])

    st.markdown("</div>", unsafe_allow_html=True)

with center:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🚀 Performance")

    mileage = st.slider("📊 Mileage (km/l)", 5.0, 35.0, 18.0)
    engine = st.slider("🔩 Engine (CC)", 500, 4000, 1200)
    power = st.slider("⚡ Power (bhp)", 40.0, 400.0, 90.0)
    new_price = st.slider("💰 New Price (Lakhs ₹)", 2.0, 50.0, 8.0)

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="ad">', unsafe_allow_html=True)
    st.subheader("🔥 Mega Car Sale")
    st.write("🚘 Flat 20% OFF on New Cars")
    st.write("📞 1800-CAR-SALE")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="ad">', unsafe_allow_html=True)
    st.subheader("⚡ Insurance Offer")
    st.write("🛡️ Free Insurance for 1 Year")
    st.write("💳 No Cost EMI")
    st.markdown("</div>", unsafe_allow_html=True)

    st.image(
        "https://media.giphy.com/media/l0HlQ7LRal8P6m9So/giphy.gif",
        caption="AI analysing your car 🚀",
        use_container_width=True
    )

# ================= Prepare Input =================
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

# ================= Prediction =================
st.markdown("---")
mid = st.columns(3)[1]

with mid:
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

        # ================= Animated Chart =================
        chart_df = pd.DataFrame({
            "Scenario": ["Low", "Predicted", "High"],
            "Price (Lakhs)": [prediction * 0.85, prediction, prediction * 1.15]
        })

        chart = alt.Chart(chart_df).mark_bar(
            cornerRadiusTopLeft=10,
            cornerRadiusTopRight=10
        ).encode(
            x="Scenario",
            y="Price (Lakhs)",
            color="Scenario",
            tooltip=["Price (Lakhs)"]
        ).properties(
            height=300
        )

        st.altair_chart(chart, use_container_width=True)

# ================= Footer =================
st.markdown(
    '<div class="footer">✨ AI • Streamlit • ML • Future Tech ✨</div>',
    unsafe_allow_html=True
)
