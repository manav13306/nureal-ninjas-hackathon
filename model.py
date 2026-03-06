from sklearn.ensemble import RandomForestRegressor
import numpy as np
import os
import joblib

MODEL_PATH = 'risk_model.pkl'

def train_initial_model():
    if os.path.exists(MODEL_PATH):
        print("Model already exists. Skipping training.")
        return
        
    print("Training initial dummy Random Forest model...")
    # Features: [speed (km/h), density (0-1), is_rainy (0/1), hour (0-23)]
    # Target: risk score (0-1.0)
    
    # Generate some mock data
    np.random.seed(42)
    # 1000 samples
    X = np.random.rand(1000, 4)
    # Adjust ranges
    X[:, 0] = X[:, 0] * 120  # speed 0-120
    X[:, 1] = X[:, 1]        # density 0-1
    X[:, 2] = np.round(X[:, 2]) # rainy or not
    X[:, 3] = X[:, 3] * 23   # hour 0-23

    # Create a dummy risk function
    # Risk goes up with speed, density, rain, and night time
    y = (X[:, 0] / 120.0 * 0.3) + (X[:, 1] * 0.4) + (X[:, 2] * 0.2) + (np.abs(X[:, 3] - 12) / 12.0 * 0.1)
    y = np.clip(y, 0.0, 1.0)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    joblib.dump(model, MODEL_PATH)
    print("Model trained and saved.")

def predict_risk(features):
    try:
        model = joblib.load(MODEL_PATH)
        return model.predict(features)[0]
    except Exception as e:
        print(f"Error loading model: {e}")
        return 0.5 # default moderate risk
