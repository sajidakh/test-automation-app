/*
  File: ui/tests/smoke.spec.ts
  Purpose: UI dev harness / components. Keep side-effects obvious and small.
  Notes: prefer functional components, typed props, and clear error handling.
*/import { test, expect, request } from "@playwright/test";

const UI  = process.env.UI_URL  || "http://localhost:5173";
const API = process.env.API_URL || "http://localhost:8000";

test("UI root loads", async ({ page }) => {
  const resp = await page.goto(UI + "/");
  expect(resp?.ok()).toBeTruthy();
});

test("API /health ok", async () => {
  const r = await request.newContext();
  const res = await r.get(API + "/health");
  expect(res.status()).toBeLessThan(300);
  expect((await res.text()).trim()).toBe("ok");
});


