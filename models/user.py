from tortoise import fields, models

class User(models.Model):
    id = fields.IntField(pk=True)
    chat_id = fields.BigIntField()
    first_name = fields.CharField(max_length=255)
    lang = fields.CharField(max_length=5)

    # phone = fields.BigIntField(null=True)
    is_premium = fields.BooleanField(default=False, null=True)
    is_admin = fields.BooleanField(default=False, null=True)

    class Meta:
        table = "user"
