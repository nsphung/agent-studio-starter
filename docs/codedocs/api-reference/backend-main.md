---
title: "backend/src/agent/main.py"
description: "API reference for the FastAPI app, health endpoint, and server entry point."
---

Source file: `backend/src/agent/main.py`

This module exposes the compiled agent graph over HTTP. It creates the FastAPI application, registers the LangGraph AGUI endpoint, defines the health route, and provides a `main()` entry point for Uvicorn.

## Import Path

```python
from agent.main import app, health_check, main
```

## App Construction

### `app`

```python
app = FastAPI(
    title="Weather Application Assistant",
    description="Get personalized weather updates based on your location and preferences",
    version="1.0.0",
)
```

This is the process-wide FastAPI app. During module import it immediately attempts to:

1. call `build_agent()`
2. wrap the graph in `LangGraphAGUIAgent`
3. register it at `path="/"` with `add_langgraph_fastapi_endpoint(...)`

If graph construction fails, the module prints an error and re-raises the exception.

## Functions

### `health_check`

```python
async def health_check() -> dict
```

Simple health endpoint exposed at `GET /healthz`.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| None | — | — | The handler takes no route parameters or query parameters. |

Return type:

```python
dict
```

Example response:

```json
{
  "status": "healthy",
  "service": "weather-application-assistant",
  "version": "1.0.0"
}
```

### `main`

```python
def main() -> None
```

Runs the Uvicorn development server using environment-driven host and port values.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| None | — | — | `main` reads process environment instead of accepting parameters. |

Environment variables read by `main()`:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `SERVER_HOST` | `str` | `0.0.0.0` | Bind host for the Uvicorn process. |
| `SERVER_PORT` | `str` parsed as `int` | `8123` | Bind port for the Uvicorn process. |

Internal call:

```python
uvicorn.run(
    "main:app",
    host=host,
    port=port,
    reload=True,
    log_level="info",
)
```

## Registered Agent Endpoint

The LangGraph endpoint registration currently looks like this:

```python
add_langgraph_fastapi_endpoint(
    app=app,
    agent=LangGraphAGUIAgent(
        name="weather_application_assistant",
        description="Get personalized weather updates based on your location and preferences",
        graph=agent_graph,
    ),
    path="/",
)
```

This is the backend route the frontend `LangGraphHttpAgent` ultimately talks to.

## Examples

### Run the service locally

```bash
cd /workspace/home/agent-studio-starter/backend
uv run python src/agent/main.py
```

### Verify the health endpoint

```bash
curl http://localhost:8123/healthz
```

### Reuse the app in another ASGI server

```python
from agent.main import app
```

That import is enough if your deployment platform handles ASGI startup separately.

## Notes

- The app performs graph construction at import time, so startup failures surface early.
- The registered agent name on the backend is `weather_application_assistant`, while the frontend runtime key is `weather_assistant`. Those names live in different layers and do not need to match exactly.
- `reload=True` is convenient for local development but is not a production server setting.
