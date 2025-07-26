import os
import joblib
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from preprocess import load_and_preprocess_data

# Constants
DATA_PATH = os.path.join("data", "simfluence_reddit_training.csv")
MODEL_SAVE_PATH = os.path.join("models", "likes_predictor.pkl")

def train_and_save_model():
    print("📦 Loading and preprocessing data...")
    X_train, X_test, y_train, y_test, feature_columns = load_and_preprocess_data(DATA_PATH)

    print("⚙️ Training XGBoost regression model...")
    model = XGBRegressor()
    model.fit(X_train, y_train)

    print("🧪 Evaluating model...")
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"✅ Model trained! MSE: {mse:.2f}")

    print("💾 Saving model to:", MODEL_SAVE_PATH)
    joblib.dump({
        "model": model,
        "features": feature_columns
    }, MODEL_SAVE_PATH)

if __name__ == "__main__":
    train_and_save_model()
