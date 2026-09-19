<div align="center">

# 🎵 TikTok IA Analytics

### Analyses avancées & Insights IA pour optimiser votre présence TikTok

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D%2016.x-339933?logo=node.js&logoColor=white)](https://nodejs.org)
[![Express](https://img.shields.io/badge/Express-4.x-000000?logo=express&logoColor=white)](https://expressjs.com)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/gunout/Analytics-seo-tiktok/pulls)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-red)](https://github.com/gunout)

**Dashboard d'analyse TikTok avec données réelles, scoring SEO et recommandations stratégiques.**

[📸 Aperçu](#-aperçu) · [🚀 Installation](#-installation) · [📖 Utilisation](#-utilisation) · [🛠️ Stack](#️-stack-technique) · [🤝 Contribution](#-contribution)

</div>

---

## 📋 Table des matières

- [Présentation](#-présentation)
- [Fonctionnalités](#-fonctionnalités)
- [Aperçu](#-aperçu)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Stack technique](#️-stack-technique)
- [Structure du projet](#-structure-du-projet)
- [API Reference](#-api-reference)
- [Roadmap](#-roadmap)
- [Contribuer](#-contribution)
- [Licence](#-licence)
- [Auteur](#-auteur)

---

## 🎯 Présentation

**TikTok IA Analytics** est un dashboard web qui analyse en temps réel un compte TikTok à partir de son `@username`. Il combine :

- 🎨 **Une interface moderne** aux couleurs officielles TikTok (cyan `#25F4EE` / rose `#FE2C55`)
- 📊 **Un moteur de scoring SEO** (`SEO PowerScore™`) basé sur les métadonnées du profil
- 🤖 **Des recommandations stratégiques** générées localement (bio, fréquence de publication, engagement)
- 🌐 **Deux modes de fonctionnement** : version locale avec backend Node.js ou version single-page sans backend

Le projet est pensé pour être **simple à lancer**, **facile à personnaliser** et **utilisable sans clé API** pour une première évaluation.

---

## ✨ Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| 🔍 **Analyse par username** | Accepte `@username`, `username` ou une URL TikTok complète |
| 📈 **SEO PowerScore™** | Score sur 100 basé sur la bio, l'activité et la complétude du profil |
| 🏷️ **Hashtags & Keywords** | Suggestions contextuelles adaptées à la niche détectée |
| 💡 **Plan d'action SEO** | Recommandations concrètes (bio, rythme, engagement, sons tendance) |
| 🎨 **UI TikTok authentique** | Palette officielle, effets néon, dégradés cyan/rose |
| ⚡ **Deux modes** | `index.html` (oEmbed direct, zéro backend) ou `indexLocalhost.html` + `server.js` (backend Express) |
| 📱 **Responsive** | Optimisé mobile / tablette / desktop |
| 🌐 **Sans clé API** | Fonctionne via l'API oEmbed publique de TikTok |

---

## 📸 Aperçu

> *Ajoute ici une capture d'écran de ton dashboard*
> Exemple : `![Aperçu du dashboard](docs/preview.png)`

    ┌─────────────────────────────────────────────────────────┐
    │  🎵 TikTok Scope® Real                                  │
    │  Audit SEO & engagement — zéro backend requis           │
    ├─────────────────────────────────────────────────────────┤
    │  [ @khaby.lame                              ] [Analyser]│
    ├─────────────────────────────────────────────────────────┤
    │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │
    │  │ @username    │ │ SEO Score    │ │ Keywords     │     │
    │  │ Force: Fort  │ │   78/100     │ │ #fyp #viral  │     │
    │  └──────────────┘ └──────────────┘ └──────────────┘     │
    └─────────────────────────────────────────────────────────┘

---

## 🚀 Installation

### Prérequis

- **Node.js** ≥ 16.x ([télécharger](https://nodejs.org))
- **npm** ≥ 8.x (inclus avec Node.js)
- Un navigateur moderne (Chrome, Firefox, Edge, Safari)

### Étapes

    git clone https://github.com/gunout/Analytics-seo-tiktok.git
    cd Analytics-seo-tiktok
    npm install
    npm start

Le serveur démarre sur **http://localhost:3000**.

### Mode alternatif — Sans backend

Pour utiliser la version **single-page** (aucun serveur requis), ouvre simplement le fichier `index.html` dans ton navigateur :

    open index.html      # macOS
    start index.html     # Windows
    xdg-open index.html  # Linux

---

## 📖 Utilisation

### Mode 1 — Backend Express (`server.js` + `indexLocalhost.html`)

1. Lance `npm start`
2. Ouvre `http://localhost:3000`
3. Saisis un `@username` (ex: `@khaby.lame`)
4. Clique sur **Analyser**

**Endpoint test** :

    curl http://localhost:3000/api/health
    curl http://localhost:3000/api/tiktok/khaby.lame

### Mode 2 — Single Page (`index.html`)

1. Ouvre directement `index.html` dans ton navigateur
2. Saisis un `@username`
3. Clique sur **Analyser**

> ⚠️ Le mode single-page utilise l'API oEmbed publique de TikTok — pas de followers/likes précis, mais fonctionne instantanément sans installation.

---

## 🛠️ Stack technique

| Couche | Technologie |
|---|---|
| **Frontend** | HTML5, CSS3 (Grid, Flexbox, variables CSS), JavaScript Vanilla |
| **Backend** | Node.js, Express 4.x |
| **HTTP Client** | Axios |
| **Parsing HTML** | Cheerio |
| **CORS** | Middleware `cors` |
| **Police** | Inter, Space Grotesk (Google Fonts) |
| **Icônes** | Font Awesome 6 |

**Dépendances (`package.json`)** :

    {
      "express": "^4.18.2",
      "axios": "^1.6.0",
      "cors": "^2.8.5",
      "cheerio": "^1.0.0-rc.12",
      "nodemon": "^3.0.1"
    }

---

## 📁 Structure du projet

    Analytics-seo-tiktok/
    ├── index.html              # Version single-page (sans backend)
    ├── indexLocalhost.html     # Version frontend connectée au backend
    ├── server.js               # Serveur Express + endpoint /api/tiktok/:username
    ├── package.json            # Dépendances et scripts npm
    ├── LICENSE                 # Licence MIT
    └── README.md               # Ce fichier

---

## 🔌 API Reference

### `GET /api/tiktok/:username`

Récupère les données publiques d'un utilisateur TikTok.

**Paramètres**

| Nom | Type | Description |
|---|---|---|
| `username` | `string` | Nom d'utilisateur TikTok (sans `@`) |

**Exemple**

    curl http://localhost:3000/api/tiktok/khaby.lame

**Réponse**

    {
      "success": true,
      "username": "khaby.lame",
      "nickname": "Khabane lame",
      "bio": "…",
      "verified": true,
      "followers": 162000000,
      "following": 0,
      "hearts": 2500000000,
      "videos": 1000,
      "engagementRate": "3.2",
      "seoScore": 85,
      "bioOptimization": 78,
      "accountStrength": "Très fort",
      "source": "real_tiktok_api"
    }

### `GET /api/health`

Vérifie que le serveur est opérationnel.

    { "status": "ok", "message": "TikTok Real Analytics API is running" }

---

## 🗺️ Roadmap

- [x] Dashboard SEO avec score visuel
- [x] Deux modes : backend + single-page
- [x] UI aux couleurs officielles TikTok
- [ ] Historique des analyses (localStorage / SQLite)
- [ ] Export PDF / CSV des rapports
- [ ] Intégration d'une API tierce (followers/likes réels)
- [ ] Comparaison multi-comptes
- [ ] Mode sombre / clair
- [ ] Internationalisation (FR / EN)

---

## 🤝 Contribution

Les contributions sont **les bienvenues** ! 🎉

    # 1. Fork le projet
    # 2. Crée ta branche
    git checkout -b feature/ma-super-feature

    # 3. Commit tes changements
    git commit -m "feat: ajout d'une super feature"

    # 4. Push
    git push origin feature/ma-super-feature

    # 5. Ouvre une Pull Request

**Conventions de commit** : [Conventional Commits](https://www.conventionalcommits.org/)

- `feat:` nouvelle fonctionnalité
- `fix:` correction de bug
- `docs:` documentation
- `style:` formatage
- `refactor:` refactoring
- `chore:` maintenance

---

## 📄 Licence

Distribué sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.

---

## 👤 Auteur

**Gleaphe** — *Gunout*

- GitHub : [@gunout](https://github.com/gunout)
- Projet : [Analytics-seo-tiktok](https://github.com/gunout/Analytics-seo-tiktok)

---

<div align="center">

### ⭐ Si ce projet t'a aidé, n'oublie pas de lui mettre une étoile !

**© 2026 Gleaphe — Tous droits réservés**

*Fait avec ❤️ et beaucoup de ☕*

</div>

---

# Analytics-seo-tiktok
TikTok IA Analytics - Analyses avancées &amp; Insights IA pour optimiser votre présence TikTok

# INSTALLATION SERVER.JS 

    npm install 

# DEMARRER LE SERVER.JS

    npm start

![t](https://github.com/user-attachments/assets/c8594976-842f-49b7-aeac-8d4b855ef44a)


# OPEN indexLocalhost.html on a webrowser 



<img width="1794" height="1246" alt="Screenshot 2026-03-30 at 16-35-32 TikTok Analytics Pro DONNÉES RÉELLES" src="https://github.com/user-attachments/assets/75cfa368-4473-4427-847d-ad01256eb2d6" />


---


By Gleaphe 2026 . 
