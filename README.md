# 🚀 Insurance Loan Predictor API

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Machine Learning](https://img.shields.io/badge/ML-ScikitLearn-orange)
![Status](https://img.shields.io/badge/Status-Production--Ready-success)

A Machine Learning-powered Insurance Loan Prediction System built using FastAPI, Scikit-Learn, and Docker. It provides real-time predictions through a scalable REST API with a clean modular backend architecture.

---

## 🧠 Problem Statement

Financial systems need an automated way to predict insurance loan outcomes based on user inputs while ensuring scalability, validation, and production readiness.

---

## 🏗️ System Architecture

User Input → FastAPI Backend → Pydantic Validation → Service Layer → ML Model (model.pkl) → Database Storage → Response Output

---

## ⚙️ Features

- Machine Learning-based prediction engine  
- FastAPI REST API backend  
- Modular architecture (core, services, schemas, models)  
- Pydantic validation layer  
- Dockerized deployment  
- Docker Compose support  
- CI/CD pipeline integration  
- Separate ML training and inference pipeline  
- Frontend dashboard for predictions  

---

## 🧰 Tech Stack

Backend:
- Python
- FastAPI

Machine Learning:
- NumPy
- Pandas
- Scikit-Learn

Validation:
- Pydantic

DevOps:
- Docker
- Docker Compose
- GitHub Actions (CI/CD)

Frontend:
- Python-based UI (frontend.py)

---

## 📁 Project Structure
backend/
│── app/
│   ├── core/
│   ├── db/
│   ├── main.py
│   ├── ml/model_store/
│   ├── models/
│   ├── schemas/
│   └── services/
│
frontend/
ml-training/
ml_prediction/
images/
docker-compose.yml
requirements.txt

---

## 🔄 Workflow

User Input → API Request → Schema Validation → Business Logic → ML Model Prediction → Database Save → Response

---

## ⚙️ Local Setup

```bash
git clone https://github.com/ronitjagdale39/insurance_loan_predictor.git
cd insurance_loan_predictor

## Backend run

cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

## frontend run

cd frontend
pip install -r requirements.txt
python frontend.py

## 🐳 Docker Setup
docker build -t insurance_backend -f backend/Dockerfile.backend .

Run:
docker run -p 8000:8000 insurance_backend

Compose:
docker compose up --build
docker compose down

## 🧪 ML Training
cd ml-training
python train.py

jupyter notebook insurance_predictor.ipynb

🚀 Future Improvements

* PostgreSQL database integration
* JWT authentication system
* Advanced ML models (XGBoost / LightGBM)
* Model monitoring & drift detection
* Cloud deployment (AWS / Azure)
* Prediction history dashboard
* Rate limiting & security improvements

⸻

📊 Impact

* Real-time predictions (<100ms response time)
* Reduced manual underwriting effort
* Scalable API architecture
* Production-ready ML system

⸻

👨‍💻 Author

Ronit Jagdale
B.Tech Information Technology
Pillai College of Engineering, Panvel

GitHub: https://github.com/ronitjagdale39
