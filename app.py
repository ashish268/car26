import streamlit as st
import joblib
import pandas as pd

# ==============================
# Load Model (from dict)
# ==============================
data = joblib.load("car_model.pkl")
model = data['model']          # pipeline model
columns = data['columns']      # training columns

# ==============================
# Login System
# ==============================
PASSWORD = "12345"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 Login Page")
    pwd = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        if pwd == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
        else:
            st.error("Wrong Password ❌")

# ==============================
# Prediction Page
# ==============================
def prediction_page():
    st.title("🚗 Used Car Price Prediction")

    # Example inputs (modify based on your dataset)
    brand = st.text_input("Brand")
    km_driven = st.number_input("KM Driven", 0)
    fuel = st.text_input("Fuel Type")
    car_age = st.number_input("Car Age", 0)

    if st.button("Predict Price"):
        # Create input dataframe
        input_dict = {
            'brand': brand,
            'km_driven': km_driven,
            'fuel': fuel,
            'car_age': car_age
        }

        input_df = pd.DataFrame([input_dict])

        # Ensure same columns as training
        for col in columns:
            if col not in input_df:
                input_df[col] = 0

        input_df = input_df[columns]

        # Prediction
        prediction = model.predict(input_df)

        st.success(f"Estimated Price: ₹ {int(prediction[0])}")

# ==============================
# Main Flow
# ==============================
if not st.session_state.logged_in:
    login()
else:
    prediction_page()
