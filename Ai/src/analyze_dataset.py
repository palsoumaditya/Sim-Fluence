import os
import time
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

def analyze_dataset():
    """Analyze the actual dataset and training process"""
    print("🔍 COMPREHENSIVE DATASET ANALYSIS")
    print("=" * 60)
    
    csv_path = "../data/simfluence_reddit_training_fixed.csv"
    
    # Check file details
    print(f"\n📁 FILE ANALYSIS:")
    file_size = os.path.getsize(csv_path)
    print(f"File path: {csv_path}")
    print(f"File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
    
    # Count lines manually
    with open(csv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f"Total lines in file: {len(lines):,}")
    print(f"Data rows (excluding header): {len(lines)-1:,}")
    
    # Read with pandas
    print(f"\n📊 PANDAS READ ANALYSIS:")
    start_time = time.time()
    df = pd.read_csv(csv_path)
    read_time = time.time() - start_time
    
    print(f"Pandas read time: {read_time:.2f} seconds")
    print(f"DataFrame shape: {df.shape}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    
    # Check for duplicates
    print(f"\n🔍 DATA QUALITY:")
    print(f"Duplicate rows: {df.duplicated().sum()}")
    print(f"Unique rows: {len(df.drop_duplicates())}")
    
    # Check data distribution
    print(f"\n📈 DATA DISTRIBUTION:")
    print(f"Received Likes:")
    print(f"  - Min: {df['receivedLikes'].min()}")
    print(f"  - Max: {df['receivedLikes'].max()}")
    print(f"  - Mean: {df['receivedLikes'].mean():.2f}")
    print(f"  - Median: {df['receivedLikes'].median():.2f}")
    
    # Check for missing values
    print(f"\n🔍 MISSING VALUES:")
    missing_counts = df.isnull().sum()
    total_missing = missing_counts.sum()
    print(f"Total missing values: {total_missing}")
    if total_missing > 0:
        print(missing_counts[missing_counts > 0])
    
    # Now test the full preprocessing and training
    print(f"\n🔄 FULL PREPROCESSING TEST:")
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
                print(f"  Filled {df[col].isnull().sum()} missing values in {col}")
    
    # One-hot encode categorical features
    categorical_columns = ['postTimeOfDay', 'dayOfWeek', 'topCommentSentiment']
    df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)
    
    # Define feature columns
    feature_columns = df.drop([
        'receivedLikes', 'receivedComments', 'receivedShares',
        'suggestions', 'postText', 'hashtags'
    ], axis=1).columns.tolist()
    
    preprocessing_time = time.time() - start_time
    print(f"✅ Preprocessing completed! Time: {preprocessing_time:.2f} seconds")
    print(f"   Final shape: {df.shape}")
    print(f"   Feature columns: {len(feature_columns)}")
    
    # Test actual training with detailed timing
    print(f"\n⚙️ DETAILED TRAINING TEST:")
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
    
    # Train model with detailed timing
    print(f"\n🚀 TRAINING WITH DETAILED TIMING:")
    start_time = time.time()
    
    # Use more trees and verbose output
    model = XGBRegressor(
        random_state=42, 
        n_estimators=100, 
        verbosity=1,
        max_depth=6,
        learning_rate=0.1
    )
    
    print(f"   Starting training...")
    model.fit(X_train, y_train)
    
    training_time = time.time() - start_time
    
    print(f"✅ Training completed! Time: {training_time:.2f} seconds")
    
    # Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"   MSE: {mse:.2f}")
    
    # Detailed analysis
    print(f"\n⏱️ DETAILED TIMING ANALYSIS:")
    print(f"   File read time: {read_time:.2f} seconds")
    print(f"   Preprocessing time: {preprocessing_time:.2f} seconds")
    print(f"   Training time: {training_time:.2f} seconds")
    print(f"   Total time: {read_time + preprocessing_time + training_time:.2f} seconds")
    print(f"   Training samples: {len(X_train):,}")
    print(f"   Features: {len(feature_columns)}")
    print(f"   Time per sample: {training_time/len(X_train)*1000:.2f} milliseconds")
    
    # Check if training time is reasonable
    expected_time = len(X_train) * len(feature_columns) * 0.0001  # Rough estimate
    print(f"\n📊 EXPECTED vs ACTUAL:")
    print(f"   Expected training time: {expected_time:.2f} seconds")
    print(f"   Actual training time: {training_time:.2f} seconds")
    
    if training_time < 5:
        print(f"   ⚠️  WARNING: Training completed very quickly!")
        print(f"   This might indicate:")
        print(f"     - Model is not training properly")
        print(f"     - Data is too simple")
        print(f"     - Model parameters are too basic")
    else:
        print(f"   ✅ Training time seems reasonable")
    
    print(f"\n🎯 CONCLUSION:")
    print(f"   Dataset size: {len(df):,} samples")
    print(f"   Features: {len(feature_columns)}")
    print(f"   Training time: {training_time:.2f} seconds")
    print(f"   Model performance: MSE = {mse:.2f}")

if __name__ == "__main__":
    analyze_dataset() 