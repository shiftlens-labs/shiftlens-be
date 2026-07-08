from flask import Blueprint

from app.modules.repository import repo

shifts_bp = Blueprint("shifts", __name__)


@shifts_bp.get("/current")
def current_shift():
    return repo.current_shift()
