import { AGENTS, DELEGATE_TOOLS, ORDER, agentFromAudit, type AgentKey } from "./agents";
import type { AgentEvent } from "./types";

// What an agent is doing, in plain words, for each MCP tool.
const DOING: Record<string, string> = {
  get_ticket: "reading the ticket",
  list_open_tickets: "going through the ticket pile",
  get_stock: "checking stock",
  list_vendors: "looking up vendors",
  get_vendor_invoices: "checking the vendor's invoices",
  get_invoice: "reading an invoice",
  get_cash: "checking the cash",
  get_pricing: "checking prices",
  get_lease: "reading the lease",
  get_today: "checking today's date",
  list_payments: "checking past payments",
  pay_invoice: "paying an invoice",
  pay_rent: "paying the rent",
  order_stock: "placing a stock order",
};

export type Line = {
  key: string;
  time: string;
  who: AgentKey | "human" | "system";
  to?: AgentKey | "human";
  kind: "ask" | "tool" | "answer" | "say" | "human" | "system" | "result";
  text: string;
};

// Nothing is cut here any more: the ticket tape shows full text (the bubbles on the table clamp it with CSS and show it all on hover).
const clip = (s: string, _n?: number) => s;

function field(raw: string | undefined, name: string): string | undefined {
  if (!raw) return undefined;
  try {
    const v = JSON.parse(raw)[name];
    return typeof v === "string" ? v : v === undefined ? undefined : JSON.stringify(v);
  } catch {
    // The audit trail cuts very long values, so fall back to a loose match.
    const m = raw.match(new RegExp(`"${name}"\\s*:\\s*"((?:[^"\\\\]|\\\\.)*)`));
    return m ? m[1] : undefined;
  }
}

const money = (n: unknown) => (typeof n === "number" ? `$${n.toLocaleString("en-US", { minimumFractionDigits: 2 })}` : "?");

// Turn an agent's final structured answer into one readable sentence.
export function summarizeOutput(output: string | undefined): string {
  if (!output) return "";
  let o: Record<string, unknown>;
  try {
    o = JSON.parse(output);
  } catch {
    return clip(output);
  }
  if (typeof o.decision === "string") return o.decision as string;
  if (typeof o.message === "string") return clip(o.message as string, 260);
  if ("on_hand" in o) {
    const parts = [`${o.sku} size ${o.size}: ${o.on_hand ?? "unknown"} on hand`];
    if (typeof o.shortage === "number" && o.shortage > 0) parts.push(`short by ${o.shortage}`);
    if (o.vendor_name) parts.push(`vendor ${o.vendor_name} (${o.lead_days ?? "?"} day lead)`);
    if (o.vendor_has_open_invoice) parts.push("vendor has an open invoice");
    return parts.join(", ");
  }
  if ("monthly_rent" in o)
    return `${o.landlord ?? "Lease"}: ${money(o.monthly_rent)} due ${o.next_due ?? "?"}` + (typeof o.days_left === "number" ? ` (${o.days_left} days left)` : "");
  if (typeof o.answer === "string") return clip(o.answer as string, 260);
  return clip(output);
}

export function describe(e: AgentEvent, i: number): Line | null {
  const key = `${e.time}-${i}`;
  const base = { key, time: e.time };
  const who = agentFromAudit(e.agent);

  if (e.kind === "run_start") return { ...base, who: "system", kind: "system", text: "The team has started on this ticket." };
  if (e.kind === "run_end") return { ...base, who: "system", kind: "system", text: "The Boss has finished." };
  if (e.kind === "run_stopped") return { ...base, who: "system", kind: "system", text: `The run stopped: ${e.reason ?? "unknown reason"}` };
  if (e.kind === "database_reset") return { ...base, who: "system", kind: "system", text: "The shop was reset to its original values." };
  if (e.kind === "guardrail_flag") return { ...base, who: "system", kind: "system", text: `Safety flag: ${e.detail ?? ""}` };

  if (e.kind === "human_decision") {
    const words = e.decision === "approved" ? "Approved" : e.decision === "denied" ? "Denied" : "Waiting for a decision";
    return { ...base, who: "human", kind: "human", text: `${words}: ${e.description ?? ""}` };
  }
  if (!who) return null;

  if (e.kind === "tool_call" && e.tool) {
    if (e.tool === "final_result") return null; // the agent handing in its final answer; shown as its own line
    if (e.tool === "ask_human")
      return { ...base, who, to: "human", kind: "ask", text: `asks you to approve: ${field(e.args, "description") ?? ""}` };
    const target = DELEGATE_TOOLS[e.tool];
    if (target) return { ...base, who, to: target, kind: "ask", text: clip(field(e.args, "question") ?? "") };
    return { ...base, who, kind: "tool", text: `is ${DOING[e.tool] ?? e.tool}…` };
  }
  if (e.kind === "tool_result" && e.tool === "ask_human")
    return { ...base, who, kind: "result", text: `The Table said: ${clip(e.result ?? "", 120)}` };
  if ((e.kind === "tool_result") && e.tool && /^(pay_|order_)/.test(e.tool)) {
    const ok = field(e.result, "ok");
    return { ...base, who, kind: "result", text: ok === "true" ? `Payment went through (${e.tool}).` : `Payment refused: ${field(e.result, "reason") ?? e.result}` };
  }
  if (e.kind === "model_text" && e.text) return { ...base, who, kind: "say", text: clip(e.text) };
  if (e.kind === "final_output") return { ...base, who, kind: "answer", text: summarizeOutput(e.output) };
  return null; // prompts, raw tool results and other plumbing stay out of the feed
}

export type AgentStatus = "working" | "done" | "idle";

export type AgentSummary = {
  key: AgentKey;
  called: boolean;
  status: AgentStatus;
  said: string; // their latest line, shown in the speech bubble
  tools: string[]; // MCP tools used
  asked: AgentKey[]; // who they delegated to
  answer: string; // their final report
};

// Everything the board shows per agent, worked out from one run's events.
export function summarize(events: AgentEvent[], running: boolean): Record<AgentKey, AgentSummary> {
  const out = {} as Record<AgentKey, AgentSummary>;
  for (const key of ORDER) out[key] = { key, called: false, status: "idle", said: "", tools: [], asked: [], answer: "" };

  events.forEach((e, i) => {
    const who = agentFromAudit(e.agent);
    if (!who) return;
    const s = out[who];
    s.called = true;
    if (e.kind === "tool_call" && e.tool) {
      const target = DELEGATE_TOOLS[e.tool];
      if (target) {
        if (!s.asked.includes(target)) s.asked.push(target);
      } else if (e.tool !== "ask_human" && !s.tools.includes(e.tool)) s.tools.push(e.tool);
    }
    if (e.kind === "final_output") s.answer = summarizeOutput(e.output);
    const line = describe(e, i);
    if (line) s.said = line.kind === "ask" && line.to ? `${line.to === "human" ? "To you" : `To ${AGENTS[line.to].name}`}: ${line.text}` : line.text;
  });

  // An agent still "works" while the run is going and they have not given their final answer.
  for (const key of ORDER) {
    const s = out[key];
    if (!s.called) continue;
    s.status = s.answer ? "done" : running ? "working" : "done";
  }
  // A delegated agent answers, then goes quiet; the Boss stays at work until his own final answer.
  return out;
}

// Only the most recent run for the ticket (a ticket can be run more than once).
export function latestRun(events: AgentEvent[]): AgentEvent[] {
  let id: string | undefined;
  for (const e of events) if (e.kind === "run_start") id = e.run_id;
  return id ? events.filter((e) => e.run_id === id) : [];
}
