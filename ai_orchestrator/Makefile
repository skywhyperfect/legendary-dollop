# Variables
BACKEND_DIR=backend
BOT_DIR=bot
FRONTEND_DIR=frontend

.PHONY: env
env:
	cp .env.example .env

.PHONY: run-backend
run-backend:
	cd $(BACKEND_DIR) && uvicorn app.main:app --reload --port 8000

.PHONY: run-bot
run-bot:
	cd $(BOT_DIR) && python main.py

.PHONY: run-frontend
run-frontend:
	cd $(FRONTEND_DIR) && npm run dev
