# 🔗 Sniplink — URL Shortener

> Fast, free, and privacy-friendly URL shortener built with Flask and PostgreSQL.

[![Python](https://img.shields.io/badge/Python-3.12-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-000000?style=flat-square&logo=vercel&logoColor=white)](https://vercel.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-8b5cf6?style=flat-square)](LICENSE)

---

## ✨ Features

- **Shorten URLs** — Paste any long URL and get a clean, shareable short link
- **Instant Redirects** — Short links redirect to the original URL via 302
- **Click Tracking** — Every redirect increments a click counter
- **Stats API** — Query click count and creation date for any short link
- **Recent Links** — Dashboard shows the 10 most recently shortened URLs
- **Responsive Design** — Beautiful dark-mode UI that works on all devices
- **Production Ready** — Deployed on Vercel with PostgreSQL

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, Flask, Flask-CORS |
| **Database** | PostgreSQL (Vercel Postgres) / SQLite (local) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Hosting** | Vercel (Serverless Functions) |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/shorten` | Shorten a URL. Body: `{"url": "https://example.com"}` |
| `GET` | `/<short_code>` | Redirect to the original URL (302) |
| `GET` | `/api/stats/<code>` | Get click count and metadata |
| `GET` | `/api/recent` | Get 10 most recent shortened URLs |
| `GET` | `/api/health` | Health check |

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

> **Note**: Local development uses SQLite. No database setup required.

---

## 🌐 Deploy to Vercel

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Sniplink URL Shortener"
git remote add origin https://github.com/YOUR_USERNAME/CodeAlpha_URLShortener.git
git push -u origin main
```

### 2. Import to Vercel

1. Go to [vercel.com](https://vercel.com) and import your GitHub repository
2. Vercel auto-detects the `vercel.json` config — no settings to change

### 3. Add PostgreSQL Database

1. In your Vercel project dashboard, go to **Storage**
2. Click **Create Database** → **Postgres** (Neon)
3. Vercel automatically injects the `POSTGRES_URL` environment variable
4. **Redeploy** your project

Your URL shortener is now live! 🎉

---

## 📂 Project Structure

```
CodeAlpha_URLShortener/
├── api/
│   └── index.py          # Flask app (Vercel serverless entry point)
├── database.py            # Dual-mode DB (SQLite local / Postgres prod)
├── static/
│   ├── index.html         # Frontend SPA
│   ├── style.css          # Dark-mode glassmorphism styles
│   ├── script.js          # Frontend logic
│   └── favicon.svg        # Custom gradient favicon
├── vercel.json            # Vercel routing config
├── requirements.txt       # Python dependencies
├── .gitignore
├── LICENSE
└── README.md
```

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Syed** — Built as part of the [CodeAlpha](https://www.codealpha.tech) Backend Development Internship (2026).
