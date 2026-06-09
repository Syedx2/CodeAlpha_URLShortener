"""
Sniplink — URL Shortener API
Flask application configured for Vercel serverless deployment.
Locally runs with SQLite; in production uses Vercel Postgres.
"""

import os
import sys
import string
import random
from urllib.parse import urlparse

from flask import Flask, request, jsonify, redirect, send_from_directory, abort
from flask_cors import CORS

# Add parent directory to path so we can import database module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import database

# ---------------------------------------------------------------------------
# App Setup
# ---------------------------------------------------------------------------

STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/static")
CORS(app)

SHORT_CODE_LENGTH = 6
CHARACTERS = string.ascii_letters + string.digits  # a-z A-Z 0-9

# Initialize database on cold start
database.init_db()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def generate_short_code(length: int = SHORT_CODE_LENGTH) -> str:
    """Generate a random alphanumeric short code."""
    return "".join(random.choices(CHARACTERS, k=length))


def is_valid_url(url: str) -> bool:
    """Basic URL validation — must have a scheme and a network location."""
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# Routes — Frontend
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Serve the frontend SPA."""
    return send_from_directory(STATIC_DIR, "index.html")


@app.route("/favicon.svg")
def favicon():
    """Serve the favicon."""
    return send_from_directory(STATIC_DIR, "favicon.svg")


# ---------------------------------------------------------------------------
# Routes — API
# ---------------------------------------------------------------------------

@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    """
    Accept a JSON body with { "url": "<long_url>" }.
    Returns the generated short URL and short code.
    """
    data = request.get_json(silent=True)
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' field in request body."}), 400

    original_url = data["url"].strip()

    # Auto-add https:// if no scheme is provided
    if not original_url.startswith(("http://", "https://")):
        original_url = "https://" + original_url

    if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL. Please provide a valid HTTP/HTTPS URL."}), 400

    # Generate a unique short code (retry on collision)
    max_retries = 10
    for _ in range(max_retries):
        short_code = generate_short_code()
        if database.save_url(short_code, original_url):
            break
    else:
        return jsonify({"error": "Could not generate a unique short code. Please try again."}), 500

    # Build the full short URL
    base_url = request.host_url.rstrip("/")
    short_url = f"{base_url}/{short_code}"

    return jsonify({
        "short_url": short_url,
        "short_code": short_code,
        "original_url": original_url,
    }), 201


@app.route("/api/stats/<short_code>", methods=["GET"])
def url_stats(short_code):
    """Return click count and metadata for a given short code."""
    stats = database.get_stats(short_code)
    if not stats:
        return jsonify({"error": "Short code not found."}), 404
    return jsonify(stats)


@app.route("/api/recent", methods=["GET"])
def recent_urls():
    """Return the 10 most recently shortened URLs."""
    urls = database.get_recent_urls(limit=10)
    return jsonify(urls)


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        "status": "healthy",
        "service": "sniplink",
        "database": "postgres" if database.USE_POSTGRES else "sqlite",
    })


# ---------------------------------------------------------------------------
# Routes — Redirect
# ---------------------------------------------------------------------------

@app.route("/<short_code>")
def redirect_to_url(short_code):
    """Look up the short code and redirect (302) to the original URL."""
    # Skip common static file requests
    if short_code in ("favicon.ico", "robots.txt", "sitemap.xml"):
        abort(404)

    original_url = database.get_url(short_code)
    if not original_url:
        return jsonify({"error": "Short URL not found."}), 404

    database.increment_clicks(short_code)
    return redirect(original_url, code=302)


# ---------------------------------------------------------------------------
# Error Handlers
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    """Custom 404 handler."""
    if request.path.startswith("/api/"):
        return jsonify({"error": "Endpoint not found."}), 404
    return send_from_directory(STATIC_DIR, "index.html"), 404


@app.errorhandler(500)
def internal_error(e):
    """Custom 500 handler."""
    return jsonify({"error": "Internal server error. Please try again later."}), 500


# ---------------------------------------------------------------------------
# Entry Point (local development)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n  >> Sniplink running at http://localhost:5000\n")
    app.run(debug=True, port=5000)
