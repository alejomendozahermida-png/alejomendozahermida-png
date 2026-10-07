"""Génère les visuels SVG du profil GitHub (thème « Glacier »).

    python scripts/generate.py           # visuels statiques -> assets/
    python scripts/generate.py --stats   # + carte de stats live -> dist/stats.svg (besoin de GITHUB_TOKEN)
"""
import json
import os
import sys
import textwrap
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import profile_data as D  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
DIST = ROOT / "dist"

C = {
    "bg": "#111B27", "panel": "#16222F", "bar": "#0B131C", "border": "#22324A",
    "text": "#E8EEF4", "muted": "#7D8FA3", "dim": "#3A4B60", "faint": "#1C2A3A",
    "ice": "#7CC4E4", "sky": "#5B9BD5", "terra": "#D2875A", "sand": "#E3B98A",
    "sage": "#8FC1A9", "rose": "#D99A9A",
}
SANS = "'Segoe UI', Ubuntu, -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', Consolas, Menlo, 'Courier New', monospace"
W = 880


def col(c):
    return C.get(c, c)


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def t(x, y, s, size=13, fill="text", font=MONO, weight=None, anchor=None, extra=""):
    a = f' font-weight="{weight}"' if weight else ""
    a += f' text-anchor="{anchor}"' if anchor else ""
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
            f'fill="{col(fill)}"{a} {extra}>{esc(s)}</text>')


def mono_w(s, size):
    return len(s) * size * 0.6


def svg(w, h, label, body, style=""):
    st = f"<style>{style}</style>" if style else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(label)}"><title>{esc(label)}</title>{st}{body}</svg>')


def window(h, title, body, w=W):
    """Cadre d'éditeur : barre de titre + 3 pastilles."""
    return (f'<rect width="{w}" height="{h}" rx="12" fill="{C["panel"]}"/>'
            f'<path d="M12 0h{w-24}a12 12 0 0 1 12 12v24H0V12A12 12 0 0 1 12 0z" fill="{C["bar"]}"/>'
            f'<circle cx="22" cy="18" r="6" fill="{C["rose"]}"/><circle cx="42" cy="18" r="6" fill="{C["sand"]}"/>'
            f'<circle cx="62" cy="18" r="6" fill="{C["sage"]}"/>'
            + t(w / 2, 22, f"{title} — {D.NAME_FIRST.lower()}-{D.NAME_LAST.lower()}", 12, "muted", SANS, anchor="middle")
            + body
            + f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="none" stroke="{C["border"]}"/>')


def pill(x, y, s, color, size=11, filled=False, font=SANS, h=None, weight="600"):
    h = h or size + 11
    w = mono_w(s, size) * (1.0 if font == MONO else 0.98) + 18
    fill = col(color) if filled else C["faint"]
    return (f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{fill}" '
            f'fill-opacity="{0.18 if filled else 1}" stroke="{col(color)}" stroke-opacity=".55"/>'
            + t(x + w / 2, y + h / 2 + size * 0.36, s, size, color, font, weight, "middle")), w


# --------------------------------------------------------------------------- header
TABS = [("README.md", "ice"), ("whoami.py", "sand"), ("builds.sql", "terra"),
        ("journey.yaml", "sage"), ("stack.toml", "rose")]


def header():
    H = 340
    b = [f'<defs><linearGradient id="peak" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="#4E86B8"/><stop offset="1" stop-color="{C["panel"]}"/></linearGradient>'
         f'<linearGradient id="back" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="#2C4462"/><stop offset="1" stop-color="{C["panel"]}"/></linearGradient>'
         f'<clipPath id="type"><rect x="60" y="226" width="0" height="24">'
         f'<animate attributeName="width" from="0" to="490" begin=".6s" dur="2.4s" fill="freeze"/></rect></clipPath>'
         f'</defs>']
    # onglets
    b.append(f'<rect y="36" width="{W}" height="32" fill="{C["bar"]}"/>')
    x = 0
    for i, (name, c) in enumerate(TABS):
        w = mono_w(name, 12) + 44
        b.append(f'<rect x="{x}" y="36" width="{w:.1f}" height="32" fill="{C["panel"] if i == 0 else C["bar"]}"/>')
        if i == 0:
            b.append(f'<rect x="{x}" y="36" width="{w:.1f}" height="2" fill="{C["ice"]}"/>')
        b.append(f'<circle cx="{x+16}" cy="52" r="4" fill="{col(c)}"/>')
        b.append(t(x + 28, 56, name, 12, "text" if i == 0 else "muted"))
        x += w
    # numéros de ligne
    for i in range(9):
        b.append(t(34, 106 + i * 22.5, i + 1, 12, "dim", anchor="end"))
    # code
    b.append(t(64, 106, "# ¡hola! · bonjour · welcome to my GitHub", 13, "muted"))
    b.append(f'<text x="64" y="134" font-family="{MONO}" font-size="16" class="r1">'
             f'<tspan fill="{C["sky"]}">&gt;&gt;&gt; </tspan><tspan fill="{C["text"]}">print(</tspan>'
             f'<tspan fill="{C["sand"]}">"Hi, I\'m"</tspan><tspan fill="{C["text"]}">)</tspan></text>')
    b.append(f'<text x="62" y="196" font-family="{SANS}" font-size="50" font-weight="800" class="r2" '
             f'letter-spacing="-1"><tspan fill="{C["text"]}">{esc(D.NAME_FIRST)} </tspan>'
             f'<tspan fill="{C["terra"]}">{esc(D.NAME_LAST)}</tspan></text>')
    b.append(f'<g clip-path="url(#type)"><text x="64" y="243" font-family="{MONO}" font-size="14.5">'
             f'<tspan fill="{C["sky"]}">role</tspan><tspan fill="{C["text"]}"> = </tspan>'
             f'<tspan fill="{C["sage"]}">"{esc(D.ROLE)}"</tspan></text></g>')
    cx = 64 + mono_w(f'role = "{D.ROLE}"', 14.5) + 4
    b.append(f'<rect x="{cx:.0f}" y="230" width="8" height="17" fill="{C["ice"]}" class="cur" opacity="0">'
             f'<set attributeName="opacity" to="1" begin="3s"/></rect>')
    b.append(t(64, 286, "# MSc IA appliquée au business @ Eugenia School · CO → FR", 12.5, "muted", extra='class="r3"'))

    # montagne
    m = []
    for sx, sy, d in [(612, 96, 0), (842, 112, 1.2), (668, 84, 2.1), (800, 88, .6), (860, 150, 1.7)]:
        m.append(f'<circle cx="{sx}" cy="{sy}" r="1.6" fill="{C["text"]}" class="tw" style="animation-delay:{d}s"/>')
    m.append(f'<polygon points="586,306 646,196 684,232 732,158 792,220 834,182 878,306" fill="url(#back)" opacity=".85"/>')
    m.append('<polygon points="604,306 738,100 872,306" fill="url(#peak)"/>')
    m.append(f'<polygon points="738,100 708,146 722,140 734,154 749,138 768,148" fill="{C["text"]}" opacity=".92"/>')
    route = "M660 300 L702 266 L672 236 L730 208 L704 180 L746 152 L738 108"
    m.append(f'<path d="{route}" fill="none" stroke="{C["terra"]}" stroke-width="2" stroke-dasharray="3 5" '
             f'stroke-linecap="round" opacity=".9"/>')
    m.append(f'<circle r="4.5" fill="{C["sand"]}"><animateMotion dur="7s" repeatCount="indefinite" path="{route}" '
             f'keyPoints="0;1;1" keyTimes="0;.85;1" calcMode="linear"/></circle>')
    m.append(f'<line x1="738" y1="108" x2="738" y2="78" stroke="{C["text"]}" stroke-width="2"/>')
    m.append(f'<path d="M738 78 L760 84 L738 91 Z" fill="{C["terra"]}">'
             f'<animate attributeName="d" values="M738 78 L760 84 L738 91 Z;M738 78 L758 87 L738 91 Z;M738 78 L760 84 L738 91 Z" '
             f'dur="1.6s" repeatCount="indefinite"/></path>')
    pts = [(702, 266, "R"), (672, 236, "L"), (730, 208, "R"), (704, 180, "L"), (746, 152, "R")]
    for (px, py, side), label in zip(pts, D.ROUTE):
        w = mono_w(label, 10.5) * .95 + 16
        lx = px + 9 if side == "R" else px - 9 - w
        m.append(f'<circle cx="{px}" cy="{py}" r="3.5" fill="{C["terra"]}"/>')
        m.append(f'<rect x="{lx:.1f}" y="{py-10}" width="{w:.1f}" height="20" rx="10" fill="{C["bar"]}" '
                 f'stroke="{C["terra"]}" stroke-opacity=".6"/>')
        m.append(t(lx + w / 2, py + 4, label, 10.5, "text", SANS, "600", "middle"))
    b.append('<g class="r2">' + "".join(m) + "</g>")

    # barre de statut
    b.append(f'<rect y="{H-28}" width="{W}" height="28" fill="{C["bar"]}"/>')
    b.append(f'<path d="M0 {H-28}h96v28H12a12 12 0 0 1-12-12z" fill="{C["sky"]}"/>')
    b.append(t(14, H - 10, "⎇ main ✓", 12, "bar", weight="600"))
    b.append(t(112, H - 10, f"● Alternance 2 ans · Île-de-France · 4j / 1j   ✉ {D.EMAIL}", 11.5, "muted"))
    b.append(t(W - 14, H - 10, "UTF-8  Python  Glacier", 11.5, "muted", anchor="end"))
    style = ("@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}.cur{animation:blink 1s step-end infinite}"
             "@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}"
             ".r1{animation:rise .6s ease-out}.r2{animation:rise 1s ease-out}.r3{animation:rise 1.4s ease-out}"
             "@keyframes tw{0%,100%{opacity:.2}50%{opacity:.9}}.tw{animation:tw 3s ease-in-out infinite}")
    return svg(W, H, f"{D.NAME_FIRST} {D.NAME_LAST} — {D.ROLE}", window(H, "README.md", "".join(b)), style)


# --------------------------------------------------------------------------- highlights
def highlights():
    H, gap = 118, 12
    n = len(D.HIGHLIGHTS)
    cw = (W - gap * (n - 1)) / n
    b = []
    for i, (val, l1, l2, c) in enumerate(D.HIGHLIGHTS):
        x = i * (cw + gap)
        b.append(f'<g class="r" style="animation-delay:{i*.12:.2f}s">'
                 f'<rect x="{x:.1f}" y="1" width="{cw:.1f}" height="{H-2}" rx="10" fill="{C["panel"]}" stroke="{C["border"]}"/>'
                 f'<rect x="{x+10:.1f}" y="1" width="{cw-20:.1f}" height="3" rx="1.5" fill="{col(c)}"/>'
                 + t(x + cw / 2, 56, val, 34, c, SANS, "800", "middle")
                 + t(x + cw / 2, 82, l1, 12.5, "text", SANS, anchor="middle")
                 + t(x + cw / 2, 100, l2, 11.5, "muted", SANS, anchor="middle") + "</g>")
    style = "@keyframes r{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}.r{animation:r .7s ease-out both}"
    label = " · ".join(f"{v} {a} {b_}" for v, a, b_, _ in D.HIGHLIGHTS)
    return svg(W, H, label, "".join(b), style)


# --------------------------------------------------------------------------- builds
def builds_bar():
    H = 60
    q = "SELECT title, impact FROM builds WHERE shipped OR building;"
    b = (f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="{C["panel"]}" stroke="{C["border"]}"/>'
         f'<text x="24" y="36" font-family="{MONO}" font-size="13.5"><tspan fill="{C["terra"]}">SELECT</tspan>'
         f'<tspan fill="{C["text"]}"> title, impact </tspan><tspan fill="{C["terra"]}">FROM</tspan>'
         f'<tspan fill="{C["sand"]}"> builds </tspan><tspan fill="{C["terra"]}">WHERE</tspan>'
         f'<tspan fill="{C["text"]}"> shipped </tspan><tspan fill="{C["terra"]}">OR</tspan>'
         f'<tspan fill="{C["text"]}"> building;</tspan></text>'
         + t(W - 24, 36, f"-- {len(D.BUILDS)} rows · featured", 12.5, "muted", anchor="end"))
    return svg(W, H, q, b)


def card(p):
    CW, CH = 560, 420
    c1, c2 = p["cover"]
    sl, sc = p["status"]
    b = [f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/>'
         f'<stop offset="1" stop-color="{c2}"/></linearGradient>'
         f'<clipPath id="r"><rect width="{CW}" height="{CH}" rx="16"/></clipPath></defs>',
         f'<g clip-path="url(#r)"><rect width="{CW}" height="{CH}" fill="{C["panel"]}"/>'
         f'<rect width="{CW}" height="128" fill="url(#g)"/>'
         f'<path d="M0 128 L90 92 L150 112 L240 70 L330 108 L420 80 L{CW} 118 L{CW} 128 Z" fill="#000" opacity=".14"/></g>']
    b.append(t(36, 80, p["icon"], 46, "text", SANS))
    b.append(t(108, 60, " · ".join(p["categories"]), 16, "#F4F7FA", MONO, extra='letter-spacing="2" opacity=".9"'))
    b.append(t(108, 90, p["role"], 16, "#F4F7FA", MONO, extra='opacity=".75"'))
    pw = mono_w(sl, 13) + 40
    b.append(f'<rect x="{CW-24-pw:.1f}" y="154" width="{pw:.1f}" height="32" rx="16" fill="{C["bar"]}" stroke="{col(sc)}" stroke-opacity=".45"/>'
             f'<circle cx="{CW-24-pw+18:.1f}" cy="170" r="4.5" fill="{col(sc)}"><animate attributeName="opacity" '
             f'values="1;.3;1" dur="2s" repeatCount="indefinite"/></circle>'
             + t(CW - 24 - pw + 30, 175, sl, 13, sc, MONO, "700"))
    b.append(t(36, 180, p["title"], 30, "text", SANS, "800"))
    b.append(t(36, 208, "// " + p["subtitle"], 15.5, "muted", MONO))
    for i, line in enumerate(textwrap.wrap(p["desc"], 52)[:4]):
        b.append(t(36, 246 + i * 26, line, 17.5, "#C9D4DF", SANS))
    if p.get("metrics"):
        b.append(t(36, 360, "▲ " + "  ·  ".join(p["metrics"]), 14.5, sc, MONO, "600"))
    x = 36
    for tag in p["tags"]:
        s, w = pill(x, 376, tag, sc, 14, filled=True, h=30)
        b.append(s)
        x += w + 8
    if p.get("url"):
        b.append(t(CW - 32, 397, "open ↗", 16, "ice", MONO, anchor="end"))
    b.append(f'<rect x=".75" y=".75" width="{CW-1.5}" height="{CH-1.5}" rx="16" fill="none" stroke="{C["border"]}" stroke-width="1.5"/>')
    return svg(CW, CH, f'{p["title"]} — {p["subtitle"]}', "".join(b))


# --------------------------------------------------------------------------- journey
def journey():
    step = 100
    H = 36 + 34 + len(D.JOURNEY) * step + 40 + len(D.EDUCATION) * step + 10
    b = []
    y = 66

    def entry(e, y):
        c = e["color"]
        s = []
        if e["current"]:
            s.append(f'<circle cx="50" cy="{y+8}" r="13" fill="{col(c)}" opacity=".18">'
                     f'<animate attributeName="r" values="11;15;11" dur="2.4s" repeatCount="indefinite"/></circle>')
        s.append(f'<circle cx="50" cy="{y+8}" r="7" fill="{C["panel"]}" stroke="{col(c)}" stroke-width="2.5"/>')
        s.append(t(76, y + 4, e["period"], 11.5, "muted"))
        s.append(t(76, y + 26, e["title"], 17, "text", SANS, "700"))
        if e["current"]:
            tw = len(e["title"]) * 17 * 0.53
            s.append(t(76 + tw + 16, y + 25, "● EN COURS", 10.5, "sage", MONO, "600"))
        org = "@ " + e["org"]
        s.append(t(76, y + 50, org, 13.5, c, SANS, "700"))
        ox = 76 + len(org) * 13.5 * 0.74 + 12
        p_, _ = pill(ox, y + 37, e["type"], c, 10.5)
        s.append(p_)
        s.append(t(76, y + 74, e["line"], 13, "#C9D4DF", SANS))
        x = W - 24
        for tag in reversed(e["tags"]):
            w = mono_w(tag, 10.5) * .98 + 18
            x -= w
            p_, _ = pill(x, y - 8, tag, "sky", 10.5)
            s.append(p_)
            x -= 6
        return "".join(s)

    b.append(f'<text x="34" y="{y-6}" font-family="{MONO}" font-size="13"><tspan fill="{C["sky"]}">experience</tspan>'
             f'<tspan fill="{C["text"]}">:</tspan><tspan fill="{C["muted"]}">  # du terrain vers l\'automatisation</tspan></text>')
    y += 22
    top = y
    for e in D.JOURNEY:
        b.append(entry(e, y))
        y += step
    b.insert(1, f'<line x1="50" y1="{top+8}" x2="50" y2="{y-step+8}" stroke="{C["dim"]}" stroke-width="2"/>')
    y += 8
    b.append(f'<text x="34" y="{y}" font-family="{MONO}" font-size="13"><tspan fill="{C["sky"]}">education</tspan>'
             f'<tspan fill="{C["text"]}">:</tspan></text>')
    y += 28
    top2 = y
    edu = [entry(e, y + i * step) for i, e in enumerate(D.EDUCATION)]
    b.append(f'<line x1="50" y1="{top2+8}" x2="50" y2="{top2+(len(D.EDUCATION)-1)*step+8}" stroke="{C["dim"]}" stroke-width="2"/>')
    b.extend(edu)
    H = top2 + len(D.EDUCATION) * step - 4
    return svg(W, H, "Parcours : " + ", ".join(e["org"] for e in D.JOURNEY + D.EDUCATION),
               window(H, "journey.yaml", "".join(b)))


# --------------------------------------------------------------------------- stack
def stack():
    LEVEL = {3: "au quotidien", 2: "à l'aise", 1: "en apprentissage"}
    cols = [[], []]
    load = [0, 0]
    for g in D.STACK:
        i = 0 if load[0] <= load[1] else 1
        cols[i].append(g)
        load[i] += len(g[2]) + 1.6
    b = [f'<text x="34" y="66" font-family="{MONO}" font-size="12.5"><tspan fill="{C["sky"]}">level</tspan>'
         f'<tspan fill="{C["text"]}"> = {{ </tspan>'
         + "".join(f'<tspan fill="{C["sand"]}">{k}</tspan><tspan fill="{C["text"]}">: </tspan>'
                   f'<tspan fill="{C["sage"]}">"{esc(v)}"</tspan><tspan fill="{C["text"]}">{", " if k > 1 else ""}</tspan>'
                   for k, v in LEVEL.items())
         + f'<tspan fill="{C["text"]}"> }}</tspan></text>']
    bottom = 0
    for ci, groups in enumerate(cols):
        x0 = 38 + ci * 440
        y = 104
        for name, c, items in groups:
            b.append(t(x0, y, name, 11, c, MONO, "700", extra='letter-spacing="2"'))
            y += 26
            for label, lvl in items:
                b.append(t(x0, y, label, 14, "text", SANS))
                for k in range(3):
                    filled = k < lvl
                    b.append(f'<circle cx="{x0+222+k*16}" cy="{y-4.5}" r="5" '
                             f'fill="{col(c) if filled else "none"}" stroke="{col(c) if filled else C["dim"]}" stroke-width="1.5"/>')
                b.append(t(x0 + 274, y, LEVEL[lvl], 11, "muted", MONO))
                y += 28
            y += 18
        bottom = max(bottom, y)
    H = bottom - 4
    return svg(W, H, "Stack : " + ", ".join(i[0] for g in D.STACK for i in g[2]),
               window(H, "stack.toml", "".join(b)))


# --------------------------------------------------------------------------- stats (live)
def gql(query, token):
    req = urllib.request.Request("https://api.github.com/graphql",
                                 data=json.dumps({"query": query}).encode(),
                                 headers={"Authorization": f"bearer {token}", "User-Agent": D.LOGIN})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["data"]


def stats():
    token = os.environ.get("GITHUB_TOKEN")
    q = """{ user(login: "%s") {
      followers { totalCount }
      contributionsCollection { contributionCalendar { totalContributions } }
      repositories(ownerAffiliations: OWNER, privacy: PUBLIC, first: 100, isFork: false) {
        totalCount
        nodes { stargazerCount languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } } } } } } }""" % D.LOGIN
    u = gql(q, token)["user"]
    repos = u["repositories"]
    stars = sum(n["stargazerCount"] for n in repos["nodes"])
    langs = {}
    for n in repos["nodes"]:
        for e in n["languages"]["edges"]:
            k = e["node"]["name"]
            langs.setdefault(k, [0, e["node"]["color"] or C["muted"]])[0] += e["size"]
    top = sorted(langs.items(), key=lambda kv: -kv[1][0])[:6]
    total = sum(v[0] for _, v in top) or 1
    nums = [(u["contributionsCollection"]["contributionCalendar"]["totalContributions"], "contributions · 12 mois", "terra"),
            (repos["totalCount"], "repos publics", "ice"), (stars, "étoiles", "sand"),
            (u["followers"]["totalCount"], "followers", "sage")]
    H = 196
    b = [f'<text x="34" y="66" font-family="{MONO}" font-size="12.5"><tspan fill="{C["muted"]}"># mis à jour chaque jour par une GitHub Action</tspan></text>']
    cw = (W - 68 - 3 * 12) / 4
    for i, (v, lab, c) in enumerate(nums):
        x = 34 + i * (cw + 12)
        b.append(f'<rect x="{x:.1f}" y="80" width="{cw:.1f}" height="56" rx="8" fill="{C["bar"]}" stroke="{C["border"]}"/>'
                 + t(x + 16, 114, v, 24, c, SANS, "800") + t(x + 16 + len(str(v)) * 15 + 10, 113, lab, 12, "muted", SANS))
    x = 34.0
    bw = W - 68
    for name, (size, color) in top:
        w = bw * size / total
        b.append(f'<rect x="{x:.1f}" y="152" width="{max(w-2, 1):.1f}" height="8" rx="4" fill="{color}"/>')
        x += w
    x = 34
    for name, (size, color) in top:
        s = f"{name} {100*size/total:.0f}%"
        b.append(f'<circle cx="{x+5}" cy="180" r="5" fill="{color}"/>' + t(x + 15, 184, s, 12, "text", SANS))
        x += len(s) * 7 + 34
    DIST.mkdir(exist_ok=True)
    (DIST / "stats.svg").write_text(svg(W, H, "Statistiques GitHub", window(H, "stats.py", "".join(b))), encoding="utf-8")


def main():
    ASSETS.mkdir(exist_ok=True)
    out = {"header.svg": header(), "highlights.svg": highlights(), "builds.svg": builds_bar(),
           "journey.svg": journey(), "stack.svg": stack()}
    for i, p in enumerate(D.BUILDS, 1):
        out[f"build-{i:02d}.svg"] = card(p)
    for name, s in out.items():
        (ASSETS / name).write_text(s, encoding="utf-8")
    print(f"{len(out)} visuels écrits dans assets/")
    if "--stats" in sys.argv:
        stats()
        print("dist/stats.svg écrit")


if __name__ == "__main__":
    main()
