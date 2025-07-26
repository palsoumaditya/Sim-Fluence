from flask import Blueprint, request, jsonify
from predict import predict_shares
from logger import logger
from utils import transform_input_features

shares_bp = Blueprint('shares', __name__)

@shares_bp.route('/predict/shares', methods=['POST'])
def predict_shares_endpoint():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        transformed_input = transform_input_features(data)
        predicted_shares = predict_shares(transformed_input)
        logger.info(f"Shares prediction successful: {predicted_shares:.1f} shares")
        return jsonify({
            "predicted_shares": round(predicted_shares, 1),
            "status": "success"
        })
    except Exception as e:
        logger.error(f"Shares prediction error: {str(e)}")
        return jsonify({"error": f"Shares prediction failed: {str(e)}"}), 500 