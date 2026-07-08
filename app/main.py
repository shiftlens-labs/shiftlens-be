from flask import Flask
from flask_cors import CORS

from app.modules.alerts.routes import alerts_bp
from app.modules.auth.routes import auth_bp
from app.modules.handoff.routes import handoff_bp
from app.modules.shifts.routes import shifts_bp


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(shifts_bp, url_prefix="/api/v1/shifts")
    app.register_blueprint(handoff_bp, url_prefix="/api/v1/handoff-cards")
    app.register_blueprint(alerts_bp, url_prefix="/api/v1/alerts")

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "shiftlens-be"}

    return app


app = create_app()
