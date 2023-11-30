from django.db import models

class Pricebook(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    devicename = models.CharField(blank=True, null=True)
    unitprice = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sfid = models.CharField(blank=True, null=True)
    pricebook2id = models.TextField(blank=True, null=True)  # This field type is a guess.
    product2id = models.CharField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pricebook'
