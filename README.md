# 🔗 Sniplink — URL Shortener

> Fast, free, and privacy-friendly URL shortener built with Flask and PostgreSQL. Designed for serverless deployment on Vercel.

[![Python](https://img.shields.io/badge/Python-3.12-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-000000?style=flat-square&logo=vercel&logoColor=white)](https://vercel.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-8b5cf6?style=flat-square)](LICENSE)

---

## ✨ Features

- **Shorten URLs** — Paste any long URL and get a clean, shareable short link instantly.
- **Instant Redirects** — Quick millisecond-level redirection (302) to original URLs.
- **Click Tracking** — Automatically increments a click counter for each redirect.
- **Stats API** — Query click metrics (total clicks, original URL, creation date) for any short link.
- **Privacy by Design** — "Recent Links" history is saved strictly in the user's browser via HTML5 `localStorage`. No data harvesting.
- **Clean Subpage Routing** — Serving clean, extension-less paths for Info Pages:
  - `/about` — App details, technical stack, and creator credentials.
  - `/privacy` — Clear, cookie-free data disclosure policy.
  - `/terms` — Acceptable use policies, disclaimers, and limitation of liability.
- **SEO Configurations** — Full search engine optimization utilizing `robots.txt` (to block crawler redirects and API paths) and `sitemap.xml` (for indexing page listings).
- **Responsive Dark-Mode UI** — Modern glassmorphism design with responsive grid layouts, SVG icons, and micro-animations.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, Flask, Flask-CORS |
| **Database** | PostgreSQL (Vercel Neon Postgres in production) / SQLite (local offline development) |
| **Frontend** | Vanilla HTML5, CSS3 (Custom Glassmorphism styling), Vanilla JavaScript |
| **Hosting** | Vercel (Serverless Functions) |

---

## 📂 Project Structure

```
CodeAlpha_URLShortener/
├── api/
│   └── index.py          # Flask backend API, routes, and clean redirect controllers
├── database.py            # Dual-mode database layer (auto-switches to PG on production env)
├── static/
│   ├── index.html         # Frontend homepage SPA
│   ├── about.html         # About page info layout
│   ├── privacy.html       # Privacy policy disclosure
│   ├── terms.html         # Terms of Service page
│   ├── style.css          # Dark-mode styling, responsive layouts, content page typography
│   ├── script.js          # API client, clipboard helpers, localStorage history managers
│   ├── favicon.svg        # Custom gradient favicon
│   ├── robots.txt         # SEO robot crawling specifications
│   └── sitemap.xml        # Search engine sitemap index
├── vercel.json            # Vercel serverless routing and request configurations
├── requirements.txt       # Python dependency declarations
├── .gitignore
├── LICENSE
└── README.md
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/shorten` | Shorten a URL. Body: `{"url": "https://example.com"}` |
| `GET` | `/<short_code>` | Redirect to the original URL (302) |
| `GET` | `/api/stats/<code>` | Retrieve click count and creation timestamp |
| `GET` | `/api/health` | Service and database health checks |

### Example Request

```bash
curl -X POST https://your-app.vercel.app/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/trending"}'
```

### Example Response

```json
{
  "short_url": "https://your-app.vercel.app/aB3xK9",
  "short_code": "aB3xK9",
  "original_url": "https://github.com/trending"
}
```

---

## 🚀 Local Development

### Prerequisites

- Python 3.10+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/CodeAlpha_URLShortener.git
cd CodeAlpha_URLShortener

# Install dependencies
pip install -r requirements.txt

# Run the development server
python api/index.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

> **Note**: Local development defaults to a local SQLite database file (`url_shortener.db`). No database server setup required.

---

## 🌐 Production Deployment (Vercel)

### 1. Link to GitHub
Push your local code to your GitHub repository:
```bash
git init
git add .
git commit -m "Initial commit: Sniplink URL Shortener"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/CodeAlpha_URLShortener.git
git push -u origin main
```

### 2. Import in Vercel
1. Sign in to your [vercel.com](https://vercel.com) dashboard.
2. Select **Add New** → **Project**, and import your repository.
3. Vercel automatically reads `vercel.json` and configures the build steps.

### 3. Connect Postgres Storage
1. From your Vercel project dashboard, go to the **Storage** tab.
2. Under marketplace providers, click **Create Database** next to **Neon (Serverless Postgres)**.
3. Keep the default settings (standard `STORAGE_URL` prefix) and click **Connect**.
4. Go back to the **Deployments** tab and select **Redeploy**.
5. The backend automatically detects the Postgres database and is ready to use!

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Syed**  
*Backend Development Intern (2026) at CodeAlpha*  
* [GitHub Profile](https://github.com/Syedx2)  
* [LinkedIn Profile](https://www.linkedin.com/in/syed-abdul-raheem-7bb8453a9)  
* Email: [syeds.devs@gmail.com](mailto:syeds.devs@gmail.com)
