/*
  File: backend/node/src/lib/api.ts
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

async function req(path: string, apiKey?: string, init?: RequestInit) {/**
async function req(path: string, apiKey?: string, init?: RequestInit) { * req — purpose.
async function req(path: string, apiKey?: string, init?: RequestInit) { * @param {*} …  describe params
async function req(path: string, apiKey?: string, init?: RequestInit) { * @returns {*}   describe return
async function req(path: string, apiKey?: string, init?: RequestInit) { */
async function req(path: string, apiKey?: string, init?: RequestInit) {
  const headers: Record<string, string> = { "x-request-id": rid() };
  if (apiKey) headers["x-api-key"] = apiKey;
  const res = await fetch(`${API_BASE}${path}`, { headers, ...init });
  const txt = await res.text();
  let body: any = txt;
  try { body = JSON.parse(txt); } catch {}
  return { status: res.status, headers: res.headers, body };
}

export const apiPing = () => req("/health");/**
export const apiPing = () => req("/health"); * apiPing — purpose.
export const apiPing = () => req("/health"); * @param {*} …  describe params
export const apiPing = () => req("/health"); * @returns {*}   describe return
export const apiPing = () => req("/health"); */
export const apiPing = () => req("/health");
export const apiSecurePing = (key?: string) => req("/secure-ping", key);/**
export const apiSecurePing = (key?: string) => req("/secure-ping", key); * apiSecurePing — purpose.
export const apiSecurePing = (key?: string) => req("/secure-ping", key); * @param {*} …  describe params
export const apiSecurePing = (key?: string) => req("/secure-ping", key); * @returns {*}   describe return
export const apiSecurePing = (key?: string) => req("/secure-ping", key); */
export const apiSecurePing = (key?: string) => req("/secure-ping", key);
export const apiBoom = () => req("/boom");/**
export const apiBoom = () => req("/boom"); * apiBoom — purpose.
export const apiBoom = () => req("/boom"); * @param {*} …  describe params
export const apiBoom = () => req("/boom"); * @returns {*}   describe return
export const apiBoom = () => req("/boom"); */
export const apiBoom = () => req("/boom");
export const apiProjects = (key?: string) => req("/projects", key);/**
export const apiProjects = (key?: string) => req("/projects", key); * apiProjects — purpose.
export const apiProjects = (key?: string) => req("/projects", key); * @param {*} …  describe params
export const apiProjects = (key?: string) => req("/projects", key); * @returns {*}   describe return
export const apiProjects = (key?: string) => req("/projects", key); */
export const apiProjects = (key?: string) => req("/projects", key);


