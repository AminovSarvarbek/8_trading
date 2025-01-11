from tortoise import fields, models

class Crypto(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=10)
    symbol = fields.CharField(max_length=10)
    is_premium = fields.BooleanField(default=False)

    class Meta:
        table = "crypto"
