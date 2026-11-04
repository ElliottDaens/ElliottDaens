<!-- Visuels faits main : scripts/build_assets.py génère assets/*.svg (clair + sombre) -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg"/>
  <img src="assets/hero-light.svg" width="100%" alt="Elliott Daens, développeur web freelance full-stack. Disponible pour missions."/>
</picture>

<br/>

Je conçois et livre des **applis web complètes** : back **Symfony, Django, Laravel ou Node**, front moderne, **IA intégrée** (RAG, recherche sémantique, agents), puis déploiement **Docker** jusqu'en prod.
En ce moment, en mission avec **Coteo** sur [Opalenews](https://www.opalenews.com/) et Contacto.

## Projets

<sub>Dépôts privés (projets clients et prod perso). Démo ou visite du code sur demande.</sub>

<p>
<a href="https://www.opalenews.com/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-opalenews-dark.svg"/><img src="assets/card-opalenews-light.svg" width="58%" alt="Opalenews : événements de la Côte d'Opale, recherche sémantique et assistant IA. Symfony 8. En ligne."/></picture></a>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-contacto-dark.svg"/><img src="assets/card-contacto-light.svg" width="40%" alt="Contacto : mise en relation pour réseaux d'entreprises. Django 6, Celery, Redis."/></picture>
</p>
<p>
<a href="https://runtracker.daens-elliott-projet-1.fr"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-runtracker-dark.svg"/><img src="assets/card-runtracker-light.svg" width="40%" alt="RunTracker : suivi de course à pied, import Strava et GPX, coach IA. En ligne."/></picture></a>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-tunnelwa-dark.svg"/><img src="assets/card-tunnelwa-light.svg" width="58%" alt="TunnelWa : SaaS multi-clients de séquences WhatsApp Business via l'API Meta. Node, PostgreSQL, React."/></picture>
</p>
<p>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-pitwall-dark.svg"/><img src="assets/card-pitwall-light.svg" width="58%" alt="Pit Wall et Paddock : PWA temps réel F1 et MotoGP avec pronostics ML."/></picture>
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/card-pixeloffice-dark.svg"/><img src="assets/card-pixeloffice-light.svg" width="40%" alt="Pixel Office : bureau pixel art des sessions Claude Code, MCP et WebSocket."/></picture>
</p>

<details>
<summary><b>Plus de projets</b></summary>
<br/>

| Projet | Ce que c'est | Stack |
|:--|:--|:--|
| **Bot Vinted** | Pousse les nouvelles annonces Vinted sur Telegram en quelques secondes | aiogram 3 · httpx HTTP/2 · pydantic |
| **Jeu de fléchettes** | x01, Cricket, Shanghai, Killer… robots de niveau 1 à 10, stats, bilan IA | Flask · SQLite · JS |
| **Go Akademi** | Site vitrine d'un club de jiu-jitsu brésilien à Calais, avec back-office | Laravel 12 · Tailwind 4 |
| **L'Atelier** | Prise de rendez-vous en ligne : créneaux, espace client et admin | Laravel 13 · PHPUnit |
| **Bot Discord** | Modération, niveaux, classements, cartes de rang générées | discord.js 14 · SQLite |
| **Prompt Master** | Réécrit un prompt brut selon le guide Anthropic | FastAPI · Groq |
| **todo-relay** | Une todo par projet, saisie au téléphone, lue par Claude Code | FastAPI · Streamlit · MCP |
| **Perso Hub** | Habitudes, tâches, watchlist ciné (Letterboxd, TMDB) | Streamlit · plotly |

</details>

## Homelab

Tout mon perso tourne en prod sur un **NAS Ubuntu : 57 conteneurs Docker**. Le PC (RTX 5070) sert à entraîner les modèles.

```mermaid
flowchart LR
    PC["💻 PC · RTX 5070<br/>entraînement ML"]
    TEL["📱 Téléphone"]
    PC & TEL -- "VPN Tailscale" --> NAS

    subgraph NAS["🗄️ NAS Ubuntu · 57 conteneurs Docker"]
        direction TB
        APPS["🌐 Mes applis<br/>Pit Wall · Paddock · foot · Contacto<br/>TunnelWa · Pixel Office · Perso Hub"]
        BOTS["🤖 Bots<br/>Vinted · Discord · Telegram"]
        DOMO["🏠 Domotique<br/>Home Assistant · Zigbee2MQTT<br/>Mosquitto · Frigate · Matter"]
        MEDIA["🎬 Médias<br/>Plex · Tautulli · Kometa · Immich"]
        SEC["🔐 Réseau & sécurité<br/>AdGuard Home · Vaultwarden"]
        SUP["📊 Supervision<br/>System Hub · Glances · Scrutiny<br/>Portainer · Diun · watchdogs"]
    end

    PC -- "restic chiffré, chaque nuit" --> NAS
    PC <-- "Syncthing" --> NAS
    SUP -- "alertes" --> TG["📨 Telegram · ntfy"]
    DOMO -- "détection de personne" --> TG
```

<details>
<summary><b>Ce qui tourne tout seul</b></summary>
<br/>

- **System Hub** (fait maison) : CPU, RAM, GPU, disques et conteneurs du NAS **et** du PC, avec historique
- **Watchdogs** : sauvegarde du PC absente depuis 48 h, capteurs Home Assistant, Zigbee hors ligne, disque à 90 %
- **Santé des disques** (Scrutiny) et **nouvelles versions d'images** (Diun)
- **Ménage Docker** chaque semaine, **ventilateur GPU** piloté par script (NVML)
- **Tri des médias** automatique dès qu'un fichier arrive
- **Sessions Claude Code** sur le NAS pour l'administration, toutes visibles dans Pixel Office

</details>

## Machine learning

Des modèles sur le sport, **mesurés contre une référence simple** plutôt que vendus au pourcentage flatteur.

| | Modèles | Résultat |
|:--|:--|:--|
| **F1** | Régression logistique, XGBoost calibré, Elo, Monte-Carlo (titre) | 2022-2025, 92 GP : **62 %** de vainqueurs trouvés contre 55 % pour « le poleman gagne » ; log-loss 1,08 contre 1,54 |
| **Ligue 1 & C1** | Poisson / Dixon-Coles sur les xG, Elo, pi-ratings | Log-loss 0,989 en walk-forward 2016-2025 : **au niveau des bookmakers** (0,983) |
| **MotoGP** | Régression logistique, gradient boosting | ~30 % de vainqueurs trouvés, contre 18 à 31 % pour les repères simples |
| **OpenTTD** | Apprentissage par renforcement (PPO masqué) | En cours : 250 M de pas, +545 000 £ en moyenne sur 48 parties |

## Stack

<p>
<img src="https://skillicons.dev/icons?i=php,symfony,laravel,python,django,fastapi,flask,nodejs,express&theme=dark" height="40" alt="Back : PHP, Symfony, Laravel, Python, Django, FastAPI, Flask, Node.js, Express"/>
<br/>
<img src="https://skillicons.dev/icons?i=html,css,js,react,vite,tailwind,postgres,mysql,redis,sqlite&theme=dark" height="40" alt="Front et données : HTML, CSS, JavaScript, React, Vite, Tailwind, PostgreSQL, MySQL, Redis, SQLite"/>
<br/>
<img src="https://skillicons.dev/icons?i=docker,linux,nginx,caddy,cloudflare,githubactions,sklearn,pytorch,homeassistant&theme=dark" height="40" alt="Infra et ML : Docker, Linux, Nginx, Caddy, Cloudflare, GitHub Actions, scikit-learn, PyTorch, Home Assistant"/>
</p>

## Activité

<!-- Mise à jour chaque nuit par .github/workflows/metrics.yml -->
<p>
<img src="metrics/languages.svg" width="49%" alt="Langages les plus utilisés"/>
<img src="metrics/isocalendar.svg" width="49%" alt="Calendrier isométrique des contributions"/>
</p>

## Contact

Un site, une appli, une mission freelance ? Je réponds vite.

<p>
<a href="mailto:daenselliott691@gmail.com"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-mail-dark.svg"/><img src="assets/btn-mail-light.svg" height="48" alt="Écrivez-moi : daenselliott691@gmail.com"/></picture></a>
<a href="https://www.linkedin.com/in/elliott-daens-906b8b32a/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/btn-linkedin-dark.svg"/><img src="assets/btn-linkedin-light.svg" height="48" alt="LinkedIn : Elliott Daens"/></picture></a>
</p>

<sub>Hors du code : jiu-jitsu brésilien, musculation, Formule 1, cinéma, gaming.</sub>
