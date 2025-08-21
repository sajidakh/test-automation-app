/*
  File: ui/src/main.tsx
  Purpose: UI dev harness / components. Keep side-effects obvious and small.
  Notes: prefer functional components, typed props, and clear error handling.
*/import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";

const el = document.getElementById("root") || (() => {
  const d = document.createElement("div");
  d.id = "root"; document.body.appendChild(d); return d;
})();

createRoot(el).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);


