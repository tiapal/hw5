import type { Approval, AgentEvent, Cash, Ticket } from "./types";

// The problem 7 backend. Its CORS settings allow this page (http://localhost:5173).
export const API = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function call<T>(path: string, method = "GET"): Promise<T> {
  const res = await fetch(`${API}${path}`, { method });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(body.detail ?? `${res.status} ${res.statusText}`);
  return body as T;
}

export const getTickets = () => call<Ticket[]>("/tickets");
export const getCash = () => call<Cash>("/cash");
export const getEvents = (ticketId: number) => call<AgentEvent[]>(`/events?limit=500&ticket_id=${ticketId}`);
export const runTicket = (id: number) => call<{ run_id: string }>(`/tickets/${id}/run`, "POST");
export const approve = (id: number) => call<Approval>(`/approvals/${id}/approve`, "POST");
export const deny = (id: number) => call<Approval>(`/approvals/${id}/deny`, "POST");
export const resetShop = () => call<{ message: string }>("/reset", "POST");
