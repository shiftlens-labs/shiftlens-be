from flask import Blueprint, request

from app.modules.repository import repo

handoff_bp = Blueprint("handoff", __name__)


@handoff_bp.get("")
def list_cards():
    return repo.list_cards(status=request.args.get("status"), shift_id=request.args.get("shiftId"))


@handoff_bp.get("/<card_id>")
def get_card(card_id):
    card = repo.get_card(card_id)
    if not card:
        return {"error": "card_not_found"}, 404
    return card


@handoff_bp.patch("/<card_id>")
def update_card(card_id):
    card = repo.update_card(card_id, request.get_json(silent=True) or {})
    if not card:
        return {"error": "card_not_found"}, 404
    return card


@handoff_bp.post("/<card_id>/actions")
def add_action(card_id):
    action = repo.add_action(card_id, request.get_json(silent=True) or {})
    if not action:
        return {"error": "card_not_found"}, 404
    return action, 201
