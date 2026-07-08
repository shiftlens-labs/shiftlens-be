from datetime import datetime
from uuid import uuid4


def now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def new_id(prefix):
    return f"{prefix}-{uuid4().hex[:10]}"
