"""Génère les visuels SVG du profil (thèmes clair et sombre), dans la DA du portfolio
https://www.portfolio-daens-elliott.fr/ : fond #101217, vert citron #D4FF3D,
Space Grotesk + Instrument Serif italique + JetBrains Mono, étiquettes « // ».

Les polices (licence OFL) sont dans scripts/fonts/ : chaque SVG embarque
seulement les lettres qu'il utilise (sous-ensemble woff2 en base64).

Usage : python scripts/build_assets.py  -> écrit dans assets/
Besoin de : pip install fonttools brotli
"""
import base64
import io
import re
from functools import lru_cache
from html import escape, unescape
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "assets"
OUT.mkdir(exist_ok=True)

FONTS = {  # classe CSS -> (famille, fichier, style, graisses, repli)
    "sg": ("Space Grotesk", "space-grotesk-variable.woff2", "normal", "300 700", "system-ui,sans-serif"),
    "is": ("Instrument Serif", "instrument-serif-400-italic.woff2", "italic", "400", "Georgia,serif"),
    "jb": ("JetBrains Mono", "jetbrains-mono-variable.woff2", "normal", "100 800", "ui-monospace,monospace"),
}

THEMES = {
    "dark": dict(bg="#101217", card="#171A21", ink="#F0EEE9", muted="#A9ACB4", faint="#898D96",
                 line="#F0EEE9", lo=.12, hi=.28, chip=.45, accent="#D4FF3D", acc="#D4FF3D",
                 on_acc="#101217", dots=.11, init=.13, heat="#D4FF3D"),
    "light": dict(bg="#F0EEE9", card="#FFFFFF", ink="#101217", muted="#5B5E66", faint="#63666E",
                  line="#101217", lo=.1, hi=.2, chip=.45, accent="#D4FF3D", acc="#101217",
                  on_acc="#101217", dots=.12, init=.1, heat="#101217"),
}
CODE = dict(bg="#171A21", ink="#F0EEE9", kw="#C9B8FF", num="#9A9DA5", str="#D4FF3D")


def e(s: str) -> str:
    return escape(s, quote=True)


# ------------------------------------------------------------ POLICES
@lru_cache(None)
def _font(key, wght=None):
    f = TTFont(HERE / "fonts" / FONTS[key][1])
    if wght and "fvar" in f:
        f = instancer.instantiateVariableFont(f, {"wght": wght})
    return f


def width(text, key, size, wght=400):
    """Largeur réelle du texte en px (avance des glyphes à la bonne graisse)."""
    f = _font(key, wght)
    cmap, hmtx = f.getBestCmap(), f["hmtx"]
    upm = f["head"].unitsPerEm
    return sum(hmtx[cmap.get(ord(c), cmap[ord("n")])][0] for c in text) * size / upm


def wrap(text, key, size, maxw, wght=400):
    lines, cur = [], ""
    for word in text.split():
        test = f"{cur} {word}".strip()
        if cur and width(test, key, size, wght) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = test
    return lines + [cur] if cur else lines


@lru_cache(None)
def _subset(key, chars):
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt"]
    opts.name_IDs = ["*"]
    f = TTFont(HERE / "fonts" / FONTS[key][1])
    s = subset.Subsetter(opts)
    s.populate(text=chars)
    s.subset(f)
    buf = io.BytesIO()
    f.flavor = "woff2"
    f.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def font_css(svg):
    texte = unescape(re.sub(r"<style>.*?</style>|<[^>]+>", " ", svg, flags=re.S))
    chars = "".join(sorted(set(texte) | set(" ")))
    css = []
    for key, (fam, _, style, wght, fb) in FONTS.items():
        if not re.search(rf'class="[^"]*\b{key}\b', svg):
            continue
        css.append(f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{wght};"
                   f"src:url(data:font/woff2;base64,{_subset(key, chars)}) format('woff2')}}"
                   f".{key}{{font-family:'{fam}',{fb};font-style:{style}}}")
    return f"<style>{''.join(css)}</style>"


def write(name, svg):
    (OUT / name).write_text(svg.replace("<!--FONTS-->", font_css(svg)), encoding="utf-8")


# ------------------------------------------------------------ BRIQUES
def defs(t, uid):
    return f"""
  <defs>
    <pattern id="d{uid}" width="18" height="18" patternUnits="userSpaceOnUse">
      <circle cx="9" cy="9" r="1" fill="{t['line']}" fill-opacity="{t['dots']}"/>
    </pattern>
  </defs>"""


def label(t, x, y, text, size=13, anchor="start", tone="faint"):
    """Étiquette façon portfolio : « // SERVICES »."""
    return (f'<text x="{x}" y="{y}" class="jb" font-size="{size}" font-weight="500" letter-spacing="{size * .16:.1f}" '
            f'text-anchor="{anchor}"><tspan fill="{t["acc"]}">//</tspan><tspan fill="{t[tone]}"> {e(text.upper())}</tspan></text>')


def arrow(x, y, s, color, diag=False, sw=1.7):
    """Flèche dessinée (les polices n'ont pas → ni ↗)."""
    if diag:
        d = f"M{x} {y + s / 2}L{x + s} {y - s / 2}M{x + s * .35} {y - s / 2}H{x + s}V{y + s * .15}"
    else:
        d = f"M{x} {y}H{x + s}M{x + s - s * .42} {y - s * .42}L{x + s} {y}L{x + s - s * .42} {y + s * .42}"
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def brackets(x, y, w, h, color, l=16, off=10, sw=1.5):
    """Coins en équerre, comme autour du portrait du portfolio."""
    x0, y0, x1, y1 = x - off, y - off, x + w + off, y + h + off
    d = (f"M{x0} {y0 + l}V{y0}H{x0 + l} M{x1 - l} {y0}H{x1}V{y0 + l} "
         f"M{x1} {y1 - l}V{y1}H{x1 - l} M{x0 + l} {y1}H{x0}V{y1 - l}")
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"/>'


def pill(t, x, y, text, filled, h=34, size=13):
    w = width(text, "jb", size, 600) + 44
    if filled:
        box = f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{t["accent"]}"/>'
        dot, col = t["on_acc"], t["on_acc"]
    else:
        box = (f'<rect x="{x + .75}" y="{y + .75}" width="{w - 1.5:.0f}" height="{h - 1.5}" rx="{h / 2}" fill="none" '
               f'stroke="{t["line"]}" stroke-opacity="{t["chip"]}" stroke-width="1.5"/>')
        dot, col = t["acc"], t["ink"]
    return w, (f'{box}<circle class="dot" cx="{x + 17}" cy="{y + h / 2}" r="3.5" fill="{dot}"/>'
               f'<text x="{x + 28}" y="{y + h / 2 + size * .36:.1f}" class="jb" font-size="{size}" font-weight="600" fill="{col}">{e(text)}</text>')


ANIM = """
    .dot{animation:p 2s ease-in-out infinite} @keyframes p{50%{opacity:.25}}
    .ln{animation:in .45s ease-out backwards} @keyframes in{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}
    .cur{animation:b 1.1s steps(1) infinite} @keyframes b{50%{opacity:0}}
    .flow{stroke-dasharray:6 8;animation:f 1.4s linear infinite} @keyframes f{to{stroke-dashoffset:-28}}
    @media (prefers-reduced-motion:reduce){*{animation:none!important}}"""


# ------------------------------------------------------------ HERO
CODE_LINES = [
    [("kw", "const "), ("ink", "elliott = {")],
    [("ink", "  back: ["), ("str", '"Symfony"'), ("ink", ", "), ("str", '"Django"'), ("ink", ", "), ("str", '"Laravel"'), ("ink", "],")],
    [("ink", "  front: ["), ("str", '"React"'), ("ink", ", "), ("str", '"Vite"'), ("ink", ", "), ("str", '"Tailwind"'), ("ink", "],")],
    [("ink", "  ia: ["), ("str", '"RAG"'), ("ink", ", "), ("str", '"Mistral"'), ("ink", ", "), ("str", '"MCP"'), ("ink", "],")],
    [("ink", "  infra: "), ("str", '"Docker, 57 conteneurs"'), ("ink", ",")],
    [("ink", "  mission: "), ("str", '"Coteo"'), ("ink", ",")],
    [("ink", "};")],
]


def hero(t):
    W, H = 1200, 460
    px, py, pw, ph = 700, 112, 436, 270
    code = []
    for i, parts in enumerate(CODE_LINES):
        y = py + 50 + i * 32
        spans = "".join(f'<tspan fill="{CODE[k]}">{e(s)}</tspan>' for k, s in parts)
        code.append(f'<g class="ln" style="animation-delay:{.15 + i * .12:.2f}s">'
                    f'<text x="{px + 24}" y="{y}" class="jb" font-size="13" fill="{CODE["num"]}">{i + 1:02d}</text>'
                    f'<text x="{px + 60}" y="{y}" class="jb" font-size="14.5" xml:space="preserve">{spans}</text></g>')
    last = py + 50 + (len(CODE_LINES) - 1) * 32
    curx = px + 60 + width("};", "jb", 14.5) + 4
    dw = width("Daens", "is", 132)
    w1, p1 = pill(t, 64, 380, "Disponible pour de nouveaux projets", True)
    _, p2 = pill(t, 64 + w1 + 12, 380, "Calais · remote", False)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Elliott Daens, développeur web freelance full-stack. Disponible pour de nouveaux projets.">
  <title>Elliott Daens, développeur web freelance</title><!--FONTS-->{defs(t, 'h')}
  <style>{ANIM}</style>
  <clipPath id="hc"><rect width="{W}" height="{H}" rx="6"/></clipPath>
  <g clip-path="url(#hc)">
    <rect width="{W}" height="{H}" fill="{t['bg']}"/>
    <rect width="{W}" height="{H}" fill="url(#dh)"/>
    <text x="560" y="470" class="sg" font-size="440" font-weight="700" letter-spacing="-12" fill="none" stroke="{t['line']}" stroke-opacity="{t['init']}" stroke-width="1.5">ED</text>
    <path d="M{W - 210} 0V58H{W}" fill="none" stroke="{t['accent']}" stroke-width="1.5"/>
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="6" fill="none" stroke="{t['line']}" stroke-opacity="{t['hi']}"/>

  <rect x="64" y="46" width="28" height="28" rx="4" fill="{t['accent']}"/>
  <text x="78" y="65" class="jb" font-size="11" font-weight="800" text-anchor="middle" fill="{t['on_acc']}">ED</text>
  <text x="104" y="65" class="jb" font-size="13" font-weight="700" letter-spacing="2" fill="{t['ink']}">ELLIOTT DAENS</text>
  {label(t, W - 236, 65, "Calais — FR", 12, "end", "ink")}

  <text x="56" y="210" class="sg" font-size="112" font-weight="700" letter-spacing="-4" fill="{t['ink']}">Elliott</text>
  <text x="58" y="320" class="is" font-size="132" fill="{t['ink']}">Daens</text>
  <circle cx="{58 + dw + 16:.0f}" cy="309" r="12" fill="{t['accent']}"/>
  <text x="64" y="356" class="jb" font-size="14" font-weight="600" letter-spacing="2.4" fill="{t['acc']}">// DÉVELOPPEUR WEB FREELANCE · FULL-STACK</text>
  {p1}{p2}

  <rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6" fill="{CODE['bg']}"/>
  {brackets(px, py, pw, ph, t['ink'])}
  {''.join(code)}
  <rect class="cur" x="{curx:.0f}" y="{last - 13}" width="8" height="17" fill="{CODE['str']}"/>
  <text x="{px}" y="{py + ph + 42}" class="jb" font-size="12" fill="{t['faint']}">// stack.ts</text>
</svg>"""


# ------------------------------------------------------------ TITRES DE SECTION
SECTIONS = [
    ("projets", "01", "Projets", "Projets", "récents"),
    ("homelab", "02", "Homelab", "Tout tourne", "chez moi"),
    ("ml", "03", "Machine learning", "Des modèles", "mesurés"),
    ("stack", "04", "Stack", "Mes", "outils"),
    ("activite", "05", "Activité", "Sur", "GitHub"),
    ("contact", "06", "Contact", "Un projet ?", "Parlons-en"),
]


def section(t, num, lab, title, italic):
    W, H = 1200, 118
    x2 = width(title + " ", "sg", 52, 700) - 1.5 * len(title) + 4
    end = x2 + width(italic, "is", 60)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{e(title)} {e(italic)}">
  <title>{e(lab)}</title><!--FONTS-->
  {label(t, 2, 30, f"{num} — {lab}", 14)}
  <text x="0" y="98" class="sg" font-size="52" font-weight="700" letter-spacing="-1.5" fill="{t['ink']}">{e(title)}</text>
  <text x="{x2:.0f}" y="98" class="is" font-size="60" fill="{t['ink']}">{e(italic)}</text>
  <line x1="{end + 32:.0f}" y1="84" x2="{W}" y2="84" stroke="{t['line']}" stroke-opacity="{t['hi']}"/>
</svg>"""


# ------------------------------------------------------------ CARTES PROJET
def card(t, uid, w, h, num, tag, title, desc, stack, status, live):
    pad = 32
    body = wrap(desc, "sg", 16.5, w - 2 * pad)[:4]
    tspans = "".join(f'<tspan x="{pad}" dy="{0 if i == 0 else 25}">{e(l)}</tspan>' for i, l in enumerate(body))
    items = []
    for s in stack:
        test = " / ".join(items + [s])
        if width(test, "jb", 13) > w - 2 * pad:
            break
        items.append(s)
    sw = width(status, "jb", 12, 600) + 40
    sx = w - pad - sw
    if live:
        st = (f'<rect x="{sx:.0f}" y="32" width="{sw:.0f}" height="28" rx="14" fill="{t["accent"]}"/>'
              f'<circle class="dot" cx="{sx + 16:.0f}" cy="46" r="3.5" fill="{t["on_acc"]}"/>'
              f'<text x="{sx + 27:.0f}" y="50.5" class="jb" font-size="12" font-weight="600" fill="{t["on_acc"]}">{e(status)}</text>')
    else:
        st = (f'<rect x="{sx + .75:.1f}" y="32.75" width="{sw - 1.5:.0f}" height="26.5" rx="13.25" fill="none" stroke="{t["line"]}" stroke-opacity="{t["chip"]}" stroke-width="1.5"/>'
              f'<circle class="dot" cx="{sx + 16:.0f}" cy="46" r="3.5" fill="{t["acc"]}"/>'
              f'<text x="{sx + 27:.0f}" y="50.5" class="jb" font-size="12" font-weight="600" fill="{t["ink"]}">{e(status)}</text>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{e(title)} : {e(desc)}">
  <title>{e(title)}</title><!--FONTS-->
  <style>{ANIM}</style>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="6" fill="{t['card']}" stroke="{t['line']}" stroke-opacity="{t['hi']}"/>
  {label(t, pad, 51, f"{num} — {tag}", 12.5)}
  {st}
  <text x="{pad}" y="108" class="sg" font-size="34" font-weight="700" letter-spacing="-1" fill="{t['ink']}">{e(title)}</text>
  <text x="{pad}" y="146" class="sg" font-size="16.5" fill="{t['muted']}">{tspans}</text>
  <line x1="{pad}" y1="{h - 62}" x2="{w - pad}" y2="{h - 62}" stroke="{t['line']}" stroke-opacity="{t['lo']}"/>
  <text x="{pad}" y="{h - 28}" class="jb" font-size="13" fill="{t['faint']}">{e(' / '.join(items))}</text>
</svg>"""


WIDE, NARROW, H = 708, 480, 300
CARDS = [  # slug, largeur, étiquette, titre, description, stack, statut, en ligne publique
    ("opalenews", WIDE, "Mission Coteo", "Opalenews",
     "Les événements de la Côte d'Opale : recherche sémantique, assistant IA (RAG), "
     "carte interactive, site en FR / EN / NL, newsletter et modération.",
     ["Symfony 8", "PHP 8.4", "Gemini", "Pinecone", "DeepL", "CI/CD"], "En ligne", True),
    ("contacto", NARROW, "Mission Coteo", "Contacto",
     "Mise en relation pour réseaux d'entreprises : messagerie temps réel, relances "
     "auto, passkeys, IA Mistral. 300+ tests.",
     ["Django 6", "Celery", "Redis", "WebAuthn"], "En prod", False),
    ("runtracker", NARROW, "Produit perso", "RunTracker",
     "Suivi de course à pied : sorties, records, objectifs, import Strava et GPX, "
     "coach IA qui rédige les bilans.",
     ["Django 6", "PostgreSQL", "Groq"], "En ligne", True),
    ("tunnelwa", WIDE, "SaaS", "TunnelWa",
     "SaaS multi-clients qui envoie des séquences de messages WhatsApp Business "
     "(premier message puis relances) via l'API Meta. Webhooks signés HMAC, secrets chiffrés, JWT.",
     ["Node 20", "Express", "PostgreSQL", "React 18", "Vite", "Tailwind"], "En prod", False),
    ("pitwall", WIDE, "Temps réel + ML", "Pit Wall & Paddock",
     "Deux PWA pour la F1 et la MotoGP : direct live, télémétrie, duels, classements, "
     "pronostics par machine learning, chances de titre, rappels Telegram.",
     ["FastAPI", "Socket.IO", "SignalR", "XGBoost", "Docker"], "En prod", False),
    ("pixeloffice", NARROW, "Agents IA", "Pixel Office",
     "Un bureau en pixel art où chaque session Claude Code devient un avatar : "
     "état en direct, chat, courrier entre agents.",
     ["Node", "WebSocket", "MCP", "PWA"], "En prod", False),
]


# ------------------------------------------------------------ BOUTONS
def button(t, text, primary, diag):
    h, size = 56, 15
    w = 30 + width(text, "jb", size, 700) + 14 + 13 + 30
    tw = 30 + width(text, "jb", size, 700) + 14
    if primary:
        box = f'<rect width="{w:.0f}" height="{h}" rx="{h / 2}" fill="{t["accent"]}"/>'
        col = t["on_acc"]
    else:
        box = (f'<rect x=".75" y=".75" width="{w - 1.5:.0f}" height="{h - 1.5}" rx="{(h - 1.5) / 2}" fill="none" '
               f'stroke="{t["line"]}" stroke-opacity="{t["chip"]}" stroke-width="1.5"/>')
        col = t["ink"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h}" viewBox="0 0 {w:.0f} {h}" role="img" aria-label="{e(text)}">
  <title>{e(text)}</title><!--FONTS-->
  {box}
  <text x="30" y="{h / 2 + 5.4:.1f}" class="jb" font-size="{size}" font-weight="700" fill="{col}">{e(text)}</text>
  {arrow(tw, h / 2, 13, col, diag, 1.9)}
</svg>"""


BUTTONS = [  # nom, texte, principal, flèche en diagonale
    ("mail", "Écrivez-moi", True, False),
    ("portfolio", "Portfolio", False, True),
    ("linkedin", "LinkedIn", False, True),
]


# ------------------------------------------------------------ HOMELAB
TILES = [
    ("Mes applis", ["Pit Wall · Paddock", "Virage · Étoiles", "Contacto · TunnelWa", "Pixel Office · Perso Hub"]),
    ("Bots", ["Annonces Vinted", "Discord (discord.js)", "Telegram : alertes", "et commandes à distance"]),
    ("Domotique", ["Home Assistant", "Zigbee2MQTT · Mosquitto", "Frigate (caméras)", "Matter Hub · Piper (voix)"]),
    ("Médias", ["Plex · Tautulli", "Kometa", "Immich (photos)", "media-sorter (maison)"]),
    ("Réseau & sécurité", ["Tailscale (VPN)", "AdGuard Home (DNS)", "Vaultwarden", "HTTPS : Caddy · Nginx"]),
    ("Supervision", ["System Hub (maison)", "Glances · Scrutiny", "Portainer · Diun", "Watchdogs (alertes)"]),
]


def homelab(t):
    W, H = 1200, 560
    nx, ny, nw, nh = 300, 52, 690, 470
    gap, tw, th = 16, 206, 178
    ty0 = ny + 76

    def item(x, y, s):
        return f'<text x="{x}" y="{y}" class="sg" font-size="14.5" fill="{t["muted"]}">{e(s)}</text>'

    tiles = []
    for i, (title, items) in enumerate(TILES):
        x = nx + 20 + (i % 3) * (tw + gap)
        y = ty0 + (i // 3) * (th + gap)
        lines = "".join(item(x + 20, y + 78 + j * 25, it) for j, it in enumerate(items))
        tiles.append(f"""
    <rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="6" fill="{t['bg']}" stroke="{t['line']}" stroke-opacity="{t['lo']}"/>
    <text x="{x + 20}" y="{y + 30}" class="jb" font-size="11.5" font-weight="600" fill="{t['acc']}">{i + 1:02d}</text>
    <text x="{x + 20}" y="{y + 52}" class="sg" font-size="17" font-weight="700" fill="{t['ink']}">{e(title)}</text>{lines}""")

    def side(x, y, w, h, tag, title, lines):
        ls = "".join(item(x + 20, y + 78 + j * 25, l) for j, l in enumerate(lines))
        return f"""
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{t['card']}" stroke="{t['line']}" stroke-opacity="{t['hi']}"/>
    <text x="{x + 20}" y="{y + 30}" class="jb" font-size="11.5" font-weight="600" letter-spacing="1.5" fill="{t['faint']}">{e(tag)}</text>
    <text x="{x + 20}" y="{y + 52}" class="sg" font-size="17" font-weight="700" fill="{t['ink']}">{e(title)}</text>{ls}"""

    def flow(x1, y1, x2, y2, delay=0):
        return (f'<path d="M{x1} {y1} C{(x1 + x2) / 2} {y1} {(x1 + x2) / 2} {y2} {x2} {y2}" class="flow" '
                f'style="animation-delay:-{delay}s" fill="none" stroke="{t["acc"]}" stroke-width="2"/>'
                f'<circle cx="{x2}" cy="{y2}" r="4.5" fill="{t["accent"]}" stroke="{t["on_acc"]}" stroke-width="1.5"/>')

    tg_y = ty0 + th / 2 + gap / 2
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Schéma du homelab : un NAS Ubuntu avec 57 conteneurs Docker (applis, bots, domotique, médias, sécurité, supervision), relié au PC et au téléphone par Tailscale, alertes sur Telegram.">
  <title>Homelab : NAS Ubuntu, 57 conteneurs Docker</title><!--FONTS-->{defs(t, 'l')}
  <style>{ANIM}</style>
  <rect width="{W}" height="{H}" rx="6" fill="{t['bg']}"/>
  <rect width="{W}" height="{H}" rx="6" fill="url(#dl)"/>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="6" fill="none" stroke="{t['line']}" stroke-opacity="{t['hi']}"/>

  <rect x="{nx}" y="{ny}" width="{nw}" height="{nh}" rx="6" fill="{t['card']}" stroke="{t['line']}" stroke-opacity="{t['hi']}"/>
  {brackets(nx, ny, nw, nh, t['acc'], 18, 9, 1.8)}
  <text x="{nx + 24}" y="{ny + 46}" class="sg" font-size="24" font-weight="700" letter-spacing="-.5" fill="{t['ink']}">NAS <tspan class="is" font-size="27" font-weight="400">Ubuntu</tspan></text>
  <text x="{nx + nw - 24}" y="{ny + 44}" class="jb" font-size="12.5" font-weight="600" letter-spacing="1.5" text-anchor="end" fill="{t['acc']}">57 CONTENEURS · GTX 1050 TI · 10 TO</text>
  {''.join(tiles)}

  {label(t, 30, ny + 44, "Via Tailscale", 12)}
  {side(30, ty0, 230, th, "POSTE FIXE", "PC · RTX 5070", ["Entraînement ML", "Sauvegarde restic", "chiffrée chaque nuit", "Syncthing"])}
  {side(30, ty0 + th + gap, 230, th, "MOBILE", "Téléphone", ["Applis en PWA", "Alertes Telegram", "Administration", "à distance"])}
  {flow(260, ty0 + th / 2, nx, ty0 + th / 2, 0)}
  {flow(260, ty0 + th * 1.5 + gap, nx, ty0 + th * 1.5 + gap, .5)}

  {side(1020, tg_y, 150, th, "NOTIFS", "Telegram", ["Alertes", "Caméras", "Rapports", "Commandes"])}
  {flow(nx + nw, ty0 + th + gap / 2, 1020, ty0 + th + gap / 2, .9)}
</svg>"""


if __name__ == "__main__":
    for mode, t in THEMES.items():
        write(f"hero-{mode}.svg", hero(t))
        for slug, num, lab, title, italic in SECTIONS:
            write(f"titre-{slug}-{mode}.svg", section(t, num, lab, title, italic))
        for i, (slug, w, tag, title, desc, stack, status, live) in enumerate(CARDS):
            write(f"card-{slug}-{mode}.svg", card(t, f"c{i}", w, H, f"{i + 1:02d}", tag, title, desc, stack, status, live))
        for name, text, primary, diag in BUTTONS:
            write(f"btn-{name}-{mode}.svg", button(t, text, primary, diag))
        write(f"homelab-{mode}.svg", homelab(t))
    print("ok", len(list(OUT.glob("*.svg"))), "fichiers")
