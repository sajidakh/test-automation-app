import { app, BrowserWindow } from "electron";
import * as fs from "fs";
import * as path from "path";

function resolveUiUrl(): string {
  const envUrl = process.env.FF_UI_URL;
  if (envUrl && envUrl.trim()) return envUrl.trim();

  const candidates = [
    path.resolve(__dirname, "..", "..", "..", ".ff_ui_port"),
    path.resolve(__dirname, "..", "..", ".ff_ui_port"),
  ];
  for (const f of candidates) {
    try {
      if (fs.existsSync(f)) {
        const port = fs.readFileSync(f, "ascii").trim();
        if (port) return `http://127.0.0.1:${port}/`;
      }
    } catch { /* ignore */ }
  }
  return "http://127.0.0.1:5173/";
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: { contextIsolation: true, nodeIntegration: false, sandbox: true },
  });

  const url = resolveUiUrl();
  console.log("Electron loading URL:", url);
  void win.loadURL(url);
}

app.whenReady().then(createWindow);
app.on("window-all-closed", () => { if (process.platform !== "darwin") app.quit(); });
app.on("activate", () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });
