import pandas as pd
from sklearn.model_selection import train_test_split

def load_and_preprocess_data(csv_path: str = None):
    """Load and preprocess the dataset with proper handling of missing values"""
    # Use ultimate fixed CSV file by default
    if csv_path is None:
        csv_path = "../data/simfluence_reddit_training_ultimate.csv"
    
    # Load dataset
    df = pd.read_csv(csv_path)
    print(f"Original dataset shape: {df.shape}")

    # Convert string boolean to int
    df['containsImage'] = df['containsImage'].map({'True': 1, 'False': 0})
    df['shouldImprove'] = df['shouldImprove'].map({'True': 1, 'False': 0})

    # Convert numeric columns to proper types and handle missing values
    numeric_columns = ['length', 'userFollowers', 'userFollowing', 'userKarma', 
                      'accountAgeDays', 'avgEngagementRate', 'avgLikes', 'avgComments',
                      'receivedLikes', 'receivedComments', 'receivedShares']
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            if df[col].isnull().sum() > 0:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                print(f"Filled {df[col].isnull().sum()} missing values in {col} with median: {median_val}")

    # Handle categorical columns
    categorical_columns = ['postTimeOfDay', 'dayOfWeek', 'topCommentSentiment']
    for col in categorical_columns:
        if col in df.columns and df[col].isnull().sum() > 0:
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)
            print(f"Filled {df[col].isnull().sum()} missing values in {col} with mode: {mode_val}")

    # One-hot encode categorical features
    df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)

    # Define feature columns
    feature_columns = df.drop([
        'receivedLikes', 'receivedComments', 'receivedShares',
        'suggestions', 'postText', 'hashtags'
    ], axis=1).columns.tolist()

    print(f"Final dataset shape: {df.shape}")
    print(f"Feature columns: {len(feature_columns)}")

    return df, feature_columns

def split_data(df, feature_columns, target_column, test_size=0.2, random_state=42):
    """Split data into training and testing sets"""
    X = df[feature_columns]
    y = df[target_column]
    
    return train_test_split(X, y, test_size=test_size, random_state=random_state)
