import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(CURRENT_DIR, "heart.csv")

df = pd.read_csv(data_path)

target_column = "target" if "target" in df.columns else df.columns[-1]

X = df.drop(target_column, axis=1)
y = df[target_column]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=6,
    min_samples_split=10,
    random_state=42
)

model.fit(X_train, y_train)

# ✅ Predictions
y_pred = model.predict(X_test)

# ✅ Metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("Confusion Matrix:\n", cm)

# ✅ SAVE MODEL
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
model_dir = os.path.join(PROJECT_ROOT, "backend", "ml")
os.makedirs(model_dir, exist_ok=True)

model_path = os.path.join(model_dir, "model.pkl")

with open(model_path, "wb") as file:
    pickle.dump(model, file)

print("Model saved:", model_path)