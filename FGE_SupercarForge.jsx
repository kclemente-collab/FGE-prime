import { useState, useCallback } from "react";

const ARCHETYPES = [
  { id: "predator", name: "Fluid Predator", desc: "Continuous curvature, organic threat, satin silver" },
  { id: "kintsugi", name: "Kintsugi Machine", desc: "Volcanic black, lava crack paint, broken luxury" },
  { id: "cyber", name: "Cyber Wireframe", desc: "Faceted geometry, neon seams, digital made physical" },
  { id: "apex", name: "Apex Concept", desc: "Pure aerodynamic sculpture, no compromise" },
];

const ENVIRONMENTS = [
  { id: "volcanic", name: "Volcanic Field", shader: "volcanic rock terrain, ash atmosphere, lava glow on ground, dramatic backlight" },
  { id: "studio", name: "Dark Studio", shader: "pure black studio, controlled reflections, ground plane mirror, no distraction" },
  { id: "grid", name: "Cyber Grid", shader: "neon wireframe grid environment, blue-pink light, reflective floor, digital world" },
  { id: "golden", name: "Golden Hour", shader: "desert golden hour, warm 3000K, long shadow, atmospheric dust" },
  { id: "night", name: "Night City", shader: "night city, neon reflections, wet asphalt, deep blue-black atmosphere" },
];

const PAINTS = [
  { id: "volcanic-black", name: "Volcanic Black", shader: "deep matte black with lava crack network, orange-red glow in fractures, kintsugi automotive paint, volcanic obsidian surface" },
  { id: "liquid-silver", name: "Liquid Silver", shader: "continuous satin silver metallic, flowing highlight across surface curvature, no harsh breaks, liquid metal quality" },
  { id: "cyber-black", name: "Cyber Black + Neon", shader: "faceted gloss black panels with neon edge illumination, blue-cyan seam glow, geometric surface treatment" },
  { id: "pearl-black", name: "Midnight Pearl", shader: "deep black pearlescent, green-blue iridescent shift, three-layer clear coat, angle-dependent color" },
  { id: "chrome", name: "Liquid Chrome", shader: "mirror chrome full body, 100% environment reflection, surface curves distort reflection, razor panel edges" },
  { id: "carbon", name: "Raw Carbon", shader: "exposed carbon fiber 2x2 twill weave, directional sheen, minimal clear coat, raw performance material" },
];

const sliderConfig = [
  { key: "aggression", label: "Aggression", lo: "Grand Tourer", hi: "Track Weapon", color: "#ff4444" },
  { key: "curvature", label: "Curvature", lo: "Faceted/Angular", hi: "Fluid/Organic", color: "#44aaff" },
  { key: "aero", label: "Aero Expression", lo: "Subtle Hints", hi: "Extreme Geometry", color: "#ffaa00" },
  { key: "stance", label: "Stance Width", lo: "Balanced", hi: "Dominant Wide", color: "#aa44ff" },
  { key: "gloss", label: "Gloss Intensity", lo: "Matte/Raw", hi: "Mirror/Liquid", color: "#44ffaa" },
];

function buildPrompt(sliders, archetype, environment, paint, custom) {
  const agg = sliders.aggression;
  const curv = sliders.curvature;
  const aero = sliders.aero;
  const stance = sliders.stance;
  const gloss = sliders.gloss;

  const arch = ARCHETYPES.find(a => a.id === archetype);
  const env = ENVIRONMENTS.find(e => e.id === environment);
  const pnt = PAINTS.find(p => p.id === paint);

  const rendererMode = agg >= 7
    ? "Think like V-Ray automotive exterior. Physical accuracy non-negotiable. Hero shot."
    : gloss >= 8
    ? "Think like OctaneRender 2026 spectral. GPU-accelerated. Vibrant chromatic accuracy."
    : "Think like Autodesk VRED. Real-time ray tracing. Complex material layers.";

  const formLanguage = curv >= 7
    ? "continuous flowing surface curvature, seamless panel transitions, organic body sculpture, every line inevitable"
    : curv >= 4
    ? "balanced curved and angular surfaces, controlled tension between flow and edge"
    : "faceted angular geometry, hard panel breaks, crystalline surface treatment";

  const aeroDetail = aero >= 8
    ? "extreme active aero elements, aggressive vents and channels, cut-through geometry, diffuser dominates rear"
    : aero >= 5
    ? "purposeful aerodynamic channels, integrated side intakes, rear diffuser visible, function-driven form"
    : "subtle aerodynamic hints, clean surface, minimal visual noise";

  const stanceDesc = stance >= 7
    ? "dramatically wide rear haunches, dominant fender flare, planted aggressive stance, rear overpowers front"
    : stance >= 4
    ? "balanced wide stance, assertive presence, proportion controlled"
    : "elegant balanced proportions, long and low, speed implied through length";

  const glossDesc = gloss >= 8
    ? "mirror-quality paint, environment fully reflected, surface reads as liquid, maximum reflective drama"
    : gloss >= 5
    ? "high gloss metallic, strong reflections tracking curvature, clear coat depth visible"
    : "satin to matte finish, absorbed light, surface reads as material not mirror";

  const camera = agg >= 7
    ? "3/4 front low angle, 28mm wide, ground level drama"
    : "3/4 front angle, 85mm compression, studio distance";

  const customBlock = custom ? `\n\nADDITIONAL: ${custom}` : "";

  return `${rendererMode}

CONCEPT: ${arch?.name} — ${arch?.desc}

FORM: ${formLanguage}
AERO: ${aeroDetail}
STANCE: ${stanceDesc}
SURFACE: ${glossDesc}

PAINT: ${pnt?.shader}

ENVIRONMENT: ${env?.shader}

LIGHTING: dramatic chiaroscuro, single dominant source, deep shadow, surface highlights track every curve, no flat zones

CAMERA: ${camera}, hyper-realistic, extreme detail, concept car quality, no branding, no text

RENDER QUALITY: physically based materials, 8K, path tracing, film grain subtle${customBlock}

SLIDERS: AGG:${agg} CURV:${curv} AERO:${aero} STANCE:${stance} GLOSS:${gloss}`;
}

const Slider = ({ config, value, onChange }) => (
  <div style={{ marginBottom: "20px" }}>
    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px", alignItems: "center" }}>
      <span style={{ fontSize: "11px", color: config.color, textTransform: "uppercase", letterSpacing: "0.15em", fontWeight: 700 }}>
        {config.label}
      </span>
      <span style={{ fontSize: "18px", fontWeight: 800, color: config.color, fontFamily: "monospace", minWidth: "28px", textAlign: "right" }}>
        {value}
      </span>
    </div>
    <div style={{ position: "relative", height: "4px", background: "rgba(255,255,255,0.08)", borderRadius: "2px" }}>
      <div style={{
        position: "absolute", left: 0, top: 0, height: "100%",
        width: `${value * 10}%`, background: config.color,
        borderRadius: "2px", transition: "width 0.1s ease",
        boxShadow: `0 0 8px ${config.color}66`,
      }} />
      <input type="range" min={0} max={10} value={value}
        onChange={e => onChange(config.key, parseInt(e.target.value))}
        style={{
          position: "absolute", inset: "-8px 0",
          opacity: 0, cursor: "pointer", width: "100%",
        }}
      />
    </div>
    <div style={{ display: "flex", justifyContent: "space-between", marginTop: "4px" }}>
      <span style={{ fontSize: "9px", color: "#333" }}>{config.lo}</span>
      <span style={{ fontSize: "9px", color: "#333" }}>{config.hi}</span>
    </div>
  </div>
);

export default function SupercarForge() {
  const [sliders, setSliders] = useState({ aggression: 7, curvature: 8, aero: 6, stance: 7, gloss: 9 });
  const [archetype, setArchetype] = useState("predator");
  const [environment, setEnvironment] = useState("volcanic");
  const [paint, setPaint] = useState("volcanic-black");
  const [custom, setCustom] = useState("");
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState("build");

  const updateSlider = useCallback((key, val) => {
    setSliders(prev => ({ ...prev, [key]: val }));
  }, []);

  const prompt = buildPrompt(sliders, archetype, environment, paint, custom);

  const copyPrompt = () => {
    navigator.clipboard.writeText(prompt);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const dominantColor = sliders.aggression >= 7 ? "#ff4444" : sliders.gloss >= 8 ? "#44ffaa" : "#44aaff";

  return (
    <div style={{
      minHeight: "100vh", background: "#060606",
      color: "#e0e0e0", fontFamily: "'Helvetica Neue', Arial, sans-serif",
    }}>
      {/* Header */}
      <div style={{
        padding: "20px 16px 0",
        borderBottom: "1px solid rgba(255,255,255,0.05)",
        background: "#080808",
        position: "sticky", top: 0, zIndex: 100,
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: "12px" }}>
          <div>
            <div style={{ fontSize: "9px", letterSpacing: "0.4em", color: "#333", textTransform: "uppercase" }}>
              FERAL GLOSS EMPIRE
            </div>
            <div style={{
              fontSize: "20px", fontWeight: 900, letterSpacing: "-0.03em",
              background: `linear-gradient(135deg, #fff 0%, ${dominantColor} 100%)`,
              WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
              transition: "all 0.5s ease",
            }}>
              Supercar Forge
            </div>
          </div>
          <div style={{
            fontSize: "9px", color: "#333", textAlign: "right",
            lineHeight: 1.8, textTransform: "uppercase", letterSpacing: "0.1em",
          }}>
            AGG {sliders.aggression} · CURV {sliders.curvature}<br />
            AERO {sliders.aero} · STANCE {sliders.stance} · GLOSS {sliders.gloss}
          </div>
        </div>
        <div style={{ display: "flex", gap: "0" }}>
          {["build", "prompt"].map(tab => (
            <button key={tab} onClick={() => setActiveTab(tab)} style={{
              padding: "8px 20px", fontSize: "10px",
              textTransform: "uppercase", letterSpacing: "0.15em",
              cursor: "pointer", border: "none",
              borderBottom: activeTab === tab ? `2px solid ${dominantColor}` : "2px solid transparent",
              background: "transparent",
              color: activeTab === tab ? "#fff" : "#444",
              transition: "all 0.2s",
            }}>{tab}</button>
          ))}
        </div>
      </div>

      {activeTab === "build" ? (
        <div style={{ padding: "16px", paddingBottom: "100px" }}>

          {/* Archetype */}
          <div style={{ marginBottom: "24px" }}>
            <div style={{ fontSize: "9px", color: "#333", textTransform: "uppercase", letterSpacing: "0.2em", marginBottom: "10px" }}>
              Design DNA
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "6px" }}>
              {ARCHETYPES.map(a => (
                <button key={a.id} onClick={() => setArchetype(a.id)} style={{
                  padding: "10px", borderRadius: "8px", cursor: "pointer", textAlign: "left",
                  border: archetype === a.id ? `1px solid ${dominantColor}` : "1px solid rgba(255,255,255,0.06)",
                  background: archetype === a.id ? `${dominantColor}11` : "rgba(255,255,255,0.02)",
                  transition: "all 0.2s",
                }}>
                  <div style={{ fontSize: "11px", fontWeight: 700, color: archetype === a.id ? dominantColor : "#ccc", marginBottom: "3px" }}>
                    {a.name}
                  </div>
                  <div style={{ fontSize: "9px", color: "#444", lineHeight: 1.4 }}>{a.desc}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Sliders */}
          <div style={{ marginBottom: "24px" }}>
            <div style={{ fontSize: "9px", color: "#333", textTransform: "uppercase", letterSpacing: "0.2em", marginBottom: "14px" }}>
              Design Variables
            </div>
            {sliderConfig.map(cfg => (
              <Slider key={cfg.key} config={cfg} value={sliders[cfg.key]} onChange={updateSlider} />
            ))}
          </div>

          {/* Paint */}
          <div style={{ marginBottom: "24px" }}>
            <div style={{ fontSize: "9px", color: "#333", textTransform: "uppercase", letterSpacing: "0.2em", marginBottom: "10px" }}>
              Paint Shader
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: "5px" }}>
              {PAINTS.map(p => (
                <button key={p.id} onClick={() => setPaint(p.id)} style={{
                  padding: "10px 12px", borderRadius: "7px", cursor: "pointer", textAlign: "left",
                  border: paint === p.id ? `1px solid ${dominantColor}` : "1px solid rgba(255,255,255,0.05)",
                  background: paint === p.id ? `${dominantColor}0d` : "transparent",
                  transition: "all 0.2s",
                }}>
                  <span style={{ fontSize: "11px", color: paint === p.id ? dominantColor : "#888", fontWeight: 600 }}>
                    {p.name}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Environment */}
          <div style={{ marginBottom: "24px" }}>
            <div style={{ fontSize: "9px", color: "#333", textTransform: "uppercase", letterSpacing: "0.2em", marginBottom: "10px" }}>
              Environment
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "5px" }}>
              {ENVIRONMENTS.map(e => (
                <button key={e.id} onClick={() => setEnvironment(e.id)} style={{
                  padding: "9px 10px", borderRadius: "7px", cursor: "pointer",
                  border: environment === e.id ? `1px solid ${dominantColor}` : "1px solid rgba(255,255,255,0.05)",
                  background: environment === e.id ? `${dominantColor}0d` : "transparent",
                  color: environment === e.id ? dominantColor : "#666",
                  fontSize: "10px", fontWeight: 600,
                  transition: "all 0.2s",
                }}>{e.name}</button>
              ))}
            </div>
          </div>

          {/* Custom */}
          <div style={{ marginBottom: "20px" }}>
            <div style={{ fontSize: "9px", color: "#333", textTransform: "uppercase", letterSpacing: "0.2em", marginBottom: "8px" }}>
              Additional Direction
            </div>
            <textarea
              value={custom}
              onChange={e => setCustom(e.target.value)}
              placeholder="Add anything extra — specific details, FGE character reference, unique element..."
              style={{
                width: "100%", padding: "10px 12px", borderRadius: "8px",
                background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)",
                color: "#ccc", fontSize: "12px", outline: "none",
                resize: "vertical", minHeight: "72px", lineHeight: "1.6",
                boxSizing: "border-box", fontFamily: "inherit",
              }}
            />
          </div>
        </div>
      ) : (
        <div style={{ padding: "16px", paddingBottom: "100px" }}>
          <div style={{
            padding: "14px", borderRadius: "10px",
            background: "rgba(255,255,255,0.02)",
            border: `1px solid ${dominantColor}22`,
            fontSize: "11px", color: "#888", lineHeight: "1.9",
            whiteSpace: "pre-wrap", fontFamily: "monospace",
          }}>
            {prompt}
          </div>
        </div>
      )}

      {/* Fixed Copy Button */}
      <div style={{
        position: "fixed", bottom: 0, left: 0, right: 0,
        padding: "12px 16px",
        background: "linear-gradient(transparent, #060606 40%)",
        paddingTop: "30px",
      }}>
        <button onClick={copyPrompt} style={{
          width: "100%", padding: "14px",
          borderRadius: "10px", cursor: "pointer",
          border: `1px solid ${dominantColor}66`,
          background: copied ? `${dominantColor}22` : `${dominantColor}11`,
          color: copied ? "#fff" : dominantColor,
          fontSize: "12px", fontWeight: 700,
          textTransform: "uppercase", letterSpacing: "0.2em",
          transition: "all 0.2s",
        }}>
          {copied ? "✓ Prompt Copied — Paste Into Grok" : "Copy Prompt → Grok"}
        </button>
      </div>
    </div>
  );
}
