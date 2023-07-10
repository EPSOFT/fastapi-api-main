from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Stock(models.Model):
    """
    Define a new database model called Stock.
    """

    id = fields.IntField(pk=True)
    symbol = fields.CharField(max_length=20, unique=True, null=False)
    company = fields.CharField(max_length=50, null=False)
    stock_prices: fields.ReverseRelation["Stock_Price"]


class Stock_Price(models.Model):
    """
    This references a Stock_Price in a Stock
    """

    id = fields.IntField(pk=True)
    stock_id = fields.IntField(null=False)
    date = fields.DatetimeField(null=False)
    open = fields.FloatField(null=False)
    high = fields.FloatField(null=False)
    open = fields.FloatField(null=False)
    close = fields.FloatField(null=False)
    adjusted_close = fields.FloatField(null=False)
    volume = fields.IntField(null=False)

    # stock = fields.ForeignKeyField(
    #     "models.Stock",
    #     related_name="stock_prices",
    #     description="The stock this describe",
    # )


class TextSummary(models.Model):
    """
    Define a new database model called TextSummary.
    """

    url = fields.TextField()
    summary = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    sentiment = fields.TextField(null=True)
    positive_score = fields.DecimalField(max_digits=5, decimal_places=2, null=True)
    neutral_score = fields.DecimalField(max_digits=5, decimal_places=2, null=True)
    negative_score = fields.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return self.url


SummarySchema = pydantic_model_creator(TextSummary)
Stock_Pydantic = pydantic_model_creator(Stock)
Stock_Price_Pydantic = pydantic_model_creator(Stock_Price)
