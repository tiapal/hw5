// Shapes of what the problem 7 backend returns.

export type PaymentResult = {
  ok: boolean;
  reason?: string;
  amount?: number;
  new_balance?: number;
  payment_id?: number;
};

export type Approval = {
  id: number;
  ticket_id: number;
  run_id: string;
  kind: "invoice" | "rent" | "purchase" | string;
  ref: string;
  description: string;
  status: "pending" | "paid" | "refused" | string;
  result?: PaymentResult;
};

export type LastRun = {
  run_id: string;
  status: "running" | "finished" | "failed";
  result?: { decision?: string; customer_message?: string; money_spent?: number };
  error?: string;
};

export type Ticket = {
  id: number;
  type: string;
  requester: string;
  subject: string;
  status: "open" | "resolved";
  running: boolean;
  pending_approvals: Approval[];
  last_run: LastRun | null;
};

export type Cash = { account: string; balance: number; as_of: string };

// One line of output/audit_trail.json.
export type AgentEvent = {
  time: string;
  run_id?: string;
  ticket_id?: number;
  agent: string;
  depth?: number;
  step?: number;
  kind: string;
  tool?: string;
  args?: string;
  result?: string;
  text?: string;
  output?: string;
  decision?: string;
  description?: string;
  detail?: string;
  reason?: string;
};
