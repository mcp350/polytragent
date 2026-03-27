import os
import base64
import mimetypes
from pathlib import Path
from flask import Flask, send_file, send_from_directory, abort, request, Response

app = Flask(__name__, static_folder=None)

BASE_DIR = Path(__file__).parent

# Admin Basic Auth credentials — set via environment variables on Railway
ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "changeme")


def check_basic_auth():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Basic "):
        return False
    try:
        decoded = base64.b64decode(auth[6:]).decode("utf-8")
        username, password = decoded.split(":", 1)
        return username == ADMIN_USER and password == ADMIN_PASS
    except Exception:
        return False


def require_basic_auth():
    return Response(
        "Unauthorized",
        401,
        {"WWW-Authenticate": 'Basic realm="Admin"'},
    )


@app.route("/")
def index():
    return send_file(BASE_DIR / "index.html")


@app.route("/admin")
@app.route("/admin/")
def admin():
    if not check_basic_auth():
        return require_basic_auth()
    # Admin dashboard placeholder — extend as needed
    return Response(
        """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Polytragent Admin</title>
  <style>
    body { background: #0a0a0a; color: #6ee7b7; font-family: 'JetBrains Mono', monospace; padding: 40px; }
    h1 { font-size: 1.5rem; margin-bottom: 1rem; }
    p { color: #888; }
  </style>
</head>
<body>
  <h1>$ polytragent admin</h1>
  <p>Dashboard loaded successfully.</p>
</body>
</html>""",
        200,
        {"Content-Type": "text/html"},
    )


@app.route("/features")
@app.route("/features/")
def features_index():
    return send_file(BASE_DIR / "features" / "index.html")


@app.route("/features/<path:filename>")
def features_file(filename):
    # Support clean URLs: /features/edge-detection -> features/edge-detection.html
    filepath = BASE_DIR / "features" / filename
    if filepath.is_file():
        return send_file(filepath)
    html_path = BASE_DIR / "features" / (filename + ".html")
    if html_path.is_file():
        return send_file(html_path)
    abort(404)


@app.route("/blog")
@app.route("/blog/")
def blog_index():
    return send_file(BASE_DIR / "blog" / "index.html")


@app.route("/blog/<path:filename>")
def blog_file(filename):
    filepath = BASE_DIR / "blog" / filename
    if filepath.is_file():
        return send_file(filepath)
    html_path = BASE_DIR / "blog" / (filename + ".html")
    if html_path.is_file():
        return send_file(html_path)
    abort(404)


@app.route("/compare")
@app.route("/compare/")
def compare_index():
    return send_file(BASE_DIR / "compare" / "index.html")


@app.route("/compare/<path:filename>")
def compare_file(filename):
    filepath = BASE_DIR / "compare" / filename
    if filepath.is_file():
        return send_file(filepath)
    html_path = BASE_DIR / "compare" / (filename + ".html")
    if html_path.is_file():
        return send_file(html_path)
    abort(404)


@app.route("/resources")
@app.route("/resources/")
def resources_index():
    return send_file(BASE_DIR / "resources" / "index.html")


@app.route("/resources/<path:filename>")
def resources_file(filename):
    filepath = BASE_DIR / "resources" / filename
    if filepath.is_file():
        return send_file(filepath)
    html_path = BASE_DIR / "resources" / (filename + ".html")
    if html_path.is_file():
        return send_file(html_path)
    abort(404)


@app.route("/features.html")
def features_html():
    return send_file(BASE_DIR / "features.html")


@app.route("/robots.txt")
def robots():
    return send_file(BASE_DIR / "robots.txt")


@app.route("/sitemap.xml")
def sitemap():
    return send_file(BASE_DIR / "sitemap.xml")


@app.route("/<path:filename>")
def static_files(filename):
    filepath = BASE_DIR / filename
    if filepath.is_file():
        return send_file(filepath)
    # Try appending .html for clean URLs
    html_path = BASE_DIR / (filename + ".html")
    if html_path.is_file():
        return send_file(html_path)
    abort(404)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
