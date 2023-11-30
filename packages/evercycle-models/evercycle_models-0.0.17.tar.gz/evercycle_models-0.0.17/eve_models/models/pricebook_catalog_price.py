from django.db import models
from .pricebook_catalog import PricebookCatalog

class PricebookCatalogPrice(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    timestamp = models.DateTimeField(blank=True, null=True)
    pricebook_catalog = models.ForeignKey(PricebookCatalog, models.DO_NOTHING)
    grade_price = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'pricebook_catalog_price'
