from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.CharField(pk=True, max_length=64)
    email = fields.CharField(max_length=255, unique=True)
    name = fields.CharField(max_length=120)
    role = fields.CharField(max_length=32, default="operator")

    class Meta:
        table = "users"


class Shift(Model):
    id = fields.CharField(pk=True, max_length=64)
    name = fields.CharField(max_length=80)
    starts_at = fields.DatetimeField()
    ends_at = fields.DatetimeField()
    supervisor = fields.CharField(max_length=120)

    class Meta:
        table = "shifts"


class Machine(Model):
    id = fields.CharField(pk=True, max_length=64)
    line_code = fields.CharField(max_length=40, index=True)
    name = fields.CharField(max_length=120)

    class Meta:
        table = "machines"


class AlertEvent(Model):
    id = fields.CharField(pk=True, max_length=64)
    time = fields.DatetimeField(index=True)
    machine = fields.ForeignKeyField("models.Machine", related_name="alerts")
    severity = fields.CharField(max_length=24, index=True)
    code = fields.CharField(max_length=80)
    message = fields.TextField()

    class Meta:
        table = "alert_events"


class HandoffCard(Model):
    id = fields.CharField(pk=True, max_length=64)
    shift = fields.ForeignKeyField("models.Shift", related_name="cards")
    machine = fields.ForeignKeyField("models.Machine", related_name="cards")
    priority = fields.CharField(max_length=24, index=True)
    status = fields.CharField(max_length=24, index=True)
    assignee = fields.CharField(max_length=120)
    title = fields.CharField(max_length=200)
    next_action = fields.TextField()
    opened_at = fields.DatetimeField()

    class Meta:
        table = "handoff_cards"


class CardAction(Model):
    id = fields.CharField(pk=True, max_length=64)
    card = fields.ForeignKeyField("models.HandoffCard", related_name="actions")
    actor = fields.CharField(max_length=120)
    action = fields.CharField(max_length=80)
    memo = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "card_actions"


class Assignment(Model):
    id = fields.CharField(pk=True, max_length=64)
    card = fields.ForeignKeyField("models.HandoffCard", related_name="assignments")
    assignee = fields.ForeignKeyField("models.User", related_name="assignments")
    assigned_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "assignments"
