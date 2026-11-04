"""Génère les cartes de stats (langages + activité) dans le style du profil.

Lancé chaque nuit par .github/workflows/stats.yml.
Besoin d'un jeton GitHub (lecture des dépôts privés) dans la variable GH_TOKEN.
"""
import json
import os
import urllib.request
from collections import defaultdict
from datetime import date

from build_assets import THEMES, e, label, write

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
    W, H = 600, 320
    tons = [(t["accent"], 1)] + [(t["line"], o) for o in (.9, .66, .48, .34, .24, .16, .1)]
    x, bar, items = 32.0, [], []
    for i, (nom, pct, _) in enumerate(data):
        col, op = tons[min(i, len(tons) - 1)]
        w = (W - 64) * pct / 100
        bar.append(f'<rect x="{x:.1f}" y="104" width="{max(w - 3, 1):.1f}" height="14" fill="{col}" fill-opacity="{op}"/>')
        x += w
        cx, cy = 32 + (i % 2) * 284, 166 + (i // 2) * 38
        items.append(f'<rect x="{cx}" y="{cy - 11}" width="12" height="12" rx="2" fill="{col}" fill-opacity="{op}"'
                     + (f' stroke="{t["line"]}" stroke-opacity=".5"' if i == 0 and t["acc"] != t["accent"] else "") + "/>"
                     f'<text x="{cx + 24}" y="{cy}" class="sg" font-size="16.5" font-weight="600" fill="{t["ink"]}">{e(nom)}</text>'
                     f'<text x="{cx + 252}" y="{cy}" class="jb" font-size="13.5" text-anchor="end" fill="{t["faint"]}">{pct:.1f} %</text>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Langages : {e(', '.join(f'{a} {b:.0f} %' for a, b, _ in data))}">
  <title>Langages les plus utilisés</title><!--FONTS-->
  <clipPath id="barclip"><rect x="32" y="104" width="{W - 64}" height="14" rx="3"/></clipPath>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="6" fill="{t['card']}" stroke="{t['line']}" stroke-opacity="{t['hi']}"/>
  {label(t, 32, 52, "Langages", 12.5)}
  <text x="{W - 32}" y="52" class="jb" font-size="12" text-anchor="end" fill="{t['faint']}">{n} dépôts, privés compris</text>
  <g clip-path="url(#barclip)">{''.join(bar)}</g>
  {''.join(items)}
</svg>"""


def carte_activite(t, v):
    W, H = 600, 320
    cal = v["contributionsCollection"]["contributionCalendar"]
    jours = [d for w in cal["weeks"] for d in w["contributionDays"]]
    actuelle, best = series(jours)
    chiffres = [(f"{cal['totalContributions']:,}".replace(",", " "), "contributions / 12 mois"),
                (str(actuelle), "jours d'affilée"), (str(best), "record de série")]
    stats = "".join(
        f'<text x="{32 + i * 196}" y="122" class="sg" font-size="44" font-weight="700" letter-spacing="-1.5" fill="{t["ink"]}">{e(a)}</text>'
        f'<text x="{32 + i * 196}" y="146" class="jb" font-size="10.5" font-weight="500" letter-spacing="1.4" fill="{t["faint"]}">{e(b.upper())}</text>'
        for i, (a, b) in enumerate(chiffres))
    semaines = cal["weeks"][-30:]
    mx = max((d["contributionCount"] for w in semaines for d in w["contributionDays"]), default=1) or 1
    cells, size, g = [], 14, 4
    for wi, w in enumerate(semaines):
        for d in w["contributionDays"]:
            wd = (date.fromisoformat(d["date"]).weekday() + 1) % 7
            c = d["contributionCount"]
            x, y = 32 + wi * (size + g), 172 + wd * (size + g) - 4
            if c == 0:
                cells.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="2" fill="{t["line"]}" fill-opacity="{t["lo"] * .8:.3f}"/>')
            else:
                op = 0.3 + 0.7 * min(1, (c / mx) ** 0.5)
                cells.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="2" fill="{t["heat"]}" fill-opacity="{op:.2f}"/>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{e(chiffres[0][0])} contributions sur 12 mois, série actuelle {actuelle} jours, record {best} jours">
  <title>Activité GitHub</title><!--FONTS-->
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="6" fill="{t['card']}" stroke="{t['line']}" stroke-opacity="{t['hi']}"/>
  {label(t, 32, 52, "Activité", 12.5)}
  <text x="{W - 32}" y="52" class="jb" font-size="12" text-anchor="end" fill="{t['faint']}">maj {date.today().strftime('%d/%m/%Y')}</text>
  {stats}
  {''.join(cells)}
</svg>"""


if __name__ == "__main__":
    v = gql()
    data, n = langues(v)
    for mode, t in THEMES.items():
        write(f"stats-langues-{mode}.svg", carte_langues(t, data, n))
        write(f"stats-activite-{mode}.svg", carte_activite(t, v))
    print("stats ok :", ", ".join(f"{a} {b:.1f}%" for a, b, _ in data))
