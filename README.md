# 🛡️ Insurance Intelligence Platform

An end-to-end **AI-powered Insurance Premium Prediction Platform** built with **FastAPI**, **PostgreSQL**, **Docker**, and **Machine Learning**.

This project predicts insurance premiums using ML models while providing a secure, production-ready backend with JWT authentication, email verification, refresh tokens, and modern REST APIs.

---

## 🚀 Features

### 🔐 Authentication

- User Registration
- JWT Authentication
- Refresh Token Authentication
- Secure Logout
- Change Password
- Email Verification
- Forgot Password *(Coming Soon)*
- Reset Password *(Coming Soon)*

---

### 🤖 AI Prediction

- Predict Insurance Premium
- ML Model Integration
- Input Validation
- Prediction APIs

---

### 👤 User Management

- Secure Authentication
- Email Verification
- Role-based User System
- User Profile

---

### 🗄️ Database

- PostgreSQL
- SQLAlchemy ORM
- Alembic Migrations
- Foreign Key Relationships

---

### 🛡️ Security

- Password Hashing (bcrypt)
- SHA-256 Token Hashing
- JWT Access Tokens
- Refresh Tokens
- Secure Email Verification
- One-Time Verification Tokens
- Token Expiration

---

### 🐳 DevOps

- Docker
- Docker Compose
- Environment Variables
- Production Ready Structure

---

## 🏗️ Tech Stack

| Category | Technology |
|----------|------------|
| Backend | FastAPI |
| Language | Python |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Password Hashing | bcrypt |
| Token Hashing | SHA-256 |
| ML | Scikit-learn |
| Validation | Pydantic |
| Containerization | Docker |
| API Docs | Swagger UI |

---

# 📂 Project Structure

```text
app/
│
├── auth/
├── core/
├── db/
├── models/
├── routers/
├── schemas/
├── services/
├── scheduler/
├── utils/
└── main.py
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/insurance-intelligence-platform.git

cd insurance-intelligence-platform
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create

```text
.env
```

Example

```env
DATABASE_URL=

SECRET_KEY=

ALGORITHM=

ACCESS_TOKEN_EXPIRE_MINUTES=

REFRESH_TOKEN_EXPIRE_MINUTES=

EMAIL_USER=

EMAIL_PASSWORD=

EMAIL_FROM=

EMAIL_HOST=

EMAIL_PORT=
```

---

## Run Docker

```bash
docker compose up --build
```

---

## Run FastAPI

```bash
uvicorn app.main:app --reload
```

---

# 📖 API Documentation

Swagger

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# 🔐 Authentication Flow

```text
Signup
      │
      ▼
Email Verification
      │
      ▼
Login
      │
      ▼
Access Token
      │
      ▼
Refresh Token
      │
      ▼
Protected APIs
```

---

# 🤖 Prediction Flow

```text
User Input
      │
      ▼
Validation
      │
      ▼
ML Model
      │
      ▼
Premium Prediction
      │
      ▼
Database
```

---

# 🚧 Upcoming Features

- Forgot Password
- Reset Password
- Prediction History
- User Dashboard
- Prediction Analytics
- Admin Dashboard
- PDF Reports
- Docker Deployment
- CI/CD
- Unit Testing
- Redis
- Background Tasks

---

# 📈 Future Improvements

- Explainable AI (Feature Importance)
- Recommendation Engine
- Insurance Risk Analysis
- AI Chatbot
- Role Based Access Control
- Rate Limiting
- Monitoring
- Cloud Deployment

---

# 🤝 Contributing

Contributions are welcome!

Feel free to fork the repository and submit a Pull Request.

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Ronit Jagdale**

Backend Developer | Machine Learning Enthusiast

- GitHub: https://github.com/yourusername
- LinkedIn: https://linkedin.com/in/yourprofile

---

⭐ If you found this project useful, don't forget to star the repository.