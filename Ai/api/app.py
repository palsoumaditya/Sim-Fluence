from sentiment_analyzer import analyze_sentiment
from caption_generator import generate_caption
from predict import predict_likes
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import logging
from datetime import datetime

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))


# LangChain integration (optional - graceful fallback if not available)
try:
    from langchain_integration import GeminiXGBoostOptimizer, SimFluenceLangChainAgent
    LANGCHAIN_AVAILABLE = True
    logger.info("LangChain integration loaded successfully")
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    logger.warning(f"LangChain integration not available: {str(e)}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "sim-fluence-ai-api",
        "version": "1.0.0"
    })


@app.route('/predict/engagement', methods=['POST'])
def predict_engagement():
    """
    Predict likes and comments for a given post

    Expected input:
    {
        "length": 35,
        "containsImage": 1,
        "userFollowers": 1200,
        "userKarma": 4500,
        "accountAgeDays": 700,
        "avgEngagementRate": 0.06,
        "avgLikes": 20,
        "avgComments": 5,
        "dayOfWeek": "Friday",
        "postTimeOfDay": "Evening",
        "topCommentSentiment": "Positive"
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Transform categorical features to one-hot encoding
        transformed_input = transform_input_features(data)

        # Predict engagement
        predicted_likes = predict_likes(transformed_input)

        # Estimate comments based on likes (you can train a separate model for this)
        predicted_comments = max(
            0, int(predicted_likes * 0.1 + (predicted_likes * 0.02)))

        logger.info(
            f"Prediction successful: {predicted_likes:.1f} likes, {predicted_comments} comments")

        return jsonify({
            "predicted_likes": round(predicted_likes, 1),
            "predicted_comments": predicted_comments,
            "engagement_score": round((predicted_likes + predicted_comments * 2) / 10, 2),
            "status": "success"
        })

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


@app.route('/generate/caption', methods=['POST'])
def generate_post_caption():
    """
    Generate AI-powered captions for social media posts

    Expected input:
    {
        "prompt": "A sunset photo with mountains",
        "platform": "reddit",
        "tone": "casual",
        "length": "medium",
        "include_hashtags": true,
        "target_audience": "general"
    }
    """
    try:
        data = request.get_json()

        if not data or 'prompt' not in data:
            return jsonify({"error": "Prompt is required"}), 400

        # Generate caption using AI model
        caption_result = generate_caption(
            prompt=data['prompt'],
            platform=data.get('platform', 'reddit'),
            tone=data.get('tone', 'casual'),
            length=data.get('length', 'medium'),
            include_hashtags=data.get('include_hashtags', False),
            target_audience=data.get('target_audience', 'general')
        )

        logger.info(
            f"Caption generated successfully for prompt: {data['prompt'][:50]}...")

        return jsonify({
            "caption": caption_result['caption'],
            "hashtags": caption_result.get('hashtags', []),
            "confidence": caption_result.get('confidence', 0.8),
            "suggestions": caption_result.get('suggestions', []),
            "status": "success"
        })

    except Exception as e:
        logger.error(f"Caption generation error: {str(e)}")
        return jsonify({"error": f"Caption generation failed: {str(e)}"}), 500


@app.route('/analyze/sentiment', methods=['POST'])
def analyze_text_sentiment():
    """
    Analyze sentiment of text content

    Expected input:
    {
        "text": "This is amazing content!"
    }
    """
    try:
        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({"error": "Text is required"}), 400

        # Analyze sentiment
        sentiment_result = analyze_sentiment(data['text'])

        return jsonify({
            "sentiment": sentiment_result['sentiment'],
            "confidence": sentiment_result['confidence'],
            "scores": sentiment_result['scores'],
            "status": "success"
        })

    except Exception as e:
        logger.error(f"Sentiment analysis error: {str(e)}")
        return jsonify({"error": f"Sentiment analysis failed: {str(e)}"}), 500


@app.route('/optimize/post', methods=['POST'])
def optimize_post():
    """
    Complete post optimization combining all AI services

    Expected input:
    {
        "content": "My vacation photo",
        "user_data": {
            "userFollowers": 1200,
            "userKarma": 4500,
            "accountAgeDays": 700,
            "avgEngagementRate": 0.06
        },
        "post_settings": {
            "containsImage": true,
            "dayOfWeek": "Friday",
            "postTimeOfDay": "Evening"
        },
        "optimization_goals": ["engagement", "caption", "sentiment"]
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        content = data.get('content', '')
        user_data = data.get('user_data', {})
        post_settings = data.get('post_settings', {})
        goals = data.get('optimization_goals', ['engagement'])

        results = {}

        # 1. Generate optimized caption if requested
        if 'caption' in goals and content:
            caption_result = generate_caption(
                prompt=content,
                platform='reddit',
                tone='engaging'
            )
            results['optimized_caption'] = caption_result

        # 2. Analyze sentiment if requested
        if 'sentiment' in goals and content:
            sentiment_result = analyze_sentiment(content)
            results['sentiment_analysis'] = sentiment_result

        # 3. Predict engagement if requested
        if 'engagement' in goals:
            # Prepare input for engagement prediction
            engagement_input = {
                "length": len(content),
                "containsImage": 1 if post_settings.get('containsImage') else 0,
                "userFollowers": user_data.get('userFollowers', 0),
                "userKarma": user_data.get('userKarma', 0),
                "accountAgeDays": user_data.get('accountAgeDays', 365),
                "avgEngagementRate": user_data.get('avgEngagementRate', 0.05),
                "avgLikes": user_data.get('avgLikes', 10),
                "avgComments": user_data.get('avgComments', 2),
                "dayOfWeek": post_settings.get('dayOfWeek', 'Friday'),
                "postTimeOfDay": post_settings.get('postTimeOfDay', 'Evening'),
                "topCommentSentiment": "Positive"
            }

            transformed_input = transform_input_features(engagement_input)
            predicted_likes = predict_likes(transformed_input)
            predicted_comments = max(0, int(predicted_likes * 0.1))

            results['engagement_prediction'] = {
                "predicted_likes": round(predicted_likes, 1),
                "predicted_comments": predicted_comments,
                "engagement_score": round((predicted_likes + predicted_comments * 2) / 10, 2)
            }

        # 4. Generate optimization recommendations
        results['recommendations'] = generate_optimization_recommendations(
            results)

        return jsonify({
            "results": results,
            "status": "success"
        })

    except Exception as e:
        logger.error(f"Post optimization error: {str(e)}")
        return jsonify({"error": f"Post optimization failed: {str(e)}"}), 500


def transform_input_features(data):
    """Transform user-friendly input to model-ready features"""
    transformed = {
        "length": data.get("length", 0),
        "containsImage": data.get("containsImage", 0),
        "userFollowers": data.get("userFollowers", 0),
        "userKarma": data.get("userKarma", 0),
        "accountAgeDays": data.get("accountAgeDays", 365),
        "avgEngagementRate": data.get("avgEngagementRate", 0.05),
        "avgLikes": data.get("avgLikes", 10),
        "avgComments": data.get("avgComments", 2),
        "shouldImprove": 0,
    }

    # One-hot encode day of week
    days = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]
    day = data.get("dayOfWeek", "Friday")
    for d in days[:-1]:  # Drop Sunday as reference
        transformed[f"dayOfWeek_{d}"] = 1 if day == d else 0

    # One-hot encode time of day
    times = ["Morning", "Afternoon", "Evening", "Night"]
    time = data.get("postTimeOfDay", "Evening")
    for t in times[:-1]:  # Drop Night as reference
        transformed[f"postTimeOfDay_{t}"] = 1 if time == t else 0

    # One-hot encode sentiment
    sentiments = ["Negative", "Neutral", "Positive"]
    sentiment = data.get("topCommentSentiment", "Positive")
    for s in sentiments[1:]:  # Drop Negative as reference
        transformed[f"topCommentSentiment_{s}"] = 1 if sentiment == s else 0

    return transformed


def generate_optimization_recommendations(results):
    """Generate actionable recommendations based on AI analysis"""
    recommendations = []

    if 'engagement_prediction' in results:
        engagement = results['engagement_prediction']
        if engagement['engagement_score'] < 3:
            recommendations.append(
                "Consider posting at peak hours (evening) for better engagement")
            recommendations.append("Add an image to increase visual appeal")

        if engagement['predicted_likes'] < 50:
            recommendations.append(
                "Try using trending hashtags relevant to your content")
            recommendations.append(
                "Engage with your audience in comments to boost interaction")

    if 'sentiment_analysis' in results:
        sentiment = results['sentiment_analysis']
        if sentiment['sentiment'] == 'negative':
            recommendations.append(
                "Consider rephrasing content with more positive language")
        elif sentiment['sentiment'] == 'neutral':
            recommendations.append(
                "Add more emotional words to create stronger engagement")

    if 'optimized_caption' in results:
        recommendations.append(
            "Use the AI-generated caption for better performance")

    return recommendations

# LangChain + Gemini Integration Endpoints


@app.route('/ai/gemini/optimize', methods=['POST'])
def gemini_optimize_content():
    """
    Advanced content optimization using Gemini + XGBoost

    Expected input:
    {
        "content": "Your post content here",
        "user_profile": {
            "karma": 4500,
            "followers": 1200,
            "account_age_days": 700
        },
        "optimization_goals": ["engagement", "authenticity", "discussion"]
    }
    """
    if not LANGCHAIN_AVAILABLE:
        return jsonify({
            "error": "LangChain integration not available. Please install required packages.",
            "fallback_available": True,
            "status": "error"
        }), 503

    try:
        data = request.get_json()

        if not data or 'content' not in data:
            return jsonify({"error": "Content is required"}), 400

        content = data['content']
        user_profile = data.get('user_profile', {})
        optimization_goals = data.get('optimization_goals', ['engagement'])

        # Initialize Gemini optimizer
        google_api_key = os.getenv('GOOGLE_API_KEY')
        if not google_api_key:
            return jsonify({
                "error": "Google API key not configured",
                "status": "error"
            }), 500

        optimizer = GeminiXGBoostOptimizer(google_api_key)

        # Perform optimization
        result = optimizer.quick_optimize(
            content=content,
            user_karma=user_profile.get('karma', 1000),
            user_followers=user_profile.get('followers', 100)
        )

        logger.info(
            f"Gemini optimization completed for content: {content[:50]}...")

        return jsonify({
            "optimization_result": result,
            "ai_engine": "gemini_plus_xgboost",
            "status": "success"
        })

    except Exception as e:
        logger.error(f"Gemini optimization error: {str(e)}")
        return jsonify({
            "error": f"Gemini optimization failed: {str(e)}",
            "status": "error"
        }), 500


@app.route('/ai/gemini/caption', methods=['POST'])
def gemini_generate_caption():
    """
    Advanced caption generation using Gemini with context

    Expected input:
    {
        "prompt": "Description of content",
        "platform": "reddit",
        "engagement_target": "high",
        "context": {
            "user_data": {...},
            "additional_context": "..."
        }
    }
    """
    if not LANGCHAIN_AVAILABLE:
        return jsonify({
            "error": "LangChain integration not available",
            "status": "error"
        }), 503

    try:
        data = request.get_json()

        if not data or 'prompt' not in data:
            return jsonify({"error": "Prompt is required"}), 400

        prompt = data['prompt']
        platform = data.get('platform', 'reddit')
        engagement_target = data.get('engagement_target', 'medium')
        context = data.get('context', {})

        # Initialize Gemini optimizer
        google_api_key = os.getenv('GOOGLE_API_KEY')
        if not google_api_key:
            return jsonify({
                "error": "Google API key not configured",
                "status": "error"
            }), 500

        optimizer = GeminiXGBoostOptimizer(google_api_key)

        # Generate caption with context
        result = optimizer.smart_caption_generation(
            prompt=prompt,
            engagement_target=engagement_target
        )

        logger.info(f"Gemini caption generated for: {prompt[:50]}...")

        return jsonify({
            "caption_result": result,
            "ai_engine": "gemini_contextual",
            "platform": platform,
            "status": "success"
        })

    except Exception as e:
        logger.error(f"Gemini caption generation error: {str(e)}")
        return jsonify({
            "error": f"Gemini caption generation failed: {str(e)}",
            "status": "error"
        }), 500


@app.route('/ai/comprehensive', methods=['POST'])
def comprehensive_ai_analysis():
    """
    Complete AI analysis using LangChain agent with multiple tools

    Expected input:
    {
        "content": "Your content here",
        "user_data": {
            "karma": 4500,
            "followers": 1200,
            "account_age_days": 700
        },
        "analysis_depth": "full" // or "quick"
    }
    """
    if not LANGCHAIN_AVAILABLE:
        return jsonify({
            "error": "LangChain integration not available",
            "status": "error"
        }), 503

    try:
        data = request.get_json()

        if not data or 'content' not in data:
            return jsonify({"error": "Content is required"}), 400

        content = data['content']
        user_data = data.get('user_data', {})
        analysis_depth = data.get('analysis_depth', 'full')

        # Initialize LangChain agent
        google_api_key = os.getenv('GOOGLE_API_KEY')
        if not google_api_key:
            return jsonify({
                "error": "Google API key not configured",
                "status": "error"
            }), 500

        agent = SimFluenceLangChainAgent(google_api_key)

        if analysis_depth == 'quick':
            # Quick optimization
            optimizer = GeminiXGBoostOptimizer(google_api_key)
            result = optimizer.predict_and_optimize(content, user_data)
        else:
            # Full comprehensive analysis
            result = agent.comprehensive_analysis(content, user_data)

        logger.info(
            f"Comprehensive AI analysis completed for: {content[:50]}...")

        return jsonify({
            "analysis_result": result,
            "analysis_depth": analysis_depth,
            "ai_engine": "langchain_agent_gemini_xgboost",
            "status": "success"
        })

    except Exception as e:
        logger.error(f"Comprehensive AI analysis error: {str(e)}")
        return jsonify({
            "error": f"Comprehensive analysis failed: {str(e)}",
            "status": "error"
        }), 500


@app.route('/ai/models/status', methods=['GET'])
def ai_models_status():
    """Get status of all AI models and integrations"""
    try:
        status = {
            "xgboost_model": {
                "available": True,
                "model_path": "models/likes_predictor.pkl",
                "status": "ready"
            },
            "langchain_integration": {
                "available": LANGCHAIN_AVAILABLE,
                "status": "ready" if LANGCHAIN_AVAILABLE else "unavailable"
            },
            "gemini_api": {
                "configured": bool(os.getenv('GOOGLE_API_KEY')),
                "status": "ready" if os.getenv('GOOGLE_API_KEY') else "not_configured"
            }
        }

        return jsonify({
            "models_status": status,
            "overall_status": "ready" if all(
                model["status"] in ["ready", "not_configured"]
                for model in status.values()
            ) else "partial",
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({
            "error": f"Status check failed: {str(e)}",
            "status": "error"
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
