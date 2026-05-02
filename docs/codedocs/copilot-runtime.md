---
title: "Copilot Runtime Bridge"
description: "See how the Next.js route proxies browser traffic to the LangGraph backend through CopilotKit."
---

The Copilot runtime bridge is the transport layer between the browser and the backend graph. In this repo it lives in `frontend/src/app/api/copilotkit/route.ts`, and it is deliberately tiny. That file creates a `CopilotRuntime`, registers a single agent named `weather_assistant`, and forwards POST requests into `copilotRuntimeNextJSAppRouterEndpoint(...)`.

## What It Is

At runtime, the frontend never talks to the backend directly from the page component. Instead:

1. `frontend/src/app/layout.tsx` points CopilotKit at `/api/copilotkit`.
2. `frontend/src/app/api/copilotkit/route.ts` receives that request.
3. The route forwards the request to `LangGraphHttpAgent`.
4. `LangGraphHttpAgent` targets `process.env.LANGGRAPH_DEPLOYMENT_URL || "http://localhost:8123"`.

That gives you a single stable browser-facing endpoint even when the backend URL changes by environment.

## Why It Exists

This extra hop looks small, but it solves three real problems:

- The browser does not need to know the backend deployment address.
- You can swap environments with `LANGGRAPH_DEPLOYMENT_URL`.
- CopilotKit gets to own the request/response protocol, streaming behavior, and agent selection.

## How It Relates to Other Concepts

- It depends on the provider configured in `frontend/src/app/layout.tsx`.
- It depends on the backend endpoint registered in `backend/src/agent/main.py`.
- It supplies the tool call events that `frontend/src/app/page.tsx` renders.

```mermaid
graph LR
  Layout[layout.tsx CopilotKit provider] --> Route[/api/copilotkit]
  Route --> Runtime[CopilotRuntime]
  Runtime --> LG[LangGraphHttpAgent]
  LG --> Backend[FastAPI LangGraph endpoint]
  Backend --> ToolEvents[tool events and messages]
  ToolEvents --> Page[page.tsx hooks]
```

## How It Works Internally

The route file imports:

```ts
import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { LangGraphHttpAgent } from "@copilotkit/runtime/langgraph";
import { NextRequest } from "next/server";
```

`ExperimentalEmptyAdapter` is used as `serviceAdapter`. The runtime is configured with one agent:

```ts
const runtime = new CopilotRuntime({
  agents: {
    weather_assistant: new LangGraphHttpAgent({
      url: process.env.LANGGRAPH_DEPLOYMENT_URL || "http://localhost:8123",
    }),
  },
});
```

The exported handler then builds `handleRequest` on demand and returns `handleRequest(req)`. No business logic is embedded in the route. That is useful because route behavior remains stable even as you add tools or alter the backend graph.

## Basic Usage

If you keep the starter layout, you only need to set the environment variable when the backend is not local:

```bash
LANGGRAPH_DEPLOYMENT_URL=http://backend:8123 npm run dev
```

The route will still present `/api/copilotkit` to the browser, but internally it will forward to the in-cluster backend service.

## Advanced Usage

A common extension is exposing multiple agents from the same frontend route:

```ts
import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { LangGraphHttpAgent } from "@copilotkit/runtime/langgraph";

const runtime = new CopilotRuntime({
  agents: {
    weather_assistant: new LangGraphHttpAgent({
      url: process.env.WEATHER_AGENT_URL || "http://localhost:8123",
    }),
    support_assistant: new LangGraphHttpAgent({
      url: process.env.SUPPORT_AGENT_URL || "http://localhost:8124",
    }),
  },
});
```

With that change, `layout.tsx` or a child component can select a different `agent` value. The route remains the same; only runtime configuration changes.

<Callout type="warn">The agent key in the runtime must match the `agent` prop passed to `<CopilotKit>` in `frontend/src/app/layout.tsx`. In this starter the key is `weather_assistant`. If you rename one side without renaming the other, the UI will fail before any backend logic runs.</Callout>

<Accordions>
<Accordion title="Why proxy through a Next.js route instead of calling the backend directly from the browser?">
The proxy route keeps backend topology out of browser code and makes local and cluster deployments share the same frontend contract. That is useful when you want a browser to hit `/api/copilotkit` regardless of whether the backend is at `localhost`, a Kubernetes service, or a remote deployment. The trade-off is an extra layer to debug. If requests fail, you now need to verify the provider, the route, and the backend URL instead of checking a single direct fetch call.
</Accordion>
<Accordion title="Why keep a single runtime with one registered agent?">
A single-agent runtime is easier to reason about when you are proving out the tool and UI pattern. The route code stays almost declarative, and the provider only needs one `agent` name. The trade-off is that your frontend becomes specialized around one backend persona. If you later add multiple agents, create explicit naming conventions and make sure each page or provider chooses the correct agent key rather than relying on defaults.
</Accordion>
</Accordions>

This file is small, but it is the protocol choke point of the frontend. If the app cannot talk to the backend, this is the first file to inspect.
