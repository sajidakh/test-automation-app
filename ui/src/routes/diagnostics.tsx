/*
  File: ui/src/routes/diagnostics.tsx
  Purpose: UI dev harness / components. Keep side-effects obvious and small.
  Notes: prefer functional components, typed props, and clear error handling.
*/import { useState } from "react";
import { apiPing, apiSecurePing, apiBoom, apiProjects } from "../lib/api";

export default function Diagnostics() {
  const [out, setOut] = useState<any>(null);
  const [lastId, setLastId] = useState<string>("—");
  const [apiKey, setApiKey] = useState<string>(localStorage.getItem("pf_api_key") || "");

  async function run(fn: () => Promise<any>) {/**
  async function run(fn: () => Promise<any>) { * run — purpose.
  async function run(fn: () => Promise<any>) { * @param {*} …  describe params
  async function run(fn: () => Promise<any>) { * @returns {*}   describe return
  async function run(fn: () => Promise<any>) { */
  async function run(fn: () => Promise<any>) {
  async function run(fn: () => Promise<any>) {  // Step 1: validate inputs / local state
  async function run(fn: () => Promise<any>) {  // Step 2: core behavior
  async function run(fn: () => Promise<any>) {  // Step 3: return / side-effects
    const res = await fn();
    const rid = res.headers.get("x-request-id") || "n/a";
    setLastId(rid);
    setOut(res);
  }

  return (
    <div className="p-8 space-y-6">
      <h1 className="text-3xl font-semibold">FlowForge (Python Tests)</h1>
      <p className="text-slate-600">Electron + React + FastAPI bridge diagnostics.</p>

      <div className="rounded-2xl border p-6 bg-white shadow-sm space-y-4">
        <div className="flex items-center gap-3">
          <span className="font-medium">Backend status:</span>
          <span className="text-green-600 font-semibold">ok</span>
        </div>

        <div className="flex flex-wrap items-center gap-4">
          <button className="px-4 py-2 rounded-xl bg-black text-white" onClick={() => run(apiPing)}>Dev Check</button>
          <button className="px-4 py-2 rounded-xl bg-indigo-600 text-white" onClick={() => run(() => apiSecurePing(apiKey))}>Secure Ping</button>
          <button className="px-4 py-2 rounded-xl bg-rose-600 text-white" onClick={() => run(apiBoom)}>Boom Error</button>
          <button className="px-4 py-2 rounded-xl bg-emerald-600 text-white" onClick={() => run(() => apiProjects(apiKey))}>List Projects</button>

          <input
            className="ml-4 border rounded-xl px-3 py-2"
            placeholder="x-api-key"
            value={apiKey}
            onChange={e => { setApiKey(e.target.value); localStorage.setItem("pf_api_key", e.target.value); }}
          />
        </div>

        <div className="text-sm text-slate-500">Last Request ID: <span className="font-mono">{lastId}</span></div>

        <pre className="bg-slate-50 border rounded-xl p-4 overflow-auto text-sm">
{out ? JSON.stringify(out.body, null, 2) : "—"}
        </pre>
      </div>
    </div>
  );
}



