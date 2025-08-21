/*
  File: ui/src/App.tsx
  Purpose: UI dev harness / components. Keep side-effects obvious and small.
  Notes: prefer functional components, typed props, and clear error handling.
*/import React from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const API_KEY = import.meta.env.VITE_API_KEY || ""; // optional

async function call(path: string, opts: RequestInit = {}) {/**
async function call(path: string, opts: RequestInit = {}) { * call — purpose.
async function call(path: string, opts: RequestInit = {}) { * @param {*} …  describe params
async function call(path: string, opts: RequestInit = {}) { * @returns {*}   describe return
async function call(path: string, opts: RequestInit = {}) { */
async function call(path: string, opts: RequestInit = {}) {
async function call(path: string, opts: RequestInit = {}) {  // Step 1: validate inputs / local state
async function call(path: string, opts: RequestInit = {}) {  // Step 2: core behavior
async function call(path: string, opts: RequestInit = {}) {  // Step 3: return / side-effects
  const headers: Record<string,string> = { "content-type": "application/json" };
  if (API_KEY && path.includes("secure-ping")) headers["x-api-key"] = API_KEY;
  const res = await fetch(API_URL + path, { ...opts, headers });
  return res;
}

export default function App() {
  const [log, setLog] = React.useState<string[]>([]);

  async function ping(path: string, label: string) {/**
  async function ping(path: string, label: string) { * ping — purpose.
  async function ping(path: string, label: string) { * @param {*} …  describe params
  async function ping(path: string, label: string) { * @returns {*}   describe return
  async function ping(path: string, label: string) { */
  async function ping(path: string, label: string) {
  async function ping(path: string, label: string) {  // Step 1: validate inputs / local state
  async function ping(path: string, label: string) {  // Step 2: core behavior
  async function ping(path: string, label: string) {  // Step 3: return / side-effects
    const t0 = performance.now();
    try {
      const res = await call(path);
      const txt = await res.text();
      const ms  = Math.round(performance.now() - t0);
      setLog(x => [`${label}: ${res.status} in ${ms}ms — ${txt}`, ...x]);
      console.log(`[ui] ${label} -> ${res.status} in ${ms}ms body="${txt}"`);
    } catch (e:any) {
      const ms = Math.round(performance.now() - t0);
      setLog(x => [`${label}: ERROR in ${ms}ms — ${e?.message ?? e}`, ...x]);
      console.error(`[ui] ${label} ERROR in ${ms}ms`, e);
    }
  }

  return (
    <div style={{fontFamily:"system-ui", padding:20}}>
      <h1>FF Dev UI</h1>
      <p style={{margin:"4px 0 12px"}}>API: {API_URL}</p>
      <div style={{display:"flex", gap:10, margin:"12px 0"}}>
        <button data-testid="btn-health" onClick={() => ping("/health","/health")}>Health</button>
        <button data-testid="btn-secure" onClick={() => ping("/secure-ping","/secure-ping")}>Secure</button>
        <button data-testid="btn-404"    onClick={() => ping("/does-not-exist","/does-not-exist")}>404</button>
        <button data-testid="btn-clear"  onClick={() => setLog([])}>Clear</button>
      </div>
      <pre style={{background:"#111", color:"#0f0", padding:12, minHeight:160}}>{log.join("\n")}</pre>
    </div>
  );
}



