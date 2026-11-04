"""Web interface routes."""

import os
from flask import Blueprint, render_template, send_from_directory, current_app, make_response
from core.config import Config
from core.constants import SRI_LANKA_EMERGENCY_CONTACTS

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    """Renders the main LankaMedi AI interface."""
    return render_template(
        "index.html",
        active_providers=Config.get_active_providers(),
        emergency_contacts=SRI_LANKA_EMERGENCY_CONTACTS,
    )


@web_bp.route("/manifest.json")
@web_bp.route("/manifest.webmanifest")
def pwa_manifest():
    """Serves the PWA web app manifest with correct MIME type."""
    response = make_response(
        send_from_directory(
            os.path.join(current_app.root_path, "static"),
            "manifest.json",
            mimetype="application/manifest+json"
        )
    )
    response.headers["Cache-Control"] = "public, max-age=86400"
    return response


@web_bp.route("/sw.js")
def service_worker():
    """Serves the Service Worker at root scope with Service-Worker-Allowed header."""
    response = make_response(
        send_from_directory(
            os.path.join(current_app.root_path, "static"),
            "sw.js",
            mimetype="application/javascript; charset=utf-8"
        )
    )
    # Required for Service Worker to control entire domain scope "/"
    response.headers["Service-Worker-Allowed"] = "/"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response
