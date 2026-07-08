from app.main import create_app
from app.modules.repository import normalize_severity


def test_health():
    client = create_app().test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_card_status_transition():
    client = create_app().test_client()
    response = client.patch("/api/v1/handoff-cards/card-press-07", json={"status": "acknowledged"})
    assert response.status_code == 200
    assert response.json["status"] == "acknowledged"


def test_alert_ingest_creates_context():
    client = create_app().test_client()
    response = client.post(
        "/api/v1/alerts/ingest",
        json={
            "machineId": "m-robot-02",
            "lineCode": "WELD-1",
            "machineName": "Welding Robot 02",
            "severity": "sev1",
            "code": "ARC_FLASH_RISK",
            "message": "Vision model detected shield gap",
        },
    )
    assert response.status_code == 201
    assert response.json["alert"]["severity"] == "critical"
    assert response.json["handoffCard"]["status"] == "open"


def test_alert_normalization():
    assert normalize_severity("warning") == "high"
    assert normalize_severity("unknown") == "medium"


def test_handoff_action_updates_card_status():
    client = create_app().test_client()
    response = client.post(
        "/api/v1/handoff-cards/card-press-07/actions",
        json={"actor": "pytest", "action": "handoff", "memo": "next shift accepted", "status": "resolved"},
    )
    assert response.status_code == 201
    assert response.json["action"] == "handoff"

    card = client.get("/api/v1/handoff-cards/card-press-07")
    assert card.status_code == 200
    assert card.json["status"] == "resolved"
