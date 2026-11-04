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




# ---------------------------------------------------------------- BOUTONS
ICON_MAIL = '<path d="M-8 -5.5h16v11h-16z M-8 -5.5l8 6.5 8-6.5" fill="none" stroke="#fff" stroke-width="1.8" stroke-linejoin="round"/>'
ICON_IN = '<text x="0" y="5" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" font-weight="800" fill="#fff">in</text>'


def button(t, label, sub, w, icon):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="64" viewBox="0 0 {w} 64" role="img" aria-label="{e(label)} : {e(sub)}">
  <title>{e(label)}</title>{defs(t, 'btn')}
  <style>.s{{font-family:{SANS}}}</style>
  <rect x=".5" y=".5" width="{w - 1}" height="63" rx="16" fill="{t['card']}" stroke="{t['border']}"/>
  <rect x="12" y="12" width="40" height="40" rx="12" fill="url(#gbtn)"/>
  <g transform="translate(32 32)">{icon}</g>
  <text x="66" y="28" class="s" font-size="17" font-weight="700" fill="{t['text']}">{e(label)}</text>
  <text x="66" y="47" class="s" font-size="13" fill="{t['muted']}">{e(sub)}</text>
  <text x="{w - 22}" y="38" class="s" font-size="20" text-anchor="end" fill="{t['muted']}">→</text>
</svg>"""


# ---------------------------------------------------------------- HOMELAB
TILES = [
    ("Mes applis", ["Pit Wall · Paddock", "Virage · Étoiles", "Contacto · TunnelWa", "Pixel Office · Perso Hub"]),
    ("Bots", ["Vinted → Telegram", "Discord (discord.js)", "Telegram : alertes", "et commandes à distance"]),
    ("Domotique", ["Home Assistant", "Zigbee2MQTT · Mosquitto", "Frigate (caméras)", "Matter Hub · Piper (voix)"]),
    ("Médias", ["Plex · Tautulli", "Kometa", "Immich (photos)", "media-sorter (maison)"]),
    ("Réseau & sécurité", ["Tailscale (VPN)", "AdGuard Home (DNS)", "Vaultwarden", "HTTPS : Caddy · Nginx"]),
    ("Supervision", ["System Hub (maison)", "Glances · Scrutiny", "Portainer · Diun", "watchdogs → Telegram"]),
]


def homelab(t):
    W, H = 1200, 540
    nx, ny, nw, nh = 300, 36, 690, 468
    gap, tw, th = 16, 206, 178
    tiles = []
    for i, (title, items) in enumerate(TILES):
        x = nx + 20 + (i % 3) * (tw + gap)
        y = ny + 74 + (i // 3) * (th + gap)
        lines = "".join(f'<text x="{x + 20}" y="{y + 76 + j * 26}" class="s" font-size="14.5" fill="{t["muted"]}">{e(it)}</text>'
                        for j, it in enumerate(items))
        tiles.append(f"""
    <rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="14" fill="{t['bg']}" stroke="{t['border']}"/>
    <rect x="{x + 20}" y="{y + 24}" width="8" height="8" rx="2" fill="url(#gl)"/>
    <text x="{x + 36}" y="{y + 33}" class="s" font-size="16.5" font-weight="700" fill="{t['text']}">{e(title)}</text>{lines}""")

    def side(x, y, w, h, title, lines):
        ls = "".join(f'<text x="{x + 20}" y="{y + 76 + j * 26}" class="s" font-size="14.5" fill="{t["muted"]}">{e(l)}</text>'
                     for j, l in enumerate(lines))
        return f"""
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{t['card']}" stroke="{t['border']}"/>
    <text x="{x + 20}" y="{y + 33}" class="s" font-size="16.5" font-weight="700" fill="{t['text']}">{e(title)}</text>{ls}"""

    def flow(x1, y1, x2, y2, delay=0):
        return (f'<path d="M{x1} {y1} C{(x1 + x2) / 2} {y1} {(x1 + x2) / 2} {y2} {x2} {y2}" class="flow" '
                f'style="animation-delay:-{delay}s" fill="none" stroke="url(#gl)" stroke-width="2.2"/>'
                f'<circle cx="{x2}" cy="{y2}" r="4" fill="{t["a2"]}"/>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Schéma du homelab : un NAS Ubuntu avec 57 conteneurs Docker (applis, bots, domotique, médias, sécurité, supervision), relié au PC et au téléphone par Tailscale, alertes sur Telegram.">
  <title>Homelab : NAS Ubuntu, 57 conteneurs Docker</title>{defs(t, 'l')}
  <style>.s{{font-family:{SANS}}} .m{{font-family:{MONO}}}
    .flow{{stroke-dasharray:6 8;animation:f 1.4s linear infinite}} @keyframes f{{to{{stroke-dashoffset:-28}}}}
    @media (prefers-reduced-motion:reduce){{.flow{{animation:none}}}}</style>
  <rect width="{W}" height="{H}" rx="24" fill="{t['bg']}"/>
  <rect width="{W}" height="{H}" rx="24" fill="url(#pl)"/>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="23.5" fill="none" stroke="{t['border']}"/>

  <rect x="{nx}" y="{ny}" width="{nw}" height="{nh}" rx="20" fill="{t['card']}" stroke="url(#gl)" stroke-width="1.5"/>
  <text x="{nx + 24}" y="{ny + 44}" class="s" font-size="22" font-weight="800" fill="{t['text']}">NAS Ubuntu</text>
  <text x="{nx + nw - 24}" y="{ny + 44}" class="m" font-size="14" text-anchor="end" fill="url(#gl)" font-weight="700">57 conteneurs Docker · GTX 1050 Ti · 10 To</text>
  {''.join(tiles)}

  <text x="30" y="{ny + 44}" class="m" font-size="14" font-weight="700" fill="url(#gl)">accès via Tailscale</text>
  {side(30, ny + 74, 230, th, "PC · RTX 5070", ["Entraînement ML", "Sauvegarde restic", "chiffrée chaque nuit", "Syncthing"])}
  {side(30, ny + 74 + th + gap, 230, th, "Téléphone", ["Applis en PWA", "Alertes Telegram", "Administration à distance"])}
  {flow(260, ny + 74 + th / 2, nx, ny + 74 + th / 2, 0)}
  {flow(260, ny + 74 + th * 1.5 + gap, nx, ny + 74 + th * 1.5 + gap, .5)}

  {side(1020, ny + 74 + th / 2 + gap / 2, 150, th, "Telegram", ["Alertes", "Caméras", "Rapports", "Commandes"])}
  {flow(nx + nw, ny + 74 + th + gap / 2, 1020, ny + 74 + th + gap / 2, .9)}
</svg>"""


if __name__ == "__main__":
    for mode, t in THEMES.items():
        (OUT / f"hero-{mode}.svg").write_text(hero(t), encoding="utf-8")
        for i, (slug, w, tag, title, desc, chips, status) in enumerate(CARDS):
            (OUT / f"card-{slug}-{mode}.svg").write_text(
                card(t, f"c{i}", w, H, tag, title, desc, chips, status), encoding="utf-8")
        (OUT / f"btn-linkedin-{mode}.svg").write_text(
            button(t, "LinkedIn", "Elliott Daens", 250, ICON_IN), encoding="utf-8")
        (OUT / f"btn-mail-{mode}.svg").write_text(
            button(t, "Écrivez-moi", "daenselliott691@gmail.com", 320, ICON_MAIL), encoding="utf-8")
        (OUT / f"homelab-{mode}.svg").write_text(homelab(t), encoding="utf-8")
    print("ok", len(list(OUT.glob("*.svg"))), "fichiers")
