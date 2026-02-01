import streamlit as st
import pickle
import pandas as pd
import numpy as np

# ================= Page Config =================
st.set_page_config(
    page_title="AI Used Car Price Predictor",
    page_icon="🚗",
    layout="wide"
)

# ================= Custom CSS =================
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.main {
    background-color: #0e1117;
}
h1, h2, h3 {
    color: #00f5d4;
}
.card {
    background: #161b22;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 0 20px rgba(0,245,212,0.15);
}
.footer {
    text-align: center;
    color: gray;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ================= Load Model =================
data = pickle.load(open("used_car_model.pkl", "rb"))
model = data["model"]
model_columns = data["columns"]

# ================= Header =================
st.markdown("<h1>🚗 AI Used Car Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("##### Predict resale value using Machine Learning", unsafe_allow_html=True)
st.markdown("---")

# ================= Layout =================
left, right = st.columns([1.2, 1])

# ================= Inputs =================
with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔧 Car Specifications")

    year = st.slider("Year of Manufacture", 1995, 2025, 2018)
    kms_driven = st.slider("Kilometers Driven", 0, 200000, 50000)
    seats = st.selectbox("Seats", [2, 4, 5, 6, 7])

    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
    owner_type = st.selectbox("Owner Type", ["First", "Second", "Third", "Fourth & Above"])

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("⚙️ Engine & Performance")

    mileage = st.slider("Mileage (km/l)", 5.0, 35.0, 18.0)
    engine = st.slider("Engine Capacity (CC)", 500, 4000, 1200)
    power = st.slider("Power (bhp)", 40.0, 400.0, 90.0)
    new_price = st.slider("New Car Price (Lakhs ₹)", 2.0, 50.0, 8.0)

    st.markdown("</div>", unsafe_allow_html=True)

# ================= Prepare Input =================
input_dict = {
    "Year": year,
    "Kilometers_Driven": kms_driven,
    "Mileage": mileage,
    "Engine": engine,
    "Power": power,
    "Seats": seats,
    "New_Price": new_price,
    "Fuel_Type": fuel_type,
    "Transmission": transmission,
    "Owner_Type": owner_type
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
center = st.columns(3)[1]

with center:
    if st.button("🚀 Predict Price", use_container_width=True):
        prediction = model.predict(input_df)
        st.markdown(
            f"""
            <div class="card">
                <h2>💰 Estimated Price</h2>
                <h1>₹ {round(prediction[0], 2)} Lakhs</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

# ================= Footer =================
st.markdown(
    '<div class="footer">Built with ❤️ using Streamlit & Machine Learning</div>',
    unsafe_allow_html=True
)
