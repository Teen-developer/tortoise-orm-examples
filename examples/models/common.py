import tortoise.fields
from tortoise import Model


class User(Model):
    id = tortoise.fields.IntField(pk=True)
    name = tortoise.fields.CharField(max_length=64, default="John")
    surname = tortoise.fields.CharField(max_length=64, default="Doe")
    age = tortoise.fields.IntField()
    balanceUSD = tortoise.fields.FloatField(default=0)

    def __str__(self):
        return f"<User: {self.id}>"