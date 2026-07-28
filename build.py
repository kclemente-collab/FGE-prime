# -*- coding: utf-8 -*-
"""
FGE Coffee Table Lookbook — BUILD / LAYOUT LAYER
Reads data.py, emits HTML, renders to print-ready PDF via Chromium.
Page: 2:3 portrait. Trim 10x15in. We render at 1000x1500 CSS px (multiply for DPI on print).
"""
import base64, os
from playwright.sync_api import sync_playwright
import data as D

ASSETS = "assets"
PAGE_W, PAGE_H = 1000, 1500          # 2:3 ratio CSS canvas
SPREAD_W = PAGE_W * 2                  # centerfold

def b64(path):
    with open(os.path.join(ASSETS, path), "rb") as f:
        ext = "png" if path.lower().endswith("png") else "jpeg"
        return f"data:image/{ext};base64," + base64.b64encode(f.read()).decode()

# ---------- shared style ----------
GOLD = "#c9a24b"
GOLD_HI = "#e7cf8f"
INK = "#0a0a0d"
PAPER = "#111016"

FONTS = """
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap');
"""

def gold_frame_svg(w, h):
    """Ornate corner frame in the Image-2 style, crisp vector."""
    inset = 26
    return f"""
<svg class="frame" viewBox="0 0 {w} {h}" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{GOLD_HI}"/><stop offset="0.5" stop-color="{GOLD}"/>
      <stop offset="1" stop-color="#8a6d2c"/>
    </linearGradient>
  </defs>
  <rect x="{inset}" y="{inset}" width="{w-2*inset}" height="{h-2*inset}" fill="none" stroke="url(#g)" stroke-width="3"/>
  <rect x="{inset+8}" y="{inset+8}" width="{w-2*inset-16}" height="{h-2*inset-16}" fill="none" stroke="url(#g)" stroke-width="1" opacity="0.7"/>
  {''.join(corner(x,y,fx,fy,w,h,inset) for x,y,fx,fy in [(0,0,1,1),(1,0,-1,1),(0,1,1,-1),(1,1,-1,-1)])}
</svg>"""

def corner(cx, cy, fx, fy, w, h, inset):
    x = inset+10 if cx==0 else w-inset-10
    y = inset+10 if cy==0 else h-inset-10
    L = 70
    return f"""
  <g transform="translate({x},{y}) scale({fx},{fy})">
    <path d="M0,0 L{L},0 M0,0 L0,{L}" stroke="url(#g)" stroke-width="3"/>
    <path d="M14,14 q26,2 40,40" fill="none" stroke="url(#g)" stroke-width="1.4" opacity="0.85"/>
    <circle cx="0" cy="0" r="5" fill="url(#g)"/>
    <path d="M-2,-2 l-10,-10 l4,14 l14,4 z" fill="url(#g)" opacity="0.9"/>
  </g>"""

WATERMARK = f"""<div class="wm">FGE</div>"""

BASE_CSS = f"""
{FONTS}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'EB Garamond',serif; color:#e8e3d8; background:{INK}; }}
.page {{ width:{PAGE_W}px; height:{PAGE_H}px; position:relative; overflow:hidden;
        background:{PAPER}; page-break-after:always; }}
.page:last-child {{ page-break-after:auto; }}
.spread {{ width:{SPREAD_W}px; height:{PAGE_H}px; position:relative; overflow:hidden;
          background:{INK}; page-break-after:always; }}
.frame {{ position:absolute; inset:0; width:100%; height:100%; pointer-events:none; z-index:5; }}
.wm {{ position:absolute; bottom:50%; left:50%; transform:translate(-50%,50%);
       font-family:'Cormorant Garamond',serif; font-size:340px; font-weight:600;
       color:{GOLD}; opacity:0.05; letter-spacing:8px; z-index:1; user-select:none; }}
/* furniture */
.hdr,.ftr {{ position:absolute; left:54px; right:54px; display:flex; justify-content:space-between;
       font-family:'EB Garamond',serif; font-size:13px; letter-spacing:3px; text-transform:uppercase;
       color:{GOLD}; opacity:0.78; z-index:6; }}
.hdr {{ top:38px; }} .ftr {{ bottom:38px; }}
.ftr .pg {{ opacity:0.9; }}
.disp {{ font-family:'Cormorant Garamond',serif; }}
"""

# ---------- page builders ----------
def cover():
    c = D.COVER
    return f"""
<div class="page" style="background:#0c0c10;">
  <img src="{b64(c['image'])}" style="position:absolute;inset:0;width:100%;height:100%;
       object-fit:cover;object-position:center 35%;z-index:1;">
  <div style="position:absolute;inset:0;background:
       linear-gradient(180deg,rgba(8,8,11,.55) 0%,rgba(8,8,11,0) 30%,rgba(8,8,11,.2) 70%,rgba(8,8,11,.7) 100%);z-index:2;"></div>
  {gold_frame_svg(PAGE_W,PAGE_H)}
  <div style="position:absolute;top:120px;left:0;right:0;text-align:center;z-index:6;">
    <div style="font-size:16px;letter-spacing:9px;color:{GOLD};opacity:.85;text-transform:uppercase;">{c['collection']}</div>
    <h1 class="disp" style="font-size:104px;font-weight:500;letter-spacing:6px;color:{GOLD_HI};
        line-height:1;margin-top:14px;text-shadow:0 2px 30px rgba(0,0,0,.6);">{c['title']}</h1>
    <div class="disp" style="font-size:30px;font-style:italic;color:#efe9da;opacity:.9;margin-top:8px;letter-spacing:2px;">{c['subtitle']}</div>
  </div>
  <div style="position:absolute;bottom:96px;left:0;right:0;text-align:center;z-index:6;">
    <div style="font-size:13px;letter-spacing:5px;color:{GOLD};text-transform:uppercase;">{D.BRAND['empire']}</div>
    <div style="font-size:12px;letter-spacing:3px;color:#cfc8b8;opacity:.75;margin-top:6px;">{c['edition']} · {D.BRAND['series']}</div>
  </div>
</div>"""

def intro():
    i = D.INTRO
    stats = "".join(
        f"<div style='display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid rgba(201,162,75,.25);'>"
        f"<span style='font-size:13px;letter-spacing:2px;text-transform:uppercase;color:{GOLD};opacity:.8;'>{k}</span>"
        f"<span class='disp' style='font-size:17px;color:#efe9da;'>{v}</span></div>"
        for k,v in i['stats'])
    body = "".join(f"<p style='margin-bottom:16px;'>{p}</p>" for p in i['body'])
    return f"""
<div class="page" style="background:radial-gradient(120% 90% at 70% 20%,#1a1722 0%,{INK} 60%);">
  {WATERMARK}
  {gold_frame_svg(PAGE_W,PAGE_H)}
  <div style="position:absolute;top:150px;left:80px;right:80px;z-index:6;">
    <div style="font-size:14px;letter-spacing:7px;color:{GOLD};text-transform:uppercase;opacity:.85;">{i['eyebrow']}</div>
    <h2 class="disp" style="font-size:62px;font-weight:500;color:{GOLD_HI};margin-top:8px;line-height:1.02;">{i['heading']}</h2>
    <div style="width:70px;height:2px;background:{GOLD};margin:26px 0 30px;"></div>
    <div class="disp" style="font-size:21px;font-style:italic;line-height:1.55;color:#e8e3d8;max-width:620px;">{body}</div>
    <div style="margin-top:44px;max-width:520px;">{stats}</div>
  </div>
  <div class="ftr"><span>{D.BRAND['empire']}</span><span class="pg">ii</span><span>{D.BRAND['series']}</span></div>
</div>"""

ROMAN = ["i","ii","iii","iv","v","vi","vii","viii","ix","x","xi","xii","xiii","xiv","xv","xvi","xvii","xviii","xix","xx"]

def plate(p, pageno):
    return f"""
<div class="page">
  <div class="hdr"><span>{p['id']}</span><span>{D.BRAND['edition'].replace('Edition ','Ed. ')}</span></div>
  <img src="{b64(p['image'])}" style="position:absolute;top:108px;left:80px;width:840px;height:1140px;
       object-fit:{p['fit']};object-position:{p['focus']};z-index:2;
       box-shadow:0 10px 50px rgba(0,0,0,.5);">
  <div style="position:absolute;top:108px;left:80px;width:840px;height:1140px;z-index:3;pointer-events:none;
       border:1px solid rgba(201,162,75,.35);
       background:linear-gradient(180deg,rgba(0,0,0,0) 62%,rgba(8,8,11,.82) 100%);"></div>
  <div style="position:absolute;left:104px;right:104px;bottom:150px;z-index:4;">
    <h3 class="disp" style="font-size:42px;font-weight:500;color:{GOLD_HI};line-height:1;">{p['title']}</h3>
    <p class="disp" style="font-size:21px;font-style:italic;color:#efe9da;margin-top:12px;max-width:680px;line-height:1.4;">{p['line']}</p>
    <div style="margin-top:14px;font-size:12px;letter-spacing:3px;text-transform:uppercase;color:{GOLD};opacity:.7;">
      {p['archive']} · {D.BRAND['collection']} · {D.BRAND['classification']}</div>
  </div>
  <div class="wm" style="font-size:300px;">FGE</div>
  <div class="ftr"><span>{D.BRAND['empire']}</span><span class="pg">{ROMAN[pageno-1]}</span><span>{D.BRAND['series']}</span></div>
</div>"""

def centerfold():
    c = D.CENTERFOLD
    return f"""
<div class="spread">
  <img src="{b64(c['image'])}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1;">
  <div style="position:absolute;inset:0;z-index:2;background:
       linear-gradient(90deg,rgba(8,8,11,.78) 0%,rgba(8,8,11,.15) 32%,rgba(8,8,11,0) 50%,rgba(8,8,11,.1) 70%,rgba(8,8,11,.4) 100%),
       linear-gradient(180deg,rgba(8,8,11,.4) 0%,rgba(8,8,11,0) 25%,rgba(8,8,11,.55) 100%);"></div>
  <!-- gutter -->
  <div style="position:absolute;top:0;bottom:0;left:50%;width:2px;transform:translateX(-1px);z-index:3;
       background:linear-gradient(180deg,transparent,rgba(0,0,0,.5),transparent);"></div>
  {gold_frame_svg(SPREAD_W,PAGE_H)}
  <div style="position:absolute;top:130px;left:90px;width:560px;z-index:6;">
    <div style="font-size:14px;letter-spacing:7px;color:{GOLD};text-transform:uppercase;">{D.BRAND['char_id']} · CENTERFOLD</div>
    <h2 class="disp" style="font-size:72px;font-weight:500;color:{GOLD_HI};line-height:1;margin-top:10px;">{c['title']}</h2>
    <div style="width:80px;height:2px;background:{GOLD};margin:24px 0;"></div>
    <p class="disp" style="font-size:23px;font-style:italic;line-height:1.5;color:#efe9da;">{c['fragment']}</p>
  </div>
  <div style="position:absolute;bottom:120px;left:90px;right:90px;z-index:6;display:flex;gap:60px;justify-content:flex-start;">
    {''.join(f"<div style='border-left:2px solid {GOLD};padding-left:16px;'><div class=\"disp\" style=\"font-size:24px;color:{GOLD_HI};\">{t}</div><div style=\"font-size:14px;color:#dcd6c8;opacity:.85;max-width:180px;\">{d}</div></div>" for t,d in [c['left'],c['mid'],c['right']])}
  </div>
  <div class="wm" style="font-size:420px;left:50%;">FGE</div>
</div>"""

def colophon():
    c = D.COLOPHON
    sys = "".join(f"<li style='margin:6px 0;'>{s}</li>" for s in c['systems'])
    return f"""
<div class="page" style="background:radial-gradient(120% 90% at 30% 80%,#16131c 0%,{INK} 60%);">
  {WATERMARK}
  {gold_frame_svg(PAGE_W,PAGE_H)}
  <div style="position:absolute;top:200px;left:90px;right:90px;z-index:6;">
    <h2 class="disp" style="font-size:46px;font-weight:500;color:{GOLD_HI};">{c['heading']}</h2>
    <div style="width:60px;height:2px;background:{GOLD};margin:22px 0 26px;"></div>
    <p style="font-size:19px;line-height:1.5;max-width:600px;">{c['body']}</p>
    <div style="margin-top:30px;font-size:13px;letter-spacing:3px;text-transform:uppercase;color:{GOLD};">Systems Utilized</div>
    <ul style="list-style:none;font-size:18px;margin-top:10px;">{sys}</ul>
    <p style="font-size:18px;line-height:1.5;max-width:600px;margin-top:30px;color:#dcd6c8;">{c['direction']}</p>
    <p class="disp" style="font-size:24px;font-style:italic;color:{GOLD_HI};margin-top:50px;">{c['note']}</p>
    <p style="font-size:12px;letter-spacing:2px;color:{GOLD};opacity:.6;margin-top:18px;">
      {D.BRAND['provenance']} · {D.BRAND['edition']}</p>
  </div>
  <div class="ftr"><span>{D.BRAND['empire']}</span><span class="pg">{ROMAN[len(D.PLATES)+1]}</span><span>{D.BRAND['series']}</span></div>
</div>"""

def build_html():
    parts = [cover(), intro()]
    # split plates around centerfold (centerfold ~ middle)
    half = len(D.PLATES)//2
    for n,p in enumerate(D.PLATES[:half], start=1):
        parts.append(plate(p, n+2))     # +2 for cover/intro roman offset
    parts.append(centerfold())
    for n,p in enumerate(D.PLATES[half:], start=half+1):
        parts.append(plate(p, n+2))
    parts.append(colophon())
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE_CSS}</style></head><body>{''.join(parts)}</body></html>"

def page_doc(inner):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE_CSS}</style></head><body>{inner}</body></html>"

def render():
    # ordered list of (html_fragment, width, height)
    pages = [(cover(), PAGE_W, PAGE_H), (intro(), PAGE_W, PAGE_H)]
    half = len(D.PLATES)//2
    for n,p in enumerate(D.PLATES[:half], start=1):
        pages.append((plate(p, n+2), PAGE_W, PAGE_H))
    pages.append((centerfold(), SPREAD_W, PAGE_H))
    for n,p in enumerate(D.PLATES[half:], start=half+1):
        pages.append((plate(p, n+2), PAGE_W, PAGE_H))
    pages.append((colophon(), PAGE_W, PAGE_H))

    from pypdf import PdfWriter, PdfReader
    writer = PdfWriter()
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for idx,(frag,w,h) in enumerate(pages):
            pg = b.new_page(viewport={"width":w,"height":h})
            pg.set_content(page_doc(frag), wait_until="networkidle")
            pg.wait_for_timeout(900)
            fn = f"_pg_{idx:02d}.pdf"
            pg.pdf(path=fn, print_background=True,
                   width=f"{w}px", height=f"{h}px",
                   margin={"top":"0","bottom":"0","left":"0","right":"0"})
            pg.close()
            writer.append(PdfReader(fn))
        b.close()
    with open("FGE_Lilith_Noir_Lookbook.pdf","wb") as f:
        writer.write(f)
    print(f"rendered {len(pages)} pages")

if __name__ == "__main__":
    render()
