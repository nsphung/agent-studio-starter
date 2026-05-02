---
title: "frontend/src/app/api/copilotkit/route.ts"
description: "API reference for the Next.js App Router endpoint that proxies CopilotKit requests to LangGraph."
---

Source file: `frontend/src/app/api/copilotkit/route.ts`

This module is the frontend transport boundary. It exposes the App Router `POST` handler that CopilotKit uses, and it configures the runtime with a single `LangGraphHttpAgent`.

## Exports

### `POST`

```ts
export const POST = async (req: NextRequest) => Response
```

This handler creates a `handleRequest` function with `copilotRuntimeNextJSAppRouterEndpoint(...)` and immediately returns `handleRequest(req)`.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `req` | `NextRequest` | — | Incoming Next.js request from the CopilotKit provider. |

Return type:

```ts
Promise<Response>
```

Example:

```ts
export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
```

## Runtime Configuration

The file also creates two module-level values that shape request handling:

### `serviceAdapter`

```ts
const serviceAdapter = new ExperimentalEmptyAdapter();
```

### `runtime`

```ts
const runtime = new CopilotRuntime({
  agents: {
    weather_assistant: new LangGraphHttpAgent({
      url: process.env.LANGGRAPH_DEPLOYMENT_URL || "http://localhost:8123",
    }),
  },
});
```

Environment variables:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `LANGGRAPH_DEPLOYMENT_URL` | `string` | `http://localhost:8123` | Backend LangGraph HTTP base URL. |

## Usage Patterns

### Standard local development

```bash
cd /workspace/home/agent-studio-starter/frontend
npm run dev
```

With no extra environment configuration, the route forwards to `http://localhost:8123`.

### Kubernetes-aware runtime

```yaml
env:
  - name: LANGGRAPH_DEPLOYMENT_URL
    value: "http://backend:8123"
```

That deployment pattern is already present in `frontend/k8s/deployment.yaml`.

### Multiple agent expansion

```ts
const runtime = new CopilotRuntime({
  agents: {
    weather_assistant: new LangGraphHttpAgent({
      url: process.env.WEATHER_AGENT_URL || "http://localhost:8123",
    }),
    forecast_assistant: new LangGraphHttpAgent({
      url: process.env.FORECAST_AGENT_URL || "http://localhost:8124",
    }),
  },
});
```

If you use this pattern, the provider in `layout.tsx` must specify the matching agent key.

## Notes

- The browser-facing path is always `/api/copilotkit`, regardless of backend deployment target.
- This module does not contain business logic. It is strictly a runtime transport adapter.
- The frontend and backend stay decoupled because the route uses an environment variable instead of hard-coding cluster or remote URLs.
