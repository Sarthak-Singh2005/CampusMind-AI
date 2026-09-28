# CampusMind AI Architecture

CampusMind AI is a full-stack, role-aware assistant for school communities. It demonstrates how an AI interface can safely connect natural-language requests to scoped school operations.

## System overview

```text
React + Vite client
        |
        | HTTP / JSON
        v
FastAPI API -> session store -> mock school ERP data
        |
        v
LangGraph workflow
  1. Injection screening
  2. Intent and entity extraction (Ollama / Qwen)
  3. Student resolution
  4. Role-based authorization
  5. Attendance or support-request tool
  6. Language-aware response generation
```

## Design decisions

- **Role-aware tools, not prompt-only permissions.** Authorization is performed in Python tool functions for each data operation. The LLM may classify a request, but it cannot grant access to data.
- **Explicit confirmation for escalations.** Requests to contact a teacher or school management return a pending action. A separate API call submits the request only after the user confirms it.
- **Local-first AI.** Qwen runs through Ollama, so the project can be demonstrated without an external model API key.
- **Environment-based configuration.** Model URL/name, frontend origin, API metadata, and message limit are configured through `.env`, with committed example templates for a reproducible setup.
- **Deliberately bounded prototype.** Users, attendance, sessions, and support requests are in-memory mock data. Production integrations require a database, SSO, audit logging, encrypted secrets, and a persistent job queue.

## API surface

| Endpoint | Purpose |
| --- | --- |
| `GET /api/health` | Lightweight service health check |
| `GET /api/languages` | Supported response languages |
| `POST /api/login` | Creates a role-validated demo session |
| `POST /api/chat` | Runs the agent workflow for an authenticated session |
| `POST /api/support/confirm` | Confirms a human-support escalation |

## Security boundaries

The demo blocks common prompt-injection patterns, validates message size and language, validates session IDs, and checks role/data ownership inside the backend tools. These controls are illustrative; they are not a substitute for production identity management and formal security review.
