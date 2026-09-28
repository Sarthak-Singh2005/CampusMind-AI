# CampusMind AI — Backend

FastAPI-based backend for the CampusMind AI school assistant, featuring LangGraph-based AI agent orchestration, multi-language support, and role-based access control.

## Quick Start

### Prerequisites
- Python 3.11 or higher
- Ollama with Qwen 2.5 3B model

### Installation

1. **Install dependencies** from the repository root:
   ```powershell
   python -m pip install -r backend/requirements.txt
   ```

2. **Ensure Ollama is running** (in a separate terminal):
   ```powershell
   ollama run qwen2.5:3b
   ```

3. **Start the backend server**:
   ```powershell
   uvicorn backend.app.main:app --reload
   ```

The API will be available at:
- **Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)

## Project Structure

```
backend/
├── __init__.py
├── README.md
├── requirements.txt
└── app/
    ├── __init__.py
    ├── main.py              # FastAPI application & routes
    ├── auth.py              # Authentication & user validation
    ├── graph.py             # LangGraph agent orchestration
    ├── prompts.py           # System prompts & language templates
    ├── tools.py             # Tool definitions for agent
    ├── school_data.py       # Mock school data & language support
    ├── security.py          # Security utilities & validation
    └── state.py             # Pydantic state schemas
```

## API Endpoints

### Authentication

**POST** `/api/login`
- Authenticate user and create session
- Request body:
  ```json
  {
    "email": "student@example.com",
    "role": "student"
  }
  ```
- Response: Session ID, user info, role

### Chat

**POST** `/api/chat`
- Send message and receive AI response
- Request body:
  ```json
  {
    "session_id": "uuid-here",
    "message": "What is my attendance?",
    "language": "English"
  }
  ```
- Response: AI-generated response in specified language

### Utilities

**GET** `/api/languages`
- List all supported languages
- Response:
  ```json
  {
    "languages": [
      "English", "Hindi", "Tamil", ...
    ]
  }
  ```

## Key Components

### auth.py
- User authentication against mock database
- Role validation (student, parent, teacher, principal)
- User context creation

### graph.py
LangGraph state machine with nodes:
- Intent detection
- Authorization checks
- Entity extraction
- Tool routing
- Tool execution
- Response generation
- Language translation

### prompts.py
- Role-specific system prompts
- Language-specific templates
- Intent detection prompts
- Few-shot examples

### tools.py
Available tools:
- `get_attendance()` - Retrieve attendance records
- `get_grades()` - Access grade information
- `mark_attendance()` - Record attendance
- `get_schedule()` - Fetch class schedule
- `create_support_request()` - Human escalation

### security.py
- Prompt injection detection
- Input validation
- Malicious pattern detection
- Security policy enforcement

### state.py
Pydantic models for type safety:
- GraphState schema
- ChatRequest/Response models
- User and session contexts

## Configuration

Create a `.env` file in the root directory (see `.env.example` for template):
```
DEBUG=True
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:3b
```

## Supported Roles

| Role | Access Level | Key Features |
|------|--------------|--------------|
| **Student** | Personal data only | Grade queries, attendance tracking |
| **Parent** | Child's data | Progress monitoring, attendance |
| **Teacher** | Class data | Attendance marking, class reports |
| **Principal** | School-wide | Analytics, global reports |

## Supported Languages

English, Hindi, Tamil, Telugu, Marathi, Bengali, Gujarati, Punjabi, Kannada, Malayalam, Urdu

## Development

### Hot Reload
The `--reload` flag enables auto-reloading on file changes:
```powershell
uvicorn backend.app.main:app --reload
```

### Code Quality
```powershell
# Format code
black backend/

# Lint
flake8 backend/

# Type checking
mypy backend/
```

## Deployment

### Production Server
```powershell
# Using Gunicorn (recommended for production)
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
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Ollama Connection Error
- Ensure Ollama is running: `ollama run qwen2.5:3b`
- Check connection URL in `.env` (default: http://localhost:11434)
- Verify model is downloaded: `ollama list`

### CORS Errors
- Frontend must be on allowed origins (configured in main.py)
- Development: http://localhost:5173 is allowed

### Session Not Found
- Session ID in chat request must match login response
- Sessions expire after inactivity

## Performance Optimization

- **Caching**: Consider Redis for session storage
- **Database**: Replace in-memory sessions with persistent storage
- **Async**: FastAPI handles async operations efficiently
- **Batching**: Combine multiple requests where possible

## Security Notes

- Current authentication is mock-based for demo purposes
- Production should implement proper OAuth2/JWT authentication
- Sensitive data should not be logged
- Rate limiting should be added for production
- HTTPS is required for production

## Monitoring

Enable structured logging for production:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Future Enhancements

- [ ] Database integration for persistent sessions
- [ ] Advanced authentication (OAuth2, JWT)
- [ ] API rate limiting
- [ ] Websocket support for real-time chat
- [ ] Request/response caching
- [ ] Comprehensive error logging
- [ ] Performance metrics
- [ ] Load testing

