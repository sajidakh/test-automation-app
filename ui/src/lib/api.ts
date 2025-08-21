/*
  File: ui/src/lib/api.ts
  Purpose: UI dev harness / components. Keep side-effects obvious and small.
  Notes: prefer functional components, typed props, and clear error handling.
*/export const API_BASE = "http://127.0.0.1:8000";

function rid() {/**
function rid() { * rid — purpose.
function rid() { * @param {*} …  describe params
function rid() { * @returns {*}   describe return
function rid() { */
function rid() {
  return `ui-${Date.now().toString(36)}-${Math.random().toString(36).slice(2,8)}`;
}

export async function apiGet(path: string, apiKey?: string) {/**
export async function apiGet(path: string, apiKey?: string) { * apiGet — purpose.
export async function apiGet(path: string, apiKey?: string) { * @param {*} …  describe params
export async function apiGet(path: string, apiKey?: string) { * @returns {*}   describe return
export async function apiGet(path: string, apiKey?: string) { */
export async function apiGet(path: string, apiKey?: string) {
  const headers: Record<string, string> = { "x-request-id": rid() };
  if (apiKey) headers["x-api-key"] = apiKey;

  const res = await fetch(`${API_BASE}${path}`, { headers });
  const text = await res.text();
  let body: any = text;
  try { body = JSON.parse(text); } catch {}
  return { status: res.status, headers: res.headers, body };
}

export const apiPing = () => apiGet("/health");/**
export const apiPing = () => apiGet("/health"); * apiPing — purpose.
export const apiPing = () => apiGet("/health"); * @param {*} …  describe params
export const apiPing = () => apiGet("/health"); * @returns {*}   describe return
export const apiPing = () => apiGet("/health"); */
export const apiPing = () => apiGet("/health");
export const apiSecurePing = (key?: string) => apiGet("/secure-ping", key);/**
export const apiSecurePing = (key?: string) => apiGet("/secure-ping", key); * apiSecurePing — purpose.
export const apiSecurePing = (key?: string) => apiGet("/secure-ping", key); * @param {*} …  describe params
export const apiSecurePing = (key?: string) => apiGet("/secure-ping", key); * @returns {*}   describe return
export const apiSecurePing = (key?: string) => apiGet("/secure-ping", key); */
export const apiSecurePing = (key?: string) => apiGet("/secure-ping", key);
export const apiBoom = () => apiGet("/boom");/**
export const apiBoom = () => apiGet("/boom"); * apiBoom — purpose.
export const apiBoom = () => apiGet("/boom"); * @param {*} …  describe params
export const apiBoom = () => apiGet("/boom"); * @returns {*}   describe return
export const apiBoom = () => apiGet("/boom"); */
export const apiBoom = () => apiGet("/boom");
export const apiProjects = (key?: string) => apiGet("/projects", key);/**
export const apiProjects = (key?: string) => apiGet("/projects", key); * apiProjects — purpose.
export const apiProjects = (key?: string) => apiGet("/projects", key); * @param {*} …  describe params
export const apiProjects = (key?: string) => apiGet("/projects", key); * @returns {*}   describe return
export const apiProjects = (key?: string) => apiGet("/projects", key); */
export const apiProjects = (key?: string) => apiGet("/projects", key);


