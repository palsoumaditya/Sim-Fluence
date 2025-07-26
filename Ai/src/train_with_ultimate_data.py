import os
import time
import joblib
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

def train_with_ultimate_data():
    """Train models with the ultimate fixed CSV file"""
    print("🚀 TRAINING WITH ULTIMATE FIXED DATASET")
    print("=" * 60)
    
    # Use the ultimate fixed CSV file
    DATA_PATH = "../data/simfluence_reddit_training_ultimate.csv"
    
    print(f"📊 Loading dataset: {DATA_PATH}")
    start_time = time.time()
    
    # Load the dataset
    df = pd.read_csv(DATA_PATH)
    load_time = time.time() - start_time
    
    print(f"✅ Dataset loaded successfully!")
    print(f"   Shape: {df.shape}")
    print(f"   Load time: {load_time:.2f} seconds")
    print(f"   Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    
    # Check data quality
    print(f"\n🔍 DATA QUALITY CHECK:")
    print(f"   Total samples: {len(df):,}")
    print(f"   Missing values: {df.isnull().sum().sum()}")
    print(f"   Duplicate rows: {df.duplicated().sum()}")
    
    # Show sample data
    print(f"\n📋 SAMPLE DATA:")
    print(df.head(3)[['postText', 'receivedLikes', 'receivedComments', 'receivedShares']])
    
    # Preprocessing
    print(f"\n🔄 PREPROCESSING DATA:")
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
                print(f"   Filled {df[col].isnull().sum()} missing values in {col}")
    
    # Handle categorical columns
    categorical_columns = ['postTimeOfDay', 'dayOfWeek', 'topCommentSentiment']
    for col in categorical_columns:
        if col in df.columns and df[col].isnull().sum() > 0:
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)
            print(f"   Filled {df[col].isnull().sum()} missing values in {col}")
    
    # One-hot encode categorical features
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
    
    # Prepare data for training
    X = df[feature_columns]
    y_likes = df['receivedLikes']
    y_comments = df['receivedComments']
    y_shares = df['receivedShares']
    
    print(f"\n📈 TRAINING DATA SUMMARY:")
    print(f"   Features shape: {X.shape}")
    print(f"   Likes target shape: {y_likes.shape}")
    print(f"   Comments target shape: {y_comments.shape}")
    print(f"   Shares target shape: {y_shares.shape}")
    
    # Split data
    X_train, X_test, y_train_likes, y_test_likes = train_test_split(
        X, y_likes, test_size=0.2, random_state=42
    )
    _, _, y_train_comments, y_test_comments = train_test_split(
        X, y_comments, test_size=0.2, random_state=42
    )
    _, _, y_train_shares, y_test_shares = train_test_split(
        X, y_shares, test_size=0.2, random_state=42
    )
    
    print(f"   Training samples: {len(X_train):,}")
    print(f"   Test samples: {len(X_test):,}")
    
    # Train models with detailed timing
    models = {}
    
    # Train Likes Model
    print(f"\n⚙️ TRAINING LIKES MODEL:")
    start_time = time.time()
    
    likes_model = XGBRegressor(
        random_state=42, 
        n_estimators=100, 
        max_depth=6,
        learning_rate=0.1,
        verbosity=0
    )
    
    likes_model.fit(X_train, y_train_likes)
    likes_training_time = time.time() - start_time
    
    y_pred_likes = likes_model.predict(X_test)
    likes_mse = mean_squared_error(y_test_likes, y_pred_likes)
    likes_r2 = r2_score(y_test_likes, y_pred_likes)
    
    print(f"✅ Likes model trained!")
    print(f"   Training time: {likes_training_time:.2f} seconds")
    print(f"   MSE: {likes_mse:.2f}")
    print(f"   R² Score: {likes_r2:.4f}")
    
    # Train Comments Model
    print(f"\n⚙️ TRAINING COMMENTS MODEL:")
    start_time = time.time()
    
    comments_model = XGBRegressor(
        random_state=42, 
        n_estimators=100, 
        max_depth=6,
        learning_rate=0.1,
        verbosity=0
    )
    
    comments_model.fit(X_train, y_train_comments)
    comments_training_time = time.time() - start_time
    
    y_pred_comments = comments_model.predict(X_test)
    comments_mse = mean_squared_error(y_test_comments, y_pred_comments)
    comments_r2 = r2_score(y_test_comments, y_pred_comments)
    
    print(f"✅ Comments model trained!")
    print(f"   Training time: {comments_training_time:.2f} seconds")
    print(f"   MSE: {comments_mse:.2f}")
    print(f"   R² Score: {comments_r2:.4f}")
    
    # Train Shares Model
    print(f"\n⚙️ TRAINING SHARES MODEL:")
    start_time = time.time()
    
    shares_model = XGBRegressor(
        random_state=42, 
        n_estimators=100, 
        max_depth=6,
        learning_rate=0.1,
        verbosity=0
    )
    
    shares_model.fit(X_train, y_train_shares)
    shares_training_time = time.time() - start_time
    
    y_pred_shares = shares_model.predict(X_test)
    shares_mse = mean_squared_error(y_test_shares, y_pred_shares)
    shares_r2 = r2_score(y_test_shares, y_pred_shares)
    
    print(f"✅ Shares model trained!")
    print(f"   Training time: {shares_training_time:.2f} seconds")
    print(f"   MSE: {shares_mse:.2f}")
    print(f"   R² Score: {shares_r2:.4f}")
    
    # Save models
    print(f"\n💾 SAVING MODELS:")
    
    joblib.dump({
        "model": likes_model,
        "features": feature_columns
    }, "../models/likes_predictor.pkl")
    
    joblib.dump({
        "model": comments_model,
        "features": feature_columns
    }, "../models/comments_predictor.pkl")
    
    joblib.dump({
        "model": shares_model,
        "features": feature_columns
    }, "../models/shares_predictor.pkl")
    
    print(f"✅ All models saved successfully!")
    
    # Final summary
    total_training_time = likes_training_time + comments_training_time + shares_training_time
    total_time = load_time + preprocessing_time + total_training_time
    
    print(f"\n🎉 FINAL TRAINING SUMMARY:")
    print(f"   Dataset: {len(df):,} samples")
    print(f"   Features: {len(feature_columns)}")
    print(f"   Total time: {total_time:.2f} seconds")
    print(f"   Training time: {total_training_time:.2f} seconds")
    print(f"   Time per sample: {total_training_time/len(X_train)*1000:.2f} milliseconds")
    
    print(f"\n🏆 MODEL PERFORMANCE:")
    print(f"   Likes Model: MSE = {likes_mse:.2f}, R² = {likes_r2:.4f}")
    print(f"   Comments Model: MSE = {comments_mse:.2f}, R² = {comments_r2:.4f}")
    print(f"   Shares Model: MSE = {shares_mse:.2f}, R² = {shares_r2:.4f}")
    
    print(f"\n✅ TRAINING COMPLETED SUCCESSFULLY!")
    print(f"   All {len(df):,} samples processed!")
    print(f"   Models ready for production use!")

if __name__ == "__main__":
    train_with_ultimate_data() 