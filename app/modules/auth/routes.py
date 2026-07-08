from flask import Blueprint, request

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/signin")
def signin():
    payload = request.get_json(silent=True) or {}
    return {
        "user": {
            "id": "user-demo",
            "email": payload.get("email", "operator@shiftlens.local"),
            "name": "Demo Operator",
            "role": "operator",
        },
        "accessToken": "demo-access-token",
    }


@auth_bp.post("/refresh")
def refresh():
    return {"accessToken": "demo-access-token"}


@auth_bp.post("/logout")
def logout():
    return {"ok": True}
