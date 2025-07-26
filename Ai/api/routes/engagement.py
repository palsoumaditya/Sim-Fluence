from flask import Blueprint, request, jsonify
from predict import predict_likes, predict_engagement_category
from logger import logger
from utils import transform_input_features

engagement_bp = Blueprint('engagement', __name__)

@engagement_bp.route('/predict/engagement', methods=['POST'])
def predict_engagement():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        transformed_input = transform_input_features(data)
        predicted_likes = predict_likes(transformed_input)
        predicted_comments = max(0, int(predicted_likes * 0.1 + (predicted_likes * 0.02)))
        engagement_category = predict_engagement_category(predicted_likes)
        logger.info(f"Prediction successful: {predicted_likes:.1f} likes, {predicted_comments} comments")
        return jsonify({
            "predicted_likes": round(predicted_likes, 1),
            "predicted_comments": predicted_comments,
            "engagement_score": round((predicted_likes + predicted_comments * 2) / 10, 2),
            "engagement_category": engagement_category,
            "status": "success"
        })
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500 