import streamlit as st
import requests
API_URL='http://127.0.0.1:8000/prediction'
st.title("👨🏻‍💼 INSURANCE PREMIUM PREDICTOR  ")
age = st.number_input("Age", min_value=1, max_value=100, value=25)
weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7)
income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0)

smoker = st.selectbox("Are you a smoker?", options=[True, False])

city = st.selectbox(
    "City",
    ["Mumbai", "Delhi", "Bangalore", "Pune", "Chennai"]
)

occupation = st.selectbox(
    "Occupation",
    ['retired', 'freelancer', 'student', 'government_job',
     'business_owner', 'unemployed', 'private_job']
)

if st.button("Predict Premium Category"):
    input = {
        "age": int(age),              
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }
    response = requests.post(API_URL, json=input)
    
    if response.status_code==200:
       result=response.json()
       st.success(f"Prediction : {result['prediction']}")
    else:
        st.error("Failed to predict properly......")    