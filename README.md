
# Customer Churn Prediction

This project predicts customer churn based on various features using machine learning models. The system allows businesses to input customer-related information and predicts whether the customer will churn.

## Project Structure

```
customer-churn-prediction/
├── api/
│   └── api.py             # API implementation for the prediction model
├── data/
│   └── [dataset files]    # Data files used for model training and testing
├── model/
│   ├── model.py           # Model training and evaluation code
│   └── model.pkl          # Saved trained model
├── notebooks/
│   ├── V_Kottaplli_data_preprocessing.ipynb  # Data preprocessing notebook
│   ├── V_Kottaplli_Model_building.ipynb      # Model building notebook
├── ui/
│   └── main.py            # Streamlit app for user interaction
├── LICENSE                # License file
├── README.md              # Project description and instructions
```

## Installation

To set up the environment and run this project, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/customer-churn-prediction.git
   ```

2. **Install dependencies:**  
   Ensure you have Python installed, and then install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

   If a `requirements.txt` file is not available, install necessary libraries manually:
   ```bash
   pip install streamlit scikit-learn pandas numpy requests
   ```

3. **Run the Streamlit UI:**  
   Once the environment is set up, you can start the UI:
   ```bash
   streamlit run ui/main.py
   ```

4. **API:**  
   If you want to test or deploy the model via an API, run the `api/api.py` script to start a Flask-based API.

## Features

- **Customer Churn Prediction:** Predict whether a customer will churn based on their demographic and usage data.
- **Interactive UI:** A simple, user-friendly interface built using Streamlit for easy input and prediction results.

## Model Details

The project uses a machine learning model trained on customer churn data. The model is saved in the `model/model.pkl` file, which can be loaded and used to make predictions.

### Key Factors Affecting Prediction:
- Customer tenure
- Monthly charges
- Total spent
- Customer demographics (age, gender, etc.)
- Service usage patterns

## How to Use

Enter the details of the customer you want to predict the churn for, such as:
- Customer tenure
- Monthly charges
- Total spent
- Customer demographics (age, gender, etc.)
- Service usage patterns

Click the "Predict Churn" button to receive the churn prediction result.

## Contributing

If you would like to contribute to this project, please fork the repository and create a pull request with your proposed changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Created by

Venkatalakshmi Kottapalli, Yeshiva University
