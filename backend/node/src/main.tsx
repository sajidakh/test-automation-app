import React from "react";
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
