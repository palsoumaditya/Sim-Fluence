#!/usr/bin/env python3
"""
Test script for time prediction functionality
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from time_prediction import TimePredictionEngine
from time_predict import predict_optimal_time, format_time_prediction

def test_time_prediction():
    """Test the time prediction functionality"""
    print("🧪 Testing Time Prediction System...")
    print("=" * 40)
    
    # Test 1: Check if models can be loaded
    print("1. Testing model loading...")
    try:
        engine = TimePredictionEngine()
        engine.load_models()
        
        if engine.global_model:
            print("   ✅ Global model loaded successfully")
        else:
            print("   ⚠️  Global model not found (needs training)")
            
        print(f"   📊 Subreddit models: {len(engine.subreddit_models)}")
        print(f"   📊 Content models: {len(engine.content_type_models)}")
        
    except Exception as e:
        print(f"   ❌ Error loading models: {e}")
    
    # Test 2: Test prediction function
    print("\n2. Testing prediction function...")
    try:
        prediction = predict_optimal_time("funny", "image")
        print(f"   📈 Prediction result: {prediction}")
        
        if prediction.get("status") == "success":
            print("   ✅ Prediction successful")
        else:
            print("   ⚠️  Prediction returned fallback values")
            
    except Exception as e:
        print(f"   ❌ Error in prediction: {e}")
    
    # Test 3: Test formatting
    print("\n3. Testing response formatting...")
    try:
        test_prediction = {
            "optimal_hour": 15,
            "confidence": 0.85,
            "subreddit": "funny",
            "content_type": "image",
            "status": "success"
        }
        
        formatted = format_time_prediction(test_prediction)
        print(f"   📝 Formatted response: {formatted}")
        print("   ✅ Formatting successful")
        
    except Exception as e:
        print(f"   ❌ Error in formatting: {e}")
    
    # Test 4: Test different subreddits and content types
    print("\n4. Testing different scenarios...")
    test_cases = [
        ("funny", "image"),
        ("technology", "text"),
        ("gaming", "video"),
        ("science", "link")
    ]
    
    for subreddit, content_type in test_cases:
        try:
            prediction = predict_optimal_time(subreddit, content_type)
            hour = prediction.get("optimal_hour", 12)
            confidence = prediction.get("confidence", 0.5)
            print(f"   r/{subreddit} ({content_type}): {hour:02d}:00 (confidence: {confidence:.2f})")
        except Exception as e:
            print(f"   ❌ Error testing {subreddit}/{content_type}: {e}")
    
    print("\n🎉 Time prediction testing complete!")
    print("\n📝 Next steps:")
    print("   1. If models need training, run: python train_time_models.py")
    print("   2. Test API endpoints when server is running")
    print("   3. Integrate with your existing AI system")

if __name__ == "__main__":
    test_time_prediction() 