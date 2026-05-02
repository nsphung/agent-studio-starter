---
title: "backend/src/agent/utils.py"
description: "API reference for the backend tool and agent graph builder."
---

Source file: `backend/src/agent/utils.py`

This module contains the backend composition root. It defines the only tool in the starter, constructs the Deep Agent graph, and includes a direct invocation example in the `__main__` block.

## Import Paths

```python
from agent.utils import build_agent, get_weather
```

## Module State

### `model`

```python
model = ChatLiteLLM(model="github_copilot/gpt-5-mini")
```

This is a module-level model instance used by `build_agent()`. It is not wrapped in a helper function, so importing the module also initializes the LiteLLM client object.

## Functions

### `get_weather`

```python
def get_weather(city: str) -> str
```

Returns mocked weather data as a JSON string. The frontend weather card expects the serialized result to contain the keys `location`, `temperature`, `unit`, `weather`, `humidity`, and `windSpeed`.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `city` | `str` | — | City name supplied by the model when the tool is invoked. |

Return type:

```python
str
```

Example:

```python
from agent.utils import get_weather

result = get_weather("San Francisco")
print(result)
```

Expected output shape:

```json
{
  "location": "San Francisco",
  "temperature": 72,
  "unit": "F",
  "weather": "sunny",
  "humidity": 45,
  "windSpeed": 8
}
```

### `build_agent`

```python
def build_agent() -> CompiledStateGraph
```

Builds and returns the compiled Deep Agent graph used by FastAPI. Internally it creates a `MemorySaver`, then calls `create_deep_agent(...)` with the module-level model, the weather tool, CopilotKit middleware, and a simple system prompt.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| None | — | — | `build_agent` takes no arguments in the current starter. |

Return type:

```python
CompiledStateGraph
```

Example:

```python
from agent.utils import build_agent

graph = build_agent()
config = {"configurable": {"thread_id": "docs-example"}}

result = graph.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
    config=config,
)
```

## Internal Composition

`build_agent()` currently expands to the equivalent of:

```python
checkpointer = MemorySaver()
agent_graph = create_deep_agent(
    model=model,
    tools=[get_weather],
    middleware=[CopilotKitMiddleware()],
    system_prompt="You are a helpful assistant",
    checkpointer=checkpointer,
)
```

That means the following configuration is hard-coded in source:

| Setting | Value | Source |
|---------|-------|--------|
| Model | `github_copilot/gpt-5-mini` | module-level `model` |
| Tools | `[get_weather]` | `build_agent()` |
| Middleware | `[CopilotKitMiddleware()]` | `build_agent()` |
| System prompt | `"You are a helpful assistant"` | `build_agent()` |
| Checkpointer | `MemorySaver()` | `build_agent()` |

## Common Patterns

### Direct graph invocation

Use the graph directly when you want to debug backend behavior without FastAPI:

```python
from agent.utils import build_agent

graph = build_agent()
config = {"configurable": {"thread_id": "manual-run"}}

response = graph.invoke(
    {"messages": [{"role": "user", "content": "weather in Tokyo"}]},
    config=config,
)
print(response["messages"][-1].content)
```

### Reusing the tool contract in another tool

If you add more tools, keep the result format frontend-friendly:

```python
import json


def get_air_quality(city: str) -> str:
    return json.dumps(
        {
            "location": city,
            "aqi": 42,
            "category": "good",
        }
    )
```

That mirrors the `get_weather` pattern and works well with `useRenderToolCall(...)`.

## Notes

- Because a checkpointer is configured, pass a `thread_id` in direct invocations.
- Because the result is a string, frontend code must parse it before reading fields.
- Because the tool is mocked, productionizing this module means replacing the hard-coded weather payload first.
