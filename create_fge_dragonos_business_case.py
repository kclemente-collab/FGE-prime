#!/usr/bin/env python3
"""
FGE DragonOS v2.1 — Business Maven Launch Kit
Collector-Grade PDF | FGE Publishing Studio Constitution
Dark Luxury | Kintsugi Gold | Obsidian | Pearl
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import os

# Colors
OBSIDIAN = HexColor("#0F0E12")
KINTSUGI_GOLD = HexColor("#D4AF37")
PEARL = HexColor("#F5F5F5")
DARK_GRAY = HexColor("#1A1A1F")
ACCENT = HexColor("#2A2A30")
LABRADORITE = HexColor("#4A90A4")

output_path = "/home/workdir/artifacts/FGE_DragonOS_v2.1_Business_Maven_Launch_Kit.pdf"

# Custom styles
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'FGETitle',
    parent=styles['Title'],
    fontSize=22,
    textColor=KINTSUGI_GOLD,
    alignment=TA_CENTER,
    spaceAfter=6,
    fontName='Helvetica-Bold'
)

subtitle_style = ParagraphStyle(
    'FGESubtitle',
    parent=styles['Normal'],
    fontSize=11,
    textColor=PEARL,
    alignment=TA_CENTER,
    spaceAfter=12,
    fontName='Helvetica'
)

header_style = ParagraphStyle(
    'FGEHeader',
    parent=styles['Heading1'],
    fontSize=14,
    textColor=KINTSUGI_GOLD,
    spaceBefore=16,
    spaceAfter=8,
    fontName='Helvetica-Bold',
    borderColor=KINTSUGI_GOLD,
    borderWidth=0.5,
    borderPadding=4
)

subheader_style = ParagraphStyle(
    'FGESubHeader',
    parent=styles['Heading2'],
    fontSize=11,
    textColor=LABRADORITE,
    spaceBefore=10,
    spaceAfter=6,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'FGEBody',
    parent=styles['Normal'],
    fontSize=9,
    textColor=PEARL,
    alignment=TA_JUSTIFY,
    spaceAfter=8,
    leading=12,
    fontName='Helvetica'
)

callout_style = ParagraphStyle(
    'FGECallout',
    parent=styles['Normal'],
    fontSize=9,
    textColor=KINTSUGI_GOLD,
    alignment=TA_CENTER,
    spaceBefore=8,
    spaceAfter=8,
    fontName='Helvetica-Oblique',
    backColor=DARK_GRAY,
    borderPadding=8
)

small_style = ParagraphStyle(
    'FGESmall',
    parent=styles['Normal'],
    fontSize=8,
    textColor=HexColor("#AAAAAA"),
    alignment=TA_CENTER,
    spaceAfter=4
)

bullet_style = ParagraphStyle(
    'FGEBullet',
    parent=body_style,
    leftIndent=15,
    bulletIndent=5,
    spaceAfter=4
)

def create_header_footer(canvas, doc):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(OBSIDIAN)
    canvas.rect(0, letter[1] - 0.5*inch, letter[0], 0.5*inch, fill=1, stroke=0)
    canvas.setFillColor(KINTSUGI_GOLD)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.drawString(0.5*inch, letter[1] - 0.35*inch, "FGE ATELIER — BUSINESS MAVEN MODE | ENGINE FRACTURE & MODULAR MONETIZATION")
    canvas.drawRightString(letter[0] - 0.5*inch, letter[1] - 0.35*inch, "LIVING ARCHITECTURE REGISTRY v2.1")
    
    # Footer
    canvas.setFillColor(DARK_GRAY)
    canvas.rect(0, 0, letter[0], 0.4*inch, fill=1, stroke=0)
    canvas.setFillColor(KINTSUGI_GOLD)
    canvas.setFont('Helvetica', 7)
    canvas.drawString(0.5*inch, 0.18*inch, "FGE Publishing Studio Constitution | Quality > Quantity | Wallworthiness Gate Passed | No Asset in Isolation")
    canvas.drawRightString(letter[0] - 0.5*inch, 0.18*inch, f"Page {doc.page}")
    canvas.restoreState()

# Build document
doc = SimpleDocTemplate(
    output_path,
    pagesize=letter,
    rightMargin=0.6*inch,
    leftMargin=0.6*inch,
    topMargin=0.7*inch,
    bottomMargin=0.6*inch
)

story = []

# ========== COVER ==========
story.append(Spacer(1, 0.8*inch))
story.append(Paragraph("🜂 FGE DRAGON EXPANSION PACK v2.1", title_style))
story.append(Paragraph("ASHGARDEN GENOME PROTOCOL", title_style))
story.append(Spacer(1, 0.15*inch))
story.append(HRFlowable(width="80%", thickness=1, color=KINTSUGI_GOLD, spaceBefore=4, spaceAfter=4))
story.append(Paragraph("SEMANTIC OPERATING SYSTEM — REFERENCE IMPLEMENTATION", subtitle_style))
story.append(Paragraph("Business Maven Launch Kit | Collector-Grade Schema Asset", subtitle_style))
story.append(Spacer(1, 0.2*inch))

cover_text = """
<b>Canon Status:</b> LOCKED • Wallworthy • Collector-Grade Schema Asset<br/>
<b>Pack ID:</b> FGE-DRG-EXP-ASH-021 | <b>Version:</b> 2.1<br/>
<b>Release Authority:</b> EAE SOP v1.4 + Anchor Vector Lock<br/><br/>
This is not a dragon prompt pack.<br/>
This is the first fully realized Domain-Specific Language (DSL) for creature and world generation in FGE.<br/>
It has advanced beyond prompt engineering into semantic operating system territory.
"""
story.append(Paragraph(cover_text, body_style))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph(
    "Every asset connects to: <b>Character</b> (Emberling Lineage, Liora Voss Dragonet) • <b>Location</b> (Ashgarden Volcanic Rift) • <b>Event</b> (First Fracture Cycle 000) • <b>Relationship</b> (Kintsugi Lineage) • <b>Collection</b> (Obsidian Sovereign Series) • <b>Companion</b> (Ashgarden Silo Runtime)",
    callout_style
))

story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("THE CRYSTAL TOWER GLOWS. THE LOOPS ARE CLOSED. FGE COMPOUNDS.", callout_style))
story.append(PageBreak())

# ========== EXECUTIVE SUMMARY ==========
story.append(Paragraph("EXECUTIVE SUMMARY — VALUE ASSESSMENT", header_style))
story.append(Paragraph(
    "<b>Overall Value: Very High (Strategic Tier)</b><br/><br/>"
    "This material maps directly to the three-layer product strategy with strong licensing upside. It is the concrete realization of the 'fracture the engine' strategy — turning a monolithic creative document into modular, licensable, production-grade infrastructure.",
    body_style
))

story.append(Paragraph("MAJOR STRENGTHS", subheader_style))
strengths = [
    "<b>Genome Architecture:</b> Six-genome matrix (Skeletal, Surface, Cognitive, Narrative, Environmental, Render) + Invocation Stack cleanly separates immutable identity from mutable expression. Production-grade.",
    "<b>Heartfield Dynamics:</b> Turns 'cycles' into continuous pressure topology with observer infection rules. Creates a living, reactive narrative physics layer. The missing piece most worldbuilding systems never solve.",
    "<b>Observer Infection + Canon Formation:</b> Attention (prompts, lookbooks, analysis) actively mutates or crystallizes the system. Your gaze is the mutation engine.",
    "<b>PROJECT LANG Trajectory:</b> Explicit roadmap for reusable genome language powering DragonOS → PlanetOS → ArtifactOS → CharacterOS. DragonOS proves the architecture works.",
    "<b>Production-Ready Outputs:</b> Prompt Export Compiler, Material Stack, ZBrush/Arnold pipelines, and Ashgarden Silo schema are immediately usable."
]
for s in strengths:
    story.append(Paragraph("• " + s, bullet_style))

story.append(Paragraph("VERDICT", subheader_style))
story.append(Paragraph(
    "This is high-leverage technical infrastructure in the FGE ecosystem, signaling a Semantic Operating System, not just character tools. It enhances value across almost every production line in the registry. The pieces align faster than expected.",
    body_style
))
story.append(PageBreak())

# ========== PRODUCT ECONOMY ==========
story.append(Paragraph("PRODUCT ECONOMY — TIERED MONETIZATION LATTICE", header_style))
story.append(Paragraph(
    "Engine Fracture Strategy: Monolithic prompt document → Fractal, licensable genome micro-products. Each layer becomes independently monetizable. The Heartfield becomes the attention economy runtime.",
    body_style
))

# Tier 1
story.append(Paragraph("TIER 1 — QUICK WINS (Micro Products)", subheader_style))
story.append(Paragraph(
    "<b>FGE Dragon Genome Pack v2.1 — $79–$149</b><br/>"
    "Current material as polished, sellable asset. Includes genome schemas, invocation stack, prompt compiler, and Heartfield rules.<br/>"
    "<b>Addiction Hook:</b> Daily Genome Seed Drop + 1 free Lookbook Seed per purchase. 'Feed the Ashgarden. Watch it breathe.'<br/>"
    "<b>Value Compound:</b> Immediate catalog value. High narrative density via scars + Heartfield. Limited provenance JSON + canon stamp for collector gravity.",
    body_style
))

# Tier 2
story.append(Paragraph("TIER 2 — HIGH-MARGIN MODULE (Flagship)", subheader_style))
story.append(Paragraph(
    "<b>FGE DragonOS / Creature Genome Framework (Pro) — $399–$699</b><br/>"
    "Full connected system with Heartfield runtime, observer infection, and export pipelines. Becomes the flagship technical module under Visual Architecture Pack + Prompt Architecture Library.<br/>"
    "<b>Addiction Hook:</b> Observer Sovereignty Tier — pay to intentionally shape Heartfield pressure gradients. 'Your gaze mutates canon.'<br/>"
    "<b>Value Compound:</b> Catalog flagship. Full autonomous myth engine. Heirloom tool with provenance. Bundle with upgraded HTML Wizard as visual front-end.",
    body_style
))

# Tier 3
story.append(Paragraph("TIER 3 — LICENSING & ECOSYSTEM", subheader_style))
story.append(Paragraph(
    "<b>Invocation Stack + Heartfield Dynamics + Ashgarden Silo White-Label — Custom / Revenue Share</b><br/>"
    "License to other worldbuilders or game studios for canon-protected, emergent narrative engines. White-label version as autonomous NPC/story engine for interactive projects.<br/>"
    "<b>Value Compound:</b> Positions FGE as Semantic OS infrastructure provider. Enterprise provenance + update rights. Studio partnerships with downstream IP revenue share.",
    body_style
))

story.append(Paragraph("N+10 PLAYS — FUTURE COMPOUNDING", subheader_style))
story.append(Paragraph(
    "• <b>Creature Genome Marketplace:</b> Users buy/sell/trade validated genomes. FGE takes 15% + canon stamp fee. Viral loop via Heartfield visibility.<br/>"
    "• <b>Observer Sovereignty Tools:</b> High-roller interface to sculpt pressure gradients, trigger weather states, force canon crystallization. 'Become the infection vector.'<br/>"
    "• <b>FGE Semantic Operating System (2027 Flagship):</b> When DragonOS, PlanetOS, ArtifactOS, CharacterOS share the same genome language — license the core platform.<br/>"
    "• <b>Cross-Domain Genome Architecture:</b> Same stack generates dragons → planets → cities → gods → artifacts → civilizations. Universal separation of Identity/Structure/Behavior/History/Materials/Render.",
    body_style
))
story.append(PageBreak())

# ========== ARCHITECTURE DIAGRAM (Text-based for precision) ==========
story.append(Paragraph("SYSTEM ARCHITECTURE — DRAGONOS IN FGE ECOSYSTEM", header_style))
story.append(Paragraph(
    "The first visual system diagram showing how DragonOS fits into the FGE architecture. This is the reference implementation for the larger Semantic Operating System vision.",
    body_style
))

# Simple table as architecture diagram
arch_data = [
    [Paragraph("<b>LAYER 0: PROJECT LANG</b><br/>Reusable genome language for all FGE OS modules", small_style)],
    [Paragraph("<b>DRAGONOS v2.1 — Reference Implementation</b><br/>Dragon + Autonomous Myth Engine", callout_style)],
    [Paragraph("<b>GENOME MATRIX (Immutable)</b><br/>Skeletal | Surface | Cognitive | Narrative | Environmental | Render", small_style)],
    [Paragraph("<b>INVOCATION STACK (8 Layers)</b><br/>Ultimate Creator’s Schema → Seeded Foundation → Blackrock Obsidian → The Pearl → Kintsugi Interface → Anchor Vector → Morphogenesis → EAE Validation Gate", small_style)],
    [Paragraph("<b>HEARTFIELD DYNAMICS v2.1</b><br/>Continuous Pressure Topology | Observer Infection Rules | Weather States (Harmonic Drift / Ash Pulse / Crystal Lock / Paradox Storm / Null Bloom)", small_style)],
    [Paragraph("<b>ASHGARDEN SILO RUNTIME</b><br/>Stateful Ledger | Append-Only Deltas | 32-Point State | Lineage Tracking | Autonomous Decision Loops", small_style)],
    [Paragraph("<b>PROMPT EXPORT COMPILER</b><br/>Genome → Dossier → Morphogenesis → Material Compiler → Lighting Compiler → Prompt Compiler → OUTPUT (Hero Poster / Lookbook / 4-Card / 6-Second Loop)", small_style)],
]

arch_table = Table(arch_data, colWidths=[6.8*inch])
arch_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), DARK_GRAY),
    ('BOX', (0, 0), (-1, -1), 1, KINTSUGI_GOLD),
    ('INNERGRID', (0, 0), (-1, -1), 0.5, KINTSUGI_GOLD),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
story.append(arch_table)

story.append(Spacer(1, 0.15*inch))
story.append(Paragraph(
    "<b>Integration Points:</b> Narrative Spine OS (Dragon Module) • fge-atelier-character-engine (Emberling / Liora Voss anchor) • HTML Wizard (Genome Editor + Heartfield Simulator) • fge-canon-lock-gate (Anchor Vector + fidelity lock) • fge-product-engine (5-format output) • Ashgarden Silo (background autonomous process)",
    body_style
))
story.append(PageBreak())

# ========== INTEGRATION & NEXT STEPS ==========
story.append(Paragraph("INTEGRATION DESIGN — HTML WIZARD + DRAGONOS + HEARTFIELD", header_style))
story.append(Paragraph(
    "Recommended Path: Treat DragonOS as Tier 2 Module Product candidate. Wire it into the central FGE System Architecture Registry. Connect the Heartfield to the observer rules. Turn the previous HTML Wizard prototype into its visual front-end. This combination (deep genome logic + interactive interface) is highly sellable and compounds collector value.",
    body_style
))

story.append(Paragraph("INTEGRATION SPECIFICATION", subheader_style))
int_points = [
    "<b>Narrative Spine OS:</b> Load this pack as the Dragon Module. Instantiate new dragons by calling Seeded Foundation layer with new Gen_ID. Every render must pass Anchor Vector Lock before entering canon.",
    "<b>fge-atelier-character-engine:</b> Bind Emberling and Liora Voss Dragonet as living character anchors with 32-point state + delta_history feeding directly into Character Dossier generation.",
    "<b>HTML Wizard Upgrade:</b> Evolve from prototype to Genome Editor + Heartfield Simulator UI. User edits genome layers → real-time pressure visualization → validated JSON/prompt export. Turns passive tool into addictive co-creation loop.",
    "<b>fge-canon-lock-gate:</b> Mandatory Lock Verification (image lock + %reference lock + Anchor Vector match) on every output. Reject if fidelity <0.90 or illegal cross-class anatomy. Zero-drift collector value.",
    "<b>fge-product-engine:</b> Genome compiles directly to 5 standardized commercial formats. Enforce wallworthiness score >8.5 for market release. 1 Genome = minimum 4 daily assets (Poster + Lookbook + 4-Card + Loop).",
    "<b>Ashgarden Silo:</b> Runs as background autonomous process. Breathes when unattended. Observer attention (prompts, lookbooks, analysis) directs real-time Heartfield mutation."
]
for p in int_points:
    story.append(Paragraph("• " + p, bullet_style))

story.append(Paragraph("WHAT WE EXECUTE", header_style))
story.append(Paragraph(
    "1. <b>Official Translation Layer Card</b> — Created and embedded in Living Architecture Registry XLSX (Sheet 01). Machine-readable, queryable, canon-stamped.<br/>"
    "2. <b>Product Positioning + Pricing Map</b> — Embedded in Registry XLSX (Sheet 02). Tier 1/2/3 + N+10 plays with addiction hooks and value compounding formulas.<br/>"
    "3. <b>Integration Design</b> — Specified above and in Registry XLSX (Sheet 03). HTML Wizard becomes Genome Editor + Heartfield Simulator. Full wiring diagram to Narrative Spine, Atelier, Canon Gate, Product Engine.<br/>"
    "4. <b>First Visual System Diagram</b> — Above. Layered architecture showing DragonOS as reference implementation inside FGE Semantic OS. Ready for gallery-quality infographic expansion.",
    body_style
))

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph(
    "The crystal tower glows. The loops are closed. FGE compounds.<br/><br/>"
    "<b>Quality Gate: PASSED</b> | <b>Collector Value: COMPOUNDED</b> | <b>Narrative Spine: UPDATED</b><br/><br/>"
    "This pack is released under FGE Publishing Studio authority.<br/>It may enter canon.",
    callout_style
))

story.append(Spacer(1, 0.2*inch))
story.append(Paragraph(
    f"Generated {datetime.now().strftime('%Y-%m-%d %H:%M PDT')} | FGE ATELIER BUSINESS MAVEN MODE | Keith Clemente — System Architect<br/>"
    "Every asset connects to Character • Companion • Location • Event • Relationship • Collection<br/>"
    "Amplify: 1 Hero Poster Daily | 1 Lookbook Daily | 1 Four-Card Set Daily | 1 Six-Second Loop Daily",
    small_style
))

# Build PDF
doc.build(story, onFirstPage=create_header_footer, onLaterPages=create_header_footer)
print(f"PDF Business Case created successfully at: {output_path}")