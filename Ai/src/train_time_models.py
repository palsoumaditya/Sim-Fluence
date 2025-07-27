#!/usr/bin/env python3
"""
Time Prediction Model Training Script
Trains models for optimal posting time prediction using timeline data
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from time_prediction import train_time_prediction_system

def main():
    """
    Main training function
    """
    print("🚀 Starting Time Prediction Model Training...")
    print("=" * 50)
    
    try:
        # Train the complete time prediction system
        engine = train_time_prediction_system()
        
        if engine:
            print("\n✅ Training completed successfully!")
            print(f"📊 Models trained:")
            print(f"   - Global model: ✅")
            print(f"   - Subreddit models: {len(engine.subreddit_models)}")
            print(f"   - Content type models: {len(engine.content_type_models)}")
            
            # Test the system
            print("\n🧪 Testing the trained models...")
            test_cases = [
                ("funny", "image"),
                ("technology", "text"),
                ("gaming", "video"),
                ("science", "link")
            ]
            
            for subreddit, content_type in test_cases:
                prediction = engine.predict_optimal_time(subreddit, content_type)
                print(f"   r/{subreddit} ({content_type}): {prediction['optimal_hour']:02d}:00 (confidence: {prediction['confidence']:.2f})")
            
            print("\n🎉 Time prediction system is ready!")
            print("📝 Next steps:")
            print("   1. The models are saved in the models/ directory")
            print("   2. The API will automatically load these models")
            print("   3. You can test the API endpoints:")
            print("      - POST /predict/optimal-time")
            print("      - POST /predict/time-engagement")
            print("      - GET /time/status")
            
        else:
            print("❌ Training failed!")
            return 1
            
    except Exception as e:
        print(f"❌ Error during training: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 