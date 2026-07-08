from app.modules.common import now_iso


def audit_event(event, **fields):
    return {"event": event, "createdAt": now_iso(), **fields}
