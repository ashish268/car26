import streamlit as st
import pickle
import pandas as pd
import numpy as np

# ---------------- LOAD MODEL ----------------
model_data = pickle.load(open("used_car_model.pkl", "rb"))
model = model_data["model"]
model_columns = model_data["columns"]

st.title("🚗 Used Car Price Prediction")

# ---------------- USER INPUTS ----------------
year = st.number_input("Year of Purchase", min_value=1995, max_value=2025, value=2015)
km = st.number_input("Kilometers Driven", min_value=0, value=50000)
seats = st.number_input("Seats", min_value=2, max_value=10, value=5)

fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Electric", "LPG"])
transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
owner = st.selectbox("Owner Type", ["First", "Second", "Third", "Fourth & Above"])

brand = st.selectbox(
    "Car Brand",
    [
        "Audi","BMW","Bentley","Chevrolet","Datsun","Fiat","Force","Ford",
        "Hindustan","Honda","Hyundai","ISUZU","Isuzu","Jaguar","Jeep",
        "Lamborghini","Land","Mahindra","Maruti","Mercedes-Benz","Mini",
        "Mitsubishi","Nissan","OpelCorsa","Porsche","Renault","Skoda",
        "Smart","Tata","Toyota","Volkswagen","Volvo"
    ]
)

# ---------------- PREDICTION ----------------
if st.button("Predict Price"):

    # Create input dataframe with ALL training columns
    input_df = pd.DataFrame(
        np.zeros((1, len(model_columns))),
        columns=model_columns
    )

    # Numeric features
    if "Year" in input_df.columns:
        input_df["Year"] = year
    if "Kilometers_Driven" in input_df.columns:
        input_df["Kilometers_Driven"] = km
    if "Seats" in input_df.columns:
        input_df["Seats"] = seats

    # Fuel type
    fuel_col = f"Fuel_Type_{fuel}"
    if fuel_col in input_df.columns:
        input_df[fuel_col] = 1

    # Transmission
    if transmission == "Manual" and "Transmission_Manual" in input_df.columns:
        input_df["Transmission_Manual"] = 1

    # Owner type
    owner_col = f"Owner_Type_{owner}"
    if owner_col in input_df.columns:
        input_df[owner_col] = 1

    # -------- BRAND (MAIN ADDITION) --------
    brand_col = f"Brand_{brand}"
    if brand_col in input_df.columns:
        input_df[brand_col] = 1

    # Predict
    price = model.predict(input_df)[0]

# Fix unrealistic negative prediction
price = max(price, 0)

st.success(f"💰 Estimated Car Price: ₹ {price:.2f} Lakhs")
