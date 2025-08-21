/*
  File: backend/node/src/pages/Diagnostics.tsx
  Purpose: UI dev harness / components. Keep side-effects obvious and small.
  Notes: prefer functional components, typed props, and clear error handling.
*/import { useState } from "react";
import { apiGet } from "../lib/api";

type Result = {
  status: number;
  requestId?: string | null;
  body: unknown;
};

export default function Diagnostics() {
  const [apiKey, setApiKey] = useState<string>("");
  const [health, setHealth] = useState<Result | null>(null);
  const [secure, setSecure] = useState<Result | null>(null);
  const [busy, setBusy] = useState<boolean>(false);

  async function runHealth() {/**
  async function runHealth() { * runHealth — purpose.
  async function runHealth() { * @param {*} …  describe params
  async function runHealth() { * @returns {*}   describe return
  async function runHealth() { */
  async function runHealth() {
    setBusy(true);
    const res = await apiGet("/health");
    setHealth({
      status: res.status,
      requestId: res.headers.get("x-request-id"),
      body: res.body,
    });
    setBusy(false);
  }

  async function runSecure() {/**
  async function runSecure() { * runSecure — purpose.
  async function runSecure() { * @param {*} …  describe params
  async function runSecure() { * @returns {*}   describe return
  async function runSecure() { */
  async function runSecure() {
    setBusy(true);
    const res = await apiGet("/secure-ping", apiKey || undefined);
    setSecure({
      status: res.status,
      requestId: res.headers.get("x-request-id"),
      body: res.body,
    });
    setBusy(false);
  }

  return (
    <div style={{ maxWidth: 800, margin: "2rem auto", fontFamily: "system-ui, sans-serif" }}>
      <h1>Diagnostics</h1>

      <section style={{ marginTop: "1rem", padding: "1rem", border: "1px solid #ddd", borderRadius: 8 }}>
        <h2 style={{ marginTop: 0 }}>Secure Ping</h2>
        <label style={{ display: "block", marginBottom: 8 }}>
          <span style={{ display: "block", fontSize: 12, color: "#666" }}>API Key (x-api-key)</span>
          <input
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="dev-secret-123"
            style={{ width: "100%", padding: 8, borderRadius: 6, border: "1px solid #ccc" }}
          />
        </label>
        <div style={{ display: "flex", gap: 8 }}>
          <button onClick={runHealth} disabled={busy} style={{ padding: "8px 12px", borderRadius: 6 }}>
            GET /health
          </button>
          <button onClick={runSecure} disabled={busy} style={{ padding: "8px 12px", borderRadius: 6 }}>
            GET /secure-ping
          </button>
        </div>
      </section>

      <section style={{ marginTop: "1rem", display: "grid", gap: "1rem" }}>
        <div style={{ padding: "1rem", border: "1px solid #eee", borderRadius: 8 }}>
          <h3 style={{ marginTop: 0 }}>/health result</h3>
          {health ? (
            <pre style={{ whiteSpace: "pre-wrap" }}>
Status: {health.status}
Request-Id: {health.requestId ?? "(none)"}
Body:
{JSON.stringify(health.body, null, 2)}
            </pre>
          ) : (
            <div style={{ color: "#888" }}>No call yet.</div>
          )}
        </div>

        <div style={{ padding: "1rem", border: "1px solid #eee", borderRadius: 8 }}>
          <h3 style={{ marginTop: 0 }}>/secure-ping result</h3>
          {secure ? (
            <pre style={{ whiteSpace: "pre-wrap" }}>
Status: {secure.status}
Request-Id: {secure.requestId ?? "(none)"}
Body:
{JSON.stringify(secure.body, null, 2)}
            </pre>
          ) : (
            <div style={{ color: "#888" }}>No call yet.</div>
          )}
        </div>
      </section>
    </div>
  );
}


