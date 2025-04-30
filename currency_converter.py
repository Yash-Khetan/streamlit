import streamlit as st
import requests 
st.title("Live currency converter")
amount = st.number_input("Enter the amount(INR)", min_value = 1)
currency = st.selectbox("Convert to ",["USD","EUR","AED"])

if st.button("Convert"):
    url = "https://api.exchangerate-api.com/v4/latest/INR"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        rates = data["rates"][currency]
        converted_value = rates * amount
        st.success(f"Conversion of {amount}  in {currency} is {converted_value}")
    else:
        st.error("Failed to fetch conversion rate!")
