from flask import Blueprint, request

from app.modules.repository import repo

alerts_bp = Blueprint("alerts", __name__)


@alerts_bp.get("")
def list_alerts():
    return repo.list_alerts()


@alerts_bp.post("/ingest")
def ingest_alert():
    payload = request.get_json(silent=True) or {}
    if not payload.get("code"):
        return {"error": "code_required"}, 400
    return repo.ingest_alert(payload), 201
