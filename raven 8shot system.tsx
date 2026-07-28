import { useState } from "react";

const SEED_CONSTANTS = {
  character: "Raven Voss",
  anchors: ["Black panther with electric blue eyes", "Fur coat over black leather mini dress", "Mirror-box environment / smoke atmosphere", "Dramatic single-source warm backlight", "Reflections as compositional element"],
  colorDNA: { primary: "#0a0a0a", accent: "#1a6bff", warm: "#c8821a", skin: "#8B5E3C", fur: "#3d2b1a" }
};

const SHOTS = [
  {
    id: "S1",
    label: "SEED",
    name: "The Arrival",
    locked: true,
    category: "Establishing",
    frame: "Full Body — 3/4 Frontal",
    distance: "Medium-Long",
    light: "Single warm backlight + smoke diffusion",
    panther: "At heel, blue eyes forward",
    pose: "Walking toward camera, relaxed authority",
    environment: "Mirror box, full context",
    delta: "—",
    purpose: "Hero card / RC001 anchor",
    keyChange: null,
    color: "#c8821a"
  },
  {
    id: "S2",
    label: "n+1",
    name: "The Sovereign",
    locked: false,
    category: "Establishing",
    frame: "Full Body — Direct Frontal",
    distance: "Medium",
    light: "Split light: warm left / cool blue right",
    panther: "Seated beside her, facing camera",
    pose: "Standing still, arms loose, dead-eye stare",
    environment: "Mirror box — tighter crop, more reflections",
    delta: "Pose locks. Light splits. Panther sits.",
    purpose: "Power shot — dominance read",
    keyChange: "POSE: Walking → Stopped. LIGHT: Single → Split.",
    color: "#1a6bff"
  },
  {
    id: "S3",
    label: "n+2",
    name: "The Detail",
    locked: false,
    category: "Editorial",
    frame: "Waist-Up — 3/4",
    distance: "Medium Close",
    light: "Raking sidelight — fur texture emphasis",
    panther: "Out of frame",
    pose: "Coat lapel held open, slight chin tilt",
    environment: "Smoke only, no mirror context needed",
    delta: "Crop rises. Panther exits. Fur becomes hero.",
    purpose: "Fashion editorial — product emphasis",
    keyChange: "FRAME: Full body → Waist up. PANTHER: Present → Absent.",
    color: "#6b3fa0"
  },
  {
    id: "S4",
    label: "n+3",
    name: "The Gaze",
    locked: false,
    category: "Portrait",
    frame: "Bust / Head & Shoulders",
    distance: "Close",
    light: "Beauty dish — face forward, minimal fill",
    panther: "Partially visible — snout at frame bottom",
    pose: "Direct eye contact, slight smirk",
    environment: "Pure smoke, near black",
    delta: "Frame collapses to face. One expression sells everything.",
    purpose: "Character study — identity shot",
    keyChange: "FRAME: Waist → Bust. ENVIRONMENT: Context → Void.",
    color: "#8B5E3C"
  },
  {
    id: "S5",
    label: "n+4",
    name: "The Bond",
    locked: false,
    category: "Relationship",
    frame: "Medium — Low angle, 3/4",
    distance: "Medium",
    light: "Cool blue dominant — panther eyes as practical light source",
    panther: "Standing, looking up at her face",
    pose: "Looking down at panther, soft expression",
    environment: "Mirror floor reflection prominent",
    delta: "Eye line breaks fourth wall — looks at panther. Emotional register shifts.",
    purpose: "Narrative — the relationship between them",
    keyChange: "GAZE: Camera → Panther. LIGHT: Warm → Cool.",
    color: "#0d4a8a"
  },
  {
    id: "S6",
    label: "n+5",
    name: "The Turn",
    locked: false,
    category: "Editorial",
    frame: "Full Body — 3/4 Rear",
    distance: "Medium-Long",
    light: "Front-fill rim on coat edges, backlight from behind camera",
    panther: "Walking beside, same direction",
    pose: "Mid-turn, glancing back over shoulder",
    environment: "Mirror box — reflections show front face",
    delta: "Subject turns away. Mirror reveals what the pose hides.",
    purpose: "Mystery / fashion — coat back + mirror reveal",
    keyChange: "ORIENTATION: Toward camera → Away. MIRRORS: Context → Active storytelling device.",
    color: "#2a4a2a"
  },
  {
    id: "S7",
    label: "n+6",
    name: "The Crouch",
    locked: false,
    category: "Dynamic",
    frame: "Medium — Low Camera, Eye Level with Panther",
    distance: "Medium Close",
    light: "Panther eyes illuminate her face from below",
    panther: "Crouching, chest low, primal",
    pose: "Crouched beside panther, one hand on its back",
    environment: "Smoke heavy, environment dissolved",
    delta: "Camera drops. Scale inverts. She meets the animal at its level.",
    purpose: "Power shift — she descends into its register",
    keyChange: "CAMERA HEIGHT: Eye → Low. POSE: Standing → Crouching.",
    color: "#4a1a1a"
  },
  {
    id: "S8",
    label: "n+7",
    name: "The Exit",
    locked: false,
    category: "Cinematic",
    frame: "Full Body — Extreme Wide, Rear",
    distance: "Long",
    light: "Doorway / corridor light source ahead — silhouette",
    panther: "Walking beside at distance",
    pose: "Walking away, coat flowing",
    environment: "Mirror corridor — infinite recession",
    delta: "Everything reduces to silhouette. Identity dissolves into symbol.",
    purpose: "Closing card — the world they inhabit is vast",
    keyChange: "SCALE: Close → Extreme wide. EXPOSURE: Lit → Silhouette.",
    color: "#1a1a2e"
  }
];

const MODULAR_VARIABLES = [
  { axis: "FRAME", values: ["Extreme Wide", "Full Body", "Waist Up", "Bust", "Face"], icon: "⬚" },
  { axis: "ANGLE", values: ["Overhead", "Eye Level", "Low", "Extreme Low"], icon: "◈" },
  { axis: "ORIENTATION", values: ["Frontal", "3/4 Front", "Profile", "3/4 Rear", "Rear"], icon: "↻" },
  { axis: "LIGHT TEMP", values: ["Warm Gold", "Neutral", "Cool Blue", "Split"], icon: "◐" },
  { axis: "PANTHER ROLE", values: ["Absent", "Partial", "At Heel", "Beside", "Dominant"], icon: "◆" },
  { axis: "ENVIRONMENT", values: ["Void/Smoke", "Floor Reflect", "Mirror Box", "Corridor"], icon: "▣" },
  { axis: "GAZE", values: ["Camera", "Panther", "Away", "Down", "Silhouette"], icon: "◎" },
];

export default function App() {
  const [selected, setSelected] = useState("S1");
  const [view, setView] = useState("shots"); // shots | matrix | variables

  const selectedShot = SHOTS.find(s => s.id === selected);

  return (
    <div style={{
      background: "#070707",
      minHeight: "100vh",
      fontFamily: "'Courier New', monospace",
      color: "#e8e0d0",
      padding: "0",
      overflowX: "hidden"
    }}>
      {/* Header */}
      <div style={{
        borderBottom: "1px solid #2a2a2a",
        padding: "20px 28px 16px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "flex-end"
      }}>
        <div>
          <div style={{ fontSize: 9, letterSpacing: 4, color: "#666", marginBottom: 4 }}>FERAL GLOSS EMPIRE · PRODUCTION SYSTEM</div>
          <div style={{ fontSize: 22, letterSpacing: 2, color: "#fff", fontWeight: "normal" }}>RAVEN VOSS · 8-SHOT ARCHITECTURE</div>
        </div>
        <div style={{ fontSize: 9, color: "#444", letterSpacing: 2 }}>SB_330 · CANON v2.1</div>
      </div>

      {/* Nav */}
      <div style={{ display: "flex", borderBottom: "1px solid #1a1a1a", padding: "0 28px" }}>
        {[["shots", "SHOT MATRIX"], ["matrix", "DELTA MAP"], ["variables", "MODULAR AXES"]].map(([key, label]) => (
          <button key={key} onClick={() => setView(key)} style={{
            background: "none", border: "none", borderBottom: view === key ? "1px solid #c8821a" : "1px solid transparent",
            color: view === key ? "#c8821a" : "#555", fontSize: 9, letterSpacing: 3,
            padding: "12px 20px 11px", cursor: "pointer", marginBottom: -1
          }}>{label}</button>
        ))}
      </div>

      {/* SHOTS VIEW */}
      {view === "shots" && (
        <div style={{ display: "grid", gridTemplateColumns: "280px 1fr", height: "calc(100vh - 110px)" }}>
          {/* Left rail */}
          <div style={{ borderRight: "1px solid #1a1a1a", overflowY: "auto", padding: "8px 0" }}>
            {SHOTS.map(shot => (
              <div key={shot.id} onClick={() => setSelected(shot.id)} style={{
                padding: "12px 20px",
                cursor: "pointer",
                borderLeft: selected === shot.id ? `2px solid ${shot.color}` : "2px solid transparent",
                background: selected === shot.id ? "#0f0f0f" : "transparent",
                transition: "all 0.15s"
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 4 }}>
                  <span style={{ fontSize: 9, letterSpacing: 3, color: shot.color }}>{shot.label}</span>
                  <span style={{ fontSize: 8, letterSpacing: 2, color: "#333" }}>{shot.category.toUpperCase()}</span>
                </div>
                <div style={{ fontSize: 13, color: selected === shot.id ? "#fff" : "#888" }}>{shot.name}</div>
                <div style={{ fontSize: 9, color: "#444", marginTop: 3 }}>{shot.frame}</div>
              </div>
            ))}
          </div>

          {/* Detail panel */}
          {selectedShot && (
            <div style={{ padding: "32px 36px", overflowY: "auto" }}>
              <div style={{ display: "flex", alignItems: "baseline", gap: 16, marginBottom: 8 }}>
                <span style={{ fontSize: 11, letterSpacing: 4, color: selectedShot.color }}>{selectedShot.label}</span>
                {selectedShot.locked && <span style={{ fontSize: 8, letterSpacing: 2, color: "#c8821a", border: "1px solid #c8821a", padding: "2px 8px" }}>SEED · LOCKED</span>}
              </div>
              <div style={{ fontSize: 32, color: "#fff", fontWeight: "normal", letterSpacing: 1, marginBottom: 6 }}>{selectedShot.name}</div>
              <div style={{ fontSize: 11, color: "#555", letterSpacing: 3, marginBottom: 32 }}>{selectedShot.purpose}</div>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0 40px" }}>
                {[
                  ["FRAME", selectedShot.frame],
                  ["DISTANCE", selectedShot.distance],
                  ["LIGHT", selectedShot.light],
                  ["PANTHER", selectedShot.panther],
                  ["POSE", selectedShot.pose],
                  ["ENVIRONMENT", selectedShot.environment],
                ].map(([label, value]) => (
                  <div key={label} style={{ padding: "14px 0", borderBottom: "1px solid #151515" }}>
                    <div style={{ fontSize: 8, letterSpacing: 3, color: "#444", marginBottom: 5 }}>{label}</div>
                    <div style={{ fontSize: 13, color: "#ccc", lineHeight: 1.5 }}>{value}</div>
                  </div>
                ))}
              </div>

              {selectedShot.keyChange && (
                <div style={{ marginTop: 32, padding: "20px 24px", border: `1px solid ${selectedShot.color}22`, background: `${selectedShot.color}08` }}>
                  <div style={{ fontSize: 8, letterSpacing: 3, color: selectedShot.color, marginBottom: 10 }}>DELTA FROM SEED</div>
                  <div style={{ fontSize: 11, color: "#aaa", lineHeight: 2 }}>
                    {selectedShot.keyChange.split(". ").map((line, i) => (
                      <div key={i} style={{ marginBottom: 4 }}>→ {line}</div>
                    ))}
                  </div>
                </div>
              )}

              <div style={{ marginTop: 24, padding: "16px 24px", background: "#0d0d0d", borderLeft: `2px solid ${selectedShot.color}` }}>
                <div style={{ fontSize: 8, letterSpacing: 3, color: "#555", marginBottom: 8 }}>STRUCTURAL SHIFT NOTE</div>
                <div style={{ fontSize: 12, color: "#888", lineHeight: 1.7, fontStyle: "italic" }}>{selectedShot.delta}</div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* DELTA MAP VIEW */}
      {view === "matrix" && (
        <div style={{ padding: "32px 28px", overflowX: "auto" }}>
          <div style={{ fontSize: 9, letterSpacing: 3, color: "#555", marginBottom: 24 }}>EACH SHOT CHANGES EXACTLY 1–3 VARIABLES FROM SEED · ALL OTHER CONSTANTS LOCKED</div>
          <div style={{ display: "grid", gridTemplateColumns: `120px repeat(7, 1fr)`, gap: "1px", background: "#1a1a1a", fontSize: 9, minWidth: 900 }}>
            {/* Header */}
            <div style={{ background: "#070707", padding: "10px 12px", color: "#333" }}></div>
            {MODULAR_VARIABLES.map(v => (
              <div key={v.axis} style={{ background: "#0d0d0d", padding: "10px 8px", color: "#666", letterSpacing: 2, textAlign: "center" }}>
                <div style={{ fontSize: 14, marginBottom: 4 }}>{v.icon}</div>
                {v.axis}
              </div>
            ))}
            {/* Rows */}
            {SHOTS.map(shot => {
              const rowVals = {
                "FRAME": shot.frame.split("—")[0].trim(),
                "ANGLE": shot.frame.includes("Low") ? "Low" : shot.frame.includes("Overhead") ? "Overhead" : "Eye Level",
                "ORIENTATION": shot.frame.includes("Rear") ? "Rear/3/4 Rear" : shot.frame.includes("Front") ? "Frontal" : "3/4",
                "LIGHT TEMP": shot.light.includes("blue") || shot.light.includes("Cool") ? "Cool" : shot.light.includes("Split") ? "Split" : "Warm",
                "PANTHER ROLE": shot.panther.includes("Out") ? "Absent" : shot.panther.includes("Partial") ? "Partial" : shot.panther.includes("Beside") ? "Beside" : "At Heel",
                "ENVIRONMENT": shot.environment.includes("Mirror") ? "Mirror Box" : shot.environment.includes("Corridor") ? "Corridor" : "Void/Smoke",
                "GAZE": shot.pose.includes("camera") || shot.pose.includes("eye contact") ? "Camera" : shot.pose.includes("panther") ? "Panther" : shot.pose.includes("back") ? "Away" : shot.pose.includes("down") ? "Down" : "Away",
              };
              return (
                <><div key={shot.id + "l"} style={{ background: "#0a0a0a", padding: "10px 12px", borderLeft: `2px solid ${shot.color}` }}>
                  <div style={{ color: shot.color, marginBottom: 2 }}>{shot.label}</div>
                  <div style={{ color: "#777" }}>{shot.name}</div>
                </div>
                {MODULAR_VARIABLES.map(v => {
                  const val = rowVals[v.axis];
                  const isSeed = shot.id === "S1";
                  return (
                    <div key={v.axis} style={{
                      background: isSeed ? "#0f0f0a" : "#080808",
                      padding: "10px 8px",
                      color: isSeed ? "#c8821a" : "#666",
                      textAlign: "center",
                      fontSize: 9,
                      lineHeight: 1.4
                    }}>{val}</div>
                  );
                })}</>
              );
            })}
          </div>
        </div>
      )}

      {/* VARIABLES VIEW */}
      {view === "variables" && (
        <div style={{ padding: "32px 28px" }}>
          <div style={{ fontSize: 9, letterSpacing: 3, color: "#555", marginBottom: 32 }}>THE 7 MODULAR AXES · ALL OTHER CHARACTER CONSTANTS REMAIN LOCKED ACROSS ALL 8 SHOTS</div>
          
          {/* Seed constants */}
          <div style={{ marginBottom: 40, padding: "24px", border: "1px solid #1a1a1a" }}>
            <div style={{ fontSize: 9, letterSpacing: 3, color: "#c8821a", marginBottom: 16 }}>LOCKED CONSTANTS — NEVER CHANGE</div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
              {SEED_CONSTANTS.anchors.map(a => (
                <span key={a} style={{ fontSize: 10, color: "#777", border: "1px solid #222", padding: "6px 12px", letterSpacing: 1 }}>{a}</span>
              ))}
            </div>
          </div>

          {/* Axes */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
            {MODULAR_VARIABLES.map((v, i) => (
              <div key={v.axis} style={{ padding: "20px 24px", border: "1px solid #161616" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 14 }}>
                  <span style={{ fontSize: 20 }}>{v.icon}</span>
                  <div>
                    <div style={{ fontSize: 8, letterSpacing: 3, color: "#555" }}>AXIS {i + 1}</div>
                    <div style={{ fontSize: 13, color: "#fff", letterSpacing: 2 }}>{v.axis}</div>
                  </div>
                </div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                  {v.values.map(val => (
                    <span key={val} style={{ fontSize: 9, color: "#666", background: "#0d0d0d", padding: "4px 10px", letterSpacing: 1 }}>{val}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <div style={{ marginTop: 40, padding: "24px", background: "#0a0a0a", borderLeft: "2px solid #c8821a" }}>
            <div style={{ fontSize: 9, letterSpacing: 3, color: "#c8821a", marginBottom: 12 }}>THE MODULAR RULE</div>
            <div style={{ fontSize: 13, color: "#888", lineHeight: 2 }}>
              Each shot = Seed Constants + (1–3 axis changes only).<br/>
              Never change more than 3 axes per shot from the seed.<br/>
              Each axis change must serve a single, nameable purpose.<br/>
              If you cannot name why an axis changed — revert it.
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
