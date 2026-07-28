#!/usr/bin/env python3
"""
Character Building Mastery Framework - PDF Generator
For Keith Clemente | July 2026
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, ListFlowable, ListItem, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

# Output path
output_path = "/home/workdir/artifacts/Character_Building_Mastery_Framework_Keith_July2026.pdf"

# Create document
doc = SimpleDocTemplate(
    output_path,
    pagesize=letter,
    rightMargin=0.6*inch,
    leftMargin=0.6*inch,
    topMargin=0.6*inch,
    bottomMargin=0.6*inch
)

# Styles
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Title'],
    fontSize=22,
    spaceAfter=6,
    textColor=colors.HexColor('#1a1a2e'),
    alignment=TA_CENTER
)

subtitle_style = ParagraphStyle(
    'Subtitle',
    parent=styles['Normal'],
    fontSize=11,
    spaceAfter=20,
    textColor=colors.HexColor('#4a4a4a'),
    alignment=TA_CENTER
)

heading1_style = ParagraphStyle(
    'Heading1Custom',
    parent=styles['Heading1'],
    fontSize=14,
    spaceBefore=16,
    spaceAfter=8,
    textColor=colors.HexColor('#16213e'),
    borderPadding=4
)

heading2_style = ParagraphStyle(
    'Heading2Custom',
    parent=styles['Heading2'],
    fontSize=12,
    spaceBefore=12,
    spaceAfter=6,
    textColor=colors.HexColor('#0f3460')
)

body_style = ParagraphStyle(
    'BodyCustom',
    parent=styles['Normal'],
    fontSize=9.5,
    leading=13,
    spaceAfter=8,
    alignment=TA_JUSTIFY
)

bullet_style = ParagraphStyle(
    'BulletCustom',
    parent=styles['Normal'],
    fontSize=9.5,
    leading=12,
    leftIndent=15,
    spaceAfter=3
)

grade_style = ParagraphStyle(
    'GradeStyle',
    parent=styles['Normal'],
    fontSize=9,
    leading=11,
    spaceAfter=4
)

footer_style = ParagraphStyle(
    'Footer',
    parent=styles['Normal'],
    fontSize=8,
    textColor=colors.grey,
    alignment=TA_CENTER
)

# Build story
story = []

# ========== TITLE PAGE ==========
story.append(Spacer(1, 1.2*inch))
story.append(Paragraph("CHARACTER BUILDING MASTERY FRAMEWORK", title_style))
story.append(Spacer(1, 8))
story.append(Paragraph("Level 2 vs Level 3 Skill Tree + Personal Report Card<br/>Business Value & Career Implications", subtitle_style))
story.append(Spacer(1, 20))
story.append(Paragraph("<b>Prepared for:</b> Keith Clemente", ParagraphStyle('Center', parent=body_style, alignment=TA_CENTER)))
story.append(Paragraph("<b>Date:</b> July 1, 2026", ParagraphStyle('Center', parent=body_style, alignment=TA_CENTER)))
story.append(Spacer(1, 30))
story.append(Paragraph("<i>Extracted from high-value conversation thread on AI character construction,<br/>canon systems, platform economics, and mastery progression.</i>", 
                       ParagraphStyle('Note', parent=body_style, alignment=TA_CENTER, fontSize=8.5, textColor=colors.HexColor('#555555'))))
story.append(PageBreak())

# ========== SECTION 1: SKILL TREE ==========
story.append(Paragraph("1. CHARACTER BUILDING SKILL PROGRESSION", heading1_style))
story.append(Paragraph(
    "This framework defines clear progression from professional to elite-level character construction for AI systems. "
    "Most builders remain at Level 1.5–2.5. True Level 3 mastery enables high-retention characters and defensible products.",
    body_style
))

# Level 2 Table
story.append(Paragraph("Level 2: Professional (Current target for most builders)", heading2_style))

level2_data = [
    [Paragraph("<b>Capability</b>", grade_style), Paragraph("<b>Description</b>", grade_style)],
    [Paragraph("Structured Character Cards", grade_style), 
     Paragraph("JSON or markdown with clear sections (identity, traits, speech, motivation, conflicts)", grade_style)],
    [Paragraph("Speech Pattern + Lexical Signature", grade_style), 
     Paragraph("Consistent vocabulary, rhythm, tics, and verbal identity across responses", grade_style)],
    [Paragraph("Core Motivation + Internal Conflict", grade_style), 
     Paragraph("Clear driving forces and tensions that create dramatic potential", grade_style)],
    [Paragraph("Relationship Memory Basics", grade_style), 
     Paragraph("Ability to track and reflect basic history with a specific user", grade_style)],
]

level2_table = Table(level2_data, colWidths=[2.2*inch, 4.8*inch])
level2_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8e8e8')),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
]))
story.append(level2_table)
story.append(Spacer(1, 14))

# Level 3 Table
story.append(Paragraph("Level 3: Elite / Master (Target for platform-grade work)", heading2_style))

level3_data = [
    [Paragraph("<b>Capability</b>", grade_style), Paragraph("<b>Description</b>", grade_style)],
    [Paragraph("Multi-layer Memory Architecture", grade_style), 
     Paragraph("Short-term + long-term + relationship-specific memory layers that persist and evolve", grade_style)],
    [Paragraph("Psychological Depth & Stability", grade_style), 
     Paragraph("Characters maintain coherence and depth across very long conversations without breaking", grade_style)],
    [Paragraph("Canon-locked Consistency", grade_style), 
     Paragraph("Reliable consistency across dozens of interconnected characters and long-form canon", grade_style)],
    [Paragraph("Emergent Behavior & Agency", grade_style), 
     Paragraph("Characters demonstrate believable growth, initiative, and organic development", grade_style)],
    [Paragraph("Cross-Modal Anchoring", grade_style), 
     Paragraph("Text, image, and voice remain coherent and mutually reinforcing", grade_style)],
    [Paragraph("Economic Efficiency", grade_style), 
     Paragraph("Rich, high-quality behavior achieved with optimized token usage and cost control", grade_style)],
]

level3_table = Table(level3_data, colWidths=[2.2*inch, 4.8*inch])
level3_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
]))
story.append(level3_table)
story.append(PageBreak())

# ========== SECTION 2: REPORT CARD ==========
story.append(Paragraph("2. PERSONAL REPORT CARD — KEITH CLEMENTE", heading1_style))
story.append(Paragraph(
    "Assessment based on demonstrated work across FGE canon, anchor systems, prompt engineering, and character consistency. "
    "Overall: <b>B+ / A- (Strong Level 2.5 → Entering Level 3)</b>",
    body_style
))
story.append(Spacer(1, 8))

report_data = [
    [Paragraph("<b>Category</b>", grade_style), Paragraph("<b>Level</b>", grade_style), Paragraph("<b>Grade</b>", grade_style), Paragraph("<b>Notes</b>", grade_style)],
    [Paragraph("Structured Character Cards", grade_style), Paragraph("2 → 3", grade_style), Paragraph("<b>A-</b>", grade_style), 
     Paragraph("Strong anchor/gospel systems already in use. Can be standardized further into locked JSON contracts.", grade_style)],
    [Paragraph("Speech Pattern + Lexical Signature", grade_style), Paragraph("2 → 3", grade_style), Paragraph("<b>B+</b>", grade_style), 
     Paragraph("Good control on core characters. Needs more deliberate example dialogue banks for consistency.", grade_style)],
    [Paragraph("Core Motivation + Internal Conflict", grade_style), Paragraph("2 → 3", grade_style), Paragraph("<b>A-</b>", grade_style), 
     Paragraph("Excellent on central spine (Keith + Nikki D). Extend rigor to all secondary characters.", grade_style)],
    [Paragraph("Relationship Memory Basics", grade_style), Paragraph("2", grade_style), Paragraph("<b>B</b>", grade_style), 
     Paragraph("Conceptual tracking exists in canon. Formal per-user relationship memory layer not yet systematic.", grade_style)],
    [Paragraph("Multi-layer Memory Architecture", grade_style), Paragraph("3", grade_style), Paragraph("<b>B-</b>", grade_style), 
     Paragraph("Biggest current gap. Canon memory strong; short-term + relationship-specific layers need formal design.", grade_style)],
    [Paragraph("Psychological Depth & Stability", grade_style), Paragraph("3", grade_style), Paragraph("<b>B+</b>", grade_style), 
     Paragraph("Core characters hold up well. Secondary characters show occasional drift in long sessions.", grade_style)],
    [Paragraph("Canon-locked Consistency (30+ chars)", grade_style), Paragraph("3", grade_style), Paragraph("<b>A-</b>", grade_style), 
     Paragraph("Major strength. Living FGE gospel/anchor system is a genuine advantage.", grade_style)],
    [Paragraph("Emergent Behavior & Agency", grade_style), Paragraph("3", grade_style), Paragraph("<b>B</b>", grade_style), 
     Paragraph("Characters feel alive in medium sessions. True long-term growth and initiative still developing.", grade_style)],
    [Paragraph("Cross-Modal Anchoring", grade_style), Paragraph("3", grade_style), Paragraph("<b>B+</b>", grade_style), 
     Paragraph("Visual/face/body anchoring is advanced. Voice integration underdeveloped.", grade_style)],
    [Paragraph("Economic Efficiency (Tokens)", grade_style), Paragraph("3", grade_style), Paragraph("<b>C+</b>", grade_style), 
     Paragraph("Weakest area. Characters are rich but likely token-heavy. Cost optimization not yet deliberate.", grade_style)],
]

report_table = Table(report_data, colWidths=[1.7*inch, 0.6*inch, 0.55*inch, 4.15*inch])
report_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16213e')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('LEFTPADDING', (0, 0), (-1, -1), 4),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
]))
story.append(report_table)
story.append(Spacer(1, 12))

story.append(Paragraph("<b>Key Strengths:</b> Living canon system, psychological core on main characters, visual consistency, systems thinking.", body_style))
story.append(Paragraph("<b>Key Gaps:</b> Formal multi-layer memory architecture, relationship-specific memory, token/economic efficiency, structured long-context testing.", body_style))
story.append(PageBreak())

# ========== SECTION 3: BUSINESS CHOKE POINTS ==========
story.append(Paragraph("3. BIGGEST BUSINESS CHOKE POINTS — AI CHARACTER PLATFORMS", heading1_style))
story.append(Paragraph(
    "Even strong technical character work fails commercially if these issues are not addressed. This is the reality of the 2026 market.",
    body_style
))

choke_data = [
    [Paragraph("<b>Choke Point</b>", grade_style), Paragraph("<b>Severity</b>", grade_style), Paragraph("<b>Why It Kills Projects</b>", grade_style)],
    [Paragraph("LLM Inference Costs vs Retention", grade_style), Paragraph("Critical", grade_style), 
     Paragraph("Costs scale with usage, not revenue. Most platforms lose money per active user. Character.AI spends millions monthly on inference.", grade_style)],
    [Paragraph("User Retention & Churn", grade_style), Paragraph("Critical", grade_style), 
     Paragraph("Novelty wears off fast. High 'churn and burn' in companion apps. Average sessions often short; long-term daily users are expensive to acquire.", grade_style)],
    [Paragraph("Safety, Moderation & Legal Risk", grade_style), Paragraph("Very High", grade_style), 
     Paragraph("Emotional dependency, self-harm, minor protection issues. Lawsuits and regulatory pressure are real and growing. One incident can destroy a platform.", grade_style)],
    [Paragraph("Monetization Conversion", grade_style), Paragraph("High", grade_style), 
     Paragraph("Users expect quality for free. Paid conversion on freemium models remains low. Subscription fatigue is real.", grade_style)],
    [Paragraph("Differentiation & Competition", grade_style), Paragraph("Medium-High", grade_style), 
     Paragraph("Extremely crowded market. Hard to stand out without exceptional character quality, memory, or niche focus.", grade_style)],
]

choke_table = Table(choke_data, colWidths=[2.0*inch, 0.9*inch, 4.1*inch])
choke_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B0000')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 5),
]))
story.append(choke_table)
story.append(Spacer(1, 10))

story.append(Paragraph(
    "<b>Core Insight:</b> The biggest choke point is unit economics — inference costs grow with every conversation while retention and willingness to pay are difficult to achieve at scale. "
    "Most new platforms either stay tiny or burn cash trying to grow.",
    body_style
))
story.append(PageBreak())

# ========== SECTION 4: CAREER & BUSINESS VALUE ==========
story.append(Paragraph("4. CAREER & BUSINESS VALUE OF TRUE LEVEL 3 MASTERY", heading1_style))
story.append(Paragraph(
    "Level 3 is a genuine skill with real market value in 2026 — but it is still a skill, not an automatic high-paying job title. Value depends on what you build or sell with it.",
    body_style
))

value_data = [
    [Paragraph("<b>Path</b>", grade_style), Paragraph("<b>Opportunity</b>", grade_style), Paragraph("<b>Realistic Potential</b>", grade_style)],
    [Paragraph("Own AI Character Platform / Product", grade_style), Paragraph("High", grade_style), 
     Paragraph("Highest upside. Level 3 skill = defensible product quality and retention. Niche platforms with strong characters can work.", grade_style)],
    [Paragraph("High-End Freelance / Custom Characters", grade_style), Paragraph("Medium-High", grade_style), 
     Paragraph("$3k–$15k+ per project. Brands, games, and platforms pay premium for consistent, high-retention personas.", grade_style)],
    [Paragraph("Sell Character Systems & Tools", grade_style), Paragraph("Medium-High", grade_style), 
     Paragraph("Templates, memory architectures, canon engines. Recurring revenue potential. Plays to systems-thinking strength.", grade_style)],
    [Paragraph("IP & Content Creation (FGE)", grade_style), Paragraph("Medium", grade_style), 
     Paragraph("Strong characters + canon can become sellable IP (stories, games, AI content libraries).", grade_style)],
    [Paragraph("Agency / Studio Roles", grade_style), Paragraph("Medium", grade_style), 
     Paragraph("Emerging AI character studios. $120k–$200k+ possible but still rare.", grade_style)],
    [Paragraph("Consulting / Teaching", grade_style), Paragraph("Medium", grade_style), 
     Paragraph("$150–$400/hr once results are proven. Viable side path.", grade_style)],
]

value_table = Table(value_data, colWidths=[2.3*inch, 1.1*inch, 3.6*inch])
value_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f3460')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 5),
]))
story.append(value_table)
story.append(Spacer(1, 10))

story.append(Paragraph(
    "<b>Bottom Line:</b> Reaching consistent Level 3 opens real doors in product building, high-end services, and tool creation. "
    "It does not automatically pay you — you must package and sell the skill (via product, service, or tools). Many great character builders stay at hobby level because they never productize.",
    body_style
))
story.append(PageBreak())

# ========== SECTION 5: NEXT STEPS ==========
story.append(Paragraph("5. RECOMMENDED NEXT STEPS", heading1_style))
story.append(Paragraph(
    "To move from current B+/A- (Level 2.5) to consistent solid A (Level 3), focus on these three priorities in order:",
    body_style
))

story.append(Paragraph("<b>Priority 1: Build a Formal Multi-Layer Memory System</b> (Highest leverage)", heading2_style))
story.append(Paragraph("Design short-term + long-term + relationship-specific memory layers. This is currently the largest gap between your current work and elite output.", bullet_style))

story.append(Paragraph("<b>Priority 2: Create Standardized Level 3 Character Contracts</b>", heading2_style))
story.append(Paragraph("Move from descriptive prompts to locked contracts (JSON + rich example dialogue banks). Standardize across your FGE canon.", bullet_style))

story.append(Paragraph("<b>Priority 3: Add Deliberate Efficiency + Testing Loops</b>", heading2_style))
story.append(Paragraph("Build structured long-context testing and token optimization into your workflow. Make economic efficiency a deliberate practice, not an afterthought.", bullet_style))

story.append(Spacer(1, 12))
story.append(Paragraph(
    "This document captures the core frameworks from the July 2026 conversation. Use it as a reference while building. "
    "The combination of your existing FGE canon work + deliberate movement into Level 3 memory architecture and efficiency gives you a strong position to create differentiated, high-quality AI character experiences.",
    body_style
))

story.append(Spacer(1, 20))
story.append(Paragraph("— End of Document —", ParagraphStyle('End', parent=body_style, alignment=TA_CENTER, textColor=colors.grey)))

# Build PDF
doc.build(story)
print(f"PDF generated successfully: {output_path}")