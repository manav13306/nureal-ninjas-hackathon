from flask import Flask, request, jsonify
from model import predict_risk, train_initial_model
import threading

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "SafeRoute AI Prediction Service"

@app.route('/predict_risk', methods=['POST'])
def predict():
    data = request.json
    try:
        # data expected: { "speed": 60, "density": 0.8, "weather": "rain", "timeOfDay": 14 }
        # simplified features for model: [speed (km/h), density (0-1), is_rainy (0/1), hour (0-23)]
        
        speed = data.get('speed', 50)
        density = data.get('density', 0.5)
        weather = 1 if data.get('weather', '').lower() in ['rain', 'snow', 'storm'] else 0
        timeOfDay = data.get('timeOfDay', 12)
        
        features = [[speed, density, weather, timeOfDay]]
        risk_score = predict_risk(features)
        
        return jsonify({
            "risk_score": float(risk_score),
            "level": "High" if risk_score > 0.7 else "Medium" if risk_score > 0.4 else "Low"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/recalculate', methods=['POST'])
def recalculate():
    # Placeholder for updating risk zones based on newly reported incidents
    data = request.json
    print(f"Received new incident report for recalculation: {data}")
    # In a real app we'd fetch the latest traffic density and query the DB
    return jsonify({"status": "acknowledged", "risk_updated": True})

if __name__ == '__main__':
    # Train the initial model in a background thread or straight away
    train_initial_model()
    app.run(host='0.0.0.0', port=5001)
