# CampusMind AI — Intelligent Multi-Role School Assistant

<div align="center">

**A full-stack AI-powered school management assistant supporting 11 languages with role-based access, real-time speech I/O, and advanced NLP capabilities.**

[Overview](#-overview) • [Features](#-features) • [Tech Stack](#-tech-stack) • [Installation](#-installation) • [API](#-api) • [Architecture](#-architecture) • [Development](#-development)

</div>

---

## 🎯 Overview

CampusMind AI is an intelligent conversational assistant designed for educational ecosystems. It provides a unified interface for students, parents, teachers, and administrators to interact with school systems using natural language. The system uses advanced NLP techniques (intent detection, entity extraction) and LangGraph-based agent orchestration to handle role-specific workflows with 11-language support.

**Key Highlights:**
- 🌐 Multilingual support (11 Indian languages)
- 🔐 Role-based access control with session management
- 🤖 LLM-powered agent orchestration using LangGraph
- 🎤 Real-time speech recognition and text-to-speech
- 🛡️ Security features including prompt injection prevention
- 📊 Role-specific data operations (attendance, analytics)
- ⚡ Full-stack with React frontend and FastAPI backend

---

## ✨ Features

### Core Capabilities
| Feature | Description |
|---------|-------------|
| **Role-Based Access** | Dedicated interfaces for Students, Parents, Teachers, and Principals |
| **Multi-Language** | English, Hindi, Tamil, Telugu, Marathi, Bengali, Gujarati, Punjabi, Kannada, Malayalam, Urdu |
| **NLP Processing** | Intent detection, entity extraction, context-aware responses |
| **Chat History** | Per-session conversation persistence |
| **Speech I/O** | Browser speech recognition + text-to-speech |
| **Security** | Prompt injection blocking, authorization, human escalation |

### Role-Specific Workflows
- **Students**: Academic support, grade inquiries, attendance tracking
- **Parents**: Child progress monitoring, attendance updates
- **Teachers**: Attendance marking, class management
- **Principals**: School analytics, global reports

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI, Uvicorn, Pydantic |
| **AI/Agents** | LangGraph, LangChain, Qwen 2.5 3B (Ollama) |
| **Frontend** | React 19, Vite, CSS |
| **Infrastructure** | Python 3.11+, Node.js 18+ |

---

## 📦 Installation

### Prerequisites
- **Python 3.11+**
- **Node.js 18+**
- **Ollama** with Qwen 2.5 3B model installed

### Quick Start

#### 1. Start Ollama (separate terminal)
```bash
ollama run qwen2.5:3b
```

#### 2. Backend Setup
```powershell
# From repository root
python -m pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```
- Server: http://localhost:8000
- API Docs: http://localhost:8000/docs

#### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
- Frontend: http://localhost:5173

### Environment Configuration
Copy `.env.example` to `.env` and customize:
```bash
cp .env.example .env
```

---

## 🚀 API Reference

### Authentication
**POST** `/api/login`
```json
{
  "email": "student@example.com",
  "role": "student"
}
```
Response includes `session_id` for subsequent requests

### Chat
**POST** `/api/chat`
```json
{
  "session_id": "uuid",
  "message": "What is my attendance?",
  "language": "English"
}
```

### Languages
**GET** `/api/languages` — Returns list of supported languages

**Full API documentation:** http://localhost:8000/docs (Swagger UI)

---

## 🔐 Demo Accounts

| Role | Email | Features |
|------|-------|----------|
| Student | `student@example.com` | View grades, attendance, schedules |
| Parent | `parent@example.com` | Monitor child's progress |
| Teacher | `teacher@example.com` | Mark attendance, manage classes |
| Principal | `principal@example.com` | School analytics & reports |

---

## 🏗️ Architecture

### Project Structure
```
CampusMind AI/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── main.py            # API routes & session management
│   │   ├── auth.py            # User authentication & validation
│   │   ├── graph.py           # LangGraph agent orchestration
│   │   ├── prompts.py         # System prompts & language templates
│   │   ├── tools.py           # Agent tools (attendance, grades, etc.)
│   │   ├── school_data.py     # Mock data & language mappings
│   │   ├── security.py        # Input validation & security
│   │   └── state.py           # Pydantic state schemas
│   └── requirements.txt
│
├── frontend/                   # React + Vite application
│   ├── src/
│   │   ├── App.jsx            # Main chat UI component
│   │   ├── main.jsx           # React entry point
│   │   └── index.css          # Global styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── README.md
├── .env.example               # Environment configuration template
└── requirements.txt
```

### Data Flow
```
User Input (Frontend)
    ↓
HTTP POST /api/chat
    ↓
Session Validation
    ↓
LangGraph State Machine:
  ├─ Intent Detection
  ├─ Authorization Check
  ├─ Entity Extraction
  ├─ Tool Router
  ├─ Tool Execution
  ├─ Response Generation
  └─ Language Translation
    ↓
Response to Frontend
    ↓
Display + Text-to-Speech
```

### LangGraph Agent Pipeline
1. **Intent Detection** — Identifies user intent (academic, attendance, etc.)
2. **Authorization** — Validates role-based permissions
3. **Entity Extraction** — Extracts relevant data from query
4. **Tool Routing** — Selects appropriate tool based on intent
5. **Tool Execution** — Runs selected tool (get_attendance, get_grades, etc.)
6. **Response Generation** — Creates natural language response
7. **Language Translation** — Translates to target language

---

## 🔒 Security Features

- **Prompt Injection Prevention** — Input sanitization and pattern detection
- **Role-Based Authorization** — Application-layer access control
- **Session Management** — UUID-based stateful sessions
- **Input Validation** — Length limits and security checks
- **Human Escalation** — Explicit confirmation for sensitive operations

---

## 🤝 Development

### Backend Development
```powershell
# Install dependencies
pip install -r backend/requirements.txt

# Start with auto-reload
uvicorn backend.app.main:app --reload

# Endpoints
# - Main: http://localhost:8000
# - Docs: http://localhost:8000/docs
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev      # Dev server with HMR (http://localhost:5173)
npm run build    # Production build
npm run preview  # Preview production
```

### Key Files to Understand
- **main.py** — REST endpoints and session management
- **graph.py** — AI agent state machine and node definitions
- **auth.py** — User authentication against mock database
- **App.jsx** — Frontend chat interface with speech I/O

---

## 📊 Supported Languages

English, Hindi, Tamil, Telugu, Marathi, Bengali, Gujarati, Punjabi, Kannada, Malayalam, Urdu

---

## 🚀 Production Deployment

### Using Gunicorn (Recommended)
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.app.main:app
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ ./backend
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0"]
```

---

## ⚙️ Configuration

Create `.env` file (template in `.env.example`):
```ini
DEBUG=True
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:3b
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1024
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Ollama connection error | Ensure `ollama run qwen2.5:3b` is running |
| CORS error | Frontend must be on allowed origins (localhost:5173) |
| Session not found | Session ID must match login response |
| Module not found | Run `pip install -r backend/requirements.txt` |
| npm dependencies | Run `cd frontend && npm install` |

---

## 📈 Performance & Scalability

**Current (Development):**
- In-memory sessions
- Local LLM serving
- Single-threaded development server

**Production Upgrades:**
- Redis for session storage
- Dedicated LLM inference server
- Multiple Gunicorn workers
- Database (PostgreSQL) for persistent data
- Load balancer (Nginx)
- Caching layer

---

## 📝 License

MIT License — Feel free to use this project for educational and commercial purposes.

---

## 🙋 Support & Contributing

For questions, issues, or contributions:
1. Create an issue describing the problem
2. Fork and create a feature branch
3. Submit a pull request with changes

---

**Built with ❤️ for educational innovation**

*Last Updated: 2026-08-30*
- Node.js
- Ollama
- Qwen 2.5 3B

## Start Qwen

```powershell
ollama run qwen2.5:3b
```

## Start backend

From the repository root:

```powershell
python -m pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

Backend:
http://localhost:8000

## Start frontend

In another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend:
http://localhost:5173

## Notes

This is a hackathon prototype with mock school services. Real school ERP integration,
production authentication, persistent database storage, and production-grade voice/avatar
services are not included here.
