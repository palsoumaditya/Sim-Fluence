import os
import joblib
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# Constants - Updated to use fixed CSV file
DATA_PATH = os.path.join("..", "data", "simfluence_reddit_training_fixed.csv")
MODEL_SAVE_PATH = os.path.join("..", "models", "likes_predictor.pkl")

def clean_and_preprocess_data(csv_path: str):
    """Load and clean the dataset, ensuring all rows are properly processed"""
    print("📊 Loading dataset...")
    df = pd.read_csv(csv_path)
    print(f"Original dataset shape: {df.shape}")
    
    # Check for missing values
    print("\n🔍 Checking for missing values:")
    missing_counts = df.isnull().sum()
    print(missing_counts[missing_counts > 0])
    
    # Clean the data
    print("\n🧹 Cleaning data...")
    
    # Convert string boolean to int
    df['containsImage'] = df['containsImage'].map({'True': 1, 'False': 0})
    df['shouldImprove'] = df['shouldImprove'].map({'True': 1, 'False': 0})
    
    # Fill missing values in numeric columns
    numeric_columns = ['length', 'userFollowers', 'userFollowing', 'userKarma', 
                      'accountAgeDays', 'avgEngagementRate', 'avgLikes', 'avgComments',
                      'receivedLikes', 'receivedComments', 'receivedShares']
    
    for col in numeric_columns:
        if col in df.columns:
            # Convert to numeric, replacing errors with NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Fill NaN with median for numeric columns
            if df[col].isnull().sum() > 0:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                print(f"Filled {df[col].isnull().sum()} missing values in {col} with median: {median_val}")
    
    # Handle categorical columns
    categorical_columns = ['postTimeOfDay', 'dayOfWeek', 'topCommentSentiment']
    for col in categorical_columns:
        if col in df.columns and df[col].isnull().sum() > 0:
            # Fill missing categorical values with mode
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)
            print(f"Filled {df[col].isnull().sum()} missing values in {col} with mode: {mode_val}")
    
    # One-hot encode categorical features
    df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)
    
    # Define feature and label columns
    feature_columns = df.drop([
        'receivedLikes', 'receivedComments', 'receivedShares',
        'suggestions', 'postText', 'hashtags'
    ], axis=1).columns.tolist()
    
    print(f"\n✅ Cleaned dataset shape: {df.shape}")
    print(f"✅ Feature columns: {len(feature_columns)}")
    print(f"✅ No missing values remaining: {df.isnull().sum().sum() == 0}")
    
    return df, feature_columns

def train_and_save_model():
    print("🚀 Starting model training with cleaned data...")
    
    # Load and clean data
    df, feature_columns = clean_and_preprocess_data(DATA_PATH)
    
    # Prepare features and targets
    X = df[feature_columns]
    y_likes = df['receivedLikes']
    y_comments = df['receivedComments']
    y_shares = df['receivedShares']
    
    print(f"\n📈 Training data summary:")
    print(f"Features shape: {X.shape}")
    print(f"Likes target shape: {y_likes.shape}")
    print(f"Comments target shape: {y_comments.shape}")
    print(f"Shares target shape: {y_shares.shape}")
    
    # Split data for all models
    X_train, X_test, y_train_likes, y_test_likes = train_test_split(
        X, y_likes, test_size=0.2, random_state=42
    )
    _, _, y_train_comments, y_test_comments = train_test_split(
        X, y_comments, test_size=0.2, random_state=42
    )
    _, _, y_train_shares, y_test_shares = train_test_split(
        X, y_shares, test_size=0.2, random_state=42
    )
    
    # Train Likes Model
    print("\n⚙️ Training XGBoost regression model for likes...")
    likes_model = XGBRegressor(random_state=42, n_estimators=100)
    likes_model.fit(X_train, y_train_likes)
    
    y_pred_likes = likes_model.predict(X_test)
    mse_likes = mean_squared_error(y_test_likes, y_pred_likes)
    print(f"✅ Likes model trained! MSE: {mse_likes:.2f}")
    
    # Train Comments Model
    print("\n⚙️ Training XGBoost regression model for comments...")
    comments_model = XGBRegressor(random_state=42, n_estimators=100)
    comments_model.fit(X_train, y_train_comments)
    
    y_pred_comments = comments_model.predict(X_test)
    mse_comments = mean_squared_error(y_test_comments, y_pred_comments)
    print(f"✅ Comments model trained! MSE: {mse_comments:.2f}")
    
    # Train Shares Model
    print("\n⚙️ Training XGBoost regression model for shares...")
    shares_model = XGBRegressor(random_state=42, n_estimators=100)
    shares_model.fit(X_train, y_train_shares)
    
    y_pred_shares = shares_model.predict(X_test)
    mse_shares = mean_squared_error(y_test_shares, y_pred_shares)
    print(f"✅ Shares model trained! MSE: {mse_shares:.2f}")
    
    # Save models
    print("\n💾 Saving models...")
    joblib.dump({
        "model": likes_model,
        "features": feature_columns
    }, MODEL_SAVE_PATH)
    
    joblib.dump({
        "model": comments_model,
        "features": feature_columns
    }, os.path.join("..", "models", "comments_predictor.pkl"))
    
    joblib.dump({
        "model": shares_model,
        "features": feature_columns
    }, os.path.join("..", "models", "shares_predictor.pkl"))
    
    print("🎉 All models trained and saved successfully!")
    print(f"📊 Training Summary:")
    print(f"   - Total samples processed: {len(df)}")
    print(f"   - Features used: {len(feature_columns)}")
    print(f"   - Likes MSE: {mse_likes:.2f}")
    print(f"   - Comments MSE: {mse_comments:.2f}")
    print(f"   - Shares MSE: {mse_shares:.2f}")

if __name__ == "__main__":
    train_and_save_model() 