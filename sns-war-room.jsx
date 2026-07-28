import { useState, useEffect, useRef } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ReferenceLine, ResponsiveContainer } from "recharts";

// ── Generate 30-day confidence history ──────────────────────
function generateHistory() {
  const base = [
    0.83, 0.82, 0.84, 0.83, 0.85, 0.84, 0.86, 0.85, 0.87, 0.86,
    0.87, 0.88, 0.87, 0.89, 0.88, 0.89, 0.90, 0.89, 0.90, 0.91,
    0.90, 0.91, 0.91, 0.92, 0.91, 0.92, 0.92, 0.93, 0.92, 0.91,
  ];
  return base.map((c, i) => ({
    day: `D-${30 - i}`,
    c: c,
    ltv: c >= 0.85 ? 70 : c >= 0.75 ? 60 : 0,
  }));
}

const HISTORY = generateHistory();

const MEMO = `MEMORANDUM
TO:      Office of the Chief Investment Officer
         GIC Private Limited / Temasek Digital Assets Division
FROM:    SNS Capital Architecture, Principal Office
DATE:    ${new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}
RE:      First-Loss Anchor Position — SNS Sovereign Intelligence Utility
         Ref: $32.2M Floor Tranche / ERC-1155 RWA Vault Tokens

EXECUTIVE POSITION

Singapore's sovereign capital faces a structural opacity problem in AI 
infrastructure deployment. When backing regional data centers and LLM 
clusters, there is currently no mechanism to audit the real-time 
intelligence quality of the advisory layer recommending those positions.

We have solved this. The Studio Nervous System (SNS) is the first 
intelligence infrastructure that makes its own confidence auditable 
on-chain in 24-hour oracle cycles — and then collatéralizes that 
confidence score as a borrowable asset.

THE OFFER

We are extending a first-loss anchor position in the SNS Credit Pool
to a single sovereign LP before the confidence roadmap pushes our
valuation ceiling from $69.6M to $103.5M.

  Tranche Size:     $32.2M USDC (60% LTV on $53.7M floor)
  Yield Structure:  80% of enterprise retainer sweep / qtr
  Risk Architecture: Dynamic LTV gate (C < 0.75 triggers circuit
                    breaker; C must hold ≥ 0.80 for 7 consecutive
                    days before capital drawdown resumes)
  Legal Wrapper:    SPV with IP assignment; fiat→USDC ACH via
                    Circle Programmable Wallets (48h routing SLA)

THE PROTECTION MECHANISM

Our circuit breaker protects your capital more aggressively than a 
conventional risk committee. It acts in 24 hours. Quarterly reviews 
cannot replicate this.

Three oracle feeds — Chainlink Functions, Pyth Network, and an internal 
ZK-proof audit log — must reach median consensus before any LTV 
adjustment executes. No single point of failure. No discretionary 
override.

STRATEGIC RATIONALE FOR GIC / TEMASEK

Singapore requires sovereign AI independence. The SNS provides an 
auditable, on-chain risk layer to deploy capital into regional compute 
infrastructure with verifiable intelligence provenance — not black-box 
advisor reports.

We are not offering an investment fund. We are offering a 
Sovereign Intelligence Utility with a contractual confidence floor.

NEXT STEP

A 30-minute live demonstration of the SNS War Room Dashboard and 
SNSCreditVault contract is available on request. No slide deck. 
Raw machine intelligence, on screen, in real time.

Contact: [Principal Office / Secure Channel]`;

// ── Custom Tooltip ───────────────────────────────────────────
function CTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  return (
    <div style={{ background: "#0a0a0a", border: "1px solid #c8a84b", padding: "8px 12px", fontFamily: "monospace", fontSize: 11 }}>
      <div style={{ color: "#c8a84b" }}>{label}</div>
      <div style={{ color: "#fff" }}>C = {d.c.toFixed(2)}</div>
      <div style={{ color: d.ltv === 70 ? "#c8a84b" : d.ltv === 60 ? "#888" : "#ff4444" }}>
        LTV {d.ltv}%
      </div>
    </div>
  );
}

// ── Main Component ───────────────────────────────────────────
export default function SNSWarRoom() {
  const [tick, setTick] = useState(0);
  const [view, setView] = useState("dashboard"); // dashboard | memo
  const [memoTyped, setMemoTyped] = useState("");
  const memoRef = useRef(null);

  // Live clock tick
  useEffect(() => {
    const id = setInterval(() => setTick(t => t + 1), 1000);
    return () => clearInterval(id);
  }, []);

  // Typewriter for memo
  useEffect(() => {
    if (view !== "memo") return;
    setMemoTyped("");
    let i = 0;
    const id = setInterval(() => {
      setMemoTyped(MEMO.slice(0, i));
      i += 4;
      if (i > MEMO.length) clearInterval(id);
    }, 12);
    return () => clearInterval(id);
  }, [view]);

  const vault = {
    c: 91,
    oracles: { chainlink: true, pyth: true, zk: true },
    broken: false,
    borrowCap: 48.7,
    floor: 53.7,
    ceiling: 86.4,
    ltv: 70,
    usdc: 34.1,
    yield: 2.3,
    brief: { id: "047", nodes: 14, knowns: 8, unknowns: 3 },
  };

  const now = new Date();
  const timeStr = now.toISOString().substring(11, 19) + " UTC";

  const gold = "#c8a84b";
  const dark = "#0a0a0a";
  const mono = "'Courier New', 'Lucida Console', monospace";

  const panel = {
    border: `1px solid ${gold}`,
    padding: "20px",
    background: dark,
    display: "flex",
    flexDirection: "column",
    gap: 12,
  };

  const label = { fontSize: 9, letterSpacing: "0.15em", color: gold, textTransform: "uppercase" };
  const value = { fontSize: 13, color: "#fff", fontWeight: "bold" };
  const row = { display: "flex", justifyContent: "space-between", alignItems: "center" };
  const divider = { borderTop: `1px solid #222`, paddingTop: 10, marginTop: 4 };

  return (
    <div style={{ minHeight: "100vh", background: "#050505", color: gold, fontFamily: mono, padding: "16px", boxSizing: "border-box" }}>

      {/* ── Top Bar ── */}
      <div style={{ border: `1px solid ${gold}`, padding: "10px 16px", marginBottom: 16, display: "flex", justifyContent: "space-between", alignItems: "center", fontSize: 9, letterSpacing: "0.18em" }}>
        <span>SNS // CORE_ENGINE_V3 // ATTESTATION_VAULT_ACTIVE</span>
        <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
          <span style={{ color: "#4ade80", animation: "pulse 2s infinite" }}>● OPERATIONAL</span>
          <span>{timeStr}</span>
          <button
            onClick={() => setView(view === "dashboard" ? "memo" : "dashboard")}
            style={{ background: "transparent", border: `1px solid ${gold}`, color: gold, fontFamily: mono, fontSize: 9, letterSpacing: "0.15em", padding: "4px 10px", cursor: "pointer" }}
          >
            {view === "dashboard" ? "VIEW MEMO →" : "← DASHBOARD"}
          </button>
        </div>
      </div>

      {view === "memo" ? (
        /* ── MEMO VIEW ── */
        <div style={{ border: `1px solid ${gold}`, padding: "28px 32px", minHeight: 500, background: dark }}>
          <div style={{ fontSize: 9, letterSpacing: "0.2em", color: gold, marginBottom: 20, borderBottom: `1px solid #222`, paddingBottom: 12 }}>
            OUTREACH MEMORANDUM // SOVEREIGN LP TARGET: GIC / TEMASEK
          </div>
          <pre style={{ fontFamily: mono, fontSize: 11, color: "#d4c28a", lineHeight: 1.85, whiteSpace: "pre-wrap", margin: 0 }}>
            {memoTyped}<span style={{ animation: "blink 1s infinite", color: gold }}>█</span>
          </pre>
        </div>
      ) : (
        /* ── DASHBOARD VIEW ── */
        <>
          {/* 3-Panel Grid */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 16, marginBottom: 16 }}>

            {/* PANEL 1: CONFIDENCE PULSE */}
            <div style={panel}>
              <div style={{ ...row, borderBottom: `1px solid #222`, paddingBottom: 10 }}>
                <span style={label}>PANEL 1 // CONFIDENCE PULSE</span>
                <span style={{ ...label, color: "#555" }}>[24H ORACLE]</span>
              </div>
              <div style={{ fontSize: 42, fontWeight: 900, color: "#fff", letterSpacing: "-0.02em", lineHeight: 1 }}>
                C = 0.<span style={{ color: gold }}>{vault.c}</span>
              </div>
              {/* Bar */}
              <div style={{ background: "#111", border: `1px solid #333`, height: 10, overflow: "hidden" }}>
                <div style={{ background: gold, height: "100%", width: `${vault.c}%`, transition: "width 1s ease" }} />
              </div>
              <div style={{ ...row, ...divider }}>
                <span style={label}>TIER</span>
                <span style={{ ...value, color: gold }}>PREMIUM ACTIVE</span>
              </div>
              <div style={row}>
                <span style={label}>30-DAY Δ</span>
                <span style={value}>↑ +0.06 (L3 DEPLOYED)</span>
              </div>
              <div style={{ ...row, ...divider }}>
                <span style={label}>ORACLES</span>
                <span style={{ fontSize: 11, display: "flex", gap: 8 }}>
                  {[["CL", vault.oracles.chainlink], ["PYTH", vault.oracles.pyth], ["ZK", vault.oracles.zk]].map(([k, v]) => (
                    <span key={k} style={{ color: v ? "#4ade80" : "#ff4444" }}>{k} {v ? "✓" : "✗"}</span>
                  ))}
                </span>
              </div>
              <div style={{ ...row, borderTop: `1px solid ${gold}`, paddingTop: 12, marginTop: 4 }}>
                <span style={{ fontSize: 10, color: "#4ade80" }}>● CIRCUIT OPEN</span>
                <span style={value}>${vault.borrowCap}M CAPACITY</span>
              </div>
            </div>

            {/* PANEL 2: CAPITAL TOPOLOGY */}
            <div style={panel}>
              <div style={{ ...row, borderBottom: `1px solid #222`, paddingBottom: 10 }}>
                <span style={label}>PANEL 2 // CAPITAL TOPOLOGY</span>
                <span style={{ ...label, color: "#555" }}>[VAULT STATE]</span>
              </div>
              {[
                ["FLOOR ANCHOR", `$${vault.floor}M`, "#888"],
                ["CURRENT CEILING", `$${vault.ceiling}M`, "#fff"],
                ["ACTIVE LTV", `${vault.ltv}%`, gold],
              ].map(([k, v, c]) => (
                <div key={k} style={row}>
                  <span style={label}>{k}</span>
                  <span style={{ fontSize: 14, fontWeight: "bold", color: c }}>{v}</span>
                </div>
              ))}
              <div style={divider}>
                {/* Capital bar */}
                <div style={{ ...row, marginBottom: 6 }}>
                  <span style={label}>USDC DEPLOYED</span>
                  <span style={value}>${vault.usdc}M</span>
                </div>
                <div style={{ background: "#111", border: `1px solid #333`, height: 6, overflow: "hidden" }}>
                  <div style={{ background: gold, height: "100%", width: `${(vault.usdc / vault.borrowCap) * 100}%` }} />
                </div>
                <div style={{ fontSize: 9, color: "#555", marginTop: 4, textAlign: "right" }}>
                  {((vault.usdc / vault.borrowCap) * 100).toFixed(0)}% OF CAPACITY DEPLOYED
                </div>
              </div>
              <div style={{ ...row, borderTop: `1px solid ${gold}`, paddingTop: 12, marginTop: 4 }}>
                <span style={{ fontSize: 10, color: "#888" }}>3 SOVEREIGN LPs</span>
                <span style={value}>YIELD ${vault.yield}M / QTR</span>
              </div>
            </div>

            {/* PANEL 3: COMMANDER BRIEF */}
            <div style={panel}>
              <div style={{ ...row, borderBottom: `1px solid #222`, paddingBottom: 10 }}>
                <span style={label}>PANEL 3 // COMMANDER BRIEF</span>
                <span style={{ ...label, color: "#555" }}>[INTELLIGENCE]</span>
              </div>
              <div style={{ fontSize: 18, color: "#fff", fontWeight: "bold" }}>BRIEF #{vault.brief.id}</div>
              <div style={{ fontSize: 10, color: "#555" }}>{vault.brief.nodes} NODES PROCESSED</div>
              {/* Knowns bar */}
              <div style={divider}>
                <div style={{ ...row, marginBottom: 4 }}>
                  <span style={label}>CONFIRMED KNOWNS ({vault.brief.knowns})</span>
                </div>
                <div style={{ background: "#111", border: `1px solid #333`, height: 6, overflow: "hidden" }}>
                  <div style={{ background: gold, height: "100%", width: `${(vault.brief.knowns / vault.brief.nodes) * 100}%` }} />
                </div>
              </div>
              {/* Unknowns bar */}
              <div>
                <div style={{ ...row, marginBottom: 4 }}>
                  <span style={label}>DIVERGENT UNKNOWNS ({vault.brief.unknowns})</span>
                </div>
                <div style={{ background: "#111", border: `1px solid #333`, height: 6, overflow: "hidden" }}>
                  <div style={{ background: "#444", height: "100%", width: `${(vault.brief.unknowns / vault.brief.nodes) * 100}%` }} />
                </div>
              </div>
              <div style={{ fontSize: 9, color: "#555", lineHeight: 1.7, marginTop: 4 }}>
                // REFLEX: L2 contradiction checker resolved 2 conflicts auto.<br />
                // LEVER 3 consensus delta: +0.04 on 6 signals.
              </div>
              <div style={{ ...row, borderTop: `1px solid ${gold}`, paddingTop: 12, marginTop: 4 }}>
                <span style={{ fontSize: 10, color: "#4ade80" }}>ACTION WINDOW: OPEN</span>
                <span style={value}>72H VALID</span>
              </div>
            </div>
          </div>

          {/* ── Confidence Chart ── */}
          <div style={{ border: `1px solid ${gold}`, padding: "20px", background: dark }}>
            <div style={{ ...row, marginBottom: 16, borderBottom: `1px solid #222`, paddingBottom: 12 }}>
              <span style={label}>30-DAY CONFIDENCE MOVING AVERAGE // ORACLE CONSENSUS FEED</span>
              <div style={{ display: "flex", gap: 16, fontSize: 9, color: "#555" }}>
                <span style={{ color: gold }}>─ C SCORE</span>
                <span style={{ color: "#ff4444" }}>── CIRCUIT THRESHOLD (0.75)</span>
                <span style={{ color: "#4ade80" }}>── FLOOR THRESHOLD (0.85)</span>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={160}>
              <LineChart data={HISTORY} margin={{ top: 4, right: 8, left: 0, bottom: 0 }}>
                <XAxis dataKey="day" tick={{ fill: "#444", fontSize: 8, fontFamily: mono }} tickLine={false} axisLine={{ stroke: "#222" }} interval={4} />
                <YAxis domain={[0.70, 0.97]} tick={{ fill: "#444", fontSize: 8, fontFamily: mono }} tickLine={false} axisLine={{ stroke: "#222" }} tickFormatter={v => v.toFixed(2)} width={36} />
                <Tooltip content={<CTooltip />} />
                <ReferenceLine y={0.75} stroke="#ff4444" strokeDasharray="4 3" strokeWidth={1} />
                <ReferenceLine y={0.85} stroke="#4ade80" strokeDasharray="4 3" strokeWidth={1} />
                <Line type="monotone" dataKey="c" stroke={gold} strokeWidth={2} dot={false} activeDot={{ r: 4, fill: gold, stroke: dark }} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Footer */}
          <div style={{ border: `1px solid #222`, padding: "10px 16px", marginTop: 16, fontSize: 9, color: "#333", letterSpacing: "0.15em" }}>
            &gt;&gt; SPV_TREASURY_HANDSHAKE: ACTIVE // ACH ROUTING: CIRCLE_PROGRAMMABLE_WALLETS // NEXT_SWEEP: T+48H
          </div>
        </>
      )}

      <style>{`
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
        @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
        * { box-sizing: border-box; }
      `}</style>
    </div>
  );
}
