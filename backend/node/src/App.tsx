/*
  File: backend/node/src/App.tsx
  Purpose: UI dev harness / components. Keep side-effects obvious and small.
  Notes: prefer functional components, typed props, and clear error handling.
*/import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
import Diagnostics from "./pages/Diagnostics";

function Home() {
  return (
    <div style={{ maxWidth: 800, margin: "2rem auto", fontFamily: "system-ui, sans-serif" }}>
      <h1>FlowForge UI</h1>
      <p>Welcome. Use the Diagnostics page to test API connectivity.</p>
      <p><Link to="/diagnostics">Go to Diagnostics →</Link></p>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <nav style={{ padding: "0.75rem 1rem", borderBottom: "1px solid #eee", display: "flex", gap: 16 }}>
        <Link to="/">Home</Link>
        <Link to="/diagnostics">Diagnostics</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/diagnostics" element={<Diagnostics />} />
      </Routes>
    </BrowserRouter>
  );
}

