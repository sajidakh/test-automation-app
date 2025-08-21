/*
  File: backend/node/src/main.tsx
  Purpose: UI dev harness / components. Keep side-effects obvious and small.
  Notes: prefer functional components, typed props, and clear error handling.
*/import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Diagnostics from "./routes/diagnostics";

const router = createBrowserRouter([
  { path: "/", element: <Diagnostics /> },
  { path: "/diagnostics", element: <Diagnostics /> },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

