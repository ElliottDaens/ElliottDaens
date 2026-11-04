"""Génère les visuels SVG du profil (thèmes clair et sombre).

Usage : python scripts/build_assets.py  -> écrit dans assets/
"""
from html import escape
from pathlib import Path
from textwrap import wrap

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

SANS = "'Inter','Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','Cascadia Code','SF Mono',Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": dict(bg="#0d1117", card="#161b22", border="#30363d", text="#e6edf3",
                 muted="#8b949e", chip="#21262d", grid="#ffffff", grid_op=0.035,
                 a1="#818cf8", a2="#22d3ee", a3="#c084fc", ok="#3fb950", blob=0.55),
    "light": dict(bg="#ffffff", card="#f6f8fa", border="#d0d7de", text="#1f2328",
                  muted="#59636e", chip="#eaeef2", grid="#000000", grid_op=0.045,
                  a1="#4f46e5", a2="#0891b2", a3="#9333ea", ok="#1a7f37", blob=0.30),
}


def e(s: str) -> str:
    return escape(s, quote=True)


def defs(t, uid):
    return f"""
  <defs>
    <linearGradient id="g{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['a1']}"/><stop offset=".55" stop-color="{t['a3']}"/><stop offset="1" stop-color="{t['a2']}"/>
    </linearGradient>
    <pattern id="p{uid}" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="{t['grid']}" stroke-opacity="{t['grid_op']}"/>
    </pattern>
    <filter id="b{uid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>
  </defs>"""


# ------------------------------------------------------------------ HERO
STACK = [
    ("symfony", "Symfony 8 · PHP 8.4"),
    ("django", "Django 6 · Celery"),
    ("laravel", "Laravel 12 / 13"),
    ("node", "Node · React · Vite"),
    ("ia", "RAG · Mistral · MCP"),
    ("infra", "Docker · 57 conteneurs"),
]


def hero(t):
    W, H = 1200, 400
    lines = []
    for i, (k, v) in enumerate(STACK):
        y = 170 + i * 30
        lines.append(f"""
    <g class="ln" style="animation-delay:{0.6 + i * 0.35:.2f}s">
      <text x="790" y="{y}" class="m" fill="{t['a2']}">❯</text>
      <text x="812" y="{y}" class="m" fill="{t['muted']}">{e(k)}</text>
      <text x="898" y="{y}" class="m" fill="{t['text']}">{e(v)}</text>
    </g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Elliott Daens, développeur web freelance">
  <title>Elliott Daens, développeur web freelance</title>{defs(t, 'h')}
  <style>
    .s{{font-family:{SANS}}} .m{{font-family:{MONO};font-size:15px}}
    .blob{{animation:drift 14s ease-in-out infinite alternate}}
    .blob2{{animation:drift 18s ease-in-out infinite alternate-reverse}}
    @keyframes drift{{from{{transform:translate(0,0)}}to{{transform:translate(60px,30px)}}}}
    .cur{{animation:blink 1.1s steps(1) infinite}}
    @keyframes blink{{50%{{opacity:0}}}}
    .ln{{animation:in .5s ease-out backwards}}
    @keyframes in{{from{{opacity:0;transform:translateX(-8px)}}to{{opacity:1;transform:none}}}}
    .pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2s ease-out infinite}}
    @keyframes pulse{{0%{{transform:scale(1);opacity:.6}}100%{{transform:scale(2.6);opacity:0}}}}
    @media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
  </style>
  <clipPath id="clip"><rect width="{W}" height="{H}" rx="24"/></clipPath>
  <g clip-path="url(#clip)">
    <rect width="{W}" height="{H}" fill="{t['bg']}"/>
    <g opacity="{t['blob']}" filter="url(#bh)">
      <circle class="blob" cx="260" cy="70" r="170" fill="{t['a1']}"/>
      <circle class="blob2" cx="1060" cy="380" r="160" fill="{t['a2']}"/>
      <circle class="blob" cx="640" cy="440" r="120" fill="{t['a3']}"/>
    </g>
    <rect width="{W}" height="{H}" fill="url(#ph)"/>
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="23.5" fill="none" stroke="{t['border']}"/>

  <text x="64" y="92" class="m" fill="{t['muted']}">~/elliott $ whoami<tspan class="cur" fill="{t['a2']}"> ▌</tspan></text>
  <text x="61" y="174" class="s" font-size="70" font-weight="800" letter-spacing="-2" fill="{t['text']}">Elliott Daens</text>
  <text x="64" y="220" class="s" font-size="26" font-weight="700" fill="url(#gh)">Développeur web freelance · full-stack</text>
  <text x="64" y="258" class="s" font-size="18" fill="{t['muted']}">Applis web de bout en bout, IA intégrée, déployées en prod sur Docker.</text>

  <rect x="52" y="298" width="240" height="38" rx="19" fill="{t['card']}" stroke="{t['border']}"/>
  <circle class="pulse" cx="73" cy="317" r="5" fill="{t['ok']}"/>
  <circle cx="73" cy="317" r="5" fill="{t['ok']}"/>
  <text x="88" y="322" class="s" font-size="15" font-weight="600" fill="{t['text']}">Disponible pour missions</text>
  <rect x="304" y="298" width="124" height="38" rx="19" fill="{t['card']}" stroke="{t['border']}"/>
  <text x="366" y="322" class="s" font-size="15" text-anchor="middle" fill="{t['muted']}">France · remote</text>

  <rect x="760" y="70" width="390" height="276" rx="16" fill="{t['card']}" fill-opacity=".92" stroke="{t['border']}"/>
  <circle cx="784" cy="94" r="6" fill="#ff5f57"/><circle cx="804" cy="94" r="6" fill="#febc2e"/><circle cx="824" cy="94" r="6" fill="#28c840"/>
  <text x="955" y="99" class="m" font-size="13" text-anchor="middle" fill="{t['muted']}">stack.sh</text>
  <line x1="760" y1="114" x2="1150" y2="114" stroke="{t['border']}"/>
  <text x="790" y="142" class="m" fill="{t['muted']}"># ce que je livre</text>{''.join(lines)}
</svg>"""


# ---------------------------------------------------------------- CARTES
def card(t, uid, w, h, tag, title, desc, chips, status):
    pad = 32
    body = wrap(desc, int((w - 2 * pad) / 9.2))[:4]
    tspans = "".join(
        f'<tspan x="{pad}" dy="{0 if i == 0 else 26}">{e(l)}</tspan>' for i, l in enumerate(body))
    cx, cy, chips_svg = pad, h - 60, []
    for c in chips:
        cw = int(len(c) * 8 + 24)
        if cx + cw > w - pad:
            break
        chips_svg.append(
            f'<rect x="{cx}" y="{cy}" width="{cw}" height="30" rx="15" fill="{t["chip"]}"/>'
            f'<text x="{cx + cw / 2}" y="{cy + 20}" class="m" font-size="13" text-anchor="middle" fill="{t["text"]}">{e(c)}</text>')
        cx += cw + 8
    sw = int(len(status) * 7.8 + 36)
    sx = w - pad - sw
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{e(title)} : {e(desc)}">
  <title>{e(title)}</title>{defs(t, uid)}
  <style>.s{{font-family:{SANS}}} .m{{font-family:{MONO}}}
    .dot{{animation:p 2s ease-in-out infinite}} @keyframes p{{50%{{opacity:.3}}}}
    @media (prefers-reduced-motion:reduce){{.dot{{animation:none}}}}</style>
  <clipPath id="k{uid}"><rect width="{w}" height="{h}" rx="20"/></clipPath>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="20" fill="{t['card']}" stroke="{t['border']}"/>
  <rect width="{w}" height="4" fill="url(#g{uid})" clip-path="url(#k{uid})"/>
  <text x="{pad}" y="56" class="m" font-size="13" font-weight="700" letter-spacing="1.5" fill="url(#g{uid})">{e(tag.upper())}</text>
  <rect x="{sx}" y="36" width="{sw}" height="28" rx="14" fill="none" stroke="{t['border']}"/>
  <circle class="dot" cx="{sx + 16}" cy="50" r="4.5" fill="{t['ok']}"/>
  <text x="{sx + 28}" y="55" class="s" font-size="13" fill="{t['muted']}">{e(status)}</text>
  <text x="{pad}" y="106" class="s" font-size="31" font-weight="800" letter-spacing="-.6" fill="{t['text']}">{e(title)}</text>
  <text x="{pad}" y="146" class="s" font-size="17" fill="{t['muted']}">{tspans}</text>
  {''.join(chips_svg)}
</svg>"""


WIDE, NARROW, H = 700, 480, 340
CARDS = [
    ("opalenews", WIDE, "Mission Coteo", "Opalenews",
     "Les événements de la Côte d'Opale : recherche sémantique, assistant IA (RAG), "
     "carte interactive, site en FR / EN / NL, newsletter et modération.",
     ["Symfony 8", "PHP 8.4", "Gemini", "Pinecone", "DeepL", "CI/CD"], "En ligne"),
    ("contacto", NARROW, "Mission Coteo", "Contacto",
     "Mise en relation pour réseaux d'entreprises : messagerie temps réel, relances "
     "auto, passkeys, IA Mistral. 300+ tests.",
     ["Django 6", "Celery", "Redis", "WebAuthn"], "En prod"),
    ("runtracker", NARROW, "Produit perso", "RunTracker",
     "Suivi de course à pied : sorties, records, objectifs, import Strava et GPX, "
     "coach IA qui rédige les bilans.",
     ["Django 6", "PostgreSQL", "Groq"], "En ligne"),
    ("tunnelwa", WIDE, "SaaS", "TunnelWa",
     "SaaS multi-clients qui envoie des séquences de messages WhatsApp Business "
     "(premier message puis relances) via l'API Meta. Webhooks signés HMAC, secrets chiffrés, JWT.",
     ["Node 20", "Express", "PostgreSQL", "React 18", "Vite", "Tailwind"], "En prod"),
    ("pitwall", WIDE, "Temps réel + ML", "Pit Wall & Paddock",
     "Deux PWA pour la F1 et la MotoGP : direct live, télémétrie, duels, classements, "
     "pronostics par machine learning, chances de titre, rappels Telegram.",
     ["FastAPI", "Socket.IO", "SignalR", "XGBoost", "Docker"], "En prod"),
    ("pixeloffice", NARROW, "Agents IA", "Pixel Office",
     "Un bureau en pixel art où chaque session Claude Code devient un avatar : "
     "état en direct, chat, courrier entre agents.",
     ["Node", "WebSocket", "MCP", "PWA"], "En prod"),
]


def button(t, label, sub, w):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="56" viewBox="0 0 {w} 56" role="img" aria-label="{e(label)} : {e(sub)}">
  <title>{e(label)}</title>{defs(t, 'btn')}
  <style>.s{{font-family:{SANS}}}</style>
  <rect x=".5" y=".5" width="{w - 1}" height="55" rx="27.5" fill="{t['card']}" stroke="{t['border']}"/>
  <circle cx="30" cy="28" r="11" fill="url(#gbtn)"/>
  <text x="52" y="25" class="s" font-size="16" font-weight="700" fill="{t['text']}">{e(label)}</text>
  <text x="52" y="43" class="s" font-size="12.5" fill="{t['muted']}">{e(sub)}</text>
</svg>"""


for mode, t in THEMES.items():
    (OUT / f"hero-{mode}.svg").write_text(hero(t), encoding="utf-8")
    for i, (slug, w, tag, title, desc, chips, status) in enumerate(CARDS):
        (OUT / f"card-{slug}-{mode}.svg").write_text(
            card(t, f"c{i}", w, H, tag, title, desc, chips, status), encoding="utf-8")
    (OUT / f"btn-linkedin-{mode}.svg").write_text(button(t, "LinkedIn", "Elliott Daens", 230), encoding="utf-8")
    (OUT / f"btn-mail-{mode}.svg").write_text(button(t, "Écrivez-moi", "daenselliott691@gmail.com", 290), encoding="utf-8")

print("ok", len(list(OUT.glob("*.svg"))), "fichiers")
