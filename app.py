"""LankaMedi AI — Flask Application Factory and Server Entry Point."""

from flask import Flask
from core.config import Config
from routes.api import api_bp, analyze_report
from routes.web import web_bp


def create_app(config_class=Config) -> Flask:
    """Application factory for LankaMedi AI."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register modular blueprints
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)

    # Backward-compatible legacy route alias for existing scripts and integrations
    app.add_url_rule("/analyze", "legacy_analyze", analyze_report, methods=["POST"])

    return app


# Module-level instance for WSGI servers and Vercel serverless deployment
app = create_app()

if __name__ == "__main__":
    app.run(
        debug=Config.DEBUG,
        port=Config.PORT,
        host="0.0.0.0",
    )
