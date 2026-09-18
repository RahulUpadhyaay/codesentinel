# CodeSentinel AI 🛡️

**CodeSentinel AI** is an intelligent, automated application security auditor and code analysis platform powered by FastAPI, React, and Google Gemini AI. It inspects source code for OWASP Top 10 vulnerabilities, security flaws, hardcoded secrets, and performance anti-patterns, providing real-time security scores, line-by-line findings, and actionable remediation suggestions.

---

## ✨ Features

- 🛡️ **AI-Powered Code Audit**: Leverages Google Gemini 3.6 Flash with structured JSON output for precision scanning.
- 📊 **Security Score & Severity Breakdown**: Computes safety scores (0–100) and categorizes findings as `HIGH`, `MEDIUM`, or `LOW` risk.
- 💡 **Actionable Fix Suggestions**: Provides exact line numbers and code remediation recommendations for each vulnerability found.
- 🔐 **User Authentication & Persistence**: Built-in user signup, login, JWT token authentication, and scan history tracking.
- 🎨 **Modern Sleek Dashboard**: React frontend powered by Vite and Tailwind CSS.

---

## 🛠️ Tech Stack

### **Backend**
- **Framework**: Python 3.10+ / [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: SQLite with [SQLModel](https://sqlmodel.tiangolo.com/) (SQLAlchemy + Pydantic)
- **AI Engine**: [Google GenAI SDK](https://github.com/google/generative-ai-python) (`gemini-3.6-flash`)
- **Security**: Passlib (Bcrypt), PyJWT, CORS Middleware

### **Frontend**
- **Framework**: React 18 + [Vite](https://vitejs.dev/)
- **Styling**: Tailwind CSS
- **Icons & UI**: Lucide Icons / Heroicons

---

## 📂 Project Structure

```text
codesentinel/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI router endpoints (auth, audit)
│   │   ├── core/         # Security & dependency injection
│   │   ├── models/       # SQLModel database schemas (User, Scan)
│   │   ├── schemas/      # Pydantic data validation models
│   │   ├── services/     # Gemini AI scanner service
│   │   ├── config.py     # App environment configuration
│   │   ├── database.py   # DB connection & session creation
│   │   └── main.py       # FastAPI application entry point
│   ├── requirements.txt  # Python backend dependencies
│   └── test_security.py # Security test runner
├── frontend/
│   ├── src/
│   │   ├── components/   # Auth and Auditor UI components
│   │   ├── App.jsx       # Root React component
│   │   └── api.js        # Axios/Fetch API client
│   ├── package.json      # Frontend npm dependencies
│   └── vite.config.js    # Vite configuration
└── .gitignore            # Root git ignore rules
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- Gemini API Key (optional for live AI scanning, mock engine included as fallback)

---

### 1. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Create a .env file inside backend/ with:
# GEMINI_API_KEY=your_gemini_api_key_here
# SECRET_KEY=your_jwt_secret_key

# Start backend server
uvicorn app.main:app --reload --port 8000
```
Backend API will be live at `http://localhost:8000` (Docs available at `http://localhost:8000/docs`).

---

### 2. Frontend Setup

```bash
cd frontend

# Install node packages
npm install

# Start Vite development server
npm run dev
```
Frontend will be live at `http://localhost:5173`.

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).
