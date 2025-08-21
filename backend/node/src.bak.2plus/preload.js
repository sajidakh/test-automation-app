/**
 * Secure Preload Script - Provides a safe bridge for renderer
 * Prevents direct Node.js access to frontend
 */

// Minimal, safe preload. Extend later for IPC.
const { contextBridge } = require("electron");
contextBridge.exposeInMainWorld("appInfo", {
    env: process.env.NODE_ENV || "development"
});

