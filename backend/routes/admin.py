from flask import Blueprint, jsonify
from models import db, Prediction
from auth.auth_utils import token_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/stats", methods=["GET"])
def stats(user):
    try:
        total = Prediction.query.count()

        high = Prediction.query.filter(Prediction.probability > 0.7).count()
        medium = Prediction.query.filter(
            Prediction.probability.between(0.4, 0.7)
        ).count()
        low = Prediction.query.filter(Prediction.probability <= 0.4).count()

        return jsonify({
            "total_predictions": total,
            "risk_distribution": {
                "high": high,
                "medium": medium,
                "low": low
            }
        })

    except Exception as e:
        return jsonify({"message": str(e)}), 500