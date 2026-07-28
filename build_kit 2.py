# -*- coding: utf-8 -*-
"""
FGE LOOKBOOK KIT — RENDER ENGINE
Usage:  python3 build_kit.py book_lilith_noir.py
Reads a BOOK input file + its theme, renders print-ready 2:3 PDF.
SPINE is constant; THEME tokens drive all visual variance.
"""
import base64, os, sys, importlib.util
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter, PdfReader
import theme as T

ROMAN = ["i","ii","iii","iv","v","vi","vii","viii","ix","x","xi","xii","xiii",
         "xiv","xv","xvi","xvii","xviii","xix","xx","xxi","xxii","xxiii","xxiv"]

def load_book(path):
    spec = importlib.util.spec_from_file_location("book", path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.BOOK

def b64(d, path):
    with open(os.path.join(d, path), "rb") as f:
        ext = "png" if path.lower().endswith("png") else "jpeg"
        return f"data:image/{ext};base64," + base64.b64encode(f.read()).decode()

# ---------- frame (gold language constant; weight varies by theme) ----------
def frame_svg(w, h, th, weight):
    inset = 26
    sw_outer = 3 if weight == "ornate" else 1.4
    sw_inner = 1 if weight == "ornate" else 0.8
    inner = f'<rect x="{inset+8}" y="{inset+8}" width="{w-2*inset-16}" height="{h-2*inset-16}" fill="none" stroke="url(#g)" stroke-width="{sw_inner}" opacity="0.7"/>' if weight=="ornate" else ""
    corners = "".join(_corner(cx,cy,fx,fy,w,h,inset,weight)
                      for cx,cy,fx,fy in [(0,0,1,1),(1,0,-1,1),(0,1,1,-1),(1,1,-1,-1)])
    return f"""<svg class="frame" viewBox="0 0 {w} {h}" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{th['gold_hi']}"/><stop offset="0.5" stop-color="{th['gold']}"/>
<stop offset="1" stop-color="#7a5f28"/></linearGradient></defs>
<rect x="{inset}" y="{inset}" width="{w-2*inset}" height="{h-2*inset}" fill="none" stroke="url(#g)" stroke-width="{sw_outer}"/>
{inner}{corners}</svg>"""

def _corner(cx, cy, fx, fy, w, h, inset, weight):
    x = inset+10 if cx==0 else w-inset-10
    y = inset+10 if cy==0 else h-inset-10
    L = 70 if weight=="ornate" else 46
    flour = (f'<path d="M14,14 q26,2 40,40" fill="none" stroke="url(#g)" stroke-width="1.4" opacity="0.85"/>'
             f'<path d="M-2,-2 l-10,-10 l4,14 l14,4 z" fill="url(#g)" opacity="0.9"/>') if weight=="ornate" else ""
    return f"""<g transform="translate({x},{y}) scale({fx},{fy})">
<path d="M0,0 L{L},0 M0,0 L0,{L}" stroke="url(#g)" stroke-width="{3 if weight=='ornate' else 1.6}"/>
{flour}<circle cx="0" cy="0" r="{5 if weight=='ornate' else 3}" fill="url(#g)"/></g>"""

def base_css(th):
    return f"""
@import url('{T.SPINE['google_fonts']}');
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'{T.SPINE['body_font']}',serif;color:{th['text']};background:{th['ink']};}}
.page{{width:{{W}}px;height:{{H}}px;position:relative;overflow:hidden;background:{th['paper']};}}
.frame{{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:5;}}
.surface{{position:absolute;inset:0;z-index:0;background:{th['surface']};}}
.wm{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
   font-family:'{T.SPINE['display_font']}',serif;font-size:340px;font-weight:600;
   color:{th['gold']};opacity:{T.SPINE['watermark_opacity']};letter-spacing:8px;z-index:1;user-select:none;}}
.hdr,.ftr{{position:absolute;left:54px;right:54px;display:flex;justify-content:space-between;
   font-family:'{T.SPINE['body_font']}',serif;font-size:13px;letter-spacing:3px;text-transform:uppercase;
   color:{th['gold']};opacity:.78;z-index:6;}}
.hdr{{top:38px;}} .ftr{{bottom:38px;}}
.disp{{font-family:'{T.SPINE['display_font']}',serif;}}
"""

# ---------- plate placement varies by theme rhythm ----------
def plate_geometry(rhythm):
    # returns (img_css, caption_left, caption_right)
    if rhythm == "bleed":
        return ("position:absolute;inset:0;width:100%;height:100%;object-fit:cover;", 104, 104)
    if rhythm == "left":
        return ("position:absolute;top:108px;left:60px;width:620px;height:1284px;object-fit:cover;", 700, 60)
    # centered (default)
    return ("position:absolute;top:108px;left:80px;width:840px;height:1140px;object-fit:cover;", 104, 104)

# ---------- page builders ----------
def cover(bk, th, W, H, ad):
    return f"""<div class="page">
<img src="{b64(ad,bk['cover'])}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 35%;z-index:1;">
<div style="position:absolute;inset:0;z-index:2;background:linear-gradient(180deg,rgba(0,0,0,.55) 0%,rgba(0,0,0,0) 30%,rgba(0,0,0,.2) 70%,rgba(0,0,0,.7) 100%);"></div>
{frame_svg(W,H,th,th_frame(th))}
<div style="position:absolute;top:120px;left:0;right:0;text-align:center;z-index:6;">
<div style="font-size:16px;letter-spacing:9px;color:{th['gold']};opacity:.85;text-transform:uppercase;">{bk['collection']}</div>
<h1 class="disp" style="font-size:104px;font-weight:500;letter-spacing:6px;color:{th['gold_hi']};line-height:1;margin-top:14px;text-shadow:0 2px 30px rgba(0,0,0,.6);">{bk['subject']}</h1>
<div class="disp" style="font-size:30px;font-style:italic;color:{th['text']};opacity:.9;margin-top:8px;letter-spacing:2px;">{bk['subtitle']}</div></div>
<div style="position:absolute;bottom:96px;left:0;right:0;text-align:center;z-index:6;">
<div style="font-size:13px;letter-spacing:5px;color:{th['gold']};text-transform:uppercase;">{T.SPINE['empire']}</div>
<div style="font-size:12px;letter-spacing:3px;color:{th['text']};opacity:.75;margin-top:6px;">{bk['edition']} · {T.SPINE['series']}</div></div></div>"""

def th_frame(th):  # frame weight token
    return th["frame"]

def intro(bk, th, W, H):
    body = "".join(f"<p style='margin-bottom:16px;'>{p}</p>" for p in bk["intro_body"])
    stats = "".join(
        f"<div style='display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid {th['gold']}40;'>"
        f"<span style='font-size:13px;letter-spacing:2px;text-transform:uppercase;color:{th['gold']};opacity:.8;'>{k}</span>"
        f"<span class='disp' style='font-size:17px;color:{th['text']};'>{v}</span></div>" for k,v in bk["intro_stats"])
    return f"""<div class="page"><div class="surface"></div><div class="wm">{T.SPINE['watermark_text']}</div>
{frame_svg(W,H,th,th_frame(th))}
<div style="position:absolute;top:150px;left:80px;right:80px;z-index:6;">
<div style="font-size:14px;letter-spacing:7px;color:{th['gold']};text-transform:uppercase;opacity:.85;">{bk['intro_eyebrow']}</div>
<h2 class="disp" style="font-size:62px;font-weight:500;color:{th['gold_hi']};margin-top:8px;line-height:1.02;">{bk['intro_heading']}</h2>
<div style="width:70px;height:2px;background:{th['gold']};margin:26px 0 30px;"></div>
<div class="disp" style="font-size:21px;font-style:italic;line-height:1.55;color:{th['text']};max-width:620px;">{body}</div>
<div style="margin-top:44px;max-width:520px;">{stats}</div></div>
<div class="ftr"><span>{T.SPINE['empire']}</span><span>ii</span><span>{T.SPINE['series']}</span></div></div>"""

def plate(p, bk, th, W, H, ad, pageno):
    img_css, cl, cr = plate_geometry(th["rhythm"])
    overlay_on = th["rhythm"] != "left"
    overlay = (f'<div style="position:absolute;top:108px;left:80px;width:840px;height:1140px;z-index:3;pointer-events:none;'
               f'border:1px solid {th["gold"]}55;background:linear-gradient(180deg,rgba(0,0,0,0) 62%,{th["ink"]}d0 100%);"></div>'
               if th["rhythm"]=="centered" else
               (f'<div style="position:absolute;inset:0;z-index:3;pointer-events:none;background:linear-gradient(180deg,rgba(0,0,0,.2) 0%,rgba(0,0,0,0) 40%,{th["ink"]}e0 100%);"></div>' if th["rhythm"]=="bleed" else ""))
    cap_bottom = 150 if th["rhythm"]!="left" else 0
    cap_style = (f"position:absolute;left:{cl}px;right:{cr}px;bottom:{cap_bottom}px;z-index:4;"
                 if th["rhythm"]!="left"
                 else f"position:absolute;left:{cl}px;right:{cr}px;top:50%;transform:translateY(-50%);z-index:4;")
    return f"""<div class="page"><div class="surface"></div>
<div class="hdr"><span>{bk['char_id']}-P{pageno:02d}</span><span>{bk['edition'].replace('Edition ','Ed. ')}</span></div>
<img src="{b64(ad,p['image'])}" style="{img_css}z-index:2;box-shadow:0 10px 50px rgba(0,0,0,.5);">
{overlay}
<div style="{cap_style}">
<h3 class="disp" style="font-size:42px;font-weight:500;color:{th['gold_hi']};line-height:1;">{p['title']}</h3>
<p class="disp" style="font-size:21px;font-style:italic;color:{th['text']};margin-top:12px;max-width:680px;line-height:1.4;">{p['line']}</p>
<div style="margin-top:14px;font-size:12px;letter-spacing:3px;text-transform:uppercase;color:{th['gold']};opacity:.7;">
{p['archive']} · {bk['collection']} · {bk['classification']}</div></div>
<div class="wm" style="font-size:300px;">{T.SPINE['watermark_text']}</div>
<div class="ftr"><span>{T.SPINE['empire']}</span><span>{ROMAN[pageno-1]}</span><span>{T.SPINE['series']}</span></div></div>"""

def centerfold(bk, th, W2, H, ad):
    c = bk["centerfold_data"]
    cells = "".join(
        f"<div style='border-left:2px solid {th['gold']};padding-left:16px;'>"
        f"<div class='disp' style='font-size:24px;color:{th['gold_hi']};'>{t}</div>"
        f"<div style='font-size:14px;color:{th['text']};opacity:.85;max-width:180px;'>{d}</div></div>"
        for t,d in [c['left'],c['mid'],c['right']])
    return f"""<div class="page" style="width:{W2}px;background:{th['ink']};">
<img src="{b64(ad,bk['centerfold'])}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1;">
<div style="position:absolute;inset:0;z-index:2;background:linear-gradient(90deg,{th['ink']}c8 0%,{th['ink']}26 32%,transparent 50%,{th['ink']}1a 70%,{th['ink']}66 100%),linear-gradient(180deg,{th['ink']}66 0%,transparent 25%,{th['ink']}8c 100%);"></div>
<div style="position:absolute;top:0;bottom:0;left:50%;width:2px;transform:translateX(-1px);z-index:3;background:linear-gradient(180deg,transparent,rgba(0,0,0,.5),transparent);"></div>
{frame_svg(W2,H,th,th_frame(th))}
<div style="position:absolute;top:130px;left:90px;width:560px;z-index:6;">
<div style="font-size:14px;letter-spacing:7px;color:{th['gold']};text-transform:uppercase;">{bk['char_id']} · CENTERFOLD</div>
<h2 class="disp" style="font-size:72px;font-weight:500;color:{th['gold_hi']};line-height:1;margin-top:10px;">{c['title']}</h2>
<div style="width:80px;height:2px;background:{th['gold']};margin:24px 0;"></div>
<p class="disp" style="font-size:23px;font-style:italic;line-height:1.5;color:{th['text']};">{c['fragment']}</p></div>
<div style="position:absolute;bottom:120px;left:90px;right:90px;z-index:6;display:flex;gap:60px;">{cells}</div>
<div class="wm" style="font-size:420px;">{T.SPINE['watermark_text']}</div></div>"""

def colophon(bk, th, W, H, pageno):
    sys = "".join(f"<li style='margin:6px 0;'>{s}</li>" for s in ["ChatGPT (OpenAI)","Claude (Anthropic)","Grok / Imagine (xAI)"])
    return f"""<div class="page"><div class="surface"></div><div class="wm">{T.SPINE['watermark_text']}</div>
{frame_svg(W,H,th,th_frame(th))}
<div style="position:absolute;top:200px;left:90px;right:90px;z-index:6;">
<h2 class="disp" style="font-size:46px;font-weight:500;color:{th['gold_hi']};">AI Attribution / Colophon</h2>
<div style="width:60px;height:2px;background:{th['gold']};margin:22px 0 26px;"></div>
<p style="font-size:19px;line-height:1.5;max-width:600px;">This publication was developed through a human-directed artificial intelligence workflow.</p>
<div style="margin-top:30px;font-size:13px;letter-spacing:3px;text-transform:uppercase;color:{th['gold']};">Systems Utilized</div>
<ul style="list-style:none;font-size:18px;margin-top:10px;">{sys}</ul>
<p style="font-size:18px;line-height:1.5;max-width:600px;margin-top:30px;color:{th['text']};opacity:.9;">Editorial Direction, Curation, Brand Development, and Final Publishing Decisions: {T.SPINE['empire']}</p>
<p class="disp" style="font-size:24px;font-style:italic;color:{th['gold_hi']};margin-top:50px;">Every archive is a wager against forgetting.</p>
<p style="font-size:12px;letter-spacing:2px;color:{th['gold']};opacity:.6;margin-top:18px;">{bk['provenance']} · {bk['edition']}</p></div>
<div class="ftr"><span>{T.SPINE['empire']}</span><span>{ROMAN[pageno-1]}</span><span>{T.SPINE['series']}</span></div></div>"""

def full_bleed_hero(bk, th, W, H, ad):
    """Portrait centerpiece: single full-bleed page, no pillarbox. For when the
    hero image isn't a true landscape panoramic."""
    c = bk["centerfold_data"]
    cells = ''.join(f"<div style='border-left:2px solid {th['gold']};padding-left:14px;'><div class=\"disp\" style=\"font-size:22px;color:{th['gold_hi']};\">{t}</div><div style=\"font-size:13px;color:{th['text']};opacity:.85;max-width:170px;\">{d}</div></div>" for t,d in [c['left'],c['mid'],c['right']])
    return f"""<div class="page">
<img src="{b64(ad,bk['centerfold'])}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 22%;z-index:1;">
<div style="position:absolute;inset:0;z-index:2;background:linear-gradient(180deg,{th['ink']}b0 0%,transparent 28%,transparent 50%,{th['ink']}f2 100%);"></div>
{frame_svg(W,H,th,th_frame(th))}
<div style="position:absolute;top:110px;left:80px;right:80px;z-index:6;">
<div style="font-size:13px;letter-spacing:6px;color:{th['gold']};text-transform:uppercase;">{bk['char_id']} · CENTERPIECE</div>
<h2 class="disp" style="font-size:60px;font-weight:500;color:{th['gold_hi']};line-height:1;margin-top:8px;">{c['title']}</h2></div>
<div style="position:absolute;bottom:148px;left:80px;right:80px;z-index:6;">
<p class="disp" style="font-size:22px;font-style:italic;line-height:1.5;color:{th['text']};max-width:760px;">{c['fragment']}</p>
<div style="margin-top:24px;display:flex;gap:54px;">{cells}</div></div>
<div class="wm" style="font-size:300px;">{T.SPINE['watermark_text']}</div>
<div class="ftr"><span>{T.SPINE['empire']}</span><span>&#9733;</span><span>{T.SPINE['series']}</span></div></div>"""

def clean_plate(p, bk, th, W, H, ad, pageno):
    """Pre-composed image (artifact poster) full-bleed; only minimal furniture."""
    return f"""<div class="page">
<img src="{b64(ad,p['image'])}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1;">
{frame_svg(W,H,th,th_frame(th))}
<div class="ftr"><span>{T.SPINE['empire']}</span><span>{ROMAN[pageno-1]}</span><span>{T.SPINE['series']}</span></div></div>"""

def doc(css, inner, W, H):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css.replace('{W}',str(W)).replace('{H}',str(H))}</style></head><body>{inner}</body></html>"

def render(book_path):
    bk = load_book(book_path)
    th = T.get_theme(bk["theme"])
    W, H = T.SPINE["page_w"], T.SPINE["page_h"]; W2 = W*2
    ad = bk["assets_dir"]
    css = base_css(th)

    # assign archive ids to plates
    for i,p in enumerate(bk["plates"], start=2):
        p.setdefault("archive", f"ARC-{i:03d}")

    pages = [(cover(bk,th,W,H,ad), W, H), (intro(bk,th,W,H), W, H)]

    def make_plate(p, pageno):
        if p.get("clean"):
            return clean_plate(p, bk, th, W, H, ad, pageno)
        return plate(p, bk, th, W, H, ad, pageno)

    cf_mode = bk.get("centerfold_mode", "spread")  # "spread" (landscape) | "hero" (portrait)
    half = len(bk["plates"])//2
    for n,p in enumerate(bk["plates"][:half], start=1):
        pages.append((make_plate(p, n+2), W, H))
    if cf_mode == "hero":
        pages.append((full_bleed_hero(bk,th,W,H,ad), W, H))
    else:
        pages.append((centerfold(bk,th,W2,H,ad), W2, H))
    for n,p in enumerate(bk["plates"][half:], start=half+1):
        pages.append((make_plate(p, n+2), W, H))
    pages.append((colophon(bk,th,W,H,len(bk["plates"])+3), W, H))

    out = bk.get("outfile", f"FGE_{bk['subject'].title().replace(' ','_')}_Lookbook.pdf")
    writer = PdfWriter()
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for idx,(frag,w,h) in enumerate(pages):
            pg = b.new_page(viewport={"width":w,"height":h})
            pg.set_content(doc(css,frag,w,h), wait_until="networkidle")
            pg.wait_for_timeout(800)
            fn = f"_kpg_{idx:02d}.pdf"
            pg.pdf(path=fn, print_background=True, width=f"{w}px", height=f"{h}px",
                   margin={"top":"0","bottom":"0","left":"0","right":"0"})
            pg.close(); writer.append(PdfReader(fn))
        b.close()
    with open(out,"wb") as f: writer.write(f)
    for fn in os.listdir("."):
        if fn.startswith("_kpg_"): os.remove(fn)
    print(f"rendered {len(pages)} pages -> {out}  (theme: {bk['theme']})")
    return out

if __name__ == "__main__":
    render(sys.argv[1] if len(sys.argv)>1 else "book_TEMPLATE.py")
