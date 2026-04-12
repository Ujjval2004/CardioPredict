from flask import Blueprint, request, jsonify, current_app
import json
import pandas as pd

from models import db, Prediction
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.prediction_service import make_prediction

prediction_bp = Blueprint("prediction", __name__)


# ✅ SAFE EXPLANATION FUNCTION
def get_explanation(model, input_data):
    try:
        if not hasattr(model, "feature_importances_"):
            return ["Explanation not available"]

        importances = model.feature_importances_
        features = list(model.feature_names_in_)  # ✅ FIXED

        pairs = list(zip(features, importances))
        pairs.sort(key=lambda x: x[1], reverse=True)

        top_features = [f[0] for f in pairs[:3]]

        mapping = {
            "cp": "Chest Pain",
            "chol": "Cholesterol",
            "thalach": "Max Heart Rate",
            "trestbps": "Blood Pressure",
            "oldpeak": "ST Depression"
        }

        return [mapping.get(f, f) for f in top_features]

    except Exception as e:
        print("Explanation error:", e)
        return ["Explanation not available"]

@prediction_bp.route("/predict", methods=["POST"])
@jwt_required()
def predict():

    model = current_app.config["MODEL"]
    user_id = get_jwt_identity()

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    required_fields = [
        "age", "sex", "cp", "trestbps", "chol", "fbs",
        "restecg", "thalach", "exang", "oldpeak",
        "slope", "ca", "thal"
    ]

    missing_fields = [f for f in required_fields if f not in data]

    if missing_fields:
        return jsonify({
            "error": "Features missing",
            "missing_fields": missing_fields
        }), 400

    try:
        input_df = pd.DataFrame([{
            "age": float(data["age"]),
            "sex": float(data["sex"]),
            "cp": float(data["cp"]),
            "trestbps": float(data["trestbps"]),
            "chol": float(data["chol"]),
            "fbs": float(data["fbs"]),
            "restecg": float(data["restecg"]),
            "thalach": float(data["thalach"]),
            "exang": float(data["exang"]),
            "oldpeak": float(data["oldpeak"]),
            "slope": float(data["slope"]),
            "ca": float(data["ca"]),
            "thal": float(data["thal"])
        }])

        # ✅ MODEL PREDICTION
        prediction, probability, risk = make_prediction(model, input_df)

        # ✅ SAVE TO DB
        new_prediction = Prediction(
            user_id=user_id,
            input_data=json.dumps(data),
            result=risk,
            probability=float(probability)
        )

        db.session.add(new_prediction)
        db.session.commit()

        # ✅ SAFE EXPLANATION
        explanation = get_explanation(model, data)

        return jsonify({
            "probability": float(probability),
            "risk": risk,
            "explanation": explanation
        })

    except Exception as e:
        print("Prediction error:", e)
        return jsonify({"error": "Prediction failed"}), 500