# ❤️ CardioPredict – Heart Disease Prediction System

A full-stack machine learning web application that predicts the risk of heart disease based on user medical parameters.

---

## 🚀 Features

-  User Authentication (JWT-based login/register)
- Compared Machine Learning Algorithims(Random Forest, Logistic Regression and Decision Tree)
- Choose Random Forest Model as it had the most Accuracy and most Recall.
-  Machine Learning Model (Random Forest)
-  Risk Prediction (Low / Medium / High)
-  Model Performance Metrics (Accuracy, Precision, Recall, F1 Score)
-  Confusion Matrix Visualization
-  Pie Chart for Risk Distribution
-  Prediction History with Pagination
-  Explainable AI (Top factors influencing prediction)
-  Database storage (SQLite)

---

##  Machine Learning

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

Screenshots:-
<img width="1895" height="874" alt="image" src="https://github.com/user-attachments/assets/f6b41efc-3f57-49d6-b88e-762bb6058547" />
Home page

<img width="1853" height="370" alt="image" src="https://github.com/user-attachments/assets/5ee0c989-d097-49e7-a406-7f779e87dd4e" />
Model Comparision Table

<img width="1913" height="865" alt="image" src="https://github.com/user-attachments/assets/2d5171e5-1094-43b5-be47-de77d4fd022f" />
Login page

<img width="1920" height="860" alt="image" src="https://github.com/user-attachments/assets/598a7829-ec3d-4271-9c13-825ad08a08ca" />
Register page

<img width="1915" height="860" alt="image" src="https://github.com/user-attachments/assets/db567d7f-5e9b-4cd5-95bb-9c7b205f87af" />
Predict Page

View predictions page
<img width="1897" height="863" alt="image" src="https://github.com/user-attachments/assets/6e45957a-bcce-46f3-82f1-f9c4222250c8" />




