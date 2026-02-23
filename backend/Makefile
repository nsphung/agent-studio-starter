.PHONY: install format test backend reset-gh-token

install:
	uv sync --group dev --active

format:
	ruff check .
	ruff format .
	mypy . 
	
test:
	pytest -v tests/

backend:
	echo "Starting backend server..."
	uv run --active src/agent/main.py 

reset-gh-token:
	echo "Reset GitHub Copilot token..."
	rm -fr ~/.config/litellm/github_copilot