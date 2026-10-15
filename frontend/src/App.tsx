import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { API, approve, deny, getCash, getEvents, getTickets, resetShop, runTicket } from "./api";
import { AGENTS, ORDER, type AgentKey } from "./agents";
import { Avatar } from "./Avatars";
import { describe, latestRun, summarize, type AgentSummary, type Line } from "./events";
import type { AgentEvent, Approval, Cash, Ticket } from "./types";

const usd = (n: number) => n.toLocaleString("en-US", { style: "currency", currency: "USD" });
const clock = (t: string) => new Date(t).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });

type Toast = { text: string; good: boolean } | null;

export default function App() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [cash, setCash] = useState<Cash | null>(null);
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [selected, setSelected] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [toast, setToast] = useState<Toast>(null);
  const [paid, setPaid] = useState<number[]>([]); // tickets with an approved payment that still need one more run to wrap up
  const selectedRef = useRef<number | null>(null);
  const busyRef = useRef(false);
  selectedRef.current = selected;

  const refresh = useCallback(async () => {
    try {
      const [t, c] = await Promise.all([getTickets(), getCash()]);
      setTickets(t);
      setCash(c);
      busyRef.current = t.some((x) => x.running);
      const id = selectedRef.current ?? t[0]?.id ?? null;
      if (selectedRef.current === null && id !== null) setSelected(id);
      if (id !== null) {
        const fetched = await getEvents(id);
        if (selectedRef.current === id || selectedRef.current === null) setEvents(fetched); // ignore a late answer for a ticket you've left
      }
      setError(null);
    } catch (e) {
      setError((e as Error).message);
    }
  }, []);

  // Keep the board fresh: quickly while a run is going, gently otherwise.
  useEffect(() => {
    let stop = false;
    let timer: ReturnType<typeof setTimeout>;
    const tick = async () => {
      await refresh();
      if (!stop) timer = setTimeout(tick, busyRef.current ? 1000 : 2500);
    };
    tick();
    return () => {
      stop = true;
      clearTimeout(timer);
    };
  }, [refresh]);

  // Picking another ticket: drop the old ticket's events right away and load the new ones.
  useEffect(() => {
    setEvents([]);
    refresh();
  }, [selected, refresh]);

  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(() => setToast(null), 6000);
    return () => clearTimeout(t);
  }, [toast]);

  const ticket = tickets.find((t) => t.id === selected) ?? null;
  const run = useMemo(() => latestRun(events), [events]);
  const running = !!ticket?.running;
  const summaries = useMemo(() => summarize(run, running), [run, running]);
  const lines = useMemo(() => run.map(describe).filter((l): l is Line => l !== null), [run]);
  const anyRunning = tickets.some((t) => t.running);

  async function start(id: number) {
    try {
      setPaid((p) => p.filter((x) => x !== id));
      await runTicket(id);
      setToast({ text: `The team is on ticket ${id}.`, good: true });
      await refresh();
    } catch (e) {
      setToast({ text: (e as Error).message, good: false });
    }
  }

  async function okay(a: Approval) {
    try {
      const done = await approve(a.id);
      if (done.status === "paid") {
        setPaid((p) => [...p, a.ticket_id]);
        setToast({ text: `Paid ${usd(done.result?.amount ?? 0)}. The drawer now holds ${usd(done.result?.new_balance ?? 0)}.`, good: true });
      } else {
        setToast({ text: `Refused: ${done.result?.reason ?? "the payment could not be made."}`, good: false });
      }
      await refresh();
    } catch (e) {
      setToast({ text: (e as Error).message, good: false });
    }
  }

  async function no(a: Approval) {
    try {
      await deny(a.id);
      setToast({ text: "Denied. Nothing was paid, and the team won't be asked for it again.", good: true });
      await refresh();
    } catch (e) {
      setToast({ text: (e as Error).message, good: false });
    }
  }

  async function reset() {
    if (!window.confirm("Put the whole shop back to how it started?")) return;
    try {
      await resetShop();
      setPaid([]);
      setToast({ text: "Fresh start. Everything is back to the original values.", good: true });
      await refresh();
    } catch (e) {
      setToast({ text: (e as Error).message, good: false });
    }
  }

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <span className="crest">CC</span>
          <div>
            <h1>Campus Customs Desk</h1>
            <p>The family business, live at the table</p>
          </div>
        </div>
        <CashDrawer cash={cash} />
        <button className="ghost" onClick={reset} disabled={anyRunning} title={anyRunning ? "Wait for the run to finish" : "Reset the shop"}>
          Fresh start
        </button>
      </header>

      {error && (
        <div className="offline">
          The desk can't reach the backend at {API} ({error}). Start it with <code>uvicorn main:app --reload --port 8000</code> from the backend folder.
        </div>
      )}
      {toast && <div className={`toast ${toast.good ? "good" : "bad"}`}>{toast.text}</div>}

      <main className="layout">
        <aside className="pile">
          <h2>Ticket pile</h2>
          {tickets.map((t) => (
            <TicketCard key={t.id} t={t} active={t.id === selected} onPick={() => setSelected(t.id)} />
          ))}
        </aside>

        <section className="desk">
          {ticket ? (
            <>
              <div className="deskhead">
                <div>
                  <span className="eyebrow">Ticket {ticket.id} · {ticket.type.replace("_", " ")}</span>
                  <h2>{ticket.subject} <small>from {ticket.requester}</small></h2>
                </div>
                <button className="primary" onClick={() => start(ticket.id)} disabled={anyRunning || !!error}>
                  {running ? "The team is working…" : ticket.status === "resolved" ? "Run it again" : "Start the team"}
                </button>
              </div>

              <StatusBanner ticket={ticket} needsRerun={paid.includes(ticket.id)} />

              {ticket.pending_approvals.map((a) => (
                <ApprovalSlip key={a.id} a={a} onApprove={() => okay(a)} onDeny={() => no(a)} />
              ))}

              <div className="table">
                <div className="boss-row">
                  <Seat who="boss" s={summaries.boss} big />
                </div>
                <div className="crew-row">
                  {(["ina", "ama", "father", "jervis"] as AgentKey[]).map((k) => (
                    <Seat key={k} who={k} s={summaries[k]} />
                  ))}
                </div>
              </div>

              <Summaries s={summaries} hasRun={run.length > 0} />
            </>
          ) : (
            <p className="empty">Waiting for the backend…</p>
          )}
        </section>

        <aside className="tape">
          <h2>The ticket tape</h2>
          <Tape lines={lines} running={running} />
        </aside>
      </main>
    </div>
  );
}

function CashDrawer({ cash }: { cash: Cash | null }) {
  const [shown, setShown] = useState<number | null>(null);
  const [delta, setDelta] = useState<number | null>(null);
  const last = useRef<number | null>(null);

  useEffect(() => {
    if (!cash) return;
    const from = last.current;
    const to = cash.balance;
    last.current = to;
    if (from === null || from === to) {
      setShown(to);
      return;
    }
    setDelta(to - from);
    const t0 = performance.now();
    let frame = 0;
    const step = (now: number) => {
      const p = Math.min(1, (now - t0) / 900);
      setShown(from + (to - from) * (1 - Math.pow(1 - p, 3)));
      if (p < 1) frame = requestAnimationFrame(step);
    };
    frame = requestAnimationFrame(step);
    const hide = setTimeout(() => setDelta(null), 7000);
    return () => {
      cancelAnimationFrame(frame);
      clearTimeout(hide);
    };
  }, [cash]);

  return (
    <div className="drawer" aria-live="polite">
      <span className="eyebrow">Cash drawer · checking</span>
      <div className="amount">
        {shown === null ? "…" : usd(shown)}
        {delta !== null && <span className={`delta ${delta < 0 ? "out" : "in"}`}>{delta < 0 ? "−" : "+"}{usd(Math.abs(delta))}</span>}
      </div>
      <span className="asof">{cash ? `as of ${cash.as_of}` : ""}</span>
    </div>
  );
}

function TicketCard({ t, active, onPick }: { t: Ticket; active: boolean; onPick: () => void }) {
  const waiting = t.pending_approvals.length > 0;
  return (
    <button className={`ticket ${active ? "active" : ""} ${t.status}`} onClick={onPick}>
      <span className="num">#{t.id}</span>
      <strong>{t.subject}</strong>
      <span className="who">{t.requester}</span>
      <span className="kind">{t.type.replace("_", " ")}</span>
      {t.running && <span className="chip live">working now</span>}
      {!t.running && waiting && <span className="chip ask">needs your OK</span>}
      {!t.running && !waiting && t.status === "open" && <span className="chip open">open</span>}
      {t.status === "resolved" && <span className="stamp">Resolved</span>}
    </button>
  );
}

function StatusBanner({ ticket, needsRerun }: { ticket: Ticket; needsRerun: boolean }) {
  const lr = ticket.last_run;
  if (ticket.status === "resolved")
    return <div className="banner resolved"><b>Resolved.</b> Filed in the drawer.{lr?.result?.decision ? ` ${lr.result.decision}` : ""}</div>;
  if (ticket.running) return <div className="banner live"><b>The team is working.</b> Watch the table and the tape.</div>;
  if (ticket.pending_approvals.length) return <div className="banner ask"><b>Waiting on you.</b> A payment is ready, but nothing moves until you approve it below.</div>;
  if (lr?.status === "failed") return <div className="banner bad"><b>The run stopped.</b> {lr.error}</div>;
  if (needsRerun) return <div className="banner live"><b>Payment made.</b> Start the team again so the Boss can finish this ticket.</div>;
  return <div className="banner idle">Not started yet. Press <b>Start the team</b>.</div>;
}

function ApprovalSlip({ a, onApprove, onDeny }: { a: Approval; onApprove: () => void; onDeny: () => void }) {
  const [busy, setBusy] = useState(false);
  return (
    <div className="slip">
      <div>
        <span className="eyebrow">Needs a human · {a.kind === "purchase" ? "purchase" : a.kind === "rent" ? "rent payment" : "invoice payment"}</span>
        <p>{a.description}</p>
        <small>The agents only prepared this. Cash moves only when you press Approve.</small>
      </div>
      <div className="choices">
        <button
          className="approve"
          disabled={busy}
          onClick={() => {
            setBusy(true);
            onApprove();
          }}
        >
          Approve &amp; pay
        </button>
        <button
          className="deny"
          disabled={busy}
          onClick={() => {
            setBusy(true);
            onDeny();
          }}
        >
          Deny
        </button>
      </div>
    </div>
  );
}

function Seat({ who, s, big }: { who: AgentKey; s: AgentSummary; big?: boolean }) {
  const a = AGENTS[who];
  const status = s.status === "working" ? "at work" : s.status === "done" ? "done" : "not called";
  return (
    <div className={`seat ${big ? "big" : ""} ${s.status}`} style={{ ["--c" as string]: a.color, ["--soft" as string]: a.soft }}>
      <div className={`bubble ${s.said ? "has" : ""}`} title={s.said}>{s.said || (s.called ? "…" : "")}</div>
      <div className="portrait">
        <Avatar who={who} working={s.status === "working"} />
      </div>
      <div className="plate">
        <strong>{a.name}</strong>
        <span>{a.title}</span>
      </div>
      <span className={`state ${s.status}`}>{status}</span>
    </div>
  );
}

function Summaries({ s, hasRun }: { s: Record<AgentKey, AgentSummary>; hasRun: boolean }) {
  return (
    <div className="summaries">
      <h3>Who did what on this ticket</h3>
      {!hasRun && <p className="muted">Nothing yet. Start the team and each agent will report here.</p>}
      {hasRun && (
        <div className="cards">
          {ORDER.map((k) => {
            const a = AGENTS[k];
            const x = s[k];
            return (
              <div key={k} className={`card ${x.called ? "" : "off"}`} style={{ ["--c" as string]: a.color, ["--soft" as string]: a.soft }}>
                <div className="cardhead">
                  <span className="dot" />
                  <strong>{a.name}</strong>
                </div>
                {!x.called ? (
                  <p className="muted">Wasn't needed on this ticket.</p>
                ) : (
                  <>
                    {x.answer && <p>{x.answer}</p>}
                    {x.asked.length > 0 && <p className="meta">Asked: {x.asked.map((y) => AGENTS[y].name).join(", ")}</p>}
                    {x.tools.length > 0 && <p className="meta">Tools: {x.tools.map((t) => <code key={t}>{t}</code>)}</p>}
                    {!x.answer && x.status === "working" && <p className="muted">Still working…</p>}
                  </>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

function Tape({ lines, running }: { lines: Line[]; running: boolean }) {
  const end = useRef<HTMLDivElement>(null);
  useEffect(() => {
    end.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [lines.length]);
  return (
    <div className="feed">
      {lines.length === 0 && <p className="muted">Quiet at the desk. Press Start the team and the conversation shows up here, line by line.</p>}
      {lines.map((l) => {
        const a = l.who !== "human" && l.who !== "system" ? AGENTS[l.who] : null;
        const color = a ? a.color : l.who === "human" ? "#d6336c" : "#8a7d6e";
        return (
          <div key={l.key} className={`line ${l.kind}`} style={{ ["--c" as string]: color }}>
            <div className="who">
              <b>{a ? a.name : l.who === "human" ? "You (the Table)" : "Desk"}</b>
              {l.to && <span> → {l.to === "human" ? "you" : AGENTS[l.to].name}</span>}
              <time>{clock(l.time)}</time>
            </div>
            <p>{l.text}</p>
          </div>
        );
      })}
      {running && <div className="typing"><i /><i /><i /></div>}
      <div ref={end} />
    </div>
  );
}
