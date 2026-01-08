# PerplexiPlay — Phase 1: Core Platform Foundation

PerplexiPlay is an AI experimentation platform designed for building, testing, and playgrounds for AI agents.

## 📁 Project Structure

```text
perplexiplay/
│
├── backend/
│   ├── main.py             # FastAPI entry point
│   ├── database.py         # SQLAlchemy engine & session
│   ├── models/             # Database models (SQLAlchemy)
│   │   └── user.py
│   ├── schemas/            # Pydantic schemas (Request/Response)
│   │   └── user.py
│   ├── auth/               # Auth logic & dependencies
│   │   ├── jwt.py
│   │   └── dependencies.py
│   ├── routes/             # API Endpoints
│   │   └── auth.py
│   └── core/               # Security & Hashing utilities
│       └── security.py
│
├── frontend/
│   └── app.py              # Streamlit Application
│
├── .env                    # Environment secrets
├── requirements.txt        # Dependencies
└── README.md               # Documentation
```

## 🚀 How to Run

### 1. Setup Environment
Ensure you have Python 3.10+ installed.

```bash
# Clone the repository (if applicable)
cd perplexiplay

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the Backend
```bash
# From the root perplexiplay directory
set PYTHONPATH=%PYTHONPATH%;.
python backend/main.py
```
The API will be available at `http://localhost:8000`. You can access the docs at `http://localhost:8000/docs`.

### 3. Start the Frontend
```bash
# In a new terminal
streamlit run frontend/app.py
```
The dashboard will be available at `http://localhost:8501`.

### 4. Firebase Configuration
PerplexiPlay supports Firebase for additional data storage (Firestore) and file storage (Cloud Storage).

1. Place your `firebase-service-account.json` in the `perplexiplay` root directory.
2. Update the `FIREBASE_STORAGE_BUCKET` in your `.env` file.
3. The backend will automatically initialize Firebase on startup.

## 🧠 Design Choices

- **FastAPI Dependency Injection**: Used for DB sessions and user authentication to keep routes clean and testable.
- **JWT (OAuth2 Password Flow)**: Secure, stateless authentication matching modern standards.
- **Separation of Concerns**: Decoupled models from schemas and routes to allow the codebase to grow in Phase 2.
- **SQLite (SQLAlchemy)**: Used for rapid development in Phase 1; easily interchangeable with production databases.

## 🧪 API Examples

### Register User
**POST** `/auth/register`
```json
{
  "username": "testuser",
  "password": "securepassword123"
}
```

### Login
**POST** `/auth/login` (Form Data)
- `username`: `testuser`
- `password`: `securepassword123`

**Response:**
```json
{
  "access_token": "eyJhbG...",
  "token_type": "bearer"
}
```

### Get My Profile (Protected)
**GET** `/auth/me`
- **Header**: `Authorization: Bearer <TOKEN>`

**Response:**
```json
{
  "id": 1,
  "username": "testuser",
  "created_at": "2024-01-08T12:00:00"
}
```
