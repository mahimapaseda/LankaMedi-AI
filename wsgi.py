"""Production WSGI entry point for LankaMedi AI."""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()

