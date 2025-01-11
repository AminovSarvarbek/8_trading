from tortoise import fields, models

class Channel(models.Model):
    id = fields.IntField(pk=True)
    chat_id = fields.BigIntField()

    class Meta:
        table = "channel"
