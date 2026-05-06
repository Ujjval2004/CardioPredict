import os
import pickle
import json
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Database
from models import db, User, Prediction

# Blueprints
from auth.auth_routes import auth_bp
from routes.predict_routes import prediction_bp
from routes.history_routes import history_bp
from routes.admin import admin_bp

# Logger
from utils.logger import setup_logger

# ---------------- LOAD ENV ---------------- #
load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # ---------------- CONFIG ---------------- #
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    db_path = os.path.join(BASE_DIR, "instance", "cardiopredict.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 4500)
    )

    db.init_app(app)
    JWTManager(app)

    # ---------------- DB INIT ---------------- #
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")

    # ---------------- LOGGER ---------------- #
    setup_logger()
    print("Starting CardioPredict backend...")

    # ---------------- LOAD MODEL ---------------- #
    model_path = os.path.join(BASE_DIR, "ml", "model.pkl")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f" Model not found at {model_path}")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    app.config["MODEL"] = model
    print(" Model loaded successfully")

    # ---------------- ROUTES ---------------- #

    @app.route("/")
    def home():
        return {"message": "CardioPredict API Running Successfully"}

    @app.route("/stats", methods=["GET"])
    def stats():
        return jsonify({
            "users": User.query.count(),
            "predictions": Prediction.query.count()
        })

    
    @app.route("/model-metrics", methods=["GET"])
    def model_metrics():
        metrics_path = os.path.join(BASE_DIR, "ml", "metrics.json")

        if not os.path.exists(metrics_path):
            return jsonify({"error": "Metrics not found. Train model first."}), 404

        with open(metrics_path, "r") as f:
            data = json.load(f)

        return jsonify({
            "model": data["best_model"],
            "accuracy": data["best_metrics"]["accuracy"],
            "precision": data["best_metrics"]["precision"],
            "recall": data["best_metrics"]["recall"],
            "f1_score": data["best_metrics"]["f1"],
            "confusion_matrix": data["best_metrics"]["confusion_matrix"]
        })

    
    @app.route("/model-comparison", methods=["GET"])
    def model_comparison():
        metrics_path = os.path.join(BASE_DIR, "ml", "metrics.json")

        if not os.path.exists(metrics_path):
            return jsonify({"error": "Metrics not found. Train model first."}), 404

        with open(metrics_path, "r") as f:
            data = json.load(f)

        return jsonify(data)

    # ---------------- BLUEPRINTS ---------------- #
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(prediction_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(admin_bp)

    return app


# ---------------- RUN ---------------- #
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)