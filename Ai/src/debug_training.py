import os
import time
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

def debug_training_process():
    """Debug the training process to see what's actually happening"""
    print("🔍 DEBUGGING TRAINING PROCESS")
    print("=" * 50)
    
    # Check the CSV file first
    csv_path = "../data/simfluence_reddit_training_fixed.csv"
    
    print(f"\n📊 CHECKING CSV FILE:")
    print(f"File path: {csv_path}")
    
    # Check if file exists
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return
    
    # Get file size
    file_size = os.path.getsize(csv_path)
    print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    
    # Try to read with different methods
    print(f"\n🔍 ATTEMPTING TO READ CSV:")
    
    try:
        # Method 1: Basic pandas read
        print("Method 1: Basic pandas read...")
        start_time = time.time()
        df = pd.read_csv(csv_path)
        end_time = time.time()
        print(f"✅ Success! Time: {end_time - start_time:.2f} seconds")
        print(f"   Rows: {len(df):,}")
        print(f"   Columns: {len(df.columns)}")
        print(f"   Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB")
        
        # Show sample data
        print(f"\n📋 SAMPLE DATA:")
        print(f"First 3 rows:")
        print(df.head(3).to_string())
        
        # Check for missing values
        print(f"\n🔍 MISSING VALUES:")
        missing_counts = df.isnull().sum()
        print(missing_counts[missing_counts > 0])
        
        # Check data types
        print(f"\n📊 DATA TYPES:")
        print(df.dtypes)
        
        # Check unique values in key columns
        print(f"\n🎯 UNIQUE VALUES:")
        print(f"postTimeOfDay: {df['postTimeOfDay'].nunique()} unique values")
        print(f"dayOfWeek: {df['dayOfWeek'].nunique()} unique values")
        print(f"topCommentSentiment: {df['topCommentSentiment'].nunique()} unique values")
        
        # Now try the actual preprocessing
        print(f"\n🔄 TESTING PREPROCESSING:")
        start_time = time.time()
        
        # Convert string boolean to int
        df['containsImage'] = df['containsImage'].map({'True': 1, 'False': 0})
        df['shouldImprove'] = df['shouldImprove'].map({'True': 1, 'False': 0})
        
        # Convert numeric columns
        numeric_columns = ['length', 'userFollowers', 'userFollowing', 'userKarma', 
                          'accountAgeDays', 'avgEngagementRate', 'avgLikes', 'avgComments',
                          'receivedLikes', 'receivedComments', 'receivedShares']
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                if df[col].isnull().sum() > 0:
                    median_val = df[col].median()
                    df[col] = df[col].fillna(median_val)
                    print(f"Filled {df[col].isnull().sum()} missing values in {col}")
        
        # One-hot encode categorical features
        categorical_columns = ['postTimeOfDay', 'dayOfWeek', 'topCommentSentiment']
        df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)
        
        # Define feature columns
        feature_columns = df.drop([
            'receivedLikes', 'receivedComments', 'receivedShares',
            'suggestions', 'postText', 'hashtags'
        ], axis=1).columns.tolist()
        
        end_time = time.time()
        print(f"✅ Preprocessing completed! Time: {end_time - start_time:.2f} seconds")
        print(f"   Final shape: {df.shape}")
        print(f"   Feature columns: {len(feature_columns)}")
        
        # Test actual training
        print(f"\n⚙️ TESTING ACTUAL TRAINING:")
        X = df[feature_columns]
        y = df['receivedLikes']
        
        print(f"   X shape: {X.shape}")
        print(f"   y shape: {y.shape}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"   X_train shape: {X_train.shape}")
        print(f"   X_test shape: {X_test.shape}")
        
        # Train model with timing
        print(f"\n🚀 TRAINING MODEL:")
        start_time = time.time()
        
        model = XGBRegressor(random_state=42, n_estimators=100, verbosity=0)
        model.fit(X_train, y_train)
        
        end_time = time.time()
        training_time = end_time - start_time
        
        print(f"✅ Training completed! Time: {training_time:.2f} seconds")
        
        # Evaluate
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"   MSE: {mse:.2f}")
        
        # Check if training time is reasonable
        print(f"\n⏱️ TRAINING TIME ANALYSIS:")
        print(f"   Training time: {training_time:.2f} seconds")
        print(f"   Training samples: {len(X_train):,}")
        print(f"   Features: {len(feature_columns)}")
        print(f"   Time per sample: {training_time/len(X_train)*1000:.2f} milliseconds")
        
        if training_time < 5:
            print(f"   ⚠️  WARNING: Training completed very quickly!")
            print(f"   This might indicate the model is not training properly")
        else:
            print(f"   ✅ Training time seems reasonable")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_training_process() 