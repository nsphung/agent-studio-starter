.PHONY: dev backend frontend

dev:
	skaffold dev

backend:
	echo "Starting backend server..."
	cd backend && uv run src/agent/main.py

frontend:
	echo "Starting frontend server..."
	cd frontend && npm run dev

