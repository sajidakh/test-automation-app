// ui/src/env.ts
export function apiBase(): string {
    const viteEnv = (import.meta as any)?.env?.VITE_API_BASE as string | undefined;
    const injected =
        typeof window !== "undefined" &&
            (window as any).__PF__ &&
            typeof (window as any).__PF__.apiBase === "string"
            ? ((window as any).__PF__.apiBase as string)
            : undefined;

    return (viteEnv?.trim() || injected?.trim() || "http://127.0.0.1:8000");
}
