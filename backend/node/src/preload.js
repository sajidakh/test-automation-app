/*
  File: backend/node/src/preload.js
  Purpose: UI dev harness / components. Keep side-effects obvious and small.
  Notes: prefer functional components, typed props, and clear error handling.
*/// secure, minimal preload
const { contextBridge } = require("electron");
contextBridge.exposeInMainWorld("api", {
  getAppVersion: () => require("electron").app.getVersion()
});


