# AI Orchestrator (Покойо) – Smart School Assistant

> **Покойо** is a premium, AI‑driven orchestration platform for schools. It integrates **WhatsApp**, **voice‑to‑task**, **real‑time analytics**, and **AI‑generated reports** into a sleek, glass‑morphism dashboard.

---

## 📚 Table of Contents
1. [Project Overview](#-project-overview)
2. [Architecture](#-architecture)
3. [Features](#-features)
4. [Quick Start (Local Development)](#-quick-start-local-development)
5. [Backend API](#-backend-api)
6. [Frontend UI](#-frontend-ui)
7. [Environment Variables](#-environment-variables)
8. [Testing & Debugging](#-testing--debugging)
9. [Contribution Guide](#-contribution-guide)
10. [License](#-license)

---

## 🎯 Project Overview
**AI Orchestrator** (named *Покойо*) automates routine school workflows:
- Teachers send **WhatsApp messages** (voice or text) → automatically creates tasks.
- **Self‑assignment**: when a teacher replies with a confirmation keyword ("ок", "понял", etc.) the system instantly claims the pending task.
- **Analytics Dashboard**: real‑time KPIs, incident tracking, food‑service stats, and more.
- **AI‑Generated PDF Reports**: choose a period (week, month, quarter, custom) and get a beautifully styled, AI‑summarized report ready for printing.

All components are built with **FastAPI**, **React + TypeScript**, and **SQLite** for a lightweight, zero‑dependency deployment.

---

## 🏗 Architecture
```
legendary-dollop/
├─ ai_orchestrator/                # Python package (backend)
│   ├─ backend/
│   │   ├─ app/
│   │   │   ├─ api/               # FastAPI routers (bot_feed, tasks, analytics, …)
│   │   │   ├─ ai/                # LLM parsers, RAG, voice‑to‑task utilities
│   │   │   ├─ db/                # SQLite engine & migrations
│   │   │   └─ main.py            # FastAPI entry point
│   └─ whatsapp/                  # Node.js bridge forwarding WA messages to /api/bot/whatsapp-webhook
├─ frontend/                       # React + Vite UI
│   └─ src/App.tsx                # Dashboard + GenerateReportButton component
└─ orchestrator.db                 # SQLite DB (auto‑created on first run)
```

- **FastAPI** serves JSON APIs and static assets.
- **WhatsApp bridge** (Node.js) forwards inbound messages to `POST /api/bot/whatsapp-webhook`.
- **Analytics router** (`/api/analytics/report`) aggregates data and returns a printable HTML document.
- **Frontend** polls the backend every few seconds, displays glass‑morphism cards, and offers a period selector for reports.

---

## ✨ Features
| Feature | Description |
|---|---|
| **WhatsApp Integration** | Real‑time message ingestion, auto‑parsing, and task creation. |
| **Self‑Assignment Logic** | Confirmation keywords (`ок`, `принял`, `взял`…) auto‑assign tasks from "Нераспознанный сотрудник". |
| **Dynamic Keyword Expansion** | Supports natural‑language confirmations and multilingual variants. |
| **Analytics Dashboard** | KPIs: total messages, food portions, absences, task completion rate, incident list, etc. |
| **AI‑Generated Report** | Choose **week / month / quarter / custom** period → AI writes a concise summary → PDF‑ready HTML. |
| **Period Selector UI** | Tabs + custom date‑picker in the `GenerateReportButton` component. |
| **Automatic DB Migration** | Missing columns (`chat_id`, `parsed_summary`, `location`, …) are added on‑the‑fly. |
| **Premium UI** | Glass‑morphism, vibrant gradients, smooth micro‑animations, Google Inter font. |

---

## 🚀 Quick Start (Local Development)
> **Prerequisites**: Python 3.12+, Node 20+, npm, git.

```bash
# 1️⃣ Clone the repo
git clone https://github.com/skywhyperfect/legendary-dollop.git
cd legendary-dollop/ai_orchestrator

# 2️⃣ Create a virtual environment & install backend deps
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3️⃣ Set up environment variables (see section below)
cp .env.example .env
# edit .env as needed (OPENAI_API_KEY, WHATSAPP_TOKEN, etc.)

# 4️⃣ Run database migrations (auto‑run on first start)
# No manual step needed – the app will create `orchestrator.db`.

# 5️⃣ Start the FastAPI backend
uvicorn app.main:app --reload --port 8000

# 6️⃣ In another terminal, start the WhatsApp bridge (Node.js)
cd ../../whatsapp
npm install   # one‑time only
node index.js   # forwards messages to http://localhost:8000/api/bot/whatsapp-webhook

# 7️⃣ Start the React frontend (Vite)
cd ../../frontend
npm install
npm run dev   # opens http://localhost:5173
```

Open the dashboard, send a WhatsApp voice message, and watch the task appear instantly. Use the **AI Report** button at the bottom of the Analytics tab to generate a PDF.

---

## 📡 Backend API
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/bot/whatsapp-webhook` | Receives WhatsApp messages, stores them, runs self‑assignment logic. |
| `GET`  | `/api/tasks/` | List all tasks (with `is_accepted`, `is_completed`). |
| `GET`  | `/api/analytics/report` | Returns `{ html, stats }`. Accepts optional query params `date_from` & `date_to` (YYYY‑MM‑DD). |
| `GET`  | `/api/bot/messages` | Raw WhatsApp messages (debug). |
| `GET`  | `/ping` | Health check. |

All dates are stored in **localtime** (`datetime('now','localtime')`).

---

## 🎨 Frontend UI
- **Dashboard** (`App.tsx`) – glass‑morphism cards for tasks, KPIs, and director metrics.
- **GenerateReportButton** – new component with period tabs (7 days, month, quarter, custom) and date‑picker inputs.
- **Print‑Ready HTML** – generated on the backend; the button opens it in a new tab and triggers `window.print()` automatically.

> The UI uses **Tailwind‑compatible utility classes** written manually (no external UI library) to keep the bundle tiny while delivering premium aesthetics.

---

## 🔐 Environment Variables
Create a `.env` file in the project root:
```
# FastAPI
OPENAI_API_KEY=your-openai-key   # optional – fallback uses a static template
# WhatsApp bridge (example)
WHATSAPP_TOKEN=your-whatsapp-token
# Optional – set a custom DB path
SQLALCHEMY_DATABASE_URL=sqlite:///./orchestrator.db
```
If `OPENAI_API_KEY` is missing or set to `mock`, the system will use a deterministic fallback summary.

---

## 🧪 Testing & Debugging
- **Database inspection**: `sqlite3 orchestrator.db` → `SELECT * FROM tg_messages;`
- **API testing**: `curl http://localhost:8000/api/analytics/report?date_from=2026-04-01&date_to=2026-04-18`
- **Frontend logs**: open the browser console; the button prints the generated URL for the PDF.
- **WhatsApp bridge logs**: the Node process prints incoming messages and any forwarding errors.

---

## 🤝 Contribution Guide
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/awesome‑feature`).
3. Follow the existing code style (black for Python, Prettier for TS).
4. Write tests for new logic (pytest for backend, jest for frontend).
5. Submit a pull request – CI will run linting, type‑checking, and unit tests.

---

## 📄 License
This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

*Built with love for the AIS Hack 3.0 demo. Happy hacking!*
