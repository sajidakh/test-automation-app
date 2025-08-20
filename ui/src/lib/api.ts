export const API_BASE = "http://127.0.0.1:8000";

function rid() {
  return `ui-${Date.now().toString(36)}-${Math.random().toString(36).slice(2,8)}`;
}

export async function apiGet(path: string, apiKey?: string) {
  const headers: Record<string, string> = { "x-request-id": rid() };
  if (apiKey) headers["x-api-key"] = apiKey;

  const res = await fetch(`${API_BASE}${path}`, { headers });
  const text = await res.text();
  let body: any = text;
  try { body = JSON.parse(text); } catch {}
  return { status: res.status, headers: res.headers, body };
}

export const apiPing = () => apiGet("/health");
export const apiSecurePing = (key?: string) => apiGet("/secure-ping", key);
export const apiBoom = () => apiGet("/boom");
export const apiProjects = (key?: string) => apiGet("/projects", key);
