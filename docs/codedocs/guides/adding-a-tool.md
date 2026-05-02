---
title: "Adding a Tool"
description: "Add a new backend tool and wire a matching frontend renderer so the agent can produce custom UI."
---

This project becomes useful when you add tools beyond the mocked weather example. The pattern is consistent: define the tool in the backend graph, then decide whether the frontend should render it through the generic fallback or a specialized UI component.

<Steps>
<Step>
### Define the tool in `backend/src/agent/utils.py`

Add a new function with a clear signature and return shape:

```python
import json


def get_forecast(city: str, days: int = 3) -> str:
    forecast = {
        "location": city,
        "days": days,
        "forecast": [
            {"day": 1, "weather": "sunny", "high": 74, "low": 60},
            {"day": 2, "weather": "cloudy", "high": 70, "low": 58},
            {"day": 3, "weather": "rain", "high": 66, "low": 55},
        ],
    }
    return json.dumps(forecast)
```

Returning JSON text keeps the transport contract aligned with the existing weather tool.
</Step>
<Step>
### Register the tool with the graph

Update `build_agent()` so the graph can call it:

```python
agent_graph = create_deep_agent(
    model=model,
    tools=[get_weather, get_forecast],
    middleware=[CopilotKitMiddleware()],
    system_prompt="You are a helpful assistant",
    checkpointer=checkpointer,
)
```

If the tool is not listed in `tools=[...]`, the model cannot invoke it regardless of how good your prompt is.
</Step>
<Step>
### Add a frontend renderer

Create a matching renderer in `frontend/src/app/page.tsx`:

```tsx
useRenderToolCall({
  name: "get_forecast",
  render: ({ status, result }) => {
    const data =
      result && typeof result === "string" ? JSON.parse(result) : result;

    if (status !== "complete") {
      return <p>Loading forecast...</p>;
    }

    return (
      <div>
        <h3>{data.location}</h3>
        <ul>
          {data.forecast.map((item: { day: number; weather: string; high: number; low: number }) => (
            <li key={item.day}>
              Day {item.day}: {item.weather}, high {item.high}, low {item.low}
            </li>
          ))}
        </ul>
      </div>
    );
  },
});
```

This turns the tool result into app UI instead of leaving it as a generic debug block.
</Step>
<Step>
### Preserve the fallback renderer

Keep `useDefaultTool(...)` in the page:

```tsx
useDefaultTool({
  render: ({ name, status, args, result }) => (
    <details>
      <summary>{status === "complete" ? `Called ${name}` : `Calling ${name}`}</summary>
      <p>Status: {status}</p>
      <p>Args: {JSON.stringify(args)}</p>
      <p>Result: {JSON.stringify(result)}</p>
    </details>
  ),
});
```

That gives you visibility into tools that do not yet have dedicated UI.
</Step>
</Steps>

## Complete Example

Putting both sides together looks like this:

```python
# backend/src/agent/utils.py
def get_forecast(city: str, days: int = 3) -> str:
    return json.dumps(
        {
            "location": city,
            "days": days,
            "forecast": [
                {"day": 1, "weather": "sunny", "high": 74, "low": 60},
                {"day": 2, "weather": "cloudy", "high": 70, "low": 58},
            ],
        }
    )
```

```tsx
// frontend/src/app/page.tsx
useRenderToolCall({
  name: "get_forecast",
  render: ({ result }) => {
    const data = result && typeof result === "string" ? JSON.parse(result) : result;
    return <pre>{JSON.stringify(data, null, 2)}</pre>;
  },
});
```

## Common Failure Modes

- The backend tool returns a Python dict, but the frontend renderer assumes JSON text and calls `JSON.parse`.
- The tool is registered in code but not included in the `tools=[...]` list passed to `create_deep_agent(...)`.
- The tool name in `useRenderToolCall({ name: "..." })` does not match the actual backend function name.
- The renderer assumes fields exist, but the backend returns a different shape.

This repo is intentionally small, so the fastest way to grow it safely is to add one tool and one renderer at a time.
