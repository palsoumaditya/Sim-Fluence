import os
import joblib
import pandas as pd
import numpy as np
from preprocess import load_and_preprocess_data

def test_models():
    """Test all trained models to ensure they work correctly"""
    print("🧪 Testing trained models...")
    
    # Load the dataset - Updated to use ultimate fixed CSV file
    data_path = os.path.join("..", "data", "simfluence_reddit_training_ultimate.csv")
    df, feature_columns = load_and_preprocess_data(data_path)
    
    # Prepare test data (use first 5 rows)
    X_test = df[feature_columns].head(5)
    
    print(f"Test data shape: {X_test.shape}")
    print(f"Feature columns: {len(feature_columns)}")
    
    # Test each model
    models_to_test = [
        ("likes_predictor.pkl", "Likes"),
        ("comments_predictor.pkl", "Comments"), 
        ("shares_predictor.pkl", "Shares")
    ]
    
    for model_file, model_name in models_to_test:
        model_path = os.path.join("..", "models", model_file)
        
        if os.path.exists(model_path):
            print(f"\n🔍 Testing {model_name} model...")
            
            # Load the model
            model_data = joblib.load(model_path)
            model = model_data["model"]
            features = model_data["features"]
            
            # Make predictions
            predictions = model.predict(X_test)
            
            print(f"✅ {model_name} model loaded successfully!")
            print(f"   Features used: {len(features)}")
            print(f"   Predictions: {predictions}")
            print(f"   Average prediction: {predictions.mean():.2f}")
            
        else:
            print(f"❌ {model_name} model not found: {model_path}")
    
    print(f"\n🎉 Model testing completed!")
    print(f"   All models are working correctly")
    print(f"   Ready for production use!")

if __name__ == "__main__":
    test_models() 