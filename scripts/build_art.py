"""Build the README art (assets/v3/*.svg) in light and dark.

Fonts are subset to the characters each SVG uses and embedded as data URIs,
so the SVGs render identically on GitHub (which blocks external requests).
Run: python scripts/build_art.py  (needs fonttools, brotli, Pillow; font paths via FONT_DIR)
"""
import base64, html, io, os, re
from pathlib import Path
from fontTools import subset
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "v3"
FONT_DIR = Path(os.environ.get("FONT_DIR", "/home/claude/fonts"))

def font(pkg, name):
    return next(FONT_DIR.glob(f"*{pkg}*/package/files/{name}"))

FONTS = {  # css family -> (file, weight, style)
    "S": (font("instrument-serif", "instrument-serif-latin-400-normal.woff2"), 400, "normal"),
    "SI": (font("instrument-serif", "instrument-serif-latin-400-italic.woff2"), 400, "normal"),
    "M": (font("jetbrains-mono", "jetbrains-mono-latin-400-normal.woff2"), 400, "normal"),
    "MB": (font("jetbrains-mono", "jetbrains-mono-latin-700-normal.woff2"), 400, "normal"),
    "T": (font("inter", "inter-latin-400-normal.woff2"), 400, "normal"),
    "TB": (font("inter", "inter-latin-700-normal.woff2"), 400, "normal"),
}

THEMES = {
    "light": dict(bg="#F3EFE6", panel="#FBF9F4", ink="#16140F", muted="#6E685C", line="#DCD5C6",
                  accent="#2E46FF", hi="#D9FF3D", hiInk="#16140F", ok="#1F9D55"),
    "dark": dict(bg="#0F0E0C", panel="#171613", ink="#F0EBDF", muted="#948D7F", line="#2C2924",
                 accent="#8C9BFF", hi="#D9FF3D", hiInk="#0F0E0C", ok="#4ADE80"),
}

def esc(s):
    return html.escape(s, quote=False)

def subset_font(path, chars):
    opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["kern", "liga"]
    f = subset.load_font(str(path), opts)
    sub = subset.Subsetter(opts); sub.populate(text=chars + " "); sub.subset(f)
    buf = io.BytesIO(); subset.save_font(f, buf, opts)
    return base64.b64encode(buf.getvalue()).decode()

def svg(name, w, h, body, css="", label=""):
    """body is a function(theme) -> svg markup using classes .S .SI .M .MB .T .TB"""
    for mode, t in THEMES.items():
        markup = body(t)
        text = html.unescape(re.sub(r"<[^>]+>", "", re.sub(r"<style.*?</style>", "", markup, flags=re.S)))
        faces = []
        for fam, (path, wt, st) in FONTS.items():
            if f'class="{fam}' in markup or f' {fam}"' in markup:
                faces.append(f"@font-face{{font-family:{fam};src:url(data:font/woff2;base64,{subset_font(path, text)}) format('woff2')}}"
                             f".{fam}{{font-family:{fam}}}")
        out = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" '
               f'viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(label)}">\n'
               f"<style>{''.join(faces)}\n{css}\n"
               "@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>\n"
               f"{markup}\n</svg>\n")
        (OUT / f"{name}-{mode}.svg").write_text(out)

def img_uri(path, width=880):
    im = Image.open(ROOT / path).convert("RGB")
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=78, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

# ---------------------------------------------------------------- hero
BOOT = [
    ("B.Tech CSE, Lovely Professional University", "year 3 of 4"),
    ("founder's-office.service", "PicaPool, Delhi"),
    ("4 products shipped", "proof attached"),
    ("evals, load tests, live numbers", "loaded"),
]

def hero(t):
    o = [f'<defs><pattern id="d" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{t["line"]}"/></pattern>'
         f'<path id="ring" d="M1040,190 m-92,0 a92,92 0 1,1 184,0 a92,92 0 1,1 -184,0"/></defs>',
         f'<rect width="1200" height="640" rx="28" fill="{t["bg"]}"/>',
         f'<rect width="1200" height="640" rx="28" fill="url(#d)"/>',
         f'<text x="64" y="70" class="M" font-size="18" fill="{t["muted"]}">~/latharrr <tspan fill="{t["accent"]}">%</tspan> ./deepanshu --release v3.0</text>']
    for i, (a, b) in enumerate(BOOT):
        y = 124 + i * 40
        o.append(f'<g class="boot" style="animation-delay:{0.35 + i * 0.4:.2f}s">'
                 f'<text x="64" y="{y}" class="MB" font-size="19" fill="{t["muted"]}">[<tspan fill="{t["ok"]}">  OK  </tspan>]</text>'
                 f'<text x="168" y="{y}" class="M" font-size="19" fill="{t["ink"]}">{esc(a)} <tspan fill="{t["muted"]}">· {esc(b)}</tspan></text></g>')
    # rotating stamp
    o.append(f'<g class="stamp-in"><circle cx="1040" cy="190" r="118" fill="{t["hi"]}"/>'
             f'<g class="spin"><text class="MB" font-size="17" fill="{t["hiInk"]}"><textPath xlink:href="#ring" textLength="570" lengthAdjust="spacing">SHIPPED · MEASURED · REPEATED ·</textPath></text></g>'
             f'<text x="1040" y="208" text-anchor="middle" class="SI" font-size="64" fill="{t["hiInk"]}">v3.0</text></g>')
    o.append(f'<g class="name"><text x="58" y="440" class="S" font-size="148" letter-spacing="-3" fill="{t["ink"]}">Deepanshu <tspan class="SI" fill="{t["accent"]}">Lathar.</tspan></text></g>')
    o.append(f'<g class="tag"><text x="64" y="498" class="T" font-size="27" fill="{t["muted"]}">Founder\'s-office operator who ships the product too.</text></g>')
    o.append(f'<g class="pill"><rect x="64" y="536" width="720" height="52" rx="26" fill="{t["panel"]}" stroke="{t["line"]}"/>'
             f'<circle cx="94" cy="562" r="7" fill="{t["ok"]}"/><circle cx="94" cy="562" r="7" fill="none" stroke="{t["ok"]}" stroke-width="2" class="ping"/>'
             f'<text x="114" y="569" class="T" font-size="20" fill="{t["ink"]}">Open to AI PM / product internships · Bengaluru · Jan to Jun 2027</text></g>')
    o.append(f'<text x="1136" y="575" text-anchor="end" class="M" font-size="16" fill="{t["muted"]}">Delhi · IST<tspan class="blink" fill="{t["accent"]}"> ▌</tspan></text>')
    return "\n".join(o)

HERO_CSS = """
.boot{animation:in .35s ease-out both}
.name{animation:up .9s cubic-bezier(.2,.7,.1,1) 2.1s both}
.tag{animation:up .8s cubic-bezier(.2,.7,.1,1) 2.45s both}
.pill{animation:up .8s cubic-bezier(.2,.7,.1,1) 2.75s both}
.stamp-in{opacity:0;transform-origin:1040px 190px;animation:stamp .5s cubic-bezier(.3,1.6,.5,1) 1.9s both}
.spin{transform-origin:1040px 190px;animation:spin 24s linear infinite}
.ping{animation:ping 1.8s ease-out infinite}
.blink{animation:blink 1s steps(1) infinite}
@keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}
@keyframes up{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
@keyframes stamp{from{opacity:0;transform:scale(1.6) rotate(-20deg)}to{opacity:1;transform:none}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes ping{0%{r:7;opacity:.9}100%{r:18;opacity:0}}
@keyframes blink{50%{opacity:0}}
"""

# ---------------------------------------------------------------- section titles
def section(num, title, note):
    def b(t):
        return (f'<text x="0" y="74" class="MB" font-size="20" fill="{t["accent"]}">{num}</text>'
                f'<text x="48" y="80" class="S" font-size="64" fill="{t["ink"]}">{esc(title)}</text>'
                f'<text x="1200" y="74" text-anchor="end" class="M" font-size="18" fill="{t["muted"]}">{esc(note)}</text>'
                f'<line x1="0" y1="104" x2="1200" y2="104" stroke="{t["line"]}" stroke-width="2"/>'
                f'<line x1="0" y1="104" x2="1200" y2="104" stroke="{t["ink"]}" stroke-width="2" class="rule"/>')
    return b

SECTION_CSS = ".rule{stroke-dasharray:1200;animation:rule 1.4s cubic-bezier(.6,0,.2,1) .2s both}@keyframes rule{from{stroke-dashoffset:1200}to{stroke-dashoffset:0}}"

# ---------------------------------------------------------------- feature cards
def chips(t, x, y, items):
    o = []
    for it in items:
        w = 22 + len(it) * 10.2
        o.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="36" rx="18" fill="none" stroke="{t["line"]}" stroke-width="1.5"/>'
                 f'<text x="{x + w / 2:.0f}" y="{y + 24}" text-anchor="middle" class="M" font-size="16" fill="{t["muted"]}">{esc(it)}</text>')
        x += w + 10
    return "".join(o)

def card(no, status, name, tag_lines, metric, metric_note, stack, url, media):
    def b(t):
        o = [f'<rect x="1" y="1" width="1198" height="558" rx="28" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>',
             # browser frame
             f'<g class="win"><rect x="40" y="40" width="620" height="480" rx="18" fill="{t["bg"]}" stroke="{t["line"]}" stroke-width="2"/>',
             f'<circle cx="68" cy="68" r="6" fill="{t["line"]}"/><circle cx="88" cy="68" r="6" fill="{t["line"]}"/><circle cx="108" cy="68" r="6" fill="{t["line"]}"/>',
             f'<text x="350" y="74" text-anchor="middle" class="M" font-size="15" fill="{t["muted"]}">{esc(url)}</text>',
             media(t), '</g>',
             f'<text x="712" y="86" class="MB" font-size="15" letter-spacing="2" fill="{t["accent"]}">FEATURE {no} · {esc(status.upper())}</text>',
             f'<text x="708" y="160" class="S" font-size="72" fill="{t["ink"]}">{esc(name)}</text>']
        for i, ln in enumerate(tag_lines):
            o.append(f'<text x="712" y="{208 + i * 32}" class="T" font-size="23" fill="{t["muted"]}">{esc(ln)}</text>')
        my = 208 + len(tag_lines) * 32 + 70
        mw = 26 + len(metric) * 30
        o.append(f'<rect x="704" y="{my - 46}" width="{mw}" height="60" rx="6" fill="{t["hi"]}" class="mark"/>')
        o.append(f'<text x="716" y="{my}" class="TB" font-size="50" letter-spacing="-1.5" fill="{t["hiInk"]}">{esc(metric)}</text>')
        for i, ln in enumerate(metric_note):
            o.append(f'<text x="712" y="{my + 42 + i * 26}" class="M" font-size="16" fill="{t["muted"]}">{esc(ln)}</text>')
        o.append(chips(t, 712, 478, stack))
        return "\n".join(o)
    return b

CARD_CSS = """
.mark{transform-box:fill-box;transform-origin:left center;animation:mark .8s cubic-bezier(.6,0,.2,1) .4s both}
.win{animation:float 6s ease-in-out infinite}
.bar{transform-box:fill-box;transform-origin:left center;animation:mark 1.2s cubic-bezier(.6,0,.2,1) both}
@keyframes mark{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes float{50%{transform:translateY(-4px)}}
"""

def shot(path):
    uri = img_uri(path)
    def m(t):
        return (f'<clipPath id="c"><rect x="52" y="92" width="596" height="416" rx="10"/></clipPath>'
                f'<image href="{uri}" x="52" y="92" width="596" height="416" preserveAspectRatio="xMinYMin slice" clip-path="url(#c)"/>')
    return m

def dandiya_media(t):
    rows = [("signups", 640, 0.2), ("matches", 174, 0.6)]
    o = [f'<text x="80" y="150" class="M" font-size="16" fill="{t["muted"]}">delhi edition · navratri · results</text>']
    for i, (lab, n, d) in enumerate(rows):
        y = 236 + i * 110
        o.append(f'<text x="80" y="{y}" class="TB" font-size="64" letter-spacing="-2" fill="{t["ink"]}">{n}</text>'
                 f'<text x="220" y="{y}" class="T" font-size="22" fill="{t["muted"]}">{lab}</text>'
                 f'<rect x="80" y="{y + 22}" width="540" height="18" rx="9" fill="{t["bg"]}" stroke="{t["line"]}"/>'
                 f'<rect x="80" y="{y + 22}" width="{540 * n / 640:.0f}" height="18" rx="9" fill="{t["accent"] if i else t["ink"]}" class="bar" style="animation-delay:{d}s"/>')
    o.append(f'<text x="80" y="470" class="M" font-size="17" fill="{t["ink"]}">in <tspan fill="{t["accent"]}" class="MB">5 days</tspan> · onboarding → swipes → referrals</text>')
    return "".join(o)

# ---------------------------------------------------------------- changelog (git graph)
LOG = [  # (lane, label, date, title, lines)
    ("head", "HEAD", "now", "v3.0 · open for the next role", ["AI PM / product internship · on-site Bengaluru · Jan to Jun 2027"]),
    ("u", "merge", "Jan to May 2026", "UniLyf · Product & Growth", ["UK, remote · found the actions behind Day-7 retention,", "led a team of 6, 100K+ monthly views pre-launch"]),
    ("p", "branch", "Jul 2025 to present", "PicaPool · Founder's Office", ["15+ internal tools in 8 weeks · event-level attribution", "for a campaign reaching 3,000+ students"]),
    ("f", "merge", "Jun 2025 to Feb 2026", "Freelance · Web & Growth", ["paid D2C work, incl. the Spraykart Shopify store"]),
    ("main", "commit", "Mar 2025 to present", "LPU Student Organisations", ["Event Coordinator → HR Coordinator in 4 months", "225+ organisations, 30+ campus events"]),
    ("main", "init", "2024", "git init · B.Tech CSE, LPU", ["class of 2028"]),
]

def changelog(t):
    X = {"main": 70, "p": 120, "f": 170, "u": 220, "head": 70}
    col = {"main": t["ink"], "p": t["accent"], "f": t["muted"], "u": t["ok"]}
    Y = [70 + i * 134 for i in range(len(LOG))]
    o = [f'<rect x="1" y="1" width="1198" height="{Y[-1] + 70}" rx="28" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>']
    paths = [
        (f"M70,{Y[-1]} L70,{Y[0]}", t["ink"]),
        # picapool: forks off main below its row, runs to the top
        (f"M70,{Y[2] + 70} C70,{Y[2] + 30} 120,{Y[2] + 40} 120,{Y[2]} L120,{Y[0] + 30} C120,{Y[0] + 10} 90,{Y[0]} 70,{Y[0]}", t["accent"]),
        (f"M70,{Y[3] + 70} C70,{Y[3] + 30} 170,{Y[3] + 40} 170,{Y[3]} L170,{Y[1] - 20} C170,{Y[1] - 50} 70,{Y[1] - 40} 70,{Y[1] - 70}", t["muted"]),
        (f"M70,{Y[1] + 70} C70,{Y[1] + 30} 220,{Y[1] + 40} 220,{Y[1]} L220,{Y[0] + 60} C220,{Y[0] + 30} 70,{Y[0] + 40} 70,{Y[0] + 20}", t["ok"]),
    ]
    for i, (d, c) in enumerate(paths):
        o.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round" class="lane" style="animation-delay:{i * .25:.2f}s"/>')
    for i, (lane, kind, date, title, lines) in enumerate(LOG):
        y, x = Y[i], X[lane]
        c = col.get(lane, t["accent"])
        dl = 1.3 + (len(LOG) - i) * .15
        if lane == "head":
            o.append(f'<circle cx="{x}" cy="{y}" r="13" fill="{t["panel"]}" stroke="{t["accent"]}" stroke-width="4" class="dot" style="animation-delay:{dl:.2f}s"/>'
                     f'<circle cx="{x}" cy="{y}" r="13" fill="none" stroke="{t["accent"]}" stroke-width="2" class="ring"/>')
        else:
            o.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{c}" stroke="{t["panel"]}" stroke-width="4" class="dot" style="animation-delay:{dl:.2f}s"/>')
        o.append(f'<g class="row" style="animation-delay:{dl:.2f}s">'
                 f'<text x="300" y="{y - 14}" class="M" font-size="16" fill="{t["muted"]}"><tspan fill="{c}" class="MB">{kind}</tspan>  ·  {esc(date)}</text>'
                 f'<text x="300" y="{y + 18}" class="TB" font-size="27" fill="{t["ink"]}">{esc(title)}</text>')
        for j, ln in enumerate(lines):
            o.append(f'<text x="300" y="{y + 48 + j * 26}" class="T" font-size="20" fill="{t["muted"]}">{esc(ln)}</text>')
        o.append('</g>')
    return "\n".join(o)

LOG_CSS = """
.lane{stroke-dasharray:1400;animation:draw 1.6s cubic-bezier(.6,0,.2,1) both}
.dot{transform-box:fill-box;transform-origin:center;animation:pop .4s cubic-bezier(.3,1.6,.5,1) both}
.row{animation:in .5s ease-out both}
.ring{animation:ping 1.8s ease-out 2.5s infinite}
@keyframes draw{from{stroke-dashoffset:1400}to{stroke-dashoffset:0}}
@keyframes pop{from{transform:scale(0)}to{transform:scale(1)}}
@keyframes in{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:none}}
@keyframes ping{0%{r:13;opacity:.9}100%{r:30;opacity:0}}
"""

# ---------------------------------------------------------------- footer / roadmap
def footer(t):
    return "\n".join([
        f'<rect x="1" y="1" width="1198" height="378" rx="28" fill="{"#16140F"}"/>',
        f'<text x="64" y="84" class="MB" font-size="16" letter-spacing="2" fill="{"#D9FF3D"}">ROADMAP · v4.0</text>',
        f'<text x="58" y="186" class="S" font-size="96" fill="{"#F3EFE6"}">Next release: <tspan class="SI" fill="{"#D9FF3D"}">Jan 2027.</tspan></text>',
        f'<text x="64" y="240" class="T" font-size="25" fill="{"#F3EFE6"}" opacity=".72">AI PM / product internship · on-site Bengaluru · Jan to Jun 2027</text>',
        f'<text x="64" y="312" class="M" font-size="16" fill="{"#F3EFE6"}" opacity=".6">v3.0</text>',
        f'<rect x="120" y="300" width="900" height="14" rx="7" fill="{"#F3EFE6"}" opacity=".15"/>',
        f'<rect x="120" y="300" width="900" height="14" rx="7" fill="{"#D9FF3D"}" class="prog"/>',
        f'<text x="1040" y="312" class="M" font-size="16" fill="{"#D9FF3D"}">v4.0</text>',
        f'<text x="64" y="350" class="M" font-size="15" fill="{"#F3EFE6"}" opacity=".5">waiting on one merge: yours<tspan class="blink" fill="{"#D9FF3D"}"> ▌</tspan></text>',
    ])

FOOT_CSS = """
.prog{transform-box:fill-box;transform-origin:left center;animation:prog 3s cubic-bezier(.6,0,.2,1) .4s both}
.blink{animation:blink 1s steps(1) infinite}
@keyframes prog{from{transform:scaleX(0)}to{transform:scaleX(.82)}}
@keyframes blink{50%{opacity:0}}
"""

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    svg("hero", 1200, 640, hero, HERO_CSS, "Deepanshu Lathar. Founder's-office operator who ships the product too. Open to AI PM / product internships, Bengaluru, Jan to Jun 2027.")
    for n, (title, note) in enumerate([("What's new", "features shipped in this release"),
                                       ("Changelog", "git log --graph --career"),
                                       ("Under the hood", "stack, skills, defaults"),
                                       ("Known issues", "honest release notes")], 1):
        svg(f"s{n}", 1200, 112, section(f"0{n}", title, note), SECTION_CSS, f"0{n} {title}")
    svg("gapl", 1200, 560, card("01", "live beta · 10+ testers", "Gapl",
        ["AI resume review that thinks", "like a recruiter."], "41/44 → 44/44",
        ["eval pass rate after I found and", "fixed a false-rejection bug"], ["Next.js", "TypeScript", "Firebase", "Razorpay"],
        "gapl.143.lat", shot("assets/gapl.jpg")), CARD_CSS, "Gapl: AI resume review. Evals went from 41/44 to 44/44.")
    svg("proofmart", 1200, 560, card("02", "live · public API + CLI", "ProofMart",
        ["Re-adds bank statements to catch", "edits. No AI in the verdict."], "32 test files",
        ["28 unit + 4 E2E · every check pinned", "to page coordinates, results signed"], ["Next.js", "TypeScript", "Supabase", "OCR"],
        "proofmart.shop", shot("assets/proofmart-evidence-rail.jpg")), CARD_CSS, "ProofMart: bank-statement tamper detection with 28 unit and 4 E2E test files.")
    svg("lpuconnect", 1200, 560, card("03", "live", "LPU Connect",
        ["Anonymous campus chat and video.", "Messages are never stored."], "10,000 users",
        ["concurrent, 0 failures, load-tested on", "the live server · 47 tests, ~84% cov."], ["React", "Node.js", "Socket.IO", "WebRTC"],
        "tv.143.lat", shot("assets/lputv-dashboard.jpg")), CARD_CSS, "LPU Connect: 10,000 concurrent users with 0 failures in a load test.")
    svg("dandiya", 1200, 560, card("04", "shipped · product owner", "Dandiya Nights",
        ["PicaPool's Navratri partner-", "matching app, end to end."], "640 → 174",
        ["signups to matches in 5 days ·", "funnel tracked daily"], ["onboarding", "swipe pacing", "referrals"],
        "dandiya.picapool.tech", dandiya_media), CARD_CSS, "Dandiya Nights: 640 signups and 174 matches in 5 days.")
    svg("changelog", 1200, 810, changelog, LOG_CSS, "Career changelog: LPU 2024, Student Organisations, Freelance, PicaPool Founder's Office, UniLyf, now open to AI PM internships.")
    svg("roadmap", 1200, 380, footer, FOOT_CSS, "Next release: Jan 2027. AI PM / product internship, on-site Bengaluru, Jan to Jun 2027.")

if __name__ == "__main__":
    main()
