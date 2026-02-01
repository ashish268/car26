import streamlit as st
import pickle
import numpy as np
import pandas as pd

# ================= Load model & columns =================
data = pickle.load(open("used_car_model.pkl", "rb"))
model = data["model"]
model_columns = data["columns"]

st.set_page_config(page_title="Used Car Price Prediction", layout="centered")

st.title("🚗 Used Car Price Prediction")
st.write("Enter car details to predict the selling price")

# ================= User Inputs =================
year = st.number_input("Year of Manufacture", min_value=1995, max_value=2025, value=2018)

kms_driven = st.number_input("Kilometers Driven", min_value=0, value=50000)

mileage = st.number_input("Mileage (km/l)", min_value=0.0, value=18.0)

engine = st.number_input("Engine (CC)", min_value=500, value=1200)

power = st.number_input("Power (bhp)", min_value=20.0, value=80.0)

seats = st.selectbox("Seats", [2, 4, 5, 6, 7])

new_price = st.number_input("New Car Price (in Lakhs)", min_value=0.0, value=8.0)

fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
owner_type = st.selectbox("Owner Type", ["First", "Second", "Third", "Fourth & Above"])

# ================= Create input dataframe =================
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

# Apply same encoding as training
input_df = pd.get_dummies(
    input_df,
    columns=["Fuel_Type", "Transmission", "Owner_Type"],
    drop_first=True
)

# Align input with training columns
input_df = input_df.reindex(columns=model_columns, fill_value=0)

# ================= Prediction =================
if st.button("Predict Price"):
    prediction = model.predict(input_df)
    st.success(f"💰 Estimated Used Car Price: ₹ {round(prediction[0], 2)} Lakhs")
