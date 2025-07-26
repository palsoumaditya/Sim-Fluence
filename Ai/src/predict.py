import joblib
import pandas as pd
import os

MODEL_PATH = os.path.join("models", "likes_predictor.pkl")

def load_model():
    print("📦 Loading model...")
    model_data = joblib.load(MODEL_PATH)
    return model_data["model"], model_data["features"]

def predict_likes(new_input: dict):
    model, feature_columns = load_model()

    # Create dataframe with expected feature columns
    input_df = pd.DataFrame([new_input])

    # Ensure all feature columns exist
    for col in feature_columns:
        if col not in input_df.columns:
            input_df[col] = 0  # fill missing with 0

    input_df = input_df[feature_columns]  # reorder to match training

    # Predict
    prediction = model.predict(input_df)
    return prediction[0]

if __name__ == "__main__":
    # 🧪 Example input (must match feature format used in training)
    example_input = {
        "length": 35,
        "containsImage": 1,
        "userFollowers": 1200,
        "userFollowing": 300,
        "userKarma": 4500,
        "accountAgeDays": 700,
        "avgEngagementRate": 0.06,
        "avgLikes": 20,
        "avgComments": 5,
        "shouldImprove": 0,
        "dayOfWeek_Friday": 1,
        "postTimeOfDay_Evening": 1,
        "topCommentSentiment_Positive": 1
        # All other one-hot columns will be set to 0 automatically
    }

    predicted_likes = predict_likes(example_input)
    print(f"🔮 Predicted Likes: {predicted_likes:.1f}")
