"""
Flask Web Application for House Price Prediction
"""
from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load model and scaler
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model')

def load_model():
    """Load the trained model and scaler"""
    model_path = os.path.join(MODEL_DIR, 'model.pkl')
    scaler_path = os.path.join(MODEL_DIR, 'scaler.pkl')
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        raise FileNotFoundError(
            "Model files not found. Please run 'python model/train_model.py' first."
        )
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    return model, scaler

# Load model at startup
try:
    model, scaler = load_model()
    print("✅ Model loaded successfully!")
except FileNotFoundError as e:
    print(f"⚠️ {e}")
    model, scaler = None, None


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for house price prediction"""
    try:
        if model is None or scaler is None:
            return jsonify({
                'success': False,
                'error': 'Model not loaded. Please train the model first.'
            }), 500
        
        # Get data from request
        data = request.get_json()
        
        # Extract features in correct order
        features = np.array([[
            float(data.get('MedInc', 0)),
            float(data.get('HouseAge', 0)),
            float(data.get('AveRooms', 0)),
            float(data.get('AveBedrms', 0)),
            float(data.get('Population', 0)),
            float(data.get('AveOccup', 0)),
            float(data.get('Latitude', 0)),
            float(data.get('Longitude', 0))
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Predict
        prediction = model.predict(features_scaled)[0]
        
        # Convert to price (model predicts in $100K units)
        price_100k = prediction
        price_usd = prediction * 100000
        
        return jsonify({
            'success': True,
            'prediction': {
                'price_100k': round(price_100k, 2),
                'price_usd': round(price_usd, 0),
                'price_formatted': f"${price_usd:,.0f}"
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/feature-ranges', methods=['GET'])
def get_feature_ranges():
    """Return typical feature ranges for the UI"""
    return jsonify({
        'MedInc': {'min': 0.5, 'max': 15, 'default': 3.5, 'step': 0.1, 
                   'label': 'Median Income', 'unit': '$10,000s'},
        'HouseAge': {'min': 1, 'max': 52, 'default': 25, 'step': 1,
                     'label': 'House Age', 'unit': 'years'},
        'AveRooms': {'min': 1, 'max': 10, 'default': 5, 'step': 0.1,
                     'label': 'Average Rooms', 'unit': 'rooms'},
        'AveBedrms': {'min': 0.5, 'max': 5, 'default': 1, 'step': 0.1,
                      'label': 'Average Bedrooms', 'unit': 'rooms'},
        'Population': {'min': 100, 'max': 10000, 'default': 1500, 'step': 100,
                       'label': 'Population', 'unit': 'people'},
        'AveOccup': {'min': 1, 'max': 10, 'default': 3, 'step': 0.1,
                     'label': 'Average Occupancy', 'unit': 'people'},
        'Latitude': {'min': 32.5, 'max': 42, 'default': 35.5, 'step': 0.1,
                     'label': 'Latitude', 'unit': '°N'},
        'Longitude': {'min': -124.5, 'max': -114, 'default': -119.5, 'step': 0.1,
                      'label': 'Longitude', 'unit': '°W'}
    })


if __name__ == '__main__':
    print("\n🏠 House Price Prediction Web App")
    print("=" * 40)
    print("Starting server at http://localhost:5000")
    print("=" * 40 + "\n")
    app.run(debug=True, port=5000)
