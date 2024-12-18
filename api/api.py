# Import required libraries
import os
import joblib
from flask import Flask, request, jsonify

# Set up Flask app
app = Flask(__name__)

# Load the trained model
try:
    model_path = os.path.join(os.path.dirname(__file__), '../model/churn_rf_model.pkl')
    model = joblib.load(model_path)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading the model: {str(e)}")
    model = None

# Route for health check
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Churn Prediction API is running."})

# Route for predictionS
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded.'}), 500
    
    try:
        # Parse JSON input
        data = request.json
        input_data = [
            int(data['gender']),
            int(data['SeniorCitizen']),
            int(data['Partner']),
            int(data['Dependents']),
            int(data['tenure']),
            int(data['MultipleLines']),
            int(data['InternetService']),
            int(data['OnlineSecurity']),
            int(data['OnlineBackup']),
            int(data['DeviceProtection']),
            int(data['TechSupport']),
            int(data['Contract']),
            int(data['PaperlessBilling']),
            int(data['PaymentMethod']),
            float(data['MonthlyCharges']),
            float(data['TotalCharges'])
        ]

        # Make prediction
        prediction_proba = model.predict_proba([input_data])[0][1]  # Probability of churn
        if prediction_proba < 0.4:
            churn_label = "No Churn"
        elif 0.4 <= prediction_proba < 0.7:
            churn_label = "Likely to Churn"
        else:
            churn_label = "Churn"

        # Return prediction result
        return jsonify({
            'risk_probability': round(prediction_proba, 2),
            'prediction': churn_label
        })
        
    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
