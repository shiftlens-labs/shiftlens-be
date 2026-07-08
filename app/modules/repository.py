from copy import deepcopy

from app.modules.common import now_iso, new_id


class MemoryRepository:
    def __init__(self):
        self.shift = {
            "id": "shift-night-20260708",
            "name": "Night B",
            "startsAt": "2026-07-08T20:00:00+09:00",
            "endsAt": "2026-07-09T08:00:00+09:00",
            "supervisor": "Mina Park",
        }
        self.alerts = [
            {
                "id": "evt-101",
                "occurredAt": "2026-07-08T21:12:00+09:00",
                "machine": {"id": "m-press-07", "lineCode": "PRESS-2", "name": "Hydraulic Press 07"},
                "severity": "critical",
                "code": "SAFE_GUARD_OPEN",
                "message": "Safety guard opened during pressure cycle",
            }
        ]
        self.cards = [
            {
                "id": "card-press-07",
                "shiftId": self.shift["id"],
                "machine": {"id": "m-press-07", "lineCode": "PRESS-2", "name": "Hydraulic Press 07"},
                "priority": "critical",
                "status": "open",
                "assignee": "Joon Choi",
                "title": "Guard interlock needs physical re-check",
                "nextAction": "Keep line paused until maintenance signs off on guard sensor.",
                "openedAt": "2026-07-08T21:13:00+09:00",
                "sourceAlerts": deepcopy(self.alerts),
                "actions": [
                    {
                        "id": "act-1",
                        "actor": "A-shift operator",
                        "action": "temporary_hold",
                        "memo": "Stopped PRESS-2 and tagged panel. Sensor flickered twice after reset.",
                        "createdAt": "2026-07-08T21:19:00+09:00",
                    }
                ],
            }
        ]

    def current_shift(self):
        return deepcopy(self.shift)

    def list_alerts(self):
        return deepcopy(self.alerts)

    def list_cards(self, status=None, shift_id=None):
        cards = self.cards
        if status:
            cards = [card for card in cards if card["status"] == status]
        if shift_id:
            cards = [card for card in cards if card["shiftId"] == shift_id]
        return deepcopy(cards)

    def get_card(self, card_id):
        return deepcopy(next((card for card in self.cards if card["id"] == card_id), None))

    def update_card(self, card_id, patch):
        for card in self.cards:
            if card["id"] == card_id:
                for key in ("status", "assignee", "nextAction"):
                    if key in patch:
                        card[key] = patch[key]
                return deepcopy(card)
        return None

    def add_action(self, card_id, payload):
        for card in self.cards:
            if card["id"] == card_id:
                action = {
                    "id": new_id("act"),
                    "actor": payload.get("actor", "operator"),
                    "action": payload.get("action", "note"),
                    "memo": payload.get("memo", ""),
                    "createdAt": now_iso(),
                }
                card["actions"].append(action)
                if payload.get("status"):
                    card["status"] = payload["status"]
                return deepcopy(action)
        return None

    def ingest_alert(self, payload):
        severity = normalize_severity(payload.get("severity", "medium"))
        machine = payload.get("machine") or {
            "id": payload.get("machineId", "m-unknown"),
            "lineCode": payload.get("lineCode", "UNKNOWN"),
            "name": payload.get("machineName", "Unknown machine"),
        }
        alert = {
            "id": new_id("evt"),
            "occurredAt": payload.get("occurredAt", now_iso()),
            "machine": machine,
            "severity": severity,
            "code": payload.get("code", "UNKNOWN_ALERT"),
            "message": payload.get("message", "No message supplied"),
        }
        self.alerts.insert(0, alert)
        card = self._upsert_card_for_alert(alert)
        return {"alert": deepcopy(alert), "handoffCard": deepcopy(card)}

    def _upsert_card_for_alert(self, alert):
        match = next(
            (card for card in self.cards if card["machine"]["id"] == alert["machine"]["id"] and card["status"] != "resolved"),
            None,
        )
        if match:
            match["sourceAlerts"].insert(0, alert)
            if priority_rank(alert["severity"]) > priority_rank(match["priority"]):
                match["priority"] = alert["severity"]
            return match

        card = {
            "id": new_id("card"),
            "shiftId": self.shift["id"],
            "machine": alert["machine"],
            "priority": alert["severity"],
            "status": "open",
            "assignee": "unassigned",
            "title": f"{alert['code']} on {alert['machine']['lineCode']}",
            "nextAction": "Review source alert and assign an operator.",
            "openedAt": now_iso(),
            "sourceAlerts": [alert],
            "actions": [],
        }
        self.cards.insert(0, card)
        return card


def normalize_severity(value):
    value = str(value).lower()
    if value in {"critical", "high", "medium"}:
        return value
    if value in {"p1", "sev1", "danger"}:
        return "critical"
    if value in {"p2", "sev2", "warning"}:
        return "high"
    return "medium"


def priority_rank(severity):
    return {"medium": 1, "high": 2, "critical": 3}.get(severity, 1)


repo = MemoryRepository()
