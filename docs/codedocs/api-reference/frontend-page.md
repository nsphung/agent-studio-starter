---
title: "frontend/src/app/page.tsx"
description: "API reference for the main page component and its tool rendering hooks."
---

Source file: `frontend/src/app/page.tsx`

This page component is the main user interface of the starter. It does three things:

1. registers a fallback tool renderer with `useDefaultTool(...)`
2. registers a custom weather renderer with `useRenderToolCall(...)`
3. renders `<CopilotSidebar>` inside the page

## Export

### `Page`

```tsx
export default function Page(): JSX.Element
```

The source does not annotate the return type explicitly, but the component returns JSX and functions as the default export for the `/` route.

Example:

```tsx
export default function Page() {
  useDefaultTool({ ... });
  useRenderToolCall({ name: "get_weather", render: ... });

  return (
    <main>
      <h1>Your App so so good!</h1>
      <CopilotSidebar ></CopilotSidebar>
    </main>
  );
}
```

## Hook Registrations

### `useDefaultTool`

```tsx
useDefaultTool({
  render: ({ name, status, args, result }) => JSX.Element,
})
```

Purpose:

- gives unknown tools a debuggable default UI
- shows the tool name, execution status, arguments, and result

Renderer fields used:

| Field | Type | Description |
|-------|------|-------------|
| `name` | tool name-like value | Displayed in the `<summary>` text. |
| `status` | status-like value | Used to choose `Calling` versus `Called`. |
| `args` | serializable object | Displayed with `JSON.stringify(args)`. |
| `result` | serializable value | Displayed with `JSON.stringify(result)`. |

Example:

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

### `useRenderToolCall`

```tsx
useRenderToolCall({
  name: "get_weather",
  render: ({ status, args, result }) => JSX.Element,
})
```

Purpose:

- intercept the `get_weather` tool specifically
- parse the result payload
- render loading, structured, or fallback states

Renderer fields used:

| Field | Type | Description |
|-------|------|-------------|
| `status` | status-like value | Controls the loading indicator and complete state. |
| `args` | serializable object | Available for debugging or future UI, though not heavily used now. |
| `result` | `string` or object-like value | Parsed as JSON when possible. |

## Internal Helpers

The render callback defines two internal helpers:

### `getWeatherIcon`

```tsx
const getWeatherIcon = (condition: string) => string
```

Maps weather condition text to emoji such as `☀️`, `☁️`, `🌧️`, or `⛈️`.

### `getWeatherGradient`

```tsx
const getWeatherGradient = (condition: string) => string
```

Maps weather condition text to a Tailwind gradient string such as `from-yellow-400 via-orange-400 to-pink-400`.

## Usage Examples

### Keep the existing weather card behavior

```tsx
useRenderToolCall({
  name: "get_weather",
  render: ({ status, result }) => {
    const weatherData =
      result && typeof result === "string" ? JSON.parse(result) : result;

    if (status !== "complete") {
      return <p>Fetching weather...</p>;
    }

    return <p>{weatherData.location}</p>;
  },
});
```

### Add another specialized tool renderer

```tsx
useRenderToolCall({
  name: "get_forecast",
  render: ({ status, result }) => {
    const data =
      result && typeof result === "string" ? JSON.parse(result) : result;

    if (status !== "complete") {
      return <p>Loading forecast...</p>;
    }

    return <pre>{JSON.stringify(data, null, 2)}</pre>;
  },
});
```

## Notes

- The page is marked `"use client";` because it relies on client-side hooks.
- The current heading text is placeholder UI copy, not part of the runtime contract.
- The result parser falls back cleanly when the tool result is plain text instead of JSON.
