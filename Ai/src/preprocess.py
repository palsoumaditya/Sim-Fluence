import pandas as pd
from sklearn.model_selection import train_test_split

def load_and_preprocess_data(csv_path: str):
    # Load dataset
    df = pd.read_csv(csv_path)

    # Convert boolean to int
    df['containsImage'] = df['containsImage'].astype(int)
    df['shouldImprove'] = df['shouldImprove'].astype(int)

    # One-hot encode categorical features
    df = pd.get_dummies(df, columns=[
        'dayOfWeek', 'postTimeOfDay', 'topCommentSentiment'
    ], drop_first=True)

    # Define feature and label columns
    feature_columns = df.drop([
        'receivedLikes', 'receivedComments', 'receivedShares',
        'suggestions', 'postText', 'hashtags'
    ], axis=1).columns.tolist()

    X = df[feature_columns]
    y_likes = df['receivedLikes']
    y_comments = df['receivedComments']

    # Split into train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_likes, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test, feature_columns
