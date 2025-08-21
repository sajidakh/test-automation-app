/*
  File: backend/node/vitest.config.ts
  Purpose: UI dev harness / components. Keep side-effects obvious and small.
  Notes: prefer functional components, typed props, and clear error handling.
*/import { defineConfig } from "vitest/config";

export default defineConfig({
    test: {
        globals: true,
        environment: "node",
        include: ["src/**/*.test.ts"]
    }
});


