# ❤️ CardioPredict – Heart Disease Prediction System

A full-stack machine learning web application that predicts the risk of heart disease based on user medical parameters.

---

## 🚀 Features

- 🔐 User Authentication (JWT-based login/register)
- 🧠 Machine Learning Model (Random Forest)
- 📊 Risk Prediction (Low / Medium / High)
- 📈 Model Performance Metrics (Accuracy, Precision, Recall, F1 Score)
- 📉 Confusion Matrix Visualization
- 📊 Pie Chart for Risk Distribution
- 🧾 Prediction History with Pagination
- 🔍 Explainable AI (Top factors influencing prediction)
- 💾 Database storage (SQLite)

---

## 🧠 Machine Learning

- Model: Random Forest Classifier  
- Accuracy: ~83.6%  
- Features: 13 medical parameters  
- Output: Risk classification + probability  

---

## 🛠️ Tech Stack

### Backend
- Flask
- SQLAlchemy
- Flask-JWT-Extended

### Frontend
- HTML, CSS, JavaScript
- Chart.js

### ML
- Scikit-learn
- Pandas
- NumPy

---

## 📂 Project Structure

CardioPredict/
│
├── backend/
│ ├── routes/
│ ├── services/
│ ├── ml/
│ ├── models.py
│ ├── app.py
│
├── frontend/
│ ├── index.html
│ ├── login.html
│ ├── predict.html
│ ├── history.html
│
├── ml_training/
│ ├── train_model.py
│
└── README.md
