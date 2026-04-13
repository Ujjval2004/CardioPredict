import os
import pickle
import json
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix

# Models
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# ---------------- LOAD DATA ---------------- #
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(CURRENT_DIR, "heart.csv")

df = pd.read_csv(data_path)

target_column = "target" if "target" in df.columns else df.columns[-1]

X = df.drop(target_column, axis=1)
y = df[target_column]

# ---------------- SPLIT ---------------- #
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------- MODELS ---------------- #
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(max_depth=5),
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        max_depth=6,
        min_samples_split=10,
        random_state=42
    )
}

results = {}
best_model = None
best_accuracy = 0
best_model_name = ""

# ---------------- TRAIN + EVALUATE ---------------- #
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    results[name] = {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "confusion_matrix": cm.tolist()
    }

    print(f"\n{name}")
    print("Accuracy:", acc)
    print("Precision:", prec)
    print("Recall:", rec)
    print("F1 Score:", f1)
    print("Confusion Matrix:\n", cm)

    # Track best model
    if acc > best_accuracy:
        best_accuracy = acc
        best_model = model
        best_model_name = name
        best_cm = cm

print("\n✅ Best Model Selected:", best_model_name)

# ---------------- SAVE MODEL ---------------- #
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
model_dir = os.path.join(PROJECT_ROOT, "backend", "ml")
os.makedirs(model_dir, exist_ok=True)

model_path = os.path.join(model_dir, "model.pkl")

with open(model_path, "wb") as file:
    pickle.dump(best_model, file)

print("Model saved:", model_path)

# ---------------- SAVE METRICS ---------------- #
metrics_path = os.path.join(model_dir, "metrics.json")

with open(metrics_path, "w") as f:
    json.dump({
        "best_model": best_model_name,
        "best_metrics": results[best_model_name],
        "all_models": results
    }, f, indent=4)

print("Metrics saved:", metrics_path)