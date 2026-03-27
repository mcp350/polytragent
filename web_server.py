import os
from datetime import timedelta
from pathlib import Path

from flask import Flask, abort, send_file

from models import db

BASE_DIR = Path(__file__).parent

app = Flask(__name__, static_folder=None, template_folder=str(BASE_DIR / "templates"))

# ── Database ──────────────────────────────────────────────────────────────────
database_url = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR}/polytragent.db")
# Railway Postgres URLs start with postgres:// — SQLAlchemy needs postgresql://
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "polytragent-admin-secret-change-me")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)

db.init_app(app)


@app.context_processor
def inject_now():
    from datetime import datetime
    return {"now": datetime.utcnow()}


# ── Admin blueprint ───────────────────────────────────────────────────────────
from admin_routes import admin_bp  # noqa: E402

app.register_blueprint(admin_bp)

# ── Create tables on startup ──────────────────────────────────────────────────
with app.app_context():
    db.create_all()


# ── Marketing site routes ─────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_file(BASE_DIR / "index.html")


@app.route("/features")
@app.route("/features/")
def features_index():
    return send_file(BASE_DIR / "features" / "index.html")


@app.route("/features/<path:filename>")
def features_file(filename):
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
    html_path = BASE_DIR / (filename + ".html")
    if html_path.is_file():
        return send_file(html_path)
    abort(404)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
