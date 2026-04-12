import os
import pickle
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

    # ✅ Enable CORS
    CORS(app)

    # ---------------- BASE DIRECTORY ---------------- #
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # ---------------- SECRET KEYS ---------------- #
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    # ---------------- DATABASE ---------------- #
    db_path = os.path.join(BASE_DIR, "instance", "cardiopredict.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ---------------- JWT ---------------- #
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 4500)
    )

    db.init_app(app)
    JWTManager(app)

    # ---------------- CREATE TABLES ---------------- #
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")

    # ---------------- LOGGER ---------------- #
    setup_logger()
    print("Starting CardioPredict backend...")

    # ---------------- LOAD MODEL ---------------- #
    model_path = os.path.join(BASE_DIR, "ml", "model.pkl")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Model not found at {model_path}")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    app.config["MODEL"] = model
    print("✅ Model loaded successfully")

    # ---------------- ROUTES ---------------- #

    # ✅ HOME
    @app.route("/")
    def home():
        return {"message": "CardioPredict API Running Successfully"}

    # ✅ STATS
    @app.route("/stats", methods=["GET"])
    def stats():
        total_users = User.query.count()
        total_predictions = Prediction.query.count()

        return jsonify({
            "users": total_users,
            "predictions": total_predictions
        })

    # ✅ MODEL METRICS (🔥 NEW)
    @app.route("/model-metrics", methods=["GET"])
    def model_metrics():
        return jsonify({
            "model": "Random Forest",
            "accuracy": 0.836,
            "precision": 0.78,
            "recall": 0.97,
            "f1_score": 0.86,
            "confusion_matrix": [
                [19, 9],
                [1, 32]
            ]
        })

    # ---------------- BLUEPRINTS ---------------- #
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(prediction_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(admin_bp)

    return app


# ---------------- RUN ---------------- #
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)