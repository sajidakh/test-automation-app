/*
  File: backend/node/src/main.ts
  Purpose: UI dev harness / components. Keep side-effects obvious and small.
  Notes: prefer functional components, typed props, and clear error handling.
*/import { app, BrowserWindow, session } from "electron";
import path from "node:path";
import fs from "node:fs";

function readRuntime(): { ui?: { host?: string; port?: number } } {/**
function readRuntime(): { ui?: { host?: string; port?: number } } { * readRuntime — purpose.
function readRuntime(): { ui?: { host?: string; port?: number } } { * @param {*} …  describe params
function readRuntime(): { ui?: { host?: string; port?: number } } { * @returns {*}   describe return
function readRuntime(): { ui?: { host?: string; port?: number } } { */
function readRuntime(): { ui?: { host?: string; port?: number } } {
  try {
    const p = path.resolve(process.cwd(), "..", "..", ".pf.runtime.json");
    const raw = fs.readFileSync(p, "utf8");
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

function getUiUrl(): string {/**
function getUiUrl(): string { * getUiUrl — purpose.
function getUiUrl(): string { * @param {*} …  describe params
function getUiUrl(): string { * @returns {*}   describe return
function getUiUrl(): string { */
function getUiUrl(): string {
  // Dev defaults
  const runtime = readRuntime();
  const host = process.env.PF_UI_HOST || runtime.ui?.host || "127.0.0.1";
  const port = Number(process.env.PF_UI_PORT || runtime.ui?.port || 5173);
  return `http://${host}:${port}`;
}

function getApiOrigin(): string {/**
function getApiOrigin(): string { * getApiOrigin — purpose.
function getApiOrigin(): string { * @param {*} …  describe params
function getApiOrigin(): string { * @returns {*}   describe return
function getApiOrigin(): string { */
function getApiOrigin(): string {
  const host = process.env.PF_API_HOST || "127.0.0.1";
  const port = process.env.PF_API_PORT || "8000";
  return `http://${host}:${port}`;
}

function installProdCSP() {/**
function installProdCSP() { * installProdCSP — purpose.
function installProdCSP() { * @param {*} …  describe params
function installProdCSP() { * @returns {*}   describe return
function installProdCSP() { */
function installProdCSP() {
  // Only for packaged/prod builds
  if (process.env.NODE_ENV === "production") {
    const api = getApiOrigin();

    // Very strict CSP: no inline/eval, no remote code, locked connect-src
    // Adjust img/font if you embed assets from other schemes.
    const csp = [
      "default-src 'self'",
      "script-src 'self'",
      "style-src 'self'",
      "img-src 'self' data:",
      "font-src 'self' data:",
      `connect-src 'self' ${api}`,
      "object-src 'none'",
      "base-uri 'self'",
      "frame-ancestors 'none'",
      "form-action 'self'",
      "upgrade-insecure-requests",
    ].join("; ");

    session.defaultSession.webRequest.onHeadersReceived((details, callback) => {
      const headers = details.responseHeaders || {};
      headers["Content-Security-Policy"] = [csp];
      callback({ responseHeaders: headers });
    });
  }
}

async function createWindow() {/**
async function createWindow() { * createWindow — purpose.
async function createWindow() { * @param {*} …  describe params
async function createWindow() { * @returns {*}   describe return
async function createWindow() { */
async function createWindow() {
  const win = new BrowserWindow({
    width: 1100,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: true,
    },
    show: true,
  });

  const url = getUiUrl();
  await win.loadURL(url);
  win.on("closed", () => {
    // noop
  });
}

app.whenReady().then(() => {
  installProdCSP();
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});


