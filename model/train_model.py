"""
Train and save the house price prediction model
"""
import pickle
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_squared_error
import os

def train_and_save_model():
    """Train Ridge Regression model and save it with scaler"""
    
    print("📊 Loading California Housing dataset...")
    california = fetch_california_housing()
    X = california.data
    y = california.target
    feature_names = california.feature_names
    
    print(f"   Dataset shape: {X.shape}")
    print(f"   Features: {feature_names}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    print("\n⚙️ Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Ridge model (best performer from notebook analysis)
    print("\n🤖 Training Ridge Regression model...")
    model = Ridge(alpha=1.0)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print(f"\n📈 Model Performance:")
    print(f"   R² Score: {r2:.4f}")
    print(f"   RMSE: ${rmse * 100:.2f}K")
    
    # Save model and scaler
    model_dir = os.path.dirname(os.path.abspath(__file__))
    
    model_path = os.path.join(model_dir, 'model.pkl')
    scaler_path = os.path.join(model_dir, 'scaler.pkl')
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"\n💾 Model saved to: {model_path}")
    
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"💾 Scaler saved to: {scaler_path}")
    
    # Save feature names for reference
    feature_info = {
        'feature_names': feature_names,
        'feature_descriptions': {
            'MedInc': 'Median Income (in $10,000s)',
            'HouseAge': 'House Age (years)',
            'AveRooms': 'Average Rooms per Household',
            'AveBedrms': 'Average Bedrooms per Household',
            'Population': 'Block Population',
            'AveOccup': 'Average Occupancy per Household',
            'Latitude': 'Latitude',
            'Longitude': 'Longitude'
        }
    }
    
    info_path = os.path.join(model_dir, 'feature_info.pkl')
    with open(info_path, 'wb') as f:
        pickle.dump(feature_info, f)
    print(f"💾 Feature info saved to: {info_path}")
    
    print("\n✅ Model training complete!")
    
    return model, scaler

if __name__ == "__main__":
    train_and_save_model()
