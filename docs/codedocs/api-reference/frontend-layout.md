---
title: "frontend/src/app/layout.tsx"
description: "API reference for the root layout and CopilotKit provider configuration."
---

Source file: `frontend/src/app/layout.tsx`

This module wraps the entire frontend in the CopilotKit provider. Without it, the page component cannot use CopilotKit hooks or connect to the route at `/api/copilotkit`.

## Exports

### `metadata`

```ts
export const metadata: Metadata
```

Current value:

```ts
export const metadata: Metadata = {
  title: "Weather Assistant | Deep Agents with CopilotKit",
  description: "A weather assistant powered by Deep Agents and CopilotKit",
};
```

### `RootLayout`

```tsx
export default function RootLayout(
  props: Readonly<{ children: React.ReactNode }>
): JSX.Element
```

The source declares the props inline:

```tsx
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={"antialiased"}>
        <CopilotKit runtimeUrl="/api/copilotkit" agent="weather_assistant">
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `children` | `React.ReactNode` | — | Nested page content rendered inside the provider. |

## Provider Configuration

`<CopilotKit>` is configured with two important props:

| Prop | Type | Value | Description |
|------|------|-------|-------------|
| `runtimeUrl` | `string` | `/api/copilotkit` | Browser-facing route that handles CopilotKit requests. |
| `agent` | `string` | `weather_assistant` | Frontend runtime key used by `route.ts`. |

## Usage Example

### Keep the same route but switch agents

```tsx
<CopilotKit runtimeUrl="/api/copilotkit" agent="forecast_assistant">
  {children}
</CopilotKit>
```

If you make this change, `frontend/src/app/api/copilotkit/route.ts` must register `forecast_assistant` inside the runtime.

### Wrap additional application chrome around the provider

```tsx
export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <header>Agent Studio</header>
        <CopilotKit runtimeUrl="/api/copilotkit" agent="weather_assistant">
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}
```

## Notes

- This file imports `@copilotkit/react-ui/styles.css`, which is required for the sidebar styling.
- The provider depends on the route module for transport and the page module for actual rendering.
- The agent name here must match the runtime key in `route.ts`.
