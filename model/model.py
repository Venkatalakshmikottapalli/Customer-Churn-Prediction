import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb

# Load data function
def load_data(filepath):
    return pd.read_csv(filepath)

# Train model function
def train_model(X_train, y_train):
    # Initialize the model with the same hyperparameters
    model = xgb.XGBRegressor(
        learning_rate=0.1,   
        max_depth=7,         
        n_estimators=100,    
        subsample=1.0,       
        colsample_bytree=0.8, 
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

# Test model function
def test_model(X_test, y_test, model):
    # Make predictions with the trained model
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    # Print evaluation metrics
    print(f"Tuned XGBoost MSE: {mse}")
    print(f"Tuned XGBoost RMSE: {rmse}")
    print(f"Tuned XGBoost R²: {r2}")
    
    return mse, rmse, r2

# Save model function
def save_model(model, filename, dirpath=''):
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    joblib.dump(model, f"{dirpath}/{filename}")

if __name__ == "__main__":
    # Load the dataset
    data = load_data('https://raw.githubusercontent.com/Venkatalakshmikottapalli/House-Price-Prediction/refs/heads/main/data/processed/house_price_prediction.csv')  
    # Prepare train and test data
    X = data.drop(columns=['price'])  
    y = data['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model with the best hyperparameters
    model = train_model(X_train, y_train)

    # Test the model and evaluate performance
    mse, rmse, r2 = test_model(X_test, y_test, model)

    # Optionally, save the trained model
    model_path = os.path.join(os.path.dirname(__file__), 'xgb_model.pkl')
    save_model(model, 'xgb_model.pkl')
    print(f"Model saved to {model_path}")
