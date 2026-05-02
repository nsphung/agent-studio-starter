---
title: "Local Development"
description: "Run the backend and frontend together locally and verify the full request path before changing the app."
---

This guide walks through the fastest way to get the starter running on one machine. The goal is not just to see a page load. The goal is to verify the full path from browser to Next.js route to FastAPI graph to tool renderer.

<Steps>
<Step>
### Install backend dependencies

```bash
cd /workspace/home/agent-studio-starter/backend
uv sync --group dev
```

The backend requires Python 3.13 according to `backend/pyproject.toml`. The `dev` group also installs `pytest`, `ruff`, `mypy`, and `deepeval`.
</Step>
<Step>
### Start the backend

```bash
cd /workspace/home/agent-studio-starter/backend
uv run python src/agent/main.py
```

By default the server binds to `SERVER_HOST=0.0.0.0` and `SERVER_PORT=8123`. Those defaults come from `backend/src/agent/main.py`.
</Step>
<Step>
### Install frontend dependencies

```bash
cd /workspace/home/agent-studio-starter/frontend
npm install
```

The frontend depends on Next.js 16, React 19, and the CopilotKit packages declared in `frontend/package.json`.
</Step>
<Step>
### Start the frontend

```bash
cd /workspace/home/agent-studio-starter/frontend
npm run dev
```

The route at `frontend/src/app/api/copilotkit/route.ts` will use `http://localhost:8123` unless you override `LANGGRAPH_DEPLOYMENT_URL`.
</Step>
<Step>
### Verify the end-to-end flow

Open `http://localhost:3000`, open the Copilot sidebar, and ask:

```text
What's the weather in San Francisco?
```

Expected behavior:

```text
- The browser posts to /api/copilotkit.
- The runtime forwards to the backend LangGraph endpoint.
- The graph calls get_weather.
- The page renders a custom weather card instead of plain tool text.
```
</Step>
</Steps>

## Runnable Smoke Tests

If you want to isolate each layer, use these checks:

```bash
# backend health
curl http://localhost:8123/healthz

# expected JSON
{"status":"healthy","service":"weather-application-assistant","version":"1.0.0"}
```

```bash
# backend-only graph invocation
cd /workspace/home/agent-studio-starter/backend
uv run python src/agent/utils.py
```

The second command uses the `__main__` block in `backend/src/agent/utils.py`, which constructs a graph and invokes it with `thread_id=test-session-1`.

## Troubleshooting

If the page loads but tool UI never appears, check these in order:

1. Confirm the backend is reachable at `http://localhost:8123/healthz`.
2. Confirm `frontend/src/app/layout.tsx` still sets `agent="weather_assistant"`.
3. Confirm `frontend/src/app/api/copilotkit/route.ts` still registers an agent under the same key.
4. Confirm `backend/src/agent/utils.py` still exposes a tool named `get_weather`.

If the backend starts but agent calls fail, the model configuration in `backend/src/agent/utils.py` is the next place to inspect because it hard-codes `ChatLiteLLM(model="github_copilot/gpt-5-mini")`.

## Why This Guide Matters

The repo looks simple, but failures can happen at four separate layers: browser provider setup, Next.js route forwarding, FastAPI graph registration, and model or tool execution. Running this exact flow first gives you a known-good baseline before you add tools, prompts, or deployment changes.
