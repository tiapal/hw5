export type AgentKey = "boss" | "ina" | "ama" | "father" | "jervis";

export type AgentInfo = {
  key: AgentKey;
  name: string; // nameplate
  title: string;
  color: string; // the agent's own colour
  soft: string; // a pale wash of it for backgrounds
  blurb: string;
};

// Distinct colour per agent: oak, navy, red, green, grey.
export const AGENTS: Record<AgentKey, AgentInfo> = {
  boss: { key: "boss", name: "The Boss", title: "Head of the table", color: "#9a6a2b", soft: "#f1e2c8", blurb: "Assumes everyone is slacking. Reads tickets like poetry." },
  ina: { key: "ina", name: "Inventory Ina", title: "Stock & vendors", color: "#1f3a6e", soft: "#dde5f4", blurb: "Counts everything twice. Notices a shortage from across the room." },
  ama: { key: "ama", name: "Accounting Ama", title: "Cash & invoices", color: "#b3322f", soft: "#f6dcda", blurb: "Glasses, receipts, opinions. Never pays without a signature." },
  father: { key: "father", name: "Facilities Father", title: "Lease & rent", color: "#3f6b45", soft: "#dcebdd", blurb: "Grumpy about late rent. His coffee is only hot while he works." },
  jervis: { key: "jervis", name: "Jervis", title: "Customer service", color: "#6b6d72", soft: "#e4e5e8", blurb: "The butler. Drafts the letters, says only what he was told." },
};

export const ORDER: AgentKey[] = ["boss", "ina", "ama", "father", "jervis"];

// Names exactly as the audit trail writes them.
const FROM_AUDIT: Record<string, AgentKey> = {
  Boss: "boss",
  "Inventory Ina": "ina",
  "Accounting Ama": "ama",
  "Facilities Father": "father",
  "Customer Service Jervis": "jervis",
};

export const agentFromAudit = (name: string): AgentKey | null => FROM_AUDIT[name] ?? null;

// ask_* tools are delegations: the tool name says who is being asked.
export const DELEGATE_TOOLS: Record<string, AgentKey> = {
  ask_inventory_ina: "ina",
  ask_accounting_ama: "ama",
  ask_facilities_father: "father",
  ask_customer_service_jervis: "jervis",
};
