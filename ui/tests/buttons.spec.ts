/*
  File: ui/tests/buttons.spec.ts
  Purpose: UI dev harness / components. Keep side-effects obvious and small.
  Notes: prefer functional components, typed props, and clear error handling.
*/import { test, expect } from "@playwright/test";
const UI  = process.env.UI_URL  || "http://localhost:5173";

async function clickAndTime(page, testId: string, waitFor: RegExp) {/**
async function clickAndTime(page, testId: string, waitFor: RegExp) { * clickAndTime — purpose.
async function clickAndTime(page, testId: string, waitFor: RegExp) { * @param {*} …  describe params
async function clickAndTime(page, testId: string, waitFor: RegExp) { * @returns {*}   describe return
async function clickAndTime(page, testId: string, waitFor: RegExp) { */
async function clickAndTime(page, testId: string, waitFor: RegExp) {
async function clickAndTime(page, testId: string, waitFor: RegExp) {  // Step 1: validate inputs / local state
async function clickAndTime(page, testId: string, waitFor: RegExp) {  // Step 2: core behavior
async function clickAndTime(page, testId: string, waitFor: RegExp) {  // Step 3: return / side-effects
  const t0 = Date.now();
  const wait = page.waitForResponse(r => waitFor.test(r.url()), { timeout: 15000 });
  await page.getByTestId(testId).click({ timeout: 5000 });
  const res  = await wait;
  const body = await res.text();
  const ms   = Date.now() - t0;
  console.log(`[ui-e2e] ${testId} -> ${res.status()} in ${ms}ms; body="${body}"`);
  return { status: res.status(), ms, body };
}

test.beforeEach(async ({ page }) => {
  const resp = await page.goto(UI + "/");
  expect(resp?.ok()).toBeTruthy();
  await expect(page.getByTestId("btn-health")).toBeVisible({ timeout: 5000 });
  await expect(page.getByTestId("btn-secure")).toBeVisible({ timeout: 5000 });
  await expect(page.getByTestId("btn-404")).toBeVisible({ timeout: 5000 });
});

test("Health button -> /health 200", async ({ page }) => {
  const r = await clickAndTime(page, "btn-health", /\/health$/);
  expect(r.status).toBe(200);
});

test("Secure button -> /secure-ping 200", async ({ page }) => {
  const r = await clickAndTime(page, "btn-secure", /\/secure-ping$/);
  expect(r.status).toBe(200);
});

test("404 button -> /does-not-exist 404", async ({ page }) => {
  const r = await clickAndTime(page, "btn-404", /\/does-not-exist$/);
  expect(r.status).toBe(404);
});



