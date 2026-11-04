"""Génère les cartes de stats (langages + activité) dans le style du profil.

Lancé chaque nuit par .github/workflows/stats.yml.
Besoin d'un jeton GitHub (lecture des dépôts privés) dans la variable GH_TOKEN.
"""
import json
import os
import urllib.request
from collections import defaultdict
from datetime import date

from build_assets import MONO, OUT, SANS, THEMES, defs, e

EXCLUS = {
    "coteo/badgemoi2024", "coteo-technique/Opalenews", "ElliottDaens/ElliottDaens",
    "ElliottDaens/lorette", "ElliottDaens/lorette-anniv", "ElliottDaens/portail_habitat-infra",
    "vincent-vnst/wmi-24-26-daens-elliott", "emiliepoisson/TableauxBordsDescriptif",
}
IGNORES = {"Dockerfile", "Shell", "Batchfile", "PowerShell", "Procfile", "Makefile"}

QUERY = """
query {
  viewer {
    contributionsCollection {
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
      totalCommitContributions restrictedContributionsCount
    }
    repositories(first: 100, isFork: false, ownerAffiliations: [OWNER, COLLABORATOR, ORGANIZATION_MEMBER]) {
      nodes { nameWithOwner languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
        edges { size node { name color } } } }
    }
  }
}"""


def gql():
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=json.dumps({"query": QUERY}).encode(),
        headers={"Authorization": f"bearer {os.environ['GH_TOKEN']}", "User-Agent": "profile-stats"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(data["errors"])
    return data["data"]["viewer"]


def langues(v):
    """Chaque dépôt pèse autant : on additionne la part de chaque langage par dépôt."""
    poids, couleurs, n = defaultdict(float), {}, 0
    for repo in v["repositories"]["nodes"]:
        if repo["nameWithOwner"] in EXCLUS:
            continue
        edges = [x for x in repo["languages"]["edges"] if x["node"]["name"] not in IGNORES]
        total = sum(x["size"] for x in edges)
        if not total:
            continue
        n += 1
        for x in edges:
            poids[x["node"]["name"]] += x["size"] / total
            couleurs[x["node"]["name"]] = x["node"]["color"] or "#8b949e"
    somme = sum(poids.values())
    top = sorted(poids.items(), key=lambda kv: -kv[1])[:7]
    reste = somme - sum(p for _, p in top)
    res = [(nom, p / somme * 100, couleurs[nom]) for nom, p in top]
    if reste / somme > 0.005:
        res.append(("Autres", reste / somme * 100, "#6e7681"))
    return res, n


def series(jours):
    actuelle = 0
    for j in reversed(jours):
        if j["contributionCount"]:
            actuelle += 1
        elif j["date"] != date.today().isoformat():
            break
    best = cur = 0
    for j in jours:
        cur = cur + 1 if j["contributionCount"] else 0
        best = max(best, cur)
    return actuelle, best


def carte_langues(t, data, n):
    W, H = 600, 310
    x, bar = 32, []
    for nom, pct, col in data:
        w = (W - 64) * pct / 100
        bar.append(f'<rect x="{x:.1f}" y="92" width="{max(w - 2, 1):.1f}" height="12" fill="{col}"/>')
        x += w
    items = []
    for i, (nom, pct, col) in enumerate(data):
        cx, cy = 32 + (i % 2) * 280, 146 + (i // 2) * 36
        items.append(f'<circle cx="{cx + 6}" cy="{cy - 5}" r="6" fill="{col}"/>'
                     f'<text x="{cx + 22}" y="{cy}" class="s" font-size="16" font-weight="600" fill="{t["text"]}">{e(nom)}</text>'
                     f'<text x="{cx + 250}" y="{cy}" class="m" font-size="14" text-anchor="end" fill="{t["muted"]}">{pct:.1f} %</text>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Langages : {e(', '.join(f'{a} {b:.0f} %' for a, b, _ in data))}">
  <title>Langages les plus utilisés</title>{defs(t, 'sl')}
  <style>.s{{font-family:{SANS}}} .m{{font-family:{MONO}}}</style>
  <clipPath id="barclip"><rect x="32" y="92" width="{W - 64}" height="12" rx="6"/></clipPath>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="20" fill="{t['card']}" stroke="{t['border']}"/>
  <text x="32" y="50" class="m" font-size="13" font-weight="700" letter-spacing="1.5" fill="url(#gsl)">LANGAGES</text>
  <text x="{W - 32}" y="50" class="s" font-size="13" text-anchor="end" fill="{t['muted']}">sur {n} dépôts, privés compris</text>
  <g clip-path="url(#barclip)">{''.join(bar)}</g>
  {''.join(items)}
</svg>"""


def carte_activite(t, v):
    W, H = 600, 310
    cal = v["contributionsCollection"]["contributionCalendar"]
    jours = [d for w in cal["weeks"] for d in w["contributionDays"]]
    actuelle, best = series(jours)
    chiffres = [(f"{cal['totalContributions']:,}".replace(",", " "), "contributions sur 12 mois"),
                (str(actuelle), "jours d'affilée"), (str(best), "record de série")]
    stats = "".join(
        f'<text x="{32 + i * 186}" y="112" class="s" font-size="34" font-weight="800" fill="{t["text"] if i else "url(#gsa)"}">{e(a)}</text>'
        f'<text x="{32 + i * 186}" y="136" class="s" font-size="13.5" fill="{t["muted"]}">{e(b)}</text>'
        for i, (a, b) in enumerate(chiffres))
    # mini calendrier des 26 dernières semaines
    semaines = cal["weeks"][-30:]
    mx = max((d["contributionCount"] for w in semaines for d in w["contributionDays"]), default=1) or 1
    cells, size, g = [], 14, 4
    for wi, w in enumerate(semaines):
        for d in w["contributionDays"]:
            wd = (date.fromisoformat(d["date"]).weekday() + 1) % 7
            c = d["contributionCount"]
            op = 0 if c == 0 else 0.25 + 0.75 * min(1, (c / mx) ** 0.5)
            fill = t["chip"] if c == 0 else t["a2"]
            cells.append(f'<rect x="{32 + wi * (size + g)}" y="{160 + wd * (size + g)}" width="{size}" height="{size}" rx="3" fill="{fill}"'
                         + (f' fill-opacity="{op:.2f}"' if c else "") + "/>")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{e(chiffres[0][0])} contributions sur 12 mois, série actuelle {actuelle} jours, record {best} jours">
  <title>Activité GitHub</title>{defs(t, 'sa')}
  <style>.s{{font-family:{SANS}}} .m{{font-family:{MONO}}}</style>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="20" fill="{t['card']}" stroke="{t['border']}"/>
  <text x="32" y="50" class="m" font-size="13" font-weight="700" letter-spacing="1.5" fill="url(#gsa)">ACTIVITÉ</text>
  <text x="{W - 32}" y="50" class="s" font-size="13" text-anchor="end" fill="{t['muted']}">mis à jour le {date.today().strftime('%d/%m/%Y')}</text>
  {stats}
  {''.join(cells)}
</svg>"""


if __name__ == "__main__":
    v = gql()
    data, n = langues(v)
    for mode, t in THEMES.items():
        (OUT / f"stats-langues-{mode}.svg").write_text(carte_langues(t, data, n), encoding="utf-8")
        (OUT / f"stats-activite-{mode}.svg").write_text(carte_activite(t, v), encoding="utf-8")
    print("stats ok :", ", ".join(f"{a} {b:.1f}%" for a, b, _ in data))
