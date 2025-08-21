/*
  File: backend/node/src.bak.2plus/main.ts
  Purpose: UI dev harness / components. Keep side-effects obvious and small.
  Notes: prefer functional components, typed props, and clear error handling.
*/import { app, BrowserWindow } from "electron";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function createWindow() {/**
async function createWindow() { * createWindow — purpose.
async function createWindow() { * @param {*} …  describe params
async function createWindow() { * @returns {*}   describe return
async function createWindow() { */
async function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            sandbox: true,
            preload: path.join(__dirname, "preload.js")
        }
    });

    // Vite dev server (locked to strict port 5173)
    await win.loadURL("http://127.0.0.1:5173");
}

app.whenReady().then(() => {
    createWindow();
    app.on("activate", () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") app.quit();
});


