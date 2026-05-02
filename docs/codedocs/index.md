---
title: "Getting Started"
description: "Build a LangGraph Deep Agents backend and a CopilotKit generative UI frontend from the agent-studio-starter template."
---

`/nsphung/agent-studio-starter` is a starter application for building AI agents with a Python LangGraph backend and a Next.js CopilotKit frontend.

## The Problem

- Agent backends and chat frontends usually evolve as separate systems, which makes tool streaming and UI synchronization brittle.
- Teams often want custom UI for tool calls, but most starter apps stop at plain text responses.
- Local development gets messy when Python, Node.js, Docker, and Kubernetes are all introduced at once.
- Durable agent state, transport wiring, and deployment scaffolding take longer to assemble than the first useful demo.

## The Solution

This template gives you a narrow but complete vertical slice: `backend/src/agent/utils.py` builds a Deep Agents graph, `backend/src/agent/main.py` exposes it through FastAPI, `frontend/src/app/api/copilotkit/route.ts` proxies requests into that graph, and `frontend/src/app/page.tsx` turns the `get_weather` tool result into a custom weather card.

```tsx
// frontend/src/app/page.tsx
useRenderToolCall({
  name: "get_weather",
  render: ({ status, result }) => {
    const weatherData =
      result && typeof result === "string" ? JSON.parse(result) : result;

    if (status !== "complete") {
      return <p>Fetching weather...</p>;
    }

    return <p>{weatherData.location}: {weatherData.temperature}°{weatherData.unit}</p>;
  },
});
```

That pattern lets the model decide when to call a tool, while the frontend decides how the result should look.

## Installation

The backend always uses `uv`. Pick the frontend package manager your team prefers.

" "bun"]}>
<Tab value="npm">

```bash
cd /workspace/home/agent-studio-starter/backend
uv sync --group dev

cd /workspace/home/agent-studio-starter/frontend
npm install
```

</Tab>
<Tab value="pnpm">

```bash
cd /workspace/home/agent-studio-starter/backend
uv sync --group dev

cd /workspace/home/agent-studio-starter/frontend
pnpm install
```

</Tab>
<Tab value="yarn">

```bash
cd /workspace/home/agent-studio-starter/backend
uv sync --group dev

cd /workspace/home/agent-studio-starter/frontend
yarn install
```

</Tab>
<Tab value="bun">

```bash
cd /workspace/home/agent-studio-starter/backend
uv sync --group dev

cd /workspace/home/agent-studio-starter/frontend
bun install
```

</Tab>
</Tabs>

## Quick Start

Use this sequence when you want the minimum working weather assistant on your machine.

```bash
# terminal 1
cd /workspace/home/agent-studio-starter/backend
uv run python src/agent/main.py

# terminal 2
cd /workspace/home/agent-studio-starter/frontend
npm run dev
```

Then open `http://localhost:3000`, ask `What's the weather in SF?`, and the expected behavior is:

```text
1. The frontend sends a POST request to /api/copilotkit.
2. The runtime forwards the request to http://localhost:8123.
3. The backend agent calls get_weather("sf").
4. The page renders a weather card with location, temperature, humidity, and wind speed.
```

If you want a backend-only smoke test, `python src/agent/utils.py` invokes the compiled graph directly with a `thread_id` config and prints the final message.

## Key Features

- Python 3.13 FastAPI backend with `deepagents==0.3.12`
- Next.js 16 frontend with CopilotKit React and runtime packages
- Custom `useRenderToolCall` UI for structured tool results
- In-memory checkpointing through `MemorySaver`
- Local development entry points plus Skaffold and Kubernetes manifests
- Minimal surface area that is easy to replace when you add real tools or a real model

## Supported Environments

- Backend: Python 3.13, `uv`, FastAPI, Uvicorn
- Frontend: Node.js 22-compatible environment, Next.js App Router, React 19
- Deployment: Docker, Kubernetes manifests, Skaffold live-sync

<Cards>
  <Card title="Architecture" href="/docs/architecture">See how the backend graph, proxy route, and UI page connect.</Card>
  <Card title="Core Concepts" href="/docs/agent-graph">Start with the agent graph, runtime bridge, and generative UI model.</Card>
  <Card title="API Reference" href="/docs/api-reference/backend-agent-utils">Inspect exact signatures, parameters, and source files.</Card>
</Cards>
