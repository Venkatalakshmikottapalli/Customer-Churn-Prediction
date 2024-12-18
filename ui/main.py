import streamlit as st
import requests

# Set the title of the app
st.title("Check Your Customer Churn")

# Description of the app
st.write("""
    This tool allows you to predict the likelihood of a customer churning based on their details. 
    Enter the customer's information below to get insights into whether they are at risk of leaving.
""")

# Collect user input using Streamlit forms
with st.form(key="churn_form"):
    gender = st.selectbox("Gender", ["Select", "Male", "Female"], index=0)
    senior_citizen = st.selectbox("Senior Citizen", ["Select", "Yes", "No"], index=0)
    partner = st.selectbox("Partner", ["Select", "Yes", "No"], index=0)
    dependents = st.selectbox("Dependents", ["Select", "Yes", "No"], index=0)

    # Textboxes for numerical features (allowing manual entry by typing)
    tenure = st.text_input("Tenure (Months)", "")  # Leave empty as default
    monthly_charges = st.text_input("Monthly Charges", "")  # Leave empty as default
    total_charges = st.text_input("Total Charges", "")  # Leave empty as default

    multiple_lines = st.selectbox("Multiple Lines", ["Select", "Yes", "No", "No phone service"], index=0)
    internet_service = st.selectbox("Internet Service", ["Select", "DSL", "Fiber optic", "No"], index=0)
    online_security = st.selectbox("Online Security", ["Select", "Yes", "No", "No internet service"], index=0)
    online_backup = st.selectbox("Online Backup", ["Select", "Yes", "No", "No internet service"], index=0)
    device_protection = st.selectbox("Device Protection", ["Select", "Yes", "No", "No internet service"], index=0)
    tech_support = st.selectbox("Tech Support", ["Select", "Yes", "No", "No internet service"], index=0)
    contract = st.selectbox("Contract", ["Select", "Month-to-month", "One year", "Two year"], index=0)
    paperless_billing = st.selectbox("Paperless Billing", ["Select", "Yes", "No"], index=0)
    payment_method = st.selectbox("Payment Method", ["Select", "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"], index=0)

    submit_button = st.form_submit_button(label="Predict Churn")

# When the form is submitted, make a request to the API
if submit_button:
    # Validate and convert the text inputs to numeric values
    try:
        tenure = int(tenure) if tenure else 0
        monthly_charges = float(monthly_charges) if monthly_charges else 0.0
        total_charges = float(total_charges) if total_charges else 0.0
    except ValueError:
        st.error("Please enter valid numbers in the text boxes.")
        tenure = 0  # Set default values in case of invalid input
        monthly_charges = 0.0
        total_charges = 0.0

    # Prepare data for API call
    data = {
        "gender": gender if gender != "Select" else None,
        "SeniorCitizen": 1 if senior_citizen == "Yes" else (0 if senior_citizen == "No" else None),
        "Partner": 1 if partner == "Yes" else (0 if partner == "No" else None),
        "Dependents": 1 if dependents == "Yes" else (0 if dependents == "No" else None),
        "tenure": tenure,
        "MultipleLines": 1 if multiple_lines == "Yes" else (0 if multiple_lines == "No" else -1 if multiple_lines == "No phone service" else None),
        "InternetService": 1 if internet_service == "DSL" else (2 if internet_service == "Fiber optic" else 0 if internet_service == "No" else None),
        "OnlineSecurity": 1 if online_security == "Yes" else (0 if online_security == "No" else -1 if online_security == "No internet service" else None),
        "OnlineBackup": 1 if online_backup == "Yes" else (0 if online_backup == "No" else -1 if online_backup == "No internet service" else None),
        "DeviceProtection": 1 if device_protection == "Yes" else (0 if device_protection == "No" else -1 if device_protection == "No internet service" else None),
        "TechSupport": 1 if tech_support == "Yes" else (0 if tech_support == "No" else -1 if tech_support == "No internet service" else None),
        "Contract": 0 if contract == "Month-to-month" else (1 if contract == "One year" else (2 if contract == "Two year" else None)),
        "PaperlessBilling": 1 if paperless_billing == "Yes" else (0 if paperless_billing == "No" else None),
        "PaymentMethod": 0 if payment_method == "Electronic check" else (1 if payment_method == "Mailed check" else (2 if payment_method == "Bank transfer (automatic)" else 3 if payment_method == "Credit card (automatic)" else None)),
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }

    # Send the request to the API
    api_url = "http://your-api-url/predict"  # Replace with your actual API URL
    response = requests.post(api_url, json=data)

    # Process the response
    if response.status_code == 200:
        prediction = response.json()
        risk = prediction['risk_probability']
        churn_label = prediction['prediction']

        # Display the results
        st.write(f"**Risk Probability:** {risk * 100:.2f}%")
        st.write(f"**Churn Prediction:** {churn_label}")

        # Display interactive message based on prediction
        if churn_label == "Churn":
            st.warning("This customer is at high risk of churning!")
        elif churn_label == "Likely to Churn":
            st.info("This customer is likely to churn. Consider retention strategies.")
        else:
            st.success("This customer is not likely to churn. They are loyal!")

    else:
        st.error("Failed to make a prediction. Please try again.")
