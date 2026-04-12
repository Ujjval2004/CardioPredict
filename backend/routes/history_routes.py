from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Prediction
import json
import math

history_bp = Blueprint("history", __name__)

@history_bp.route("/history", methods=["GET"])
@jwt_required()
def get_history():

    current_user_id = get_jwt_identity()

    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 5, type=int)

    query = Prediction.query.filter_by(
        user_id=current_user_id
    ).order_by(Prediction.created_at.desc())

    total_records = query.count()

    predictions = Prediction.query.paginate(page=page, per_page=limit)

    result = []

    for p in predictions:
        result.append({
            "id": p.id,
            "input_data": json.loads(p.input_data),
            "result": p.result,
            "probability": round(p.probability * 100, 2),
            "created_at": p.created_at.isoformat()
        })

    total_pages = math.ceil(total_records / limit)

    return jsonify({
        "page": page,
        "limit": limit,
        "total_records": total_records,
        "total_pages": total_pages,
        "data": result
    }), 200