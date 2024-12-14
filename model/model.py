# Import the libraries
import os
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data function
def load_data(filepath):
    return pd.read_csv(filepath)

# Load model function
def load_model(model_path):
    return joblib.load(model_path)

# Train model function
def train_model(X, y, params=None):
    if params:
        model = RandomForestClassifier(**params, random_state=42)
    else:
        model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model

# Test model function
def test_model(X, y, model):
    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)
    roc_auc = roc_auc_score(y, model.predict_proba(X)[:, 1])
    conf_matrix = confusion_matrix(y, y_pred)
    conf_matrix_normalized = conf_matrix.astype('float') / conf_matrix.sum(axis=1)[:, np.newaxis]
    
    print("Classification Report:")
    print(classification_report(y, y_pred, target_names=['No Churn', 'Churn']))
    
    # Plot the normalized confusion matrix
    plt.figure(figsize=(5, 3))
    sns.heatmap(conf_matrix_normalized, annot=True, fmt='.2f', cmap='Blues', 
                xticklabels=['No Churn', 'Churn'], yticklabels=['No Churn', 'Churn'])
    plt.title('Normalized Confusion Matrix (Random Forest)')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

    return accuracy, roc_auc

# Save model function
def save_model(model, filename, dirpath=''):
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    joblib.dump(model, f"{dirpath}/{filename}")

if __name__ == "__main__":
    # Load data
    data = load_data("https://raw.githubusercontent.com/Venkatalakshmikottapalli/Customer-Churn-Prediction/refs/heads/main/data/processed/Customer_Churn_Pred.csv")

    # Prepare train and test data
    X = data.drop('Churn', axis=1)  
    y = data['Churn']  
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model with the best hyperparameters
    best_params = {
        'n_estimators': 300,
        'min_samples_split': 2,
        'min_samples_leaf': 1,
        'max_features': 'sqrt',
        'max_depth': 20,
        'bootstrap': False
    }
    model = train_model(X_train, y_train, best_params)

    # Test the model
    accuracy, roc_auc = test_model(X_test, y_test, model)
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print(f"ROC-AUC: {roc_auc:.3f}")

    # Save the trained model 
    model_path = os.path.join(os.path.dirname(__file__), 'churn_rf_model.pkl')
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
