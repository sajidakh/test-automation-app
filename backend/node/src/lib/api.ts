/*
  File: backend/node/src/lib/api.ts
  Purpose: UI dev harness / components. Keep side-effects obvious and small.
  Notes: prefer functional components, typed props, and clear error handling.
*/export const API_BASE = "http://127.0.0.1:8000";

function rid() {
  return `ui-${Date.now().toString(36)}-${Math.random().toString(36).slice(2,8)}`;
}

async function req(path: string, apiKey?: string, init?: RequestInit) {
  const headers: Record<string, string> = { "x-request-id": rid() };
  if (apiKey) headers["x-api-key"] = apiKey;
  const res = await fetch(`${API_BASE}${path}`, { headers, ...init });
  const txt = await res.text();
  let body: any = txt;
  try { body = JSON.parse(txt); } catch {}
  return { status: res.status, headers: res.headers, body };
}

export const apiPing = () => req("/health");
export const apiSecurePing = (key?: string) => req("/secure-ping", key);
export const apiBoom = () => req("/boom");
export const apiProjects = (key?: string) => req("/projects", key);

